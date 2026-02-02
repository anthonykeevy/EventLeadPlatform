# Task T06: Individual Spacing Controls

**Story:** 3.10 - Grid Layout System  
**Task ID:** T06  
**Status:** ⏳ Ready  
**Dependencies:** T03 ✅  
**Estimated Time:** 1-2 hours  

---

## 📋 Task Overview

**Objective:** Add UI controls for setting individual row and column spacing overrides, allowing users to fine-tune the gap between specific rows or columns.

**User Story:** As a form builder user, I want to adjust the spacing between specific rows or columns independently so that I can create varied visual layouts beyond uniform gaps.

---

## ✅ Scope (In)

- [ ] Add collapsible "Individual Column Spacing" section below the global Column Gap control
- [ ] Add collapsible "Individual Row Spacing" section below the global Row Gap control
- [ ] Display a slider for each column gap (between Col N and Col N+1)
- [ ] Display a slider for each row gap (between Row N and Row N+1)
- [ ] Show "Reset" button next to each individual slider (only when value differs from default)
- [ ] Update `columnGaps` object in config when individual column gap changes
- [ ] Update `rowGaps` object in config when individual row gap changes
- [ ] Remove override entry when reset to default (keep config clean)
- [ ] Visual indicator showing which gaps are customized vs using default

---

## ❌ Scope (Out)

- Cell merging (T05 - already complete)
- Global defaults integration (T07)
- Drag handles for adjusting gaps directly on the grid preview
- Gap presets or templates
- Gap copying between rows/columns

---

## 🚫 Forbidden Zones

| Zone | Reason |
|------|--------|
| `backend/` | No backend changes |
| `database/` | No schema changes |
| `UniversalFieldShell.tsx` | Rendering only |
| `ObjectLayoutSection.tsx` | Different layout system |
| `gridLayoutUtils.ts` | Utilities already handle rowGaps/columnGaps (T01/T02) |

---

## 🎯 Acceptance Criteria

### AC1: Individual Column Spacing Section Visible

**Criterion:** When grid has 2+ columns, a collapsible "Individual Column Spacing" section appears below the global Column Gap control.

**Verification:**
- Set grid to 3 columns
- Verify "Individual Column Spacing" section appears (collapsed by default)
- Expand section → shows sliders for "Col 0 → Col 1" and "Col 1 → Col 2"
- Set grid to 1 column → section disappears (no gaps between single column)

**Implementation Notes:**
- Only show section when `config.columns > 1`
- Number of sliders = `config.columns - 1`
- Label format: "Col {N} → Col {N+1}"

---

### AC2: Individual Row Spacing Section Visible

**Criterion:** When grid has 2+ rows, a collapsible "Individual Row Spacing" section appears below the global Row Gap control.

**Verification:**
- Set grid to 3 rows
- Verify "Individual Row Spacing" section appears (collapsed by default)
- Expand section → shows sliders for "Row 0 → Row 1" and "Row 1 → Row 2"
- Set grid to 1 row → section disappears (no gaps between single row)

**Implementation Notes:**
- Only show section when `config.rows > 1`
- Number of sliders = `config.rows - 1`
- Label format: "Row {N} → Row {N+1}"

---

### AC3: Adjusting Individual Gap Updates Config

**Criterion:** Changing an individual gap slider updates the corresponding `columnGaps` or `rowGaps` entry in the config.

**Verification:**
- Expand "Individual Column Spacing"
- Adjust "Col 0 → Col 1" slider from 8px to 20px
- Verify `config.columnGaps` now contains `{ 0: 20 }`
- Verify grid preview shows larger gap between columns 0 and 1

**Implementation Notes:**
- Add entries to `columnGaps` or `rowGaps` object
- Key is the index (0-based), value is gap in pixels
- Existing `handleGridConfigChange` should work

---

### AC4: Reset Button Reverts to Default Gap

**Criterion:** Each individual gap control has a "Reset" button that appears when the value differs from the default. Clicking it removes the override.

**Verification:**
- Set "Col 0 → Col 1" gap to 20px (default is 8px)
- Verify "Reset" button appears next to that slider
- Click "Reset"
- Verify gap reverts to 8px (default column gap)
- Verify `columnGaps[0]` is removed from config
- Verify "Reset" button disappears

