# Story 3.7 UAT Test Guide - Rule Evaluation Engine

**Status:** ✅ UAT Complete (All Scenarios Passed)  
**Story:** `docs/stories/story-3.7.md`  
**Context:** `docs/stories/story-context-3.7.xml`  

---

## 🛠️ Pre-requisites

Before starting the tests, ensure the following:

1. **Application is running:** Frontend dev server is active.
2. **Route (Builder):** Navigate to `/forms/:formId/builder`.
3. **Logic Panel available:** Confirm the right panel includes the **Logic** tab/panel (Story 3.6).
4. **Test form state:** Ensure the canvas has at least these fields (labels are suggestions):
   - **Field A (Source):** A discrete-value field (Select/Radio/Checkbox group) with an option value `Yes` and another value `No`.
   - **Field B (Target - Visibility):** Any field that can be shown/hidden.
   - **Field C (Target - Enabled):** Any field that can be enabled/disabled.
   - **Field D (Target - Required):** Any field that can be required/unrequired.
   - *(Optional)* **Submit Button**: Add a `submit-button` component if the runtime provides a submit/validate action in preview.
5. **Rules exist:** Create and persist rules under `formDefinition.logic.rules` (Story 3.6) and verify they persist after refresh.

### Recommended UAT Test Form Template (use this for all scenarios)

Create a single form page with these fields (labels are suggestions; **values matter**):

- **Field A (Source / Radio)**: `Are you a Male?`
  - Options: `Y` and `N` *(these are the stored values you must use in rules)*
- **Field B (Target / First Name)**: `First Name`
- **Field C (Target / Company Name)**: `Company Name`
- **Field D (Target / Email Address)**: `Email Address` (default required = true)
- **Field E (Target / Phone)**: `Phone` (default required = false)

Notes:
- **Rule comparisons are exact string matches** against option **values** (e.g., `Y` / `N`), not the label text.
- Visibility defaults to **visible**; to prove show/hide you must include a **hide** rule (or start hidden if that ever becomes a feature).

### How to verify “stored definition” contains rules (choose at least one)

- **Method A (Preferred): Network payload**
  - Open DevTools → Network.
  - Perform the app’s “Save / Publish / Save Version” action.
  - Confirm payload includes `logic.rules`.

- **Method B: Reload persistence**
  - Refresh the Builder.
  - Confirm rules remain present and ordered as saved.

### Runtime surface(s) to test

Story 3.7 requires runtime behavior in:
- **Builder preview** (interactive preview inside the builder)
- **Renderer runtime** (the runtime form view)

If your build does not yet expose a standalone renderer route, run the **Builder Preview** scenarios now and keep the **Renderer** scenarios as “Pending” until the renderer surface exists.

---

## 🧪 Test Scenarios

### Scenario 1: Runtime visibility (show/hide)

**Goal:** A rule can hide/show a target field based on a source field value.

**Rule setup (recommended – 2 rules):**
- IF Field A equals `Y` THEN `hide` Field C (Company Name)
- IF Field A equals `N` THEN `hide` Field B (First Name)

*(Optional – explicit 4 rules)* Add `show` rules as well, but ensure you also have a corresponding `hide` rule. With default `visible=true`, **show-only rules will not make anything disappear**.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In Builder, open **Preview** mode/surface where field values can be entered. | Preview renders the form fields for interaction. |
| 2 | Set Field A to `Y`. | **Company Name** is hidden; **First Name** remains visible. |
| 3 | Press `Tab` repeatedly (keyboard). | Focus does not land on hidden fields (hidden fields are removed from tab order). |
| 4 | Set Field A to `N`. | **First Name** is hidden; **Company Name** remains visible. |
| 5 | Set Field A back to `Y`. | The visibility flips back deterministically (no flicker/crash). |

---

### Scenario 2: Runtime enabled state (enable/disable)

**Goal:** A rule can enable/disable a target field based on a source field value.

**Rule setup (recommended – 2 rules):**
- IF Field A equals `Y` THEN `disable` Field C (Company Name)
- IF Field A equals `N` THEN `disable` Field B (First Name)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In Preview, set Field A to `Y`. | Company Name appears disabled (visual disabled styling). |
| 2 | Attempt to click/type into Company Name. | It does not accept input while disabled. |
| 3 | Switch Field A to `N`. | First Name becomes disabled and Company Name becomes enabled again. |

---

### Scenario 3: Runtime required state (require/unrequire)

**Goal:** A rule can require/unrequire a target field based on a source field value.

**Rule setup (recommended – 2 rules):**
- IF Field A equals `Y` THEN `require` Field B (First Name)
- IF Field A equals `N` THEN `require` Field C (Company Name)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In Preview, set Field A to `Y`. | First Name shows required indicator. |
| 2 | Leave First Name empty and click **Validate**. | A clear required-field error is shown for First Name. |
| 3 | Switch Field A to `N`. | Company Name becomes required; First Name is no longer required. |
| 4 | Leave Company Name empty and click **Validate**. | A clear required-field error is shown for Company Name (and First Name is not blocking). |

---

### Scenario 4: Rule enable/disable toggle affects runtime

