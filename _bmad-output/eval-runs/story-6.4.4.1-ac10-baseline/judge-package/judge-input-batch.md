# Form AI Judge Input Batch

Run ID: `story-6.4.4.1-ac10-baseline`
Benchmark set: `prompts-v1.1`
Rubric version: `rubric_v2`

Use `rubric_v2.md` and return JSON matching `judge-output-template.json`.
Set `judge_model_version` to the exact model/version shown in your Cursor session.
Before assigning scores for each row, identify at least one weakness per row before scoring.
Judge only the anonymised package content below.

## Row 1: `p01-au-neutral-r1__r01`

- Prompt ID: `p01-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "AU",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 39786,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 2: `p01-au-ambiguous-r1__r01`

- Prompt ID: `p01-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "AU",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 49713,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 3: `p01-au-adversarial-r1__r01`

- Prompt ID: `p01-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "AU",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 38290,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 4: `p01-nz-neutral-r1__r01`

- Prompt ID: `p01-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "NZ",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 38123,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 5: `p01-nz-ambiguous-r1__r01`

- Prompt ID: `p01-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "NZ",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 37034,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 6: `p01-nz-adversarial-r1__r01`

- Prompt ID: `p01-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "NZ",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 32557,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 7: `p01-uk-neutral-r1__r01`

- Prompt ID: `p01-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "UK",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 43359,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 8: `p01-uk-ambiguous-r1__r01`

- Prompt ID: `p01-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "UK",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 40026,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 9: `p01-uk-adversarial-r1__r01`

- Prompt ID: `p01-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "UK",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 32993,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 10: `p01-us-neutral-r1__r01`

- Prompt ID: `p01-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "US",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 34009,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 11: `p01-us-ambiguous-r1__r01`

- Prompt ID: `p01-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "US",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 47231,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 12: `p01-us-adversarial-r1__r01`

- Prompt ID: `p01-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "US",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 37590,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 13: `p01-intl-online-neutral-r1__r01`

- Prompt ID: `p01-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 35462,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 14: `p01-intl-online-ambiguous-r1__r01`

- Prompt ID: `p01-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 44314,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 15: `p01-intl-online-adversarial-r1__r01`

- Prompt ID: `p01-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 40642,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 16: `p01-eu-neutral-r1__r01`

- Prompt ID: `p01-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "EU",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 47308,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 17: `p01-eu-ambiguous-r1__r01`

- Prompt ID: `p01-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "EU",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 41272,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 18: `p01-eu-adversarial-r1__r01`

- Prompt ID: `p01-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

I need a registration form for our annual sales conference. Capture name, email, phone, dietary requirements, t-shirt size. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p01",
  "locale_axis": "EU",
  "prompt_category": "event-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 42127,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 19: `p02-au-neutral-r1__r01`

- Prompt ID: `p02-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "AU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 32744,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 20: `p02-au-ambiguous-r1__r01`

- Prompt ID: `p02-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "AU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 42865,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 21: `p02-au-adversarial-r1__r01`

- Prompt ID: `p02-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "AU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 62912,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 22: `p02-nz-neutral-r1__r01`

- Prompt ID: `p02-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "NZ",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 35987,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 23: `p02-nz-ambiguous-r1__r01`

- Prompt ID: `p02-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "NZ",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 56045,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 24: `p02-nz-adversarial-r1__r01`

- Prompt ID: `p02-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "NZ",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 68961,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 25: `p02-uk-neutral-r1__r01`

- Prompt ID: `p02-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "UK",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 27226,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 26: `p02-uk-ambiguous-r1__r01`

- Prompt ID: `p02-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "UK",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 44806,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 27: `p02-uk-adversarial-r1__r01`

- Prompt ID: `p02-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "UK",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 54629,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 28: `p02-us-neutral-r1__r01`

- Prompt ID: `p02-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "US",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 32557,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 29: `p02-us-ambiguous-r1__r01`

- Prompt ID: `p02-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "US",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 55228,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 30: `p02-us-adversarial-r1__r01`

- Prompt ID: `p02-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "US",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 64414,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 31: `p02-intl-online-neutral-r1__r01`

- Prompt ID: `p02-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 38815,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 32: `p02-intl-online-ambiguous-r1__r01`

- Prompt ID: `p02-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 50794,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 33: `p02-intl-online-adversarial-r1__r01`

