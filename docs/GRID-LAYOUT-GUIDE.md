# Grid Layout System Guide

**Purpose:** Comprehensive guide for the Grid Layout system, an additional layout option alongside the existing Object Layout system. Grid Layout allows users to arrange component objects in a customizable grid structure with configurable rows, columns, and spacing.

> **Related:** [Component Framework Reference](./COMPONENT-FRAMEWORK-REFERENCE.md) - Understanding the component structure and object system.

---

## 🎯 Overview

The Grid Layout system provides a flexible, visual way to arrange component objects (label, input, validation, etc.) in a grid structure. Unlike the Object Layout system which uses rows and groups, Grid Layout uses a true CSS Grid approach with explicit row and column definitions.

### Key Features

- **Visual Grid Editor**: Drag-and-drop objects onto grid cells
- **Configurable Grid**: Adjust number of rows and columns
- **Flexible Spacing**: Control gap between grid cells (horizontal and vertical)
- **Individual Row Spacing**: Adjust spacing between specific rows independently
- **Individual Column Spacing**: Adjust spacing between specific columns independently
- **Cell Merging**: Visually merge cells together for object spanning (horizontal and vertical)
- **Object Reuse**: Uses the same objects as Object Layout (`label`, `input`, `validation`, etc.)
- **Coexistence**: Works alongside Object Layout as an alternative layout option

### When to Use Grid Layout vs Object Layout

| Feature | Object Layout | Grid Layout |
|---------|--------------|-------------|
| **Best For** | Simple row-based arrangements | Complex multi-column layouts |
| **Structure** | Rows with horizontal objects | True grid with rows × columns |
| **Flexibility** | Fixed 3-row system | Customizable rows/columns |
| **Use Case** | Label above input, help below | Multi-column forms, side-by-side fields |

---

## 📐 Properties Schema

### Component Props Extension

```typescript
export interface ComponentProps {
    // ... existing properties ...
    
    // ═══════════════════════════════════════════════════════════════
    // GRID LAYOUT PROPERTIES
    // ═══════════════════════════════════════════════════════════════
    
    /**
     * Grid layout configuration (alternative to objectLayout).
     * When set, this takes precedence over objectLayout.
     */
    gridLayout?: GridLayoutConfig;
}

export interface GridLayoutConfig {
    /**
     * Number of rows in the grid (1-12)
     * @default 3
     */
    rows: number;
    
    /**
     * Number of columns in the grid (1-12)
     * @default 1
     */
    columns: number;
    
    /**
     * Horizontal gap between grid cells (in pixels) - default for all columns
     * @default 8
     */
    columnGap: number;
    
    /**
     * Vertical gap between grid cells (in pixels) - default for all rows
     * @default 8
     */
    rowGap: number;
    
    /**
     * Per-column spacing overrides: allows individual column gaps
     * Format: colIndex → gapInPixels
     * Example: { 0: 16, 1: 8 } - Column 0 has 16px gap to the right, Column 1 has 8px gap to the right
     * Note: Gap applies TO THE RIGHT of the specified column (between column and next column)
     * @default {}
     */
    columnGaps?: Record<number, number>;
    
    /**
     * Per-row spacing overrides: allows individual row gaps
     * Format: rowIndex → gapInPixels
     * Example: { 0: 12, 2: 16 } - Row 0 has 12px gap below, Row 2 has 16px gap below
     * Note: Gap applies BELOW the specified row (between row and next row)
     * @default {}
     */
    rowGaps?: Record<number, number>;
    
    /**
     * Grid cell assignments: maps cell coordinates to object IDs
     * Format: "row-col" → objectId
     * Example: { "0-0": "label", "1-0": "input", "2-0": "validation" }
     */
    cellAssignments: Record<string, string>;
    
    /**
     * Merged cell groups: defines which cells are merged together
     * Format: "merged-group-id" → { cells: string[], objectId: string }
     * Example: { "merge-1": { cells: ["0-0", "0-1"], objectId: "label" } }
     * Used for visual cell merging in the editor
     */
    mergedCells?: Record<string, { cells: string[]; objectId: string }>;
    
    /**
     * Object span configuration: allows objects to span multiple cells
     * Format: objectId → { rowSpan: number, colSpan: number }
     * Example: { "input": { rowSpan: 1, colSpan: 2 } }
     */
    objectSpans?: Record<string, { rowSpan?: number; colSpan?: number }>;
    
    /**
     * Grid alignment: how objects align within their grid cells
     * @default 'stretch'
     */
    cellAlignment?: 'start' | 'center' | 'end' | 'stretch';
    
    /**
     * Grid justification: how grid cells align within the container
     * @default 'start'
     */
    gridJustification?: 'start' | 'center' | 'end' | 'stretch' | 'space-between' | 'space-around' | 'space-evenly';
}
```

### Global Styles Extension

```typescript
export interface GlobalStyles {
    // ... existing properties ...
    
    // ═══════════════════════════════════════════════════════════════
    // GRID LAYOUT DEFAULTS (GLOBAL)
    // ═══════════════════════════════════════════════════════════════
    
    /**
     * Default grid layout configuration (form-wide defaults)
     * Applied to all components when component doesn't have gridLayout override
     * Components can override individual properties or the entire configuration
     */
    defaultGridLayout?: {
        /**
         * Default number of rows (1-12)
         * @default 3
         */
        rows?: number;
        
        /**
         * Default number of columns (1-12)
         * @default 1
         */
        columns?: number;
        
        /**
         * Default horizontal gap between columns (in pixels)
         * @default 8
         */
        columnGap?: number;
        
        /**
         * Default vertical gap between rows (in pixels)
         * @default 8
         */
        rowGap?: number;
        
        /**
         * Default per-column spacing overrides
         * Format: colIndex → gapInPixels
         */
        columnGaps?: Record<number, number>;
        
        /**
         * Default per-row spacing overrides
         * Format: rowIndex → gapInPixels
         */
        rowGaps?: Record<number, number>;
        
        /**
         * Default cell alignment
         * @default 'stretch'
         */
        cellAlignment?: 'start' | 'center' | 'end' | 'stretch';
        
        /**
         * Default grid justification
         * @default 'start'
         */
        gridJustification?: 'start' | 'center' | 'end' | 'stretch' | 'space-between' | 'space-around' | 'space-evenly';
        
        /**
         * Default cell assignments (optional - usually set per-component)
         * Format: "row-col" → objectId
         */
        cellAssignments?: Record<string, string>;
        
        /**
         * Default merged cell groups (optional - usually set per-component)
         */
        mergedCells?: Record<string, { cells: string[]; objectId: string }>;
        
        /**
         * Default object spans (optional - usually set per-component)
         */
        objectSpans?: Record<string, { rowSpan?: number; colSpan?: number }>;
    };
}
```

### Resolution Order (Global → Component)

Grid layout properties are resolved in this order (later overrides earlier):

```
1. System Defaults (hardcoded application defaults)
       ↓
2. Global Styles (FormDefinition.globalStyles.defaultGridLayout)
       ↓
3. Component Override (FormComponent.props.gridLayout)
       ↓
4. Final Effective Configuration
```

**Key Points:**
- **Global defaults** apply to all components in the form
- **Component overrides** can override the entire grid layout or individual properties
- **Partial overrides** merge with global defaults (component properties take precedence)
- **Undefined component properties** fall back to global defaults

