# Story 6.4.7 Single-Session Analyst Prompt

> File name retained for Epic 6 workflow compatibility. This is an Analyst-owned story, not a Dev implementation story.

You are executing **Story 6.4.7 - AU Baseline Analysis And Iterative Prompt Improvement Loop**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.7-au-baseline-analyst-loop`  
**Branch:** `story/epic6-6.4.7-au-baseline-analyst-loop`  
**PR:** [#84](https://github.com/anthonykeevy/EventLeadPlatform/pull/84) - Draft PR to `master`  
**Base:** `master` at or after commit `602b855`

---

## Mission

Use the frozen Story 6.4.6 AU baseline to propose and test one controlled prompt/context improvement for the Australian launch market.

You must:

1. Review the baseline evidence and identify the top five candidate improvements.
2. Present those candidates to Tony with risk and bundleability guidance.
3. Stop for Tony approval.
4. After approval, run one controlled Analyst experiment.
5. Coordinate judge outputs, ingest results, compare against the frozen baseline, update `AU-001`, and stop for Tony's decision.

Do not make application, backend, frontend, harness, judge-ingest, or migration code changes.

---

## Read First

1. `docs/stories/story-6.4.7.md`
2. `docs/stories/story-context-6.4.7.xml`
3. `docs/stories/STORY-6.4.7-UAT-TEST-GUIDE.md`
4. `docs/stories/STORY-6-AU-EVAL-ANALYST-LOOP.md`
5. `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`
6. `docs/stories/STORY-6.4.6-AU-BASELINE-EVIDENCE.md`
7. `docs/FORM-AI-EVAL-HARNESS.md`
8. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
9. `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/judge-ingest-summary.json`
10. `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/au-deterministic-checks.json`
11. `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/aggregate-summary.json`

---

## Step 0 - Preflight

Run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.7-au-baseline-analyst-loop" `
  -ExpectedBranch "story/epic6-6.4.7-au-baseline-analyst-loop" `
  -ReportFile "docs/stories/STORY-6.4.7-PREFLIGHT.md"
```

Verify:

- PR #84 exists and targets `master`.
- Story 6.4.6 PR #82 is merged.
- `story-6.4.6-au-baseline-current` artifacts exist.
- You are not in the Story 6.4.6 worktree.

If any precondition fails, stop and report it.

---

## Step 1 - Baseline Analysis

Review `AU-000` and the frozen baseline artifacts.

Analyse:

- Weakest rows.
- Weakest metrics.
- Deterministic AU failures.
- Judge conflict findings.
- Judge disagreement.
- Likely responsible prompt/context sections.
- Judge-suggested corrections.

Do not edit prompt text in this step.

---

## Step 2 - Top Five Candidate Improvements

Prepare a concise proposal with five candidate prompt/context improvements.

For each candidate, include:

- Target prompt/context section.
- Evidence from baseline.
- Expected metric movement.
- Known risk.
- Whether it can be safely bundled with any other candidate.

Recommend one controlled change set. Then stop and ask Tony to approve, reject, or revise.

---

## Step 3 - Approved Experiment Config

Only after Tony approval, create an experiment config under `docs/stories/experiments/`.

Recommended naming:

```text
docs/stories/experiments/story-6.4.7-au-001.json
docs/stories/experiments/story-6.4.7-au-001-candidate-a.md
```

Config shape:

```json
{
  "experiment_id": "story-6.4.7-au-001",
  "baseline_run_id": "story-6.4.6-au-baseline-current",
  "improvement_goal": "replace-with-approved-goal",
  "target_metrics": ["locale_fidelity", "cross_locale_leakage", "format_pattern_accuracy"],
  "prompts_path": "backend/tests/form_ai_eval/prompts_au_v1.yaml",
  "scenario_slice": "au-all",
  "concurrency": 4,
  "candidates": [
    {
      "label": "candidate-a",
      "run_id": "story-6.4.7-au-001-candidate-a",
      "hypothesis": "Replace with approved hypothesis.",
      "changed_section_id": "candidate_prompt_block",
      "system_prompt_addendum_file": "docs/stories/experiments/story-6.4.7-au-001-candidate-a.md",
      "expected_metric_movement": {
        "locale_fidelity": "increase",
        "cross_locale_leakage": "increase",
        "format_pattern_accuracy": "increase"
      },
      "known_risk_metrics": ["field_label_f1", "copy_quality_score"]
    }
  ]
}
```

Use explicit `prompt_ids` instead of `scenario_slice` if Tony approves a smaller slice.

---

## Step 4 - Run Candidate Experiment

From the story worktree root:

```powershell
python -m backend.tests.form_ai_eval.experiment docs/stories/experiments/story-6.4.7-au-001.json
```

Expected output:

```text
_bmad-output/eval-runs/story-6.4.7-au-001/
  experiment-summary.json
  tracking-row-payload.json
  tracking-row-payload.md
  story-6.4.7-au-001-candidate-a/
    metrics.jsonl
    summary.csv
    run-metadata.json
    shared-context-bundle.json
    judge-package/
  diffs/
```

Never overwrite `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/`.

---

## Step 5 - Cursor Judge Sessions

Use the generated judge prompts under the candidate run's `judge-package/`.

Run one Cursor judge session each for:

- Claude
- Grok
- GPT-5 mini

Save each output to the exact path embedded in the judge prompt. Then ingest:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.7-au-001/story-6.4.7-au-001-candidate-a/judge-package
```

If judge sessions expose a framework/tooling bug, stop and raise a Dev-owned fix story.

---

## Step 6 - Compare And Decide

Compare the candidate to the frozen baseline using:

- Candidate `summary.csv`.
- Candidate `au-deterministic-checks.json`.
- Candidate `judge-ingest-summary.json`.
- Diff artifacts under `diffs/`.
- `tracking-row-payload.md`.
- Baseline `AU-000`.

Summarise:

- What was expected.
- What actually moved.
- Which metrics improved.
- Which metrics regressed.
- Which individual rows improved/regressed.
- Whether deterministic AU failures improved.
- Whether judge conflict findings changed.
- Recommendation: keep / reject / revise.

Stop for Tony decision.

---

## Step 7 - Tracking And Evidence

Update `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md` with `AU-001`.

Create or update Story 6.4.7 evidence docs if needed:

- `docs/stories/STORY-6.4.7-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.7-UAT-RESULTS.md`
- `docs/stories/STORY-6.4.7-CLOSEOUT-REPORT.md`

Record Tony's decision and evidence links.

---

## Step 8 - Focused Green Gate

Run focused tests:

```powershell
python -m pytest backend/tests/test_form_ai_eval_experiment.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py backend/tests/test_eval_diff.py --tb=short
```

Frontend checks are required only if frontend files are touched. They should not be touched in this story.

Record exact final summaries in `STORY-6.4.7-GATE-EVIDENCE.md`.

---

## Hard Stop Conditions

Stop and report before continuing if:

- Tony has not approved the selected change set.
- The experiment requires Python/app/harness code changes.
- The candidate would overwrite or mutate the 6.4.6 baseline folder.
- Judge ingest fails for a tooling reason that requires code changes.
- Results suggest a second loop; ask Tony before starting it.
