# Story 6.4.4.2 UAT Results

## Status

H2 and H4 judge sessions are ingested. Both candidates fail the `rubric_v2` ship bar due material Category B regressions. Treat this story as an ablation study: do not ship H2-only or H4-only, and keep current `master` runtime behavior unchanged for now.

## Round Summary

| Round | Trigger | Single Variable | Result | Notes |
|---|---|---|---|---|
| 1 | H2 consent/legal decision table under rubric_v2 | H2 only | Fail ship bar | No structural blockers, but material Category B regressions. |
| 2 | H4 operational-notes trim under rubric_v2 | H4 only | Fail ship bar | No structural blockers, but material Category B regressions. |
| 3 | Accepted subset interaction check | H2+H4 only, if both pass | N/A | Neither individual candidate passed. |

## UAT Section Results

| Section | Result | Notes |
|---|---|---|
| §1 Baseline control | Pass | AC10 v2 baseline present and reused as control. |
| §2 H2 evidence | Fail ship bar | 270-row package generated with `prompt_shrink_mode=h2`; judge ingest and diff/stat outputs recorded. |
| §3 H4 evidence | Fail ship bar | 270-row package generated with `prompt_shrink_mode=h4`; judge ingest and diff/stat outputs recorded. |
| §4 Cursor judge sessions | Pass | H2 and H4 each have Claude, Grok, and GPT-5 mini outputs ingested. |
| §5 Accepted-subset interaction | N/A | Not run because neither individual candidate passed. |
| §6 Green gate | Pass | Focused tests passed; backend regression `805 passed, 26 skipped`. Frontend checks not applicable. |
| §7 Final decision | Measured/no-change | Do not ship H2-only or H4-only. |

