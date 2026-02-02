# Story 3.8-3.9 Issues and Proposed Solutions

**Created:** 2026-01-13  
**Purpose:** Consolidated list of all UAT issues with proposed solutions for review and approval before implementation.

---

## Summary

| Priority | Count | Status |
|----------|-------|--------|
| 🔴 Critical/High | 3 | To Fix |
| 🟡 Medium | 8 | To Fix |
| 🟢 Low | 3 | Defer/Optional |
| ✅ Already Fixed | 5 | Complete |
| 📋 Specification | 1 | Next Story |

---

## 🔴 CRITICAL/HIGH PRIORITY (Must Fix for Story Completion)

### Issue 1: Text Component `inputWidthOverride` Not Applied in Preview

**ID:** WYSIWYG-001  
**Severity:** 🔴 Critical  
**Scenario:** 20, 24  
**Status:** ✅ **ALREADY FIXED** (2026-01-12)

**Problem:**  
Company Name (`text` type) has `inputWidthOverride: 578` stored in JSON but renders at only 238px in Preview. Other types (textarea, email, phone) render correctly.

**Root Cause:**  
The `inputWidthOverride` value was not being normalized to pixel strings and applied consistently in `objectRenderers.tsx`.

**Solution Applied:**  
Modified `frontend/src/features/builder/utils/objectRenderers.tsx`:
- Normalized `inputWidthOverride` to pixel strings
- Applied to `width`, `maxWidth`, and `minWidth` CSS properties

**Verification:** Needs re-testing in UAT

---

### Issue 2: WYSIWYG - Width Not Updating in Builder Canvas

**ID:** WYSIWYG-002  
**Severity:** 🔴 High  
**Scenario:** 20, 24  
**Status:** 🔴 To Fix

**Problem:**  
Changing `Appearance → Dimensions → Width` (e.g., to 75%) does not visually update the component in the builder canvas, but the change IS applied correctly in preview.

**Root Cause (Suspected):**  
The `componentWidth` property is applied to the runtime renderer but not to the canvas surface. The builder canvas may be using fixed or default widths.

**Proposed Solution:**

1. **Locate the width application code:**
   - `frontend/src/features/builder/components/SortableComponent.tsx` - canvas wrapper
   - `frontend/src/features/builder/components/UniversalFieldShell.tsx` - component shell

2. **Apply `componentWidth` on canvas surface:**
   ```typescript
   // In SortableComponent.tsx or UniversalFieldShell.tsx
   const effectiveWidth = component.props.componentWidth || '100%';
   
   // Apply to container style
   style={{
     width: effectiveWidth,
     // ... other styles
   }}
   ```

3. **Ensure consistency between surfaces:**
   - Canvas surface should use same width calculation as runtime
   - Use `getComponentSurfaceCapabilities()` to determine if width should be applied

**Files to Modify:**
- `frontend/src/features/builder/components/SortableComponent.tsx`
- `frontend/src/features/builder/components/UniversalFieldShell.tsx`

**Estimated Effort:** 2-3 hours

---

### Issue 3: WYSIWYG - Label Wrapping/Squashing Difference

**ID:** WYSIWYG-003  
**Severity:** 🟡 Medium (but related to WYSIWYG-002)  
**Scenario:** 20  
**Status:** 🔴 To Fix

**Problem:**  
Company Name label shows on one line in builder but wraps to 2 lines in preview. The label "Company Name" becomes "Company" / "Name".

**Root Cause (Suspected):**  
- `labelWidth` property may not be applied consistently between canvas and runtime
- The container width constrains the label differently in runtime
- Related to WYSIWYG-002 (component width not applied)

**Proposed Solution:**

1. **Ensure `labelWidth` is respected in runtime:**
   - Check `UniversalFieldShell.tsx` for how `labelWidth` is applied
   - Verify the same calculation is used on both surfaces

2. **Label object renderer check:**
   - In `objectRenderers.tsx`, ensure label has proper `minWidth` or `whiteSpace: nowrap` where appropriate

