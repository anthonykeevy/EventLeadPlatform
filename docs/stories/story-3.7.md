# Story 3.7: Rule Evaluation Engine

**Epic:** 3 - Form Builder & Logic Engine  
**Domain:** Logic Engine  
**Status:** ✅ Complete  
**Priority:** High  

---

## 📖 User Story

**As a** Form Designer,  
**I want to** have my saved conditional rules execute at runtime (in builder preview and the form renderer),  
**So that** fields dynamically show/hide, enable/disable, and require/unrequire based on user input.

**Context & Entry Point:**  
- Story 3.6 is complete: rules are authored in the Builder and persisted into **DefinitionJSON** at `formDefinition.logic.rules`.
- This story activates those rules during runtime interactions.

---

## 🧭 Scope Boundary (CRITICAL)

**In scope (Story 3.7):**
- A deterministic **rule evaluation engine** that reads rules from `formDefinition.logic.rules`.
- Runtime application of rule actions to components in:
  - **Builder preview** (design-time interactive preview behavior)
  - **Renderer** (runtime form experience)
- Supported actions (minimum):
  - `show` / `hide`
  - `enable` / `disable`
  - `require` / `unrequire`
- Safe behavior for missing/broken rule references:
  - Rule is ignored
  - Warning is surfaced in UI

**Out of scope (Story 3.7):**
- Rule authoring UI changes (already delivered in Story 3.6).
- Changes to the persisted rule shape (already defined in Story 3.6).
- New operators/actions beyond the existing minimum set.
- Multi-step branching/navigation rules (future).

---

## 🎯 Functional Requirements (High Level)

### 1) Rule evaluation triggers
- Rules must be evaluated whenever **relevant values** change:
  - Source component value changes (the component referenced by `when.sourceComponentId`).
  - Rules list changes (add/update/delete/enable/disable/reorder).
  - Component graph changes affecting referenced ids (component deleted/added).

### 2) Deterministic and predictable outcomes (ordering matters)
- Rules are processed in **persisted order** (top-to-bottom as shown in Story 3.6 UI).
- Conflicts must resolve deterministically:
  - **Last applicable rule wins** for the same target + property (visibility / enabled / required).
- Engine must be **pure** and repeatable: same inputs → same outputs.

### 3) Runtime effects (builder preview + renderer)
- Engine output must be applied consistently in both runtime contexts:
  - **Visibility**: hidden components are not rendered and are removed from tab order.
  - **Enabled**: disabled components render in a disabled state and do not accept input.
  - **Required**: required components show required indicator and are validated as required.

### 4) Safety and resilience
- If a rule references a missing source/target component id, or an invalid operator/value combination:
  - Ignore that rule for evaluation
  - Emit a warning surfaced in UI (non-blocking)
- The engine must never crash the app due to malformed/broken rule data.

---

## 📐 Runtime Model (Conceptual)

### Inputs
- `FormDefinition` with rules at `formDefinition.logic.rules`
- A runtime **value map** for components, keyed by component id:
  - `valuesByComponentId: Record<string, unknown>`
- The current component graph for id lookups.

### Outputs
For each component id, compute the effective runtime state:
- `visible: boolean` (default true)
- `enabled: boolean` (default true)
- `required: boolean` (default from component props/validation)

Additionally:
- `warnings: RuntimeRuleWarning[]` (for broken/missing references, invalid comparisons, etc.)

---

## ✅ Acceptance Criteria

### 1) Engine correctness & determinism
- [x] Given a fixed `FormDefinition.logic.rules` and value map, evaluation produces the same results on every run.
- [x] Rules are applied in persisted order.
- [x] When multiple rules affect the same target property, the last applicable rule wins.

### 2) Supported actions
- [x] `show` / `hide` correctly toggles visibility for the target component.
- [x] `enable` / `disable` correctly toggles enabled state for the target component.
- [x] `require` / `unrequire` correctly toggles required state for the target component.

### 3) Trigger behavior
- [x] Updating a source component’s value re-evaluates rules that depend on that source.
- [x] Enabling/disabling a rule re-evaluates outcomes.
- [x] Reordering rules changes outcomes accordingly (ordering matters).

### 4) Builder preview integration
- [x] In builder preview, rule effects apply live as relevant values change.
- [x] Hidden components are not shown and do not receive focus.
- [x] Disabled components appear disabled and do not accept input.
- [x] Required components show required indicator consistent with existing field rendering.

### 5) Renderer integration
- [x] In the renderer, rule effects apply live as relevant values change.
- [x] Renderer behavior matches builder preview for the same rules + values.

### 6) Safe behavior + warnings
- [x] Rules with missing source/target references are ignored (do not crash evaluation).
- [x] Ignored/broken rules surface a visible warning in UI (non-blocking).

---

## 🛠️ Technical Notes (Guidance)

### Recommended architecture
- Implement a shared, testable evaluation module (pure functions) that can be reused by:
  - Builder preview runtime
  - Renderer runtime

### Comparison semantics (minimum)
- `equals`: true if normalized values match
- `notEquals`: inverse of equals
- `contains`: string containment (only for text-capable source fields)
- `isEmpty`: true for null/undefined/empty-string (and optionally empty array)

### Warning strategy
- Maintain a list of runtime warnings:
  - Missing source id
  - Missing target id
  - Invalid operator for the source type
  - Invalid/missing value for a value-requiring operator
- Warnings are displayed in the Logic panel and/or a compact warning indicator in preview/renderer.

---

## 📋 Dependencies

- Story 3.6: Conditional Logic UI (rules persisted in DefinitionJSON)
- FormDefinition types: `frontend/src/features/builder/types/builder.types.ts`

---

## 📚 Related Documentation

- `docs/stories/story-3.6.md`
- `docs/stories/story-context-3.6.xml`
- `docs/stories/EPIC-3-STATUS.md`
- `docs/stories/EPIC-3-ARCHITECTURE-REF.md`

---

## 🧪 UAT Test Guide (PLACEHOLDER)

**Completed:** `docs/stories/STORY-3.7-UAT-TEST-GUIDE.md` ✅

All UAT scenarios passed, covering:
- Builder preview rule execution (show/hide, enable/disable, require/unrequire)
- Renderer parity
- Conflict resolution / deterministic ordering
- Broken-reference behavior + warnings

---

## 📋 Completion Criteria

- [x] All Acceptance Criteria are completed.
- [x] UAT Test Guide section above is completed and tests pass.
- [x] No console errors or TypeScript warnings introduced.

---

## ✅ Completion Report

**Completed:** 2025-12-14  
**UAT:** ✅ Passed (Scenarios 1–10)

### What was delivered
- **Shared rule evaluation engine** (deterministic, pure): evaluates `formDefinition.logic.rules` in persisted order with **last applicable wins**.
- **Runtime application** in:
  - **Builder Preview (Runtime)** (toggle via header Preview button)
  - **Renderer runtime** route: `/forms/:formId/render`
- **Supported actions**: show/hide, enable/disable, require/unrequire.
- **Safety + warnings**: broken source/target references are ignored safely and surfaced as warnings (non-blocking).
- **UAT unblocker**: delete selected component(s) via `Delete`/`Backspace` with Undo/Redo support (used for broken-reference scenarios).
