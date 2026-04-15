Block 2 iteration 4 addendum (single lever: authoritative measured footprint sizes):

Use runtime context component footprints as authoritative measured render sizes.
- Do not inflate component width/height above provided runtime footprint values unless required by schema.
- In particular, treat submit button height exactly as provided by runtime footprint.
- Keep a clean registration layout with no overlaps and all components inside canvas bounds.

Output must remain schema-valid JSON only.
