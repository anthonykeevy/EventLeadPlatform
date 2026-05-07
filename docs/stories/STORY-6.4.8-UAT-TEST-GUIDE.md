# Story 6.4.8 - UAT Test Guide

**Story:** 6.4.8 - Promote AU-005 Into Production Prompt Context  
**UAT owner:** Tony + SM  
**Mode:** Evidence review + focused AU eval/judge verification

This story validates that AU-005's winning behaviour has been implemented in the production Form AI prompt/context path, while preserving AU-006's lint-clean conflict wording lesson.

---

## Section 1 - Production Context Review

Review implementation changes.

Pass criteria:

- The production prompt/context store is updated, not only eval overlays.
- If DB seed content changed, it is represented by a new migration after current head.
- Existing migrations are not rewritten.
- `config.PromptTemplateLocaleBlock` remains the source of truth for AU locale/policy/tone blocks.
- No Alembic command was run by the agent.

**Section 1 Final:** Pass / Fail

---

## Section 2 - AU-005 Behaviour Preservation

Review the production wording and implementation evidence.

Pass criteria:

- `audienceLocale = AU` is authoritative for output copy and component configuration.
- AU conventions are explicit for phone, dates, address labels, currency, privacy, marketing consent, waivers, terms, and acknowledgements.
- Form completeness, validation intent, component specificity, section ordering, and copy quality guards remain present.
- Legal/policy specificity is not generic; Privacy Act 1988 and Spam Act 2003 remain explicit.

**Section 2 Final:** Pass / Fail

---

## Section 3 - AU-006 Lint-Clean Wording

Review prompt-context lint evidence.

Pass criteria:

- Production wording avoids long forbidden-token lists.
- Conflict handling is described positively as categories/substitution behaviour.
- Prompt-context lint has `0` findings.
- The lint-clean rewrite does not repeat AU-006's policy, validation, or copy-quality regressions.

**Section 3 Final:** Pass / Fail

---

## Section 4 - p11 Risk Review

Review targeted p11-style international event/timezone evidence.

Pass criteria:

- International event/timezone prompts avoid generated foreign phone-code-like strings and overseas region names unless explicitly collecting external values.
- Legitimate external destination/source-market collection is still allowed when requested.
- Evidence explicitly calls out p11 rows.

**Section 4 Final:** Pass / Fail

---

## Section 5 - Automated Green Gate

Review `STORY-6.4.8-GATE-EVIDENCE.md`.

Pass criteria:

- Focused tests pass with exact final summaries.
- Suggested minimum focused checks:

```powershell
python -m pytest backend/tests/test_form_ai_locale_assembly.py backend/tests/test_form_ai_locale_resolution.py backend/tests/test_story_6441_migrations_static.py backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_experiment.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py backend/tests/test_eval_diff.py --tb=short
```

- Backend regression scope is explicitly justified: focused only vs full backend.
- Frontend checks are not required unless frontend files were touched.

**Section 5 Final:** Pass / Fail

---

## Section 6 - AU Eval Evidence

Review production candidate eval artifacts.

Pass criteria:

- Candidate run uses production prompt/context path, not `system_prompt_addendum`.
- Baseline comparison references `story-6.4.6-au-baseline-current`.
- AU-005 and AU-006 expectations are explicitly compared.
- Prompt-context lint remains `0`.
- Generated-output deterministic findings are materially below baseline `130`.
- p11 finding count is called out.

**Section 6 Final:** Pass / Fail

---

## Section 7 - Judge / Score Review

Review judge ingest and score comparison.

Pass criteria:

- Claude-family, Grok, and GPT-5 mini judge outputs are saved and ingested if judge verification is run.
- Candidate score remains close to AU-005's `4.471 / 5`.
- Candidate does not repeat AU-006 regressions in `policy_compliance`, `validation_intent_accuracy`, or `copy_quality_score`.
- Regressions are documented with decision rationale.

**Section 7 Final:** Pass / Fail

---

## Section 8 - Migration Handoff

If a migration is added, Tony reviews migration instructions.

Pass criteria:

- Exact Alembic command for Tony is listed.
- Expected migration ID and purpose are documented.
- Rollback/downgrade behaviour is documented.
- Agent did not execute Alembic.

**Section 8 Final:** Pass / Fail / N/A

---

## Section 9 - Final Decision

Review story closeout.

Pass criteria:

- Production promotion decision is explicit.
- Remaining prompt/eval risks are listed.
- Next recommended story is clear.

**Section 9 Final:** Pass / Fail

---

## UAT Result Summary

| Section | Result | Notes |
|---|---|---|
| Section 1 Production context review | PASS | Migration 072 + live API trace |
| Section 2 AU-005 behaviour preservation | PASS | 072 block + outbound system message |
| Section 3 AU-006 lint-clean wording | PASS | Positive categories; lint source removed |
| Section 4 p11 risk review | PENDING | Needs p11 row review from targeted eval |
| Section 5 Automated green gate | PASS | 45/45 tests green |
| Section 6 AU eval evidence | PENDING | Needs production-context eval run |
| Section 7 Judge / score review | PENDING | Needs judge package + ingest |
| Section 8 Migration handoff | PASS | Tony executed; documented |
| Section 9 Final decision | PENDING | After eval evidence |
