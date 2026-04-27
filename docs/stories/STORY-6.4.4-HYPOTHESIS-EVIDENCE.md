# Story 6.4.4 Hypothesis Evidence

## Summary

Story 6.4.4 measured prompt-shrink candidates H1, H2, H4, and combined H1+H2+H4 against the frozen `prompts-v1.0` benchmark set.

Evidence now includes:

- deterministic mock structural sweeps,
- live provider runs for baseline/H1/H2/H4/combined,
- 15 Cursor judge outputs,
- judge ingest summaries,
- live diff/statistics reports.

## Prompt Size Deltas

| Hypothesis | Before chars | After chars | Delta |
|---|---:|---:|---:|
| H1 locale block | 2395 | 91 | -2304 |
| H2 consent block | 1960 | 748 | -1212 |
| H4 context pack trim | 6595 | 6355 | -240 |
| Combined subtotal | 10950 | 7194 | -3756 |

## Live Runs And Judge Packages

| Variant | Eval run | Judge package | Judge ingest | Diff output |
|---|---|---|---|---|
| Baseline | `story-6.4.2-post-cleanup-baseline` | `.../story-6.4.2-post-cleanup-baseline/judge-package/` | 10 rows, 3 judges | baseline side |
| H1 | `story-6.4.4-live-h1-locale-one-line` | `.../story-6.4.4-live-h1-locale-one-line/judge-package/` | 10 rows, 3 judges | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h1/` |
| H2 | `story-6.4.4-live-h2-consent-decision-table` | `.../story-6.4.4-live-h2-consent-decision-table/judge-package/` | 10 rows, 3 judges | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h2/` |
| H4 | `story-6.4.4-live-h4-operational-trim` | `.../story-6.4.4-live-h4-operational-trim/judge-package/` | 10 rows, 3 judges | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-h4/` |
| Combined | `story-6.4.4-live-h1-h2-h4-combined` | `.../story-6.4.4-live-h1-h2-h4-combined/judge-package/` | 10 rows, 3 judges | `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-combined/` |

All live variant runs completed with:

- matched rows: 10/10,
- schema blockers: none,
- boundary blockers: none,
- collision blockers: none.

## Category B Results

| Hypothesis | Structural result | Category B result | Tool recommendation | Story decision |
|---|---|---|---|---|
| H1 locale one-line | No blockers | All semantic metrics inconclusive at n=10. Locale fidelity dropped from 5.0 to 4.85 (`p=0.0811`). | `rerun-at-n15` | Not evidence-backed for merge; PM/SM decision required. |
| H2 consent decision table | No blockers | All semantic metrics inconclusive at n=10. Validation intent dropped from 4.85 to 4.6 (`p=0.1081`); no significant regression. | `rerun-at-n15` | Not evidence-backed for auto-merge; plausible candidate for PM/SM acceptance or n=15 rerun. |
| H4 operational trim | No blockers | All semantic metrics inconclusive at n=10. Locale/coverage/label metrics unchanged at 5.0; row grouping dropped 4.7 to 4.55 (`p=0.1381`). | `rerun-at-n15` | Not evidence-backed for auto-merge; plausible candidate for PM/SM acceptance or n=15 rerun. |
| Combined H1+H2+H4 | No structural blockers | `locale_fidelity` significant regression: 5.0 to 4.6, `p=0.000202`, effect size 2.68. | `human-review` | Do not ship combined as-is. |

## Notable Advisory Deltas

| Hypothesis | Advisory note |
|---|---|
| H1 | Duration roughly unchanged; component count unchanged; no schema/collision/boundary regression. |
| H2 | Duration increased from 65.9s to 89.3s average (`p=0.0295`), advisory only. |
| H4 | Duration decreased from 65.9s to 54.5s average; component count slightly lower; no blockers. |
| Combined | Duration decreased from 65.9s to 45.4s average (`p=0.0258`), but locale fidelity regression blocks shipping combined. |

## Final Evidence Verdict

The evidence does not support merging the current combined prompt shrink state as-is.

Recommended PM/SM discussion points:

- Reject combined H1+H2+H4 due significant `locale_fidelity` regression.
- Treat H1 as suspect because the failing combined metric is locale-specific and H1 directly shrinks locale guidance.
- Decide whether H2 and/or H4 can be accepted on current n=10 evidence despite `rerun-at-n15` recommendations, or whether to rerun those candidates at n=15.
- If strict story criteria are applied, revert all inconclusive/failed prompt changes before merge and carry the candidates forward for n=15.

## Code State At Evidence Close

Current branch code still contains H1+H2+H4 so PM/SM can inspect the implemented candidates and associated tests. This is not a merge-ready ship decision until PM/SM explicitly choose one of:

1. accept a subset and revert the rest,
2. rerun selected variants at n=15,
3. close the story as measured-only with no prompt shrink shipped.

No changes were made to `prompts.yaml` or `rubric_v1.md`. No H3/H5/H6/Image-to-Form work was implemented.
