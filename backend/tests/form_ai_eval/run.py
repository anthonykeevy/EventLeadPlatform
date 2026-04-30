"""Story 6.4.3a Form AI eval harness runner.

This module intentionally keeps the harness under backend/tests so prompt
experiments can evolve without creating a production API surface. It calls the
existing Form AI generation service unless --mock is supplied for deterministic
smoke runs and unit tests.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence

from sqlalchemy import text

BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from modules.form_ai.schemas import (  # noqa: E402
    AttemptTraceEntry,
    AttemptValidationSummary,
    FormAiGenerateResponse,
    GenerationTraceMetadata,
)
from modules.form_ai.service import generate_form_definition  # noqa: E402
from form_ai_eval import au_diagnostics  # type: ignore[import-not-found]  # noqa: E402


BENCHMARK_SET_VERSION = "prompts-v1.1"
AU_BENCHMARK_SET_VERSION = "prompts-au-v1"
DEFAULT_PROMPTS_PATH = Path(__file__).with_name("prompts.yaml")
DEFAULT_AU_PROMPTS_PATH = Path(__file__).with_name("prompts_au_v1.yaml")
DEFAULT_OUTPUT_ROOT = Path("_bmad-output") / "eval-runs"
MAX_CONCURRENCY = 4
MAX_PROVIDER_RETRIES = 3
PROMPT_SHRINK_MODE_ENV = "FORM_AI_EVAL_PROMPT_SHRINK_MODE"
PROMPT_SHRINK_MODES = ("baseline", "h2", "h4", "h2-h4")
CATEGORY_A_FIELDS = [
    "schema_valid",
    "component_count",
    "collision_count",
    "boundary_violation_count",
    "attempt_count",
    "terminal_reason",
    "failure_class",
    "duration_ms",
    "input_tokens",
    "output_tokens",
    "total_cost_usd",
    "retry_count",
]


@dataclass(frozen=True)
class BenchmarkPrompt:
    prompt_id: str
    category: str
    variant: str
    audience_locale: str
    repetition_index: int
    prompt: str
    metadata: Dict[str, Any]
    runtime_context: Dict[str, Any]
    expected_signals: Dict[str, Any]
    llm_judge_focus: Dict[str, Any]
    expected_structural_checks: List[str]


@dataclass(frozen=True)
class PromptSet:
    benchmark_set_version: str
    prompts: List[BenchmarkPrompt]


@dataclass(frozen=True)
class EvalTask:
    sequence: int
    prompt: BenchmarkPrompt
    repetition_index: int
    key: str


@dataclass(frozen=True)
class EvalTaskResult:
    task: EvalTask
    row: Dict[str, Any]
    response: FormAiGenerateResponse
    metrics: Dict[str, Any]


class EvalHarnessError(RuntimeError):
    """Raised for harness configuration or validation failures."""


def _infer_prompt_shrink_mode(variant: str) -> str:
    """Map Story 6.4.4.2 run labels to explicit prompt candidate state."""
    normalised = variant.strip().lower()
    if "h2-h4" in normalised:
        return "h2-h4"
    if "h2" in normalised and "consent" in normalised:
        return "h2"
    if "h4" in normalised and ("operational" in normalised or "trim" in normalised):
        return "h4"
    if "baseline-no-shrink" in normalised:
        return "baseline"
    # Current master includes both carried-forward candidates unless overridden.
    return "h2-h4"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _hash_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _read_prompt_payload(path: Path) -> Dict[str, Any]:
    """Load the frozen prompt set.

    The file is JSON-shaped YAML. This keeps the artifact valid YAML while
    avoiding a PyYAML dependency in the backend test environment.
    """

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EvalHarnessError(
            f"{path} must remain JSON-shaped YAML for dependency-free loading: {exc}"
        ) from exc


def load_prompt_set(path: Path = DEFAULT_PROMPTS_PATH) -> PromptSet:
    payload = _read_prompt_payload(path)
    version = payload.get("benchmark_set_version")
    prompts_raw = payload.get("prompts")
    if version not in {BENCHMARK_SET_VERSION, AU_BENCHMARK_SET_VERSION}:
        raise EvalHarnessError(
            f"Expected benchmark_set_version in "
            f"{sorted({BENCHMARK_SET_VERSION, AU_BENCHMARK_SET_VERSION})!r}; got {version!r}"
        )
    if not isinstance(prompts_raw, list):
        raise EvalHarnessError("prompt file must contain a prompts list")
    if version == BENCHMARK_SET_VERSION and len(prompts_raw) != 270:
        raise EvalHarnessError("prompts.yaml must contain exactly 270 prompt rows")
    if version == AU_BENCHMARK_SET_VERSION and not prompts_raw:
        raise EvalHarnessError("prompts_au_v1.yaml must contain at least one AU prompt row")

    prompts: List[BenchmarkPrompt] = []
    seen_ids: set[str] = set()
    required = {
        "prompt_id",
        "category",
        "variant",
        "audience_locale",
        "repetition_index",
        "prompt",
        "metadata",
        "runtimeContext",
        "expected_signals",
        "llm_judge_focus",
        "expectedStructuralChecks",
    }
    for index, row in enumerate(prompts_raw, start=1):
        if not isinstance(row, dict):
            raise EvalHarnessError(f"Prompt row {index} must be an object")
        missing = sorted(required - set(row))
        if missing:
            raise EvalHarnessError(f"Prompt row {index} missing required fields: {missing}")
        prompt_id = row["prompt_id"]
        if not isinstance(prompt_id, str) or not prompt_id:
            raise EvalHarnessError(f"Prompt row {index} has invalid prompt_id")
        if prompt_id in seen_ids:
            raise EvalHarnessError(f"Duplicate prompt_id: {prompt_id}")
        seen_ids.add(prompt_id)

        runtime_context = row["runtimeContext"]
        if not isinstance(runtime_context, dict):
            raise EvalHarnessError(f"{prompt_id} runtimeContext must be an object")
        if runtime_context.get("audienceLocale") != row["audience_locale"]:
            raise EvalHarnessError(f"{prompt_id} runtimeContext.audienceLocale must match row audience_locale")
        if version == AU_BENCHMARK_SET_VERSION and str(row["audience_locale"]).upper() != "AU":
            raise EvalHarnessError(f"{prompt_id} must be AU for {AU_BENCHMARK_SET_VERSION}")
        metadata = dict(row["metadata"])
        if version == AU_BENCHMARK_SET_VERSION:
            if metadata.get("schema") != AU_BENCHMARK_SET_VERSION:
                raise EvalHarnessError(f"{prompt_id} metadata.schema must be {AU_BENCHMARK_SET_VERSION}")
            if "source_market_adaptation" not in metadata:
                raise EvalHarnessError(
                    f"{prompt_id} metadata.source_market_adaptation is required for AU diagnostics"
                )
        if not isinstance(runtime_context.get("canvas"), dict):
            raise EvalHarnessError(f"{prompt_id} runtimeContext.canvas is required")
        if not isinstance(runtime_context.get("termsDefaults"), dict):
            raise EvalHarnessError(f"{prompt_id} runtimeContext.termsDefaults is required")
        capability_snapshot = runtime_context.get("capabilitySnapshot")
        if not isinstance(capability_snapshot, dict) or not capability_snapshot.get("version"):
            raise EvalHarnessError(
                f"{prompt_id} runtimeContext.capabilitySnapshot.version is required"
            )

        prompts.append(
            BenchmarkPrompt(
                prompt_id=prompt_id,
                category=row["category"],
                variant=row["variant"],
                audience_locale=row["audience_locale"],
                repetition_index=int(row["repetition_index"]),
                prompt=row["prompt"],
                metadata=metadata,
                runtime_context=runtime_context,
                expected_signals=dict(row["expected_signals"]),
                llm_judge_focus=dict(row["llm_judge_focus"]),
                expected_structural_checks=list(row["expectedStructuralChecks"]),
            )
        )

    return PromptSet(benchmark_set_version=version, prompts=prompts)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Form AI eval harness.")
    parser.add_argument("--variant", default="baseline")
    parser.add_argument("--hypothesis-code", default="baseline")
    parser.add_argument("--variant-label", default="current-master-baseline")
    parser.add_argument("--prompt-id", action="append", default=[])
    parser.add_argument(
        "--locale-filter",
        type=str,
        default=None,
        help="Run only rows whose audience_locale matches the given ISO/locale (e.g. AU). Defaults to all rows.",
    )
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--concurrency", type=int, default=MAX_CONCURRENCY)
    parser.add_argument("--max-cost-usd", type=float, default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--prompts-path", type=Path, default=DEFAULT_PROMPTS_PATH)
    parser.add_argument(
        "--allow-au-context-conflicts",
        action="store_true",
        help="Record but do not fail blocking AU prompt-context lint findings.",
    )
    parser.add_argument("--resume", type=Path, default=None, help="Path to checkpoint.json")
    parser.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="Allow writing to a non-empty run folder without --resume.",
    )
    parser.add_argument("--persist-db", action="store_true")
    parser.add_argument("--mock", action="store_true", help="Use deterministic local responses")
    parser.add_argument("--model", default=None)
    parser.add_argument("--openai-transport", choices=["auto", "sync", "stream"], default="auto")
    parser.add_argument(
        "--system-prompt-addendum",
        default=None,
        help="Eval-only system prompt addendum. Recorded in run artifacts; does not change production prompt state.",
    )
    parser.add_argument(
        "--system-prompt-addendum-file",
        type=Path,
        default=None,
        help="File containing an eval-only system prompt addendum.",
    )
    parser.add_argument(
        "--prompt-shrink-mode",
        choices=PROMPT_SHRINK_MODES,
        default=None,
        help=(
            "Eval-only prompt state: baseline disables H2/H4, h2 enables only "
            "the compact consent table, h4 enables only the operational-notes trim, "
            "h2-h4 enables both."
        ),
    )
    args = parser.parse_args(argv)

    if not args.variant.strip():
        parser.error("--variant must not be empty")
    if not args.hypothesis_code.strip():
        parser.error("--hypothesis-code must not be empty")
    if args.locale_filter is not None:
        args.locale_filter = args.locale_filter.strip().upper()
        if not args.locale_filter:
            parser.error("--locale-filter must not be empty")
        suffix = f"-{args.locale_filter}"
        if not args.variant.upper().endswith(suffix):
            args.variant = f"{args.variant}{suffix}"
    if args.repetitions < 1:
        parser.error("--repetitions must be >= 1")
    if args.concurrency < 1 or args.concurrency > MAX_CONCURRENCY:
        parser.error(f"--concurrency must be between 1 and {MAX_CONCURRENCY}")
    if args.max_cost_usd is not None and args.max_cost_usd < 0:
        parser.error("--max-cost-usd must be >= 0")
    if args.prompt_shrink_mode is None:
        args.prompt_shrink_mode = _infer_prompt_shrink_mode(args.variant)
    return args


def _select_prompts(prompt_set: PromptSet, prompt_ids: Iterable[str]) -> List[BenchmarkPrompt]:
    requested = list(prompt_ids)
    if not requested:
        return list(prompt_set.prompts)
    by_id = {prompt.prompt_id: prompt for prompt in prompt_set.prompts}
    missing = sorted(set(requested) - set(by_id))
    if missing:
        raise EvalHarnessError(f"Unknown prompt_id(s): {missing}")
    return [by_id[prompt_id] for prompt_id in requested]


def _filter_prompts_by_locale(
    prompts: Iterable[BenchmarkPrompt],
    locale_filter: Optional[str],
) -> List[BenchmarkPrompt]:
    selected = list(prompts)
    if locale_filter is None:
        return selected
    expected = locale_filter.upper()
    filtered = [prompt for prompt in selected if prompt.audience_locale.upper() == expected]
    if not filtered:
        raise SystemExit(f"No prompts matched --locale-filter={locale_filter}")
    return filtered


def _default_run_id(args: argparse.Namespace) -> str:
    if args.locale_filter:
        return args.variant
    return _utc_now().strftime("%Y%m%dT%H%M%SZ-baseline")


def _read_checkpoint(path: Optional[Path]) -> Dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_system_prompt_addendum(args: argparse.Namespace) -> Optional[str]:
    inline = getattr(args, "system_prompt_addendum", None)
    file_path = getattr(args, "system_prompt_addendum_file", None)
    if inline and file_path:
        raise EvalHarnessError(
            "Use only one of --system-prompt-addendum or --system-prompt-addendum-file"
        )
    if file_path is not None:
        return Path(file_path).read_text(encoding="utf-8").strip()
    if inline is not None:
        return str(inline).strip()
    return None


def _overlay_metadata(system_prompt_addendum: Optional[str]) -> Dict[str, Any]:
    addendum = (system_prompt_addendum or "").strip()
    return {
        "system_prompt_addendum": {
            "active": bool(addendum),
            "content_hash": _hash_text(addendum) if addendum else None,
            "content": addendum,
            "scope": "eval-only",
        }
    }


def _experiment_metadata_from_args(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    metadata = getattr(args, "experiment_metadata", None)
    if isinstance(metadata, dict):
        return metadata
    return None


def _run_dir_has_outputs(run_dir: Path) -> bool:
    if not run_dir.exists():
        return False
    return any(run_dir.iterdir())


def _checkpoint_completed(path: Optional[Path]) -> set[str]:
    payload = _read_checkpoint(path)
    return set(payload.get("completed_keys", []))


def _completed_keys_from_rows(rows: Iterable[Dict[str, Any]]) -> set[str]:
    keys: set[str] = set()
    for row in rows:
        prompt_id = row.get("prompt_id")
        repetition_index = row.get("repetition_index")
        if prompt_id is None or repetition_index is None:
            continue
        keys.add(f"{prompt_id}#{repetition_index}")
    return keys


def write_checkpoint(
    checkpoint_path: Path,
    *,
    run_id: str,
    completed_keys: Iterable[str],
    halt_reason: str,
    total_cost_usd: float,
    benchmark_set_version: str = BENCHMARK_SET_VERSION,
) -> None:
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": run_id,
        "benchmark_set_version": benchmark_set_version,
        "completed_keys": sorted(set(completed_keys)),
        "halt_reason": halt_reason,
        "total_cost_usd": round(total_cost_usd, 6),
        "written_at_utc": _utc_now().isoformat(),
    }
    checkpoint_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _count_components(value: Any) -> int:
    if isinstance(value, dict):
        count = 1 if "componentType" in value or "type" in value else 0
        return count + sum(_count_components(item) for item in value.values())
    if isinstance(value, list):
        return sum(_count_components(item) for item in value)
    return 0


def _coerce_non_negative_int(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return parsed if parsed >= 0 else 0


def _coerce_non_negative_float(value: Any) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return 0.0
    return parsed if parsed >= 0 else 0.0


def _provider_usage_from_response(response: FormAiGenerateResponse) -> Dict[str, Any]:
    meta = response.meta or {}
    usage = meta.get("provider_usage")
    if isinstance(usage, dict):
        return usage
    return {}


def _metrics_from_response(
    response: FormAiGenerateResponse,
    *,
    duration_ms: int,
    retry_count: int,
) -> Dict[str, Any]:
    validation = response.trace.validationSummary
    schema_valid = bool(response.status == "completed" and validation and validation.valid)
    provider_usage = _provider_usage_from_response(response)
    metrics = {
        "schema_valid": schema_valid,
        "component_count": _count_components(response.definitionJSON or {}),
        "collision_count": validation.collisionCount if validation else 0,
        "boundary_violation_count": validation.boundaryViolationCount if validation else 0,
        "attempt_count": response.trace.attemptCount,
        "terminal_reason": response.trace.terminalReason,
        "failure_class": response.trace.failureClass or ("none" if schema_valid else "unknown"),
        "duration_ms": duration_ms,
        "input_tokens": _coerce_non_negative_int(provider_usage.get("input_tokens")),
        "output_tokens": _coerce_non_negative_int(provider_usage.get("output_tokens")),
        "total_cost_usd": _coerce_non_negative_float(provider_usage.get("total_cost_usd")),
        "retry_count": retry_count,
    }
    metrics["provider_usage"] = provider_usage or None
    metrics["category_a"] = {field: metrics[field] for field in CATEGORY_A_FIELDS}
    metrics["category_b"] = None
    metrics["category_c"] = None
    return metrics


def _is_retryable_exception(exc: BaseException) -> bool:
    response = getattr(exc, "response", None)
    status_code = getattr(response, "status_code", None)
    return status_code == 429 or (isinstance(status_code, int) and 500 <= status_code <= 599)


def _call_generation_with_retries(
    call_generation: Callable[[BenchmarkPrompt], FormAiGenerateResponse],
    prompt: BenchmarkPrompt,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[FormAiGenerateResponse, int]:
    retry_count = 0
    while True:
        try:
            return call_generation(prompt), retry_count
        except Exception as exc:
            if retry_count >= MAX_PROVIDER_RETRIES or not _is_retryable_exception(exc):
                raise
            retry_count += 1
            sleep(0.1 + random.random() * 0.25 * retry_count)


def _mock_generate(prompt: BenchmarkPrompt) -> FormAiGenerateResponse:
    component_count = max(4, min(12, len(prompt.prompt.split()) // 12))
    trace = GenerationTraceMetadata(
        attemptCount=1,
        maxSystemCorrectionAttempts=0,
        systemCorrectionAttemptsUsed=0,
        terminalReason="validated-success",
        attempts=[
            AttemptTraceEntry(
                attemptNumber=1,
                phase="initial",
                validation=AttemptValidationSummary(
                    valid=True,
                    schemaErrorCount=0,
                    boundaryViolationCount=0,
                    collisionCount=0,
                    errorCount=0,
                ),
            )
        ],
        validationSummary=AttemptValidationSummary(
            valid=True,
            schemaErrorCount=0,
            boundaryViolationCount=0,
            collisionCount=0,
            errorCount=0,
        ),
        failureClass="none",
    )
    return FormAiGenerateResponse(
        status="completed",
        definitionJSON={
            "schemaVersion": "1.0",
            "pages": [
                {
                    "components": [
                        {"id": f"{prompt.prompt_id}-c-{index}", "type": "text"}
                        for index in range(component_count)
                    ]
                }
            ],
        },
        trace=trace,
        userMessage="deterministic mock generation",
        meta={"provider_usage": None},
    )


def _service_generate(
    *,
    model: Optional[str],
    openai_transport: str,
    persist_db: bool,
    system_prompt_addendum: Optional[str] = None,
) -> Callable[[BenchmarkPrompt], FormAiGenerateResponse]:
    db_session = None
    if persist_db:
        from common.database import SessionLocal

        db_session = SessionLocal()

    def call(prompt: BenchmarkPrompt) -> FormAiGenerateResponse:
        return generate_form_definition(
            prompt.prompt,
            model_override=model,
            runtime_context=prompt.runtime_context,
            openai_transport=openai_transport,
            system_prompt_addendum=system_prompt_addendum,
            audience_locale=prompt.audience_locale,
            db_session=db_session,
        )

    call.db_session = db_session  # type: ignore[attr-defined]
    return call


def build_eval_db_row(
    *,
    benchmark_set_version: str,
    hypothesis_code: str,
    variant_label: str,
    prompt_id: str,
    repetition_index: int,
    response: FormAiGenerateResponse,
    metrics: Dict[str, Any],
    created_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    created = created_at or _utc_now()
    return {
        "benchmark_set_version": benchmark_set_version,
        "hypothesis_code": hypothesis_code,
        "variant_label": variant_label,
        "prompt_id": prompt_id,
        "repetition_index": repetition_index,
        "generation_run_id": response.generationRunId,
        "metrics_json": json.dumps(metrics, default=_json_default, sort_keys=True),
        "judge_rubric_version": None,
        "judge_agreement_score": None,
        "bias_delta_json": None,
        "baseline_expires_at": created + timedelta(days=30),
        "created_date": created,
    }


def insert_eval_db_row(db_session: Any, row: Dict[str, Any]) -> None:
    db_session.execute(
        text(
            """
            INSERT INTO [log].[FormAiEvalRun]
            (
                [BenchmarkSetVersion],
                [HypothesisCode],
                [VariantLabel],
                [PromptID],
                [RepetitionIndex],
                [GenerationRunID],
                [MetricsJSON],
                [JudgeRubricVersion],
                [JudgeAgreementScore],
                [BiasDeltaJSON],
                [BaselineExpiresAt],
                [CreatedDate]
            )
            VALUES
            (
                :benchmark_set_version,
                :hypothesis_code,
                :variant_label,
                :prompt_id,
                :repetition_index,
                :generation_run_id,
                :metrics_json,
                :judge_rubric_version,
                :judge_agreement_score,
                :bias_delta_json,
                :baseline_expires_at,
                :created_date
            )
            """
        ),
        row,
    )


def _build_eval_tasks(
    prompts: Sequence[BenchmarkPrompt],
    *,
    repetitions: int,
    completed_keys: set[str],
) -> List[EvalTask]:
    tasks: List[EvalTask] = []
    sequence = 0
    for prompt in prompts:
        for repetition_index in range(1, repetitions + 1):
            key = f"{prompt.prompt_id}#{repetition_index}"
            if key in completed_keys:
                continue
            tasks.append(
                EvalTask(
                    sequence=sequence,
                    prompt=prompt,
                    repetition_index=repetition_index,
                    key=key,
                )
            )
            sequence += 1
    return tasks


def _run_eval_task(
    task: EvalTask,
    *,
    prompt_set: PromptSet,
    args: argparse.Namespace,
    call_generation: Callable[[BenchmarkPrompt], FormAiGenerateResponse],
    shared_context_bundle: Dict[str, Any],
) -> EvalTaskResult:
    started_at = _utc_now()
    started = time.perf_counter()
    response, retry_count = _call_generation_with_retries(call_generation, task.prompt)
    completed_at = _utc_now()
    duration_ms = int((time.perf_counter() - started) * 1000)
    metrics = _metrics_from_response(
        response,
        duration_ms=duration_ms,
        retry_count=retry_count,
    )
    row = {
        "eval_sequence": task.sequence,
        "started_at_utc": started_at,
        "completed_at_utc": completed_at,
        "benchmark_set_version": prompt_set.benchmark_set_version,
        "hypothesis_code": args.hypothesis_code,
        "variant_label": args.variant_label,
        "prompt_id": task.prompt.prompt_id,
        "repetition_index": task.repetition_index,
        "generation_run_id": response.generationRunId,
        "user_prompt": task.prompt.prompt,
        "expected_au_signals": task.prompt.expected_signals,
        "prompt_context_section_refs": shared_context_bundle.get("cases", {})
        .get(task.prompt.prompt_id, {})
        .get("prompt_context_section_refs", []),
        "deterministic_au_findings": au_diagnostics.lint_generated_definition(
            response.definitionJSON,
            prompt_id=task.prompt.prompt_id,
            prompt_metadata=task.prompt.metadata,
        ),
        "generated_definition": response.definitionJSON,
        "metrics": metrics,
    }
    return EvalTaskResult(
        task=task,
        row=row,
        response=response,
        metrics=metrics,
    )


def _write_outputs(
    run_dir: Path,
    rows: List[Dict[str, Any]],
    metadata: Dict[str, Any],
    *,
    shared_context_bundle: Optional[Dict[str, Any]] = None,
    prompt_context_findings: Optional[Sequence[Dict[str, Any]]] = None,
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    ordered_rows = sorted(
        rows,
        key=lambda row: (
            _coerce_non_negative_int(row.get("eval_sequence", 1_000_000)),
            str(row.get("prompt_id") or ""),
            _coerce_non_negative_int(row.get("repetition_index")),
        ),
    )
    metadata = dict(metadata)
    metadata["token_usage_status"] = _token_usage_status(ordered_rows)
    metrics_path = run_dir / "metrics.jsonl"
    metrics_path.write_text(
        "".join(json.dumps(row, default=_json_default, sort_keys=True) + "\n" for row in ordered_rows),
        encoding="utf-8",
    )

    fieldnames = [
        "benchmark_set_version",
        "hypothesis_code",
        "variant_label",
        "prompt_id",
        "repetition_index",
        *CATEGORY_A_FIELDS,
    ]
    with (run_dir / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in ordered_rows:
            flat = {
                "benchmark_set_version": row["benchmark_set_version"],
                "hypothesis_code": row["hypothesis_code"],
                "variant_label": row["variant_label"],
                "prompt_id": row["prompt_id"],
                "repetition_index": row["repetition_index"],
            }
            flat.update(row["metrics"]["category_a"])
            writer.writerow(flat)

    (run_dir / "run-metadata.json").write_text(
        json.dumps(metadata, indent=2, default=_json_default, sort_keys=True),
        encoding="utf-8",
    )
    if shared_context_bundle is not None:
        au_diagnostics.write_diagnostic_artifacts(
            run_dir,
            shared_context_bundle=shared_context_bundle,
            prompt_context_findings=prompt_context_findings or [],
            rows=ordered_rows,
        )


def _load_existing_metric_rows(run_dir: Path) -> List[Dict[str, Any]]:
    metrics_path = run_dir / "metrics.jsonl"
    if not metrics_path.exists():
        return []
    return [
        json.loads(line)
        for line in metrics_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _effective_concurrency(args: argparse.Namespace, pending_count: int) -> int:
    if pending_count <= 1:
        return 1
    if args.persist_db:
        # SQLAlchemy sessions used by the generation service are not thread-safe.
        return 1
    return max(1, min(args.concurrency, MAX_CONCURRENCY, pending_count))


def _sum_row_cost(rows: Iterable[Dict[str, Any]]) -> float:
    return sum(
        _coerce_non_negative_float((row.get("metrics") or {}).get("total_cost_usd"))
        for row in rows
    )


def _token_usage_status(rows: Iterable[Dict[str, Any]]) -> str:
    rows_list = list(rows)
    if not rows_list:
        return "unavailable"
    if any((row.get("metrics") or {}).get("provider_usage") for row in rows_list):
        return "available"
    return "unavailable"


def _log_progress(message: str) -> None:
    print(f"[form-ai-eval] {message}", file=sys.stderr, flush=True)


def _build_run_metadata(
    *,
    run_id: str,
    prompt_set: PromptSet,
    prompts: List[BenchmarkPrompt],
    args: argparse.Namespace,
    started_at: datetime,
    completed_at: datetime,
    run_dir: Path,
    total_cost_usd: float,
    completed_count: int,
    status: str,
    system_prompt_addendum: Optional[str] = None,
) -> Dict[str, Any]:
    if system_prompt_addendum is None:
        system_prompt_addendum = getattr(args, "resolved_system_prompt_addendum", None)
    metadata = {
        "run_id": run_id,
        "benchmark_set_version": prompt_set.benchmark_set_version,
        "hypothesis_code": args.hypothesis_code,
        "variant": args.variant,
        "variant_label": args.variant_label,
        "prompts_path": str(args.prompts_path),
        "prompt_shrink_mode": args.prompt_shrink_mode,
        "prompt_shrink_env": PROMPT_SHRINK_MODE_ENV,
        "au_locale_contract_version": au_diagnostics.AU_LOCALE_CONTRACT_VERSION,
        "diagnostic_artifacts": [
            "shared-context-bundle.json",
            "prompt-context-lint.json",
            "prompt-context-lint.md",
            "au-deterministic-checks.json",
            "au-deterministic-checks.md",
        ],
        "allow_au_context_conflicts": args.allow_au_context_conflicts,
        "locale_filter": args.locale_filter,
        "prompt_ids": [prompt.prompt_id for prompt in prompts],
        "repetitions": args.repetitions,
        "concurrency_cap": min(args.concurrency, MAX_CONCURRENCY),
        "concurrency_effective": _effective_concurrency(args, max(1, len(prompts) * args.repetitions)),
        "execution_model": "thread-pool" if not args.persist_db else "serial-persist-db",
        "max_provider_retries": MAX_PROVIDER_RETRIES,
        "max_cost_usd": args.max_cost_usd,
        "persist_db": args.persist_db,
        "mock": args.mock,
        "token_usage_status": _token_usage_status([]),
        "token_cost_status": "provider-cost-not-returned",
        "started_at_utc": started_at,
        "completed_at_utc": completed_at,
        "output_folder": str(run_dir),
        "total_cost_usd": round(total_cost_usd, 6),
        "completed_count": completed_count,
        "status": status,
        "eval_only_overlay": _overlay_metadata(system_prompt_addendum),
    }
    experiment_metadata = _experiment_metadata_from_args(args)
    if experiment_metadata is not None:
        metadata["experiment"] = experiment_metadata
    return metadata


def run_harness(
    args: argparse.Namespace,
    *,
    call_generation: Optional[Callable[[BenchmarkPrompt], FormAiGenerateResponse]] = None,
) -> Dict[str, Any]:
    prompt_set = load_prompt_set(args.prompts_path)
    prompts = _filter_prompts_by_locale(
        _select_prompts(prompt_set, args.prompt_id),
        args.locale_filter,
    )
    checkpoint_payload = _read_checkpoint(args.resume)
    run_id = (
        args.run_id
        or checkpoint_payload.get("run_id")
        or _default_run_id(args)
    )
    run_dir = args.output_root / run_id
    checkpoint_path = run_dir / "checkpoint.json"
    if args.resume is None and not args.overwrite_existing and _run_dir_has_outputs(run_dir):
        raise EvalHarnessError(
            f"Refusing to overwrite non-empty eval run folder: {run_dir}. "
            "Use --resume with its checkpoint.json or pass --overwrite-existing explicitly."
        )
    completed_keys = _checkpoint_completed(args.resume)
    rows: List[Dict[str, Any]] = _load_existing_metric_rows(run_dir) if args.resume else []
    completed_keys.update(_completed_keys_from_rows(rows))
    total_cost_usd = _sum_row_cost(rows)
    started_at = _utc_now()
    previous_prompt_shrink_mode = os.environ.get(PROMPT_SHRINK_MODE_ENV)
    os.environ[PROMPT_SHRINK_MODE_ENV] = args.prompt_shrink_mode
    system_prompt_addendum = _resolve_system_prompt_addendum(args)
    args.resolved_system_prompt_addendum = system_prompt_addendum

    if call_generation is None:
        if args.mock:
            call_generation = _mock_generate
        else:
            call_generation = _service_generate(
                model=args.model,
                openai_transport=args.openai_transport,
                persist_db=args.persist_db,
                system_prompt_addendum=system_prompt_addendum,
            )

    db_session = getattr(call_generation, "db_session", None)
    if args.persist_db and db_session is None:
        from common.database import SessionLocal

        db_session = SessionLocal()
    shared_context_bundle = au_diagnostics.build_shared_context_bundle(
        prompts,
        run_id=run_id,
        benchmark_set_version=prompt_set.benchmark_set_version,
        db_session=None if args.mock else db_session,
        candidate_prompt_block=system_prompt_addendum,
        experiment_metadata=_experiment_metadata_from_args(args),
    )
    prompt_context_findings = au_diagnostics.lint_context_sections(
        shared_context_bundle.get("sections", []),
        prompt_id=None,
        prompt_metadata={},
    )
    if (
        prompt_set.benchmark_set_version == AU_BENCHMARK_SET_VERSION
        and prompt_context_findings
        and not args.allow_au_context_conflicts
    ):
        blocking = [finding for finding in prompt_context_findings if finding["severity"] == "blocking"]
        if blocking:
            _write_outputs(
                run_dir,
                rows,
                _build_run_metadata(
                    run_id=run_id,
                    prompt_set=prompt_set,
                    prompts=prompts,
                    args=args,
                    started_at=started_at,
                    completed_at=_utc_now(),
                    run_dir=run_dir,
                    total_cost_usd=total_cost_usd,
                    completed_count=len(rows),
                    status="halted-au-context-lint",
                ),
                shared_context_bundle=shared_context_bundle,
                prompt_context_findings=prompt_context_findings,
            )
            raise EvalHarnessError(
                "AU prompt-context lint found blocking conflicts; rerun with "
                "--allow-au-context-conflicts to record an explicit override."
            )
    tasks = _build_eval_tasks(
        prompts,
        repetitions=args.repetitions,
        completed_keys=completed_keys,
    )
    total_work = len(rows) + len(tasks)
    effective_concurrency = _effective_concurrency(args, len(tasks))
    halt_reason: Optional[str] = None

    def record_result(result: EvalTaskResult, *, status: str = "running") -> None:
        nonlocal total_cost_usd
        rows.append(result.row)
        total_cost_usd += _coerce_non_negative_float(result.metrics.get("total_cost_usd"))
        completed_keys.add(result.task.key)

        if args.persist_db and db_session is not None:
            insert_eval_db_row(
                db_session,
                build_eval_db_row(
                    benchmark_set_version=prompt_set.benchmark_set_version,
                    hypothesis_code=args.hypothesis_code,
                    variant_label=args.variant_label,
                    prompt_id=result.task.prompt.prompt_id,
                    repetition_index=result.task.repetition_index,
                    response=result.response,
                    metrics=result.metrics,
                ),
            )
            db_session.commit()

        write_checkpoint(
            checkpoint_path,
            run_id=run_id,
            completed_keys=completed_keys,
            halt_reason=status,
            total_cost_usd=total_cost_usd,
            benchmark_set_version=prompt_set.benchmark_set_version,
        )
        _write_outputs(
            run_dir,
            rows,
            _build_run_metadata(
                run_id=run_id,
                prompt_set=prompt_set,
                prompts=prompts,
                args=args,
                started_at=started_at,
                completed_at=_utc_now(),
                run_dir=run_dir,
                total_cost_usd=total_cost_usd,
                completed_count=len(rows),
                status=status,
            ),
            shared_context_bundle=shared_context_bundle,
            prompt_context_findings=prompt_context_findings,
        )
        _log_progress(
            f"completed {len(rows)}/{total_work} {result.task.key} "
            f"duration_ms={result.metrics.get('duration_ms')}"
        )

    def should_stop_for_cost() -> bool:
        return args.max_cost_usd is not None and total_cost_usd >= args.max_cost_usd

    try:
        if tasks:
            _log_progress(
                f"starting run_id={run_id} rows={len(tasks)} concurrency={effective_concurrency}"
            )
        next_task_index = 0
        if effective_concurrency == 1:
            for task in tasks:
                if should_stop_for_cost():
                    halt_reason = "max-cost-usd"
                    break
                _log_progress(f"starting {task.key}")
                result = _run_eval_task(
                    task,
                    prompt_set=prompt_set,
                    args=args,
                    call_generation=call_generation,
                    shared_context_bundle=shared_context_bundle,
                )
                record_result(result)
        else:
            with ThreadPoolExecutor(max_workers=effective_concurrency) as executor:
                in_flight: Dict[Future[EvalTaskResult], EvalTask] = {}

                def submit_available() -> None:
                    nonlocal next_task_index, halt_reason
                    while len(in_flight) < effective_concurrency and next_task_index < len(tasks):
                        if should_stop_for_cost():
                            halt_reason = "max-cost-usd"
                            return
                        task = tasks[next_task_index]
                        next_task_index += 1
                        future = executor.submit(
                            _run_eval_task,
                            task,
                            prompt_set=prompt_set,
                            args=args,
                            call_generation=call_generation,
                            shared_context_bundle=shared_context_bundle,
                        )
                        in_flight[future] = task
                        _log_progress(
                            f"submitted {task.key} active={len(in_flight)} "
                            f"submitted={next_task_index}/{len(tasks)}"
                        )

                submit_available()
                while in_flight:
                    done, _ = wait(in_flight, return_when=FIRST_COMPLETED)
                    captured_error: Optional[BaseException] = None
                    for future in done:
                        task = in_flight.pop(future)
                        try:
                            result = future.result()
                        except BaseException as exc:
                            captured_error = exc
                            _log_progress(f"failed {task.key}: {exc}")
                            continue
                        record_result(result)
                    if captured_error is not None:
                        for pending in in_flight:
                            pending.cancel()
                        raise captured_error
                    submit_available()
                    if halt_reason == "max-cost-usd" and not in_flight:
                        break

        if halt_reason == "max-cost-usd":
            write_checkpoint(
                checkpoint_path,
                run_id=run_id,
                completed_keys=completed_keys,
                halt_reason=halt_reason,
                total_cost_usd=total_cost_usd,
                benchmark_set_version=prompt_set.benchmark_set_version,
            )
            _write_outputs(
                run_dir,
                rows,
                _build_run_metadata(
                    run_id=run_id,
                    prompt_set=prompt_set,
                    prompts=prompts,
                    args=args,
                    started_at=started_at,
                    completed_at=_utc_now(),
                    run_dir=run_dir,
                    total_cost_usd=total_cost_usd,
                    completed_count=len(rows),
                    status="halted-max-cost-usd",
                ),
                shared_context_bundle=shared_context_bundle,
                prompt_context_findings=prompt_context_findings,
            )

    except Exception:
        if db_session is not None:
            db_session.rollback()
        write_checkpoint(
            checkpoint_path,
            run_id=run_id,
            completed_keys=completed_keys,
            halt_reason="error",
            total_cost_usd=total_cost_usd,
            benchmark_set_version=prompt_set.benchmark_set_version,
        )
        _write_outputs(
            run_dir,
            rows,
            _build_run_metadata(
                run_id=run_id,
                prompt_set=prompt_set,
                prompts=prompts,
                args=args,
                started_at=started_at,
                completed_at=_utc_now(),
                run_dir=run_dir,
                total_cost_usd=total_cost_usd,
                completed_count=len(rows),
                status="halted-error",
            ),
            shared_context_bundle=shared_context_bundle,
            prompt_context_findings=prompt_context_findings,
        )
        raise
    finally:
        if db_session is not None:
            db_session.close()
        if previous_prompt_shrink_mode is None:
            os.environ.pop(PROMPT_SHRINK_MODE_ENV, None)
        else:
            os.environ[PROMPT_SHRINK_MODE_ENV] = previous_prompt_shrink_mode

    completed_at = _utc_now()
    final_status = "halted-max-cost-usd" if halt_reason == "max-cost-usd" else "completed"
    metadata = _build_run_metadata(
        run_id=run_id,
        prompt_set=prompt_set,
        prompts=prompts,
        args=args,
        started_at=started_at,
        completed_at=completed_at,
        run_dir=run_dir,
        total_cost_usd=total_cost_usd,
        completed_count=len(rows),
        status=final_status,
    )
    metadata["token_usage_status"] = _token_usage_status(rows)
    _write_outputs(
        run_dir,
        rows,
        metadata,
        shared_context_bundle=shared_context_bundle,
        prompt_context_findings=prompt_context_findings,
    )
    return metadata


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    metadata = run_harness(args)
    print(json.dumps(metadata, indent=2, default=_json_default, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
