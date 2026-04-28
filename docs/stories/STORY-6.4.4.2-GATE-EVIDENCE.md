# Story 6.4.4.2 Gate Evidence

## Scope

Re-evaluate H2/H4 prompt-shrink candidates under `prompts-v1.1` / `rubric_v2`; retain only evidence-backed winners.

## Automated Checks

| Check | Command | Result |
|---|---|---|
| Preflight | `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4.2-h2-h4-rubric-v2-rerun" -ExpectedBranch "story/epic6-6.4.4.2-h2-h4-rubric-v2-rerun" -ReportFile "docs/stories/STORY-6.4.4.2-PREFLIGHT.md"` | TBD |
| Focused backend tests | TBD | TBD |
| Backend regression | `python -m pytest backend/tests --tb=short` | TBD |
| Frontend lint | `npm run lint` | Not applicable unless frontend files are touched |
| Frontend unit tests | `npm run test:unit -- --watch=false` | Not applicable unless frontend files are touched |

## Eval/Judge Gates

| Gate | Result |
|---|---|
| AC10 baseline present and valid | TBD |
| H2 run complete | TBD |
| H2 judge outputs ingested | TBD |
| H2 diff/stat output recorded | TBD |
| H4 run complete | TBD |
| H4 judge outputs ingested | TBD |
| H4 diff/stat output recorded | TBD |
| Accepted H2+H4 subset checked if needed | TBD |