**Goal:** Disabling a rule prevents it from applying at runtime.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In the Logic Panel, ensure a visibility rule affecting Field B is enabled. | Rule shows enabled state. |
| 2 | In Preview, set Field A to satisfy the rule. | Field B changes state per the rule. |
| 3 | Disable the rule (toggle enabled off). | Rule shows disabled state. |
| 4 | Change Field A again to satisfy the rule. | Field B no longer changes due to the disabled rule. |

---

### Scenario 5: Deterministic ordering – conflicts on the same target property (last applicable wins)

**Goal:** When multiple enabled rules affect the same target + property, the **last applicable rule wins** based on persisted ordering.

**Rule setup (recommended conflict):** Create a second source field:
- **Field X (Source / Checkbox):** `Force Show First Name` (checked = true)

Then create two enabled rules that can both be true and both target **First Name** visibility:
- Rule 1: IF Field A equals `N` THEN `hide` First Name
- Rule 2: IF Field X equals `true` THEN `show` First Name

Reorder Rule 1 and Rule 2 to prove last-applicable wins.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Ensure both conflicting rules are enabled and ordered (Rule 1 above Rule 2). | Rule list shows a clear order. |
| 2 | In Preview, set values so both rules are applicable simultaneously. | The final state matches the **last** applicable rule in the list. |
| 3 | Reorder rules (swap them) and persist. | Order change is saved. |
| 4 | Re-run the same inputs in Preview. | The final state flips accordingly, proving ordering determinism. |

---

### Scenario 6: Deterministic ordering – independence across properties

**Goal:** Conflicts resolve per-property (visibility vs enabled vs required) without cross-contamination.

**Rule setup (recommended):**
- Keep the Scenario 5 conflict rules for **visibility** on First Name.
- Add two rules that can also both be true and target **enabled** on Company Name (independent property):
  - Rule A: IF Field A equals `Y` THEN `disable` Company Name
  - Rule B: IF Field X equals `true` THEN `enable` Company Name

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Create rules so Field B visibility conflicts resolve one way, while Field C enabled rules resolve another way under the same inputs. | Rules exist and are ordered. |
| 2 | In Preview, enter the triggering inputs. | Field B final visibility matches last-wins for visibility; Field C final enabled state matches last-wins for enabled; outcomes are consistent and predictable. |

---

### Scenario 7: Broken reference – deleted source component id

**Goal:** If a rule’s source component is missing, the rule is ignored safely and surfaced as a warning.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Create a rule with Field A as the source and Field B as the target; persist it. | Rule exists and is enabled. |
| 2 | Select Field A on the canvas and press `Delete` (or `Backspace`). | Field A is removed from the form. |
| 3 | Open Preview and interact with the form. | The app does not crash; the broken rule does not apply. |
| 4 | Observe the UI warning surface. | A non-blocking warning indicates the rule was ignored due to missing source reference. |

---

### Scenario 8: Broken reference – deleted target component id

**Goal:** If a rule’s target component is missing, the rule is ignored safely and surfaced as a warning.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Create a rule targeting Field B; persist it. | Rule exists and is enabled. |
| 2 | Select Field B on the canvas and press `Delete` (or `Backspace`). | Field B is removed. |
| 3 | Open Preview and interact with remaining fields. | The app does not crash; the broken rule does not apply to any other field. |
| 4 | Observe the UI warning surface. | A non-blocking warning indicates the rule was ignored due to missing target reference. |

---

### Scenario 9: Stability under rapid changes (no flicker/crash)

**Goal:** Repeated changes produce stable, deterministic results.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In Preview, rapidly toggle Field A between `Y` and `N` several times. | No crashes; state updates are consistent (fields do not get stuck in the wrong state). |
| 2 | Repeat while multiple rules are enabled (including ordering conflicts). | Final state always matches last-wins ordering and current inputs. |

---

### Scenario 10: Renderer parity (if renderer runtime is available)

**Goal:** Renderer behavior matches Builder Preview for the same rules + inputs.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the renderer runtime for the same form definition. | Renderer loads successfully. |
| 2 | Repeat Scenarios 1–9 using the renderer UI. | Outcomes match Builder Preview for show/hide, enable/disable, require/unrequire, ordering, and broken reference warnings. |

---

## 📊 Test Summary (To be completed during execution)

| Scenario | Description | Status |
|----------|-------------|--------|
| **1** | Runtime visibility (show/hide) | ✅ Passed |
| **2** | Runtime enabled state (enable/disable) | ✅ Passed |
| **3** | Runtime required state (require/unrequire) | ✅ Passed |
| **4** | Rule enabled toggle affects runtime | ✅ Passed |
| **5** | Deterministic ordering (last applicable wins) | ✅ Passed |
| **6** | Determinism across independent properties | ✅ Passed |
| **7** | Broken source reference ignored + warning | ✅ Passed |
| **8** | Broken target reference ignored + warning | ✅ Passed |
| **9** | Stability under rapid changes | ✅ Passed |
| **10** | Renderer parity (if available) | ✅ Passed |

---

## 📝 Notes for Testers

1. **Ordering matters:** Conflicts must resolve deterministically using persisted rule order (last applicable wins).
2. **Hidden means non-interactive:** Hidden fields should not render and should be removed from tab order.
3. **Broken references must be safe:** Broken rules are ignored and surfaced as **non-blocking warnings**; the app must not crash.
