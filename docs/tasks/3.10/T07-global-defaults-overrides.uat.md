# UAT Checklist: T07 - Global Defaults & Overrides

**Story:** 3.10 - Grid Layout System  
**Task ID:** T07  
**Date:** 2026-01-14

---

## Environment Setup

- [ ] Open form builder with at least one component that supports Grid Layout (e.g., text field)
- [ ] Ensure no components currently have `gridLayout` overrides (or note which ones do)

---

## Verification Steps

### AC1: Global Grid Defaults Section in GlobalStylesPanel

- [ ] **Step 1:** Deselect all components (click empty canvas area)
- [ ] **Step 2:** Open Global Styles panel (should be visible on right side)
- [ ] **Step 3:** Scroll to find "Grid Layout Defaults" section
- [ ] **Verify:** Section exists with icon (Grid3x3) and title "Grid Layout Defaults"
- [ ] **Step 4:** Verify controls present:
  - [ ] Default Rows (number input with +/- buttons, range 1-12)
  - [ ] Default Columns (number input with +/- buttons, range 1-12)
  - [ ] Default Row Gap (slider, range 0-48px, shows value)
  - [ ] Default Column Gap (slider, range 0-48px, shows value)
- [ ] **Step 5:** Change Default Rows to 4
- [ ] **Verify:** Value updates immediately, input shows "4"
- [ ] **Step 6:** Change Default Columns to 2
- [ ] **Verify:** Value updates immediately, input shows "2"
- [ ] **Step 7:** Adjust Default Row Gap slider to 12px
- [ ] **Verify:** Slider moves, value display shows "12px"
- [ ] **Step 8:** Adjust Default Column Gap slider to 16px
- [ ] **Verify:** Slider moves, value display shows "16px"

---

### AC2: Components Inherit Global Defaults

- [ ] **Step 1:** Set global defaults (from AC1): rows=4, columns=2, rowGap=12, columnGap=16
- [ ] **Step 2:** Select a component that supports Grid Layout (e.g., text field)
- [ ] **Step 3:** Click "Grid Layout" button in Layout Mode section
- [ ] **Step 4:** Verify component switches to Grid Layout mode
- [ ] **Step 5:** Check Grid Structure controls
- [ ] **Verify:** Rows shows "4", Columns shows "2"
- [ ] **Step 6:** Check Gap controls
- [ ] **Verify:** Row Gap shows "12px", Column Gap shows "16px"
- [ ] **Step 7:** Check component props using one of these methods:
  - **Method C (Console - Recommended):** In browser console, run:
    ```javascript
    const store = window.__ZUSTAND_STORE__;
    const component = store?.getState()?.getSelectedComponent?.();
    console.log('gridLayout:', component?.props?.gridLayout);
    ```
    Expected output: `gridLayout: undefined`
  - **Method B (Visual Check - Easiest):** Look at the badge in GridLayoutSection - it should show "🌐 Using Global Default" (not "🔧 Component Override")
  - **Method A (React DevTools):** Install React DevTools extension → Components tab → Select the FormComponent → In right panel, expand `props` → Look for `gridLayout` property (should be `undefined` or not present)
- [ ] **Verify:** `component.props.gridLayout` is `undefined` (component inheriting from global) OR badge shows "🌐 Using Global Default"
- [ ] **Step 8:** Look at canvas preview
- [ ] **Verify:** Component displays 4×2 grid structure (if objects are assigned)

---

### AC3: Component Override Takes Precedence

- [ ] **Step 1:** Set global defaults: rows=3, columnGap=8 (leave other values as default)
- [ ] **Step 2:** Select a component using Grid Layout mode
- [ ] **Step 3:** Click "Override Global" button
- [ ] **Verify:** Badge changes from "🌐 Using Global Default" to "🔧 Component Override"
- [ ] **Step 4:** Change Rows to 5 (using +/- buttons or direct input)
- [ ] **Verify:** Rows value updates to 5
- [ ] **Step 5:** Check Columns value
- [ ] **Verify:** Columns shows "1" (inherited from global default)
- [ ] **Step 6:** Check Column Gap value
- [ ] **Verify:** Column Gap shows "8px" (inherited from global default)
- [ ] **Step 7:** Check component props using one of these methods:
  - **Method C (Console - Recommended):** In browser console, run:
    ```javascript
    const store = window.__ZUSTAND_STORE__;
    const component = store?.getState()?.getSelectedComponent?.();
    console.log('gridLayout:', component?.props?.gridLayout);
    console.log('rows:', component?.props?.gridLayout?.rows);
    console.log('columns:', component?.props?.gridLayout?.columns);
    ```
    Expected output: `gridLayout: {rows: 5, ...}`, `rows: 5`, `columns: undefined`
  - **Method B (Visual Check - Easiest):** Look at the badge in GridLayoutSection - it should show "🔧 Component Override" (indigo badge)
  - **Method A (React DevTools):** Install React DevTools extension → Components tab → Select the FormComponent → In right panel, expand `props` → Look for `gridLayout` property → Expand it to see `rows: 5`
- [ ] **Verify:** `component.props.gridLayout` exists and has `rows: 5`
- [ ] **Verify:** `component.props.gridLayout.columns` is `undefined` (will inherit from global)
- [ ] **Verify:** Effective display shows rows=5, columns=1, columnGap=8

---

### AC4: "Override Global" and "Reset to Global" Actions

#### Test Override Global

