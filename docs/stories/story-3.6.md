# Story 3.6: Conditional Logic UI

**Epic:** 3 - Form Builder & Logic Engine  
**Domain:** Logic Engine  
**Status:** ✅ Complete  
**Priority:** High  

---

## 📖 User Story

**As a** Form Designer,  
**I want to** create and edit conditional rules like “Show Field X if Field Y equals ‘Yes’”,  
**So that** I can build dynamic forms without writing code.

**Context & Entry Point:**  
The user has already:
1. Entered the Builder (Route: `/forms/:formId/builder`).
2. Added components to the Canvas.
3. Configured component properties in the right-side Properties Panel (Story 3.5).

---

## 🧭 Scope Boundary (CRITICAL)

**In scope (Story 3.6):**
- UI for authoring rules (create/edit/delete/reorder).
- A structured JSON data model for rules saved into the form definition (**DefinitionJSON**).
- Validation UX (prevent invalid rules, show clear messages).

**Out of scope (Story 3.6):**
- **Runtime evaluation / live application of rules** in the builder preview or renderer.
- Any “rule engine” execution logic (this is **Story 3.7**).

---

## 🎯 Functional Requirements (High Level)

### 1) Logic Panel
- Provide a **Logic Panel** for managing rules:
  - Either a **tab** in the right panel (recommended alongside Properties/Theme), or a dedicated right panel.
  - Must work when no component is selected (rules are form-level).

### 2) Minimum Rule Shape
Support authoring rules of the form:

- **IF** (SourceField) (Operator) (Value) **THEN** (TargetField) (Action)

**Operators (minimum):**
- `equals`
- `notEquals`
- `contains` (string)
- `isEmpty`

**Actions (minimum):**
- `show` / `hide`
- `require` / `unrequire`
- `enable` / `disable`

### 3) Persistence
- Rules must be saved into the form definition (**DefinitionJSON**) as **structured JSON** (no code).
- Rules must survive refresh/reload of the builder (i.e., they are part of the persisted schema).

### 4) Validation & Guardrails
- UI must prevent invalid rules, including:
  - Source field cannot equal target field.
  - Missing required parts (operator/value/action).
  - `contains` only allowed for string-capable source fields.
  - `isEmpty` does not allow a value input.
- Provide clear, actionable validation messages next to the rule row and/or in a summary area.

---

## 📐 Data Model (DefinitionJSON)

### Storage Location
Add a logic container to `FormDefinition` to hold rules:

- `formDefinition.logic.rules: LogicRule[]`

### Proposed JSON Shape (minimum)

```json
{
  "logic": {
    "rules": [
      {
        "id": "rule-uuid-or-nanoid",
        "enabled": true,
        "when": {
          "sourceComponentId": "comp-2",
          "operator": "equals",
          "value": "Yes"
        },
        "then": {
          "targetComponentId": "comp-5",
          "action": "show"
        }
      }
    ]
  }
}
```

### Notes
- `sourceComponentId` and `targetComponentId` refer to existing `FormComponent.id` values.
- `value` is required for `equals`, `notEquals`, `contains`; omitted/ignored for `isEmpty`.
- The engine in Story 3.7 will interpret these rules; Story 3.6 only defines and persists them.

---

## ✅ Acceptance Criteria

### 1) Logic Panel Presence
- [x] The builder UI includes a **Logic Panel** accessible from the right panel.
- [x] The Logic Panel is usable even when **no component is selected**.

### 2) Rule List Management
- [x] Users can **add** a new rule.
- [x] Users can **edit** an existing rule.
- [x] Users can **delete** a rule.
- [x] Users can **enable/disable** a rule (without deleting it).
- [x] Users can **reorder** rules (ordering is persisted).
- [x] The Logic Panel supports quick filters: **All**, **Enabled**, **With errors** (minimum).
- [x] The Logic Panel shows a visible **error count** (badge or summary) when one or more rules are invalid/broken.
- [x] Deleting a rule is protected against accidents via **confirm delete** (implemented).

### 3) Rule Authoring Controls
- [x] The rule editor supports selecting a **Source Field** from existing components.
- [x] The rule editor supports selecting an **Operator** from the required list.
- [x] The rule editor supports entering/selecting a **Value** when required.
- [x] The rule editor supports selecting a **Target Field** from existing components.
- [x] The rule editor supports selecting an **Action** from the required list.
- [x] Field pickers are **searchable** and display enough identity to disambiguate duplicates (e.g., `Label (exportName)` or `Label (componentId)`).
- [x] Each rule row renders a concise **human-readable summary** of the rule (scannable sentence format).
- [x] (Optional, recommended) Users can set an optional **Rule Name** to help manage large rule sets.

