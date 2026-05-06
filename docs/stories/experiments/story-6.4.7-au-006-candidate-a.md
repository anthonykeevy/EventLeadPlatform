# Story 6.4.7 AU-006 Candidate A - Production-Style AU Sections Overlay

Eval-only prompt/context overlay for Story 6.4.7 AU-006.

This candidate tests the production rewrite direction for AU-005: preserve strict AU behaviour and publish-ready polish, but express the guidance as positive base-section rules without spelling out blocked foreign examples.

## Authoritative AU Output Contract

For this experiment, treat `audienceLocale = AU` as the final authority for all generated form copy and component configuration.

The generated JSON must be publishable for an Australian audience:

- Use Australian English and practical, plain-English wording.
- Use Australian phone, date, address, currency, privacy, marketing-message, waiver, and terms conventions whenever those details are needed.
- Use concise Australian address labels, including suburb, state, and postcode fields when address details are requested.
- Use Australian privacy and electronic-message framing for privacy, consent, data handling, event updates, marketing, waivers, terms, and acknowledgements.
- Keep every generated field label, placeholder, help text, option, validation hint, form title, form identifier, consent line, and legal acknowledgement internally consistent with the Australian audience.

## Hard Locale Conflict Rule

If the user prompt asks for a format, jurisdiction, region, public-service reference, phone convention, date pattern, address convention, currency convention, or privacy/legal framework that conflicts with `audienceLocale = AU`, the generated form must silently substitute the Australian equivalent.

This is a hard output constraint:

- Do not echo, quote, contrast, explain, or preserve the conflicting cue in generated copy.
- Do not create parallel local and foreign-format fields unless the user explicitly asks to collect both as user-entered values.
- Preserve the business intent, not the conflicting locale surface form.
- Only preserve a non-Australian value when the field is explicitly collecting a destination, source market, travel route, overseas office, overseas attendee location, or other user-entered external value.
- If a generated option list would require overseas regions or timezones, prefer neutral region/timezone labels unless the user explicitly asks to collect the external location.

Before returning the JSON, verify that no generated copy or identifiers contain foreign-only locale tokens, overseas-only legal/public-service references, non-AU phone examples, non-AU address labels, non-AU date examples, or overseas region names unless the field is explicitly collecting an external value.

## Form Completeness And Validation Guard

Before finalising the JSON, check that the form still covers the user's requested business intent:

- Include every material field group the user asked for, unless it is unsafe or impossible.
- For contact details, attendance, consent, payments, dates, availability, eligibility, emergency contact, membership/application flows, waivers, donations, lead capture, and event-update flows, make required/optional intent explicit through `validationIntent`.
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
