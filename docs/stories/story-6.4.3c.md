# Story 6.4.3c — Eval Diff + Statistics Tooling

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.4.3c  
**Title:** Eval Diff + Statistics Tooling  
**Status:** ✅ **Complete** — UAT passed and merged
**Branch:** `story/epic6-6.4.3c-eval-diff-statistics`  
**PR:** [#71](https://github.com/anthonykeevy/EventLeadPlatform/pull/71)  
**Completed:** 2026-04-25  
**Created:** 2026-04-25  
**Depends On:** Story 6.4.3a ✅ Complete, Story 6.4.2 ✅ Complete, Story 6.4.3b ✅ Complete  
**Unblocks:** Story 6.4.4 prompt shrink sweeps

---

## 1) Goal

Complete the evaluation harness decision layer so prompt experiments can be compared with deterministic structural gates, judge-score deltas, and statistical evidence.

This story adds the diff/report tooling and statistics module on top of the harness, baseline, and judge-ingest layers already shipped in 6.4.3a/6.4.2/6.4.3b. It does **not** run H1/H2/H4 sweeps or change prompt content.

Success means Story 6.4.4 can run measured prompt shrink experiments and produce:

- Markdown and CSV diff reports,
- structural blocking signals,
- judge-score comparison tables,
- Welch t-test and Fisher exact outputs,
- effect-size results,
- clear "ship / revert / inconclusive" recommendation scaffolding.

---

## 2) In Scope

### 2.1 Statistics module

Create `backend/tests/form_ai_eval/stats.py`.

Required functions:

- Welch's t-test for continuous metrics,
- Cohen's `d` effect size,
- Fisher's exact test for binary metrics such as `schema_valid`,
- safe handling for tiny samples / zero variance,
- verdict helper using Epic 6 rules:
  - continuous metric win when `p < 0.05` and Cohen's `d >= 0.3`,
  - binary metric evaluated via Fisher exact,
  - Category B inconclusive when `p > 0.05` should flag auto-rerun at n=15.

Use Python standard library where practical. If Dev needs SciPy or another dependency, pause and justify before adding it.

### 2.2 Diff tool

Create `backend/tests/form_ai_eval/diff.py`.

Required behavior:

- compare two eval run folders, e.g. baseline vs variant,
- load `metrics.jsonl`, `summary.csv`, `run-metadata.json`, and judge ingest summary where present,
- align rows by prompt id + repetition + variant/run identity,
- compare Category A metrics,
- compare Category B judge metrics when judge summaries exist,
- compute statistical outputs using `stats.py`,
- emit a Markdown report and CSV detail output,
- emit machine-readable JSON summary,
- flag blocking conditions:
  - any `schema_valid` regression,
  - any `boundary_violation_count > 0`,
- keep all other deltas advisory for human decision.

### 2.3 Report format

Diff output must include:

- run metadata for both inputs,
- structural summary table,
- per-prompt regression table,
- judge metric delta table when available,
- statistical significance section,
- blocking/advisory decision section,
- explicit limitations and sample-size warnings.

The CLI should support a documented output folder and default to a safe location under `_bmad-output/eval-runs/<comparison-id>/`.

### 2.4 Public docs

Create `docs/FORM-AI-EVAL-DIFF-STATS.md`.

It must explain:

- how to compare two runs,
- how to interpret blocking vs advisory outcomes,
- how Welch/Fisher/Cohen's d are used,
- when auto-rerun at n=15 is recommended,
- how 6.4.4 should use the tool for H1/H2/H4 and combined variants,
- what remains out of scope for CI automation.

### 2.5 Tests

Add focused tests:

- `backend/tests/test_eval_stats.py`
- `backend/tests/test_eval_diff.py`

No live LLM calls.

Test coverage must include:

- Welch t-test sane output on known data,
- Cohen's d effect-size direction/magnitude,
- Fisher exact on binary counts,
- zero-variance / tiny-sample safe handling,
- diff report detects `schema_valid` regression,
- diff report detects boundary violation blocker,
- judge metric deltas included when judge summaries exist,
- output files are written.

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| H1/H2/H4 prompt shrink edits | Story 6.4.4. |
| Running formal prompt sweeps | Story 6.4.4 and later hypothesis stories. |
| PR comment CI integration | Future story after report format stabilizes. |
| Changing judge rubric | Requires rubric ADR / `rubric_v2.md`; not part of 6.4.3c. |
| Changing `prompts.yaml` | Frozen by 6.4.3a. |
| Adding live model APIs | Explicitly out of the judge architecture. |
| Making automatic product decisions | Tool recommends; Human/SM/PM decide. |

---

## 4) Acceptance Criteria

1. **AC-1 Stats module exists:** `backend/tests/form_ai_eval/stats.py` implements Welch t-test, Cohen's d, Fisher exact, and safe handling for tiny/degenerate samples.
2. **AC-2 Stats tests pass:** `backend/tests/test_eval_stats.py` covers known outputs, effect size, binary Fisher exact, zero variance, and tiny samples.
3. **AC-3 Diff tool exists:** `backend/tests/form_ai_eval/diff.py` compares two eval run folders and writes Markdown, CSV, and JSON outputs.
4. **AC-4 Row alignment is deterministic:** Diff aligns rows by prompt id and repetition and reports missing/extra rows clearly.
5. **AC-5 Blocking gates implemented:** Diff flags any `schema_valid` regression and any `boundary_violation_count > 0` as blocking.
6. **AC-6 Advisory metrics reported:** Component count, collision count, attempt count, duration, token/cost, and judge-score deltas are reported as advisory unless explicitly configured otherwise.
7. **AC-7 Judge metrics included:** When judge ingest summaries exist, Category B metrics and GPT-5 mini bias deltas appear in the report.
8. **AC-8 Auto-rerun recommendation exists:** Inconclusive Category B results with `p > 0.05` recommend rerun at n=15.
9. **AC-9 Public docs complete:** `docs/FORM-AI-EVAL-DIFF-STATS.md` explains usage and interpretation for Story 6.4.4.
10. **AC-10 Diff tests pass:** `backend/tests/test_eval_diff.py` covers blockers, advisory deltas, judge metrics, missing rows, and output files.
11. **AC-11 No scope leak:** No prompt content changes, no sweeps, no CI PR-comment automation.
12. **AC-12 Closeout complete:** `STORY-6.4.3c-CLOSEOUT-REPORT.md` records AC evidence, test gates, known limitations, and 6.4.4 handoff instructions.

---

## 5) Definition of Done

- All ACs are mapped to `STORY-6.4.3c-GATE-EVIDENCE.md`.
- Focused tests pass.
- Backend gate is run unless a clear CI-backed exception is recorded.
- Docs explain exactly how 6.4.4 uses the diff/statistics tool.
- Stale-field audit passes before merge.

---

## Dev Agent Record

### Implementation Notes

- Implemented dependency-free `stats.py` with Welch t-test, Cohen's `d`, Fisher exact, and verdict helper including Category B `rerun-at-n15`.
- Implemented `diff.py` CLI/report generator with `metrics.jsonl` / `summary.csv` loading, metadata loading, judge ingest summary loading, deterministic row alignment, blocking gates, advisory deltas, Markdown/CSV/JSON outputs.
- Added Story 6.4.4 public handoff docs and closeout report.
- Created local sample eval fixtures because committed eval artifacts were absent from this worktree.

### Debug Log

- Red stats test failed on missing `form_ai_eval.stats`; green after adding `stats.py`.
- Red diff test failed on missing `form_ai_eval.diff`; green after adding `diff.py`.
- Sample CLI initially failed under `python -m backend.tests.form_ai_eval.diff` due import path; fixed to match existing eval harness path setup.

### Test Results

- Preflight: PASS; `docs/stories/STORY-6.4.3c-PREFLIGHT.md`.
- Focused gate: PASS; `python -m pytest tests/test_eval_stats.py tests/test_eval_diff.py --tb=short` => `8 passed, 116 warnings`.
- Backend gate: PASS; `python -m pytest --tb=short` => `781 passed, 26 skipped, 5711 warnings`.
- Evidence: `docs/stories/STORY-6.4.3c-GATE-EVIDENCE.md`.

### File List

- `_bmad-output/eval-runs/story-6.4.3c-sample-baseline/judge-package/judge-ingest-summary.json`
- `_bmad-output/eval-runs/story-6.4.3c-sample-baseline/metrics.jsonl`
- `_bmad-output/eval-runs/story-6.4.3c-sample-baseline/run-metadata.json`
- `_bmad-output/eval-runs/story-6.4.3c-sample-diff/diff-details.csv`
- `_bmad-output/eval-runs/story-6.4.3c-sample-diff/diff-report.md`
- `_bmad-output/eval-runs/story-6.4.3c-sample-diff/diff-summary.json`
- `_bmad-output/eval-runs/story-6.4.3c-sample-variant/judge-package/judge-ingest-summary.json`
- `_bmad-output/eval-runs/story-6.4.3c-sample-variant/metrics.jsonl`
- `_bmad-output/eval-runs/story-6.4.3c-sample-variant/run-metadata.json`
- `backend/tests/form_ai_eval/diff.py`
- `backend/tests/form_ai_eval/stats.py`
- `backend/tests/test_eval_diff.py`
- `backend/tests/test_eval_stats.py`
- `docs/FORM-AI-EVAL-DIFF-STATS.md`
- `docs/stories/EPIC-6-STATUS.md`
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`
- `docs/stories/STORY-6.4.3c-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.4.3c-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.3c-PREFLIGHT.md`
- `docs/stories/STORY-6.4.3c-UAT-TEST-GUIDE.md`
- `docs/stories/story-6.4.3c.md`

### Change Log

- 2026-04-25: Added eval diff/statistics tooling, focused tests, documentation, sample evidence, and closeout artifacts.
