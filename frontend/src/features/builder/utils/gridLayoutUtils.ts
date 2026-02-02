/**
 * Grid Layout Utilities
 * 
 * Utility functions for the Grid Layout system.
 * Provides CSS generation, cell coordinate handling, and validation.
 * 
 * See docs/GRID-LAYOUT-GUIDE.md for full specification.
 * 
 * @module gridLayoutUtils
 * @story 3.10 - Grid Layout System
 * @task T01 - Types & Utilities Foundation
 */

import type { ComponentStructure, ComponentType, GlobalStyles, GridLayoutConfig, ObjectLayoutType } from '../types/builder.types';
import type { CSSProperties } from 'react';

// ═══════════════════════════════════════════════════════════════════════════
// CELL COORDINATE HELPERS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a cell key from row and column indices.
 * Format: "row-col" (e.g., "0-0", "1-2")
 * 
 * @param row - Row index (0-based)
 * @param col - Column index (0-based)
 * @returns Cell key string
 * 
 * @example
 * cellKey(0, 0) // "0-0"
 * cellKey(1, 2) // "1-2"
 */
export function cellKey(row: number, col: number): string {
    return `${row}-${col}`;
}

/**
 * Parse a cell key into row and column indices.
 * 
 * @param key - Cell key string (e.g., "0-0", "1-2")
 * @returns Object with row and col properties
 * 
 * @example
 * parseCell("0-0") // { row: 0, col: 0 }
 * parseCell("1-2") // { row: 1, col: 2 }
 */
export function parseCell(key: string): { row: number; col: number } {
    const parts = key.split('-');
    const row = parseInt(parts[0], 10);
    const col = parseInt(parts[1], 10);
    return { row, col };
}

// ═══════════════════════════════════════════════════════════════════════════
// CSS GRID GENERATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Generate CSS Grid styles from a GridLayoutConfig.
 * 
 * Converts the grid configuration into React CSSProperties that can be
 * applied to a container element to create the CSS Grid layout.
 * 
 * Uses gap tracks in gridTemplateRows/gridTemplateColumns to support
 * individual row/column spacing overrides.
 * 
 * @param config - Grid layout configuration
 * @returns CSS properties object for the grid container
 * 
 * @example
 * const styles = generateGridStyles({
 *   rows: 3,
 *   columns: 2,
 *   columnGap: 8,
 *   rowGap: 8,
 *   cellAssignments: { "0-0": "label", "1-0": "input" }
 * });
 * // Returns: { display: 'grid', gridTemplateRows: '1fr 8px 1fr 8px 1fr', ... }
 */
export function generateGridStyles(config: GridLayoutConfig): CSSProperties {
    const rowTrack = config.rowSizing === 'auto' ? 'auto' : '1fr';
    const columnTrack = config.columnSizing === 'auto' ? 'auto' : '1fr';
    const cellAlignment = config.cellAlignment || 'stretch';
    const effectiveAlignment =
        cellAlignment === 'stretch' && (config.rowSizing === 'auto' || config.columnSizing === 'auto')
            ? 'start'
            : cellAlignment;

    // Build gridTemplateRows with individual row gaps
    const rowTemplate: string[] = [];
    for (let i = 0; i < config.rows; i++) {
        rowTemplate.push(rowTrack);
        // Add gap after row (except last row)
        if (i < config.rows - 1) {
            const gap = config.rowGaps?.[i] ?? config.rowGap;
            rowTemplate.push(`${gap}px`);
        }
    }

    // Build gridTemplateColumns with individual column gaps
    const colTemplate: string[] = [];
    for (let i = 0; i < config.columns; i++) {
        colTemplate.push(columnTrack);
        // Add gap after column (except last column)
        if (i < config.columns - 1) {
            const gap = config.columnGaps?.[i] ?? config.columnGap;
            colTemplate.push(`${gap}px`);
        }
    }

    const display = columnTrack === 'auto' ? 'inline-grid' : 'grid';

    return {
        display,
        gridTemplateRows: rowTemplate.join(' '),
        gridTemplateColumns: colTemplate.join(' '),
        justifyContent: config.gridJustification || 'start',
        alignItems: effectiveAlignment,
        justifyItems: effectiveAlignment,
    };
}

