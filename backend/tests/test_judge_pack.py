import json
import sys
from types import SimpleNamespace
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import judge_pack  # noqa: E402


def _write_fixture_eval_run(tmp_path: Path) -> Path:
    run_dir = tmp_path / "fixture-run"
    run_dir.mkdir(parents=True)
    (run_dir / "run-metadata.json").write_text(
        json.dumps(
            {
                "run_id": "fixture-run",
                "benchmark_set_version": "prompts-v1.1",
                "variant_label": "fixture-variant",
            }
        ),
        encoding="utf-8",
    )
    rows = [
        {
            "benchmark_set_version": "prompts-v1.1",
            "generation_run_id": 202,
            "hypothesis_code": "baseline",
            "metrics": {"category_a": {"schema_valid": True, "component_count": 3}},
            "prompt_id": "p02-au-neutral-r1",
            "repetition_index": 1,
            "variant_label": "fixture-variant",
            "generated_definition": {"fields": [{"label": "Email", "example": "alex@example.test"}]},
        },
        {
            "benchmark_set_version": "prompts-v1.1",
            "eval_run_id": 101,
            "generation_run_id": 201,
            "hypothesis_code": "baseline",
            "metrics": {"category_a": {"schema_valid": True, "component_count": 4}},
            "prompt_id": "p01-au-neutral-r1",
            "repetition_index": 1,
            "variant_label": "fixture-variant",
            "generated_definition": {
                "fields": [
                    {
                        "label": "Attendee name",
                        "placeholder": "John Doe",
                        "help": "Call +61 400 123 456 before 2026-05-01",
                    }
                ]
            },
        },
    ]
    (run_dir / "metrics.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    return run_dir


def test_judge_package_generation_is_deterministic_and_scrubs_values(tmp_path):
    run_dir = _write_fixture_eval_run(tmp_path)

    package_dir = judge_pack.write_judge_package(run_dir)

    assert (package_dir / "rubric_v2.md").exists()
    assert (package_dir / "judge-input-batch.md").exists()
    assert (package_dir / "judge-output-template.json").exists()
    assert (package_dir / "results").is_dir()

    metadata = json.loads((package_dir / "judge-package-metadata.json").read_text(encoding="utf-8"))
    row_ids = [row["row_id"] for row in metadata["rows"]]
    assert row_ids == [
        "p01-au-neutral-r1__r01",
        "p02-au-neutral-r1__r01",
    ]
    assert metadata["rows"][0]["eval_run_id"] == 101

    judge_input = (package_dir / "judge-input-batch.md").read_text(encoding="utf-8")
    assert "[SCRUBBED_EMAIL]" in judge_input
    assert "[SCRUBBED_PHONE]" in judge_input
    assert "[SCRUBBED_DATE]" in judge_input
    assert "[SCRUBBED_NAME]" in judge_input
    assert "Attendee name" in judge_input
    assert "alex@example.test" not in judge_input
    assert "identify at least one weakness per row before scoring" in judge_input
    assert "judge_model_version" in judge_input


def test_judge_output_template_shape(tmp_path):
    run_dir = _write_fixture_eval_run(tmp_path)
    package_dir = judge_pack.write_judge_package(run_dir)

    template = json.loads((package_dir / "judge-output-template.json").read_text(encoding="utf-8"))

    assert template["rubric_version"] == "rubric_v2"
    assert template["judge_model"] == "claude"
    assert "judge_model_version" in template
    assert len(template["rows"]) == 2
    assert set(template["rows"][0]["scores"]) == set(judge_pack.CATEGORY_B_METRICS)
    assert all(value is None for value in template["rows"][0]["scores"].values())


def test_package_can_enrich_eval_run_id_from_fake_db(tmp_path):
    run_dir = _write_fixture_eval_run(tmp_path)
    rows = [
        SimpleNamespace(
            GenerationRunID=202,
            ArtifactJson=json.dumps({"fields": [{"label": "DB field"}]}),
        )
    ]
    eval_rows = [SimpleNamespace(GenerationRunID=202, EvalRunID=302)]

    class FakeSession:
        def execute(self, statement, params):
            sql = str(statement)
            if "dbo.GenerationArtifact" in sql:
                return rows
            if "[log].[FormAiEvalRun]" in sql:
                return eval_rows
            raise AssertionError(sql)

    package_rows = judge_pack.build_package_rows(run_dir, db_session=FakeSession())
    by_prompt = {row.prompt_id: row for row in package_rows}

    assert by_prompt["p02-au-neutral-r1"].eval_run_id == 302
    assert by_prompt["p02-au-neutral-r1"].generated_definition == {
        "fields": [{"label": "Email", "example": "[SCRUBBED_EMAIL]"}]
    }
