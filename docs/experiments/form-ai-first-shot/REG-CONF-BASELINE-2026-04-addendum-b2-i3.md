Block 2 iteration 3 addendum (single lever: exact footprint math):

Keep first-shot schema-valid output and preserve requested fields/options/submit label exactly.

Use runtime footprint math as strict placement rules for every generated component:
- Set each component `style.width` to the runtime footprint width for that component type.
- Set each component `style.height` to the runtime footprint height for that component type (or higher if needed, never lower).
- Keep a deterministic vertical stack and compute:
  - `next.position.y = current.position.y + current.style.height + current.recommendedGapAfter`
- Use runtime `recommendedGapAfter` per component type; if missing, use 24.
- Keep all components fully within `canvasSettings` bounds and do not overlap.
