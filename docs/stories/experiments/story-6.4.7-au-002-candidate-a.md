# Story 6.4.7 AU-002 Candidate A - Clean AU Builder Quality Overlay

Eval-only prompt/context overlay for Story 6.4.7 AU-002.

## Authoritative AU Audience Context

For this experiment, treat `audienceLocale = AU` as the authoritative audience context for generated labels, placeholders, help text, options, validation hints, consent copy, and legal acknowledgements.

- Use Australian English with practical, plain-English wording.
- Use Australian phone, date, address, currency, privacy, and electronic-message conventions whenever those details are needed.
- Keep the generated form internally consistent with an Australian audience, even when the user's subject matter mentions another market or jurisdiction.
- If the user asks for a non-Australian format or market-specific cue that conflicts with the resolved audience, do not create parallel foreign-format fields. Preserve the user's business intent using Australian audience conventions.

## Form Completeness And Validation Guard

Before finalising the JSON, check that the form still covers the user's requested business intent:

- Include every material field group the user asked for, unless it is unsafe or impossible.
- For contact details, attendance, consent, payments, dates, availability, eligibility, emergency contact, and membership/application flows, make required/optional intent explicit through `validationIntent`.
- Use the most specific supported component type for each requested field instead of falling back to generic text fields.
- Keep labels short, user-facing, and semantically precise.
- Keep help text useful but brief; do not add legal or locale explanations unless the field needs them.
- Do not let locale compliance remove requested form sections, validation rules, or key options.

## Output Quality Check

Prefer a complete, practical form over a minimal compliance-only form. The final component plan should read like something an event organiser can publish after light editing: complete enough, well grouped, correctly validated, and locally appropriate.
