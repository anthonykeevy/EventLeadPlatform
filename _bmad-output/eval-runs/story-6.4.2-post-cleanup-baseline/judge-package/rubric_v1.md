# Form AI Eval Rubric v1

**Rubric version:** `rubric_v1`  
**Benchmark set:** `prompts-v1.0`  
**Story:** 6.4.3b — Eval Judge Package + Rubric ADR

This rubric scores semantic quality for Form AI generated definitions. Judge only the anonymised package content supplied in `judge-input-batch.md`; do not infer hidden product requirements or use external knowledge.

## Judge Workflow

1. Read this rubric completely.
2. Read each package row independently.
3. Score every Category B metric from `0` to `5`.
4. Return JSON that matches `judge-output-template.json`.
5. Include short rationales grounded in package evidence.
6. Do not modify `row_id`, `prompt_id`, `repetition_index`, or `variant_label`.

## Score Scale

| Score | Anchor |
|-------|--------|
| 0 | Missing, unusable, or contradicts the prompt. |
| 1 | Major omissions or severe mismatch; only a small part is useful. |
| 2 | Some correct intent, but important fields, labels, validations, or grouping are weak. |
| 3 | Mostly usable with moderate gaps or unclear details. |
| 4 | Strong fit with minor omissions or wording issues. |
| 5 | Excellent fit; complete, clear, and faithful to the prompt and context. |

## Category B Metrics

### `field_coverage_recall`

How completely the generated form covers the fields and user intents requested by the prompt.

- `0`: Almost all requested fields are missing.
- `3`: Core fields are present, but one or two important requested concepts are missing.
- `5`: All required fields and prompt-specific edge cases are represented.

### `field_label_f1`

How accurately and clearly field labels/options map to the requested concepts.

- `0`: Labels are absent, generic, misleading, or mostly unrelated.
- `3`: Labels are understandable but several are vague, duplicated, or awkward.
- `5`: Labels and option text are precise, user-facing, and easy to judge against the prompt.

### `validation_intent_accuracy`

How well required/optional status, validation types, consent, acknowledgement, and input constraints match the prompt.

- `0`: Validation intent is missing or actively wrong.
- `3`: Basic required fields are reasonable, but nuanced validation/consent intent is incomplete.
- `5`: Validation and consent behavior clearly matches the requested form intent.

### `row_group_agreement`

How well sections, pages, ordering, and grouping support the flow implied by the prompt.

- `0`: Form structure is disordered or groups unrelated fields together.
- `3`: Ordering is mostly usable with some grouping or flow issues.
- `5`: Structure is coherent, deterministic, and easy for an end user to complete.

### `locale_fidelity`

How well terminology, dates, phone/contact patterns, currency/tax wording, and legal terms stay appropriate for the prompt without inventing incompatible locale assumptions.

- `0`: Locale-sensitive wording is clearly wrong or inconsistent.
- `3`: Mostly neutral wording with minor assumptions or missed locale cues.
- `5`: Locale-sensitive wording is neutral or correctly aligned with the prompt/context.

### `copy_quality_score`

How clear, concise, consistent, and professional the generated form copy is.

- `0`: Copy is confusing, unprofessional, or unusable.
- `3`: Copy is understandable but verbose, inconsistent, or slightly awkward.
- `5`: Copy is concise, consistent, and production-ready for the requested form.

## Required JSON Shape

Each judge output file must be valid JSON:

```json
{
  "rubric_version": "rubric_v1",
  "judge_model": "claude",
  "rows": [
    {
      "row_id": "p-01-event-registration-conference__r01",
      "prompt_id": "p-01-event-registration-conference",
      "repetition_index": 1,
      "variant_label": "post-642-capability-cleanup",
      "scores": {
        "field_coverage_recall": 4,
        "field_label_f1": 4,
        "validation_intent_accuracy": 3,
        "row_group_agreement": 4,
        "locale_fidelity": 5,
        "copy_quality_score": 4
      },
      "rationale": "Short evidence-based explanation."
    }
  ]
}
```

## Edge Cases

- If a generated definition omits the final rendered JSON, score only from the visible package content and explain the limitation in `rationale`.
- Do not penalise a form for avoiding payment processing when the prompt asks only for payment acknowledgement or donation interest.
- Do penalise invented sensitive fields that were not requested.
- Treat clearly future style/layout metrics as out of scope for `rubric_v1`; this rubric scores semantic form quality only.
- If obvious PII-adjacent values were scrubbed, judge the surrounding field intent rather than the placeholder token.

## Future Category C Placeholders

Future H5/H6 stories may add style, density, and conversion-focused metrics. Those are not active in `rubric_v1` and must not be included in judge scores.