### 3.1) Type-Aware Value Inputs (UX requirement)
- [x] When the Source Field is a **select/radio/checkbox group**, the **Value** control is a picker of that field’s allowed option values (not free-text by default).
- [x] When the Source Field is **text-capable**, the Value control is a text input and `contains` is available.
- [x] When Operator is `isEmpty`, the Value control is **hidden/disabled** and no value is saved.

### 4) Validation UX
- [x] The UI prevents saving a rule when it is incomplete or invalid.
- [x] If `SourceField == TargetField`, the UI blocks save and shows: “Source field cannot be the same as target field.”
- [x] If operator/value is invalid or missing, the UI shows a field-level message explaining what to fix.
- [x] Validation messages are clear and do not require developer knowledge.
- [x] Broken references are surfaced clearly (e.g., “Source field was deleted”) and included in the **With errors** filter.
- [x] Validation messages are specific and actionable (e.g., “Choose a target field”, “Value is required for equals”, “Contains is only available for text fields”).

### 5) Persistence in DefinitionJSON
- [x] Created/edited rules are saved into `FormDefinition.logic.rules`.
- [x] Rules are persisted as structured JSON in `FormVersion.DefinitionJSON` (no code strings).

### 6) Explicit Non-Goal Confirmation (Boundary)
- [x] This story does **not** implement runtime evaluation of rules in the preview/renderer.
- [x] The Logic Panel includes a clear note that rules are **saved now** but **take effect when the evaluation engine ships (Story 3.7)**.

---

## 🛠️ Technical Notes (Guidance)

### UI/UX Recommendations
- Rule list as a table/stack of “Rule Rows” with inline editing.
- Each row has:
  - Enabled toggle
  - IF: SourceField dropdown → Operator dropdown → Value input
  - THEN: TargetField dropdown → Action dropdown
  - Row-level error display
  - Delete action
- Recommended: keep rules **scannable** (sentence-style view) with a clear “edit” affordance.

### Data Integrity Constraints
- Source/Target dropdowns must exclude invalid selections (e.g., exclude the selected source from the target list).
- If a component referenced by a rule is deleted from the canvas, the rule must surface an error state (e.g., “Missing field”).
  - (Resolution behavior can be “requires user fix” in 3.6; engine behavior is 3.7.)
- Reordering must be usable without drag-and-drop (accessibility): include **Move up / Move down** controls (keyboard accessible) in addition to any drag handle.

### Suggested Types
- `LogicOperator = 'equals' | 'notEquals' | 'contains' | 'isEmpty'`
- `LogicAction = 'show' | 'hide' | 'require' | 'unrequire' | 'enable' | 'disable'`

---

## 📋 Dependencies

- Story 3.2: DefinitionJSON schema contract.
- Story 3.5: Properties Panel and editable component configs.

---

## 📚 Related Documentation

- `docs/stories/EPIC-3-ARCHITECTURE-REF.md`
- `docs/stories/EPIC-3-STATUS.md`
- `docs/stories/story-3.5.md`
- `docs/stories/story-context-3.5.xml`

---

## 🧪 UAT Test Guide

**Full Guide:** `docs/stories/STORY-3.6-UAT-TEST-GUIDE.md` ✅ PASSED

---

## 📋 Completion Criteria

- [x] All Acceptance Criteria are completed.
- [x] The story includes (or links to) a completed UAT test guide and the tests pass.
- [x] No console errors or TypeScript warnings introduced by the UI changes.

---

## ✅ Completion Report

**Completed:** 2025-12-12  
**UAT:** ✅ PASSED — `docs/stories/STORY-3.6-UAT-TEST-GUIDE.md`  

### Delivered Outcomes
- **Logic Panel (UI Authoring)**: Right panel includes a dedicated **Logic** tab for managing conditional rules.
- **Rule CRUD**: Create, edit, delete, enable/disable, and reorder rules with persistent ordering.
- **Validation & Guardrails**: Prevents incomplete rules; blocks Source == Target; type-aware operator/value inputs; broken references surface as clear errors.
- **Persistence**: Rules are stored in `FormDefinition.logic.rules` as deterministic JSON (no code/functions) and survive builder reload.
- **Boundary honored**: No runtime evaluation engine or rule application in preview (reserved for Story 3.7).

### Key Implementation Touchpoints
- `frontend/src/features/builder/components/PropertiesPanel.tsx` (Inspector/Logic tabs)
- `frontend/src/features/builder/components/logic/LogicPanel.tsx` (Rule list + editor UI)
- `frontend/src/features/builder/components/logic/ruleValidation.ts` (Validation + type rules)
- `frontend/src/features/builder/stores/useBuilderStore.ts` (Rule CRUD + persistence)
- `frontend/src/features/builder/types/builder.types.ts` (Rule JSON types + FormDefinition.logic)
- `backend/schemas/form_definition.py` (Pydantic support for `logic.rules`)
