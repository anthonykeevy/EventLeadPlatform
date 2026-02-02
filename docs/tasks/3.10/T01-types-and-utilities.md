# Task T01: Types & Utilities Foundation

**Story:** 3.10 - Grid Layout System  
**Task ID:** T01  
**Status:** ⏳ Ready  
**Dependencies:** None  
**Estimated Time:** 1-2 hours  

---

## 📋 Task Overview

**Objective:** Create the TypeScript interfaces and utility functions that form the foundation for the Grid Layout system. This is a foundation task that establishes types and helpers without UI implementation.

---

## ✅ Scope (In)

- [ ] Define `GridLayoutConfig` interface in `builder.types.ts`
- [ ] Extend `ComponentProps` with optional `gridLayout` property
- [ ] Extend `GlobalStyles` with optional `defaultGridLayout` property
- [ ] Create `gridLayoutUtils.ts` with CSS generation functions
- [ ] Create helper functions for cell coordinate handling

---

## 🚫 Scope (Out)

- ❌ Any UI components (modal, editor, etc.)
- ❌ Rendering integration (UniversalFieldShell changes)
- ❌ Drag-and-drop functionality
- ❌ Global styles panel changes
- ❌ Store changes beyond type imports

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `frontend/src/features/builder/components/` | UI components are for T02-T08 |
| `frontend/src/features/builder/stores/` | Store changes are for later tasks |
| `backend/` | No backend changes |

---

## 📐 Acceptance Criteria

### AC1: GridLayoutConfig Interface
- **Criterion:** `GridLayoutConfig` interface exists with all required properties
- **Verification:** TypeScript compiles without errors; interface matches GRID-LAYOUT-GUIDE.md schema

### AC2: ComponentProps Extension
- **Criterion:** `ComponentProps` has optional `gridLayout?: GridLayoutConfig` property
- **Verification:** Existing components still compile; new property is optional

### AC3: GlobalStyles Extension
- **Criterion:** `GlobalStyles` has optional `defaultGridLayout` property with partial grid config
- **Verification:** TypeScript compiles; property is optional and partial

### AC4: CSS Generation Utility
- **Criterion:** `generateGridStyles()` function converts `GridLayoutConfig` to CSS Grid styles
- **Verification:** Unit test or manual verification with example config

### AC5: Cell Coordinate Helpers
- **Criterion:** Helper functions exist for: `cellKey(row, col)`, `parseCell(key)`, `getObjectGridArea()`
- **Verification:** Functions return expected values for test inputs

---

## 🔧 Implementation Details

### File: `frontend/src/features/builder/types/builder.types.ts`

Add these types (reference: `docs/GRID-LAYOUT-GUIDE.md`):

```typescript
// ═══════════════════════════════════════════════════════════════
// GRID LAYOUT TYPES
// ═══════════════════════════════════════════════════════════════

export interface GridLayoutConfig {
    rows: number;                    // 1-12
    columns: number;                 // 1-12
    columnGap: number;               // Default gap (px)
    rowGap: number;                  // Default gap (px)
    columnGaps?: Record<number, number>;  // Per-column overrides
    rowGaps?: Record<number, number>;     // Per-row overrides
    cellAssignments: Record<string, string>;  // "row-col" → objectId
    mergedCells?: Record<string, { cells: string[]; objectId: string }>;
    objectSpans?: Record<string, { rowSpan?: number; colSpan?: number }>;
    cellAlignment?: 'start' | 'center' | 'end' | 'stretch';
    gridJustification?: 'start' | 'center' | 'end' | 'stretch' | 'space-between' | 'space-around' | 'space-evenly';
}

// Add to ComponentProps:
// gridLayout?: GridLayoutConfig;

// Add to GlobalStyles:
// defaultGridLayout?: Partial<GridLayoutConfig>;
```

### File: `frontend/src/features/builder/utils/gridLayoutUtils.ts` (NEW)

```typescript
import { GridLayoutConfig } from '../types/builder.types';

/**
 * Generate CSS Grid styles from GridLayoutConfig
 */
export function generateGridStyles(config: GridLayoutConfig): React.CSSProperties {
    // Build gridTemplateRows with individual gaps
    // Build gridTemplateColumns with individual gaps
    // Return CSS properties object
}

/**
 * Create cell key from row/col indices
 */
export function cellKey(row: number, col: number): string {
    return `${row}-${col}`;
}

/**
 * Parse cell key to row/col indices
 */
export function parseCell(key: string): { row: number; col: number } {
    const [row, col] = key.split('-').map(Number);
    return { row, col };
}

/**
 * Get CSS grid-area for an object based on config
 */
export function getObjectGridArea(
    objectId: string,
    config: GridLayoutConfig
): { gridRow: string; gridColumn: string } | null {
    // Find object in cellAssignments or mergedCells
    // Calculate gridRow and gridColumn based on spans
}

/**
 * Create default GridLayoutConfig
 */
export function createDefaultGridLayout(): GridLayoutConfig {
    return {
        rows: 3,
        columns: 1,
        columnGap: 8,
        rowGap: 8,
        cellAssignments: {},
    };
}

/**
 * Validate GridLayoutConfig
 */
export function validateGridLayout(config: GridLayoutConfig): string[] {
    const errors: string[] = [];
    // Validate rows/columns range
    // Validate cell assignments don't overlap
    // Validate merged cells form rectangles
    return errors;
}
```

---

## 🧪 Required Tests

### Manual Verification
1. Import `GridLayoutConfig` in a test file - should compile
2. Call `generateGridStyles({ rows: 3, columns: 2, columnGap: 8, rowGap: 8, cellAssignments: {} })`
   - Should return valid CSS properties object
3. Call `cellKey(1, 2)` - should return `"1-2"`
4. Call `parseCell("1-2")` - should return `{ row: 1, col: 2 }`

### Build Verification
```bash
cd frontend && npm run build
# Should complete without TypeScript errors
```

---

## 📝 Expected Error Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Invalid rows (0 or >12) | `validateGridLayout` returns error |
| Invalid columns (0 or >12) | `validateGridLayout` returns error |
| Overlapping cell assignments | `validateGridLayout` returns error |
| Non-rectangular merge | `validateGridLayout` returns error |

---

## 🔄 Out-of-Scope Handling

**If user asks to:**
- Add UI components → Route to T03 (Basic Grid Editor)
- Integrate with UniversalFieldShell → Route to T02 (Grid CSS Rendering)
- Add drag-and-drop → Route to T04 (Object Drag-and-Drop)
- Add global styles UI → Route to T07 (Global Defaults)

---

## 📤 Handoff Requirements

After completion, provide:
1. List of all files created/modified
2. TypeScript compilation verification (no errors)
3. Example usage of each utility function
4. Any patterns discovered → add to LESSONS-LEARNED.md

---

## 📚 References

- Specification: `docs/GRID-LAYOUT-GUIDE.md`
- Existing Types: `frontend/src/features/builder/types/builder.types.ts`
- Existing Utils Pattern: `frontend/src/features/builder/utils/spacingCalculation.ts`

---

*Task spec created by Ralf-SM*  
*Last Updated: 2026-01-14*
