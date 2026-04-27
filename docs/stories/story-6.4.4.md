# Story 6.4.4 — Prompt Shrink Sweeps H1/H2/H4

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.4.4  
**Title:** Prompt Shrink Sweeps H1/H2/H4  
**Status:** Evidence complete — PM/SM ship decision required
**Branch:** `story/epic6-6.4.4-prompt-shrink-sweeps`  
**PR:** [#72](https://github.com/anthonykeevy/EventLeadPlatform/pull/72) — Draft  
**Created:** 2026-04-25  
**Depends On:** Stories 6.4.3a, 6.4.2, 6.4.3b, 6.4.3c ✅ Complete  
**Unblocks:** Story 6.4.5 and downstream additive AI capability stories

---

## 1) Goal

Run the first measured prompt-shrink experiments using the completed eval harness, judge package, ingest, and diff/statistics tooling.

This story tests H1, H2, H4, and the combined H1+H2+H4 variant:

- **H1:** replace AU/NZ locale block with a one-line directive.
- **H2:** shrink consent/legal guidance from the current large heuristic block to a compact decision table.
- **H4:** trim operational notes/context-pack duplication.
- **Combined:** apply H1+H2+H4 together to catch interaction effects.

The story must ship only winners backed by evidence and revert losers before merge.

---

## 2) In Scope

### 2.1 Baseline and sweep discipline

Use the frozen `prompts-v1.0` benchmark set.

For each hypothesis:

- run baseline/current control as needed,
- run the variant under a distinct `HypothesisCode` / `VariantLabel`,
- include the combined variant in the sweep,
- persist outputs under `_bmad-output/eval-runs/`,
- generate judge packages where Category B semantic evidence is required,
- ingest judge outputs if Anthony completes the Cursor judge flow,
- run diff/statistics comparison,
- record results in `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`.

Minimum formal target from the brief:

- Category A structural metrics: 5 reps minimum.
- Category B semantic confidence: 10 reps minimum, or document why a smaller run is only a smoke/provisional result.
- Auto-rerun at n=15 when Category B is inconclusive (`p > 0.05`) before final verdict.

### 2.2 H1 locale shrink

Current source: `_LOCALE_PROMPT_BLOCKS["AU"]` in `backend/modules/form_ai/service.py`.

Test variant:

```text
Form audience: Australia/New Zealand. Use AU/NZ spelling, address, phone, date conventions.
```

Revert on first confirmed locale regression affecting phone, postcode, date, or AU/NZ copy.

### 2.3 H2 consent/legal shrink

Current source: `_CONSENT_GUIDANCE_BLOCK` in `backend/modules/form_ai/service.py`.

Test variant: compact ~1 KB decision table preserving:

- when to use `terms`,
- when to use `checkbox`,
- company-managed terms behavior,
- required acknowledgement behavior,
- no invented legal URLs/content unless user requests it.

Revert if terms component selection regresses.

### 2.4 H4 operational notes trim

Current source: context pack / sectioned prompt content used by `_build_initial_messages()`.

Test variant: remove or trim duplicated operational notes already covered by the sectioned addendum and active prompt contract.

Revert if collision recovery, row grouping, tab order, or supported catalog behavior regresses.

### 2.5 Combined variant

Run combined H1+H2+H4 after individual variants. Combined result can fail even if individual variants pass.

Decision rule:

- ship only the subset of individual changes that win,
- do not ship combined-only behavior unless each underlying change is acceptable individually or PM/SM explicitly approves the coupling.

### 2.6 Evidence and closeout

Required artifacts:

- `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`
- `STORY-6.4.4-CLOSEOUT-REPORT.md`
- `_bmad-output/eval-runs/<story-6.4.4-runs>/`

Evidence must include:

- commands run,
- run IDs,
- prompt size deltas,
- Category A structural tables,
- judge/diff/statistics outputs where available,
- ship/revert/inconclusive verdict for each hypothesis,
- exact code changes retained at closeout.

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| H3 Component Property Cheat Sheet | Story 6.4.5. |
| H5 Style Intent resolver | Later style story. |
| H6 Google Fonts directive | Conditional later story. |
| Image-to-Form | Later 6.5b-vision story. |
| Changing benchmark prompts or rubric | Requires separate ADR. |
| CI PR-comment automation | Future story; not required for prompt sweep decisions. |
| Shipping inconclusive prompt shrink changes | Evidence-first rule; leave reverted or behind a clearly documented follow-up. |

---

## 4) Acceptance Criteria

1. **AC-1 H1 variant implemented and measured:** Locale one-line directive variant is run through the harness and compared against baseline.
2. **AC-2 H2 variant implemented and measured:** Consent/legal compact decision table variant is run through the harness and compared against baseline.
3. **AC-3 H4 variant implemented and measured:** Operational notes trim variant is run through the harness and compared against baseline.
4. **AC-4 Combined variant measured:** H1+H2+H4 combined variant is run and compared against baseline.
5. **AC-5 Structural gates pass for shipped changes:** Any shipped change has no `schema_valid` regression and no boundary violations.
6. **AC-6 Semantic evidence recorded:** Judge package/ingest/diff evidence is recorded for semantic metrics where available; gaps are explicit.
7. **AC-7 Statistical outputs recorded:** Diff/statistics reports are linked for each variant, including p-values/effect sizes where applicable.
8. **AC-8 Revert losers:** Any failing or inconclusive prompt change is reverted before merge unless PM/SM explicitly accepts a follow-up.
9. **AC-9 Prompt size delta documented:** Before/after prompt-size estimates are recorded per variant and final shipped state.
10. **AC-10 Hypothesis evidence complete:** `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` contains verdicts and evidence for H1, H2, H4, and combined.
11. **AC-11 No unrelated capability work:** No H3/H5/H6/Image-to-Form implementation leaks into this story.
12. **AC-12 Closeout complete:** `STORY-6.4.4-CLOSEOUT-REPORT.md` records final shipped changes, reverted changes, carry-forward items, and gates.

---

## 5) Definition of Done

- All ACs are mapped to `STORY-6.4.4-GATE-EVIDENCE.md`.
- Hypothesis evidence is complete and readable.
- Focused prompt/harness tests pass.
- Backend gate is run unless a clear CI-backed exception is recorded.
- Human/SM accepts final ship/revert verdicts.
- Stale-field audit passes before merge.

---

## Tasks / Subtasks

- [x] Step 0 - Preflight
  - [x] Attempt documented preflight command.
  - [x] Record missing `scripts/agent/preflight.py` result in `STORY-6.4.4-PREFLIGHT.md`.
- [x] Step 1 - Establish baseline
  - [x] Run deterministic mock baseline over frozen `prompts-v1.0` set.
  - [x] Record run ID and artifact path in hypothesis evidence.
- [x] Step 2 - H1 locale shrink
  - [x] Replace AU/NZ locale block with one-line directive.
  - [x] Add prompt contract tests and mock diff evidence.
- [x] Step 3 - H2 consent/legal shrink
  - [x] Replace `_CONSENT_GUIDANCE_BLOCK` with compact decision table.
  - [x] Add prompt contract tests and mock diff evidence.
- [x] Step 4 - H4 operational notes trim
  - [x] Trim context-pack operational notes from `_build_initial_messages()` prompt assembly.
  - [x] Add prompt contract tests and mock diff evidence.
- [x] Step 5 - Combined variant
  - [x] Retain H1+H2+H4 together.
  - [x] Run combined mock sweep and diff.
- [x] Step 6 - Judge evidence
  - [x] Generate live judge packages for baseline, H1, H2, H4, and combined.
  - [x] Ingest GPT-5 mini, Claude, and Gemini judge outputs for all five packages.
  - [x] Generate live diff/statistical reports for all variants.
- [x] Step 7 - Gates
  - [x] Run focused prompt/eval tests.
  - [x] Run full backend gate.
  - [x] Check lints for touched files.
- [x] Step 8 - Closeout
  - [x] Complete hypothesis evidence, gate evidence, and closeout report with final findings.
  - [x] Update Dev Agent Record and File List.

---

## Dev Agent Record

### Debug Log

- Preflight command failed with exit code 2 because `scripts/agent/preflight.py` is absent from the worktree; recorded in `STORY-6.4.4-PREFLIGHT.md`.
- Red phase added prompt shrink and variant parsing tests; expected failures observed before implementation.
- Full backend gate initially failed because older locale tests asserted detailed `Postcode`/`Mobile` prompt content. Tests were updated to the Story 6.4.4 one-line locale contract.

### Completion Notes

- Implemented H1 locale one-line directive in `backend/modules/form_ai/service.py`.
- Implemented H2 compact consent/legal decision table while preserving `terms` vs `checkbox`, company-managed terms, required acknowledgement, and no invented legal URLs/content.
- Implemented H4 context-pack operational notes trim during prompt assembly without mutating the source context pack.
- Updated eval harness CLI validation to support Story 6.4.4 non-baseline variant labels.
- Generated deterministic mock baseline, H1, H2, H4, combined runs and diff reports with no Category A structural blockers.
- Live Category B judging completed across GPT-5 mini, Claude, and Gemini for baseline/H1/H2/H4/combined.
- Individual H1/H2/H4 results were inconclusive at n=10; each received `rerun-at-n15` recommendations.
- Combined H1+H2+H4 produced a significant `locale_fidelity` regression and should not ship as-is.

### File List

- `backend/modules/form_ai/service.py`
- `backend/tests/form_ai_eval/run.py`
- `backend/tests/test_form_ai_eval_harness.py`
- `backend/tests/test_form_ai_prompt_capabilities.py`
- `backend/tests/test_story_631_content_widths.py`
- `docs/stories/story-6.4.4.md`
- `docs/stories/STORY-6.4.4-PREFLIGHT.md`
- `docs/stories/STORY-6.4.4-HYPOTHESIS-EVIDENCE.md`
- `docs/stories/STORY-6.4.4-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.4-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.4.4-JUDGE-PROMPTS.md`
- `_bmad-output/eval-runs/story-6.4.4-mock-baseline/`
- `_bmad-output/eval-runs/story-6.4.4-mock-h1-locale-one-line/`
- `_bmad-output/eval-runs/story-6.4.4-mock-h2-consent-decision-table/`
- `_bmad-output/eval-runs/story-6.4.4-mock-h4-operational-trim/`
- `_bmad-output/eval-runs/story-6.4.4-mock-h1-h2-h4-combined/`
- `_bmad-output/eval-runs/story-6.4.4-mock-baseline-vs-h1/`
- `_bmad-output/eval-runs/story-6.4.4-mock-baseline-vs-h2/`
- `_bmad-output/eval-runs/story-6.4.4-mock-baseline-vs-h4/`
- `_bmad-output/eval-runs/story-6.4.4-mock-baseline-vs-combined/`

### Change Log

- 2026-04-25: Implemented prompt shrink candidates H1/H2/H4, added variant-capable eval harness parsing, generated mock/live structural and semantic evidence, and documented PM/SM ship decision required before merge.
