/**
 * GridLayoutSection Component
 * 
 * Properties Panel section for configuring Grid Layout.
 * Provides:
 * - Toggle between Object Layout and Grid Layout
 * - Grid structure controls (rows, columns)
 * - Gap controls (row gap, column gap)
 * - Visual grid preview via GridLayoutEditor
 * - Drag-and-drop object assignment to grid cells
 * 
 * @story 3.10 - Grid Layout System
 * @task T03 - Basic Grid Editor UI
 * @task T04 - Object Drag-and-Drop
 */

import React, { useCallback, useMemo, useState } from 'react';
import { Grid3x3, LayoutGrid, Rows, Columns, Space, Package, GripVertical, X, ChevronRight } from 'lucide-react';
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
    DragEndEvent,
    DragStartEvent,
    DragOverlay,
    UniqueIdentifier,
} from '@dnd-kit/core';
import {
    SortableContext,
    sortableKeyboardCoordinates,
    useSortable,
    horizontalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { FormComponent, ComponentStructure, ComponentProps, GridLayoutConfig, ObjectLayoutType, GlobalStyles } from '../../types/builder.types';
import { 
    createDefaultGridLayout, 
    cellKey, 
    isValidMergeSelection, 
    mergeCells, 
    unmergeCells,
    getMergeGroupForCell,
    getMergeSpan,
    getEffectiveGridLayout,
    hasGridLayoutOverride,
    createGridLayoutFromObjectLayout,
    resolveComponentDefaultGridLayout
} from '../../utils/gridLayoutUtils';
import { computeFieldStyles } from '../../utils/styleUtils';
import { GridLayoutEditor } from '../ui/GridLayoutEditor';
import { devLogger } from '../../utils/devLogger';

interface GridLayoutSectionProps {
    component: FormComponent;
    structure: ComponentStructure;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
    globalStyles?: GlobalStyles;
}

// ═══════════════════════════════════════════════════════════════════════════
// DRAGGABLE GRID OBJECT COMPONENT
// ═══════════════════════════════════════════════════════════════════════════

interface DraggableGridObjectProps {
    id: string;
    label: string;
    isInPool?: boolean;
    onRemove?: () => void;
}

/**
 * Draggable object item used in Available Objects pool and grid cells.
 */
const DraggableGridObject: React.FC<DraggableGridObjectProps> = ({ 
    id, 
    label, 
    isInPool,
    onRemove 
}) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id });

    const style: React.CSSProperties = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1,
        cursor: 'grab',
    };

    return (
        <div
            ref={setNodeRef}
            style={style}
            className={`flex items-center gap-1 px-2 py-1.5 rounded border transition-colors select-none ${
                isInPool 
                    ? 'bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-600 hover:border-indigo-400' 
                    : 'bg-white dark:bg-gray-700 border-indigo-300 dark:border-indigo-600 hover:border-indigo-400 dark:hover:border-indigo-500'
            }`}
        >
            <div {...attributes} {...listeners} className="flex items-center gap-1 flex-1">
                <GripVertical size={12} className="text-gray-400" />
                <span className="text-[10px] font-medium truncate">{label}</span>
            </div>
            {onRemove && (
                <button
                    type="button"
                    onClick={(e) => {
                        e.stopPropagation();
                        onRemove();
                    }}
                    className="p-0.5 rounded hover:bg-red-100 dark:hover:bg-red-900/30 text-gray-400 hover:text-red-500 transition-colors"
                    title="Remove from cell"
                >
                    <X size={10} />
                </button>
            )}
        </div>
    );
};

/**
 * Drag overlay item (shown while dragging)
 */
const DragOverlayItem: React.FC<{ label: string }> = ({ label }) => (
    <div className="flex items-center gap-1 px-2 py-1.5 rounded border border-indigo-500 bg-indigo-50 dark:bg-indigo-900/50 shadow-lg">
        <GripVertical size={12} className="text-indigo-400" />
        <span className="text-[10px] font-medium text-indigo-700 dark:text-indigo-300">{label}</span>
    </div>
);

// ═══════════════════════════════════════════════════════════════════════════
// INDIVIDUAL SPACING SECTION COMPONENT
// ═══════════════════════════════════════════════════════════════════════════

interface IndividualSpacingSectionProps {
    title: string;
    count: number;
    labelTemplate: (index: number) => string;
    gaps: Record<number, number>;
    defaultGap: number;
    onGapChange: (index: number, value: number) => void;
    onReset: (index: number) => void;
}

