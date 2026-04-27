# Story 6.4.4.1-ac10 — AC-10 Baseline Re-Judge Execution (parallel-batched)

**Epic:** 6 — AI Generation & Monetization Engine
**Story ID:** 6.4.4.1-ac10
**Title:** AC-10 Baseline Re-Judge Execution + Parallel-Batch Harness Extension + Stale-Field Housekeeping
**Status:** Complete
**Branch:** `story/epic6-6.4.4.1-ac10-baseline-rejudge`
**PR:** #77
**Created:** 2026-04-27
**Depends On:** Story 6.4.4.1 ([PR #75](https://github.com/anthonykeevy/EventLeadPlatform/pull/75)) merged at `6d6bf13`.
**Successor To:** Story 6.4.4.1 (deferred AC-10 manual gate to here).
**Decides Next:** **Story 6.4.4.2** (conditional H2/H4 v2 re-run) **or** skip directly to **Story 6.4.5** (H3 component cheat sheet) — depending on AC-10 outcome.

---

## 1) Goal

Execute the AC-10 baseline re-judge under `rubric_v2` that was deferred from Story 6.4.4.1's automated implementation. Extend the eval harness to support **parallel batch slicing** (so 6 background agents can run one locale each in ~6–8 min wall-clock instead of one sequential ~30–45 min run). Verify that judge-package prompts include **explicit output file paths** so the Cursor judges write outputs without ambiguity. Run the gate. Decide what comes next.

This is an **execution + small code extension** story — not an architecture story. The locale architecture (Story 6.4.4.1) is already on master.

Success means we have v2-rubric baseline numbers to inform the 6.4.4.2 vs 6.4.5 decision and a clean stale-field audit on master.

---

## 2) In Scope

### 2.1 Parallel-batch harness extension

`backend/tests/form_ai_eval/run.py` gains a filter flag (e.g. `--locale-filter <ISO>` or `--prompt-range <start>:<end>`) so a single invocation runs only a subset of `prompts-v1.1`. Each invocation writes to a non-overlapping output directory (e.g. `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-<locale>/`). 6 parallel Dev background agents run one locale each.

- One unit test in `backend/tests/test_form_ai_eval_harness.py` (or new file) confirming the filter slices the dataset deterministically and produces a strict subset.
- No other harness behaviour changes.

### 2.2 Judge-package path-clarity verification

`backend/tests/form_ai_eval/judge_pack.py` must emit per-judge prompts that include the **exact output file path** the judge should write to. Required text shape (or equivalent) inside each emitted judge prompt:

> "Write your output JSON to: `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-<judge>.json`"

If the current generator (post-PR #75) already does this, no change. If not, Dev patches it before generating the package. **Tonyk's hard requirement: judges must know exactly where to write.** Cursor judge sessions copy-paste-easy.

### 2.3 Aggregated judge package (single session per judge, not per locale)

After the 6 parallel locale runs complete, Dev produces a **single judge package** covering all 270 cells (not 6 separate packages). Tonyk runs **3 Cursor sessions total**, not 18.

Mechanism options (Dev decides minimal-change path):

- **Option A:** small `--inputs <run-id>[,<run-id>...]` flag on `judge_pack.py` to consume multiple run dirs.
- **Option B:** pre-merge step that concatenates `metrics.jsonl` / `summary.csv` from sub-runs into a synthetic parent run dir before standard `judge_pack.py` invocation.
- **Option C:** all 6 parallel runs write to subdirectories under a single parent run-id; `judge_pack.py` reads from sub-dirs.

Whichever path: the judge package emits **3 prompts total** (Claude 4.7 / Grok 4 / GPT-5 mini), each pointing to one output JSON path.

### 2.4 Tonyk Cursor judge flow (Tonyk-time)

Dev posts the 3 ready-to-paste prompts in chat. Tonyk pastes each into its respective Cursor session (3 windows, one per judge). Each session writes its `judge-output-<judge>.json` to the path the prompt specifies. Tonyk reports back when all three are done.

Per Tonyk's prior-flow guidance: Dev preps the next batch / monitors orchestration in parallel with Tonyk's Cursor work, so wall-clock is dominated by judge time (~30 min per session × 3 = 1.5 hr serial; or ~30 min if Tonyk runs three Cursor windows concurrently).

### 2.5 Ingest + AC-10 gate verdict

Run `python -m backend.tests.form_ai_eval.judge_ingest --run-id <run-id>`. Inspect `judge-ingest-summary.json`:

- **Pass:** Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 across the baseline → AC-10 met.
- **Ceiling-lock (round 1):** apply one calibration tweak (rubric anchor sharpening — change one anchor on items 7 / 8 to a sharper threshold per the Multi-Round UAT Protocol; one variable per round; RequestID lineage in `STORY-6.4.4.1-AC10-UAT-RESULTS.md`). Re-package, re-judge, re-ingest.
- **Ceiling-lock (round 2):** invoke escape clause. Register `JUDGE-ARCHITECTURE-RE-INVESTIGATION` as a P0 carry-forward in `EPIC-6-CARRY-FORWARD-BACKLOG.md`. AC-10 closes by escape clause; architecture is not blocked.

### 2.6 Decision artifact

Story closeout report records the AC-10 outcome and the recommended next story:

| Outcome | Recommended next story |
|---|---|
| Pass with real variance | Story 6.4.4.2 (re-evaluate H2/H4 under v2; H1 deleted) |
| Escape clause invoked | Skip directly to Story 6.4.5 (H3 component cheat sheet); register `JUDGE-ARCHITECTURE-RE-INVESTIGATION` |
| Pass but H2/H4 evidence still inconclusive at v2 sample size | Skip to Story 6.4.5; defer 6.4.4.2 until a clear signal warrants it |

The decision is held with PM (John) + Tonyk in a 30-min review **after** AC-10 numbers exist.

### 2.7 Stale-field housekeeping

Per workflow guide §SM post-merge reset row 3, four documents on master from PR #75 still say "ready to merge" and need fixing in this story's branch:

| File | Line | Fix |
|---|---|---|
| `docs/stories/STORY-6.4.4.1-CLOSEOUT-REPORT.md` | 7 | "Closeout decision: ready to merge via PR #75." → "Closeout decision: merged via PR #75 on 2026-04-27." |
| `docs/stories/EPIC-6-STATUS.md` | 81 | "✅ **Complete / ready to merge** (2026-04-27, PR #75)" → "✅ **Complete** (merged 2026-04-27, PR #75)" |
| `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` | 16 | Same fix, prepend "merged " to the date. |
| `docs/stories/story-6.4.4.1.md` | 6 | "**Status:** Complete / ready to merge (2026-04-27)" → "**Status:** Complete (merged 2026-04-27, PR #75)" |

---

## 3) Out of Scope

| Item | Reason / future home |
|---|---|
| Story 6.4.4.2 (H2/H4 v2 re-run) | Decided by AC-10 outcome; drafted as a separate story afterwards if pass. |
| Story 6.4.5 (H3 cheat sheet) | Drafted afterwards regardless (just sequencing depends on AC-10). |
| Rubric v3 design | No rubric architecture changes; only anchor sharpening on items 7/8 if round-1 ceiling-locked. |
| Judge swap (further) | Claude 4.7 + Grok 4 + GPT-5 mini panel from rubric_v2 ADR is unchanged. |
| Company brand settings UI | `g-6441-company-brand-settings-ui` carry-forward; separate story. |
| Native-speaker review of DE/JP/FR | `g-6441-native-speaker-review` carry-forward. |
| Per-form locale dropdown | `g-6441-per-form-locale-dropdown` carry-forward. |
| Nightly automation of v1.1 eval on master | Future infrastructure story; not gated on AC-10. |

---

## 4) Acceptance Criteria

1. **AC-1 Parallel-batch flag added to `run.py`:** `--locale-filter` (or equivalent) accepts a single ISO/locale value; sliced dataset matches expected row count (15 prompts × 3 reps = 45 cells per locale); unit test in `backend/tests/`.
2. **AC-2 Judge prompts include explicit output paths:** each of the 3 emitted judge prompts contains the exact file path the judge should write to; verified by reading the generated package.
3. **AC-3 6 parallel locale runs complete:** AU, NZ, UK, US, INTL_ONLINE, EU runs all produce valid `metrics.jsonl` + `summary.csv` + `run-metadata.json`; aggregated to a single 270-cell judge package (one session per judge).
4. **AC-4 Cursor judge sessions completed:** Tonyk-confirmed JSON outputs written to the paths specified by the emitted prompts; 3 files (Claude / Grok / GPT-5 mini) present in `judge-package/results/`.
5. **AC-5 Ingest summary written:** `python -m backend.tests.form_ai_eval.judge_ingest --run-id <run-id>` produces `judge-ingest-summary.json` and `judge-ingest-summary.csv`; primary mean = (claude + grok) / 2; GPT-5 mini bias delta computed.
6. **AC-6 AC-10 gate verdict recorded:** outcome (Pass / escape-clause-invoked) documented in `STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md` with the recommended next story (6.4.4.2 vs 6.4.5).
7. **AC-7 Stale-field housekeeping:** 4 doc fixes from §2.7 applied in a final SM housekeeping commit before merge; rg-scan clean.
8. **AC-8 Backend regression:** `pytest backend/tests` passes (no new failures introduced by the harness extension).
9. **AC-9 Status doc updates:** `EPIC-6-STATUS.md` adds story row; `EPIC-6-WORKFLOW-GUIDE.md` Current Focus advances to whichever story AC-6 recommends.

---

## 5) Definition of Done

- All 9 ACs green.
- Closeout report committed (mandatory: ships a small public-facing harness flag + new evidence files).
- Gate evidence file with focused-test + backend regression summaries.
- Stale-field audit clean on master after merge.
- AC-10 outcome recorded; next-story recommendation surfaced for PM/Tonyk decision.

---

## 6) Estimated Size

**~1–1.5 dev days** + ~1–1.5 hr Tonyk-time:

| Block | Dev days | Tonyk hrs |
|---|---|---|
| `run.py` `--locale-filter` flag + unit test | 0.25 | — |
| `judge_pack.py` path-clarity verification + (if needed) patch | 0.25 | — |
| 6 parallel locale runs orchestrated via background agents | 0.25 | — |
| Cursor judge sessions (3 windows concurrent) | — | 1.0–1.5 |
| Ingest + AC-10 gate verdict + report | 0.25 | 0.5 |
| Stale-field housekeeping (4 docs) | 0.1 | — |
| Closeout report + status doc updates | 0.1 | — |
| **Total** | **~1.2 days** | **~1.5–2 hrs** |

Risk: if round-1 ceiling-locks, +0.5 day for one calibration tweak round (rubric anchor sharpening + re-judge).

---

## 7) References

- Authoritative spec: this file + the Story 6.4.4.1 pack on master.
- Rubric v2 ADR (governs rubric methodology; AC-10 escape clause is §7): [`STORY-6.4.4.1-RUBRIC-V2-ADR.md`](./STORY-6.4.4.1-RUBRIC-V2-ADR.md)
- AC-10 origin: [`story-6.4.4.1.md`](./story-6.4.4.1.md) §4 AC-10 + §2.11.
- UAT for AC-10 in 6.4.4.1: [`STORY-6.4.4.1-UAT-TEST-GUIDE.md`](./STORY-6.4.4.1-UAT-TEST-GUIDE.md) §10.
- Judge prompts: [`STORY-6.4.4.1-JUDGE-PROMPTS.md`](./STORY-6.4.4.1-JUDGE-PROMPTS.md) (referenced by `judge_pack.py`).
- Benchmark spec: [`STORY-6.4.4.1-PROMPTS-V1.1-SPEC.md`](./STORY-6.4.4.1-PROMPTS-V1.1-SPEC.md).
- Eval harness docs: [`docs/FORM-AI-EVAL-HARNESS.md`](../FORM-AI-EVAL-HARNESS.md), [`docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`](../FORM-AI-EVAL-JUDGE-WORKFLOW.md), [`docs/FORM-AI-EVAL-DIFF-STATS.md`](../FORM-AI-EVAL-DIFF-STATS.md).

---

## Dev Agent Record

### Implementation Notes

- Preflight passed for worktree `C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge` on branch `story/epic6-6.4.4.1-ac10-baseline-rejudge`; report written to `STORY-6.4.4.1-AC10-PREFLIGHT.md`.
- Added `--locale-filter` to the eval runner. The filter is case-normalised, exits on empty matches, slices `prompts-v1.1` to 45 rows per locale, records `locale_filter` in metadata, and uses a locale-suffixed variant as the default run id for sliced runs.
- Added per-judge prompt files to judge packages: `judge-prompt-claude.md`, `judge-prompt-grok.md`, and `judge-prompt-gpt5mini.md`. Each prompt embeds the exact output path under `judge-package/results/`.
- Added `judge_pack.py --inputs` so six locale run dirs can be aggregated into one judge package for three total Cursor judge sessions.
- Applied stale-field housekeeping for Story 6.4.4.1 PR #75 merge status; `ready to merge` scan is clean across the four specified docs.
- v1 ingest backwards-compat smoke passed against an alternate historical Story 6.4.2 v1 judge package. The first external copy failed because its GPT-5 mini file contains extra data after the JSON object; this is a data artifact issue, not a v1 ingest path failure.
- Six AC-10 locale batches completed, producing 270 total rows, but the first aggregate judge package had `generated_definition_available = 0 / 270`; the resulting judge outputs are invalid for AC-10.
- Root cause: `run.py` did not persist `response.definitionJSON` into `metrics.jsonl`, and `--use-db` could not recover definitions because `generation_run_id` was `null` for all rows.
- Fixed harness artifact contract: `run.py` now writes `generated_definition` into each metrics row, and focused tests cover the field.
- Regenerated full baseline `story-6.4.4.1-ac10-baseline-v2` produced 270/270 generated definitions and 0 unavailable-definition warnings.
- Final judge ingest includes Claude, Grok, and GPT-5 mini. AC-10 passed: Grok mean `4.2667` and every judge scored baseline cells below 4.
- Recommended next story: Story 6.4.4.2 to re-evaluate H2/H4 under `rubric_v2`.

### Test Results

- Preflight: PASS.
- `python -m pytest backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_locale_filter.py --tb=short` -> `14 passed`.
- `python -m pytest backend/tests/test_judge_pack.py --tb=short` -> `5 passed`.
- `python -m pytest backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_locale_filter.py backend/tests/test_judge_pack.py --tb=short` -> `19 passed`.
- `ReadLints` on touched eval/test files: no linter errors.
- Judge ingest against first package: invalid for AC-10 because the package lacked generated definitions.
- Judge ingest against regenerated v2 package: PASS; 270 rows, primary judges Claude + Grok, control judge GPT-5 mini, cross-model mean `4.2637`.
- Backend regression: `python -m pytest backend/tests --tb=short` -> `800 passed, 26 skipped`.

### File List

- `backend/tests/form_ai_eval/run.py`
- `backend/tests/form_ai_eval/judge_pack.py`
- `backend/tests/test_form_ai_eval_locale_filter.py`
- `backend/tests/test_judge_pack.py`
- `docs/FORM-AI-EVAL-HARNESS.md`
- `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md`
- `docs/stories/STORY-6.4.4.1-AC10-PREFLIGHT.md`
- `docs/stories/STORY-6.4.4.1-AC10-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.4.4.1-AC10-UAT-RESULTS.md`
- `docs/stories/STORY-6.4.4.1-CLOSEOUT-REPORT.md`
- `docs/stories/EPIC-6-STATUS.md`
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`
- `docs/stories/story-6.4.4.1.md`
- `docs/stories/story-6.4.4.1-ac10.md`

### Change Log

- 2026-04-27: Added locale-filtered eval execution, explicit judge prompt output paths, multi-input judge package aggregation, AC10 evidence skeletons, and stale-field housekeeping.
