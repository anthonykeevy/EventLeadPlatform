# Story 3.8 UAT Test Guide - Public Form Renderer

**Status:** 📋 TBD (Run during Story 3.8 implementation)  
**Story:** `docs/stories/story-3.8.md`  
**Context:** `docs/stories/story-context-3.8.xml`  

> Note: At time of writing, the Story 3.8 story/context files may not exist yet in-repo. This UAT guide is based on Epic 3 requirements in `docs/stories/EPIC-3-WORKFLOW-GUIDE.md` and `docs/stories/EPIC-3-ARCHITECTURE-REF.md`. If Story 3.8 specifies different routes/UI labels, update this guide to match.

---

## 🛠️ Pre-requisites

Before starting the tests, ensure the following:

1. **Application is running:** Frontend dev server is active.
2. **Backend is running:** API is reachable (needed to fetch `FormVersion.DefinitionJSON`).
3. **Test form exists:** You have at least one Form that has a **published/active version** containing `FormVersion.DefinitionJSON`.
4. **Access to a public render entry point:** One of the following is available:
   - **Preferred:** A **Preview URL** / **Public URL** surfaced in the UI (e.g., from a Form detail view).
   - **Alternative:** A documented public route for the renderer (as implemented in Story 3.8).
5. **A “Logic-enabled” test form is available:** A form whose DefinitionJSON contains `logic.rules` (authored in Builder; Story 3.6) and is expected to execute at runtime (Story 3.7).

### How to verify “renderer is reading stored DefinitionJSON” (choose at least one)

- **Method A (Preferred): Network response**
  - Open DevTools → Network.
  - Load the public renderer page.
  - Identify the API request returning `DefinitionJSON` (or a form version payload containing it).
  - Confirm the response contains the expected keys (at minimum): pages/components and (if applicable) `logic.rules`.

- **Method B: Change persisted definition, then reload**
  - Modify the form in the Builder.
  - Publish/Save a new version (whatever operation creates/updates `FormVersion.DefinitionJSON`).
  - Reload the public renderer page and confirm it reflects the updated definition.

- **Method C: Known test fixture**
  - Use a known seed/test form whose DefinitionJSON is stable and documented.

---

## 🧪 Test Scenarios

### Scenario 1: Render from stored DefinitionJSON (Happy Path)

**Goal:** The public renderer loads and renders a form purely from stored `FormVersion.DefinitionJSON`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Obtain the form’s public renderer URL (Preview/Public URL or Story 3.8 route). | You have a URL that opens the renderer for a specific form/version. |
| 2 | Open the renderer URL in a desktop browser. | Page loads without blank screens or crashes. |
| 3 | Verify renderer fetches definition (Network Method A). | Network shows a request returning `DefinitionJSON` (or equivalent payload). |
| 4 | Confirm at least 3 component types render (e.g., text/email/select). | Components render with correct labels/placeholders and consistent spacing. |
| 5 | Interact with each field (type/select). | Input accepts entry; cursor/focus behaves normally. |
| 6 | Verify validation message area presence. | Each field has a stable area for validation/help text (no layout jumps when errors appear). |

---

### Scenario 2: Theme / global styles apply in the renderer

**Goal:** Renderer applies theme/global styles from DefinitionJSON (fonts/colors/spacing).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the renderer for a form with non-default global styles (font, primary color, spacing). | Renderer loads successfully. |
| 2 | Observe typography and primary color usage. | Fonts and colors match the configured theme (no fallback to inconsistent defaults). |
| 3 | Compare at least one component style with Builder preview (same definition). | Visual output is consistent enough that users recognize it as the same form (allowing for builder-only editing chrome not present in renderer). |

---

### Scenario 3: Unknown component type fallback (Do not crash)

**Goal:** Renderer does not crash if DefinitionJSON contains an unknown component `type`.

