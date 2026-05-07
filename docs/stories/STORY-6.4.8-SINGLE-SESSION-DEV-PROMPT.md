# Story 6.4.8 Single-Session Dev Prompt

You are implementing **Story 6.4.8 - Promote AU-005 Into Production Prompt Context**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.8-au-production-prompt-context`  
**Branch:** `story/epic6-6.4.8-au-production-prompt-context`  
**PR:** [#85](https://github.com/anthonykeevy/EventLeadPlatform/pull/85) - Draft PR to `master`  
**Base:** `master` at or after PR #84 merge commit `61de75c`

---

## Mission

Promote Story 6.4.7's winning AU prompt behaviour into the production Form AI prompt/context path.

Use:

- `AU-005` as the behaviour target.
- `AU-006` as the lint-clean wording lesson.

Do not copy an eval-only overlay into production literally. Implement the behaviour in the production context store and prove it with focused tests and AU eval evidence.

---

## Read First

1. `docs/stories/story-6.4.8.md`
2. `docs/stories/story-context-6.4.8.xml`
3. `docs/stories/STORY-6.4.8-UAT-TEST-GUIDE.md`
4. `docs/stories/STORY-6.4.7-CLOSEOUT-REPORT.md`
5. `docs/stories/STORY-6-AU-EVAL-ITERATION-TRACKING.md`
6. `docs/FORM-AI-EVAL-HARNESS.md`
7. `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
8. `backend/modules/form_ai/service.py`
9. `backend/migrations/versions/063_story_6441_prompt_template_locale_block.py`
10. `backend/migrations/versions/065_story_6441_seed_locale_blocks_au.py`
11. `backend/tests/test_form_ai_locale_assembly.py`
12. `backend/tests/test_form_ai_locale_resolution.py`
13. `backend/tests/form_ai_eval/au_locale_contract_v1.json`
14. `backend/tests/form_ai_eval/prompts_au_v1.yaml`

---

## Step 0 - Preflight

Run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.8-au-production-prompt-context" `
  -ExpectedBranch "story/epic6-6.4.8-au-production-prompt-context" `
  -ReportFile "docs/stories/STORY-6.4.8-PREFLIGHT.md"
```

Verify:

- PR #85 exists and targets `master`.
- PR #84 is merged.
- Story 6.4.7 evidence exists under `_bmad-output/eval-runs/story-6.4.7-au-005/` and `_bmad-output/eval-runs/story-6.4.7-au-006/`.
- You are not in the Story 6.4.7 worktree.

If any precondition fails, stop and report it.

---

## Step 1 - Implementation Plan

Before editing, identify the smallest production change that implements the behaviour.

Expected path:

- Add a new migration after current head to update AU rows in `config.PromptTemplateLocaleBlock`.
- Keep `backend/modules/form_ai/service.py` unchanged unless production prompt assembly cannot express the required behaviour via the context store.
- Update tests to validate the new AU block text/behaviour and fallback remains sane.

Do not mutate old migrations.

Do not run Alembic.

---

## Step 2 - Production Context Store Update

Implement production AU prompt context with these requirements:

- `audienceLocale = AU` is authoritative.
- AU conventions cover phone, dates, address labels, currency, privacy, marketing-message consent, waivers, terms, and acknowledgements.
- Foreign-market cues conflicting with AU are converted to Australian equivalents unless the form explicitly collects an external destination/source-market value.
- Wording is lint-clean: describe categories/substitution behaviour, not long lists of forbidden examples.
- Legal/policy text stays explicit: Privacy Act 1988, Spam Act 2003, and AU-appropriate consent/terms/acknowledgement behaviour.
- Form completeness and publish-ready polish are preserved:
  - include every material field group requested,
  - make `validationIntent` clear,
  - choose the most specific supported component type,
  - preserve requested sections/options,
  - order identity/contact, form-specific choices, operational notes/preferences, then consent/terms,
  - avoid unnecessary extra fields,
  - prefer checkbox/terms acknowledgement over typed signature unless signature is requested.