---

## 🎨 Grid Layout Modal Mockup

### Modal Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│  Grid Layout Configuration                              [×] Close  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Grid Settings                                               │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  Rows:    [─] 3  [+]    Columns:  [─] 2  [+]               │   │
│  │                                                               │   │
│  │  Column Gap:  [══════●══════]  8px  (Default for all columns)│   │
│  │  Row Gap:     [══════●══════]  8px  (Default for all rows)   │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────┐     │   │
│  │  │  Individual Column Spacing                 [▼]      │     │   │
│  │  ├─────────────────────────────────────────────────────┤     │   │
│  │  │  Col 0 → Col 1:  [══════●══════]  8px  [Reset]     │     │   │
│  │  │  Col 1 → Col 2:  [══════●══════]  16px [Reset]     │     │   │
│  │  │                                                      │     │   │
│  │  │  Adjust spacing between specific columns individually│     │   │
│  │  └─────────────────────────────────────────────────────┘     │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────┐     │   │
│  │  │  Individual Row Spacing                    [▼]      │     │   │
│  │  ├─────────────────────────────────────────────────────┤     │   │
│  │  │  Row 0 → Row 1:  [══════●══════]  8px  [Reset]     │     │   │
│  │  │  Row 1 → Row 2:  [══════●══════]  12px [Reset]     │     │   │
│  │  │  Row 2 → Row 3:  [══════●══════]  8px  [Reset]     │     │   │
│  │  │                                                      │     │   │
│  │  │  Adjust spacing between specific rows individually   │     │   │
│  │  └─────────────────────────────────────────────────────┘     │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Grid Preview                                    [Clear All] │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  ┌──────────┐  ┌──────────┐                                 │   │
│  │  │          │  │          │  ← Row 0                        │   │
│  │  │  [Label] │  │  [Input] │  Right-click: [Merge] [Span]    │   │
│  │  │          │  │          │                                 │   │
│  │  └──────────┘  └──────────┘                                 │   │
│  │                                                               │   │
│  │  ┌──────────────────────────┐                               │   │
│  │  │ ════════════════════════ │  ← Row 1 (merged: 0-1, 0-2)   │   │
│  │  │   [Validation spans]     │  Right-click: [Unmerge]        │   │
│  │  │ ════════════════════════ │  Span: 1×2                    │   │
│  │  └──────────────────────────┘                                 │   │
│  │                                                               │   │
│  │  ┌──────────┐  ┌──────────┐                                 │   │
│  │  │          │  │          │  ← Row 2                        │   │
│  │  │          │  │          │                                 │   │
│  │  └──────────┘  └──────────┘                                 │   │
│  │                                                               │   │
│  │  Column 0      Column 1                                       │   │
│  │                                                               │   │
│  │  💡 Tips:                                                      │   │
│  │  • Right-click cells to merge/unmerge                        │   │
│  │  • Select multiple cells (Shift+Click) then right-click        │   │
│  │  • Merged cells show thicker border (═══)                    │   │
│  │  • Objects automatically span merged area                    │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Available Objects                                            │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │   │
│  │  │ [Label]  │  │ [Input]  │  │[Validation]│                │   │
│  │  └──────────┘  └──────────┘  └──────────┘                  │   │
│  │                                                               │   │
│  │  Drag objects from here to grid cells above                  │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Advanced Options                                    [▼]     │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  Cell Alignment:  [Stretch ▼]                                │   │
│  │  Grid Justification:  [Start ▼]                              │   │
│  │                                                               │   │
│  │  ☑ Enable cell merging (merge cells for object spanning)      │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  [Cancel]                              [Apply Grid Layout]    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Detailed UI Components

#### 1. Layout Source Panel

```
┌─────────────────────────────────────────────────────────────┐
│  Layout Source                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ● Using Global Default  ○ Component Override               │
│                                                              │
│  [Override Global]  [Reset to Global]                       │
│                                                              │
│  💡 Global Mode: Changes affect all components              │
│  💡 Override Mode: Changes affect only this component       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 2. Grid Settings Panel

```
┌─────────────────────────────────────────────────────────────┐
│  Grid Settings                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  💡 Using Global Default (changes affect all components)    │
│                                                              │
│  Rows:    [─] 3  [+]    (Range: 1-12)                       │
│  Columns: [─] 2  [+]    (Range: 1-12)                       │
│                                                              │
│  Column Gap:  [══════●══════]  8px    (Range: 0-48px)      │
│  Row Gap:     [══════●══════]  8px    (Range: 0-48px)       │
│                                                              │
│  ☑ Sync gaps (keep row and column gaps equal)               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Controls:**
- **Layout Source Indicator**: Shows whether editing global defaults or component override
- **Override Global Button**: Creates component override from current global values
- **Reset to Global Button**: Removes component override, returns to global defaults
- **Rows/Columns**: Number inputs with increment/decrement buttons
- **Column Gap**: Default horizontal gap slider (applies to all columns by default)
- **Row Gap**: Default vertical gap slider (applies to all rows by default)
- **Individual Column Spacing**: Per-column gap controls with reset buttons
  - Each column shows spacing control for gap to the right of it
  - "Reset" button restores default column gap
  - Only visible columns have spacing controls
- **Individual Row Spacing**: Per-row gap controls with reset buttons
  - Each row shows spacing control for gap below it
  - "Reset" button restores default row gap
  - Only visible rows have spacing controls
- **Sync Gaps**: Checkbox to keep row and column gaps synchronized (when enabled, updates all gaps together)

**Mode Indicators:**
- **Global Mode**: "Using Global Default" badge, changes affect all components
- **Component Override Mode**: "Component Override" badge, changes affect only this component

#### 3. Grid Preview Area

```
┌─────────────────────────────────────────────────────────────┐
│  Grid Preview                                    [Clear All] │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │              │  │              │  ← Row 0                │
│  │   [Label]    │  │   [Input]    │                        │
│  │              │  │              │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │              │  │              │  ← Row 1                │
│  │              │  │[Validation]   │                        │
│  │              │  │              │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │              │  │              │  ← Row 2                │
│  │              │  │              │                        │
│  │              │  │              │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                              │
│  Column 0          Column 1                                 │
│                                                              │
│  [Empty cells show drop zone indicator when dragging]        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- **Visual Grid**: Shows actual grid structure with cells
- **Drop Zones**: Empty cells highlight when dragging objects
- **Object Indicators**: Shows which objects are in which cells
- **Row/Column Labels**: Clear labeling for grid structure
- **Cell Merging**: 
  - Right-click on cell to open context menu with "Merge" options
  - Select multiple cells (Shift+Click or drag) then right-click to merge
  - Merged cells show visual border indicating merged state
  - Objects in merged cells automatically span the merged area
- **Span Controls**: When object is selected, shows span controls (rowSpan × colSpan)
- **Clear All Button**: Quick reset of all assignments and merges

#### 3. Available Objects Pool

```
┌─────────────────────────────────────────────────────────────┐
│  Available Objects                                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ [Label]  │  │ [Input]  │  │[Validation]│                │
│  └──────────┘  └──────────┘  └──────────┘                 │
│                                                              │
│  Drag objects from here to grid cells above                  │
│                                                              │
│  Objects already placed in grid are dimmed but still         │
│  draggable (can be moved to different cells)                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Shows all available objects from component structure
- Objects can be dragged to grid cells
- Objects already in grid remain visible but dimmed
- Clicking an object in grid selects it (shows properties)