**Files to Modify:**
- `frontend/src/features/builder/components/UniversalFieldShell.tsx`
- `frontend/src/features/builder/utils/objectRenderers.tsx`

**Estimated Effort:** 1-2 hours (likely fixed by WYSIWYG-002)

---

## 🟡 MEDIUM PRIORITY (Should Fix for Story Completion)

### Issue 4: Inline Validation Error Messages Not Displayed

**ID:** VAL-001  
**Severity:** 🟡 Medium  
**Scenario:** 18, 23  
**Status:** ✅ **ALREADY FIXED** (2026-01-12)

**Problem:**  
Validation error messages were not displaying inline next to individual form fields in runtime mode.

**Solution Applied:**  
- Added `error` property to `ConditionalContext` interface
- Modified `UniversalFieldShell.tsx` to pass `runtimeMode.error` to conditional context
- Updated `conditionalEvaluation.ts` to check for `context.error` in validation rule

**Verification:** Needs re-testing in UAT

---

### Issue 5: `optionsDirection` Not Working for Radio/Checkbox

**ID:** LAYOUT-001  
**Severity:** 🟡 Medium  
**Scenario:** 20, 21  
**Status:** ✅ **ALREADY FIXED** (2026-01-12)

**Problem:**  
Setting `optionsDirection: horizontal` on Radio/Checkbox components does not display options in a single row.

**Solution Applied:**  
Modified `frontend/src/features/builder/utils/objectRenderers.tsx`:
- Set individual option item `width` to `'auto'` for horizontal layouts
- Previously was `'100%'` which prevented horizontal wrapping

**Verification:** Needs re-testing in UAT

---

### Issue 6: Textarea Properties Already Exist

**ID:** PROP-001  
**Severity:** 🟡 Medium  
**Scenario:** 21  
**Status:** ✅ **ALREADY CONFIRMED** (2026-01-12)

**Problem:**  
`showCharacterCount`, `height`, and `resizeMode` properties were reported as missing.

**Resolution:**  
Confirmed these properties already exist in `TextareaPropertiesSection.tsx`:
- "Resize Mode" dropdown
- "Default Height" input
- "Max Characters" input
- "Show Character Count" toggle

**Action:** No code change needed. User may need to locate these in the Properties Panel.

---

### Issue 7: Submit Button Validation Messages

**ID:** VAL-002  
**Severity:** 🟡 Medium  
**Scenario:** 15  
**Status:** 🟡 To Fix

**Problem:**  
Submit button does not show validation messages when form has errors. When multiple required fields fail, users only see errors on individual components, not on the submit button.

**Proposed Solution:**

1. **Add validation message to submit button component:**
   - Submit button should have a validation object in its structure
   - When form has errors, show first error message (sorted by tabOrder)

2. **Implementation approach:**
   ```typescript
   // In submit button runtime component
   const sortedErrors = Object.entries(allFormErrors)
     .sort((a, b) => getComponentTabOrder(a[0]) - getComponentTabOrder(b[0]));
   
   const firstError = sortedErrors[0]?.[1];
   
   // Display firstError in validation area
   ```

3. **Alternative: Summary message:**
   - Show count: "2 fields require attention"
   - Less specific but always fits in one line

**Files to Modify:**
- `frontend/src/features/builder/registry/ComponentRegistry.tsx` (submit-button runtime)
- `frontend/src/features/renderer/components/PublicFormArtboard.tsx` (pass errors to submit)

**Estimated Effort:** 2-3 hours

---

### Issue 8: SmartBorder Sizing Issue for Radio

**ID:** LAYOUT-002  
**Severity:** 🟡 Medium  
**Scenario:** 20  
**Status:** 🟡 To Fix

**Problem:**  
Customer Type radio component has excessive whitespace next to radio values. SmartBorder appears wider than the content requires.

**Root Cause (Suspected):**  
SmartBorder may be:
- Including validation message area width incorrectly
- Using parent container width instead of content width
- Not recalculating after option changes

**Proposed Solution:**