- Include the p11 guard: avoid generated timezone options/labels that introduce foreign phone-code-like strings or overseas region names unless explicitly collecting external values.

---

## Step 3 - Tests

Run focused tests after implementation:

```powershell
python -m pytest `
  backend/tests/test_form_ai_locale_assembly.py `
  backend/tests/test_form_ai_locale_resolution.py `
  backend/tests/test_story_6441_migrations_static.py `
  backend/tests/test_form_ai_eval_harness.py `
  backend/tests/test_form_ai_eval_experiment.py `
  backend/tests/test_judge_pack.py `
  backend/tests/test_judge_ingest.py `
  backend/tests/test_eval_diff.py `
  --tb=short
```

If migration static tests need an update for the new migration, update tests rather than weakening them.

Record exact output in `docs/stories/STORY-6.4.8-GATE-EVIDENCE.md`.

---

## Step 4 - AU Production Candidate Eval

Run an AU eval that exercises the production prompt/context path.

Use a new immutable run ID, for example:

```text
story-6.4.8-au-production-context
```

Expected shape:

```powershell
python -m backend.tests.form_ai_eval.run `
  --prompts-path backend/tests/form_ai_eval/prompts_au_v1.yaml `
  --variant production-context `
  --hypothesis-code production-au-context `
  --variant-label story-6.4.8-au-production-context `
  --run-id story-6.4.8-au-production-context `
  --concurrency 4
```

Do not pass `--system-prompt-addendum`.

If a full 45-row live run is too expensive/time-consuming, run a targeted slice first and document the limitation. Include p11 rows either way.

---

## Step 5 - Judge Package And Ingest

Generate the judge package:

```powershell
python -m backend.tests.form_ai_eval.judge_pack `
  _bmad-output/eval-runs/story-6.4.8-au-production-context `
  --prompts-path backend/tests/form_ai_eval/prompts_au_v1.yaml `
  --use-db
```

Tony runs/saves the judge outputs if manual Cursor judge sessions are required.

Then ingest:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest `
  _bmad-output/eval-runs/story-6.4.8-au-production-context/judge-package
```

Record exact paths and summaries in gate evidence.

---

## Step 6 - Compare Against Baseline / AU-005 / AU-006

Compare candidate evidence against:

- Baseline: `story-6.4.6-au-baseline-current`
- Behaviour target: `story-6.4.7-au-005-candidate-a`
- Lint-clean lesson: `story-6.4.7-au-006-candidate-a`

Required checks:

- Prompt-context lint is `0`.
- Generated-output deterministic findings are materially below baseline `130`, and preferably close to AU-006's `3`.
- Judge score remains close to AU-005's `4.471 / 5`.
- Candidate does not repeat AU-006 regressions in `policy_compliance`, `validation_intent_accuracy`, or `copy_quality_score`.
- p11 rows are reviewed explicitly.

---

## Step 7 - Migration Handoff

If a migration was added, include exact commands for Tony to run.

Do not run them yourself.

Example format:

```powershell
cd backend
alembic upgrade head
```

Also document:

- Migration file name.
- What rows it updates/inserts.
- Downgrade behaviour.
- How to verify seeded rows after Tony applies it.

---

## Step 8 - Closeout

Before asking for UAT/merge:

1. Fill `docs/stories/STORY-6.4.8-GATE-EVIDENCE.md`.
2. Fill `docs/stories/STORY-6.4.8-UAT-RESULTS.md`.
3. Fill `docs/stories/STORY-6.4.8-CLOSEOUT-REPORT.md`.
4. Update `docs/stories/story-6.4.8.md`, `EPIC-6-STATUS.md`, and `EPIC-6-WORKFLOW-GUIDE.md`.
5. Run SM stale-field audit.

Expected next-story routing:

- If production prompt context passes: resume the planned Epic 6 roadmap (`6.5a` / image-to-form sequencing decision).
- If prompt context misses AU-005 quality: create the smallest follow-up prompt refinement story with evidence.
