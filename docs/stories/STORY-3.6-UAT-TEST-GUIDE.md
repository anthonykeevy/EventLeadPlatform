# Story 3.6 UAT Test Guide - Conditional Logic UI

**Status:** ✅ PASSED  
**Story:** `docs/stories/story-3.6.md`  
**Context:** `docs/stories/story-context-3.6.xml`

---

## 🛠️ Pre-requisites

Before starting the tests, ensure the following:

1. **Application is running:** Frontend dev server is active.
2. **Route:** Navigate to `/forms/:formId/builder`.
3. **Environment:** Desktop browser (Chrome/Edge recommended).
4. **Canvas State:** Ensure at least **two distinct fields** exist on the canvas:
   - **Field A (Source):** Prefer a field with discrete values (e.g., Select/Radio/Checkbox group) named “Field A”.
   - **Field B (Target):** Any other field named “Field B”.
5. **Logic Panel Available:** Confirm the right panel includes a **Logic** tab/panel.
6. **Important Scope Note:** In Story 3.6, rules are **authored and saved** but may **not take effect in preview/runtime** until Story 3.7.

### How to verify “stored definition” (choose at least one)

Use **one** of the following methods to confirm the rule is persisted to the form’s DefinitionJSON:

- **Method A (Preferred): Network payload**
  - Open DevTools → Network.
  - Perform the app’s “Save” / “Publish” / “Save Version” action.
  - Inspect the request payload and confirm it contains `logic.rules`.

- **Method B: Reload persistence**
  - Refresh the Builder page.
  - Confirm the rule list appears exactly as saved.

- **Method C: Export/Download JSON (if available)**
  - Use any “Export/Download Definition JSON” action.
  - Confirm the exported JSON contains `logic.rules`.

---

## 🧪 Test Scenarios

### Scenario 1: Create Rule

**Goal:** Create a simple rule (IF A equals X THEN show B) and save it.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the **Logic Panel**. | Logic Panel is visible and shows existing rules list (may be empty). |
| 2 | Click **Add Rule** (or equivalent). | A new rule row appears in an editable state. |
| 3 | Set **Source Field** to **Field A**. | Source field is selected; target list should not allow selecting the same field as target. |
| 4 | Set **Operator** to `equals`. | Operator is set; value input becomes available (since `equals` requires a value). |
| 5 | Set **Value** to a valid value **X** (from options if Field A is select/radio/checkbox). | Value is accepted; no validation errors shown for the value control. |
| 6 | Set **Target Field** to **Field B**. | Target field is selected; Source ≠ Target enforced. |
| 7 | Set **Action** to `show`. | Action is selected; rule reads as “If A equals X then show B”. |
| 8 | Save/commit the rule (if explicit) and then perform the app’s persistence action (Save/Publish/Save Version). | Rule appears in the rules list as a stable entry, with a readable summary. No validation errors. |
| 9 | Verify stored definition (Method A/B/C from prerequisites). | DefinitionJSON includes the new rule under `logic.rules` with correct fields (`sourceComponentId`, `operator`, `value`, `targetComponentId`, `action`). |

**Scenario 1 Result:** ✅ PASSED

---

### Scenario 2: Edit Rule

**Goal:** Change operator/value/action and verify it persists.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In the Logic Panel, locate the rule created in Scenario 1. | Rule is visible with its current configuration and readable summary. |
| 2 | Change **Operator** (e.g., from `equals` → `notEquals`). | Operator updates; validation remains clear; value remains required. |
| 3 | Change **Value** (e.g., X → Y). | Value updates and is accepted. |
| 4 | Change **Action** (e.g., `show` → `hide`). | Action updates and the readable summary reflects the change. |
| 5 | Persist changes (Save/Publish/Save Version). | No validation errors; rule remains enabled/visible. |
| 6 | Verify stored definition (Method A/B/C). | Persisted JSON reflects the updated operator/value/action for the same rule id (or equivalent stable identity). |

**Scenario 2 Result:** ✅ PASSED

---

### Scenario 3: Delete Rule

**Goal:** Remove a rule and verify it is removed from stored definition.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In the Logic Panel, locate the rule created earlier. | Rule is visible. |
| 2 | Click **Delete** on the rule. | A safety mechanism appears: **confirm delete** OR an **Undo** option is presented (per Story 3.6 UX requirements). |
| 3 | Confirm deletion (or delete then allow the undo window to pass). | Rule disappears from the list. |
| 4 | Persist changes (Save/Publish/Save Version). | Save completes without errors. |
| 5 | Verify stored definition (Method A/B/C). | `logic.rules` no longer contains the deleted rule entry. |

**Scenario 3 Result:** ✅ PASSED

---

### Scenario 4: Rule Validation

**Goal:** Attempt to save an incomplete rule and verify clear UI errors.

> Run these as separate sub-tests; each should produce a clear, actionable validation message and prevent saving.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click **Add Rule** to create a new rule row. | New rule row appears. |
| 2 | Attempt to save with **missing Source Field**. | Save is blocked; message such as “Choose a source field” is shown near the control/row. |
| 3 | Select Source Field but leave **Operator** empty; attempt to save. | Save is blocked; message such as “Choose an operator” is shown. |
| 4 | Select Operator `equals` but leave **Value** empty; attempt to save. | Save is blocked; message such as “Value is required for equals” is shown. |
| 5 | Select Source/Operator/Value but leave **Target Field** empty; attempt to save. | Save is blocked; message such as “Choose a target field” is shown. |
| 6 | Select Target Field but leave **Action** empty; attempt to save. | Save is blocked; message such as “Choose an action” is shown. |
| 7 | Confirm that incomplete/invalid rules are visually flagged and counted. | The rule row shows an error state; Logic Panel **error count** increases and **With errors** filter includes this rule. |

**Scenario 4 Result:** ✅ PASSED

---

### Scenario 5: Invalid Rule Guardrails

**Goal:** Attempt to create a rule where Source == Target and verify UI blocks it.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click **Add Rule** to create a new rule. | New rule row appears. |
| 2 | Set **Source Field** to **Field A**. | Source selected. |
| 3 | Attempt to set **Target Field** to the same field (**Field A**). | UI prevents selection OR allows selection but flags it immediately as invalid. |
| 4 | If selection is allowed, attempt to save the rule. | Save is blocked with a clear message: “Source field cannot be the same as target field.” |
| 5 | Confirm the UI provides a clear fix path. | Target field control indicates what to change; rule remains in error state until corrected. |

**Scenario 5 Result:** ✅ PASSED

---

## 📊 Test Summary

| Scenario | Description | Status |
|----------|-------------|--------|
| **1** | Create Rule | ✅ PASSED |
| **2** | Edit Rule | ✅ PASSED |
| **3** | Delete Rule | ✅ PASSED |
| **4** | Rule Validation | ✅ PASSED |
| **5** | Invalid Rule Guardrails | ✅ PASSED |

## 📝 Notes for Testers

1. **Persistence vs. Runtime:** Passing these tests does **not** require the form preview/renderer to actually hide/show/require fields yet (that is Story 3.7).
2. **Type-aware values:** If Source Field is select/radio/checkbox, expect a value picker (not free text) and only valid values should be selectable.
3. **Searchable pickers:** Source/Target pickers should support search and disambiguation (e.g., `Label (exportName)` / `Label (id)`).

---

## 📚 Related Documentation

- `docs/stories/story-3.6.md`
- `docs/stories/story-context-3.6.xml`
- `docs/stories/EPIC-3-ARCHITECTURE-REF.md`
