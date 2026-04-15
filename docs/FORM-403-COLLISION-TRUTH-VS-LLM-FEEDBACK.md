# Form 403: Canvas truth vs LLM collision feedback

This note ties together **measured SmartBorder / canvas geometry** (browser), **server-side collision boxes** used in validation, and **the exact text** the model receives when validation fails.

## 1. Where feedback to the LLM comes from

On each generation attempt, after the model returns JSON, the backend runs (in order):

1. **`validate_definition_payload`** — deterministic schema + `form_validate` collisions (uses `_component_size` from style/props; **no** minimum-height inflation from footprints).
2. **`_merge_guardrail_errors`** — single-page guardrails.
3. **`_merge_visual_boundaries`** — canvas boundary checks using footprint-inflated widths in `_flatten_boundary_visual_components`.
4. **`_merge_visual_collisions`** — merges **`_collect_visual_collisions`** into the validation result (pairwise AABB from `_flatten_collision_visual_components` / `_collision_component_width_height`: **stated width**, **height = max(stated, minimum_render_height)** with optional footprint minimum for height).

If validation is still invalid and retries remain, the next user message is:

```text
_build_correction_message(validation, candidate_definition, runtime_context)
```

Implementation: `backend/modules/form_ai/service.py` — `_build_correction_message`, `_enrich_collision_feedback_lines`, `_collision_pair_hint`.

## 2. How collisions are represented in that message

The correction message always starts with:

```text
Your previous JSON failed validation. Correct it deterministically.
Keep user intent while fixing all errors.
Return only one valid JSON object.
```

Then optional sections:

| Section | Content |
|--------|---------|
| **Schema errors** | `- {path}: {message} ({code})` |
| **Boundary violations** | `- {componentId} on {pageId}: left=…, right=…, top=…, bottom=…` |
| **Collisions** | See below |

### Collisions block

- **Header:** `Collisions:` then one line per `CollisionViolation`.
- **Enriched line** (when the candidate definition is present and both ids resolve in `_flatten_collision_visual_components`):

  ```text
  - `{componentAId}` ({typeA}) box x={xa} y={ya} w={wa} h={ha} vs `{componentBId}` ({typeB}) x={xb} y={yb} w={wb} h={hb} — overlap ~{x_ov}px × {y_ov}px (area={overlapArea}). [optional _collision_pair_hint]
  ```

  Recomputed overlap `x_ov`, `y_ov` is derived from those **same** server boxes (not from SmartBorder).

- **Fallback line** (missing id, or recomputed `x_ov <= 0` or `y_ov <= 0` while the violation still exists):

  ```text
  - {componentAId} overlaps {componentBId} on {pageId} (area={overlapArea})
  ```

- **Optional footer** when `runtime_context.componentFootprints` is a list:

  ```text
  Note: `runtimeContext.componentFootprints` are measured toolbox/canvas hints; collision uses your JSON `position`/`style` plus minimum heights per type. If a field renders taller than `style.height`, increase height or move components below.
  ```

### Pair hints (`_collision_pair_hint`)

After the enriched line, a short deterministic hint may be appended:

- **Same row** (|yA − yB| ≤ 56px and horizontal overlap dominates): suggests narrowing width or moving `position.x` (≥ left + width + 56px) or stacking.
- **Vertical stack** (lower overlaps upper): suggests increasing `position.y` of the lower component (≥ upper y + height + 8px); extra sentence for **textarea + submit-button**.

These hints are **JSON-oriented**, not SmartBorder-oriented.

## 3. Truth table: canvas (measured) vs definition position

Measured on the builder at **desktop 1920×980**, stage scale ≈ **0.715** (viewport-dependent). **Definition position** is the authoritative `(x,y)` from the form JSON; **SmartBorder path AABB** is the SVG path bounding box in **canvas coordinates** (aligned with `component.position` + local path, same idea as `buildCanvasRectsForComponents` + SmartBorder polygon).

| Component id | Definition **(x, y)** | SmartBorder path AABB **(x, y, w, h)** canvas px |
|--------------|------------------------|--------------------------------------------------|
| event-header | (1000, 64) | (1000, 64, 560, 74) |
| event-dates | (1000, 160) | (1000, 160, 560, 110) |
| first-name | (64, 64) | (64, 64, 420, 109) |
| last-name | (524, 64) | (524, 64, 420, 109) |
| address | (64, 192) | (64, 192, 880, 109) |
| phone | (64, 320) | (64, 320, 420, 109) |
| email | (524, 320) | (524, 320, 420, 109) |
| company | (64, 448) | (64, 448, 880, 109) |
| comments | (64, 576) | (64, 576, 720, 269) |
| submit | (64, 832) | (64, 832, 167, 111) approx. |

**Submit** path width is narrower than `style.width` in JSON because SmartBorder wraps **tight** to drawn content; the server collision box uses **stated** width/height from JSON instead, so server and SmartBorder can disagree on **submit** and **textarea** extents.

