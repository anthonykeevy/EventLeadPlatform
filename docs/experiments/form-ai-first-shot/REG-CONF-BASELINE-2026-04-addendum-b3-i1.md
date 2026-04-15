Block 3 iteration 1 addendum (single lever: dropdown auto-width semantics):

Dropdown width behavior rule (important):
- For `dropdown` / `select`, the visible control auto-sizes to the widest option label (plus control padding and arrow chrome).
- Do NOT assume dropdown control width equals component full-row width.
- Keep dropdown component width conservative and near control width unless explicitly required wider by layout.
- For overlap planning, treat dropdown visual width as "widest-option width + chrome", not full two-column span.
- When placing nearby components, reserve horizontal spacing from that visual dropdown width.

Concrete generation rule:
- If dropdown appears in a full-row section, set dropdown `style.width` to computed control width (or computed width + 24px buffer), not the entire row width.

Output schema-valid JSON only and keep components within canvas bounds.
