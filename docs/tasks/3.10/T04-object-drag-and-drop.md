# Task T04: Object Drag-and-Drop

**Story:** 3.10 - Grid Layout System  
**Task ID:** T04  
**Status:** ⏳ Ready  
**Dependencies:** T03 ✅  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Add drag-and-drop functionality to the Grid Layout editor, allowing users to assign component objects (label, input, validation, help) to grid cells.

**User Story:** As a form builder user, I want to drag objects from an "Available Objects" pool onto grid cells so that I can visually arrange component elements in a grid layout.

---

## ✅ Scope (In)

- [ ] Display "Available Objects" pool showing unassigned objects from component structure
- [ ] Make grid cells droppable targets for objects
- [ ] Allow dragging objects from pool to empty grid cells
- [ ] Allow moving objects between cells (drag from one cell to another)
- [ ] Allow returning objects to pool (drag out of cell or click remove button)
- [ ] Update `cellAssignments` in `GridLayoutConfig` on every drop action
- [ ] Visual feedback: highlight valid drop zones during drag
- [ ] Ensure single placement: each object can only be in one cell at a time

---

## ❌ Scope (Out)

- Cell merging UI (T05)
- Individual row/column spacing controls (T06)
- Global defaults integration (T07)
- Multi-select objects
- Undo/redo for DnD operations (handled by existing undo system)
- Keyboard-only object assignment

---

## 🚫 Forbidden Zones

| Zone | Reason |
|------|--------|
| `backend/` | No backend changes |
| `database/` | No schema changes |
| `UniversalFieldShell.tsx` | Rendering only (T02 complete) |
| `ObjectLayoutSection.tsx` | Different layout system |
| `gridLayoutUtils.ts` | Utilities frozen (T01 complete) |

---

## 🎯 Acceptance Criteria

### AC1: Available Objects Pool Displayed

**Criterion:** When Grid Layout is active, display an "Available Objects" section showing all objects from the component's structure that are NOT currently assigned to any cell.

**Verification:**
- Open Properties Panel for component with Grid Layout enabled
- Verify "Available Objects" section appears
- Verify it lists only unassigned objects (label, input, validation, help as applicable)
- Verify assigned objects do NOT appear in pool

**Implementation Notes:**
- Get objects from `structure.objects` array (already passed to component)
- Filter out objects that exist in `config.cellAssignments` values
- Display each with draggable grip handle and object label

---

### AC2: Objects Can Be Dragged to Empty Cells

**Criterion:** User can drag an object from the Available Objects pool and drop it onto an empty grid cell. The cell should visually highlight as a valid drop zone.

**Verification:**
- Start dragging an object from pool
- Verify empty cells highlight (e.g., blue border or background)
- Drop on empty cell
- Verify object appears in cell
- Verify object removed from pool
- Verify `config.cellAssignments` updated with new `"row-col": "objectId"` entry

**Implementation Notes:**
- Use `@dnd-kit` library (already in project)
- Reference `ObjectLayoutSection.tsx` for DnD patterns
- Use `useDroppable` hook for each cell
- Use `useDraggable` or `useSortable` for objects

---

### AC3: Objects Can Be Moved Between Cells

**Criterion:** User can drag an object from one cell to another empty cell to reposition it.

**Verification:**
- Assign an object to a cell (via AC2)
- Drag object from that cell to a different empty cell
- Verify object moves to new cell
- Verify old cell becomes empty
- Verify `cellAssignments` updated correctly

**Implementation Notes:**
- Objects in cells should also be draggable
- On drop: remove old assignment, add new assignment
- Key formula: `cellKey(row, col)` returns `"row-col"` format

---

### AC4: Objects Can Be Removed From Cells

**Criterion:** User can remove an object from a cell, returning it to the Available Objects pool.

**Verification:**
- Object is assigned to a cell
- User can remove it via:
  - Option A: Drag to "Available Objects" pool (if droppable pool exists)
  - Option B: Click X/remove button on the object
- Verify object returns to Available Objects pool
- Verify cell becomes empty
- Verify `cellAssignments` entry removed

**Implementation Notes:**
- Recommended: Add small X button to objects in cells
- On remove: `delete cellAssignments[cellKey]`

---

### AC5: Single Placement Enforced

**Criterion:** Each object can only be placed in ONE cell at a time. If an object is dragged to a new cell while already assigned, it moves (not duplicates).

**Verification:**
- Assign "label" to cell (0,0)
- Drag "label" to cell (1,1)
- Verify "label" is ONLY in cell (1,1)
- Verify cell (0,0) is empty
- Verify only one `cellAssignments` entry for "label"

**Implementation Notes:**
- Before adding new assignment, check if objectId exists in any value
- If found, delete the old assignment first
- Use helper: `findCellForObject(objectId, config)` from T01 utilities

---

## 🔧 Implementation Details

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `GridLayoutSection.tsx` | Modify | Add Available Objects pool UI, integrate with DnD context |
| `GridLayoutEditor.tsx` | Modify | Make cells droppable, add DnD context wrapper |