#### 5. Advanced Options Panel

```
┌─────────────────────────────────────────────────────────────┐
│  Advanced Options                                    [▼]     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Cell Alignment:  [Stretch ▼]                                │
│    • Start    - Align objects to start of cell              │
│    • Center   - Center objects within cell                    │
│    • End      - Align objects to end of cell                │
│    • Stretch  - Objects fill entire cell (default)           │
│                                                              │
│  Grid Justification:  [Start ▼]                               │
│    • Start          - Grid starts at container start         │
│    • Center         - Grid centered in container             │
│    • End            - Grid aligned to container end          │
│    • Stretch        - Grid fills container width             │
│    • Space Between  - Equal space between columns           │
│    • Space Around   - Equal space around columns             │
│    • Space Evenly   - Equal space everywhere                 │
│                                                              │
│  Cell Merging:                                                 │
│  ☑ Enable cell merging                                        │
│     When enabled, cells can be merged horizontally,          │
│     vertically, or both. Objects automatically span          │
│     merged cells.                                             │
│                                                              │
│  Merge Options:                                               │
│    • Right-click single cell → Merge options menu            │
│    • Select multiple cells → Right-click → Merge             │
│    • Merged cells show visual indicator (thicker border)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Interaction Flow

### 1. Opening Grid Layout Modal

**Trigger:** User clicks "Grid Layout" button in Object Layout section of Properties Panel

**Preconditions:**
- Component must have a structure with objects
- Component is selected on canvas

**Initial State:**
- **If component has `gridLayout` override**: Load component configuration, show "Component Override" selected
- **If component uses global default**: Load `globalStyles.defaultGridLayout`, show "Using Global Default" selected
- **If no global default exists**: Use system defaults (3 rows, 1 column, 8px gaps)

**Layout Source Indicator:**
- Shows whether current configuration comes from global defaults or component override
- "Override Global" button: Creates component override from current global values
- "Reset to Global" button: Removes component override, returns to global defaults

### 2. Configuring Grid Structure

**Steps:**
1. User adjusts rows/columns using number inputs
2. Grid preview updates in real-time
3. User adjusts gap sliders
4. Preview shows updated spacing

**Validation:**
- Rows: 1-12 (inclusive)
- Columns: 1-12 (inclusive)
- Gaps: 0-48px (inclusive)

### 3. Assigning Objects to Grid Cells

**Drag and Drop:**
1. User drags object from "Available Objects" pool
2. Grid cells highlight as drop zones
3. User drops object on target cell
4. Object appears in that cell
5. Object is removed from "Available Objects" (or dimmed if duplicates allowed)

**Click to Assign:**
1. User clicks empty grid cell
2. Dropdown menu appears with available objects
3. User selects object
4. Object is assigned to that cell

**Remove Object:**
1. User clicks object in grid cell
2. Context menu appears
3. User selects "Remove"
4. Object returns to "Available Objects" pool

### 4. Cell Merging and Spanning

**Merging Cells (Visual Method):**
1. User selects one or more adjacent cells (click to select, Shift+Click for multiple)
2. Right-click to open context menu
3. Select "Merge Cells" → options: "Merge Horizontally", "Merge Vertically", "Merge Both"
4. Selected cells visually merge into single cell
5. If cell contains object, object automatically spans merged area
6. Merged cells show visual indicator (thicker border or background)

**Unmerging Cells:**
1. User right-clicks on merged cell
2. Context menu shows "Unmerge Cells" option
3. Merged cells split back into individual cells
4. Object span adjusts automatically (if object was spanning merged area)

**Spanning via Properties (Alternative Method):**
1. User selects object in grid cell
2. Properties panel shows span controls
3. User adjusts `rowSpan` and `colSpan` values
4. Object visually spans multiple cells
5. Spanned cells show as "occupied" and cannot accept other objects
6. Merged cells are automatically created when spanning is applied

### 5. Adjusting Individual Row Spacing

**Steps:**
1. User expands "Individual Row Spacing" section in Grid Settings
2. For each row (0 to rows-1), a slider appears showing gap below that row
3. User adjusts slider for specific row
4. Preview updates to show new spacing
5. "Reset" button restores that row's gap to default `rowGap` value
6. Changes apply immediately to preview

**Visual Feedback:**
- Row spacing controls show current gap value
- Preview shows visual spacing between rows
- Different row gaps create varied spacing throughout grid

### 6. Adjusting Individual Column Spacing

**Steps:**
1. User expands "Individual Column Spacing" section in Grid Settings
2. For each column (0 to columns-1), a slider appears showing gap to the right of that column
3. User adjusts slider for specific column
4. Preview updates to show new spacing
5. "Reset" button restores that column's gap to default `columnGap` value
6. Changes apply immediately to preview

**Visual Feedback:**
- Column spacing controls show current gap value
- Preview shows visual spacing between columns
- Different column gaps create varied spacing throughout grid

### 7. Overriding Global Defaults

**Creating Component Override:**
1. User clicks "Override Global" button
2. Current global default values are copied to `component.props.gridLayout`
3. Modal switches to "Component Override" mode
4. User can now modify values independently of global defaults
5. Changes affect only this component

**Resetting to Global:**
1. User clicks "Reset to Global" button
2. `component.props.gridLayout` is set to `undefined`
3. Component now uses `globalStyles.defaultGridLayout`
4. Modal switches to "Using Global Default" mode
5. Changes to global defaults will now affect this component

**Visual Indicators:**
- "Using Global Default" mode: Shows global values, changes affect all components
- "Component Override" mode: Shows component-specific values, changes affect only this component
- Override indicator badge shows when component has override

### 8. Applying Changes

**Apply Button (Global Mode):**
- Validates grid configuration
- Updates `globalStyles.defaultGridLayout`
- All components using global defaults are updated
- Closes modal
- Canvas updates to show new grid layout

**Apply Button (Component Override Mode):**
- Validates grid configuration
- Updates `component.props.gridLayout`
- Only this component is updated
- Closes modal
- Canvas updates to show new grid layout

**Cancel Button:**
- Discards all changes
- Closes modal
- Returns to previous state

---

## 💻 Implementation Notes

### CSS Grid Generation

```typescript
function generateGridStyles(config: GridLayoutConfig): React.CSSProperties {
    // Build row template with individual row gaps
    const rowTemplate: string[] = [];
    for (let i = 0; i < config.rows; i++) {
        rowTemplate.push('1fr');
        // Add gap after row (except last row)
        if (i < config.rows - 1) {
            const gap = config.rowGaps?.[i] ?? config.rowGap;
            rowTemplate.push(`${gap}px`);
        }
    }
    
    // Build column template with individual column gaps
    const colTemplate: string[] = [];
    for (let i = 0; i < config.columns; i++) {
        colTemplate.push('1fr');
        // Add gap after column (except last column)
        if (i < config.columns - 1) {
            const gap = config.columnGaps?.[i] ?? config.columnGap;
            colTemplate.push(`${gap}px`);
        }
    }
    
    return {
        display: 'grid',
        gridTemplateRows: rowTemplate.join(' '),
        gridTemplateColumns: colTemplate.join(' '),
        // Note: gaps are now handled via gridTemplateRows/gridTemplateColumns
        justifyContent: config.gridJustification || 'start',
        alignItems: config.cellAlignment || 'stretch',
    };
}
```

**Alternative Approach (Using CSS Grid with gap tracks):**
```typescript
function generateGridStyles(config: GridLayoutConfig): React.CSSProperties {
    // Build row template with individual row gaps
    const rowTemplate: string[] = [];
    for (let i = 0; i < config.rows; i++) {
        rowTemplate.push('1fr');
        if (i < config.rows - 1) {
            const gap = config.rowGaps?.[i] ?? config.rowGap;
            rowTemplate.push(`${gap}px`);
        }
    }
    
    // Build column template with individual column gaps
    const colTemplate: string[] = [];
    for (let i = 0; i < config.columns; i++) {
        colTemplate.push('1fr');
        if (i < config.columns - 1) {
            const gap = config.columnGaps?.[i] ?? config.columnGap;
            colTemplate.push(`${gap}px`);
        }
    }
    
    return {
        display: 'grid',
        gridTemplateRows: rowTemplate.join(' '),
        gridTemplateColumns: colTemplate.join(' '),
        // Fallback gaps for browsers that don't support gap tracks
        columnGap: `${config.columnGap}px`,
        rowGap: `${config.rowGap}px`,
        justifyContent: config.gridJustification || 'start',
        alignItems: config.cellAlignment || 'stretch',
    };
}
```

### Cell Assignment Mapping

```typescript
function getObjectPosition(objectId: string, config: GridLayoutConfig): { row: number; col: number } | null {
    for (const [cellKey, assignedObjectId] of Object.entries(config.cellAssignments)) {
        if (assignedObjectId === objectId) {
            const [row, col] = cellKey.split('-').map(Number);
            return { row, col };
        }
    }
    return null;
}

