# Story 6.5b - Prompt Equivalence Diff (AC-19 gate artefact)

- Commit: `e1d9fbbd6b67a32317f0ac0e24b09b4f695f8ec5`
- Generated: 2026-05-20 03:01:57Z
- Postures covered: local, heritage, neutral, transcreate
- Audience locale: AU
- User prompt: `Build a contact form for an AU tech conference.`

## Summary

| Posture | A | B | I | G | C |
|---|---|---|---|---|---|
| local | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |
| heritage | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |
| neutral | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |
| transcreate | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL | IDENTICAL |

## Top-level verdict: PASS

## Tony sign-off

- [ ] All in-scope blocks (A, B, C, G, I) report `IDENTICAL` or `WHITESPACE` for every covered posture.
- [ ] No `CONTENT` deltas remain in the in-scope blocks.
- [ ] D_HEADER is allowed to differ only when `_assemble_locale_block` output is content-aware (this is expected; Block D moves into the registry in Story 6.5c).

## Posture: `local`

Inputs:
- audience_locale = `AU`
- brand_heritage_origin = `(none)`
- user_prompt = `Build a contact form for an AU tech conference.`

### Block A - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
You generate an EventLead semantic form plan for Story 6.3.1.
Output a single JSON object only. No markdown or prose.
Return FormSemanticPlan only; do not output any coordinates, pixel widths, x/y positions, style blocks, or final DefinitionJSON.
```

</details>

### Block B - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## CONSENT & LEGAL ACKNOWLEDGEMENTS
| User intent | Component | Required guidance |
|---|---|---|
| Marketing consent, terms acceptance, privacy acknowledgement, data/cookie consent, waiver, release, code-of-conduct or indemnity acknowledgement | ``terms`` | Set ``validationIntent.required = true`` unless explicitly optional. Use company-managed terms when runtime context provides them. |
| Consent text but no company-managed terms | ``terms`` | Keep the acknowledgement sentence in ``label`` or ``props.termsContent``. Do not invent legal URLs or policy content. |
| Interests, preferences, dietary choices, availability, feature toggles or other non-legal multi-select | ``checkbox`` | Treat as ordinary choices, not legal acknowledgement. |
```

</details>

### Block I - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
REQUIRED ROOT KEYS (exact, case-sensitive):
  - semanticPlanVersion: must be the string "1.0" (do NOT use the story number).
  - formId: short slug or id (string).
  - title: form title (string).
  - components: array of component intents (see below).
Do NOT add any other root keys.

EACH COMPONENT (object):
  - componentType (required), label, placeholder, helpText, section, rowGroup,
  - widthIntent: one of "compact" | "half" | "full".
    This is a HINT, not a final width. The deterministic compiler picks
    the actual pixel width from a per-type tier table and may shrink the
    component further (or wrap it onto its own row) so the layout fits
    the canvas. Treat widthIntent as a maximum cap: use "compact" when
    the field's content is short (e.g. zip, age, state code), "full"
    only when you genuinely want the field to span the row.
    Use rowGroup to indicate which fields you'd like packed side-by-side;
    the compiler decides whether they actually fit.
  - options: array of {label,value} for dropdown/radio,
  - validationIntent: an OBJECT (not an array) with any of these boolean/number keys:
      required, email, phone, url, minLength, maxLength, min, max, pattern.
    Example: "validationIntent": { "required": true, "email": true }.
    NEVER emit validationIntent as a list of strings (e.g. ["required","email"]).

Use only Story 6.2/6.3.1 supported component catalog and single-page constraints.

# STORY-6.2 AI Context Pack

**Context Pack Version:** 1.3  
**Last Updated:** 2026-04-02  
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
```

</details>

### Block G - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text

```

</details>

### Block D_HEADER - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## LOCALE AND BRAND POSTURE
Audience locale NEUTRAL. Use clear international English, ISO-friendly formats where useful, avoid country-specific law citations unless the user requests them, and keep field labels globally understandable.
```

</details>

### Block C - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
Brand posture: local. Match copy voice to the resolved audience locale.
```

</details>

## Posture: `heritage`

Inputs:
- audience_locale = `AU`
- brand_heritage_origin = `Australia`
- user_prompt = `Build a contact form for an AU tech conference.`

