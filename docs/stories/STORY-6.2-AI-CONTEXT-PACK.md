# STORY-6.2 AI Context Pack

**Context Pack Version:** 1.1  
**Last Updated:** 2026-03-20  
**Owner:** SM Agent

---

## Purpose

Provide a consistent instruction bundle for the LLM so generated `DefinitionJSON` matches EventLead product behavior, component rules, and validation constraints.

---

## Product Usage Context

1. Users describe a form in natural language.
2. AI generates an initial single-page form definition draft.
3. System validates draft via Story 6.1 validator.
4. If invalid, system sends structured correction instructions and retries.
5. If valid, draft loads into Builder canvas for human refinement.
6. Final save/publish remains in existing manual workflows.

---

## Component Catalog (MVP Set)

Allowed component types for Story 6.2 MVP generation:
- `text`
- `first-name`
- `email`
- `phone`
- `url`
- `number`
- `date`
- `dropdown`
- `checkbox`
- `radio`
- `textarea`
- `address`
- `rating`
- `terms`
- `header`
- `paragraph`
- `divider`
- `submit-button`

Component-specific notes for expanded set:
- `url`: use `validation.url: true`; optional `urlPrefix` and `urlPattern` can be included.
- `rating`: include `ratingMax` (typically 5 or 10) and `ratingStyle` (`stars` | `numbers` | `emoji`).
- `paragraph`: display-only content block (prefer `text`, fallback `label` for legacy compatibility).
- `file-upload`: planned (Story 6.2.2), not available in Story 6.2/6.2.1 generation output.

For each component:
- Must include stable `id`.
- Must include `type`.
- Must include `position` (`x`, `y`) for render placement.
- Should include width/height style hints where relevant.

Disallowed in this story:
- Payment component logic (Story 6.7).
- Multi-page generation orchestration.

---

## Layout and Canvas Rules

1. Single-page only.
2. Components must stay within canvas boundaries.
3. Components must not overlap.
4. Prefer top-to-bottom reading flow with reasonable spacing.
5. Keep layout simple and editable by humans after load.

---

## Strict Output Contract (JSON Only)

LLM output requirements:
1. Return valid JSON object only.
2. Do not include markdown, prose, comments, or code fences.
3. Root must be a DefinitionJSON-compatible object.
4. Maintain deterministic key/value structure where practical.

---

## Validator Feedback to Correction Mapping

When validator returns errors:
1. `schemaErrors`:
   - fix missing/incorrect required fields and types.
2. `boundaryViolations`:
   - reposition or resize affected components inside canvas.
3. `collisions`:
   - re-space components to remove overlap while preserving intent.
4. Re-submit corrected JSON for validation until:
   - `valid=true`, or
   - max retries reached.

Correction priorities:
1. Schema correctness
2. Boundary correctness
3. Collision removal
4. Visual readability improvements

---

## Example A (Valid Generation)

```json
{
  "schemaVersion": "1.0",
  "formId": "gen-contact-form",
  "canvasSettings": { "width": 500, "height": 700, "gridSize": 8 },
  "pages": [
    {
      "id": "page-1",
      "title": "Contact Form",
      "components": [
        { "id": "h1", "type": "header", "props": { "text": "Contact Us" }, "position": { "x": 20, "y": 20 }, "style": { "width": 460, "height": 48 } },
        { "id": "name", "type": "text", "props": { "label": "Full Name" }, "position": { "x": 20, "y": 90 }, "style": { "width": 460, "height": 72 } },
        { "id": "email", "type": "email", "props": { "label": "Email" }, "position": { "x": 20, "y": 180 }, "style": { "width": 460, "height": 72 } },
        { "id": "submit", "type": "submit-button", "props": { "label": "Submit" }, "position": { "x": 20, "y": 280 }, "style": { "width": 180, "height": 56 } }
      ]
    }
  ]
}
```

---

## Example B (Invalid -> Corrected)

### Invalid Candidate (collision + boundary)

```json
{
  "schemaVersion": "1.0",
  "formId": "gen-invalid",
  "canvasSettings": { "width": 500, "height": 400, "gridSize": 8 },
  "pages": [
    {
      "id": "page-1",
      "title": "Broken Layout",
      "components": [
        { "id": "a", "type": "text", "props": { "label": "A" }, "position": { "x": -10, "y": 20 }, "style": { "width": 300, "height": 72 } },
        { "id": "b", "type": "email", "props": { "label": "B" }, "position": { "x": 100, "y": 40 }, "style": { "width": 320, "height": 72 } }
      ]
    }
  ]
}
```

### Corrected Candidate

```json
{
  "schemaVersion": "1.0",
  "formId": "gen-invalid",
  "canvasSettings": { "width": 500, "height": 400, "gridSize": 8 },
  "pages": [
    {
      "id": "page-1",
      "title": "Broken Layout",
      "components": [
        { "id": "a", "type": "text", "props": { "label": "A" }, "position": { "x": 20, "y": 20 }, "style": { "width": 460, "height": 72 } },
        { "id": "b", "type": "email", "props": { "label": "B" }, "position": { "x": 20, "y": 110 }, "style": { "width": 460, "height": 72 } }
      ]
    }
  ]
}
```

---

## Operational Notes

1. Provider credentials (for example `OPENAI_API_KEY`) are loaded from local environment only.
2. Never log or return provider secrets.
3. Keep this context pack versioned and update when component contracts evolve.
