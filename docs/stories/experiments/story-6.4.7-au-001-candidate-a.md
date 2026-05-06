# Story 6.4.7 AU-001 Candidate A - Strict AU Locale Overlay

Eval-only prompt/context overlay for Story 6.4.7 AU-001.

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