- [ ] **Step 1:** Select a component using Grid Layout mode with global defaults (no override)
- [ ] **Verify:** Badge shows "🌐 Using Global Default" (gray background)
- [ ] **Verify:** "Override Global" button is visible
- [ ] **Verify:** "Reset to Global" button is NOT visible
- [ ] **Step 2:** Note current global default values (e.g., rows=4, columns=2, rowGap=12, columnGap=16)
- [ ] **Step 3:** Click "Override Global" button
- [ ] **Verify:** Badge changes to "🔧 Component Override" (indigo background)
- [ ] **Verify:** "Override Global" button disappears
- [ ] **Verify:** "Reset to Global" button appears
- [ ] **Step 4:** Check Grid Structure controls
- [ ] **Verify:** Values match the global defaults that were set (rows=4, columns=2, etc.)
- [ ] **Step 5:** Check component props using one of these methods:
  - **Method A (React DevTools):** Install React DevTools extension → Select component in Components tab → Check `props.gridLayout` in right panel
  - **Method B (Visual Check):** Look at the badge - it should show "🔧 Component Override" (indigo badge)
  - **Method C (Console):** In browser console, run:
    ```javascript
    // Access Zustand store (if exposed)
    const store = window.__ZUSTAND_STORE__;
    const component = store?.getState()?.getSelectedComponent?.();
    console.log('gridLayout:', component?.props?.gridLayout);
    ```
- [ ] **Verify:** `component.props.gridLayout` now exists with values matching global defaults OR badge shows "🔧 Component Override"

#### Test Reset to Global

- [ ] **Step 1:** With component override active (from previous test)
- [ ] **Verify:** Badge shows "🔧 Component Override" (indigo background)
- [ ] **Verify:** "Reset to Global" button is visible
- [ ] **Step 2:** Change some values (e.g., Rows to 6, Column Gap to 20)
- [ ] **Step 3:** Click "Reset to Global" button
- [ ] **Verify:** Badge changes back to "🌐 Using Global Default" (gray background)
- [ ] **Verify:** "Reset to Global" button disappears
- [ ] **Verify:** "Override Global" button appears
- [ ] **Step 4:** Check Grid Structure controls
- [ ] **Verify:** Values return to global defaults (not the overridden values)
- [ ] **Step 5:** Check component props using one of these methods:
  - **Method C (Console - Recommended):** In browser console, run:
    ```javascript
    const store = window.__ZUSTAND_STORE__;
    const component = store?.getState()?.getSelectedComponent?.();
    console.log('gridLayout:', component?.props?.gridLayout);
    ```
    Expected output: `gridLayout: undefined`
  - **Method B (Visual Check - Easiest):** Look at the badge - it should show "🌐 Using Global Default" (gray badge)
  - **Method A (React DevTools):** Install React DevTools extension → Components tab → Select the FormComponent → In right panel, expand `props` → `gridLayout` should be `undefined` or not present
- [ ] **Verify:** `component.props.gridLayout` is `undefined` (component now uses global defaults) OR badge shows "🌐 Using Global Default"

---

### AC5: Override Indicator When Component Differs

- [ ] **Step 1:** Select a component with no gridLayout override (using global defaults)
- [ ] **Verify:** Badge shows "🌐 Using Global Default"
- [ ] **Verify:** Badge has gray background (`bg-gray-100` / `bg-gray-800`)
- [ ] **Verify:** Badge text is gray (`text-gray-600` / `text-gray-400`)
- [ ] **Step 2:** Click "Override Global" to create override
- [ ] **Verify:** Badge changes to "🔧 Component Override"
- [ ] **Verify:** Badge has indigo background (`bg-indigo-100` / `bg-indigo-900/30`)
- [ ] **Verify:** Badge text is indigo (`text-indigo-700` / `text-indigo-300`)
- [ ] **Step 3:** Verify badge is visible in GridLayoutSection header area (above Grid Structure controls)

---

## Regression Check

- [ ] **Step 1:** Create a new component
- [ ] **Verify:** Component can switch between Object Layout and Grid Layout modes
- [ ] **Step 2:** Set global defaults, then create component override
- [ ] **Verify:** Component override values are preserved when switching away and back
- [ ] **Step 3:** Test with multiple components
- [ ] **Verify:** Each component can have independent overrides
- [ ] **Verify:** Components without overrides all use global defaults
- [ ] **Step 4:** Change global defaults
- [ ] **Verify:** Components with overrides are NOT affected
- [ ] **Verify:** Components without overrides ARE affected

---

## Edge Cases

- [ ] **Test:** No global default set (all values undefined)
- [ ] **Verify:** Component uses system defaults (3 rows, 1 column, 8px gaps)

- [ ] **Test:** Global default partially set (e.g., only rows defined)
- [ ] **Verify:** Component inherits defined values, uses system defaults for undefined

- [ ] **Test:** Component override with partial values (e.g., only rows)
- [ ] **Verify:** Missing values inherit from global, then system defaults

- [ ] **Test:** Switch from Grid Layout to Object Layout
- [ ] **Verify:** `gridLayout` cleared, global defaults have no effect

---

## Cleanup

- [ ] Reset global defaults to reasonable values (if needed)
- [ ] Remove any test component overrides (if desired)

---

## Test Results

**Tester:** _________________  
**Date:** _________________  
**Status:** [ ] PASS [ ] FAIL

**Notes:**
- 

---

*UAT checklist auto-generated by Ralf-Dev*  
*Date: 2026-01-14*