function getObjectGridArea(objectId: string, config: GridLayoutConfig): string {
    const position = getObjectPosition(objectId, config);
    if (!position) return 'unset';
    
    // Check if object is in a merged cell group
    const mergedGroup = Object.values(config.mergedCells || {}).find(
        group => group.objectId === objectId
    );
    
    if (mergedGroup && mergedGroup.cells.length > 0) {
        // Calculate span from merged cells
        const cellPositions = mergedGroup.cells.map(cellKey => {
            const [row, col] = cellKey.split('-').map(Number);
            return { row, col };
        });
        
        const minRow = Math.min(...cellPositions.map(p => p.row));
        const maxRow = Math.max(...cellPositions.map(p => p.row));
        const minCol = Math.min(...cellPositions.map(p => p.col));
        const maxCol = Math.max(...cellPositions.map(p => p.col));
        
        const rowSpan = maxRow - minRow + 1;
        const colSpan = maxCol - minCol + 1;
        
        return `${minRow + 1} / ${minCol + 1} / ${minRow + 1 + rowSpan} / ${minCol + 1 + colSpan}`;
    }
    
    // Use explicit span configuration
    const span = config.objectSpans?.[objectId];
    const rowSpan = span?.rowSpan || 1;
    const colSpan = span?.colSpan || 1;
    
    return `${position.row + 1} / ${position.col + 1} / ${position.row + 1 + rowSpan} / ${position.col + 1 + colSpan}`;
}

function mergeCells(
    cellKeys: string[],
    objectId: string | null,
    config: GridLayoutConfig
): GridLayoutConfig {
    if (cellKeys.length < 2) return config;
    
    // Validate cells are adjacent
    const positions = cellKeys.map(key => {
        const [row, col] = key.split('-').map(Number);
        return { row, col, key };
    });
    
    // Check if cells form a rectangle (valid merge)
    const rows = [...new Set(positions.map(p => p.row))].sort((a, b) => a - b);
    const cols = [...new Set(positions.map(p => p.col))].sort((a, b) => a - b);
    
    const expectedCells = rows.length * cols.length;
    if (cellKeys.length !== expectedCells) {
        throw new Error('Cells must form a rectangle to merge');
    }
    
    // Create merged cell group
    const mergeId = `merge-${Date.now()}`;
    const mergedCells = {
        ...(config.mergedCells || {}),
        [mergeId]: {
            cells: cellKeys,
            objectId: objectId || ''
        }
    };
    
    // If objectId provided, assign to first cell and update spans
    let cellAssignments = { ...config.cellAssignments };
    let objectSpans = { ...(config.objectSpans || {}) };
    
    if (objectId) {
        // Assign object to first cell (top-left)
        const firstCell = positions[0].key;
        cellAssignments[firstCell] = objectId;
        
        // Remove object from other cells
        cellKeys.slice(1).forEach(key => {
            if (cellAssignments[key] === objectId) {
                delete cellAssignments[key];
            }
        });
        
        // Set span to match merged area
        objectSpans[objectId] = {
            rowSpan: rows.length,
            colSpan: cols.length
        };
    }
    
    return {
        ...config,
        mergedCells,
        cellAssignments,
        objectSpans
    };
}

function unmergeCells(mergeId: string, config: GridLayoutConfig): GridLayoutConfig {
    const mergedCells = { ...(config.mergedCells || {}) };
    delete mergedCells[mergeId];
    
    return {
        ...config,
        mergedCells
    };
}
```

### Integration with UniversalFieldShell

```typescript
// In UniversalFieldShell.tsx
function renderWithGridLayout(
    structure: ComponentStructure,
    gridLayout: GridLayoutConfig,
    renderers: ObjectRenderers
): React.ReactNode {
    const gridStyles = generateGridStyles(gridLayout);
    
    return (
        <div style={gridStyles} className="grid-layout-container">
            {structure.objects.map(obj => {
                const gridArea = getObjectGridArea(obj.id, gridLayout);
                if (!gridArea || gridArea === 'unset') return null;
                
                const Renderer = renderers[obj.id];
                if (!Renderer) return null;
                
                return (
                    <div key={obj.id} style={{ gridArea }}>
                        <Renderer />
                    </div>
                );
            })}
        </div>
    );
}
```

### Priority Resolution

```typescript
/**
 * Get effective grid layout configuration for a component
 * Merges global defaults with component overrides
 */
