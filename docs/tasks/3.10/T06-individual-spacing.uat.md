# UAT Checklist: T06 - Individual Spacing Controls

**Story:** 3.10 - Grid Layout System  
**Task:** T06 - Individual Spacing Controls  
**Generated:** 2026-01-14  

---

## Pre-conditions

- [ ] Backend server is running
- [ ] Frontend is running (`npm run dev` in frontend directory)
- [ ] User is logged in to the form builder
- [ ] A form with at least one component exists
- [ ] Component has Grid Layout enabled (switch from Object Layout to Grid Layout)
- [ ] Grid has at least 2 rows and 2 columns configured

---

## Test Steps

### AC1: Individual Column Spacing Section Visible

**Objective:** Verify that the "Individual Column Spacing" section appears when grid has 2+ columns, shows correct number of sliders, and disappears when columns = 1.

- [ ] **Step 1:** Open Grid Layout section in Properties Panel for a component
- [ ] **Step 2:** Set grid to 1 column → Verify: "Individual Column Spacing" section does NOT appear (no gaps between single column)
- [ ] **Step 3:** Set grid to 2 columns → Verify: "Individual Column Spacing" section appears below Column Gap control (collapsed by default)
- [ ] **Step 4:** Click to expand "Individual Column Spacing" section → Verify: Shows 1 slider labeled "Col 0 → Col 1"
- [ ] **Step 5:** Set grid to 3 columns → Verify: Section shows 2 sliders: "Col 0 → Col 1" and "Col 1 → Col 2"
- [ ] **Step 6:** Set grid to 4 columns → Verify: Section shows 3 sliders: "Col 0 → Col 1", "Col 1 → Col 2", "Col 2 → Col 3"
- [ ] **Step 7:** Set grid back to 1 column → Verify: Section disappears

**Expected Result:** Section appears only when columns > 1, shows correct number of sliders (columns - 1), collapsed by default.

---

### AC2: Individual Row Spacing Section Visible

**Objective:** Verify that the "Individual Row Spacing" section appears when grid has 2+ rows, shows correct number of sliders, and disappears when rows = 1.

- [ ] **Step 1:** Set grid to 1 row → Verify: "Individual Row Spacing" section does NOT appear (no gaps between single row)
- [ ] **Step 2:** Set grid to 2 rows → Verify: "Individual Row Spacing" section appears below Row Gap control (collapsed by default)
- [ ] **Step 3:** Click to expand "Individual Row Spacing" section → Verify: Shows 1 slider labeled "Row 0 → Row 1"
- [ ] **Step 4:** Set grid to 3 rows → Verify: Section shows 2 sliders: "Row 0 → Row 1" and "Row 1 → Row 2"
- [ ] **Step 5:** Set grid to 4 rows → Verify: Section shows 3 sliders: "Row 0 → Row 1", "Row 1 → Row 2", "Row 2 → Row 3"
- [ ] **Step 6:** Set grid back to 1 row → Verify: Section disappears

**Expected Result:** Section appears only when rows > 1, shows correct number of sliders (rows - 1), collapsed by default.

---

### AC3: Adjusting Individual Gap Updates Config

**Objective:** Verify that changing an individual gap slider updates the config and grid preview.

- [ ] **Step 1:** Set grid to 3 columns, default column gap 8px
- [ ] **Step 2:** Expand "Individual Column Spacing" section
- [ ] **Step 3:** Adjust "Col 0 → Col 1" slider from 8px to 20px → Verify: Value display updates to "20px" and shows indigo color (custom)
- [ ] **Step 4:** Open browser DevTools → Inspect component props → Verify: `gridLayout.columnGaps` contains `{ 0: 20 }`
- [ ] **Step 5:** Verify: Grid preview shows larger gap between columns 0 and 1 (visually wider spacing)
- [ ] **Step 6:** Adjust "Col 1 → Col 2" slider to 4px → Verify: Config now has `columnGaps: { 0: 20, 1: 4 }`
- [ ] **Step 7:** Verify: Grid preview shows varying gaps (20px between col 0-1, 4px between col 1-2)
- [ ] **Step 8:** Repeat same test for row gaps:
  - Set grid to 3 rows, default row gap 8px
  - Expand "Individual Row Spacing" section
  - Adjust "Row 0 → Row 1" to 16px → Verify: `rowGaps: { 0: 16 }` in config
  - Verify: Grid preview shows larger gap below row 0

**Expected Result:** Individual gap changes update config immediately, grid preview reflects changes visually.

---

### AC4: Reset Button Reverts to Default Gap

**Objective:** Verify that Reset button appears for custom values and removes override when clicked.

- [ ] **Step 1:** Set grid to 3 columns, default column gap 8px
- [ ] **Step 2:** Expand "Individual Column Spacing" section
- [ ] **Step 3:** Adjust "Col 0 → Col 1" slider to 20px → Verify: "Reset" button appears next to slider
- [ ] **Step 4:** Verify: Value display shows "20px" in indigo color (custom indicator)
- [ ] **Step 5:** Click "Reset" button → Verify: Gap reverts to 8px (default column gap)
- [ ] **Step 6:** Verify: Value display shows "8px" in gray color (default indicator)
- [ ] **Step 7:** Verify: "Reset" button disappears
- [ ] **Step 8:** Open DevTools → Inspect config → Verify: `columnGaps[0]` is removed (no entry for index 0)
- [ ] **Step 9:** If `columnGaps` was only `{ 0: 20 }`, verify it becomes `undefined` (not empty object `{}`)
- [ ] **Step 10:** Repeat same test for row gaps:
  - Set "Row 0 → Row 1" to 16px → Verify Reset button appears
  - Click Reset → Verify reverts to default, button disappears, entry removed