### New Components (optional - can be inline)

| Component | Purpose |
|-----------|---------|
| `DraggableGridObject` | Draggable object item for pool and cells |
| `DroppableGridCell` | Cell that accepts dropped objects |

### DnD Architecture

```typescript
// Wrap entire Grid Layout section in DndContext
<DndContext
    sensors={sensors}
    collisionDetection={closestCenter}
    onDragStart={handleDragStart}
    onDragEnd={handleDragEnd}
>
    {/* Available Objects Pool */}
    <SortableContext items={availableObjectIds}>
        {availableObjects.map(obj => (
            <DraggableGridObject key={obj.id} id={obj.id} label={obj.label} />
        ))}
    </SortableContext>
    
    {/* Grid Preview with Droppable Cells */}
    <div style={gridStyles}>
        {cells.map(cell => (
            <DroppableGridCell
                key={cell.key}
                row={cell.row}
                col={cell.col}
                objectId={cell.objectId}
                onRemove={() => handleRemoveObject(cell.key)}
            />
        ))}
    </div>
    
    {/* Drag Overlay */}
    <DragOverlay>
        {activeId ? <DragOverlayItem id={activeId} /> : null}
    </DragOverlay>
</DndContext>
```

### Key Functions

```typescript
// Handle drag end - main logic
function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    
    if (!over) return; // Dropped outside valid zone
    
    const objectId = active.id as string;
    const targetCellKey = over.id as string;
    
    // Build new cellAssignments
    const newAssignments = { ...currentGridConfig.cellAssignments };
    
    // Remove object from current position (if any)
    for (const [key, id] of Object.entries(newAssignments)) {
        if (id === objectId) {
            delete newAssignments[key];
            break;
        }
    }
    
    // If dropped on a cell (not pool), assign to new cell
    if (targetCellKey !== 'available-pool') {
        newAssignments[targetCellKey] = objectId;
    }
    
    // Update config
    handleGridConfigChange({ cellAssignments: newAssignments });
}

// Handle remove button click
function handleRemoveObject(cellKey: string) {
    const newAssignments = { ...currentGridConfig.cellAssignments };
    delete newAssignments[cellKey];
    handleGridConfigChange({ cellAssignments: newAssignments });
}
```

### Visual States

| State | Visual Treatment |
|-------|------------------|
| Empty cell (not dragging) | Dashed gray border |
| Empty cell (valid drop target) | Solid blue/teal border, light background |
| Cell with object | Solid teal border, object label displayed |
| Object being dragged | Semi-transparent original, solid overlay following cursor |
| Invalid drop zone | No highlight |

---

## 🧪 Required Tests

### Manual Verification

1. **Pool Display**
   - Switch to Grid Layout mode
   - Verify Available Objects pool shows objects from component structure
   
2. **Drag to Cell**
   - Drag "label" from pool to cell (0,0)
   - Verify visual feedback during drag
   - Verify "label" appears in cell after drop
   
3. **Move Between Cells**
   - Drag "label" from cell (0,0) to cell (1,0)
   - Verify cell (0,0) is now empty
   - Verify "label" is in cell (1,0)
   
4. **Remove from Cell**
   - Click remove button on "label" in cell (1,0)
   - Verify "label" returns to Available Objects pool
   - Verify cell (1,0) is empty

### Build Verification

```bash
# Check for linter errors
ReadLints tool on changed files

# Check app loads (use DevTools MCP)
navigate_page to http://localhost:3000/builder
list_console_messages - no errors
```

### State Verification (DevTools MCP)

```javascript
// Verify cellAssignments in component props
evaluate_script: `
    const store = window.__ZUSTAND_DEVTOOLS__;
    const component = store.getState().components.find(c => c.id === 'COMPONENT_ID');
    console.log(JSON.stringify(component.props.gridLayout.cellAssignments, null, 2));
`
```

---

## 📚 References

- **DnD Pattern Reference:** `frontend/src/features/builder/components/properties/ObjectLayoutSection.tsx`
- **Grid Layout Spec:** `docs/GRID-LAYOUT-GUIDE.md` (sections 3 "Assigning Objects to Grid Cells")
- **T01 Utilities:** `frontend/src/features/builder/utils/gridLayoutUtils.ts`
- **T03 UI Base:** `frontend/src/features/builder/components/properties/GridLayoutSection.tsx`

---

## ⚠️ Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Component has no objects | Show empty "Available Objects" section with message |
| All objects assigned | Available Objects pool is empty |
| Drop on occupied cell | Do nothing (prevent drop or swap - recommend prevent) |
| Drag outside any zone | Cancel drag, return to original position |
| Grid resized to fewer cells | Objects in removed cells return to pool |

---

## 📝 Handoff Requirements

On completion, provide:
1. `T04-object-drag-and-drop.completion.md` with:
   - Files changed
   - AC verification evidence
   - Build/lint verification
2. `T04-object-drag-and-drop.uat.md` with:
   - Step-by-step manual test instructions
   - DevTools MCP verification steps

---

*Task Spec created by PM Agent*  
*Date: 2026-01-14*