// ═══════════════════════════════════════════════════════════════════════════
// OBJECT POSITIONING
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Get the position of an object in the grid.
 * 
 * @param objectId - The object ID to find
 * @param config - Grid layout configuration
 * @returns Position { row, col } or null if not found
 */
export function getObjectPosition(
    objectId: string,
    config: GridLayoutConfig
): { row: number; col: number } | null {
    for (const [key, assignedObjectId] of Object.entries(config.cellAssignments)) {
        if (assignedObjectId === objectId) {
            return parseCell(key);
        }
    }
    return null;
}

/**
 * Get CSS grid-area for an object based on its position and span configuration.
 * 
 * Handles both simple cell assignments and merged cell groups.
 * Returns gridRow and gridColumn values for CSS positioning.
 * 
 * Note: Grid lines are 1-indexed in CSS Grid, so we add 1 to row/col.
 * When using gap tracks, we need to account for the gap rows/columns:
 * - Actual row index in CSS = (row * 2) + 1
 * - Actual col index in CSS = (col * 2) + 1
 * 
 * @param objectId - The object ID to get grid area for
 * @param config - Grid layout configuration
 * @returns Object with gridRow and gridColumn CSS values, or null if not found
 * 
 * @example
 * const area = getObjectGridArea("label", config);
 * // Returns: { gridRow: "1 / 2", gridColumn: "1 / 2" }
 */
export function getObjectGridArea(
    objectId: string,
    config: GridLayoutConfig
): { gridRow: string; gridColumn: string } | null {
    // First check if object is in a merged cell group
    const mergedGroup = Object.values(config.mergedCells || {}).find(
        (group) => group.objectId === objectId
    );

    if (mergedGroup && mergedGroup.cells.length > 0) {
        // Calculate span from merged cells
        const cellPositions = mergedGroup.cells.map((key) => parseCell(key));

        const minRow = Math.min(...cellPositions.map((p) => p.row));
        const maxRow = Math.max(...cellPositions.map((p) => p.row));
        const minCol = Math.min(...cellPositions.map((p) => p.col));
        const maxCol = Math.max(...cellPositions.map((p) => p.col));

        // Convert to CSS grid lines (1-indexed, accounting for gap tracks)
        // Each content row/col takes 2 grid lines (content + gap), except last
        const startRow = minRow * 2 + 1;
        const endRow = maxRow * 2 + 2; // +2 to span the content row
        const startCol = minCol * 2 + 1;
        const endCol = maxCol * 2 + 2;

        return {
            gridRow: `${startRow} / ${endRow}`,
            gridColumn: `${startCol} / ${endCol}`,
        };
    }

    // Find object in cell assignments
    const position = getObjectPosition(objectId, config);
    if (!position) {
        return null;
    }

    // Get span configuration
    const span = config.objectSpans?.[objectId];
    const rowSpan = span?.rowSpan || 1;
    const colSpan = span?.colSpan || 1;

    // Convert to CSS grid lines (accounting for gap tracks)
    const startRow = position.row * 2 + 1;
    const endRow = (position.row + rowSpan - 1) * 2 + 2;
    const startCol = position.col * 2 + 1;
    const endCol = (position.col + colSpan - 1) * 2 + 2;

    return {
        gridRow: `${startRow} / ${endRow}`,
        gridColumn: `${startCol} / ${endCol}`,
    };
}

// ═══════════════════════════════════════════════════════════════════════════
// DEFAULT CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a default GridLayoutConfig.
 * 
 * Provides sensible defaults for a new grid layout:
 * - 3 rows, 1 column (vertical stack)
 * - 8px gaps
 * - Empty cell assignments
 * 
 * @returns Default grid layout configuration
 */
export function createDefaultGridLayout(): GridLayoutConfig {
    return {
        rows: 3,
        columns: 1,
        columnGap: 8,
        rowGap: 8,
        cellAssignments: {},
        rowSizing: 'auto',
        columnSizing: 'auto',
    };
}

/**
 * Create a GridLayoutConfig from an Object Layout configuration.
 * 
 * Conversion rules:
 * - Vertical: 3 rows × 1 column, assign label/input/validation in order
 * - Horizontal: 1 row × 3 columns, assign label/input/validation in order
 * - Mixed: rows = number of layoutGroups rows, columns = max objects in any row,
 *          assign objects based on layoutGroups ordering
 */