## 4. Pairwise: canvas / server truth vs what the LLM would read

For each pair, **canvas SmartBorder AABB** shows whether the **rendered** outlines overlap. **Server collision** uses **definition JSON** boxes from `_flatten_collision_visual_components` (not SmartBorder).

| Pair | Overlap on canvas (path AABB)? | Typical server JSON AABB overlap (current rules)? | If this pair appears in `validation.collisions`, LLM sees |
|------|--------------------------------|---------------------------------------------------|---------------------------------------------------------|
| first-name / last-name | **No** (40px horizontal gap) | **No** for 420px-wide row | Enriched line with `w≈420`, `h≈110`, overlap dims + same-row **hint**, *or* fallback if ids/boxes disagree |
| phone / email | **No** | **No** | Same pattern |
| event-dates / last-name | **No** (no horizontal overlap; small vertical band only) | **No** | Enriched or fallback |
| event-header / last-name | **No** | **No** | Enriched or fallback |
| comments / submit | **Possibly** (vertical band; path heights vs y) | **Depends** on stated `style.height` vs min textarea height | Often **vertical** hint; textarea+submit extra sentence |

**Important:** If the list of `CollisionViolation` entries is **empty** for the current candidate, the **`Collisions:`** section is **omitted** entirely — the model only gets schema/boundary sections for those errors.

## 5. Why “false positives” can still show up in the message

1. **Server ≠ SmartBorder** — Feedback is built from **JSON** geometry + min heights, not from measured SmartBorder paths (`_enrich_collision_feedback_lines` uses `_flatten_collision_visual_components` only).
2. **Stale or merged violations** — `_merge_visual_collisions` **adds** visual collisions to `form_validate` collisions; ordering and pairing come from the validator, not from the canvas.
3. **Fallback lines** — If enrichment detects **zero** overlap when re-pairing boxes (`x_ov`/`y_ov` ≤ 0) but the violation is still present, the model sees the short **area=** line only — confusing vs canvas.
4. **Footprints note** — Suggests runtime measurements; collision math does **not** use footprint **width** for collision boxes (width is stated in code comments), but **height** can follow footprint minimums — mixed message for the model.

## 6. Complete review of “response after the LLM” (checklist)

- [ ] Log or inspect **`_build_correction_message`** output for the failing attempt (full string).
- [ ] Compare **`validation.collisions`** to **`_collect_visual_collisions(candidate, runtime_context)`** only — ensure no duplicate or guardrail-only pairs.
- [ ] For each pair, confirm **`_enrich_collision_feedback_lines`** recomputed `x_ov`/`y_ov` > 0; if not, expect **fallback** lines and fix validator/enrichment mismatch.
- [ ] Compare JSON **stated** boxes to **SmartBorder** table above for form 403; align submit/textarea rules if product requires SmartBorder parity.
- [ ] Optionally attach **runtime** `componentFootprints` only where height hints help; avoid implying footprint drives **width** for collisions.

## 7. What `log.ApiRequest` actually sent vs what current code recomputes

This is the **direct** check: parse **`RequestPayload`** on outbound OpenAI calls and compare the **logged** user “correction” message to **`_build_correction_message`** run on the **same** failing candidate JSON with the same **sample** `runtimeContext` (canvas 1920×980 + textarea / first-name / text footprints).

**Inbound correlation ID (example):** `903afb9d-36c5-40ab-a6f2-feaa8ad34596`

| log.ApiRequestID | Logged correction (summary) | Recomputed with **current** `form_ai` + sample `runtimeContext` |
|------------------|------------------------------|-------------------------------------------------------------------|
| **455047** | Boundary: **submit** `bottom=True`. **Collisions:** 5 short lines (`comments`/`submit`, `event-dates`/`last-name`, `event-header`/`last-name`, `first-name`/`last-name`, `phone`/`email`) with areas 2640, 1568, 7056, 8800, 8800. | **Boundary:** submit `bottom=True` (matches). **Collisions:** **none** — `_collect_visual_collisions` returns **0** for that candidate, so the **`Collisions:`** block should **not** appear. |
| **455048** | **Collisions only:** same five pairs (areas 880, 1176, 5292, 11000, 11000). No boundary block in the logged excerpt. | **valid=true** (no schema, boundary, or collision errors) for the **assistant JSON before that correction** — recomputed message is **preamble only**; the **five collision lines in the log are not reproducible** from current validator logic on that definition. |

**Conclusion**

1. **Logged feedback overstated collisions** relative to **current** server geometry for the stored candidates: either the trace was produced with **older collision width/merge rules**, or **`runtimeContext`** at runtime differed from the sample used in the script.
2. The **boundary** warning on **submit** (455047) **does** match recomputation — that part of the feedback is **credible** for the model.
3. The **short** collision lines (`… overlaps … (area=…)`) are the **fallback** shape from `_build_correction_message` when enrichment does not emit the long `x= y= w= h=` lines — they still carry **wrong pairs** if the underlying `CollisionViolation` list is wrong.

