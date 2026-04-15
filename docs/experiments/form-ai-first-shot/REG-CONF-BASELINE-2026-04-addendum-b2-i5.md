Block 2 iteration 5 addendum (single lever: rendered-block spacing safety margin):

Layout must avoid overlap using each component's full rendered block footprint, not just control height.

Rules:
- Treat each component as a full rectangle: label + control + validation/helper area + shell padding.
- Vertical placement for stacked components:
  `next.position.y >= current.position.y + current.style.height + 40`
- Horizontal placement for side-by-side components:
  `right.position.x >= left.position.x + left.style.width + 56`
- Submit-button clearance rule:
  reserve at least +56px below submit-button before any next component.
- Keep all components fully within canvas bounds.
- Output schema-valid JSON only.