export function createGridLayoutFromObjectLayout(
    layout: ObjectLayoutType,
    objectIds: string[],
    layoutGroups?: Record<string, string[]>,
    baseConfig?: Partial<GridLayoutConfig>
): GridLayoutConfig {
    const base = {
        ...createDefaultGridLayout(),
        ...baseConfig,
    };

    let rows = 3;
    let columns = 1;
    const cellAssignments: Record<string, string> = {};

    const standardOrder = ['label', 'input', 'validation'];
    const orderedStandard = standardOrder.filter((id) => objectIds.includes(id));
    const remainingIds = objectIds.filter((id) => !standardOrder.includes(id));
    const orderedIds = [...orderedStandard, ...remainingIds];

    if (layout === 'horizontal') {
        rows = 1;
        columns = 3;
        orderedIds.slice(0, 3).forEach((objectId, colIndex) => {
            cellAssignments[cellKey(0, colIndex)] = objectId;
        });
    } else if (layout === 'mixed') {
        const rowKeys = Object.keys(layoutGroups || {});
        const orderedRowKeys = rowKeys
            .map((key) => ({
                key,
                order: Number.parseInt(key.replace(/\D/g, ''), 10),
            }))
            .sort((a, b) => (Number.isNaN(a.order) || Number.isNaN(b.order) ? a.key.localeCompare(b.key) : a.order - b.order))
            .map(({ key }) => key);

        rows = orderedRowKeys.length > 0 ? orderedRowKeys.length : 3;
        columns = orderedRowKeys.reduce((maxCols, key) => {
            const count = layoutGroups?.[key]?.length ?? 0;
            return Math.max(maxCols, count);
        }, 1);

        const allowedIds = new Set(objectIds);
        orderedRowKeys.forEach((rowKey, rowIndex) => {
            const rowObjects = (layoutGroups?.[rowKey] || []).filter((id) => allowedIds.has(id));
            rowObjects.forEach((objectId, colIndex) => {
                cellAssignments[cellKey(rowIndex, colIndex)] = objectId;
            });
        });
    } else {
        rows = 3;
        columns = 1;
        orderedIds.slice(0, 3).forEach((objectId, rowIndex) => {
            cellAssignments[cellKey(rowIndex, 0)] = objectId;
        });
    }

    return {
        rows,
        columns,
        columnGap: base.columnGap ?? 8,
        rowGap: base.rowGap ?? 8,
        columnGaps: base.columnGaps,
        rowGaps: base.rowGaps,
        cellAssignments,
        cellAlignment: base.cellAlignment,
        gridJustification: base.gridJustification,
        rowSizing: base.rowSizing ?? 'auto',
        columnSizing: base.columnSizing ?? 'fr',
    };
}

/**
 * Build per-component default grid layouts from component structures.
 * Uses layoutGroups when present (treated as mixed layout).
 */
export function extractGridStructureDefaults(config: GridLayoutConfig): Partial<GridLayoutConfig> {
    return {
        rows: config.rows,
        columns: config.columns,
        cellAssignments: config.cellAssignments,
        mergedCells: config.mergedCells,
        objectSpans: config.objectSpans,
    };
}

export function buildDefaultGridLayoutsByComponent(
    components: Array<{ type: ComponentType; structure: ComponentStructure }>,
    layoutMode: ObjectLayoutType = 'mixed'
): Record<ComponentType, Partial<GridLayoutConfig>> {
    return components.reduce<Record<ComponentType, Partial<GridLayoutConfig>>>((acc, component) => {
        const objectIds = component.structure.objects.map((obj) => obj.id);
        const resolvedLayout: ObjectLayoutType =
            layoutMode === 'mixed'
                ? (component.structure.layoutGroups ? 'mixed' : component.structure.defaultLayout)
                : layoutMode;

        const resolved = createGridLayoutFromObjectLayout(
            resolvedLayout,
            objectIds,
            component.structure.layoutGroups
        );

        acc[component.type] = extractGridStructureDefaults(resolved);

        return acc;
    }, {} as Record<ComponentType, Partial<GridLayoutConfig>>);
}

