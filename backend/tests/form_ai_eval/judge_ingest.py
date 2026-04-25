"""Story 6.4.3b judge output ingest.

Validates manually saved Cursor judge JSON files and computes rubric_v1
aggregates. DB persistence is optional; local summary artifacts are always
written when validation succeeds.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Sequence

from sqlalchemy import text

BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval.judge_pack import (  # type: ignore[import-not-found]  # noqa: E402
    CATEGORY_B_METRICS,
    RUBRIC_VERSION,
)


EXPECTED_RESULT_FILES = {
    "gpt5mini": "judge-output-gpt5mini.json",
    "claude": "judge-output-claude.json",
    "gemini": "judge-output-gemini.json",
}
PRIMARY_JUDGES = ("claude", "gemini")
CONTROL_JUDGE = "gpt5mini"


class JudgeIngestError(RuntimeError):
    """Raised when judge outputs are malformed or incomplete."""


@dataclass(frozen=True)
class PackageRow:
    row_id: str
    eval_run_id: Optional[int]
    generation_run_id: Optional[int]
    prompt_id: str
    repetition_index: int
    variant_label: str


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest Form AI judge output JSON files.")
    parser.add_argument("judge_package_dir", type=Path)
    parser.add_argument("--persist-db", action="store_true")
    return parser.parse_args(argv)


def load_package_rows(judge_package_dir: Path) -> List[PackageRow]:
    metadata_path = judge_package_dir / "judge-package-metadata.json"
    if not metadata_path.exists():
        raise JudgeIngestError(f"Missing package metadata: {metadata_path}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    rows = metadata.get("rows")
    if not isinstance(rows, list) or not rows:
        raise JudgeIngestError("judge-package-metadata.json must contain non-empty rows")
    return [
        PackageRow(
            row_id=str(row["row_id"]),
            eval_run_id=_coerce_int(row.get("eval_run_id")),
            generation_run_id=_coerce_int(row.get("generation_run_id")),
            prompt_id=str(row["prompt_id"]),
            repetition_index=int(row["repetition_index"]),
            variant_label=str(row["variant_label"]),
        )
        for row in rows
    ]


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise JudgeIngestError(f"Missing judge result file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise JudgeIngestError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise JudgeIngestError(f"{path} must contain a JSON object")
    return payload


def load_judge_outputs(judge_package_dir: Path) -> Dict[str, Dict[str, Any]]:
    results_dir = judge_package_dir / "results"
    outputs: Dict[str, Dict[str, Any]] = {}
    for judge_model, filename in EXPECTED_RESULT_FILES.items():
        path = results_dir / filename
        if path.exists():
            outputs[judge_model] = _load_json(path)
    if not outputs:
        raise JudgeIngestError(f"No judge result files found under {results_dir}")
    return outputs


def validate_judge_output(
    judge_model: str,
    payload: Dict[str, Any],
    expected_rows: Sequence[PackageRow],
) -> Dict[str, Dict[str, Any]]:
    if payload.get("rubric_version") != RUBRIC_VERSION:
        raise JudgeIngestError(
            f"{judge_model}: rubric_version must be {RUBRIC_VERSION!r}; got {payload.get('rubric_version')!r}"
        )
    if payload.get("judge_model") != judge_model:
        raise JudgeIngestError(
            f"{judge_model}: judge_model must match result filename; got {payload.get('judge_model')!r}"
        )
    rows = payload.get("rows")
    if not isinstance(rows, list):
        raise JudgeIngestError(f"{judge_model}: rows must be a list")

    expected_by_id = {row.row_id: row for row in expected_rows}
    seen: Dict[str, Dict[str, Any]] = {}
    duplicates: List[str] = []
    unknown: List[str] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise JudgeIngestError(f"{judge_model}: row {index} must be an object")
        row_id = row.get("row_id")
        if not isinstance(row_id, str):
            raise JudgeIngestError(f"{judge_model}: row {index} missing row_id")
        if row_id in seen:
            duplicates.append(row_id)
            continue
        if row_id not in expected_by_id:
            unknown.append(row_id)
            continue
        expected = expected_by_id[row_id]
        if row.get("prompt_id") != expected.prompt_id:
            raise JudgeIngestError(f"{judge_model}: {row_id} prompt_id mismatch")
        if int(row.get("repetition_index", -1)) != expected.repetition_index:
            raise JudgeIngestError(f"{judge_model}: {row_id} repetition_index mismatch")
        if row.get("variant_label") != expected.variant_label:
            raise JudgeIngestError(f"{judge_model}: {row_id} variant_label mismatch")

        scores = row.get("scores")
        if not isinstance(scores, dict):
            raise JudgeIngestError(f"{judge_model}: {row_id} scores must be an object")
        score_keys = set(scores)
        expected_keys = set(CATEGORY_B_METRICS)
        if score_keys != expected_keys:
            raise JudgeIngestError(
                f"{judge_model}: {row_id} scores must contain exactly {sorted(expected_keys)}"
            )
        for metric, score in scores.items():
            if not isinstance(score, (int, float)) or isinstance(score, bool):
                raise JudgeIngestError(f"{judge_model}: {row_id} {metric} must be numeric")
            if float(score) < 0 or float(score) > 5:
                raise JudgeIngestError(f"{judge_model}: {row_id} {metric} out of range 0..5")
        if not isinstance(row.get("rationale"), str):
            raise JudgeIngestError(f"{judge_model}: {row_id} rationale must be a string")
        seen[row_id] = row

    if duplicates:
        raise JudgeIngestError(f"{judge_model}: duplicate row IDs: {sorted(duplicates)}")
    if unknown:
        raise JudgeIngestError(f"{judge_model}: unknown row IDs: {sorted(unknown)}")
    missing = sorted(set(expected_by_id) - set(seen))
    if missing:
        raise JudgeIngestError(f"{judge_model}: missing row IDs: {missing}")
    return seen


def validate_all_outputs(
    outputs: Dict[str, Dict[str, Any]], expected_rows: Sequence[PackageRow]
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    missing_primary = [judge for judge in PRIMARY_JUDGES if judge not in outputs]
    if missing_primary:
        raise JudgeIngestError(
            f"Missing primary judge output(s): {missing_primary}; Claude and Gemini are required"
        )
    return {
        judge_model: validate_judge_output(judge_model, payload, expected_rows)
        for judge_model, payload in outputs.items()
    }


def _agreement_score(claude_scores: Dict[str, Any], gemini_scores: Dict[str, Any]) -> float:
    distances = [
        abs(float(claude_scores[metric]) - float(gemini_scores[metric])) / 5.0
        for metric in CATEGORY_B_METRICS
    ]
    return round(max(0.0, 1.0 - mean(distances)), 3)


def compute_summary(
    package_rows: Sequence[PackageRow],
    validated_outputs: Dict[str, Dict[str, Dict[str, Any]]],
) -> Dict[str, Any]:
    summaries: List[Dict[str, Any]] = []
    for package_row in package_rows:
        row_id = package_row.row_id
        claude_scores = validated_outputs["claude"][row_id]["scores"]
        gemini_scores = validated_outputs["gemini"][row_id]["scores"]
        cross_model_mean = {
            metric: round(mean([float(claude_scores[metric]), float(gemini_scores[metric])]), 3)
            for metric in CATEGORY_B_METRICS
        }
        control_scores = (
            validated_outputs.get(CONTROL_JUDGE, {}).get(row_id, {}).get("scores")
            if CONTROL_JUDGE in validated_outputs
            else None
        )
        bias_delta = None
        if isinstance(control_scores, dict):
            bias_delta = {
                metric: round(float(control_scores[metric]) - cross_model_mean[metric], 3)
                for metric in CATEGORY_B_METRICS
            }
        summaries.append(
            {
                "row_id": row_id,
                "eval_run_id": package_row.eval_run_id,
                "generation_run_id": package_row.generation_run_id,
                "prompt_id": package_row.prompt_id,
                "repetition_index": package_row.repetition_index,
                "variant_label": package_row.variant_label,
                "cross_model_mean": cross_model_mean,
                "gpt5mini_bias_delta": bias_delta,
                "judge_agreement_score": _agreement_score(claude_scores, gemini_scores),
                "judge_models_present": sorted(validated_outputs),
            }
        )
    return {
        "rubric_version": RUBRIC_VERSION,
        "primary_judges": list(PRIMARY_JUDGES),
        "control_judge": CONTROL_JUDGE if CONTROL_JUDGE in validated_outputs else None,
        "row_count": len(summaries),
        "rows": summaries,
    }


def write_summary_artifacts(judge_package_dir: Path, summary: Dict[str, Any]) -> None:
    summary_path = judge_package_dir / "judge-ingest-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    csv_path = judge_package_dir / "judge-ingest-summary.csv"
    fieldnames = [
        "row_id",
        "eval_run_id",
        "generation_run_id",
        "prompt_id",
        "repetition_index",
        "variant_label",
        "judge_agreement_score",
        *[f"mean_{metric}" for metric in CATEGORY_B_METRICS],
        *[f"gpt5mini_delta_{metric}" for metric in CATEGORY_B_METRICS],
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary["rows"]:
            flat = {
                "row_id": row["row_id"],
                "eval_run_id": row["eval_run_id"],
                "generation_run_id": row["generation_run_id"],
                "prompt_id": row["prompt_id"],
                "repetition_index": row["repetition_index"],
                "variant_label": row["variant_label"],
                "judge_agreement_score": row["judge_agreement_score"],
            }
            flat.update(
                {f"mean_{metric}": row["cross_model_mean"][metric] for metric in CATEGORY_B_METRICS}
            )
            bias_delta = row.get("gpt5mini_bias_delta") or {}
            flat.update(
                {
                    f"gpt5mini_delta_{metric}": bias_delta.get(metric)
                    for metric in CATEGORY_B_METRICS
                }
            )
            writer.writerow(flat)


def build_eval_update_params(row_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "eval_run_id": row_summary.get("eval_run_id"),
        "generation_run_id": row_summary.get("generation_run_id"),
        "prompt_id": row_summary["prompt_id"],
        "repetition_index": row_summary["repetition_index"],
        "variant_label": row_summary["variant_label"],
        "judge_rubric_version": RUBRIC_VERSION,
        "judge_agreement_score": row_summary["judge_agreement_score"],
        "bias_delta_json": json.dumps(
            {
                "cross_model_mean": row_summary["cross_model_mean"],
                "gpt5mini_bias_delta": row_summary.get("gpt5mini_bias_delta"),
                "primary_judges": list(PRIMARY_JUDGES),
                "control_judge": CONTROL_JUDGE,
            },
            sort_keys=True,
        ),
    }


def update_eval_run_judge_fields(db_session: Any, params: Dict[str, Any]) -> None:
    if params.get("eval_run_id") is not None:
        db_session.execute(
            text(
                """
                UPDATE [log].[FormAiEvalRun]
                   SET JudgeRubricVersion = :judge_rubric_version,
                       JudgeAgreementScore = :judge_agreement_score,
                       BiasDeltaJSON = :bias_delta_json
                 WHERE EvalRunID = :eval_run_id
                """
            ),
            params,
        )
        return
    db_session.execute(
        text(
            """
            UPDATE [log].[FormAiEvalRun]
               SET JudgeRubricVersion = :judge_rubric_version,
                   JudgeAgreementScore = :judge_agreement_score,
                   BiasDeltaJSON = :bias_delta_json
             WHERE GenerationRunID = :generation_run_id
               AND PromptID = :prompt_id
               AND RepetitionIndex = :repetition_index
               AND VariantLabel = :variant_label
            """
        ),
        params,
    )


def persist_summary_to_db(db_session: Any, summary: Dict[str, Any]) -> int:
    count = 0
    for row in summary["rows"]:
        update_eval_run_judge_fields(db_session, build_eval_update_params(row))
        count += 1
    db_session.commit()
    return count


def ingest_judge_package(judge_package_dir: Path, *, db_session: Any = None) -> Dict[str, Any]:
    package_rows = load_package_rows(judge_package_dir)
    outputs = load_judge_outputs(judge_package_dir)
    validated = validate_all_outputs(outputs, package_rows)
    summary = compute_summary(package_rows, validated)
    summary["db_update_status"] = "not-requested"
    if db_session is not None:
        summary["db_update_status"] = "updated"
        summary["db_update_count"] = persist_summary_to_db(db_session, summary)
    write_summary_artifacts(judge_package_dir, summary)
    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    db_session = None
    try:
        if args.persist_db:
            from common.database import SessionLocal

            db_session = SessionLocal()
        summary = ingest_judge_package(args.judge_package_dir, db_session=db_session)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    finally:
        if db_session is not None:
            db_session.close()


if __name__ == "__main__":
    raise SystemExit(main())
