# Task T04: Object Drag-and-Drop - UAT Checklist

**Story:** 3.10 - Grid Layout System  
**Task ID:** T04  
**UAT Type:** Manual Verification  

---

## 🔧 Environment Setup

- [ ] Frontend dev server running (`npm run dev` in frontend/)
- [ ] Backend server running (if needed for form loading)
- [ ] Browser DevTools console open
- [ ] Navigate to Form Builder: `http://localhost:3000/builder`

---

## 📋 Pre-Test Setup

1. [ ] Select or create a form with at least one component (e.g., First Name field)
2. [ ] Click on a component to select it
3. [ ] Locate the Properties Panel on the right side

---

## ✅ AC1: Available Objects Pool Displayed

**Steps:**
1. [ ] In Properties Panel, find "Layout Mode" section
2. [ ] Click "Grid Layout" button to enable Grid Layout mode
3. [ ] Verify "Available Objects" section appears with Package icon
4. [ ] Verify objects from component structure are listed (e.g., "label", "input", "validation")

**Expected Result:**
- Available Objects pool shows all unassigned objects
- Each object has a grip handle (⠿) for dragging
- Objects use gray/neutral styling (not assigned yet)

**Verification:**
- [ ] Pool visible when Grid Layout is active
- [ ] Correct objects listed based on component type
- [ ] Empty message shows when all objects assigned

---

## ✅ AC2: Objects Can Be Dragged to Empty Cells

**Steps:**
1. [ ] Grid should show empty cells with dashed borders (e.g., 3 rows × 1 column default)
2. [ ] Start dragging "label" object from Available Objects pool
3. [ ] Hover over an empty cell
4. [ ] Verify cell highlights (indigo border, tinted background, shows "Drop here")
5. [ ] Drop the object on the cell
6. [ ] Verify object appears in the cell with grip handle and X button
7. [ ] Verify object is removed from Available Objects pool

**Expected Result:**
- Empty cells show visual drop zone feedback when hovering
- Object moves from pool to cell on drop
- Pool updates to reflect assignment

**Verification:**
- [ ] Drag feedback visible during drag
- [ ] Drop zone highlight on hover
- [ ] Object appears in cell after drop
- [ ] Pool updated (object removed)

---

## ✅ AC3: Objects Can Be Moved Between Cells

**Steps:**
1. [ ] Ensure at least one object is assigned to a cell (from AC2)
2. [ ] Start dragging the object from its current cell
3. [ ] Hover over a different empty cell
4. [ ] Verify new cell highlights as drop zone
5. [ ] Drop the object on the new cell
6. [ ] Verify object is now in new cell
7. [ ] Verify old cell is now empty (dashed border)

**Expected Result:**
- Object can be moved from one cell to another
- Old cell becomes empty
- Single placement: object only exists in one cell

**Verification:**
- [ ] Object draggable from cell
- [ ] Old cell empty after move
- [ ] New cell contains object

---

## ✅ AC4: Objects Can Be Removed From Cells

**Option A: Remove via X Button**
1. [ ] Ensure at least one object is in a cell
2. [ ] Click the X button on the object (right side)
3. [ ] Verify object is removed from cell
4. [ ] Verify object reappears in Available Objects pool
5. [ ] Verify cell shows empty state (dashed border)

**Option B: Drag Back to Pool**
1. [ ] Ensure at least one object is in a cell
2. [ ] Start dragging the object from the cell
3. [ ] Drop it on the Available Objects pool area
4. [ ] Verify object is removed from cell
5. [ ] Verify object reappears in pool

**Expected Result:**
- Both methods return object to pool
- Cell becomes empty

**Verification:**
- [ ] X button removes object
- [ ] Drag to pool removes object
- [ ] Object returns to pool
- [ ] Cell shows empty state

---

## ✅ AC5: Single Placement Enforced

**Steps:**
1. [ ] Assign "label" object to cell (0,0)
2. [ ] Drag "label" from cell (0,0) to cell (1,0) 
3. [ ] Drop it on cell (1,0)
4. [ ] Verify "label" is ONLY in cell (1,0)
5. [ ] Verify cell (0,0) is empty
6. [ ] Check console: should NOT show duplicate assignment

**Additional Check - Occupied Cell Prevention:**
1. [ ] Assign "label" to cell (0,0)
2. [ ] Assign "input" to cell (1,0)
3. [ ] Try to drag "label" onto cell (1,0) which has "input"
4. [ ] Verify drop is prevented or blocked
5. [ ] Check console for `gridlayout.drop.blocked` log

**Expected Result:**
- Objects cannot exist in multiple cells
- Moving to occupied cell is blocked
- No duplicate entries in cellAssignments

**Verification:**
- [ ] Object exists in only one cell after move
- [ ] Old cell becomes empty
- [ ] Cannot drop on occupied cell

---

## 🔍 Edge Cases

### Empty Component (No Objects)
1. [ ] Select a component type with no objects (if available)
2. [ ] Enable Grid Layout
3. [ ] Verify Available Objects pool shows empty message

### All Objects Assigned
1. [ ] Assign all available objects to cells
2. [ ] Verify Available Objects pool shows "All objects assigned to grid cells" message
3. [ ] Verify objects can still be moved between cells or removed

### Grid Resize with Assigned Objects
1. [ ] Assign objects to cells (e.g., in a 3×1 grid)
2. [ ] Reduce grid rows to 2
3. [ ] Check if objects in removed rows return to pool (edge case for T03 integration)

---

## 🖥️ Console Verification

Open browser DevTools console and verify logging:

1. [ ] Drag start: `gridlayout.drag.start` with objectId
2. [ ] Object assigned: `gridlayout.object.assigned` with objectId and targetCell
3. [ ] Object removed: `gridlayout.object.removed` with objectId and fromCell
4. [ ] Object returned to pool: `gridlayout.object.returned`
5. [ ] Drop blocked: `gridlayout.drop.blocked` when dropping on occupied cell

---

## 🔄 Regression Check

1. [ ] Object Layout mode still works (toggle back to Object Layout)
2. [ ] Grid structure controls (rows, columns) still work
3. [ ] Gap controls still work
4. [ ] Grid preview updates correctly with changes
5. [ ] No console errors during any operation

---

## 📝 Test Summary

| Test | Result |
|------|--------|
| AC1: Available Objects Pool | ⬜ Pass / ⬜ Fail |
| AC2: Drag to Empty Cells | ⬜ Pass / ⬜ Fail |
| AC3: Move Between Cells | ⬜ Pass / ⬜ Fail |
| AC4: Remove from Cells | ⬜ Pass / ⬜ Fail |
| AC5: Single Placement | ⬜ Pass / ⬜ Fail |
| Edge Cases | ⬜ Pass / ⬜ Fail |
| Console Logging | ⬜ Pass / ⬜ Fail |
| Regression Check | ⬜ Pass / ⬜ Fail |

---

## 📋 UAT Sign-Off

**Tester:** _________________  
**Date:** _________________  
**Result:** ⬜ PASS / ⬜ FAIL  

**Notes:**
```
[Add any observations, issues, or feedback here]
```

---

*UAT Checklist generated by Ralf-Dev*  
*Date: 2026-01-14*
