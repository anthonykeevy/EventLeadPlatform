> **Documentation only - runtime source moved 2026-05-20 (Story 6.5b)**
>
> This file is preserved for reference. The runtime source for the AI form-generation
> few-shot context pack (Block G in the prompt assembly tree) is now
> `config.PromptSectionVariant` seeded by migration `081_story_6_5b_seed_block_g_context_pack.py`
> against registry `FORM_AI_V1`. Update the registry via a new
> `PromptSectionVariant` row (or a new `PromptAssemblyRegistryVersion`); do **not** edit this file
> expecting a runtime effect. See `docs/architecture/prompt-assembly-registry-architecture.md`
> for the architecture and `docs/stories/story-6.5b.md` for the migration history.
>
> **R6 closure:** moving Block G to the registry eliminates the on-disk file
> read in `service.py::_load_context_pack` that caused the
> `context-pack-load-failed` failure on the deployed Test environment.

# STORY-6.2 AI Context Pack

**Context Pack Version:** 1.3  
**Last Updated:** 2026-04-02  
**Owner:** SM Agent  
**Runtime status (post-Story-6.5b):** _Documentation only._ Runtime source is `config.PromptSectionVariant` (variant `DEFAULT` for `SectionCode='G'` under registry `FORM_AI_V1`).

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
- `file-upload`
- `terms`
- `header`
- `paragraph`
- `divider`
- `submit-button`

Component-specific notes for expanded set:
- `url`: use `validation.url: true`; optional `urlPrefix` and `urlPattern` can be included.
- `rating`: include `ratingMax` (typically 5 or 10) and `ratingStyle` (`stars` | `numbers` | `emoji`).
- `paragraph`: display-only content block (prefer `text`, fallback `label` for legacy compatibility).
- `file-upload`: **available** (Story 6.2.2). Use `allowMultiple` / `maxFiles` only when multiple files in one control are required; answers store **public attachment UUIDs** only (never paths). Generation must respect max size and `accept` / `acceptedFileTypes` hints.

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
4. Prefer top-to-bottom **reading order** with reasonable spacing (rows still read top → bottom).
5. Keep layout simple and editable by humans after load.
6. **Multi-column rows (encouraged on wide canvases):** You **may and should** place **two related short inputs on the same horizontal row** when the user lists them as separate fields — same `position.y`, different `position.x`, each with roughly **half** the main form width (minus a **gap** of about **56–96px** between fields). Typical pairs: **First name | Last name**, **Phone | Email**. Keep **full-width rows** for `textarea`, `address`, and other tall/wide controls. This uses horizontal space, **saves vertical space**, and helps keep **`submit-button` clearly below** `textarea` so collision validation passes. On narrow canvases or when the user asks for one column, a single stack is fine.
7. **`textarea` + `submit-button` (bottom of form):** The builder reserves a **validation / error message band** under controls. Do **not** rely on a minimal `style.height` (~140px) for comments when a submit sits below — use **`style.height` ≥ 180–240px** (prefer **200+**). Place **`submit-button` last** with **`position.y` ≥ `textarea.y + textarea.style.height + 48–72px`**. If corrections still report collisions between submit and textarea, **increase that gap** and/or **textarea height** before changing column layout.

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
