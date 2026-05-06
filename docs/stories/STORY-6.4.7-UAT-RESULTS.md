# Story 6.4.7 UAT Results

**Story:** 6.4.7 - AU Baseline Analysis And Iterative Prompt Improvement Loop  
**Status:** Complete  
**UAT owner:** Tony + SM

## Round Summary

| Round | Date | Scope | Result | Notes |
|---|---|---|---|---|
| 1 | 2026-05-05 | Baseline review and AU-001 candidate approval | Pass | `AU-000` evidence reviewed; Tony approved the first controlled experiment. |
| 2 | 2026-05-05 | AU-001 and AU-002 evaluation | Pass | AU-001 proved strict AU direction; AU-002 showed cleaner wording was too weak. |
| 3 | 2026-05-06 | AU-003 and AU-004 evaluation | Pass | AU-003 became the behavioural base; AU-004 proved soft lint-clean wording regressed output quality. |
| 4 | 2026-05-06 | AU-005 and AU-006 evaluation + closeout | Pass | AU-005 produced the strongest judged result; AU-006 proved lint-clean wording but regressed policy/validation/copy quality. |

## Section Results

| Section | Result | Notes |
|---|---|---|
| Section 1 Baseline review | Pass | `AU-000`, deterministic findings, judge conflicts, weak rows, and responsible sections reviewed. |
| Section 2 Candidate proposal gate | Pass | Initial top five candidates were recorded before AU-001. Later rounds were Tony-approved continuations. |
| Section 3 Scope boundary | Pass | Story remained Analyst/evidence focused; production implementation is deferred to follow-up. |
| Section 4 Experiment config | Pass | AU-001 through AU-006 configs and overlays are stored under `docs/stories/experiments/`. |
| Section 5 Candidate eval run | Pass | Candidate runs and diff artifacts exist under `_bmad-output/eval-runs/story-6.4.7-au-*/`. |
| Section 6 Cursor judge sessions | Pass | Claude-family, Grok, and GPT-5 mini judge outputs were ingested for the completed rounds. |
| Section 7 Candidate comparison | Pass | Gate evidence and tracking rows compare metric movement, deterministic findings, and regressions. |
| Section 8 Tracking sheet | Pass | `AU-001` through `AU-006` rows are recorded in `STORY-6-AU-EVAL-ITERATION-TRACKING.md`. |
| Section 9 Green gate | Pass | Focused Analyst green gate passed: `18 passed`, `116 warnings`. |
| Section 10 Final decision | Pass | Close Story 6.4.7; use AU-005 as the production behaviour target and AU-006 as lint-clean wording evidence. |

## Final UAT Decision

UAT is complete. Story 6.4.7 is accepted as an Analyst-owned evaluation and decision story. The follow-up work should promote AU-005 behaviour into production prompt/context sections while preserving AU-006's lint-clean conflict wording lessons.