**Implementation Notes:**
- Show Reset button only when `columnGaps[index] !== undefined`
- On reset: delete the entry from `columnGaps` object
- If `columnGaps` becomes empty, set to `undefined` (clean config)

---

### AC5: Individual Gaps Reflected in Grid Preview

**Criterion:** The grid preview (GridLayoutEditor) visually reflects individual gap overrides.

**Verification:**
- Set 3 columns, default gap 8px
- Set "Col 0 → Col 1" to 24px (large gap)
- Set "Col 1 → Col 2" to 4px (small gap)
- Verify grid preview shows varying column widths between cells
- Same verification for row gaps

**Implementation Notes:**
- GridLayoutEditor uses `generateGridStyles()` which already handles `rowGaps`/`columnGaps`
- This should work automatically if config is updated correctly

---

## 🔧 Implementation Details

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `GridLayoutSection.tsx` | Modify | Add collapsible individual spacing sections |

### UI Component Structure

```tsx
{/* Below existing Column Gap control */}
{config.columns > 1 && (
    <IndividualSpacingSection
        title="Individual Column Spacing"
        count={config.columns - 1}
        labelTemplate={(i) => `Col ${i} → Col ${i + 1}`}
        gaps={config.columnGaps || {}}
        defaultGap={config.columnGap}
        onGapChange={(index, value) => handleIndividualColumnGapChange(index, value)}
        onReset={(index) => handleResetColumnGap(index)}
    />
)}

{/* Below existing Row Gap control */}
{config.rows > 1 && (
    <IndividualSpacingSection
        title="Individual Row Spacing"
        count={config.rows - 1}
        labelTemplate={(i) => `Row ${i} → Row ${i + 1}`}
        gaps={config.rowGaps || {}}
        defaultGap={config.rowGap}
        onGapChange={(index, value) => handleIndividualRowGapChange(index, value)}
        onReset={(index) => handleResetRowGap(index)}
    />
)}
```

### Handler Functions

```typescript
// Handle individual column gap change
const handleIndividualColumnGapChange = useCallback((index: number, value: number) => {
    const gap = Math.max(0, Math.min(48, value));
    const columnGaps = { ...(currentGridConfig.columnGaps || {}) };
    
    if (gap === currentGridConfig.columnGap) {
        // Reset to default: remove override
        delete columnGaps[index];
    } else {
        columnGaps[index] = gap;
    }
    
    handleGridConfigChange({
        columnGaps: Object.keys(columnGaps).length > 0 ? columnGaps : undefined
    });
}, [currentGridConfig, handleGridConfigChange]);

// Handle reset column gap
const handleResetColumnGap = useCallback((index: number) => {
    const columnGaps = { ...(currentGridConfig.columnGaps || {}) };
    delete columnGaps[index];
    
    handleGridConfigChange({
        columnGaps: Object.keys(columnGaps).length > 0 ? columnGaps : undefined
    });
}, [currentGridConfig, handleGridConfigChange]);

// Same pattern for row gaps
const handleIndividualRowGapChange = useCallback((index: number, value: number) => {
    const gap = Math.max(0, Math.min(48, value));
    const rowGaps = { ...(currentGridConfig.rowGaps || {}) };
    
    if (gap === currentGridConfig.rowGap) {
        delete rowGaps[index];
    } else {
        rowGaps[index] = gap;
    }
    
    handleGridConfigChange({
        rowGaps: Object.keys(rowGaps).length > 0 ? rowGaps : undefined
    });
}, [currentGridConfig, handleGridConfigChange]);

const handleResetRowGap = useCallback((index: number) => {
    const rowGaps = { ...(currentGridConfig.rowGaps || {}) };
    delete rowGaps[index];
    
    handleGridConfigChange({
        rowGaps: Object.keys(rowGaps).length > 0 ? rowGaps : undefined
    });
}, [currentGridConfig, handleGridConfigChange]);
```

### Collapsible Section Component (inline or extracted)

