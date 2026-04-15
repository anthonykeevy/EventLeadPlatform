# STORY-6.2 AI Context Pack

**Context Pack Version:** 2.0.1  
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

## Changes from v1.1

- **v2.0.1:** Added **textarea + validation band + submit-button** vertical stacking rules so models leave enough space below multi-line fields (reduces bottom-of-form collision retries).
- Bumped to **v2.0** with **default canvas footprints** aligned with frontend `buildAiRuntimeFootprints.ts` (`estimateConfiguredFootprint` + `generateComponent` defaults) — same policy as builder canvas for new drops.
- Documented **toolbox vs canvas**: toolbox tiles use compact surface previews and are **not** 1:1 with canvas placement; use this pack’s footprint table and/or `runtimeContext.componentFootprints` for layout math (not raw toolbox thumbnail pixels).
- Reinforced **`file-upload`** (post‑6.2.2): public attachment **UUIDs** only; `allowMultiple` / `maxFiles` when needed; never paths; honor `acceptedFileTypes` / accept hints.
- Authoritative prop names: **`docs/COMPONENT-FRAMEWORK-GUIDE.md`**.
- Optional pack path override: **`FORM_AI_CONTEXT_PACK_PATH`** in `backend/modules/form_ai/service.py` (default: this file).
- **Benchmark prompts are frozen:** `STORY-6.2-BENCHMARK-FORMS.md` text is the **regression baseline**; quality fixes for vague user wording (labels, width, margins) are made **here in the context pack** only, so harness prompts and scores stay comparable over time.
- **Multi-column rows:** Paired short fields may sit **side-by-side** on wide canvases (see Layout rules) — not limited to a single vertical stack.

---

## Default canvas footprints (builder alignment)

These recommended default `style.width` / `style.height` values match **`frontend/src/features/builder/components/ai/buildAiRuntimeFootprints.ts`** → `estimateConfiguredFootprint`.

Let **W** = `canvasSettings.width` (typical builder **1920**).

| Rule | Value |
|------|--------|
| Typical **default** width for inputs on a wide canvas | width ≈ **48%** of W, **capped at 560** (see `recommendedMaxFootprintWidth` in `buildAiRuntimeFootprints.ts`) |
| `textarea`, `address` | cap **720** (≈52% of W on large canvases) |
| `submit-button` | width = **220**, height = **64** (keep compact — avoids eating bottom canvas margin) |
| `dropdown`, `radio`, `checkbox`, `select` | Add **20 px** height per option **beyond the first 3** |

| Component type | Typical height (px) | Notes |
|----------------|---------------------|--------|
| `text`, `first-name`, `email`, `phone`, `number`, `url`, `date` | 110 | |
| `address` | 120 | |
| `dropdown`, `select`, `radio`, `checkbox` | 120 + option growth | See option rule above |
| `textarea` | **180–280** (use **≥ 200** when a `submit-button` sits directly below) | Builder shows label + control + **validation/error band**; do not use the bare minimum height when stacking submit underneath. |
| `terms` | 120 | |
| `header` | 52 | |
| `paragraph` | 88 | Prefer `text` in props; `label` legacy |
| `divider` | 20 | |
| `rating` | 96 | Set `ratingMax`, `ratingStyle` (`stars` \| `numbers` \| `emoji`) |
| `file-upload` | 132 | Adjust upward for dense multi-file UX |

