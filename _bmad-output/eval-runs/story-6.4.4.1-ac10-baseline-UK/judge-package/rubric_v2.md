# Form AI Eval Rubric v2

**Rubric version:** `rubric_v2`
**Benchmark set:** `prompts-v1.1`
**Story:** 6.4.4.1 — Locale Architecture: Wire the Registry

Judge only the anonymised package content supplied in `judge-input-batch.md`. Use the row's `audience_locale`, `expected_signals`, and `llm_judge_focus` metadata when scoring locale behavior.

## Judge Workflow

1. Score every Category B metric from `0` to `5`.
2. Return JSON matching `judge-output-template.json`.
3. Include `judge_model_version` at top level.
4. Ground rationales in visible package evidence.

## Score Scale

| Score | Anchor |
|-------|--------|
| 0 | Missing, unusable, or contradicts prompt/locale. |
| 1 | Major omissions or severe mismatch. |
| 2 | Some correct intent, but important gaps remain. |
| 3 | Mostly usable with moderate gaps. |
| 4 | Strong fit with minor omissions. |
| 5 | Excellent fit, complete and locale-faithful. |

## Category B Metrics

### `field_coverage_recall`
Completeness of requested fields and intent.

### `field_label_f1`
Clarity and semantic accuracy of labels and option text.

### `validation_intent_accuracy`
Required/optional status, validation types, consent, acknowledgement, and constraints.

### `row_group_agreement`
Sections, ordering, grouping, and completion flow.

### `locale_fidelity`
Overall alignment with `audience_locale`.

### `policy_compliance`
Privacy, consent, marketing opt-in, sensitive-field avoidance, and legal-reference appropriateness.

### `cultural_register`
Tone/register fit using `llm_judge_focus.tone_register` and mandatory-language strictness.

### `cross_locale_leakage`
Absence of forbidden locale leaks listed in `expected_signals.cross_locale_leakage_forbidden`.

### `format_pattern_accuracy`
Date, phone, address, currency, and naming convention fit against `expected_signals`.

### `copy_quality_score`
Clear, concise, consistent, production-usable copy.

## Required JSON Shape

```json
{
  "rubric_version": "rubric_v2",
  "judge_model": "claude",
  "judge_model_version": "claude-4.7",
  "rows": [
    {
      "row_id": "p01-au-neutral-r1__r01",
      "prompt_id": "p01-au-neutral-r1",
      "repetition_index": 1,
      "variant_label": "current-master-baseline",
      "scores": {
        "field_coverage_recall": 4,
        "field_label_f1": 4,
        "validation_intent_accuracy": 3,
        "row_group_agreement": 4,
        "locale_fidelity": 5,
        "policy_compliance": 4,
        "cultural_register": 4,
        "cross_locale_leakage": 5,
        "format_pattern_accuracy": 5,
        "copy_quality_score": 4
      },
      "rationale": "Short evidence-based explanation."
    }
  ]
}
```

## Calibration Anchors

- AU/NZ: penalise US-only ZIP/cell-phone/MM-DD wording; reward Privacy Act references only when privacy/consent copy is present.
- UK/EU/IE: reward GDPR/UK GDPR where appropriate; penalise CCPA-only language.
- US: penalise invented SSN/TIN fields; CCPA/CPRA should appear only when California is explicitly implied.
- INTL_ONLINE: reward neutral E.164/ISO/country-aware patterns; penalise country-specific legal claims.
- Adversarial prompts: do not reward explicitly requested cross-locale leakage when it conflicts with `audience_locale`.