export function resolveComponentDefaultGridLayout(args: {
    structure: ComponentStructure;
    componentType?: ComponentType;
    globalStyles?: GlobalStyles;
}): Partial<GridLayoutConfig> | undefined {
    const { structure, componentType, globalStyles } = args;
    if (!globalStyles) return undefined;

    const objectIds = structure.objects.map((obj) => obj.id);
    const defaultLayoutType = globalStyles.defaultObjectLayout ?? structure.defaultLayout;
    const verticalOverrides: Record<ComponentType, Partial<GridLayoutConfig>> = {
        terms: {
            rows: 3,
            columns: 1,
            cellAssignments: {
                '1-0': 'label',
                '0-0': 'input',
                '2-0': 'validation',
            },
        },
        'submit-button': {
            rows: 3,
            columns: 1,
            cellAssignments: {
                '1-0': 'loading',
                '0-0': 'button',
                '2-0': 'validation',
            },
        },
    };
    const horizontalOverrides: Record<ComponentType, Partial<GridLayoutConfig>> = {
        terms: {
            rows: 1,
            columns: 3,
            cellAssignments: {
                '0-1': 'label',
                '0-0': 'input',
                '0-2': 'validation',
            },
        },
        'submit-button': {
            rows: 1,
            columns: 3,
            cellAssignments: {
                '0-1': 'loading',
                '0-0': 'button',
                '0-2': 'validation',
            },
        },
    };

    if (defaultLayoutType === 'mixed') {
        const fromMap = componentType ? globalStyles.defaultGridLayoutsByComponent?.[componentType] : undefined;
        if (fromMap) return fromMap;

        const mixed = createGridLayoutFromObjectLayout('mixed', objectIds, structure.layoutGroups);
        return extractGridStructureDefaults(mixed);
    }

    if (defaultLayoutType === 'vertical' && componentType && verticalOverrides[componentType]) {
        return verticalOverrides[componentType];
    }

    if (defaultLayoutType === 'horizontal' && componentType && horizontalOverrides[componentType]) {
        return horizontalOverrides[componentType];
    }

    const resolved = createGridLayoutFromObjectLayout(defaultLayoutType, objectIds);
    return extractGridStructureDefaults(resolved);
}

// ═══════════════════════════════════════════════════════════════════════════
// VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Validation result for grid layout configuration.
 */
export interface GridValidationResult {
    isValid: boolean;
    errors: string[];
}

/**
 * Validate a GridLayoutConfig for correctness.
 * 
 * Checks:
 * - Rows/columns are within valid range (1-12)
 * - Gaps are within valid range (0-48px)
 * - Cell assignments reference valid cells
 * - Merged cells form valid rectangles
 * - Object spans don't exceed grid bounds
 * 
 * @param config - Grid layout configuration to validate
 * @returns Validation result with errors array
 * 
 * @example
 * const result = validateGridLayout(config);
 * if (!result.isValid) {
 *   console.error(result.errors);
 * }
 */