function getEffectiveGridLayout(
    component: FormComponent,
    globalStyles: GlobalStyles
): GridLayoutConfig | null {
    const global = globalStyles.defaultGridLayout;
    const componentOverride = component.props.gridLayout;
    
    // If component has gridLayout override, use it (with global fallbacks for undefined properties)
    if (componentOverride) {
        return {
            rows: componentOverride.rows ?? global?.rows ?? 3,
            columns: componentOverride.columns ?? global?.columns ?? 1,
            columnGap: componentOverride.columnGap ?? global?.columnGap ?? 8,
            rowGap: componentOverride.rowGap ?? global?.rowGap ?? 8,
            columnGaps: componentOverride.columnGaps ?? global?.columnGaps,
            rowGaps: componentOverride.rowGaps ?? global?.rowGaps,
            cellAssignments: componentOverride.cellAssignments ?? global?.cellAssignments ?? {},
            mergedCells: componentOverride.mergedCells ?? global?.mergedCells,
            objectSpans: componentOverride.objectSpans ?? global?.objectSpans,
            cellAlignment: componentOverride.cellAlignment ?? global?.cellAlignment ?? 'stretch',
            gridJustification: componentOverride.gridJustification ?? global?.gridJustification ?? 'start',
        };
    }
    
    // If global has defaultGridLayout, use it
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
 * Determine which layout system to use (Grid vs Object Layout)
 */
function getEffectiveLayout(component: FormComponent, globalStyles: GlobalStyles): 'object' | 'grid' | null {
    // Grid Layout takes precedence if defined (component or global)
    const gridLayout = getEffectiveGridLayout(component, globalStyles);
    if (gridLayout) {
        return 'grid';
    }
    
    // Otherwise use Object Layout
    if (component.props.objectLayout || globalStyles.defaultObjectLayout) {
        return 'object';
    }
    
    // Fallback to structure default
    return 'object'; // Default to object layout
}

/**
 * Check if component has grid layout override (vs using global default)
 */
function hasGridLayoutOverride(component: FormComponent): boolean {
    return component.props.gridLayout !== undefined;
}

/**
 * Reset component grid layout to use global defaults
 */
function resetToGlobalDefault(component: FormComponent): Partial<ComponentProps> {
    return {
        gridLayout: undefined  // Removing override makes it use global default
    };
}
```

---

## 📋 Example Configurations

### Example 1: Simple Vertical Layout (3 rows, 1 column)

```typescript
{
    rows: 3,
    columns: 1,
    columnGap: 8,
    rowGap: 8,
    cellAssignments: {
        "0-0": "label",
        "1-0": "input",
        "2-0": "validation"
    }
}
```

**Visual Result:**
```
┌──────────────┐
│   [Label]    │
├──────────────┤
│   [Input]    │
├──────────────┤
│ [Validation] │
└──────────────┘
```

### Example 2: Horizontal Layout (1 row, 3 columns)

```typescript
{
    rows: 1,
    columns: 3,
    columnGap: 12,
    rowGap: 8,
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "0-2": "validation"
    }
}
```

**Visual Result:**
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ [Label]  │  │ [Input]  │  │[Validation]│
└──────────┘  └──────────┘  └──────────┘
```

### Example 3: Complex Multi-Column Layout (2 rows, 2 columns)

```typescript
{
    rows: 2,
    columns: 2,
    columnGap: 16,
    rowGap: 12,
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "1-0": "validation",
        "1-1": "help"
    },
    objectSpans: {
        "input": { colSpan: 1 },
        "validation": { colSpan: 2 }  // Spans both columns
    }
}
```

**Visual Result:**
```
┌──────────┐  ┌──────────┐
│ [Label]  │  │ [Input]  │
├──────────┴──┴──────────┤
│   [Validation spans]   │
└────────────────────────┘
```

### Example 4: Label Beside Input (2 rows, 2 columns)

```typescript
{
    rows: 2,
    columns: 2,
    columnGap: 12,
    rowGap: 8,
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "1-1": "validation"  // Validation below input only
    }
}
```

**Visual Result:**
```
┌──────────┐  ┌──────────┐
│ [Label]  │  │ [Input]  │
│          ├──┴──────────┤
│          │[Validation] │
└──────────┴─────────────┘
```

### Example 5: Individual Column Spacing (1 row, 3 columns with varied gaps)

```typescript
{
    rows: 1,
    columns: 3,
    columnGap: 8,  // Default gap
    columnGaps: {
        0: 20,  // Larger gap after column 0 (between label and input)
        1: 8    // Default gap after column 1
    },
    rowGap: 8,
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "0-2": "validation"
    }
}
```

**Visual Result:**
```
┌──────────┐      ┌──────────┐  ┌──────────┐
│ [Label]  │      │ [Input]  │  │[Validation]│
└──────────┘      └──────────┘  └──────────┘
     ↑ 20px gap      ↑ 8px gap
```

### Example 6: Individual Row Spacing (3 rows, 1 column with varied gaps)

```typescript
{
    rows: 3,
    columns: 1,
    columnGap: 8,
    rowGap: 8,  // Default gap
    rowGaps: {
        0: 16,  // Larger gap below row 0 (between label and input)
        1: 4    // Smaller gap below row 1 (between input and validation)
    },
    cellAssignments: {
        "0-0": "label",
        "1-0": "input",
        "2-0": "validation"
    }
}
```

**Visual Result:**
```
┌──────────────┐
│   [Label]    │
│              │  ← 16px gap (custom)
├──────────────┤
│   [Input]    │
│              │  ← 4px gap (custom)
├──────────────┤
│ [Validation] │
└──────────────┘
```

### Example 7: Merged Cells with Spanning (2 rows, 2 columns)

```typescript
{
    rows: 2,
    columns: 2,
    columnGap: 12,
    rowGap: 8,
    cellAssignments: {
        "0-0": "label",
        "0-1": "input"
    },
    mergedCells: {
        "merge-1": {
            cells: ["1-0", "1-1"],  // Merged cells in row 1
            objectId: "validation"
        }
    },
    objectSpans: {
        "validation": { rowSpan: 1, colSpan: 2 }  // Spans both columns
    }
}
```

**Visual Result:**
```
┌──────────┐  ┌──────────┐
│ [Label]  │  │ [Input]  │
├──────────┴──┴──────────┤
│   [Validation spans]    │  ← Merged cells (1×2)
└────────────────────────┘
```

### Example 8: Individual Row and Column Spacing Combined (3 rows, 3 columns)

```typescript
{
    rows: 3,
    columns: 3,
    columnGap: 8,  // Default column gap
    rowGap: 8,     // Default row gap
    columnGaps: {
        0: 16,  // Larger gap after column 0
        1: 4    // Smaller gap after column 1
    },
    rowGaps: {
        0: 12,  // Larger gap below row 0
        1: 4    // Smaller gap below row 1
    },
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "0-2": "help",
        "1-0": "validation",
        "2-0": "status"
    }
}
```

**Visual Result:**
```
┌──────────┐      ┌──────────┐ ┌──────────┐
│ [Label]  │      │ [Input]  │ │  [Help]  │
└──────────┘      └──────────┘ └──────────┘
     ↑ 16px          ↑ 4px
│                    │
│  12px gap          │
│                    │
├────────────────────┴──────────┐ ┌──────────┐
│   [Validation]                │ │          │
└───────────────────────────────┘ └──────────┘
│
│  4px gap
│
├──────────┐
│ [Status] │
└──────────┘
```

### Example 9: Complex Merged Layout (3 rows, 3 columns)

```typescript
{
    rows: 3,
    columns: 3,
    columnGap: 8,
    rowGap: 8,
    rowGaps: {
        1: 16  // Extra space between row 1 and row 2
    },
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "2-0": "help"
    },
    mergedCells: {
        "merge-1": {
            cells: ["0-0", "0-1", "0-2"],  // Label spans entire first row
            objectId: "label"
        },
        "merge-2": {
            cells: ["2-0", "2-1", "2-2"],  // Help spans entire last row
            objectId: "help"
        }
    },
    objectSpans: {
        "label": { rowSpan: 1, colSpan: 3 },
        "help": { rowSpan: 1, colSpan: 3 }
    }
}
```

**Visual Result:**
```
┌────────────────────────────┐
│   [Label spans 3 columns]  │  ← Merged (1×3)
├────────────────────────────┤
│        [Input]             │
│                            │  ← 16px gap (custom)
├────────────────────────────┤
│   [Help spans 3 columns]   │  ← Merged (1×3)
└────────────────────────────┘
```

### Example 10: Global Defaults with Component Overrides

