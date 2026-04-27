import json
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import diff  # type: ignore[import-not-found]  # noqa: E402


def _metric_row(prompt_id: str, repetition_index: int, variant_label: str, **category_a):
    defaults = {
        "schema_valid": True,
        "component_count": 4,
        "collision_count": 0,
        "boundary_violation_count": 0,
        "attempt_count": 1,
        "duration_ms": 100,
        "input_tokens": 10,
        "output_tokens": 20,
        "total_cost_usd": 0.01,
    }
    defaults.update(category_a)
    return {
        "benchmark_set_version": "prompts-v1.0",
        "hypothesis_code": "fixture",
        "variant_label": variant_label,
        "prompt_id": prompt_id,
        "repetition_index": repetition_index,
        "generation_run_id": f"{variant_label}-{prompt_id}-{repetition_index}",
        "metrics": {"category_a": defaults},
    }


def _write_run(run_dir: Path, rows: list[dict], *, run_id: str):
    run_dir.mkdir(parents=True)
    (run_dir / "run-metadata.json").write_text(
        json.dumps({"run_id": run_id, "variant_label": rows[0]["variant_label"] if rows else run_id}),
        encoding="utf-8",
    )
    (run_dir / "metrics.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_judge_summary(run_dir: Path, variant_label: str, scores: list[float]):
    package_dir = run_dir / "judge-package"
    package_dir.mkdir()
    summary = {
        "rubric_version": "rubric_v1",
        "row_count": len(scores),
        "rows": [
            {
                "row_id": f"p-0{index}__r01",
                "prompt_id": f"p-0{index}",
                "repetition_index": 1,
                "variant_label": variant_label,
                "cross_model_mean": {
                    "field_coverage_recall": score,
                    "field_label_f1": score,
                    "validation_intent_accuracy": score,
                    "row_group_agreement": score,
                    "locale_fidelity": score,
                    "copy_quality_score": score,
                },
                "gpt5mini_bias_delta": {"field_coverage_recall": 0.2},
                "judge_agreement_score": 0.9,
            }
            for index, score in enumerate(scores, start=1)
        ],
    }
    (package_dir / "judge-ingest-summary.json").write_text(json.dumps(summary), encoding="utf-8")


def test_compare_runs_flags_blocking_schema_and_boundary_regressions(tmp_path):
    baseline = tmp_path / "baseline"
    variant = tmp_path / "variant"
    _write_run(
        baseline,
        [
            _metric_row("p-01", 1, "baseline", schema_valid=True),
            _metric_row("p-02", 1, "baseline", boundary_violation_count=0),
        ],
        run_id="baseline",
    )
    _write_run(
        variant,
        [
            _metric_row("p-01", 1, "variant", schema_valid=False),
            _metric_row("p-02", 1, "variant", boundary_violation_count=1),
        ],
        run_id="variant",
    )

    summary = diff.compare_runs(baseline, variant, tmp_path / "out")

    assert summary["decision"]["blocked"] is True
    assert "schema_valid_regression" in summary["decision"]["blocking_reasons"]
    assert "boundary_violation" in summary["decision"]["blocking_reasons"]


def test_compare_runs_ignores_boundary_violations_on_extra_variant_rows(tmp_path):
    baseline = tmp_path / "baseline"
    variant = tmp_path / "variant"
    _write_run(
        baseline,
        [_metric_row("p-01", 1, "baseline", boundary_violation_count=0)],
        run_id="baseline",
    )
    _write_run(
        variant,
        [
            _metric_row("p-01", 1, "variant", boundary_violation_count=0),
            _metric_row("p-extra", 1, "variant", boundary_violation_count=1),
        ],
        run_id="variant",
    )

    summary = diff.compare_runs(baseline, variant, tmp_path / "out")

    assert summary["row_alignment"]["matched_count"] == 1
    assert summary["row_alignment"]["extra_in_variant"] == ["p-extra__r01"]
    assert summary["decision"]["blocked"] is False
    assert summary["decision"]["blocking_reasons"] == []
    assert summary["decision"]["blocking_rows"] == []


def test_compare_runs_reports_advisory_deltas_missing_extra_rows_and_outputs(tmp_path):
    baseline = tmp_path / "baseline"
    variant = tmp_path / "variant"
    output = tmp_path / "out"
    _write_run(
        baseline,
        [
            _metric_row("p-01", 1, "baseline", component_count=4),
            _metric_row("p-02", 1, "baseline", component_count=5),
        ],
        run_id="baseline",
    )
    _write_run(
        variant,
        [
            _metric_row("p-01", 1, "variant", component_count=7, attempt_count=2),
            _metric_row("p-03", 1, "variant", component_count=6),
        ],
        run_id="variant",
    )

    summary = diff.compare_runs(baseline, variant, output)

    assert summary["row_alignment"]["matched_count"] == 1
    assert summary["row_alignment"]["missing_in_variant"] == ["p-02__r01"]
    assert summary["row_alignment"]["extra_in_variant"] == ["p-03__r01"]
    assert summary["advisory_metric_deltas"]["component_count"]["delta"] == 3
    assert (output / "diff-report.md").exists()
    assert (output / "diff-details.csv").exists()
    assert (output / "diff-summary.json").exists()


def test_compare_runs_includes_judge_metrics_and_auto_rerun_recommendation(tmp_path):
    baseline = tmp_path / "baseline"
    variant = tmp_path / "variant"
    _write_run(
        baseline,
        [_metric_row(f"p-0{index}", 1, "baseline") for index in range(1, 4)],
        run_id="baseline",
    )
    _write_run(
        variant,
        [_metric_row(f"p-0{index}", 1, "variant") for index in range(1, 4)],
        run_id="variant",
    )
    _write_judge_summary(baseline, "baseline", [4.0, 4.2, 3.8])
    _write_judge_summary(variant, "variant", [4.1, 4.0, 3.9])

    summary = diff.compare_runs(baseline, variant, tmp_path / "out")

    metric = summary["judge_metric_deltas"]["field_coverage_recall"]
    assert metric["baseline_mean"] == 4.0
    assert metric["variant_mean"] == 4.0
    assert metric["recommended_action"] == "rerun-at-n15"
    assert summary["judge_bias_deltas"]["field_coverage_recall"]["variant_mean"] == 0.2