export function validateGridLayout(config: GridLayoutConfig): GridValidationResult {
    const errors: string[] = [];

    // Validate rows (1-12)
    if (config.rows < 1 || config.rows > 12) {
        errors.push('Rows must be between 1 and 12');
    }

    // Validate columns (1-12)
    if (config.columns < 1 || config.columns > 12) {
        errors.push('Columns must be between 1 and 12');
    }

    // Validate column gap (0-48px)
    if (config.columnGap < 0 || config.columnGap > 48) {
        errors.push('Column gap must be between 0 and 48px');
    }

    // Validate row gap (0-48px)
    if (config.rowGap < 0 || config.rowGap > 48) {
        errors.push('Row gap must be between 0 and 48px');
    }

    // Validate individual column gaps
    if (config.columnGaps) {
        for (const [colIndexStr, gap] of Object.entries(config.columnGaps)) {
            const colIndex = Number(colIndexStr);
            // Column gap applies between columns, so valid for 0 to columns-2
            if (colIndex < 0 || colIndex >= config.columns - 1) {
                errors.push(
                    `Column gap override for column ${colIndex} is invalid (must be 0 to ${config.columns - 2})`
                );
            }
            if (gap < 0 || gap > 48) {
                errors.push(`Column gap for column ${colIndex} must be between 0 and 48px`);
            }
        }
    }

    // Validate individual row gaps
    if (config.rowGaps) {
        for (const [rowIndexStr, gap] of Object.entries(config.rowGaps)) {
            const rowIndex = Number(rowIndexStr);
            // Row gap applies between rows, so valid for 0 to rows-2
            if (rowIndex < 0 || rowIndex >= config.rows - 1) {
                errors.push(
                    `Row gap override for row ${rowIndex} is invalid (must be 0 to ${config.rows - 2})`
                );
            }
            if (gap < 0 || gap > 48) {
                errors.push(`Row gap for row ${rowIndex} must be between 0 and 48px`);
            }
        }
    }

    // Validate cell assignments
    for (const [key] of Object.entries(config.cellAssignments)) {
        const { row, col } = parseCell(key);

        if (row < 0 || row >= config.rows) {
            errors.push(`Cell assignment "${key}" has invalid row (must be 0 to ${config.rows - 1})`);
        }

        if (col < 0 || col >= config.columns) {
            errors.push(`Cell assignment "${key}" has invalid column (must be 0 to ${config.columns - 1})`);
        }
    }

    // Validate merged cells
    if (config.mergedCells) {
        for (const [mergeId, mergeGroup] of Object.entries(config.mergedCells)) {
            if (mergeGroup.cells.length < 2) {
                errors.push(`Merged cell group "${mergeId}" must contain at least 2 cells`);
                continue;
            }

            // Validate all cells in merge are valid
            const positions: Array<{ row: number; col: number }> = [];
            for (const key of mergeGroup.cells) {
                const { row, col } = parseCell(key);
                if (row < 0 || row >= config.rows) {
                    errors.push(`Merged cell "${key}" in group "${mergeId}" has invalid row`);
                }
                if (col < 0 || col >= config.columns) {
                    errors.push(`Merged cell "${key}" in group "${mergeId}" has invalid column`);
                }
                positions.push({ row, col });
            }

            // Validate cells form a rectangle
            if (positions.length >= 2) {
                const rows = [...new Set(positions.map((p) => p.row))].sort((a, b) => a - b);
                const cols = [...new Set(positions.map((p) => p.col))].sort((a, b) => a - b);
                const expectedCells = rows.length * cols.length;

                if (mergeGroup.cells.length !== expectedCells) {
                    errors.push(`Merged cell group "${mergeId}" cells must form a rectangle`);
                }
            }
        }
    }

    // Validate object spans
    if (config.objectSpans) {
        for (const [objectId, span] of Object.entries(config.objectSpans)) {
            const position = getObjectPosition(objectId, config);
            if (!position) {
                errors.push(`Object "${objectId}" has span but no cell assignment`);
                continue;
            }

            if (span.rowSpan && span.rowSpan < 1) {
                errors.push(`Object "${objectId}" rowSpan must be at least 1`);
            }

            if (span.colSpan && span.colSpan < 1) {
                errors.push(`Object "${objectId}" colSpan must be at least 1`);
            }

            if (span.rowSpan && position.row + span.rowSpan > config.rows) {
                errors.push(`Object "${objectId}" rowSpan exceeds grid rows`);
            }

            if (span.colSpan && position.col + span.colSpan > config.columns) {
                errors.push(`Object "${objectId}" colSpan exceeds grid columns`);
            }
        }
    }

    return {
        isValid: errors.length === 0,
        errors,
    };
}

// ═══════════════════════════════════════════════════════════════════════════
// CELL OCCUPANCY HELPERS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Check if a cell is occupied by any object (including spans and merges).
 * 
 * @param row - Row index
 * @param col - Column index
 * @param config - Grid layout configuration
 * @returns The objectId occupying the cell, or null if empty
 */
export function getCellOccupant(
    row: number,
    col: number,
    config: GridLayoutConfig
): string | null {
    const key = cellKey(row, col);

    // Check direct assignment
    if (config.cellAssignments[key]) {
        return config.cellAssignments[key];
    }

    // Check merged cells
    if (config.mergedCells) {
        for (const mergeGroup of Object.values(config.mergedCells)) {
            if (mergeGroup.cells.includes(key)) {
                return mergeGroup.objectId;
            }
        }
    }

    // Check object spans
    if (config.objectSpans) {
        for (const [objectId, span] of Object.entries(config.objectSpans)) {
            const position = getObjectPosition(objectId, config);
            if (!position) continue;

            const rowSpan = span.rowSpan || 1;
            const colSpan = span.colSpan || 1;

            if (
                row >= position.row &&
                row < position.row + rowSpan &&
                col >= position.col &&
                col < position.col + colSpan
            ) {
                return objectId;
            }
        }
    }

    return null;
}

