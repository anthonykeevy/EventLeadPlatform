# STORY-6.3 AI Context Pack

**Context Pack Version:** 0.1.1  
**Prompt Section Profile Version:** v1.0.1  
**Last Updated:** 2026-04-04  
**Owner:** Form AI benchmark team

---

## Purpose

Provide a sectioned prompt architecture for Story 6.3 runs while preserving Story 6.2 generation behavior as the baseline contract.

This pack is designed to be layered on top of:

- `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` (baseline contract)

---

## Section contract (v1.0.1)

The section order is fixed for deterministic runs:

1. `layout`
2. `data_collection`
3. `validation_rules`
4. `appearance`
5. `logic`
6. `delivery_summary`

Each section must define:

- `objective`: one sentence
- `instructions[]`: specific, testable constraints
- no overlap across unrelated concerns

---

## Scope by section

### 1) Layout
- Canvas geometry, no-overlap, no-boundary violations
- Uses runtime footprints and closed-control geometry assumptions
- Primary metrics: `coll`, `bnd`, `L`

### 2) Data Collection
- Field list completeness, labels/placeholders, required flags, options, export naming, tab order
- Primary metrics: goal coverage for requested fields/options

### 3) Validation Rules
- Type-appropriate validation objects/messages
- Schema-safe keys only
- Primary metrics: schema-validity + validation issue counts

### 4) Appearance
- Respect locked globals and readable dimensions/spacing
- Avoid style regressions that impact layout
- Primary metrics: visual parity checks + layout side effects

### 5) Logic
- Minimal valid logic rules with stable source/target ids
- Primary metrics: rule validity and runtime sanity

### 6) Delivery Summary
- Output contract guardrails: DefinitionJSON only, deterministic structure
- `tabOrder` may appear only at `component.props.tabOrder` (never top-level on component)
- Primary metrics: parse success + schema validity

---

## Canonical section prompt payload (v1.0.1)

This is the exact section context that is concatenated and sent as `systemPromptAddendum` with the user prompt.

### Section 1: `layout` (Canvas Layout)

**Objective:** Place components on canvas with no overlap and no boundary violations.

**Instructions:**
- Use runtimeContext.componentFootprints as authoritative geometry when provided.
- Treat dropdown/select as closed controls for placement geometry.
- Keep all components within canvasSettings width and height bounds.
- Use deterministic vertical rhythm and spacing with readable row flow.

### Section 2: `data_collection` (Data Collection)

**Objective:** Capture requested fields and options with stable structure.

**Instructions:**
- Include all requested inputs with deterministic ids and labels.
- Set required flags, placeholders, and option lists where relevant.
- Assign tabOrder in visual reading order.
- Use component types that best match user intent.

### Section 3: `validation_rules` (Validation Rules)

**Objective:** Apply clear validation contract per input type.

**Instructions:**
- Use validation keys compatible with Story 6.2 schema.
- Apply required, email, phone, url, and length constraints where implied.
- Keep validation messages concise and user-friendly.
- Never emit unsupported keys.

### Section 4: `appearance` (Appearance Typography Colors)

**Objective:** Preserve readability while respecting locked globals and framework defaults.

**Instructions:**
- Respect runtimeContext.lockedGlobals for theme/globalStyles/canvasSettings.
- Prefer framework-consistent default dimensions over inflated widths.
- Keep styles editable in builder after generation.
- Maintain toolbox/canvas/runtime parity assumptions.

### Section 5: `logic` (Logic Rules)

**Objective:** Add only necessary logic with valid references.

**Instructions:**
- Add logic only when user asks or behavior clearly requires it.
- Ensure sourceComponentId and targetComponentId exist and are different.
- Use valid operator/action pairs.
- Keep rule set minimal and deterministic.

### Section 6: `delivery_summary` (Delivery Summary)

**Objective:** Guarantee parseable deterministic JSON output.

**Instructions:**
- Return a single DefinitionJSON object only.
- Place tabOrder only inside component.props.tabOrder, never as component.tabOrder.
- Do not include markdown, prose, or code fences.
- Prioritize schema validity first, then layout quality.

---

## Sections that affect layout outcomes

Layout quality (`coll`, `bnd`, `L`) is driven by more than one section.

### Direct layout sections

- `layout` (**primary direct impact**)
  - Placement rules, no-overlap intent, canvas bounds, spacing rhythm.
- `appearance` (**direct geometric impact**)
  - Width/height guidance and footprint consistency influence collision geometry.

### Indirect layout sections

- `data_collection` (**indirect but strong impact**)
  - Missing/extra fields, ordering, and component choice alter row density and collision risk.
- `validation_rules` (**indirect impact**)
  - Validation/help content can change effective rendered height.
- `delivery_summary` (**indirect safety impact**)
  - Schema correctness prevents malformed structures that can create misleading layout validation.
- `logic` (**low immediate impact in first-shot visual layout**)
  - Mostly runtime behavior; limited effect on static placement unless logic-specific objects are introduced.

### Practical interpretation for iterations

- If `coll`/`bnd` regress with same prompt, check in order:
  1. `layout`
  2. `appearance`
  3. `data_collection`
- Keep one lever per iteration, but evaluate all six sections after every run.

---

## Iteration workflow (control chat protocol)

For each iteration:

1. Agree one lever/change before running.
2. Run from Builder AI Agent panel (frontend).
3. Use retry count = `0` for first-shot baseline section evaluation.
4. Capture and review all section events:
   - `ai.sections.run.start`
   - `ai.sections.run.result`
   - `ai.sections.run.error`
5. Evaluate all sections each run to detect cross-section regressions.

---

## Versioning and change tracking

- Bump **Prompt Section Profile Version** for section instruction changes.
- Bump **Context Pack Version** for broader pack-level updates.
- Log both versions in run metadata/events where possible.
- Keep one-change-per-iteration discipline to preserve attribution.

---

## Activation

To activate this Story 6.3 pack in backend experiments, set:

- `FORM_AI_CONTEXT_PACK_PATH=docs/stories/STORY-6.3-AI-CONTEXT-PACK.md`

If unset, backend default remains Story 6.2 context pack.