**Setup note:** This requires a definition containing a component with a `type` not present in the registry.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load a form version whose DefinitionJSON contains an unknown component type. | Page loads; no crash/white screen. |
| 2 | Scroll to where the unknown component should render. | A safe fallback UI is shown (e.g., “Unsupported component: <type>”). |
| 3 | Verify other components still render and remain usable. | The rest of the form is fully interactive. |
| 4 | Verify console does not show unhandled exceptions. | No uncaught runtime errors; warnings are acceptable if non-blocking. |

---

### Scenario 4: Malformed component config fallback (Do not crash)

**Goal:** Renderer tolerates missing/invalid props/config for a known component type.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load a form version where a known component has missing/invalid props (e.g., missing label). | Page loads successfully. |
| 2 | Locate the affected component. | Component renders with safe defaults and/or a non-blocking warning; no crash. |
| 3 | Interact with other fields. | Other fields function normally. |

---

### Scenario 5: Responsive layout (Tablet viewport)

**Goal:** Renderer is tablet-friendly (layout, scrolling, touch targets).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the renderer in Chrome/Edge. | Renderer loads. |
| 2 | Switch DevTools device emulation to **768×1024** (tablet portrait). | Layout adapts; content remains readable. |
| 3 | Scroll from top to bottom. | Smooth scrolling; no jittery layout shifts; no “stuck” scroll regions. |
| 4 | Confirm no unintended horizontal scrolling. | Page does not require horizontal scroll to use the form. |
| 5 | Tap/click into text fields and open selects. | Touch/click targets are large enough; controls open reliably. |
| 6 | Rotate to tablet landscape (e.g., 1024×768). | Layout remains usable; inputs remain accessible without clipping. |

---

### Scenario 6: Long form usability (Scrolling + focus)

**Goal:** Long forms remain usable on tablets (focus, keyboard, and scrolling behavior).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Use a form with enough components to exceed one screen height (10+ fields). | Renderer loads. |
| 2 | Fill fields near the top, then scroll mid-page and fill additional fields. | Scroll position is stable; entered values remain intact. |
| 3 | Focus a field near the bottom (tablet emulation). | The focused input remains visible (no hidden-behind-keyboard behavior in common browsers, within reason). |
| 4 | Use Tab/Shift+Tab navigation (desktop keyboard). | Focus order is sensible and excludes hidden fields (if any rules hide fields). |

---

### Scenario 7: Runtime logic – visibility (show/hide)

**Goal:** Runtime rules affect component visibility during data entry.

**Setup note:** Use a form with at least one rule: “Show Field B if Field A equals ‘Yes’”.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load the renderer for the logic-enabled form. | Renderer loads. |
| 2 | Confirm Field B is initially hidden (if rule condition starts false). | Field B is not visible and not focusable. |
| 3 | Set Field A to the value that makes the rule true (e.g., select “Yes”). | Field B becomes visible immediately (or within a short, consistent delay). |
| 4 | Change Field A back to a non-matching value. | Field B becomes hidden again; focus/tab order updates accordingly. |

---

### Scenario 8: Runtime logic – required/unrequire

**Goal:** Runtime rules affect required state during entry and validation.

**Setup note:** Use a rule: “Require Field B if Field A equals ‘Yes’” (and optionally “Unrequire” otherwise).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load the renderer. | Renderer loads. |
| 2 | Ensure Field A is set so the rule is false. | Field B is not marked required (no required indicator). |
| 3 | Set Field A so the rule becomes true. | Field B shows required indicator/state. |
| 4 | Attempt to proceed with validation behavior (e.g., try to submit, or trigger validation as defined by the renderer UX). | Field B produces a clear required-field error if empty, using the validation message area. |
| 5 | Toggle Field A back so Field B becomes unrequired. | Required indicator is removed; required validation no longer blocks the user for Field B. |

---

### Scenario 9: Runtime logic – enable/disable

**Goal:** Runtime rules affect enabled/disabled state during entry.