### Block A - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
You generate an EventLead semantic form plan for Story 6.3.1.
Output a single JSON object only. No markdown or prose.
Return FormSemanticPlan only; do not output any coordinates, pixel widths, x/y positions, style blocks, or final DefinitionJSON.
```

</details>

### Block B - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## CONSENT & LEGAL ACKNOWLEDGEMENTS
| User intent | Component | Required guidance |
|---|---|---|
| Marketing consent, terms acceptance, privacy acknowledgement, data/cookie consent, waiver, release, code-of-conduct or indemnity acknowledgement | ``terms`` | Set ``validationIntent.required = true`` unless explicitly optional. Use company-managed terms when runtime context provides them. |
| Consent text but no company-managed terms | ``terms`` | Keep the acknowledgement sentence in ``label`` or ``props.termsContent``. Do not invent legal URLs or policy content. |
| Interests, preferences, dietary choices, availability, feature toggles or other non-legal multi-select | ``checkbox`` | Treat as ordinary choices, not legal acknowledgement. |
```

</details>

### Block I - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
REQUIRED ROOT KEYS (exact, case-sensitive):
  - semanticPlanVersion: must be the string "1.0" (do NOT use the story number).
  - formId: short slug or id (string).
  - title: form title (string).
  - components: array of component intents (see below).
Do NOT add any other root keys.

EACH COMPONENT (object):
  - componentType (required), label, placeholder, helpText, section, rowGroup,
  - widthIntent: one of "compact" | "half" | "full".
    This is a HINT, not a final width. The deterministic compiler picks
    the actual pixel width from a per-type tier table and may shrink the
    component further (or wrap it onto its own row) so the layout fits
    the canvas. Treat widthIntent as a maximum cap: use "compact" when
    the field's content is short (e.g. zip, age, state code), "full"
    only when you genuinely want the field to span the row.
    Use rowGroup to indicate which fields you'd like packed side-by-side;
    the compiler decides whether they actually fit.
  - options: array of {label,value} for dropdown/radio,
  - validationIntent: an OBJECT (not an array) with any of these boolean/number keys:
      required, email, phone, url, minLength, maxLength, min, max, pattern.
    Example: "validationIntent": { "required": true, "email": true }.
    NEVER emit validationIntent as a list of strings (e.g. ["required","email"]).

Use only Story 6.2/6.3.1 supported component catalog and single-page constraints.

# STORY-6.2 AI Context Pack

**Context Pack Version:** 1.3  
**Last Updated:** 2026-04-02  
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
```

</details>

### Block G - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text

```

</details>

### Block D_HEADER - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## LOCALE AND BRAND POSTURE
Audience locale NEUTRAL. Use clear international English, ISO-friendly formats where useful, avoid country-specific law citations unless the user requests them, and keep field labels globally understandable.
```

</details>

### Block C - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
Brand posture: heritage. Audience locale still controls field shape and compliance; copy voice may lightly reflect Australia brand heritage.
```

</details>

## Posture: `neutral`

Inputs:
- audience_locale = `AU`
- brand_heritage_origin = `(none)`
- user_prompt = `Build a contact form for an AU tech conference.`

### Block A - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
You generate an EventLead semantic form plan for Story 6.3.1.
Output a single JSON object only. No markdown or prose.
Return FormSemanticPlan only; do not output any coordinates, pixel widths, x/y positions, style blocks, or final DefinitionJSON.
```

</details>

### Block B - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## CONSENT & LEGAL ACKNOWLEDGEMENTS
| User intent | Component | Required guidance |
|---|---|---|
| Marketing consent, terms acceptance, privacy acknowledgement, data/cookie consent, waiver, release, code-of-conduct or indemnity acknowledgement | ``terms`` | Set ``validationIntent.required = true`` unless explicitly optional. Use company-managed terms when runtime context provides them. |
| Consent text but no company-managed terms | ``terms`` | Keep the acknowledgement sentence in ``label`` or ``props.termsContent``. Do not invent legal URLs or policy content. |
| Interests, preferences, dietary choices, availability, feature toggles or other non-legal multi-select | ``checkbox`` | Treat as ordinary choices, not legal acknowledgement. |
```

</details>

### Block I - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
REQUIRED ROOT KEYS (exact, case-sensitive):
  - semanticPlanVersion: must be the string "1.0" (do NOT use the story number).
  - formId: short slug or id (string).
  - title: form title (string).
  - components: array of component intents (see below).
Do NOT add any other root keys.