1. **Investigate SmartBorder calculation:**
   - Check how SmartBorder determines its width
   - Ensure it wraps content tightly, not container

2. **Fix width calculation:**
   ```typescript
   // SmartBorder should use content width, not container width
   const borderWidth = Math.max(
     labelObjectWidth,
     inputObjectWidth,
     validationObjectWidth // Only if visible
   );
   ```

**Files to Modify:**
- `frontend/src/features/builder/components/SmartBorder.tsx` (if exists)
- `frontend/src/features/builder/components/UniversalFieldShell.tsx`

**Estimated Effort:** 2-3 hours

---

### Issue 9: Button Width/Align Not Working

**ID:** LAYOUT-003  
**Severity:** 🟡 Medium  
**Scenario:** 21  
**Status:** 🟡 To Fix

**Problem:**  
Setting `buttonWidth` to 100% and `buttonAlign` to center via Appearance → Dimensions does not visually update the Submit button.

**Root Cause (Suspected):**  
Button styling properties may not be applied in the action object renderer.

**Proposed Solution:**

1. **Check action renderer for button properties:**
   - In `objectRenderers.tsx`, ensure `buttonWidth` and `buttonAlign` are applied

2. **Apply styling:**
   ```typescript
   // In createActionRenderer
   const buttonStyle = {
     width: component.props.buttonWidth || 'auto',
     // Parent container needs justify-content for alignment
   };
   
   const containerStyle = {
     display: 'flex',
     justifyContent: component.props.buttonAlign || 'flex-start',
   };
   ```

**Files to Modify:**
- `frontend/src/features/builder/utils/objectRenderers.tsx`

**Estimated Effort:** 1-2 hours

---

### Issue 10: Initial Component State (Hidden/Disabled)

**ID:** PROP-002  
**Severity:** 🟡 Medium  
**Scenario:** 11, 17  
**Status:** 🟡 To Fix (or Defer)

**Problem:**  
Cannot preset a component's initial state (hidden/disabled) in builder. Components default to visible and enabled, making it impossible to test `show`/`enable` logic actions.

**Proposed Solution:**

1. **Add initial state properties to General section:**
   ```typescript
   // In GeneralSection.tsx
   <label>Initial Visibility</label>
   <select value={props.initialVisibility || 'visible'}>
     <option value="visible">Visible</option>
     <option value="hidden">Hidden</option>
   </select>
   
   <label>Initial State</label>
   <select value={props.initialState || 'enabled'}>
     <option value="enabled">Enabled</option>
     <option value="disabled">Disabled</option>
   </select>
   ```

2. **Apply in runtime:**
   - Before logic rules run, set component to initial state
   - Logic rules can then override (show/hide, enable/disable)

**Files to Modify:**
- `frontend/src/features/builder/components/properties/GeneralSection.tsx`
- `frontend/src/features/logic-engine/evaluateRules.ts`
- Component schema in `builder.types.ts`

**Estimated Effort:** 3-4 hours

**Alternative:** Defer to next story as it's an enhancement, not a bug.

---

### Issue 11: exportName Not Available for All Components

**ID:** PROP-003  
**Severity:** 🟢 Low  
**Scenario:** 21  
**Status:** 🟡 To Fix (or Defer)

**Problem:**  
Some components (e.g., Terms & Conditions checkbox) don't show the `exportName` field in the Properties Panel.

**Proposed Solution:**

1. **Add exportName to GeneralSection for all field components:**
   - Already exists for most fields
   - Ensure Terms & Conditions and other checkbox types include it

**Files to Modify:**
- `frontend/src/features/builder/components/properties/GeneralSection.tsx`

**Estimated Effort:** 30 minutes

---

## 🟢 LOW PRIORITY (Defer to Next Story)

### Issue 12: Missing Header/Paragraph Components

**ID:** COMP-001  
**Severity:** 🟢 Low  
**Status:** ⬜ Deferred

**Problem:**  
Header and Paragraph components are not available in the component toolbox.

**Decision:** Explicitly deferred - not required for current scope.

---

### Issue 13: Divider Not Visible During Drag