**Example (W = 1920):** default columns: inputs **~560** wide, `textarea`/**address** up to **720**, submit **220×64**. Full-bleed **1880** only when the user explicitly wants edge-to-edge fields.

**How to use footprints with real `canvasSettings`:** Read `canvasSettings.width` and `canvasSettings.height` from the definition you emit. `runtimeContext.componentFootprints` widths are **recommended planning widths** (capped for readability). Emit `style.width` near those values unless the user clearly asks for full-width fields.

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

### Multi-column rows (pair related short fields — encouraged)

**Do not assume every field must be full-width stacked vertically.** On **wide** canvases (typical builder **≥ ~900px** width), you **should** place **two related, short inputs on the same row** when it matches the user’s intent: same `position.y`, **different** `position.x`, with a **horizontal gap** between boxes (e.g. **56–96px** between the right edge of the left field and the left edge of the right field).

**Good candidates to pair on one row** (when both appear in the prompt):

| Row idea | Left field | Right field |
|---------|------------|-------------|
| Name | `first-name` or “First name” `text` | “Last name” `text` |
| Contact | `phone` | `email` (especially if both required/asked together) |
| Other pairs | Only when both are **short** single-line types (`text`, `phone`, `email`, `number`, `date`, etc.) | |

**Usually keep full row width** (one component per row, or spanning both columns) for:

- `textarea` (comments / long text)
- `address` (often taller / wider)
- `terms`, dense `checkbox` / `radio` lists, `file-upload`, large `dropdown` option sets

**Widths:** Use the **default footprint widths** (e.g. **~560** per column on a 1920 canvas — see table above). **Left column:** `x` near your left margin (e.g. **40–80**). **Right column:** `x` ≈ `left_x + left.width + gap` (e.g. **~680** when left width is 560 and gap ~80). Snap `x` / `y` to **`gridSize`** when present.

**Why this matters:** A single full-width column of many fields consumes **vertical** space quickly; **`textarea` + label/validation chrome + `submit-button`** then compete for the bottom of the canvas and trigger **collision** failures. Pairing short fields **frees vertical space** so submit can sit **clearly below** the textarea.

**Post-process note:** `_rebalance_single_column_vertical_spacing` only runs when **all** components share roughly the **same** `x` (single-column detection). Deliberate **two-column** `x` positions **skip** that rebalance — which is correct: your `y` spacing must already be **collision-safe** (inflate mentally for textarea/submit).

### Textarea, validation band, and `submit-button` (collision-safe stacking)

The automated **collision** check uses each component’s `position`, `style.width`, and **`max(stated height, type minimum)`**. The **builder canvas** also reserves a **validation / error message row** under many controls (visible as grey helper text in edit mode). That row sits **inside the interactive footprint** the human sees, but models often under-state vertical space and place **`submit-button` too high**, so the button overlaps the textarea’s **bottom chrome** — a common **retry‑cap** failure.

**Rules (apply on every generation and correction):**

1. **Treat `textarea` as taller than a single-line field.** For “Comments”, “Message”, or any long text: set `style.height` to **at least 180–240px** (prefer **200+** on busy forms). Wider `textarea` blocks may use up to the **720** width cap from the table above.
2. **Place `submit-button` last** in reading order. Its **`position.y`** must satisfy:  
   `submit.y ≥ textarea.y + textarea.style.height + **48–72px`** (use the **larger** gap when `canvasSettings.height` is tight or many fields are stacked). Do **not** tuck submit into the gap between textarea’s **stated** box and the real validation band — the extra gap absorbs that.
3. **Horizontal overlap:** If submit is **left‑aligned** under a **full‑width** textarea, keep **`submit.position.x`** aligned with the textarea’s **`position.x`** (same column). If submit sits under a **two‑column** layout, align it under the **left** column or span the pair with **full width** — avoid placing submit under **only** the right column when the textarea spans both columns.
4. **If collision feedback mentions the submit + textarea pair:** first **increase vertical gap** and/or **increase `textarea.style.height`**, then nudge **`submit.y` down**; only then shrink widths or change column layout.

### Canvas width, margins, and “full bleed” behaviour

User prompts do **not** control exact pixel widths. You **do** control sizing:

- Always reason from **`canvasSettings.width`** and **`canvasSettings.height`** (they vary by form).
- **Avoid** defaulting every input to ~90–100% of canvas width on **wide** canvases unless the user clearly wants a single full-width column (e.g. “full width fields”, “use the whole canvas”). Prefer a **readable** field width, **symmetric side margins**, and **reserved** horizontal or vertical bands for future content (event blurb, imagery, or whitespace).
- Example on a **wide** canvas: main form column `style.width` roughly **40–55%** of `canvasSettings.width`, `position.x` **2–8%** of width from the left, leaving the remainder for an optional **informational** region or empty margin — adjust when the prompt implies event/RSVP/registration context (see below).
- Narrow canvases (small `width`) may still use most of the horizontal band; keep minimum margins so components validate.

### Compatibility with vertical spacing (post-process)

The pipeline may **rebalance vertical gaps** between components in a detected **single-column** layout so **top** and **bottom** margins are consistent. That step adjusts **`position.y`** (and related height sync) only; it does **not** force maximum `style.width`. **Narrower fields with deliberate side margins** work together with that behaviour — **no conflict**.

### Event-context split layout (optional, when prompt implies it)

For **RSVP**, **registration**, **ticket**, or similar prompts where the organiser may show **event details** beside the form:

- When **`runtimeContext.eventInformation`** is present (builder toggle): you **must** show those facts in at least one **`header`** and/or **`paragraph`** above the fields (name, dates, venue from the object — no invented details).
- On **wide** canvases (`canvasSettings.width` roughly ≥ 900px, scale proportionally if smaller): favour **two regions** expressed in **relative** terms: **left** band ≈ **45–52%** of canvas width for **interactive fields**; **right** band for **read-only** `header` / `paragraph` placeholders (“Event title”, “Date & time”, “Venue”, “Notes”) the human will edit.
- Express placement using **actual** `canvasSettings.width` (e.g. right column `position.x` ≈ **0.50–0.52 × width**, with consistent margins). Do **not** invent real event facts.
- If the user did **not** imply event collateral and asked only for a compact form, a single column with modest width is fine.

### Copy and question clarity (labels without changing user or benchmark prompts)

Benchmark prompts in `STORY-6.2-BENCHMARK-FORMS.md` stay **verbatim** for baseline scoring. Real users may use short or vague phrasing. Improve outcomes with **clearer field labels** and optional `helpText` where supported — **without** contradicting an explicit user instruction.

- **Party / RSVP / guest counts:** If the prompt asks how many people someone is “bringing” or “guests” but does **not** define whether that includes the respondent, prefer an unambiguous label such as **“How many people are you bringing excluding yourself?”** or **“Number of additional guests”**. If the user **explicitly** asks for **total** headcount including themselves, **follow that** instead.
- **Other forms:** Resolve ambiguity in favour of respondents and downstream reporting; do not copy vague source phrases into `label` when a precise industry-standard wording exists.
- When in doubt, match the **intent** of the prompt, not the weakest literal wording.

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
