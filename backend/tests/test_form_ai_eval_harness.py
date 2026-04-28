import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import run as eval_run  # type: ignore[import-not-found]  # noqa: E402


def test_prompt_yaml_loads_exact_frozen_set():
    prompt_set = eval_run.load_prompt_set()

    assert prompt_set.benchmark_set_version == "prompts-v1.1"
    assert len(prompt_set.prompts) == 270
    assert prompt_set.prompts[0].prompt_id == "p01-au-neutral-r1"
    assert prompt_set.prompts[-1].prompt_id == "p15-eu-adversarial-r1"


def test_prompt_loader_rejects_missing_required_field(tmp_path):
    payload = json.loads(eval_run.DEFAULT_PROMPTS_PATH.read_text(encoding="utf-8"))
    del payload["prompts"][0]["runtimeContext"]
    broken = tmp_path / "prompts.yaml"
    broken.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(eval_run.EvalHarnessError, match="missing required fields"):
        eval_run.load_prompt_set(broken)


def test_runtime_context_has_frozen_eval_shape():
    prompt_set = eval_run.load_prompt_set()

    for prompt in prompt_set.prompts:
        runtime = prompt.runtime_context
        assert runtime["canvas"]["width"] > 0
        assert runtime["canvas"]["height"] > 0
        assert "termsDefaults" in runtime
        assert runtime["audienceLocale"] == prompt.audience_locale
        assert runtime["capabilitySnapshot"]["version"] == "FORM_AI_CAPABILITY_POLICY:v1"
        assert isinstance(runtime["componentFootprints"], list)
        assert runtime["componentFootprints"]


def test_cli_parsing_accepts_story_644_hypothesis_variants(tmp_path):
    args = eval_run.parse_args(
        [
            "--variant",
            "candidate",
            "--hypothesis-code",
            "H1",
            "--variant-label",
            "h1-locale-one-line",
            "--prompt-id",
            "p03-au-neutral-r1",
            "--repetitions",
            "2",
            "--concurrency",
            "4",
            "--max-cost-usd",
            "1",
            "--output-root",
            str(tmp_path),
        ]
    )

    assert args.variant == "candidate"
    assert args.hypothesis_code == "H1"
    assert args.variant_label == "h1-locale-one-line"
    assert args.prompt_id == ["p03-au-neutral-r1"]
    assert args.repetitions == 2
    assert args.prompt_shrink_mode == "h2-h4"

    with pytest.raises(SystemExit):
        eval_run.parse_args(["--concurrency", "5"])


def test_cli_infers_story_6442_prompt_shrink_modes():
    h2_args = eval_run.parse_args(["--variant", "story-6.4.4.2-h2-consent-v2"])
    h4_args = eval_run.parse_args(["--variant", "story-6.4.4.2-h4-operational-trim-v2"])
    subset_args = eval_run.parse_args(["--variant", "story-6.4.4.2-h2-h4-accepted-v2"])
    explicit_args = eval_run.parse_args(
        [
            "--variant",
            "manual-control",
            "--prompt-shrink-mode",
            "baseline",
        ]
    )

    assert h2_args.prompt_shrink_mode == "h2"
    assert h4_args.prompt_shrink_mode == "h4"
    assert subset_args.prompt_shrink_mode == "h2-h4"
    assert explicit_args.prompt_shrink_mode == "baseline"


def test_checkpoint_write_and_resume(tmp_path):
    checkpoint = tmp_path / "checkpoint.json"

    eval_run.write_checkpoint(
        checkpoint,
        run_id="run-1",
        completed_keys=["p-01#1", "p-02#1"],
        halt_reason="max-cost-usd",
        total_cost_usd=0.25,
    )

    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert payload["benchmark_set_version"] == "prompts-v1.1"
    assert payload["halt_reason"] == "max-cost-usd"
    assert eval_run._checkpoint_completed(checkpoint) == {"p-01#1", "p-02#1"}