/**
 * Collapsible section for individual spacing controls (row or column gaps).
 * Shows sliders for each gap with reset buttons when values differ from default.
 */
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
                type="button"
                onClick={() => setIsExpanded(!isExpanded)}
                className="flex items-center gap-1 text-[10px] text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
            >
                <ChevronRight 
                    size={12} 
                    className={`transition-transform ${isExpanded ? 'rotate-90' : ''}`} 
                />
                {title}
            </button>
            
            {isExpanded && (
                <div className="mt-2 ml-4 space-y-2">
                    {Array.from({ length: count }, (_, i) => {
                        const currentGap = gaps[i] ?? defaultGap;
                        const isCustom = gaps[i] !== undefined;
                        
                        return (
                            <div key={i} className="flex items-center gap-2">
                                <span className="text-[9px] text-gray-400 dark:text-gray-500 w-24">
                                    {labelTemplate(i)}
                                </span>
                                <input
                                    type="range"
                                    min={0}
                                    max={48}
                                    step={1}
                                    value={currentGap}
                                    onChange={(e) => onGapChange(i, parseInt(e.target.value))}
                                    className="flex-1 h-1 accent-indigo-500"
                                />
                                <span className={`text-[9px] w-8 ${
                                    isCustom 
                                        ? 'text-indigo-600 dark:text-indigo-400 font-medium' 
                                        : 'text-gray-400 dark:text-gray-500'
                                }`}>
                                    {currentGap}px
                                </span>
                                {isCustom && (
                                    <button
                                        type="button"
                                        onClick={() => onReset(i)}
                                        className="text-[8px] text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors"
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

// ═══════════════════════════════════════════════════════════════════════════
// AVAILABLE OBJECTS POOL COMPONENT
// ═══════════════════════════════════════════════════════════════════════════

interface AvailableObjectsPoolProps {
    objectIds: string[];
    objectLabels: Record<string, string>;
}

/**
 * Available Objects Pool - shows unassigned objects that can be dragged to grid cells.
 * Also serves as a drop target to return objects from cells.
 */
const AvailableObjectsPool: React.FC<AvailableObjectsPoolProps> = ({
    objectIds,
    objectLabels,
}) => {
    const { setNodeRef, isOver } = useSortable({ 
        id: 'available-pool',
        disabled: true, // Pool itself is not draggable, just a drop target
    });

    return (
        <div
            ref={setNodeRef}
            className={`p-2 rounded border-2 min-h-[48px] transition-colors ${
                isOver 
                    ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' 
                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900'
            }`}
        >
            <div className="flex flex-wrap gap-1.5">
                {objectIds.length === 0 ? (
                    <div className="text-[10px] text-gray-400 dark:text-gray-500 italic py-1">
                        All objects assigned to grid cells
                    </div>
                ) : (
                    objectIds.map(objId => (
                        <DraggableGridObject
                            key={objId}
                            id={objId}
                            label={objectLabels[objId] || objId}
                            isInPool
                        />
                    ))
                )}
            </div>
        </div>
    );
};

/**
 * Layout mode type: 'object' for Object Layout, 'grid' for Grid Layout
 */
type LayoutMode = 'object' | 'grid';

/**
 * Determine current layout mode based on component props and global defaults
 */
function getLayoutMode(
    component: FormComponent,
    globalStyles?: {
        defaultGridLayout?: Partial<GridLayoutConfig>;
        defaultGridLayoutsByComponent?: Record<string, Partial<GridLayoutConfig>>;
    }
): LayoutMode {
    // If component explicitly sets gridLayout to null, use object layout (opt-out)
    if (component.props.gridLayout === null) {
        return 'object';
    }
    // If component has gridLayout override (not null, not undefined), it's in grid mode
    if (component.props.gridLayout !== undefined) {
        return 'grid';
    }
    // If global defaults exist, component can use grid mode (even without override)
    if (globalStyles?.defaultGridLayoutsByComponent?.[component.type] || globalStyles?.defaultGridLayout) {
        return 'grid';
    }
    // Otherwise, use object layout
    return 'object';
}

/**
 * GridLayoutSection - Properties Panel section for Grid Layout configuration
 */
export const GridLayoutSection: React.FC<GridLayoutSectionProps> = ({
    component,
    structure,
    onPropsChange,
    globalStyles,
}) => {
    // DnD state
    const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);
    
    // Cell selection state
    const [selectedCells, setSelectedCells] = useState<Set<string>>(new Set());
    
    // Current layout mode - memoized to ensure it updates when component.props.gridLayout changes
    const layoutMode = useMemo(() => {
        return getLayoutMode(component, globalStyles);
    }, [
        component.props.gridLayout,
        component.id,
        globalStyles?.defaultGridLayoutsByComponent,
        globalStyles?.defaultGridLayout,
    ]);
    const isGridMode = layoutMode === 'grid';
    
    // DnD sensors
    const sensors = useSensors(
        useSensor(PointerSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );
    
    // Get effective grid configuration using resolution system
    const currentGridConfig = useMemo((): GridLayoutConfig => {
        // If explicitly opted out (null), return default for display but component won't use grid
        if (component.props.gridLayout === null) {
            return createDefaultGridLayout();
        }
        const componentDefault = resolveComponentDefaultGridLayout({
            structure,
            componentType: component.type,
            globalStyles,
        });
        const effective = getEffectiveGridLayout(
            component.props.gridLayout,
            componentDefault,
            globalStyles?.defaultGridLayout
        );
        // If no grid layout configured at all, return default (for display purposes)
        return effective ?? createDefaultGridLayout();
    }, [component.props.gridLayout, component.type, globalStyles, structure]);
    
    // Check if component has override - memoized to ensure it updates when component changes
    const hasOverride = useMemo(() => {
        return hasGridLayoutOverride(component.props.gridLayout ?? undefined);
    }, [component.props.gridLayout]);
    
    // Get visible objects from structure (same logic as ObjectLayoutSection)
    const visibleObjects = useMemo(() => {
        return structure.objects.filter(obj => {
            if (obj.type === 'validation') return true;
            if (obj.required) return true;
            const cond = obj.conditional;
            if (!cond) return true;
            if (cond.type === 'prop' && cond.prop === 'allowOther') {
                return Boolean((component.props as Record<string, unknown>)?.allowOther);
            }
            return true;
        });
    }, [structure.objects, component.props]);
    
    // Get assigned object IDs from cellAssignments
    const assignedObjectIds = useMemo(() => {
        return new Set(Object.values(currentGridConfig.cellAssignments));
    }, [currentGridConfig.cellAssignments]);
    
    // Get available objects (not yet assigned to any cell)
    const availableObjects = useMemo(() => {
        return visibleObjects.filter(obj => !assignedObjectIds.has(obj.id));
    }, [visibleObjects, assignedObjectIds]);
    
    // Object labels map for display
    const objectLabels = useMemo(() => {
        const labels: Record<string, string> = {};
        visibleObjects.forEach(obj => {
            labels[obj.id] = obj.label || obj.id;
        });
        return labels;
    }, [visibleObjects]);
    
    // Handle layout mode toggle
    const handleLayoutModeChange = useCallback((mode: LayoutMode) => {
        const currentLayoutMode = getLayoutMode(component, globalStyles);
        devLogger.info('gridlayout.mode.changed', {
            componentId: component.id,
            from: currentLayoutMode,
            to: mode,
        });

        devLogger.info('panel.layout.changed', {
            componentId: component.id,
            property: 'layoutMode',
            from: currentLayoutMode,
            to: mode,
            componentType: component.type,
        });
        
        if (mode === 'grid') {
            const effectiveObjectLayout: ObjectLayoutType =
                component.props.objectLayout ||
                globalStyles?.defaultObjectLayout ||
                structure.defaultLayout ||
                'vertical';
            const effectiveLayoutGroups =
                component.props.layoutGroups ||
                globalStyles?.defaultLayoutGroups ||
                structure.layoutGroups ||
                {};

            const visibleObjectIds = visibleObjects.map((obj) => obj.id);
            const preferredObjectIds = ['label', 'input', 'validation'].filter((id) =>
                visibleObjectIds.includes(id)
            );
            const objectIdsForConversion =
                effectiveObjectLayout === 'mixed'
                    ? visibleObjectIds
                    : preferredObjectIds.length > 0
                        ? preferredObjectIds
                        : visibleObjectIds;

            const spacingOverrides = {
                labelGapOverride: component.props.labelGapOverride,
                inputHelpGapOverride: component.props.inputHelpGapOverride,
            };
            const computedFieldStyles = computeFieldStyles(
                globalStyles,
                component.props.styleOverrides,
                component.props.componentScale ?? 100,
                spacingOverrides
            );
            const labelGapPx = Number.parseFloat(String(computedFieldStyles.labelStyle.marginBottom ?? '0'));
            const inputHelpGapPx = Number.parseFloat(String(computedFieldStyles.helpTextStyle.marginTop ?? '0'));
            const defaultRowGap = globalStyles?.defaultGridLayout?.rowGap ?? 8;
            const defaultColumnGap = globalStyles?.defaultGridLayout?.columnGap ?? 8;
            const rowGap = component.props.objectSpacing?.verticalSpacing ?? defaultRowGap;
            const columnGap = component.props.objectSpacing?.horizontalGap ?? defaultColumnGap;

            const rowGaps =
                effectiveObjectLayout === 'vertical'
                    ? {
                        0: Number.isFinite(labelGapPx) ? labelGapPx : rowGap,
                        1: Number.isFinite(inputHelpGapPx) ? inputHelpGapPx : rowGap,
                    }
                    : undefined;

            const baseGridConfig: Partial<GridLayoutConfig> = {
                rowGap,
                columnGap,
                rowGaps,
                rowSizing: 'auto',
                columnSizing: 'auto',
            };

            devLogger.info('gridlayout.convert.inputs', {
                componentId: component.id,
                componentType: component.type,
                objectLayout: effectiveObjectLayout,
                layoutGroupKeys: Object.keys(effectiveLayoutGroups || {}),
                visibleObjectIds,
                objectIdsForConversion,
                hasGlobalDefaults: Boolean(globalStyles?.defaultGridLayout),
                hasGlobalObjectLayoutDefault: Boolean(globalStyles?.defaultObjectLayout),
                spacing: {
                    labelGapPx,
                    inputHelpGapPx,
                    rowGap,
                    columnGap,
                    rowGaps,
                    rowSizing: baseGridConfig.rowSizing,
                    columnSizing: baseGridConfig.columnSizing,
                },
            });

            let gridLayout = createGridLayoutFromObjectLayout(
                effectiveObjectLayout,
                objectIdsForConversion,
                effectiveLayoutGroups,
                {
                    ...globalStyles?.defaultGridLayout,
                    ...baseGridConfig,
                }
            );

            devLogger.info('gridlayout.convert.result', {
                componentId: component.id,
                rows: gridLayout.rows,
                columns: gridLayout.columns,
                assignments: gridLayout.cellAssignments,
            });

            if (effectiveObjectLayout === 'vertical' && (gridLayout.rows !== 3 || gridLayout.columns !== 1)) {
                gridLayout = createGridLayoutFromObjectLayout(
                    'vertical',
                    objectIdsForConversion,
                    {},
                    globalStyles?.defaultGridLayout
                );

                devLogger.info('gridlayout.convert.fallback', {
                    componentId: component.id,
                    reason: 'vertical_shape_mismatch',
                    rows: gridLayout.rows,
                    columns: gridLayout.columns,
                    assignments: gridLayout.cellAssignments,
                });
            }

            if (effectiveObjectLayout === 'horizontal' && (gridLayout.rows !== 1 || gridLayout.columns !== 3)) {
                gridLayout = createGridLayoutFromObjectLayout(
                    'horizontal',
                    objectIdsForConversion,
                    {},
                    globalStyles?.defaultGridLayout
                );

                devLogger.info('gridlayout.convert.fallback', {
                    componentId: component.id,
                    reason: 'horizontal_shape_mismatch',
                    rows: gridLayout.rows,
                    columns: gridLayout.columns,
                    assignments: gridLayout.cellAssignments,
                });
            }

            devLogger.info('gridlayout.converted.from.object', {
                componentId: component.id,
                objectLayout: effectiveObjectLayout,
                rows: gridLayout.rows,
                columns: gridLayout.columns,
                assignments: gridLayout.cellAssignments,
            });

            onPropsChange({ gridLayout });
        } else {
            // Switch back to Object Layout: explicitly set gridLayout to null to opt out of grid mode
            // even when global defaults exist. null is different from undefined - undefined means "inherit",
            // null means "explicitly use object layout"
            onPropsChange({ gridLayout: null as any });
        }
    }, [
        component,
        globalStyles,
        onPropsChange,
        structure.defaultLayout,
        structure.layoutGroups,
        visibleObjects
    ]);
    
    // Handle grid config updates
    const handleGridConfigChange = useCallback((updates: Partial<GridLayoutConfig>) => {
        // Always create/update component override when user makes changes
        // Start from current effective config (which may be from global defaults)
        const baseConfig = currentGridConfig;
        const newConfig: GridLayoutConfig = {
            ...baseConfig,
            ...updates,
        };
        
        devLogger.info('gridlayout.config.changed', {
            componentId: component.id,
            hasExistingOverride: component.props.gridLayout !== undefined,
            updates,
            baseConfig,
            newConfig,
        });
        
        // Always create/update the override - even if we started from global defaults
        onPropsChange({ gridLayout: newConfig });
    }, [component.id, component.props.gridLayout, currentGridConfig, onPropsChange]);
    
    // Handle rows change with validation and cleanup invalid rowGaps
    const handleRowsChange = useCallback((value: number) => {
        const rows = Math.max(1, Math.min(12, value));
        
        // Clean up invalid rowGaps entries (indices >= rows-1)
        let rowGaps = currentGridConfig.rowGaps;
        if (rowGaps) {
            const cleanedRowGaps: Record<number, number> = {};
            for (const [indexStr, gap] of Object.entries(rowGaps)) {
                const index = Number(indexStr);
                if (index < rows - 1) {
                    cleanedRowGaps[index] = gap;
                }
            }
            rowGaps = Object.keys(cleanedRowGaps).length > 0 ? cleanedRowGaps : undefined;
        }
        
        handleGridConfigChange({ rows, rowGaps });
    }, [currentGridConfig.rowGaps, handleGridConfigChange]);
    
    // Handle columns change with validation and cleanup invalid columnGaps
    const handleColumnsChange = useCallback((value: number) => {
        const columns = Math.max(1, Math.min(12, value));
        
        // Clean up invalid columnGaps entries (indices >= columns-1)
        let columnGaps = currentGridConfig.columnGaps;
        if (columnGaps) {
            const cleanedColumnGaps: Record<number, number> = {};
            for (const [indexStr, gap] of Object.entries(columnGaps)) {
                const index = Number(indexStr);
                if (index < columns - 1) {
                    cleanedColumnGaps[index] = gap;
                }
            }
            columnGaps = Object.keys(cleanedColumnGaps).length > 0 ? cleanedColumnGaps : undefined;
        }
        
        handleGridConfigChange({ columns, columnGaps });
    }, [currentGridConfig.columnGaps, handleGridConfigChange]);
    
    // Handle row gap change with validation
    const handleRowGapChange = useCallback((value: number) => {
        const rowGap = Math.max(0, Math.min(48, value));
        // Clear per-row overrides so the default row gap takes effect
        handleGridConfigChange({ rowGap, rowGaps: undefined });
    }, [handleGridConfigChange]);
    
    // Handle column gap change with validation
    const handleColumnGapChange = useCallback((value: number) => {
        const columnGap = Math.max(0, Math.min(48, value));
        handleGridConfigChange({ columnGap });
    }, [handleGridConfigChange]);
    
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
    
    // Handle individual row gap change
    const handleIndividualRowGapChange = useCallback((index: number, value: number) => {
        const gap = Math.max(0, Math.min(48, value));
        const rowGaps = { ...(currentGridConfig.rowGaps || {}) };
        
        if (gap === currentGridConfig.rowGap) {
            // Reset to default: remove override
            delete rowGaps[index];
        } else {
            rowGaps[index] = gap;
        }
        
        handleGridConfigChange({
            rowGaps: Object.keys(rowGaps).length > 0 ? rowGaps : undefined
        });
    }, [currentGridConfig, handleGridConfigChange]);
    
    // Handle reset row gap
    const handleResetRowGap = useCallback((index: number) => {
        const rowGaps = { ...(currentGridConfig.rowGaps || {}) };
        delete rowGaps[index];
        
        handleGridConfigChange({
            rowGaps: Object.keys(rowGaps).length > 0 ? rowGaps : undefined
        });
    }, [currentGridConfig, handleGridConfigChange]);
    
    // Handle drag start
    const handleDragStart = useCallback((event: DragStartEvent) => {
        setActiveId(event.active.id);
        devLogger.info('gridlayout.drag.start', {
            componentId: component.id,
            objectId: String(event.active.id),
        });
    }, [component.id]);

    // Clear an object's assignment from any merged cell groups
    const clearObjectFromMergedCells = useCallback((
        objectId: string,
        mergedCells?: GridLayoutConfig['mergedCells']
    ): { mergedCells?: GridLayoutConfig['mergedCells']; didChange: boolean } => {
        if (!mergedCells) {
            return { mergedCells, didChange: false };
        }

        let didChange = false;
        const updatedMergedCells: GridLayoutConfig['mergedCells'] = { ...mergedCells };

        for (const [mergeId, group] of Object.entries(mergedCells)) {
            if (group.objectId === objectId) {
                updatedMergedCells[mergeId] = {
                    ...group,
                    objectId: '',
                };
                didChange = true;
            }
        }

        return { mergedCells: didChange ? updatedMergedCells : mergedCells, didChange };
    }, []);
    
    // Handle drag end - main DnD logic
    const handleDragEnd = useCallback((event: DragEndEvent) => {
        const { active, over } = event;
        setActiveId(null);
        
        if (!over) {
            devLogger.info('gridlayout.drag.cancel', {
                componentId: component.id,
                objectId: String(active.id),
            });
            return;
        }
        
        const objectId = String(active.id);
        const targetId = String(over.id);
        
        // Build new cellAssignments
        const newAssignments = { ...currentGridConfig.cellAssignments };
        const newObjectSpans = { ...(currentGridConfig.objectSpans || {}) };
        let updatedMergedCells = currentGridConfig.mergedCells;
        
        // Remove object from current position (enforce single placement)
        for (const [key, id] of Object.entries(newAssignments)) {
            if (id === objectId) {
                delete newAssignments[key];
                break;
            }
        }
        
        // Remove object span if it existed
        if (newObjectSpans[objectId]) {
            delete newObjectSpans[objectId];
        }

        // Remove object from any merged cell groups (prevents ghost assignments)
        const clearedMergeInfo = clearObjectFromMergedCells(objectId, updatedMergedCells);
        updatedMergedCells = clearedMergeInfo.mergedCells;
        
        // Determine target
        if (targetId === 'available-pool') {
            // Dropped on pool - object was already removed above
            devLogger.info('gridlayout.object.returned', {
                componentId: component.id,
                objectId,
            });
        } else if (targetId.startsWith('cell-')) {
            // Dropped on a cell - extract row-col from cell-row-col
            const cellKey = targetId.replace('cell-', '');
            
            // Check if target cell is part of a merged group
            const mergeInfo = getMergeGroupForCell(cellKey, currentGridConfig);
            
            if (mergeInfo) {
                // Dropped into merged cell - assign to first cell and update span
                const firstCell = mergeInfo.group.cells[0];
                
                // Check if merged cell already has an object
                if (mergeInfo.group.objectId && mergeInfo.group.objectId !== objectId) {
                    devLogger.info('gridlayout.drop.blocked.merged', {
                        componentId: component.id,
                        objectId,
                        targetCell: cellKey,
                        occupiedBy: mergeInfo.group.objectId,
                    });
                    return;
                }
                
                // Assign to first cell
                newAssignments[firstCell] = objectId;
                
                // Calculate span from merged cells
                const span = getMergeSpan(mergeInfo.group.cells);
                newObjectSpans[objectId] = span;
                
                // Update mergedCells to include objectId
                const mergedCellsWithAssignment = { ...(updatedMergedCells || {}) };
                mergedCellsWithAssignment[mergeInfo.mergeId] = {
                    ...mergeInfo.group,
                    objectId,
                };
                
                devLogger.info('gridlayout.object.assigned.merged', {
                    componentId: component.id,
                    objectId,
                    targetCell: cellKey,
                    mergeId: mergeInfo.mergeId,
                    span,
                });
                
                handleGridConfigChange({ 
                    cellAssignments: newAssignments,
                    objectSpans: newObjectSpans,
                    mergedCells: mergedCellsWithAssignment,
                });
                return;
            }
            
            // Regular cell drop
            // Check if target cell is empty (or occupied by same object)
            const existingObject = newAssignments[cellKey];
            if (existingObject && existingObject !== objectId) {
                // Cell is occupied by another object - prevent drop
                devLogger.info('gridlayout.drop.blocked', {
                    componentId: component.id,
                    objectId,
                    targetCell: cellKey,
                    occupiedBy: existingObject,
                });
                return;
            }
            
            // Assign object to new cell
            newAssignments[cellKey] = objectId;
            
            devLogger.info('gridlayout.object.assigned', {
                componentId: component.id,
                objectId,
                targetCell: cellKey,
            });
        }
        
        // Update config
        handleGridConfigChange({ 
            cellAssignments: newAssignments,
            objectSpans: Object.keys(newObjectSpans).length > 0 ? newObjectSpans : undefined,
            mergedCells: updatedMergedCells,
        });
    }, [component.id, currentGridConfig, handleGridConfigChange, clearObjectFromMergedCells]);
    
    // Handle remove object from cell
    const handleRemoveObject = useCallback((cellKeyToRemove: string) => {
        const newAssignments = { ...currentGridConfig.cellAssignments };
        const objectId = newAssignments[cellKeyToRemove];
        delete newAssignments[cellKeyToRemove];

        const newObjectSpans = { ...(currentGridConfig.objectSpans || {}) };
        if (objectId && newObjectSpans[objectId]) {
            delete newObjectSpans[objectId];
        }

        const clearedMergeInfo = objectId
            ? clearObjectFromMergedCells(objectId, currentGridConfig.mergedCells)
            : { mergedCells: currentGridConfig.mergedCells, didChange: false };
        
        devLogger.info('gridlayout.object.removed', {
            componentId: component.id,
            objectId,
            fromCell: cellKeyToRemove,
        });
        
        handleGridConfigChange({
            cellAssignments: newAssignments,
            objectSpans: Object.keys(newObjectSpans).length > 0 ? newObjectSpans : undefined,
            mergedCells: clearedMergeInfo.mergedCells,
        });
    }, [component.id, currentGridConfig.cellAssignments, currentGridConfig.objectSpans, currentGridConfig.mergedCells, handleGridConfigChange, clearObjectFromMergedCells]);
    
    // Handle cell click for selection
    const handleCellClick = useCallback((cellKeyValue: string, event: React.MouseEvent) => {
        // Check if Shift key is pressed for range selection
        if (event.shiftKey && selectedCells.size > 0) {
            // Range selection: select all cells between first selected and clicked cell
            const firstSelected = Array.from(selectedCells)[0];
            const firstPos = parseCell(firstSelected);
            const clickedPos = parseCell(cellKeyValue);
            
            const minRow = Math.min(firstPos.row, clickedPos.row);
            const maxRow = Math.max(firstPos.row, clickedPos.row);
            const minCol = Math.min(firstPos.col, clickedPos.col);
            const maxCol = Math.max(firstPos.col, clickedPos.col);
            
            const rangeCells = new Set<string>();
            for (let row = minRow; row <= maxRow; row++) {
                for (let col = minCol; col <= maxCol; col++) {
                    rangeCells.add(cellKey(row, col));
                }
            }
            setSelectedCells(rangeCells);
        } else {
            // Toggle selection for single cell
            const newSelection = new Set(selectedCells);
            if (newSelection.has(cellKeyValue)) {
                newSelection.delete(cellKeyValue);
            } else {
                newSelection.add(cellKeyValue);
            }
            setSelectedCells(newSelection);
        }
    }, [selectedCells]);
    
    // Helper to parse cell key
    const parseCell = (key: string): { row: number; col: number } => {
        const parts = key.split('-');
        return { row: parseInt(parts[0], 10), col: parseInt(parts[1], 10) };
    };
    
    // Handle merge cells action
    const handleMergeCells = useCallback(() => {
        const cellArray = Array.from(selectedCells);
        if (!isValidMergeSelection(cellArray)) {
            devLogger.warn('gridlayout.merge.invalid', {
                componentId: component.id,
                selectedCells: cellArray,
            });
            return;
        }
        
        try {
            const newConfig = mergeCells(cellArray, currentGridConfig);
            handleGridConfigChange(newConfig);
            setSelectedCells(new Set()); // Clear selection after merge
            devLogger.info('gridlayout.cells.merged', {
                componentId: component.id,
                cells: cellArray,
            });
        } catch (error) {
            devLogger.error('gridlayout.merge.failed', {
                componentId: component.id,
                error: error instanceof Error ? error.message : String(error),
            });
        }
    }, [selectedCells, currentGridConfig, component.id, handleGridConfigChange]);
    
    // Handle unmerge cells action
    const handleUnmergeCells = useCallback((mergeId: string) => {
        const newConfig = unmergeCells(mergeId, currentGridConfig);
        handleGridConfigChange(newConfig);
        devLogger.info('gridlayout.cells.unmerged', {
            componentId: component.id,
            mergeId,
        });
    }, [currentGridConfig, component.id, handleGridConfigChange]);
    
    // Check if current selection is valid for merging
    const canMerge = useMemo(() => {
        if (selectedCells.size < 2) return false;
        return isValidMergeSelection(Array.from(selectedCells));
    }, [selectedCells]);
    
    // All sortable IDs (available objects + assigned objects)
    const allSortableIds = useMemo(() => {
        const poolIds = availableObjects.map(obj => obj.id);
        const assignedIds = Object.values(currentGridConfig.cellAssignments);
        return [...poolIds, ...assignedIds];
    }, [availableObjects, currentGridConfig.cellAssignments]);
    
    return (
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <Grid3x3 size={16} className="text-gray-500" />
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Layout Mode
                    </h4>
                </div>
            </div>
            
            {/* Layout Mode Toggle */}
            <div className="space-y-3">
                <div className="grid grid-cols-2 gap-2">
                    {/* Object Layout Button */}
                    <button
                        type="button"
                        onClick={() => handleLayoutModeChange('object')}
                        className={`p-2 rounded border-2 transition-colors flex flex-col items-center gap-1 ${
                            !isGridMode
                                ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                        }`}
                        title="Object Layout: Row-based layout with vertical/horizontal/mixed options"
                    >
                        <LayoutGrid size={16} className={!isGridMode ? 'text-teal-600' : 'text-gray-400'} />
                        <span className="text-[10px] font-medium">Object Layout</span>
                    </button>
                    
                    {/* Grid Layout Button */}
                    <button
                        type="button"
                        onClick={() => handleLayoutModeChange('grid')}
                        className={`p-2 rounded border-2 transition-colors flex flex-col items-center gap-1 ${
                            isGridMode
                                ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20'
                                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                        }`}
                        title="Grid Layout: CSS Grid-based layout with rows × columns"
                    >
                        <Grid3x3 size={16} className={isGridMode ? 'text-indigo-600' : 'text-gray-400'} />
                        <span className="text-[10px] font-medium">Grid Layout</span>
                    </button>
                </div>
                
                {/* Mode Description */}
                <div className="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded">
                    {isGridMode ? (
                        <>
                            <strong className="text-indigo-600 dark:text-indigo-400">Grid Layout:</strong>{' '}
                            Arrange objects in a configurable rows × columns grid structure with CSS Grid.
                        </>
                    ) : (
                        <>
                            <strong className="text-teal-600 dark:text-teal-400">Object Layout:</strong>{' '}
                            Arrange objects in rows with vertical, horizontal, or mixed layout options.
                        </>
                    )}
                </div>
            </div>
            
            {/* Grid Configuration (only shown when in Grid mode) */}
            {isGridMode && (
                <div className="mt-4 space-y-4">
                    {/* Source Indicator and Override/Reset Actions */}
                    <div className="flex items-center justify-between mb-3">
                        {/* Source Indicator */}
                        <div className={`text-[10px] px-2 py-0.5 rounded ${
                            hasOverride
                                ? 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'
                                : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
                        }`}>
                            {hasOverride 
                                ? '🔧 Component Override' 
                                : '🌐 Using Global Default'}
                        </div>
                        
                        {/* Action Buttons */}
                        <div className="flex gap-2">
                            {!hasOverride ? (
                                <button
                                    type="button"
                                    onClick={() => {
                                        const componentDefault = resolveComponentDefaultGridLayout({
                                            structure,
                                            componentType: component.type,
                                            globalStyles,
                                        });
                                        const effective = getEffectiveGridLayout(
                                            component.props.gridLayout,
                                            componentDefault,
                                            globalStyles?.defaultGridLayout
                                        );
                                        if (effective) {
                                            onPropsChange({ gridLayout: { ...effective } });
                                        }
                                    }}
                                    className="text-[10px] text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300"
                                >
                                    Override Global
                                </button>
                            ) : (
                                <button
                                    type="button"
                                    onClick={() => {
                                        onPropsChange({ gridLayout: undefined });
                                    }}
                                    className="text-[10px] text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400"
                                >
                                    Reset to Global
                                </button>
                            )}
                        </div>
                    </div>
                    
                    {/* Grid Structure Controls */}
                    <div className="space-y-3">
                        <label className="text-xs text-gray-600 dark:text-gray-400 font-medium block">
                            Grid Structure
                        </label>
                        
                        {/* Rows Control */}
                        <div className="flex items-center gap-3">
                            <div className="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-400 w-20">
                                <Rows size={12} />
                                <span>Rows</span>
                            </div>
                            <div className="flex items-center gap-2 flex-1">
                                <button
                                    type="button"
                                    onClick={() => handleRowsChange(currentGridConfig.rows - 1)}
                                    disabled={currentGridConfig.rows <= 1}
                                    className="w-6 h-6 flex items-center justify-center rounded border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    −
                                </button>
                                <input
                                    type="number"
                                    min={1}
                                    max={12}
                                    value={currentGridConfig.rows}
                                    onChange={(e) => handleRowsChange(parseInt(e.target.value) || 1)}
                                    className="w-12 h-6 text-center text-xs border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
                                />
                                <button
                                    type="button"
                                    onClick={() => handleRowsChange(currentGridConfig.rows + 1)}
                                    disabled={currentGridConfig.rows >= 12}
                                    className="w-6 h-6 flex items-center justify-center rounded border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    +
                                </button>
                                <span className="text-[10px] text-gray-400">(1-12)</span>
                            </div>
                        </div>
                        
                        {/* Columns Control */}
                        <div className="flex items-center gap-3">
                            <div className="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-400 w-20">
                                <Columns size={12} />
                                <span>Columns</span>
                            </div>
                            <div className="flex items-center gap-2 flex-1">
                                <button
                                    type="button"
                                    onClick={() => handleColumnsChange(currentGridConfig.columns - 1)}
                                    disabled={currentGridConfig.columns <= 1}
                                    className="w-6 h-6 flex items-center justify-center rounded border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    −
                                </button>
                                <input
                                    type="number"
                                    min={1}
                                    max={12}
                                    value={currentGridConfig.columns}
                                    onChange={(e) => handleColumnsChange(parseInt(e.target.value) || 1)}
                                    className="w-12 h-6 text-center text-xs border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
                                />
                                <button
                                    type="button"
                                    onClick={() => handleColumnsChange(currentGridConfig.columns + 1)}
                                    disabled={currentGridConfig.columns >= 12}
                                    className="w-6 h-6 flex items-center justify-center rounded border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    +
                                </button>
                                <span className="text-[10px] text-gray-400">(1-12)</span>
                            </div>
                        </div>
                    </div>
                    
                    {/* Gap Controls */}
                    <div className="space-y-3">
                        <label className="text-xs text-gray-600 dark:text-gray-400 font-medium flex items-center gap-1.5">
                            <Space size={12} />
                            Gap (Default Spacing)
                        </label>
                        
                        {/* Row Gap */}
                        <div className="flex items-center gap-3">
                            <span className="text-[10px] text-gray-500 dark:text-gray-400 w-20">Row Gap</span>
                            <div className="flex items-center gap-2 flex-1">
                                <input
                                    type="range"
                                    min={0}
                                    max={48}
                                    step={1}
                                    value={currentGridConfig.rowGap}
                                    onChange={(e) => handleRowGapChange(parseInt(e.target.value))}
                                    disabled={!!currentGridConfig.rowGaps}
                                    className="flex-1 h-1.5 accent-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                                />
                                <span className="text-[10px] text-gray-600 dark:text-gray-400 w-10 text-right">
                                    {currentGridConfig.rowGap}px
                                </span>
                            </div>
                        </div>
                        {currentGridConfig.rowGaps && (
                            <div className="text-[9px] text-gray-400 dark:text-gray-500">
                                Default Row Gap is disabled while individual row spacing is set.
                            </div>
                        )}
                        
                        {/* Column Gap */}
                        <div className="flex items-center gap-3">
                            <span className="text-[10px] text-gray-500 dark:text-gray-400 w-20">Column Gap</span>
                            <div className="flex items-center gap-2 flex-1">
                                <input
                                    type="range"
                                    min={0}
                                    max={48}
                                    step={1}
                                    value={currentGridConfig.columnGap}
                                    onChange={(e) => handleColumnGapChange(parseInt(e.target.value))}
                                    className="flex-1 h-1.5 accent-indigo-500"
                                />
                                <span className="text-[10px] text-gray-600 dark:text-gray-400 w-10 text-right">
                                    {currentGridConfig.columnGap}px
                                </span>
                            </div>
                        </div>
                        
                        {/* Individual Column Spacing Section */}
                        {currentGridConfig.columns > 1 && (
                            <IndividualSpacingSection
                                title="Individual Column Spacing"
                                count={currentGridConfig.columns - 1}
                                labelTemplate={(i) => `Col ${i} → Col ${i + 1}`}
                                gaps={currentGridConfig.columnGaps || {}}
                                defaultGap={currentGridConfig.columnGap}
                                onGapChange={handleIndividualColumnGapChange}
                                onReset={handleResetColumnGap}
                            />
                        )}
                        
                        {/* Individual Row Spacing Section */}
                        {currentGridConfig.rows > 1 && (
                            <IndividualSpacingSection
                                title="Individual Row Spacing"
                                count={currentGridConfig.rows - 1}
                                labelTemplate={(i) => `Row ${i} → Row ${i + 1}`}
                                gaps={currentGridConfig.rowGaps || {}}
                                defaultGap={currentGridConfig.rowGap}
                                onGapChange={handleIndividualRowGapChange}
                                onReset={handleResetRowGap}
                            />
                        )}
                    </div>
                    
                    {/* Grid Preview with DnD */}
                    <DndContext
                        sensors={sensors}
                        collisionDetection={closestCenter}
                        onDragStart={handleDragStart}
                        onDragEnd={handleDragEnd}
                    >
                        <SortableContext items={allSortableIds} strategy={horizontalListSortingStrategy}>
                            {/* Available Objects Pool */}
                            <div className="space-y-2 mb-4">
                                <label className="text-xs text-gray-600 dark:text-gray-400 font-medium flex items-center gap-1.5">
                                    <Package size={12} />
                                    Available Objects
                                </label>
                                <AvailableObjectsPool
                                    objectIds={availableObjects.map(obj => obj.id)}
                                    objectLabels={objectLabels}
                                />
                            </div>
                            
                            {/* Merge/Unmerge Actions */}
                            {selectedCells.size >= 2 && (
                                <div className="flex items-center gap-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded border border-blue-200 dark:border-blue-800">
                                    <span className="text-xs text-blue-700 dark:text-blue-300">
                                        {selectedCells.size} cell{selectedCells.size !== 1 ? 's' : ''} selected
                                    </span>
                                    {canMerge ? (
                                        <button
                                            type="button"
                                            onClick={handleMergeCells}
                                            className="px-2 py-1 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded transition-colors"
                                        >
                                            Merge Cells
                                        </button>
                                    ) : (
                                        <button
                                            type="button"
                                            disabled
                                            className="px-2 py-1 text-xs font-medium text-gray-400 bg-gray-200 dark:bg-gray-700 rounded cursor-not-allowed"
                                            title="Only rectangular selections can be merged"
                                        >
                                            Merge Cells
                                        </button>
                                    )}
                                    <button
                                        type="button"
                                        onClick={() => setSelectedCells(new Set())}
                                        className="px-2 py-1 text-xs font-medium text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
                                    >
                                        Clear
                                    </button>
                                </div>
                            )}
                            
                            {/* Grid Preview */}
                            <div className="space-y-2">
                                <label className="text-xs text-gray-600 dark:text-gray-400 font-medium block">
                                    Grid Preview
                                </label>
                                <GridLayoutEditor
                                    config={currentGridConfig}
                                    structure={structure}
                                    showCoordinates={true}
                                    maxHeight={200}
                                    selectedCells={selectedCells}
                                    onCellClick={handleCellClick}
                                    onRemoveObject={handleRemoveObject}
                                    onUnmerge={handleUnmergeCells}
                                />
                            </div>
                        </SortableContext>
                        
                        {/* Drag Overlay */}
                        <DragOverlay>
                            {activeId ? (
                                <DragOverlayItem label={objectLabels[String(activeId)] || String(activeId)} />
                            ) : null}
                        </DragOverlay>
                    </DndContext>
                </div>
            )}
        </div>
    );
};

export default GridLayoutSection;
