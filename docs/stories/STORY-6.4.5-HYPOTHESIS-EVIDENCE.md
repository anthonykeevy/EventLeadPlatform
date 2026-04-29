# Story 6.4.5 Hypothesis Evidence

## Summary

This file records H3: Component Property Cheat Sheet under `prompts-v1.1` / `rubric_v2`.

Final verdict: **no-go as-is / measured no-change**. H3 produced useful positive signals, but it also introduced material Category B regressions and the current benchmark frame mixes prompt-candidate effects with locale/context-conflict noise. The H3 prompt block was removed from the final shipped state.

Control baseline: `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/`.

## Baseline Control

| Field | Value |
|---|---|
| Run id | `story-6.4.4.1-ac10-baseline-v2` |
| Benchmark | `prompts-v1.1` |
| Rubric | `rubric_v2` |
| Rows | 270 |
| Generated definitions | 270/270 |
| Judge ingest summary | `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package/judge-ingest-summary.json` |

## H3 Prompt Delta

| Candidate | Before chars | After chars | Delta | Notes |
|---|---:|---:|---:|---|
| H3 component property cheat sheet | N/A | N/A | N/A | Implemented and measured during the run, then reverted before closeout. Final shipped prompt state is unchanged. |

## Variant Evidence

| Candidate | Run id | Judge package | Judge ingest | Diff/stat output | Verdict |
|---|---|---|---|---|---|
| H3 | `story-6.4.5-h3-component-property-cheat-sheet` | `_bmad-output/eval-runs/story-6.4.5-h3-component-property-cheat-sheet/judge-package/` | `_bmad-output/eval-runs/story-6.4.5-h3-component-property-cheat-sheet/judge-package/judge-ingest-summary.json` | `_bmad-output/eval-runs/story-6.4.5-baseline-vs-h3-component-property-cheat-sheet/diff-report.md` | No-go as-is / measured no-change |

## Judge Prompt Paths

- Claude: `_bmad-output/eval-runs/story-6.4.5-h3-component-property-cheat-sheet/judge-package/judge-prompt-claude.md`
- Grok: `_bmad-output/eval-runs/story-6.4.5-h3-component-property-cheat-sheet/judge-package/judge-prompt-grok.md`
- GPT-5 mini: `_bmad-output/eval-runs/story-6.4.5-h3-component-property-cheat-sheet/judge-package/judge-prompt-gpt5mini.md`

## Diff / Statistics Summary

Diff output:

- Markdown: `_bmad-output/eval-runs/story-6.4.5-baseline-vs-h3-component-property-cheat-sheet/diff-report.md`
- JSON: `_bmad-output/eval-runs/story-6.4.5-baseline-vs-h3-component-property-cheat-sheet/diff-summary.json`
- CSV: `_bmad-output/eval-runs/story-6.4.5-baseline-vs-h3-component-property-cheat-sheet/diff-details.csv`

Structural result:

- Matched rows: 270.
- Blocking structural regressions: none.
- `schema_valid` remained usable for the generated set; `boundary_violation_count` did not introduce blockers.

Category B primary judge deltas:

| Metric | Baseline mean | H3 mean | Delta | Decision |
|---|---:|---:|---:|---|
| `field_coverage_recall` | 4.4093 | 4.8574 | +0.4481 | win |
| `field_label_f1` | 4.9852 | 4.0611 | -0.9241 | regression |
| `validation_intent_accuracy` | 4.4093 | 4.0278 | -0.3815 | regression |
| `row_group_agreement` | 4.8019 | 4.6574 | -0.1444 | regression |
| `locale_fidelity` | 3.7889 | 4.2259 | +0.4370 | win |
| `policy_compliance` | 3.9519 | 4.5167 | +0.5648 | win |
| `cultural_register` | 4.0889 | 4.3722 | +0.2833 | win |
| `cross_locale_leakage` | 3.9352 | 4.1556 | +0.2204 | inconclusive |
| `format_pattern_accuracy` | 3.9093 | 4.2519 | +0.3426 | win |
| `copy_quality_score` | 4.3574 | 4.4426 | +0.0852 | advisory |

Interpretation: H3 improved several high-level metrics, but the material `field_label_f1` regression is not acceptable for merge. The current cross-locale/adversarial benchmark also confounds H3 with locale/context conflicts, so the positive signals are not clean enough to ship.

## Decision Notes

- H3 should not ship from this PR.
- Reason: material `field_label_f1` regression plus unresolved locale/context-conflict noise in the current evaluation framework.
- Evaluation artifacts and judge outputs are preserved as evidence.
- Recommendation: pause further prompt-candidate sweeps until an AU-only diagnostic evaluation framework is implemented.

## Final Verdict

**Measured/no-change.** H3 is no-go as-is and was reverted from the final shipped state. PR #81 can close as evidence-only/no-change after final gate evidence is recorded.

