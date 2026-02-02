# UAT Checklist: T03

**Story:** 3.10 - Grid Layout System  
**Task:** T03 - Basic Grid Editor UI  
**Generated:** 2026-01-14

---

## Pre-conditions

- [ ] Backend server is running (`cd backend && python -m uvicorn main:app --reload`)
- [ ] Frontend is running (`cd frontend && npm run dev`)
- [ ] User is logged in to the Form Builder
- [ ] A form exists or can be created

## Test Steps

### AC1: Grid Layout option appears in Properties Panel

- [ ] Step 1: Create a new form or open an existing form in the Builder
- [ ] Step 2: Drag a "First Name" or "Text" component onto the canvas
- [ ] Step 3: Click to select the component
- [ ] Step 4: Look at the Properties Panel on the right
  → **Verify:** A "Layout Mode" section appears with a grid icon
  → **Verify:** Two buttons visible: "Object Layout" and "Grid Layout"

### AC2: User can switch between Object Layout and Grid Layout

- [ ] Step 1: With component selected, confirm "Object Layout" button is highlighted (teal border)
- [ ] Step 2: Click the "Grid Layout" button
  → **Verify:** "Grid Layout" button becomes highlighted (indigo border)
  → **Verify:** Object Layout button is no longer highlighted
  → **Verify:** The "Object Layout" detailed section (with Vertical/Horizontal/Mixed) disappears
  → **Verify:** Grid configuration controls appear (Rows, Columns, Gap sliders, Preview)
- [ ] Step 3: Click "Object Layout" button again
  → **Verify:** "Object Layout" button becomes highlighted again
  → **Verify:** Grid configuration controls disappear
  → **Verify:** Object Layout section reappears

### AC3: Grid preview displays correct number of rows × columns

- [ ] Step 1: Switch to Grid Layout mode
- [ ] Step 2: Note the default grid preview (should be 3 rows × 1 column = 3 cells)
  → **Verify:** Preview shows 3 cell boxes stacked vertically
  → **Verify:** Header shows "3 rows × 1 col"
- [ ] Step 3: Click the "+" button next to Columns
  → **Verify:** Preview now shows 3 rows × 2 columns = 6 cells
  → **Verify:** Header updates to "3 rows × 2 cols"
- [ ] Step 4: Change Rows to 4 (using number input or + button)
  → **Verify:** Preview shows 4 rows × 2 columns = 8 cells
- [ ] Step 5: Set Rows=2, Columns=3
  → **Verify:** Preview shows 2 rows × 3 columns = 6 cells in a 2×3 grid
- [ ] Step 6: Try setting Rows to 12 (maximum)
  → **Verify:** Value is accepted, preview shows 12 rows
- [ ] Step 7: Try setting Rows to 0 or negative
  → **Verify:** Value is clamped to minimum of 1

### AC4: Gap sliders adjust spacing visually

- [ ] Step 1: In Grid Layout mode with 2×2 or larger grid
- [ ] Step 2: Note the current Row Gap value (default: 8px)
- [ ] Step 3: Drag the Row Gap slider to the right (increase)
  → **Verify:** The gap value display updates (e.g., "16px", "24px")
  → **Verify:** Visual spacing between rows in the preview increases
- [ ] Step 4: Drag the Row Gap slider to 0
  → **Verify:** Value shows "0px"
  → **Verify:** Rows appear closer together in preview
- [ ] Step 5: Drag the Column Gap slider to increase spacing
  → **Verify:** Visual spacing between columns increases in preview
  → **Verify:** Value display updates accordingly
- [ ] Step 6: Set Row Gap to max (48px)
  → **Verify:** Maximum value is 48px, slider stops there

### AC5: Config saves to component.props.gridLayout

- [ ] Step 1: Open browser DevTools (F12) → React DevTools tab
- [ ] Step 2: With component selected in Grid Layout mode
- [ ] Step 3: Navigate to the component in React DevTools
- [ ] Step 4: Inspect the component's props
  → **Verify:** `props.gridLayout` object exists
  → **Verify:** Contains `rows` property matching UI value
  → **Verify:** Contains `columns` property matching UI value
  → **Verify:** Contains `rowGap` property matching UI value
  → **Verify:** Contains `columnGap` property matching UI value
  → **Verify:** Contains `cellAssignments` property (empty object `{}` is OK)
- [ ] Step 5: Change rows in the UI
  → **Verify:** `props.gridLayout.rows` updates in DevTools
- [ ] Step 6: Switch to Object Layout mode
  → **Verify:** `props.gridLayout` becomes `undefined`

## Regression Check

- [ ] Verify Object Layout section still works when in Object Layout mode
- [ ] Verify switching between Vertical/Horizontal/Mixed still works (in Object Layout mode)
- [ ] Verify other Properties Panel sections (General, Validation, Appearance) still work
- [ ] No console errors in browser during layout mode switching
- [ ] No console errors when adjusting grid controls

## Edge Cases

- [ ] Try rapidly clicking between Object Layout and Grid Layout
  → **Verify:** No errors, UI stays consistent
- [ ] Select a different component type (e.g., Submit Button)
  → **Verify:** Layout Mode section should NOT appear for button components
- [ ] Select divider component
  → **Verify:** Layout Mode section should NOT appear

## Post-conditions

- [ ] Component's gridLayout config persists when de-selecting and re-selecting
- [ ] Switching to Grid Layout and back to Object Layout clears gridLayout

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