- Prompt ID: `p02-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 53945,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 34: `p02-eu-neutral-r1__r01`

- Prompt ID: `p02-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "EU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 39408,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 35: `p02-eu-ambiguous-r1__r01`

- Prompt ID: `p02-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "EU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 51709,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 36: `p02-eu-adversarial-r1__r01`

- Prompt ID: `p02-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a conference RSVP form with attendee details, session choice, dietary needs, and consent to receive event updates. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p02",
  "locale_axis": "EU",
  "prompt_category": "conference-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 66175,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 37: `p03-au-neutral-r1__r01`

- Prompt ID: `p03-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "AU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 48686,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 38: `p03-au-ambiguous-r1__r01`

- Prompt ID: `p03-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "AU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 65284,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 39: `p03-au-adversarial-r1__r01`

- Prompt ID: `p03-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "AU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 73024,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 40: `p03-nz-neutral-r1__r01`

- Prompt ID: `p03-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "NZ",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 51739,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 41: `p03-nz-ambiguous-r1__r01`

- Prompt ID: `p03-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "NZ",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 46297,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 42: `p03-nz-adversarial-r1__r01`

- Prompt ID: `p03-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "NZ",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 53498,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 43: `p03-uk-neutral-r1__r01`

- Prompt ID: `p03-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "UK",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 60546,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 44: `p03-uk-ambiguous-r1__r01`

- Prompt ID: `p03-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "UK",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 66449,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 45: `p03-uk-adversarial-r1__r01`

- Prompt ID: `p03-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "UK",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 59221,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 46: `p03-us-neutral-r1__r01`

- Prompt ID: `p03-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "US",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 63904,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 47: `p03-us-ambiguous-r1__r01`

- Prompt ID: `p03-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "US",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 51790,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 48: `p03-us-adversarial-r1__r01`

- Prompt ID: `p03-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "US",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 48898,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 49: `p03-intl-online-neutral-r1__r01`

- Prompt ID: `p03-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 54218,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 50: `p03-intl-online-ambiguous-r1__r01`

- Prompt ID: `p03-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 52381,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 51: `p03-intl-online-adversarial-r1__r01`

- Prompt ID: `p03-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 44625,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 52: `p03-eu-neutral-r1__r01`

- Prompt ID: `p03-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "EU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 44116,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 53: `p03-eu-ambiguous-r1__r01`

- Prompt ID: `p03-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "EU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 44181,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 54: `p03-eu-adversarial-r1__r01`

- Prompt ID: `p03-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a workshop signup form capturing participant details, skill level, accessibility needs, and preferred workshop stream. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p03",
  "locale_axis": "EU",
  "prompt_category": "workshop-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 50721,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 55: `p04-au-neutral-r1__r01`

- Prompt ID: `p04-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "AU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 63608,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 56: `p04-au-ambiguous-r1__r01`

- Prompt ID: `p04-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "AU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 57502,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 57: `p04-au-adversarial-r1__r01`

- Prompt ID: `p04-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "AU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 66270,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 58: `p04-nz-neutral-r1__r01`

- Prompt ID: `p04-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "NZ",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 38927,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 59: `p04-nz-ambiguous-r1__r01`

- Prompt ID: `p04-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "NZ",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 115716,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 60: `p04-nz-adversarial-r1__r01`

- Prompt ID: `p04-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "NZ",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 61473,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 61: `p04-uk-neutral-r1__r01`

- Prompt ID: `p04-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "UK",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 123915,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 62: `p04-uk-ambiguous-r1__r01`

- Prompt ID: `p04-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "UK",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 46219,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 63: `p04-uk-adversarial-r1__r01`

- Prompt ID: `p04-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "UK",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 81447,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 64: `p04-us-neutral-r1__r01`

- Prompt ID: `p04-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "US",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 39738,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 65: `p04-us-ambiguous-r1__r01`

- Prompt ID: `p04-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "US",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 56616,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 66: `p04-us-adversarial-r1__r01`

- Prompt ID: `p04-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "US",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 55277,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 67: `p04-intl-online-neutral-r1__r01`

- Prompt ID: `p04-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 51183,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 68: `p04-intl-online-ambiguous-r1__r01`

- Prompt ID: `p04-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 69555,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 69: `p04-intl-online-adversarial-r1__r01`

- Prompt ID: `p04-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 59889,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 70: `p04-eu-neutral-r1__r01`

- Prompt ID: `p04-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "EU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 49018,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 71: `p04-eu-ambiguous-r1__r01`