/**
 * Get all objects assigned to the grid with their positions.
 * 
 * @param config - Grid layout configuration
 * @returns Array of { objectId, row, col } for each assigned object
 */
export function getAssignedObjects(
    config: GridLayoutConfig
): Array<{ objectId: string; row: number; col: number }> {
    const result: Array<{ objectId: string; row: number; col: number }> = [];

    for (const [key, objectId] of Object.entries(config.cellAssignments)) {
        const { row, col } = parseCell(key);
        result.push({ objectId, row, col });
    }

    return result;
}

// ═══════════════════════════════════════════════════════════════════════════
// CELL MERGING UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Check if a set of cells forms a valid rectangular selection for merging.
 * 
 * Validates that:
 * - At least 2 cells are selected
 * - Cells form a complete rectangle (no L-shapes or gaps)
 * - Rows and columns are contiguous
 * 
 * @param cellKeys - Array of cell keys (e.g., ["0-0", "0-1", "1-0", "1-1"])
 * @returns True if cells form a valid rectangle, false otherwise
 * 
 * @example
 * isValidMergeSelection(["0-0", "0-1"]) // true - 1×2 rectangle
 * isValidMergeSelection(["0-0", "0-1", "1-0", "1-1"]) // true - 2×2 rectangle
 * isValidMergeSelection(["0-0", "0-1", "1-0"]) // false - L-shape
 */
export function isValidMergeSelection(cellKeys: string[]): boolean {
    if (cellKeys.length < 2) return false;
    
    const positions = cellKeys.map(key => parseCell(key));
    const rows = [...new Set(positions.map(p => p.row))].sort((a, b) => a - b);
    const cols = [...new Set(positions.map(p => p.col))].sort((a, b) => a - b);
    
    // Check if cells form a complete rectangle
    const expectedCount = rows.length * cols.length;
    if (cellKeys.length !== expectedCount) return false;
    
    // Check that rows are contiguous
    for (let i = 1; i < rows.length; i++) {
        if (rows[i] !== rows[i - 1] + 1) return false;
    }
    
    // Check that columns are contiguous
    for (let i = 1; i < cols.length; i++) {
        if (cols[i] !== cols[i - 1] + 1) return false;
    }
    
    return true;
}

/**
 * Merge cells into a single group.
 * 
 * Creates a merged cell group in the config. If cells already contain objects,
 * only one object can remain (assigned to the first cell).
 * 
 * @param cellKeys - Array of cell keys to merge (must form a rectangle)
 * @param config - Grid layout configuration
 * @returns New grid layout configuration with merged cells
 * @throws Error if cells don't form a valid rectangle
 * 
 * @example
 * const newConfig = mergeCells(["0-0", "0-1"], config);
 * // Creates merge group with both cells
 */
export function mergeCells(
    cellKeys: string[],
    config: GridLayoutConfig
): GridLayoutConfig {
    if (!isValidMergeSelection(cellKeys)) {
        throw new Error('Cells must form a rectangle to merge');
    }
    
    // Check if any cells are already in a merge group
    const existingMerges = config.mergedCells || {};
    for (const cellKey of cellKeys) {
        const existingMerge = getMergeGroupForCell(cellKey, config);
        if (existingMerge) {
            throw new Error(`Cell ${cellKey} is already part of a merged group`);
        }
    }
    
    // Check if multiple objects are in the selected cells
    const objectsInCells = new Set<string>();
    for (const cellKey of cellKeys) {
        const objectId = config.cellAssignments[cellKey];
        if (objectId) {
            objectsInCells.add(objectId);
        }
    }
    
    if (objectsInCells.size > 1) {
        throw new Error('Cannot merge cells with multiple different objects');
    }
    
    const mergeId = `merge-${Date.now()}`;
    const objectId = objectsInCells.size === 1 ? Array.from(objectsInCells)[0] : '';
    
    // Create merged cell group
    const mergedCells = {
        ...existingMerges,
        [mergeId]: {
            cells: [...cellKeys].sort(), // Sort for consistency
            objectId
        }
    };
    
    // Update cell assignments: keep only first cell assignment, remove others
    const cellAssignments = { ...config.cellAssignments };
    const firstCell = cellKeys[0];
    const firstCellObject = cellAssignments[firstCell];
    
    // Remove assignments from other cells in the merge
    for (let i = 1; i < cellKeys.length; i++) {
        delete cellAssignments[cellKeys[i]];
    }
    
    // If no object in first cell but there was one elsewhere, assign it
    if (!firstCellObject && objectId) {
        cellAssignments[firstCell] = objectId;
    }
    
    // Update objectSpans if there's an object
    let objectSpans = { ...(config.objectSpans || {}) };
    if (objectId) {
        const span = getMergeSpan(cellKeys);
        objectSpans[objectId] = span;
    }
    
    return {
        ...config,
        mergedCells,
        cellAssignments,
        objectSpans: Object.keys(objectSpans).length > 0 ? objectSpans : undefined
    };
}