**Reproduce locally:**

```text
cd backend
python scripts/compare_logged_llm_feedback_vs_recomputed.py 903afb9d-36c5-40ab-a6f2-feaa8ad34596
```

The script finds the **failing candidate** as the last **assistant** DefinitionJSON **before** the correction **user** message in each outbound payload.

### What to change for accurate, useful LLM feedback

- **Align deployed code** with the branch that uses **stated-width** collision boxes (`_collision_component_width_height`) so logged traces match recomputation.
- **After** validation, assert **`_build_collision_truth_feedback`** recomputed area **matches** `overlapArea` on each pair (or explain mismatch in Notes); drop or flag pairs where `x_ov`/`y_ov` ≤ 0.
- **Do not send** a `Collisions:` section when **`_merge_visual_collisions`** adds nothing and `form_validate` reported none — avoid contradicting canvas/SmartBorder truth.
- Optionally **attach** one line: “Collision checks use DefinitionJSON boxes, not SmartBorder,” when sending footprint `runtimeContext`.

## 8. New collision feedback shape (truth table in the prompt)

The correction message no longer uses only bullet “box x= … overlap ~” lines. It includes:

1. **Layout snapshot** — Markdown table of every component’s collision box (`id`, `type`, `x`, `y`, `width`, `height`) from `_flatten_collision_visual_components` (same as validator).
2. **Reported overlaps** — One table row per `CollisionViolation` with:
   - overlap **W×H** in px (or `0 (no overlap)`),
   - **area (validator)** vs **area (recomputed)**,
   - **Notes**: existing `_collision_pair_hint` text, or `**INCONSISTENT**` when recompute shows no overlap but the validator still reported a pair.

Implementation: `backend/modules/form_ai/service.py` — `_build_collision_truth_feedback`, used from `_build_correction_message`.

### Example (two stacked fields; from `test_story_6_2_collision_correction_includes_geometry_and_hints`)

```text
Collisions:
Collision layout (DefinitionJSON boxes — same math as the validator; not SmartBorder pixels).

Layout snapshot (page page-1):
| id | type | x | y | width | height |
| --- | --- | ---: | ---: | ---: | ---: |
| a | text | 20 | 20 | 300 | 110 |
| b | email | 20 | 80 | 300 | 110 |

Reported overlaps (recompute sanity-check vs validator `overlapArea`):
| A | B | overlap W×H | area (validator) | area (recomputed) | Notes |
| --- | --- | --- | ---: | ---: | --- |
| `a` | `b` | 300×50px | 120 | 15000 | Vertical overlap: set `b.position.y` ... (area mismatch vs validator 120) |
```

Heights are **110** because of minimum render height for `text` / `email`. The **recomputed** area can differ from the **validator** `overlapArea` when sources disagree — the note makes that explicit so the model can prioritize **geometry + hints** over a stale area figure.

This gives the model **full context** to edit JSON without guessing widths, and surfaces **INCONSISTENT** rows when recompute finds zero overlap for a reported pair.

## 9. First-shot tuning CLI uses the same “server” collision definition as this doc

`backend/scripts/form_ai_first_shot_tune.py` calls `generate_form_definition(..., max_system_correction_attempts=0)` and reads **`trace.attempts[0].validation.collisionCount`** from the same merged validation as production generate:

- **`_merge_visual_collisions`** → **`_collect_visual_collisions`** → **`_flatten_collision_visual_components`** (DefinitionJSON `position` + **`_collision_component_width_height`**: stated width, height = max(stated, minimum render height); **not** SmartBorder).

So **`coll` in experiment logs is “FORM-403 server box” truth**, not “looks overlapped on canvas.” If you eyeball the Builder and only **some** server-reported pairs look touching, that matches **§3–§5** (JSON vs SmartBorder path AABB, submit/textarea width/height mismatch, etc.).

**End of each experiment block (recommended):**

1. Take the **best** first-shot run (e.g. highest **combined** or policy: min **bnd** then min **coll**).
2. Save its **`definitionJSON`** to something like  
   `docs/experiments/form-ai-first-shot/artifacts/<experiment-id>-block<N>-best.json`  
   (CLI: `--save-definition` on that winning run; directory may be under the story worktree).
3. **Visual review:** load that JSON into the Form Builder (import / paste into draft) and compare **SmartBorder** outlines to server pairs using `debug_form_ai_collisions.py` on the same file if needed.

Keep this note as the methodology anchor; **do not** overwrite §3’s measured table unless you refresh canvas captures for the same form. Updating the **artifact JSON** per block is how you refresh the **working** layout you inspect—not by deleting §1–§8.

---

*Canvas measurements from DevTools session (login + `/forms/403/builder`); server behavior from `backend/modules/form_ai/service.py`; ApiRequest comparison from `backend/scripts/compare_logged_llm_feedback_vs_recomputed.py` against `log.ApiRequest`.*
