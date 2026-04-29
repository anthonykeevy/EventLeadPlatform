# Story 6.4.6 Gate Evidence

## Scope

Build the AU-only diagnostic evaluation framework and produce the current-state AU baseline. This story must not apply prompt/context improvements.

## Automated Checks

| Check | Command | Result |
|---|---|---|
| Preflight | `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.6-au-diagnostic-eval-framework" -ExpectedBranch "story/epic6-6.4.6-au-diagnostic-eval-framework" -ReportFile "docs/stories/STORY-6.4.6-PREFLIGHT.md"` | TBD |
| Focused eval/judge tests | `python -m pytest backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_locale_filter.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py backend/tests/test_eval_diff.py --tb=short` | TBD |
| Backend regression | `python -m pytest backend/tests --tb=short` | TBD |
| Frontend lint | `npm run lint` | Not applicable unless frontend files are touched |
| Frontend unit tests | `npm run test:unit -- --watch=false` | Not applicable unless frontend files are touched |
| SM stale-field audit | `gh pr view 82 --json state,isDraft,mergedAt,headRefName,baseRefName,url`; `rg -n "Draft\|Ready for UAT\|Ready for UAT/SM review\|Keep PR .* open\|Current Focus\|TBD" docs/stories/story-6.4.6.md docs/stories/STORY-6.4.6-CLOSEOUT-REPORT.md docs/stories/STORY-6.4.6-GATE-EVIDENCE.md docs/stories/STORY-6.4.6-UAT-RESULTS.md docs/stories/STORY-6.4.6-AU-BASELINE-EVIDENCE.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md` | TBD |

## Eval/Judge Gates

| Gate | Result |
|---|---|
| AU prompt set created and validated | TBD |
| AU locale contract created and validated | TBD |
| Prompt-context preflight/linter artifacts produced | TBD |
| Shared context bundle produced | TBD |
| Deterministic AU checks produced | TBD |
| Current-state AU baseline run complete | TBD |
| Judge package generated with shared context bundle | TBD |
| Judge outputs ingested with diagnostic fields | TBD |
| Tracking row `AU-000` updated | TBD |

## Final Code State

TBD
