# Form AI Post-Processing Guide

## Purpose

This guide documents the active post-processing behavior in `backend/modules/form_ai/service.py`, including what each step does, associated risks, and when to enable or disable it during Story 6.3+ tuning.

Current execution order in `generate_form_definition(...)`:

1. `_extract_json_candidate(...)`
2. `_normalize_display_component_props(...)`
3. `_post_process_generated_definition(...)`
   - heading filtering + prompt intent gating
   - tab-order normalization
   - `_sync_style_dimensions_into_props(...)`
   - `_rebalance_single_column_vertical_spacing(...)`

---

## Active Post-Processing Steps

### 1) `_normalize_display_component_props`

- **Function**
  - Recursively walks generated components.
  - For `header` and `paragraph`, copies `props.text` into `props.label` when `label` is missing/empty.
- **Primary benefit**
  - Prevents render inconsistencies for display components when the model emits text in one field only.
- **Risks**
  - Can hide prompt/schema drift by auto-repairing missing labels.
  - Can obscure intentional text/label divergence if that pattern is introduced later.
- **Enable when**
  - You need resilient rendering while prompt architecture is still unstable.
- **Disable when**
  - You are evaluating strict raw-model compliance with no mutation.

### 2) `_sync_style_dimensions_into_props`

- **Function**
  - Mirrors `style.width` and `style.height` into `props.width` and `props.height`.
  - Normalizes width to pixel string and height to integer.
- **Primary benefit**
  - Keeps size fields consistent for parts of the stack that still read from `props`.
- **Risks**
  - Overwrites intentional differences between `style` and `props`.
  - Makes raw-vs-final diffing harder in diagnostics.
- **Enable when**
  - Any active renderer/editor/validator path still expects `props` dimensions.
- **Disable when**
  - Contract is style-first and you need exact model-output observability.

### 3) `_rebalance_single_column_vertical_spacing`

- **Function**
  - Detects single-column layouts.
  - Recomputes effective component heights from style + minimum footprint rules.
  - Rewrites `position.y` to evenly distribute spacing in available canvas height.
  - Synchronizes resulting height values into `style` and `props`.
- **Primary benefit**
  - Reduces dense-stack overlap for single-column drafts.
  - Improves immediate readability in many first-shot outputs.
- **Risks**
  - Mutates model-authored coordinates; can mask prompt improvements/regressions.
  - Even spacing can conflict with intended visual grouping hierarchy.
  - Quality depends on runtime footprint fidelity.
- **Enable when**
  - UX stability is prioritized over strict model-coordinate fidelity.
- **Disable when**
  - Benchmarking prompt quality and layout logic without backend mutation.

---

## Additional Behavior Inside `_post_process_generated_definition`

### Heading gating and placeholder filtering

- Removes placeholder `header`/`paragraph` entries and suppresses headings when prompt intent does not request title/intro content.
- **Use for:** reducing decorative noise.
- **Risk:** may remove user-expected heading content in ambiguous prompts.

### Deterministic tab-order normalization

- Reassigns `props.tabOrder` in top-to-bottom, then left-to-right order.
- **Use for:** keyboard navigation consistency.
- **Risk:** overrides deliberate custom tab-order intent from prompt/user.

---

## Recommended Operating Modes

### A) Prompt Benchmark Mode (for first-shot tuning)

- Keep: `_normalize_display_component_props`
- Disable: `_sync_style_dimensions_into_props`, `_rebalance_single_column_vertical_spacing`
- Optional: disable heading gating/tab-order normalization if strict raw-output analysis is required
- **Goal:** maximize diagnostic fidelity

### B) UX Stability Mode (for production-facing behavior)

- Keep all active post-processing enabled
- **Goal:** maximize usable drafts and reduce obvious overlap/ordering failures

### C) Hybrid Mode (for controlled rollout)

- Keep: `_normalize_display_component_props`, tab-order normalization
- Conditional: `_sync_style_dimensions_into_props` only if props-based consumers remain
- Conditional: `_rebalance_single_column_vertical_spacing` only for known single-column overlap classes
- **Goal:** balance fidelity with practical safety

---

## Decision Checklist

Before enabling any post-processing step:

1. Confirm it addresses a recurring, measured failure class.
2. Confirm it does not hide the metric currently being tuned.
3. Confirm its mutations are visible in trace/log diagnostics.
4. Confirm there are tests for both enabled and disabled behavior where practical.
5. Confirm rollback is trivial (feature flag or isolated function toggle).

---

## Suggested Follow-up Improvement

Introduce per-step feature flags so benchmark/stability modes can be toggled without code edits:

- `FORM_AI_PP_NORMALIZE_DISPLAY_PROPS`
- `FORM_AI_PP_SYNC_STYLE_TO_PROPS`
- `FORM_AI_PP_REBALANCE_SINGLE_COLUMN`
- `FORM_AI_PP_HEADING_FILTER`
- `FORM_AI_PP_TABORDER_NORMALIZE`