```tsx
interface IndividualSpacingSectionProps {
    title: string;
    count: number;
    labelTemplate: (index: number) => string;
    gaps: Record<number, number>;
    defaultGap: number;
    onGapChange: (index: number, value: number) => void;
    onReset: (index: number) => void;
}

const IndividualSpacingSection: React.FC<IndividualSpacingSectionProps> = ({
    title,
    count,
    labelTemplate,
    gaps,
    defaultGap,
    onGapChange,
    onReset
}) => {
    const [isExpanded, setIsExpanded] = useState(false);
    
    return (
        <div className="mt-2">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="flex items-center gap-1 text-[10px] text-gray-500 hover:text-gray-700"
            >
                <ChevronRight size={12} className={isExpanded ? 'rotate-90' : ''} />
                {title}
            </button>
            
            {isExpanded && (
                <div className="mt-2 ml-4 space-y-2">
                    {Array.from({ length: count }, (_, i) => {
                        const currentGap = gaps[i] ?? defaultGap;
                        const isCustom = gaps[i] !== undefined;
                        
                        return (
                            <div key={i} className="flex items-center gap-2">
                                <span className="text-[9px] text-gray-400 w-24">
                                    {labelTemplate(i)}
                                </span>
                                <input
                                    type="range"
                                    min={0}
                                    max={48}
                                    value={currentGap}
                                    onChange={(e) => onGapChange(i, parseInt(e.target.value))}
                                    className="flex-1 h-1 accent-indigo-500"
                                />
                                <span className={`text-[9px] w-8 ${isCustom ? 'text-indigo-600 font-medium' : 'text-gray-400'}`}>
                                    {currentGap}px
                                </span>
                                {isCustom && (
                                    <button
                                        onClick={() => onReset(i)}
                                        className="text-[8px] text-gray-400 hover:text-red-500"
                                        title="Reset to default"
                                    >
                                        Reset
                                    </button>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};
```

### Visual States

| State | Visual Treatment |
|-------|------------------|
| Collapsed section | Shows section title with chevron icon |
| Expanded section | Shows all gap sliders |
| Default gap value | Normal text color (gray) |
| Custom gap value | Highlighted color (indigo) + "Reset" button visible |
| Reset button | Small text, appears only when value is customized |

---

## 🧪 Required Tests

### Manual Verification

1. **Column Spacing Section Visibility**
   - Set 1 column → section hidden
   - Set 2 columns → section shows 1 slider
   - Set 3 columns → section shows 2 sliders
   
2. **Row Spacing Section Visibility**
   - Set 1 row → section hidden
   - Set 2 rows → section shows 1 slider
   - Set 3 rows → section shows 2 sliders
   
3. **Adjust Individual Gap**
   - Change "Col 0 → Col 1" to 24px
   - Verify grid preview updates
   - Verify config has `columnGaps: { 0: 24 }`
   
4. **Reset Gap**
   - With custom gap set, click Reset
   - Verify value returns to default
   - Verify config no longer has that entry

5. **Grid Preview Updates**
   - Set varied column gaps (4px, 24px)
   - Verify visible difference in grid preview

### Build Verification

```bash
# Use ReadLints tool on changed files
ReadLints: GridLayoutSection.tsx
```

---

## 📚 References

- **Mockup:** `docs/GRID-LAYOUT-GUIDE.md` (see "Individual Column Spacing" and "Individual Row Spacing" sections in mockups)
- **CSS Generation:** `gridLayoutUtils.ts` → `generateGridStyles()` (already handles rowGaps/columnGaps)
- **Existing Controls:** `GridLayoutSection.tsx` → global Row Gap and Column Gap controls

---

## ⚠️ Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| Grid resized to fewer columns | Remove invalid columnGaps entries (indices >= columns-1) |
| Grid resized to fewer rows | Remove invalid rowGaps entries (indices >= rows-1) |
| All gaps reset | `columnGaps`/`rowGaps` becomes `undefined` (not empty object) |
| Set individual gap same as default | Remove entry (treated as reset) |

---

## 📝 Handoff Requirements

On completion, provide:
1. `T06-individual-spacing.completion.md` with:
   - Files changed
   - AC verification evidence
   - Build/lint verification
2. `T06-individual-spacing.uat.md` with:
   - Step-by-step manual test instructions

---

*Task Spec created by Ralf-SM*  
*Date: 2026-01-14*
