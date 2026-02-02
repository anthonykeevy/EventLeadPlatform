# UAT Checklist: T05 - Cell Merging

**Story:** 3.10 - Grid Layout System  
**Task:** T05 - Cell Merging  
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

### AC1: User Can Select Multiple Adjacent Cells

**Objective:** Verify that users can click cells to select them, with visual highlighting and toggle behavior.

- [ ] **Step 1:** Open Grid Layout section in Properties Panel for a component
- [ ] **Step 2:** Click on empty cell (0,0) → Verify: Cell shows blue border and light blue background (selection highlight)
- [ ] **Step 3:** Click on empty cell (0,1) → Verify: Both cells (0,0) and (0,1) now show selection highlight
- [ ] **Step 4:** Click on cell (0,0) again → Verify: Cell (0,0) deselected (no blue highlight), only (0,1) remains selected
- [ ] **Step 5:** Click on cell (1,0) → Verify: Both (0,1) and (1,0) are selected
- [ ] **Step 6:** Verify: Selection state is local (not persisted when closing/reopening properties panel)

**Expected Result:** Cells can be individually selected/deselected with clear visual feedback. Selection is temporary UI state.

---

### AC2: Merge Cells Button Appears for Valid Selection

**Objective:** Verify that merge button appears only for valid rectangular selections.

- [ ] **Step 1:** Select cells (0,0) and (0,1) → Verify: "Merge Cells" button appears above grid with "2 cells selected" text
- [ ] **Step 2:** Select cells (0,0), (0,1), (1,0), (1,1) → Verify: "Merge Cells" button appears (2×2 rectangle)
- [ ] **Step 3:** Select cells (0,0), (0,1), (1,0) → Verify: "Merge Cells" button is DISABLED (L-shape, invalid)
- [ ] **Step 4:** Hover over disabled button → Verify: Tooltip shows "Only rectangular selections can be merged"
- [ ] **Step 5:** Select only 1 cell → Verify: "Merge Cells" button does NOT appear
- [ ] **Step 6:** Click "Clear" button → Verify: Selection cleared, merge button disappears

**Expected Result:** Merge button appears for valid rectangular selections (2+ cells), disabled for invalid selections, hidden for single cell.

---

### AC3: Merging Creates a Merged Cell Group

**Objective:** Verify that merging creates a merged cell group and displays as single visual cell.

- [ ] **Step 1:** Select cells (0,0) and (0,1) (horizontal merge)
- [ ] **Step 2:** Click "Merge Cells" button → Verify: Cells visually merge into single cell spanning both columns
- [ ] **Step 3:** Open browser DevTools → Console → Verify: Log shows `gridlayout.cells.merged` event
- [ ] **Step 4:** Inspect component props → Verify: `gridLayout.mergedCells` contains new entry with both cell keys
- [ ] **Step 5:** Verify: Selection is cleared after merge (no blue highlights)
- [ ] **Step 6:** Verify: Merged cell shows thicker teal border and merge indicator icon (⧉) in top-right
- [ ] **Step 7:** Create 2×2 merge: Select (1,0), (1,1), (2,0), (2,1) → Click "Merge Cells" → Verify: 2×2 merged cell spans both rows and columns

**Expected Result:** Merged cells display as single visual unit with clear visual indicators. Config contains merge group entry.

---

### AC4: Objects in Merged Cells Span Correctly

**Objective:** Verify that objects placed in merged cells automatically span the merged area.

- [ ] **Step 1:** Create a 2×1 merged cell group (cells 0,0 and 0,1)
- [ ] **Step 2:** Drag "label" object from Available Objects pool into the merged area
- [ ] **Step 3:** Verify: Object appears spanning both columns in the merged cell
- [ ] **Step 4:** Inspect component props → Verify: `cellAssignments["0-0"] === "label"` (assigned to first cell only)
- [ ] **Step 5:** Inspect component props → Verify: `objectSpans["label"] === { rowSpan: 1, colSpan: 2 }`
- [ ] **Step 6:** Verify: Object visually spans entire merged area (not just first cell)
- [ ] **Step 7:** Create 2×2 merge, drag object → Verify: Object spans 2 rows × 2 columns correctly

**Expected Result:** Objects in merged cells automatically span the merged area. `objectSpans` config updated with correct span values.

---

### AC5: Unmerge Action Splits Merged Cells

