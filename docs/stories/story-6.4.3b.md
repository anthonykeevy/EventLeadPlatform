# Story 6.4.3b — Eval Judge Package + Rubric ADR

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.4.3b  
**Title:** Eval Judge Package + Rubric ADR  
**Status:** ✅ **Complete** — UAT passed and DB-backed judge ingest verified
**Branch:** `story/epic6-6.4.3b-eval-judge-package-rubric`  
**PR:** [#70](https://github.com/anthonykeevy/EventLeadPlatform/pull/70) — Draft  
**Created:** 2026-04-25  
**Depends On:** Story 6.4.3a ✅ Complete (harness + `log.FormAiEvalRun`), Story 6.4.2 ✅ Complete (capability prompt cleanup + post-cleanup baseline)  
**Unblocks:** Story 6.4.3c, Story 6.4.4 prompt shrink sweeps

---

## 1) Goal

Add the human-in-the-loop judge layer for the Form AI eval harness without introducing new model API clients or secrets.

This story packages benchmark generations into a deterministic, anonymised judge input bundle, defines and locks `rubric_v1.md`, validates per-judge JSON score files saved from Cursor multi-model chats, ingests those scores into the eval run record, and documents the manual judge workflow.

Success means a future prompt sweep can produce:

- a stable judge package per sweep,
- a clear rubric that does not drift mid-experiment,
- three Cursor judge outputs (GPT-5 mini control + Claude + Gemini),
- validated JSON ingest,
- judge agreement and self-bias fields ready for the 6.4.3c diff/statistics layer.

---

## 2) In Scope

### 2.1 Locked rubric v1

Create `backend/tests/form_ai_eval/rubric_v1.md`.

The rubric must define Category B semantic metrics from the brief:

- `field_coverage_recall`
- `field_label_f1`
- `validation_intent_accuracy`
- `row_group_agreement`
- `locale_fidelity`
- `copy_quality_score`

It may include Category C placeholders for H5/H6 future use, but 6.4.3b does not score style runs yet.

The rubric must include:

- score ranges and anchors,
- required JSON shape,
- judge instructions,
- examples for common edge cases,
- explicit instruction to judge only the anonymised package content.

Rubric changes after this story require ADR/update to `STORY-6.4.3b-RUBRIC-ADR.md` and a new rubric version.

### 2.2 Rubric ADR

Complete `docs/stories/STORY-6.4.3b-RUBRIC-ADR.md`.

The ADR must record:

- why the rubric is file-versioned,
- why three Cursor judges are used instead of API integration,
- why GPT-5 mini is a control and excluded from the primary mean,
- what requires a `rubric_v2.md`,
- how baseline re-snapshotting is handled if rubric changes.

### 2.3 Judge package generator

Create `backend/tests/form_ai_eval/judge_pack.py`.

Required behavior:

- input: an eval run folder, e.g. `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/`,
- output: a judge package folder, e.g. `_bmad-output/eval-runs/<run-id>/judge-package/`,
- copy/include `rubric_v1.md`,
- generate `judge-input-batch.md`,
- generate `judge-output-template.json`,
- anonymise PII-adjacent values where practical,
- preserve deterministic row ordering,
- include enough row metadata to link judge scores back to `EvalRunID` / prompt id / repetition / variant.

The package must be usable by a human in Cursor chat without extra setup.

### 2.4 Judge JSON ingest

Create `backend/tests/form_ai_eval/judge_ingest.py`.

Required behavior:

- input: judge package folder with one or more files under `results/`,
- expected file names:
  - `judge-output-gpt5mini.json`
  - `judge-output-claude.json`
  - `judge-output-gemini.json`
- validate JSON shape, row IDs, metric ranges, and missing/duplicate rows,
- compute per-row cross-model means from Claude + Gemini,
- compute GPT-5 mini self-bias deltas against cross-model means,
- compute per-row judge agreement score,
- write an ingest summary artifact,
- update `log.FormAiEvalRun` judge fields where DB persistence is available.

If DB persistence is unavailable, ingest must still validate files and emit local summary JSON/CSV.

### 2.5 Judge workflow documentation

Create `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`.

It must cover:

- how to generate a package,
- how Anthony runs three Cursor chats,
- which models to use,
- where to save output JSON,
- how to run ingest,
- how to handle judge disagreement,
- data handling / PII-adjacent constraints,
- what remains for 6.4.3c.

### 2.6 Tests

Add focused tests, expected homes:

- `backend/tests/test_judge_pack.py`
- `backend/tests/test_judge_ingest.py`

Tests must not call any live model.

Coverage must include:

- package generation from a fixture eval run,
- deterministic ordering,
- anonymisation/scrubbing behavior for obvious email/name/date-like values,
- output template shape,
- ingest validation success,
- ingest validation failure for missing rows / duplicate rows / out-of-range scores,
- cross-model mean and GPT-5 mini bias delta calculation,
- DB update mapping through a mock/fake session where practical.

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| Live judge execution by API | Explicitly ruled out; judges run via Cursor chats. |
| Welch/Fisher statistics and diff reports | Story 6.4.3c. |
| PR comment CI integration | Future story after diff output exists. |
| Prompt shrink experiments H1/H2/H4 | Story 6.4.4. |
| Changing `prompts.yaml` | Frozen by 6.4.3a unless an ADR approves mutation. |
| Changing `log.FormAiEvalRun` schema unless absolutely required | 6.4.3a included nullable judge fields for this story. |
| Human semantic verdict on a winner | Later sweep stories. This story validates the judge workflow and ingest mechanics. |

---

## 4) Acceptance Criteria

1. **AC-1 Rubric exists:** `backend/tests/form_ai_eval/rubric_v1.md` exists and defines Category B metrics, scoring anchors, JSON shape, and judge instructions.
2. **AC-2 Rubric ADR complete:** `STORY-6.4.3b-RUBRIC-ADR.md` documents rubric governance, v2 trigger, Cursor-judge rationale, and baseline re-snapshot policy.
3. **AC-3 Judge package generator works:** `judge_pack.py` generates `rubric_v1.md`, `judge-input-batch.md`, `judge-output-template.json`, and `results/` from a fixture or real eval run folder.
4. **AC-4 Judge package is deterministic:** Re-running package generation from the same inputs produces stable row order and stable row IDs.
5. **AC-5 PII-adjacent scrubbing:** Judge input does not expose obvious raw email/phone/date/name-like synthetic values when scrub rules can identify them; limitations are documented.
6. **AC-6 Cursor workflow documented:** `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` tells Anthony how to run GPT-5 mini, Claude, and Gemini Cursor chats and save outputs.
7. **AC-7 Ingest validates JSON:** `judge_ingest.py` rejects missing rows, duplicate rows, unknown row IDs, malformed metric keys, and out-of-range scores with clear errors.
8. **AC-8 Ingest computes judge aggregates:** Ingest computes Claude+Gemini cross-model means, GPT-5 mini bias deltas, and judge agreement score.
9. **AC-9 DB update path works or degrades cleanly:** When DB is available, ingest updates nullable judge fields on `log.FormAiEvalRun`; when unavailable, it emits local summary artifacts and records the gap.
10. **AC-10 Tests cover pack and ingest:** Focused tests pass without live model calls.
11. **AC-11 No statistics scope leak:** No Welch/Fisher/diff tool is implemented in this story.
12. **AC-12 Closeout complete:** `STORY-6.4.3b-CLOSEOUT-REPORT.md` records AC evidence, judge workflow readiness, known limitations, and carry-forward to 6.4.3c.

---

## 5) Definition of Done

- All ACs have evidence in `STORY-6.4.3b-GATE-EVIDENCE.md`.
- `rubric_v1.md`, `judge_pack.py`, `judge_ingest.py`, and judge workflow docs exist.
- Focused tests pass.
- Backend gate is run unless a clear CI-backed exception is recorded.
- No live model judge execution is required for Dev completion.
- Stale-field audit passes before merge.

---

## 6) Dev Agent Record

### Implementation Notes

- Added locked `rubric_v1.md` with Category B metrics, score anchors, required JSON shape, judge instructions, and future Category C placeholders only.
- Completed `STORY-6.4.3b-RUBRIC-ADR.md` with rubric versioning, Cursor manual judge rationale, GPT-5 mini control behavior, `rubric_v2.md` triggers, and baseline re-score policy.
- Added `judge_pack.py` to generate deterministic `judge-package/` folders from eval run artifacts, with optional DB enrichment from `dbo.GenerationArtifact` and `log.FormAiEvalRun`.
- Added `judge_ingest.py` to validate Cursor-saved judge JSON, compute Claude+Gemini primary means, GPT-5 mini bias deltas, judge agreement scores, local summary artifacts, and optional DB judge-field updates.
- Added `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` for Anthony's manual three-model Cursor workflow.
- Generated a real judge package for `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/` using `--use-db`; all 10 rows have generated definitions and `EvalRunID` mappings.
- Anthony completed the optional GPT-5 mini, Claude, and Gemini judge chats and ran DB-backed ingest; 10/10 rows updated with agreement scores from `0.933` to `1.0`.

### Tests And Gates

- `python -m pytest backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py --tb=short` from worktree root: `7 passed`.
- `.\scripts\workflow\run-green-gate.ps1 -StoryId "6.4.3b" -FocusedTestCommand "python -m pytest tests/test_judge_pack.py tests/test_judge_ingest.py --tb=short" -BackendGateCommand "python -m pytest --tb=short" -EvidenceFile "docs/stories/STORY-6.4.3b-GATE-EVIDENCE.md"`: focused `7 passed`; backend `773 passed, 26 skipped`.
- `python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package --persist-db`: pass; wrote `judge-ingest-summary.json` and `judge-ingest-summary.csv`, `db_update_status = updated`, `db_update_count = 10`.

### File List

- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/judge-input-batch.md`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/judge-output-template.json`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/judge-package-metadata.json`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/judge-ingest-summary.csv`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/judge-ingest-summary.json`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/rubric_v1.md`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/results/judge-output-claude.json`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/results/judge-output-gemini.json`
- `_bmad-output/eval-runs/story-6.4.2-post-cleanup-baseline/judge-package/results/judge-output-gpt5mini.json`
- `backend/tests/form_ai_eval/judge_ingest.py`
- `backend/tests/form_ai_eval/judge_pack.py`
- `backend/tests/form_ai_eval/rubric_v1.md`
- `backend/tests/test_judge_ingest.py`
- `backend/tests/test_judge_pack.py`
- `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
- `docs/stories/EPIC-6-STATUS.md`
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`
- `docs/stories/STORY-6.4.3b-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.4.3b-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.3b-PREFLIGHT.md`
- `docs/stories/STORY-6.4.3b-RUBRIC-ADR.md`
- `docs/stories/STORY-6.4.3b-UAT-TEST-GUIDE.md`
