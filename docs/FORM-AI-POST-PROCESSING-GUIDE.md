# Form AI Post-Processing Guide

## Purpose

This guide defines the current post-processing workflow in `backend/modules/form_ai/service.py`, what each step does, the risks, and when each step should be enabled for Story 6.3 tuning.

Current compiler-first pipeline order in `generate_form_definition`:

1. `_extract_json_candidate(...)`
2. semantic plan extraction/validation (`_extract_semantic_plan_candidate(...)`)
3. deterministic compile (`compile_semantic_plan_to_definition(...)`)
4. `_normalize_display_component_props(...)`
5. `_post_process_generated_definition(...)`
   - internal: heading filtering + tab order normalization
   - internal: `_sync_style_dimensions_into_props(...)`
   - internal: `_rebalance_single_column_vertical_spacing(...)`

Notes:
- The LLM no longer owns final coordinates in the runtime path.
- Post-processing is now compatibility/finalization logic after deterministic compile, not a primary layout generator.

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

## Per-step feature flags (Story 6.3.1)

The post-processing pipeline now exposes four boolean env flags. They are read on every call to `_post_process_generated_definition` and surfaced in `compileSummary.postProcessingApplied` for trace visibility (AC-3).

| Env var | Controls | Default in `deterministic-grid` | Default in `legacy` |
|---------|----------|---------------------------------|---------------------|
| `FORM_AI_PP_HEADING_FILTER` | Heading gating + placeholder text filter | `true` | `true` |
| `FORM_AI_PP_TAB_ORDER` | Sequential tab-order rewrite from layout | `true` | `true` |
| `FORM_AI_PP_SYNC_STYLE_PROPS` | `_sync_style_dimensions_into_props` (copies `style.width/height` into `props`) | `false` | `true` |
| `FORM_AI_PP_REBALANCE` | `_rebalance_single_column_vertical_spacing` (rewrites `position.y` and heights) | `false` | `true` |

Truthy values: `1`, `true`, `yes`, `on`. Falsy values: `0`, `false`, `no`, `off`. Anything else (including unset) uses the per-mode default.

The destructive geometry transforms (`SYNC_STYLE_PROPS`, `REBALANCE`) default OFF in the deterministic-grid path so the compiler stays the single owner of layout. They remain ON in the legacy fallback path so pre-Story-6.3.1 generations keep their previous behaviour.

`_normalize_display_component_props` is non-destructive (only fills missing `props.label` from `props.text` for header/paragraph) and runs unconditionally.

### Profile recipes

| Profile | Env settings |
|---------|--------------|
| **A — Prompt benchmark mode** | `FORM_AI_PP_SYNC_STYLE_PROPS=false`, `FORM_AI_PP_REBALANCE=false` (already the default for deterministic-grid) |
| **B — UX stability mode** | `FORM_AI_PP_SYNC_STYLE_PROPS=true`, `FORM_AI_PP_REBALANCE=true` (forces all mutations even in deterministic-grid) |
| **C — Hybrid mode** | `FORM_AI_PP_SYNC_STYLE_PROPS=true`, `FORM_AI_PP_REBALANCE=false` |

---

## Failure modes (Story 6.3.1)

The form-AI generation pipeline now runs as five explicit phases. Each phase has its own failure handling so that LLM-fault outcomes (the model emitted something we asked it to fix) are never confused with compiler-fault outcomes (our deterministic pipeline produced an invalid definition).

```
[provider] -> [json-parse] -> [semantic-plan] -> [semantic-rules gate] -> [compile + post-process] -> [compile-validation self-check]
```

LLM-fault stages (`json-parse`, `semantic-plan`, `semantic-rules`) feed a phase-specific correction message back to the model and burn one of the `max_system_correction_attempts` (default 3, capped at 10). When the cap is exhausted, the run terminates with the corresponding `terminalReason`.

Compiler-fault stages (`compile`, `compile-validation`) **never feed back to the LLM**: the model cannot fix geometry it did not produce. The run terminates immediately and the draft (when available) is returned so the user/ops can inspect it on the canvas.