- Prompt ID: `p04-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "EU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 56972,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 72: `p04-eu-adversarial-r1__r01`

- Prompt ID: `p04-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a webinar registration form with contact details, organisation, role, timezone, questions for the speaker, and marketing opt-in. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p04",
  "locale_axis": "EU",
  "prompt_category": "webinar-registration",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 62565,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 73: `p05-au-neutral-r1__r01`

- Prompt ID: `p05-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "AU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 73078,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 74: `p05-au-ambiguous-r1__r01`

- Prompt ID: `p05-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "AU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 55067,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 75: `p05-au-adversarial-r1__r01`

- Prompt ID: `p05-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "AU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 46441,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 76: `p05-nz-neutral-r1__r01`

- Prompt ID: `p05-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "NZ",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 46046,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 77: `p05-nz-ambiguous-r1__r01`

- Prompt ID: `p05-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "NZ",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 54449,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 78: `p05-nz-adversarial-r1__r01`

- Prompt ID: `p05-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "NZ",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 45982,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 79: `p05-uk-neutral-r1__r01`

- Prompt ID: `p05-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "UK",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 54962,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 80: `p05-uk-ambiguous-r1__r01`

- Prompt ID: `p05-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "UK",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 46118,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 81: `p05-uk-adversarial-r1__r01`

- Prompt ID: `p05-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "UK",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 44657,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 82: `p05-us-neutral-r1__r01`

- Prompt ID: `p05-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "US",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 52188,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 83: `p05-us-ambiguous-r1__r01`

- Prompt ID: `p05-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "US",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 52777,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 84: `p05-us-adversarial-r1__r01`

- Prompt ID: `p05-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "US",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 65716,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 85: `p05-intl-online-neutral-r1__r01`

- Prompt ID: `p05-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 47640,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 86: `p05-intl-online-ambiguous-r1__r01`

- Prompt ID: `p05-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 56672,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 87: `p05-intl-online-adversarial-r1__r01`

- Prompt ID: `p05-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 57527,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 88: `p05-eu-neutral-r1__r01`

- Prompt ID: `p05-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "EU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 62954,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 89: `p05-eu-ambiguous-r1__r01`

- Prompt ID: `p05-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "EU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 58034,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 90: `p05-eu-adversarial-r1__r01`

- Prompt ID: `p05-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a wedding RSVP form with guest details, attendance, plus-one, meal choice, dietary needs, song request, and message. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p05",
  "locale_axis": "EU",
  "prompt_category": "wedding-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 55589,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 91: `p06-au-neutral-r1__r01`

- Prompt ID: `p06-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "AU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 48486,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 92: `p06-au-ambiguous-r1__r01`

- Prompt ID: `p06-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "AU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 61392,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 93: `p06-au-adversarial-r1__r01`

- Prompt ID: `p06-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "AU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 68238,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 94: `p06-nz-neutral-r1__r01`

- Prompt ID: `p06-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "NZ",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 57136,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 95: `p06-nz-ambiguous-r1__r01`

- Prompt ID: `p06-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "NZ",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 18,
  "duration_ms": 66812,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 96: `p06-nz-adversarial-r1__r01`

- Prompt ID: `p06-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "NZ",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 21,
  "duration_ms": 66188,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 97: `p06-uk-neutral-r1__r01`

- Prompt ID: `p06-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "UK",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 38374,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 98: `p06-uk-ambiguous-r1__r01`

- Prompt ID: `p06-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "UK",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 53420,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 99: `p06-uk-adversarial-r1__r01`

- Prompt ID: `p06-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "UK",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 51632,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 100: `p06-us-neutral-r1__r01`

- Prompt ID: `p06-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "US",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 51839,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 101: `p06-us-ambiguous-r1__r01`

- Prompt ID: `p06-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "US",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 21,
  "duration_ms": 56563,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 102: `p06-us-adversarial-r1__r01`

- Prompt ID: `p06-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "US",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 57282,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 103: `p06-intl-online-neutral-r1__r01`

- Prompt ID: `p06-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 19,
  "duration_ms": 54654,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 104: `p06-intl-online-ambiguous-r1__r01`

- Prompt ID: `p06-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 54967,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 105: `p06-intl-online-adversarial-r1__r01`

- Prompt ID: `p06-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 71989,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 106: `p06-eu-neutral-r1__r01`

- Prompt ID: `p06-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "EU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 43265,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 107: `p06-eu-ambiguous-r1__r01`

