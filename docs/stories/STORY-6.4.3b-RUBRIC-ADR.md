# Story 6.4.3b ADR — Rubric v1 Governance

**Status:** Accepted for `rubric_v1`  
**Story:** 6.4.3b — Eval Judge Package + Rubric ADR  
**Decision Owner:** SM + Dev; Architect review required for rubric version changes  
**Date:** 2026-04-25

---

## Context

Epic 6 prompt changes need measured evidence. Category A structural metrics are deterministic and already covered by the 6.4.3a harness. Category B semantic quality requires judge scoring.

The approved brief locks the judge architecture:

- three judges via Cursor chats,
- GPT-5 mini as control,
- Claude and Gemini as cross-model primary judges,
- no API integration,
- rubric file versioning,
- future rubric changes require ADR and baseline re-snapshotting.

---

## Decision

Use `backend/tests/form_ai_eval/rubric_v1.md` as the locked rubric for the first generation of semantic judge scoring.

Primary score aggregation:

- Claude + Gemini mean is the primary metric value.
- GPT-5 mini is retained as a self-judging control and excluded from the primary mean.
- Bias delta is `gpt5mini_score - cross_model_mean`.

Rubric changes:

- Any scoring definition, anchor, metric key, or required JSON shape change creates `rubric_v2.md`.
- Bumping the rubric requires updating this ADR or adding a new ADR.
- Baseline judge packages must be regenerated and re-scored when the rubric version changes.

---

## Rationale

- Manual Cursor chats avoid new secrets and model API clients.
- A file-versioned rubric makes experiments reproducible.
- Claude + Gemini primary mean reduces GPT-5 mini self-preference risk.
- Keeping GPT-5 mini as control still surfaces self-bias deltas for the closeout retro.

---

## Consequences

Positive:

- Prompt experiments can cite stable semantic scoring evidence.
- Judge workflow remains low-cost and no-secret.
- Future rubric changes are visible and auditable.

Negative:

- Anthony has manual copy/paste work per sweep.
- Judging remains asynchronous and human-orchestrated.
- Rubric errors require re-scoring affected baselines.

---

## Implementation Evidence

Final rubric: `backend/tests/form_ai_eval/rubric_v1.md`.

Final Category B metric list:

- `field_coverage_recall`
- `field_label_f1`
- `validation_intent_accuracy`
- `row_group_agreement`
- `locale_fidelity`
- `copy_quality_score`

Required judge JSON shape:

- top-level `rubric_version = "rubric_v1"`,
- top-level `judge_model` matching `gpt5mini`, `claude`, or `gemini`,
- `rows[]` containing `row_id`, `prompt_id`, `repetition_index`, `variant_label`, `scores`, and `rationale`,
- `scores` must contain exactly the six Category B metric keys with numeric values from `0` to `5`.

Judge package folder shape:

```text
_bmad-output/eval-runs/<run-id>/judge-package/
├── rubric_v1.md
├── judge-input-batch.md
├── judge-output-template.json
├── judge-package-metadata.json
└── results/
```

Ingest behavior:

- validates required result files when present under `results/`,
- rejects missing rows, duplicate rows, unknown row IDs, malformed metric keys, and out-of-range scores,
- computes Claude + Gemini per-metric means as the primary judge score,
- computes GPT-5 mini self-bias deltas as `gpt5mini_score - cross_model_mean`,
- computes row-level judge agreement from Claude/Gemini score distance,
- writes local summary artifacts even when DB persistence is unavailable,
- updates nullable `log.FormAiEvalRun` judge fields when DB persistence is enabled and rows can be mapped.

Rubric v2 is required when any of these change:

- metric key names,
- score ranges or anchors,
- required JSON shape,
- active scoring categories,
- judge role semantics, including which model is excluded from the primary mean.

Baseline re-snapshot policy:

- Existing `rubric_v1` judge outputs remain valid only for `rubric_v1` comparisons.
- If `rubric_v2.md` is introduced, baseline judge packages must be regenerated from the same eval run artifacts and re-scored with the new rubric.
- Diff/statistical reports must not compare `rubric_v1` and `rubric_v2` scores as if they were the same measurement.

---

## Review Questions

1. Are all Category B metrics scoreable from the generated package without hidden context?
2. Are score anchors specific enough for three different models to follow consistently?
3. Does the JSON schema make invalid/missing rows obvious before ingest?
4. Does the workflow clearly tell Anthony which Cursor model to use for each file?
5. Is the rubric narrow enough to avoid judging style before H5/H6 stories?
