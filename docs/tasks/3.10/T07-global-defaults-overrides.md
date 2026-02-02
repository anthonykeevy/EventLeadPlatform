# Task T07: Global Defaults & Overrides

**Story:** 3.10 - Grid Layout System  
**Task ID:** T07  
**Status:** ⏳ Ready  
**Dependencies:** T02 ✅, T03 ✅  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Add global grid layout defaults to the Global Styles panel and implement the resolution system where components inherit global defaults but can override them.

**User Story:** As a form builder user, I want to set form-wide default grid layout settings so that all components have consistent grid layouts unless I specifically override them.

---

## ✅ Scope (In)

- [ ] Add "Grid Layout Defaults" section to GlobalStylesPanel
- [ ] Allow setting default rows, columns, rowGap, columnGap at form level
- [ ] Components without `gridLayout` override inherit `globalStyles.defaultGridLayout`
- [ ] Add layout source indicator in GridLayoutSection ("Using Global Default" vs "Component Override")
- [ ] Add "Override Global" action to create component override from global values
- [ ] Add "Reset to Global" action to clear component override
- [ ] Implement `getEffectiveGridLayout()` utility function for resolution
- [ ] Visual indicator when component differs from global

---

## ❌ Scope (Out)

- Cell merging in global defaults (global defines structure, not cell assignments)
- Individual row/column gaps in global defaults (only default gaps)
- Migrating existing components to use global defaults
- Runtime preview changes (already uses gridLayout from config)

---

## 🚫 Forbidden Zones

| Zone | Reason |
|------|--------|
| `backend/` | No backend changes |
| `database/` | No schema changes |
| `UniversalFieldShell.tsx` | Already handles gridLayout rendering (T02) |
| `ObjectLayoutSection.tsx` | Different layout system |

---

## 🎯 Acceptance Criteria

### AC1: Global Grid Defaults Section in GlobalStylesPanel

**Criterion:** GlobalStylesPanel has a new collapsible "Grid Layout Defaults" section with controls for default rows, columns, rowGap, and columnGap.

**Verification:**
- Open Global Styles panel (when no component selected)
- Verify "Grid Layout Defaults" section exists
- Verify controls for: Default Rows, Default Columns, Default Row Gap, Default Column Gap
- Change Default Rows to 4 → verify `globalStyles.defaultGridLayout.rows` updates

**Implementation Notes:**
- Add section similar to existing "Default Object Layout" control
- Use PropertyNumberInput for rows/columns (1-12 range)
- Use slider for gaps (0-48px range)
- Store in `globalStyles.defaultGridLayout`

---

### AC2: Components Inherit Global Defaults

**Criterion:** When a component has no `gridLayout` override, it inherits configuration from `globalStyles.defaultGridLayout`.

**Verification:**
- Set global defaults: rows=4, columns=2, rowGap=12, columnGap=16
- Select a component that uses Grid Layout mode
- Verify component displays 4×2 grid with 12px/16px gaps
- Verify `component.props.gridLayout` is `undefined`

**Implementation Notes:**
- GridLayoutSection should check `component.props.gridLayout`
- If undefined, use `globalStyles.defaultGridLayout` for display
- Use `getEffectiveGridLayout()` utility for resolution

---

### AC3: Component Override Takes Precedence

**Criterion:** When a component has `gridLayout` defined, it takes precedence over global defaults. Partial overrides merge with global (component properties take priority).

**Verification:**
- Set global: rows=3, columnGap=8
- Create component override with rows=5 only
- Verify effective config: rows=5 (override), columns=1 (global fallback), columnGap=8 (global fallback)

**Implementation Notes:**
- `getEffectiveGridLayout()` merges global + component
- Each property: `componentOverride.prop ?? global.prop ?? systemDefault`
- cellAssignments, mergedCells, objectSpans always come from component (not global)

---

### AC4: "Override Global" and "Reset to Global" Actions

**Criterion:** GridLayoutSection shows "Override Global" button when using global defaults, and "Reset to Global" button when using component override.

**Verification:**
- Select component using global defaults → "Override Global" button visible
- Click "Override Global" → global values copied to `component.props.gridLayout`
- Now shows "Reset to Global" button
- Click "Reset to Global" → `component.props.gridLayout` set to `undefined`
- Component now uses global defaults again

**Implementation Notes:**
```typescript
// Override Global
const handleOverrideGlobal = () => {
    const effective = getEffectiveGridLayout(component, globalStyles);
    if (effective) {
        onPropsChange({ gridLayout: { ...effective } });
    }
};

// Reset to Global
const handleResetToGlobal = () => {
    onPropsChange({ gridLayout: undefined });
};
```

---

### AC5: Override Indicator When Component Differs

**Criterion:** When a component has a `gridLayout` override, a visual indicator shows it's using component-specific settings rather than global defaults.

