# Form AI Judge Input Batch

Run ID: `story-6.4.7-au-006-candidate-a`
Benchmark set: `prompts-au-v1`
Rubric version: `rubric_v2`

## Experiment Context

This judge package is for one candidate arm of an Analyst prompt experiment.

```json
{
  "baseline_run_id": "story-6.4.6-au-baseline-current",
  "candidate_hypothesis": "A production-style rewrite of AU-005 that avoids literal forbidden examples while preserving hard AU output constraints will retain AU-005's judged quality gains and reduce prompt-context lint findings.",
  "candidate_label": "candidate-a",
  "changed_section_id": "candidate_prompt_block",
  "eval_only": true,
  "expected_metric_movement": {
    "copy_quality_score": "increase",
    "cross_locale_leakage": "increase",
    "field_coverage_recall": "increase",
    "field_label_f1": "increase",
    "format_pattern_accuracy": "increase",
    "locale_fidelity": "increase",
    "policy_compliance": "increase",
    "row_group_agreement": "increase",
    "validation_intent_accuracy": "increase"
  },
  "experiment_id": "story-6.4.7-au-006",
  "improvement_goal": "production-style-strict-au-publish-ready",
  "known_risk_metrics": [
    "cultural_register"
  ],
  "scenario_slice": "au-all",
  "selected_prompt_ids": [],
  "system_prompt_addendum_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
  "target_metrics": [
    "locale_fidelity",
    "cross_locale_leakage",
    "format_pattern_accuracy",
    "policy_compliance",
    "field_coverage_recall",
    "validation_intent_accuracy",
    "copy_quality_score",
    "row_group_agreement",
    "field_label_f1"
  ]
}
```

Use `rubric_v2.md` and return JSON matching `judge-output-template.json`.
Set `judge_model_version` to the exact model/version shown in your Cursor session.
Before assigning scores for each row, identify at least one weakness per row before scoring.
Use `shared-context-bundle.json` to inspect prompt/context sections. Fill the diagnostic fields for conflicts, likely responsible section IDs, suggested correction, and confidence.
Judge only the anonymised package content below.

## Row 1: `p01-au-neutral-r1__r01`

