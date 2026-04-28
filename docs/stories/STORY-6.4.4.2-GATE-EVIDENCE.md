# Story 6.4.4.2 Gate Evidence

## Scope

Re-evaluate H2/H4 prompt-shrink candidates under `prompts-v1.1` / `rubric_v2`; retain only evidence-backed winners.

## Automated Checks

| Check | Command | Result |
|---|---|---|
| Preflight | `.\scripts\workflow\preflight-story.ps1 -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4.2-h2-h4-rubric-v2-rerun" -ExpectedBranch "story/epic6-6.4.4.2-h2-h4-rubric-v2-rerun" -ReportFile "docs/stories/STORY-6.4.4.2-PREFLIGHT.md"` | PASS |
| Focused backend tests | `python -m pytest backend/tests/test_judge_pack.py backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_form_ai_eval_harness.py --tb=short` | `31 passed` |
| Backend regression | `python -m pytest backend/tests --tb=short` | `805 passed, 26 skipped` |
| Frontend lint | `npm run lint` | Not applicable unless frontend files are touched |
| Frontend unit tests | `npm run test:unit -- --watch=false` | Not applicable unless frontend files are touched |
| Stale-field audit | `gh pr view 79 --json state,isDraft,mergedAt,headRefName,baseRefName,url`; workflow-guide stale-field scan across story/status docs | PASS: PR #79 is open against `master`; no unintended stale status placeholders remain |

## Eval/Judge Gates

| Gate | Result |
|---|---|
| AC10 baseline present and valid | PASS: `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/judge-ingest-summary.json`, 270 rows, Claude + Grok primary, GPT-5 mini control |
| H2 run complete | PASS: six locale slices completed, aggregate package `_bmad-output/eval-runs/story-6.4.4.2-h2-consent-v2/judge-package/`, 270/270 generated definitions |
| H2 judge outputs ingested | PASS: `_bmad-output/eval-runs/story-6.4.4.2-h2-consent-v2/judge-package/judge-ingest-summary.json`, 270 rows, Claude + Grok primary, GPT-5 mini control |
| H2 diff/stat output recorded | PASS: `_bmad-output/eval-runs/story-6.4.4.2-baseline-vs-h2-consent-v2/`; no structural blockers, material Category B regressions |
| H4 run complete | PASS: six locale slices completed, aggregate package `_bmad-output/eval-runs/story-6.4.4.2-h4-operational-trim-v2/judge-package/`, 270/270 generated definitions |
| H4 judge outputs ingested | PASS: `_bmad-output/eval-runs/story-6.4.4.2-h4-operational-trim-v2/judge-package/judge-ingest-summary.json`, 270 rows, Claude + Grok primary, GPT-5 mini control |
| H4 diff/stat output recorded | PASS: `_bmad-output/eval-runs/story-6.4.4.2-baseline-vs-h4-operational-trim-v2/`; no structural blockers, material Category B regressions |
| Accepted H2+H4 subset checked if needed | N/A: neither H2 nor H4 passed individually |

