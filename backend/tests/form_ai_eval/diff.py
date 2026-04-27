"""Compare two Form AI eval runs and emit diff/statistics reports."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from statistics import mean
from typing import Any, Optional, Sequence

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import stats

CATEGORY_A_FIELDS = [
    "schema_valid",
    "component_count",
    "collision_count",
    "boundary_violation_count",
    "attempt_count",
    "duration_ms",
    "input_tokens",
    "output_tokens",
    "total_cost_usd",
]
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
ADVISORY_FIELDS = [
    "component_count",
    "collision_count",
    "attempt_count",
    "duration_ms",
    "input_tokens",
    "output_tokens",
    "total_cost_usd",
]


class EvalDiffError(RuntimeError):
    """Raised when eval comparison inputs are invalid."""


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two Form AI eval run folders.")
    parser.add_argument("--baseline-run", type=Path, required=True)
    parser.add_argument("--variant-run", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args(argv)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _row_key(prompt_id: str, repetition_index: int) -> str:
    return f"{prompt_id}__r{int(repetition_index):02d}"


def _category_a(row: dict[str, Any]) -> dict[str, Any]:
    metrics = row.get("metrics")
    if isinstance(metrics, dict):
        category_a = metrics.get("category_a")
        if isinstance(category_a, dict):
            return dict(category_a)
    return {field: row.get(field) for field in CATEGORY_A_FIELDS if field in row}


def _load_metrics_jsonl(run_dir: Path) -> list[dict[str, Any]]:
    metrics_path = run_dir / "metrics.jsonl"
    if not metrics_path.exists():
        return []
    return [
        json.loads(line)
        for line in metrics_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _load_summary_csv(run_dir: Path) -> list[dict[str, Any]]:
    summary_path = run_dir / "summary.csv"
    if not summary_path.exists():
        return []
    with summary_path.open(newline="", encoding="utf-8") as handle:
        return [
            {
                **row,
                "metrics": {"category_a": {field: _coerce_value(row.get(field)) for field in CATEGORY_A_FIELDS}},
            }
            for row in csv.DictReader(handle)
        ]


def _coerce_value(value: Any) -> Any:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value
    text = str(value)
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return value


def _load_metric_rows(run_dir: Path) -> list[dict[str, Any]]:
    rows = _load_metrics_jsonl(run_dir) or _load_summary_csv(run_dir)
    if not rows:
        raise EvalDiffError(f"No metrics.jsonl or summary.csv rows found in {run_dir}")
    return rows


def _index_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = _row_key(str(row["prompt_id"]), int(row.get("repetition_index", 1)))
        if key in indexed:
            raise EvalDiffError(f"Duplicate eval row key: {key}")
        indexed[key] = row
    return indexed


def _numeric(value: Any) -> Optional[float]:
    coerced = _coerce_value(value)
    if isinstance(coerced, bool) or coerced is None:
        return None
    if isinstance(coerced, (int, float)):
        return float(coerced)
    return None


def _mean(values: list[float]) -> Optional[float]:
    return mean(values) if values else None


def _load_judge_summary(run_dir: Path) -> dict[str, Any]:
    candidates = [
        run_dir / "judge-package" / "judge-ingest-summary.json",
        run_dir / "judge-ingest-summary.json",
    ]
    candidates.extend(sorted(run_dir.rglob("judge-ingest-summary.json")))
    for candidate in candidates:
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {}


def _index_judge_rows(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = summary.get("rows")
    if not isinstance(rows, list):
        return {}
    return {
        _row_key(str(row["prompt_id"]), int(row.get("repetition_index", 1))): row
        for row in rows
    }


def _compare_advisory_metrics(
    matched_keys: list[str],
    baseline_rows: dict[str, dict[str, Any]],
    variant_rows: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for field in ADVISORY_FIELDS:
        baseline_values: list[float] = []
        variant_values: list[float] = []
        for key in matched_keys:
            baseline_value = _numeric(_category_a(baseline_rows[key]).get(field))
            variant_value = _numeric(_category_a(variant_rows[key]).get(field))
            if baseline_value is None or variant_value is None:
                continue
            baseline_values.append(baseline_value)
            variant_values.append(variant_value)
        if baseline_values and variant_values:
            baseline_mean = mean(baseline_values)
            variant_mean = mean(variant_values)
            verdict = stats.verdict_for_metric(
                metric_name=field,
                baseline_values=baseline_values,
                variant_values=variant_values,
                metric_kind="continuous",
                category="A",
                higher_is_better=False if field in {"duration_ms", "input_tokens", "output_tokens", "total_cost_usd", "attempt_count", "collision_count"} else True,
            )
            result[field] = {
                "baseline_mean": baseline_mean,
                "variant_mean": variant_mean,
                "delta": variant_mean - baseline_mean,
                "p_value": verdict["p_value"],
                "effect_size": verdict["effect_size"],
                "decision": "advisory",
            }
    return result


def _compare_judge_metrics(
    matched_keys: list[str],
    baseline_judge_rows: dict[str, dict[str, Any]],
    variant_judge_rows: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    metric_deltas: dict[str, dict[str, Any]] = {}
    bias_deltas: dict[str, dict[str, Any]] = {}
    judge_keys = [key for key in matched_keys if key in baseline_judge_rows and key in variant_judge_rows]
    for metric in CATEGORY_B_METRICS:
        baseline_values = [
            float(baseline_judge_rows[key]["cross_model_mean"][metric])
            for key in judge_keys
            if metric in baseline_judge_rows[key].get("cross_model_mean", {})
        ]
        variant_values = [
            float(variant_judge_rows[key]["cross_model_mean"][metric])
            for key in judge_keys
            if metric in variant_judge_rows[key].get("cross_model_mean", {})
        ]
        if baseline_values and variant_values and len(baseline_values) == len(variant_values):
            metric_deltas[metric] = stats.verdict_for_metric(
                metric_name=metric,
                baseline_values=baseline_values,
                variant_values=variant_values,
                metric_kind="continuous",
                category="B",
            )

        baseline_bias_values = [
            float(baseline_judge_rows[key].get("gpt5mini_bias_delta", {}).get(metric))
            for key in judge_keys
            if baseline_judge_rows[key].get("gpt5mini_bias_delta", {}).get(metric) is not None
        ]
        variant_bias_values = [
            float(variant_judge_rows[key].get("gpt5mini_bias_delta", {}).get(metric))
            for key in judge_keys
            if variant_judge_rows[key].get("gpt5mini_bias_delta", {}).get(metric) is not None
        ]
        if baseline_bias_values or variant_bias_values:
            baseline_mean = _mean(baseline_bias_values)
            variant_mean = _mean(variant_bias_values)
            bias_deltas[metric] = {
                "baseline_mean": baseline_mean,
                "variant_mean": variant_mean,
                "delta": None
                if baseline_mean is None or variant_mean is None
                else variant_mean - baseline_mean,
            }
    return metric_deltas, bias_deltas


def _blocking_reasons(
    matched_keys: list[str],
    baseline_rows: dict[str, dict[str, Any]],
    variant_rows: dict[str, dict[str, Any]],
) -> tuple[list[str], list[dict[str, Any]]]:
    reasons: set[str] = set()
    rows: list[dict[str, Any]] = []
    for key in matched_keys:
        baseline_a = _category_a(baseline_rows[key])
        variant_a = _category_a(variant_rows[key])
        if baseline_a.get("schema_valid") is True and variant_a.get("schema_valid") is False:
            reasons.add("schema_valid_regression")
            rows.append({"row_id": key, "reason": "schema_valid_regression"})
    for key, row in variant_rows.items():
        variant_a = _category_a(row)
        if int(_coerce_value(variant_a.get("boundary_violation_count")) or 0) > 0:
            reasons.add("boundary_violation")
            rows.append({"row_id": key, "reason": "boundary_violation"})
    return sorted(reasons), rows


def _write_outputs(
    output_dir: Path,
    summary: dict[str, Any],
    matched_keys: list[str],
    baseline_rows: dict[str, dict[str, Any]],
    variant_rows: dict[str, dict[str, Any]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "diff-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with (output_dir / "diff-details.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["row_id", "prompt_id", "repetition_index", "metric", "baseline", "variant", "delta", "classification"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key in matched_keys:
            baseline_row = baseline_rows[key]
            variant_row = variant_rows[key]
            prompt_id = baseline_row["prompt_id"]
            repetition_index = baseline_row.get("repetition_index", 1)
            for metric in CATEGORY_A_FIELDS:
                baseline_value = _category_a(baseline_row).get(metric)
                variant_value = _category_a(variant_row).get(metric)
                baseline_numeric = _numeric(baseline_value)
                variant_numeric = _numeric(variant_value)
                writer.writerow(
                    {
                        "row_id": key,
                        "prompt_id": prompt_id,
                        "repetition_index": repetition_index,
                        "metric": metric,
                        "baseline": baseline_value,
                        "variant": variant_value,
                        "delta": None
                        if baseline_numeric is None or variant_numeric is None
                        else variant_numeric - baseline_numeric,
                        "classification": "blocking"
                        if metric in {"schema_valid", "boundary_violation_count"}
                        else "advisory",
                    }
                )

    report = _render_markdown(summary)
    (output_dir / "diff-report.md").write_text(report, encoding="utf-8")


def _render_markdown(summary: dict[str, Any]) -> str:
    decision = summary["decision"]
    lines = [
        "# Form AI Eval Diff Report",
        "",
        "## Runs",
        "",
        f"- Baseline: `{summary['baseline']['run_id']}`",
        f"- Variant: `{summary['variant']['run_id']}`",
        "",
        "## Structural Summary",
        "",
        f"- Matched rows: {summary['row_alignment']['matched_count']}",
        f"- Missing in variant: {len(summary['row_alignment']['missing_in_variant'])}",
        f"- Extra in variant: {len(summary['row_alignment']['extra_in_variant'])}",
        "",
        "## Blocking Decision",
        "",
        f"- Blocked: `{decision['blocked']}`",
        f"- Reasons: {', '.join(decision['blocking_reasons']) if decision['blocking_reasons'] else 'none'}",
        "",
        "## Advisory Metric Deltas",
        "",
        "| Metric | Baseline Mean | Variant Mean | Delta |",
        "|---|---:|---:|---:|",
    ]
    for metric, payload in summary["advisory_metric_deltas"].items():
        lines.append(
            f"| {metric} | {payload['baseline_mean']} | {payload['variant_mean']} | {payload['delta']} |"
        )
    lines.extend(
        [
            "",
            "## Judge Metric Deltas",
            "",
            "| Metric | Baseline Mean | Variant Mean | p-value | Action |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for metric, payload in summary["judge_metric_deltas"].items():
        lines.append(
            f"| {metric} | {payload['baseline_mean']} | {payload['variant_mean']} | {payload['p_value']} | {payload['recommended_action']} |"
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Non-blocking deltas are advisory and require PM/SM review.",
            "- Small or statistically inconclusive Category B samples should be rerun at n=15.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _default_output_dir(baseline_run: Path, variant_run: Path) -> Path:
    return Path("_bmad-output") / "eval-runs" / f"{baseline_run.name}-vs-{variant_run.name}-diff"


def compare_runs(baseline_run: Path, variant_run: Path, output_dir: Optional[Path] = None) -> dict[str, Any]:
    baseline_run = Path(baseline_run)
    variant_run = Path(variant_run)
    output_dir = Path(output_dir) if output_dir is not None else _default_output_dir(baseline_run, variant_run)

    baseline_metadata = _load_json(baseline_run / "run-metadata.json")
    variant_metadata = _load_json(variant_run / "run-metadata.json")
    baseline_rows = _index_rows(_load_metric_rows(baseline_run))
    variant_rows = _index_rows(_load_metric_rows(variant_run))
    matched_keys = sorted(set(baseline_rows) & set(variant_rows))
    missing_in_variant = sorted(set(baseline_rows) - set(variant_rows))
    extra_in_variant = sorted(set(variant_rows) - set(baseline_rows))

    blocking_reasons, blocking_rows = _blocking_reasons(matched_keys, baseline_rows, variant_rows)
    baseline_judge = _index_judge_rows(_load_judge_summary(baseline_run))
    variant_judge = _index_judge_rows(_load_judge_summary(variant_run))
    judge_metric_deltas, judge_bias_deltas = _compare_judge_metrics(
        matched_keys, baseline_judge, variant_judge
    )
    summary = {
        "baseline": {
            "path": str(baseline_run),
            "run_id": baseline_metadata.get("run_id", baseline_run.name),
            "variant_label": baseline_metadata.get("variant_label"),
        },
        "variant": {
            "path": str(variant_run),
            "run_id": variant_metadata.get("run_id", variant_run.name),
            "variant_label": variant_metadata.get("variant_label"),
        },
        "row_alignment": {
            "matched_count": len(matched_keys),
            "missing_in_variant": missing_in_variant,
            "extra_in_variant": extra_in_variant,
        },
        "decision": {
            "blocked": bool(blocking_reasons),
            "blocking_reasons": blocking_reasons,
            "blocking_rows": blocking_rows,
            "recommendation": "revert-or-investigate" if blocking_reasons else "human-review",
        },
        "advisory_metric_deltas": _compare_advisory_metrics(
            matched_keys, baseline_rows, variant_rows
        ),
        "judge_metric_deltas": judge_metric_deltas,
        "judge_bias_deltas": judge_bias_deltas,
        "output_files": {
            "markdown": str(output_dir / "diff-report.md"),
            "csv": str(output_dir / "diff-details.csv"),
            "json": str(output_dir / "diff-summary.json"),
        },
        "limitations": [
            "Only schema_valid regressions and boundary violations are blocking.",
            "Other deltas are advisory for PM/SM decision.",
            "Inconclusive Category B results should rerun at n=15.",
        ],
    }
    _write_outputs(output_dir, summary, matched_keys, baseline_rows, variant_rows)
    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    summary = compare_runs(args.baseline_run, args.variant_run, args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
