# Story 6.4.5 Gate Evidence

## Scope

Implement and measure H3 Component Property Cheat Sheet; ship only if `prompts-v1.1` / `rubric_v2` evidence clears the bar.

## Automated Checks

| Check | Command | Result |
|---|---|---|
| Preflight | `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.5-component-property-cheat-sheet" -ExpectedBranch "story/epic6-6.4.5-component-property-cheat-sheet" -ReportFile "docs/stories/STORY-6.4.5-PREFLIGHT.md"` | TBD |
| Focused backend tests | `python -m pytest backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_form_ai_eval_harness.py backend/tests/test_judge_pack.py --tb=short` | TBD |
| Backend regression | `python -m pytest backend/tests --tb=short` | TBD |
| Frontend lint | `npm run lint` | Not applicable unless frontend files are touched |
| Frontend unit tests | `npm run test:unit -- --watch=false` | Not applicable unless frontend files are touched |

## Eval/Judge Gates

| Gate | Result |
|---|---|
| AC10 baseline present and valid | TBD |
| H3 run complete | TBD |
| H3 judge package generated | TBD |
| H3 judge outputs ingested | TBD |
| H3 diff/stat output recorded | TBD |

