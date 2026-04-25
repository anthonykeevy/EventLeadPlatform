# Story 6.4.3b — Single-Session Dev Prompt

**Story:** 6.4.3b — Eval Judge Package + Rubric ADR  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** `C:\wt\elp\story-epic6-6.4.3b-eval-judge-package-rubric`  
**Branch:** `story/epic6-6.4.3b-eval-judge-package-rubric`  
**PR:** [#70](https://github.com/anthonykeevy/EventLeadPlatform/pull/70) — Draft PR to `master`  
**Sizing:** S-M, expected single focused session.

---

## Execution Contract

Implement `docs/stories/story-6.4.3b.md` using `docs/stories/story-context-6.4.3b.xml` as the map.

This story adds judge package + ingest mechanics. It does **not** run live judge model APIs, add statistics, or change prompts.

Strict build order:

1. Rubric v1.
2. Rubric ADR.
3. Judge package generator.
4. Judge JSON ingest.
5. Judge workflow documentation.
6. Focused tests and closeout.

---

## Step 0 — Preflight

Run from the story worktree:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.3b-eval-judge-package-rubric" `
  -ExpectedBranch "story/epic6-6.4.3b-eval-judge-package-rubric" `
  -ReportFile "docs/stories/STORY-6.4.3b-PREFLIGHT.md"
```

---

## Step 1 — Read Sources In Order

1. `docs/stories/story-6.4.3b.md`
2. `docs/stories/story-context-6.4.3b.xml`
3. `docs/FORM-AI-EVAL-HARNESS.md`
4. `backend/tests/form_ai_eval/run.py`
5. `backend/tests/form_ai_eval/prompts.yaml`
6. `docs/stories/STORY-6.4.2-CLOSEOUT-REPORT.md`
7. `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/`

---

## Step 2 — Rubric v1

Create `backend/tests/form_ai_eval/rubric_v1.md`.

Define Category B metrics:

- `field_coverage_recall`
- `field_label_f1`
- `validation_intent_accuracy`
- `row_group_agreement`
- `locale_fidelity`
- `copy_quality_score`

Include score anchors, required JSON shape, judge instructions, and examples.

Keep style metrics out of active rubric scoring unless clearly marked as future placeholders.

---

## Step 3 — Rubric ADR

Complete `docs/stories/STORY-6.4.3b-RUBRIC-ADR.md`.

It must explain:

- why rubric is file-versioned,
- why Cursor manual judges are used,
- why GPT-5 mini is control only,
- when `rubric_v2.md` is required,
- what baseline re-snapshot/re-score means.

---

## Step 4 — Judge Package Generator

Create `backend/tests/form_ai_eval/judge_pack.py`.

Required output:

```text
_bmad-output/eval-runs/<run-id>/judge-package/
├── rubric_v1.md
├── judge-input-batch.md
├── judge-output-template.json
└── results/
```

Package rows must be deterministic and link back to prompt/eval run identity. Scrub obvious PII-adjacent synthetic values where practical and document limitations.

---

## Step 5 — Judge Ingest

Create `backend/tests/form_ai_eval/judge_ingest.py`.

Expected result files:

- `results/judge-output-gpt5mini.json`
- `results/judge-output-claude.json`
- `results/judge-output-gemini.json`

Ingest must:

- validate shape,
- reject missing/duplicate/unknown rows,
- reject out-of-range scores,
- compute Claude+Gemini primary means,
- compute GPT-5 mini bias deltas,
- compute judge agreement score,
- write summary artifacts,
- update DB judge fields where available, or degrade cleanly when DB is unavailable.

---

## Step 6 — Judge Workflow Doc

Create `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`.

Write it for Anthony. Include exact file paths, model list, save paths, commands, disagreement handling, and PII-adjacent handling.

---

## Step 7 — Tests

Add:

- `backend/tests/test_judge_pack.py`
- `backend/tests/test_judge_ingest.py`

No live model calls.

Cover deterministic packaging, scrub behavior, template shape, ingest happy path, ingest validation failures, aggregate calculations, and DB mapping via fake/mock session.

---

## Step 8 — Gates

Suggested:

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.4.3b" `
  -FocusedTestCommand "python -m pytest backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py --tb=short" `
  -BackendGateCommand "python -m pytest --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.4.3b-GATE-EVIDENCE.md"
```

Adjust working directory if needed and record exact commands.

---

## Step 9 — Closeout + Stale-Field Audit

Complete `STORY-6.4.3b-CLOSEOUT-REPORT.md`.

Before merge, run:

```powershell
gh pr view 70 --json state,isDraft,mergedAt,headRefName,baseRefName,url
rg -n "Draft|Ready for UAT|Ready for UAT/SM review|Keep PR .* open|Current Focus" docs/stories/story-6.4.3b.md docs/stories/STORY-6.4.3b-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md
```

Every hit must be intentional for the current phase. Fix stale fields in a final housekeeping commit before asking Anthony to merge.
