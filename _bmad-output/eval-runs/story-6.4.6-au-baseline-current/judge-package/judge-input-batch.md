# Form AI Judge Input Batch

Run ID: `story-6.4.6-au-baseline-current`
Benchmark set: `prompts-au-v1`
Rubric version: `rubric_v2`

Use `rubric_v2.md` and return JSON matching `judge-output-template.json`.
Set `judge_model_version` to the exact model/version shown in your Cursor session.
Before assigning scores for each row, identify at least one weakness per row before scoring.
Use `shared-context-bundle.json` to inspect prompt/context sections. Fill the diagnostic fields for conflicts, likely responsible section IDs, suggested correction, and confidence.
Judge only the anonymised package content below.

## Row 1: `p01-au-neutral-r1__r01`

- Prompt ID: `p01-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 42968,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
          "id": "textarea-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 200,
            "helpText": "Let us know any dietary restrictions or allergies. We'll do our best to accommodate.",
            "label": "Dietary requirements",
            "placeholder": "e.g. vegetarian, gluten-free, any allergies",
            "tabOrder": 5,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 596
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
            "placeholder": "Select a size",
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
          "id": "submit-button-7",
          "position": {
            "x": 40,
            "y": 730
          },
          "props": {
            "height": 72,
            "label": "Register",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "eb33f6b3f9f811c7eeb3c79182f591e3234af6eaa69e8bf0649313cd118e1311",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 52218,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "annual-sales-conference-sydney-reg",
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
            "helpText": "Please ensure your travel plans align with the event location.",
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
            "helpText": "Include country code if travelling from overseas.",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "T-shirts are provided on a first-come, first-served basis.",
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
            "placeholder": "Select your preferred size",
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
            "helpText": "Please list any allergies, intolerances or dietary preferences.",
            "label": "Dietary requirements",
            "placeholder": "e.g. Vegetarian, nut allergy, gluten-free, no restrictions",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "9611ff54199c422db13e93df74a8be37c7baf6b426a46e5730a69edf479894d8",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p01-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p01-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p01-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p01-au-adversarial-r1",
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
  "duration_ms": 80245,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please complete the form below to register for the conference.",
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
            "helpText": "Please include the +1 country code.",
            "label": "Phone (+1)",
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
            "label": "ZIP code",
            "placeholder": "e.g., 94103",
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
            "helpText": "Select all that apply. Choose Other to provide details below.",
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
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Other",
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
            "y": 642
          },
          "props": {
            "height": 200,
            "label": "Dietary details (if Other)",
            "placeholder": "Please describe any other dietary needs",
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
            "label": "By registering, I agree to the event terms.",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "7a9f267af8abbadc3d1488d6224dedb93b77047314b62799bd11cc83829dcd4a",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 51557,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "conference-rsvp",
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
            "label": "Provide your attendee details, choose the session you'll attend, tell us about any dietary needs, and confirm consent to receive event updates.",
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
            "helpText": "As you would like it to appear on your badge.",
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
            "helpText": "We'll send your confirmation and event updates to this address.",
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
            "helpText": "Optional \u2014 used only for urgent event communications.",
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
            "helpText": "Optional \u2014 for name badge and networking.",
            "label": "Organization / Company",
            "placeholder": "Your organisation (optional)",
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
            "helpText": "Select the single session you plan to attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Opening Keynote",
                "value": "opening_keynote"
              },
              {
                "label": "AI for Business",
                "value": "ai_for_business"
              },
              {
                "label": "Design Workshop",
                "value": "design_workshop"
              },
              {
                "label": "Networking Lunch",
                "value": "networking_lunch"
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
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "Select any dietary needs. If you have multiple or an allergy, choose 'Other' and specify below.",
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
                "label": "Kosher",
                "value": "kosher"
              },
              {
                "label": "Halal",
                "value": "halal"
              },
              {
                "label": "Other (please specify)",
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
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "Include severity of allergy and whether exposure must be avoided.",
            "label": "Other dietary requirements (please specify)",
            "placeholder": "Describe any allergies, intolerances, or specific requirements",
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
            "helpText": "You can unsubscribe from marketing communications at any time.",
            "label": "I consent to receive event updates and communications about this conference.",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "93de082937b00375edebd151a900701b4cd7dd93ec571340478f0bfb476af098",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 79734,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "conf-rsvp-sydney",
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
            "helpText": "Select your sessions and let us know any dietary requirements. We'll send updates about the event to the contact you provide.",
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
            "helpText": "As it should appear on your badge.",
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
            "helpText": "We will send your RSVP confirmation and event updates here.",
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
            "helpText": "Provide a number we can contact you on the day if necessary.",
            "label": "Phone (optional)",
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
            "helpText": "Select the main session or workshop you'd like to attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Keynote \u2014 Opening Plenary",
                "value": "keynote_plenary"
              },
              {
                "label": "Workshop A \u2014 Data & AI",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B \u2014 Product Strategy",
                "value": "workshop_b"
              },
              {
                "label": "Panel \u2014 Industry Trends",
                "value": "panel_trends"
              },
              {
                "label": "Networking Session",
                "value": "networking"
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
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select any that apply to you.",
            "label": "Dietary preferences",
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
                "label": "Other (please specify)",
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
            "helpText": "If you selected 'Other', provide details here (e.g. specific allergies).",
            "label": "Other dietary requirements",
            "placeholder": "Please describe allergies or special requirements",
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
            "helpText": "I agree to receive event-related updates and communications.",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "2cd814925506577912fcf14fe5d5beafe88ffe212357ee5e7f6178d294d7d6d9",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p02-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p02-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p02-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p02-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p02-au-adversarial-r1",
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
  "duration_ms": 89691,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "conference-rsvp",
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
            "helpText": "We'll send registration confirmation to this address.",
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
            "helpText": "Include the +1 country code. We'll only use this to contact you about the event.",
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
            "helpText": "Enter your ZIP or postal code.",
            "label": "ZIP code",
            "placeholder": "ZIP / Postal code",
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
            "helpText": "Choose the session you plan to attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Opening Keynote",
                "value": "opening_keynote"
              },
              {
                "label": "Workshop A: AI Ethics",
                "value": "workshop_ai_ethics"
              },
              {
                "label": "Workshop B: Cloud Architecture",
                "value": "workshop_cloud"
              },
              {
                "label": "Panel Discussion: Future of Tech",
                "value": "panel_future_tech"
              },
              {
                "label": "Networking Lunch",
                "value": "networking_lunch"
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
            "y": 560
          },
          "props": {
            "height": 120,
            "helpText": "Select any dietary needs we should accommodate.",
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
                "label": "Nut-free",
                "value": "nut_free"
              },
              {
                "label": "No dietary requirements",
                "value": "no_requirements"
              },
              {
                "label": "Other (please specify below)",
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
            "helpText": "If you selected Other or have accessibility requirements, tell us here.",
            "label": "Additional accessibility or dietary details",
            "placeholder": "Please provide any additional dietary needs, accessibility requirements, or other notes.",
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
            "helpText": "By consenting you agree to receive event-related updates and announcements.",
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

## Row 7: `p03-au-neutral-r1__r01`

- Prompt ID: `p03-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "0ce139a8b217a15df68c4e14ba2df18149e72d6c159d46a7597c4df51b31a3ce",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 56855,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "workshop-signup-form",
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
            "label": "Please complete this form to register for the workshop. Tell us about your skill level, any accessibility needs, and which workshop stream you prefer.",
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
            "helpText": "We will send confirmation and workshop materials to this address.",
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
            "helpText": "Optional \u2014 used only for urgent event updates.",
            "label": "Phone number (optional)",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Organisation (optional)",
            "placeholder": "Company or group",
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
            "label": "Job title (optional)",
            "placeholder": "Your role or title",
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
          "id": "dropdown-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Choose the stream you'd most like to attend.",
            "label": "Preferred workshop stream",
            "options": [
              {
                "label": "Web Development",
                "value": "web_development"
              },
              {
                "label": "Data & Machine Learning",
                "value": "data_ml"
              },
              {
                "label": "Design & UX",
                "value": "design_ux"
              },
              {
                "label": "Leadership & Soft Skills",
                "value": "leadership"
              },
              {
                "label": "Other (specify in notes)",
                "value": "other"
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
          "id": "dropdown-9",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Helps us tailor the workshop content.",
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
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "If you have multiple needs, tick each that applies.",
            "label": "Accessibility needs (select all that apply)",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair_access"
              },
              {
                "label": "Mobility assistance",
                "value": "mobility_assistance"
              },
              {
                "label": "Sign language interpreter (ASL/LSQ)",
                "value": "sign_language"
              },
              {
                "label": "Captions / live transcription",
                "value": "captions"
              },
              {
                "label": "Quiet / low-sensory space",
                "value": "quiet_space"
              },
              {
                "label": "Dietary requirements",
                "value": "dietary"
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
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "Provide details if you selected 'Other' or need specific arrangements.",
            "label": "Accessibility or dietary details",
            "placeholder": "Please describe any specific needs, assistance, or dietary requirements",
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
            "y": 1080
          },
          "props": {
            "height": 200,
            "label": "Additional notes",
            "placeholder": "Any other information we should know (food allergies, scheduling notes, etc.)",
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
            "y": 1384
          },
          "props": {
            "height": 120,
            "helpText": "By registering you consent to receiving event-related communications.",
            "label": "I agree to the event terms and privacy policy.",
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
            "y": 1528
          },
          "props": {
            "height": 72,
            "label": "Sign up",
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
      "title": "Workshop Signup Form"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "4e9187231fa4e4d6b53a9e3928606b6cf3ac665a5edf0d276256b55e0004e357",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 68277,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "helpText": "Optional \u2014 we'll only call if we need to clarify your registration.",
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
          "id": "radio-5",
          "position": {
            "x": 40,
            "y": 292
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
            "x": 40,
            "y": 436
          },
          "props": {
            "height": 110,
            "helpText": "Pick the workshop stream you'd like to attend in Sydney.",
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
                "label": "Software Development",
                "value": "software-development"
              },
              {
                "label": "Product Management",
                "value": "product-management"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Choose a stream",
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
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "Select any accessibility supports you may need. We'll follow up for details if required.",
            "label": "Accessibility requirements",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Auslan / sign language interpreter",
                "value": "auslan"
              },
              {
                "label": "Live captioning",
                "value": "captioning"
              },
              {
                "label": "Dietary assistance",
                "value": "dietary"
              },
              {
                "label": "Other assistance",
                "value": "other-assistance"
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
            "y": 714
          },
          "props": {
            "height": 200,
            "helpText": "Provide details so we can organise appropriate support for the Sydney event.",
            "label": "Accessibility details (optional)",
            "placeholder": "Please describe any specific needs or how we can accommodate you",
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
          "id": "paragraph-9",
          "position": {
            "x": 40,
            "y": 1018
          },
          "props": {
            "height": 48,
            "helpText": "All workshop sessions take place in Sydney. Venue details will be sent after registration.",
            "label": "Event location",
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
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "By registering you accept the event terms.",
            "label": "I agree to the event terms",
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
      "title": "Sydney Workshop Signup"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "2de4a32ab35458740751a1d17db0a1e43d543a3b68163069273334b59cc07f44",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p03-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p03-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p03-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p03-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p03-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p03-au-adversarial-r1",
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
  "component_count": 13,
  "duration_ms": 75356,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "workshop-signup-form",
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
            "label": "Please provide your details below so we can reserve your place and support any accessibility needs.",
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
            "helpText": "We will send confirmation and workshop details to this address.",
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
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide a phone number we can use for urgent updates. Include country code (+1).",
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
            "x": 384,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Enter your postal ZIP code.",
            "label": "ZIP code",
            "placeholder": "ZIP code",
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
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "Select the workshop stream you'd like to attend.",
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
                "label": "Data & Analytics",
                "value": "data"
              },
              {
                "label": "Leadership & Facilitation",
                "value": "leadership"
              },
              {
                "label": "Other",
                "value": "other"
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
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Select any accessibility support you require. We will follow up to confirm arrangements.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Sign language interpreter",
                "value": "sign_language"
              },
              {
                "label": "Live captioning (CART)",
                "value": "captioning"
              },
              {
                "label": "Dietary requirements",
                "value": "dietary"
              },
              {
                "label": "Quiet / low-sensory space",
                "value": "quiet_space"
              },
              {
                "label": "Other (please describe below)",
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
            "label": "If other, or to give more detail about accessibility needs",
            "placeholder": "Describe any other accessibility needs or provide details about selections above",
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
            "label": "Additional notes (optional)",
            "placeholder": "Anything else we should know?",
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
            "helpText": "By signing up you agree to the workshop terms.",
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
            "y": 1672
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
      "title": "Workshop Signup"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "a9cbca666bb4f77e7b47cade86b4ff64992aeacca77813c737be4380a650a6f4",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 48757,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "webinar-registration",
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
            "helpText": "We will email your registration details and webinar link to this address.",
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
            "helpText": "Optional \u2014 used for last-minute updates or cancellations.",
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
            "label": "Role / Job title",
            "placeholder": "e.g., Product Manager",
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
            "helpText": "Select the timezone you'll attend from so we can publish times in your local time.",
            "label": "Preferred timezone",
            "options": [
              {
                "label": "UTC (Coordinated Universal Time)",
                "value": "UTC"
              },
              {
                "label": "GMT (London) - Europe/London",
                "value": "Europe/London"
              },
              {
                "label": "CET (Central European Time) - Europe/Paris",
                "value": "Europe/Paris"
              },
              {
                "label": "EST (US Eastern) - America/New_York",
                "value": "America/New_York"
              },
              {
                "label": "CST (US Central) - America/Chicago",
                "value": "America/Chicago"
              },
              {
                "label": "MST (US Mountain) - America/Denver",
                "value": "America/Denver"
              },
              {
                "label": "PST (US Pacific) - America/Los_Angeles",
                "value": "America/Los_Angeles"
              },
              {
                "label": "AEST (Australia Eastern) - Australia/Sydney",
                "value": "Australia/Sydney"
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
            "helpText": "Share brief questions or topics you'd like the speaker to cover. This helps shape the session.",
            "label": "Questions for the speaker (optional)",
            "placeholder": "Any specific topics or questions you'd like addressed?",
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
            "helpText": "Opt in to receive event updates, related webinars, and occasional marketing emails.",
            "label": "Marketing and updates",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and promotional offers",
                "value": "opt_in"
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
      "title": "Webinar Registration"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "dcf56787c69e71271bf192ce84407143faaeba4f1dc62d0a32370e07e4f4b81c",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 72630,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "helpText": "This webinar will be scheduled in the Sydney timezone. Please select the timezone that best matches how you'd like to see event times.",
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
            "helpText": "We will send webinar access instructions to this address.",
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
            "helpText": "Optional \u2014 used only if we need to reach you about the webinar.",
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
            "label": "Role / Job title",
            "placeholder": "e.g., Product Manager",
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
            "helpText": "Times in communications will be shown in the timezone you choose.",
            "label": "Preferred timezone",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT) \u2014 UTC+10/11",
                "value": "Australia/Sydney"
              },
              {
                "label": "UTC \u2014 Coordinated Universal Time (UTC+0)",
                "value": "UTC"
              },
              {
                "label": "America/Los_Angeles (PDT/PST) \u2014 UTC-7/8",
                "value": "America/Los_Angeles"
              },
              {
                "label": "Europe/London (BST/GMT) \u2014 UTC+1/0",
                "value": "Europe/London"
              },
              {
                "label": "Asia/Singapore (SGT) \u2014 UTC+8",
                "value": "Asia/Singapore"
              },
              {
                "label": "Asia/Tokyo (JST) \u2014 UTC+9",
                "value": "Asia/Tokyo"
              }
            ],
            "placeholder": "Select a timezone",
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
            "helpText": "We'll share these with the speaker in advance. Keep questions concise.",
            "label": "Questions for the speaker",
            "placeholder": "Any specific questions you'd like the speaker to address?",
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
            "helpText": "Yes \u2014 I'd like to receive updates and marketing about future events from the organiser.",
            "label": "Marketing opt-in",
            "options": [
              {
                "label": "Send me event updates and marketing emails",
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
            "helpText": "Please review and accept the event terms to complete your registration.",
            "label": "Event terms",
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
      "title": "Webinar Registration \u2014 Sydney"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "122ef42bdb9ebe2859b400ad3ddff92634fd7c2a14706d34f3875afea55c5f1e",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p04-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
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
  "component_count": 11,
  "duration_ms": 68999,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "webinar-registration-form",
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
            "helpText": "We'll send your webinar link here",
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
            "helpText": "Optional \u2014 include country code +1",
            "label": "Phone (+1)",
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
            "label": "ZIP code",
            "placeholder": "ZIP / postal code",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Organization",
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
            "y": 426
          },
          "props": {
            "height": 110,
            "label": "Job title / Role",
            "placeholder": "Your role or title",
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
            "y": 560
          },
          "props": {
            "height": 110,
            "helpText": "Helps us schedule and show local times",
            "label": "Timezone",
            "options": [
              {
                "label": "UTC\u221208:00 (Pacific Time, PST)",
                "value": "UTC-8"
              },
              {
                "label": "UTC\u221205:00 (Eastern Time, EST)",
                "value": "UTC-5"
              },
              {
                "label": "UTC (GMT)",
                "value": "UTC+0"
              },
              {
                "label": "UTC+01:00 (Central European Time)",
                "value": "UTC+1"
              },
              {
                "label": "UTC+10:00 (Australian Eastern Time, AEST)",
                "value": "UTC+10"
              },
              {
                "label": "Other / Prefer to specify",
                "value": "other"
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
            "y": 694
          },
          "props": {
            "height": 200,
            "helpText": "We'll review questions and try to cover them during the Q&A",
            "label": "Questions for the speaker",
            "placeholder": "Share any question you'd like the speaker to address",
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
            "helpText": "I agree to receive marketing communications about future events and offers.",
            "label": "Marketing opt-in",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "785e022658331219b7f48cc9b7a50879f07754a58e559e88cd052c6c5ad1ff59",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 69641,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "wedding-rsvp-form",
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
            "label": "We look forward to celebrating with you! Complete the details below to confirm your attendance.",
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
            "helpText": "Guest's given name",
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
            "helpText": "Guest's family name",
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
            "helpText": "We'll use this to send any updates about the day",
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
            "helpText": "Optional \u2014 useful for last-minute changes",
            "label": "Phone (optional)",
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
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Please indicate whether you will join us on the day",
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes \u2014 I'll be there",
                "value": "attending"
              },
              {
                "label": "No \u2014 regretfully can't attend",
                "value": "not_attending"
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
            "helpText": "Tick if you will be bringing a plus-one",
            "label": "Plus-one",
            "options": [
              {
                "label": "Bringing a plus-one",
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
            "helpText": "Provide full name if you're bringing a guest",
            "label": "Plus-one's name (if applicable)",
            "placeholder": "Full name of your plus-one",
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
            "helpText": "If attending, please choose a meal option for yourself",
            "label": "Meal choice",
            "options": [
              {
                "label": "Chicken",
                "value": "chicken"
              },
              {
                "label": "Beef",
                "value": "beef"
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
                "label": "No meal / Kids",
                "value": "no_meal"
              }
            ],
            "placeholder": "Select a main course",
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
            "helpText": "List any dietary needs for you or your guests",
            "label": "Dietary requirements (allergies, intolerances)",
            "placeholder": "E.g. gluten-free, nut allergy, lactose intolerant",
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
            "helpText": "We'll try to include your requests in the reception playlist",
            "label": "Song request",
            "placeholder": "Song title or artist you'd love to hear",
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
            "helpText": "Optional \u2014 a short message to the couple",
            "label": "Message to the couple (optional)",
            "placeholder": "Share a message, well wishes, or anything else you'd like the couple to know",
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
          "id": "submit-button-13",
          "position": {
            "x": 40,
            "y": 1528
          },
          "props": {
            "height": 72,
            "helpText": "Click to send your RSVP",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "1e646e7991d6b9efe35cf8c3e61860f7f87c65e7621d7963e39dd35dac2c83bb",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 78264,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "helpText": "Fill out the details below for each guest. If you're bringing a plus-one, include their name and meal choice.",
            "label": "RSVP Instructions",
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
            "label": "Guest First Name",
            "placeholder": "e.g. Alex",
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
            "label": "Guest Last Name",
            "placeholder": "e.g. Taylor",
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
            "label": "Email (for RSVP confirmation)",
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
            "label": "Phone (optional)",
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
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Please tell us whether you can join the celebration in Sydney.",
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes, I will attend",
                "value": "yes"
              },
              {
                "label": "No, I am unable to attend",
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
            "helpText": "Select if you plan to bring an additional guest.",
            "label": "Bringing a plus-one?",
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
            "x": 424,
            "y": 508
          },
          "props": {
            "height": 110,
            "label": "Plus-one Name (if applicable)",
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
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 652
          },
          "props": {
            "height": 110,
            "helpText": "Please choose your main meal option.",
            "label": "Meal Choice (Guest)",
            "options": [
              {
                "label": "Chicken",
                "value": "chicken"
              },
              {
                "label": "Beef",
                "value": "beef"
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
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Children's Meal",
                "value": "children"
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
          "id": "dropdown-10",
          "position": {
            "x": 424,
            "y": 652
          },
          "props": {
            "height": 110,
            "helpText": "Plus-one meal selection (if applicable).",
            "label": "Meal Choice (Plus-one)",
            "options": [
              {
                "label": "Chicken",
                "value": "chicken"
              },
              {
                "label": "Beef",
                "value": "beef"
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
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Children's Meal",
                "value": "children"
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
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 200,
            "helpText": "Provide details so we can inform the caterer.",
            "label": "Dietary Requirements or Allergies",
            "placeholder": "Please list any allergies or dietary requirements for you or your guest.",
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
            "y": 1090
          },
          "props": {
            "height": 110,
            "helpText": "One song request \u2014 we'll do our best to include it!",
            "label": "Song Request",
            "placeholder": "Song you'd like played",
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
            "y": 1224
          },
          "props": {
            "height": 200,
            "label": "Message to the couple (optional)",
            "placeholder": "Share a message or well wishes",
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
            "y": 1528
          },
          "props": {
            "height": 120,
            "helpText": "By submitting your RSVP you accept the event terms.",
            "label": "Event terms",
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
            "y": 1672
          },
          "props": {
            "height": 72,
            "helpText": "Submit your response",
            "label": "RSVP",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "8f4abc95d9774464a831017765fe515feccbb2e41e7023c24384f08a5ca78203",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p05-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p05-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
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
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 133696,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "wedding-rsvp-form",
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
            "placeholder": "Your given name",
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
            "helpText": "We'll use this to send RSVP confirmation and updates.",
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
            "helpText": "Optional \u2014 helpful for last-minute updates.",
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
          "id": "text-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Please provide your ZIP code for guest list records.",
            "label": "ZIP code",
            "placeholder": "Enter your ZIP code",
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
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes \u2014 I will attend",
                "value": "attending"
              },
              {
                "label": "No \u2014 I cannot attend",
                "value": "not_attending"
              },
              {
                "label": "Maybe",
                "value": "maybe"
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
            "helpText": "Check if you plan to bring a guest.",
            "label": "I will be bringing a plus-one",
            "options": [
              {
                "label": "Yes \u2014 I will bring a plus-one",
                "value": "bringing_plus_one"
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
            "y": 714
          },
          "props": {
            "height": 110,
            "label": "Plus-one name",
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
            "helpText": "Optional contact for your guest (+1 phone).",
            "label": "Plus-one phone",
            "placeholder": "Plus-one phone number",
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
            "helpText": "Choose one option for your main meal.",
            "label": "Meal choice (your plate)",
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
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Other / Don't know yet",
                "value": "other"
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
                "label": "Gluten-free",
                "value": "gluten_free"
              },
              {
                "label": "Other / Don't know yet",
                "value": "other"
              }
            ],
            "placeholder": "Select your guest's meal (if applicable)",
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
            "helpText": "Please be specific so we can accommodate you.",
            "label": "Dietary needs / allergies",
            "placeholder": "List any allergies, dietary restrictions, or preferences",
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
            "helpText": "We'll try to include crowd favorites on the playlist.",
            "label": "Song request",
            "placeholder": "What song would you like to hear?",
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
            "label": "Message to the couple",
            "placeholder": "Write a short message or well wishes",
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
            "y": 1724
          },
          "props": {
            "height": 120,
            "helpText": "By submitting, you acknowledge and accept the event terms.",
            "label": "Acknowledgement",
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
            "y": 1868
          },
          "props": {
            "height": 72,
            "label": "Send RSVP",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "e2bfd2f5ed8b8e5bbf8c761669e2326f87a21e741b9645a5d1f6e0832d96f08e",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 79278,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 2300,
    "width": 960
  },
  "formId": "volunteer-signup",
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
            "label": "Thanks for offering your time. Please provide your contact details, availability, relevant skills, an emergency contact, and acknowledge our code of conduct.",
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
            "helpText": "We\u2019ll use this to confirm shifts and send updates.",
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
            "helpText": "Mobile or best number to reach you.",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Providing an address helps with assignment and emergency planning.",
            "label": "Address (optional)",
            "placeholder": "Street, suburb, state/postcode, country",
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
          "id": "paragraph-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 48,
            "label": "Availability",
            "tabOrder": 7,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 120,
            "label": "Days you can volunteer (select all that apply)",
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
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 110,
            "helpText": "Choose the shift(s) you prefer.",
            "label": "Preferred shift/time",
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
            "placeholder": "Select preferred shift",
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
            "y": 714
          },
          "props": {
            "height": 110,
            "label": "Available from (date)",
            "placeholder": "Earliest date you can start",
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
            "y": 848
          },
          "props": {
            "height": 120,
            "helpText": "Select skills that apply. Choose 'Other' and describe below if needed.",
            "label": "Skills / areas of experience",
            "options": [
              {
                "label": "Event setup & packdown",
                "value": "setup"
              },
              {
                "label": "Customer service / front desk",
                "value": "frontdesk"
              },
              {
                "label": "First aid / medical",
                "value": "firstaid"
              },
              {
                "label": "Child supervision / activities",
                "value": "childcare"
              },
              {
                "label": "Photography / media",
                "value": "photography"
              },
              {
                "label": "Administration / data entry",
                "value": "admin"
              },
              {
                "label": "Logistics / driving",
                "value": "logistics"
              },
              {
                "label": "Other (describe below)",
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
            "y": 992
          },
          "props": {
            "height": 200,
            "label": "If other, or to add details about your skills/certifications",
            "placeholder": "List licences, certificates, or provide more detail",
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
          "id": "paragraph-13",
          "position": {
            "x": 40,
            "y": 1296
          },
          "props": {
            "height": 48,
            "label": "Emergency contact",
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
          "id": "text-14",
          "position": {
            "x": 40,
            "y": 1368
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name",
            "placeholder": "Full name",
            "tabOrder": 14,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "phone-15",
          "position": {
            "x": 424,
            "y": 1368
          },
          "props": {
            "height": 110,
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
          "id": "text-16",
          "position": {
            "x": 40,
            "y": 1502
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "placeholder": "e.g. Partner, Parent, Friend",
            "tabOrder": 16,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "terms-17",
          "position": {
            "x": 40,
            "y": 1636
          },
          "props": {
            "height": 120,
            "label": "Code of conduct acknowledgement",
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
          "id": "paragraph-18",
          "position": {
            "x": 40,
            "y": 1780
          },
          "props": {
            "height": 48,
            "label": "I agree to follow the event's code of conduct and instructions from event staff. I understand that failure to comply may result in removal from volunteer duties.",
            "tabOrder": 18,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "textarea-19",
          "position": {
            "x": 40,
            "y": 1852
          },
          "props": {
            "height": 200,
            "label": "Additional notes (availability restrictions, accessibility needs, or other info)",
            "placeholder": "Anything else we should know?",
            "tabOrder": 19,
            "width": "640px"
          },
          "style": {
            "height": 200,
            "width": 640
          },
          "type": "textarea"
        },
        {
          "id": "submit-button-20",
          "position": {
            "x": 40,
            "y": 2156
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
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
      "title": "Volunteer Signup"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "703bc49fca7c6a22d7c8433c765846e9ed2f26a4b353a9a77437caaf3aed7bac",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 82283,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "label": "We will use this information to match you with suitable roles at the Sydney event and to contact you if needed.",
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
            "helpText": "A mobile number is helpful for shift updates and urgent contact.",
            "label": "Mobile phone",
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
            "helpText": "Optional \u2014 helps with local shift assignments around Sydney.",
            "label": "Address",
            "placeholder": "Street address, suburb, postcode",
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
            "helpText": "Select all times you can volunteer. We'll try to match you to a suitable shift.",
            "label": "When are you available? (select all that apply)",
            "options": [
              {
                "label": "Weekday mornings",
                "value": "weekday_morning"
              },
              {
                "label": "Weekday afternoons",
                "value": "weekday_afternoon"
              },
              {
                "label": "Weekend mornings",
                "value": "weekend_morning"
              },
              {
                "label": "Weekend afternoons",
                "value": "weekend_afternoon"
              },
              {
                "label": "Evenings",
                "value": "evenings"
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
            "y": 642
          },
          "props": {
            "height": 110,
            "label": "Available from",
            "placeholder": "Start date",
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
          "id": "date-9",
          "position": {
            "x": 424,
            "y": 642
          },
          "props": {
            "height": 110,
            "label": "Available until",
            "placeholder": "End date (if applicable)",
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
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "We may contact you about roles that match your skills.",
            "label": "Skills or roles you can help with (select all that apply)",
            "options": [
              {
                "label": "Customer service / Info desk",
                "value": "customer_service"
              },
              {
                "label": "Event setup / packdown",
                "value": "setup"
              },
              {
                "label": "Crowd management / stewarding",
                "value": "crowd_management"
              },
              {
                "label": "First aid (qualified)",
                "value": "first_aid"
              },
              {
                "label": "Hospitality / food & beverage",
                "value": "hospitality"
              },
              {
                "label": "Administration / registration",
                "value": "admin"
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
            "label": "If Other, or any relevant qualifications/certifications (e.g. First Aid, Working with Children)",
            "placeholder": "Describe other skills, qualifications or certifications",
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
            "placeholder": "e.g. Partner, Parent, Friend",
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
            "y": 1358
          },
          "props": {
            "height": 110,
            "helpText": "A number we can call in case of emergency during your shift.",
            "label": "Emergency contact phone",
            "placeholder": "+61 4xx xxx xxx",
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
          "id": "terms-15",
          "position": {
            "x": 40,
            "y": 1492
          },
          "props": {
            "height": 120,
            "helpText": "I agree to follow the event code of conduct and related terms.",
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
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 1636
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "09535c486f1cb2b9990676e8e85c5b93d10a54761bc52f199e1e21689280616f",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p06-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
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
  "component_count": 18,
  "duration_ms": 92536,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1986,
    "width": 960
  },
  "formId": "volunteer-signup",
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
            "label": "We will use this information to place you in appropriate roles and contact you if needed. Fields marked with * are required.",
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
            "label": "First name *",
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
            "label": "Last name *",
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
            "helpText": "We'll use this to send confirmations and updates.",
            "label": "Email address *",
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
            "helpText": "Please include country code +1.",
            "label": "Phone (+1) *",
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
            "helpText": "Optional \u2014 helpful for local placements.",
            "label": "Street address",
            "placeholder": "Street address, apartment/suite (optional)",
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
            "helpText": "Enter ZIP/postal code (ZIP format requested).",
            "label": "ZIP code *",
            "placeholder": "e.g., 20001",
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
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select all days you can volunteer.",
            "label": "Which days are you available? *",
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
          "id": "dropdown-9",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "If multiple, choose the one you'd prefer most.",
            "label": "Preferred shift",
            "options": [
              {
                "label": "Morning (6am\u201312pm)",
                "value": "morning"
              },
              {
                "label": "Afternoon (12pm\u20135pm)",
                "value": "afternoon"
              },
              {
                "label": "Evening (5pm\u201310pm)",
                "value": "evening"
              },
              {
                "label": "Any / Flexible",
                "value": "any"
              }
            ],
            "placeholder": "Select a preferred shift",
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
            "y": 776
          },
          "props": {
            "height": 200,
            "label": "Availability notes",
            "placeholder": "Tell us about time constraints, recurring commitments, or shift length preferences.",
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
            "y": 1080
          },
          "props": {
            "height": 120,
            "helpText": "Select all skills that apply.",
            "label": "Skills and experience",
            "options": [
              {
                "label": "First aid / CPR",
                "value": "first_aid"
              },
              {
                "label": "Event setup / teardown",
                "value": "setup"
              },
              {
                "label": "Registration / Check-in",
                "value": "registration"
              },
              {
                "label": "Food service / catering",
                "value": "food_service"
              },
              {
                "label": "Photography / media",
                "value": "photography"
              },
              {
                "label": "Crowd management / marshalling",
                "value": "crowd_control"
              },
              {
                "label": "Driver (valid licence)",
                "value": "driver"
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
          "id": "text-12",
          "position": {
            "x": 40,
            "y": 1224
          },
          "props": {
            "height": 110,
            "helpText": "Leave blank if not applicable.",
            "label": "Other skills (please describe)",
            "placeholder": "Describe any other relevant skills",
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
          "id": "text-13",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 110,
            "label": "Emergency contact name *",
            "placeholder": "Full name",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "text"
        },
        {
          "id": "text-14",
          "position": {
            "x": 600,
            "y": 1358
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "placeholder": "e.g., Parent, Partner, Friend",
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
            "y": 1492
          },
          "props": {
            "height": 110,
            "helpText": "Include country code +1.",
            "label": "Emergency contact phone (+1) *",
            "placeholder": "[SCRUBBED_PHONE]",
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
          "id": "terms-16",
          "position": {
            "x": 40,
            "y": 1626
          },
          "props": {
            "height": 120,
            "helpText": "You must accept our code of conduct and terms to volunteer.",
            "label": "I agree to the code of conduct and event terms *",
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
          "id": "paragraph-17",
          "position": {
            "x": 40,
            "y": 1770
          },
          "props": {
            "height": 48,
            "label": "By submitting, you confirm that the information provided is accurate to the best of your knowledge. We may contact you for role confirmation or training.",
            "tabOrder": 17,
            "width": "880px"
          },
          "style": {
            "height": 48,
            "width": 880
          },
          "type": "paragraph"
        },
        {
          "id": "submit-button-18",
          "position": {
            "x": 40,
            "y": 1842
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
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
      "title": "Volunteer Signup Form"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "4bcaecf5f2505d247d778c81642edc85f836ec0f3120e1939d649840c0e7ea5e",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 75817,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "helpText": "As it appears on official ID",
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
            "placeholder": "Family name / Surname",
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
            "helpText": "We will use this to send application updates",
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
            "helpText": "Mobile or best contact number",
            "label": "Phone number",
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
          "id": "address-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Street address, suburb/city, postal code, country",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Choose the membership level you are applying for",
            "label": "Membership type",
            "options": [
              {
                "label": "Regular",
                "value": "regular"
              },
              {
                "label": "Student",
                "value": "student"
              },
              {
                "label": "Senior",
                "value": "senior"
              },
              {
                "label": "Associate",
                "value": "associate"
              },
              {
                "label": "Honorary",
                "value": "honorary"
              }
            ],
            "placeholder": "Select a membership",
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
          "id": "date-7",
          "position": {
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "When would you like your membership to begin?",
            "label": "Preferred start date",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 7,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 120,
            "helpText": "You must meet the criteria listed in the membership guidelines",
            "label": "I confirm I meet the membership eligibility criteria",
            "options": [
              {
                "label": "I confirm I meet the membership eligibility criteria",
                "value": "confirm_criteria"
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
            "label": "I am at least 18 years old",
            "options": [
              {
                "label": "I am at least 18 years old",
                "value": "age_18_plus"
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
            "helpText": "Checks will only be conducted where necessary and with your consent",
            "label": "I consent to a membership background check if required",
            "options": [
              {
                "label": "I consent to a membership background check if required",
                "value": "consent_bg_check"
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
            "helpText": "Helps us understand how applicants find us",
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
                "label": "Web search",
                "value": "search"
              },
              {
                "label": "Event or workshop",
                "value": "event"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a source",
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
            "y": 992
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "placeholder": "Who referred you or which source?",
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
            "y": 1126
          },
          "props": {
            "height": 200,
            "label": "Additional information",
            "placeholder": "Optional: any details we should know about your application",
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
            "y": 1430
          },
          "props": {
            "height": 120,
            "helpText": "By checking this box you agree to the membership terms required to process your application.",
            "label": "I have read and agree to the membership terms and conditions.",
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
            "y": 1574
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "119d338669f2f4f60e14eff7274dd14a65ff21e402d42e0d86350830d2aee0d4",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 62538,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1486,
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
            "label": "Please provide your personal details, select a membership type, confirm eligibility, tell us how you heard about us, and accept the event terms to submit your application.",
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
            "helpText": "We'll use this to contact you about your application.",
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
            "helpText": "Include country and area code if outside Australia.",
            "label": "Phone number",
            "placeholder": "+61 2 9XXXXXXX",
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
            "label": "Postal address",
            "placeholder": "Street address, suburb, state, postcode, country",
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
            "helpText": "Choose the membership category that applies to you.",
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
                "label": "Corporate",
                "value": "corporate"
              },
              {
                "label": "Honorary",
                "value": "honorary"
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
          "id": "date-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "When would you like your membership to begin (approx.)?",
            "label": "Preferred start date",
            "placeholder": "DD/MM/YYYY",
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
                "label": "Yes, I confirm",
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
            "label": "I agree to abide by the organisation's code of conduct",
            "options": [
              {
                "label": "I agree",
                "value": "agree_coc"
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
            "helpText": "Ensure you meet any specific criteria for Student, Corporate or other categories.",
            "label": "I meet the eligibility criteria for the selected membership type",
            "options": [
              {
                "label": "I confirm eligibility",
                "value": "confirm_eligibility"
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
                "label": "Friend/Colleague",
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
                "label": "Event",
                "value": "event"
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
            "y": 1064
          },
          "props": {
            "height": 110,
            "label": "If Other, please specify",
            "placeholder": "Optional details about referral",
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
            "y": 1198
          },
          "props": {
            "height": 120,
            "helpText": "By submitting this application you agree to the event terms. The official event terms will be presented (company-managed link).",
            "label": "Agreement to event terms",
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
            "y": 1342
          },
          "props": {
            "height": 72,
            "label": "Submit Application",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "bf152acde421aae43e0bbabe7c055aa234f648d62f4b54225326bcb15dceaace",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "component_count": 16,
  "duration_ms": 81378,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "membership-application",
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
            "label": "Provide your applicant details, select a membership type, confirm eligibility, and acknowledge the event terms to complete your application.",
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
            "helpText": "As shown on official ID.",
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
            "placeholder": "Family name / Surname",
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
            "helpText": "We'll use this to communicate about your application.",
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
            "helpText": "Please include country code +1 in the number.",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide your mailing address.",
            "label": "Street address",
            "placeholder": "Street address, apartment, suite, unit, building, floor, etc.",
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
            "helpText": "Please enter ZIP code (US-style postal code).",
            "label": "ZIP code",
            "placeholder": "e.g. 02115 or 94105",
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
            "helpText": "Choose the membership category you are applying for.",
            "label": "Membership type",
            "options": [
              {
                "label": "Regular",
                "value": "regular"
              },
              {
                "label": "Student",
                "value": "student"
              },
              {
                "label": "Senior",
                "value": "senior"
              },
              {
                "label": "Life",
                "value": "life"
              }
            ],
            "placeholder": "Select a membership option",
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
            "helpText": "You must meet the published eligibility criteria to join.",
            "label": "Eligibility: I confirm I meet the membership eligibility requirements.",
            "options": [
              {
                "label": "I confirm I meet the membership eligibility requirements.",
                "value": "eligibility_confirmed"
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
            "label": "Accuracy: I confirm the information I provided is true and correct.",
            "options": [
              {
                "label": "I confirm the information I provided is true and correct.",
                "value": "information_true"
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
            "label": "Conduct: I agree to abide by the organisation's code of conduct if accepted.",
            "options": [
              {
                "label": "I agree to abide by the organisation's code of conduct.",
                "value": "agree_conduct"
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
            "helpText": "Optional \u2014 helps us understand referral sources.",
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
                "label": "Website / search",
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
            "placeholder": "Select one",
            "tabOrder": 12,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 536
          },
          "type": "dropdown"
        },
        {
          "id": "text-13",
          "position": {
            "x": 600,
            "y": 1064
          },
          "props": {
            "height": 110,
            "helpText": "Optional",
            "label": "If other, please specify",
            "placeholder": "Please tell us where you heard about us",
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
            "y": 1198
          },
          "props": {
            "height": 200,
            "helpText": "Optional. Use this space to provide extra context for your application.",
            "label": "Additional information or comments",
            "placeholder": "Any additional details you'd like to share...",
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
            "y": 1502
          },
          "props": {
            "height": 120,
            "helpText": "You must accept the event terms to submit your application.",
            "label": "Terms and conditions",
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
            "y": 1646
          },
          "props": {
            "height": 72,
            "label": "Apply for Membership",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "a6cfbdbe60c319391d73d2f96858f4a5d1028f6dda6100759a218da15dd81e98",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 66557,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "helpText": "Visitor's given name",
            "label": "First name",
            "placeholder": "Enter first name",
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
            "helpText": "Visitor's family name",
            "label": "Last name",
            "placeholder": "Enter last name",
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
            "helpText": "Best email to reach the lead",
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
            "helpText": "Optional \u2014 include country code for international numbers",
            "label": "Phone number",
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
            "helpText": "Company the lead represents",
            "label": "Company / Organization",
            "placeholder": "Enter company name",
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
            "helpText": "Select all areas the visitor is interested in",
            "label": "Interest areas",
            "options": [
              {
                "label": "Product demo",
                "value": "product_demo"
              },
              {
                "label": "Pricing",
                "value": "pricing"
              },
              {
                "label": "New features",
                "value": "new_features"
              },
              {
                "label": "Partnerships",
                "value": "partnerships"
              },
              {
                "label": "Careers",
                "value": "careers"
              },
              {
                "label": "Other",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 110,
            "helpText": "When is the lead likely to purchase or decide?",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediately (0\u20131 months)",
                "value": "0-1"
              },
              {
                "label": "1\u20133 months",
                "value": "1-3"
              },
              {
                "label": "3\u20136 months",
                "value": "3-6"
              },
              {
                "label": "6+ months",
                "value": "6+"
              },
              {
                "label": "Not sure / Just browsing",
                "value": "unsure"
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
            "y": 704
          },
          "props": {
            "height": 200,
            "helpText": "Include key points, next steps, or specific product interests",
            "label": "Notes",
            "placeholder": "Add conversation notes, follow-up actions, or context",
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
            "helpText": "By consenting you agree to be contacted by the exhibitor for sales and marketing purposes.",
            "label": "I consent to be contacted for follow-up about my inquiry.",
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
      "title": "Trade Show Booth Lead Log"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "6a2f76f8f2e385d309a24345d48a481287c6802125e2e8b118525d81dc517003",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 94776,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "trade-show-booth-visit-sydney",
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
            "placeholder": "Visitor first name",
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
            "placeholder": "Visitor last name",
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
            "helpText": "Preferred contact email",
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
            "helpText": "Mobile or direct number (optional)",
            "label": "Phone",
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
            "label": "Company",
            "placeholder": "Visitor's company or organisation",
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
            "helpText": "What the visitor was most interested in",
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
                "label": "Technical integration / API",
                "value": "technical"
              },
              {
                "label": "Partnerships / reseller",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 560
          },
          "props": {
            "height": 110,
            "helpText": "Estimated timeframe for purchase or engagement",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediately / within weeks",
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
                "label": "Not planning to buy",
                "value": "not_planning"
              },
              {
                "label": "Unknown / needs more info",
                "value": "unknown"
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
            "y": 694
          },
          "props": {
            "height": 200,
            "helpText": "Include any follow-up actions, product interests, or contact preferences.",
            "label": "Notes / Conversation summary",
            "placeholder": "Key discussion points, requirements, agreed next steps",
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
            "y": 998
          },
          "props": {
            "height": 120,
            "helpText": "You can view the event terms for more details.",
            "label": "I consent to be contacted for follow-up regarding products, services and offers related to this event.",
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
            "y": 1142
          },
          "props": {
            "height": 72,
            "label": "Log Visit",
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
      "title": "Trade Show Booth Visit Log \u2014 Sydney"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "6a8beebabb80d0bf2f9ffc52a07a8c374eaffdc165f8f65a58936e2a3d82e726",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p08-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p08-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p08-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p08-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p08-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p08-au-adversarial-r1",
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
  "duration_ms": 84188,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
          "id": "text-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "label": "Company",
            "options": [],
            "placeholder": "Company / Organization",
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
            "helpText": "Collect postal ZIP code (US format). Include even if not local.",
            "label": "ZIP code",
            "options": [],
            "placeholder": "ZIP code",
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
            "helpText": "Please include the +1 country code in phone numbers.",
            "label": "Phone (+1)",
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
          "id": "email-6",
          "position": {
            "x": 424,
            "y": 292
          },
          "props": {
            "height": 110,
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "What product or solution area is the visitor most interested in?",
            "label": "Area of interest",
            "options": [
              {
                "label": "Product demos",
                "value": "product_demos"
              },
              {
                "label": "Pricing & licensing",
                "value": "pricing"
              },
              {
                "label": "Technical integration / APIs",
                "value": "integration"
              },
              {
                "label": "Partnerships / reselling",
                "value": "partnerships"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select area of interest",
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
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "When does the visitor expect to make a purchase or decision?",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate (0-3 months)",
                "value": "0-3_months"
              },
              {
                "label": "Near term (3-6 months)",
                "value": "3-6_months"
              },
              {
                "label": "Mid term (6-12 months)",
                "value": "6-12_months"
              },
              {
                "label": "Longer term (12+ months)",
                "value": "12+_months"
              },
              {
                "label": "Undecided / researching",
                "value": "undecided"
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
            "y": 570
          },
          "props": {
            "height": 200,
            "helpText": "Record key details from the conversation to help with follow-up.",
            "label": "Notes",
            "options": [],
            "placeholder": "Notes from conversation, product needs, action items",
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
            "helpText": "I agree to be contacted for follow-up in accordance with the event terms.",
            "label": "Consent to follow up",
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
            "y": 1018
          },
          "props": {
            "height": 72,
            "label": "Log Visit",
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

## Row 25: `p09-au-neutral-r1__r01`

- Prompt ID: `p09-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "0793d94a0416423190bae7fe30947d12443d65742e0fe2e3cf64455fb2eb7b16",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 46819,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "newsletter-subscription",
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
            "placeholder": "Your first name",
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
            "helpText": "We\u2019ll use this to send the newsletter. We\u2019ll never share your email.",
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
            "helpText": "Select the topics you\u2019d like to receive.",
            "label": "Content interests",
            "options": [
              {
                "label": "Product updates",
                "value": "product_updates"
              },
              {
                "label": "Events & webinars",
                "value": "events_webinars"
              },
              {
                "label": "Blog posts & articles",
                "value": "blog_posts"
              },
              {
                "label": "Special offers",
                "value": "special_offers"
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
            "helpText": "Choose the email frequency that suits you.",
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
            "helpText": "By subscribing you consent to receive promotional messages from us.",
            "label": "I agree to receive marketing emails and understand I can unsubscribe at any time.",
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
      "title": "Newsletter Subscription"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "f35aa3283d88862e0d8de01111052c21f6e97d90855a996c4bb128d62e98c793",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 56211,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "newsletter-sydney",
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
            "label": "Get the latest news and schedules for the Sydney event. Tell us what you care about and how often you'd like to hear from us.",
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
            "placeholder": "Your first name",
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
          "id": "email-3",
          "position": {
            "x": 324,
            "y": 96
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send newsletters to this address.",
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
          "id": "checkbox-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 120,
            "helpText": "Choose the topics you'd like to receive about.",
            "label": "Content interests",
            "options": [
              {
                "label": "Event news & schedule",
                "value": "event_news"
              },
              {
                "label": "Speakers & sessions",
                "value": "speakers"
              },
              {
                "label": "Promotions & offers",
                "value": "promotions"
              },
              {
                "label": "Jobs & opportunities",
                "value": "jobs"
              },
              {
                "label": "Research & insights",
                "value": "insights"
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
            "y": 374
          },
          "props": {
            "height": 120,
            "helpText": "How often would you like to receive emails?",
            "label": "Email frequency",
            "options": [
              {
                "label": "As published (immediate)",
                "value": "immediate"
              },
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
            "y": 518
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive marketing communications about the Sydney event and accept the event terms.",
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
            "y": 662
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
      "title": "Sydney Event Newsletter Subscription"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "663bc91f80038f6576c615c718803d64738f964feae536df0e0b05169b4b9491",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p09-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p09-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p09-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p09-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p09-au-adversarial-r1",
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
  "duration_ms": 33996,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "newsletter-subscription",
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
            "placeholder": "e.g., Alex",
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
            "placeholder": "e.g., Smith",
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
            "helpText": "We\u2019ll send a confirmation to this address.",
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
            "helpText": "Provide a phone number with +1 country code.",
            "label": "Phone (+1)",
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
            "helpText": "Postal ZIP code.",
            "label": "ZIP code",
            "placeholder": "12345",
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
            "helpText": "Select all topics you\u2019re interested in.",
            "label": "Content interests",
            "options": [
              {
                "label": "Product updates",
                "value": "product_updates"
              },
              {
                "label": "Event announcements",
                "value": "events"
              },
              {
                "label": "Case studies & reports",
                "value": "case_studies"
              },
              {
                "label": "Promotions & offers",
                "value": "promotions"
              },
              {
                "label": "Blog posts & articles",
                "value": "blog"
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
            "helpText": "Choose the frequency that suits you.",
            "label": "How often would you like to hear from us?",
            "options": [
              {
                "label": "Weekly",
                "value": "weekly"
              },
              {
                "label": "Bi-weekly",
                "value": "biweekly"
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
            "helpText": "Optional: receive marketing communications about products and offers.",
            "label": "Marketing opt-in",
            "options": [
              {
                "label": "Yes \u2014 send me marketing emails",
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
            "y": 858
          },
          "props": {
            "height": 120,
            "helpText": "By subscribing you agree to our event terms.",
            "label": "Agreement",
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
      "title": "Newsletter Subscription"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "55eeb548e9ae1477ac19ef62d5ac0137baa19cdc383338feff618faacad874c8",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 75383,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1646,
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
            "label": "Your pledge helps us continue our programs. Complete the form below to register your donation intent. We'll send a receipt according to your preference.",
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
            "helpText": "As you'd like it to appear on the receipt",
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
            "helpText": "As you'd like it to appear on the receipt",
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
            "helpText": "We'll email your receipt to this address",
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
            "helpText": "Optional \u2014 in case we need to contact you about your pledge",
            "label": "Phone (optional)",
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
            "helpText": "Provide if you prefer a mailed receipt or for postal correspondence",
            "label": "Postal address (optional)",
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
            "helpText": "Select a preset amount or enter a custom amount",
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
                "label": "Other amount",
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
          "id": "number-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Only fill this if you selected 'Other amount' above",
            "label": "Custom amount (AUD)",
            "placeholder": "Enter amount (numbers only)",
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
            "helpText": "Choose whether this is a one-off pledge or recurring support",
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
          "id": "date-10",
          "position": {
            "x": 424,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "If recurring, choose the date for the first scheduled payment",
            "label": "First payment date (optional)",
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
          "id": "dropdown-11",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 110,
            "helpText": "How would you like to receive your donation receipt?",
            "label": "Receipt preference",
            "options": [
              {
                "label": "Email receipt",
                "value": "email"
              },
              {
                "label": "Postal receipt",
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
            "height": 110,
            "width": 360
          },
          "type": "dropdown"
        },
        {
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 910
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you'd like a tax-deductible receipt where applicable",
            "label": "Tax receipt",
            "options": [
              {
                "label": "I would like a tax receipt",
                "value": "tax_receipt"
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
          "id": "checkbox-13",
          "position": {
            "x": 40,
            "y": 1054
          },
          "props": {
            "height": 120,
            "helpText": "Receive news and campaign updates. You can unsubscribe at any time.",
            "label": "Campaign updates",
            "options": [
              {
                "label": "Please send me campaign updates and news",
                "value": "campaign_updates"
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
          "id": "textarea-14",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 200,
            "helpText": "This message will be stored with your pledge and may appear on internal records",
            "label": "Dedication or message (optional)",
            "placeholder": "Leave a note for your pledge (e.g., in honour of someone)",
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
          "id": "submit-button-15",
          "position": {
            "x": 40,
            "y": 1502
          },
          "props": {
            "height": 72,
            "helpText": "Click to submit your pledge. We'll follow up with payment instructions if required.",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "534401316c956a61efbc17e38ed256f6b16fd526728613f4eadc81e9d934c855",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 72358,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "label": "Please complete your details below to pledge a donation. We will send a receipt if requested.",
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
            "helpText": "We'll use this to send your receipt and donation confirmation.",
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
            "label": "Phone number (optional)",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Donation amount (AUD)",
            "options": [
              {
                "label": "A$25",
                "value": "25"
              },
              {
                "label": "A$50",
                "value": "50"
              },
              {
                "label": "A$100",
                "value": "100"
              },
              {
                "label": "A$250",
                "value": "250"
              },
              {
                "label": "Other (enter below)",
                "value": "other"
              }
            ],
            "placeholder": "Select an amount or choose Other",
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
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Enter a whole number (e.g. 75).",
            "label": "Other amount (AUD)",
            "placeholder": "Enter a custom amount in AUD",
            "tabOrder": 7,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 360
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
            "helpText": "Choose one-off or set up a recurring pledge.",
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
          "id": "date-9",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Leave blank for immediate start.",
            "label": "Start date (for recurring)",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 9,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "radio-10",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "label": "Would you like a donation receipt?",
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
          "id": "text-11",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 110,
            "label": "Receipt name (optional)",
            "placeholder": "Name or organisation for receipt",
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
          "id": "email-12",
          "position": {
            "x": 424,
            "y": 786
          },
          "props": {
            "height": 110,
            "label": "Receipt email (optional)",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 12,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "checkbox-13",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to receive news and updates about this Sydney campaign.",
            "label": "Campaign updates",
            "options": [
              {
                "label": "Yes \u2014 send me campaign updates by email",
                "value": "opt_in_updates"
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
            "y": 1064
          },
          "props": {
            "height": 120,
            "helpText": "By pledging you accept the event terms. (company-managed)",
            "label": "I agree to the event terms",
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
            "y": 1208
          },
          "props": {
            "height": 72,
            "label": "Pledge Donation",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "c40f7ddd92b35513908267e2de9c45da8a09b20879d2f003b6b644e5361f3a03",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p10-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p10-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p10-au-adversarial-r1",
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
  "duration_ms": 56882,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1486,
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
            "label": "Thank you for supporting our cause. This form collects donor details, your pledge amount and frequency, receipt information, and consent for updates.",
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
            "helpText": "As it should appear on your receipt",
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
          "id": "email-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We use this to send your receipt and donation updates.",
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
            "helpText": "Include country code. Entering a phone helps us contact you about your pledge.",
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
            "helpText": "Postal code for your billing or mailing address.",
            "label": "ZIP / Postal code",
            "placeholder": "e.g. 02139",
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
            "helpText": "Choose a suggested amount or select Other to enter a custom pledge.",
            "label": "Pledge amount (USD)",
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
          "id": "number-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter a custom pledge amount if you selected Other.",
            "label": "Other amount (USD)",
            "placeholder": "Enter amount in USD",
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
            "helpText": "Select whether this pledge is a one-off or recurring donation.",
            "label": "Donation frequency",
            "options": [
              {
                "label": "One-off",
                "value": "one_off"
              },
              {
                "label": "Monthly (recurring)",
                "value": "recurring_monthly"
              },
              {
                "label": "Annually (recurring)",
                "value": "recurring_annual"
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
            "y": 776
          },
          "props": {
            "height": 110,
            "helpText": "Name to appear on your tax receipt (optional).",
            "label": "Receipt name (as you'd like it to appear)",
            "placeholder": "Full name or organisation",
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
            "y": 910
          },
          "props": {
            "height": 120,
            "helpText": "If checked, we will send a tax receipt to the email address provided.",
            "label": "Send a tax receipt",
            "options": [
              {
                "label": "Yes \u2014 please send a tax receipt",
                "value": "send_receipt"
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
            "y": 1054
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to receive email updates about our campaigns and events.",
            "label": "Campaign updates",
            "options": [
              {
                "label": "I would like to receive campaign updates",
                "value": "updates_opt_in"
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
            "y": 1198
          },
          "props": {
            "height": 120,
            "helpText": "By submitting this pledge you agree to the event terms and privacy policy.",
            "label": "Agreement and terms",
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
            "y": 1342
          },
          "props": {
            "height": 72,
            "helpText": "Click to submit your pledge. We'll follow up with confirmation and receipt details.",
            "label": "Submit Pledge",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "9b013010856eb0def5c5d2eb8873c0addef89416579987291d2414e9e4bd186d",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "component_count": 9,
  "duration_ms": 71570,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "international-event-registration",
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
            "helpText": "We'll use this to send your ticket and event updates.",
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
            "helpText": "Include country code so we can contact you if needed.",
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
                "label": "Brazil",
                "value": "BR"
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
            "helpText": "Choose the timezone where you will attend from.",
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
                "label": "UTC\u221210:00",
                "value": "UTC-10"
              },
              {
                "label": "UTC\u221209:00",
                "value": "UTC-9"
              },
              {
                "label": "UTC\u221208:00 (PST)",
                "value": "UTC-8"
              },
              {
                "label": "UTC\u221207:00 (MST)",
                "value": "UTC-7"
              },
              {
                "label": "UTC\u221206:00 (CST)",
                "value": "UTC-6"
              },
              {
                "label": "UTC\u221205:00 (EST)",
                "value": "UTC-5"
              },
              {
                "label": "UTC\u221204:00",
                "value": "UTC-4"
              },
              {
                "label": "UTC\u221203:00",
                "value": "UTC-3"
              },
              {
                "label": "UTC\u221202:00",
                "value": "UTC-2"
              },
              {
                "label": "UTC\u221201:00",
                "value": "UTC-1"
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
                "label": "UTC+05:00",
                "value": "UTC+5"
              },
              {
                "label": "UTC+05:30",
                "value": "UTC+5:30"
              },
              {
                "label": "UTC+06:00",
                "value": "UTC+6"
              },
              {
                "label": "UTC+07:00",
                "value": "UTC+7"
              },
              {
                "label": "UTC+08:00",
                "value": "UTC+8"
              },
              {
                "label": "UTC+09:00",
                "value": "UTC+9"
              },
              {
                "label": "UTC+10:00",
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
              },
              {
                "label": "Other",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select your timezone (UTC offset)",
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
            "helpText": "Select all sessions you plan to attend.",
            "label": "Sessions you're interested in",
            "options": [
              {
                "label": "Keynote: The Future of AI",
                "value": "keynote_ai"
              },
              {
                "label": "Workshop: Hands-on Labs",
                "value": "workshop_labs"
              },
              {
                "label": "Panel: Global Trends",
                "value": "panel_trends"
              },
              {
                "label": "Networking Session",
                "value": "networking"
              },
              {
                "label": "Product Deep Dive",
                "value": "product_deep_dive"
              },
              {
                "label": "Other",
                "value": "other_session"
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
            "y": 570
          },
          "props": {
            "height": 120,
            "helpText": "By registering you agree to share your contact details with the event organisers for registration and event-related communication.",
            "label": "I consent to receive event communications and agree to the event terms and privacy practices.",
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
            "y": 714
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "ea480e92f16b62fcd90523064237a94d3510558cd3d9b8f0a689b94540a47aa2",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 70752,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "intl-online-event-sydney",
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
            "helpText": "The event is associated with Sydney (Australia). Session times will be listed in Australia/Sydney timezone. Select your timezone so we can provide localisation details.",
            "label": "Event association",
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
            "helpText": "We'll use this to send your registration confirmation and session links.",
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
            "helpText": "Include your country code. For SMS updates about the event.",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Country of residence for regional communications and time conversions.",
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
                "label": "Brazil",
                "value": "BR"
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
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Event times will be published in Australia/Sydney. Choose your timezone so we can show localised session times.",
            "label": "Your timezone",
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
                "label": "Europe/London (GMT/BST)",
                "value": "Europe/London"
              },
              {
                "label": "America/New_York (EST/EDT)",
                "value": "America/New_York"
              },
              {
                "label": "America/Los_Angeles (PST/PDT)",
                "value": "America/Los_Angeles"
              },
              {
                "label": "Asia/Tokyo (JST)",
                "value": "Asia/Tokyo"
              },
              {
                "label": "Asia/Shanghai (CST)",
                "value": "Asia/Shanghai"
              },
              {
                "label": "Asia/Kolkata (IST)",
                "value": "Asia/Kolkata"
              },
              {
                "label": "Europe/Berlin (CET/CEST)",
                "value": "Europe/Berlin"
              },
              {
                "label": "Other",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select your timezone (event: Australia/Sydney)",
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
            "helpText": "Select all sessions you plan to attend or are interested in.",
            "label": "Sessions you're interested in",
            "options": [
              {
                "label": "Opening Keynote",
                "value": "keynote"
              },
              {
                "label": "Technical Workshop",
                "value": "workshop"
              },
              {
                "label": "Networking Session",
                "value": "networking"
              },
              {
                "label": "Closing Panel",
                "value": "closing"
              },
              {
                "label": "Other / Unsure",
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
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event terms to complete registration.",
            "label": "Consent & terms",
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
      "title": "International Online Event Registration (Sydney)"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "2dbe48f36e81be1a67a01ce2ed8b54261cb3a4bfce7ae13345e972598e9b9045",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "duration_ms": 65779,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "This registration form collects basic attendee details, location, session interests and consent to the event terms.",
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
            "helpText": "We will send your registration confirmation here.",
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
            "helpText": "Include country code \u2014 e.g. +1 for US/Canada (presented intentionally).",
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
                "label": "United States",
                "value": "US"
              },
              {
                "label": "Canada",
                "value": "CA"
              },
              {
                "label": "United Kingdom",
                "value": "GB"
              },
              {
                "label": "Australia",
                "value": "AU"
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
          "id": "text-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Enter your postal code. (ZIP wording intentionally included.)",
            "label": "ZIP / Postal code",
            "placeholder": "e.g. 90210 or SW1A 1AA",
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
            "helpText": "Choose the timezone that applies to your primary location.",
            "label": "Timezone",
            "options": [
              {
                "label": "UTC\u221212:00",
                "value": "UTC-12:00"
              },
              {
                "label": "UTC\u221208:00 (US Pacific)",
                "value": "UTC-08:00"
              },
              {
                "label": "UTC\u221205:00 (US Eastern)",
                "value": "UTC-05:00"
              },
              {
                "label": "UTC (GMT)",
                "value": "UTC+00:00"
              },
              {
                "label": "UTC+01:00 (CET)",
                "value": "UTC+01:00"
              },
              {
                "label": "UTC+10:00 (AEST)",
                "value": "UTC+10:00"
              },
              {
                "label": "Other / Not listed",
                "value": "OTHER"
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
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply.",
            "label": "Which sessions are you interested in?",
            "options": [
              {
                "label": "Opening Keynote",
                "value": "keynote"
              },
              {
                "label": "Workshop: Product Strategy",
                "value": "workshop_product"
              },
              {
                "label": "Workshop: Technical Deep Dive",
                "value": "workshop_tech"
              },
              {
                "label": "Panel Discussion",
                "value": "panel"
              },
              {
                "label": "Networking Session",
                "value": "networking"
              },
              {
                "label": "Virtual-only attendance",
                "value": "virtual"
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
            "helpText": "By registering you agree to the event terms.",
            "label": "Terms & Consent",
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "fca64bf05a5edc92624c9ca4e6202916b32193fdd7bc2d09de5ef5d81579c1a4",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "matched_text": "+44",
    "prompt_id": "p12-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "privacy_law_without_au_anchor",
    "description": "GDPR/CCPA-only privacy wording where AU privacy wording is expected",
    "matched_text": "GDPR",
    "prompt_id": "p12-au-neutral-r1",
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
  "component_count": 9,
  "duration_ms": 58344,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "helpText": "We will process your personal data to manage your registration, send event updates, and meet legal obligations. Data is retained only as long as necessary. For information about your rights or to contact our data team, please use the contact details you provide below.",
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
            "placeholder": "Enter your first name",
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
            "placeholder": "Enter your last name",
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
            "helpText": "We will use this address for registration confirmations and event updates.",
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
            "helpText": "Optional \u2014 include country code if outside your country.",
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
            "label": "Organization / Company (optional)",
            "placeholder": "Your organisation",
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
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive promotional emails about future events and related offers. You can withdraw consent at any time.",
            "label": "Marketing communications (optional)",
            "options": [
              {
                "label": "Yes \u2014 I consent to receive marketing emails",
                "value": "marketing_emails"
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
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "I consent to the organiser processing my personal data for event registration, communications, and necessary administrative purposes. I acknowledge that the lawful basis for processing is my consent and activities necessary to perform event administration. I understand my rights to access, correct, restrict, or request deletion of my data and that I may withdraw consent at any time.",
            "label": "GDPR consent and lawful-basis acknowledgement",
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
            "y": 786
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
      "title": "EU Event Registration"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "d7fdcdb6a56e3792c4053500ddc94d418a6a4de863646d42e42fd2c9af2ad4d5",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 73193,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "sydney-eu-event-registration",
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
            "helpText": "We process personal data for event administration, attendance management, and emergency contact. Read the event terms for full details.",
            "label": "Please review the data handling notice below and provide your contact details. This event is associated with Sydney. Individuals from the EU must confirm GDPR-related acknowledgements before registering.",
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
            "helpText": "As shown on your ID",
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
            "helpText": "We will send event updates and your registration confirmation to this address.",
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
            "helpText": "Provide an international-format number for urgent contact on the day.",
            "label": "Phone number",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Organization / Company (optional)",
            "placeholder": "Your organisation",
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
          "id": "address-7",
          "position": {
            "x": 417,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide if you require mailed materials or an invoice.",
            "label": "Postal address (optional)",
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
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Confirm you have read how we lawfully process your data for event administration.",
            "label": "Lawful-basis acknowledgement",
            "options": [
              {
                "label": "I acknowledge that the lawful basis for processing my personal data for event administration is set out in the data handling notice and may include legitimate interests, contract performance, or consent where applicable.",
                "value": "lawful_basis_ack"
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
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "Consent required to process the personal data necessary to register you and manage attendance/emergency contact.",
            "label": "GDPR processing consent for registration",
            "options": [
              {
                "label": "I consent to the processing of my personal data for registration, attendance management and emergency contact purposes.",
                "value": "registration_processing_consent"
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
            "helpText": "Optional consent under GDPR for marketing about future events.",
            "label": "Marketing communications (optional)",
            "options": [
              {
                "label": "I consent to receive marketing and promotional communications about future events by email.",
                "value": "marketing_email_consent"
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
            "helpText": "Please review and accept the event terms before submitting. (Opens company-managed terms.)",
            "label": "Accept event terms",
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
      "title": "Sydney Event Registration (EU)"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "a9f7830932b46446f8937967fa9708d9f7e645c49a86af535413fa8677287c0d",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p12-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p12-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
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
  },
  {
    "check_id": "privacy_law_without_au_anchor",
    "description": "GDPR/CCPA-only privacy wording where AU privacy wording is expected",
    "matched_text": "gdpr",
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
  "component_count": 11,
  "duration_ms": 66291,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "eu-event-registration-gdpr",
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
            "label": "Data handling notice: We collect and process the personal data you provide to register you for this event. Your data will be used for event administration, communications about this event, and as otherwise described in our event terms. Where required by law we rely on the lawful basis you select below. You have rights to access, correct, and request deletion of your personal data.",
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
            "helpText": "Enter your first name as it appears on official ID",
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
            "helpText": "We will send event confirmations and updates to this address",
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
            "helpText": "Provide a phone number we can use for urgent event updates. The form requests +1 country-code formatting by design.",
            "label": "Phone (include country code, e.g. +1)",
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
            "helpText": "Include full postal address for any physical correspondence",
            "label": "Postal address",
            "placeholder": "Street address, city, country",
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
            "helpText": "Include your ZIP / postal code",
            "label": "ZIP / Postal Code",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select the lawful basis under EU GDPR that applies to processing your data for this event.",
            "label": "Lawful basis for processing (GDPR)",
            "options": [
              {
                "label": "Consent (you give consent for event communications)",
                "value": "consent"
              },
              {
                "label": "Contract (processing is necessary to perform a contract)",
                "value": "contract"
              },
              {
                "label": "Legal obligation",
                "value": "legal_obligation"
              },
              {
                "label": "Vital interests",
                "value": "vital_interests"
              },
              {
                "label": "Public task",
                "value": "public_task"
              },
              {
                "label": "Legitimate interests (we have a legitimate interest)",
                "value": "legitimate_interests"
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
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "I acknowledge the lawful basis I selected and consent to the collection and processing of my personal data for the purposes described. I have read the event terms and data handling notice.",
            "label": "GDPR consent and acknowledgement",
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
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 120,
            "helpText": "Choose how you'd like to receive optional marketing or follow-up communications. These are optional and will be used only if you opt in.",
            "label": "Marketing & communications preferences (optional)",
            "options": [
              {
                "label": "Email updates about future events",
                "value": "marketing_email"
              },
              {
                "label": "SMS updates about future events (+1 suggested format)",
                "value": "marketing_sms"
              },
              {
                "label": "Postal mail about future events",
                "value": "marketing_post"
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
            "y": 930
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
      "title": "EU Event Registration \u2014 GDPR Consent"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "1f7748bcc74eafc6a13e27742f0800bbda98b88e72a568354e99ec97bcd3bfb0",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "section_id": "candidate_prompt_block"
  }
]
```

### Deterministic AU Findings

```json
[
  {
    "check_id": "foreign_date_format",
    "description": "MM/DD/YYYY where DD/MM/YYYY is expected",
    "matched_text": "MM/DD/YYYY",
    "prompt_id": "p13-au-neutral-r1",
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
  "component_count": 13,
  "duration_ms": 47445,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1492,
    "width": 960
  },
  "formId": "us-onboarding-interest",
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
            "label": "Please provide your contact details and the role you're interested in. Fields marked required must be completed.",
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
            "helpText": "We'll use this to follow up about onboarding next steps.",
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
            "helpText": "Optional \u2014 include country code if outside the US.",
            "label": "Phone number",
            "placeholder": "([SCRUBBED_PHONE]",
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
            "helpText": "Optional \u2014 leave blank if you're an individual applicant.",
            "label": "Organization",
            "placeholder": "Company or organisation (if applicable)",
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
            "helpText": "Choose the best match for your interest.",
            "label": "Role you're interested in",
            "options": [
              {
                "label": "Software Engineer / Developer",
                "value": "engineer"
              },
              {
                "label": "Product Manager",
                "value": "product"
              },
              {
                "label": "Designer",
                "value": "design"
              },
              {
                "label": "Sales / Business Development",
                "value": "sales"
              },
              {
                "label": "Marketing",
                "value": "marketing"
              },
              {
                "label": "Operations / HR",
                "value": "operations"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a role",
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
            "helpText": "Optional \u2014 use this if you selected Other above.",
            "label": "If Other, please specify",
            "placeholder": "Role or title",
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
          "id": "date-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 if you have a preferred start or onboarding date.",
            "label": "Preferred start date",
            "placeholder": "MM/DD/YYYY",
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
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 110,
            "label": "How did you hear about us?",
            "options": [
              {
                "label": "Company website",
                "value": "website"
              },
              {
                "label": "Referral",
                "value": "referral"
              },
              {
                "label": "Job board",
                "value": "job_board"
              },
              {
                "label": "Social media",
                "value": "social"
              },
              {
                "label": "Recruiter",
                "value": "recruiter"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select an option",
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
            "y": 900
          },
          "props": {
            "height": 200,
            "helpText": "Include anything you'd like us to know about your fit for the role or onboarding preferences.",
            "label": "Tell us a bit about your background or interest",
            "placeholder": "Brief summary of experience, availability, or questions (200\u2013500 words recommended)",
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
            "y": 1204
          },
          "props": {
            "height": 120,
            "helpText": "Select any types of communications you'd like to receive.",
            "label": "Communications preferences",
            "options": [
              {
                "label": "Email updates about onboarding and opportunities",
                "value": "email_updates"
              },
              {
                "label": "SMS/text updates",
                "value": "sms_updates"
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
            "y": 1348
          },
          "props": {
            "height": 72,
            "label": "Submit interest",
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
      "title": "US Onboarding Interest Form"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "76e0fa9cbc6bde6390848f07781597215aa0155f8784cc9c63cfb82b69d5e158",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p13-au-ambiguous-r1",
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
  "duration_ms": 58073,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "us-onboarding-interest-sydney",
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
            "label": "This form is for US-based onboarding interest related to the Sydney event. We will not ask for SSN or TIN.",
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
            "label": "Company",
            "placeholder": "Organization name (optional)",
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
            "helpText": "Select the option that best matches your role for onboarding",
            "label": "Role",
            "options": [
              {
                "label": "Attendee",
                "value": "attendee"
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
                "label": "Partner",
                "value": "partner"
              },
              {
                "label": "Recruiter / HR",
                "value": "recruiter"
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
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Job title",
            "placeholder": "e.g., Product Manager",
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
            "y": 632
          },
          "props": {
            "height": 200,
            "label": "Additional notes or questions",
            "placeholder": "Tell us about your interest or any questions you have (optional)",
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
            "helpText": "Please review and accept the event terms to proceed.",
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
            "y": 1080
          },
          "props": {
            "height": 72,
            "label": "Submit interest",
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
      "title": "US Onboarding Interest \u2014 Sydney Event"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "94e662a2411cd1e143ddc833292ebc03d867e61a2f611b446723cfb776fa2925",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p13-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p13-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p13-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p13-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p13-au-adversarial-r1",
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
  "duration_ms": 59208,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "us-onboarding-interest",
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
            "label": "Please share your contact details and role so we can follow up about opportunities. We will not request SSN or TIN on this form.",
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
            "helpText": "Please include country code +1.",
            "label": "Phone (+1)",
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
            "helpText": "US ZIP format expected",
            "label": "ZIP code",
            "placeholder": "e.g. 90210",
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
            "label": "Role",
            "options": [
              {
                "label": "Attendee",
                "value": "attendee"
              },
              {
                "label": "Speaker",
                "value": "speaker"
              },
              {
                "label": "Organizer",
                "value": "organizer"
              },
              {
                "label": "Volunteer",
                "value": "volunteer"
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
          "id": "textarea-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 200,
            "helpText": "Share any relevant experience or preferences.",
            "label": "Tell us about your interests",
            "placeholder": "What are you most interested in (events, speaking, volunteering, sponsorship)?",
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
            "y": 802
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms.",
            "label": "Terms and acknowledgement",
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
            "y": 946
          },
          "props": {
            "height": 72,
            "label": "Submit interest",
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
      "title": "US Onboarding Interest Form"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "2b2c9a18feed2339d814d663ea378d7e459fd9701c3a37906e52998a784076dc",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "matched_text": "+44",
    "prompt_id": "p14-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+44",
    "prompt_id": "p14-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "nhs",
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
  "component_count": 16,
  "duration_ms": 57114,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "uk-nhs-waiver",
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
            "label": "This waiver collects participant details, relevant health information, and emergency contact details for activities run in association with NHS-adjacent services. Completing this form does not replace medical advice. If you have urgent medical concerns, contact your GP or local health services.",
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
            "helpText": "As shown on official ID",
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
            "helpText": "Used to verify age where relevant",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "text-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Providing your NHS number helps match records but is optional.",
            "label": "NHS number (optional)",
            "placeholder": "10\u2011digit NHS number (if known)",
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
          "id": "email-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "We may use this to send confirmation and safety updates.",
            "label": "Email address (optional)",
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
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Mobile or landline we can use in an emergency",
            "label": "Primary phone number",
            "placeholder": "+44 7xxx xxxxxx",
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
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select any conditions we should be aware of. If none apply, choose 'None of the above'.",
            "label": "Pre-existing health conditions (select all that apply)",
            "options": [
              {
                "label": "Asthma or chronic respiratory condition",
                "value": "asthma"
              },
              {
                "label": "Heart condition or circulatory issue",
                "value": "heart"
              },
              {
                "label": "Diabetes",
                "value": "diabetes"
              },
              {
                "label": "Neurological condition (e.g. epilepsy)",
                "value": "neurological"
              },
              {
                "label": "Pregnant or possibly pregnant",
                "value": "pregnant"
              },
              {
                "label": "None of the above",
                "value": "none"
              },
              {
                "label": "Prefer not to say",
                "value": "prefer_not_to_say"
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
            "helpText": "Provide details that may be relevant in an emergency or to manage participation safely.",
            "label": "Other health information or current medications (optional)",
            "placeholder": "List any medications, allergies, or other details we should know",
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
            "y": 946
          },
          "props": {
            "height": 110,
            "helpText": "Person we should contact if there is an incident",
            "label": "Emergency contact \u2014 Full name",
            "placeholder": "Name of primary emergency contact",
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
            "y": 946
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Phone",
            "placeholder": "+44 7xxx xxxxxx",
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
            "y": 1080
          },
          "props": {
            "height": 110,
            "label": "Emergency contact \u2014 Relationship to participant",
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
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 120,
            "helpText": "This is a legal acknowledgement. Please read carefully before consenting.",
            "label": "Consent and waiver: I confirm that the information I have provided is accurate to the best of my knowledge. I understand the nature of the activities and accept the risks involved. By checking this box I voluntarily consent to participate in activities affiliated with this NHS-adjacent programme and agree to the waiver and release of liability where permitted by law.",
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
          "id": "text-14",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 110,
            "helpText": "Typing your name acts as a digital signature confirming consent.",
            "label": "Digital signature \u2014 Full name",
            "placeholder": "Type your full name to sign",
            "tabOrder": 14,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "text"
        },
        {
          "id": "date-15",
          "position": {
            "x": 424,
            "y": 1358
          },
          "props": {
            "height": 110,
            "label": "Date signed",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 15,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "submit-button-16",
          "position": {
            "x": 40,
            "y": 1492
          },
          "props": {
            "height": 72,
            "helpText": "Submit your responses. You will receive a confirmation if an email was provided.",
            "label": "Submit Waiver",
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
      "title": "NHS-adjacent Participant Waiver"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "afc7646351792867b4dfbc4ef7d5ff621bb5f7cead189b80faf528b1a658499c",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "matched_text": "nhs",
    "prompt_id": "p14-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "NHS",
    "prompt_id": "p14-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "NHS",
    "prompt_id": "p14-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
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
  "component_count": 16,
  "duration_ms": 58264,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
  "formId": "nhs-adjacent-waiver-sydney",
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
            "label": "This waiver collects participant details and relevant health information to help event staff support you safely. Where legal acknowledgment is required, you will be asked to accept the event terms.",
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
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 4,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "date"
        },
        {
          "id": "text-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 provide only if applicable.",
            "label": "NHS number (optional)",
            "placeholder": "If available, provide NHS number",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide your usual residential address.",
            "label": "Home address",
            "placeholder": "Street, city, postcode",
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
          "id": "email-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
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
          "id": "phone-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Number we can use to contact you about the event.",
            "label": "Phone number",
            "placeholder": "+61 4XX XXX XXX",
            "tabOrder": 8,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 200,
            "helpText": "This information helps event staff respond appropriately in an emergency.",
            "label": "Relevant health information (allergies, medical conditions, medications)",
            "placeholder": "List any conditions, allergies, medications, mobility needs or other details relevant to participation. If none, write 'None'.",
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
            "y": 936
          },
          "props": {
            "height": 48,
            "label": "Emergency contact \u2014 someone we can reach if needed during the event.",
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
          "id": "text-11",
          "position": {
            "x": 40,
            "y": 1008
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
            "y": 1008
          },
          "props": {
            "height": 110,
            "label": "Emergency contact phone",
            "placeholder": "+61 4XX XXX XXX",
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
          "id": "dropdown-13",
          "position": {
            "x": 40,
            "y": 1142
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
          "id": "checkbox-14",
          "position": {
            "x": 40,
            "y": 1276
          },
          "props": {
            "height": 120,
            "helpText": "Tick to confirm accuracy of the information provided.",
            "label": "Confirmation",
            "options": [
              {
                "label": "I confirm that the information I have provided is accurate to the best of my knowledge.",
                "value": "confirm_accuracy"
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
            "y": 1420
          },
          "props": {
            "height": 120,
            "helpText": "Please review the event terms before accepting. (Company-managed terms will be presented.)",
            "label": "I agree to the event terms and waiver",
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
            "y": 1564
          },
          "props": {
            "height": 72,
            "label": "Submit waiver",
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
      "title": "NHS-style Participant Waiver \u2014 Sydney Event"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "6d2fdd76a248420f39069b365680bad7ca1fd6e8ee5d04af3098cf0673c23cf8",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+1",
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "nhs",
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "NHS",
    "prompt_id": "p14-au-adversarial-r1",
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
  "duration_ms": 77602,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1912,
    "width": 960
  },
  "formId": "nhs-adj-waiver-uk",
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
            "label": "This form collects participant and health information to support safe participation. It includes a consent acknowledgement (company-managed event terms).",
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
            "helpText": "Provide your date of birth to help clinical assessment if required.",
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
            "helpText": "Please include the +1 country code as requested.",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE]",
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
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter your postal code. ZIP is requested per form instructions.",
            "label": "ZIP / Postcode",
            "placeholder": "e.g. SW1A 1AA or 12345",
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
          "id": "divider-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 20,
            "tabOrder": 8,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 676
          },
          "props": {
            "height": 120,
            "helpText": "Select any conditions that apply.",
            "label": "Relevant health conditions",
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
                "label": "Allergies",
                "value": "allergies"
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
            "y": 820
          },
          "props": {
            "height": 200,
            "helpText": "Provide any details that event clinical staff should know.",
            "label": "Health details and medications",
            "placeholder": "List any medications, recent surgeries, mobility needs, or other health notes",
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
            "y": 1124
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
            "y": 1168
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
            "y": 1168
          },
          "props": {
            "height": 110,
            "label": "Relationship to participant",
            "placeholder": "e.g. Partner, Parent, Friend",
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
            "y": 1302
          },
          "props": {
            "height": 110,
            "helpText": "Provide a reachable number. Include +1 country code as requested.",
            "label": "Emergency contact phone",
            "placeholder": "[SCRUBBED_PHONE]",
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
            "y": 1302
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
          "id": "divider-16",
          "position": {
            "x": 40,
            "y": 1436
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
          "id": "terms-17",
          "position": {
            "x": 40,
            "y": 1480
          },
          "props": {
            "height": 120,
            "helpText": "Company-managed terms are available via the linked event terms.",
            "label": "I have read and agree to the event terms and release the organisers from liability where permitted by law.",
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
          "id": "checkbox-18",
          "position": {
            "x": 40,
            "y": 1624
          },
          "props": {
            "height": 120,
            "helpText": "Tick to authorise organisers to seek emergency medical treatment if you are unable to consent.",
            "label": "Emergency medical treatment permission",
            "options": [
              {
                "label": "I authorise emergency medical treatment if required",
                "value": "authorize_emergency_treatment"
              }
            ],
            "tabOrder": 18,
            "width": "640px"
          },
          "style": {
            "height": 120,
            "width": 640
          },
          "type": "checkbox"
        },
        {
          "id": "submit-button-19",
          "position": {
            "x": 40,
            "y": 1768
          },
          "props": {
            "height": 72,
            "helpText": "By submitting you confirm the information is accurate to the best of your knowledge.",
            "label": "Sign and Submit",
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
      "title": "NHS-adjacent Participant Waiver"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "c1d551dbff19654cfdf700d57e734e255113361b0f432c19d95352af0e70ea2d",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "matched_text": "+64",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "auckland",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Wellington",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "wellington",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Canterbury",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "canterbury",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Otago",
    "prompt_id": "p15-au-neutral-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "otago",
    "prompt_id": "p15-au-neutral-r1",
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
  "duration_ms": 65084,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1548,
    "width": 960
  },
  "formId": "nz-rsvp",
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
            "label": "Please confirm your attendance and let us know any dietary or accessibility needs. We may use the contact details you provide to share event information and updates.",
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
            "helpText": "Enter a New Zealand phone number. Include country code if you are outside NZ.",
            "label": "Phone (New Zealand)",
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
            "helpText": "Optional \u2014 we'll use this to send event information and updates.",
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
            "helpText": "Select the region where you currently live.",
            "label": "Region",
            "options": [
              {
                "label": "Northland",
                "value": "northland"
              },
              {
                "label": "Auckland",
                "value": "auckland"
              },
              {
                "label": "Waikato",
                "value": "waikato"
              },
              {
                "label": "Bay of Plenty",
                "value": "bay-of-plenty"
              },
              {
                "label": "Gisborne",
                "value": "gisborne"
              },
              {
                "label": "Hawke's Bay",
                "value": "hawkes-bay"
              },
              {
                "label": "Taranaki",
                "value": "taranaki"
              },
              {
                "label": "Manawat\u016b-Whanganui",
                "value": "manawatu-whanganui"
              },
              {
                "label": "Wellington",
                "value": "wellington"
              },
              {
                "label": "Tasman",
                "value": "tasman"
              },
              {
                "label": "Nelson",
                "value": "nelson"
              },
              {
                "label": "Marlborough",
                "value": "marlborough"
              },
              {
                "label": "West Coast",
                "value": "west-coast"
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
                "label": "Southland",
                "value": "southland"
              }
            ],
            "placeholder": "Select your region",
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
            "y": 364
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
            "y": 508
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply. Use the field below to add details or other requirements.",
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
                "label": "No dietary requirements",
                "value": "none"
              },
              {
                "label": "Other",
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
            "y": 652
          },
          "props": {
            "height": 200,
            "helpText": "Include details such as severity, required avoidance, or cross-contamination concerns.",
            "label": "Other or additional dietary details",
            "placeholder": "Describe allergies, intolerances, or special instructions",
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
            "y": 956
          },
          "props": {
            "height": 200,
            "helpText": "Examples: mobility access, hearing/vision support, assistance person, or additional needs.",
            "label": "Accessibility requirements",
            "placeholder": "Please describe any accessibility needs we should plan for",
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
            "y": 1260
          },
          "props": {
            "height": 120,
            "label": "I agree to receive event updates and important information about this event via the contact details I have provided.",
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
            "y": 1404
          },
          "props": {
            "height": 72,
            "label": "Submit RSVP",
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
      "title": "New Zealand RSVP"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "3267597a4813d70d14f1c4277d70a04f16a6470e598fdf25873647a5789f2235",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "matched_text": "+64",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+64",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Auckland",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "auckland",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Canterbury",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "canterbury",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Otago",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "otago",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "Wellington",
    "prompt_id": "p15-au-ambiguous-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "nhs_or_nz_region",
    "description": "NHS or NZ-region leakage",
    "matched_text": "wellington",
    "prompt_id": "p15-au-ambiguous-r1",
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
  "component_count": 13,
  "duration_ms": 80804,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
    "height": 1826,
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
            "label": "This RSVP is for an event associated with Sydney. If you're located in New Zealand, please complete the details below so we can manage capacity and support needs.",
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
            "helpText": "We'll use this to send your RSVP confirmation and event updates if consent is given.",
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
            "helpText": "Include country code (+64) if calling from outside New Zealand.",
            "label": "Phone (NZ)",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Select the New Zealand region where you are based.",
            "label": "Region (New Zealand)",
            "options": [
              {
                "label": "Auckland",
                "value": "auckland"
              },
              {
                "label": "Bay of Plenty",
                "value": "bay_of_plenty"
              },
              {
                "label": "Canterbury",
                "value": "canterbury"
              },
              {
                "label": "Gisborne",
                "value": "gisborne"
              },
              {
                "label": "Hawke's Bay",
                "value": "hawkes_bay"
              },
              {
                "label": "Manawat\u016b-Whanganui",
                "value": "manawatu_whanganui"
              },
              {
                "label": "Marlborough",
                "value": "marlborough"
              },
              {
                "label": "Nelson",
                "value": "nelson"
              },
              {
                "label": "Northland",
                "value": "northland"
              },
              {
                "label": "Otago",
                "value": "otago"
              },
              {
                "label": "Southland",
                "value": "southland"
              },
              {
                "label": "Taranaki",
                "value": "taranaki"
              },
              {
                "label": "Waikato",
                "value": "waikato"
              },
              {
                "label": "Wellington",
                "value": "wellington"
              },
              {
                "label": "West Coast",
                "value": "west_coast"
              }
            ],
            "placeholder": "Select your region",
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
            "helpText": "Please let us know whether you will be attending the event.",
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
            "helpText": "Select all that apply.",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "No special dietary requirements",
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
            "helpText": "Provide details if you selected 'Other'.",
            "label": "If Other, please specify dietary needs",
            "placeholder": "Describe any other dietary requirements",
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
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "Select any accessibility support you require. If none apply, leave blank.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Mobility assistance (e.g. wheelchair access)",
                "value": "mobility"
              },
              {
                "label": "Hearing support (e.g. Auslan/interpreter)",
                "value": "hearing"
              },
              {
                "label": "Visual support (e.g. large print)",
                "value": "visual"
              },
              {
                "label": "Cognitive support",
                "value": "cognitive"
              },
              {
                "label": "Other (please describe)",
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
            "y": 1234
          },
          "props": {
            "height": 200,
            "helpText": "Provide details so we can arrange appropriate support.",
            "label": "Accessibility details",
            "placeholder": "Describe any accessibility requirements or how we can assist you",
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
            "y": 1538
          },
          "props": {
            "height": 120,
            "helpText": "By checking this box you agree to receive event-related updates and communications.",
            "label": "Consent to receive event updates",
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
            "y": 1682
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
      "title": "New Zealand RSVP \u2014 Sydney Event"
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
- Variant: `story-6.4.6-au-baseline-current`
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
    "content_hash": "f8c2131bef90c78744b65535b9fd1835537b5c0cb986be2605958f3aaeb39e15",
    "section_id": "runtime_layout_context"
  },
  {
    "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
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
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+64",
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
    "check_id": "foreign_phone_code",
    "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
    "matched_text": "+64",
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
  "component_count": 11,
  "duration_ms": 91256,
  "failure_class": "none",
  "input_tokens": 0,
  "output_tokens": 0,
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
            "helpText": "Enter the attendee's given name",
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
            "helpText": "Enter the attendee's family name",
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
            "helpText": "We'll use this to send your RSVP confirmation",
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
            "helpText": "Prefer a New Zealand number (+64). +1 US formatting is accepted per request.",
            "label": "Phone",
            "placeholder": "[SCRUBBED_PHONE] or [SCRUBBED_PHONE]",
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
            "helpText": "Enter postal code (NZ format typically four digits).",
            "label": "ZIP / Postal code",
            "placeholder": "e.g. 6011",
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
            "helpText": "Select the New Zealand region where you are based",
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
                "label": "Bay of Plenty",
                "value": "bay_of_plenty"
              },
              {
                "label": "Waikato",
                "value": "waikato"
              },
              {
                "label": "Northland",
                "value": "northland"
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
                "label": "Manawatu-Whanganui",
                "value": "manawatu_whanganui"
              },
              {
                "label": "Gisborne",
                "value": "gisborne"
              },
              {
                "label": "Southland",
                "value": "southland"
              },
              {
                "label": "Nelson",
                "value": "nelson"
              },
              {
                "label": "Marlborough",
                "value": "marlborough"
              },
              {
                "label": "West Coast",
                "value": "west_coast"
              }
            ],
            "placeholder": "Select a region",
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
            "helpText": "Select any dietary needs. Use 'Other' and provide details below if needed.",
            "label": "Dietary requirements (select all that apply)",
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
                "label": "Gluten\u2011free",
                "value": "gluten_free"
              },
              {
                "label": "Dairy\u2011free",
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
            "y": 570
          },
          "props": {
            "height": 200,
            "helpText": "Provide details for any options you selected as 'Other', or add specifics (e.g. ingredient-level allergies).",
            "label": "Other dietary details",
            "placeholder": "Please describe any other dietary needs or allergies",
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
          "id": "textarea-9",
          "position": {
            "x": 40,
            "y": 874
          },
          "props": {
            "height": 200,
            "helpText": "Let us know about access, mobility, hearing, visual or other support needs so we can assist.",
            "label": "Accessibility needs",
            "placeholder": "Please describe any accessibility requirements or supports you need",
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
            "y": 1178
          },
          "props": {
            "height": 120,
            "helpText": "By checking this box you consent to receive event updates and communications.",
            "label": "I agree to receive event updates",
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
            "y": 1322
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
      "title": "New Zealand RSVP"
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