| `terminalReason` | Phase | `failureClass` | LLM correction? | Surface |
|------------------|-------|----------------|-----------------|---------|
| `validated-success` | (none — happy path) | `none` | n/a | `definitionJSON` populated, `status="completed"` |
| `provider-error` | provider call (httpx / OpenAI SDK) | `provider-fault` | no | retains last good draft if any |
| `context-pack-load-failed` | startup (context pack file missing) | `infrastructure-fault` | no | no attempts recorded |
| `json-parse-failed` | LLM output is not parseable JSON | `llm-fault` | yes (until cap) | `attempts[].failedAt="json-parse"`, `compileDiagnostics.jsonParseError` |
| `semantic-plan-invalid` | JSON parses but does not match `FormSemanticPlan` (Pydantic shape) | `llm-fault` | yes (until cap) | `attempts[].failedAt="semantic-plan"`, `compileDiagnostics.semanticPlanError` |
| `semantic-rules-violated` | Plan parses but the policy gate found rule violations (unknown component type, disallowed widthIntent, missing options, invalid validation rule, duplicate componentId) | `llm-fault` | yes (until cap) | `attempts[].failedAt="semantic-rules"`, `compileDiagnostics.semanticGateViolations`, `trace.semanticValidationViolations` |
| `compiler-error` | Exception in `compile_semantic_plan_to_definition` or `_post_process_generated_definition`; OR the compiler dropped a component the gate said was clean | `compiler-fault` | **never** | `attempts[].failedAt="compile"`, `compileDiagnostics.compilerError`, `compileSummary.droppedComponentReasons` (when applicable) |
| `compiler-validation-failed` | `validate_definition_payload` (schema + visual collisions/boundaries) reports invalid output | `compiler-fault` | **never** | `attempts[].failedAt="compile-validation"`, draft returned for inspection |
| `retry-cap-exhausted` | LLM-fault correction loop ran out of attempts at the semantic-rules gate | `llm-fault` | already exhausted | last attempt's diagnostics |
| `first-shot-invalid` | `max_system_correction_attempts=0` and the first attempt failed an LLM-fault stage | `llm-fault` | n/a | last attempt's diagnostics |

`failureClass` is a coarse roll-up for dashboards and is set on every terminal exit (including `validated-success` → `"none"`).

### Triage rules of thumb

- `failureClass="llm-fault"` and the same `terminalReason` keeps recurring across runs → tighten the prompt template, add an example, or extend the validation contract.
- `failureClass="compiler-fault"` ever → file a bug. The user's prompt is not at fault. Check `attempts[-1].compileDiagnostics` and `compileSummary` (especially `droppedComponentReasons` and `stageDiagnostics`) for root cause.
- `failureClass="provider-fault"` recurring → check OpenAI status / API key / rate limits, not the form-AI code.
- `failureClass="infrastructure-fault"` ever → bad deploy (missing context pack file). Check the build artefacts.

### Semantic-validation gate rules

The gate (`backend/modules/form_ai/semantic_validator.py`) runs AFTER `FormSemanticPlan` parses and BEFORE the compiler. It catches LLM faults that the Pydantic shape parser cannot:

| Rule code | Fires when |
|-----------|------------|
| `empty-plan` | `components` is empty. |
| `unknown-component-type` | `componentType` is not registered in the resolved capability snapshot. |
| `width-intent-not-allowed` | `widthIntent` is not in this component's allowed `widthClasses`. |
| `missing-options-for-choice` | `componentType` ∈ {`dropdown`, `radio`, `checkbox`, `select`} but `options` is missing or empty. |
| `invalid-validation-rule` | A key in `validationIntent` is not in this component's `allowedRules` from the validation contract. |
| `duplicate-component-id` | The same `componentId` is reused (only enforced when explicitly set; auto-synthesised ids are always unique). |

The gate is permissive when no governance is configured (no capability snapshot or no validation contracts in the resolved governance bundle) so a fresh install can still generate forms.