- Prompt ID: `p01-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "event-registration",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 39604,
  "failure_class": "none",
  "input_tokens": 3802,
  "output_tokens": 3841,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sales-conference-registration",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll send your registration confirmation here",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or direct number for event updates",
            "label": "Phone number",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "We order T-shirts based on this selection",
            "label": "T-shirt size",
            "options": [
              {
                "label": "XS",
                "value": "XS"
              },
              {
                "label": "S",
                "value": "S"
              },
              {
                "label": "M",
                "value": "M"
              },
              {
                "label": "L",
                "value": "L"
              },
              {
                "label": "XL",
                "value": "XL"
              },
              {
                "label": "XXL",
                "value": "XXL"
              }
            ],
            "placeholder": "Select your size",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 200,
            "helpText": "Tell us any dietary needs or allergies",
            "label": "Dietary requirements",
            "placeholder": "e.g. vegetarian, gluten-free, no nuts",
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 730
          },
          "props": {
            "height": 120,
            "helpText": "Opt in if you'd like to receive occasional offers and news",
            "label": "Marketing & offers",
            "options": [
              {
                "label": "Yes \u2014 send me marketing, event news and offers",
                "value": "marketing_opt_in"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-8",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 120,
            "label": "I agree to the event privacy notice and understand my information will be used to manage my registration and send important event updates.",
            "tabOrder": 8,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-9",
          "position": {
            "x": 40,
            "y": 1018
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 9,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Annual Sales Conference Registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 2: `p01-au-ambiguous-r1__r01`

- Prompt ID: `p01-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "event-registration",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 39025,
  "failure_class": "none",
  "input_tokens": 3874,
  "output_tokens": 3757,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sales-conference-registration-sydney",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send your registration confirmation here.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Local number for event updates and changes.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll provide T-shirts at the event.",
            "label": "T-shirt size",
            "options": [
              {
                "label": "XS",
                "value": "XS"
              },
              {
                "label": "S",
                "value": "S"
              },
              {
                "label": "M",
                "value": "M"
              },
              {
                "label": "L",
                "value": "L"
              },
              {
                "label": "XL",
                "value": "XL"
              },
              {
                "label": "XXL",
                "value": "XXL"
              }
            ],
            "placeholder": "Select size",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about allergies or special dietary needs.",
            "label": "Dietary requirements",
            "placeholder": "e.g. vegetarian, gluten-free, dairy allergy",
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-7",
          "position": {
            "x": 40,
            "y": 730
          },
          "props": {
            "height": 120,
            "helpText": "By registering you accept the event terms and our privacy practices.",
            "label": "I agree to the event terms and privacy policy",
            "tabOrder": 7,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-8",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 8,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Annual Sales Conference Registration \u2014 Sydney"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 3: `p01-au-adversarial-r1__r01`

- Prompt ID: `p01-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "event-registration",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 41575,
  "failure_class": "none",
  "input_tokens": 3884,
  "output_tokens": 4102,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sales-conference-registration",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 384,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Include country code for SMS/WhatsApp (e.g. +61 for Australia)",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "email-4",
          "position": {
            "x": 384,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send your registration confirmation here",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Australian 4-digit postcode",
            "label": "Postcode",
            "placeholder": "e.g. 2000",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "T-shirt size",
            "options": [
              {
                "label": "XS",
                "value": "XS"
              },
              {
                "label": "S",
                "value": "S"
              },
              {
                "label": "M",
                "value": "M"
              },
              {
                "label": "L",
                "value": "L"
              },
              {
                "label": "XL",
                "value": "XL"
              },
              {
                "label": "XXL",
                "value": "XXL"
              }
            ],
            "placeholder": "Select your size",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "None / No special requirements",
                "value": "none"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "placeholder": "Please specify any other dietary needs",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 838
          },
          "props": {
            "height": 120,
            "label": "I agree to the event terms and privacy policy",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 982
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Annual Sales Conference Registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 4: `p02-au-neutral-r1__r01`

- Prompt ID: `p02-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 40868,
  "failure_class": "none",
  "input_tokens": 3799,
  "output_tokens": 4059,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1466,
    "width": 960
  },
  "formId": "conference-rsvp-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We will send booking confirmations and event updates to this address.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We may send urgent event updates by SMS.",
            "label": "Mobile phone",
            "placeholder": "04xx xxx xxx",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Select the session you plan to attend.",
            "label": "Session selection",
            "options": [
              {
                "label": "Full-day pass (all sessions)",
                "value": "full_day"
              },
              {
                "label": "Keynote + Networking (morning)",
                "value": "keynote_morning"
              },
              {
                "label": "Workshop A \u2014 Data Ethics (afternoon)",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B \u2014 AI in Healthcare (afternoon)",
                "value": "workshop_b"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Tick all that apply.",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "No dietary requirements",
                "value": "none"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Other (please specify below)",
                "value": "other"
              }
            ],
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 200,
            "helpText": "Include any allergies or special requirements.",
            "label": "Other dietary requirements (please specify)",
            "placeholder": "List allergies, intolerances or details we should know",
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 200,
            "helpText": "Supply any information that will help us accommodate you.",
            "label": "Accessibility or additional requirements (optional)",
            "placeholder": "Let us know any accessibility needs or other requests",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 1178
          },
          "props": {
            "height": 120,
            "helpText": "You can opt out at any time. We will use your contact details for event updates, program changes and occasional event offers.",
            "label": "I consent to receive event updates and important communications by email and SMS.",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1322
          },
          "props": {
            "height": 72,
            "label": "RSVP",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Conference RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 5: `p02-au-ambiguous-r1__r01`

- Prompt ID: `p02-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 37724,
  "failure_class": "none",
  "input_tokens": 3871,
  "output_tokens": 4176,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sydney-conference-rsvp",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Hosted in Sydney. Please tell us about yourself and your session preference.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We'll use this for event updates and tickets.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include area code for calls or SMS.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose the primary session you will attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Keynote \u2014 Future of AI",
                "value": "keynote-ai"
              },
              {
                "label": "Workshop \u2014 Data Ethics",
                "value": "workshop-ethics"
              },
              {
                "label": "Panel \u2014 Industry Trends",
                "value": "panel-trends"
              },
              {
                "label": "Networking Session",
                "value": "networking"
              }
            ],
            "placeholder": "Select a session",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "No dietary requirements",
                "value": "none"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Dairy-free",
                "value": "dairy_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 200,
            "helpText": "Only needed if you selected 'Other'.",
            "label": "Other dietary details",
            "placeholder": "Please describe any other requirements (e.g. allergies)",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive event updates, program changes and marketing messages from the organiser.",
            "label": "Consent to receive event updates",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1090
          },
          "props": {
            "height": 72,
            "label": "RSVP",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Conference RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 6: `p02-au-adversarial-r1__r01`

- Prompt ID: `p02-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 41235,
  "failure_class": "none",
  "input_tokens": 3881,
  "output_tokens": 4510,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "conference-rsvp-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 567,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send your confirmation and updates to this address.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 567,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Local Australian number preferred for urgent updates.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "phone"
        },
        {
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode.",
            "label": "Address",
            "placeholder": "Street address",
            "tabOrder": 5,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "address"
        },
        {
          "id": "text-6",
          "position": {
            "x": 567,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Postcode",
            "placeholder": "e.g. 2000",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "text"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Please select the session you will attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Keynote & plenary",
                "value": "keynote_plenary"
              },
              {
                "label": "Track A: Data & AI",
                "value": "track_a_data_ai"
              },
              {
                "label": "Track B: Sustainability",
                "value": "track_b_sustainability"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 503
          },
          "type": "radio"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 567,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Select any dietary needs we should cater for.",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "None",
                "value": "none"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select one",
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 200,
            "label": "If other, please specify dietary needs",
            "placeholder": "Please list allergies or special requirements",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 120,
            "helpText": "We will send event updates and related information. By consenting you accept our event terms and privacy practices.",
            "label": "Consent to receive event updates",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-11",
          "position": {
            "x": 40,
            "y": 1018
          },
          "props": {
            "height": 72,
            "label": "RSVP",
            "tabOrder": 11,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Conference RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 7: `p03-au-neutral-r1__r01`

- Prompt ID: `p03-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 32667,
  "failure_class": "none",
  "input_tokens": 3797,
  "output_tokens": 3627,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "workshop-signup-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "helpText": "As you'd like us to address you",
            "label": "First name",
            "placeholder": "Enter your first name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Enter your family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll use this for essential event updates",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Mobile number for any urgent event contact",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "helpText": "Pick the option that best matches your experience",
            "label": "Skill level",
            "options": [
              {
                "label": "Beginner",
                "value": "beginner"
              },
              {
                "label": "Intermediate",
                "value": "intermediate"
              },
              {
                "label": "Advanced",
                "value": "advanced"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Choose the workshop stream you\u2019d most like to attend",
            "label": "Preferred stream",
            "options": [
              {
                "label": "Data & AI",
                "value": "data_ai"
              },
              {
                "label": "Design & UX",
                "value": "design_ux"
              },
              {
                "label": "Web development",
                "value": "web_dev"
              },
              {
                "label": "Product strategy",
                "value": "product_strategy"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a stream",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 120,
            "helpText": "Tick any support you need; we\u2019ll follow up to arrange details",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair_access"
              },
              {
                "label": "Auslan interpreter",
                "value": "auslan"
              },
              {
                "label": "Large print or alternative format",
                "value": "large_print"
              },
              {
                "label": "Quiet or low-sensory workspace",
                "value": "quiet_workspace"
              },
              {
                "label": "Assistance with mobility",
                "value": "mobility_assist"
              },
              {
                "label": "Other",
                "value": "other_access"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 580
          },
          "props": {
            "height": 200,
            "helpText": "Provide as much detail as you\u2019re comfortable sharing so we can support you",
            "label": "Details of accessibility needs",
            "placeholder": "Please describe any adjustments or assistance you need",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 884
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you\u2019d like occasional event updates and offers",
            "label": "Marketing preferences",
            "options": [
              {
                "label": "Yes \u2014 I\u2019d like to receive event updates and offers",
                "value": "marketing_opt_in"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 1028
          },
          "props": {
            "height": 120,
            "label": "I agree to the event privacy policy and consent to my information being used to manage my registration and send essential event communications.",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-11",
          "position": {
            "x": 40,
            "y": 1172
          },
          "props": {
            "height": 72,
            "label": "Sign up",
            "tabOrder": 11,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Workshop sign-up"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 8: `p03-au-ambiguous-r1__r01`

- Prompt ID: `p03-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 32254,
  "failure_class": "none",
  "input_tokens": 3869,
  "output_tokens": 3532,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sydney-workshop-signup",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Tell us a bit about yourself and which stream you'd like to attend in Sydney.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll use this for event updates and tickets.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include area code if not a mobile.",
            "label": "Phone number",
            "placeholder": "Mobile or daytime number",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide suburb, state and postcode for local admin.",
            "label": "Address (suburb, state, postcode)",
            "placeholder": "Suburb, State, Postcode",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select the option that best describes your current experience.",
            "label": "Skill level",
            "options": [
              {
                "label": "Beginner",
                "value": "beginner"
              },
              {
                "label": "Intermediate",
                "value": "intermediate"
              },
              {
                "label": "Advanced",
                "value": "advanced"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose the workshop stream you'd like to attend.",
            "label": "Preferred stream",
            "options": [
              {
                "label": "Python fundamentals",
                "value": "python_fundamentals"
              },
              {
                "label": "Data analysis with Python",
                "value": "data_analysis"
              },
              {
                "label": "Web development with JavaScript",
                "value": "web_development"
              }
            ],
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "Tick any supports you require. If none apply, leave blank.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Step-free access",
                "value": "step_free"
              },
              {
                "label": "Assistive listening / captioning",
                "value": "assistive_listening"
              },
              {
                "label": "Hands-on assistance",
                "value": "hands_on_assist"
              },
              {
                "label": "Dietary support for event catering",
                "value": "dietary_support"
              },
              {
                "label": "Other (please detail below)",
                "value": "other"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 200,
            "helpText": "Provide as much detail as you can so we can arrange suitable support.",
            "label": "Accessibility details",
            "placeholder": "Please describe any adjustments or requirements (e.g. mobility, hearing, visual, dietary).",
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-11",
          "position": {
            "x": 40,
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "By signing up you accept the event terms and consent to receive event communications.",
            "label": "I agree to the event terms and the privacy policy.",
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-12",
          "position": {
            "x": 40,
            "y": 1234
          },
          "props": {
            "height": 72,
            "label": "Sign up",
            "tabOrder": 12,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Workshop \u2014 Sign up"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 9: `p03-au-adversarial-r1__r01`

- Prompt ID: `p03-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 39697,
  "failure_class": "none",
  "input_tokens": 3879,
  "output_tokens": 4473,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1754,
    "width": 960
  },
  "formId": "workshop-signup-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll use this for booking and updates",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Provide a number we can use for event updates (include +61 for Australia).",
            "label": "Phone",
            "placeholder": "Include country code (e.g. +61)",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "4-digit Australian postcode",
            "label": "Postcode",
            "placeholder": "e.g. 3000",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Choose the option that best matches your experience",
            "label": "Skill level",
            "options": [
              {
                "label": "Beginner",
                "value": "beginner"
              },
              {
                "label": "Intermediate",
                "value": "intermediate"
              },
              {
                "label": "Advanced",
                "value": "advanced"
              }
            ],
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Preferred stream",
            "options": [
              {
                "label": "Design",
                "value": "design"
              },
              {
                "label": "Development",
                "value": "development"
              },
              {
                "label": "Research",
                "value": "research"
              },
              {
                "label": "Leadership",
                "value": "leadership"
              }
            ],
            "placeholder": "Select a stream",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Tick any that apply",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Hearing support / Auslan",
                "value": "hearing"
              },
              {
                "label": "Vision support",
                "value": "vision"
              },
              {
                "label": "Dietary requirements",
                "value": "dietary"
              },
              {
                "label": "Other (I will provide details below)",
                "value": "other"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 200,
            "helpText": "We\u2019ll contact you to arrange support if needed.",
            "label": "Accessibility details",
            "placeholder": "Tell us more about any accessibility needs or adjustments",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 1018
          },
          "props": {
            "height": 200,
            "label": "Additional comments",
            "placeholder": "Any other information for organisers",
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 1322
          },
          "props": {
            "height": 120,
            "helpText": "Optional \u2013 we\u2019ll send event information and related offers.",
            "label": "Event updates & marketing",
            "options": [
              {
                "label": "Yes, I\u2019d like to receive event updates and marketing",
                "value": "yes"
              }
            ],
            "tabOrder": 11,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-12",
          "position": {
            "x": 40,
            "y": 1466
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and the handling of my personal information.",
            "label": "Terms and privacy",
            "tabOrder": 12,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1610
          },
          "props": {
            "height": 72,
            "label": "Sign up",
            "tabOrder": 13,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Workshop signup"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 10: `p04-au-neutral-r1__r01`

- Prompt ID: `p04-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 39238,
  "failure_class": "none",
  "input_tokens": 3802,
  "output_tokens": 4487,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "webinar-registration-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "options": [],
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "options": [],
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We will send your webinar link to this address.",
            "label": "Email address",
            "options": [],
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Mobile number for urgent updates (optional).",
            "label": "Phone (optional)",
            "options": [],
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Organisation",
            "options": [],
            "placeholder": "Company or organisation",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Role / job title",
            "options": [],
            "placeholder": "e.g. Product Manager",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "We will schedule event times in this zone.",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT)",
                "value": "Australia/Sydney"
              },
              {
                "label": "Australia/Brisbane (AEST)",
                "value": "Australia/Brisbane"
              },
              {
                "label": "Australia/Adelaide (ACST/ACDT)",
                "value": "Australia/Adelaide"
              },
              {
                "label": "Australia/Perth (AWST)",
                "value": "Australia/Perth"
              },
              {
                "label": "UTC (Coordinated Universal Time)",
                "value": "UTC"
              },
              {
                "label": "Europe/London (BST/GMT)",
                "value": "Europe/London"
              },
              {
                "label": "America/New_York (EDT/EST)",
                "value": "America/New_York"
              },
              {
                "label": "Asia/Singapore (SGT)",
                "value": "Asia/Singapore"
              },
              {
                "label": "Asia/Tokyo (JST)",
                "value": "Asia/Tokyo"
              },
              {
                "label": "Other / IANA timezone",
                "value": "other"
              }
            ],
            "placeholder": "Select your timezone",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 200,
            "helpText": "We'll pass these to the presenter. Keep responses concise.",
            "label": "Questions for the speaker (optional)",
            "options": [],
            "placeholder": "Type any questions you'd like the speaker to address",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 864
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive webinar reminders and related communications.",
            "label": "Marketing and event updates",
            "options": [
              {
                "label": "Yes \u2014 email me event updates and occasional offers",
                "value": "opt_in_email"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 120,
            "helpText": "By registering you agree to our privacy and event terms. We will use your contact details to send event information and updates. See event terms: https://example.test/terms",
            "label": "Privacy & data handling",
            "options": [],
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-11",
          "position": {
            "x": 40,
            "y": 1152
          },
          "props": {
            "height": 72,
            "label": "Register",
            "options": [],
            "tabOrder": 11,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Webinar registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 11: `p04-au-ambiguous-r1__r01`

- Prompt ID: `p04-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 44838,
  "failure_class": "none",
  "input_tokens": 3874,
  "output_tokens": 5044,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "webinar-registration-sydney",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "This webinar is associated with Sydney. We'll send the joining link and any updates to the contact details you provide.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will email the webinar link and reminders to this address.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Mobile is useful for SMS reminders (optional).",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Optional",
            "label": "Organisation",
            "placeholder": "Company or institution",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Role / job title",
            "placeholder": "e.g. Marketing Manager",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Event time is Sydney (AEST/AEDT). Tell us where you'll join from.",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT)",
                "value": "Australia/Sydney"
              },
              {
                "label": "Australia/Melbourne (AEST/AEDT)",
                "value": "Australia/Melbourne"
              },
              {
                "label": "Australia/Brisbane (AEST)",
                "value": "Australia/Brisbane"
              },
              {
                "label": "Australia/Perth (AWST)",
                "value": "Australia/Perth"
              }
            ],
            "placeholder": "Select timezone",
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 200,
            "helpText": "We'll share submitted questions with the speaker to help guide the session.",
            "label": "Questions for the speaker",
            "placeholder": "Optional \u2014 let us know what you'd like the speaker to cover",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 936
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive news about future events and resources by email. You can unsubscribe at any time.",
            "label": "Marketing opt-in",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive event updates and marketing emails",
                "value": "opt_in_marketing"
              }
            ],
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-11",
          "position": {
            "x": 40,
            "y": 1080
          },
          "props": {
            "height": 120,
            "helpText": "Please review and accept our event terms and privacy policy to confirm your registration.",
            "label": "Event terms & privacy",
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-12",
          "position": {
            "x": 40,
            "y": 1224
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 12,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Webinar registration \u2014 Sydney"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 12: `p04-au-adversarial-r1__r01`

- Prompt ID: `p04-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 40074,
  "failure_class": "none",
  "input_tokens": 3884,
  "output_tokens": 4402,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1574,
    "width": 960
  },
  "formId": "webinar-registration-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Register below and we\u2019ll email the access link and details.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We may call about urgent event updates.",
            "label": "Phone (include country code)",
            "placeholder": "e.g. +61 4XX XXX XXX",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Organisation",
            "placeholder": "Company or organisation",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Role / job title",
            "placeholder": "e.g. Product manager",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Australian postcode (four digits).",
            "label": "Postcode",
            "placeholder": "e.g. 2000",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Select the timezone you\u2019ll attend from.",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT)",
                "value": "Australia/Sydney"
              },
              {
                "label": "Australia/Adelaide (ACST/ACDT)",
                "value": "Australia/Adelaide"
              },
              {
                "label": "Australia/Perth (AWST)",
                "value": "Australia/Perth"
              },
              {
                "label": "UTC",
                "value": "UTC"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-10",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "label": "If Other, specify timezone",
            "placeholder": "e.g. Europe/London",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 we\u2019ll pass selected questions to the presenter.",
            "label": "Questions for the speaker",
            "placeholder": "What would you like the speaker to cover?",
            "tabOrder": 11,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 1070
          },
          "props": {
            "height": 120,
            "helpText": "You can unsubscribe at any time.",
            "label": "Marketing and event updates",
            "options": [
              {
                "label": "Yes \u2014 send me webinar updates and occasional marketing emails",
                "value": "opt_in_marketing"
              }
            ],
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "paragraph-13",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 48,
            "label": "By registering you consent to us storing your contact details and sending event-related messages. We handle personal data in line with Australian privacy practice.",
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1286
          },
          "props": {
            "height": 120,
            "label": "Please accept the event terms and conditions",
            "tabOrder": 14,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-15",
          "position": {
            "x": 40,
            "y": 1430
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 15,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Webinar registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 13: `p05-au-neutral-r1__r01`

- Prompt ID: `p05-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 45824,
  "failure_class": "none",
  "input_tokens": 3803,
  "output_tokens": 4448,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1878,
    "width": 960
  },
  "formId": "wedding-rsvp-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We may send brief event updates by SMS.",
            "label": "Phone (mobile)",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes \u2014 I will attend",
                "value": "attend_yes"
              },
              {
                "label": "No \u2014 I can't attend",
                "value": "attend_no"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "checkbox-6",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 120,
            "helpText": "Select if you will bring a guest.",
            "label": "Plus one",
            "options": [
              {
                "label": "I will bring a plus-one",
                "value": "plus_one_yes"
              }
            ],
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "first-name-7",
          "position": {
            "x": 40,
            "y": 580
          },
          "props": {
            "height": 110,
            "label": "Plus-one first name",
            "placeholder": "Given name",
            "tabOrder": 7,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-8",
          "position": {
            "x": 424,
            "y": 580
          },
          "props": {
            "height": 110,
            "label": "Plus-one last name",
            "placeholder": "Family name",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 110,
            "label": "Main course selection",
            "options": [
              {
                "label": "Beef",
                "value": "beef"
              },
              {
                "label": "Chicken",
                "value": "chicken"
              },
              {
                "label": "Fish",
                "value": "fish"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              }
            ],
            "placeholder": "Choose a meal (if attending)",
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 200,
            "helpText": "Include details for you and any guest you bring.",
            "label": "Dietary requirements or allergies",
            "placeholder": "Please list any allergies, intolerances or special dietary needs",
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "text-11",
          "position": {
            "x": 40,
            "y": 1152
          },
          "props": {
            "height": 110,
            "label": "Song request",
            "placeholder": "Song title or artist",
            "tabOrder": 11,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1286
          },
          "props": {
            "height": 200,
            "label": "Message to the couple",
            "placeholder": "A short message or well wishes",
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1590
          },
          "props": {
            "height": 120,
            "helpText": "You can withdraw marketing consent at any time. Photography consent covers group photos and on-site event coverage.",
            "label": "I agree to receive essential wedding updates by email or SMS and consent to photography at the event. I understand how my personal information will be used for event administration in accordance with the privacy notice.",
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-14",
          "position": {
            "x": 40,
            "y": 1734
          },
          "props": {
            "height": 72,
            "label": "Send RSVP",
            "tabOrder": 14,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Wedding RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 14: `p05-au-ambiguous-r1__r01`

- Prompt ID: `p05-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 37909,
  "failure_class": "none",
  "input_tokens": 3875,
  "output_tokens": 3696,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1744,
    "width": 960
  },
  "formId": "wedding-rsvp-sydney",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We will use this to confirm your RSVP and send event updates.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 we'll only call if needed for urgent updates.",
            "label": "Phone (Australian format)",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes \u2014 I will be there",
                "value": "yes"
              },
              {
                "label": "No \u2014 I\u2019m sorry I can\u2019t attend",
                "value": "no"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "radio-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 120,
            "helpText": "If yes, please include their name in 'Message' below.",
            "label": "Bringing a plus-one?",
            "options": [
              {
                "label": "No",
                "value": "no"
              },
              {
                "label": "Yes \u2014 I will bring a guest",
                "value": "yes"
              }
            ],
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 110,
            "helpText": "Please select your preferred main course. Required if attending.",
            "label": "Meal choice (main)",
            "options": [
              {
                "label": "Roast chicken",
                "value": "chicken"
              },
              {
                "label": "Beef fillet",
                "value": "beef"
              },
              {
                "label": "Barramundi (fish)",
                "value": "fish"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Children's meal",
                "value": "children"
              }
            ],
            "placeholder": "Select a main course",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 200,
            "helpText": "Include allergies, intolerances or accessibility needs. Leave blank if none.",
            "label": "Dietary requirements or allergies",
            "placeholder": "Tell us any allergies, intolerances or dietary needs",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 we'll try to play requests during the reception.",
            "label": "Song request",
            "placeholder": "Artist \u2014 Song title",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 200,
            "helpText": "Use this to tell us the name of your plus-one or any additional notes.",
            "label": "Message & guest names",
            "placeholder": "Add a message, plus-one name(s) or other notes",
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 1312
          },
          "props": {
            "height": 120,
            "helpText": "Optional \u2014 receive a few emails with event updates and logistics.",
            "label": "Event updates",
            "options": [
              {
                "label": "Yes, I\u2019d like to receive event updates by email",
                "value": "updates_yes"
              }
            ],
            "tabOrder": 11,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-12",
          "position": {
            "x": 40,
            "y": 1456
          },
          "props": {
            "height": 120,
            "helpText": "By submitting you agree to our event terms and privacy handling of your RSVP data.",
            "label": "Privacy & event terms",
            "tabOrder": 12,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1600
          },
          "props": {
            "height": 72,
            "label": "Send RSVP",
            "tabOrder": 13,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Wedding RSVP \u2014 Sydney"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 15: `p05-au-adversarial-r1__r01`

- Prompt ID: `p05-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 78710,
  "failure_class": "none",
  "input_tokens": 9715,
  "output_tokens": 7319,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2156,
    "width": 960
  },
  "formId": "wedding-rsvp-aus",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "e.g. Olivia",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "e.g. Smith",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll use this for booking and event updates.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or best contact number for event updates.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Suburb, state and postcode are helpful for place cards.",
            "label": "Address (optional)",
            "placeholder": "Street address",
            "tabOrder": 5,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes \u2014 I will attend",
                "value": "yes"
              },
              {
                "label": "No \u2014 sadly cannot attend",
                "value": "no"
              }
            ],
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Select Yes if you will bring a guest.",
            "label": "Will you bring a plus-one?",
            "options": [
              {
                "label": "Yes",
                "value": "yes"
              },
              {
                "label": "No",
                "value": "no"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 110,
            "label": "Plus-one full name",
            "placeholder": "Full name of your guest",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-9",
          "position": {
            "x": 424,
            "y": 714
          },
          "props": {
            "height": 110,
            "helpText": "Optional contact number for your guest.",
            "label": "Plus-one phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 110,
            "label": "Meal choice",
            "options": [
              {
                "label": "Chicken (main)",
                "value": "chicken"
              },
              {
                "label": "Beef (main)",
                "value": "beef"
              },
              {
                "label": "Vegetarian (main)",
                "value": "vegetarian"
              },
              {
                "label": "Vegan (main)",
                "value": "vegan"
              },
              {
                "label": "Kids meal",
                "value": "kids"
              }
            ],
            "placeholder": "Select your meal",
            "tabOrder": 10,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-11",
          "position": {
            "x": 424,
            "y": 848
          },
          "props": {
            "height": 110,
            "label": "Plus-one meal choice",
            "options": [
              {
                "label": "Chicken (main)",
                "value": "chicken"
              },
              {
                "label": "Beef (main)",
                "value": "beef"
              },
              {
                "label": "Vegetarian (main)",
                "value": "vegetarian"
              },
              {
                "label": "Vegan (main)",
                "value": "vegan"
              },
              {
                "label": "Kids meal",
                "value": "kids"
              }
            ],
            "placeholder": "Select guest's meal (if bringing one)",
            "tabOrder": 11,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 982
          },
          "props": {
            "height": 200,
            "helpText": "Include any allergens or medical dietary needs.",
            "label": "Dietary requirements",
            "placeholder": "Please list allergies, intolerances or dietary needs",
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1286
          },
          "props": {
            "height": 110,
            "helpText": "We may add this to the reception playlist.",
            "label": "Song request",
            "placeholder": "Song title and artist",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-14",
          "position": {
            "x": 40,
            "y": 1420
          },
          "props": {
            "height": 200,
            "helpText": "Optional message or congratulations.",
            "label": "Message to the couple",
            "placeholder": "Share a note for the couple",
            "tabOrder": 14,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-15",
          "position": {
            "x": 40,
            "y": 1724
          },
          "props": {
            "height": 120,
            "helpText": "We'll only use your details for event updates and RSVP follow-up.",
            "label": "Yes \u2014 I'd like to receive wedding updates by email",
            "options": [
              {
                "label": "Yes \u2014 I'd like to receive wedding updates by email",
                "value": "email_updates"
              }
            ],
            "tabOrder": 15,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-16",
          "position": {
            "x": 40,
            "y": 1868
          },
          "props": {
            "height": 120,
            "helpText": "By submitting this RSVP you accept the event terms and consent to the use of your details for event arrangements.",
            "label": "I agree to the event terms and privacy policy",
            "tabOrder": 16,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-17",
          "position": {
            "x": 40,
            "y": 2012
          },
          "props": {
            "height": 72,
            "label": "Send RSVP",
            "tabOrder": 17,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Wedding RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 16: `p06-au-neutral-r1__r01`

- Prompt ID: `p06-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 46281,
  "failure_class": "none",
  "input_tokens": 3799,
  "output_tokens": 4446,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2012,
    "width": 960
  },
  "formId": "volunteer-signup-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll use this for event updates and confirmations.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Best number for urgent contact on event day.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode.",
            "label": "Residential address",
            "tabOrder": 5,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "checkbox-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Tick all days you can volunteer",
            "label": "Available days",
            "options": [
              {
                "label": "Monday",
                "value": "monday"
              },
              {
                "label": "Tuesday",
                "value": "tuesday"
              },
              {
                "label": "Wednesday",
                "value": "wednesday"
              },
              {
                "label": "Thursday",
                "value": "thursday"
              },
              {
                "label": "Friday",
                "value": "friday"
              },
              {
                "label": "Saturday",
                "value": "saturday"
              },
              {
                "label": "Sunday",
                "value": "sunday"
              }
            ],
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "If you can do any shift, choose 'Any time'.",
            "label": "Preferred shift",
            "options": [
              {
                "label": "Morning (e.g. 8am\u201312pm)",
                "value": "morning"
              },
              {
                "label": "Afternoon (e.g. 12pm\u20134pm)",
                "value": "afternoon"
              },
              {
                "label": "Evening (e.g. 4pm\u20138pm)",
                "value": "evening"
              },
              {
                "label": "Any time",
                "value": "any"
              }
            ],
            "placeholder": "Choose a shift",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "date-8",
          "position": {
            "x": 424,
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "If you have a start date, tell us here.",
            "label": "Available from",
            "placeholder": "First available date",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 200,
            "helpText": "Include regular weekly availability or any blackout dates.",
            "label": "Availability notes",
            "placeholder": "eg. I am available most weekends, unavailable during school holidays, etc.",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 120,
            "helpText": "Select any skills you can bring to the event (tick all that apply).",
            "label": "Skills and experience",
            "options": [
              {
                "label": "First aid / CPR",
                "value": "first_aid"
              },
              {
                "label": "Event setup / pack down",
                "value": "setup"
              },
              {
                "label": "Hospitality / front desk",
                "value": "hospitality"
              },
              {
                "label": "Crowd management / stewarding",
                "value": "stewarding"
              },
              {
                "label": "Photography / videography",
                "value": "photography"
              },
              {
                "label": "Administration / data entry",
                "value": "administration"
              },
              {
                "label": "Driving (light vehicles)",
                "value": "driving"
              },
              {
                "label": "Other (please specify below)",
                "value": "other"
              }
            ],
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 1152
          },
          "props": {
            "height": 200,
            "helpText": "Include relevant certificates or licences (e.g. RSA, Working with Children).",
            "label": "Other skills or qualifications",
            "placeholder": "Tell us about other skills, licences, or certifications",
            "tabOrder": 11,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "first-name-12",
          "position": {
            "x": 40,
            "y": 1456
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 First name",
            "placeholder": "Given name",
            "tabOrder": 12,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-13",
          "position": {
            "x": 424,
            "y": 1456
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Last name",
            "placeholder": "Family name",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "phone-14",
          "position": {
            "x": 40,
            "y": 1590
          },
          "props": {
            "height": 110,
            "helpText": "Primary contact if there's an incident.",
            "label": "Emergency contact \u2014 Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 14,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "text-15",
          "position": {
            "x": 424,
            "y": 1590
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Relationship",
            "placeholder": "e.g. Partner, Parent, Friend",
            "tabOrder": 15,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "terms-16",
          "position": {
            "x": 40,
            "y": 1724
          },
          "props": {
            "height": 120,
            "helpText": "By ticking this box you confirm you accept the code of conduct and our use of your contact details for event purposes.",
            "label": "I agree to follow the volunteer code of conduct and understand organisers may remove volunteers who breach it. I consent to my details being used for event coordination and emergency contact.",
            "tabOrder": 16,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-17",
          "position": {
            "x": 40,
            "y": 1868
          },
          "props": {
            "height": 72,
            "label": "Submit application",
            "tabOrder": 17,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Volunteer sign-up form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 17: `p06-au-ambiguous-r1__r01`

- Prompt ID: `p06-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 61966,
  "failure_class": "none",
  "input_tokens": 3871,
  "output_tokens": 5773,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2228,
    "width": 960
  },
  "formId": "sydney-volunteer-signup",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "We\u2019ll only use your details to arrange shifts and for safety. Required fields are marked.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or landline we can contact in Australia",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Street address, suburb, state and postcode",
            "label": "Address",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select all times you can volunteer",
            "label": "Availability",
            "options": [
              {
                "label": "Weekday mornings (6am\u201312pm)",
                "value": "weekday_morning"
              },
              {
                "label": "Weekday afternoons (12pm\u20136pm)",
                "value": "weekday_afternoon"
              },
              {
                "label": "Weekday evenings (6pm\u201310pm)",
                "value": "weekday_evening"
              },
              {
                "label": "Weekend mornings (6am\u201312pm)",
                "value": "weekend_morning"
              },
              {
                "label": "Weekend afternoons (12pm\u20136pm)",
                "value": "weekend_afternoon"
              },
              {
                "label": "Weekend evenings (6pm\u201310pm)",
                "value": "weekend_evening"
              },
              {
                "label": "Specific dates (see notes below)",
                "value": "specific_dates"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 list exact dates or timing conflicts",
            "label": "Specific dates or availability notes",
            "placeholder": "e.g. 12\u201315 March mornings, or list exact dates",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "Select any skills you can bring to the role",
            "label": "Skills & experience",
            "options": [
              {
                "label": "Customer service",
                "value": "customer_service"
              },
              {
                "label": "First aid",
                "value": "first_aid"
              },
              {
                "label": "Crowd control",
                "value": "crowd_control"
              },
              {
                "label": "Ticketing",
                "value": "ticketing"
              },
              {
                "label": "Logistics & setup",
                "value": "logistics"
              },
              {
                "label": "Photography",
                "value": "photography"
              },
              {
                "label": "IT / technical support",
                "value": "it_support"
              },
              {
                "label": "Child-safe (WWCC)",
                "value": "child_safe"
              },
              {
                "label": "Other (describe below)",
                "value": "other"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 1090
          },
          "props": {
            "height": 110,
            "label": "Other skills (brief)",
            "placeholder": "If 'Other', describe briefly",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "text-11",
          "position": {
            "x": 40,
            "y": 1224
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "placeholder": "Full name",
            "tabOrder": 11,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-12",
          "position": {
            "x": 424,
            "y": 1224
          },
          "props": {
            "height": 110,
            "label": "Emergency contact phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 12,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "placeholder": "e.g. partner, parent, friend",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-14",
          "position": {
            "x": 40,
            "y": 1492
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 we only use this to make reasonable adjustments",
            "label": "Medical or accessibility needs",
            "placeholder": "Share anything we should know to support you (optional)",
            "tabOrder": 14,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-15",
          "position": {
            "x": 40,
            "y": 1796
          },
          "props": {
            "height": 120,
            "helpText": "I agree to follow the event code of conduct and the event terms.",
            "label": "Code of conduct & event terms",
            "tabOrder": 15,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "checkbox-16",
          "position": {
            "x": 40,
            "y": 1940
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive occasional updates about this event and future volunteering roles (optional).",
            "label": "Event updates & volunteering opportunities",
            "options": [
              {
                "label": "Yes \u2014 send me updates",
                "value": "updates_opt_in"
              }
            ],
            "tabOrder": 16,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "submit-button-17",
          "position": {
            "x": 40,
            "y": 2084
          },
          "props": {
            "height": 72,
            "label": "Submit signup",
            "tabOrder": 17,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Volunteer signup"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 18: `p06-au-adversarial-r1__r01`

- Prompt ID: `p06-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 19,
  "duration_ms": 53592,
  "failure_class": "none",
  "input_tokens": 3881,
  "output_tokens": 5024,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2506,
    "width": 960
  },
  "formId": "volunteer-signup-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "We\u2019ll use your contact details to schedule shifts and send important updates. Thanks for volunteering.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send shift confirmations here.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country and area code so we can contact you quickly.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode if available.",
            "label": "Address",
            "placeholder": "Street address, suburb, state",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter your local postcode.",
            "label": "Postcode",
            "placeholder": "Postcode",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Tick any days you can volunteer.",
            "label": "Availability \u2014 days of week",
            "options": [
              {
                "label": "Monday",
                "value": "monday"
              },
              {
                "label": "Tuesday",
                "value": "tuesday"
              },
              {
                "label": "Wednesday",
                "value": "wednesday"
              },
              {
                "label": "Thursday",
                "value": "thursday"
              },
              {
                "label": "Friday",
                "value": "friday"
              },
              {
                "label": "Saturday",
                "value": "saturday"
              },
              {
                "label": "Sunday",
                "value": "sunday"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Select any shifts you prefer.",
            "label": "Preferred shifts",
            "options": [
              {
                "label": "Morning",
                "value": "morning"
              },
              {
                "label": "Afternoon",
                "value": "afternoon"
              },
              {
                "label": "Evening",
                "value": "evening"
              },
              {
                "label": "Overnight",
                "value": "overnight"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "date-10",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 110,
            "helpText": "If you\u2019re available from a specific date, tell us here.",
            "label": "Available from",
            "placeholder": "Select a date",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 1054
          },
          "props": {
            "height": 120,
            "helpText": "Tick all that apply.",
            "label": "Skills & experience",
            "options": [
              {
                "label": "First aid / CPR",
                "value": "first_aid"
              },
              {
                "label": "Event setup & packdown",
                "value": "setup"
              },
              {
                "label": "Crowd management / stewarding",
                "value": "crowd"
              },
              {
                "label": "Registration / check-in",
                "value": "registration"
              },
              {
                "label": "Food & beverage service",
                "value": "food_bev"
              },
              {
                "label": "Logistics / driving",
                "value": "logistics"
              },
              {
                "label": "Social media / photography",
                "value": "media"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 11,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 200,
            "label": "Other skills or licences",
            "placeholder": "Tell us about other skills, licences or certifications (e.g. driver licence, RSA).",
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1502
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "placeholder": "Full name",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-14",
          "position": {
            "x": 424,
            "y": 1502
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "placeholder": "e.g. Partner, Parent, Friend",
            "tabOrder": 14,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "phone-15",
          "position": {
            "x": 40,
            "y": 1636
          },
          "props": {
            "height": 110,
            "helpText": "Include country and area code.",
            "label": "Emergency contact phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 15,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "textarea-16",
          "position": {
            "x": 40,
            "y": 1770
          },
          "props": {
            "height": 200,
            "label": "Anything else we should know?",
            "placeholder": "Allergies, accessibility needs, or scheduling notes",
            "tabOrder": 16,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-17",
          "position": {
            "x": 40,
            "y": 2074
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you\u2019d like to receive news about future events and volunteering opportunities.",
            "label": "Updates & opportunities",
            "options": [
              {
                "label": "Yes \u2014 email me about future events and volunteer opportunities",
                "value": "opt_in_email"
              }
            ],
            "tabOrder": 17,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-18",
          "position": {
            "x": 40,
            "y": 2218
          },
          "props": {
            "height": 120,
            "label": "I agree to the code of conduct and event terms",
            "tabOrder": 18,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-19",
          "position": {
            "x": 40,
            "y": 2362
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
            "tabOrder": 19,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Volunteer sign-up"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 19: `p07-au-neutral-r1__r01`

- Prompt ID: `p07-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "membership-application",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 42522,
  "failure_class": "none",
  "input_tokens": 3799,
  "output_tokens": 3993,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1568,
    "width": 960
  },
  "formId": "membership-application-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please provide your details below. We will review your application and contact you with next steps.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will use this to contact you about your application.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or landline \u2014 include area code if needed.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode.",
            "label": "Address",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select the membership category you are applying for.",
            "label": "Membership type",
            "options": [
              {
                "label": "Individual",
                "value": "individual"
              },
              {
                "label": "Family",
                "value": "family"
              },
              {
                "label": "Concession / Student",
                "value": "concession"
              },
              {
                "label": "Corporate",
                "value": "corporate"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "label": "I confirm I meet the membership eligibility criteria",
            "options": [
              {
                "label": "I confirm I meet the membership eligibility criteria",
                "value": "eligible_confirm"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 120,
            "label": "I agree to abide by the association's code of conduct",
            "options": [
              {
                "label": "I agree to abide by the association's code of conduct",
                "value": "agree_conduct"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 930
          },
          "props": {
            "height": 120,
            "label": "I declare I have not been suspended or expelled from another member organisation",
            "options": [
              {
                "label": "I declare I have not been suspended or expelled from another member organisation",
                "value": "no_suspension"
              }
            ],
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "dropdown-11",
          "position": {
            "x": 40,
            "y": 1074
          },
          "props": {
            "height": 110,
            "label": "How did you hear about us?",
            "options": [
              {
                "label": "Friend or colleague",
                "value": "friend"
              },
              {
                "label": "Social media",
                "value": "social"
              },
              {
                "label": "Our website",
                "value": "website"
              },
              {
                "label": "Event or conference",
                "value": "event"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 11,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-12",
          "position": {
            "x": 424,
            "y": 1074
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "placeholder": "Please specify",
            "tabOrder": 12,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "paragraph-13",
          "position": {
            "x": 40,
            "y": 1208
          },
          "props": {
            "height": 48,
            "label": "Privacy: we will handle your personal information in accordance with our privacy policy. We may contact you about your application and membership.",
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1280
          },
          "props": {
            "height": 120,
            "helpText": "You can withdraw consent at any time in line with our privacy policy.",
            "label": "By applying I accept the membership terms and privacy policy and consent to receive membership communications.",
            "tabOrder": 14,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-15",
          "position": {
            "x": 40,
            "y": 1424
          },
          "props": {
            "height": 72,
            "label": "Apply for Membership",
            "tabOrder": 15,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Membership Application"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 20: `p07-au-ambiguous-r1__r01`

- Prompt ID: `p07-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "membership-application",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 49176,
  "failure_class": "none",
  "input_tokens": 3871,
  "output_tokens": 4256,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1852,
    "width": 960
  },
  "formId": "sydney-membership-application",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Provide an Australian mobile number we can contact",
            "label": "Mobile phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "date-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Used to confirm eligibility",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Choose the membership that applies",
            "label": "Membership type",
            "options": [
              {
                "label": "Individual",
                "value": "individual"
              },
              {
                "label": "Family",
                "value": "family"
              },
              {
                "label": "Concession (student / pensioner)",
                "value": "concession"
              },
              {
                "label": "Corporate",
                "value": "corporate"
              },
              {
                "label": "Life member",
                "value": "life"
              }
            ],
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "address-7",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 110,
            "helpText": "Include street, suburb, state and postcode",
            "label": "Residential address",
            "tabOrder": 7,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 694
          },
          "props": {
            "height": 120,
            "label": "I confirm I am 18 years of age or older",
            "options": [
              {
                "label": "Yes, I confirm",
                "value": "age_confirm"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 838
          },
          "props": {
            "height": 120,
            "label": "I confirm I meet the eligibility criteria for the membership type selected",
            "options": [
              {
                "label": "Yes, I confirm",
                "value": "eligibility_confirm"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 982
          },
          "props": {
            "height": 120,
            "label": "I agree to comply with the organisation's code of conduct",
            "options": [
              {
                "label": "Yes, I agree",
                "value": "conduct_agree"
              }
            ],
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "dropdown-11",
          "position": {
            "x": 40,
            "y": 1126
          },
          "props": {
            "height": 110,
            "label": "How did you hear about us?",
            "options": [
              {
                "label": "Friend or family",
                "value": "friend_family"
              },
              {
                "label": "Social media",
                "value": "social_media"
              },
              {
                "label": "Online search",
                "value": "online_search"
              },
              {
                "label": "Event or expo",
                "value": "event_expo"
              },
              {
                "label": "Referral from a member",
                "value": "member_referral"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 11,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-12",
          "position": {
            "x": 424,
            "y": 1126
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "placeholder": "Where did you hear about us?",
            "tabOrder": 12,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 1260
          },
          "props": {
            "height": 200,
            "label": "Additional information (optional)",
            "placeholder": "Tell us anything else we should know",
            "tabOrder": 13,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1564
          },
          "props": {
            "height": 120,
            "helpText": "By applying you agree to the event terms and membership conditions (see event terms).",
            "label": "Terms and membership conditions",
            "tabOrder": 14,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-15",
          "position": {
            "x": 40,
            "y": 1708
          },
          "props": {
            "height": 72,
            "label": "Apply for membership",
            "tabOrder": 15,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Membership Application"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 21: `p07-au-adversarial-r1__r01`

- Prompt ID: `p07-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "membership-application",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 86320,
  "failure_class": "none",
  "input_tokens": 9335,
  "output_tokens": 7326,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1414,
    "width": 960
  },
  "formId": "membership-application-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 600,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll use this for membership updates",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 600,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Australian phone number, including area code",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include street, suburb, state and postcode",
            "label": "Address",
            "tabOrder": 5,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "address"
        },
        {
          "id": "text-6",
          "position": {
            "x": 600,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Postcode",
            "placeholder": "e.g. 3000",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Membership type",
            "options": [
              {
                "label": "Individual",
                "value": "individual"
              },
              {
                "label": "Family",
                "value": "family"
              },
              {
                "label": "Student",
                "value": "student"
              },
              {
                "label": "Concession",
                "value": "concession"
              },
              {
                "label": "Corporate",
                "value": "corporate"
              }
            ],
            "placeholder": "Select membership type",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 110,
            "label": "How did you hear about us?",
            "options": [
              {
                "label": "Friend or colleague",
                "value": "friend"
              },
              {
                "label": "Social media",
                "value": "social_media"
              },
              {
                "label": "Web search",
                "value": "web_search"
              },
              {
                "label": "Event or promotion",
                "value": "event"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select source",
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "dropdown"
        },
        {
          "id": "text-9",
          "position": {
            "x": 600,
            "y": 560
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 694
          },
          "props": {
            "height": 120,
            "label": "I confirm I meet the eligibility criteria for this membership",
            "options": [
              {
                "label": "Yes, I confirm I meet the eligibility criteria",
                "value": "confirm_eligibility"
              }
            ],
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 838
          },
          "props": {
            "height": 120,
            "label": "I agree to abide by the organisation\u2019s code of conduct",
            "options": [
              {
                "label": "I agree to abide by the code of conduct",
                "value": "agree_code_of_conduct"
              }
            ],
            "tabOrder": 11,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 982
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to marketing and event communication",
            "label": "I'd like to receive news and event updates",
            "options": [
              {
                "label": "Yes, sign me up for news and event updates",
                "value": "opt_in_marketing"
              }
            ],
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1126
          },
          "props": {
            "height": 120,
            "helpText": "Please read and accept our event terms",
            "label": "Terms and conditions",
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-14",
          "position": {
            "x": 40,
            "y": 1270
          },
          "props": {
            "height": 72,
            "label": "Apply for membership",
            "tabOrder": 14,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Membership application"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 22: `p08-au-neutral-r1__r01`

- Prompt ID: `p08-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 40970,
  "failure_class": "none",
  "input_tokens": 3805,
  "output_tokens": 3476,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "trade-show-booth-visit-log",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Best email for follow-up",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Include country code if outside Australia",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Company or organisation",
            "label": "Company / organisation",
            "placeholder": "Organisation name",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Interest area",
            "options": [
              {
                "label": "Product demo",
                "value": "product_demo"
              },
              {
                "label": "Pricing & purchase",
                "value": "pricing_purchase"
              },
              {
                "label": "Technical integration",
                "value": "technical_integration"
              },
              {
                "label": "Partnership / reseller",
                "value": "partnership"
              },
              {
                "label": "Careers / recruitment",
                "value": "careers"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select primary interest",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate (0\u201330 days)",
                "value": "0_30_days"
              },
              {
                "label": "1\u20133 months",
                "value": "1_3_months"
              },
              {
                "label": "3\u20136 months",
                "value": "3_6_months"
              },
              {
                "label": "6\u201312 months",
                "value": "6_12_months"
              },
              {
                "label": "Not currently buying / just browsing",
                "value": "browsing"
              }
            ],
            "placeholder": "Select timeframe",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 200,
            "helpText": "Record any actions or important details for follow-up",
            "label": "Notes from visit",
            "placeholder": "Key points, pain points, requested follow-up, next steps",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 864
          },
          "props": {
            "height": 120,
            "helpText": "We will handle your information in line with our privacy policy.",
            "label": "I consent to be contacted about this enquiry, event updates and occasional marketing.",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 72,
            "label": "Save lead",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Trade Show Booth Visit Log"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 23: `p08-au-ambiguous-r1__r01`

- Prompt ID: `p08-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 56397,
  "failure_class": "none",
  "input_tokens": 3877,
  "output_tokens": 4819,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sydney-booth-lead-log",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Use business or preferred contact email.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Australian number preferred. Optional if email provided.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Company",
            "placeholder": "Organisation name",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "What the lead expressed interest in at the booth.",
            "label": "Interest area",
            "options": [
              {
                "label": "Product demo",
                "value": "product_demo"
              },
              {
                "label": "Pricing & budget",
                "value": "pricing_budget"
              },
              {
                "label": "Technical details",
                "value": "technical"
              },
              {
                "label": "Partnership / reseller",
                "value": "partnership"
              },
              {
                "label": "Training / services",
                "value": "services"
              },
              {
                "label": "General inquiry",
                "value": "general"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select interest",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Use the option that best matches the lead's expected purchase window.",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate (ready to buy)",
                "value": "immediate"
              },
              {
                "label": "1\u20133 months",
                "value": "1-3m"
              },
              {
                "label": "3\u20136 months",
                "value": "3-6m"
              },
              {
                "label": "6\u201312 months",
                "value": "6-12m"
              },
              {
                "label": "Researching / No fixed timeframe",
                "value": "researching"
              }
            ],
            "placeholder": "When do they plan to buy?",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 200,
            "helpText": "Include qualifying details, decision makers, budget notes and agreed next action.",
            "label": "Notes / Lead details",
            "placeholder": "Key points from conversation, qualifying info, next steps",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 864
          },
          "props": {
            "height": 120,
            "helpText": "We will use the details you provide to follow up. See the event terms for full privacy details.",
            "label": "I agree to be contacted about this enquiry and receive event-related follow-up from the exhibitor.",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 72,
            "label": "Save lead",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Trade show booth lead log \u2014 Sydney"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 24: `p08-au-adversarial-r1__r01`

- Prompt ID: `p08-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 49305,
  "failure_class": "none",
  "input_tokens": 3887,
  "output_tokens": 4173,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "trade-show-booth-lead-log-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "label": "Company",
            "placeholder": "Organisation name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Australian postcode (4 digits)",
            "label": "Postcode",
            "placeholder": "e.g. 3000",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include country code +61 for Australian numbers",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "email-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Interest area",
            "options": [
              {
                "label": "Product demos",
                "value": "product_demos"
              },
              {
                "label": "Pricing & packages",
                "value": "pricing"
              },
              {
                "label": "Technical integration",
                "value": "integration"
              },
              {
                "label": "Partnerships",
                "value": "partnerships"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select primary interest",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediately (0\u20133 months)",
                "value": "0_3"
              },
              {
                "label": "3\u20136 months",
                "value": "3_6"
              },
              {
                "label": "6\u201312 months",
                "value": "6_12"
              },
              {
                "label": "12+ months",
                "value": "12_plus"
              },
              {
                "label": "Not sure",
                "value": "unsure"
              }
            ],
            "placeholder": "Select timeframe",
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 200,
            "helpText": "Visible to the sales team",
            "label": "Notes",
            "placeholder": "Key conversation points, product interest, next steps",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 864
          },
          "props": {
            "height": 120,
            "helpText": "I agree to be contacted about this enquiry and receive event updates.",
            "label": "Consent to follow up",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-11",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 72,
            "label": "Log lead",
            "tabOrder": 11,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Trade show booth lead log"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 25: `p09-au-neutral-r1__r01`

- Prompt ID: `p09-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 6,
  "duration_ms": 32764,
  "failure_class": "none",
  "input_tokens": 3797,
  "output_tokens": 2718,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "newsletter-subscription-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "helpText": "Helps us personalise emails.",
            "label": "First name",
            "placeholder": "Optional",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 260
          },
          "type": "first-name"
        },
        {
          "id": "email-2",
          "position": {
            "x": 324,
            "y": 24
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll only use this to send the newsletter and event updates.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 2,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "checkbox-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 120,
            "helpText": "Select topics you\u2019d like to receive.",
            "label": "Content interests",
            "options": [
              {
                "label": "Product updates",
                "value": "product-updates"
              },
              {
                "label": "Events & webinars",
                "value": "events-webinars"
              },
              {
                "label": "Research & insights",
                "value": "research-insights"
              },
              {
                "label": "Offers & promotions",
                "value": "offers-promotions"
              },
              {
                "label": "Community stories",
                "value": "community-stories"
              }
            ],
            "tabOrder": 3,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "radio-4",
          "position": {
            "x": 40,
            "y": 302
          },
          "props": {
            "height": 120,
            "helpText": "Choose how often you\u2019d like to hear from us.",
            "label": "Newsletter frequency",
            "options": [
              {
                "label": "Weekly",
                "value": "weekly"
              },
              {
                "label": "Fortnightly",
                "value": "fortnightly"
              },
              {
                "label": "Monthly",
                "value": "monthly"
              }
            ],
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "terms-5",
          "position": {
            "x": 40,
            "y": 446
          },
          "props": {
            "height": 120,
            "helpText": "We will handle your personal information in accordance with our privacy policy.",
            "label": "I consent to receive marketing emails, event updates and offers. I understand I can unsubscribe at any time.",
            "tabOrder": 5,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-6",
          "position": {
            "x": 40,
            "y": 590
          },
          "props": {
            "height": 72,
            "label": "Subscribe",
            "tabOrder": 6,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Subscribe to our newsletter"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 26: `p09-au-ambiguous-r1__r01`

- Prompt ID: `p09-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 56406,
  "failure_class": "none",
  "input_tokens": 3869,
  "output_tokens": 4809,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sydney-event-newsletter",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Sign up to receive news and updates about our upcoming Sydney event.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 260
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 324,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name (optional)",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We'll send the newsletter to this address.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "label": "How often would you like to hear from us?",
            "options": [
              {
                "label": "Weekly",
                "value": "weekly"
              },
              {
                "label": "Fortnightly",
                "value": "fortnightly"
              },
              {
                "label": "Monthly",
                "value": "monthly"
              },
              {
                "label": "Only for major updates",
                "value": "major_updates"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "checkbox-6",
          "position": {
            "x": 40,
            "y": 508
          },
          "props": {
            "height": 120,
            "helpText": "Select all the topics you want to receive.",
            "label": "Content interests",
            "options": [
              {
                "label": "Speakers & sessions",
                "value": "speakers_sessions"
              },
              {
                "label": "Schedule & venue updates",
                "value": "schedule_updates"
              },
              {
                "label": "Networking opportunities",
                "value": "networking"
              },
              {
                "label": "Sponsorships & special offers",
                "value": "sponsors_offers"
              },
              {
                "label": "Volunteer & participation info",
                "value": "volunteer"
              },
              {
                "label": "Photography & media",
                "value": "media"
              }
            ],
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-7",
          "position": {
            "x": 40,
            "y": 652
          },
          "props": {
            "height": 120,
            "helpText": "You can unsubscribe at any time.",
            "label": "I agree to receive marketing and event updates by email and accept the event terms.",
            "tabOrder": 7,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-8",
          "position": {
            "x": 40,
            "y": 796
          },
          "props": {
            "height": 72,
            "label": "Subscribe",
            "tabOrder": 8,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Event Newsletter"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 27: `p09-au-adversarial-r1__r01`

- Prompt ID: `p09-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 87728,
  "failure_class": "none",
  "input_tokens": 8818,
  "output_tokens": 7326,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "newsletter-subscription-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll send newsletters here",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 for SMS updates",
            "label": "Mobile phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Australian postcode (4 digits)",
            "label": "Postcode",
            "placeholder": "2000",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "checkbox-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Choose the types of content you'd like to receive",
            "label": "Content interests",
            "options": [
              {
                "label": "Events",
                "value": "events"
              },
              {
                "label": "Articles & guides",
                "value": "articles"
              },
              {
                "label": "Promotions",
                "value": "promotions"
              },
              {
                "label": "Partner offers",
                "value": "partner_offers"
              },
              {
                "label": "Surveys & research",
                "value": "surveys"
              }
            ],
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "label": "How often would you like to hear from us?",
            "options": [
              {
                "label": "Weekly",
                "value": "weekly"
              },
              {
                "label": "Fortnightly",
                "value": "fortnightly"
              },
              {
                "label": "Monthly",
                "value": "monthly"
              },
              {
                "label": "Occasional (only major updates)",
                "value": "occasional"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 120,
            "helpText": "You can unsubscribe at any time.",
            "label": "I agree to receive marketing communications",
            "options": [
              {
                "label": "Yes, I agree to receive marketing communications",
                "value": "agree_marketing"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 858
          },
          "props": {
            "height": 120,
            "helpText": "Read the event terms.",
            "label": "I accept the event terms",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1002
          },
          "props": {
            "height": 72,
            "label": "Subscribe",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Subscribe to our newsletter"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 28: `p10-au-neutral-r1__r01`

- Prompt ID: `p10-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 44781,
  "failure_class": "none",
  "input_tokens": 3804,
  "output_tokens": 3725,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "charity-donation-pledge-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We will send your donation receipt to this address.",
            "label": "Email for receipt",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Provide a daytime number in Australian format if we need to contact you.",
            "label": "Phone (optional)",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Choose a suggested amount or select Other to enter a custom AUD amount.",
            "label": "Donation amount",
            "options": [
              {
                "label": "$25",
                "value": "25"
              },
              {
                "label": "$50",
                "value": "50"
              },
              {
                "label": "$100",
                "value": "100"
              },
              {
                "label": "Other amount (enter below)",
                "value": "other"
              }
            ],
            "placeholder": "Select an amount",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "number-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Enter a whole amount in Australian dollars if you selected Other.",
            "label": "Other amount (AUD)",
            "placeholder": "Enter whole AUD amount",
            "tabOrder": 6,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "number"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Choose whether this is a one-off pledge or a recurring gift.",
            "label": "Donation type",
            "options": [
              {
                "label": "One-off",
                "value": "one_off"
              },
              {
                "label": "Monthly",
                "value": "monthly"
              },
              {
                "label": "Quarterly",
                "value": "quarterly"
              },
              {
                "label": "Annually",
                "value": "annually"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Select Postal only if you would like a mailed receipt.",
            "label": "Receipt preference",
            "options": [
              {
                "label": "Email (preferred)",
                "value": "email"
              },
              {
                "label": "Postal",
                "value": "postal"
              }
            ],
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "address-9",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode for mailed receipts.",
            "label": "Postal address (only if you want a mailed receipt)",
            "tabOrder": 9,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 120,
            "helpText": "Optional: consenting helps us keep you informed about our work and impact.",
            "label": "Yes \u2014 send me campaign updates and occasional appeals by email. I understand I can unsubscribe at any time.",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "terms-11",
          "position": {
            "x": 40,
            "y": 992
          },
          "props": {
            "height": 120,
            "helpText": "Required to process your pledge and issue a receipt.",
            "label": "I agree to the charity processing my donation and understand the privacy handling of my personal information for donation and receipt purposes.",
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "paragraph-12",
          "position": {
            "x": 40,
            "y": 1136
          },
          "props": {
            "height": 48,
            "helpText": "We handle donor information in accordance with applicable Australian privacy practices. Contact us if you have questions about personal data or receipts.",
            "label": "Privacy",
            "tabOrder": 12,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1208
          },
          "props": {
            "height": 72,
            "label": "Pledge donation",
            "tabOrder": 13,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Charity Donation Pledge"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 29: `p10-au-ambiguous-r1__r01`

- Prompt ID: `p10-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 57873,
  "failure_class": "none",
  "input_tokens": 3876,
  "output_tokens": 4815,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sydney-charity-donation-pledge",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll send your donation receipt here.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 useful for urgent queries about your donation.",
            "label": "Mobile or phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "helpText": "Choose a preset amount or enter a custom amount.",
            "label": "Donation amount (AUD)",
            "options": [
              {
                "label": "$25",
                "value": "25"
              },
              {
                "label": "$50",
                "value": "50"
              },
              {
                "label": "$100",
                "value": "100"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "number-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "If you selected \u2018Other\u2019, enter the amount here. Minimum $1.",
            "label": "Other amount (AUD)",
            "placeholder": "Enter amount in AUD",
            "tabOrder": 6,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "number"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 120,
            "helpText": "Select whether this is a one\u2011off pledge or recurring gift.",
            "label": "Donation type",
            "options": [
              {
                "label": "One\u2011off",
                "value": "one_off"
              },
              {
                "label": "Recurring",
                "value": "recurring"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 424,
            "y": 436
          },
          "props": {
            "height": 110,
            "helpText": "Only needed for recurring donations (monthly, quarterly or annually).",
            "label": "If recurring, frequency",
            "options": [
              {
                "label": "Monthly",
                "value": "monthly"
              },
              {
                "label": "Quarterly",
                "value": "quarterly"
              },
              {
                "label": "Annually",
                "value": "annually"
              }
            ],
            "placeholder": "Select frequency",
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 580
          },
          "props": {
            "height": 110,
            "helpText": "How the name should appear on your donation receipt.",
            "label": "Receipt name",
            "placeholder": "Name for receipt (organisation or individual)",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "radio-10",
          "position": {
            "x": 424,
            "y": 580
          },
          "props": {
            "height": 120,
            "helpText": "We will email receipts by default. Choose postal if you need a paper receipt.",
            "label": "Receipt method",
            "options": [
              {
                "label": "Email (default)",
                "value": "email"
              },
              {
                "label": "Postal mail",
                "value": "postal"
              }
            ],
            "tabOrder": 10,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "address-11",
          "position": {
            "x": 40,
            "y": 724
          },
          "props": {
            "height": 110,
            "helpText": "Provide suburb, state and postcode for postal receipts. Leave blank if you chose Email.",
            "label": "Postal address (only needed for postal receipts)",
            "tabOrder": 11,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 858
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to hear about this campaign and other appeals.",
            "label": "Campaign updates",
            "options": [
              {
                "label": "Email updates about this campaign",
                "value": "email_updates"
              },
              {
                "label": "SMS updates",
                "value": "sms_updates"
              },
              {
                "label": "Postal updates",
                "value": "postal_updates"
              }
            ],
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1002
          },
          "props": {
            "height": 120,
            "helpText": "Required to process your donation and send receipts.",
            "label": "Privacy, receipt & event terms",
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-14",
          "position": {
            "x": 40,
            "y": 1146
          },
          "props": {
            "height": 72,
            "label": "Pledge donation",
            "tabOrder": 14,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Charity Donation Pledge"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 30: `p10-au-adversarial-r1__r01`

- Prompt ID: `p10-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 46448,
  "failure_class": "none",
  "input_tokens": 3886,
  "output_tokens": 3826,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "charity-donation-pledge-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Thank you for supporting our cause. Please tell us how you'd like to pledge and how we should send your receipt.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 417,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will send your receipt here unless you request a postal receipt.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 417,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 helpful for urgent contact about your gift.",
            "label": "Phone (AU) \u2014 include country code +61",
            "placeholder": "+61 4xx xxx xxx",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "phone"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose an amount or enter a custom amount.",
            "label": "Pledge amount (AUD)",
            "options": [
              {
                "label": "$25",
                "value": "25"
              },
              {
                "label": "$50",
                "value": "50"
              },
              {
                "label": "$100",
                "value": "100"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "dropdown"
        },
        {
          "id": "number-7",
          "position": {
            "x": 417,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Custom amount (AUD)",
            "placeholder": "Enter amount in AUD",
            "tabOrder": 7,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "number"
        },
        {
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select one-off or recurring.",
            "label": "Donation type",
            "options": [
              {
                "label": "One-off",
                "value": "one_off"
              },
              {
                "label": "Monthly recurring",
                "value": "monthly"
              },
              {
                "label": "Annually recurring",
                "value": "annually"
              }
            ],
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "Choose how you'd like to receive your tax receipt.",
            "label": "Receipt preference",
            "options": [
              {
                "label": "Email receipt (default)",
                "value": "email"
              },
              {
                "label": "Postal receipt",
                "value": "postal"
              }
            ],
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "dropdown"
        },
        {
          "id": "address-10",
          "position": {
            "x": 417,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "Include street, suburb, state and postcode. Only needed if you chose Postal receipt.",
            "label": "Postal address for receipt",
            "tabOrder": 10,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "address"
        },
        {
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to receive updates and appeals. You can unsubscribe at any time.",
            "label": "Send me campaign updates",
            "options": [
              {
                "label": "Email updates",
                "value": "email_updates"
              },
              {
                "label": "SMS updates",
                "value": "sms_updates"
              }
            ],
            "tabOrder": 11,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-12",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and the charity's privacy policy. I consent to the collection and use of my personal information to process this donation and send receipts and updates.",
            "label": "Agreement",
            "tabOrder": 12,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1064
          },
          "props": {
            "height": 72,
            "label": "Pledge donation",
            "tabOrder": 13,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Charity Donation Pledge"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 31: `p11-au-neutral-r1__r01`

- Prompt ID: `p11-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p11-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  }
]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 54983,
  "failure_class": "none",
  "input_tokens": 3800,
  "output_tokens": 4477,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "intl-event-registration-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send registration details to this address",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Include country code if outside Australia",
            "label": "Phone number",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Your current country of residence",
            "label": "Country",
            "options": [
              {
                "label": "Australia",
                "value": "AU"
              },
              {
                "label": "United States",
                "value": "US"
              },
              {
                "label": "United Kingdom",
                "value": "GB"
              },
              {
                "label": "Canada",
                "value": "CA"
              },
              {
                "label": "New Zealand",
                "value": "NZ"
              },
              {
                "label": "India",
                "value": "IN"
              },
              {
                "label": "China",
                "value": "CN"
              },
              {
                "label": "Japan",
                "value": "JP"
              },
              {
                "label": "Germany",
                "value": "DE"
              },
              {
                "label": "France",
                "value": "FR"
              },
              {
                "label": "Other",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select country",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Choose the timezone where you\u2019ll join from",
            "label": "Timezone",
            "options": [
              {
                "label": "UTC\u221212:00",
                "value": "UTC-12"
              },
              {
                "label": "UTC\u221211:00",
                "value": "UTC-11"
              },
              {
                "label": "UTC\u221210:00 (HST)",
                "value": "UTC-10"
              },
              {
                "label": "UTC\u221208:00 (PST)",
                "value": "UTC-8"
              },
              {
                "label": "UTC\u221205:00 (EST)",
                "value": "UTC-5"
              },
              {
                "label": "UTC\u00b100:00 (GMT)",
                "value": "UTC+0"
              },
              {
                "label": "UTC+01:00",
                "value": "UTC+1"
              },
              {
                "label": "UTC+02:00",
                "value": "UTC+2"
              },
              {
                "label": "UTC+03:00",
                "value": "UTC+3"
              },
              {
                "label": "UTC+04:00",
                "value": "UTC+4"
              },
              {
                "label": "UTC+05:30",
                "value": "UTC+5:30"
              },
              {
                "label": "UTC+07:00",
                "value": "UTC+7"
              },
              {
                "label": "UTC+08:00 (AET)",
                "value": "UTC+8"
              },
              {
                "label": "UTC+09:00",
                "value": "UTC+9"
              },
              {
                "label": "UTC+10:00 (AEST)",
                "value": "UTC+10"
              },
              {
                "label": "UTC+11:00",
                "value": "UTC+11"
              },
              {
                "label": "UTC+12:00",
                "value": "UTC+12"
              },
              {
                "label": "UTC+13:00",
                "value": "UTC+13"
              },
              {
                "label": "UTC+14:00",
                "value": "UTC+14"
              }
            ],
            "placeholder": "Select timezone",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Select all sessions you plan to attend",
            "label": "Sessions of interest",
            "options": [
              {
                "label": "Opening keynote",
                "value": "keynote"
              },
              {
                "label": "Workshop A: Marketing",
                "value": "workshop_marketing"
              },
              {
                "label": "Workshop B: Product",
                "value": "workshop_product"
              },
              {
                "label": "Panel discussion",
                "value": "panel"
              },
              {
                "label": "Closing networking",
                "value": "networking"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Optional: receive news, offers and future event updates",
            "label": "Marketing and event updates",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and marketing",
                "value": "yes"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 120,
            "helpText": "Required to confirm registration",
            "label": "Terms & privacy",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 858
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "International Event Registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 32: `p11-au-ambiguous-r1__r01`

- Prompt ID: `p11-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p11-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p11-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  }
]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 53392,
  "failure_class": "none",
  "input_tokens": 3872,
  "output_tokens": 4333,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sydney-online-event-registration",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Join our international online event hosted from Sydney. Please provide your details below so we can send event access details and match you to sessions.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will send event access and updates to this address.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country code for international numbers. We'll use this only for urgent event updates.",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Where you are located for communications and local time references.",
            "label": "Country",
            "options": [
              {
                "label": "Australia",
                "value": "AU"
              },
              {
                "label": "United States",
                "value": "US"
              },
              {
                "label": "United Kingdom",
                "value": "GB"
              },
              {
                "label": "Canada",
                "value": "CA"
              },
              {
                "label": "India",
                "value": "IN"
              },
              {
                "label": "China",
                "value": "CN"
              },
              {
                "label": "New Zealand",
                "value": "NZ"
              },
              {
                "label": "Singapore",
                "value": "SG"
              },
              {
                "label": "Germany",
                "value": "DE"
              },
              {
                "label": "France",
                "value": "FR"
              },
              {
                "label": "Other",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select your country",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose the timezone you will join from. Defaulted to Sydney for event scheduling.",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT)",
                "value": "Australia/Sydney"
              },
              {
                "label": "UTC",
                "value": "UTC"
              },
              {
                "label": "America/New_York (ET)",
                "value": "America/New_York"
              },
              {
                "label": "Europe/London (GMT/BST)",
                "value": "Europe/London"
              },
              {
                "label": "Asia/Singapore (SGT)",
                "value": "Asia/Singapore"
              },
              {
                "label": "Asia/Kolkata (IST)",
                "value": "Asia/Kolkata"
              },
              {
                "label": "Pacific/Auckland (NZST/NZDT)",
                "value": "Pacific/Auckland"
              },
              {
                "label": "Other",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select your timezone",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select the sessions you plan to attend (select at least one).",
            "label": "Session interest",
            "options": [
              {
                "label": "Keynote \u2014 Opening",
                "value": "keynote"
              },
              {
                "label": "Workshop: Data & AI",
                "value": "workshop_data_ai"
              },
              {
                "label": "Workshop: Product & Design",
                "value": "workshop_product_design"
              },
              {
                "label": "Panel: Industry Trends",
                "value": "panel_industry_trends"
              },
              {
                "label": "Networking session",
                "value": "networking"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about access needs or other information the organiser should know.",
            "label": "Additional information",
            "placeholder": "Dietary needs, accessibility requirements, or other notes",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive event updates and occasional marketing from the organiser. You can unsubscribe at any time.",
            "label": "Event updates and marketing",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and offers",
                "value": "opt_in_marketing"
              }
            ],
            "tabOrder": 10,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-11",
          "position": {
            "x": 40,
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and the organiser's privacy policy.",
            "label": "Terms and privacy",
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-12",
          "position": {
            "x": 40,
            "y": 1234
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 12,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Online Event \u2014 Registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 33: `p11-au-adversarial-r1__r01`

- Prompt ID: `p11-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 58141,
  "failure_class": "none",
  "input_tokens": 3882,
  "output_tokens": 4668,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "intl-event-registration-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Include country code, e.g. +61 for Australia",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Country",
            "options": [
              {
                "label": "Australia",
                "value": "AU"
              },
              {
                "label": "United States",
                "value": "US"
              },
              {
                "label": "United Kingdom",
                "value": "GB"
              },
              {
                "label": "Canada",
                "value": "CA"
              },
              {
                "label": "India",
                "value": "IN"
              },
              {
                "label": "Other",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select country",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Australian postcode (4 digits)",
            "label": "Postcode",
            "placeholder": "e.g. 2000",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Choose the timezone where you'll attend from",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT) \u2014 UTC+10/11",
                "value": "Australia/Sydney"
              },
              {
                "label": "UTC\u221208:00 (Pacific Time)",
                "value": "UTC-08:00"
              },
              {
                "label": "UTC\u221205:00 (Eastern Time)",
                "value": "UTC-05:00"
              },
              {
                "label": "UTC\u00b100:00 (Greenwich Mean Time)",
                "value": "UTC+00:00"
              },
              {
                "label": "UTC+01:00 (Central European Time)",
                "value": "UTC+01:00"
              },
              {
                "label": "Other / not listed",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select your timezone",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 120,
            "helpText": "Select all sessions you may attend",
            "label": "Sessions you're interested in",
            "options": [
              {
                "label": "Keynote sessions",
                "value": "keynote"
              },
              {
                "label": "Workshops",
                "value": "workshops"
              },
              {
                "label": "Networking sessions",
                "value": "networking"
              },
              {
                "label": "Technical deep dives",
                "value": "technical"
              },
              {
                "label": "Career roundtables",
                "value": "career"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 120,
            "helpText": "By registering you accept the organiser's event terms and privacy policy.",
            "label": "I agree to the event terms and privacy policy",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "International Online Event Registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 34: `p12-au-neutral-r1__r01`

- Prompt ID: `p12-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 51037,
  "failure_class": "none",
  "input_tokens": 3802,
  "output_tokens": 4037,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1584,
    "width": 960
  },
  "formId": "au-event-registration",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Register to attend. Provide your contact details and consent to our privacy and data handling for event administration and updates.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will send event updates and your ticket here.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "For urgent event updates or on-day contact.",
            "label": "Mobile or phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode if relevant.",
            "label": "Address (optional)",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Ticket type",
            "options": [
              {
                "label": "General admission",
                "value": "general"
              },
              {
                "label": "Student (valid ID required)",
                "value": "student"
              },
              {
                "label": "VIP",
                "value": "vip"
              }
            ],
            "placeholder": "Select ticket type",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Tick any that apply",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "None",
                "value": "none"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Other (please specify below)",
                "value": "other"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "We use this to make appropriate arrangements.",
            "label": "Accessibility or other requirements",
            "placeholder": "Let us know any access needs or special requests",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "paragraph-10",
          "position": {
            "x": 40,
            "y": 1080
          },
          "props": {
            "height": 48,
            "label": "Privacy & data handling: We collect and handle personal information under the Australian Privacy Act for event administration, ticketing and important updates. Your details will be used by the event organiser for registrations, on-day communication and follow-up related to this event.",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "terms-11",
          "position": {
            "x": 40,
            "y": 1152
          },
          "props": {
            "height": 120,
            "helpText": "You must accept to complete registration.",
            "label": "I consent to the collection and use of my personal information under Australian privacy laws for the purposes described above, and acknowledge the organiser's stated data handling practices.",
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 1296
          },
          "props": {
            "height": 120,
            "helpText": "Optional \u2014 receive news and offers about this event and future events.",
            "label": "Marketing & event updates",
            "options": [
              {
                "label": "Yes \u2014 email me event updates and occasional offers",
                "value": "opt_in_email"
              }
            ],
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1440
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 13,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Event registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 35: `p12-au-ambiguous-r1__r01`

- Prompt ID: `p12-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 51335,
  "failure_class": "none",
  "input_tokens": 3874,
  "output_tokens": 4236,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "sydney-event-registration-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "helpText": "This form registers you for the Sydney event and captures contact and consent details for event administration.",
            "label": "Event location: Sydney",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will use this to send event updates and tickets.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Used for urgent event updates or safety messages.",
            "label": "Phone (mobile preferred)",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode for local mailings if needed.",
            "label": "Postal address",
            "placeholder": "Street address, suburb, state, postcode",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Attendance type",
            "options": [
              {
                "label": "In-person (Sydney)",
                "value": "in_person"
              },
              {
                "label": "Online / livestream",
                "value": "online"
              }
            ],
            "placeholder": "Select...",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "number-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "How many people are you registering now?",
            "label": "Number of attendees",
            "placeholder": "1",
            "tabOrder": 8,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "number"
        },
        {
          "id": "paragraph-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 48,
            "helpText": "We collect and use personal information to manage registration, communicate event updates, and for health & safety. Information is handled in line with Australian privacy law and our privacy policy.",
            "label": "Data handling notice",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 120,
            "helpText": "You must accept our privacy practices to register.",
            "label": "Privacy & data-handling acknowledgement",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "terms-11",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 120,
            "helpText": "I acknowledge that my personal information will be handled lawfully for event administration and safety.",
            "label": "Acknowledgement of lawful handling",
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 992
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive occasional news, offers and future event updates by email.",
            "label": "Marketing & updates",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive event updates and marketing",
                "value": "opt_in"
              }
            ],
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1136
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 13,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney event registration \u2014 privacy & consent"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 36: `p12-au-adversarial-r1__r01`

- Prompt ID: `p12-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 48193,
  "failure_class": "none",
  "input_tokens": 3884,
  "output_tokens": 3992,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "au-event-registration",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "helpText": "See the event terms for full details on data handling and retention.",
            "label": "We collect and use your personal information in line with the Australian Privacy Principles (APPs) to manage your registration, tickets and event updates. The organiser will retain and handle data only for event administration and legal obligations.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will send tickets and important updates to this address.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Used for urgent event updates.",
            "label": "Phone (include country code, e.g. +61)",
            "placeholder": "+61 4xx xxx xxx",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Please include suburb, state and postcode.",
            "label": "Postal address",
            "placeholder": "Street, suburb, state, postcode",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Acknowledgement required to process your registration.",
            "label": "Privacy & lawful basis",
            "options": [
              {
                "label": "I acknowledge that the organiser may collect and use my personal information for event administration and communications in accordance with the Australian Privacy Principles.",
                "value": "privacy_ack"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "Optional: get news about future events.",
            "label": "Marketing & updates",
            "options": [
              {
                "label": "I agree to receive event news and offers by email or SMS.",
                "value": "marketing_opt_in"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 120,
            "helpText": "By registering you accept the event terms and privacy practices.",
            "label": "Terms and privacy",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 930
          },
          "props": {
            "height": 72,
            "label": "Register",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Event registration"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 37: `p13-au-neutral-r1__r01`

- Prompt ID: `p13-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 44858,
  "failure_class": "none",
  "input_tokens": 3804,
  "output_tokens": 3749,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "onboarding-interest-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll use this for event updates.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Include country code if you\u2019re outside Australia (e.g. +61).",
            "label": "Mobile number",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Role you're interested in",
            "options": [
              {
                "label": "Attendee",
                "value": "attendee"
              },
              {
                "label": "Volunteer",
                "value": "volunteer"
              },
              {
                "label": "Presenter / Speaker",
                "value": "presenter"
              },
              {
                "label": "Sponsor",
                "value": "sponsor"
              },
              {
                "label": "Partner",
                "value": "partner"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a role",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 up to 500 characters.",
            "label": "Tell us about your experience or interest",
            "placeholder": "Briefly describe your background or why you\u2019re interested in this role",
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-7",
          "position": {
            "x": 40,
            "y": 730
          },
          "props": {
            "height": 120,
            "helpText": "View terms: https://example.test/terms",
            "label": "I agree to receive event updates and accept the event terms and privacy policy.",
            "tabOrder": 7,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-8",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 72,
            "label": "Register interest",
            "tabOrder": 8,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Onboarding Interest Form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 38: `p13-au-ambiguous-r1__r01`

- Prompt ID: `p13-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 39306,
  "failure_class": "none",
  "input_tokens": 3876,
  "output_tokens": 3233,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "onboarding-interest-sydney-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Tell us a little about yourself so our Sydney team can follow up.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll use this to confirm details and send updates.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or landline \u2014 include area code.",
            "label": "Phone (AU)",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose the role that best describes your interest.",
            "label": "Role / interest",
            "options": [
              {
                "label": "Attendee",
                "value": "attendee"
              },
              {
                "label": "Volunteer",
                "value": "volunteer"
              },
              {
                "label": "Speaker / Presenter",
                "value": "speaker"
              },
              {
                "label": "Partner / Sponsor",
                "value": "partner"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select your role or interest",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 share anything helpful for organisers.",
            "label": "Tell us more",
            "placeholder": "Any details we should know (availability, experience, questions)...",
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-8",
          "position": {
            "x": 40,
            "y": 802
          },
          "props": {
            "height": 120,
            "helpText": "By submitting you agree to the event terms (link) and our privacy practices.",
            "label": "I agree to the event terms and privacy policy",
            "tabOrder": 8,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-9",
          "position": {
            "x": 40,
            "y": 946
          },
          "props": {
            "height": 72,
            "label": "Register interest",
            "tabOrder": 9,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney onboarding interest"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 39: `p13-au-adversarial-r1__r01`

- Prompt ID: `p13-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 42285,
  "failure_class": "none",
  "input_tokens": 3886,
  "output_tokens": 3446,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "onboarding-interest-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "We\u2019ll contact you with next steps if there\u2019s a fit. Required fields are marked.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "e.g. Emma",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "e.g. Smith",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send onboarding updates here.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or landline we can call about onboarding.",
            "label": "Phone (Australia +61)",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Role you\u2019re interested in",
            "options": [
              {
                "label": "Volunteer",
                "value": "volunteer"
              },
              {
                "label": "Staff",
                "value": "staff"
              },
              {
                "label": "Speaker",
                "value": "speaker"
              },
              {
                "label": "Vendor",
                "value": "vendor"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a role",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "address-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb and postcode for local coverage.",
            "label": "Address",
            "placeholder": "Street address, suburb, state, postcode",
            "tabOrder": 7,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "terms-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "I accept the organiser\u2019s event terms and privacy policy.",
            "label": "I agree to the event terms",
            "tabOrder": 8,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 72,
            "label": "Submit interest",
            "tabOrder": 9,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Onboarding interest form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 40: `p14-au-neutral-r1__r01`

- Prompt ID: `p14-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 50198,
  "failure_class": "none",
  "input_tokens": 3801,
  "output_tokens": 4122,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1690,
    "width": 960
  },
  "formId": "au-event-waiver",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please complete this form to help us manage your safety at the event. Personal and health information is handled in line with Australian privacy practice.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 384,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "date-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Day / Month / Year",
            "label": "Date of birth",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Mobile phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "email-6",
          "position": {
            "x": 384,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Tick all that apply so we can plan for your safety",
            "label": "Health conditions (tick any that apply)",
            "options": [
              {
                "label": "Asthma",
                "value": "asthma"
              },
              {
                "label": "Diabetes",
                "value": "diabetes"
              },
              {
                "label": "Heart condition",
                "value": "heart_condition"
              },
              {
                "label": "Epilepsy",
                "value": "epilepsy"
              },
              {
                "label": "Pregnancy",
                "value": "pregnancy"
              },
              {
                "label": "None of the above",
                "value": "none"
              },
              {
                "label": "Other (see details below)",
                "value": "other"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 200,
            "label": "Medications, allergies or other important health details",
            "placeholder": "List current medications, allergies, mobility needs or any other health information organisers should know",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "Required for participation",
            "label": "Emergency medical treatment consent",
            "options": [
              {
                "label": "I consent to organisers seeking emergency medical treatment on my behalf if required",
                "value": "consent_emergency"
              }
            ],
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to proceed",
            "label": "I acknowledge I have read the event safety information, accept the risks involved, and release the organisers to the extent permitted by law. I consent to the collection and use of my personal and health information by the organisers for safety, care and event administration in line with Australian privacy practice.",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "divider-11",
          "position": {
            "x": 40,
            "y": 1234
          },
          "props": {
            "height": 20,
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "first-name-12",
          "position": {
            "x": 40,
            "y": 1278
          },
          "props": {
            "height": 110,
            "label": "Contact first name",
            "placeholder": "Given name",
            "tabOrder": 12,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "first-name"
        },
        {
          "id": "text-13",
          "position": {
            "x": 384,
            "y": 1278
          },
          "props": {
            "height": 110,
            "label": "Contact last name",
            "placeholder": "Family name",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-14",
          "position": {
            "x": 40,
            "y": 1412
          },
          "props": {
            "height": 110,
            "label": "Relationship to participant",
            "placeholder": "e.g. Partner, Parent, Friend",
            "tabOrder": 14,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "phone-15",
          "position": {
            "x": 384,
            "y": 1412
          },
          "props": {
            "height": 110,
            "label": "Contact phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 15,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 1546
          },
          "props": {
            "height": 72,
            "label": "Submit and acknowledge",
            "tabOrder": 16,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Participant waiver & health form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 41: `p14-au-ambiguous-r1__r01`

- Prompt ID: `p14-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 50219,
  "failure_class": "none",
  "input_tokens": 3873,
  "output_tokens": 4209,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1790,
    "width": 960
  },
  "formId": "sydney-event-waiver-au",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "helpText": "This event is held in Sydney. If you are attending from interstate or overseas, tell us in the health notes if you have recent travel-related health concerns.",
            "label": "Event location: Sydney",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "date-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Used to confirm eligibility and to assist medical responders if needed.",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "email-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "We will send event updates and confirmations here.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-6",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide a number we can use in an emergency or for event updates.",
            "label": "Mobile phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "textarea-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 200,
            "helpText": "Include any conditions, medications, allergies or other health details organisers should know. If helpful, include your GP contact details.",
            "label": "Relevant health information",
            "placeholder": "Allergies, current medications, mobility or assistance needs, chronic conditions",
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 802
          },
          "props": {
            "height": 120,
            "helpText": "Tick any that apply so we can make arrangements.",
            "label": "Assistive needs",
            "options": [
              {
                "label": "I require mobility assistance",
                "value": "mobility"
              },
              {
                "label": "I require help with medication",
                "value": "medication_help"
              },
              {
                "label": "I have severe allergies (epipen)",
                "value": "severe_allergy"
              },
              {
                "label": "No special assistance needed",
                "value": "none"
              }
            ],
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 946
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "placeholder": "Full name",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "dropdown-10",
          "position": {
            "x": 424,
            "y": 946
          },
          "props": {
            "height": 110,
            "label": "Relationship to participant",
            "options": [
              {
                "label": "Partner / Spouse",
                "value": "partner"
              },
              {
                "label": "Parent / Guardian",
                "value": "parent"
              },
              {
                "label": "Friend",
                "value": "friend"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select relationship",
            "tabOrder": 10,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "phone-11",
          "position": {
            "x": 40,
            "y": 1080
          },
          "props": {
            "height": 110,
            "helpText": "Primary phone number for emergency contact.",
            "label": "Emergency contact phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 11,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 120,
            "helpText": "I authorise event staff to arrange or provide urgent medical treatment if required.",
            "label": "Consent to emergency medical treatment",
            "options": [
              {
                "label": "I consent to emergency medical treatment where necessary",
                "value": "consent_medical"
              }
            ],
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 120,
            "helpText": "I have read and accept the event terms and privacy policy (opens in a new window). By agreeing you consent to the collection and use of personal information for event safety and communications.",
            "label": "Event terms and privacy",
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "checkbox-14",
          "position": {
            "x": 40,
            "y": 1502
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to receive event updates and occasional promotional messages by email or SMS. You can unsubscribe at any time.",
            "label": "Event updates and marketing",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive updates and offers",
                "value": "marketing_opt_in"
              }
            ],
            "tabOrder": 14,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "submit-button-15",
          "position": {
            "x": 40,
            "y": 1646
          },
          "props": {
            "height": 72,
            "label": "Submit waiver",
            "tabOrder": 15,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Sydney Event \u2014 Participant Waiver"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 42: `p14-au-adversarial-r1__r01`

- Prompt ID: `p14-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 20,
  "duration_ms": 66148,
  "failure_class": "none",
  "input_tokens": 3883,
  "output_tokens": 5620,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2226,
    "width": 960
  },
  "formId": "au-participant-waiver-form",
  "pages": [
    {
      "components": [
        {
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Provide your contact details, relevant health information and emergency contact. You must accept the waiver and privacy acknowledgement to participate.",
            "tabOrder": 1,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "first-name-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 2,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 424,
            "y": 96
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country code, e.g. +61",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "date-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Day / Month / Year",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Street address",
            "placeholder": "Unit, street",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "label": "Suburb",
            "placeholder": "Suburb",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "label": "State/Territory",
            "options": [
              {
                "label": "New South Wales (NSW)",
                "value": "NSW"
              },
              {
                "label": "Victoria (VIC)",
                "value": "VIC"
              },
              {
                "label": "Queensland (QLD)",
                "value": "QLD"
              },
              {
                "label": "South Australia (SA)",
                "value": "SA"
              },
              {
                "label": "Western Australia (WA)",
                "value": "WA"
              },
              {
                "label": "Tasmania (TAS)",
                "value": "TAS"
              },
              {
                "label": "Australian Capital Territory (ACT)",
                "value": "ACT"
              },
              {
                "label": "Northern Territory (NT)",
                "value": "NT"
              }
            ],
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 110,
            "helpText": "4 digits",
            "label": "Postcode",
            "placeholder": "Postcode",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "divider-11",
          "position": {
            "x": 40,
            "y": 900
          },
          "props": {
            "height": 20,
            "tabOrder": 11,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "radio-12",
          "position": {
            "x": 40,
            "y": 944
          },
          "props": {
            "height": 120,
            "label": "Do you have any medical conditions we should know about?",
            "options": [
              {
                "label": "Yes",
                "value": "yes"
              },
              {
                "label": "No",
                "value": "no"
              }
            ],
            "tabOrder": 12,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 1088
          },
          "props": {
            "height": 200,
            "helpText": "Include relevant conditions, medications and allergies. Leave blank if none.",
            "label": "Health details",
            "placeholder": "List conditions, medications, allergies or mobility needs",
            "tabOrder": 13,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-14",
          "position": {
            "x": 40,
            "y": 1392
          },
          "props": {
            "height": 120,
            "helpText": "This allows staff or contracted medical responders to provide necessary care in an emergency.",
            "label": "Medical consent",
            "options": [
              {
                "label": "I consent to on-site first aid and medical treatment if required",
                "value": "consent_first_aid"
              }
            ],
            "tabOrder": 14,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "text-15",
          "position": {
            "x": 40,
            "y": 1536
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "placeholder": "Full name",
            "tabOrder": 15,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-16",
          "position": {
            "x": 424,
            "y": 1536
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "placeholder": "e.g. Partner, Parent, Friend",
            "tabOrder": 16,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-17",
          "position": {
            "x": 40,
            "y": 1670
          },
          "props": {
            "height": 110,
            "helpText": "Include country code, e.g. +61",
            "label": "Emergency contact phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 17,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "date-18",
          "position": {
            "x": 40,
            "y": 1804
          },
          "props": {
            "height": 110,
            "label": "Date",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 18,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "terms-19",
          "position": {
            "x": 40,
            "y": 1938
          },
          "props": {
            "height": 120,
            "helpText": "Please review and accept our event terms and privacy notice before submitting.",
            "label": "Waiver & privacy acknowledgement",
            "tabOrder": 19,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-20",
          "position": {
            "x": 40,
            "y": 2082
          },
          "props": {
            "height": 72,
            "label": "Sign and submit",
            "tabOrder": 20,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Participant Waiver & Health Form"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 43: `p15-au-neutral-r1__r01`

- Prompt ID: `p15-au-neutral-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "neutral"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 60804,
  "failure_class": "none",
  "input_tokens": 3803,
  "output_tokens": 5098,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1400,
    "width": 960
  },
  "formId": "event-rsvp-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "helpText": "As you\u2019d like it on the guest list",
            "label": "First name",
            "placeholder": "e.g. Alex",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "e.g. Smith",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send booking confirmation and updates to this address",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Australian mobile or landline for urgent event updates (optional)",
            "label": "Phone number",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes \u2014 I will attend",
                "value": "yes"
              },
              {
                "label": "No \u2014 I cannot attend",
                "value": "no"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "State / Territory",
            "options": [
              {
                "label": "New South Wales (NSW)",
                "value": "nsw"
              },
              {
                "label": "Victoria (VIC)",
                "value": "vic"
              },
              {
                "label": "Queensland (QLD)",
                "value": "qld"
              },
              {
                "label": "South Australia (SA)",
                "value": "sa"
              },
              {
                "label": "Western Australia (WA)",
                "value": "wa"
              },
              {
                "label": "Tasmania (TAS)",
                "value": "tas"
              },
              {
                "label": "Australian Capital Territory (ACT)",
                "value": "act"
              },
              {
                "label": "Northern Territory (NT)",
                "value": "nt"
              },
              {
                "label": "Prefer not to say",
                "value": "prefer_not_say"
              }
            ],
            "placeholder": "Select your state or territory",
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 120,
            "helpText": "Select any that apply",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Dairy-free",
                "value": "dairy_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 580
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "placeholder": "Please describe any other dietary needs",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 200,
            "helpText": "We\u2019ll use this to make appropriate arrangements; include carer attendance if needed",
            "label": "Accessibility or support needs",
            "placeholder": "Tell us about any mobility, hearing, vision or support needs",
            "tabOrder": 9,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 1018
          },
          "props": {
            "height": 120,
            "helpText": "I consent to receive event updates and marketing messages from the organiser and agree to the privacy statement.",
            "label": "Consent to event updates",
            "tabOrder": 10,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-11",
          "position": {
            "x": 40,
            "y": 1162
          },
          "props": {
            "height": 72,
            "label": "Submit RSVP",
            "tabOrder": 11,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Event RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 44: `p15-au-ambiguous-r1__r01`

- Prompt ID: `p15-au-ambiguous-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "ambiguous"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 55970,
  "failure_class": "none",
  "input_tokens": 3875,
  "output_tokens": 4745,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 1466,
    "width": 960
  },
  "formId": "rsvp-sydney-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send your RSVP confirmation here.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Australian number for event updates and urgent contact.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Select the Australian state or territory you\u2019re based in.",
            "label": "State / Territory",
            "options": [
              {
                "label": "New South Wales (NSW)",
                "value": "NSW"
              },
              {
                "label": "Victoria (VIC)",
                "value": "VIC"
              },
              {
                "label": "Queensland (QLD)",
                "value": "QLD"
              },
              {
                "label": "South Australia (SA)",
                "value": "SA"
              },
              {
                "label": "Western Australia (WA)",
                "value": "WA"
              },
              {
                "label": "Tasmania (TAS)",
                "value": "TAS"
              },
              {
                "label": "Australian Capital Territory (ACT)",
                "value": "ACT"
              },
              {
                "label": "Northern Territory (NT)",
                "value": "NT"
              }
            ],
            "placeholder": "Select state or territory",
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Tick all that apply.",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "None",
                "value": "none"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Allergies (please specify below)",
                "value": "allergies"
              },
              {
                "label": "Other (please specify below)",
                "value": "other"
              }
            ],
            "tabOrder": 6,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "textarea-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 200,
            "helpText": "Only needed if you selected 'Allergies' or 'Other'.",
            "label": "Dietary details",
            "placeholder": "List allergies or other dietary needs",
            "tabOrder": 7,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 200,
            "helpText": "We\u2019ll follow up if we need more information to support you.",
            "label": "Accessibility needs",
            "placeholder": "Please describe any access support or reasonable adjustments required",
            "tabOrder": 8,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 1178
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive event updates and marketing and accept the event terms.",
            "label": "Event updates & privacy",
            "tabOrder": 9,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1322
          },
          "props": {
            "height": 72,
            "label": "Submit RSVP",
            "tabOrder": 10,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "RSVP \u2014 Sydney event"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```

## Row 45: `p15-au-adversarial-r1__r01`

- Prompt ID: `p15-au-adversarial-r1`
- Repetition: `1`
- Variant: `candidate-a`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `metrics.jsonl`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "benchmark_market": "AU",
  "benchmark_version": "prompts-au-v1",
  "foreign_market_cues_reviewed": [
    "NHS",
    "UK GDPR",
    "NZ regions",
    "ZIP/+1",
    "+44/+64",
    "EU lawful basis",
    "CCPA-only"
  ],
  "locale_axis": "AU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-au-v1",
  "source_market_adaptation": false,
  "variant": "adversarial"
}
```

### Expected AU Signals

```json
{
  "address_field_pattern": "Suburb/State/Postcode",
  "cross_locale_leakage_forbidden": [
    "ZIP",
    "MM/DD/YYYY",
    "+1 (555)"
  ],
  "currency": "AUD",
  "date_format": "DD/MM/YYYY",
  "name_convention": [
    "First name|Given name",
    "Last name|Surname"
  ],
  "phone_country_code": "+61"
}
```

### Prompt Context Section References

```json
[
  {
    "content_hash": "bbd7c8be8ae77b5445286f233c9c3301a36577d795b67bc49b7d33d2809b0ce5",
    "section_id": "system_prompt_output_contract"
  },
  {
    "content_hash": "d96fd9c9255dd75cd5a48d9ea4aab7276bd6b10c6d9df8f64cb62e286fd10a16",
    "section_id": "au_locale_block"
  },
  {
    "content_hash": "9ac128f47d5991793b60e8629c3e40af262b2351620bd415f70f476537b1be08",
    "section_id": "brand_posture_block"
  },
  {
    "content_hash": "88e524f09560bd1cf0dbefc3f6944c6aaf1d36edf5ca1e760a3e35a67263e176",
    "section_id": "component_capability_block"
  },
  {
    "content_hash": "0b9842479af084d35469f68bb5f832a77dd1bd33c4ff207b67a72e821044e10f",
    "section_id": "component_property_cheat_sheet"
  },
  {
    "content_hash": "4a01b0976500be1707eddc4c5e62950cf40688b9831d86338186f682949196ce",
    "section_id": "consent_legal_guidance"
  },
  {
    "content_hash": "06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853",
    "section_id": "context_pack_excerpt"
  },
  {
    "content_hash": "307a153e8b4c1868925bcdee7665214ff446d9a32e4bbe18d649724c44133db2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "f613338e06cc5fcd40c83e6c84d78232581486626b7d2e208a0e51c8d7b1d820",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[]
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 94010,
  "failure_class": "none",
  "input_tokens": 9533,
  "output_tokens": 7746,
  "retry_count": 0,
  "schema_valid": true,
  "terminal_reason": "validated-success",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "canvasSettings": {
    "gridSize": 8,
    "height": 2146,
    "width": 960
  },
  "formId": "event-rsvp-au",
  "pages": [
    {
      "components": [
        {
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 1,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-2",
          "position": {
            "x": 424,
            "y": 24
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 2,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "email-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send RSVP confirmations here",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 3,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Include country code if outside Australia",
            "label": "Phone number",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes, I will attend",
                "value": "yes"
              },
              {
                "label": "No, I cannot attend",
                "value": "no"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "number-6",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 110,
            "helpText": "Maximum 10",
            "label": "Number of guests (including you)",
            "placeholder": "1",
            "tabOrder": 6,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 220
          },
          "type": "number"
        },
        {
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 110,
            "label": "Street address",
            "placeholder": "Street and number (optional)",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 110,
            "label": "Suburb",
            "placeholder": "Suburb",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 424,
            "y": 704
          },
          "props": {
            "height": 110,
            "label": "State / Territory",
            "options": [
              {
                "label": "New South Wales (NSW)",
                "value": "NSW"
              },
              {
                "label": "Victoria (VIC)",
                "value": "VIC"
              },
              {
                "label": "Queensland (QLD)",
                "value": "QLD"
              },
              {
                "label": "South Australia (SA)",
                "value": "SA"
              },
              {
                "label": "Western Australia (WA)",
                "value": "WA"
              },
              {
                "label": "Tasmania (TAS)",
                "value": "TAS"
              },
              {
                "label": "Australian Capital Territory (ACT)",
                "value": "ACT"
              },
              {
                "label": "Northern Territory (NT)",
                "value": "NT"
              }
            ],
            "placeholder": "Select state or territory",
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 838
          },
          "props": {
            "height": 110,
            "label": "Postcode",
            "placeholder": "e.g. 2000",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "dropdown-11",
          "position": {
            "x": 40,
            "y": 972
          },
          "props": {
            "height": 110,
            "label": "Dietary requirements",
            "options": [
              {
                "label": "No special requirements",
                "value": "none"
              },
              {
                "label": "Vegetarian",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select an option",
            "tabOrder": 11,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1106
          },
          "props": {
            "height": 200,
            "label": "Dietary details",
            "placeholder": "Please list allergies or preferences (if applicable)",
            "tabOrder": 12,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 1410
          },
          "props": {
            "height": 200,
            "helpText": "e.g. mobility access, carer support, sensory considerations",
            "label": "Accessibility needs",
            "placeholder": "Tell us any access requirements or support you need",
            "tabOrder": 13,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "checkbox-14",
          "position": {
            "x": 40,
            "y": 1714
          },
          "props": {
            "height": 120,
            "helpText": "Includes updates about the event, venue changes and reminders",
            "label": "Please send me event updates (email or SMS)",
            "options": [
              {
                "label": "Email updates",
                "value": "email"
              },
              {
                "label": "SMS updates",
                "value": "sms"
              }
            ],
            "tabOrder": 14,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-15",
          "position": {
            "x": 40,
            "y": 1858
          },
          "props": {
            "height": 120,
            "helpText": "Read the event terms",
            "label": "I agree to the event terms",
            "tabOrder": 15,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 2002
          },
          "props": {
            "height": 72,
            "label": "RSVP",
            "tabOrder": 16,
            "width": "280px"
          },
          "style": {
            "height": 72,
            "width": 280
          },
          "type": "submit-button"
        }
      ],
      "id": "page-1",
      "title": "Event RSVP"
    }
  ],
  "schemaVersion": "1.0",
  "theme": {
    "backgroundColor": "#FFFFFF",
    "fontFamily": "Inter",
    "primaryColor": "#0055FF"
  }
}
```