/**
 * Unmerge a merged cell group.
 * 
 * Removes the merge group and restores cells to individual state.
 * If an object was in the merged cell, it remains in the first cell only.
 * 
 * @param mergeId - ID of the merge group to unmerge
 * @param config - Grid layout configuration
 * @returns New grid layout configuration with merge removed
 * 
 * @example
 * const newConfig = unmergeCells("merge-1234567890", config);
 * // Removes merge group and restores individual cells
 */
export function unmergeCells(
    mergeId: string,
    config: GridLayoutConfig
): GridLayoutConfig {
    const mergedCells = { ...(config.mergedCells || {}) };
    const mergeGroup = mergedCells[mergeId];
    
    if (!mergeGroup) {
        // Merge group doesn't exist, return config as-is
        return config;
    }
    
    // Remove span for object if one was assigned
    let objectSpans = { ...(config.objectSpans || {}) };
    if (mergeGroup.objectId) {
        delete objectSpans[mergeGroup.objectId];
    }
    
    // Remove the merge group
    delete mergedCells[mergeId];
    
    return {
        ...config,
        mergedCells: Object.keys(mergedCells).length > 0 ? mergedCells : undefined,
        objectSpans: Object.keys(objectSpans).length > 0 ? objectSpans : undefined
    };
}

/**
 * Get the merge group that contains a specific cell.
 * 
 * @param cellKey - Cell key to search for (e.g., "0-0")
 * @param config - Grid layout configuration
 * @returns Merge group info { mergeId, group } or null if cell is not merged
 * 
 * @example
 * const merge = getMergeGroupForCell("0-0", config);
 * // Returns: { mergeId: "merge-123", group: { cells: ["0-0", "0-1"], objectId: "label" } }
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
 * 
 * @param cells - Array of cell keys in the merge group
 * @returns Object with rowSpan and colSpan values
 * 
 * @example
 * getMergeSpan(["0-0", "0-1"]) // { rowSpan: 1, colSpan: 2 }
 * getMergeSpan(["0-0", "0-1", "1-0", "1-1"]) // { rowSpan: 2, colSpan: 2 }
 */
export function getMergeSpan(cells: string[]): { rowSpan: number; colSpan: number } {
    const positions = cells.map(key => parseCell(key));
    const rows = [...new Set(positions.map(p => p.row))];
    const cols = [...new Set(positions.map(p => p.col))];
    return { rowSpan: rows.length, colSpan: cols.length };
}

// ═══════════════════════════════════════════════════════════════════════════
// GLOBAL DEFAULTS & RESOLUTION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Get effective grid layout configuration for a component.
 * Merges global defaults with component overrides.
 * 
 * Resolution order:
 * 1. Component override (highest priority)
 * 2. Per-component global default
 * 3. Global defaults
 * 4. System defaults (fallback)
 * 
 * @param componentGridLayout - Component's gridLayout override (may be undefined)
 * @param componentDefaultGridLayout - Per-component default grid layout (may be undefined)
 * @param globalDefaultGridLayout - Global default grid layout (may be undefined)
 * @returns Effective GridLayoutConfig or null if grid layout not enabled
 * 
 * @example
 * // Component with override
 * const effective = getEffectiveGridLayout(
 *   { rows: 5, columns: 2, columnGap: 16, rowGap: 8, cellAssignments: {} },
 *   { rows: 3, columns: 1, columnGap: 8, rowGap: 8 },
 *   { rows: 4, columns: 2, columnGap: 12, rowGap: 10 }
 * );
 * // Returns: { rows: 5, columns: 2, columnGap: 16, rowGap: 8, ... }
 * 
 * // Component using global defaults
 * const effective = getEffectiveGridLayout(
 *   undefined,
 *   { rows: 4, columns: 2, columnGap: 12, rowGap: 10 },
 *   { rows: 3, columns: 1, columnGap: 8, rowGap: 8 }
 * );
 * // Returns: { rows: 4, columns: 2, columnGap: 12, rowGap: 10, ... }
 */