**Setup note:** Use a rule: “Disable Field C if Field A equals ‘No’” (and “Enable Field C if Field A equals ‘Yes’” if desired).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load the renderer. | Renderer loads. |
| 2 | Set Field A to the value that disables Field C. | Field C visibly becomes disabled (disabled styling). |
| 3 | Attempt to type/select into Field C. | Input is blocked (no changes possible while disabled). |
| 4 | Change Field A so the rule enables Field C. | Field C becomes enabled and editable again. |

---

### Scenario 10: Broken rule references (Do not crash)

**Goal:** If `logic.rules` references missing component ids, renderer stays stable.

**Setup note:** Use a form version where at least one rule references a deleted/missing source or target component id.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load the renderer for the form version with broken rule references. | Renderer loads; no crash/white screen. |
| 2 | Observe the UI for warnings/indicators. | A non-blocking warning is surfaced (banner, toast, or inline indicator) stating some rules could not be applied. |
| 3 | Interact with unaffected fields. | Form remains usable; rule engine ignores broken rules safely. |
| 4 | Check browser console. | No uncaught exceptions; warnings are acceptable. |

---

### Scenario 11: Unknown component + runtime logic combined

**Goal:** Renderer can tolerate unknown components while still applying rules to known components.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load a definition that includes (a) an unknown component type and (b) valid rules affecting known components. | Renderer loads without crashing. |
| 2 | Trigger runtime logic conditions by changing source values. | Rules apply to known target components correctly. |
| 3 | Locate the unknown component. | It renders with fallback UI and does not block the rest of the form. |

---

### Scenario 12: Deterministic rule ordering / conflict resolution (last applicable rule wins)

**Goal:** When multiple enabled rules affect the same target property, the renderer resolves conflicts deterministically based on persisted rule order (top-to-bottom).

**Setup note:** Create a test form where two enabled rules can both apply to the same target component and the same property (e.g., visibility), but lead to different outcomes. Example: two rules targeting Field B with opposite actions (`show` and `hide`) that can both be true under the same inputs. Ensure the rules are ordered and reorderable (Story 3.6), and that runtime evaluation is active (Story 3.7).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Load the renderer for the conflict-test form. | Renderer loads normally. |
| 2 | Set inputs so that **both** conflicting rules evaluate to true at the same time. | Both rules are eligible to apply; renderer does not crash or flicker uncontrollably. |
| 3 | Observe the final state of the affected target property (e.g., Field B visibility). | The outcome matches the **last applicable rule** in the persisted rule order. |
| 4 | Change the rule order in the Builder (swap the conflicting rules), publish/save the definition, then reload the renderer. | The outcome flips accordingly, proving ordering determinism from stored DefinitionJSON. |

---

## 📊 Test Summary (To be completed during execution)

| Scenario | Description | Status |
|----------|-------------|--------|
| **1** | Render from stored DefinitionJSON (Happy Path) | ⬜ TBD |
| **2** | Theme/global styles apply | ⬜ TBD |
| **3** | Unknown component fallback | ⬜ TBD |
| **4** | Malformed config fallback | ⬜ TBD |
| **5** | Tablet responsive layout | ⬜ TBD |
| **6** | Long form usability (scroll + focus) | ⬜ TBD |
| **7** | Runtime logic: show/hide | ⬜ TBD |
| **8** | Runtime logic: require/unrequire | ⬜ TBD |
| **9** | Runtime logic: enable/disable | ⬜ TBD |
| **10** | Broken rule references do not crash | ⬜ TBD |
| **11** | Unknown component + rules combined | ⬜ TBD |
| **12** | Deterministic ordering / conflict resolution (last wins) | ⬜ TBD |

---

## 📝 Notes for Testers

1. **Submission/outbox is out of scope (Story 3.9):** If a Submit action exists, UAT should validate only client-side behavior (field state, validation UI), not backend transport reliability.
2. **Determinism expectation:** Rule outcomes should be predictable; if conflicting rules exist, behavior must follow the ordering rules defined by the Logic Engine story.
3. **Non-blocking warnings:** Warnings for broken references/unknown types should be visible but must not prevent form interaction.