**Objective:** Verify that unmerging restores cells to individual state.

- [ ] **Step 1:** Create merged cell group (cells 0,0 and 0,1) with "label" object inside
- [ ] **Step 2:** Click on merged cell → Verify: "Unmerge" button appears at bottom of merged cell
- [ ] **Step 3:** Click "Unmerge" button → Verify: Merged cells split back into individual cells
- [ ] **Step 4:** Verify: `mergedCells` entry removed from config (check DevTools)
- [ ] **Step 5:** Verify: "label" object remains in cell (0,0) only (first cell)
- [ ] **Step 6:** Verify: `objectSpans["label"]` entry removed from config
- [ ] **Step 7:** Verify: Cells display as separate units (no teal border, no merge indicator)

**Expected Result:** Unmerging restores cells to individual state. Object remains in first cell. Span configuration removed.

---

### AC6: L-Shaped Selections Cannot Merge (Validation)

**Objective:** Verify that non-rectangular selections cannot be merged.

- [ ] **Step 1:** Select cells (0,0), (0,1), (1,0) → Verify: Forms L-shape
- [ ] **Step 2:** Verify: "Merge Cells" button is DISABLED (grayed out)
- [ ] **Step 3:** Hover over disabled button → Verify: Tooltip shows "Only rectangular selections can be merged"
- [ ] **Step 4:** Try clicking disabled button → Verify: No merge occurs
- [ ] **Step 5:** Select non-adjacent cells: (0,0) and (0,2) → Verify: Button disabled (gap in selection)
- [ ] **Step 6:** Select valid rectangle: (0,0), (0,1) → Verify: Button enabled, merge succeeds

**Expected Result:** Invalid selections (L-shapes, gaps) cannot be merged. Button disabled with helpful tooltip.

---

## Regression Check

- [ ] **Step 1:** Verify existing drag-and-drop still works: Drag object to empty cell → Verify: Object assigned correctly
- [ ] **Step 2:** Verify object removal still works: Click × on object in cell → Verify: Object removed, returns to pool
- [ ] **Step 3:** Verify grid structure controls still work: Change rows/columns → Verify: Grid updates correctly
- [ ] **Step 4:** Verify gap controls still work: Adjust row/column gaps → Verify: Spacing updates correctly
- [ ] **Step 5:** Open browser console → Verify: No JavaScript errors
- [ ] **Step 6:** Check backend logs → Verify: No new errors

---

## Edge Cases

- [ ] **Edge Case 1:** Try merging cells that already contain different objects → Verify: Merge prevented (validation error)
- [ ] **Edge Case 2:** Try merging cells that are already part of another merge → Verify: Merge prevented (validation error)
- [ ] **Edge Case 3:** Merge cells, then resize grid to remove merged cells → Verify: Merged group removed, object returns to pool
- [ ] **Edge Case 4:** Select all cells in a row (e.g., 0,0 through 0,3) → Verify: Valid rectangle, merge succeeds
- [ ] **Edge Case 5:** Select all cells in a column (e.g., 0,0 through 3,0) → Verify: Valid rectangle, merge succeeds
- [ ] **Edge Case 6:** Merge cells, place object, then unmerge → Verify: Object stays in first cell, span removed

---

## Post-conditions

- [ ] Grid Layout editor still functional
- [ ] No console errors
- [ ] Component props contain valid `gridLayout` config
- [ ] Merged cells display correctly in grid preview
- [ ] Selection state cleared when closing properties panel

---

## DevTools MCP Verification (Optional)

If DevTools MCP is available, use these steps for automated verification:

1. **Navigate to builder page:**
   ```
   navigate_page to form builder
   ```

2. **Take snapshot to verify UI:**
   ```
   take_snapshot
   ```
   - Verify merge button appears when cells selected
   - Verify merged cells show visual indicators

3. **Check console messages:**
   ```
   list_console_messages
   ```
   - Verify no errors
   - Verify merge/unmerge events logged

4. **Evaluate component state:**
   ```
   evaluate_script: component.props.gridLayout.mergedCells
   ```
   - Verify merge groups exist in config

---

**Instructions for Human Tester:**

1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures or unexpected behavior
4. When complete, run `@ralf-uat *record-uat` with your results

---

*UAT Checklist generated by Ralf-Dev*  
*Date: 2026-01-14*