**Global Default Configuration:**
```typescript
// Set in Global Properties Panel
globalStyles.defaultGridLayout = {
    rows: 3,
    columns: 1,
    columnGap: 8,
    rowGap: 8,
    rowGaps: {
        0: 12  // Larger gap below label globally
    },
    cellAlignment: 'stretch',
    gridJustification: 'start'
};
```

**Component A: Uses Global Default**
```typescript
// Component A has no gridLayout override
componentA.props.gridLayout = undefined;

// Effective configuration (inherits from global):
{
    rows: 3,           // From global
    columns: 1,        // From global
    columnGap: 8,      // From global
    rowGap: 8,         // From global
    rowGaps: { 0: 12 }, // From global
    cellAlignment: 'stretch',  // From global
    gridJustification: 'start' // From global
}
```

**Component B: Partial Override**
```typescript
// Component B overrides only rows and columnGap
componentB.props.gridLayout = {
    rows: 4,        // Override: 4 rows instead of 3
    columnGap: 16   // Override: larger column gap
    // Other properties inherit from global
};

// Effective configuration (merged):
{
    rows: 4,           // From component override
    columns: 1,        // From global (inherited)
    columnGap: 16,     // From component override
    rowGap: 8,         // From global (inherited)
    rowGaps: { 0: 12 }, // From global (inherited)
    cellAlignment: 'stretch',  // From global (inherited)
    gridJustification: 'start' // From global (inherited)
}
```

**Component C: Complete Override**
```typescript
// Component C has complete override (independent of global)
componentC.props.gridLayout = {
    rows: 2,
    columns: 2,
    columnGap: 12,
    rowGap: 6,
    columnGaps: {
        0: 20  // Custom column spacing
    },
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "1-0": "validation"
    }
};

// Effective configuration (no inheritance):
{
    rows: 2,           // From component override
    columns: 2,         // From component override
    columnGap: 12,     // From component override
    rowGap: 6,         // From component override
    columnGaps: { 0: 20 }, // From component override
    // Global defaults not used
}
```

**Visual Comparison:**
```
Component A (Global Default):
┌──────────────┐
│   [Label]    │
│              │  ← 12px gap (from global)
├──────────────┤
│   [Input]    │
├──────────────┤
│ [Validation] │
└──────────────┘

Component B (Partial Override):
┌──────────────┐
│   [Label]    │
│              │  ← 12px gap (from global)
├──────────────┤
│   [Input]    │
├──────────────┤
│ [Validation] │
├──────────────┤
│   [Help]     │  ← Extra row (component override)
└──────────────┘

Component C (Complete Override):
┌──────────┐      ┌──────────┐
│ [Label] │      │ [Input]  │
└──────────┘      └──────────┘
     ↑ 20px gap
├────────────────┐
│ [Validation]   │
└────────────────┘
```

```typescript
{
    rows: 3,
    columns: 3,
    columnGap: 8,
    rowGap: 8,
    rowGaps: {
        1: 16  // Extra space between row 1 and row 2
    },
    cellAssignments: {
        "0-0": "label",
        "0-1": "input",
        "2-0": "help"
    },
    mergedCells: {
        "merge-1": {
            cells: ["0-0", "0-1", "0-2"],  // Label spans entire first row
            objectId: "label"
        },
        "merge-2": {
            cells: ["2-0", "2-1", "2-2"],  // Help spans entire last row
            objectId: "help"
        }
    },
    objectSpans: {
        "label": { rowSpan: 1, colSpan: 3 },
        "help": { rowSpan: 1, colSpan: 3 }
    }
}
```

**Visual Result:**
```
┌────────────────────────────┐
│   [Label spans 3 columns]  │  ← Merged (1×3)
├────────────────────────────┤
│        [Input]             │
│                            │  ← 16px gap (custom)
├────────────────────────────┤
│   [Help spans 3 columns]   │  ← Merged (1×3)
└────────────────────────────┘
```

---

## 🌐 Global Properties Panel Integration

### Setting Global Grid Layout Defaults

The Grid Layout system integrates with the Global Properties Panel, allowing form-wide defaults to be set:

**Location:** Global Properties Panel → Grid Layout Section

**UI Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│  Global Properties Panel                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Grid Layout (Global Defaults)                      │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │  Default Rows:    [─] 3  [+]                       │   │
│  │  Default Columns: [─] 1  [+]                       │   │
│  │                                                      │   │
│  │  Default Column Gap:  [══════●══════]  8px         │   │
│  │  Default Row Gap:     [══════●══════]  8px         │   │
│  │                                                      │   │
│  │  [Individual Column Spacing...]                     │   │
│  │  [Individual Row Spacing...]                        │   │
│  │                                                      │   │
│  │  Default Cell Alignment:  [Stretch ▼]              │   │
│  │  Default Grid Justification:  [Start ▼]            │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Changes to global defaults apply to all components using global defaults
- Components with overrides are not affected by global changes
- Global defaults provide a consistent starting point for all components
- Individual components can override any global property

**Use Cases:**
- **Form-wide consistency**: Set default grid structure for entire form
- **Brand guidelines**: Enforce consistent spacing across all components
- **Rapid prototyping**: Quickly apply grid layout to all components
- **Bulk updates**: Change spacing for all components at once

---

## 🔗 Integration with Existing Systems

### Global vs Component Level

**Global Defaults (`globalStyles.defaultGridLayout`):**
- Set once at the form level
- Apply to all components that don't have component-level overrides
- Changes to global defaults affect all components using them
- Useful for consistent grid layouts across the form

**Component Overrides (`component.props.gridLayout`):**
- Override global defaults for specific components
- Component-specific configuration takes precedence
- Changes affect only that component
- Useful for components that need unique grid layouts

**Resolution Priority:**
1. Component override (`component.props.gridLayout`) - highest priority
2. Global default (`globalStyles.defaultGridLayout`) - fallback
3. System defaults (hardcoded) - final fallback

### Object Layout vs Grid Layout

**Coexistence:**
- Both layout systems can exist in the same component props
- Grid Layout takes precedence when `gridLayout` is defined (component or global)
- Object Layout is used as fallback when `gridLayout` is undefined

**Switching Between Layouts:**
- User can switch from Object Layout to Grid Layout via modal
- Existing `objectLayout` and `layoutGroups` are preserved
- User can switch back to Object Layout (clears `gridLayout`)

**Global vs Component:**
- Global Grid Layout defaults can be set independently of Object Layout defaults
- Component can override Grid Layout while still using global Object Layout defaults
- Each layout system (Grid/Object) has its own global/component hierarchy

### Component Structure Compatibility

**Objects:**
- Grid Layout uses the same objects as Object Layout
- Objects are defined in `ComponentStructure.objects`
- Conditional objects follow the same visibility rules

**Archetypes:**
- Object styling (PrimaryLabel, InputControl, HelperText) remains unchanged
- Grid Layout only affects positioning, not styling

### Global Styles Integration

**Global Defaults:**
- `defaultGridLayout` in `GlobalStyles` provides form-wide defaults
- Set via Global Properties Panel → Grid Layout section
- Applies to all components that don't have component-level overrides
- Changes propagate to all components using global defaults

**Component Overrides:**
- `gridLayout` in `ComponentProps` overrides global defaults
- Set via Component Properties Panel → Grid Layout section
- Only affects the specific component
- Can override entire configuration or individual properties

