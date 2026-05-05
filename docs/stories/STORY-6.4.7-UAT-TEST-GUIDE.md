# Story 6.4.7 - UAT Test Guide

**Story:** 6.4.7 - AU Baseline Analysis And Iterative Prompt Improvement Loop  
**UAT owner:** Tony + SM  
**Mode:** Evidence review + controlled Analyst experiment + Cursor judge sessions

This story validates that the Analyst loop uses the frozen Story 6.4.6 AU baseline correctly, tests one approved prompt/context change set, and stops for Tony's decision.

---

## Section 1 - Baseline Review

Review the Analyst's baseline analysis.

Pass criteria:

- `AU-000` baseline row is referenced.
- Deterministic AU findings are reviewed.
- Judge conflict findings are reviewed before prompt text changes.
- Low-scoring rows and judge disagreement are considered, not just aggregate mean.
- Likely responsible prompt/context sections are identified.

**Section 1 Final:** Pass / Fail

---

## Section 2 - Candidate Proposal Gate

Review the top five candidate improvements before any experiment edit.

Pass criteria:

- Five candidates are listed.
- Each candidate has evidence, target section, expected movement, risk, and bundleability.
- Analyst recommends one controlled change set.
- Tony approval is recorded before edits/runs.

**Section 2 Final:** Pass / Fail

---

## Section 3 - Scope Boundary

Review changed files before the candidate run is accepted.

Pass criteria:

- No application/backend/frontend/harness/judge-ingest/migration code changed.
- Changes are limited to story docs, tracking docs, experiment config/overlay files, and eval output artifacts.
- If a code change is needed, the story is stopped and a Dev-owned fix story is raised.

**Section 3 Final:** Pass / Fail

---

## Section 4 - Experiment Config

Review the approved experiment config and any overlay files.

Pass criteria:

- Baseline run ID is `story-6.4.6-au-baseline-current`.
- Candidate run ID is new and immutable.
- `prompts_path` points to `backend/tests/form_ai_eval/prompts_au_v1.yaml`.
- Hypothesis and expected metric movement are explicit.
- Changed prompt/context section is recorded.
- Scenario slice or prompt IDs are stable.

**Section 4 Final:** Pass / Fail

---

## Section 5 - Candidate Eval Run

Review candidate run artifacts.

Pass criteria:

- Candidate run completes without overwriting the baseline folder.
- `run-metadata.json`, `metrics.jsonl`, `summary.csv`, shared context bundle, and AU deterministic artifacts exist.
- Experiment metadata is present.
- Diff artifacts compare candidate against the frozen baseline.

**Section 5 Final:** Pass / Fail

---

## Section 6 - Cursor Judge Sessions

For the candidate judge package:

1. Run one Cursor judge session each for Claude, Grok, and GPT-5 mini.
2. Save each output to the path embedded in its judge prompt.
3. Confirm ingest succeeds.

Pass criteria:

- Each output has `rubric_version: "rubric_v2"`.
- Each output has `judge_model` and `judge_model_version`.
- Each row includes metric scores, rationale, conflict flag, conflict description, likely responsible section IDs, suggested correction, and confidence.
- Ingest summary JSON/CSV exists and includes diagnostic fields.

**Section 6 Final:** Pass / Fail

---

## Section 7 - Candidate Comparison

Review the Analyst's comparison summary.

Pass criteria:

- Actual metric movement is compared with expected movement.
- Improved metrics and regressed metrics are listed.
- Improved/regressed individual rows are called out.
- Deterministic AU findings are compared against baseline.
- Judge disagreements are treated as review flags, not ignored.
- Recommendation is keep / reject / revise, with reason.

**Section 7 Final:** Pass / Fail

---

## Section 8 - Tracking Sheet

Review `STORY-6-AU-EVAL-ITERATION-TRACKING.md`.

Pass criteria:

- `AU-001` row is filled.
- Baseline and candidate run IDs are present.
- Prompt/context section changed and exact change are present.
- Evidence links point to candidate run, judge package, ingest outputs, and diff artifacts.
- Tony decision is recorded.

**Section 8 Final:** Pass / Fail

---

## Section 9 - Green Gate Review

Review Story 6.4.7 gate evidence.

Pass criteria:

- Focused Analyst harness tests are green, at minimum:

```powershell
python -m pytest backend/tests/test_form_ai_eval_experiment.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py backend/tests/test_eval_diff.py --tb=short
```

- Frontend lint/unit checks are not required unless frontend files were touched.
- No truncated output is treated as green.

**Section 9 Final:** Pass / Fail

---

## Section 10 - Final Decision

Review final story outcome.

Pass criteria:

- Tony's keep / reject / revise / continue decision is explicit.
- If kept, the follow-up promotion path is clear.
- If rejected or revised, the failed hypothesis and evidence remain preserved.
- The story stops before a second loop unless Tony explicitly approves continuation.

**Section 10 Final:** Pass / Fail

---

## UAT Result Summary

| Section | Result | Notes |
|---|---|---|
| Section 1 Baseline review | TBD |  |
| Section 2 Candidate proposal gate | TBD |  |
| Section 3 Scope boundary | TBD |  |
| Section 4 Experiment config | TBD |  |
| Section 5 Candidate eval run | TBD |  |
| Section 6 Cursor judge sessions | TBD |  |
| Section 7 Candidate comparison | TBD |  |
| Section 8 Tracking sheet | TBD |  |
| Section 9 Green gate | TBD |  |
| Section 10 Final decision | TBD |  |