**Verification:**
- Component with no override: shows "Using Global Default" badge/text
- Component with override: shows "Component Override" badge/text
- Badge is visible in GridLayoutSection header area

**Implementation Notes:**
- Check `component.props.gridLayout !== undefined`
- Display small badge or text indicator
- Use different colors: gray for global, indigo for override

---

## 🔧 Implementation Details

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `GlobalStylesPanel.tsx` | Modify | Add "Grid Layout Defaults" section |
| `GridLayoutSection.tsx` | Modify | Add source indicator, Override/Reset buttons, use global defaults |
| `gridLayoutUtils.ts` | Add | `getEffectiveGridLayout()` function |

### New Utility Function

Add to `frontend/src/features/builder/utils/gridLayoutUtils.ts`:

```typescript
/**
 * Get effective grid layout configuration for a component.
 * Merges global defaults with component overrides.
 * 
 * Resolution order:
 * 1. Component override (highest priority)
 * 2. Global defaults
 * 3. System defaults (fallback)
 * 
 * @param component - The form component
 * @param globalStyles - Global styles with defaultGridLayout
 * @returns Effective GridLayoutConfig or null if grid layout not enabled
 */
export function getEffectiveGridLayout(
    componentGridLayout: GridLayoutConfig | undefined,
    globalDefaultGridLayout: Partial<GridLayoutConfig> | undefined
): GridLayoutConfig | null {
    const global = globalDefaultGridLayout;
    const componentOverride = componentGridLayout;

    // If component has gridLayout override, merge with global fallbacks
    if (componentOverride) {
        return {
            rows: componentOverride.rows ?? global?.rows ?? 3,
            columns: componentOverride.columns ?? global?.columns ?? 1,
            columnGap: componentOverride.columnGap ?? global?.columnGap ?? 8,
            rowGap: componentOverride.rowGap ?? global?.rowGap ?? 8,
            columnGaps: componentOverride.columnGaps ?? global?.columnGaps,
            rowGaps: componentOverride.rowGaps ?? global?.rowGaps,
            // cellAssignments always from component (not global)
            cellAssignments: componentOverride.cellAssignments ?? {},
            mergedCells: componentOverride.mergedCells,
            objectSpans: componentOverride.objectSpans,
            cellAlignment: componentOverride.cellAlignment ?? global?.cellAlignment ?? 'stretch',
            gridJustification: componentOverride.gridJustification ?? global?.gridJustification ?? 'start',
        };
    }

    // If global has defaultGridLayout, use it with system defaults
    if (global) {
        return {
            rows: global.rows ?? 3,
            columns: global.columns ?? 1,
            columnGap: global.columnGap ?? 8,
            rowGap: global.rowGap ?? 8,
            columnGaps: global.columnGaps,
            rowGaps: global.rowGaps,
            cellAssignments: global.cellAssignments ?? {},
            mergedCells: global.mergedCells,
            objectSpans: global.objectSpans,
            cellAlignment: global.cellAlignment ?? 'stretch',
            gridJustification: global.gridJustification ?? 'start',
        };
    }

    // No grid layout configured
    return null;
}

/**
 * Check if component has grid layout override (vs using global default)
 */
export function hasGridLayoutOverride(componentGridLayout: GridLayoutConfig | undefined): boolean {
    return componentGridLayout !== undefined;
}
```

### GlobalStylesPanel Changes

Add new section after existing "Default Object Layout" control:

```tsx
{/* Grid Layout Defaults Section */}
<div className="p-4 border-b border-gray-200 dark:border-gray-700">
    <div className="flex items-center gap-2 mb-3">
        <Grid3x3 size={16} className="text-gray-500" />
        <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Grid Layout Defaults
        </h4>
    </div>
    <p className="text-[10px] text-gray-400 mb-3">
        Default grid settings for components using Grid Layout mode
    </p>
    
    <div className="space-y-3">
        {/* Default Rows */}
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 w-24">Default Rows</span>
            <PropertyNumberInput
                value={effectiveGlobalStyles.defaultGridLayout?.rows ?? 3}
                onChange={(value) => onGlobalStylesChange({
                    defaultGridLayout: {
                        ...effectiveGlobalStyles.defaultGridLayout,
                        rows: value
                    }
                })}
                min={1}
                max={12}
            />
        </div>
        
        {/* Default Columns */}
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 w-24">Default Columns</span>
            <PropertyNumberInput
                value={effectiveGlobalStyles.defaultGridLayout?.columns ?? 1}
                onChange={(value) => onGlobalStylesChange({
                    defaultGridLayout: {
                        ...effectiveGlobalStyles.defaultGridLayout,
                        columns: value
                    }
                })}
                min={1}
                max={12}
            />
        </div>
        
        {/* Default Row Gap */}
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 w-24">Default Row Gap</span>
            <input
                type="range"
                min={0}
                max={48}
                value={effectiveGlobalStyles.defaultGridLayout?.rowGap ?? 8}
                onChange={(e) => onGlobalStylesChange({
                    defaultGridLayout: {
                        ...effectiveGlobalStyles.defaultGridLayout,
                        rowGap: parseInt(e.target.value)
                    }
                })}
                className="flex-1 h-1.5 accent-indigo-500"
            />
            <span className="text-[10px] text-gray-600 w-10">
                {effectiveGlobalStyles.defaultGridLayout?.rowGap ?? 8}px
            </span>
        </div>
        
        {/* Default Column Gap */}
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 w-24">Default Col Gap</span>
            <input
                type="range"
                min={0}
                max={48}
                value={effectiveGlobalStyles.defaultGridLayout?.columnGap ?? 8}
                onChange={(e) => onGlobalStylesChange({
                    defaultGridLayout: {
                        ...effectiveGlobalStyles.defaultGridLayout,
                        columnGap: parseInt(e.target.value)
                    }
                })}
                className="flex-1 h-1.5 accent-indigo-500"
            />
            <span className="text-[10px] text-gray-600 w-10">
                {effectiveGlobalStyles.defaultGridLayout?.columnGap ?? 8}px
            </span>
        </div>
    </div>
</div>
```

