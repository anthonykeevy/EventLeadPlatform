Block 2 iteration 1 addendum (single lever: minimum component heights):

Keep the successful single-column approach and preserve schema validity:
- Output schema-valid payload only (no malformed JSON, no missing required fields, no extra keys).
- Place all inputs and the country dropdown in one vertical column within canvas bounds, then submit button.
- No component boxes may overlap.

Collision-focused lever for this iteration:
- Use explicit minimum `style.height` values so rendered boxes are not underestimated:
  - text/email/tel inputs: minimum 56
  - select dropdown: minimum 56
  - submit button: minimum 48
- Compute each next component `y` from the previous component bottom + at least 24px gap using those minimum heights.
