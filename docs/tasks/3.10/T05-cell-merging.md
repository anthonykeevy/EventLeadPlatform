# Task T05: Cell Merging

**Story:** 3.10 - Grid Layout System  
**Task ID:** T05  
**Status:** ⏳ Ready  
**Dependencies:** T04 ✅  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Add cell selection and merging functionality to allow users to merge multiple adjacent grid cells into a single larger cell for object spanning.

**User Story:** As a form builder user, I want to select multiple adjacent cells and merge them so that an object can span across multiple rows or columns.

---

## ✅ Scope (In)

- [ ] Add cell selection state management (track selected cells)
- [ ] Add click-to-select for individual cells (toggle selection)
- [ ] Add Shift+Click for range selection (rectangular)
- [ ] Add "Merge Cells" action button (appears when 2+ cells selected)
- [ ] Add "Unmerge" action for merged cell groups
- [ ] Validate that only rectangular selections can merge (no L-shapes)
- [ ] Update `mergedCells` in `GridLayoutConfig` when merging
- [ ] Update `objectSpans` when object placed in merged cell
- [ ] Visual indicator for merged cells (thicker border, different background)
- [ ] Add merge utility functions to `gridLayoutUtils.ts`

---

## ❌ Scope (Out)

- Individual row/column spacing controls (T06)
- Global defaults integration (T07)
- Context menu (use button-based UI instead for simplicity)
- Drag-to-select (use click-based selection)
- Keyboard-only cell selection

---

## 🚫 Forbidden Zones

| Zone | Reason |
|------|--------|
| `backend/` | No backend changes |
| `database/` | No schema changes |
| `UniversalFieldShell.tsx` | Rendering already handles objectSpans (T02) |
| `ObjectLayoutSection.tsx` | Different layout system |

---

## 🎯 Acceptance Criteria

### AC1: User Can Select Multiple Adjacent Cells

**Criterion:** User can click on cells to select them. Selected cells are visually highlighted. Clicking a selected cell deselects it.

**Verification:**
- Click on empty cell (0,0) → Cell shows selection highlight
- Click on empty cell (0,1) → Both cells now selected
- Click on cell (0,0) again → Cell (0,0) deselected, only (0,1) selected
- Selection state is local (not persisted to config)

**Implementation Notes:**
- Use `useState<Set<string>>` for selected cell keys
- Add visual highlight (e.g., blue border/background) for selected cells
- Selection is separate from object assignment

---

### AC2: Merge Cells Button Appears for Valid Selection

**Criterion:** When 2 or more cells are selected in a valid rectangular pattern, a "Merge Cells" button appears. L-shaped or non-adjacent selections do not show the button.

**Verification:**
- Select cells (0,0) and (0,1) → "Merge Cells" button appears
- Select cells (0,0), (0,1), (1,0), (1,1) → "Merge Cells" button appears (2×2 rectangle)
- Select cells (0,0), (0,1), (1,0) → Button does NOT appear (L-shape)
- Select only 1 cell → Button does NOT appear

**Implementation Notes:**
- Validation function: `isValidMergeSelection(selectedCells: string[]): boolean`
- Check that cells form a complete rectangle (rows × cols = cell count)

---

### AC3: Merging Creates a Merged Cell Group

**Criterion:** Clicking "Merge Cells" creates a merged cell group in the config. The merged area displays as a single visual cell.

**Verification:**
- Select cells (0,0) and (0,1)
- Click "Merge Cells"
- Verify `config.mergedCells` contains new group with both cells
- Verify cells (0,0) and (0,1) display as single merged visual cell
- Selection is cleared after merge

**Implementation Notes:**
- Use format: `mergedCells: { "merge-{timestamp}": { cells: ["0-0", "0-1"], objectId: "" } }`
- Merged cells render as one visual block spanning the grid area

---

### AC4: Objects in Merged Cells Span Correctly

**Criterion:** When an object is dragged into a merged cell, it automatically spans the entire merged area. The `objectSpans` config is updated accordingly.

**Verification:**
- Create a 2×1 merged cell group (cells 0,0 and 0,1)
- Drag "label" object into the merged area
- Verify `cellAssignments` has entry `"0-0": "label"` (first cell only)
- Verify `objectSpans` has entry `"label": { rowSpan: 1, colSpan: 2 }`
- Verify "label" visually spans both columns

