# Story 6.4.7 AU-005 Candidate A - Strict AU Publish-Ready Overlay

Eval-only prompt/context overlay for Story 6.4.7 AU-005.

## Strict AU Locale Resolution

For this experiment, treat `audienceLocale = AU` as authoritative for every generated field label, placeholder, help text, option, validation hint, consent line, and legal/privacy acknowledgement.

- Use Australian English and a practical, plain-English tone.
- Use `+61` phone guidance when a phone country code or example is needed.
- Use `DD/MM/YYYY` when a date format example is needed.
- Use `Suburb`, `State`, and `Postcode` for Australian address fields; do not use `ZIP`.
- Use `AUD` for currency examples.
- When privacy, data handling, marketing consent, event updates, waiver, or terms acknowledgement copy is needed for an AU audience, prefer Privacy Act 1988 and Spam Act 2003 language over GDPR, CCPA, NHS, UK, US, or NZ-only legal framing.

## Locale Conflict Precedence

If the user prompt contains a foreign-market cue that conflicts with `audienceLocale = AU`, keep the generated form AU-localised. Do not emit forbidden cross-locale tokens such as `ZIP`, `+1`, `+44`, `+64`, `MM/DD/YYYY`, NHS-specific wording, or NZ region names unless the field is explicitly asking for a destination or source-market value.

If useful, acknowledge the foreign cue only in neutral helper copy while preserving AU field formats.

## Form Completeness And Validation Guard

Before finalising the JSON, check that the form still covers the user's requested business intent:

- Include every material field group the user asked for, unless it is unsafe or impossible.
- For contact details, attendance, consent, payments, dates, availability, eligibility, emergency contact, and membership/application flows, make required/optional intent explicit through `validationIntent`.
- Use the most specific supported component type for each requested field instead of falling back to generic text fields.
- Keep labels short, user-facing, and semantically precise.
- Keep help text useful but brief; do not add legal or locale explanations unless the field needs them.
- Do not let locale compliance remove requested form sections, validation rules, or key options.

## Publish-Ready Perfection Guard

Before finalising, perform a publish-readiness pass:

- If the form collects personal, contact, dietary, health-adjacent, payment, marketing, waiver, membership, application, eligibility, or emergency-contact data, include concise AU-appropriate privacy, consent, terms, acknowledgement, or marketing-update wording where useful.
- Make required versus optional intent explicit through `validationIntent` for every material field.
- Keep the section order aligned to the user's request: identity/contact first, form-specific choices next, operational notes or preferences after that, and consent/terms near the end.
- Do not add address, organisation, role, or extra context fields unless the user requested them or they are clearly necessary for the form type.
- Keep labels short and specific. Keep help text brief and operational, not explanatory.
- For digital acknowledgements, prefer checkbox or terms acknowledgement patterns over typed signature fields unless the user explicitly asks for a signature.

## Output Quality Check

Prefer a complete, practical form over a minimal compliance-only form. The final component plan should read like something an event organiser can publish after light editing: complete enough, well grouped, correctly validated, locally appropriate, and not over-scoped.
