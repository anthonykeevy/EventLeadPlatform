# Story 6.4.4.1-ac10 Closeout Report

## Summary

Story 6.4.4.1-ac10 executes the deferred AC-10 baseline re-judge under `rubric_v2`. It adds locale slicing to the eval runner, explicit result paths to generated judge prompts, and an aggregated judge-package path for six parallel locale batches.

## Implementation

- Added `--locale-filter` to `backend/tests/form_ai_eval/run.py`; each locale slice filters `prompts-v1.1` to 45 rows and records `locale_filter` in run metadata.
- Added generated `judge-prompt-claude.md`, `judge-prompt-grok.md`, and `judge-prompt-gpt5mini.md` files to each judge package. Each prompt includes the exact output JSON path under `judge-package/results/`.
- Added `judge_pack.py --inputs` to combine multiple locale run folders into one judge package for 3 total Cursor judge sessions.
- Applied stale-field housekeeping for PR #75 merge status.

## AC-10 Outcome

Initial live baseline generation completed: 6 locale slices x 45 rows = 270 rows.

However, the first aggregate judge package was incomplete for semantic judging: `generated_definition_available = 0 / 270`, so each row exposed only the prompt and Category A metrics, not the generated form definition.

Root cause: `run.py` did not persist `response.definitionJSON` into `metrics.jsonl`, and `--use-db` could not recover definitions because `generation_run_id` was `null` for all rows.

Fix applied: `run.py` now writes `generated_definition` into each metrics row and focused tests cover it.

Regeneration complete: `story-6.4.4.1-ac10-baseline-v2` has 270/270 generated definitions in the aggregate judge package and 0 unavailable-definition warnings.

Judge consolidation is complete for the corrected v2 package:

- Claude: valid `rubric_v2`, 270 rows, 2,700 non-zero metric scores.
- Grok: valid `rubric_v2`, 270 rows, 2,700 non-zero metric scores.
- GPT-5 mini: valid `rubric_v2`, 270 rows, 2,548 non-zero metric scores, no all-zero rows.

The final ingest summary is written to `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/judge-ingest-summary.json` and reports `control_judge: gpt5mini`.

AC-10 verdict: **Pass**. Grok 4 mean is below 5.00 (`4.2667`), and each judge scored at least one baseline cell below 4: Claude `439`, Grok `270`, GPT-5 mini `644`.

## Recommended Next Story

Story 6.4.4.2 — re-evaluate H2/H4 under `rubric_v2`.

## Verification

See `STORY-6.4.4.1-AC10-GATE-EVIDENCE.md`.

## Files Added

- `backend/tests/test_form_ai_eval_locale_filter.py`
- `docs/stories/STORY-6.4.4.1-AC10-PREFLIGHT.md`
- `docs/stories/STORY-6.4.4.1-AC10-GATE-EVIDENCE.md`
- `docs/stories/STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md`
- `docs/stories/STORY-6.4.4.1-AC10-UAT-RESULTS.md`
- `docs/stories/STORY-6.4.4.1-AC10-JUDGE-PROMPTS-STATUS.md`

Judge JSONs and ingest summary from the incomplete package are present but not valid for AC-10 closeout. The regenerated v2 package has all three judge outputs plus the final ingest summary.
