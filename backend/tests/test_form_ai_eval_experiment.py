import json
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import experiment, run as eval_run  # type: ignore[import-not-found]  # noqa: E402


def test_analyst_experiment_resolves_named_scenario_slices():
    prompt_ids = experiment._resolve_prompt_ids(
        {"scenario_slice": "au-neutral"},
        eval_run.DEFAULT_AU_PROMPTS_PATH,
    )

    assert len(prompt_ids) == 15
    assert all("-au-neutral-" in prompt_id for prompt_id in prompt_ids)


def test_analyst_experiment_runs_candidates_and_packages_judges(tmp_path):
    baseline_args = eval_run.parse_args(
        [
            "--mock",
            "--prompts-path",
            str(eval_run.DEFAULT_AU_PROMPTS_PATH),
            "--prompt-id",
            "p01-au-neutral-r1",
            "--prompt-id",
            "p02-au-neutral-r1",
            "--run-id",
            "baseline-run",
            "--output-root",
            str(tmp_path),
        ]
    )
    eval_run.run_harness(baseline_args)
    config = {
        "experiment_id": "story-6.4.7-validation-intent-r1",
        "baseline_run_id": "baseline-run",
        "output_root": str(tmp_path),
        "prompts_path": str(eval_run.DEFAULT_AU_PROMPTS_PATH),
        "improvement_goal": "improve-validation-intent",
        "target_metrics": ["validation_intent_accuracy", "field_coverage_recall"],
        "prompt_ids": ["p01-au-neutral-r1", "p02-au-neutral-r1"],
        "mock": True,
        "allow_au_context_conflicts": True,
        "candidates": [
            {
                "label": "candidate-a",
                "hypothesis": "Make validation intent explicit.",
                "changed_section_id": "candidate_prompt_block",
                "system_prompt_addendum": "Eval-only candidate A: prefer explicit validation intent.",
            },
            {
                "label": "candidate-b",
                "hypothesis": "Make required fields explicit.",
                "changed_section_id": "candidate_prompt_block",
                "system_prompt_addendum": "Eval-only candidate B: mark required contact fields.",
            },
        ],
    }
    config_path = tmp_path / "experiment.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    summary = experiment.run_experiment(config_path)

    experiment_dir = tmp_path / "story-6.4.7-validation-intent-r1"
    assert summary["experiment_dir"] == str(experiment_dir)
    assert len(summary["candidate_runs"]) == 2
    for candidate in summary["candidate_runs"]:
        run_dir = Path(candidate["run_dir"])
        metadata = json.loads((run_dir / "run-metadata.json").read_text(encoding="utf-8"))
        shared_context = json.loads((run_dir / "shared-context-bundle.json").read_text(encoding="utf-8"))
        candidate_section = next(
            section
            for section in shared_context["sections"]
            if section["section_id"] == "candidate_prompt_block"
        )
        judge_input = run_dir / "judge-package" / "judge-input-batch.md"
        judge_prompt = run_dir / "judge-package" / "judge-prompt-claude.md"

        assert metadata["experiment"]["experiment_id"] == config["experiment_id"]
        assert metadata["experiment"]["candidate_label"] == candidate["candidate_label"]
        assert metadata["eval_only_overlay"]["system_prompt_addendum"]["active"] is True
        assert candidate_section["active"] is True
        assert "Eval-only candidate" in candidate_section["content"]
        assert "## Experiment Context" in judge_input.read_text(encoding="utf-8")
        assert "Analyst Form AI prompt experiment" in judge_prompt.read_text(encoding="utf-8")
        assert Path(candidate["diff_dir"], "diff-summary.json").exists()

    tracking = json.loads((experiment_dir / "tracking-row-payload.json").read_text(encoding="utf-8"))
    assert tracking["candidate_count"] == 2
    assert (experiment_dir / "tracking-row-payload.md").exists()
