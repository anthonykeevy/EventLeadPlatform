# UAT Checklist: T01

**Story:** 3.10 - Grid Layout System  
**Task:** T01 - Types & Utilities Foundation  
**Generated:** 2026-01-14

---

## Pre-conditions

- [ ] IDE open with EventLeadPlatform workspace
- [ ] TypeScript language service active (for import verification)

## Test Steps

### AC1: GridLayoutConfig Interface

- [ ] Open `frontend/src/features/builder/types/builder.types.ts`
- [ ] Search for `interface GridLayoutConfig` → Verify: Interface exists
- [ ] Verify interface contains these properties:
  - [ ] `rows: number` with JSDoc comment mentioning 1-12 range
  - [ ] `columns: number` with JSDoc comment mentioning 1-12 range
  - [ ] `columnGap: number` (default gap in px)
  - [ ] `rowGap: number` (default gap in px)
  - [ ] `columnGaps?: Record<number, number>` (optional per-column overrides)
  - [ ] `rowGaps?: Record<number, number>` (optional per-row overrides)
  - [ ] `cellAssignments: Record<string, string>` (required)
  - [ ] `mergedCells?: Record<string, { cells: string[]; objectId: string }>` (optional)
  - [ ] `objectSpans?: Record<string, { rowSpan?: number; colSpan?: number }>` (optional)
  - [ ] `cellAlignment?: 'start' | 'center' | 'end' | 'stretch'` (optional)
  - [ ] `gridJustification?: 'start' | 'center' | 'end' | 'stretch' | 'space-between' | 'space-around' | 'space-evenly'` (optional)

### AC2: ComponentProps Extension

- [ ] In same file, search for `interface ComponentProps`
- [ ] Verify: Property `gridLayout?: GridLayoutConfig` exists
- [ ] Verify: Property is optional (has `?`)
- [ ] Verify: JSDoc comment references "alternative to objectLayout"

### AC3: GlobalStyles Extension

- [ ] In same file, search for `interface GlobalStyles`
- [ ] Verify: Property `defaultGridLayout?: Partial<GridLayoutConfig>` exists
- [ ] Verify: Property is optional and uses `Partial<>` type
- [ ] Search for `DEFAULT_GLOBAL_STYLES`
- [ ] Verify: Contains `defaultGridLayout: undefined`

### AC4: CSS Generation Utility

- [ ] Open `frontend/src/features/builder/utils/gridLayoutUtils.ts`
- [ ] Verify: File exists and is not empty
- [ ] Search for `function generateGridStyles`
- [ ] Verify function signature: `(config: GridLayoutConfig): CSSProperties`
- [ ] Verify function returns object with:
  - [ ] `display: 'grid'`
  - [ ] `gridTemplateRows` (built from rows + gaps)
  - [ ] `gridTemplateColumns` (built from columns + gaps)
  - [ ] `justifyContent` (from config.gridJustification)
  - [ ] `alignItems` (from config.cellAlignment)

### AC5: Cell Coordinate Helpers

- [ ] In `gridLayoutUtils.ts`, verify these functions exist:

**cellKey function:**
- [ ] Search for `function cellKey`
- [ ] Verify signature: `(row: number, col: number): string`
- [ ] Verify implementation returns `${row}-${col}` format

**parseCell function:**
- [ ] Search for `function parseCell`
- [ ] Verify signature: `(key: string): { row: number; col: number }`
- [ ] Verify implementation splits on `-` and parses integers

**getObjectGridArea function:**
- [ ] Search for `function getObjectGridArea`
- [ ] Verify signature includes `(objectId: string, config: GridLayoutConfig)`
- [ ] Verify return type: `{ gridRow: string; gridColumn: string } | null`

**Additional helpers (bonus verification):**
- [ ] `createDefaultGridLayout()` exists → returns default config
- [ ] `validateGridLayout(config)` exists → returns `{ isValid, errors }`
- [ ] `getCellOccupant(row, col, config)` exists → returns objectId or null
- [ ] `getAssignedObjects(config)` exists → returns array of assignments

## Regression Check

- [ ] No new TypeScript errors introduced (check VSCode Problems panel)
- [ ] No linter errors in changed files
- [ ] Existing `builder.types.ts` exports still work (no breaking changes)

## Post-conditions

- [ ] `GridLayoutConfig` interface is ready for use by T02-T08
- [ ] All utility functions are exported and importable
- [ ] Types match specification in `docs/GRID-LAYOUT-GUIDE.md`

## Edge Cases (optional)

- [ ] Verify `parseCell("0-0")` returns `{ row: 0, col: 0 }` (handles zero indices)
- [ ] Verify `validateGridLayout` catches rows < 1 or > 12
- [ ] Verify `validateGridLayout` catches non-rectangular merged cells

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
