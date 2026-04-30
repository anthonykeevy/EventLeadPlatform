# Form AI Judge Input Batch

Run ID: `story-6.4.6-au-baseline-current-smoke`
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
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p01-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p01-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p01-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p01-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 2: `p01-au-ambiguous-r1__r01`

- Prompt ID: `p01-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p01-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p01-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p01-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p01-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 3: `p01-au-adversarial-r1__r01`

- Prompt ID: `p01-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p01-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p01-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p01-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p01-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 4: `p02-au-neutral-r1__r01`

- Prompt ID: `p02-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p02-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p02-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p02-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p02-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 5: `p02-au-ambiguous-r1__r01`

- Prompt ID: `p02-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p02-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p02-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p02-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p02-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 6: `p02-au-adversarial-r1__r01`

- Prompt ID: `p02-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p02-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p02-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p02-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p02-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 7: `p03-au-neutral-r1__r01`

- Prompt ID: `p03-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p03-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p03-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p03-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p03-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 8: `p03-au-ambiguous-r1__r01`

- Prompt ID: `p03-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p03-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p03-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p03-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p03-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 9: `p03-au-adversarial-r1__r01`

- Prompt ID: `p03-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p03-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p03-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p03-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p03-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 10: `p04-au-neutral-r1__r01`

- Prompt ID: `p04-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p04-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p04-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p04-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p04-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 11: `p04-au-ambiguous-r1__r01`

- Prompt ID: `p04-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p04-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p04-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p04-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p04-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 12: `p04-au-adversarial-r1__r01`

- Prompt ID: `p04-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p04-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p04-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p04-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p04-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 13: `p05-au-neutral-r1__r01`

- Prompt ID: `p05-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p05-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p05-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p05-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p05-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 14: `p05-au-ambiguous-r1__r01`

- Prompt ID: `p05-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p05-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p05-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p05-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p05-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 15: `p05-au-adversarial-r1__r01`

- Prompt ID: `p05-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p05-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p05-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p05-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p05-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 16: `p06-au-neutral-r1__r01`

- Prompt ID: `p06-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p06-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p06-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p06-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p06-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 17: `p06-au-ambiguous-r1__r01`

- Prompt ID: `p06-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p06-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p06-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p06-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p06-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 18: `p06-au-adversarial-r1__r01`

- Prompt ID: `p06-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p06-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p06-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p06-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p06-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 19: `p07-au-neutral-r1__r01`

- Prompt ID: `p07-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p07-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p07-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p07-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p07-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 20: `p07-au-ambiguous-r1__r01`

- Prompt ID: `p07-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p07-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p07-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p07-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p07-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 21: `p07-au-adversarial-r1__r01`

- Prompt ID: `p07-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p07-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p07-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p07-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p07-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 22: `p08-au-neutral-r1__r01`

- Prompt ID: `p08-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p08-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p08-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p08-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p08-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 23: `p08-au-ambiguous-r1__r01`

- Prompt ID: `p08-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p08-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p08-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p08-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p08-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 24: `p08-au-adversarial-r1__r01`

- Prompt ID: `p08-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p08-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p08-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p08-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p08-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 25: `p09-au-neutral-r1__r01`

- Prompt ID: `p09-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p09-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p09-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p09-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p09-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 26: `p09-au-ambiguous-r1__r01`

- Prompt ID: `p09-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p09-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p09-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p09-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p09-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 27: `p09-au-adversarial-r1__r01`

- Prompt ID: `p09-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p09-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p09-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p09-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p09-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 28: `p10-au-neutral-r1__r01`

- Prompt ID: `p10-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p10-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p10-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p10-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p10-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 29: `p10-au-ambiguous-r1__r01`

- Prompt ID: `p10-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p10-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p10-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p10-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p10-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 30: `p10-au-adversarial-r1__r01`

- Prompt ID: `p10-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p10-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p10-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p10-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p10-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 31: `p11-au-neutral-r1__r01`

- Prompt ID: `p11-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p11-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p11-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p11-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p11-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 32: `p11-au-ambiguous-r1__r01`

- Prompt ID: `p11-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p11-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p11-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p11-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p11-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 33: `p11-au-adversarial-r1__r01`

- Prompt ID: `p11-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p11-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p11-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p11-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p11-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 34: `p12-au-neutral-r1__r01`

- Prompt ID: `p12-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p12-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p12-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p12-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p12-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 35: `p12-au-ambiguous-r1__r01`

- Prompt ID: `p12-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p12-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p12-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p12-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p12-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 36: `p12-au-adversarial-r1__r01`

- Prompt ID: `p12-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p12-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p12-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p12-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p12-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 37: `p13-au-neutral-r1__r01`

- Prompt ID: `p13-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p13-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p13-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p13-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p13-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 38: `p13-au-ambiguous-r1__r01`

- Prompt ID: `p13-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p13-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p13-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p13-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p13-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 39: `p13-au-adversarial-r1__r01`

- Prompt ID: `p13-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p13-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p13-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p13-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p13-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 40: `p14-au-neutral-r1__r01`

- Prompt ID: `p14-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p14-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p14-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p14-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p14-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 41: `p14-au-ambiguous-r1__r01`

- Prompt ID: `p14-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p14-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p14-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p14-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p14-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 42: `p14-au-adversarial-r1__r01`

- Prompt ID: `p14-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p14-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p14-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p14-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p14-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 43: `p15-au-neutral-r1__r01`

- Prompt ID: `p15-au-neutral-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p15-au-neutral-r1-c-0",
          "type": "text"
        },
        {
          "id": "p15-au-neutral-r1-c-1",
          "type": "text"
        },
        {
          "id": "p15-au-neutral-r1-c-2",
          "type": "text"
        },
        {
          "id": "p15-au-neutral-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 44: `p15-au-ambiguous-r1__r01`

- Prompt ID: `p15-au-ambiguous-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p15-au-ambiguous-r1-c-0",
          "type": "text"
        },
        {
          "id": "p15-au-ambiguous-r1-c-1",
          "type": "text"
        },
        {
          "id": "p15-au-ambiguous-r1-c-2",
          "type": "text"
        },
        {
          "id": "p15-au-ambiguous-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```

## Row 45: `p15-au-adversarial-r1__r01`

- Prompt ID: `p15-au-adversarial-r1`
- Repetition: `1`
- Variant: `story-6.4.6-au-baseline-current-smoke`
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
[]
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 4,
  "duration_ms": 0,
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
  "pages": [
    {
      "components": [
        {
          "id": "p15-au-adversarial-r1-c-0",
          "type": "text"
        },
        {
          "id": "p15-au-adversarial-r1-c-1",
          "type": "text"
        },
        {
          "id": "p15-au-adversarial-r1-c-2",
          "type": "text"
        },
        {
          "id": "p15-au-adversarial-r1-c-3",
          "type": "text"
        }
      ]
    }
  ],
  "schemaVersion": "1.0"
}
```
