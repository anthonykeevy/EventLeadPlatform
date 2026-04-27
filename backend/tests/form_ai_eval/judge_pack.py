"""Story 6.4.3b judge package generator.

Builds a deterministic, anonymised package from a Form AI eval run folder.
The local metrics artifacts link to ``GenerationRunID``; when DB access is
available the generator can enrich rows with persisted ``final-definition``
artifacts from ``dbo.GenerationArtifact``.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from sqlalchemy import text

BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import run as eval_run  # noqa: E402


RUBRIC_VERSION = "rubric_v2"
DEFAULT_RUBRIC_PATH = Path(__file__).with_name("rubric_v2.md")
PACKAGE_SCHEMA_VERSION = "judge-package-v2"
JUDGE_MODELS = ["gpt5mini", "claude", "grok"]
CATEGORY_B_METRICS = [
    "field_coverage_recall",
    "field_label_f1",
    "validation_intent_accuracy",
    "row_group_agreement",
    "locale_fidelity",
    "policy_compliance",
    "cultural_register",
    "cross_locale_leakage",
    "format_pattern_accuracy",
    "copy_quality_score",
]

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")
DATE_RE = re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b")
COMMON_SYNTHETIC_NAMES = re.compile(
    r"\b(?:John Doe|Jane Doe|Jane Smith|Alex Smith|Sam Taylor|Taylor Morgan)\b",
    re.IGNORECASE,
)


class JudgePackageError(RuntimeError):
    """Raised when a judge package cannot be built from the provided inputs."""


@dataclass(frozen=True)
class JudgePackageRow:
    row_id: str
    eval_run_id: Optional[int]
    generation_run_id: Optional[int]
    prompt_id: str
    repetition_index: int
    variant_label: str
    benchmark_set_version: str
    prompt_text: str
    prompt_metadata: Dict[str, Any]
    metrics: Dict[str, Any]
    generated_definition: Optional[Dict[str, Any]]
    generated_definition_source: str


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Form AI judge package.")
    parser.add_argument("eval_run_dir", type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--prompts-path", type=Path, default=eval_run.DEFAULT_PROMPTS_PATH)
    parser.add_argument("--rubric-path", type=Path, default=DEFAULT_RUBRIC_PATH)
    parser.add_argument(
        "--use-db",
        action="store_true",
        help="Load final-definition artifacts and EvalRunID mappings from the configured DB.",
    )
    return parser.parse_args(argv)


def row_id_for(prompt_id: str, repetition_index: int) -> str:
    return f"{prompt_id}__r{int(repetition_index):02d}"


def load_metric_rows(eval_run_dir: Path) -> List[Dict[str, Any]]:
    metrics_path = eval_run_dir / "metrics.jsonl"
    if not metrics_path.exists():
        raise JudgePackageError(f"Missing metrics artifact: {metrics_path}")
    rows = [
        json.loads(line)
        for line in metrics_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not rows:
        raise JudgePackageError(f"No metric rows found in {metrics_path}")
    return rows


def load_run_metadata(eval_run_dir: Path) -> Dict[str, Any]:
    metadata_path = eval_run_dir / "run-metadata.json"
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def scrub_pii_adjacent(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: scrub_pii_adjacent(item) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub_pii_adjacent(item) for item in value]
    if not isinstance(value, str):
        return value

    scrubbed = EMAIL_RE.sub("[SCRUBBED_EMAIL]", value)
    scrubbed = DATE_RE.sub("[SCRUBBED_DATE]", scrubbed)
    scrubbed = PHONE_RE.sub("[SCRUBBED_PHONE]", scrubbed)
    scrubbed = COMMON_SYNTHETIC_NAMES.sub("[SCRUBBED_NAME]", scrubbed)
    return scrubbed


def _json_default(value: Any) -> str:
    return str(value)


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _definition_from_metric_row(row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for key in ("definition_json", "definitionJSON", "generated_definition", "final_definition"):
        value = row.get(key)
        if isinstance(value, dict):
            return value
    return None


def fetch_final_definitions_from_db(
    db_session: Any, generation_run_ids: Iterable[int]
) -> Dict[int, Dict[str, Any]]:
    run_ids = sorted({int(run_id) for run_id in generation_run_ids if run_id is not None})
    if not run_ids:
        return {}
    placeholders = ", ".join(f":run_{index}" for index, _ in enumerate(run_ids))
    params = {f"run_{index}": run_id for index, run_id in enumerate(run_ids)}
    result = db_session.execute(
        text(
            f"""
            SELECT GenerationRunID, ArtifactJson
            FROM dbo.GenerationArtifact
            WHERE ArtifactType = 'final-definition'
              AND GenerationRunID IN ({placeholders})
            ORDER BY GenerationRunID ASC, SequenceNumber ASC
            """
        ),
        params,
    )
    rows = result.all() if hasattr(result, "all") else result

    definitions: Dict[int, Dict[str, Any]] = {}
    for row in rows:
        if int(row.GenerationRunID) in definitions:
            continue
        payload = json.loads(row.ArtifactJson)
        if isinstance(payload, dict):
            definitions[int(row.GenerationRunID)] = payload
    return definitions


def fetch_eval_run_ids_from_db(
    db_session: Any, generation_run_ids: Iterable[int]
) -> Dict[int, int]:
    run_ids = sorted({int(run_id) for run_id in generation_run_ids if run_id is not None})
    if not run_ids:
        return {}
    placeholders = ", ".join(f":run_{index}" for index, _ in enumerate(run_ids))
    params = {f"run_{index}": run_id for index, run_id in enumerate(run_ids)}
    result = db_session.execute(
        text(
            f"""
            SELECT EvalRunID, GenerationRunID
            FROM [log].[FormAiEvalRun]
            WHERE GenerationRunID IN ({placeholders})
            """
        ),
        params,
    )
    rows = result.all() if hasattr(result, "all") else result
    return {int(row.GenerationRunID): int(row.EvalRunID) for row in rows}


def build_package_rows(
    eval_run_dir: Path,
    *,
    prompts_path: Path = eval_run.DEFAULT_PROMPTS_PATH,
    db_session: Any = None,
) -> List[JudgePackageRow]:
    metric_rows = load_metric_rows(eval_run_dir)
    prompt_set = eval_run.load_prompt_set(prompts_path)
    prompts_by_id = {prompt.prompt_id: prompt for prompt in prompt_set.prompts}
    prompt_order = {prompt.prompt_id: index for index, prompt in enumerate(prompt_set.prompts)}
    generation_run_ids = [
        generation_run_id
        for generation_run_id in (_coerce_int(row.get("generation_run_id")) for row in metric_rows)
        if generation_run_id is not None
    ]
    db_definitions = (
        fetch_final_definitions_from_db(db_session, generation_run_ids) if db_session is not None else {}
    )
    db_eval_run_ids = (
        fetch_eval_run_ids_from_db(db_session, generation_run_ids) if db_session is not None else {}
    )

    package_rows: List[JudgePackageRow] = []
    for row in metric_rows:
        prompt_id = row.get("prompt_id")
        if prompt_id not in prompts_by_id:
            raise JudgePackageError(f"Metric row references unknown prompt_id: {prompt_id!r}")
        repetition_index = int(row.get("repetition_index", 1))
        generation_run_id = _coerce_int(row.get("generation_run_id"))
        definition = _definition_from_metric_row(row)
        source = "metrics.jsonl"
        if definition is None and generation_run_id in db_definitions:
            definition = db_definitions[generation_run_id]
            source = "dbo.GenerationArtifact"
        if definition is None:
            source = "unavailable"

        prompt = prompts_by_id[prompt_id]
        eval_run_id = _coerce_int(row.get("eval_run_id") or row.get("EvalRunID"))
        if eval_run_id is None and generation_run_id is not None:
            eval_run_id = db_eval_run_ids.get(generation_run_id)
        package_rows.append(
            JudgePackageRow(
                row_id=row_id_for(prompt_id, repetition_index),
                eval_run_id=eval_run_id,
                generation_run_id=generation_run_id,
                prompt_id=prompt_id,
                repetition_index=repetition_index,
                variant_label=str(row.get("variant_label", "")),
                benchmark_set_version=str(
                    row.get("benchmark_set_version", prompt_set.benchmark_set_version)
                ),
                prompt_text=prompt.prompt,
                prompt_metadata=dict(prompt.metadata),
                metrics=dict(row.get("metrics") or {}),
                generated_definition=scrub_pii_adjacent(definition) if definition is not None else None,
                generated_definition_source=source,
            )
        )

    return sorted(
        package_rows,
        key=lambda item: (
            prompt_order.get(item.prompt_id, 9999),
            item.repetition_index,
            item.generation_run_id or 0,
        ),
    )


def _row_to_metadata(row: JudgePackageRow) -> Dict[str, Any]:
    return {
        "row_id": row.row_id,
        "eval_run_id": row.eval_run_id,
        "generation_run_id": row.generation_run_id,
        "prompt_id": row.prompt_id,
        "repetition_index": row.repetition_index,
        "variant_label": row.variant_label,
        "benchmark_set_version": row.benchmark_set_version,
        "generated_definition_source": row.generated_definition_source,
        "generated_definition_available": row.generated_definition is not None,
    }


def build_output_template(rows: Sequence[JudgePackageRow], judge_model: str = "claude") -> Dict[str, Any]:
    return {
        "rubric_version": RUBRIC_VERSION,
        "judge_model": judge_model,
        "judge_model_version": "",
        "rows": [
            {
                "row_id": row.row_id,
                "prompt_id": row.prompt_id,
                "repetition_index": row.repetition_index,
                "variant_label": row.variant_label,
                "scores": {metric: None for metric in CATEGORY_B_METRICS},
                "rationale": "",
            }
            for row in rows
        ],
    }


def render_judge_input(rows: Sequence[JudgePackageRow], metadata: Dict[str, Any]) -> str:
    lines = [
        "# Form AI Judge Input Batch",
        "",
        f"Run ID: `{metadata.get('run_id', 'unknown')}`",
        f"Benchmark set: `{metadata.get('benchmark_set_version', 'prompts-v1.0')}`",
        f"Rubric version: `{RUBRIC_VERSION}`",
        "",
        "Use `rubric_v2.md` and return JSON matching `judge-output-template.json`.",
        "Set `judge_model_version` to the exact model/version shown in your Cursor session.",
        "Before assigning scores for each row, identify at least one weakness per row before scoring.",
        "Judge only the anonymised package content below.",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"## Row {index}: `{row.row_id}`",
                "",
                f"- Prompt ID: `{row.prompt_id}`",
                f"- Repetition: `{row.repetition_index}`",
                f"- Variant: `{row.variant_label}`",
                f"- EvalRunID: `{row.eval_run_id}`",
                f"- GenerationRunID: `{row.generation_run_id}`",
                f"- Definition source: `{row.generated_definition_source}`",
                "",
                "### Prompt",
                "",
                row.prompt_text,
                "",
                "### Prompt Metadata",
                "",
                "```json",
                json.dumps(row.prompt_metadata, indent=2, sort_keys=True),
                "```",
                "",
                "### Category A Metrics",
                "",
                "```json",
                json.dumps(row.metrics.get("category_a", row.metrics), indent=2, sort_keys=True),
                "```",
                "",
                "### Generated Definition",
                "",
                "```json",
                json.dumps(
                    row.generated_definition
                    if row.generated_definition is not None
                    else {"warning": "generated definition unavailable in local artifacts"},
                    indent=2,
                    sort_keys=True,
                    default=_json_default,
                ),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_judge_package(
    eval_run_dir: Path,
    *,
    output_dir: Optional[Path] = None,
    prompts_path: Path = eval_run.DEFAULT_PROMPTS_PATH,
    rubric_path: Path = DEFAULT_RUBRIC_PATH,
    db_session: Any = None,
) -> Path:
    eval_run_dir = eval_run_dir.resolve()
    package_dir = (output_dir or (eval_run_dir / "judge-package")).resolve()
    rows = build_package_rows(eval_run_dir, prompts_path=prompts_path, db_session=db_session)
    run_metadata = load_run_metadata(eval_run_dir)
    package_metadata = {
        "package_schema_version": PACKAGE_SCHEMA_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "run_id": run_metadata.get("run_id", eval_run_dir.name),
        "benchmark_set_version": run_metadata.get("benchmark_set_version", "prompts-v1.0"),
        "variant_label": run_metadata.get("variant_label"),
        "source_eval_run_dir": str(eval_run_dir),
        "row_count": len(rows),
        "judge_models": JUDGE_MODELS,
        "category_b_metrics": CATEGORY_B_METRICS,
        "rows": [_row_to_metadata(row) for row in rows],
        "notes": [
            "Obvious email, phone, ISO/date-like, and common synthetic full-name values are scrubbed.",
            "Name-like field labels are preserved so semantic judging remains possible.",
            "If generated definitions are unavailable, rerun with --use-db against a DB that has dbo.GenerationArtifact final-definition rows.",
        ],
    }

    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "results").mkdir(exist_ok=True)
    shutil.copyfile(rubric_path, package_dir / "rubric_v2.md")
    (package_dir / "judge-input-batch.md").write_text(
        render_judge_input(rows, run_metadata), encoding="utf-8"
    )
    (package_dir / "judge-output-template.json").write_text(
        json.dumps(build_output_template(rows), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (package_dir / "judge-package-metadata.json").write_text(
        json.dumps(package_metadata, indent=2, sort_keys=True, default=_json_default) + "\n",
        encoding="utf-8",
    )
    return package_dir


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    db_session = None
    try:
        if args.use_db:
            from common.database import SessionLocal

            db_session = SessionLocal()
        package_dir = write_judge_package(
            args.eval_run_dir,
            output_dir=args.output_dir,
            prompts_path=args.prompts_path,
            rubric_path=args.rubric_path,
            db_session=db_session,
        )
        print(json.dumps({"judge_package_dir": str(package_dir)}, indent=2, sort_keys=True))
        return 0
    finally:
        if db_session is not None:
            db_session.close()


if __name__ == "__main__":
    raise SystemExit(main())