EACH COMPONENT (object):
  - componentType (required), label, placeholder, helpText, section, rowGroup,
  - widthIntent: one of "compact" | "half" | "full".
    This is a HINT, not a final width. The deterministic compiler picks
    the actual pixel width from a per-type tier table and may shrink the
    component further (or wrap it onto its own row) so the layout fits
    the canvas. Treat widthIntent as a maximum cap: use "compact" when
    the field's content is short (e.g. zip, age, state code), "full"
    only when you genuinely want the field to span the row.
    Use rowGroup to indicate which fields you'd like packed side-by-side;
    the compiler decides whether they actually fit.
  - options: array of {label,value} for dropdown/radio,
  - validationIntent: an OBJECT (not an array) with any of these boolean/number keys:
      required, email, phone, url, minLength, maxLength, min, max, pattern.
    Example: "validationIntent": { "required": true, "email": true }.
    NEVER emit validationIntent as a list of strings (e.g. ["required","email"]).

Use only Story 6.2/6.3.1 supported component catalog and single-page constraints.

# STORY-6.2 AI Context Pack

**Context Pack Version:** 1.3  
**Last Updated:** 2026-04-02  
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
```

</details>

### Block G - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text

```

</details>

### Block D_HEADER - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## LOCALE AND BRAND POSTURE
Audience locale NEUTRAL. Use clear international English, ISO-friendly formats where useful, avoid country-specific law citations unless the user requests them, and keep field labels globally understandable.
```

</details>

### Block C - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
Brand posture: neutral. Use market-neutral voice; audience locale still controls field shape and compliance.
```

</details>

## Posture: `transcreate`

Inputs:
- audience_locale = `AU`
- brand_heritage_origin = `(none)`
- user_prompt = `Build a contact form for an AU tech conference.`

### Block A - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
You generate an EventLead semantic form plan for Story 6.3.1.
Output a single JSON object only. No markdown or prose.
Return FormSemanticPlan only; do not output any coordinates, pixel widths, x/y positions, style blocks, or final DefinitionJSON.
```

</details>

### Block B - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## CONSENT & LEGAL ACKNOWLEDGEMENTS
| User intent | Component | Required guidance |
|---|---|---|
| Marketing consent, terms acceptance, privacy acknowledgement, data/cookie consent, waiver, release, code-of-conduct or indemnity acknowledgement | ``terms`` | Set ``validationIntent.required = true`` unless explicitly optional. Use company-managed terms when runtime context provides them. |
| Consent text but no company-managed terms | ``terms`` | Keep the acknowledgement sentence in ``label`` or ``props.termsContent``. Do not invent legal URLs or policy content. |
| Interests, preferences, dietary choices, availability, feature toggles or other non-legal multi-select | ``checkbox`` | Treat as ordinary choices, not legal acknowledgement. |
```

</details>

### Block I - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
REQUIRED ROOT KEYS (exact, case-sensitive):
  - semanticPlanVersion: must be the string "1.0" (do NOT use the story number).
  - formId: short slug or id (string).
  - title: form title (string).
  - components: array of component intents (see below).
Do NOT add any other root keys.

EACH COMPONENT (object):
  - componentType (required), label, placeholder, helpText, section, rowGroup,
  - widthIntent: one of "compact" | "half" | "full".
    This is a HINT, not a final width. The deterministic compiler picks
    the actual pixel width from a per-type tier table and may shrink the
    component further (or wrap it onto its own row) so the layout fits
    the canvas. Treat widthIntent as a maximum cap: use "compact" when
    the field's content is short (e.g. zip, age, state code), "full"
    only when you genuinely want the field to span the row.
    Use rowGroup to indicate which fields you'd like packed side-by-side;
    the compiler decides whether they actually fit.
  - options: array of {label,value} for dropdown/radio,
  - validationIntent: an OBJECT (not an array) with any of these boolean/number keys:
      required, email, phone, url, minLength, maxLength, min, max, pattern.
    Example: "validationIntent": { "required": true, "email": true }.
    NEVER emit validationIntent as a list of strings (e.g. ["required","email"]).

Use only Story 6.2/6.3.1 supported component catalog and single-page constraints.

# STORY-6.2 AI Context Pack

**Context Pack Version:** 1.3  
**Last Updated:** 2026-04-02  
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
```

</details>

### Block G - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text

```

</details>

### Block D_HEADER - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
## LOCALE AND BRAND POSTURE
Audience locale NEUTRAL. Use clear international English, ISO-friendly formats where useful, avoid country-specific law citations unless the user requests them, and keep field labels globally understandable.
```

</details>

### Block C - verdict: IDENTICAL [OK]

Bytes are identical between OLD (literal) and NEW (registry).

<details><summary>OLD == NEW (click to expand)</summary>

```text
Brand posture: transcreate. Adapt copy idiomatically for the audience locale while preserving the user's intent.
```

</details>
