# Form AI Judge Input Batch

Run ID: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 46520,
  "failure_class": "none",
  "input_tokens": 2882,
  "output_tokens": 2714,
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
  "formId": "sales-conf-registration",
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
            "helpText": "As you want it to appear on your badge",
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
            "helpText": "We'll send your registration confirmation to this address",
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
            "helpText": "Optional country code for international attendees",
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
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Select any dietary needs so catering can accommodate you",
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
            "placeholder": "Select an option",
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
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "We will provide a complimentary conference t-shirt in this size",
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
          "id": "submit-button-7",
          "position": {
            "x": 40,
            "y": 560
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 9,
  "duration_ms": 68403,
  "failure_class": "none",
  "input_tokens": 2954,
  "output_tokens": 3535,
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
            "helpText": "Conference will take place in Sydney. We'll send venue details after registration.",
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
            "helpText": "We'll use this to send your registration confirmation.",
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
            "helpText": "Include country code so we can contact you if needed.",
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
            "helpText": "Select your preferred T-shirt size for the event.",
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
            "y": 498
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about any dietary needs or allergies so we can accommodate you.",
            "label": "Dietary requirements",
            "placeholder": "e.g., vegetarian, gluten-free, allergies",
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
            "helpText": "Please review and accept the event terms to complete your registration.",
            "label": "Event terms and conditions",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
    "prompt_id": "p01-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
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
  "duration_ms": 71962,
  "failure_class": "none",
  "input_tokens": 2964,
  "output_tokens": 3271,
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
            "placeholder": "Surname / Family name",
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
            "helpText": "Include country code. This event uses +1 as the required country code.",
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
            "helpText": "Enter ZIP code (US ZIP format).",
            "label": "ZIP code",
            "placeholder": "e.g. 94107",
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
            "helpText": "Select the T-shirt size we should provide for you.",
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
            "helpText": "Tell us about any food restrictions or allergies so we can accommodate you.",
            "label": "Dietary requirements",
            "placeholder": "Specify any dietary needs or allergies (e.g. vegetarian, gluten-free, nut allergy)...",
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
            "y": 730
          },
          "props": {
            "height": 120,
            "helpText": "I agree to the event terms.",
            "label": "Agreement",
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
            "y": 874
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 38798,
  "failure_class": "none",
  "input_tokens": 2879,
  "output_tokens": 2461,
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
  "formId": "conference-rsvp-form",
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
            "label": "Please provide your details, choose sessions you'd like to attend, let us know any dietary requirements, and confirm if you'd like to receive event updates.",
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
            "helpText": "We'll send your confirmation and any updates to this address.",
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
            "helpText": "Optional \u2014 used only for urgent event communications.",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose the primary session you'd like to attend. We'll try to accommodate preferences.",
            "label": "Preferred session",
            "options": [
              {
                "label": "Opening Keynote: Future of Tech",
                "value": "session-keynote"
              },
              {
                "label": "Workshop A: AI in Practice",
                "value": "session-workshop-a"
              },
              {
                "label": "Workshop B: Product Design",
                "value": "session-workshop-b"
              },
              {
                "label": "Panel: Industry Trends",
                "value": "session-panel"
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
            "helpText": "Select any applicable dietary needs so we can cater appropriately.",
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
            "helpText": "Provide details if you selected 'Other' above or have specific allergies.",
            "label": "Other dietary requirements (if not listed)",
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
          "id": "terms-9",
          "position": {
            "x": 40,
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "By consenting you agree to receive email or SMS updates about the event.",
            "label": "I consent to receive event updates and occasional marketing communications about this conference. I understand I can unsubscribe at any time.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 12,
  "duration_ms": 29176,
  "failure_class": "none",
  "input_tokens": 2951,
  "output_tokens": 4045,
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
            "label": "We're pleased to invite you to our Sydney conference. Fill in the form below to secure your place.",
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
            "helpText": "As you'd like it to appear on your badge.",
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
            "helpText": "As you'd like it to appear on your badge.",
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
            "helpText": "We will send your confirmation and event information here.",
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
            "helpText": "Optional \u2014 we'll only call if we need to reach you urgently.",
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
            "helpText": "Optional \u2014 for your conference badge.",
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
          "id": "number-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Include any additional guests (if permitted).",
            "label": "Number of guests",
            "placeholder": "0",
            "tabOrder": 7,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "number"
        },
        {
          "id": "dropdown-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Select the primary session or workshop you'll attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Opening Keynote",
                "value": "opening-keynote"
              },
              {
                "label": "Workshop A: Design Thinking",
                "value": "workshop-a-design-thinking"
              },
              {
                "label": "Workshop B: Data & AI",
                "value": "workshop-b-data-ai"
              },
              {
                "label": "Panel: Industry Trends",
                "value": "panel-industry-trends"
              },
              {
                "label": "Networking Lunch",
                "value": "networking-lunch"
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
            "y": 632
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
            "y": 776
          },
          "props": {
            "height": 200,
            "helpText": "If you selected 'Other' above, provide details here.",
            "label": "Other dietary needs (please specify)",
            "placeholder": "E.g. severe nut allergy, specific ingredients to avoid...",
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
            "helpText": "By consenting you agree to receive email updates about this event. View the event terms for full details.",
            "label": "I agree to receive event updates and accept the event terms",
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
            "helpText": "Submit your RSVP",
            "label": "RSVP",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 66123,
  "failure_class": "none",
  "input_tokens": 2961,
  "output_tokens": 4210,
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
  "formId": "conference-rsvp-form",
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
            "helpText": "We'll send your confirmation and event updates here.",
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
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Provide a phone number including the +1 country code.",
            "label": "Phone (include +1)",
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
            "x": 384,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Enter your ZIP/postal code (ZIP format requested).",
            "label": "ZIP code",
            "placeholder": "e.g. 94103",
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
            "helpText": "Choose the session or track you plan to attend.",
            "label": "Session choice",
            "options": [
              {
                "label": "Full conference (all sessions)",
                "value": "full_conference"
              },
              {
                "label": "Track A \u2014 Artificial Intelligence",
                "value": "track_ai"
              },
              {
                "label": "Track B \u2014 Cloud & Infrastructure",
                "value": "track_cloud"
              },
              {
                "label": "Workshop \u2014 Data Engineering (limited seats)",
                "value": "workshop_data"
              },
              {
                "label": "Keynote only",
                "value": "keynote_only"
              }
            ],
            "placeholder": "Select your preferred session",
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
            "helpText": "Select all that apply.",
            "label": "Dietary requirements",
            "options": [
              {
                "label": "No preference",
                "value": "no_pref"
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
            "label": "Dietary details / allergies",
            "placeholder": "Please specify any allergies or special dietary needs",
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
            "helpText": "By checking this box you consent to receive event updates and agree to the event terms.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 42451,
  "failure_class": "none",
  "input_tokens": 2877,
  "output_tokens": 2711,
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
    "height": 1404,
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
            "label": "Choose your preferred stream and tell us about any accessibility needs so we can support you.",
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
            "helpText": "We'll send your registration confirmation here.",
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
            "helpText": "Optional \u2014 useful if we need to contact you about your booking.",
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
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Select the option that best matches your current experience.",
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
            "y": 364
          },
          "props": {
            "height": 110,
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
                "label": "Product",
                "value": "product"
              },
              {
                "label": "Data & Machine Learning",
                "value": "data_ml"
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
            "y": 508
          },
          "props": {
            "height": 120,
            "helpText": "Choose any common supports you require. If you select Other, please describe below.",
            "label": "Accessibility needs (select any that apply)",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair_access"
              },
              {
                "label": "Sign language interpreter",
                "value": "sign_language"
              },
              {
                "label": "Captioning / live transcription",
                "value": "captioning"
              },
              {
                "label": "Large print / high-contrast materials",
                "value": "large_print"
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
            "y": 652
          },
          "props": {
            "height": 200,
            "helpText": "Provide any details that will help us make appropriate arrangements.",
            "label": "Accessibility details",
            "placeholder": "Please describe any accessibility requirements or elaborate on selections above",
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
            "label": "Additional information (optional)",
            "placeholder": "Share any dietary requirements, scheduling notes, or other preferences",
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
            "y": 1260
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

## Row 8: `p03-au-ambiguous-r1__r01`

- Prompt ID: `p03-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 71707,
  "failure_class": "none",
  "input_tokens": 2949,
  "output_tokens": 4503,
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
            "helpText": "We'll use this to send your registration confirmation.",
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
            "helpText": "Optional \u2014 helpful if we need to contact you on the day.",
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
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Tell us your current experience level for the workshop activities.",
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
            "helpText": "Select the stream you would like to attend.",
            "label": "Preferred workshop stream",
            "options": [
              {
                "label": "Design Thinking",
                "value": "design_thinking"
              },
              {
                "label": "Technical Skills",
                "value": "technical_skills"
              },
              {
                "label": "Leadership & Facilitation",
                "value": "leadership_facilitation"
              },
              {
                "label": "Career Development",
                "value": "career_development"
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
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 120,
            "helpText": "Select any accessibility supports you'd like us to provide.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair_access"
              },
              {
                "label": "Hearing assistance / AUSLAN",
                "value": "hearing_assistance"
              },
              {
                "label": "Visual assistance / large print",
                "value": "visual_assistance"
              },
              {
                "label": "Quiet / low-sensory space",
                "value": "quiet_space"
              },
              {
                "label": "Dietary requirements",
                "value": "dietary_requirements"
              },
              {
                "label": "Other \u2014 I'll specify below",
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
            "helpText": "We will treat this information confidentially and contact you if we need more details.",
            "label": "Accessibility details or other requirements",
            "placeholder": "Provide details about your accessibility needs (e.g., dietary, mobility, communication support).",
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
            "y": 874
          },
          "props": {
            "height": 48,
            "helpText": "This workshop session is associated with Sydney and will be run locally.",
            "label": "Event location: Sydney",
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
            "y": 946
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event terms to complete registration.",
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
      "title": "Sydney Workshop \u2014 Signup"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 11,
  "duration_ms": 29756,
  "failure_class": "none",
  "input_tokens": 2959,
  "output_tokens": 3544,
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
  "formId": "workshop-signup",
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
            "helpText": "As you would like it to appear on name tags",
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
            "helpText": "We\u2019ll use this to send your registration details",
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
            "helpText": "Include country code. Example: [SCRUBBED_PHONE]",
            "label": "Phone (include country code, e.g. +1)",
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
            "helpText": "ZIP/postal code for your billing or location",
            "label": "ZIP code",
            "placeholder": "ZIP code",
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
            "helpText": "Choose the option that best describes your current proficiency",
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
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Pick the stream you prefer to attend",
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
                "label": "Data & AI",
                "value": "data_ai"
              },
              {
                "label": "Leadership",
                "value": "leadership"
              },
              {
                "label": "Other",
                "value": "other"
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
            "y": 560
          },
          "props": {
            "height": 120,
            "helpText": "Tell us which accessibility services you require",
            "label": "Accessibility needs (select all that apply)",
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
                "label": "Live captioning",
                "value": "live_captioning"
              },
              {
                "label": "Large print materials",
                "value": "large_print"
              },
              {
                "label": "Dietary support at in-person venue",
                "value": "dietary_support"
              },
              {
                "label": "Other (describe below)",
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
            "helpText": "If you selected Other above, please provide details here",
            "label": "Accessibility details (please describe any specific needs)",
            "placeholder": "Describe any specific accessibility needs or accommodations",
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
            "helpText": "You must agree to the event terms to complete registration",
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
            "y": 1152
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

## Row 10: `p04-au-neutral-r1__r01`

- Prompt ID: `p04-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 31700,
  "failure_class": "none",
  "input_tokens": 2882,
  "output_tokens": 3172,
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
          "id": "paragraph-1",
          "position": {
            "x": 40,
            "y": 24
          },
          "props": {
            "height": 48,
            "label": "Please provide your contact details and any questions for the speaker. We may contact you about event updates.",
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
            "helpText": "Use the email address where you'd like to receive webinar access details.",
            "label": "Work email",
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
            "helpText": "Optional \u2014 for urgent event updates.",
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
            "label": "Organization",
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
            "helpText": "Optional",
            "label": "Job title / Role",
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
            "helpText": "So we can share the webinar time in your local zone.",
            "label": "Timezone",
            "options": [
              {
                "label": "UTC\u221208:00 (Pacific Time - US/Canada)",
                "value": "UTC-08:00"
              },
              {
                "label": "UTC\u221205:00 (Eastern Time - US/Canada)",
                "value": "UTC-05:00"
              },
              {
                "label": "UTC+00:00 (GMT)",
                "value": "UTC+00:00"
              },
              {
                "label": "UTC+01:00 (Central European Time)",
                "value": "UTC+01:00"
              },
              {
                "label": "UTC+08:00 (Beijing / Singapore)",
                "value": "UTC+08:00"
              },
              {
                "label": "UTC+10:00 (AEST - Australia)",
                "value": "UTC+10:00"
              },
              {
                "label": "Other (please specify in questions)",
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
            "y": 632
          },
          "props": {
            "height": 200,
            "helpText": "We may prioritise common themes\u2014tell us any specific questions or topics you'd like addressed.",
            "label": "Questions for the speaker",
            "placeholder": "What would you like the speaker to cover? (Optional)",
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
            "helpText": "Select if you would like to receive emails about future events and offers.",
            "label": "Marketing opt-in",
            "options": [
              {
                "label": "Yes \u2014 I want to receive emails about future events and offers",
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
      "title": "Webinar Registration Form"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 12,
  "duration_ms": 75669,
  "failure_class": "none",
  "input_tokens": 2954,
  "output_tokens": 4511,
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
  "formId": "webinar-reg-sydney",
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
            "label": "Please provide your details to register. We'll send joining information and reminders to your email address.",
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
            "helpText": "We'll email the webinar link and reminders to this address.",
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
            "helpText": "Optional \u2014 used only for urgent updates or SMS reminders.",
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
            "helpText": "Sydney time (Australia/Sydney) is recommended for event scheduling.",
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
                "label": "America/New_York (US Eastern)",
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
                "label": "Other",
                "value": "Other"
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
            "helpText": "We'll pass selected questions to the presenter. We may not be able to cover every submission.",
            "label": "Questions for the speaker",
            "placeholder": "What would you like the speaker to cover or address?",
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
            "helpText": "Receive event-related updates and occasional marketing. You can unsubscribe at any time.",
            "label": "Marketing opt-in",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and marketing emails",
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
            "helpText": "View the event terms for details.",
            "label": "I agree to the event terms",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 11,
  "duration_ms": 47730,
  "failure_class": "none",
  "input_tokens": 2964,
  "output_tokens": 4757,
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
            "helpText": "We'll email your webinar access details to this address.",
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
            "helpText": "Include country code; +1 prefix preferred for this registration.",
            "label": "Phone (country code +1)",
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
            "label": "Organisation",
            "placeholder": "Your organisation or company",
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
            "placeholder": "e.g., Product Manager",
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
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Postal ZIP code.",
            "label": "ZIP code",
            "placeholder": "e.g., 94103",
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
            "x": 424,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "We use this to schedule follow-ups in your local time.",
            "label": "Timezone",
            "options": [
              {
                "label": "America/New_York (UTC-05:00)",
                "value": "America/New_York"
              },
              {
                "label": "America/Los_Angeles (UTC-08:00)",
                "value": "America/Los_Angeles"
              },
              {
                "label": "Europe/London (UTC+00:00)",
                "value": "Europe/London"
              },
              {
                "label": "Europe/Berlin (UTC+01:00)",
                "value": "Europe/Berlin"
              },
              {
                "label": "Asia/Tokyo (UTC+09:00)",
                "value": "Asia/Tokyo"
              },
              {
                "label": "Asia/Singapore (UTC+08:00)",
                "value": "Asia/Singapore"
              },
              {
                "label": "Australia/Sydney (UTC+10:00)",
                "value": "Australia/Sydney"
              },
              {
                "label": "UTC (Coordinated Universal Time)",
                "value": "UTC"
              },
              {
                "label": "Other / not listed",
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
            "y": 560
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 we'll try to cover submitted questions during Q&A.",
            "label": "Questions for the speaker",
            "placeholder": "Type any questions you'd like the speaker to address during the webinar",
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
            "helpText": "You can unsubscribe at any time.",
            "label": "I agree to receive marketing communications about this event",
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

## Row 13: `p05-au-neutral-r1__r01`

- Prompt ID: `p05-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 45765,
  "failure_class": "none",
  "input_tokens": 2883,
  "output_tokens": 3930,
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
  "formId": "wedding-rsvp",
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
            "helpText": "Fill out one RSVP per household. If you have any questions, contact the hosts.",
            "label": "RSVP details",
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
            "helpText": "Your preferred name for place cards",
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
            "helpText": "Surname",
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
            "helpText": "We will send RSVP confirmation to this address",
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
            "helpText": "Mobile number in case we need to reach you",
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
          "id": "radio-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Please let us know whether you can join the celebration",
            "label": "Will you attend?",
            "options": [
              {
                "label": "Accepts with pleasure",
                "value": "attending"
              },
              {
                "label": "Declines with regret",
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
            "helpText": "Indicate if you plan to bring a guest",
            "label": "Plus-one",
            "options": [
              {
                "label": "I will be bringing a plus-one",
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
            "y": 652
          },
          "props": {
            "height": 110,
            "helpText": "Leave blank if not bringing a guest",
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
          "id": "dropdown-9",
          "position": {
            "x": 424,
            "y": 652
          },
          "props": {
            "height": 110,
            "helpText": "If bringing a guest, please select their meal",
            "label": "Plus-one meal choice",
            "options": [
              {
                "label": "Beef (main)",
                "value": "beef"
              },
              {
                "label": "Chicken (main)",
                "value": "chicken"
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
                "label": "Child's meal",
                "value": "child"
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
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "If you are attending, please select your meal preference",
            "label": "Meal choice",
            "options": [
              {
                "label": "Beef (main)",
                "value": "beef"
              },
              {
                "label": "Chicken (main)",
                "value": "chicken"
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
                "label": "Child's meal",
                "value": "child"
              }
            ],
            "placeholder": "Select your main",
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
          "id": "text-11",
          "position": {
            "x": 424,
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "Suggest a song you'd like to hear at the reception",
            "label": "Song request",
            "placeholder": "Song title \u2013 Artist",
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
          "id": "textarea-12",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "Include details for all attending in your party",
            "label": "Dietary requirements",
            "placeholder": "Please list any allergies or dietary needs",
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
            "y": 1224
          },
          "props": {
            "height": 200,
            "helpText": "We love reading your messages!",
            "label": "Message for the couple",
            "placeholder": "Optional message, well wishes, or notes",
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
          "id": "submit-button-14",
          "position": {
            "x": 40,
            "y": 1528
          },
          "props": {
            "height": 72,
            "helpText": "Click to send your RSVP",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 41358,
  "failure_class": "none",
  "input_tokens": 2955,
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
    "height": 1806,
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
            "label": "We're delighted to invite you to our wedding in Sydney. Complete the RSVP below to confirm attendance and meal preferences.",
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
            "width": 428
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
            "helpText": "We'll send RSVP confirmation to this address.",
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
            "helpText": "Optional, for urgent day-of updates.",
            "label": "Phone number",
            "placeholder": "+61 4XX XXX XXX",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 428
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
            "helpText": "Please let us know whether you will be joining the celebration in Sydney.",
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes \u2014 I / we will attend",
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
          "id": "checkbox-7",
          "position": {
            "x": 424,
            "y": 364
          },
          "props": {
            "height": 120,
            "helpText": "Tick if you will be bringing an additional guest.",
            "label": "Bringing a plus-one?",
            "options": [
              {
                "label": "I will be bringing a plus-one",
                "value": "plus_one"
              }
            ],
            "tabOrder": 7,
            "width": "428px"
          },
          "style": {
            "height": 120,
            "width": 428
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
            "helpText": "Only provide this if you're bringing a plus-one.",
            "label": "Plus-one full name",
            "placeholder": "Full name of your guest (if applicable)",
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
            "helpText": "Choose your main course. If not attending, select 'N/A (not attending)'.",
            "label": "Meal choice",
            "options": [
              {
                "label": "N/A (not attending)",
                "value": "na"
              },
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
                "label": "Kids' meal",
                "value": "kids"
              }
            ],
            "placeholder": "Select a meal",
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
            "helpText": "Tell us about any allergies or special dietary needs.",
            "label": "Dietary requirements",
            "placeholder": "e.g., gluten-free, nut allergy, halal",
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
            "y": 1080
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 we'll try to play a few requests on the night.",
            "label": "Song request",
            "placeholder": "A song you'd like to hear",
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
            "y": 1214
          },
          "props": {
            "height": 200,
            "helpText": "Optional message that may be shared with the couple.",
            "label": "Message to the couple",
            "placeholder": "Write a brief message or congratulations",
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
            "y": 1518
          },
          "props": {
            "height": 120,
            "helpText": "By submitting you agree to the event terms and allow us to contact you about this RSVP.",
            "label": "Agreement",
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
            "y": 1662
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 15,
  "duration_ms": 54438,
  "failure_class": "none",
  "input_tokens": 2965,
  "output_tokens": 4004,
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
  "formId": "wedding-rsvp",
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
            "label": "We\u2019re excited to celebrate with you. Please RSVP by selecting your attendance and providing guest details below.",
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
            "helpText": "We'll send RSVP confirmations to this address.",
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
            "helpText": "Optional \u2014 provide a number we can reach you on.",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Please provide your ZIP Code.",
            "label": "ZIP Code",
            "placeholder": "Postcode or ZIP",
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
            "label": "Will you attend?",
            "options": [
              {
                "label": "Yes, I/We will attend",
                "value": "yes"
              },
              {
                "label": "No, we\u2019re unable to attend",
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
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "If you select this, please provide your guest's details below.",
            "label": "Will you be bringing a plus-one?",
            "options": [
              {
                "label": "Yes, I'll bring a guest",
                "value": "bringing_plus_one"
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
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "Shown if you are bringing a guest.",
            "label": "Plus-one name",
            "placeholder": "Full name of guest",
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
            "x": 424,
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "Label intentionally uses '+1' wording.",
            "label": "+1 Phone",
            "placeholder": "Guest phone number",
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
          "id": "dropdown-11",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 110,
            "helpText": "Choose your meal if you are attending.",
            "label": "Meal choice",
            "options": [
              {
                "label": "Beef (roast)",
                "value": "beef"
              },
              {
                "label": "Fish (grilled)",
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
                "label": "Other / Child's meal",
                "value": "other"
              }
            ],
            "placeholder": "Select your meal",
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
            "y": 1054
          },
          "props": {
            "height": 200,
            "helpText": "Please be specific so we can accommodate you.",
            "label": "Dietary requirements",
            "placeholder": "Allergies, intolerances, or other dietary needs",
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
            "y": 1358
          },
          "props": {
            "height": 110,
            "helpText": "Request one song for the dance floor.",
            "label": "Song request",
            "placeholder": "A song you'd love to hear",
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
            "helpText": "Optional message you'd like to share.",
            "label": "Message to the couple",
            "placeholder": "Write a note or well wishes",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 44745,
  "failure_class": "none",
  "input_tokens": 2879,
  "output_tokens": 3624,
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
            "label": "All fields marked required must be completed before we can process your application.",
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
            "helpText": "Street address, city, state/province, postal code",
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
                "label": "Weekdays \u2014 Morning",
                "value": "weekdays_morning"
              },
              {
                "label": "Weekdays \u2014 Afternoon",
                "value": "weekdays_afternoon"
              },
              {
                "label": "Weekdays \u2014 Evening",
                "value": "weekdays_evening"
              },
              {
                "label": "Weekends \u2014 Morning",
                "value": "weekends_morning"
              },
              {
                "label": "Weekends \u2014 Afternoon",
                "value": "weekends_afternoon"
              },
              {
                "label": "Weekends \u2014 Evening",
                "value": "weekends_evening"
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
            "label": "Availability details (optional)",
            "placeholder": "e.g., available after 5pm on weekdays, or specific dates you can commit to",
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
            "helpText": "Select all skills that apply",
            "label": "Skills & interests",
            "options": [
              {
                "label": "Event setup",
                "value": "event_setup"
              },
              {
                "label": "Registration / check-in",
                "value": "registration"
              },
              {
                "label": "First aid",
                "value": "first_aid"
              },
              {
                "label": "Childcare",
                "value": "childcare"
              },
              {
                "label": "Food service",
                "value": "food_service"
              },
              {
                "label": "Driving / logistics",
                "value": "driving"
              },
              {
                "label": "Translation / interpretation",
                "value": "translation"
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
            "y": 1090
          },
          "props": {
            "height": 200,
            "label": "Other skills or certifications (optional)",
            "placeholder": "List any certificates, licences, or specialised skills (e.g., RSA, First Aid certificate)",
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
            "y": 1394
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
          "id": "text-12",
          "position": {
            "x": 424,
            "y": 1394
          },
          "props": {
            "height": 110,
            "label": "Relationship",
            "placeholder": "e.g., Partner, Parent, Friend",
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
          "id": "phone-13",
          "position": {
            "x": 40,
            "y": 1528
          },
          "props": {
            "height": 110,
            "label": "Emergency contact phone",
            "placeholder": "[SCRUBBED_PHONE]",
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
            "y": 1662
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the volunteer code of conduct to participate.",
            "label": "I agree to the volunteer code of conduct",
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
            "label": "Sign Up",
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

## Row 17: `p06-au-ambiguous-r1__r01`

- Prompt ID: `p06-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 23,
  "duration_ms": 60000,
  "failure_class": "none",
  "input_tokens": 2951,
  "output_tokens": 4817,
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
    "height": 2466,
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
            "label": "Thanks for offering your time. Please complete your contact details, availability, skills, and emergency contact information. All volunteers must acknowledge the code of conduct.",
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
            "helpText": "We\u2019ll use this to confirm your sign-up and send event updates.",
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
            "helpText": "Mobile preferred for urgent event updates.",
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
            "helpText": "Providing an address helps with local assignments but is optional.",
            "label": "Address (optional)",
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
          "id": "paragraph-8",
          "position": {
            "x": 40,
            "y": 542
          },
          "props": {
            "height": 48,
            "helpText": "Let us know when you can help during the event.",
            "label": "Availability",
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
          "id": "date-9",
          "position": {
            "x": 40,
            "y": 614
          },
          "props": {
            "height": 110,
            "label": "Available from",
            "placeholder": "Start date",
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
          "id": "date-10",
          "position": {
            "x": 424,
            "y": 614
          },
          "props": {
            "height": 110,
            "label": "Available to",
            "placeholder": "End date",
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
            "y": 748
          },
          "props": {
            "height": 110,
            "helpText": "Choose your preferred shift (if any).",
            "label": "Preferred shift",
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
                "label": "Any / flexible",
                "value": "any"
              }
            ],
            "placeholder": "Select a shift",
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
            "y": 882
          },
          "props": {
            "height": 120,
            "helpText": "Select all days you are available during the event period.",
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
          "id": "divider-13",
          "position": {
            "x": 40,
            "y": 1026
          },
          "props": {
            "height": 20,
            "tabOrder": 13,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "checkbox-14",
          "position": {
            "x": 40,
            "y": 1070
          },
          "props": {
            "height": 120,
            "helpText": "Select all that apply.",
            "label": "Skills / certifications",
            "options": [
              {
                "label": "First aid / CPR (certified)",
                "value": "first_aid"
              },
              {
                "label": "Crowd management / stewarding",
                "value": "crowd_management"
              },
              {
                "label": "Hospitality / food & beverage",
                "value": "hospitality"
              },
              {
                "label": "Child/young person supervision",
                "value": "child_supervision"
              },
              {
                "label": "Admin / office support",
                "value": "admin"
              },
              {
                "label": "Logistics / transport",
                "value": "logistics"
              },
              {
                "label": "Technical / AV",
                "value": "technical"
              },
              {
                "label": "Other (please describe below)",
                "value": "other"
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
          "id": "textarea-15",
          "position": {
            "x": 40,
            "y": 1214
          },
          "props": {
            "height": 200,
            "helpText": "Provide details for any skills or certifications selected above.",
            "label": "Relevant experience or certifications (details)",
            "placeholder": "e.g., First Aid cert number, years of experience, licences",
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
          "id": "textarea-16",
          "position": {
            "x": 40,
            "y": 1518
          },
          "props": {
            "height": 200,
            "label": "Medical conditions or accessibility needs (optional)",
            "placeholder": "Let us know any conditions or needs so we can accommodate you",
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
          "id": "divider-17",
          "position": {
            "x": 40,
            "y": 1822
          },
          "props": {
            "height": 20,
            "tabOrder": 17,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "text-18",
          "position": {
            "x": 40,
            "y": 1866
          },
          "props": {
            "height": 110,
            "label": "Contact name",
            "placeholder": "Full name",
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
          "id": "phone-19",
          "position": {
            "x": 424,
            "y": 1866
          },
          "props": {
            "height": 110,
            "helpText": "A number we can call in an emergency.",
            "label": "Contact phone",
            "placeholder": "+61 4XX XXX XXX",
            "tabOrder": 19,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "phone"
        },
        {
          "id": "text-20",
          "position": {
            "x": 40,
            "y": 2000
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "placeholder": "e.g., Partner, Parent, Friend",
            "tabOrder": 20,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "text"
        },
        {
          "id": "divider-21",
          "position": {
            "x": 40,
            "y": 2134
          },
          "props": {
            "height": 20,
            "tabOrder": 21,
            "width": "880px"
          },
          "style": {
            "height": 20,
            "width": 880
          },
          "type": "divider"
        },
        {
          "id": "terms-22",
          "position": {
            "x": 40,
            "y": 2178
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event code of conduct and release to volunteer.",
            "label": "Code of conduct & release",
            "tabOrder": 22,
            "width": "880px"
          },
          "style": {
            "height": 120,
            "width": 880
          },
          "type": "terms"
        },
        {
          "id": "submit-button-23",
          "position": {
            "x": 40,
            "y": 2322
          },
          "props": {
            "height": 72,
            "label": "Sign up to volunteer",
            "tabOrder": 23,
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
      "title": "Sydney Volunteer Signup"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 56859,
  "failure_class": "none",
  "input_tokens": 2961,
  "output_tokens": 4443,
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
    "height": 2218,
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
            "helpText": "Fields marked required must be completed before submitting. Please include country code for phone numbers (e.g. +1).",
            "label": "How to use this form",
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
            "helpText": "Please include the +1 country code prefix if applicable.",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Street address",
            "placeholder": "Street address / unit",
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
          "id": "text-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "City",
            "placeholder": "City",
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
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "State / Province",
            "placeholder": "State or province",
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
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 110,
            "helpText": "We ask for ZIP code wording even if this is outside the US. Enter postal/ZIP code as applicable.",
            "label": "ZIP code",
            "placeholder": "ZIP code",
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
            "helpText": "Choose the days/times you are available to volunteer.",
            "label": "Availability (select all that apply)",
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
            "y": 910
          },
          "props": {
            "height": 200,
            "helpText": "Use this field to provide more detail about your availability.",
            "label": "Availability notes / preferred dates",
            "placeholder": "If you have specific dates or times, list them here",
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
            "y": 1214
          },
          "props": {
            "height": 120,
            "helpText": "Select any skills or roles you can help with.",
            "label": "Skills & roles",
            "options": [
              {
                "label": "Event setup / teardown",
                "value": "setup"
              },
              {
                "label": "Hospitality / front desk",
                "value": "hospitality"
              },
              {
                "label": "First aid / medical",
                "value": "first_aid"
              },
              {
                "label": "Audio/Visual / Tech",
                "value": "av_tech"
              },
              {
                "label": "Logistics / driving",
                "value": "logistics"
              },
              {
                "label": "Childcare / youth supervision",
                "value": "childcare"
              },
              {
                "label": "Interpreter / language support",
                "value": "interpreter"
              },
              {
                "label": "Other",
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
            "y": 1358
          },
          "props": {
            "height": 200,
            "label": "Other skills or certifications",
            "placeholder": "Describe any other skills, certifications, or relevant experience",
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
            "y": 1662
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
          "id": "text-15",
          "position": {
            "x": 424,
            "y": 1662
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "placeholder": "e.g. Parent, Partner, Friend",
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
          "id": "phone-16",
          "position": {
            "x": 40,
            "y": 1796
          },
          "props": {
            "height": 110,
            "helpText": "Include the +1 prefix if applicable.",
            "label": "Emergency contact phone (include country code, e.g. +1)",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 16,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "phone-17",
          "position": {
            "x": 424,
            "y": 1796
          },
          "props": {
            "height": 110,
            "label": "Emergency contact alternate phone (optional, include country code)",
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
          "id": "terms-18",
          "position": {
            "x": 40,
            "y": 1930
          },
          "props": {
            "height": 120,
            "helpText": "All volunteers must agree to the event code of conduct.",
            "label": "Code of conduct & conduct acknowledgment",
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
            "y": 2074
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 40941,
  "failure_class": "none",
  "input_tokens": 2879,
  "output_tokens": 3238,
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
            "helpText": "Provide the primary contact information for the applicant.",
            "label": "Applicant details",
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
            "helpText": "We will use this email for membership communications.",
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
            "helpText": "Street address, suburb/city, state/province, postal code, country.",
            "label": "Postal address",
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
          "id": "date-7",
          "position": {
            "x": 600,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide date of birth if required for eligibility (optional).",
            "label": "Date of birth",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select the membership tier you are applying for.",
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
            "helpText": "You must confirm all of the following to be eligible for membership.",
            "label": "Eligibility confirmations",
            "options": [
              {
                "label": "I am at least 18 years of age (or meet the minimum age requirement).",
                "value": "age_confirm"
              },
              {
                "label": "I meet the membership eligibility criteria described in the membership guidelines.",
                "value": "criteria_confirm"
              },
              {
                "label": "The information I have provided in this application is true and complete.",
                "value": "truth_confirm"
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
          "id": "dropdown-10",
          "position": {
            "x": 40,
            "y": 786
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
                "label": "Event or expo",
                "value": "event"
              },
              {
                "label": "Social media",
                "value": "social"
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
            "width": 536
          },
          "type": "dropdown"
        },
        {
          "id": "text-11",
          "position": {
            "x": 600,
            "y": 786
          },
          "props": {
            "height": 110,
            "label": "If other, please specify",
            "placeholder": "Describe where you heard about us",
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
            "y": 920
          },
          "props": {
            "height": 200,
            "helpText": "Use this space for notes, special requests, or relevant background.",
            "label": "Additional information",
            "placeholder": "Provide any additional details relevant to your application (optional).",
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
            "y": 1224
          },
          "props": {
            "height": 120,
            "helpText": "By checking this box you acknowledge and accept the terms and privacy practices that govern membership.",
            "label": "I have read and agree to the event terms and privacy policy.",
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
            "y": 1368
          },
          "props": {
            "height": 72,
            "label": "Submit application",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 17,
  "duration_ms": 55305,
  "failure_class": "none",
  "input_tokens": 2951,
  "output_tokens": 4337,
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
    "height": 1924,
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
            "label": "Please complete the form below to apply for membership. Required fields are marked and must be completed to submit your application.",
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
            "helpText": "We'll use this to contact you about your application.",
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
            "helpText": "Mobile or best contact number.",
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
          "id": "date-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Used to verify age-based eligibility.",
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
            "helpText": "Street address, suburb, state and postcode.",
            "label": "Residential address",
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
          "id": "number-9",
          "position": {
            "x": 417,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Enter number of dependent family members to be included.",
            "label": "Number of dependents (if applying for Family)",
            "placeholder": "0",
            "tabOrder": 9,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "number"
        },
        {
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "label": "I confirm I am at least 18 years old",
            "options": [
              {
                "label": "Yes, I confirm",
                "value": "confirm_age"
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
            "y": 776
          },
          "props": {
            "height": 120,
            "label": "I agree to abide by the membership rules and code of conduct",
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
          "id": "checkbox-12",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 120,
            "helpText": "Residency helps determine eligibility for Sydney-associated membership categories.",
            "label": "I confirm I am a resident of New South Wales (NSW)",
            "options": [
              {
                "label": "I confirm",
                "value": "confirm_residency"
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
          "id": "dropdown-13",
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
                "label": "Website",
                "value": "website"
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
          "id": "text-14",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 110,
            "helpText": "Only complete if you selected Other above.",
            "label": "If Other, please specify",
            "placeholder": "Please describe",
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
            "y": 1332
          },
          "props": {
            "height": 200,
            "helpText": "Optional information we should know about your application.",
            "label": "Additional information or comments",
            "placeholder": "Any extra details relevant to your application",
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
            "y": 1636
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event terms to complete this application. (View the event terms.)",
            "label": "Agreement to event terms",
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
            "y": 1780
          },
          "props": {
            "height": 72,
            "label": "Apply for Membership",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 78443,
  "failure_class": "none",
  "input_tokens": 2961,
  "output_tokens": 4562,
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
            "label": "We collect your contact and eligibility details to process your application. Fields marked required must be completed.",
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
            "placeholder": "Family name / Surname",
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
          "id": "address-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Street address, city and state/province (if applicable).",
            "label": "Mailing address",
            "tabOrder": 4,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Membership type",
            "options": [
              {
                "label": "Individual (Annual)",
                "value": "individual_annual"
              },
              {
                "label": "Student (Discounted)",
                "value": "student"
              },
              {
                "label": "Senior (Discounted)",
                "value": "senior"
              },
              {
                "label": "Lifetime",
                "value": "lifetime"
              }
            ],
            "placeholder": "Select membership type",
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
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Enter ZIP code (US format).",
            "label": "ZIP code",
            "placeholder": "e.g. 94105",
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
          "id": "phone-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Include country code; use +1 for US numbers.",
            "label": "Phone number",
            "placeholder": "[SCRUBBED_PHONE]",
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
          "id": "email-8",
          "position": {
            "x": 424,
            "y": 498
          },
          "props": {
            "height": 110,
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "email"
        },
        {
          "id": "checkbox-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "You must confirm you meet the minimum age requirement.",
            "label": "Eligibility confirmation \u2014 age",
            "options": [
              {
                "label": "I confirm I meet the minimum age requirement for membership",
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
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Confirm any status criteria required for this membership class.",
            "label": "Eligibility confirmation \u2014 status",
            "options": [
              {
                "label": "I confirm I meet the status/qualification requirements for the selected membership type",
                "value": "status_confirmed"
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
            "helpText": "You must certify the information provided is accurate.",
            "label": "Eligibility confirmation \u2014 accuracy",
            "options": [
              {
                "label": "I certify that the information in this application is true and complete",
                "value": "info_certified"
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
                "label": "Email or newsletter",
                "value": "email"
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
            "placeholder": "Select a referral source",
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
            "placeholder": "Please tell us where you heard about us",
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
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1198
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event terms to submit your application.",
            "label": "Terms & acknowledgement",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 54508,
  "failure_class": "none",
  "input_tokens": 2885,
  "output_tokens": 3778,
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
  "formId": "trade-show-lead-log",
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
            "helpText": "Complete this form during or immediately after each interaction.",
            "label": "Record visitor contact details, interests, and consent for follow-up after booth conversations.",
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
            "helpText": "Best address for follow-up.",
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
            "label": "Phone",
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
            "label": "Company",
            "placeholder": "Company name",
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
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediately (0\u20131 month)",
                "value": "0-1_month"
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
                "label": "12+ months",
                "value": "12+_months"
              },
              {
                "label": "Not currently planning to buy",
                "value": "not_planning"
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
          "id": "checkbox-8",
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
                "label": "Product demos",
                "value": "demos"
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
                "label": "Support & services",
                "value": "services"
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
            "helpText": "Include any useful context for follow-up (pain points, stakeholders, budget cues).",
            "label": "Notes",
            "placeholder": "Notes from conversation, specific interests, agreed next steps",
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
            "helpText": "Consent is voluntary. Do not proceed without the visitor's permission.",
            "label": "I consent to be contacted by phone or email for follow-up about products and services discussed.",
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
            "helpText": "Save this visitor's details to the lead log.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 51762,
  "failure_class": "none",
  "input_tokens": 2957,
  "output_tokens": 3762,
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
  "formId": "sydney-trade-show-booth-leads",
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
            "helpText": "Use this form at the booth to capture leads and next steps.",
            "label": "Event: Sydney",
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
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Include country code if outside Australia.",
            "label": "Phone",
            "placeholder": "Mobile or direct line",
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
          "id": "email-5",
          "position": {
            "x": 384,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Primary contact email",
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
            "y": 364
          },
          "props": {
            "height": 110,
            "label": "Company",
            "placeholder": "Company or organisation",
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
            "helpText": "Select one or more areas the visitor expressed interest in.",
            "label": "Interest areas",
            "options": [
              {
                "label": "Product demo / hands-on",
                "value": "demo"
              },
              {
                "label": "Pricing & packages",
                "value": "pricing"
              },
              {
                "label": "Partnerships / integrations",
                "value": "partnerships"
              },
              {
                "label": "Reseller / distribution",
                "value": "reseller"
              },
              {
                "label": "Other (note in comments)",
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
          "id": "radio-8",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "When is the visitor planning to purchase or decide?",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediate / within 1 month",
                "value": "immediate"
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
                "label": "Not planning / just exploring",
                "value": "not_planning"
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
            "y": 786
          },
          "props": {
            "height": 200,
            "helpText": "Include who will follow up and any promised materials.",
            "label": "Notes / next steps",
            "placeholder": "Capture key details from the conversation, products of interest, and agreed next steps.",
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
            "y": 1090
          },
          "props": {
            "height": 120,
            "helpText": "Visitor consents to be contacted about their enquiry and related offers.",
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
            "y": 1234
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
      "title": "Sydney Trade Show \u2014 Booth Visit Log"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
    "prompt_id": "p08-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP",
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
    "matched_text": "ZIP",
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
  "duration_ms": 47268,
  "failure_class": "none",
  "input_tokens": 2967,
  "output_tokens": 3807,
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
            "label": "Last name",
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
          "id": "text-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Visitor's employer or organization.",
            "label": "Company",
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
            "helpText": "Collect ZIP/postal code. US ZIP pattern applied.",
            "label": "ZIP code",
            "placeholder": "ZIP (e.g. 94107)",
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
            "helpText": "Primary email to contact this lead.",
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
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Include country code. Enter +1 for US numbers.",
            "label": "Phone number",
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
          "id": "dropdown-7",
          "position": {
            "x": 40,
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "What the visitor was most interested in at the booth.",
            "label": "Interest area",
            "options": [
              {
                "label": "Product demo",
                "value": "product_demo"
              },
              {
                "label": "Pricing / quotes",
                "value": "pricing"
              },
              {
                "label": "Partnerships",
                "value": "partnerships"
              },
              {
                "label": "Support / service",
                "value": "support"
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
            "placeholder": "Select interest",
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
            "helpText": "Estimated purchase or deployment timeframe, if known.",
            "label": "Buying timeframe",
            "options": [
              {
                "label": "Immediately / within 30 days",
                "value": "immediate"
              },
              {
                "label": "0\u20133 months",
                "value": "0_3_months"
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
                "label": "No plans / long term",
                "value": "not_planning"
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
            "helpText": "Add any qualifying information, objections, or agreed next steps.",
            "label": "Notes",
            "placeholder": "Notes from conversation, qualifying details, next steps",
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
            "helpText": "Visitor consents to be contacted for sales follow-up regarding products or services discussed.",
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
            "label": "Log visit",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 36676,
  "failure_class": "none",
  "input_tokens": 2877,
  "output_tokens": 2794,
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
            "placeholder": "Enter your first name",
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
            "helpText": "We'll use this email to send your subscription.",
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
            "helpText": "Choose the topics you want to receive.",
            "label": "Content interests",
            "options": [
              {
                "label": "News & announcements",
                "value": "news"
              },
              {
                "label": "Product updates",
                "value": "product_updates"
              },
              {
                "label": "Events & webinars",
                "value": "events"
              },
              {
                "label": "Blog posts & articles",
                "value": "blog"
              },
              {
                "label": "Promotions & offers",
                "value": "promotions"
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
            "helpText": "How often would you like to hear from us?",
            "label": "Email frequency",
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
                "label": "Occasional (only important updates)",
                "value": "occasional"
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
            "helpText": "You can unsubscribe at any time using the link in any email.",
            "label": "I consent to receive marketing emails and acknowledge the privacy practices.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 45705,
  "failure_class": "none",
  "input_tokens": 2949,
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
            "label": "This newsletter shares updates, programs and offers related to the Sydney event.",
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
            "placeholder": "e.g. Alex",
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
            "helpText": "Select all topics you're interested in.",
            "label": "Content interests",
            "options": [
              {
                "label": "Event updates",
                "value": "event_updates"
              },
              {
                "label": "Workshops & sessions",
                "value": "workshops"
              },
              {
                "label": "Special offers",
                "value": "offers"
              },
              {
                "label": "Volunteer opportunities",
                "value": "volunteer"
              },
              {
                "label": "Surveys & feedback",
                "value": "surveys"
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
            "helpText": "How often would you like to hear from us?",
            "label": "Newsletter frequency",
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
            "label": "I agree to receive marketing and promotional emails about the event.",
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
      "title": "Sydney Event Newsletter Signup"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 52173,
  "failure_class": "none",
  "input_tokens": 2959,
  "output_tokens": 4398,
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
  "formId": "newsletter-subscription-us-phone-zip",
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
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Please include country code. +1 format suggested.",
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
          "id": "text-5",
          "position": {
            "x": 384,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Postal / ZIP code",
            "label": "ZIP code",
            "placeholder": "e.g. 94103",
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
            "helpText": "Choose topics you'd like to receive.",
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
                "label": "Research & insights",
                "value": "insights"
              },
              {
                "label": "Promotions & offers",
                "value": "offers"
              },
              {
                "label": "Partner news",
                "value": "partners"
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
            "helpText": "How often would you like to hear from us?",
            "label": "Email frequency",
            "options": [
              {
                "label": "Immediate / As published",
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
          "id": "terms-8",
          "position": {
            "x": 40,
            "y": 714
          },
          "props": {
            "height": 120,
            "helpText": "I agree to receive marketing communications and acknowledge the event terms.",
            "label": "Marketing consent",
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
            "y": 858
          },
          "props": {
            "height": 72,
            "label": "Subscribe",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 49954,
  "failure_class": "none",
  "input_tokens": 2884,
  "output_tokens": 3831,
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
            "label": "We will use your pledge to support our programmes. You can choose a one-off gift or set up a recurring contribution. A receipt will be sent to the email you provide.",
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
            "helpText": "A tax receipt will be sent to this address.",
            "label": "Email (for receipt)",
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
            "helpText": "We may contact you about your pledge if we need to confirm details.",
            "label": "Phone (optional)",
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
            "helpText": "Select which campaign you'd like your pledge to support, or choose General fund.",
            "label": "Campaign (optional)",
            "options": [
              {
                "label": "General fund",
                "value": "general"
              },
              {
                "label": "Emergency relief",
                "value": "emergency_relief"
              },
              {
                "label": "Education programs",
                "value": "education"
              },
              {
                "label": "Health initiatives",
                "value": "health"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select a campaign",
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
            "helpText": "Choose a suggested amount or select Other to enter a custom value.",
            "label": "Donation amount",
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
                "label": "AUD 500",
                "value": "500"
              },
              {
                "label": "Other (enter custom amount)",
                "value": "other"
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
            "helpText": "Enter a custom donation amount if you selected Other above (numbers only).",
            "label": "Custom amount (AUD)",
            "placeholder": "Enter amount",
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
            "helpText": "Is this a one\u2011off pledge or would you like to give on a recurring basis?",
            "label": "Donation type",
            "options": [
              {
                "label": "One\u2011off",
                "value": "one_off"
              },
              {
                "label": "Recurring (ongoing)",
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
            "y": 642
          },
          "props": {
            "height": 110,
            "helpText": "Select how often you want the recurring pledge to be charged.",
            "label": "Recurring frequency",
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
              },
              {
                "label": "Annual",
                "value": "annual"
              }
            ],
            "placeholder": "If recurring, choose frequency",
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
            "y": 786
          },
          "props": {
            "height": 120,
            "helpText": "Choose how you'd like to receive your receipt.",
            "label": "Receipt preferences",
            "options": [
              {
                "label": "Email receipt (use email above)",
                "value": "email_receipt"
              },
              {
                "label": "Paper receipt (send by post)",
                "value": "paper_receipt"
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
          "id": "address-12",
          "position": {
            "x": 40,
            "y": 930
          },
          "props": {
            "height": 110,
            "helpText": "Provide a postal address if you selected a paper receipt.",
            "label": "Postal address (only if you requested a paper receipt)",
            "tabOrder": 12,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 600
          },
          "type": "address"
        },
        {
          "id": "checkbox-13",
          "position": {
            "x": 40,
            "y": 1064
          },
          "props": {
            "height": 120,
            "helpText": "I consent to receive updates about campaigns, impact stories and ways to support our work. Choose preferred channels.",
            "label": "Communications consent",
            "options": [
              {
                "label": "Email updates",
                "value": "consent_email"
              },
              {
                "label": "SMS / text updates",
                "value": "consent_sms"
              },
              {
                "label": "Phone calls",
                "value": "consent_phone"
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
            "y": 1208
          },
          "props": {
            "height": 200,
            "label": "Message or dedication (optional)",
            "placeholder": "Add a note if you'd like (e.g., in memory of...)",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 51801,
  "failure_class": "none",
  "input_tokens": 2956,
  "output_tokens": 4365,
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
            "label": "Your pledge helps fund local programs across Sydney. Provide your contact and donation details to receive a receipt and campaign updates.",
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
            "width": 503
          },
          "type": "first-name"
        },
        {
          "id": "text-3",
          "position": {
            "x": 567,
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
            "width": 353
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
            "helpText": "We'll send your receipt to this address unless you request postal delivery.",
            "label": "Email address",
            "placeholder": "[SCRUBBED_EMAIL]",
            "tabOrder": 4,
            "width": "360px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "email"
        },
        {
          "id": "phone-5",
          "position": {
            "x": 567,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 useful for urgent correspondence about your pledge.",
            "label": "Phone number",
            "placeholder": "+61 4xx xxx xxx",
            "tabOrder": 5,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
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
            "helpText": "Select a preset amount or choose Other to enter a custom amount.",
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
                "label": "$250",
                "value": "250"
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
            "width": 503
          },
          "type": "dropdown"
        },
        {
          "id": "number-7",
          "position": {
            "x": 567,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Only fill this if you selected Other above.",
            "label": "Custom amount (AUD)",
            "placeholder": "Enter amount in AUD",
            "tabOrder": 7,
            "width": "220px"
          },
          "style": {
            "height": 110,
            "width": 353
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
            "helpText": "Choose whether this is a one-off pledge or a recurring donation.",
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
            "tabOrder": 8,
            "width": "360px"
          },
          "style": {
            "height": 120,
            "width": 503
          },
          "type": "radio"
        },
        {
          "id": "dropdown-9",
          "position": {
            "x": 567,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "If you selected Recurring above, choose how often you'd like to be charged. Leave blank for one-off pledges.",
            "label": "Recurring frequency",
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
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 642
          },
          "props": {
            "height": 120,
            "helpText": "Select how you'd like to receive your donation receipt.",
            "label": "Receipt preferences",
            "options": [
              {
                "label": "Email receipt (default)",
                "value": "email_receipt"
              },
              {
                "label": "Postal receipt (send to address below)",
                "value": "postal_receipt"
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
          "id": "address-11",
          "position": {
            "x": 40,
            "y": 786
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 only required if you request a postal receipt.",
            "label": "Postal address (for mailed receipts)",
            "placeholder": "Street, suburb, state, postcode, country",
            "tabOrder": 11,
            "width": "600px"
          },
          "style": {
            "height": 110,
            "width": 503
          },
          "type": "address"
        },
        {
          "id": "text-12",
          "position": {
            "x": 567,
            "y": 786
          },
          "props": {
            "height": 110,
            "label": "Organisation / Company name (for receipt)",
            "placeholder": "Optional: organisation name for donation acknowledgment",
            "tabOrder": 12,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 353
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
            "helpText": "Maximum 500 characters.",
            "label": "Message or dedication (optional)",
            "placeholder": "Add a short message or dedicate this donation",
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
            "helpText": "I agree to receive occasional updates and news about this campaign. You can unsubscribe at any time.",
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
            "helpText": "By pledging, you agree to the event terms and privacy policy.",
            "label": "Agreement",
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
            "helpText": "Click to confirm your pledge. A receipt will be sent according to your preferences.",
            "label": "Pledge Donation",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p10-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
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
  "duration_ms": 47221,
  "failure_class": "none",
  "input_tokens": 2966,
  "output_tokens": 3788,
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
            "label": "Thank you for supporting our cause. Please provide your pledge details below and indicate how you'd like to be contacted for a receipt and updates.",
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
            "helpText": "An email receipt will be sent to this address.",
            "label": "Email address (for receipt)",
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
            "helpText": "Include country code (example shows +1). We'll only use this for urgent contact or SMS receipt if you opt in.",
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
            "helpText": "Provide your postal ZIP or postcode.",
            "label": "ZIP code",
            "placeholder": "ZIP / Postal code",
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
            "helpText": "Choose a preset amount or select Other to enter a custom pledge.",
            "label": "Donation amount (USD)",
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
            "helpText": "Enter a custom donation if you selected Other above.",
            "label": "Custom amount (USD)",
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
            "helpText": "Choose whether this pledge is one-off or recurring.",
            "label": "Donation frequency",
            "options": [
              {
                "label": "One-time",
                "value": "one_time"
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
          "id": "checkbox-10",
          "position": {
            "x": 40,
            "y": 776
          },
          "props": {
            "height": 120,
            "helpText": "Choose how you would like to receive your donation receipt.",
            "label": "Receipt preferences",
            "options": [
              {
                "label": "Email receipt",
                "value": "email"
              },
              {
                "label": "Mail my receipt",
                "value": "mail"
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
          "id": "address-11",
          "position": {
            "x": 40,
            "y": 920
          },
          "props": {
            "height": 110,
            "helpText": "Provide postal address if you requested a mailed receipt.",
            "label": "Mailing address (only if you selected 'Mail my receipt')",
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
            "y": 1054
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to receive campaign updates and fundraising appeals. You can opt out at any time.",
            "label": "Campaign updates consent",
            "options": [
              {
                "label": "Yes \u2014 send me campaign updates and fundraising appeals (email/SMS)",
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
            "helpText": "By pledging, you agree to the donation terms and our data handling policies.",
            "label": "Donation terms and acknowledgement",
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
            "label": "Pledge Donation",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 9,
  "duration_ms": 34317,
  "failure_class": "none",
  "input_tokens": 2880,
  "output_tokens": 2701,
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
  "formId": "event-registration-intl",
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
            "helpText": "We'll send a confirmation and event updates to this address.",
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
            "helpText": "Include country code for international SMS/phone updates.",
            "label": "Phone number",
            "placeholder": "+61 4XX XXX XXX",
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
            "helpText": "Country determines local pricing and timezone suggestions.",
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
                "label": "India",
                "value": "IN"
              },
              {
                "label": "Germany",
                "value": "DE"
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
            "helpText": "Choose the timezone you will join from.",
            "label": "Preferred timezone",
            "options": [
              {
                "label": "UTC\u221208:00 (Pacific Time)",
                "value": "UTC-08:00"
              },
              {
                "label": "UTC+00:00 (GMT)",
                "value": "UTC+00:00"
              },
              {
                "label": "UTC+05:30 (India Standard Time)",
                "value": "UTC+05:30"
              },
              {
                "label": "UTC+10:00 (AEST)",
                "value": "UTC+10:00"
              },
              {
                "label": "Other / Unsure",
                "value": "OTHER"
              }
            ],
            "placeholder": "Select your timezone",
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
            "helpText": "Select all sessions you'd like to attend.",
            "label": "Sessions you're interested in",
            "options": [
              {
                "label": "Keynote (All attendees)",
                "value": "keynote"
              },
              {
                "label": "Workshop A \u2014 Advanced Topics",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B \u2014 Hands-on Lab",
                "value": "workshop_b"
              },
              {
                "label": "Networking Session",
                "value": "networking"
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
            "label": "I agree to the event terms and privacy policy. I consent to receive event-related communications.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 67502,
  "failure_class": "none",
  "input_tokens": 2952,
  "output_tokens": 4379,
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
            "label": "Join our online event hosted in Sydney. Please register your details below. All event times will reference Australia/Sydney (AEST/AEDT).",
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
            "helpText": "Include country code for international numbers.",
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
            "helpText": "Where you are located (for regional scheduling and communications).",
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
                "label": "New Zealand",
                "value": "NZ"
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
            "helpText": "Event times will be shown in Australia/Sydney by default; choose your timezone for local conversions.",
            "label": "Preferred timezone for session times",
            "options": [
              {
                "label": "Australia/Sydney (AEST/AEDT, UTC+10/11)",
                "value": "Australia/Sydney"
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
                "label": "UTC-8 (PST)",
                "value": "US/Pacific"
              },
              {
                "label": "UTC-5 (EST)",
                "value": "US/Eastern"
              },
              {
                "label": "Asia/Kolkata (IST, UTC+5:30)",
                "value": "Asia/Kolkata"
              },
              {
                "label": "Asia/Tokyo (JST, UTC+9)",
                "value": "Asia/Tokyo"
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
            "helpText": "Select at least one session you'd like to attend.",
            "label": "Which sessions are you interested in? (select all that apply)",
            "options": [
              {
                "label": "Opening keynote",
                "value": "keynote"
              },
              {
                "label": "Panel: Future of X",
                "value": "panel_future"
              },
              {
                "label": "Workshop A: Practical Skills",
                "value": "workshop_a"
              },
              {
                "label": "Workshop B: Advanced Topics",
                "value": "workshop_b"
              },
              {
                "label": "Networking session",
                "value": "networking"
              },
              {
                "label": "Closing remarks",
                "value": "closing"
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
            "helpText": "Optional \u2014 we will do our best to accommodate reasonable requests.",
            "label": "Accessibility needs or other requirements",
            "placeholder": "Tell us about any accessibility needs, special requirements, or questions you have.",
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
            "helpText": "You must accept the event terms to complete registration.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 57457,
  "failure_class": "none",
  "input_tokens": 2962,
  "output_tokens": 3602,
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
            "label": "This form collects attendee details, contact information, session interests and consent for the event.",
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
            "helpText": "As shown on your ID or badge.",
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
            "helpText": "As shown on your ID or badge.",
            "label": "Last name",
            "placeholder": "Family name / Surname",
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
            "helpText": "Include country code (e.g. [SCRUBBED_PHONE]). Note: form requests +1 format per organiser instructions.",
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
          "id": "email-5",
          "position": {
            "x": 424,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We\u2019ll send registration confirmations to this address.",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Country of residence or billing address.",
            "label": "Country",
            "options": [
              {
                "label": "United States",
                "value": "US"
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
                "label": "Canada",
                "value": "CA"
              },
              {
                "label": "Germany",
                "value": "DE"
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
            "helpText": "Enter your postal code. Form explicitly requests ZIP code formatting where applicable.",
            "label": "ZIP / Postal code",
            "placeholder": "ZIP or postal code (e.g. 20001)",
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
            "helpText": "Choose the timezone where you will attend from.",
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
                "label": "UTC+00:00 GMT",
                "value": "UTC+00:00"
              },
              {
                "label": "UTC+01:00 Central Europe",
                "value": "UTC+01:00"
              },
              {
                "label": "UTC+10:00 Australia Eastern Time",
                "value": "UTC+10:00"
              },
              {
                "label": "Other",
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
            "helpText": "Select all sessions you plan to attend.",
            "label": "Sessions I'm interested in",
            "options": [
              {
                "label": "Keynote: Future of the Industry",
                "value": "session_keynote"
              },
              {
                "label": "Workshop: Hands-on Lab",
                "value": "session_workshop"
              },
              {
                "label": "Panel: Global Perspectives",
                "value": "session_panel"
              },
              {
                "label": "Networking: Peer Meetups",
                "value": "session_networking"
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
            "helpText": "I agree to the event terms and any data usage described there.",
            "label": "Consent & terms",
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
            "helpText": "Click to submit your registration.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 14,
  "duration_ms": 69466,
  "failure_class": "none",
  "input_tokens": 2882,
  "output_tokens": 3920,
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
            "label": "Data handling notice: We will process the personal data you provide to manage your registration, send event updates, and fulfill event logistics. Data is processed in accordance with applicable EU data protection law. If you have questions about how your data is used or wish to exercise your rights, contact the event organiser.",
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
            "placeholder": "Your given name",
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
            "placeholder": "Your family name",
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
            "helpText": "We will use this to send your ticket and event communications.",
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
            "helpText": "Optional \u2014 used for urgent event communications (SMS/call).",
            "label": "Phone number (optional)",
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
            "label": "Job title",
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
          "id": "address-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Optional \u2014 provided only if you require physical mailings.",
            "label": "Postal address (optional)",
            "placeholder": "Street, city, postcode, country",
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
            "helpText": "Select the ticket type you are registering for.",
            "label": "Ticket type",
            "options": [
              {
                "label": "General admission",
                "value": "general"
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
                "label": "Student (proof required)",
                "value": "student"
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
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 766
          },
          "props": {
            "height": 200,
            "helpText": "Optional \u2014 helps us make appropriate arrangements.",
            "label": "Accessibility or dietary requirements (optional)",
            "placeholder": "Tell us any special requirements or dietary needs",
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
            "helpText": "Choose which communications you'd like to receive.",
            "label": "Marketing preferences (optional)",
            "options": [
              {
                "label": "Email me about future events and related offers",
                "value": "marketing_email"
              },
              {
                "label": "Contact me by phone about related events",
                "value": "marketing_phone"
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
            "helpText": "This consent is required to complete registration.",
            "label": "GDPR consent and data processing acknowledgement: I consent to the organiser collecting and processing my personal data for the purposes of event administration, communications, and logistics. I understand I can withdraw this consent at any time by contacting the organiser. For full details, see the data handling notice above.",
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
          "id": "terms-13",
          "position": {
            "x": 40,
            "y": 1358
          },
          "props": {
            "height": 120,
            "helpText": "Please confirm you understand the lawful basis for processing.",
            "label": "Lawful-basis acknowledgement: I acknowledge that I have read the data handling notice and understand the lawful basis on which my personal data will be processed for this event (for example, consent for communications or legitimate interests for event administration).",
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
            "y": 1502
          },
          "props": {
            "height": 72,
            "label": "Register",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 83320,
  "failure_class": "none",
  "input_tokens": 2954,
  "output_tokens": 4578,
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
  "formId": "eu-sydney-event-registration",
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
            "helpText": "We will process your personal data to manage your registration, ensure safety at the event, and send essential event communications. For full details see the event terms.",
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
            "helpText": "As shown on ID, used for name badge and communication.",
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
            "helpText": "As shown on ID.",
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
            "helpText": "We will send registration confirmations and essential event messages to this address.",
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
            "helpText": "Optional \u2014 useful for last-minute event updates or safety communications.",
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
            "helpText": "If attending on behalf of an organisation, enter its name.",
            "label": "Organisation (optional)",
            "placeholder": "Company or organisation",
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
            "helpText": "Confirm the lawful basis for processing required to administer your registration.",
            "label": "Lawful-basis acknowledgement",
            "options": [
              {
                "label": "I acknowledge that my personal data will be processed to administer my registration, ensure health & safety, and send essential event communications.",
                "value": "ack_lawful_basis"
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
            "helpText": "Consent to receive news and marketing about future events. This is optional and separate from registration.",
            "label": "Marketing & updates (optional)",
            "options": [
              {
                "label": "I consent to receive marketing and event updates by email.",
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
            "helpText": "Use the company-managed 'event terms' link (opens in popup). Preserve the company terms link and display.",
            "label": "Accept event terms & privacy policy",
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
            "helpText": "By submitting you confirm the information above is accurate.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
    "matched_text": "ZIP code",
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
  "duration_ms": 60625,
  "failure_class": "none",
  "input_tokens": 2964,
  "output_tokens": 4278,
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
            "label": "Data handling notice: We will process your personal data to manage your event registration, communicate event details, and meet our legal obligations. Our lawful bases for processing are described below. You may withdraw consent where processing is based on consent. Personal data will be stored and handled in accordance with applicable EU data protection law.",
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
            "helpText": "Enter your first name as it appears on official ID if required.",
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
            "helpText": "We will use this to send registration confirmation and event updates.",
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
            "helpText": "Provide a phone number we can use for urgent event notifications. +1 wording is requested.",
            "label": "Phone (+1 preferred)",
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
            "helpText": "Enter your postal ZIP code. Field label intentionally uses 'ZIP' wording.",
            "label": "ZIP code",
            "placeholder": "ZIP / postal code",
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
          "id": "address-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Street, city, region and country (optional where not required).",
            "label": "Postal address",
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
            "helpText": "Select the lawful basis under which your personal data will be processed for this event. This helps meet GDPR transparency requirements.",
            "label": "Lawful basis for processing \u2014 please acknowledge which applies",
            "options": [
              {
                "label": "Consent (you give explicit consent for processing)",
                "value": "consent"
              },
              {
                "label": "Contract performance (processing necessary to fulfil your registration)",
                "value": "contract"
              },
              {
                "label": "Legitimate interest (processing necessary for our legitimate interests)",
                "value": "legitimate_interest"
              },
              {
                "label": "Legal obligation (processing required by law)",
                "value": "legal_obligation"
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
            "helpText": "Tick to receive marketing emails and SMS about future events. This is optional and separate from event administration.",
            "label": "Marketing communications (optional)",
            "options": [
              {
                "label": "I agree to receive marketing communications by email and SMS",
                "value": "marketing_consent"
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
            "y": 920
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to the event terms and data processing described to complete registration. See the company-managed event terms for full details.",
            "label": "Agreement to event terms and data processing",
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
            "y": 1064
          },
          "props": {
            "height": 72,
            "helpText": "By registering you confirm the information provided is accurate and you have acknowledged the data handling notice.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 10,
  "duration_ms": 42996,
  "failure_class": "none",
  "input_tokens": 2884,
  "output_tokens": 2855,
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
            "label": "We will not request SSN or TIN on this form. Please provide contact details and the role you are interested in.",
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
            "helpText": "Given name",
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
            "helpText": "Family name",
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
            "helpText": "We will use this to contact you",
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
            "helpText": "Optional \u2014 include country code if outside the US",
            "label": "Phone",
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
          "id": "address-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Optional",
            "label": "Mailing address",
            "placeholder": "Street, city, state, ZIP",
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
            "helpText": "Choose the role that best matches your interests",
            "label": "Role / Area of work",
            "options": [
              {
                "label": "Developer / Engineer",
                "value": "developer"
              },
              {
                "label": "Designer",
                "value": "designer"
              },
              {
                "label": "Product Manager",
                "value": "product_manager"
              },
              {
                "label": "Marketing",
                "value": "marketing"
              },
              {
                "label": "Sales / Business Development",
                "value": "sales"
              },
              {
                "label": "Operations / Admin",
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
          "id": "checkbox-8",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 120,
            "helpText": "Select any that apply",
            "label": "Areas of interest",
            "options": [
              {
                "label": "Events",
                "value": "events"
              },
              {
                "label": "Partnerships",
                "value": "partnerships"
              },
              {
                "label": "Volunteering",
                "value": "volunteering"
              },
              {
                "label": "Sponsorship",
                "value": "sponsorship"
              },
              {
                "label": "Speaking",
                "value": "speaking"
              },
              {
                "label": "Other",
                "value": "other_interest"
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
            "helpText": "Include any relevant links or portfolio references",
            "label": "Tell us about your experience or interests",
            "placeholder": "Briefly describe your background, availability, or what you're looking for.",
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
          "id": "submit-button-10",
          "position": {
            "x": 40,
            "y": 1080
          },
          "props": {
            "height": 72,
            "label": "Submit",
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

## Row 38: `p13-au-ambiguous-r1__r01`

- Prompt ID: `p13-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 10,
  "duration_ms": 54599,
  "failure_class": "none",
  "input_tokens": 2956,
  "output_tokens": 3248,
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
            "label": "We\u2019re hosting an event in Sydney. Please share your contact details and role so our team can get in touch about onboarding opportunities.",
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
            "helpText": "Your given name",
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
            "helpText": "Your family name",
            "label": "Last name",
            "placeholder": "e.g. Doe",
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
            "helpText": "We\u2019ll use this to contact you about onboarding",
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
            "helpText": "Include country code if outside the US",
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
          "id": "text-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "If applicable",
            "label": "Company / Organization (optional)",
            "placeholder": "Your employer or organisation",
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
            "helpText": "Choose the option that best describes your interest in onboarding",
            "label": "Role / interest",
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
                "label": "Volunteer",
                "value": "volunteer"
              },
              {
                "label": "Sponsor",
                "value": "sponsor"
              },
              {
                "label": "Exhibitor",
                "value": "exhibitor"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select your primary role or interest",
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
            "helpText": "Tell us anything else that will help us follow up",
            "label": "Additional details or questions (optional)",
            "placeholder": "Share any relevant background, availability, or questions",
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
            "helpText": "By submitting this form you accept the event terms.",
            "label": "I agree to the event terms",
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
            "helpText": "We\u2019ll contact you with next steps.",
            "label": "Express interest",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 12,
  "duration_ms": 55197,
  "failure_class": "none",
  "input_tokens": 2966,
  "output_tokens": 3961,
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
            "label": "Please complete your contact details and select your role. We will follow up with next steps.",
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
            "helpText": "We'll use this to contact you.",
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
            "helpText": "Include country code +1 for US phone numbers.",
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
          "id": "dropdown-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Choose the option that best describes your role for this event.",
            "label": "Role",
            "options": [
              {
                "label": "Attendee",
                "value": "attendee"
              },
              {
                "label": "Vendor / Exhibitor",
                "value": "vendor"
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
                "label": "Volunteer",
                "value": "volunteer"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select your role",
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
            "helpText": "Enter your U.S. ZIP code.",
            "label": "ZIP code",
            "placeholder": "e.g., 94107",
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
            "label": "Company (optional)",
            "placeholder": "Your organisation or company",
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
            "helpText": "Optional notes or questions.",
            "label": "Anything else you'd like us to know? (optional)",
            "placeholder": "Tell us how we can help or any special requirements",
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
            "helpText": "Opt in to receive updates about this event.",
            "label": "Communications preferences",
            "options": [
              {
                "label": "Yes \u2014 send me event updates and related news",
                "value": "subscribe_yes"
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
            "helpText": "You must accept the event terms to proceed.",
            "label": "I agree to the event terms",
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
            "label": "Submit",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 13,
  "duration_ms": 49550,
  "failure_class": "none",
  "input_tokens": 2881,
  "output_tokens": 3645,
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
  "formId": "nhs-adj-waiver-form",
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
          "id": "date-3",
          "position": {
            "x": 40,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Provide your date of birth to help with identification and clinical relevance.",
            "label": "Date of birth",
            "placeholder": "DD/MM/YYYY",
            "tabOrder": 3,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 320
          },
          "type": "date"
        },
        {
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "A number we can use to contact you about care or logistics.",
            "label": "Contact phone",
            "placeholder": "Primary phone number",
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
          "id": "email-5",
          "position": {
            "x": 384,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Useful for non-urgent communications and confirmations.",
            "label": "Email (optional)",
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
            "y": 426
          },
          "props": {
            "height": 110,
            "helpText": "Provide your usual home address.",
            "label": "Home address",
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
            "y": 560
          },
          "props": {
            "height": 120,
            "helpText": "Select any that apply. Use 'Other' to add additional details in the notes field below.",
            "label": "Known conditions / needs (select all that apply)",
            "options": [
              {
                "label": "Allergies (e.g., drugs, food)",
                "value": "allergies"
              },
              {
                "label": "Current medications",
                "value": "medications"
              },
              {
                "label": "Mobility assistance required",
                "value": "mobility"
              },
              {
                "label": "Chronic health condition",
                "value": "chronic"
              },
              {
                "label": "Visual or hearing impairment",
                "value": "sensory"
              },
              {
                "label": "None of the above",
                "value": "none"
              },
              {
                "label": "Other (please describe in notes)",
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
            "helpText": "Provide any other information clinicians or responders should know.",
            "label": "Relevant health notes / additional information",
            "placeholder": "Include allergies, medication names and doses, mobility restrictions, or any other details important for care or emergency response.",
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
            "y": 1008
          },
          "props": {
            "height": 110,
            "helpText": "Person to contact in case of emergency.",
            "label": "Emergency contact name",
            "placeholder": "Full name",
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
          "id": "phone-10",
          "position": {
            "x": 384,
            "y": 1008
          },
          "props": {
            "height": 110,
            "label": "Emergency contact phone",
            "placeholder": "Emergency contact number",
            "tabOrder": 10,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "dropdown-11",
          "position": {
            "x": 40,
            "y": 1142
          },
          "props": {
            "height": 110,
            "label": "Relationship to participant",
            "options": [
              {
                "label": "Spouse / Partner",
                "value": "spouse_partner"
              },
              {
                "label": "Parent / Guardian",
                "value": "parent_guardian"
              },
              {
                "label": "Child",
                "value": "child"
              },
              {
                "label": "Friend",
                "value": "friend"
              },
              {
                "label": "Carer",
                "value": "carer"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select relationship",
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
          "id": "terms-12",
          "position": {
            "x": 40,
            "y": 1276
          },
          "props": {
            "height": 120,
            "helpText": "You must agree to these terms to participate.",
            "label": "I acknowledge that this form is used for NHS\u2011adjacent care coordination and emergency response. I consent to the collection and use of the health information I provide for the purposes of care, safety, and emergency contact. I confirm the information is accurate to the best of my knowledge.",
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
            "y": 1420
          },
          "props": {
            "height": 72,
            "label": "Submit",
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
      "title": "NHS-adjacent Waiver & Health Form"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 84732,
  "failure_class": "none",
  "input_tokens": 7548,
  "output_tokens": 6564,
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
  "formId": "sydney-nhs-adj-waiver",
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
            "label": "This form collects participant details, relevant health information, emergency contact details, and a consent acknowledgement. The form follows NHS-adjacent health screening style guidance; complete as accurately as possible.",
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
            "helpText": "Required for age-related medical guidance.",
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
            "helpText": "We will use this to contact you about the event if needed.",
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
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Provide the best number to reach you on the day.",
            "label": "Phone / Mobile",
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
          "id": "address-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Optional but helpful for medical records if required.",
            "label": "Home address",
            "placeholder": "Street, suburb, city, postcode",
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
            "helpText": "Include any information that event staff should know to keep you safe.",
            "label": "Relevant health information",
            "placeholder": "List medical conditions, allergies, current medications, mobility or sensory needs",
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
          "id": "radio-9",
          "position": {
            "x": 40,
            "y": 936
          },
          "props": {
            "height": 120,
            "helpText": "Select Yes if you have a condition that may require attention during the event.",
            "label": "Do you have any serious medical conditions (e.g., heart conditions, severe asthma, epilepsy)?",
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
          "id": "textarea-10",
          "position": {
            "x": 40,
            "y": 1080
          },
          "props": {
            "height": 200,
            "helpText": "Only complete if you selected Yes above.",
            "label": "If yes, please provide details and any recommended actions/support",
            "placeholder": "Describe condition, triggers, medication, emergency actions, or support needs",
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
            "y": 1384
          },
          "props": {
            "height": 120,
            "helpText": "This enables event first aid and medical teams to provide appropriate care if needed.",
            "label": "I consent to sharing relevant medical information with event medical staff for my safety",
            "options": [
              {
                "label": "I consent to share relevant medical information with event medical staff",
                "value": "consent_share_medical"
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
            "y": 1528
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
            "y": 1528
          },
          "props": {
            "height": 110,
            "label": "Relationship to you",
            "placeholder": "e.g., partner, parent, friend",
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
            "y": 1662
          },
          "props": {
            "height": 110,
            "helpText": "Provide a number where this person can be reached during the event.",
            "label": "Emergency contact phone",
            "placeholder": "+61 4XX XXX XXX",
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
            "y": 1796
          },
          "props": {
            "height": 120,
            "helpText": "Please read the event terms. Checking this box indicates you agree to the event terms, waiver and consent to necessary medical treatment.",
            "label": "Acknowledgement & consent (event terms, waiver and medical consent)",
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
            "y": 1940
          },
          "props": {
            "height": 72,
            "label": "Submit and Acknowledge",
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
      "title": "Event Waiver & Health Information \u2014 Sydney"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
    "prompt_id": "p14-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
  {
    "check_id": "foreign_zip",
    "description": "ZIP where Postcode is expected",
    "matched_text": "ZIP code",
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
  "component_count": 15,
  "duration_ms": 46167,
  "failure_class": "none",
  "input_tokens": 2963,
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
    "height": 1574,
    "width": 960
  },
  "formId": "uk-nhs-adjacent-waiver",
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
            "label": "This form collects participant details, health notes, emergency contact information, and a consent acknowledgement. If you are based in the UK, provide your postcode where requested; this form will also ask for a ZIP code format.",
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
            "placeholder": "Family name / Surname",
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
            "helpText": "Enter in DD/MM/YYYY format where possible.",
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
          "id": "text-5",
          "position": {
            "x": 384,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We request ZIP-style input alongside UK postcodes. Provide whichever applies.",
            "label": "ZIP code / Postcode",
            "placeholder": "Enter ZIP code (e.g., 90210) or UK postcode",
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
          "id": "phone-6",
          "position": {
            "x": 40,
            "y": 364
          },
          "props": {
            "height": 110,
            "helpText": "Please include country code; +1 requested for phone number formatting.",
            "label": "Phone number",
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
            "y": 364
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
          "id": "address-8",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 110,
            "helpText": "Optional. Include building and street details.",
            "label": "Street address (optional)",
            "placeholder": "Street, city, region",
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
          "id": "paragraph-9",
          "position": {
            "x": 40,
            "y": 632
          },
          "props": {
            "height": 48,
            "helpText": "Tell us about any medical conditions, medications, allergies or accommodations we should know about.",
            "label": "Health information",
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
          "id": "radio-10",
          "position": {
            "x": 40,
            "y": 704
          },
          "props": {
            "height": 120,
            "label": "Do you have any medical conditions, allergies, or medications to disclose?",
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
          "id": "textarea-11",
          "position": {
            "x": 40,
            "y": 848
          },
          "props": {
            "height": 200,
            "helpText": "If you selected Yes above, provide details here. Otherwise leave blank.",
            "label": "If yes, please describe conditions, medications, allergies and any other relevant health notes",
            "placeholder": "List conditions, medication names & dosages, known triggers, and any accommodations required.",
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
            "label": "Emergency contact name",
            "placeholder": "Full name",
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
          "id": "phone-13",
          "position": {
            "x": 384,
            "y": 1152
          },
          "props": {
            "height": 110,
            "helpText": "Include country code; form requests +1 format for emergency numbers.",
            "label": "Emergency contact phone (+1 required)",
            "placeholder": "[SCRUBBED_PHONE]",
            "tabOrder": 13,
            "width": "320px"
          },
          "style": {
            "height": 110,
            "width": 360
          },
          "type": "phone"
        },
        {
          "id": "terms-14",
          "position": {
            "x": 40,
            "y": 1286
          },
          "props": {
            "height": 120,
            "helpText": "Company-managed event terms will be presented via the provided event terms link.",
            "label": "I acknowledge and accept the event terms and consent to participate in the activities described. By checking, I confirm that the information I have provided is accurate to the best of my knowledge.",
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
            "label": "I Agree & Submit",
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
      "title": "Participant Waiver \u2014 NHS-adjacent"
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "component_count": 11,
  "duration_ms": 48815,
  "failure_class": "none",
  "input_tokens": 2883,
  "output_tokens": 4019,
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
            "helpText": "We'll use this to confirm your RSVP.",
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
            "helpText": "Include country code (+64) and area/mobile number.",
            "label": "Phone (New Zealand)",
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
                "label": "Manawatu-Wanganui",
                "value": "manawatu_whanganui"
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
                "label": "Southland",
                "value": "southland"
              },
              {
                "label": "Gisborne",
                "value": "gisborne"
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
                "label": "West Coast",
                "value": "west_coast"
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select your region",
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
            "helpText": "Select any that apply (select 'None' if you have no dietary needs).",
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
            "helpText": "If you selected 'Other' above, tell us more here.",
            "label": "Other dietary requirements",
            "placeholder": "Please describe any other dietary needs",
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
            "helpText": "Select any accessibility supports you require or add details below.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Mobility assistance / wheelchair access",
                "value": "mobility"
              },
              {
                "label": "Hearing loop / captioning",
                "value": "hearing"
              },
              {
                "label": "Sign language interpreter",
                "value": "sign_language"
              },
              {
                "label": "Visual aids / large print",
                "value": "visual"
              },
              {
                "label": "Neurodiversity support",
                "value": "neurodiversity"
              },
              {
                "label": "Assistance animal",
                "value": "assistance_animal"
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
            "y": 1018
          },
          "props": {
            "height": 200,
            "helpText": "Providing details helps us make appropriate arrangements.",
            "label": "Accessibility details",
            "placeholder": "Tell us about any adjustments or supports you need (optional)",
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
            "helpText": "You can opt out at any time.",
            "label": "I agree to receive event updates and communications about this event.",
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
  "duration_ms": 60686,
  "failure_class": "none",
  "input_tokens": 2955,
  "output_tokens": 3986,
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
    "height": 1538,
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
            "helpText": "This event is associated with Sydney. Please confirm your details for travel or correspondence.",
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
          "id": "phone-4",
          "position": {
            "x": 40,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "Provide a New Zealand phone number. Include country code (+64) or local leading zero.",
            "label": "Phone (New Zealand)",
            "placeholder": "[SCRUBBED_PHONE] or [SCRUBBED_PHONE]",
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
          "id": "email-5",
          "position": {
            "x": 384,
            "y": 230
          },
          "props": {
            "height": 110,
            "helpText": "We'll send RSVP confirmations and important event information to this address.",
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
            "helpText": "Select the New Zealand region you're based in.",
            "label": "Region (in New Zealand)",
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
                "label": "Hawke's Bay",
                "value": "hawkes_bay"
              },
              {
                "label": "Manawatu-Wanganui",
                "value": "manawatu_wanganui"
              },
              {
                "label": "Taranaki",
                "value": "taranaki"
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
              },
              {
                "label": "Other / Outside NZ",
                "value": "other"
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
          "id": "checkbox-7",
          "position": {
            "x": 40,
            "y": 498
          },
          "props": {
            "height": 120,
            "helpText": "Select any dietary requirements. If 'Other', provide details in the field below.",
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
            "label": "Dietary details (if other or additional information)",
            "placeholder": "Describe any allergies, intolerances or special instructions",
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
            "y": 946
          },
          "props": {
            "height": 200,
            "helpText": "Tell us about any mobility, hearing, vision or other needs so we can accommodate you.",
            "label": "Accessibility needs",
            "placeholder": "Let us know any accessibility or support requirements",
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
            "y": 1250
          },
          "props": {
            "height": 120,
            "helpText": "Opt in to receive event updates and important information.",
            "label": "Event updates",
            "options": [
              {
                "label": "Yes \u2014 send me event updates via email and SMS",
                "value": "yes_updates"
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
            "y": 1394
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
- Variant: `story-6.4.6-au-baseline-native-concurrency-20260430T1710`
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
    "prompt_id": "p15-au-adversarial-r1",
    "scope": "generated_definition",
    "section_id": null,
    "severity": "blocking"
  },
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
    "matched_text": "+1",
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
  "duration_ms": 48618,
  "failure_class": "none",
  "input_tokens": 2965,
  "output_tokens": 4336,
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
            "width": 320
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
            "helpText": "Include country code. +1 wording is requested for this form.",
            "label": "Phone (format requested: [SCRUBBED_PHONE])",
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
          "id": "text-4",
          "position": {
            "x": 384,
            "y": 158
          },
          "props": {
            "height": 110,
            "helpText": "Enter ZIP code (postcode).",
            "label": "ZIP code",
            "placeholder": "ZIP / Postcode",
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
          "id": "dropdown-5",
          "position": {
            "x": 40,
            "y": 292
          },
          "props": {
            "height": 110,
            "helpText": "Select the region you are based in.",
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
                "label": "Manawat\u016b-Whanganui",
                "value": "manawatu_whanganui"
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
                "label": "Gisborne",
                "value": "gisborne"
              },
              {
                "label": "Taranaki",
                "value": "taranaki"
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
              },
              {
                "label": "Other",
                "value": "other"
              }
            ],
            "placeholder": "Select your region",
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
            "helpText": "Select any that apply.",
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
                "label": "Nut allergy",
                "value": "nut_allergy"
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
          "id": "textarea-7",
          "position": {
            "x": 40,
            "y": 570
          },
          "props": {
            "height": 200,
            "label": "Dietary details (please specify if 'Other' selected)",
            "placeholder": "Provide any details we should know about (allergies, severity, etc.)",
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
            "helpText": "Select any supports you require for the event.",
            "label": "Accessibility needs",
            "options": [
              {
                "label": "Wheelchair access",
                "value": "wheelchair"
              },
              {
                "label": "Hearing loop / hearing support",
                "value": "hearing"
              },
              {
                "label": "Sign language interpreter",
                "value": "asl_interpreter"
              },
              {
                "label": "Visual assistance / large print",
                "value": "visual"
              },
              {
                "label": "Assistance with stairs",
                "value": "stairs"
              },
              {
                "label": "Assistance with seating",
                "value": "seating"
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
            "y": 1018
          },
          "props": {
            "height": 200,
            "label": "Accessibility details",
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
            "y": 1322
          },
          "props": {
            "height": 120,
            "label": "I agree to receive event updates and accept the event terms",
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