**Inheritance Pattern:**
- Same pattern as Object Layout (`defaultObjectLayout` → `objectLayout`)
- Same pattern as Typography & Spacing (global → component styleOverrides)
- Consistent with framework's global-first approach

**Example Inheritance:**
```typescript
// Global default (affects all components)
globalStyles.defaultGridLayout = {
    rows: 3,
    columns: 1,
    columnGap: 8,
    rowGap: 8
};

// Component A: Uses global default (no override)
componentA.props.gridLayout = undefined;  // → Uses global

// Component B: Overrides rows only
componentB.props.gridLayout = {
    rows: 4,  // Override: 4 rows instead of 3
    // Other properties inherit from global
    columns: 1,      // From global
    columnGap: 8,    // From global
    rowGap: 8        // From global
};

// Component C: Complete override
componentC.props.gridLayout = {
    rows: 2,
    columns: 2,
    columnGap: 16,
    rowGap: 12
    // Independent of global defaults
};
```

---

## ✅ Validation Rules

### Grid Configuration Validation

```typescript
function validateGridLayout(config: GridLayoutConfig): ValidationResult {
    const errors: string[] = [];
    
    // Rows validation
    if (config.rows < 1 || config.rows > 12) {
        errors.push('Rows must be between 1 and 12');
    }
    
    // Columns validation
    if (config.columns < 1 || config.columns > 12) {
        errors.push('Columns must be between 1 and 12');
    }
    
    // Gap validation
    if (config.columnGap < 0 || config.columnGap > 48) {
        errors.push('Column gap must be between 0 and 48px');
    }
    
    if (config.rowGap < 0 || config.rowGap > 48) {
        errors.push('Row gap must be between 0 and 48px');
    }
    
    // Individual column gap validation
    if (config.columnGaps) {
        for (const [colIndexStr, gap] of Object.entries(config.columnGaps)) {
            const colIndex = Number(colIndexStr);
            if (colIndex < 0 || colIndex >= config.columns - 1) {
                errors.push(`Column gap override for column ${colIndex} is invalid (must be 0 to ${config.columns - 2})`);
            }
            if (gap < 0 || gap > 48) {
                errors.push(`Column gap for column ${colIndex} must be between 0 and 48px`);
            }
        }
    }
    
    // Individual row gap validation
    if (config.rowGaps) {
        for (const [rowIndexStr, gap] of Object.entries(config.rowGaps)) {
            const rowIndex = Number(rowIndexStr);
            if (rowIndex < 0 || rowIndex >= config.rows - 1) {
                errors.push(`Row gap override for row ${rowIndex} is invalid (must be 0 to ${config.rows - 2})`);
            }
            if (gap < 0 || gap > 48) {
                errors.push(`Row gap for row ${rowIndex} must be between 0 and 48px`);
            }
        }
    }
    
    // Merged cells validation
    if (config.mergedCells) {
        for (const [mergeId, mergeGroup] of Object.entries(config.mergedCells)) {
            if (mergeGroup.cells.length < 2) {
                errors.push(`Merged cell group "${mergeId}" must contain at least 2 cells`);
            }
            
            // Validate all cells in merge are valid
            for (const cellKey of mergeGroup.cells) {
                const [row, col] = cellKey.split('-').map(Number);
                if (row < 0 || row >= config.rows) {
                    errors.push(`Merged cell "${cellKey}" has invalid row`);
                }
                if (col < 0 || col >= config.columns) {
                    errors.push(`Merged cell "${cellKey}" has invalid column`);
                }
            }
            
            // Validate cells form a rectangle
            const positions = mergeGroup.cells.map(key => {
                const [row, col] = key.split('-').map(Number);
                return { row, col };
            });
            const rows = [...new Set(positions.map(p => p.row))].sort((a, b) => a - b);
            const cols = [...new Set(positions.map(p => p.col))].sort((a, b) => a - b);
            const expectedCells = rows.length * cols.length;
            
            if (mergeGroup.cells.length !== expectedCells) {
                errors.push(`Merged cell group "${mergeId}" cells must form a rectangle`);
            }
        }
    }
    
    // Cell assignment validation
    for (const [cellKey, objectId] of Object.entries(config.cellAssignments)) {
        const [row, col] = cellKey.split('-').map(Number);
        
        if (row < 0 || row >= config.rows) {
            errors.push(`Cell assignment "${cellKey}" has invalid row`);
        }
        
        if (col < 0 || col >= config.columns) {
            errors.push(`Cell assignment "${cellKey}" has invalid column`);
        }
    }
    
    // Span validation
    if (config.objectSpans) {
        for (const [objectId, span] of Object.entries(config.objectSpans)) {
            const position = getObjectPosition(objectId, config);
            if (!position) {
                errors.push(`Object "${objectId}" has span but no cell assignment`);
                continue;
            }
            
            if (span.rowSpan && (position.row + span.rowSpan > config.rows)) {
                errors.push(`Object "${objectId}" rowSpan exceeds grid rows`);
            }
            
            if (span.colSpan && (position.col + span.colSpan > config.columns)) {
                errors.push(`Object "${objectId}" colSpan exceeds grid columns`);
            }
        }
    }
    
    return {
        isValid: errors.length === 0,
        errors
    };
}
```

---

## 🎨 UI Component Specifications

### Grid Cell Component

```typescript
interface GridCellProps {
    row: number;
    col: number;
    objectId: string | null;
    isDropZone: boolean;
    onDrop: (objectId: string) => void;
    onRemove: () => void;
    onSelect: () => void;
}

const GridCell: React.FC<GridCellProps> = ({
    row,
    col,
    objectId,
    isDropZone,
    onDrop,
    onRemove,
    onSelect
}) => {
    const { setNodeRef, isOver } = useDroppable({
        id: `cell-${row}-${col}`
    });
    
    return (
        <div
            ref={setNodeRef}
            className={`
                grid-cell
                ${isOver ? 'drop-zone-active' : ''}
                ${objectId ? 'has-object' : 'empty'}
            `}
            onClick={onSelect}
        >
            {objectId ? (
                <div className="cell-object">
                    <span>{objectId}</span>
                    <button onClick={onRemove}>×</button>
                </div>
            ) : (
                <div className="cell-empty">
                    {isDropZone ? 'Drop here' : ''}
                </div>
            )}
        </div>
    );
};
```

### Grid Settings Panel Component

