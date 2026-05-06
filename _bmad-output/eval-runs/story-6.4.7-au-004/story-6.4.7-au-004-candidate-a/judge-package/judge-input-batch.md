# Form AI Judge Input Batch

Run ID: `story-6.4.7-au-004-candidate-a`
Benchmark set: `prompts-au-v1`
Rubric version: `rubric_v2`

## Experiment Context

This judge package is for one candidate arm of an Analyst prompt experiment.

```json
{
  "baseline_run_id": "story-6.4.6-au-baseline-current",
  "candidate_hypothesis": "A cleaned AU-003 overlay that keeps strict AU behaviour, silently substitutes AU equivalents, and avoids forbidden-token examples will retain AU-003's high judged score while reducing deterministic prompt-context and generated-output leakage.",
  "candidate_label": "candidate-a",
  "changed_section_id": "candidate_prompt_block",
  "eval_only": true,
  "expected_metric_movement": {
    "copy_quality_score": "increase",
    "cross_locale_leakage": "increase",
    "field_coverage_recall": "increase",
    "format_pattern_accuracy": "increase",
    "locale_fidelity": "increase",
    "policy_compliance": "increase",
    "row_group_agreement": "increase",
    "validation_intent_accuracy": "increase"
  },
  "experiment_id": "story-6.4.7-au-004",
  "improvement_goal": "clean-strict-au-builder-quality",
  "known_risk_metrics": [
    "field_label_f1",
    "cultural_register"
  ],
  "scenario_slice": "au-all",
  "selected_prompt_ids": [],
  "system_prompt_addendum_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
  "target_metrics": [
    "locale_fidelity",
    "cross_locale_leakage",
    "format_pattern_accuracy",
    "policy_compliance",
    "field_coverage_recall",
    "validation_intent_accuracy",
    "copy_quality_score",
    "row_group_agreement"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 34734,
  "failure_class": "none",
  "input_tokens": 3420,
  "output_tokens": 2819,
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
  "formId": "sales-conf-registration-2026",
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
            "helpText": "We will send your ticket and event updates to this email.",
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
            "helpText": "Mobile number for event-day contact",
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
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Tell us any dietary needs for catering.",
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
                "label": "Dairy-free",
                "value": "dairy_free"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select one",
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
            "helpText": "A complimentary conference T-shirt will be provided.",
            "label": "T-shirt size",
            "options": [
              {
                "label": "XS",
                "value": "xs"
              },
              {
                "label": "S",
                "value": "s"
              },
              {
                "label": "M",
                "value": "m"
              },
              {
                "label": "L",
                "value": "l"
              },
              {
                "label": "XL",
                "value": "xl"
              },
              {
                "label": "XXL",
                "value": "xxl"
              }
            ],
            "placeholder": "Select size",
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
            "y": 426
          },
          "props": {
            "height": 200,
            "helpText": "Only fill this in if your dietary need isn't listed.",
            "label": "Other dietary requirements (please specify)",
            "placeholder": "If you selected 'Other', tell us here",
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
          "id": "submit-button-8",
          "position": {
            "x": 40,
            "y": 730
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 31513,
  "failure_class": "none",
  "input_tokens": 3492,
  "output_tokens": 2512,
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
  "formId": "sales-conference-sydney-registration",
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
            "label": "Use this form to register for the Sydney session of our annual sales conference.",
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
            "placeholder": "e.g. Olivia",
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
            "helpText": "We'll send your registration confirmation to this address.",
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
            "helpText": "Mobile or daytime number (Australian format).",
            "label": "Phone",
            "placeholder": "+61 4XX XXX XXX",
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
          "id": "textarea-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 200,
            "helpText": "If none, you can leave this blank.",
            "label": "Dietary requirements or allergies",
            "placeholder": "Please list any dietary requirements, allergies or intolerances",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 668
          },
          "props": {
            "height": 110,
            "helpText": "Select your preferred conference T-shirt size.",
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
            "placeholder": "Select a size",
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
          "id": "submit-button-8",
          "position": {
            "x": 40,
            "y": 802
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
      "title": "Annual Sales Conference \u2014 Sydney Registration"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 47109,
  "failure_class": "none",
  "input_tokens": 3502,
  "output_tokens": 3898,
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
  "formId": "annual-sales-conference-registration",
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
            "helpText": "Include country code if calling from outside Australia.",
            "label": "Phone",
            "placeholder": "+61 4xx xxx xxx",
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
            "helpText": "Australian postcode (4 digits).",
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
          "id": "textarea-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 200,
            "helpText": "Let us know any allergies or dietary needs. Leave blank if none.",
            "label": "Dietary requirements",
            "placeholder": "Allergies, intolerances or other requirements",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 730
          },
          "props": {
            "height": 110,
            "helpText": "Sizing uses standard unisex measurements.",
            "label": "T\u2011shirt size",
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
          "id": "terms-8",
          "position": {
            "x": 40,
            "y": 864
          },
          "props": {
            "height": 120,
            "helpText": "By registering you agree to our event terms and privacy practices.",
            "label": "Terms & privacy",
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
            "y": 1008
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 41972,
  "failure_class": "none",
  "input_tokens": 3417,
  "output_tokens": 3455,
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
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Tell us who will be attending and which session you plan to join. Fields marked with * are required.",
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
            "helpText": "We\u2019ll send your registration confirmation and event updates to this address.",
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
            "helpText": "Include country code if you are travelling from overseas.",
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
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Select the session you will attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Keynote & Opening",
                "value": "keynote_opening"
              },
              {
                "label": "Data & AI track",
                "value": "data_ai"
              },
              {
                "label": "Product & Design track",
                "value": "product_design"
              },
              {
                "label": "Workshops (afternoon)",
                "value": "workshops_afternoon"
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
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 508
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply.",
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
                "label": "Gluten\u2011free",
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
                "label": "Dairy\u2011free",
                "value": "dairy_free"
              },
              {
                "label": "Nut allergy",
                "value": "nut_allergy"
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
            "y": 652
          },
          "props": {
            "height": 200,
            "helpText": "Provide details if you selected 'Other' or have multiple allergies.",
            "label": "Other dietary requirements",
            "placeholder": "Please detail allergies or specific needs (e.g. ingredient to avoid)",
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
            "y": 956
          },
          "props": {
            "height": 120,
            "helpText": "We will manage your personal information in line with our privacy policy and Australian privacy law.",
            "label": "I agree to receive event updates, news and marketing communications from the event organiser. I understand I can withdraw consent at any time.",
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
            "y": 1100
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 40176,
  "failure_class": "none",
  "input_tokens": 3489,
  "output_tokens": 3654,
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
            "helpText": "We will send your booking confirmation and event updates here.",
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
            "helpText": "Australian mobile or landline (optional).",
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
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Organisation",
            "placeholder": "Company or institution (optional)",
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
            "helpText": "Choose the session you'll attend in Sydney.",
            "label": "Session choice",
            "options": [
              {
                "label": "Keynotes (Morning)",
                "value": "keynotes_morning"
              },
              {
                "label": "Workshops (Afternoon)",
                "value": "workshops_afternoon"
              },
              {
                "label": "Full day (Keynotes + Workshops)",
                "value": "full_day"
              },
              {
                "label": "Evening networking",
                "value": "evening_networking"
              }
            ],
            "placeholder": "Select your session",
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
            "helpText": "Select any that apply",
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
            "y": 704
          },
          "props": {
            "height": 200,
            "helpText": "Provide details if you selected 'Other' or have allergies.",
            "label": "Dietary details",
            "placeholder": "Describe any allergies or specific needs (e.g. severe nut allergy)",
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
            "y": 1008
          },
          "props": {
            "height": 120,
            "helpText": "We'll use your email to send event updates. Review the event terms.",
            "label": "I agree to receive event updates and accept the event terms",
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
            "y": 1152
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 43923,
  "failure_class": "none",
  "input_tokens": 3499,
  "output_tokens": 4050,
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
    "height": 1512,
    "width": 960
  },
  "formId": "conf-rsvp-au",
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
            "label": "Please complete your details below so we can reserve your place and dietary requirements.",
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
            "width": 536
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 600,
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
            "helpText": "We'll send your confirmation here.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 600,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or best contact number",
            "label": "Phone (incl. +61)",
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
            "helpText": "Include suburb, state and postcode where possible.",
            "label": "Postal address",
            "placeholder": "Street address, suburb, state",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "address"
        },
        {
          "id": "text-7",
          "position": {
            "x": 600,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Australian 4-digit postcode",
            "label": "Postcode",
            "placeholder": "e.g. 3000",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes",
                "value": "yes"
              },
              {
                "label": "No",
                "value": "no"
              },
              {
                "label": "Maybe",
                "value": "maybe"
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
            "helpText": "Choose the main session you'd like to attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Data & AI \u2014 Morning",
                "value": "data_ai_morning"
              },
              {
                "label": "Cloud Infrastructure \u2014 Morning",
                "value": "cloud_infra_morning"
              },
              {
                "label": "Security & Privacy \u2014 Afternoon",
                "value": "security_afternoon"
              },
              {
                "label": "Product & Design \u2014 Afternoon",
                "value": "product_design_afternoon"
              },
              {
                "label": "Networking Lunch",
                "value": "networking_lunch"
              }
            ],
            "placeholder": "Select your preferred session",
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
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply",
            "label": "Dietary needs",
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
                "label": "Other (please specify)",
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
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "Include allergies or specific instructions",
            "label": "Other dietary requirements",
            "placeholder": "Please provide details if you selected Other",
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
          "id": "terms-12",
          "position": {
            "x": 40,
            "y": 1224
          },
          "props": {
            "height": 120,
            "helpText": "You can unsubscribe at any time.",
            "label": "I agree to receive event updates and promotional messages",
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
            "y": 1368
          },
          "props": {
            "height": 72,
            "label": "Submit RSVP",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 40504,
  "failure_class": "none",
  "input_tokens": 3415,
  "output_tokens": 3790,
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
    "height": 1440,
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
            "helpText": "We'll send booking confirmation and event updates to this address.",
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
            "helpText": "Local number we can use for urgent day-of-event messages.",
            "label": "Phone number (optional)",
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
            "label": "Organisation (optional)",
            "placeholder": "Company or institution",
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
            "helpText": "Choose the option that best matches your current experience.",
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
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "We'll aim to place you in your preferred stream where possible.",
            "label": "Preferred workshop stream",
            "options": [
              {
                "label": "Design Thinking",
                "value": "design-thinking"
              },
              {
                "label": "Data & Analytics",
                "value": "data-analytics"
              },
              {
                "label": "Coding Foundations",
                "value": "coding-foundations"
              },
              {
                "label": "Leadership & Facilitation",
                "value": "leadership-facilitation"
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
            "y": 704
          },
          "props": {
            "height": 120,
            "helpText": "Select any supports you require; we will contact you to confirm arrangements if needed.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair-access"
              },
              {
                "label": "Auslan interpreter",
                "value": "auslan-interpreter"
              },
              {
                "label": "Large-print materials",
                "value": "large-print"
              },
              {
                "label": "Quiet workspace / low-sensory area",
                "value": "quiet-workspace"
              },
              {
                "label": "Assistance with mobility",
                "value": "mobility-assistance"
              },
              {
                "label": "Other (please describe below)",
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
            "y": 848
          },
          "props": {
            "height": 200,
            "helpText": "Providing details helps us make appropriate arrangements.",
            "label": "If other or further details, tell us here (optional)",
            "placeholder": "Describe any specific accessibility requirements or supports you need",
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
            "y": 1152
          },
          "props": {
            "height": 120,
            "helpText": "By agreeing you consent to communications about this event and related logistics.",
            "label": "I agree to the event terms and understand my personal information will be used to manage my registration and to send event communications.",
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
            "y": 1296
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 38024,
  "failure_class": "none",
  "input_tokens": 3487,
  "output_tokens": 3595,
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
    "height": 1430,
    "width": 960
  },
  "formId": "sydney-workshop-signup",
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
            "helpText": "We'll use this for your ticket and event updates",
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
            "helpText": "Mobile preferred for event SMS updates",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode if relevant",
            "label": "Address (optional)",
            "placeholder": "Street address, suburb, state, postcode",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
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
            "placeholder": "Select your skill level",
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
            "y": 560
          },
          "props": {
            "height": 110,
            "helpText": "Select the stream you'd most like to attend",
            "label": "Preferred workshop stream",
            "options": [
              {
                "label": "Design Thinking",
                "value": "design_thinking"
              },
              {
                "label": "Data & Analytics",
                "value": "data_analytics"
              },
              {
                "label": "Communication & Leadership",
                "value": "communication_leadership"
              }
            ],
            "placeholder": "Choose a stream",
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
            "y": 694
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply",
            "label": "Accessibility requirements",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair_access"
              },
              {
                "label": "Auslan interpreter",
                "value": "auslan_interpreter"
              },
              {
                "label": "Quiet or low-sensory space",
                "value": "quiet_space"
              },
              {
                "label": "Assistance with mobility",
                "value": "mobility_assist"
              },
              {
                "label": "Dietary requirements (if catering provided)",
                "value": "dietary_requirements"
              },
              {
                "label": "Other (please describe below)",
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
            "y": 838
          },
          "props": {
            "height": 200,
            "helpText": "We will contact you if we need more information to support your attendance",
            "label": "Accessibility or dietary details",
            "placeholder": "Describe any accessibility needs or dietary requirements",
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
            "y": 1142
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and to receive event-related communications.",
            "label": "Agreement",
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
            "y": 1286
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
      "title": "Sydney workshop signup"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 51238,
  "failure_class": "none",
  "input_tokens": 3497,
  "output_tokens": 4583,
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
    "height": 1522,
    "width": 960
  },
  "formId": "workshop-signup-au",
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
            "label": "Tell us about yourself and your preferences so we can place you in the right stream.",
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
            "helpText": "We\u2019ll send confirmation and event updates to this address.",
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
            "helpText": "Include country code if outside Australia.",
            "label": "Phone number",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "4-digit Australian postcode.",
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
            "label": "Preferred workshop stream",
            "options": [
              {
                "label": "Data Science",
                "value": "data_science"
              },
              {
                "label": "Web Development",
                "value": "web_development"
              },
              {
                "label": "Design Thinking",
                "value": "design_thinking"
              },
              {
                "label": "Project Management",
                "value": "project_management"
              }
            ],
            "placeholder": "Choose a stream",
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
            "helpText": "Select any supports you require. Provide details below if needed.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair_access"
              },
              {
                "label": "Hearing support / captions",
                "value": "hearing_support"
              },
              {
                "label": "Visual assistance / large print",
                "value": "visual_assistance"
              },
              {
                "label": "Dietary requirements",
                "value": "dietary_requirements"
              },
              {
                "label": "Other",
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
            "helpText": "Include any specifics (e.g. mobility, sensory, dietary) and we'll follow up.",
            "label": "Accessibility details",
            "placeholder": "Tell us about any support or adjustments you need",
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
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "Optional: agree to receive event updates and related news by email.",
            "label": "Marketing consent",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive event updates and news by email",
                "value": "marketing_opt_in"
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
            "y": 1234
          },
          "props": {
            "height": 120,
            "helpText": "By signing up you agree to the event terms and our privacy practices. View the event terms.",
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
            "y": 1378
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
    "prompt_id": "p04-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p04-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p04-au-neutral-r1",
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
  "component_count": 11,
  "duration_ms": 44566,
  "failure_class": "none",
  "input_tokens": 3420,
  "output_tokens": 3938,
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
            "helpText": "As it will appear on the attendee list.",
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
            "helpText": "We\u2019ll send your joining link and event updates to this address.",
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
            "helpText": "Optional \u2014 for urgent updates by SMS or phone.",
            "label": "Phone (optional)",
            "placeholder": "+61 4XX XXX XXX",
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
            "helpText": "Optional \u2014 used for attendee reporting.",
            "label": "Organisation",
            "placeholder": "Company or institution",
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
            "label": "Job title / role",
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
            "helpText": "So we can show the session time in your local zone.",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST, UTC+10)",
                "value": "Australia/Sydney"
              },
              {
                "label": "Australia/Adelaide (ACST, UTC+9:30)",
                "value": "Australia/Adelaide"
              },
              {
                "label": "Australia/Perth (AWST, UTC+8)",
                "value": "Australia/Perth"
              },
              {
                "label": "New Zealand/Auckland (NZDT, UTC+13)",
                "value": "Pacific/Auckland"
              },
              {
                "label": "UTC (Coordinated Universal Time)",
                "value": "UTC"
              },
              {
                "label": "Other (please specify below)",
                "value": "Other"
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
          "id": "text-8",
          "position": {
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 enter an IANA timezone or UTC offset if not listed.",
            "label": "Timezone (if Other)",
            "placeholder": "e.g. Europe/London or UTC+1",
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
            "y": 560
          },
          "props": {
            "height": 200,
            "helpText": "We'll try to address common questions during Q&A.",
            "label": "Questions for the speaker",
            "placeholder": "Let us know any topics or questions you\u2019d like covered",
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
            "y": 864
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive updates about this event and occasional marketing messages. You can unsubscribe anytime.",
            "label": "Marketing and event updates",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and marketing emails",
                "value": "yes_marketing"
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
          "id": "submit-button-11",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 72,
            "label": "Register",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
    "prompt_id": "p04-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p04-au-ambiguous-r1",
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
  "duration_ms": 46891,
  "failure_class": "none",
  "input_tokens": 3492,
  "output_tokens": 4138,
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
            "label": "Join us online \u2014 the webinar will run in Sydney time. Please tell us a bit about yourself so we can send your access details.",
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
            "placeholder": "First name",
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
            "placeholder": "Last name",
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
            "helpText": "We'll send webinar access details to this address.",
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
            "helpText": "Provide a number if you prefer SMS updates about the event.",
            "label": "Phone (optional)",
            "placeholder": "[SCRUBBED_PHONE]",
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
            "label": "Job title / role",
            "placeholder": "e.g. Product Manager",
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
            "helpText": "Webinar will run in Australia/Sydney time (AEST/AEDT). Choose your local timezone for calendar invites.",
            "label": "Your timezone",
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
              },
              {
                "label": "New Zealand/Auckland (NZST/NZDT)",
                "value": "Pacific/Auckland"
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
                "label": "Europe/London (GMT/BST)",
                "value": "Europe/London"
              },
              {
                "label": "Europe/Berlin (CET/CEST)",
                "value": "Europe/Berlin"
              },
              {
                "label": "America/New_York (ET)",
                "value": "America/New_York"
              },
              {
                "label": "America/Los_Angeles (PT)",
                "value": "America/Los_Angeles"
              }
            ],
            "placeholder": "Select your timezone",
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
            "helpText": "We'll try to cover common questions during the session and the Q&A.",
            "label": "Questions for the speaker (optional)",
            "placeholder": "Let us know any questions you'd like the speaker to address",
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
            "helpText": "Tick if you'd like event updates and occasional marketing from us.",
            "label": "Marketing preferences",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and occasional marketing",
                "value": "marketing_opt_in"
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
            "helpText": "By registering you accept the event terms and privacy policy.",
            "label": "I agree to the event terms and privacy policy",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p04-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p04-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p04-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p04-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p04-au-adversarial-r1",
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
  "duration_ms": 47894,
  "failure_class": "none",
  "input_tokens": 3502,
  "output_tokens": 4172,
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
  "formId": "webinar-registration-zip-plus1",
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
            "label": "We\u2019ll send joining details and a calendar invite after registration.",
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
            "helpText": "We\u2019ll use this for event updates and the join link.",
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
            "helpText": "Optional \u2014 include country code (+1).",
            "label": "Phone (+1)",
            "placeholder": "[SCRUBBED_PHONE]",
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
            "placeholder": "e.g. Product Manager",
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
            "helpText": "We\u2019ll schedule reminders in your local time.",
            "label": "Timezone",
            "options": [
              {
                "label": "UTC\u221208:00 Pacific Time (US & Canada)",
                "value": "UTC-08:00"
              },
              {
                "label": "UTC\u221205:00 Eastern Time (US & Canada)",
                "value": "UTC-05:00"
              },
              {
                "label": "UTC\u00b100:00 (GMT)",
                "value": "UTC+00:00"
              },
              {
                "label": "UTC+01:00 Central European Time",
                "value": "UTC+01:00"
              },
              {
                "label": "UTC+05:30 India Standard Time",
                "value": "UTC+05:30"
              },
              {
                "label": "UTC+10:00 Australia/Sydney",
                "value": "Australia/Sydney"
              }
            ],
            "placeholder": "Select your timezone",
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
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Include ZIP/postal code for your billing or records if needed.",
            "label": "ZIP code",
            "placeholder": "e.g. 94105",
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
            "y": 766
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 we may share selected questions with the presenter.",
            "label": "Questions for the speaker",
            "placeholder": "Any questions you\u2019d like the speaker to address?",
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
            "y": 1070
          },
          "props": {
            "height": 120,
            "helpText": "You can opt out at any time.",
            "label": "I agree to receive event updates and marketing",
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
            "y": 1214
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "component_count": 15,
  "duration_ms": 72311,
  "failure_class": "none",
  "input_tokens": 8550,
  "output_tokens": 6343,
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
            "helpText": "We'll send confirmation and event updates to this address.",
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
            "helpText": "Local Australian number; used only for urgent event updates.",
            "label": "Phone (optional)",
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
            "label": "Attendance",
            "options": [
              {
                "label": "Yes \u2014 I will be attending",
                "value": "attending"
              },
              {
                "label": "No \u2014 Sorry, I can't make it",
                "value": "not_attending"
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
            "helpText": "Tick if you will bring a guest and provide their details below.",
            "label": "Bringing a plus-one?",
            "options": [
              {
                "label": "Yes \u2014 I will bring a guest",
                "value": "bringing_plus_one"
              }
            ],
            "tabOrder": 6,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
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
            "width": 360
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
            "label": "Your meal choice",
            "options": [
              {
                "label": "Beef (eye fillet)",
                "value": "beef"
              },
              {
                "label": "Chicken (free-range)",
                "value": "chicken"
              },
              {
                "label": "Pan-fried fish",
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
                "value": "kids"
              }
            ],
            "placeholder": "Select your main",
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
          "id": "dropdown-10",
          "position": {
            "x": 424,
            "y": 714
          },
          "props": {
            "height": 110,
            "helpText": "If bringing a plus-one, choose their meal.",
            "label": "Plus-one meal choice",
            "options": [
              {
                "label": "Beef (eye fillet)",
                "value": "beef"
              },
              {
                "label": "Chicken (free-range)",
                "value": "chicken"
              },
              {
                "label": "Pan-fried fish",
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
                "value": "kids"
              }
            ],
            "placeholder": "Select plus-one's main",
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
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 200,
            "helpText": "Please list any dietary needs for you and your guest.",
            "label": "Dietary requirements",
            "placeholder": "Allergies, intolerances or special requests",
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
          "id": "text-12",
          "position": {
            "x": 40,
            "y": 1152
          },
          "props": {
            "height": 110,
            "helpText": "We'll pass this to the DJ if possible.",
            "label": "Song request (optional)",
            "placeholder": "Song title \u2014 artist",
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
            "y": 1286
          },
          "props": {
            "height": 200,
            "label": "Message for the couple (optional)",
            "placeholder": "A short message or well wishes",
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
            "y": 1590
          },
          "props": {
            "height": 120,
            "helpText": "Optional: we'll only contact you about this wedding.",
            "label": "I'd like to receive event updates (email or SMS)",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive event updates (email or SMS)",
                "value": "consent_updates"
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
            "y": 1734
          },
          "props": {
            "height": 72,
            "label": "Send RSVP",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "component_count": 15,
  "duration_ms": 74847,
  "failure_class": "none",
  "input_tokens": 8569,
  "output_tokens": 6606,
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
    "height": 1940,
    "width": 960
  },
  "formId": "rsvp-wedding-sydney",
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
            "label": "We're so glad you're invited. Fill in your details below to let us know if you'll attend and any preferences.",
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
            "helpText": "We'll send an RSVP confirmation to this address.",
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
            "helpText": "Optional \u2014 helpful for last-minute updates.",
            "label": "Phone (optional)",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
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
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Please let us know whether you can attend the wedding in Sydney.",
            "label": "Attendance",
            "options": [
              {
                "label": "Accept with pleasure",
                "value": "accept"
              },
              {
                "label": "Regretfully decline",
                "value": "decline"
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
          "id": "checkbox-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you're bringing an accompanying guest.",
            "label": "I will be bringing a plus-one",
            "options": [
              {
                "label": "Yes \u2014 I will bring a plus-one",
                "value": "bringing_plus_one"
              }
            ],
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "checkbox"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 508
          },
          "props": {
            "height": 110,
            "helpText": "If bringing a guest, provide their name.",
            "label": "Plus-one full name",
            "placeholder": "Full name of your guest",
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
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "If attending, please choose your main course.",
            "label": "Your meal choice",
            "options": [
              {
                "label": "Roast chicken (main)",
                "value": "chicken"
              },
              {
                "label": "Beef (main)",
                "value": "beef"
              },
              {
                "label": "Seafood (main)",
                "value": "seafood"
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
                "label": "Children's meal",
                "value": "children"
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
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 110,
            "helpText": "If bringing a guest, choose their meal.",
            "label": "Plus-one meal choice",
            "options": [
              {
                "label": "Roast chicken (main)",
                "value": "chicken"
              },
              {
                "label": "Beef (main)",
                "value": "beef"
              },
              {
                "label": "Seafood (main)",
                "value": "seafood"
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
                "label": "Children's meal",
                "value": "children"
              }
            ],
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
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 910
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about allergies or dietary restrictions.",
            "label": "Dietary requirements / allergies",
            "placeholder": "List any dietary needs, allergies or intolerances",
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
          "id": "text-12",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 110,
            "helpText": "One song you'd like to hear at the reception.",
            "label": "Song request",
            "placeholder": "Song title \u2014 artist",
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
            "y": 1348
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 a short message to the couple.",
            "label": "Message for the couple",
            "placeholder": "Optional message or well wishes",
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
            "y": 1652
          },
          "props": {
            "height": 120,
            "helpText": "View the event terms.",
            "label": "I agree to the event terms and privacy policy",
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
            "y": 1796
          },
          "props": {
            "height": 72,
            "label": "Send RSVP",
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
      "title": "Sydney Wedding RSVP"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p05-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p05-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p05-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p05-au-adversarial-r1",
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
  "component_count": 17,
  "duration_ms": 65207,
  "failure_class": "none",
  "input_tokens": 3503,
  "output_tokens": 5912,
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
    "height": 2084,
    "width": 960
  },
  "formId": "wedding-rsvp-au",
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
            "label": "We look forward to celebrating with you \u2014 let us know your plans.",
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
            "width": 536
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 600,
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
            "helpText": "We\u2019ll use this for RSVP confirmations and updates.",
            "label": "Email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 600,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Mobile preferred for last-minute updates.",
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
            "helpText": "Optional \u2014 used for seating and directions if needed.",
            "label": "Address",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "address"
        },
        {
          "id": "text-7",
          "position": {
            "x": 600,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include postcode (label includes ZIP by request).",
            "label": "Postcode (ZIP)",
            "placeholder": "Postcode or ZIP",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes, I will attend",
                "value": "attending_yes"
              },
              {
                "label": "No, I am sorry I can\u2019t attend",
                "value": "attending_no"
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
          "id": "radio-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "If yes, please provide their details below.",
            "label": "Will you bring a plus-one?",
            "options": [
              {
                "label": "Yes \u2014 I will bring a plus-one",
                "value": "plus_one_yes"
              },
              {
                "label": "No \u2014 I will not bring a plus-one",
                "value": "plus_one_no"
              }
            ],
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 110,
            "label": "Plus-one name",
            "placeholder": "Full name",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "text"
        },
        {
          "id": "phone-11",
          "position": {
            "x": 600,
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "Provide a contact number for your plus-one if available.",
            "label": "Plus-one phone (+1)",
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
          "id": "dropdown-12",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 110,
            "helpText": "Choose the menu option for the guest named above.",
            "label": "Meal choice",
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
              },
              {
                "label": "Children\u2019s meal",
                "value": "children"
              },
              {
                "label": "Other / I\u2019ll provide details",
                "value": "other"
              }
            ],
            "placeholder": "Select a meal",
            "tabOrder": 12,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 1054
          },
          "props": {
            "height": 200,
            "helpText": "Include details for the guest and any plus-one.",
            "label": "Dietary requirements or allergies",
            "placeholder": "Please list any allergies or dietary needs (e.g. gluten-free, nut allergy)",
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
          "id": "text-14",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 110,
            "helpText": "One song request per RSVP, if you like!",
            "label": "Song request",
            "placeholder": "Song title and artist",
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
          "id": "textarea-15",
          "position": {
            "x": 40,
            "y": 1492
          },
          "props": {
            "height": 200,
            "label": "Message for the couple",
            "placeholder": "A short message or well wishes",
            "tabOrder": 15,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-16",
          "position": {
            "x": 40,
            "y": 1796
          },
          "props": {
            "height": 120,
            "helpText": "Please accept the event terms to submit your RSVP.",
            "label": "Acknowledgement",
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
            "y": 1940
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 52627,
  "failure_class": "none",
  "input_tokens": 3417,
  "output_tokens": 4705,
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
    "height": 1780,
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
            "label": "Thanks for offering to volunteer. Please provide your contact details, availability and any skills or certifications you hold.",
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
            "helpText": "We will send shift confirmations and event updates to this address.",
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
            "helpText": "We may contact you by SMS or phone about shifts.",
            "label": "Mobile phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
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
            "helpText": "Provide suburb, state and postcode for location planning.",
            "label": "Address (street, suburb, state, postcode)",
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
          "id": "date-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Optional: earliest date you can start",
            "label": "Available from",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "date-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Optional: last date you're available",
            "label": "Available to",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "label": "Which days/times can you volunteer? (select all that apply)",
            "options": [
              {
                "label": "Weekday mornings",
                "value": "weekday_mornings"
              },
              {
                "label": "Weekday afternoons",
                "value": "weekday_afternoons"
              },
              {
                "label": "Weekday evenings",
                "value": "weekday_evenings"
              },
              {
                "label": "Weekend mornings",
                "value": "weekend_mornings"
              },
              {
                "label": "Weekend afternoons",
                "value": "weekend_afternoons"
              },
              {
                "label": "Weekend evenings",
                "value": "weekend_evenings"
              },
              {
                "label": "Any time",
                "value": "any_time"
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
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Include formal certifications you hold.",
            "label": "Skills and certifications (select all that apply)",
            "options": [
              {
                "label": "First aid / CPR",
                "value": "first_aid"
              },
              {
                "label": "Crowd management / stewarding",
                "value": "crowd_management"
              },
              {
                "label": "Hospitality / catering",
                "value": "hospitality"
              },
              {
                "label": "Sound / AV / technical",
                "value": "sound_av"
              },
              {
                "label": "Logistics / setup / packdown",
                "value": "logistics"
              },
              {
                "label": "Driver's licence",
                "value": "drivers_licence"
              },
              {
                "label": "Working with children check (if held)",
                "value": "wwcc"
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
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "Only include details relevant to volunteering and safety.",
            "label": "Other skills or notes",
            "placeholder": "Tell us about any other skills, accessibility needs or medical conditions you are comfortable sharing",
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
          "id": "text-12",
          "position": {
            "x": 40,
            "y": 1224
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "placeholder": "Full name",
            "tabOrder": 12,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-13",
          "position": {
            "x": 424,
            "y": 1224
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "placeholder": "e.g. partner, parent, friend",
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
          "id": "phone-14",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 110,
            "label": "Emergency contact phone",
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
          "id": "email-15",
          "position": {
            "x": 424,
            "y": 1358
          },
          "props": {
            "height": 110,
            "label": "Emergency contact email (optional)",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 15,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "terms-16",
          "position": {
            "x": 40,
            "y": 1492
          },
          "props": {
            "height": 120,
            "helpText": "By agreeing you consent to event-related communications necessary for your role.",
            "label": "I agree to the volunteer code of conduct and understand that I must follow safety instructions and directions from event staff. I understand serious breaches may result in removal from duties.",
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
            "y": 1636
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
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
      "title": "Volunteer signup form"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 50881,
  "failure_class": "none",
  "input_tokens": 3489,
  "output_tokens": 4526,
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
    "height": 1778,
    "width": 960
  },
  "formId": "volunteer-signup-sydney",
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
            "label": "Shifts and roles vary across the event. We'll contact you by email or phone to confirm details.",
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
            "helpText": "Mobile preferred so we can contact you on the day.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
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
            "helpText": "Include suburb, state and postcode",
            "label": "Home address",
            "placeholder": "Street address",
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
          "id": "divider-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 20,
            "tabOrder": 7,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 542
          },
          "props": {
            "height": 120,
            "helpText": "Tick all times you can help",
            "label": "Availability",
            "options": [
              {
                "label": "Weekdays \u2014 Morning (8am\u201312pm)",
                "value": "weekdays_morning"
              },
              {
                "label": "Weekdays \u2014 Afternoon (12pm\u20135pm)",
                "value": "weekdays_afternoon"
              },
              {
                "label": "Weekdays \u2014 Evening (5pm\u20139pm)",
                "value": "weekdays_evening"
              },
              {
                "label": "Saturday \u2014 Morning",
                "value": "saturday_morning"
              },
              {
                "label": "Saturday \u2014 Afternoon",
                "value": "saturday_afternoon"
              },
              {
                "label": "Sunday \u2014 Morning",
                "value": "sunday_morning"
              },
              {
                "label": "Sunday \u2014 Afternoon",
                "value": "sunday_afternoon"
              },
              {
                "label": "I can help any day/time",
                "value": "any_time"
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
            "y": 686
          },
          "props": {
            "height": 120,
            "helpText": "Select any that apply",
            "label": "Skills & experience",
            "options": [
              {
                "label": "First aid (certified)",
                "value": "first_aid"
              },
              {
                "label": "Crowd management",
                "value": "crowd_management"
              },
              {
                "label": "Registration / check-in",
                "value": "registration"
              },
              {
                "label": "Setup / packdown",
                "value": "setup_packdown"
              },
              {
                "label": "Food service (food safety trained)",
                "value": "food_service"
              },
              {
                "label": "Photography / social media",
                "value": "photography"
              },
              {
                "label": "Driver (light vehicle)",
                "value": "driver"
              },
              {
                "label": "Other \u2014 please describe below",
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
            "y": 830
          },
          "props": {
            "height": 200,
            "helpText": "Use this field to expand on any selected skills or note other relevant experience.",
            "label": "Skills details or certifications",
            "placeholder": "List certificates, previous roles or training (include certificate numbers if applicable)",
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
          "id": "divider-11",
          "position": {
            "x": 40,
            "y": 1134
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
          "id": "text-12",
          "position": {
            "x": 40,
            "y": 1178
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 full name",
            "placeholder": "Full name",
            "tabOrder": 12,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "dropdown-13",
          "position": {
            "x": 424,
            "y": 1178
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "options": [
              {
                "label": "Partner",
                "value": "partner"
              },
              {
                "label": "Parent",
                "value": "parent"
              },
              {
                "label": "Sibling",
                "value": "sibling"
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
            "tabOrder": 13,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "phone-14",
          "position": {
            "x": 40,
            "y": 1312
          },
          "props": {
            "height": 110,
            "helpText": "Local phone number we can call in an emergency.",
            "label": "Emergency contact \u2014 phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 14,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "divider-15",
          "position": {
            "x": 40,
            "y": 1446
          },
          "props": {
            "height": 20,
            "tabOrder": 15,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "terms-16",
          "position": {
            "x": 40,
            "y": 1490
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the code of conduct to volunteer.",
            "label": "I have read and agree to the event code of conduct and volunteer guidelines. See event terms.",
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
            "y": 1634
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
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
      "title": "Volunteer Signup \u2014 Sydney"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p06-au-adversarial-r1",
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
  "component_count": 19,
  "duration_ms": 61702,
  "failure_class": "none",
  "input_tokens": 3499,
  "output_tokens": 5455,
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
            "helpText": "We'll use this for event updates and shift confirmations.",
            "label": "Email address",
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
            "helpText": "Include the +1 country code as shown.",
            "label": "Phone (include +1 country code)",
            "placeholder": "[SCRUBBED_PHONE]",
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
            "helpText": "Optional \u2014 useful for local role assignments.",
            "label": "Street address",
            "placeholder": "Street address, suburb, state",
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
            "helpText": "Provide ZIP code as requested.",
            "label": "ZIP code",
            "placeholder": "e.g. 02138",
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
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Select all days you can volunteer",
            "label": "Availability \u2014 days",
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
          "id": "date-8",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 110,
            "label": "Availability start date",
            "placeholder": "Start date",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "date"
        },
        {
          "id": "date-9",
          "position": {
            "x": 567,
            "y": 570
          },
          "props": {
            "height": 110,
            "label": "Availability end date",
            "placeholder": "End date (optional)",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "date"
        },
        {
          "id": "radio-10",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 120,
            "helpText": "Choose your usual availability window",
            "label": "Preferred shift time",
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
                "label": "Any",
                "value": "any"
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
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 120,
            "helpText": "Select relevant skills or experience",
            "label": "Skills",
            "options": [
              {
                "label": "First aid / CPR",
                "value": "first_aid"
              },
              {
                "label": "Crowd management",
                "value": "crowd_management"
              },
              {
                "label": "Registration / check-in",
                "value": "registration"
              },
              {
                "label": "Food service",
                "value": "food_service"
              },
              {
                "label": "Child supervision",
                "value": "child_supervision"
              },
              {
                "label": "Languages (specify in notes)",
                "value": "languages"
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
            "y": 992
          },
          "props": {
            "height": 200,
            "label": "Other skills or notes",
            "placeholder": "Tell us about other skills, certifications or language fluency",
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
            "y": 1296
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 full name",
            "placeholder": "Full name",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "text"
        },
        {
          "id": "dropdown-14",
          "position": {
            "x": 567,
            "y": 1296
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "options": [
              {
                "label": "Partner / spouse",
                "value": "partner"
              },
              {
                "label": "Parent",
                "value": "parent"
              },
              {
                "label": "Sibling",
                "value": "sibling"
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
            "tabOrder": 14,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "dropdown"
        },
        {
          "id": "phone-15",
          "position": {
            "x": 40,
            "y": 1430
          },
          "props": {
            "height": 110,
            "helpText": "We will only use this in an emergency.",
            "label": "Emergency contact phone (include +1 country code)",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 15,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "phone"
        },
        {
          "id": "phone-16",
          "position": {
            "x": 567,
            "y": 1430
          },
          "props": {
            "height": 110,
            "label": "Alternate phone (optional)",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 16,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "phone"
        },
        {
          "id": "textarea-17",
          "position": {
            "x": 40,
            "y": 1564
          },
          "props": {
            "height": 200,
            "label": "Medical or accessibility info (optional)",
            "placeholder": "Let us know any medical needs or accessibility requirements",
            "tabOrder": 17,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "terms-18",
          "position": {
            "x": 40,
            "y": 1868
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event terms and code of conduct to volunteer.",
            "label": "Code of conduct acknowledgement",
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
            "y": 2012
          },
          "props": {
            "height": 72,
            "label": "Sign up",
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
      "title": "Volunteer signup form"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 55915,
  "failure_class": "none",
  "input_tokens": 3417,
  "output_tokens": 4926,
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
    "height": 1764,
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
            "label": "Please complete this form to apply for membership. Fields marked required must be completed.",
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
            "helpText": "We'll send membership info and receipts to this address.",
            "label": "Email",
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
            "helpText": "Australian mobile or landline number.",
            "label": "Phone",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
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
          "id": "date-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "You must be 18 years or older to apply.",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "date"
        },
        {
          "id": "address-7",
          "position": {
            "x": 417,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode.",
            "label": "Postal address",
            "tabOrder": 7,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "address"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 40,
            "y": 498
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
                "label": "Student (proof required)",
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
            "placeholder": "Select a membership type",
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
            "y": 632
          },
          "props": {
            "height": 120,
            "label": "I confirm I am 18 years of age or older",
            "options": [
              {
                "label": "I confirm I am 18 years of age or older",
                "value": "confirm_over_18"
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
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "I understand eligibility criteria set by the organisation.",
            "label": "I meet the membership eligibility criteria",
            "options": [
              {
                "label": "I meet the membership eligibility criteria",
                "value": "meet_criteria"
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
            "y": 920
          },
          "props": {
            "height": 120,
            "label": "I agree to abide by the organisation\u2019s code of conduct",
            "options": [
              {
                "label": "I agree to abide by the organisation\u2019s code of conduct",
                "value": "agree_code"
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
          "id": "dropdown-12",
          "position": {
            "x": 40,
            "y": 1064
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
                "label": "Event or expo",
                "value": "event"
              },
              {
                "label": "Advertisement",
                "value": "ad"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select one",
            "tabOrder": 12,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "placeholder": "Who or where?",
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
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1332
          },
          "props": {
            "height": 120,
            "helpText": "By applying I agree to the organisation's membership terms and the handling of my personal information as described in the privacy notice. I consent to receiving electronic communications regarding my membership.",
            "label": "Membership terms & privacy",
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
          "id": "checkbox-15",
          "position": {
            "x": 40,
            "y": 1476
          },
          "props": {
            "height": 120,
            "helpText": "Optional: you can opt out at any time.",
            "label": "I agree to receive occasional updates and offers by email",
            "options": [
              {
                "label": "I agree to receive occasional updates and offers by email",
                "value": "marketing_consent"
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
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 1620
          },
          "props": {
            "height": 72,
            "label": "Apply for membership",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 44077,
  "failure_class": "none",
  "input_tokens": 3489,
  "output_tokens": 3806,
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
  "formId": "membership-application-sydney",
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
            "label": "All fields marked required must be completed. We'll contact you at the email or phone number you provide.",
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
            "helpText": "We'll use this to send membership confirmation.",
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
            "helpText": "Australian phone number, include country code if applicable.",
            "label": "Phone number",
            "placeholder": "+61 4XX XXX XXX",
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
          "id": "date-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Enter your date of birth (day/month/year).",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "date"
        },
        {
          "id": "address-7",
          "position": {
            "x": 417,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide your current residential or postal address in Sydney.",
            "label": "Postal address",
            "placeholder": "Street address, suburb, state, postcode",
            "tabOrder": 7,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "address"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose the membership level you are applying for.",
            "label": "Membership type",
            "options": [
              {
                "label": "Standard",
                "value": "standard"
              },
              {
                "label": "Premium",
                "value": "premium"
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
                "label": "Organisation / Business",
                "value": "organisation"
              }
            ],
            "placeholder": "Select membership type",
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
            "y": 632
          },
          "props": {
            "height": 120,
            "label": "I confirm I am 18 years of age or older",
            "options": [
              {
                "label": "I confirm",
                "value": "confirm_age"
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
            "y": 776
          },
          "props": {
            "height": 120,
            "label": "I live or work in the Sydney area",
            "options": [
              {
                "label": "I confirm",
                "value": "confirm_residency"
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
            "y": 920
          },
          "props": {
            "height": 120,
            "label": "I will comply with the organisation's code of conduct",
            "options": [
              {
                "label": "I agree",
                "value": "agree_code"
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
          "id": "dropdown-12",
          "position": {
            "x": 40,
            "y": 1064
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
                "label": "Flyer or poster",
                "value": "flyer"
              },
              {
                "label": "Event or workshop",
                "value": "event"
              },
              {
                "label": "Website search",
                "value": "website"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select an option",
            "tabOrder": 12,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 353
          },
          "type": "dropdown"
        },
        {
          "id": "text-13",
          "position": {
            "x": 417,
            "y": 1064
          },
          "props": {
            "height": 110,
            "helpText": "Optional",
            "label": "If other, please specify",
            "placeholder": "Tell us where you heard about us",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "text"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 120,
            "helpText": "You must accept the event terms to complete your application. See event terms.",
            "label": "Agreement and terms",
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
          "id": "textarea-15",
          "position": {
            "x": 40,
            "y": 1342
          },
          "props": {
            "height": 200,
            "helpText": "Include accessibility requirements or other notes.",
            "label": "Additional information (optional)",
            "placeholder": "Any other information we should know",
            "tabOrder": 15,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 1646
          },
          "props": {
            "height": 72,
            "label": "Submit application",
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
      "title": "Sydney membership application"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 49300,
  "failure_class": "none",
  "input_tokens": 3499,
  "output_tokens": 4214,
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
    "height": 1502,
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
            "label": "Please complete the form to apply for membership. Required fields are marked.",
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
            "helpText": "We will use this for membership communications.",
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
            "helpText": "Mobile or best contact number.",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Membership type",
            "options": [
              {
                "label": "Standard",
                "value": "standard"
              },
              {
                "label": "Premium",
                "value": "premium"
              },
              {
                "label": "Student (proof required)",
                "value": "student"
              },
              {
                "label": "Concession (proof required)",
                "value": "concession"
              },
              {
                "label": "Life",
                "value": "life"
              }
            ],
            "placeholder": "Select a membership",
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
            "helpText": "Please confirm all items to proceed.",
            "label": "Eligibility confirmations",
            "options": [
              {
                "label": "I am 18 years of age or older",
                "value": "age_18_plus"
              },
              {
                "label": "I am an Australian resident",
                "value": "australian_resident"
              },
              {
                "label": "I agree to abide by the membership code of conduct",
                "value": "agree_code_of_conduct"
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
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 776
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
                "label": "Search engine",
                "value": "search"
              },
              {
                "label": "Event or meetup",
                "value": "event"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a source",
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
            "y": 776
          },
          "props": {
            "height": 110,
            "label": "Referral details (if Other)",
            "placeholder": "Please specify who or where",
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
            "y": 910
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 brief summary of your interest or involvement.",
            "label": "Tell us about your interest",
            "placeholder": "Why do you want to join?",
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
          "id": "terms-12",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 120,
            "helpText": "I have read and accept the event terms and the privacy handling of my application.",
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
            "y": 1358
          },
          "props": {
            "height": 72,
            "label": "Submit application",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 43662,
  "failure_class": "none",
  "input_tokens": 3423,
  "output_tokens": 3773,
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
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Thanks for visiting our stand. Please record the visitor's details and interests so our team can follow up.",
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
          "id": "text-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Visitor's employer or company name",
            "label": "Company",
            "placeholder": "Organisation",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Australian phone number (optional)",
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
          "id": "email-6",
          "position": {
            "x": 384,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Best email for follow-up",
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
            "helpText": "Select all that apply",
            "label": "Interest areas",
            "options": [
              {
                "label": "Product demo",
                "value": "demo"
              },
              {
                "label": "Pricing & licensing",
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
          "id": "dropdown-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "When do they expect to purchase or decide?",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediately (0\u201330 days)",
                "value": "0-30"
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
                "label": "Not currently looking",
                "value": "not_looking"
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
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "Include any product preferences or agreed actions",
            "label": "Notes / meeting summary",
            "placeholder": "Key points, action items, next steps",
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
            "y": 1080
          },
          "props": {
            "height": 120,
            "label": "Consent to be contacted",
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
            "y": 1224
          },
          "props": {
            "height": 72,
            "label": "Save lead",
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
      "title": "Trade show booth visit \u2014 Lead capture"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 40140,
  "failure_class": "none",
  "input_tokens": 3495,
  "output_tokens": 3506,
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
            "placeholder": "e.g. Jane",
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
          "id": "phone-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Local Australian number (optional)",
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
            "helpText": "Best address for follow-up",
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
            "label": "Organisation",
            "placeholder": "Company or organisation",
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
            "x": 384,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "What the visitor was most interested in",
            "label": "Interest area",
            "options": [
              {
                "label": "Product demo",
                "value": "product_demo"
              },
              {
                "label": "Pricing & quote",
                "value": "pricing"
              },
              {
                "label": "Technical integration",
                "value": "integration"
              },
              {
                "label": "Partnership",
                "value": "partnership"
              },
              {
                "label": "Careers / hiring",
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
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "When they expect to purchase or decide",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate / within 30 days",
                "value": "0-30_days"
              },
              {
                "label": "1\u20133 months",
                "value": "1-3_months"
              },
              {
                "label": "3\u20136 months",
                "value": "3-6_months"
              },
              {
                "label": "6\u201312 months",
                "value": "6-12_months"
              },
              {
                "label": "12+ months / undecided",
                "value": "12_plus"
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
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 200,
            "helpText": "Include actions and who will follow up",
            "label": "Notes / qualifying info",
            "placeholder": "Key points from the conversation, next steps, demo requests, competitor mentions",
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
            "y": 874
          },
          "props": {
            "height": 120,
            "helpText": "I agree to be contacted about this enquiry and receive event-related updates.",
            "label": "Consent to follow up",
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
            "y": 1018
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 54366,
  "failure_class": "none",
  "input_tokens": 3505,
  "output_tokens": 4926,
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
  "formId": "trade-show-booth-lead-log",
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
            "placeholder": "Company or organisation",
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
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include country code, e.g. [SCRUBBED_PHONE]",
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
          "id": "email-5",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Local postcode",
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
            "y": 560
          },
          "props": {
            "height": 110,
            "label": "Interest area",
            "options": [
              {
                "label": "Product demos",
                "value": "product-demos"
              },
              {
                "label": "Pricing & quotes",
                "value": "pricing-quotes"
              },
              {
                "label": "Technical details",
                "value": "technical-details"
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
            "placeholder": "Select an option",
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
            "y": 560
          },
          "props": {
            "height": 110,
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate (within 30 days)",
                "value": "immediate"
              },
              {
                "label": "Soon (1\u20133 months)",
                "value": "1-3-months"
              },
              {
                "label": "This year (3\u201312 months)",
                "value": "3-12-months"
              },
              {
                "label": "Not sure / Just browsing",
                "value": "not-sure"
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
            "y": 694
          },
          "props": {
            "height": 200,
            "label": "Notes",
            "placeholder": "Key interests, questions, next steps",
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
            "y": 998
          },
          "props": {
            "height": 120,
            "helpText": "I agree to be contacted about this enquiry and accept the event terms.",
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
            "y": 1142
          },
          "props": {
            "height": 72,
            "label": "Save lead",
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
      "title": "Trade show booth visit log"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 30253,
  "failure_class": "none",
  "input_tokens": 3415,
  "output_tokens": 2771,
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
            "helpText": "Optional \u2014 helps us personalise emails.",
            "label": "First name",
            "placeholder": "e.g. Jamie",
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
            "helpText": "We'll only use this to send the newsletter and related updates.",
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
            "helpText": "Tick all that apply",
            "label": "Content interests",
            "options": [
              {
                "label": "Product updates",
                "value": "product_updates"
              },
              {
                "label": "Events & webinars",
                "value": "events"
              },
              {
                "label": "Promotions & offers",
                "value": "promotions"
              },
              {
                "label": "Blog posts & news",
                "value": "blog_posts"
              },
              {
                "label": "Research & insights",
                "value": "research"
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
            "helpText": "Choose the cadence you prefer.",
            "label": "How often would you like to hear from us?",
            "options": [
              {
                "label": "Weekly",
                "value": "weekly"
              },
              {
                "label": "Monthly",
                "value": "monthly"
              },
              {
                "label": "Quarterly",
                "value": "quarterly"
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
            "helpText": "By subscribing you agree to receive electronic communications.",
            "label": "I consent to receive newsletters and marketing communications by email. I understand I can unsubscribe at any time and that my personal information will be handled in accordance with the privacy statement.",
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
      "title": "Newsletter subscription"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 42627,
  "failure_class": "none",
  "input_tokens": 3487,
  "output_tokens": 4025,
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
  "formId": "sydney-newsletter-subscription",
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
            "label": "Subscribe for updates on events, news and special offers across Sydney.",
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
            "placeholder": "e.g. Aisha",
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
            "placeholder": "e.g. Lee",
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
            "helpText": "We'll send updates about Sydney events to this address.",
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
          "id": "checkbox-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Select the topics you want to hear about.",
            "label": "Content interests",
            "options": [
              {
                "label": "Local Sydney events",
                "value": "sydney_events"
              },
              {
                "label": "Industry news",
                "value": "industry_news"
              },
              {
                "label": "Workshops & training",
                "value": "workshops"
              },
              {
                "label": "Special offers & promotions",
                "value": "offers"
              },
              {
                "label": "Volunteer & community opportunities",
                "value": "volunteer"
              }
            ],
            "tabOrder": 5,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 508
          },
          "props": {
            "height": 120,
            "helpText": "How often would you like to receive emails?",
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
              },
              {
                "label": "Occasional (event-driven)",
                "value": "occasional"
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
          "id": "terms-7",
          "position": {
            "x": 40,
            "y": 652
          },
          "props": {
            "height": 120,
            "helpText": "You can withdraw consent at any time. Privacy and communications are subject to the event terms.",
            "label": "I agree to receive newsletters and accept the event terms",
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
      "title": "Sydney Events Newsletter Subscription"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 50220,
  "failure_class": "none",
  "input_tokens": 3497,
  "output_tokens": 4786,
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
          "id": "text-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 helps us personalise emails",
            "label": "Full name",
            "placeholder": "e.g. [SCRUBBED_NAME]",
            "tabOrder": 1,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-2",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "We'll send newsletters to this address",
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
          "id": "phone-3",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 include country code for best delivery",
            "label": "Phone",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "text-4",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Optional",
            "label": "Postcode",
            "placeholder": "Postcode",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "checkbox-5",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Select topics you'd like to receive",
            "label": "Content interests",
            "options": [
              {
                "label": "News",
                "value": "news"
              },
              {
                "label": "Events",
                "value": "events"
              },
              {
                "label": "Promotions",
                "value": "promotions"
              },
              {
                "label": "Product updates",
                "value": "product_updates"
              },
              {
                "label": "Research & insights",
                "value": "research_insights"
              }
            ],
            "tabOrder": 5,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "How often would you like to hear from us?",
            "label": "Frequency preference",
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
          "id": "terms-7",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive marketing emails and accept the event terms.",
            "label": "Marketing consent",
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
            "y": 858
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
      "title": "Newsletter subscription"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 46129,
  "failure_class": "none",
  "input_tokens": 3422,
  "output_tokens": 4351,
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
    "height": 1496,
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
            "label": "Your pledge helps fund our programs and supports our community work. All donations are greatly appreciated.",
            "options": [],
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
            "options": [],
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
            "options": [],
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
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 useful for SMS confirmations or urgent contact.",
            "label": "Mobile phone",
            "options": [],
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
          "id": "email-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We'll send your tax receipt and donation confirmation here.",
            "label": "Email address",
            "options": [],
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode if you want a printed receipt.",
            "label": "Postal address",
            "options": [],
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
            "helpText": "Choose an amount or select Custom to enter your own pledge (AUD).",
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
                "label": "$250",
                "value": "250"
              },
              {
                "label": "Custom amount",
                "value": "custom"
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
          "id": "number-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter a whole dollar amount if you selected Custom.",
            "label": "Custom amount (AUD)",
            "options": [],
            "placeholder": "Enter amount in dollars",
            "tabOrder": 8,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "number"
        },
        {
          "id": "radio-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "Select whether this pledge is one-off or recurring.",
            "label": "Donation type",
            "options": [
              {
                "label": "One-off",
                "value": "one_off"
              },
              {
                "label": "Monthly (recurring)",
                "value": "monthly"
              },
              {
                "label": "Annually (recurring)",
                "value": "annual"
              }
            ],
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "If the receipt should be issued to a different name or organisation.",
            "label": "Receipt name (if different)",
            "options": [],
            "placeholder": "Name for tax receipt",
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
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive a printed receipt at your postal address.",
            "label": "Printed receipt",
            "options": [
              {
                "label": "Please send a printed receipt to my postal address",
                "value": "printed_receipt"
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
            "y": 1064
          },
          "props": {
            "height": 120,
            "helpText": "Tick how you'd like to hear about our campaigns and events. You can unsubscribe at any time.",
            "label": "Campaign updates",
            "options": [
              {
                "label": "Email updates",
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
            "y": 1208
          },
          "props": {
            "height": 120,
            "helpText": "By pledging you agree to our terms and to receive your receipt. See our privacy practices for how we handle your personal information.",
            "label": "I agree to the charity's donation terms, privacy policy and consent to be contacted for donation and campaign purposes.",
            "options": [],
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
            "y": 1352
          },
          "props": {
            "height": 72,
            "label": "Pledge donation",
            "options": [],
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
      "title": "Charity donation pledge"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 60432,
  "failure_class": "none",
  "input_tokens": 3494,
  "output_tokens": 5668,
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
    "height": 1656,
    "width": 960
  },
  "formId": "sydney-charity-donation-pledge",
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
            "label": "Complete this form to pledge your donation. We'll contact you about receipts and delivery of any updates you opt into.",
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
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Useful for urgent queries about your pledge.",
            "label": "Phone (optional)",
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
          "id": "email-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We'll send your receipt and confirmation to this address.",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode if you require a postal tax receipt.",
            "label": "Postal address (for receipt)",
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
            "helpText": "Pick a suggested amount or enter your own below.",
            "label": "Suggested donation",
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
                "label": "$250",
                "value": "250"
              }
            ],
            "placeholder": "Choose a suggested amount",
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
            "helpText": "Enter whole dollars. Minimum $1.",
            "label": "Donation amount (AUD)",
            "placeholder": "Enter amount in AUD",
            "tabOrder": 8,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "number"
        },
        {
          "id": "radio-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Choose one-off or recurring pledge.",
            "label": "Donation type",
            "options": [
              {
                "label": "One-off",
                "value": "one_off"
              },
              {
                "label": "Recurring",
                "value": "recurring"
              }
            ],
            "tabOrder": 9,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "dropdown-10",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Only needed if you selected Recurring.",
            "label": "If recurring, choose frequency",
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
                "label": "Yearly",
                "value": "yearly"
              }
            ],
            "placeholder": "Select frequency",
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
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Select how you'd like to receive an official tax receipt.",
            "label": "Tax receipt preference",
            "options": [
              {
                "label": "Email receipt (to address above)",
                "value": "email_receipt"
              },
              {
                "label": "Postal receipt (use postal address above)",
                "value": "postal_receipt"
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
            "y": 920
          },
          "props": {
            "height": 120,
            "helpText": "We will only send updates where you've opted in. You can change preferences anytime.",
            "label": "Campaign updates",
            "options": [
              {
                "label": "Email updates",
                "value": "updates_email"
              },
              {
                "label": "SMS updates",
                "value": "updates_sms"
              },
              {
                "label": "Postal updates",
                "value": "updates_post"
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
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 1064
          },
          "props": {
            "height": 200,
            "helpText": "We'll include this with your pledge where possible.",
            "label": "Message or dedication (optional)",
            "placeholder": "Add a short message or dedication to include with your pledge",
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
            "y": 1368
          },
          "props": {
            "height": 120,
            "helpText": "By pledging you accept our event terms and privacy practices.",
            "label": "Terms and privacy",
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
            "y": 1512
          },
          "props": {
            "height": 72,
            "label": "Pledge donation",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 46955,
  "failure_class": "none",
  "input_tokens": 3504,
  "output_tokens": 4316,
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
    "height": 1674,
    "width": 960
  },
  "formId": "charity-donation-pledge",
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
            "label": "Thank you for supporting our cause. Please tell us who you are, how much you'd like to pledge and how we should send your receipt.",
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
            "helpText": "We will send your donation receipt here.",
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
            "helpText": "Provide a number we can contact you on if needed.",
            "label": "Phone number",
            "placeholder": "e.g. [SCRUBBED_PHONE]",
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
            "helpText": "Include suburb, state and postcode.",
            "label": "Postal address",
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
            "helpText": "4-digit Australian postcode",
            "label": "Postcode",
            "placeholder": "e.g. 3000",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Choose a suggested amount or enter your own.",
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
          "id": "number-9",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Minimum $1",
            "label": "Other amount (AUD)",
            "placeholder": "Enter amount in AUD",
            "tabOrder": 9,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "number"
        },
        {
          "id": "radio-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "label": "Donation frequency",
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
                "label": "Annually",
                "value": "annually"
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
          "id": "radio-11",
          "position": {
            "x": 424,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Select how you'd like to receive your tax receipt.",
            "label": "Send receipt via",
            "options": [
              {
                "label": "Email",
                "value": "email"
              },
              {
                "label": "Post",
                "value": "post"
              },
              {
                "label": "No receipt required",
                "value": "none"
              }
            ],
            "tabOrder": 11,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 120,
            "helpText": "Tick if the receipt should be issued in an organisation's name and provide the name below.",
            "label": "Receipt details",
            "options": [
              {
                "label": "Issue receipt in an organisation's name",
                "value": "org_receipt"
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
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1064
          },
          "props": {
            "height": 110,
            "label": "Organisation name for receipt",
            "placeholder": "Organisation name (leave blank if personal)",
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
          "id": "checkbox-14",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive campaign updates and news.",
            "label": "Campaign updates consent",
            "options": [
              {
                "label": "Yes \u2014 email me campaign updates",
                "value": "updates_email"
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
            "y": 1342
          },
          "props": {
            "height": 120,
            "helpText": "By pledging a donation you accept the event terms and privacy policy (see event terms).",
            "label": "I agree to the event terms and privacy policy",
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
          "id": "divider-16",
          "position": {
            "x": 40,
            "y": 1486
          },
          "props": {
            "height": 20,
            "tabOrder": 16,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "submit-button-17",
          "position": {
            "x": 40,
            "y": 1530
          },
          "props": {
            "height": 72,
            "label": "Pledge donation",
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
      "title": "Charity donation pledge"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
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
  "component_count": 12,
  "duration_ms": 41152,
  "failure_class": "none",
  "input_tokens": 3418,
  "output_tokens": 3721,
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
  "formId": "intl-online-event-registration",
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
            "label": "Complete your details. We\u2019ll send joining instructions and any session updates to the email you provide.",
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
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Local or international number \u2014 include country code.",
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
          "id": "email-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send event access details and updates to this address.",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Country of residence or where you\u2019ll join from.",
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
                "label": "Germany",
                "value": "DE"
              },
              {
                "label": "France",
                "value": "FR"
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
            "helpText": "Choose the timezone where you\u2019ll watch the event.",
            "label": "Timezone",
            "options": [
              {
                "label": "(UTC+10:00) Australia/Sydney (AEST)",
                "value": "UTC+10"
              },
              {
                "label": "(UTC+11:00) Pacific/Auckland",
                "value": "UTC+11"
              },
              {
                "label": "(UTC+09:00) Asia/Tokyo",
                "value": "UTC+9"
              },
              {
                "label": "(UTC+08:00) Asia/Shanghai, Asia/Singapore",
                "value": "UTC+8"
              },
              {
                "label": "(UTC+05:30) Asia/Kolkata",
                "value": "UTC+5:30"
              },
              {
                "label": "(UTC+01:00) Europe/Berlin (Central European Time)",
                "value": "UTC+1"
              },
              {
                "label": "(UTC+00:00) Europe/London (GMT)",
                "value": "UTC+0"
              },
              {
                "label": "(UTC-05:00) America/New_York (Eastern Time)",
                "value": "UTC-5"
              },
              {
                "label": "(UTC-08:00) America/Los_Angeles (Pacific Time)",
                "value": "UTC-8"
              },
              {
                "label": "Other / Unsure",
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
            "helpText": "Select all that apply.",
            "label": "Which sessions are you interested in?",
            "options": [
              {
                "label": "Opening keynote \u2014 industry trends",
                "value": "keynote"
              },
              {
                "label": "Workshop: Hands-on demo",
                "value": "workshop"
              },
              {
                "label": "Panel discussion & Q&A",
                "value": "panel"
              },
              {
                "label": "Networking breakout rooms",
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
            "helpText": "We\u2019ll do our best to accommodate requests.",
            "label": "Accessibility or other requirements (optional)",
            "placeholder": "Let us know if you need accessibility support or other assistance.",
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
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "By registering you consent to use of your information for event administration and communications. You can opt out of marketing messages at any time.",
            "label": "I agree to the event terms and privacy policy and consent to receive event-related emails and updates.",
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
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you'd like occasional news about future events (optional).",
            "label": "Marketing and updates",
            "options": [
              {
                "label": "Yes \u2014 send me event news and offers",
                "value": "optin_marketing"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 52281,
  "failure_class": "none",
  "input_tokens": 3490,
  "output_tokens": 4777,
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
            "label": "Join us online for sessions, workshops and networking. Please provide your details below so we can reserve your place and share event access information.",
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
            "helpText": "We will send event access details and updates to this address.",
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
            "helpText": "Include country code for international numbers. We may contact you about access or schedule changes.",
            "label": "Phone number",
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
            "helpText": "Country where you are based",
            "label": "Country",
            "options": [
              {
                "label": "Australia",
                "value": "AU"
              },
              {
                "label": "New Zealand",
                "value": "NZ"
              },
              {
                "label": "United Kingdom",
                "value": "GB"
              },
              {
                "label": "United States",
                "value": "US"
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
                "label": "Canada",
                "value": "CA"
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
            "helpText": "Select the timezone you normally use. Sydney (Australia/Sydney) is recommended for event times.",
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
                "label": "Europe/London (BST/GMT)",
                "value": "Europe/London"
              },
              {
                "label": "America/New_York (EDT/EST)",
                "value": "America/New_York"
              },
              {
                "label": "Asia/Kolkata (IST)",
                "value": "Asia/Kolkata"
              },
              {
                "label": "Asia/Shanghai (CST)",
                "value": "Asia/Shanghai"
              },
              {
                "label": "Other",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select timezone",
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
            "helpText": "Select all that apply",
            "label": "Which sessions are you interested in?",
            "options": [
              {
                "label": "Keynote: The future of AI",
                "value": "keynote_ai"
              },
              {
                "label": "Workshop: Hands-on lab",
                "value": "workshop_lab"
              },
              {
                "label": "Panel: Industry leaders",
                "value": "panel_industry"
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
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "label": "Organisation (optional)",
            "placeholder": "Company or institution",
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
          "id": "terms-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "By registering you consent to event communications and the organiser's privacy practices.",
            "label": "I agree to the event terms and privacy policy.",
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
            "y": 920
          },
          "props": {
            "height": 72,
            "label": "Register",
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
      "title": "Sydney Online Event Registration"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p11-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p11-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p11-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p11-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p11-au-adversarial-r1",
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
  "component_count": 11,
  "duration_ms": 54818,
  "failure_class": "none",
  "input_tokens": 3500,
  "output_tokens": 4853,
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
  "formId": "intl-event-registration",
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
            "helpText": "We'll send your registration confirmation to this address.",
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
            "helpText": "Include country code. Example shown uses +1 country code.",
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
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Select the country where you are based.",
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
            "helpText": "Choose your primary timezone (e.g. Australia/Sydney, America/New_York).",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT)",
                "value": "Australia/Sydney"
              },
              {
                "label": "Australia/Perth (AWST)",
                "value": "Australia/Perth"
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
                "label": "UTC",
                "value": "UTC"
              },
              {
                "label": "Other",
                "value": "OTHER"
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
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Enter your ZIP code (US-style) or your local postal code.",
            "label": "ZIP code",
            "placeholder": "ZIP or postal code",
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
            "y": 560
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply.",
            "label": "Which sessions are you interested in?",
            "options": [
              {
                "label": "Keynote",
                "value": "keynote"
              },
              {
                "label": "Workshop A: Product Deep-dive",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B: Hands-on Lab",
                "value": "workshop_b"
              },
              {
                "label": "Networking session",
                "value": "networking"
              },
              {
                "label": "Other (please specify in notes)",
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
            "y": 704
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about any special requirements or questions.",
            "label": "Additional notes",
            "placeholder": "Any dietary requirements, accessibility needs or session preferences",
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
            "y": 1008
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and to receive event updates and important information about this event.",
            "label": "Agree to event terms and updates",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 44754,
  "failure_class": "none",
  "input_tokens": 3420,
  "output_tokens": 3862,
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
            "helpText": "The organiser will collect and use your personal information for event administration, ticketing and updates. See the privacy notice below for more detail.",
            "label": "How we use your information",
            "options": [],
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
            "options": [],
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
            "options": [],
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
            "helpText": "We will send your ticket and important event updates to this address.",
            "label": "Email address",
            "options": [],
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
            "helpText": "Optional \u2014 used for urgent event communications (SMS or call).",
            "label": "Phone",
            "options": [],
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
            "helpText": "Include suburb, state and postcode if relevant (optional).",
            "label": "Postal address",
            "options": [],
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
          "id": "date-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Date of attendance",
            "options": [],
            "placeholder": "Select a date",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "number-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "How many people will attend on this booking?",
            "label": "Number of tickets",
            "options": [],
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
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 200,
            "helpText": "Please include any medical or accessibility information the organiser should be aware of.",
            "label": "Additional requirements",
            "options": [],
            "placeholder": "Dietary needs, accessibility requirements or other information we should know",
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
            "helpText": "Tick if you agree to receive event updates and occasional marketing from the organiser by email.",
            "label": "Marketing preferences",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive event updates and marketing",
                "value": "marketing_opt_in"
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
            "helpText": "I acknowledge that the organiser will collect and process my personal information for event administration, ticketing and communications. I understand the lawful basis for processing is my consent and necessary administration. I can withdraw consent and request access to, or correction of, my personal information. By checking below I give my consent to this processing in accordance with the organiser's privacy notice.",
            "label": "Privacy & data handling \u2014 consent and lawful basis (required)",
            "options": [],
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
            "options": [],
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "privacy_law_without_au_anchor",
    "description": "GDPR/CCPA-only privacy wording where AU privacy wording is expected",
    "matched_text": "GDPR",
    "prompt_id": "p12-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  }
]
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 77631,
  "failure_class": "none",
  "input_tokens": 8535,
  "output_tokens": 6929,
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
    "height": 1762,
    "width": 960
  },
  "formId": "eu-event-registration-sydney",
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
            "label": "This event is associated with Sydney. The organiser will process your personal data to manage registration and attendance. Please review the data handling notice and provide consent where requested.",
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
          "id": "divider-2",
          "position": {
            "x": 40,
            "y": 96
          },
          "props": {
            "height": 20,
            "tabOrder": 2,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "first-name-3",
          "position": {
            "x": 40,
            "y": 140
          },
          "props": {
            "height": 110,
            "label": "First name",
            "placeholder": "Given name",
            "tabOrder": 3,
            "width": "260px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "first-name"
        },
        {
          "id": "text-4",
          "position": {
            "x": 424,
            "y": 140
          },
          "props": {
            "height": 110,
            "label": "Last name",
            "placeholder": "Family name",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "email-5",
          "position": {
            "x": 40,
            "y": 274
          },
          "props": {
            "height": 110,
            "helpText": "We will use this to send your booking confirmation and event updates.",
            "label": "Email address",
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
            "y": 274
          },
          "props": {
            "height": 110,
            "helpText": "Include country code for international attendees.",
            "label": "Phone (mobile preferred)",
            "placeholder": "+61 4XX XXX XXX",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 408
          },
          "props": {
            "height": 110,
            "label": "Organisation",
            "placeholder": "Company or organisation name",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "text-8",
          "position": {
            "x": 424,
            "y": 408
          },
          "props": {
            "height": 110,
            "label": "Job title",
            "placeholder": "e.g. Marketing Manager",
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
          "id": "address-9",
          "position": {
            "x": 40,
            "y": 542
          },
          "props": {
            "height": 110,
            "helpText": "Provide suburb, state and postcode for postal communications where needed.",
            "label": "Postal address",
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
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 676
          },
          "props": {
            "height": 110,
            "label": "Attendance type",
            "options": [
              {
                "label": "In-person (Sydney venue)",
                "value": "in_person"
              },
              {
                "label": "Virtual / online",
                "value": "virtual"
              },
              {
                "label": "Undecided / Other",
                "value": "other"
              }
            ],
            "placeholder": "Select attendance type",
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
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 810
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 tell us about allergies or access needs.",
            "label": "Dietary requirements or accessibility needs",
            "placeholder": "Tell us any dietary needs or accessibility requirements",
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
          "id": "radio-12",
          "position": {
            "x": 40,
            "y": 1114
          },
          "props": {
            "height": 120,
            "helpText": "Please acknowledge the lawful basis the organiser will rely on to process your registration data.",
            "label": "Lawful basis for processing (acknowledgement)",
            "options": [
              {
                "label": "Consent \u2014 I give explicit consent for processing my personal data for this event",
                "value": "consent"
              },
              {
                "label": "Contractual necessity \u2014 processing is necessary to fulfil registration and attendance",
                "value": "contract"
              },
              {
                "label": "Legitimate interests \u2014 organiser's legitimate interests in running the event",
                "value": "legitimate_interests"
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
          "id": "checkbox-13",
          "position": {
            "x": 40,
            "y": 1258
          },
          "props": {
            "height": 120,
            "helpText": "Select which communications you agree to receive. You can opt out at any time.",
            "label": "Marketing & updates preferences",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive event updates and optional marketing by email",
                "value": "marketing_email"
              }
            ],
            "tabOrder": 13,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1402
          },
          "props": {
            "height": 120,
            "helpText": "You must accept the organiser's data handling terms to register. The organiser is responsible for compliance with GDPR for EU attendees.",
            "label": "GDPR consent and data handling notice (required)",
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
          "id": "paragraph-15",
          "position": {
            "x": 40,
            "y": 1546
          },
          "props": {
            "height": 48,
            "label": "Data handling summary: Your personal data will be used to manage your registration, to provide event communications, and to meet legal and safety obligations. Where required, the organiser relies on the lawful basis you acknowledged above. For full details see the event terms.",
            "tabOrder": 15,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 1618
          },
          "props": {
            "height": 72,
            "label": "Complete registration",
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
      "title": "EU Event Registration \u2014 Sydney"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p12-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p12-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p12-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p12-au-adversarial-r1",
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
  "duration_ms": 63413,
  "failure_class": "none",
  "input_tokens": 3502,
  "output_tokens": 5681,
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
  "formId": "eu-event-registration",
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
            "helpText": "We collect and use your personal information to manage your registration, provide event updates and comply with legal obligations. See the event terms for full details.",
            "label": "Data handling summary",
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
            "helpText": "We will send registration confirmations and event updates to this address.",
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
            "helpText": "Include country code. Example format shown with +1 prefix per request.",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
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
            "label": "Postal address",
            "placeholder": "Street address",
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
            "helpText": "Provide ZIP code where applicable (included per request).",
            "label": "ZIP code",
            "placeholder": "12345",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Choose the basis we rely on to process your personal data for this event.",
            "label": "Lawful basis for processing personal data",
            "options": [
              {
                "label": "I consent to processing for event administration and communications",
                "value": "consent"
              },
              {
                "label": "Processing is necessary for event administration (legitimate interest)",
                "value": "legitimate_interest"
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
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "By registering you acknowledge the privacy notice and agree to the event terms linked below. This consent covers the uses described in the data handling summary.",
            "label": "Privacy notice & event terms",
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
            "y": 920
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 34763,
  "failure_class": "none",
  "input_tokens": 3422,
  "output_tokens": 3237,
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
  "formId": "au-onboarding-interest",
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
            "helpText": "We'll contact you at this address about your interest.",
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
            "helpText": "Include area code if relevant; Australian format preferred.",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode.",
            "label": "Postal address",
            "placeholder": "Street address, suburb, state, postcode",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Choose the role you'd like to be considered for.",
            "label": "Role of interest",
            "options": [
              {
                "label": "Volunteer",
                "value": "volunteer"
              },
              {
                "label": "Team member",
                "value": "team_member"
              },
              {
                "label": "Coordinator",
                "value": "coordinator"
              },
              {
                "label": "Manager",
                "value": "manager"
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
          "id": "text-7",
          "position": {
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Other role (if selected)",
            "placeholder": "If other, specify the role",
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
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 up to 1,000 characters.",
            "label": "Tell us why you're interested",
            "placeholder": "A short note about your interest, experience or availability",
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
            "helpText": "Select any you agree to.",
            "label": "Contact preferences",
            "options": [
              {
                "label": "I agree to be contacted about onboarding and future opportunities (email or phone).",
                "value": "consent_contact"
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
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1008
          },
          "props": {
            "height": 72,
            "label": "Send interest",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 35664,
  "failure_class": "none",
  "input_tokens": 3494,
  "output_tokens": 3277,
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
  "formId": "sydney-onboarding-interest-au",
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
            "label": "Complete this short form and we'll be in touch with next steps for onboarding and event details.",
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
            "helpText": "We'll use this to contact you about onboarding and event updates.",
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
            "helpText": "Local Australian number preferred for SMS updates.",
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
            "helpText": "Choose the role you're interested in for the Sydney event.",
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
                "label": "Speaker",
                "value": "speaker"
              },
              {
                "label": "Sponsor / Partner",
                "value": "sponsor"
              },
              {
                "label": "Media / Press",
                "value": "media"
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
          "id": "text-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "If applicable, the organisation you represent.",
            "label": "Organisation (optional)",
            "placeholder": "Company or organisation",
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
          "id": "address-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Provide suburb, state and postcode for local arrangements.",
            "label": "Suburb, state & postcode",
            "placeholder": "Suburb, state, postcode",
            "tabOrder": 8,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 include anything that will help with onboarding.",
            "label": "Any other details or questions",
            "placeholder": "Tell us about availability, access requirements or anything else we should know.",
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
            "y": 936
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and to receive event-related messages.",
            "label": "Terms and privacy",
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
            "y": 1080
          },
          "props": {
            "height": 72,
            "label": "Express interest",
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
      "title": "Onboarding interest \u2014 Sydney"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 55263,
  "failure_class": "none",
  "input_tokens": 3504,
  "output_tokens": 4539,
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
  "formId": "onboarding-interest-form",
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
            "label": "Tell us a little about yourself and your interest in onboarding with us.",
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
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country code",
            "label": "Phone",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "email-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will use this to contact you about onboarding",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Role",
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
                "label": "Speaker",
                "value": "speaker"
              },
              {
                "label": "Sponsor",
                "value": "sponsor"
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
          "id": "text-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "4-digit Australian postcode",
            "label": "Postcode",
            "placeholder": "e.g. 2000",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 200,
            "label": "Tell us about your interest",
            "placeholder": "Share anything relevant \u2014 experience, availability or goals",
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
            "y": 802
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to receive event news and onboarding updates",
            "label": "Event updates",
            "options": [
              {
                "label": "Yes, send me event updates",
                "value": "subscribe_updates"
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
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and privacy policy.",
            "label": "Terms and privacy",
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
            "y": 1090
          },
          "props": {
            "height": 72,
            "label": "Register interest",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 51424,
  "failure_class": "none",
  "input_tokens": 3419,
  "output_tokens": 4205,
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
    "height": 1770,
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
            "label": "Before participating, please provide your details, relevant health information and an emergency contact. Read the waiver and consent below and initial to confirm your answers.",
            "options": [],
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
            "label": "Given name",
            "options": [],
            "placeholder": "As shown on your ID",
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
            "label": "Family name",
            "options": [],
            "placeholder": "Surname",
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
          "id": "date-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Use Australian date format (DD/MM/YYYY).",
            "label": "Date of birth",
            "options": [],
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Address",
            "options": [],
            "placeholder": "Street address, suburb, state, postcode",
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
          "id": "email-6",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "We may use this to send event updates and safety information.",
            "label": "Email",
            "options": [],
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
          "id": "phone-7",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Australian phone number for event communications and emergencies.",
            "label": "Mobile phone",
            "options": [],
            "placeholder": "e.g. [SCRUBBED_PHONE]",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Tick any that apply, or select 'None of the above'.",
            "label": "Medical conditions or restrictions (tick any that apply)",
            "options": [
              {
                "label": "Asthma",
                "value": "asthma"
              },
              {
                "label": "Heart condition",
                "value": "heart_condition"
              },
              {
                "label": "Diabetes",
                "value": "diabetes"
              },
              {
                "label": "Severe allergies",
                "value": "allergies"
              },
              {
                "label": "Pregnant",
                "value": "pregnant"
              },
              {
                "label": "Mobility impairment",
                "value": "mobility_impairment"
              },
              {
                "label": "None of the above",
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
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "Include medication names, dosage and any emergency instructions.",
            "label": "If any condition applies, please provide details (medication, triggers, emergency care needed)",
            "options": [],
            "placeholder": "List medications, recent injuries, allergies, or anything else organisers should know.",
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
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 1080
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "options": [],
            "placeholder": "Full name",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-11",
          "position": {
            "x": 424,
            "y": 1080
          },
          "props": {
            "height": 110,
            "label": "Emergency contact phone",
            "options": [],
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
          "id": "dropdown-12",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "options": [
              {
                "label": "Parent / Guardian",
                "value": "parent_guardian"
              },
              {
                "label": "Partner",
                "value": "partner"
              },
              {
                "label": "Sibling",
                "value": "sibling"
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
            "tabOrder": 12,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1348
          },
          "props": {
            "height": 110,
            "helpText": "Typing your initials confirms that information is correct and that you accept the waiver.",
            "label": "Initials (type your initials to confirm accuracy)",
            "options": [],
            "placeholder": "Your initials",
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
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1482
          },
          "props": {
            "height": 120,
            "helpText": "By checking this box you consent to electronic communications and the use of your information for event safety and emergency purposes.",
            "label": "I confirm that the information I have provided is accurate. I understand the risks associated with participation, consent to the collection and use of my personal and health information for safety, emergency contact and event management purposes, and agree to follow organiser instructions.",
            "options": [],
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
            "y": 1626
          },
          "props": {
            "height": 72,
            "label": "I agree & Submit",
            "options": [],
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
      "title": "Event Waiver & Health Information"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 53367,
  "failure_class": "none",
  "input_tokens": 3491,
  "output_tokens": 4338,
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
    "height": 1636,
    "width": 960
  },
  "formId": "sydney-event-waiver",
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
            "label": "This form collects participant details, medical information, and emergency contact details. By submitting, you confirm the information is accurate and you agree to the event terms and waiver.",
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
            "helpText": "As shown on your ID",
            "label": "Given name",
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
            "label": "Surname",
            "placeholder": "Surname",
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
            "helpText": "Enter day, month and year",
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
          "id": "phone-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "For event updates and emergency contact",
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
            "helpText": "We\u2019ll send confirmation and event updates",
            "label": "Email address",
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
          "id": "address-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Include suburb, state and postcode",
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
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 200,
            "helpText": "Provide details that may affect your participation or emergency treatment",
            "label": "Relevant health information (conditions, allergies, medications)",
            "placeholder": "List any medical conditions, allergies, medications, or accessibility needs the organisers should know about",
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
            "y": 936
          },
          "props": {
            "height": 120,
            "helpText": "Tick and give details in the health information field above",
            "label": "Special assistance required",
            "options": [
              {
                "label": "I require special assistance or reasonable adjustments",
                "value": "assistance_required"
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
            "y": 1080
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Full name",
            "placeholder": "Full name",
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
            "x": 384,
            "y": 1080
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "placeholder": "e.g. Partner, Parent, Friend",
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
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 110,
            "helpText": "Primary number to call in an emergency",
            "label": "Emergency contact \u2014 Phone",
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
          "id": "email-13",
          "position": {
            "x": 384,
            "y": 1214
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Email (optional)",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 13,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1348
          },
          "props": {
            "height": 120,
            "helpText": "Please review the event terms before consenting. The terms include the event waiver and consent to necessary emergency medical treatment where appropriate.",
            "label": "Event terms, waiver and emergency medical consent",
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
            "y": 1492
          },
          "props": {
            "height": 72,
            "label": "Submit Waiver",
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
      "title": "Sydney Event Waiver & Health Form"
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 63905,
  "failure_class": "none",
  "input_tokens": 3501,
  "output_tokens": 5287,
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
    "height": 2110,
    "width": 960
  },
  "formId": "au-waiver-health-form",
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
            "label": "This form collects personal and health information needed to manage risks and respond to emergencies. By signing the waiver you acknowledge the risks and agree to the event terms.",
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
          "id": "date-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Enter your date of birth.",
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
            "helpText": "We will use this to send event updates.",
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
            "helpText": "Include country code (e.g. +61).",
            "label": "Mobile phone",
            "placeholder": "+61 4XX XXX XXX",
            "tabOrder": 6,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
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
            "placeholder": "Street and number",
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
          "id": "text-9",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "label": "State / Territory",
            "placeholder": "State or territory",
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
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 110,
            "helpText": "4-digit Australian postcode.",
            "label": "Postcode",
            "placeholder": "e.g. 3000",
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
          "id": "checkbox-11",
          "position": {
            "x": 40,
            "y": 900
          },
          "props": {
            "height": 120,
            "helpText": "Tick all that apply.",
            "label": "Relevant health conditions (tick any that apply)",
            "options": [
              {
                "label": "Asthma",
                "value": "asthma"
              },
              {
                "label": "Allergies",
                "value": "allergies"
              },
              {
                "label": "Current medication",
                "value": "medication"
              },
              {
                "label": "Heart condition",
                "value": "heart_condition"
              },
              {
                "label": "Pregnancy",
                "value": "pregnancy"
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
            "y": 1044
          },
          "props": {
            "height": 200,
            "helpText": "If you selected 'Other' above, please add details here.",
            "label": "Medication, allergies or other health notes",
            "placeholder": "List medications, allergy details, or any other information we should know",
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
            "y": 1348
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
            "y": 1348
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
            "y": 1482
          },
          "props": {
            "height": 110,
            "helpText": "Include country code (e.g. +61).",
            "label": "Emergency contact phone",
            "placeholder": "+61 4XX XXX XXX",
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
          "id": "paragraph-16",
          "position": {
            "x": 40,
            "y": 1616
          },
          "props": {
            "height": 48,
            "helpText": "By signing below you acknowledge the risks associated with participation and agree to the terms linked below. You consent to emergency medical treatment if required.",
            "label": "Waiver and consent",
            "tabOrder": 16,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "terms-17",
          "position": {
            "x": 40,
            "y": 1688
          },
          "props": {
            "height": 120,
            "label": "I have read and agree to the waiver and event terms",
            "tabOrder": 17,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "text-18",
          "position": {
            "x": 40,
            "y": 1832
          },
          "props": {
            "height": 110,
            "label": "Full name (signing)",
            "placeholder": "Type your full name to sign",
            "tabOrder": 18,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "date-19",
          "position": {
            "x": 424,
            "y": 1832
          },
          "props": {
            "height": 110,
            "label": "Date signed",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 19,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "submit-button-20",
          "position": {
            "x": 40,
            "y": 1966
          },
          "props": {
            "height": 72,
            "label": "Submit waiver",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 45810,
  "failure_class": "none",
  "input_tokens": 3421,
  "output_tokens": 4010,
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
    "height": 1610,
    "width": 960
  },
  "formId": "au-event-rsvp",
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
            "helpText": "We'll send your ticket and event updates here",
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
            "helpText": "Mobile or daytime number (Australian format)",
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
            "label": "State / territory",
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
                "label": "Western Australia (WA)",
                "value": "wa"
              },
              {
                "label": "South Australia (SA)",
                "value": "sa"
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
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a state or territory",
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
            "helpText": "Select all that apply or choose 'No dietary requirements'",
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
                "label": "Nut-free",
                "value": "nut_free"
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
                "label": "Other (please specify)",
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
            "helpText": "Include severity and typical reactions if relevant",
            "label": "Dietary details",
            "placeholder": "Tell us about allergies or special requirements",
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
            "y": 874
          },
          "props": {
            "height": 120,
            "helpText": "Select supports we should prepare for you",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Hearing loop / captioning",
                "value": "hearing"
              },
              {
                "label": "Assistance animal",
                "value": "assistance_animal"
              },
              {
                "label": "Seating assistance",
                "value": "seating"
              },
              {
                "label": "Visual aids / large print",
                "value": "visual"
              },
              {
                "label": "Other (please describe)",
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
            "y": 1018
          },
          "props": {
            "height": 200,
            "helpText": "Tell us how we can make the event accessible for you",
            "label": "Accessibility details",
            "placeholder": "Please describe any support, equipment or arrangements needed",
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
            "y": 1322
          },
          "props": {
            "height": 120,
            "helpText": "By consenting you agree to receive electronic communications about this event and related offers.",
            "label": "I agree to receive event updates and occasional marketing from the organiser via email and SMS. I understand I can opt out at any time.",
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
            "y": 1466
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
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
  "duration_ms": 57613,
  "failure_class": "none",
  "input_tokens": 3493,
  "output_tokens": 5065,
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
    "height": 1970,
    "width": 960
  },
  "formId": "sydney-rsvp-au",
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
            "label": "Location: Sydney\nPlease complete your details to confirm attendance.",
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
            "helpText": "We'll send your RSVP confirmation here.",
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
            "helpText": "Australian number preferred for event updates.",
            "label": "Phone number",
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
                "label": "Overseas",
                "value": "overseas"
              }
            ],
            "placeholder": "Select state or territory",
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
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 498
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
          "id": "number-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter 0 if you are not attending.",
            "label": "Number of guests (including you)",
            "placeholder": "Enter total attendees covered by this RSVP",
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
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply.",
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
                "label": "Other",
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
            "label": "If other, please specify dietary needs",
            "placeholder": "Tell us about any other dietary requirements",
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
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "Select any supports you require; we will follow up if needed.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Hearing assistance / Auslan",
                "value": "hearing"
              },
              {
                "label": "Vision assistance",
                "value": "vision"
              },
              {
                "label": "Assistance animal",
                "value": "assistance_animal"
              },
              {
                "label": "Seating preference",
                "value": "seating"
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
            "y": 1234
          },
          "props": {
            "height": 200,
            "label": "If other, please describe accessibility needs",
            "placeholder": "Provide any details that will help us accommodate you",
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
          "id": "checkbox-13",
          "position": {
            "x": 40,
            "y": 1538
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive event updates and related news. You can unsubscribe at any time.",
            "label": "Event updates",
            "options": [
              {
                "label": "Yes \u2014 I'd like to receive event updates by email",
                "value": "updates_email"
              }
            ],
            "tabOrder": 13,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1682
          },
          "props": {
            "height": 120,
            "helpText": "By submitting this form you accept the event terms.",
            "label": "Terms & privacy",
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
            "y": 1826
          },
          "props": {
            "height": 72,
            "label": "Submit RSVP",
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
    "content_hash": "cb8bb827bb1350b860772d2a043ff4e3050bd9fc58ca7459ba2607d286904d91",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "auckland",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Wellington",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "wellington",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Canterbury",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "canterbury",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Otago",
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "otago",
    "prompt_id": "p15-au-adversarial-r1",
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
  "component_count": 14,
  "duration_ms": 65237,
  "failure_class": "none",
  "input_tokens": 3503,
  "output_tokens": 5372,
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
    "height": 1914,
    "width": 960
  },
  "formId": "nz-rsvp-form",
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
            "helpText": "Prefer a New Zealand number where possible",
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
                "label": "Yes",
                "value": "yes"
              },
              {
                "label": "No",
                "value": "no"
              }
            ],
            "tabOrder": 5,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 319
          },
          "type": "radio"
        },
        {
          "id": "number-6",
          "position": {
            "x": 383,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Number of guests (including you)",
            "placeholder": "1",
            "tabOrder": 6,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 195
          },
          "type": "number"
        },
        {
          "id": "dropdown-7",
          "position": {
            "x": 601,
            "y": 292
          },
          "props": {
            "height": 110,
            "label": "Region",
            "options": [
              {
                "label": "Auckland",
                "value": "auckland"
              },
              {
                "label": "Wellington",
                "value": "wellington"
              },
              {
                "label": "Canterbury",
                "value": "canterbury"
              },
              {
                "label": "Otago",
                "value": "otago"
              },
              {
                "label": "Waikato",
                "value": "waikato"
              },
              {
                "label": "Bay of Plenty",
                "value": "bay_of_plenty"
              },
              {
                "label": "Manawatu\u2011Whanganui",
                "value": "manawatu_whanganui"
              },
              {
                "label": "Hawke's Bay",
                "value": "hawkes_bay"
              },
              {
                "label": "Taranaki",
                "value": "taranaki"
              },
              {
                "label": "Northland",
                "value": "northland"
              },
              {
                "label": "Southland",
                "value": "southland"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select region",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 319
          },
          "type": "dropdown"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 110,
            "label": "ZIP code",
            "placeholder": "e.g. 12345",
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
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "No preference",
                "value": "no_preference"
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
            "y": 714
          },
          "props": {
            "height": 200,
            "label": "Other dietary requirements",
            "placeholder": "Please specify any other dietary needs",
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
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 1018
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 we will treat this information confidentially",
            "label": "Accessibility needs",
            "placeholder": "Tell us about any accessibility requirements we should plan for",
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
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 1322
          },
          "props": {
            "height": 200,
            "label": "Additional information",
            "placeholder": "Any other details we should know?",
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
            "y": 1626
          },
          "props": {
            "height": 120,
            "label": "I agree to the event terms and consent to receive event updates",
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
            "y": 1770
          },
          "props": {
            "height": 72,
            "label": "Submit RSVP",
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
      "title": "RSVP \u2014 New Zealand Event"
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