def test_category_a_metrics_shape_from_mock_response():
    prompt = eval_run.load_prompt_set().prompts[0]
    response = eval_run._mock_generate(prompt)

    metrics = eval_run._metrics_from_response(response, duration_ms=123, retry_count=2)

    assert set(eval_run.CATEGORY_A_FIELDS).issubset(metrics)
    assert set(eval_run.CATEGORY_A_FIELDS) == set(metrics["category_a"])
    assert metrics["schema_valid"] is True
    assert metrics["component_count"] > 0
    assert metrics["retry_count"] == 2
    assert metrics["category_b"] is None
    assert metrics["category_c"] is None


def test_runner_writes_jsonl_csv_metadata_without_live_llm(tmp_path):
    args = eval_run.parse_args(
        [
            "--mock",
            "--prompt-id",
            "p02-au-neutral-r1",
            "--repetitions",
            "2",
            "--run-id",
            "unit-run",
            "--output-root",
            str(tmp_path),
        ]
    )

    metadata = eval_run.run_harness(args)

    run_dir = tmp_path / "unit-run"
    jsonl_rows = [
        json.loads(line)
        for line in (run_dir / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert metadata["benchmark_set_version"] == "prompts-v1.1"
    assert metadata["concurrency_cap"] == 4
    assert len(jsonl_rows) == 2
    assert jsonl_rows[0]["generated_definition"]["schemaVersion"] == "1.0"
    assert jsonl_rows[0]["generated_definition"]["pages"]
    assert (run_dir / "summary.csv").exists()
    assert (run_dir / "run-metadata.json").exists()


def test_runner_sets_prompt_shrink_env_and_restores(tmp_path, monkeypatch):
    monkeypatch.setenv(eval_run.PROMPT_SHRINK_MODE_ENV, "baseline")
    seen_modes = []

    def fake_generate(prompt):
        seen_modes.append(os.environ.get(eval_run.PROMPT_SHRINK_MODE_ENV))
        return eval_run._mock_generate(prompt)

    args = eval_run.parse_args(
        [
            "--variant",
            "story-6.4.4.2-h2-consent-v2",
            "--mock",
            "--prompt-id",
            "p02-au-neutral-r1",
            "--run-id",
            "h2-env-run",
            "--output-root",
            str(tmp_path),
        ]
    )

    metadata = eval_run.run_harness(args, call_generation=fake_generate)

    assert seen_modes == ["h2"]
    assert metadata["prompt_shrink_mode"] == "h2"
    assert os.environ[eval_run.PROMPT_SHRINK_MODE_ENV] == "baseline"


def test_resume_keeps_existing_rows_and_skips_completed_work(tmp_path):
    first_args = eval_run.parse_args(
        [
            "--mock",
            "--prompt-id",
            "p02-au-neutral-r1",
            "--repetitions",
            "1",
            "--run-id",
            "resume-run",
            "--output-root",
            str(tmp_path),
        ]
    )
    eval_run.run_harness(first_args)
    checkpoint = tmp_path / "resume-run" / "checkpoint.json"
    eval_run.write_checkpoint(
        checkpoint,
        run_id="resume-run",
        completed_keys=["p02-au-neutral-r1#1"],
        halt_reason="test-resume",
        total_cost_usd=0,
    )

    resume_args = eval_run.parse_args(
        [
            "--mock",
            "--prompt-id",
            "p02-au-neutral-r1",
            "--repetitions",
            "2",
            "--resume",
            str(checkpoint),
            "--output-root",
            str(tmp_path),
        ]
    )
    eval_run.run_harness(resume_args)

    jsonl_rows = [
        json.loads(line)
        for line in (tmp_path / "resume-run" / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert [row["repetition_index"] for row in jsonl_rows] == [1, 2]


def test_mock_runner_persists_eval_row_when_enabled(tmp_path, monkeypatch):
    class FakeSession:
        def __init__(self):
            self.inserted = []
            self.committed = False
            self.closed = False

        def execute(self, statement, params):
            assert "INSERT INTO [log].[FormAiEvalRun]" in str(statement)
            self.inserted.append(params)

        def commit(self):
            self.committed = True

        def rollback(self):
            raise AssertionError("rollback should not run for successful mock persist")

        def close(self):
            self.closed = True

    fake_session = FakeSession()

    import common.database

    monkeypatch.setattr(common.database, "SessionLocal", lambda: fake_session)
    args = eval_run.parse_args(
        [
            "--mock",
            "--persist-db",
            "--prompt-id",
            "p03-au-neutral-r1",
            "--repetitions",
            "1",
            "--run-id",
            "mock-persist-run",
            "--output-root",
            str(tmp_path),
        ]
    )

    eval_run.run_harness(args)

    assert len(fake_session.inserted) == 1
    assert fake_session.inserted[0]["prompt_id"] == "p03-au-neutral-r1"
    assert fake_session.inserted[0]["benchmark_set_version"] == "prompts-v1.1"
    assert fake_session.committed is True
    assert fake_session.closed is True


def test_runner_flushes_partial_outputs_when_later_prompt_fails(tmp_path):
    prompt_set = eval_run.load_prompt_set()
    responses = {prompt_set.prompts[0].prompt_id: eval_run._mock_generate(prompt_set.prompts[0])}

    def flaky_generation(prompt):
        if prompt.prompt_id in responses:
            return responses[prompt.prompt_id]
        raise RuntimeError("provider failed after first completed row")

    args = eval_run.parse_args(
        [
            "--prompt-id",
            prompt_set.prompts[0].prompt_id,
            "--prompt-id",
            prompt_set.prompts[1].prompt_id,
            "--repetitions",
            "1",
            "--run-id",
            "partial-flush-run",
            "--output-root",
            str(tmp_path),
        ]
    )

    with pytest.raises(RuntimeError, match="provider failed"):
        eval_run.run_harness(args, call_generation=flaky_generation)

    run_dir = tmp_path / "partial-flush-run"
    jsonl_rows = [
        json.loads(line)
        for line in (run_dir / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    metadata = json.loads((run_dir / "run-metadata.json").read_text(encoding="utf-8"))
    checkpoint = json.loads((run_dir / "checkpoint.json").read_text(encoding="utf-8"))

    assert len(jsonl_rows) == 1
    assert jsonl_rows[0]["prompt_id"] == prompt_set.prompts[0].prompt_id
    assert metadata["completed_count"] == 1
    assert metadata["status"] == "halted-error"
    assert checkpoint["completed_keys"] == [f"{prompt_set.prompts[0].prompt_id}#1"]
    assert "schema_valid" in (run_dir / "summary.csv").read_text(encoding="utf-8")


def test_db_row_mapping_and_insert_without_live_llm():
    prompt = eval_run.load_prompt_set().prompts[0]
    response = eval_run._mock_generate(prompt)
    response.generationRunId = 9001
    metrics = eval_run._metrics_from_response(response, duration_ms=10, retry_count=0)
    created = datetime(2026, 4, 25, tzinfo=timezone.utc)

    row = eval_run.build_eval_db_row(
        benchmark_set_version="prompts-v1.1",
        hypothesis_code="baseline",
        variant_label="current-master-baseline",
        prompt_id=prompt.prompt_id,
        repetition_index=1,
        response=response,
        metrics=metrics,
        created_at=created,
    )

    assert row["generation_run_id"] == 9001
    assert row["baseline_expires_at"].date().isoformat() == "2026-05-25"
    assert row["judge_rubric_version"] is None
    assert json.loads(row["metrics_json"])["category_a"]["schema_valid"] is True

    class FakeSession:
        def __init__(self):
            self.params = None

        def execute(self, statement, params):
            assert "INSERT INTO [log].[FormAiEvalRun]" in str(statement)
            self.params = params

    fake = FakeSession()
    eval_run.insert_eval_db_row(fake, row)
    assert fake.params["benchmark_set_version"] == "prompts-v1.1"
