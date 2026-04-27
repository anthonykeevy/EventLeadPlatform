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

---

## Supersession status (added 2026-04-27 by Story 6.4.4 closeout amendment)

**Status:** rubric_v1 is being superseded by rubric_v2 under Story 6.4.4.1 — Locale Architecture: Wire the Registry.

**Trigger:** Story 6.4.4 measured a `locale_fidelity` regression (`p=0.000202`, effect 2.68) on the combined H1+H2+H4 variant under rubric_v1, but PM analysis surfaced that (a) two of the three judges (Gemini 2.5 Flash, GPT-5 mini) gave 60/60 perfect 5/5 across all 5 runs — structurally zero variance — and (b) `prompts-v1.0` contained no locale anchor per prompt, so `locale_fidelity` had no ground truth. Tonyk's lived AU experience confirmed several of Claude's locale downscores were AU-pedantry false positives. See [`STORY-6.4.4-CLOSEOUT-AMENDMENT.md`](./STORY-6.4.4-CLOSEOUT-AMENDMENT.md) and [`_bmad-output/planning-artifacts/STORY-6.4.4.1-SM-HANDOFF-BRIEF.md`](../../_bmad-output/planning-artifacts/STORY-6.4.4.1-SM-HANDOFF-BRIEF.md) for the full reasoning chain.

**What rubric_v2 changes (drafted in Story 6.4.4.1):**

- Replaces the single-anchor `locale_fidelity` metric with a 9-element scoring rubric (Memo 2's 8 + Memo 3's cross-locale leakage element).
- Splits scoring methodology: 6 elements deterministic (regex / field presence / convention check) + 3 elements LLM-judged (consent citation, tone register, mandatory-field strictness).
- Adds Tonyk's lived-AU calibration anchors (e.g. "First name / Last name" → full marks; mandatory `+61` prefix on AU domestic form → score 0).
- Bumps the required JSON shape (`rubric_version: rubric_v2`; new `judge_model_version` field; new metric keys).
- Pinned model versions for all three judges (Claude 4.7 + Grok 4 + GPT-5 mini control); Gemini 2.5 Flash retired from the panel.

**Validity boundary:**

- rubric_v1 judge outputs (including all Story 6.4.4 results) **remain valid only for rubric_v1 comparisons**.
- Cross-comparison of rubric_v1 and rubric_v2 scores is explicitly disallowed by the "Baseline re-snapshot policy" section above.
- When rubric_v2 lands, baseline judge packages will be regenerated from the same eval run artifacts and re-scored under v2 (per the existing policy).

**ADR successor:** `docs/stories/STORY-6.4.4.1-RUBRIC-V2-ADR.md` (drafted concurrently with the closeout amendment as part of the Story 6.4.4.1 SM pack).

This ADR remains the authoritative governance document for `rubric_v1` for as long as rubric_v1 outputs are referenced in the historical record.
