# Form AI Post-Processing Guide

## Purpose

This guide defines the current post-processing workflow in `backend/modules/form_ai/service.py`, what each step does, the risks, and when each step should be enabled for Story 6.3 tuning.

Current pipeline order in `generate_form_definition`:

1. `_extract_json_candidate(...)`
2. `_normalize_display_component_props(...)`
3. `_post_process_generated_definition(...)`
   - internal: heading filtering + tab order normalization
   - internal: `_sync_style_dimensions_into_props(...)`
   - internal: `_rebalance_single_column_vertical_spacing(...)`

---

## Post-Processing Steps

### 1) `_normalize_display_component_props`

- **What it does**
  - Walks all components recursively.
  - For `header` and `paragraph`, if `props.label` is empty and `props.text` exists, copies trimmed `props.text` into `props.label`.
- **Why it exists**
  - Prevents display components from failing builder/renderer expectations when the model outputs text in one property but not the other.
- **Risks**
  - Can mask prompt/schema drift by auto-filling label instead of forcing model correction.
  - If both fields intentionally differ in future UX patterns, this can hide that intent.
- **Enable when**
  - You want robust rendering while prompt quality is still being tuned.
  - You see frequent display-component schema or rendering mismatches.
- **Disable when**
  - You need strict raw-model-output evaluation and want no automatic text normalization.

### 2) `_sync_style_dimensions_into_props`

- **What it does**
  - Copies `style.width` and `style.height` into `props.width` and `props.height` for each component.
  - Normalizes width to `"Npx"` string and height to numeric integer.
- **Why it exists**
  - Keeps duplicated size fields aligned where parts of the stack read from `props` while others read from `style`.
- **Risks**
  - Can overwrite intentionally different values between `style` and `props`.
  - Can make root-cause analysis harder because the final JSON no longer reflects the model's exact field split.
- **Enable when**
  - Builder runtime still depends on `props` dimensions in any rendering, validation, or editing paths.
  - You are stabilizing cross-layer compatibility.
- **Disable when**
  - Contract is fully unified on `style` and you want zero mutation for diagnostics.

### 3) `_rebalance_single_column_vertical_spacing`

- **What it does**
  - Detects probable single-column layouts.
  - Recomputes component heights using footprint/min-height rules.
  - Redistributes `position.y` so components are evenly spaced within canvas height.
  - Writes resulting heights into both `style.height` and `props.height`.
- **Why it exists**
  - Reduces vertical overlaps when model outputs dense/stacked layouts.
  - Produces cleaner first-pass readability for single-column forms.
- **Risks**
  - Alters model-authored y-positions, which can hide prompt improvements/regressions.
  - Even spacing may conflict with intentional grouping rhythm (tight group, larger section gap).
  - Depends on runtime footprint quality; weak footprints can create wrong spacing decisions.
- **Enable when**
  - You prioritize immediate non-overlap readability over strict fidelity to model coordinates.
  - Runtime footprints are trusted and canvas sizing is reliable.
- **Disable when**
  - You are benchmarking raw placement quality from prompt-only changes.
  - You need exact model-vs-render coordinate diagnostics.

---

## Additional Logic Inside `_post_process_generated_definition`

### Heading gating + placeholder filtering

- Removes placeholder `header`/`paragraph` labels and suppresses headers when prompt intent does not request heading/title content.
- **Use when:** controlling noisy decorative output in generic prompts.
- **Risk:** can remove content that user expected if prompt intent detection is too strict.

### Tab order normalization

- Rewrites `props.tabOrder` sequentially from layout order (top-to-bottom, then left-to-right).
- **Use when:** keyboard navigation consistency is required.
- **Risk:** can override deliberate custom tab order from prompt/user intent.

---

## Recommended Enablement Profiles

### Profile A: Prompt Benchmark Mode (recommended for first-shot tuning)

- Keep: `_normalize_display_component_props`
- Disable: `_sync_style_dimensions_into_props`, `_rebalance_single_column_vertical_spacing`, heading filtering
- Keep or disable tab order normalization based on whether tab order is in scope for the benchmark
- **Goal:** measure raw model layout quality with minimal mutation.

### Profile B: UX Stability Mode (recommended for production safety)

- Keep all three steps enabled.
- Keep heading filtering and tab order normalization enabled.
- **Goal:** maximize usable canvas output and keyboard consistency, even when model output is imperfect.

### Profile C: Hybrid Mode (recommended during controlled rollout)

- Keep: `_normalize_display_component_props`, tab order normalization
- Toggle: `_sync_style_dimensions_into_props` only if downstream consumers still require `props` dimensions
- Toggle: `_rebalance_single_column_vertical_spacing` only for known failing prompt classes
- **Goal:** preserve most model intent while preventing common breakages.

---

## Decision Criteria Checklist

Before enabling a post-processing step, confirm:

1. The step fixes a recurring class of failures observed in logs.
2. The step does not hide the metric currently being tuned.
3. The step's mutations are observable in trace/log output.
4. There is at least one test proving expected behavior when the step is on.
5. There is at least one test proving raw behavior when the step is off (if benchmark mode is used).

---

## Suggested Next Improvement

Add per-step feature flags (example: `FORM_AI_PP_NORMALIZE`, `FORM_AI_PP_SYNC_STYLE_PROPS`, `FORM_AI_PP_REBALANCE_SINGLE_COLUMN`) so you can run benchmark and stability modes without code edits.