**Implementation Notes:**
- On drop into merged cell: assign to first cell of group
- Calculate rowSpan/colSpan from merged cell extent
- Update T04's handleDragEnd to check for merged cell drops

---

### AC5: Unmerge Action Splits Merged Cells

**Criterion:** User can unmerge a merged cell group, returning cells to individual state.

**Verification:**
- Click on merged cell group (or select it)
- "Unmerge" button appears
- Click "Unmerge"
- Verify merged cells return to individual cells
- Verify `mergedCells` entry removed from config
- If object was in merged cell, it remains in first cell only
- Verify `objectSpans` entry for that object is removed

**Implementation Notes:**
- Remove merge group from `mergedCells`
- Remove span from `objectSpans` for affected object
- Keep object assignment in original (first) cell

---

### AC6: L-Shaped Selections Cannot Merge (Validation)

**Criterion:** Attempting to merge a non-rectangular selection shows an error or prevents the action.

**Verification:**
- Select cells (0,0), (0,1), (1,0) — L-shape
- Verify "Merge Cells" button is disabled or hidden
- No merge occurs
- Optionally show tooltip: "Only rectangular selections can be merged"

**Implementation Notes:**
- Validation: `rows.length * cols.length === cells.length`
- If invalid, button is disabled (not hidden) with tooltip

---

## 🔧 Implementation Details

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `gridLayoutUtils.ts` | Add | `mergeCells()`, `unmergeCells()`, `isValidMergeSelection()`, `getMergeGroupForCell()` |
| `GridLayoutSection.tsx` | Modify | Add selection state, merge/unmerge buttons |
| `GridLayoutEditor.tsx` | Modify | Add visual merged cell rendering, selection highlights |

### New Utility Functions

Add to `frontend/src/features/builder/utils/gridLayoutUtils.ts`:

```typescript
/**
 * Check if a set of cells forms a valid rectangular selection for merging.
 */
export function isValidMergeSelection(cellKeys: string[]): boolean {
    if (cellKeys.length < 2) return false;
    
    const positions = cellKeys.map(key => parseCell(key));
    const rows = [...new Set(positions.map(p => p.row))].sort((a, b) => a - b);
    const cols = [...new Set(positions.map(p => p.col))].sort((a, b) => a - b);
    
    // Check if cells form a complete rectangle
    const expectedCount = rows.length * cols.length;
    if (cellKeys.length !== expectedCount) return false;
    
    // Check that rows and columns are contiguous
    for (let i = 1; i < rows.length; i++) {
        if (rows[i] !== rows[i - 1] + 1) return false;
    }
    for (let i = 1; i < cols.length; i++) {
        if (cols[i] !== cols[i - 1] + 1) return false;
    }
    
    return true;
}

/**
 * Merge cells into a single group.
 */
export function mergeCells(
    cellKeys: string[],
    config: GridLayoutConfig
): GridLayoutConfig {
    if (!isValidMergeSelection(cellKeys)) {
        throw new Error('Cells must form a rectangle to merge');
    }
    
    const mergeId = `merge-${Date.now()}`;
    const mergedCells = {
        ...(config.mergedCells || {}),
        [mergeId]: {
            cells: [...cellKeys].sort(), // Sort for consistency
            objectId: ''
        }
    };
    
    return {
        ...config,
        mergedCells
    };
}

/**
 * Unmerge a merged cell group.
 */
export function unmergeCells(
    mergeId: string,
    config: GridLayoutConfig
): GridLayoutConfig {
    const mergedCells = { ...(config.mergedCells || {}) };
    const mergeGroup = mergedCells[mergeId];
    
    // Remove span for object if one was assigned
    let objectSpans = { ...(config.objectSpans || {}) };
    if (mergeGroup?.objectId) {
        delete objectSpans[mergeGroup.objectId];
    }
    
    delete mergedCells[mergeId];
    
    return {
        ...config,
        mergedCells: Object.keys(mergedCells).length > 0 ? mergedCells : undefined,
        objectSpans: Object.keys(objectSpans).length > 0 ? objectSpans : undefined
    };
}

/**
 * Get the merge group that contains a specific cell.
 */
export function getMergeGroupForCell(
    cellKey: string,
    config: GridLayoutConfig
): { mergeId: string; group: { cells: string[]; objectId: string } } | null {
    if (!config.mergedCells) return null;
    
    for (const [mergeId, group] of Object.entries(config.mergedCells)) {
        if (group.cells.includes(cellKey)) {
            return { mergeId, group };
        }
    }
    
    return null;
}

/**
 * Calculate the span extent for a merged cell group.
 */
export function getMergeSpan(cells: string[]): { rowSpan: number; colSpan: number } {
    const positions = cells.map(key => parseCell(key));
    const rows = [...new Set(positions.map(p => p.row))];
    const cols = [...new Set(positions.map(p => p.col))];
    return { rowSpan: rows.length, colSpan: cols.length };
}
```