### GridLayoutSection Changes

Add source indicator and action buttons:

```tsx
// At top of Grid Layout section when in grid mode
{isGridMode && (
    <div className="flex items-center justify-between mb-3">
        {/* Source Indicator */}
        <div className={`text-[10px] px-2 py-0.5 rounded ${
            hasGridLayoutOverride(component.props.gridLayout)
                ? 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'
                : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
        }`}>
            {hasGridLayoutOverride(component.props.gridLayout) 
                ? '🔧 Component Override' 
                : '🌐 Using Global Default'}
        </div>
        
        {/* Action Buttons */}
        <div className="flex gap-2">
            {!hasGridLayoutOverride(component.props.gridLayout) ? (
                <button
                    onClick={handleOverrideGlobal}
                    className="text-[10px] text-indigo-600 hover:text-indigo-800"
                >
                    Override Global
                </button>
            ) : (
                <button
                    onClick={handleResetToGlobal}
                    className="text-[10px] text-gray-500 hover:text-red-600"
                >
                    Reset to Global
                </button>
            )}
        </div>
    </div>
)}
```

### Visual States

| State | Indicator | Action Available |
|-------|-----------|------------------|
| Using global default | "🌐 Using Global Default" badge (gray) | "Override Global" button |
| Component override | "🔧 Component Override" badge (indigo) | "Reset to Global" button |
| No global default set | Same as override (component has its own) | "Reset to Global" clears to undefined |

---

## 🧪 Required Tests

### Manual Verification

1. **Global Defaults Section**
   - Open Global Styles panel
   - Verify "Grid Layout Defaults" section exists
   - Change values → verify `globalStyles.defaultGridLayout` updates
   
2. **Inheritance**
   - Set global: rows=4, columns=2
   - Select component with Grid Layout enabled, no override
   - Verify displays 4×2 grid
   
3. **Override Creation**
   - Click "Override Global"
   - Verify `component.props.gridLayout` now has values
   - Verify shows "Component Override" badge
   
4. **Reset to Global**
   - Click "Reset to Global"
   - Verify `component.props.gridLayout` is `undefined`
   - Verify shows "Using Global Default" badge
   
5. **Partial Override Merge**
   - Set global: rows=3, columnGap=8
   - Create component override: rows=5 only
   - Verify rows=5, columnGap=8 (from global)

### Build Verification

```bash
# Use ReadLints tool on changed files
ReadLints: GlobalStylesPanel.tsx, GridLayoutSection.tsx, gridLayoutUtils.ts
```

---

## 📚 References

- **Resolution Order Spec:** `docs/GRID-LAYOUT-GUIDE.md` (section "Resolution Order")
- **Global/Override Examples:** `docs/GRID-LAYOUT-GUIDE.md` (Example 10: Global Defaults with Component Overrides)
- **Similar Pattern:** `defaultObjectLayout` in GlobalStylesPanel
- **Type Definition:** `GlobalStyles.defaultGridLayout` in `builder.types.ts`

---

## ⚠️ Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| No global default set | Component uses system defaults (3×1, 8px gaps) |
| Global default removed | Components with no override use system defaults |
| Partial component override | Missing properties fall back to global, then system defaults |
| Switch from Grid to Object Layout | `gridLayout` cleared, global has no effect |

---

## 📝 Handoff Requirements

On completion, provide:
1. `T07-global-defaults-overrides.completion.md` with:
   - Files changed
   - AC verification evidence
   - Build/lint verification
2. `T07-global-defaults-overrides.uat.md` with:
   - Step-by-step manual test instructions

---

*Task Spec created by Ralf-SM*  
*Date: 2026-01-14*