**ID:** UX-001  
**Severity:** 🟢 Low  
**Status:** ⬜ Defer

**Problem:**  
When dragging a Divider component, there is no visible component preview during the drag operation.

**Proposed Solution:**  
Add visual feedback in `DragOverlay` for Divider components.

**Decision:** Defer to polish story.

---

### Issue 14: Access Control UX Gaps

**ID:** ACCESS-001  
**Severity:** 📋 Specification Created  
**Status:** ⬜ Next Story

**Problem:**  
Multiple UX issues with form access controls.

**Resolution:**  
Comprehensive specification created: `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`

**Decision:** Implement in dedicated story after 3.8-3.9 completion.

---

## ✅ ALREADY FIXED (During Previous Sessions)

| Issue | Fix Applied | Date |
|-------|------------|------|
| Checkbox Equals/NotEquals Bug | Fixed array handling in `evaluateRules.ts` | 2026-01-12 |
| Contains Operator Substring Bug | User corrected rule to use `equals` | 2026-01-12 |
| Backend Schema Missing Operators | Added numeric operators to `LogicOperator` enum | 2026-01-12 |
| Security: LocalStorage Fallback | Fixed 403/404 error handling | 2026-01-12 |
| ReferenceError: actualStr | Fixed scoping in `evaluateRules.ts` | 2026-01-12 |
| Text Component inputWidthOverride | Fixed in `objectRenderers.tsx` | 2026-01-12 |
| Inline Validation Messages | Fixed conditional context and evaluation | 2026-01-12 |
| optionsDirection for Radio/Checkbox | Fixed option item width in `objectRenderers.tsx` | 2026-01-12 |

---

## Recommended Fix Order

### Phase 1: WYSIWYG Critical (1-2 hours)
1. ~~Issue 1: inputWidthOverride~~ ✅ Already Fixed
2. Issue 2: Width not updating in builder
3. Issue 3: Label wrapping (likely fixed by #2)

### Phase 2: Validation & UX (2-3 hours)
4. ~~Issue 4: Inline validation~~ ✅ Already Fixed
5. Issue 7: Submit button validation messages
6. ~~Issue 5: optionsDirection~~ ✅ Already Fixed

### Phase 3: Layout & Styling (2-3 hours)
7. Issue 8: SmartBorder sizing
8. Issue 9: Button width/align

### Phase 4: Properties (1-2 hours)
9. Issue 10: Initial component state (optional - can defer)
10. Issue 11: exportName for all components

### Total Estimated Effort: 6-10 hours

---

## Approval Checklist

Please review and approve each item:

| # | Issue | Proposed Solution | Approve? |
|---|-------|-------------------|----------|
| 1 | inputWidthOverride | ✅ Already fixed | ✅ |
| 2 | Width not updating in builder | Apply componentWidth on canvas surface | ⬜ |
| 3 | Label wrapping | Ensure labelWidth consistency | ⬜ |
| 4 | Inline validation | ✅ Already fixed | ✅ |
| 5 | optionsDirection | ✅ Already fixed | ✅ |
| 6 | Textarea properties | ✅ Already exists | ✅ |
| 7 | Submit button validation | Show first error by tabOrder | ⬜ |
| 8 | SmartBorder sizing | Fix width calculation | ⬜ |
| 9 | Button width/align | Apply in action renderer | ⬜ |
| 10 | Initial component state | Add properties to General section | ⬜ Defer? |
| 11 | exportName | Add to GeneralSection | ⬜ Defer? |
| 12 | Header/Paragraph | Deferred | ⬜ Defer |
| 13 | Divider drag preview | Deferred | ⬜ Defer |
| 14 | Access Control UX | Next story | ⬜ Defer |

---

## Notes

- Issues 2, 3, and 8 may share root cause (WYSIWYG canvas vs runtime styling)
- Issue 7 requires proper tabOrder on components
- Issues 10-14 can be safely deferred without blocking story completion
- After fixes, re-run Scenarios 15, 18, 20, 21, 22, 23, 24
