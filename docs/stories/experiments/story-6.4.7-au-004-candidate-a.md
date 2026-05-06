# Story 6.4.7 AU-004 Candidate A - Clean Strict AU Builder Overlay

Eval-only prompt/context overlay for Story 6.4.7 AU-004.

## Authoritative AU Locale Resolution

For this experiment, treat `audienceLocale = AU` as authoritative for every generated field label, placeholder, help text, option, validation hint, consent line, and legal/privacy acknowledgement.

- Use Australian English and a practical, plain-English tone.
- Use Australian phone, date, address, currency, privacy, and electronic-message conventions whenever those details are needed.
- Use concise Australian address labels, including suburb, state, and postcode fields when address details are requested.
- When privacy, data handling, marketing consent, event updates, waiver, or terms acknowledgement copy is needed for an AU audience, use Australian privacy and electronic-message framing.

## Silent AU Substitution

If the user prompt contains a market, jurisdiction, format, legal, regional, phone, date, address, or currency cue that conflicts with `audienceLocale = AU`, silently produce the Australian equivalent in the generated form.

- Do not repeat, quote, contrast, or explain the conflicting cue in labels, placeholders, help text, validation hints, options, consent copy, or legal acknowledgements.
- Preserve the user's business intent using Australian audience conventions.
- Only preserve a non-Australian value when the field is explicitly collecting a destination, source market, travel route, overseas office, or other user-entered external value.
- Avoid parallel duplicate fields for both local and external conventions unless the user explicitly asks to collect both.

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