**Expected Result:** Reset button appears only for custom values, removes override when clicked, config cleaned up properly.

---

### AC5: Individual Gaps Reflected in Grid Preview

**Objective:** Verify that the grid preview visually reflects individual gap overrides.

- [ ] **Step 1:** Set grid to 3 columns, default column gap 8px
- [ ] **Step 2:** Expand "Individual Column Spacing" section
- [ ] **Step 3:** Set "Col 0 → Col 1" to 24px (large gap) → Verify: Grid preview shows visibly wider gap between columns 0 and 1
- [ ] **Step 4:** Set "Col 1 → Col 2" to 4px (small gap) → Verify: Grid preview shows narrow gap between columns 1 and 2
- [ ] **Step 5:** Verify: Visual difference is clear (24px vs 4px vs 8px default)
- [ ] **Step 6:** Repeat for row gaps:
  - Set grid to 3 rows, default row gap 8px
  - Expand "Individual Row Spacing" section
  - Set "Row 0 → Row 1" to 20px → Verify: Larger vertical gap below row 0
  - Set "Row 1 → Row 2" to 4px → Verify: Smaller vertical gap below row 1
  - Verify: Visual difference is clear in grid preview

**Expected Result:** Grid preview accurately reflects individual gap overrides with visible spacing differences.

---

## Edge Cases

### EC1: Grid Resized to Fewer Columns

- [ ] **Step 1:** Set grid to 4 columns
- [ ] **Step 2:** Set "Col 0 → Col 1" to 20px, "Col 1 → Col 2" to 16px, "Col 2 → Col 3" to 12px
- [ ] **Step 3:** Verify: Config has `columnGaps: { 0: 20, 1: 16, 2: 12 }`
- [ ] **Step 4:** Reduce columns to 2 → Verify: Invalid entry `columnGaps[2]` is removed
- [ ] **Step 5:** Verify: Config now has `columnGaps: { 0: 20, 1: 16 }` (only valid indices remain)
- [ ] **Step 6:** Reduce columns to 1 → Verify: All `columnGaps` entries removed, becomes `undefined`

**Expected Result:** Invalid gap entries are automatically cleaned up when grid is resized.

### EC2: Grid Resized to Fewer Rows

- [ ] **Step 1:** Set grid to 4 rows
- [ ] **Step 2:** Set "Row 0 → Row 1" to 20px, "Row 1 → Row 2" to 16px, "Row 2 → Row 3" to 12px
- [ ] **Step 3:** Reduce rows to 2 → Verify: Invalid entry `rowGaps[2]` is removed
- [ ] **Step 4:** Verify: Config has `rowGaps: { 0: 20, 1: 16 }` (only valid indices remain)
- [ ] **Step 5:** Reduce rows to 1 → Verify: All `rowGaps` entries removed, becomes `undefined`

**Expected Result:** Invalid gap entries are automatically cleaned up when grid is resized.

### EC3: Set Individual Gap Same as Default

- [ ] **Step 1:** Set default column gap to 12px
- [ ] **Step 2:** Set "Col 0 → Col 1" to 20px (custom) → Verify: Entry exists in config
- [ ] **Step 3:** Adjust slider back to 12px (same as default) → Verify: Entry is automatically removed
- [ ] **Step 4:** Verify: Reset button disappears, value shows in gray (default color)
- [ ] **Step 5:** Verify: Config no longer has `columnGaps[0]` entry

**Expected Result:** Setting gap to default value automatically removes override entry.

### EC4: All Gaps Reset

- [ ] **Step 1:** Set multiple individual column gaps (e.g., `{ 0: 20, 1: 16 }`)
- [ ] **Step 2:** Click Reset on "Col 0 → Col 1" → Verify: Entry removed, config has `{ 1: 16 }`
- [ ] **Step 3:** Click Reset on "Col 1 → Col 2" → Verify: Config now has `columnGaps: undefined` (not empty object `{}`)
- [ ] **Step 4:** Verify: Section still shows sliders (they use default values)

**Expected Result:** When all overrides are removed, config property becomes `undefined` (clean config).

---

## Regression Check

- [ ] **Step 1:** Verify: Global Row Gap and Column Gap controls still work correctly
- [ ] **Step 2:** Verify: Grid structure controls (rows/columns) still work correctly
- [ ] **Step 3:** Verify: Grid preview still renders correctly with default gaps
- [ ] **Step 4:** Verify: Object drag-and-drop still works correctly
- [ ] **Step 5:** Verify: Cell merging still works correctly (if T05 completed)
- [ ] **Step 6:** Verify: Switching between Object Layout and Grid Layout still works

**Expected Result:** No regressions in existing Grid Layout functionality.

---

## Cleanup

- [ ] Reset grid to default configuration (3 rows, 1 column, 8px gaps)
- [ ] Close Properties Panel
- [ ] No cleanup needed (changes are component-specific)

---

## Test Results

**Tester:** Anthony Keevy  
**Date:** 2026-01-14  
**Status:** ✅ PASS  

**Notes:**
- All acceptance criteria passed
- All edge cases passed
- Regression checks passed
- Two UX enhancement opportunities identified (see uat-results.md):
  1. Screen flicker when Properties panel is narrow and Individual Column/Row Spacing is being changed
  2. Properties panel jumps to top when dragging objects from Grid Preview to Available Objects

---

*UAT checklist generated by Ralf-Dev*  
*Date: 2026-01-14*
