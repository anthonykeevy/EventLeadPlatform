# Story 6.4.3a — Single-Session Dev Prompt

**Story:** 6.4.3a — AI Eval Harness Bones  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** `C:\wt\elp\story-epic6-6.4.3a-ai-eval-harness-bones`  
**Branch:** `story/epic6-6.4.3a-ai-eval-harness-bones`  
**PR:** [#68](https://github.com/anthonykeevy/EventLeadPlatform/pull/68) — Draft PR to `master`  
**Sizing:** S-M, expected single focused session plus migration/UAT handoff.

---

## Execution Contract

Implement `docs/stories/story-6.4.3a.md` using `docs/stories/story-context-6.4.3a.xml` as the map.

This story builds the **harness bones only**:

- frozen `prompts.yaml`
- CLI baseline runner
- `log.FormAiEvalRun` migration
- Category A structural metrics
- baseline snapshot artifact
- focused tests and docs

Do not implement judge packages, rubric scoring, stats/diff tooling, prompt shrink experiments, or capability snapshot changes.

---

## Step 0 — Preflight

Run from the story worktree:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.3a-ai-eval-harness-bones" `
  -ExpectedBranch "story/epic6-6.4.3a-ai-eval-harness-bones" `
  -ReportFile "docs/stories/STORY-6.4.3a-PREFLIGHT.md"
```

If DB resolution differs between environment and `common.database`, stop and resolve before implementing persistence.

---

## Step 1 — Read Sources In Order

1. `docs/stories/story-6.4.3a.md`
2. `docs/stories/story-context-6.4.3a.xml`
3. `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`
4. `_bmad-output/planning-artifacts/EPIC-6-PROMPT-ENGINEERING-IDEATION-BRIEF.md`
5. Existing Form AI service/tests under `backend/modules/form_ai/` and `backend/tests/`
6. Existing migration style under `backend/migrations/versions/`

---

## Step 2 — Benchmark Set

Create `backend/tests/form_ai_eval/prompts.yaml` with benchmark version `prompts-v1.0` and exactly 10 rows:

1. conference event registration
2. SaaS demo lead-gen
3. NPS survey
4. gym waiver
5. wedding RSVP
6. post-event feedback
7. consultation booking
8. employee onboarding
9. scholarship application
10. charity donation

Each row needs stable `prompt_id`, prompt text, metadata, and frozen `runtimeContext`. Keep runtime context synthetic and PII-adjacent-safe.

Add loader validation so tests fail when a required field is missing.

---

## Step 3 — CLI Runner

Create `backend/tests/form_ai_eval/run.py`.

Required behavior:

- baseline-only variant support for this story
- `--hypothesis-code baseline`
- `--variant baseline`
- `--prompt-id` optional filter
- `--repetitions` default suitable for smoke testing
- concurrency cap 4
- retry-with-jitter for 429/5xx, max 3 retries
- `--max-cost-usd`
- checkpoint-on-halt
- resume from checkpoint
- JSONL/CSV outputs under `_bmad-output/eval-runs/<run-id>/`
- optional DB persistence to `log.FormAiEvalRun`

Prefer reusing the existing Form AI generation service/API path instead of duplicating generation logic. Document the chosen call path in `docs/FORM-AI-EVAL-HARNESS.md`.

---

## Step 4 — Migration

Prepare a reversible migration for `log.FormAiEvalRun`.

Do **not** run Alembic. Anthony runs migrations.

The migration must include the required logical fields from `story-6.4.3a.md` and index `(HypothesisCode, VariantLabel, PromptID)`.

If `form_ai.GenerationRun` is unavailable or named differently in the current schema, keep `GenerationRunID` nullable and document the mapping decision in gate evidence.

---

## Step 5 — Metrics And Outputs

Capture Category A metrics per generation:

- schema validity
- component count
- collision count
- boundary violation count
- attempt count
- terminal reason
- failure class
- duration
- input/output tokens
- total cost
- retry count

Persist the whole metrics payload as structured JSON so 6.4.3b/6.4.3c can enrich it without a schema migration.

---

## Step 6 — Docs And Baseline

Create `docs/FORM-AI-EVAL-HARNESS.md` with:

- architecture/data flow
- smoke baseline command
- formal baseline command
- checkpoint/resume
- cost cap
- DB persistence
- PII-adjacent handling
- future extension points for judge packages and stats

Complete `docs/stories/STORY-6.4.3a-BENCHMARK-BASELINE.md` after a smoke run. If live LLM access is unavailable, complete it with the deterministic mocked run and clearly mark live baseline as pending Anthony/UAT.

---

## Step 7 — Tests

Add focused backend tests, expected file `backend/tests/test_form_ai_eval_harness.py`, covering:

- prompt YAML loading and required fields
- frozen `runtimeContext` shape
- CLI parsing
- checkpoint write/resume
- Category A metrics shape
- DB row mapping without live LLM calls

Run focused tests first, then the backend gate per workflow.

---

## Step 8 — Gates

Use the workflow tool where practical:

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.4.3a" `
  -FocusedTestCommand "python -m pytest backend/tests/test_form_ai_eval_harness.py --tb=short" `
  -BackendGateCommand "python -m pytest --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.4.3a-GATE-EVIDENCE.md"
```

If the repo's pytest path conventions require running from `backend/`, adjust the command and record the exact working directory in gate evidence.

---

## Step 9 — UAT Handoff

Before asking Anthony for UAT:

- `STORY-6.4.3a-GATE-EVIDENCE.md` has final command summaries.
- `STORY-6.4.3a-BENCHMARK-BASELINE.md` is complete or explicitly marks the live-run gap.
- Migration command for Anthony is documented but not executed by you.
- `STORY-6.4.3a-CLOSEOUT-REPORT.md` is updated with implementation facts.
- PR diff contains no judge/rubric/stats/prompt-shrink scope.

---

## Step 10 — Closeout

Complete the mandatory closeout report because this story ships a migration and deliberately defers in-scope later harness layers to 6.4.3b/6.4.3c.

Do not mark Complete until Anthony has confirmed UAT and migration-backed persistence.
