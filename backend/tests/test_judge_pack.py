import json
import sys
from types import SimpleNamespace
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import judge_pack  # type: ignore[import-not-found]  # noqa: E402


def _write_fixture_eval_run(tmp_path: Path, run_name: str = "fixture-run") -> Path:
    run_dir = tmp_path / run_name
    run_dir.mkdir(parents=True)
    (run_dir / "run-metadata.json").write_text(
        json.dumps(
            {
                "run_id": run_name,
                "benchmark_set_version": "prompts-v1.1",
                "variant_label": "fixture-variant",
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "shared-context-bundle.json").write_text(
        json.dumps(
            {
                "schema_version": "shared-context-bundle-v1",
                "sections": [
                    {
                        "section_id": "au_locale_block",
                        "content_hash": "fixture-hash",
                        "content": "AU contract",
                    }
                ],
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
    assert (package_dir / "shared-context-bundle.json").exists()
    assert (package_dir / "judge-prompt-claude.md").exists()
    assert (package_dir / "judge-prompt-grok.md").exists()
    assert (package_dir / "judge-prompt-gpt5mini.md").exists()
    assert (package_dir / "results").is_dir()

    metadata = json.loads((package_dir / "judge-package-metadata.json").read_text(encoding="utf-8"))
    row_ids = [row["row_id"] for row in metadata["rows"]]
    assert row_ids == [
        "p01-au-neutral-r1__r01",
        "p02-au-neutral-r1__r01",
    ]
    assert metadata["rows"][0]["eval_run_id"] == 101
    assert metadata["shared_context_bundle"] == "shared-context-bundle.json"

    judge_input = (package_dir / "judge-input-batch.md").read_text(encoding="utf-8")
    assert "[SCRUBBED_EMAIL]" in judge_input
    assert "[SCRUBBED_PHONE]" in judge_input
    assert "[SCRUBBED_DATE]" in judge_input
    assert "[SCRUBBED_NAME]" in judge_input
    assert "Attendee name" in judge_input
    assert "alex@example.test" not in judge_input
    assert "identify at least one weakness per row before scoring" in judge_input
    assert "judge_model_version" in judge_input
    assert "Expected AU Signals" in judge_input
    assert "Prompt Context Section References" in judge_input


def test_judge_prompts_include_exact_output_paths(tmp_path):
    run_dir = _write_fixture_eval_run(tmp_path)
    package_dir = judge_pack.write_judge_package(run_dir)

    for judge_model, filename in judge_pack.JUDGE_OUTPUT_FILES.items():
        prompt = (package_dir / f"judge-prompt-{judge_model}.md").read_text(encoding="utf-8")
        expected_path = judge_pack._display_path(package_dir / "results" / filename)

        assert f"Save your output JSON to: `{expected_path}`" in prompt
        assert "Do not write anywhere else" in prompt
        assert f'Set judge_model to "{judge_model}"' in prompt


def test_story_6442_judge_prompt_names_h2_scope(tmp_path):
    package_dir = (
        tmp_path
        / "_bmad-output"
        / "eval-runs"
        / "story-6.4.4.2-h2-consent-v2"
        / "judge-package"
    )

    prompt = judge_pack.render_judge_prompt("claude", package_dir)

    assert "Story 6.4.4.2 H2 consent/legal rubric_v2 re-evaluation" in prompt


def test_story_646_judge_prompt_names_au_diagnostic_scope(tmp_path):
    package_dir = (
        tmp_path
        / "_bmad-output"
        / "eval-runs"
        / "story-6.4.6-au-baseline-current"
        / "judge-package"
    )

    prompt = judge_pack.render_judge_prompt("claude", package_dir)

    assert "Story 6.4.6 AU-only diagnostic baseline" in prompt


def test_judge_package_can_combine_multiple_input_runs(tmp_path):
    run_dir_a = _write_fixture_eval_run(tmp_path, "fixture-run-a")
    run_dir_b = _write_fixture_eval_run(tmp_path, "fixture-run-b")
    run_b_rows = [
        json.loads(line)
        for line in (run_dir_b / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    run_b_rows[0]["prompt_id"] = "p02-nz-neutral-r1"
    run_b_rows[1]["prompt_id"] = "p01-nz-neutral-r1"
    (run_dir_b / "metrics.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in run_b_rows),
        encoding="utf-8",
    )
    aggregate_dir = tmp_path / "fixture-aggregate"

    package_dir = judge_pack.write_judge_package(
        aggregate_dir,
        input_dirs=[run_dir_a, run_dir_b],
    )

    metadata = json.loads((package_dir / "judge-package-metadata.json").read_text(encoding="utf-8"))
    template = json.loads((package_dir / "judge-output-template.json").read_text(encoding="utf-8"))
    assert metadata["run_id"] == "fixture-aggregate"
    assert metadata["row_count"] == 4
    assert len(metadata["source_eval_run_dirs"]) == 2
    assert len(template["rows"]) == 4


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
    assert template["rows"][0]["conflicting_data_exists"] is None
    assert template["rows"][0]["likely_responsible_section_ids"] == []
    assert template["rows"][0]["confidence"] is None


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
