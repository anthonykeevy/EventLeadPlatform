# Story 6.4.3c — Single-Session Dev Prompt

**Story:** 6.4.3c — Eval Diff + Statistics Tooling  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** `C:\wt\elp\story-epic6-6.4.3c-eval-diff-statistics`  
**Branch:** `story/epic6-6.4.3c-eval-diff-statistics`  
**PR:** [#71](https://github.com/anthonykeevy/EventLeadPlatform/pull/71) — merged to `master`  
**Sizing:** S, expected single focused session.

---

## Execution Contract

Implement `docs/stories/story-6.4.3c.md` using `docs/stories/story-context-6.4.3c.xml` as the map.

This story adds diff/statistics tooling only. Do not run prompt shrink sweeps or edit production prompt content.

Build order:

1. `stats.py`
2. `diff.py`
3. focused tests
4. public docs
5. sample diff output/evidence
6. closeout

---

## Step 0 — Preflight

Run from the story worktree:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.3c-eval-diff-statistics" `
  -ExpectedBranch "story/epic6-6.4.3c-eval-diff-statistics" `
  -ReportFile "docs/stories/STORY-6.4.3c-PREFLIGHT.md"
```

---

## Step 1 — Read Sources In Order

1. `docs/stories/story-6.4.3c.md`
2. `docs/stories/story-context-6.4.3c.xml`
3. `backend/tests/form_ai_eval/run.py`
4. `backend/tests/form_ai_eval/judge_ingest.py`
5. `docs/FORM-AI-EVAL-HARNESS.md`
6. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
7. `docs/stories/STORY-6.4.3b-CLOSEOUT-REPORT.md`

---

## Step 2 — Stats Module

Create `backend/tests/form_ai_eval/stats.py`.

Implement:

- Welch t-test,
- Cohen's d,
- Fisher exact,
- verdict helper,
- safe inconclusive output for tiny/degenerate samples.

Avoid adding SciPy or other dependencies unless you pause and justify first.

---

## Step 3 — Diff Tool

Create `backend/tests/form_ai_eval/diff.py`.

It must compare two eval run folders and write:

- Markdown report,
- CSV details,
- JSON summary.

It must load structural metrics and judge summaries when present.

Blocking rules:

- `schema_valid` regression blocks.
- Any `boundary_violation_count > 0` blocks.

All other deltas are advisory.

---

## Step 4 — Tests

Add:

- `backend/tests/test_eval_stats.py`
- `backend/tests/test_eval_diff.py`

No live model calls.

Cover blockers, advisory deltas, judge metrics, missing/extra rows, output files, zero variance, tiny sample, and auto-rerun recommendation.

---

## Step 5 — Docs

Create `docs/FORM-AI-EVAL-DIFF-STATS.md`.

Write it for Story 6.4.4 usage:

- how to compare baseline vs variant,
- how to interpret blocking vs advisory outcomes,
- how Welch/Fisher/Cohen's d are used,
- when to rerun at n=15,
- how to hand results to PM/SM for a ship/revert decision,
- what remains out of scope for CI automation.

---

## Step 6 — Evidence Run

Run the diff tool on available committed eval artifacts.

Suggested input:

```powershell
python -m backend.tests.form_ai_eval.diff `
  --baseline-run "_bmad-output/eval-runs/story-6.4.3a-live-full-10row-baseline" `
  --variant-run "_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline" `
  --output-dir "_bmad-output/eval-runs/story-6.4.3c-sample-diff"
```

Use the actual CLI shape you implement and record the exact command.

---

## Step 7 — Gates

Suggested:

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.4.3c" `
  -FocusedTestCommand "python -m pytest tests/test_eval_stats.py tests/test_eval_diff.py --tb=short" `
  -BackendGateCommand "python -m pytest --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.4.3c-GATE-EVIDENCE.md"
```

Adjust working directory if needed and record exact commands.

---

## Step 8 — Closeout + Stale-Field Audit

Complete `STORY-6.4.3c-CLOSEOUT-REPORT.md`.

Before merge, run:

```powershell
gh pr view 71 --json state,isDraft,mergedAt,headRefName,baseRefName,url
rg -n "Draft|Ready for UAT|Ready for UAT/SM review|Keep PR .* open|Current Focus" docs/stories/story-6.4.3c.md docs/stories/STORY-6.4.3c-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md
```

Every hit must be intentional for the current phase. Fix stale fields in a final housekeeping commit before asking Anthony to merge.