```typescript
interface GridSettingsPanelProps {
    config: GridLayoutConfig;
    onChange: (updates: Partial<GridLayoutConfig>) => void;
}

const GridSettingsPanel: React.FC<GridSettingsPanelProps> = ({
    config,
    onChange
}) => {
    const handleColumnGapChange = (colIndex: number, gap: number) => {
        const columnGaps = { ...(config.columnGaps || {}) };
        if (gap === config.columnGap) {
            // Reset to default: remove override
            delete columnGaps[colIndex];
        } else {
            columnGaps[colIndex] = gap;
        }
        onChange({ columnGaps });
    };
    
    const handleRowGapChange = (rowIndex: number, gap: number) => {
        const rowGaps = { ...(config.rowGaps || {}) };
        if (gap === config.rowGap) {
            // Reset to default: remove override
            delete rowGaps[rowIndex];
        } else {
            rowGaps[rowIndex] = gap;
        }
        onChange({ rowGaps });
    };
    
    return (
        <div className="grid-settings-panel">
            <div className="setting-row">
                <label>Rows:</label>
                <NumberInput
                    value={config.rows}
                    min={1}
                    max={12}
                    onChange={(rows) => onChange({ rows })}
                />
            </div>
            
            <div className="setting-row">
                <label>Columns:</label>
                <NumberInput
                    value={config.columns}
                    min={1}
                    max={12}
                    onChange={(columns) => onChange({ columns })}
                />
            </div>
            
            <div className="setting-row">
                <label>Column Gap (Default):</label>
                <Slider
                    value={config.columnGap}
                    min={0}
                    max={48}
                    onChange={(columnGap) => onChange({ columnGap })}
                />
                <span>{config.columnGap}px</span>
            </div>
            
            <div className="setting-row">
                <label>Row Gap (Default):</label>
                <Slider
                    value={config.rowGap}
                    min={0}
                    max={48}
                    onChange={(rowGap) => onChange({ rowGap })}
                />
                <span>{config.rowGap}px</span>
            </div>
            
            {/* Individual Column Spacing */}
            {config.columns > 1 && (
                <div className="individual-column-spacing">
                    <label className="section-label">Individual Column Spacing:</label>
                    {Array.from({ length: config.columns - 1 }, (_, i) => {
                        const currentGap = config.columnGaps?.[i] ?? config.columnGap;
                        const isCustom = config.columnGaps?.[i] !== undefined;
                        
                        return (
                            <div key={i} className="setting-row column-gap-control">
                                <label>Col {i} → Col {i + 1}:</label>
                                <Slider
                                    value={currentGap}
                                    min={0}
                                    max={48}
                                    onChange={(gap) => handleColumnGapChange(i, gap)}
                                />
                                <span className={isCustom ? 'custom-value' : ''}>
                                    {currentGap}px
                                </span>
                                {isCustom && (
                                    <button
                                        type="button"
                                        onClick={() => handleColumnGapChange(i, config.columnGap)}
                                        className="reset-button"
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
            
            {/* Individual Row Spacing */}
            {config.rows > 1 && (
                <div className="individual-row-spacing">
                    <label className="section-label">Individual Row Spacing:</label>
                    {Array.from({ length: config.rows - 1 }, (_, i) => {
                        const currentGap = config.rowGaps?.[i] ?? config.rowGap;
                        const isCustom = config.rowGaps?.[i] !== undefined;
                        
                        return (
                            <div key={i} className="setting-row row-gap-control">
                                <label>Row {i} → Row {i + 1}:</label>
                                <Slider
                                    value={currentGap}
                                    min={0}
                                    max={48}
                                    onChange={(gap) => handleRowGapChange(i, gap)}
                                />
                                <span className={isCustom ? 'custom-value' : ''}>
                                    {currentGap}px
                                </span>
                                {isCustom && (
                                    <button
                                        type="button"
                                        onClick={() => handleRowGapChange(i, config.rowGap)}
                                        className="reset-button"
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

### Grid Cell Component (Enhanced with Merging)

```typescript
interface GridCellProps {
    row: number;
    col: number;
    objectId: string | null;
    isDropZone: boolean;
    isMerged: boolean;
    mergeGroupId?: string;
    onDrop: (objectId: string) => void;
    onRemove: () => void;
    onSelect: () => void;
    onMerge: (direction: 'horizontal' | 'vertical' | 'both') => void;
    onUnmerge: () => void;
}

const GridCell: React.FC<GridCellProps> = ({
    row,
    col,
    objectId,
    isDropZone,
    isMerged,
    mergeGroupId,
    onDrop,
    onRemove,
    onSelect,
    onMerge,
    onUnmerge
}) => {
    const { setNodeRef, isOver } = useDroppable({
        id: `cell-${row}-${col}`
    });
    
    const handleContextMenu = (e: React.MouseEvent) => {
        e.preventDefault();
        // Show context menu with merge options
    };
    
    return (
        <div
            ref={setNodeRef}
            className={`
                grid-cell
                ${isOver ? 'drop-zone-active' : ''}
                ${objectId ? 'has-object' : 'empty'}
                ${isMerged ? 'merged' : ''}
            `}
            onClick={onSelect}
            onContextMenu={handleContextMenu}
        >
            {objectId ? (
                <div className="cell-object">
                    <span>{objectId}</span>
                    {isMerged && (
                        <span className="merge-indicator" title="Merged cell">
                            ⧉
                        </span>
                    )}
                    <button onClick={onRemove}>×</button>
                </div>
            ) : (
                <div className="cell-empty">
                    {isDropZone ? 'Drop here' : ''}
                </div>
            )}
        </div>
    );
};
```

---

## 📝 Migration Path

### From Object Layout to Grid Layout

**Automatic Conversion (Optional):**
```typescript
function convertObjectLayoutToGrid(
    objectLayout: ObjectLayoutType,
    layoutGroups: Record<string, string[]>
): GridLayoutConfig {
    if (objectLayout === 'vertical') {
        // Convert vertical to 3-row, 1-column grid
        const objects = Object.values(layoutGroups).flat();
        const cellAssignments: Record<string, string> = {};
        objects.forEach((objId, index) => {
            cellAssignments[`${index}-0`] = objId;
        });
        
        return {
            rows: objects.length,
            columns: 1,
            columnGap: 8,
            rowGap: 8,
            cellAssignments
        };
    }
    
    if (objectLayout === 'horizontal') {
        // Convert horizontal to 1-row, N-column grid
        const objects = Object.values(layoutGroups).flat();
        const cellAssignments: Record<string, string> = {};
        objects.forEach((objId, index) => {
            cellAssignments[`0-${index}`] = objId;
        });
        
        return {
            rows: 1,
            columns: objects.length,
            columnGap: 8,
            rowGap: 8,
            cellAssignments
        };
    }
    
    // Mixed layout: convert rows to grid rows
    const rowKeys = Object.keys(layoutGroups).sort();
    const maxColumns = Math.max(...rowKeys.map(key => layoutGroups[key].length));
    
    const cellAssignments: Record<string, string> = {};
    rowKeys.forEach((rowKey, rowIndex) => {
        layoutGroups[rowKey].forEach((objId, colIndex) => {
            cellAssignments[`${rowIndex}-${colIndex}`] = objId;
        });
    });
    
    return {
        rows: rowKeys.length,
        columns: maxColumns,
        columnGap: 8,
        rowGap: 8,
        cellAssignments
    };
}
```

---

## 🚀 Future Enhancements

### Potential Features

1. **Grid Templates**: Pre-defined grid layouts (e.g., "Form Layout", "Card Layout")
2. **Responsive Grids**: Different grid configurations for different screen sizes
3. **Grid Snapping**: Snap objects to grid cells automatically
4. **Grid Guides**: Visual guides showing grid structure on canvas
5. **Nested Grids**: Support for grids within grid cells
6. **Grid Presets**: Save and reuse custom grid configurations

---

## 📚 Related Documentation

- [Component Framework Reference](./COMPONENT-FRAMEWORK-REFERENCE.md) - Core component system
- [Component Framework Guide](./COMPONENT-FRAMEWORK-GUIDE.md) - Implementation guide
- [Object Layout Section](../frontend/src/features/builder/components/properties/ObjectLayoutSection.tsx) - Current Object Layout implementation

---

*Last Updated: January 13, 2026*
