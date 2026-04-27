# Form AI Judge Input Batch

Run ID: `story-6.4.4.1-ac10-baseline-US`
Benchmark set: `prompts-v1.1`
Rubric version: `rubric_v2`

Use `rubric_v2.md` and return JSON matching `judge-output-template.json`.
Set `judge_model_version` to the exact model/version shown in your Cursor session.
Before assigning scores for each row, identify at least one weakness per row before scoring.
Judge only the anonymised package content below.

## Row 1: `p01-us-neutral-r1__r01`

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

## Row 2: `p01-us-ambiguous-r1__r01`

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

## Row 3: `p01-us-adversarial-r1__r01`

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

## Row 4: `p02-us-neutral-r1__r01`

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

## Row 5: `p02-us-ambiguous-r1__r01`

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

## Row 6: `p02-us-adversarial-r1__r01`

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

## Row 7: `p03-us-neutral-r1__r01`

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

## Row 8: `p03-us-ambiguous-r1__r01`

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

## Row 9: `p03-us-adversarial-r1__r01`

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

## Row 10: `p04-us-neutral-r1__r01`

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

## Row 11: `p04-us-ambiguous-r1__r01`

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

## Row 12: `p04-us-adversarial-r1__r01`

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

## Row 13: `p05-us-neutral-r1__r01`

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

## Row 14: `p05-us-ambiguous-r1__r01`

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

## Row 15: `p05-us-adversarial-r1__r01`

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

## Row 16: `p06-us-neutral-r1__r01`

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

## Row 17: `p06-us-ambiguous-r1__r01`

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

## Row 18: `p06-us-adversarial-r1__r01`

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

## Row 19: `p07-us-neutral-r1__r01`

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

## Row 20: `p07-us-ambiguous-r1__r01`

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

## Row 21: `p07-us-adversarial-r1__r01`

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

## Row 22: `p08-us-neutral-r1__r01`

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

## Row 23: `p08-us-ambiguous-r1__r01`

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

## Row 24: `p08-us-adversarial-r1__r01`

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

## Row 25: `p09-us-neutral-r1__r01`

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

## Row 26: `p09-us-ambiguous-r1__r01`

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

## Row 27: `p09-us-adversarial-r1__r01`

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

## Row 28: `p10-us-neutral-r1__r01`

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

## Row 29: `p10-us-ambiguous-r1__r01`

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

## Row 30: `p10-us-adversarial-r1__r01`

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

## Row 31: `p11-us-neutral-r1__r01`

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

## Row 32: `p11-us-ambiguous-r1__r01`

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

## Row 33: `p11-us-adversarial-r1__r01`

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

## Row 34: `p12-us-neutral-r1__r01`

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

## Row 35: `p12-us-ambiguous-r1__r01`

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

## Row 36: `p12-us-adversarial-r1__r01`

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

## Row 37: `p13-us-neutral-r1__r01`

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

## Row 38: `p13-us-ambiguous-r1__r01`

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

## Row 39: `p13-us-adversarial-r1__r01`

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

## Row 40: `p14-us-neutral-r1__r01`

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

## Row 41: `p14-us-ambiguous-r1__r01`

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

## Row 42: `p14-us-adversarial-r1__r01`

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

## Row 43: `p15-us-neutral-r1__r01`

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

## Row 44: `p15-us-ambiguous-r1__r01`

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

## Row 45: `p15-us-adversarial-r1__r01`

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
