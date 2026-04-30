import json
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import judge_ingest, judge_pack  # type: ignore[import-not-found]  # noqa: E402
from test_judge_pack import _write_fixture_eval_run  # type: ignore[import-not-found]  # noqa: E402


def _make_score(value: float):
    return {metric: value for metric in judge_pack.CATEGORY_B_METRICS}


def _write_outputs(package_dir: Path):
    metadata = json.loads((package_dir / "judge-package-metadata.json").read_text(encoding="utf-8"))
    result_rows = []
    for row in metadata["rows"]:
        result_rows.append(
            {
                "row_id": row["row_id"],
                "prompt_id": row["prompt_id"],
                "repetition_index": row["repetition_index"],
                "variant_label": row["variant_label"],
                "scores": _make_score(4),
                "rationale": "Fixture rationale.",
                "conflicting_data_exists": False,
                "conflict_description": "",
                "likely_responsible_section_ids": [],
                "suggested_correction": "",
                "confidence": 0.9,
            }
        )
    results_dir = package_dir / "results"
    for judge_model, value in [("gpt5mini", 5), ("claude", 4), ("grok", 2)]:
        payload = {
            "rubric_version": "rubric_v2",
            "judge_model": judge_model,
            "judge_model_version": f"{judge_model}-fixture",
            "rows": [{**row, "scores": _make_score(value)} for row in result_rows],
        }
        (results_dir / f"judge-output-{judge_model}.json").write_text(
            json.dumps(payload, sort_keys=True),
            encoding="utf-8",
        )


def _package_with_outputs(tmp_path: Path) -> Path:
    run_dir = _write_fixture_eval_run(tmp_path)
    package_dir = judge_pack.write_judge_package(run_dir)
    _write_outputs(package_dir)
    return package_dir


def test_ingest_valid_outputs_writes_summary_and_aggregates(tmp_path):
    package_dir = _package_with_outputs(tmp_path)

    summary = judge_ingest.ingest_judge_package(package_dir)

    assert summary["rubric_version"] == "rubric_v2"
    assert summary["row_count"] == 2
    first = summary["rows"][0]
    assert first["cross_model_mean"]["field_coverage_recall"] == 3
    assert first["gpt5mini_bias_delta"]["field_coverage_recall"] == 2
    assert first["judge_agreement_score"] == 0.6
    assert (package_dir / "judge-ingest-summary.json").exists()
    assert (package_dir / "judge-ingest-summary.csv").exists()


def test_ingest_rejects_missing_duplicate_and_unknown_rows(tmp_path):
    package_dir = _package_with_outputs(tmp_path)
    claude_path = package_dir / "results" / "judge-output-claude.json"
    payload = json.loads(claude_path.read_text(encoding="utf-8"))
    payload["rows"] = payload["rows"][:1]
    claude_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(judge_ingest.JudgeIngestError, match="missing row IDs"):
        judge_ingest.ingest_judge_package(package_dir)

    package_dir = _package_with_outputs(tmp_path / "dup")
    claude_path = package_dir / "results" / "judge-output-claude.json"
    payload = json.loads(claude_path.read_text(encoding="utf-8"))
    payload["rows"].append(payload["rows"][0])
    claude_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(judge_ingest.JudgeIngestError, match="duplicate row IDs"):
        judge_ingest.ingest_judge_package(package_dir)

    package_dir = _package_with_outputs(tmp_path / "unknown")
    claude_path = package_dir / "results" / "judge-output-claude.json"
    payload = json.loads(claude_path.read_text(encoding="utf-8"))
    payload["rows"][0]["row_id"] = "unknown-row"
    claude_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(judge_ingest.JudgeIngestError, match="unknown row IDs"):
        judge_ingest.ingest_judge_package(package_dir)


def test_ingest_rejects_out_of_range_score(tmp_path):
    package_dir = _package_with_outputs(tmp_path)
    claude_path = package_dir / "results" / "judge-output-claude.json"
    payload = json.loads(claude_path.read_text(encoding="utf-8"))
    payload["rows"][0]["scores"]["copy_quality_score"] = 6
    claude_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(judge_ingest.JudgeIngestError, match="out of range"):
        judge_ingest.ingest_judge_package(package_dir)


def test_ingest_rejects_missing_diagnostic_fields(tmp_path):
    package_dir = _package_with_outputs(tmp_path)
    claude_path = package_dir / "results" / "judge-output-claude.json"
    payload = json.loads(claude_path.read_text(encoding="utf-8"))
    del payload["rows"][0]["conflicting_data_exists"]
    claude_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(judge_ingest.JudgeIngestError, match="conflicting_data_exists"):
        judge_ingest.ingest_judge_package(package_dir)


def test_ingest_updates_db_with_fake_session(tmp_path):
    package_dir = _package_with_outputs(tmp_path)

    class FakeSession:
        def __init__(self):
            self.params = []
            self.committed = False

        def execute(self, statement, params):
            assert "UPDATE [log].[FormAiEvalRun]" in str(statement)
            self.params.append(params)

        def commit(self):
            self.committed = True

    fake = FakeSession()
    summary = judge_ingest.ingest_judge_package(package_dir, db_session=fake)

    assert summary["db_update_status"] == "updated"
    assert summary["db_update_count"] == 2
    assert len(fake.params) == 2
    assert fake.params[0]["judge_rubric_version"] == "rubric_v2"
    assert fake.params[0]["judge_agreement_score"] == 0.6
    assert "cross_model_mean" in json.loads(fake.params[0]["bias_delta_json"])
    assert "judge_diagnostics" in json.loads(fake.params[0]["bias_delta_json"])
    assert fake.committed is True
