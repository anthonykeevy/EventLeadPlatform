# Story 6.4.6 Gate Evidence

## Scope

Build the AU-only diagnostic evaluation framework and produce the current-state AU baseline. This story must not apply prompt/context improvements.

## Automated Checks

| Check | Command | Result |
|---|---|---|
| Preflight | `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.6-au-diagnostic-eval-framework" -ExpectedBranch "story/epic6-6.4.6-au-diagnostic-eval-framework" -ReportFile "docs/stories/STORY-6.4.6-PREFLIGHT.md"` | PASS. Report written to `docs/stories/STORY-6.4.6-PREFLIGHT.md`. PR #82 is open/draft to `master`; PR #81 is merged. |
| Focused eval/judge tests | `python -m pytest backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_locale_filter.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py backend/tests/test_eval_diff.py backend/tests/test_form_ai_eval_experiment.py --tb=short` | PASS: 39 passed, 116 warnings in 2.04s after judge ingest/UAT documentation updates. |
| Backend regression | `python -m pytest backend/tests --tb=short` | PASS: 806 passed, 28 skipped, 5669 warnings in 1608.46s. |
| Frontend lint | `npm run lint` | Not applicable unless frontend files are touched |
| Frontend unit tests | `npm run test:unit -- --watch=false` | Not applicable unless frontend files are touched |
| SM stale-field audit | PR #82 status check plus stale phrase search across story/status/closeout docs | PASS: PR #82 is open/draft to `master`; remaining draft/current-focus hits are intentional for the unmerged story PR and active workflow guide. No stale judge-ingest language remains after doc updates. |

## Eval/Judge Gates

| Gate | Result |
|---|---|
| AU prompt set created and validated | PASS: `backend/tests/form_ai_eval/prompts_au_v1.yaml`, benchmark `prompts-au-v1`, 45 AU rows. |
| AU locale contract created and validated | PASS: `backend/tests/form_ai_eval/au_locale_contract_v1.json`, version `au-locale-contract-v1`. |
| Prompt-context preflight/linter artifacts produced | PASS: `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/prompt-context-lint.json`; 0 prompt-context findings. |
| Shared context bundle produced | PASS: `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/shared-context-bundle.json`. |
| Deterministic AU checks produced | PASS: `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/au-deterministic-checks.json`; 130 generated-output findings across 25 prompts. |
| Current-state AU baseline run complete | PASS: 45/45 live rows aggregated as `story-6.4.6-au-baseline-current`; 45/45 schema-valid. This aggregate was produced before provider usage capture was wired through, so token fields remain placeholders in this artifact; new runs capture provider token usage when the provider returns it. |
| Judge package generated with shared context bundle | PASS: `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/`; package has 45 rows and `shared-context-bundle.json`. |
| Judge outputs ingested with diagnostic fields | PASS: Claude, Grok, and GPT-5 mini outputs saved and ingested; `judge-ingest-summary.json` and `.csv` produced with diagnostic fields. |
| Tracking row `AU-000` updated | PASS: baseline run ID, deterministic findings, judge metrics, conflict findings, suggested corrections, and follow-up action recorded. |

## Final Code State

Framework implementation is test-green from the focused and backend regression gates. Live AU baseline aggregate, judge package, judge ingest, `AU-000`, UAT evidence, closeout report, stale-field audit, Tony acceptance, and merge to `master` are complete. Parallel timing evidence is recorded in `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/parallel-execution-summary.json` with max observed concurrency = 4.
