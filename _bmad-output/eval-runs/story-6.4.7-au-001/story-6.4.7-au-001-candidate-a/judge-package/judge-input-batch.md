# Form AI Judge Input Batch

Run ID: `story-6.4.7-au-001-candidate-a`
Benchmark set: `prompts-au-v1`
Rubric version: `rubric_v2`

## Experiment Context

This judge package is for one candidate arm of an Analyst prompt experiment.

```json
{
  "baseline_run_id": "story-6.4.6-au-baseline-current",
  "candidate_hypothesis": "Replacing the conflicting neutral/international AU locale framing with strict AU locale precedence will reduce foreign locale leakage and improve AU format fidelity without materially regressing field coverage or copy quality.",
  "candidate_label": "candidate-a",
  "changed_section_id": "candidate_prompt_block",
  "eval_only": true,
  "expected_metric_movement": {
    "cross_locale_leakage": "increase",
    "format_pattern_accuracy": "increase",
    "locale_fidelity": "increase",
    "policy_compliance": "increase"
  },
  "experiment_id": "story-6.4.7-au-001",
  "improvement_goal": "strict-au-locale-resolution",
  "known_risk_metrics": [
    "field_coverage_recall",
    "field_label_f1",
    "copy_quality_score"
  ],
  "scenario_slice": "au-all",
  "selected_prompt_ids": [],
  "system_prompt_addendum_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
  "target_metrics": [
    "locale_fidelity",
    "cross_locale_leakage",
    "format_pattern_accuracy",
    "policy_compliance"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 25959,
  "failure_class": "none",
  "input_tokens": 3214,
  "output_tokens": 2893,
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
            "helpText": "We\u2019ll send your confirmation and ticket to this address.",
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
            "helpText": "Include country code if outside Australia. Example: [SCRUBBED_PHONE]",
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
            "helpText": "Choose the size for your complimentary conference t-shirt.",
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
            "helpText": "Select all that apply so we can cater accordingly.",
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
            "helpText": "If you selected Other or have allergies, please provide details here.",
            "label": "Dietary details (allergies or other)",
            "placeholder": "E.g. allergic to peanuts; prefer dairy-free options",
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
      "title": "Annual Sales Conference \u2014 Registration"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 22799,
  "failure_class": "none",
  "input_tokens": 3286,
  "output_tokens": 2471,
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
  "formId": "annual-sales-conference-sydney",
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
            "helpText": "This registration is for the Sydney event. If you need a different location, contact the organiser.",
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
            "helpText": "We'll send your registration confirmation and event updates to this address.",
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
            "helpText": "Include country code if outside Australia. Example: [SCRUBBED_PHONE].",
            "label": "Phone number",
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
          "id": "textarea-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 200,
            "helpText": "List any allergies or dietary preferences. We'll do our best to accommodate requests.",
            "label": "Dietary requirements",
            "placeholder": "e.g. Vegetarian, gluten-free, nut allergy",
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
            "helpText": "Select the size for your event T-shirt. Sizes in Australian standards.",
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
            "placeholder": "Select your T-shirt size",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 25330,
  "failure_class": "none",
  "input_tokens": 3296,
  "output_tokens": 2835,
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
            "helpText": "As you would like it to appear on your badge.",
            "label": "First name",
            "options": [],
            "placeholder": "First name",
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
            "helpText": "Family name or surname.",
            "label": "Last name",
            "options": [],
            "placeholder": "Last name",
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
            "helpText": "We will send your registration confirmation to this address.",
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
            "helpText": "Include country code, e.g. +61 for Australia. We may SMS you event updates.",
            "label": "Phone number",
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
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "We provide shirts in these sizes. Please select your preferred size.",
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
                "label": "2XL",
                "value": "2XL"
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
          "id": "text-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Australian postcode (four digits). Include Suburb and State where helpful.",
            "label": "Postcode",
            "options": [],
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
          "id": "textarea-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 200,
            "helpText": "Please list any dietary needs or allergies so we can accommodate you.",
            "label": "Dietary requirements",
            "options": [],
            "placeholder": "e.g. vegetarian, gluten-free, nut allergy",
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
            "options": [],
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 37095,
  "failure_class": "none",
  "input_tokens": 3211,
  "output_tokens": 4261,
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
    "height": 1888,
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
            "helpText": "As you would like it to appear on your badge.",
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
            "helpText": "We'll send confirmation and event updates to this address.",
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
            "helpText": "Include country code if outside Australia (e.g. +61).",
            "label": "Mobile number",
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
            "placeholder": "Your organisation",
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
            "label": "Job title",
            "placeholder": "e.g. Marketing Manager",
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
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Choose how you'll attend.",
            "label": "Attendance type",
            "options": [
              {
                "label": "In-person",
                "value": "in_person"
              },
              {
                "label": "Virtual",
                "value": "virtual"
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
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Select the session(s) you plan to attend.",
            "label": "Sessions",
            "options": [
              {
                "label": "Keynote: Opening",
                "value": "keynote_opening"
              },
              {
                "label": "Workshop A: Data Strategy",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B: Product Design",
                "value": "workshop_b"
              },
              {
                "label": "Panel: Future of Tech",
                "value": "panel_future_tech"
              },
              {
                "label": "Networking Lunch",
                "value": "networking_lunch"
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
            "y": 714
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
            "y": 858
          },
          "props": {
            "height": 200,
            "helpText": "Provide details if you selected 'Other' or have allergies.",
            "label": "Other dietary details",
            "placeholder": "Please specify other dietary needs or allergies",
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
            "y": 1162
          },
          "props": {
            "height": 200,
            "helpText": "We'll contact you to discuss reasonable adjustments if needed.",
            "label": "Accessibility or support needs",
            "placeholder": "Let us know any accessibility requirements or support we can provide",
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
          "id": "number-12",
          "position": {
            "x": 40,
            "y": 1466
          },
          "props": {
            "height": 110,
            "helpText": "Enter how many guests you're bringing (if any).",
            "label": "Number of additional guests",
            "placeholder": "0",
            "tabOrder": 12,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 220
          },
          "type": "number"
        },
        {
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1600
          },
          "props": {
            "height": 120,
            "helpText": "By consenting you agree to receive event-related emails and SMS; you can unsubscribe at any time.",
            "label": "I consent to receive event updates and marketing communications. I understand my personal information will be handled in accordance with the Privacy Act 1988 and the Spam Act 2003. I may opt out at any time.",
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
            "y": 1744
          },
          "props": {
            "height": 72,
            "label": "RSVP",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 42944,
  "failure_class": "none",
  "input_tokens": 3283,
  "output_tokens": 4489,
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
            "helpText": "Please provide your details, choose a session, and tell us about any dietary needs. We'll use your contact details to send event updates for this Sydney conference.",
            "label": "Event details",
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
            "helpText": "We will send your RSVP confirmation and event updates to this email.",
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
            "helpText": "Include country code, e.g. +61 for Australia.",
            "label": "Phone number",
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
            "placeholder": "Company or institution (optional)",
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
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose the main session you plan to attend during the Sydney conference.",
            "label": "Session choice",
            "options": [
              {
                "label": "Keynote \u2014 Opening (09:00)",
                "value": "keynote_opening"
              },
              {
                "label": "Workshop A \u2014 Data Ethics (10:30)",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B \u2014 AI in Practice (10:30)",
                "value": "workshop_b"
              },
              {
                "label": "Panel \u2014 Future of Tech (14:00)",
                "value": "panel_future_tech"
              },
              {
                "label": "Networking Lunch (12:30)",
                "value": "networking_lunch"
              }
            ],
            "placeholder": "Select the session you will attend",
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
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Choose any dietary needs so catering can be arranged.",
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
                "label": "Other (please specify below)",
                "value": "other"
              }
            ],
            "placeholder": "Select an option",
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
            "y": 766
          },
          "props": {
            "height": 200,
            "helpText": "Only fill this in if you have specific dietary requirements or selected 'Other'.",
            "label": "Please specify dietary needs or allergies",
            "placeholder": "E.g. severe nut allergy, dairy intolerance, or details related to 'Other'",
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
            "y": 1070
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive event updates and accept the event terms and privacy information for this Sydney conference.",
            "label": "Consent to receive event updates and accept event terms",
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
            "y": 1214
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 46650,
  "failure_class": "none",
  "input_tokens": 3293,
  "output_tokens": 4838,
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
            "helpText": "As you would like it to appear on your badge.",
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
            "helpText": "We\u2019ll use this address to send your ticket and event updates.",
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
            "helpText": "Include country code; for Australian numbers use +61.",
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
            "helpText": "Please include Suburb, State and Postcode.",
            "label": "Address",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Select the session you plan to attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Morning keynote (09:00\u201310:30)",
                "value": "morning_keynote"
              },
              {
                "label": "Workshop A \u2014 Data & AI (11:00\u201312:30)",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B \u2014 Product Strategy (11:00\u201312:30)",
                "value": "workshop_b"
              },
              {
                "label": "Evening networking (17:30\u201319:00)",
                "value": "evening_networking"
              }
            ],
            "placeholder": "Choose a session",
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
            "helpText": "Tick any that apply.",
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
            "helpText": "Provide details if you selected 'Other' or have allergies. Max 500 characters.",
            "label": "Other dietary requirements",
            "placeholder": "Please specify any allergies or special requirements",
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
            "helpText": "I consent to receive event updates and marketing communications. Personal information will be handled in line with the Privacy Act 1988 and we will comply with the Spam Act 2003. See the event terms for more information.",
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
            "y": 1152
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 38680,
  "failure_class": "none",
  "input_tokens": 3209,
  "output_tokens": 3994,
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
            "label": "Please complete your details so we can tailor the workshop and support your participation.",
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
            "helpText": "As you prefer to be addressed",
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
            "helpText": "We'll send confirmation and event updates to this address.",
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
            "helpText": "Include country code (+61) if you may receive SMS or calls while travelling.",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide suburb, state and postcode (used for reporting and regional planning).",
            "label": "Address",
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
            "helpText": "Helps us tailor examples and exercises.",
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
              },
              {
                "label": "Prefer not to say",
                "value": "prefer_not_say"
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
            "helpText": "Choose the stream you'd like to attend; we'll try to accommodate your preference.",
            "label": "Preferred workshop stream",
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
                "label": "Data & Analytics",
                "value": "data"
              },
              {
                "label": "No preference",
                "value": "no_preference"
              }
            ],
            "placeholder": "Select a stream",
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
            "helpText": "Select any support you require. We'll contact you to follow up if needed.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair_access"
              },
              {
                "label": "Hearing assistance or Auslan interpretation",
                "value": "hearing_assistance"
              },
              {
                "label": "Vision assistance / large print",
                "value": "vision_assistance"
              },
              {
                "label": "Dietary requirements (catering)",
                "value": "dietary_requirements"
              },
              {
                "label": "Quiet space or extra breaks",
                "value": "quiet_space"
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
          "id": "text-10",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "We will only use this information to provide appropriate support.",
            "label": "If other, please specify",
            "placeholder": "Provide brief details about additional needs",
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
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 use this to tell us about goals or special requirements.",
            "label": "Anything else we should know?",
            "placeholder": "Accessibility details, learning goals, or other notes",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 50793,
  "failure_class": "none",
  "input_tokens": 3281,
  "output_tokens": 4959,
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
            "helpText": "Sessions run in Sydney. We'll contact you with venue details and any event updates.",
            "label": "Please complete your details below so we can confirm your place and make any necessary arrangements.",
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
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will use this to send your registration confirmation and important event updates.",
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
            "helpText": "Include country code for SMS updates (e.g. +61). Optional but helpful for urgent updates.",
            "label": "Phone number",
            "options": [],
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Use Suburb, State and Postcode (e.g. Sydney, NSW, 2000). Useful for local arrangements and catering.",
            "label": "Postal address",
            "options": [],
            "placeholder": "Street address, Suburb, State, Postcode",
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
            "helpText": "Choose the option that best matches your current experience for appropriate session placement.",
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
              },
              {
                "label": "Prefer not to say",
                "value": "prefer_not_to_say"
              }
            ],
            "placeholder": "Select your skill level",
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
          "id": "radio-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Pick the stream you would like to attend. We'll try to accommodate your choice.",
            "label": "Preferred workshop stream",
            "options": [
              {
                "label": "Data & Analytics",
                "value": "data_analytics"
              },
              {
                "label": "Design & UX",
                "value": "design_ux"
              },
              {
                "label": "Product Management",
                "value": "product_management"
              },
              {
                "label": "Developer Tools",
                "value": "developer_tools"
              },
              {
                "label": "No preference",
                "value": "no_preference"
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
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 200,
            "helpText": "If you need adjustments (e.g. wheelchair access, sign language), please describe them so we can follow up.",
            "label": "Accessibility requirements or dietary needs",
            "options": [],
            "placeholder": "Tell us about any access requirements, mobility needs, or dietary requirements for catering",
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
            "helpText": "Tick to receive event updates and occasional marketing about future workshops. Optional.",
            "label": "Communications preference",
            "options": [
              {
                "label": "Yes \u2014 I'd like to receive event updates and marketing",
                "value": "opt_in_updates"
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
            "helpText": "By registering you agree to the organiser's event terms and privacy notice. View the event terms on the event page.",
            "label": "I agree to the event terms and privacy notice",
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
            "y": 1234
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
      "title": "Sydney Workshop \u2014 Participant Signup"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 29727,
  "failure_class": "none",
  "input_tokens": 3291,
  "output_tokens": 3010,
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
            "helpText": "We\u2019ll use this address for event updates and confirmations.",
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
            "helpText": "Include your country code if outside Australia (e.g. +61).",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Enter Suburb, State and Postcode (e.g. Sydney, NSW 2000).",
            "label": "Address",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Choose the option that best describes your current proficiency.",
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
          "id": "radio-7",
          "position": {
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Select the stream you\u2019d most like to attend.",
            "label": "Preferred workshop stream",
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
                "label": "Management",
                "value": "management"
              },
              {
                "label": "Research",
                "value": "research"
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
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Select any adjustments or support you require to participate fully.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Hearing assistance / Auslan interpreter",
                "value": "hearing"
              },
              {
                "label": "Vision assistance / large print",
                "value": "vision"
              },
              {
                "label": "Quiet space or low-sensory area",
                "value": "quiet"
              },
              {
                "label": "Dietary requirements (for catering)",
                "value": "dietary"
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
            "y": 714
          },
          "props": {
            "height": 200,
            "helpText": "Include any details that will help us make appropriate arrangements.",
            "label": "If other, or to provide details, please describe accessibility or dietary needs",
            "placeholder": "Describe any specific adjustments, equipment or support you need",
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
            "label": "Additional notes (optional)",
            "placeholder": "Anything else we should know?",
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
          "id": "submit-button-11",
          "position": {
            "x": 40,
            "y": 1322
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 30044,
  "failure_class": "none",
  "input_tokens": 3214,
  "output_tokens": 3062,
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
            "helpText": "As you\u2019d like it to appear on the attendee list.",
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
            "helpText": "We\u2019ll send webinar access details and a calendar invite. No spam.",
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
            "helpText": "Include country code (e.g. +61) if outside Australia. Used only for urgent event updates.",
            "label": "Phone number",
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
            "helpText": "We\u2019ll show webinar times in your chosen zone.",
            "label": "Time zone",
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
                "label": "UTC (Coordinated Universal Time)",
                "value": "UTC"
              },
              {
                "label": "Europe/London (GMT/BST)",
                "value": "Europe/London"
              },
              {
                "label": "America/New_York (ET)",
                "value": "America/New_York"
              }
            ],
            "placeholder": "Select your time zone",
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
            "helpText": "Optional: we\u2019ll try to address these during the Q&A.",
            "label": "Questions for the speaker",
            "placeholder": "Any topics or specific questions you\u2019d like covered?",
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
            "helpText": "We may contact you about future events and resources relevant to this webinar.",
            "label": "Marketing and event updates: I agree to receive marketing communications and event updates (including by email). I understand I can unsubscribe at any time and that personal information will be handled in accordance with the Privacy Act 1988.",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 40065,
  "failure_class": "none",
  "input_tokens": 3286,
  "output_tokens": 3815,
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
            "label": "We\u2019ll email joining instructions and any updates for this webinar. Times shown in your confirmation will use the timezone you select.",
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
            "helpText": "We\u2019ll use this to send joining details and any updates.",
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
            "helpText": "Include country code (Australia: +61) if you may receive SMS updates.",
            "label": "Phone number",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Organisation",
            "placeholder": "Company or organisation name",
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
            "helpText": "Choose the timezone you prefer for calendar invites and reminders.",
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
                "label": "UTC (Coordinated Universal Time)",
                "value": "UTC"
              },
              {
                "label": "Asia/Tokyo (JST)",
                "value": "Asia/Tokyo"
              },
              {
                "label": "America/Los_Angeles (PST/PDT)",
                "value": "America/Los_Angeles"
              },
              {
                "label": "Europe/London (GMT/BST)",
                "value": "Europe/London"
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
            "helpText": "We may select and share questions with the speaker during the session.",
            "label": "Questions for the speaker",
            "placeholder": "Share any questions you'd like the speaker to address (optional).",
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
            "helpText": "Opt in to receive event updates, future webinar invitations and marketing communications.",
            "label": "Marketing and event updates",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 40362,
  "failure_class": "none",
  "input_tokens": 3296,
  "output_tokens": 4085,
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
          "id": "text-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Your employer or organisation name",
            "label": "Organisation",
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
            "label": "Job title / role",
            "placeholder": "e.g. Marketing Manager",
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
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send confirmation and joining details to this address.",
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
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include country code, e.g. +61 for Australia.",
            "label": "Phone",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Choose the timezone you\u2019ll join from.",
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
                "label": "Australia/Brisbane (AEST)",
                "value": "Australia/Brisbane"
              },
              {
                "label": "UTC",
                "value": "UTC"
              },
              {
                "label": "Europe/London (GMT/BST)",
                "value": "Europe/London"
              },
              {
                "label": "America/New_York (EST/EDT)",
                "value": "America/New_York"
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
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 110,
            "helpText": "Australian postcode (4 digits).",
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
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 694
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 tell us any specific points you want addressed.",
            "label": "Questions for the speaker",
            "placeholder": "Any questions or topics you'd like the speaker to cover",
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
            "helpText": "I agree to receive event updates and marketing communications.",
            "label": "Marketing and communications",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 35040,
  "failure_class": "none",
  "input_tokens": 3215,
  "output_tokens": 3538,
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
            "helpText": "We'll use this only to send RSVP confirmation or event updates.",
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
            "helpText": "Include +61 country code if outside Australia.",
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
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "helpText": "Please tell us if you can join the celebration.",
            "label": "Will you attend?",
            "options": [
              {
                "label": "Accepts with pleasure",
                "value": "yes"
              },
              {
                "label": "Regrets, cannot attend",
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
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 120,
            "helpText": "Select 'Yes' only if you're bringing a plus-one.",
            "label": "Will you be bringing a guest?",
            "options": [
              {
                "label": "No",
                "value": "no"
              },
              {
                "label": "Yes",
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
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 580
          },
          "props": {
            "height": 110,
            "helpText": "Only complete this if you answered 'Yes' above.",
            "label": "Guest name (if bringing a plus-one)",
            "placeholder": "Guest's full name",
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
            "y": 714
          },
          "props": {
            "height": 110,
            "helpText": "Please select one meal per attending guest.",
            "label": "Meal choice",
            "options": [
              {
                "label": "Beef \u2013 roast sirloin (AUD sample menu)",
                "value": "beef"
              },
              {
                "label": "Chicken \u2013 herb roast",
                "value": "chicken"
              },
              {
                "label": "Fish \u2013 grilled fillet",
                "value": "fish"
              },
              {
                "label": "Vegetarian \u2013 seasonal vegetables",
                "value": "vegetarian"
              },
              {
                "label": "Vegan \u2013 plant-based main",
                "value": "vegan"
              },
              {
                "label": "Children's meal",
                "value": "children"
              }
            ],
            "placeholder": "Select your main course",
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
            "y": 848
          },
          "props": {
            "height": 200,
            "helpText": "Tell us any dietary needs for you and your guest.",
            "label": "Dietary requirements",
            "placeholder": "Allergies, intolerances, dietary preferences (e.g. gluten-free, halal).",
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
            "y": 1152
          },
          "props": {
            "height": 110,
            "helpText": "Suggest a tune you'd like to hear on the night.",
            "label": "Song request",
            "placeholder": "Artist \u2013 Song title",
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
            "y": 1286
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 we may read selected messages during the celebrations.",
            "label": "Message to the couple",
            "placeholder": "A note, wish or message for the newlyweds.",
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
            "y": 1590
          },
          "props": {
            "height": 120,
            "label": "Privacy & communications",
            "options": [],
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
            "y": 1734
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 41693,
  "failure_class": "none",
  "input_tokens": 3287,
  "output_tokens": 4492,
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
    "height": 1816,
    "width": 960
  },
  "formId": "wedding-rsvp-sydney",
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
            "label": "Please complete the RSVP below so we can finalise numbers with our caterer.",
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
            "helpText": "We\u2019ll use this to confirm your RSVP and any updates.",
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
            "helpText": "Include +61 country code if you're in Australia.",
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
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 364
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
                "label": "No \u2014 sorry, I can't make it",
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
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 508
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you plan to bring a guest.",
            "label": "Bringing a plus-one?",
            "options": [
              {
                "label": "I will bring a plus-one",
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
            "x": 424,
            "y": 508
          },
          "props": {
            "height": 110,
            "helpText": "Fill this only if you are bringing a plus-one.",
            "label": "Plus-one name (if applicable)",
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
            "y": 652
          },
          "props": {
            "height": 110,
            "label": "Main meal choice",
            "options": [
              {
                "label": "Beef (roast sirloin)",
                "value": "beef"
              },
              {
                "label": "Chicken (herb roasted)",
                "value": "chicken"
              },
              {
                "label": "Vegetarian (chef's selection)",
                "value": "vegetarian"
              },
              {
                "label": "Vegan",
                "value": "vegan"
              },
              {
                "label": "Children's meal",
                "value": "child_meal"
              }
            ],
            "placeholder": "Choose a meal",
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
            "y": 786
          },
          "props": {
            "height": 200,
            "helpText": "We will share this information with our caterer to accommodate requirements.",
            "label": "Dietary requirements (allergies, restrictions, intolerances)",
            "placeholder": "Please list any dietary needs we should know about",
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
            "y": 1090
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll do our best to include your request.",
            "label": "Song request (optional)",
            "placeholder": "Artist \u2014 Song title (e.g., ABBA \u2014 Dancing Queen)",
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
            "y": 1224
          },
          "props": {
            "height": 200,
            "label": "Message to the couple (optional)",
            "placeholder": "Leave a message or well wishes",
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
            "y": 1528
          },
          "props": {
            "height": 120,
            "helpText": "By submitting you accept the event terms and privacy handling.",
            "label": "I agree to the event terms and the handling of my RSVP information in accordance with the organiser\u2019s privacy practices.",
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
            "y": 1672
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 36661,
  "failure_class": "none",
  "input_tokens": 3297,
  "output_tokens": 4136,
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
    "height": 1950,
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
            "label": "Please complete one RSVP per household. If you're bringing additional guests, indicate their details below.",
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
            "width": 535
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 599,
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
            "width": 321
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
            "helpText": "We\u2019ll send RSVP confirmations to this email.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 535
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 599,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include the country code (+61) for Australian numbers.",
            "label": "Phone number",
            "placeholder": "+61 4xx xxx xxx",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 321
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
            "helpText": "Use Suburb, State and Postcode for Australian addresses.",
            "label": "Postal address",
            "placeholder": "Suburb, State, Postcode",
            "tabOrder": 6,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 535
          },
          "type": "address"
        },
        {
          "id": "radio-7",
          "position": {
            "x": 599,
            "y": 364
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
            "width": 321
          },
          "type": "radio"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 508
          },
          "props": {
            "height": 120,
            "label": "Bringing a plus one?",
            "options": [
              {
                "label": "Yes \u2014 I will bring a plus one",
                "value": "bringing_plus_one"
              }
            ],
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "checkbox"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 652
          },
          "props": {
            "height": 110,
            "label": "Plus-one full name",
            "placeholder": "Guest's first and last name",
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
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "If you are not attending, you may leave this blank.",
            "label": "Main meal choice",
            "options": [
              {
                "label": "Beef (roast)",
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
                "label": "Children's meal",
                "value": "child"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
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
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about any allergies or dietary needs so we can accommodate them.",
            "label": "Dietary requirements",
            "placeholder": "List allergies, intolerances or other requirements",
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
            "helpText": "One song request per RSVP, if you'd like.",
            "label": "Song request",
            "placeholder": "Artist \u2014 Song title",
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
            "y": 1358
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 any well wishes or notes for the couple.",
            "label": "Message to the couple",
            "placeholder": "A short message or congratulations",
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
            "y": 1662
          },
          "props": {
            "height": 120,
            "helpText": "By submitting your RSVP you accept the organiser\u2019s event terms and privacy policy (opens in a popup).",
            "label": "Agree to event terms and privacy",
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
            "y": 1806
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 35717,
  "failure_class": "none",
  "input_tokens": 3211,
  "output_tokens": 4344,
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
            "helpText": "We'll contact you about shifts and important updates. Use an address you check regularly.",
            "label": "Email",
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
            "helpText": "Please include your country code if outside Australia (example: +61 4xx xxx xxx).",
            "label": "Phone",
            "options": [],
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Provide Suburb, State and Postcode. We use this for shift allocation and emergency contact purposes.",
            "label": "Address",
            "options": [],
            "placeholder": "Street address, Suburb, State, Postcode",
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
            "helpText": "Select all days you can volunteer.",
            "label": "Days available",
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
          "id": "date-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "Start date (DD/MM/YYYY).",
            "label": "Available from",
            "options": [],
            "placeholder": "DD/MM/YYYY",
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
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "End date (DD/MM/YYYY). Leave blank if ongoing.",
            "label": "Available until",
            "options": [],
            "placeholder": "DD/MM/YYYY",
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
            "y": 704
          },
          "props": {
            "height": 120,
            "helpText": "Select skills or roles you can help with. Choose at least one.",
            "label": "Skills and roles",
            "options": [
              {
                "label": "Event setup / pack down",
                "value": "setup"
              },
              {
                "label": "Front of house / info desk",
                "value": "front_of_house"
              },
              {
                "label": "First aid / medical",
                "value": "first_aid"
              },
              {
                "label": "Child supervision",
                "value": "child_supervision"
              },
              {
                "label": "Logistics / driving",
                "value": "logistics"
              },
              {
                "label": "Photography / media",
                "value": "photography"
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
            "y": 848
          },
          "props": {
            "height": 200,
            "helpText": "Include expiry dates for any certifications where relevant.",
            "label": "Relevant experience or certifications",
            "options": [],
            "placeholder": "Describe any experience, licences or certifications (e.g. first aid certificate, RSA, driver licence).",
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
            "label": "Emergency contact name",
            "options": [],
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
          "id": "dropdown-12",
          "position": {
            "x": 424,
            "y": 1152
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "options": [
              {
                "label": "Partner / Spouse",
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
          "id": "phone-13",
          "position": {
            "x": 40,
            "y": 1286
          },
          "props": {
            "height": 110,
            "helpText": "Include country code where applicable.",
            "label": "Emergency contact phone",
            "options": [],
            "placeholder": "+61 4xx xxx xxx",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1420
          },
          "props": {
            "height": 120,
            "helpText": "I agree to follow the event code of conduct and any reasonable direction from event staff. I understand my information will be used to coordinate volunteering and held in line with the Privacy Act 1988. I consent to receiving event-related communications.",
            "label": "Code of conduct acknowledgement",
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
          "id": "textarea-15",
          "position": {
            "x": 40,
            "y": 1564
          },
          "props": {
            "height": 200,
            "helpText": "Optional. If urgent medical info, also tell staff on arrival.",
            "label": "Additional notes",
            "options": [],
            "placeholder": "Any accessibility needs, medical conditions, or other info we should know",
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
            "y": 1868
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
            "options": [],
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 32605,
  "failure_class": "none",
  "input_tokens": 3283,
  "output_tokens": 3824,
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
    "height": 1708,
    "width": 960
  },
  "formId": "volunteer-signup-sydney",
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
            "helpText": "We\u2019ll use this to confirm your role and send event updates.",
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
            "helpText": "Local number with country code \u2014 e.g. [SCRUBBED_PHONE].",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Provide Suburb, State and Postcode (AU).",
            "label": "Address",
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
            "helpText": "Select all days you can volunteer.",
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
          "id": "date-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "Start date (DD/MM/YYYY).",
            "label": "Available from",
            "placeholder": "DD/MM/YYYY",
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
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "End date (DD/MM/YYYY). Leave blank if ongoing.",
            "label": "Available to",
            "placeholder": "DD/MM/YYYY",
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
            "y": 704
          },
          "props": {
            "height": 120,
            "helpText": "Tell us what you can help with; select all that apply.",
            "label": "Skills & experience",
            "options": [
              {
                "label": "Event setup / pack in",
                "value": "setup"
              },
              {
                "label": "Registration / welcome desk",
                "value": "registration"
              },
              {
                "label": "Crowd management",
                "value": "crowd_management"
              },
              {
                "label": "First aid / medical",
                "value": "first_aid"
              },
              {
                "label": "Childcare / family support",
                "value": "childcare"
              },
              {
                "label": "Logistics / transport",
                "value": "logistics"
              },
              {
                "label": "Photography / social media",
                "value": "media"
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
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 200,
            "label": "Other skills or qualifications",
            "placeholder": "Describe licences, certifications (e.g. RSA, first aid), or additional notes.",
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
            "label": "Emergency contact \u2014 full name",
            "placeholder": "e.g. [SCRUBBED_NAME]",
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
          "id": "phone-12",
          "position": {
            "x": 40,
            "y": 1286
          },
          "props": {
            "height": 110,
            "helpText": "Include country code \u2014 e.g. [SCRUBBED_PHONE].",
            "label": "Emergency contact \u2014 phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 12,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "dropdown-13",
          "position": {
            "x": 424,
            "y": 1286
          },
          "props": {
            "height": 110,
            "label": "Relationship to emergency contact",
            "options": [
              {
                "label": "Parent",
                "value": "parent"
              },
              {
                "label": "Partner / spouse",
                "value": "partner"
              },
              {
                "label": "Friend",
                "value": "friend"
              },
              {
                "label": "Colleague",
                "value": "colleague"
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
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1420
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the code of conduct to volunteer.",
            "label": "Code of conduct & event terms",
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
            "y": 1564
          },
          "props": {
            "height": 72,
            "label": "Sign up",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 37955,
  "failure_class": "none",
  "input_tokens": 3293,
  "output_tokens": 4516,
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
            "helpText": "We will use these details to contact you about volunteering opportunities and for safety/administration purposes.",
            "label": "How we use your information",
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
            "helpText": "We'll use this to send confirmations and event updates.",
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
            "helpText": "Primary contact number. Include country code if outside Australia (e.g. +61).",
            "label": "Phone",
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
            "helpText": "Please include Suburb, State and Postcode.",
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
            "helpText": "Tick all times you can volunteer.",
            "label": "Availability",
            "options": [
              {
                "label": "Monday \u2013 Morning",
                "value": "mon_morning"
              },
              {
                "label": "Monday \u2013 Afternoon",
                "value": "mon_afternoon"
              },
              {
                "label": "Tuesday \u2013 Morning",
                "value": "tue_morning"
              },
              {
                "label": "Tuesday \u2013 Afternoon",
                "value": "tue_afternoon"
              },
              {
                "label": "Wednesday \u2013 Morning",
                "value": "wed_morning"
              },
              {
                "label": "Wednesday \u2013 Afternoon",
                "value": "wed_afternoon"
              },
              {
                "label": "Thursday \u2013 Morning",
                "value": "thu_morning"
              },
              {
                "label": "Thursday \u2013 Afternoon",
                "value": "thu_afternoon"
              },
              {
                "label": "Friday \u2013 Morning",
                "value": "fri_morning"
              },
              {
                "label": "Friday \u2013 Afternoon",
                "value": "fri_afternoon"
              },
              {
                "label": "Weekend \u2013 Any",
                "value": "weekend_any"
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
            "helpText": "Tick any skills or roles you can help with.",
            "label": "Skills and interests",
            "options": [
              {
                "label": "Event setup / pack-down",
                "value": "setup"
              },
              {
                "label": "Registration / welcome desk",
                "value": "registration"
              },
              {
                "label": "Crowd management / stewarding",
                "value": "stewarding"
              },
              {
                "label": "Logistics / equipment",
                "value": "logistics"
              },
              {
                "label": "First aid",
                "value": "first_aid"
              },
              {
                "label": "Photography / social media",
                "value": "photography"
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
            "y": 786
          },
          "props": {
            "height": 200,
            "helpText": "Please provide any details that help us place you in the right role.",
            "label": "Other skills or experience",
            "placeholder": "Tell us about relevant experience, certificates (e.g. first aid) and how recently you trained.",
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
            "y": 1090
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
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
            "y": 1090
          },
          "props": {
            "height": 110,
            "helpText": "A number we can call in an emergency. Include country code if outside Australia (e.g. +61).",
            "label": "Emergency contact phone",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "terms-12",
          "position": {
            "x": 40,
            "y": 1224
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the code of conduct to volunteer.",
            "label": "Code of conduct acknowledgement",
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
      "title": "Volunteer signup"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 33204,
  "failure_class": "none",
  "input_tokens": 3211,
  "output_tokens": 3895,
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
            "helpText": "We will use this to contact you about your application.",
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
            "helpText": "Include country code (+61) for mobile or landline.",
            "label": "Phone number",
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
            "helpText": "Use Suburb, State, Postcode for Australian addresses.",
            "label": "Postal address",
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
            "helpText": "Select the membership category you are applying for.",
            "label": "Membership type",
            "options": [
              {
                "label": "Individual (AUD 50/year)",
                "value": "individual"
              },
              {
                "label": "Concession (AUD 30/year)",
                "value": "concession"
              },
              {
                "label": "Student (AUD 25/year)",
                "value": "student"
              },
              {
                "label": "Organisation (AUD 200/year)",
                "value": "organisation"
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
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "You must confirm you meet the eligibility requirements to apply.",
            "label": "Eligibility confirmation",
            "options": [
              {
                "label": "I confirm I meet all eligibility requirements, am 18 years or older, and agree to abide by the organisation's code of conduct.",
                "value": "eligibility_confirmed"
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
            "y": 714
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
                "label": "Website",
                "value": "website"
              },
              {
                "label": "Social media",
                "value": "social"
              },
              {
                "label": "Event or expo",
                "value": "event"
              },
              {
                "label": "Poster or leaflet",
                "value": "poster"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select an option",
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
            "y": 848
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 tell us more about the referral source.",
            "label": "If other, please specify",
            "placeholder": "Who or where?",
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
            "y": 982
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive news and offers. You can unsubscribe at any time.",
            "label": "Marketing communications (optional)",
            "options": [
              {
                "label": "Yes \u2014 I consent to receive membership news and offers by email and SMS.",
                "value": "marketing_consent"
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
            "y": 1126
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the membership terms and authorise the organisation to use my personal information for membership administration, communications and services in accordance with the Privacy Act 1988.",
            "label": "Terms & privacy acknowledgement",
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
            "y": 1270
          },
          "props": {
            "height": 72,
            "label": "Submit application",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 38429,
  "failure_class": "none",
  "input_tokens": 3283,
  "output_tokens": 4589,
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
    "height": 1934,
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
            "helpText": "This application is for people seeking membership associated with our Sydney chapter. If you have questions, contact us before applying.",
            "label": "About this form",
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
            "helpText": "We'll use this email for membership communication. Provide a regularly checked address.",
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
            "helpText": "Include country code, e.g. +61 for Australia.",
            "label": "Phone",
            "options": [],
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
          "id": "date-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Enter your date of birth (DD/MM/YYYY). Applicants must be 18 years or older to join.",
            "label": "Date of birth",
            "options": [],
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
          "id": "address-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Use Suburb, State and Postcode for Australian addresses.",
            "label": "Residential address",
            "options": [],
            "placeholder": "Street address, unit number",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 632
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
                "label": "Student (proof required)",
                "value": "student"
              },
              {
                "label": "Corporate",
                "value": "corporate"
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
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "label": "I confirm I am at least 18 years old",
            "options": [
              {
                "label": "Yes \u2014 I confirm I am 18 years or older",
                "value": "age_confirmed"
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
            "y": 920
          },
          "props": {
            "height": 120,
            "label": "I am a resident of Australia",
            "options": [
              {
                "label": "Yes \u2014 I am currently resident in Australia",
                "value": "residency_confirmed"
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
            "y": 1064
          },
          "props": {
            "height": 120,
            "helpText": "I agree to abide by the association's code of conduct if my application is accepted.",
            "label": "Code of conduct agreement",
            "options": [
              {
                "label": "I agree to the code of conduct",
                "value": "conduct_agree"
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
            "y": 1208
          },
          "props": {
            "height": 110,
            "helpText": "Tell us how you found out about the association or this membership opportunity.",
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
                "label": "Event in Sydney",
                "value": "sydney_event"
              },
              {
                "label": "Search engine",
                "value": "search"
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
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "text-13",
          "position": {
            "x": 424,
            "y": 1208
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 provide more details if you selected Other.",
            "label": "Referral details (if Other)",
            "options": [],
            "placeholder": "Please specify",
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
            "y": 1342
          },
          "props": {
            "height": 200,
            "helpText": "Use this space to tell us about special circumstances, professional affiliations, or questions.",
            "label": "Additional information",
            "options": [],
            "placeholder": "Any other information you'd like us to know",
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
            "y": 1646
          },
          "props": {
            "height": 120,
            "helpText": "Please review and accept our event terms and privacy policy to proceed.",
            "label": "Terms and privacy",
            "options": [],
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
            "y": 1790
          },
          "props": {
            "height": 72,
            "label": "Apply for membership",
            "options": [],
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
      "title": "Membership Application \u2014 Sydney"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
    "prompt_id": "p07-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p07-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p07-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p07-au-adversarial-r1",
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
  "duration_ms": 39761,
  "failure_class": "none",
  "input_tokens": 3293,
  "output_tokens": 4749,
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
    "height": 1718,
    "width": 960
  },
  "formId": "membership-application",
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
            "helpText": "We\u2019ll use this to contact you about your application.",
            "label": "Email address",
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
            "helpText": "Include country code (user requested +1 example).",
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
            "helpText": "Include street number and name. Include Suburb, State and Postcode in the address lines where relevant.",
            "label": "Street address",
            "placeholder": "Street address",
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
            "helpText": "User requested field labelled ZIP code (include if applicable).",
            "label": "ZIP code",
            "placeholder": "e.g. 90210",
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
              }
            ],
            "placeholder": "Select a membership type",
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
            "label": "I confirm I am aged 18 years or older",
            "options": [
              {
                "label": "I confirm I am aged 18 years or older",
                "value": "age_18_plus"
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
            "y": 704
          },
          "props": {
            "height": 120,
            "label": "I confirm I meet the membership eligibility criteria",
            "options": [
              {
                "label": "I meet the membership eligibility criteria",
                "value": "meets_criteria"
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
            "y": 848
          },
          "props": {
            "height": 120,
            "helpText": "Consent may include identity or background checks as required by membership rules.",
            "label": "I consent to any routine checks required for my application",
            "options": [
              {
                "label": "I consent to required checks",
                "value": "consent_checks"
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
            "y": 992
          },
          "props": {
            "height": 110,
            "helpText": "Select the option that best describes how you found out about this membership.",
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
                "label": "Event or promotion",
                "value": "event"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select one",
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
            "y": 1126
          },
          "props": {
            "height": 200,
            "helpText": "Use this field to tell us anything relevant to your application.",
            "label": "Additional information",
            "placeholder": "Any other details (optional)",
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
            "y": 1430
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event terms and privacy handling to proceed.",
            "label": "Agreement & terms",
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
            "y": 1574
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 21459,
  "failure_class": "none",
  "input_tokens": 3217,
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
            "helpText": "Organisation name or employer.",
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
            "helpText": "Include country code (+61 for Australia) where possible.",
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
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Best address for follow-up.",
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
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Which product or service interested them most?",
            "label": "Interest area",
            "options": [
              {
                "label": "Product demo / features",
                "value": "product_demo"
              },
              {
                "label": "Pricing & procurement",
                "value": "pricing"
              },
              {
                "label": "Technical integration",
                "value": "integration"
              },
              {
                "label": "Partnership / reseller",
                "value": "partnership"
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
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "When do they plan to purchase or engage?",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate \u2014 0 to 3 months",
                "value": "0-3_months"
              },
              {
                "label": "3 to 6 months",
                "value": "3-6_months"
              },
              {
                "label": "6 to 12 months",
                "value": "6-12_months"
              },
              {
                "label": "12+ months",
                "value": "12+_months"
              },
              {
                "label": "Just researching",
                "value": "researching"
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
            "helpText": "Capture key points, product interests, and agreed actions.",
            "label": "Notes",
            "placeholder": "Conversation highlights, objections, next steps...",
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
            "helpText": "You can withdraw consent at any time. We may contact you about this enquiry and related offers.",
            "label": "I consent to be contacted by phone or email about my enquiry and future event or product updates. I understand how my personal information will be used to respond to this request and for marketing communications in accordance with applicable Australian privacy laws.",
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
      "title": "Trade show booth \u2014 Lead capture"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 28904,
  "failure_class": "none",
  "input_tokens": 3289,
  "output_tokens": 3899,
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
          "id": "text-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "label": "Company / Organisation",
            "placeholder": "Organisation or employer",
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
          "id": "dropdown-4",
          "position": {
            "x": 424,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Choose the main topic the visitor was interested in.",
            "label": "Interest area",
            "options": [
              {
                "label": "Product demo",
                "value": "product_demo"
              },
              {
                "label": "Pricing & licensing",
                "value": "pricing"
              },
              {
                "label": "Solutions & integrations",
                "value": "integrations"
              },
              {
                "label": "Technical details",
                "value": "technical"
              },
              {
                "label": "Partnership opportunities",
                "value": "partnerships"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select area of interest",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "email-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Use a business email where possible for follow-up.",
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
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include country code (+61) for follow-up calls or SMS.",
            "label": "Phone",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "When does the visitor expect to make a purchasing decision?",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate (0\u20133 months)",
                "value": "0-3_months"
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
                "label": "12+ months",
                "value": "12+_months"
              },
              {
                "label": "Just browsing / no timeframe",
                "value": "no_timeframe"
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
            "helpText": "Include action items or follow-up instructions. Keep notes concise.",
            "label": "Notes",
            "placeholder": "Key points from the conversation, agreed next steps, who to contact...",
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
            "helpText": "Required to contact this person after the event for sales or product information.",
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
      "title": "Sydney Trade Show \u2014 Booth Lead Log"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 42900,
  "failure_class": "none",
  "input_tokens": 3299,
  "output_tokens": 4340,
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
    "height": 1564,
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
            "width": 320
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
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll use this to send meeting notes and quotes.",
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
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include country code where possible. For AU numbers use +61.",
            "label": "Phone",
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
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Provide Suburb, State and Postcode (AU format).",
            "label": "Business address",
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
            "y": 560
          },
          "props": {
            "height": 110,
            "helpText": "4\u2011digit Australian postcode",
            "label": "Postcode",
            "placeholder": "e.g. 2000",
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
            "y": 694
          },
          "props": {
            "height": 120,
            "helpText": "Select all areas the visitor showed interest in.",
            "label": "Interest area",
            "options": [
              {
                "label": "Product demos",
                "value": "product_demos"
              },
              {
                "label": "Pricing & quotes",
                "value": "pricing_quotes"
              },
              {
                "label": "Technical integration / APIs",
                "value": "technical_integration"
              },
              {
                "label": "Partnerships",
                "value": "partnerships"
              },
              {
                "label": "Other / general interest",
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
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 838
          },
          "props": {
            "height": 110,
            "helpText": "When does the visitor expect to make a purchase decision?",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate \u2013 ready to buy",
                "value": "immediate"
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
                "label": "Just researching / no plan",
                "value": "researching"
              }
            ],
            "placeholder": "Select timeframe",
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
            "y": 972
          },
          "props": {
            "height": 200,
            "helpText": "Include any commitments or next steps agreed at the booth.",
            "label": "Notes from conversation",
            "placeholder": "Key points, pain points, follow-up actions, who else to contact\u2026",
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
            "y": 1276
          },
          "props": {
            "height": 120,
            "helpText": "By checking this box you consent to be contacted about your enquiry and related offers. Personal data handling is subject to our event terms and our obligations under the Privacy Act 1988 and the Spam Act 2003.",
            "label": "Follow-up consent",
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
            "y": 1420
          },
          "props": {
            "height": 72,
            "label": "Save lead",
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
      "title": "Trade Show Booth Lead Log (AU)"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "component_count": 7,
  "duration_ms": 25136,
  "failure_class": "none",
  "input_tokens": 3209,
  "output_tokens": 3155,
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
            "helpText": "Optional \u2014 helps us personalise your emails.",
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
          "id": "text-2",
          "position": {
            "x": 324,
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
            "helpText": "We\u2019ll only use this to send the newsletter. You can unsubscribe any time.",
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
          "id": "checkbox-4",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "helpText": "Select all topics you\u2019re interested in.",
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
                "label": "Guides & tips",
                "value": "guides"
              },
              {
                "label": "Promotions & offers",
                "value": "promotions"
              },
              {
                "label": "Research & surveys",
                "value": "research"
              }
            ],
            "tabOrder": 4,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 120,
            "helpText": "Choose the cadence that suits you.",
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
          "id": "terms-6",
          "position": {
            "x": 40,
            "y": 580
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive marketing emails and updates. We handle your personal information in accordance with the Privacy Act 1988 and the Spam Act 2003. You can unsubscribe at any time.",
            "label": "Marketing consent",
            "tabOrder": 6,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-7",
          "position": {
            "x": 40,
            "y": 724
          },
          "props": {
            "height": 72,
            "label": "Subscribe",
            "tabOrder": 7,
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 29759,
  "failure_class": "none",
  "input_tokens": 3281,
  "output_tokens": 3623,
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
          "id": "first-name-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 110,
            "helpText": "Helps us personalise emails (optional).",
            "label": "First name",
            "placeholder": "e.g. Alex",
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
            "helpText": "We\u2019ll send the newsletter to this address. You can unsubscribe at any time.",
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
            "helpText": "Select all that apply.",
            "label": "What content are you interested in?",
            "options": [
              {
                "label": "Talks & speakers",
                "value": "talks_speakers"
              },
              {
                "label": "Workshops",
                "value": "workshops"
              },
              {
                "label": "Networking events",
                "value": "networking"
              },
              {
                "label": "Venue & logistics",
                "value": "venue_logistics"
              },
              {
                "label": "Offers & sponsors",
                "value": "offers_sponsors"
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
            "helpText": "Choose how often you want the newsletter.",
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
                "label": "Only for major events",
                "value": "major_events"
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
            "helpText": "You can unsubscribe any time. Personal data will be handled in line with the Privacy Act 1988.",
            "label": "I agree to receive marketing and event update emails from the organiser and accept the event terms.",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 35608,
  "failure_class": "none",
  "input_tokens": 3291,
  "output_tokens": 3312,
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
            "helpText": "As you\u2019d like it to appear in emails.",
            "label": "First name",
            "placeholder": "e.g. Jamie",
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
          "id": "email-2",
          "position": {
            "x": 384,
            "y": 24
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send newsletters and subscription confirmations here.",
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
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Include country code, e.g. +61 for Australia. Used only for urgent updates or SMS alerts.",
            "label": "Phone number (optional)",
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
            "x": 384,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Provide your Suburb, State and Postcode to help localise content.",
            "label": "Postcode",
            "placeholder": "e.g. 2000",
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
          "id": "checkbox-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 120,
            "helpText": "Select the topics you want to receive.",
            "label": "Content interests",
            "options": [
              {
                "label": "Technology",
                "value": "technology"
              },
              {
                "label": "Business & Industry",
                "value": "business"
              },
              {
                "label": "Local events",
                "value": "events"
              },
              {
                "label": "Promotions & offers",
                "value": "promotions"
              },
              {
                "label": "Weekly highlights",
                "value": "weekly"
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
            "y": 436
          },
          "props": {
            "height": 120,
            "helpText": "Choose how frequently you want newsletters.",
            "label": "How often would you like to hear from us?",
            "options": [
              {
                "label": "Daily",
                "value": "daily"
              },
              {
                "label": "Weekly",
                "value": "weekly"
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
            "y": 580
          },
          "props": {
            "height": 120,
            "helpText": "By subscribing you agree to receive marketing communications. We handle your personal data in accordance with the Privacy Act 1988 and the Spam Act 2003. See the event terms for details.",
            "label": "Consent to marketing",
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
            "y": 724
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 50770,
  "failure_class": "none",
  "input_tokens": 3216,
  "output_tokens": 5194,
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
            "label": "Thank you for supporting us. Fields marked * are required.",
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
            "helpText": "As you would like it to appear on a receipt.",
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
            "helpText": "Surname or family name.",
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
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We will send donation receipts to this address.",
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
            "helpText": "Optional \u2014 useful for SMS receipts or urgent contact. Include +61 country code for Australian numbers.",
            "label": "Phone",
            "options": [],
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide Suburb, State and Postcode if you want a mailed receipt.",
            "label": "Postal address (for mailed receipts)",
            "options": [],
            "placeholder": "Street address or PO Box",
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
            "helpText": "Choose a preset amount or select Other to enter a specific gift in AUD.",
            "label": "Pledge amount (AUD)",
            "options": [
              {
                "label": "AUD 25",
                "value": "25"
              },
              {
                "label": "AUD 50",
                "value": "50"
              },
              {
                "label": "AUD 100",
                "value": "100"
              },
              {
                "label": "AUD 250",
                "value": "250"
              },
              {
                "label": "Other (enter amount)",
                "value": "other"
              }
            ],
            "placeholder": "Select an amount",
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
            "helpText": "Minimum AUD 1. Enter numbers only, without currency symbols.",
            "label": "Other amount (AUD)",
            "options": [],
            "placeholder": "Enter amount in whole dollars",
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
            "helpText": "Choose whether this is a one-off pledge or recurring.",
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
            "helpText": "Choose how often to charge the recurring pledge.",
            "label": "If recurring, frequency",
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
                "label": "Quarterly",
                "value": "quarterly"
              },
              {
                "label": "Annually",
                "value": "annually"
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
          "id": "radio-11",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Choose how you'd like to receive your donation receipt.",
            "label": "Send receipt via",
            "options": [
              {
                "label": "Email",
                "value": "email"
              },
              {
                "label": "SMS",
                "value": "sms"
              },
              {
                "label": "Post",
                "value": "post"
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
          "id": "text-12",
          "position": {
            "x": 424,
            "y": 776
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 leave blank to use your donor name.",
            "label": "Receipt name (if different)",
            "options": [],
            "placeholder": "Name for the receipt",
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
          "id": "textarea-13",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "This message may appear on receipts or acknowledgements. Up to 1000 characters.",
            "label": "Message or dedication (optional)",
            "options": [],
            "placeholder": "Add a short message, dedication, or note to accompany your pledge",
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
            "y": 1224
          },
          "props": {
            "height": 120,
            "helpText": "You can unsubscribe at any time. We handle your data in line with our privacy policy.",
            "label": "I would like to receive campaign updates and news",
            "options": [
              {
                "label": "Sign me up for email updates",
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
            "y": 1368
          },
          "props": {
            "height": 120,
            "helpText": "By confirming, you consent to our collection and use of personal data to process your donation and provide receipts.",
            "label": "I acknowledge this pledge and agree to the charity\u2019s donation terms and privacy handling.",
            "options": [],
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
            "y": 1512
          },
          "props": {
            "height": 72,
            "label": "Confirm Pledge",
            "options": [],
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 46519,
  "failure_class": "none",
  "input_tokens": 3288,
  "output_tokens": 4647,
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
  "formId": "sydney-donation-pledge",
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
            "label": "Thank you for supporting our Sydney community. Please complete your details below to pledge a donation. Your pledge helps local programs and community services.",
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
            "helpText": "We'll send a tax receipt to this email. Enter an address you check regularly.",
            "label": "Email for receipt",
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
            "helpText": "Provide a phone number with country code if outside Australia. Example: [SCRUBBED_PHONE].",
            "label": "Phone (optional)",
            "placeholder": "+61 4XX XXX XXX",
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
            "helpText": "Please include Suburb, State and Postcode. We use Australian address format where applicable.",
            "label": "Postal address (optional) for mailed receipts",
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
            "helpText": "Select a suggested gift or enter a custom amount.",
            "label": "Choose an amount (AUD)",
            "options": [
              {
                "label": "AUD 25",
                "value": "25"
              },
              {
                "label": "AUD 50",
                "value": "50"
              },
              {
                "label": "AUD 100",
                "value": "100"
              },
              {
                "label": "AUD 250",
                "value": "250"
              },
              {
                "label": "Other (enter below)",
                "value": "other"
              }
            ],
            "placeholder": "Select a suggested amount",
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
            "helpText": "Enter a whole amount in AUD. Minimum AUD 5.",
            "label": "Custom amount (AUD)",
            "placeholder": "Enter whole AUD amount, e.g. 75",
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
            "helpText": "Choose how often you'd like to be charged if you select Recurring.",
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
            "helpText": "By opting in you agree to receive campaign updates and fundraising messages. We handle your personal information in line with the Privacy Act 1988 and comply with the Spam Act 2003. You can unsubscribe at any time.",
            "label": "Yes, I'd like to receive campaign updates and fundraising messages",
            "options": [
              {
                "label": "I agree to receive campaign updates",
                "value": "opt_in"
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
            "helpText": "I confirm my pledge and agree to the event terms and privacy policy.",
            "label": "Agreement and privacy",
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
            "label": "Pledge Donation",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 35567,
  "failure_class": "none",
  "input_tokens": 3298,
  "output_tokens": 4203,
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
            "label": "Your pledge helps fund vital programs and services. All donations are in AUD.",
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
            "helpText": "We will send your receipt to this email if you choose an email receipt.",
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
            "helpText": "Include country code (e.g. +61 for Australia). We may contact you about your pledge.",
            "label": "Phone number",
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
            "helpText": "Include Suburb, State and Postcode. Required only if you request a postal receipt.",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose a preset amount or select Other to enter a custom amount in AUD.",
            "label": "Donation amount (AUD)",
            "options": [
              {
                "label": "AUD 25",
                "value": "25"
              },
              {
                "label": "AUD 50",
                "value": "50"
              },
              {
                "label": "AUD 100",
                "value": "100"
              },
              {
                "label": "Other amount",
                "value": "other"
              }
            ],
            "placeholder": "Select an amount",
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
            "helpText": "Enter a whole number amount in AUD if you selected Other above. Minimum AUD 1.",
            "label": "Other amount (AUD)",
            "placeholder": "Enter amount in AUD",
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
          "id": "radio-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Choose One-off or a recurring schedule.",
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
                "label": "Quarterly",
                "value": "quarterly"
              },
              {
                "label": "Annually",
                "value": "annually"
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
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 110,
            "helpText": "Select Email (recommended) or Postal. If Postal, please provide your postal address above.",
            "label": "Receipt preference",
            "options": [
              {
                "label": "Email receipt",
                "value": "email"
              },
              {
                "label": "Postal receipt",
                "value": "postal"
              }
            ],
            "placeholder": "How would you like to receive your receipt?",
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
            "y": 910
          },
          "props": {
            "height": 120,
            "helpText": "Yes \u2014 send me updates about this campaign and future appeals. You can unsubscribe at any time. Communications will follow the Privacy Act 1988 and the Spam Act 2003.",
            "label": "Campaign updates",
            "options": [
              {
                "label": "I agree to receive campaign updates and appeals",
                "value": "subscribe"
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
            "y": 1054
          },
          "props": {
            "height": 120,
            "helpText": "By pledging you agree to our event terms and privacy practices.",
            "label": "Acknowledgement and terms",
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
            "y": 1198
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 36176,
  "failure_class": "none",
  "input_tokens": 3212,
  "output_tokens": 4280,
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
  "formId": "international-event-registration-au",
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
            "label": "Please provide your details and select the sessions you'd like to attend.",
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
            "helpText": "We'll send your registration confirmation to this address.",
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
            "helpText": "Include country code, e.g. +61 for Australia. We may contact you about event updates.",
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
            "helpText": "Country of residence",
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
            "helpText": "Choose the timezone where you'll attend from. Dates are shown as DD/MM/YYYY.",
            "label": "Timezone",
            "options": [
              {
                "label": "UTC\u221212:00",
                "value": "UTC-12:00"
              },
              {
                "label": "UTC\u221211:00",
                "value": "UTC-11:00"
              },
              {
                "label": "UTC\u221210:00",
                "value": "UTC-10:00"
              },
              {
                "label": "UTC\u221208:00 (Pacific)",
                "value": "UTC-08:00"
              },
              {
                "label": "UTC+00:00 (London)",
                "value": "UTC+00:00"
              },
              {
                "label": "UTC+08:00 (Beijing, Perth)",
                "value": "UTC+08:00"
              },
              {
                "label": "UTC+10:00 (Sydney)",
                "value": "UTC+10:00"
              },
              {
                "label": "UTC+11:00 (Norfolk/Solomon Is.)",
                "value": "UTC+11:00"
              },
              {
                "label": "Other / IANA timezone",
                "value": "OTHER_TZ"
              }
            ],
            "placeholder": "Select your timezone (UTC offset)",
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
            "helpText": "Select one or more sessions you'd like to attend.",
            "label": "Sessions you're interested in",
            "options": [
              {
                "label": "Keynote",
                "value": "keynote"
              },
              {
                "label": "Workshop: Data & AI",
                "value": "workshop_data_ai"
              },
              {
                "label": "Workshop: Product",
                "value": "workshop_product"
              },
              {
                "label": "Networking session",
                "value": "networking"
              },
              {
                "label": "Technical deep-dive",
                "value": "technical"
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
            "helpText": "Tell us about any accessibility needs, dietary preferences (e.g. vegetarian) or other notes.",
            "label": "Special requirements or questions",
            "placeholder": "Dietary requirements, accessibility needs, or questions for organisers",
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
            "helpText": "You may withdraw consent at any time. For questions about data handling, contact the event organiser.",
            "label": "I consent to receive event updates and accept the privacy notice. I understand my personal data will be used to manage my registration and to send relevant communications under the Privacy Act 1988 and the Spam Act 2003.",
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
            "helpText": "By registering you confirm the details provided are correct.",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 42548,
  "failure_class": "none",
  "input_tokens": 3284,
  "output_tokens": 4939,
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
  "formId": "event-registration-sydney",
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
            "helpText": "This event is based in Sydney. Please select your local timezone so we can schedule sessions and send calendar invites in your local time.",
            "label": "Event location",
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
            "placeholder": "Family name / surname",
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
            "helpText": "We will send booking confirmations and session links to this address.",
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
            "helpText": "Include country code (e.g. +61 for Australia). We may call or SMS with urgent event updates.",
            "label": "Phone",
            "placeholder": "+61 2 9XXXXXXX",
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
            "helpText": "Where you are based for this registration.",
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
                "label": "Japan",
                "value": "JP"
              },
              {
                "label": "China",
                "value": "CN"
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
            "helpText": "Select the timezone where you will attend from. If you are in Sydney choose Australia/Sydney (AEST/AEDT).",
            "label": "Timezone",
            "options": [
              {
                "label": "Australia/Sydney \u2014 AEST / AEDT (Sydney local time)",
                "value": "Australia/Sydney"
              },
              {
                "label": "UTC \u2014 Coordinated Universal Time",
                "value": "UTC"
              },
              {
                "label": "America/New_York \u2014 Eastern Time (US & Canada)",
                "value": "America/New_York"
              },
              {
                "label": "Europe/London \u2014 British Summer Time / GMT",
                "value": "Europe/London"
              },
              {
                "label": "Asia/Kolkata \u2014 India Standard Time",
                "value": "Asia/Kolkata"
              },
              {
                "label": "Asia/Tokyo \u2014 Japan Standard Time",
                "value": "Asia/Tokyo"
              },
              {
                "label": "Other (select closest)",
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
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Organisation (optional)",
            "placeholder": "Company or organisation",
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
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Select all sessions you'd like to attend. We'll confirm availability and session capacity after registration.",
            "label": "Sessions you are interested in",
            "options": [
              {
                "label": "Opening keynote \u2014 Sydney time slot",
                "value": "keynote_sydney"
              },
              {
                "label": "Workshop A: Cloud & Infrastructure",
                "value": "workshop_cloud"
              },
              {
                "label": "Workshop B: Data & AI",
                "value": "workshop_data"
              },
              {
                "label": "Panel: Global collaboration",
                "value": "panel_global"
              },
              {
                "label": "Networking session",
                "value": "networking"
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
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "Please tell us about any needs so we can accommodate you.",
            "label": "Special requirements or comments",
            "placeholder": "Dietary needs, accessibility requests or other notes",
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
            "y": 1080
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and the handling of my personal data as described in the event terms.",
            "label": "Terms & privacy",
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
            "y": 1224
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive event updates and occasional marketing about related events. You can unsubscribe at any time.",
            "label": "Marketing & updates (optional)",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and related offers",
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
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1368
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
      "title": "International Event Registration \u2014 Sydney"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 44020,
  "failure_class": "none",
  "input_tokens": 3294,
  "output_tokens": 5137,
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
  "formId": "event-registration-international",
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
            "helpText": "Select sessions, provide contact details, and accept the event terms to register.",
            "label": "Event details",
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
            "helpText": "We'll send your registration confirmation to this address.",
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
            "helpText": "Include your country code (e.g. +61 for Australia).",
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
                "label": "Germany",
                "value": "DE"
              },
              {
                "label": "France",
                "value": "FR"
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
            "helpText": "Choose the timezone you usually use for meeting times.",
            "label": "Timezone",
            "options": [
              {
                "label": "UTC+11:00 (AEDT - Sydney)",
                "value": "UTC+11"
              },
              {
                "label": "UTC+10:00 (AEST - Brisbane/Sydney standard)",
                "value": "UTC+10"
              },
              {
                "label": "UTC+09:00 (Japan)",
                "value": "UTC+09"
              },
              {
                "label": "UTC+05:30 (India)",
                "value": "UTC+05:30"
              },
              {
                "label": "UTC+01:00 (CET - Berlin/Paris)",
                "value": "UTC+01"
              },
              {
                "label": "UTC+00:00 (GMT)",
                "value": "UTC+00"
              },
              {
                "label": "UTC-05:00 (EST - New York/Toronto)",
                "value": "UTC-05"
              },
              {
                "label": "UTC-08:00 (PST - Los Angeles)",
                "value": "UTC-08"
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
          "id": "address-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Include Suburb, State and Postcode where applicable.",
            "label": "Street address",
            "placeholder": "Street address, Suburb, State",
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
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "4-digit Australian Postcode if applicable.",
            "label": "Postcode",
            "placeholder": "e.g. 2000",
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
            "y": 766
          },
          "props": {
            "height": 120,
            "helpText": "Select all sessions you plan to attend.",
            "label": "Sessions interested in",
            "options": [
              {
                "label": "Keynote",
                "value": "keynote"
              },
              {
                "label": "Workshop A: Data & AI",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B: Product Design",
                "value": "workshop_b"
              },
              {
                "label": "Panel discussion",
                "value": "panel"
              },
              {
                "label": "Networking session",
                "value": "networking"
              },
              {
                "label": "Virtual attendance",
                "value": "virtual"
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
            "y": 910
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive event updates and promotional emails. You can unsubscribe at any time.",
            "label": "Marketing and event updates",
            "options": [
              {
                "label": "Yes, I want to receive event updates and promotional emails",
                "value": "opt_in"
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
            "y": 1054
          },
          "props": {
            "height": 120,
            "helpText": "Please accept the event terms and privacy policy to complete registration.",
            "label": "Terms & privacy",
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
            "y": 1198
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 47226,
  "failure_class": "none",
  "input_tokens": 3214,
  "output_tokens": 5002,
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
    "height": 1806,
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
            "label": "Please provide your contact details and review the data handling and consent statements. We collect personal information to manage registrations and communicate event details under the Privacy Act 1988.",
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
            "helpText": "We will send confirmation and tickets to this address.",
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
            "helpText": "Include country code (+61) for Australian numbers.",
            "label": "Mobile or phone",
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
            "label": "Job title",
            "placeholder": "Your role",
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
            "helpText": "Use Suburb, State and Postcode for Australian addresses.",
            "label": "Postal address",
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
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 632
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
                "label": "VIP",
                "value": "vip"
              },
              {
                "label": "Student (ID required)",
                "value": "student"
              }
            ],
            "placeholder": "Select ticket type",
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
          "id": "date-10",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Use DD/MM/YYYY format.",
            "label": "Attendance date",
            "placeholder": "DD/MM/YYYY",
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
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about allergies or intolerances.",
            "label": "Dietary requirements",
            "placeholder": "Vegetarian, gluten-free, allergies...",
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
            "y": 1070
          },
          "props": {
            "height": 200,
            "helpText": "If you need assistance, tell us how we can help you attend.",
            "label": "Accessibility or support needs",
            "placeholder": "Let us know any access requirements",
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
            "y": 1374
          },
          "props": {
            "height": 120,
            "helpText": "Required to complete registration.",
            "label": "Data handling and lawful-basis acknowledgement: By registering you consent to the collection and use of your personal information for event administration, ticketing and communications under the Privacy Act 1988. You acknowledge that processing is necessary for contractual performance and for our legitimate interests in managing the event and ensuring safety. Marketing communications will only be sent with separate opt\u2011in. We will handle your data in accordance with the Privacy Act and the Spam Act 2003.",
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
            "y": 1518
          },
          "props": {
            "height": 120,
            "helpText": "Optional \u2014 not required to register.",
            "label": "Marketing preferences (optional)",
            "options": [
              {
                "label": "I agree to receive event updates and occasional marketing by email or SMS. I understand I may opt out at any time.",
                "value": "opt_in"
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
            "y": 1662
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
      "title": "Event registration \u2014 Privacy & consent"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 49104,
  "failure_class": "none",
  "input_tokens": 3286,
  "output_tokens": 5713,
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
            "helpText": "We collect the personal information you provide to manage your registration and attendance. If you are resident in the EU, your data will be processed in line with the GDPR; otherwise we process personal information in accordance with the Privacy Act 1988 and the Spam Act 2003. See the event terms for full privacy and cross-border transfer details.",
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
            "helpText": "Include country code (use +61 for Australia). We may call or SMS for urgent event updates.",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Please include Suburb, State and Postcode. Country is optional if same as event location.",
            "label": "Address",
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
          "id": "radio-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select 'Yes' if your usual residence is inside the EU \u2014 this helps us apply GDPR rules to your data.",
            "label": "Are you resident in the European Union?",
            "options": [
              {
                "label": "Yes \u2014 I am resident in the EU",
                "value": "eu_resident"
              },
              {
                "label": "No \u2014 I am not resident in the EU",
                "value": "not_eu"
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
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Choose the lawful basis that applies to your registration. If unsure, select 'Consent'.",
            "label": "Lawful basis for processing personal data",
            "options": [
              {
                "label": "Consent",
                "value": "consent"
              },
              {
                "label": "Contract (to fulfil registration and attendance)",
                "value": "contract"
              },
              {
                "label": "Legal obligation",
                "value": "legal_obligation"
              },
              {
                "label": "Legitimate interests",
                "value": "legitimate_interests"
              },
              {
                "label": "Other lawful basis",
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
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "I explicitly consent to the processing of my personal data for event administration and for the purposes described in the data notice and event terms. If you are an EU resident, this consent will be handled under the GDPR.",
            "label": "Explicit GDPR consent (required if Consent is selected)",
            "options": [
              {
                "label": "I give explicit consent for processing my personal data as described",
                "value": "gdpr_consent"
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
            "y": 786
          },
          "props": {
            "height": 120,
            "helpText": "Optional: agree to receive news, offers and marketing about future events. You can opt out at any time.",
            "label": "Marketing & event updates (optional)",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and marketing by email",
                "value": "marketing_email"
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
            "y": 930
          },
          "props": {
            "height": 120,
            "helpText": "Please read and accept the event terms and privacy information. The event terms include details on data transfers, retention and your rights under applicable law.",
            "label": "Event terms and privacy",
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
            "y": 1074
          },
          "props": {
            "height": 72,
            "helpText": "By registering you confirm the details above and accept the event terms.",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 42689,
  "failure_class": "none",
  "input_tokens": 3296,
  "output_tokens": 4564,
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
  "formId": "eu-event-registration-au-localised",
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
            "helpText": "We collect the personal data shown on this form to manage your registration and communicate event updates. Our handling practices are governed by the Privacy Act 1988 and relevant Australian law. See the event terms for full details.",
            "label": "Data handling notice",
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
            "helpText": "We will use this for booking confirmations and event updates.",
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
            "helpText": "Include the country code (for AU, use +61). We use this only to contact you about your registration.",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide Suburb, State and Postcode for postal correspondence. (Form localised to Australian address fields.)",
            "label": "Postal address",
            "placeholder": "Street address, Suburb, State, Postcode",
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
          "id": "textarea-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 200,
            "helpText": "We will use this information to make reasonable adjustments for the event.",
            "label": "Accessibility or special requirements",
            "placeholder": "Tell us about any access needs, dietary requirements, or other support we should plan for",
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
            "helpText": "I acknowledge that my personal data will be processed to manage my registration and for event administration in accordance with the Privacy Act 1988 and the event terms.",
            "label": "Acknowledgement of data handling",
            "options": [
              {
                "label": "I acknowledge the data handling notice and agree to processing for registration purposes",
                "value": "ack_data_handling"
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
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "Tick to receive occasional updates about this event and related events. You can unsubscribe at any time. Communications are subject to the Spam Act 2003.",
            "label": "Marketing & communications consent (optional)",
            "options": [
              {
                "label": "Yes \u2014 I agree to receive marketing and event updates",
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
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "You must accept the event terms and privacy information to complete registration.",
            "label": "Terms & privacy",
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
            "y": 1234
          },
          "props": {
            "height": 72,
            "label": "Complete registration",
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
      "title": "Event registration (EU event) \u2014 registration and data acknowledgements"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 32837,
  "failure_class": "none",
  "input_tokens": 3216,
  "output_tokens": 3534,
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
            "label": "Tell us a little about yourself and your interest in onboarding with us. We'll only use your details to contact you about this process.",
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
            "helpText": "We'll contact you at this address about onboarding.",
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
            "helpText": "Include country code, e.g. +61",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Organisation",
            "placeholder": "Company or group (optional)",
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
          "id": "dropdown-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "What best describes your role in relation to onboarding?",
            "label": "Role / Position",
            "options": [
              {
                "label": "Attendee / Participant",
                "value": "attendee"
              },
              {
                "label": "Speaker / Presenter",
                "value": "speaker"
              },
              {
                "label": "Sponsor / Partner",
                "value": "sponsor"
              },
              {
                "label": "Vendor / Supplier",
                "value": "vendor"
              },
              {
                "label": "Volunteer",
                "value": "volunteer"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select your role",
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
          "id": "address-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Please include Suburb, State and Postcode.",
            "label": "Address",
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
          "id": "date-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "If known, use DD/MM/YYYY.",
            "label": "Available start date",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 200,
            "label": "Tell us about your interest or relevant experience",
            "placeholder": "Briefly describe why you\u2019re interested and any relevant experience",
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
            "y": 1070
          },
          "props": {
            "height": 120,
            "helpText": "Select if you\u2019d like to receive event updates and marketing communications.",
            "label": "Event updates and marketing",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and marketing",
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
            "y": 1214
          },
          "props": {
            "height": 120,
            "helpText": "You can contact us to update your preferences or request access to your information.",
            "label": "I acknowledge and agree that my personal information will be collected and used for onboarding and communications in accordance with the Privacy Act 1988 and the Spam Act 2003. I consent to being contacted about this onboarding process.",
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
            "label": "Register interest",
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 39100,
  "failure_class": "none",
  "input_tokens": 3288,
  "output_tokens": 4144,
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
  "formId": "onboarding-interest-sydney",
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
            "label": "We\u2019ll use these details to contact you about the Sydney event. Providing your contact details lets us share onboarding steps, event updates and relevant opportunities.",
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
            "placeholder": "e.g. Jamie",
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
            "helpText": "We\u2019ll use this to send event information and important updates.",
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
            "helpText": "Include the country code (e.g. +61) \u2014 we may send SMS updates.",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Organisation",
            "placeholder": "e.g. Acme Pty Ltd",
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
          "id": "dropdown-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose the option that best describes your primary role.",
            "label": "Role",
            "options": [
              {
                "label": "Developer / Engineer",
                "value": "developer"
              },
              {
                "label": "Product manager",
                "value": "product_manager"
              },
              {
                "label": "Designer",
                "value": "designer"
              },
              {
                "label": "Marketing / Communications",
                "value": "marketing"
              },
              {
                "label": "Operations / HR",
                "value": "operations_hr"
              },
              {
                "label": "Student / Early career",
                "value": "student"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select your role",
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
          "id": "address-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Please provide Suburb, State and Postcode (Australian format).",
            "label": "Address",
            "placeholder": "Street address",
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
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Select any that apply.",
            "label": "How would you like to be involved?",
            "options": [
              {
                "label": "Attending the onboarding session",
                "value": "attend"
              },
              {
                "label": "Speaking or presenting",
                "value": "speak"
              },
              {
                "label": "Volunteering or helping run sessions",
                "value": "volunteer"
              },
              {
                "label": "Sponsorship or partnership",
                "value": "sponsor"
              },
              {
                "label": "Other",
                "value": "other_involvement"
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
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms and to the handling of my personal data for event administration and marketing in line with the Privacy Act 1988 and the Spam Act 2003.",
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
            "y": 920
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
- Definition source: `unavailable`

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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "component_count": 0,
  "duration_ms": 9649,
  "failure_class": "provider-fault",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": false,
  "terminal_reason": "provider-error",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "warning": "generated definition unavailable in local artifacts"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
    "matched_text": "NHS",
    "prompt_id": "p14-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "NHS",
    "prompt_id": "p14-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "NHS",
    "prompt_id": "p14-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "NHS",
    "prompt_id": "p14-au-neutral-r1",
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
  "duration_ms": 46352,
  "failure_class": "none",
  "input_tokens": 3213,
  "output_tokens": 4737,
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
            "label": "Please provide your details, relevant health information, and an emergency contact. If you were directed by UK NHS guidance, note that this form is localised for Australian use \u2014 include any UK-specific notes in Health Notes and contact the organisers for NHS-specific advice.",
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
            "helpText": "Enter date in DD/MM/YYYY format",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Use Suburb, State and Postcode for Australian addresses",
            "label": "Address (Street, Suburb, State, Postcode)",
            "placeholder": "Street address, Suburb, State, Postcode",
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
          "id": "phone-6",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Best contact number. Use +61 for Australia.",
            "label": "Phone (participant)",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "email-7",
          "position": {
            "x": 384,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Optional. We'll use this for event updates if provided.",
            "label": "Email (participant)",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "text-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "placeholder": "Full name",
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
          "id": "text-9",
          "position": {
            "x": 384,
            "y": 632
          },
          "props": {
            "height": 110,
            "label": "Relation to participant",
            "placeholder": "e.g. Partner, Parent, Friend",
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
          "id": "phone-10",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 110,
            "helpText": "Primary number for emergency contact. Use +61 for Australia.",
            "label": "Emergency contact phone",
            "placeholder": "+61 4xx xxx xxx",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "email-11",
          "position": {
            "x": 384,
            "y": 766
          },
          "props": {
            "height": 110,
            "helpText": "Optional secondary contact.",
            "label": "Emergency contact email",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 11,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 900
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply. If none, leave blank.",
            "label": "Please indicate any of the following that apply",
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
                "label": "Severe allergies (e.g. anaphylaxis)",
                "value": "allergies"
              },
              {
                "label": "Regular medication",
                "value": "medication"
              },
              {
                "label": "Pregnancy",
                "value": "pregnancy"
              },
              {
                "label": "Other \u2014 see notes below",
                "value": "other"
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
            "y": 1044
          },
          "props": {
            "height": 200,
            "helpText": "Include medication names and dosages where relevant.",
            "label": "Health notes \u2014 allergies, medications, details",
            "placeholder": "List conditions, medications, allergies, emergency medication (e.g. EpiPen), and any other relevant information.",
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
          "id": "radio-14",
          "position": {
            "x": 40,
            "y": 1348
          },
          "props": {
            "height": 120,
            "helpText": "Consent allows authorised medical personnel to provide necessary emergency care.",
            "label": "Do you consent to emergency medical treatment if required?",
            "options": [
              {
                "label": "Yes, I consent",
                "value": "yes"
              },
              {
                "label": "No, I do not consent",
                "value": "no"
              }
            ],
            "tabOrder": 14,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 360
          },
          "type": "radio"
        },
        {
          "id": "terms-15",
          "position": {
            "x": 40,
            "y": 1492
          },
          "props": {
            "height": 120,
            "helpText": "By submitting you consent to collection and handling of personal and health information for event safety and medical purposes in accordance with the Privacy Act 1988. You may receive event updates in accordance with the Spam Act 2003. If you require UK NHS-specific handling, note that this form is localised for AU \u2014 contact the organisers for NHS-specific arrangements.",
            "label": "Waiver & consent: I confirm that the information I have provided is accurate to the best of my knowledge. I accept the risks associated with participation and consent to the organisers arranging medical treatment if required.",
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
          "id": "date-16",
          "position": {
            "x": 40,
            "y": 1636
          },
          "props": {
            "height": 110,
            "helpText": "Enter the date you are signing this form (DD/MM/YYYY).",
            "label": "Date of consent",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 16,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "submit-button-17",
          "position": {
            "x": 40,
            "y": 1770
          },
          "props": {
            "height": 72,
            "label": "I agree and submit",
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
      "title": "Event Waiver & Health Consent (AU)"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
    "matched_text": "NHS",
    "prompt_id": "p14-au-ambiguous-r1",
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
  "component_count": 15,
  "duration_ms": 52531,
  "failure_class": "none",
  "input_tokens": 3285,
  "output_tokens": 4533,
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
  "formId": "sydney-waiver-au",
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
            "helpText": "This form requests personal and health information for participation in a Sydney event. You asked for UK NHS\u2013style clinical details; that cue is acknowledged here, but legal framing and data handling follow Australian standards (Privacy Act 1988, Spam Act 2003).",
            "label": "Event and Health Information",
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
            "helpText": "Use DD/MM/YYYY format.",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include Suburb, State and Postcode.",
            "label": "Residential address",
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
          "id": "phone-6",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Provide a number we can use in an emergency. Include +61 for Australian numbers.",
            "label": "Mobile phone",
            "placeholder": "[SCRUBBED_PHONE]",
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
          "id": "email-7",
          "position": {
            "x": 384,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "We may send event updates by email (Spam Act 2003 applies).",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 7,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Select any current conditions that organisers should be aware of.",
            "label": "Relevant health conditions (tick all that apply)",
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
                "label": "Allergies (including anaphylaxis)",
                "value": "allergies"
              },
              {
                "label": "Mobility or assistance needs",
                "value": "mobility_assistance"
              },
              {
                "label": "None of the above",
                "value": "none"
              },
              {
                "label": "Other (see notes)",
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
            "helpText": "Include medication names, recent injuries, and any triggers. Do not include Medicare or insurance numbers.",
            "label": "Health details, medications and limitations",
            "placeholder": "Describe current health conditions, regular medications, allergies, or special assistance you need.",
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
          "id": "phone-11",
          "position": {
            "x": 384,
            "y": 1080
          },
          "props": {
            "height": 110,
            "helpText": "Include country code (+61) for Australian numbers.",
            "label": "Emergency contact phone",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 11,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "radio-12",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 120,
            "label": "Relationship to participant",
            "options": [
              {
                "label": "Spouse / Partner",
                "value": "partner"
              },
              {
                "label": "Parent / Guardian",
                "value": "parent_guardian"
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
            "y": 1358
          },
          "props": {
            "height": 120,
            "helpText": "Tick to authorise event staff to contact this person if required and to act in your best interests in an emergency.",
            "label": "Authorisation",
            "options": [
              {
                "label": "I authorise event staff to contact my emergency contact and to provide necessary information to assist in my care.",
                "value": "authorise_contact"
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
            "y": 1502
          },
          "props": {
            "height": 120,
            "helpText": "Please review the event terms and consent to the collection and use of your personal and health information for safety and administration. Data handling follows the Privacy Act 1988.",
            "label": "Waiver, consent and data acknowledgement",
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
            "y": 1646
          },
          "props": {
            "height": 72,
            "label": "Sign & Submit",
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
      "title": "Participant Waiver & Consent \u2014 Sydney"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "component_count": 18,
  "duration_ms": 96738,
  "failure_class": "none",
  "input_tokens": 8501,
  "output_tokens": 8742,
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
    "height": 2460,
    "width": 960
  },
  "formId": "event-waiver-health-form",
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
            "helpText": "By signing you acknowledge the risks associated with participation, confirm the accuracy of the health information provided, and consent to the event's safety procedures. Personal data will be handled in accordance with the Privacy Act 1988 and communications subject to the Spam Act 2003.",
            "label": "Waiver summary",
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
            "helpText": "Enter date of birth in DD/MM/YYYY format.",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide street address, Suburb, State and Postcode.",
            "label": "Address",
            "placeholder": "Street address, Suburb, State, Postcode",
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
            "helpText": "We will use this to send confirmation and important event updates.",
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
          "id": "phone-7",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Include country code (e.g. +61) and the best number to reach you.",
            "label": "Phone",
            "placeholder": "+61 4xx xxx xxx",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "paragraph-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 48,
            "helpText": "Provide someone we can contact if there is an incident.",
            "label": "Emergency contact",
            "tabOrder": 8,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "text-9",
          "position": {
            "x": 40,
            "y": 704
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
            "y": 704
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
                "value": "parent_guardian"
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
            "y": 838
          },
          "props": {
            "height": 110,
            "helpText": "Include country code (e.g. +61).",
            "label": "Emergency contact phone",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 972
          },
          "props": {
            "height": 200,
            "helpText": "Include conditions that may affect participation or require special attention.",
            "label": "Relevant medical conditions",
            "placeholder": "Describe any medical conditions we should be aware of",
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
            "y": 1276
          },
          "props": {
            "height": 200,
            "label": "Allergies",
            "placeholder": "List any allergies (e.g. food, medication, insect bites)",
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
          "id": "textarea-14",
          "position": {
            "x": 40,
            "y": 1580
          },
          "props": {
            "height": 200,
            "helpText": "Include dosage and frequency where relevant.",
            "label": "Current medications",
            "placeholder": "List any medications taken regularly",
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
            "y": 1884
          },
          "props": {
            "height": 120,
            "label": "I confirm the information I have provided is true and complete to the best of my knowledge",
            "options": [
              {
                "label": "I confirm the information I have provided is true and complete to the best of my knowledge",
                "value": "confirm_accuracy"
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
            "y": 2028
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the waiver and acknowledge the event terms. Personal information will be handled under the Privacy Act 1988. Communications may be sent under the Spam Act 2003.",
            "label": "Waiver & consent (required)",
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
          "id": "checkbox-17",
          "position": {
            "x": 40,
            "y": 2172
          },
          "props": {
            "height": 120,
            "helpText": "Optional \u2014 you can unsubscribe at any time.",
            "label": "I consent to receive event updates and marketing communications",
            "options": [
              {
                "label": "Yes, I consent to receive event updates and marketing communications",
                "value": "consent_marketing"
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
          "id": "submit-button-18",
          "position": {
            "x": 40,
            "y": 2316
          },
          "props": {
            "height": 72,
            "label": "Sign & Submit",
            "tabOrder": 18,
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
      "title": "Event Waiver & Health Form (Australia-localised)"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 46755,
  "failure_class": "none",
  "input_tokens": 3215,
  "output_tokens": 4520,
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
    "height": 1816,
    "width": 960
  },
  "formId": "rsvp-nz-event",
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
            "label": "We look forward to welcoming you. Complete this form to RSVP. If you need help, contact the organiser.",
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
            "placeholder": "e.g. Jane",
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
            "helpText": "We'll use this to send your RSVP confirmation and event information.",
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
            "helpText": "Provide a number we can reach you on for event updates if needed.",
            "label": "Phone number",
            "placeholder": "Include country code, e.g. [SCRUBBED_PHONE]",
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
            "helpText": "Select the region closest to you (this helps planning and local communications).",
            "label": "Region",
            "options": [
              {
                "label": "North Island",
                "value": "north_island"
              },
              {
                "label": "South Island",
                "value": "south_island"
              },
              {
                "label": "Other / Overseas",
                "value": "other"
              },
              {
                "label": "Prefer not to say",
                "value": "prefer_not_to_say"
              }
            ],
            "placeholder": "Select region",
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
          "id": "number-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter how many people will attend with this RSVP.",
            "label": "Number of attendees (including you)",
            "placeholder": "1",
            "tabOrder": 7,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 220
          },
          "type": "number"
        },
        {
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes, I will attend",
                "value": "attending"
              },
              {
                "label": "No, I cannot attend",
                "value": "not_attending"
              },
              {
                "label": "Maybe / Unsure",
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
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Choose any that apply. If you select 'Other', please describe below.",
            "label": "Dietary requirements (select all that apply)",
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
            "y": 920
          },
          "props": {
            "height": 200,
            "label": "Dietary details (if Other selected)",
            "placeholder": "Please describe any specific requirements or allergies",
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
            "y": 1224
          },
          "props": {
            "height": 200,
            "helpText": "We may contact you to discuss adjustments to ensure you can attend comfortably.",
            "label": "Accessibility requirements",
            "placeholder": "Tell us about any mobility, hearing, vision or other accessibility needs",
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
            "y": 1528
          },
          "props": {
            "height": 120,
            "helpText": "You can opt out of marketing communications at any time. Contact the organiser for privacy inquiries.",
            "label": "I consent to receive event updates and agree that my contact details will be used to send event communications. I understand how my personal information will be handled in accordance with the Privacy Act 1988 and the Spam Act 2003.",
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
            "y": 1672
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 52521,
  "failure_class": "none",
  "input_tokens": 3287,
  "output_tokens": 4833,
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
    "height": 1816,
    "width": 960
  },
  "formId": "nz-rsvp-sydney",
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
            "helpText": "Fill in the form below. Times and venue details will be sent to the email you provide.",
            "label": "Event details",
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
            "helpText": "We will send confirmation and event updates here.",
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
            "helpText": "Include +61 country code where possible so we can contact you about last-minute changes.",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose your state or region. If you are in New Zealand, choose Other.",
            "label": "State / Region",
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
                "label": "Other (including New Zealand)",
                "value": "other"
              }
            ],
            "placeholder": "Select state or region",
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
            "helpText": "Provide Suburb, State and Postcode if you want a postal confirmation.",
            "label": "Address (optional)",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 632
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
          "id": "number-9",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Enter additional people in your party (not including yourself). Max 10.",
            "label": "Number of additional guests",
            "placeholder": "0",
            "tabOrder": 9,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "number"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 776
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
            "label": "If other, please specify dietary needs",
            "placeholder": "Please detail any specific dietary requirements",
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
            "y": 1224
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about any adjustments we can make to support your attendance.",
            "label": "Accessibility or support needs",
            "placeholder": "E.g. mobility access, hearing support, carer assistance",
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
            "y": 1528
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive event updates and related communications about this event. Message rates may apply.",
            "label": "Consent to receive event updates",
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
            "y": 1672
          },
          "props": {
            "height": 72,
            "label": "RSVP",
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
      "title": "New Zealand RSVP \u2014 Sydney event"
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
    "content_hash": "67b67f85fad5f55bd5fa2acce6af747429588ac936d3ade8042d45495a35bb22",
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
  "duration_ms": 46633,
  "failure_class": "none",
  "input_tokens": 3297,
  "output_tokens": 4413,
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
    "height": 1672,
    "width": 960
  },
  "formId": "nz-rsvp-form",
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
            "label": "Tell us who is attending and any needs we should be aware of. We'll only use your details for event administration and updates.",
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
            "helpText": "We will send your RSVP confirmation to this address.",
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
            "helpText": "Include your country code, e.g. +61 for Australia. We'll use this to contact you about the event.",
            "label": "Phone number",
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
            "helpText": "Provide Suburb, State and Postcode for correspondence if required.",
            "label": "Postal address",
            "placeholder": "Street address, Suburb, State, Postcode",
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
            "helpText": "Select the State or Territory.",
            "label": "Region / State",
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
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter your postcode (4 digits).",
            "label": "Postcode",
            "placeholder": "Postcode",
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
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Select any dietary needs we should plan for.",
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
                "label": "Other (please specify)",
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
            "y": 776
          },
          "props": {
            "height": 200,
            "label": "If other, please specify",
            "placeholder": "Please specify any other dietary requirements",
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
            "y": 1080
          },
          "props": {
            "height": 200,
            "helpText": "Tell us any accessibility requirements so we can make arrangements.",
            "label": "Accessibility needs",
            "placeholder": "E.g. mobility access, seating assistance, hearing loop",
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
            "y": 1384
          },
          "props": {
            "height": 120,
            "helpText": "By agreeing, you consent to receiving event updates. Read our event terms and privacy information.",
            "label": "I agree to receive event updates and related communications",
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
            "y": 1528
          },
          "props": {
            "height": 72,
            "label": "RSVP",
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
