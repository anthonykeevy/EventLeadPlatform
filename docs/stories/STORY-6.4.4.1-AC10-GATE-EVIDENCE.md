# Story 6.4.4.1-ac10 Gate Evidence

## Scope

AC-10 baseline re-judge execution, parallel locale-batch harness extension, judge package path clarity, stale-field housekeeping.

## Automated Checks

| Check | Command | Result |
|---|---|---|
| Preflight | `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge" -ExpectedBranch "story/epic6-6.4.4.1-ac10-baseline-rejudge" -ReportFile "docs/stories/STORY-6.4.4.1-AC10-PREFLIGHT.md"` | PASS |
| Locale filter focused tests | `python -m pytest backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_locale_filter.py --tb=short` | `14 passed` |
| Judge package focused tests | `python -m pytest backend/tests/test_judge_pack.py --tb=short` | `5 passed` |
| Combined focused eval tests | `python -m pytest backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_locale_filter.py backend/tests/test_judge_pack.py --tb=short` | `19 passed` |
| Backend regression | `python -m pytest backend/tests --tb=short` | `800 passed, 26 skipped` |
| Stale ready-to-merge scan | `rg -n "ready to merge" docs/stories/STORY-6.4.4.1-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md docs/stories/story-6.4.4.1.md` | PASS: no hits |
| v1 ingest backwards-compat smoke | `python -m backend.tests.form_ai_eval.judge_ingest "<alternate v1 historical judge-package>"` | PASS: `rubric_v1`, `row_count=10`, primary judges `claude` + `gemini` |

Note: the first external `story-6.4.2-post-cleanup-baseline` package path failed JSON parsing because its `judge-output-gpt5mini.json` contains extra data after the JSON object. The alternate historical copy ingested successfully, so the version-gated v1 ingest code path remains covered.

## AC-10 Baseline Run

Status: complete; final aggregate judge package ready.

Locale slices:

| Slice | Rows | Status |
|---|---:|---|
| `story-6.4.4.1-ac10-baseline-AU` | 45 | Completed |
| `story-6.4.4.1-ac10-baseline-NZ` | 45 | Completed |
| `story-6.4.4.1-ac10-baseline-UK` | 45 | Completed |
| `story-6.4.4.1-ac10-baseline-US` | 45 | Completed |
| `story-6.4.4.1-ac10-baseline-INTL_ONLINE` | 45 | Completed |
| `story-6.4.4.1-ac10-baseline-EU` | 45 | Completed |

Aggregate package: `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/`

Aggregate row count: 270.

Judge prompt doc: `STORY-6.4.4.1-AC10-JUDGE-PROMPTS-STATUS.md`.

Runtime observation: successful locale runs emitted repeated non-fatal SQLAlchemy/API logging messages around unresolved `FormPublicLink` relationship resolution on `FormSubmission`, plus the existing Pydantic v2 `schema_extra` warning. The eval harness still completed all six slices and wrote valid artifacts.

## Judge Package Completeness Finding

The first aggregate judge package was structurally valid but incomplete for semantic judging:

- `judge-package-metadata.json` reported `generated_definition_available = 0 / 270`.
- Every row in `judge-input-batch.md` had `Definition source: unavailable`.
- Each row's Generated Definition block contained only `{"warning": "generated definition unavailable in local artifacts"}`.
- Root cause: the harness wrote Category A metrics but did not persist `response.definitionJSON` in `metrics.jsonl`; `--use-db` also could not recover definitions because `generation_run_id` was `null` for all rows.

Fix:

- `backend/tests/form_ai_eval/run.py` now writes `generated_definition` into each metrics row.
- `backend/tests/test_form_ai_eval_harness.py` asserts the mock runner persists `generated_definition`.
- Focused tests remain green: `19 passed`.

Smoke validation:

| Check | Result |
|---|---:|
| Smoke run id | `story-6.4.4.1-ac10-smoke10-with-definitions` |
| Live generated rows | 10 |
| Metrics rows with `generated_definition` | 10 |
| Judge package row count | 10 |
| Judge package rows with generated definition available | 10 |
| Generated definition source | `metrics.jsonl` |
| Unavailable-definition warnings in `judge-input-batch.md` | 0 |

Full regenerated baseline validation:

| Check | Result |
|---|---:|
| Regenerated aggregate run id | `story-6.4.4.1-ac10-baseline-v2` |
| Locale slices completed | 6 |
| Total live generated rows | 270 |
| Metrics rows with `generated_definition` | 270 |
| Judge package row count | 270 |
| Judge package rows with generated definition available | 270 |
| Generated definition source | `metrics.jsonl` |
| Unavailable-definition warnings in `judge-input-batch.md` | 0 |

## Judge Ingest Summary

Status: complete against the regenerated `story-6.4.4.1-ac10-baseline-v2` package.

Previous judge outputs against the incomplete package are invalid for AC-10 because no generated form definitions were available to judge. The corrected v2 package is ready for re-judge.

Verification on 2026-04-28:

| Judge | Expected output | Verification |
|---|---|---|
| Claude | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/results/judge-output-claude.json` | PASS: valid JSON, `rubric_v2`, 270 rows, 2,700 non-zero metric scores, modified 2026-04-28 08:00 local |
| Grok | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/results/judge-output-grok.json` | PASS: valid JSON, `rubric_v2`, 270 rows, 2,700 non-zero metric scores, modified 2026-04-28 07:51 local |
| GPT-5 mini | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/results/judge-output-gpt5mini.json` | PASS: valid JSON, `rubric_v2`, 270 rows, 2,548 non-zero metric scores, no all-zero rows, modified 2026-04-28 08:24 local |

Final ingest output:

| Check | Result |
|---|---:|
| Ingest command | `python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package` |
| Summary JSON | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/judge-ingest-summary.json` |
| Summary CSV | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/judge-ingest-summary.csv` |
| Rows consolidated | 270 |
| Primary judges present | Claude + Grok |
| Control judge present | GPT-5 mini |
| Claude mean | 4.2607 |
| Grok mean | 4.2667 |
| GPT-5 mini mean | 4.2978 |
| Cross-model mean | 4.2637 |
| Cross-model cells below 4 | 385 |
| Rows with any cross-model metric below 4 | 174 |
| Claude cells below 4 | 439 |
| Grok cells below 4 | 270 |
| GPT-5 mini cells below 4 | 644 |

AC-10 verdict: **Pass**. Grok 4 mean is below 5.00, each judge scored at least one baseline cell below 4, and the GPT-5 mini control output is present in the final ingest.
