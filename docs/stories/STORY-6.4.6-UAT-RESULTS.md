# Story 6.4.6 UAT Results

**Story:** 6.4.6 - AU-Only Diagnostic Evaluation Framework + Baseline  
**Status:** Automated UAT complete; pending Tony/SM final acceptance  
**UAT owner:** Tony + SM

## Round Summary

| Round | Date | Scope | Result | Notes |
|---|---|---|---|---|
| 1 | 2026-04-29 | Framework smoke evidence review | Pass | Automated framework smoke completed. |
| 2 | 2026-04-30 | Live single-row and parallel proof | Pass | One live row and three concurrent live rows completed successfully. |
| 3 | 2026-04-30 | Full live AU baseline aggregate | Pass | 45/45 live rows schema-valid; aggregate judge package generated. |
| 4 | 2026-04-30 | Judge sessions and ingest | Pass | Claude, Grok, and GPT-5 mini outputs saved and ingested; diagnostic fields validated after normalising placeholder/null and percentage confidence values. |

## Section Results

| Section | Result | Notes |
|---|---|---|
| Section 1 AU prompt set | Pass | Implementation smoke passed for `prompts-au-v1`. |
| Section 2 AU locale contract | Pass | `au-locale-contract-v1` created. |
| Section 3 Context preflight/shared bundle | Pass | Live aggregate artifacts produced. |
| Section 4 Deterministic AU checks | Pass | Live aggregate artifacts produced: 130 generated-output findings across 25 prompts, 0 prompt-context findings. |
| Section 5 Current-state AU baseline | Pass | 45/45 live rows completed and aggregated under `story-6.4.6-au-baseline-current`. |
| Section 6 Cursor judge sessions | Pass | Claude, Grok, and GPT-5 mini judge outputs saved under `judge-package/results/` and ingested. |
| Section 7 Tracking sheet handoff | Pass | `AU-000` updated with baseline run ID, deterministic findings, judge metrics, conflict findings, and handoff action. |
| Section 8 Green gate | Pass | Focused eval/judge/experiment rerun passed: 39 passed, 116 warnings in 2.04s. Full backend regression previously passed: 806 passed, 28 skipped, 5669 warnings in 1608.46s. Stale-field audit passed with only intentional draft/current-focus hits. |
| Section 9 Final decision | Pending Tony/SM | Automated UAT evidence is complete; Tony/SM final acceptance remains manual. |

## Final UAT Decision

Automated UAT is complete. Tony/SM final acceptance remains the only manual UAT decision.