- Prompt ID: `p06-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "EU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 56298,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 108: `p06-eu-adversarial-r1__r01`

- Prompt ID: `p06-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a volunteer signup form with contact details, availability, skills, emergency contact, and code of conduct acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p06",
  "locale_axis": "EU",
  "prompt_category": "volunteer-signup",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 5,
  "collision_count": 0,
  "component_count": 18,
  "duration_ms": 57911,
  "failure_class": "compiler-fault",
  "input_tokens": 0,
  "output_tokens": 0,
  "retry_count": 0,
  "schema_valid": false,
  "terminal_reason": "compiler-validation-failed",
  "total_cost_usd": 0.0
}
```

### Generated Definition

```json
{
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 109: `p07-au-neutral-r1__r01`

- Prompt ID: `p07-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "AU",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 46698,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 110: `p07-au-ambiguous-r1__r01`

- Prompt ID: `p07-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "AU",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 68363,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 111: `p07-au-adversarial-r1__r01`

- Prompt ID: `p07-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "AU",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 59127,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 112: `p07-nz-neutral-r1__r01`

- Prompt ID: `p07-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "NZ",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 46047,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 113: `p07-nz-ambiguous-r1__r01`

- Prompt ID: `p07-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "NZ",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 47288,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 114: `p07-nz-adversarial-r1__r01`

- Prompt ID: `p07-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "NZ",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 47601,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 115: `p07-uk-neutral-r1__r01`

- Prompt ID: `p07-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "UK",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 45980,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 116: `p07-uk-ambiguous-r1__r01`

- Prompt ID: `p07-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "UK",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 52975,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 117: `p07-uk-adversarial-r1__r01`

- Prompt ID: `p07-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "UK",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 60221,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 118: `p07-us-neutral-r1__r01`

- Prompt ID: `p07-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "US",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 40051,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 119: `p07-us-ambiguous-r1__r01`

- Prompt ID: `p07-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "US",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 48427,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 120: `p07-us-adversarial-r1__r01`

- Prompt ID: `p07-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "US",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 50171,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 121: `p07-intl-online-neutral-r1__r01`

- Prompt ID: `p07-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 40154,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 122: `p07-intl-online-ambiguous-r1__r01`

- Prompt ID: `p07-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 51263,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 123: `p07-intl-online-adversarial-r1__r01`

- Prompt ID: `p07-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 84803,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 124: `p07-eu-neutral-r1__r01`

- Prompt ID: `p07-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "EU",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 48733,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 125: `p07-eu-ambiguous-r1__r01`

- Prompt ID: `p07-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "EU",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 54912,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 126: `p07-eu-adversarial-r1__r01`

- Prompt ID: `p07-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a membership application form with applicant details, membership type, eligibility confirmations, referral source, and terms acknowledgement. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p07",
  "locale_axis": "EU",
  "prompt_category": "membership-application",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 50362,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 127: `p08-au-neutral-r1__r01`

- Prompt ID: `p08-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "AU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 41833,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 128: `p08-au-ambiguous-r1__r01`

- Prompt ID: `p08-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "AU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 39171,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 129: `p08-au-adversarial-r1__r01`

- Prompt ID: `p08-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "AU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 40692,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 130: `p08-nz-neutral-r1__r01`

- Prompt ID: `p08-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "NZ",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 43517,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 131: `p08-nz-ambiguous-r1__r01`

- Prompt ID: `p08-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "NZ",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 38878,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 132: `p08-nz-adversarial-r1__r01`

- Prompt ID: `p08-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "NZ",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 62106,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 133: `p08-uk-neutral-r1__r01`

- Prompt ID: `p08-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "UK",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 48748,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 134: `p08-uk-ambiguous-r1__r01`

- Prompt ID: `p08-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "UK",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 47587,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 135: `p08-uk-adversarial-r1__r01`

- Prompt ID: `p08-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "UK",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 46323,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 136: `p08-us-neutral-r1__r01`

- Prompt ID: `p08-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "US",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 50502,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 137: `p08-us-ambiguous-r1__r01`

- Prompt ID: `p08-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "US",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 48543,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 138: `p08-us-adversarial-r1__r01`

- Prompt ID: `p08-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "US",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 54107,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 139: `p08-intl-online-neutral-r1__r01`

- Prompt ID: `p08-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 43693,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 140: `p08-intl-online-ambiguous-r1__r01`

- Prompt ID: `p08-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 40489,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 141: `p08-intl-online-adversarial-r1__r01`

- Prompt ID: `p08-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 53013,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 142: `p08-eu-neutral-r1__r01`

- Prompt ID: `p08-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "EU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 41222,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 143: `p08-eu-ambiguous-r1__r01`

- Prompt ID: `p08-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "EU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 56201,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 144: `p08-eu-adversarial-r1__r01`

- Prompt ID: `p08-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a trade show booth visit log for collecting lead contact details, company, interest area, buying timeframe, notes, and follow-up consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p08",
  "locale_axis": "EU",
  "prompt_category": "trade-show-lead-log",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 53486,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 145: `p09-au-neutral-r1__r01`

- Prompt ID: `p09-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "AU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 34866,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 146: `p09-au-ambiguous-r1__r01`

- Prompt ID: `p09-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "AU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 51303,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 147: `p09-au-adversarial-r1__r01`

- Prompt ID: `p09-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "AU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 50865,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 148: `p09-nz-neutral-r1__r01`

- Prompt ID: `p09-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "NZ",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 43405,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 149: `p09-nz-ambiguous-r1__r01`

- Prompt ID: `p09-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "NZ",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 6,
  "duration_ms": 56409,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 150: `p09-nz-adversarial-r1__r01`

- Prompt ID: `p09-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "NZ",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 48197,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 151: `p09-uk-neutral-r1__r01`

- Prompt ID: `p09-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "UK",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 37907,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 152: `p09-uk-ambiguous-r1__r01`

- Prompt ID: `p09-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "UK",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 6,
  "duration_ms": 31424,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 153: `p09-uk-adversarial-r1__r01`

- Prompt ID: `p09-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "UK",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 56271,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 154: `p09-us-neutral-r1__r01`

- Prompt ID: `p09-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "US",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 26781,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 155: `p09-us-ambiguous-r1__r01`

- Prompt ID: `p09-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "US",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 41552,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 156: `p09-us-adversarial-r1__r01`

- Prompt ID: `p09-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "US",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 53564,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 157: `p09-intl-online-neutral-r1__r01`

- Prompt ID: `p09-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 6,
  "duration_ms": 28700,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 158: `p09-intl-online-ambiguous-r1__r01`

- Prompt ID: `p09-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 7,
  "duration_ms": 43429,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 159: `p09-intl-online-adversarial-r1__r01`

- Prompt ID: `p09-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 51528,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 160: `p09-eu-neutral-r1__r01`

- Prompt ID: `p09-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "EU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 38258,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 161: `p09-eu-ambiguous-r1__r01`

- Prompt ID: `p09-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "EU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 6,
  "duration_ms": 36047,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 162: `p09-eu-adversarial-r1__r01`

- Prompt ID: `p09-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a newsletter subscription form with name, email, content interests, frequency preference, and marketing consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p09",
  "locale_axis": "EU",
  "prompt_category": "newsletter-subscription",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 57008,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 163: `p10-au-neutral-r1__r01`

- Prompt ID: `p10-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "AU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 48996,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 164: `p10-au-ambiguous-r1__r01`

- Prompt ID: `p10-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "AU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 56846,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 165: `p10-au-adversarial-r1__r01`

- Prompt ID: `p10-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "AU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 55642,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 166: `p10-nz-neutral-r1__r01`

- Prompt ID: `p10-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "NZ",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 50875,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 167: `p10-nz-ambiguous-r1__r01`

- Prompt ID: `p10-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "NZ",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 55516,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 168: `p10-nz-adversarial-r1__r01`

- Prompt ID: `p10-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "NZ",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 55956,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 169: `p10-uk-neutral-r1__r01`

- Prompt ID: `p10-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "UK",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 47405,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 170: `p10-uk-ambiguous-r1__r01`

- Prompt ID: `p10-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "UK",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 60888,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 171: `p10-uk-adversarial-r1__r01`

- Prompt ID: `p10-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "UK",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 62781,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 172: `p10-us-neutral-r1__r01`

- Prompt ID: `p10-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "US",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 50725,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 173: `p10-us-ambiguous-r1__r01`

- Prompt ID: `p10-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "US",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 52435,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 174: `p10-us-adversarial-r1__r01`

- Prompt ID: `p10-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "US",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 50196,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 175: `p10-intl-online-neutral-r1__r01`

- Prompt ID: `p10-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 56522,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 176: `p10-intl-online-ambiguous-r1__r01`

- Prompt ID: `p10-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 64600,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 177: `p10-intl-online-adversarial-r1__r01`

- Prompt ID: `p10-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 51113,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 178: `p10-eu-neutral-r1__r01`

- Prompt ID: `p10-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "EU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 50526,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 179: `p10-eu-ambiguous-r1__r01`

- Prompt ID: `p10-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "EU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 19,
  "duration_ms": 49198,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 180: `p10-eu-adversarial-r1__r01`

- Prompt ID: `p10-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a charity donation pledge form with donor details, amount preference, one-off or recurring intent, receipt details, and campaign updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p10",
  "locale_axis": "EU",
  "prompt_category": "charity-donation-pledge",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 67956,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 181: `p11-au-neutral-r1__r01`

- Prompt ID: `p11-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "AU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 33373,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 182: `p11-au-ambiguous-r1__r01`

- Prompt ID: `p11-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "AU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 44883,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 183: `p11-au-adversarial-r1__r01`

- Prompt ID: `p11-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "AU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 42960,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 184: `p11-nz-neutral-r1__r01`

- Prompt ID: `p11-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "NZ",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 42766,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 185: `p11-nz-ambiguous-r1__r01`

- Prompt ID: `p11-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "NZ",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 40265,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 186: `p11-nz-adversarial-r1__r01`

- Prompt ID: `p11-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "NZ",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 40088,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 187: `p11-uk-neutral-r1__r01`

- Prompt ID: `p11-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "UK",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 34940,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 188: `p11-uk-ambiguous-r1__r01`

- Prompt ID: `p11-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "UK",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 43435,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 189: `p11-uk-adversarial-r1__r01`

- Prompt ID: `p11-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "UK",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 35279,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 190: `p11-us-neutral-r1__r01`

- Prompt ID: `p11-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "US",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 42793,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 191: `p11-us-ambiguous-r1__r01`

- Prompt ID: `p11-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "US",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 40390,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 192: `p11-us-adversarial-r1__r01`

- Prompt ID: `p11-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "US",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 37104,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 193: `p11-intl-online-neutral-r1__r01`

- Prompt ID: `p11-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 39586,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 194: `p11-intl-online-ambiguous-r1__r01`

- Prompt ID: `p11-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 8,
  "duration_ms": 40078,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 195: `p11-intl-online-adversarial-r1__r01`

- Prompt ID: `p11-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 36908,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 196: `p11-eu-neutral-r1__r01`

- Prompt ID: `p11-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "EU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 38046,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 197: `p11-eu-ambiguous-r1__r01`

- Prompt ID: `p11-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "EU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 29385,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 198: `p11-eu-adversarial-r1__r01`

- Prompt ID: `p11-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an international online event registration form with attendee details, country, timezone, session interest, phone, and consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p11",
  "locale_axis": "EU",
  "prompt_category": "intl-online-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 42404,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 199: `p12-au-neutral-r1__r01`

- Prompt ID: `p12-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "AU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 62308,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 200: `p12-au-ambiguous-r1__r01`

- Prompt ID: `p12-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "AU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 41043,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 201: `p12-au-adversarial-r1__r01`

- Prompt ID: `p12-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "AU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 51218,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 202: `p12-nz-neutral-r1__r01`

- Prompt ID: `p12-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "NZ",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 38402,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 203: `p12-nz-ambiguous-r1__r01`

- Prompt ID: `p12-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "NZ",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 50916,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 204: `p12-nz-adversarial-r1__r01`

- Prompt ID: `p12-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "NZ",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 46232,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 205: `p12-uk-neutral-r1__r01`

- Prompt ID: `p12-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "UK",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 37301,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 206: `p12-uk-ambiguous-r1__r01`

- Prompt ID: `p12-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "UK",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 43403,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 207: `p12-uk-adversarial-r1__r01`

- Prompt ID: `p12-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "UK",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 39849,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 208: `p12-us-neutral-r1__r01`

- Prompt ID: `p12-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "US",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 43142,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 209: `p12-us-ambiguous-r1__r01`

- Prompt ID: `p12-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "US",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 59717,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 210: `p12-us-adversarial-r1__r01`

- Prompt ID: `p12-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "US",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 48219,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 211: `p12-intl-online-neutral-r1__r01`

- Prompt ID: `p12-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 38346,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 212: `p12-intl-online-ambiguous-r1__r01`

- Prompt ID: `p12-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 66035,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 213: `p12-intl-online-adversarial-r1__r01`

- Prompt ID: `p12-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 43306,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 214: `p12-eu-neutral-r1__r01`

- Prompt ID: `p12-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "EU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 35932,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 215: `p12-eu-ambiguous-r1__r01`

- Prompt ID: `p12-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "EU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 42599,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 216: `p12-eu-adversarial-r1__r01`

- Prompt ID: `p12-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create an EU event registration form that needs clear GDPR consent, lawful-basis acknowledgement, data handling notice, and contact details. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p12",
  "locale_axis": "EU",
  "prompt_category": "eu-gdpr-event",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 38007,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 217: `p13-au-neutral-r1__r01`

- Prompt ID: `p13-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "AU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 36618,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 218: `p13-au-ambiguous-r1__r01`

- Prompt ID: `p13-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "AU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 47991,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 219: `p13-au-adversarial-r1__r01`

- Prompt ID: `p13-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "AU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 31504,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 220: `p13-nz-neutral-r1__r01`

- Prompt ID: `p13-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "NZ",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 29737,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 221: `p13-nz-ambiguous-r1__r01`

- Prompt ID: `p13-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "NZ",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 35354,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 222: `p13-nz-adversarial-r1__r01`

- Prompt ID: `p13-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "NZ",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 2,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 53488,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 223: `p13-uk-neutral-r1__r01`

- Prompt ID: `p13-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "UK",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 33468,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 224: `p13-uk-ambiguous-r1__r01`

- Prompt ID: `p13-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "UK",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 39367,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 225: `p13-uk-adversarial-r1__r01`

- Prompt ID: `p13-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "UK",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 38975,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 226: `p13-us-neutral-r1__r01`

- Prompt ID: `p13-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "US",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 28036,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 227: `p13-us-ambiguous-r1__r01`

- Prompt ID: `p13-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "US",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 44134,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 228: `p13-us-adversarial-r1__r01`

- Prompt ID: `p13-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "US",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 9,
  "duration_ms": 32265,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 229: `p13-intl-online-neutral-r1__r01`

- Prompt ID: `p13-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 34653,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 230: `p13-intl-online-ambiguous-r1__r01`

- Prompt ID: `p13-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 34176,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 231: `p13-intl-online-adversarial-r1__r01`

- Prompt ID: `p13-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 38527,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 232: `p13-eu-neutral-r1__r01`

- Prompt ID: `p13-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "EU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 37176,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 233: `p13-eu-ambiguous-r1__r01`

- Prompt ID: `p13-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "EU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 38227,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 234: `p13-eu-adversarial-r1__r01`

- Prompt ID: `p13-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a US onboarding interest form. Capture contact details and role, but do not invent SSN or TIN fields unless explicitly required. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p13",
  "locale_axis": "EU",
  "prompt_category": "us-pii-onboarding",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 42474,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 235: `p14-au-neutral-r1__r01`

- Prompt ID: `p14-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "AU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 42109,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 236: `p14-au-ambiguous-r1__r01`

- Prompt ID: `p14-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "AU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 18,
  "duration_ms": 34677,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 237: `p14-au-adversarial-r1__r01`

- Prompt ID: `p14-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "AU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 19,
  "duration_ms": 40732,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 238: `p14-nz-neutral-r1__r01`

- Prompt ID: `p14-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "NZ",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 52114,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 239: `p14-nz-ambiguous-r1__r01`

- Prompt ID: `p14-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "NZ",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 44523,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 240: `p14-nz-adversarial-r1__r01`

- Prompt ID: `p14-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "NZ",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 47277,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 241: `p14-uk-neutral-r1__r01`

- Prompt ID: `p14-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "UK",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 17,
  "duration_ms": 35454,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 242: `p14-uk-ambiguous-r1__r01`

- Prompt ID: `p14-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "UK",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 37290,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 243: `p14-uk-adversarial-r1__r01`

- Prompt ID: `p14-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "UK",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 33892,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 244: `p14-us-neutral-r1__r01`

- Prompt ID: `p14-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "US",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 18,
  "duration_ms": 43516,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 245: `p14-us-ambiguous-r1__r01`

- Prompt ID: `p14-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "US",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 45711,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 246: `p14-us-adversarial-r1__r01`

- Prompt ID: `p14-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "US",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 47756,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 247: `p14-intl-online-neutral-r1__r01`

- Prompt ID: `p14-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 15,
  "duration_ms": 38640,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 248: `p14-intl-online-ambiguous-r1__r01`

- Prompt ID: `p14-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 37036,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 249: `p14-intl-online-adversarial-r1__r01`

- Prompt ID: `p14-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 45514,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 250: `p14-eu-neutral-r1__r01`

- Prompt ID: `p14-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "EU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 16,
  "duration_ms": 37226,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 251: `p14-eu-ambiguous-r1__r01`

- Prompt ID: `p14-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "EU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 21,
  "duration_ms": 63913,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 252: `p14-eu-adversarial-r1__r01`

- Prompt ID: `p14-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a UK NHS-adjacent waiver form with participant details, relevant health notes, consent acknowledgement, and emergency contact. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p14",
  "locale_axis": "EU",
  "prompt_category": "uk-nhs-waiver",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 14,
  "duration_ms": 40897,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 253: `p15-au-neutral-r1__r01`

- Prompt ID: `p15-au-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "AU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 36900,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 254: `p15-au-ambiguous-r1__r01`

- Prompt ID: `p15-au-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. The event is associated with Sydney.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "AU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 54565,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 255: `p15-au-adversarial-r1__r01`

- Prompt ID: `p15-au-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "AU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 44208,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 256: `p15-nz-neutral-r1__r01`

- Prompt ID: `p15-nz-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "NZ",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 45867,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 257: `p15-nz-ambiguous-r1__r01`

- Prompt ID: `p15-nz-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. The event is associated with Auckland.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "NZ",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 54083,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 258: `p15-nz-adversarial-r1__r01`

- Prompt ID: `p15-nz-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "NZ",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 38136,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 259: `p15-uk-neutral-r1__r01`

- Prompt ID: `p15-uk-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "UK",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 10,
  "duration_ms": 29991,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 260: `p15-uk-ambiguous-r1__r01`

- Prompt ID: `p15-uk-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. The event is associated with London.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "UK",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 41671,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 261: `p15-uk-adversarial-r1__r01`

- Prompt ID: `p15-uk-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "UK",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 49217,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 262: `p15-us-neutral-r1__r01`

- Prompt ID: `p15-us-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "US",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 38338,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 263: `p15-us-ambiguous-r1__r01`

- Prompt ID: `p15-us-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. The event is associated with Chicago.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "US",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 37056,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 264: `p15-us-adversarial-r1__r01`

- Prompt ID: `p15-us-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "US",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 44882,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 265: `p15-intl-online-neutral-r1__r01`

- Prompt ID: `p15-intl-online-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 39536,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 266: `p15-intl-online-ambiguous-r1__r01`

- Prompt ID: `p15-intl-online-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. The event is associated with online.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 12,
  "duration_ms": 39426,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 267: `p15-intl-online-adversarial-r1__r01`

- Prompt ID: `p15-intl-online-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "INTL_ONLINE",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 41607,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 268: `p15-eu-neutral-r1__r01`

- Prompt ID: `p15-eu-neutral-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "EU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "neutral"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 34189,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 269: `p15-eu-ambiguous-r1__r01`

- Prompt ID: `p15-eu-ambiguous-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. The event is associated with Berlin.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "EU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "ambiguous"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 11,
  "duration_ms": 50009,
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
  "warning": "generated definition unavailable in local artifacts"
}
```

## Row 270: `p15-eu-adversarial-r1__r01`

- Prompt ID: `p15-eu-adversarial-r1`
- Repetition: `1`
- Variant: `current-master-baseline`
- EvalRunID: `None`
- GenerationRunID: `None`
- Definition source: `unavailable`

### Prompt

Create a New Zealand RSVP form with attendee details, NZ phone, region, dietary requirements, accessibility needs, and event updates consent. Include ZIP code and +1 phone wording even if that conflicts with the audience locale.

### Prompt Metadata

```json
{
  "base_prompt_id": "p15",
  "locale_axis": "EU",
  "prompt_category": "nz-rsvp",
  "schema": "prompts-v1.1",
  "variant": "adversarial"
}
```

### Category A Metrics

```json
{
  "attempt_count": 1,
  "boundary_violation_count": 0,
  "collision_count": 0,
  "component_count": 13,
  "duration_ms": 46681,
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
  "warning": "generated definition unavailable in local artifacts"
}
```