export function getEffectiveGridLayout(
    componentGridLayout: GridLayoutConfig | null | undefined,
    componentDefaultGridLayout: Partial<GridLayoutConfig> | undefined,
    globalDefaultGridLayout: Partial<GridLayoutConfig> | undefined
): GridLayoutConfig | null {
    const global = globalDefaultGridLayout;
    const componentDefault = componentDefaultGridLayout;
    const componentOverride = componentGridLayout;

    // If component explicitly opts out (null), return null to indicate no grid layout
    if (componentOverride === null) {
        return null;
    }

    // If component has gridLayout override, merge with global fallbacks
    if (componentOverride) {
        return {
            rows: componentOverride.rows ?? componentDefault?.rows ?? global?.rows ?? 3,
            columns: componentOverride.columns ?? componentDefault?.columns ?? global?.columns ?? 1,
            columnGap: componentOverride.columnGap ?? componentDefault?.columnGap ?? global?.columnGap ?? 8,
            rowGap: componentOverride.rowGap ?? componentDefault?.rowGap ?? global?.rowGap ?? 8,
            columnGaps: componentOverride.columnGaps ?? componentDefault?.columnGaps ?? global?.columnGaps,
            rowGaps: componentOverride.rowGaps ?? componentDefault?.rowGaps ?? global?.rowGaps,
            cellAssignments:
                componentOverride.cellAssignments ??
                componentDefault?.cellAssignments ??
                global?.cellAssignments ??
                {},
            mergedCells: componentOverride.mergedCells,
            objectSpans: componentOverride.objectSpans,
            cellAlignment:
                componentOverride.cellAlignment ??
                componentDefault?.cellAlignment ??
                global?.cellAlignment ??
                'stretch',
            gridJustification:
                componentOverride.gridJustification ??
                componentDefault?.gridJustification ??
                global?.gridJustification ??
                'start',
            rowSizing: componentOverride.rowSizing ?? componentDefault?.rowSizing ?? global?.rowSizing ?? 'auto',
            columnSizing: componentOverride.columnSizing ?? componentDefault?.columnSizing ?? global?.columnSizing ?? 'auto',
        };
    }

    if (componentDefault) {
        return {
            rows: componentDefault.rows ?? global?.rows ?? 3,
            columns: componentDefault.columns ?? global?.columns ?? 1,
            columnGap: componentDefault.columnGap ?? global?.columnGap ?? 8,
            rowGap: componentDefault.rowGap ?? global?.rowGap ?? 8,
            columnGaps: componentDefault.columnGaps ?? global?.columnGaps,
            rowGaps: componentDefault.rowGaps ?? global?.rowGaps,
            cellAssignments: componentDefault.cellAssignments ?? global?.cellAssignments ?? {},
            mergedCells: componentDefault.mergedCells,
            objectSpans: componentDefault.objectSpans,
            cellAlignment: componentDefault.cellAlignment ?? global?.cellAlignment ?? 'stretch',
            gridJustification: componentDefault.gridJustification ?? global?.gridJustification ?? 'start',
            rowSizing: componentDefault.rowSizing ?? global?.rowSizing ?? 'auto',
            columnSizing: componentDefault.columnSizing ?? global?.columnSizing ?? 'auto',
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
            rowSizing: global.rowSizing ?? 'auto',
            columnSizing: global.columnSizing ?? 'auto',
        };
    }

    // No grid layout configured
    return null;
}

/**
 * Check if component has grid layout override (vs using global default)
 * 
 * @param componentGridLayout - Component's gridLayout prop (may be undefined)
 * @returns True if component has override, false if using global default
 * 
 * @example
 * hasGridLayoutOverride(undefined) // false - using global default
 * hasGridLayoutOverride({ rows: 3, columns: 1, ... }) // true - has override
 */
export function hasGridLayoutOverride(componentGridLayout: GridLayoutConfig | undefined): boolean {
    return componentGridLayout !== undefined;
}