### UI Changes

**GridLayoutSection.tsx:**
```typescript
// Add selection state
const [selectedCells, setSelectedCells] = useState<Set<string>>(new Set());

// Add merge action handler
const handleMergeCells = useCallback(() => {
    const cellArray = Array.from(selectedCells);
    if (!isValidMergeSelection(cellArray)) return;
    
    const newConfig = mergeCells(cellArray, currentGridConfig);
    handleGridConfigChange(newConfig);
    setSelectedCells(new Set()); // Clear selection
}, [selectedCells, currentGridConfig, handleGridConfigChange]);

// Add unmerge action handler
const handleUnmergeCells = useCallback((mergeId: string) => {
    const newConfig = unmergeCells(mergeId, currentGridConfig);
    handleGridConfigChange(newConfig);
}, [currentGridConfig, handleGridConfigChange]);

// Render merge button when valid selection exists
{selectedCells.size >= 2 && isValidMergeSelection(Array.from(selectedCells)) && (
    <button onClick={handleMergeCells}>Merge Cells</button>
)}
```

**GridLayoutEditor.tsx:**
```typescript
// Pass selection state and callbacks as props
interface GridLayoutEditorProps {
    config: GridLayoutConfig;
    selectedCells?: Set<string>;
    onCellClick?: (cellKey: string) => void;
    onUnmerge?: (mergeId: string) => void;
    // ... other props
}

// Render merged cells as single visual unit
// Skip rendering cells that are part of a merge (except the first cell)
// First cell renders with gridRow/gridColumn spanning the merged area
```

### Visual States

| State | Visual Treatment |
|-------|------------------|
| Normal cell | Standard dashed border |
| Selected cell | Blue/teal solid border, light blue background |
| Merged cell group | Thicker border, slightly different background |
| Merge button | Appears above grid when valid selection |
| Invalid selection | Merge button disabled with tooltip |

---

## 🧪 Required Tests

### Manual Verification

1. **Cell Selection**
   - Click cell (0,0) → selected
   - Click cell (0,1) → both selected
   - Click cell (0,0) → only (0,1) selected
   
2. **Valid Merge**
   - Select (0,0) and (0,1)
   - Click "Merge Cells"
   - Verify cells display as one unit
   - Verify config has mergedCells entry
   
3. **Object in Merged Cell**
   - Create 2×1 merge
   - Drag "input" to merged area
   - Verify object spans both columns
   - Verify objectSpans in config
   
4. **Unmerge**
   - Click on merged cell
   - Click "Unmerge"
   - Verify cells are separate again
   - Verify mergedCells entry removed

5. **Invalid Selection**
   - Select L-shape: (0,0), (0,1), (1,0)
   - Verify "Merge Cells" button disabled

### Build Verification

```bash
# Use ReadLints tool on changed files
ReadLints: gridLayoutUtils.ts, GridLayoutSection.tsx, GridLayoutEditor.tsx
```

---

## 📚 References

- **Cell Merging Spec:** `docs/GRID-LAYOUT-GUIDE.md` (Section 4 "Cell Merging and Spanning")
- **T04 DnD Implementation:** `GridLayoutSection.tsx` (for integration points)
- **Validation Patterns:** `validateGridLayout()` in `gridLayoutUtils.ts`

---

## ⚠️ Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Merge cells with object | Object spans merged area, objectSpans updated |
| Merge cells with multiple objects | Prevent merge (only one object per merged area) |
| Unmerge cell with object | Object stays in first cell, span removed |
| Grid resized to remove merged cells | Merged group is removed, object returns to pool |
| Overlapping merge attempts | Prevent (cells already in merge can't be re-merged) |

---

## 📝 Handoff Requirements

On completion, provide:
1. `T05-cell-merging.completion.md` with:
   - Files changed
   - AC verification evidence
   - Build/lint verification
2. `T05-cell-merging.uat.md` with:
   - Step-by-step manual test instructions
   - DevTools MCP verification steps

---

*Task Spec created by Ralf-SM*  
*Date: 2026-01-14*
