/**
 * ObjectLayoutSection Component
 * 
 * Properties Panel section for configuring object layout within components.
 * Allows users to change layout type (vertical/horizontal/mixed) and configure
 * layout groups for mixed layouts with drag-and-drop support.
 * 
 * Enhanced with:
 * - Single DndContext for cross-row dragging
 * - 3-row visual grid layout
 * - Available Objects pool for unassigned objects
 */

import React, { useState, useMemo } from 'react';
import { LayoutGrid, ArrowUpDown, ArrowLeftRight, Grid3x3, GripVertical, Plus, Package } from 'lucide-react';
import { 
    DndContext, 
    KeyboardSensor, 
    PointerSensor, 
    useSensor, 
    useSensors,
    DragEndEvent,
    DragStartEvent,
    DragOverlay,
    UniqueIdentifier,
    useDroppable,
    rectIntersection,
} from '@dnd-kit/core';
import {
    arrayMove,
    SortableContext,
    sortableKeyboardCoordinates,
    useSortable,
    horizontalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { FormComponent, ComponentStructure, ObjectLayoutType, ComponentProps, RowAlignment } from '../../types/builder.types';
import { devLogger } from '../../utils/devLogger';
import { PropertySelect } from './inputs';

interface ObjectLayoutSectionProps {
    component: FormComponent;
    structure: ComponentStructure;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
    globalStyles?: {
        defaultObjectLayout?: ObjectLayoutType;
        defaultLayoutGroups?: Record<string, string[]>;
    };
}

const ROW_ALIGNMENT_OPTIONS: Array<{ value: RowAlignment; label: string }> = [
    { value: 'top', label: 'Top' },
    { value: 'center', label: 'Center' },
    { value: 'bottom', label: 'Bottom' },
    { value: 'stretch', label: 'Stretch' },
];

interface DraggableObjectProps {
    id: string;
    label: string;
    isInPool?: boolean;
}

/**
 * Draggable object item used in rows and the available objects pool.
 */
const DraggableObject: React.FC<DraggableObjectProps> = ({ id, label, isInPool }) => {
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
            {...attributes}
            {...listeners}
            className={`flex items-center gap-1 px-2 py-1.5 rounded border transition-colors select-none ${
                isInPool 
                    ? 'bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-600 hover:border-teal-400' 
                    : 'bg-white dark:bg-gray-700 border-gray-200 dark:border-gray-600 hover:border-teal-400 dark:hover:border-teal-500'
            }`}
        >
            <GripVertical size={12} className="text-gray-400" />
            <span className="text-[10px] font-medium">{label}</span>
        </div>
    );
};

interface DroppableRowProps {
    rowId: string;
    rowLabel: string;
    objectIds: string[];
    allObjects: Array<{ id: string; label?: string }>;
    isOver?: boolean;
}

/**
 * DroppableRow component - a row that accepts dragged objects.
 * Renders as a drop zone that displays objects horizontally.
 */
const DroppableRow: React.FC<DroppableRowProps> = ({
    rowId,
    rowLabel,
    objectIds,
    allObjects,
}) => {
    const { setNodeRef, isOver } = useDroppable({ id: rowId });

    return (
        <div
            ref={setNodeRef}
            className={`p-2 rounded border-2 border-dashed min-h-[48px] transition-colors ${
                isOver 
                    ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' 
                    : 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800'
            }`}
        >
            <div className="text-[10px] font-medium text-gray-500 dark:text-gray-400 mb-1.5">
                {rowLabel}
            </div>
            <SortableContext items={objectIds} strategy={horizontalListSortingStrategy}>
                <div className="flex flex-wrap gap-1.5">
                    {objectIds.length === 0 ? (
                        <div className="text-[10px] text-gray-400 dark:text-gray-500 italic py-1">
                            Drop objects here
                        </div>
                    ) : (
                        objectIds.map(objId => {
                            const obj = allObjects.find(o => o.id === objId);
                            return (
                                <DraggableObject
                                    key={objId}
                                    id={objId}
                                    label={obj?.label || obj?.id || objId}
                                />
                            );
                        })
                    )}
                </div>
            </SortableContext>
        </div>
    );
};

interface AvailableObjectsPoolProps {
    objectIds: string[];
    allObjects: Array<{ id: string; label?: string }>;
}

/**
 * Available Objects Pool - shows unassigned objects that can be dragged to rows.
 */
const AvailableObjectsPool: React.FC<AvailableObjectsPoolProps> = ({
    objectIds,
    allObjects,
}) => {
    const { setNodeRef, isOver } = useDroppable({ id: 'available-pool' });

    return (
        <div
            ref={setNodeRef}
            className={`p-2 rounded border-2 min-h-[48px] transition-colors ${
                isOver 
                    ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' 
                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900'
            }`}
        >
            <div className="flex items-center gap-1.5 text-[10px] font-medium text-gray-500 dark:text-gray-400 mb-1.5">
                <Package size={12} />
                Available Objects
            </div>
            <SortableContext items={objectIds} strategy={horizontalListSortingStrategy}>
                <div className="flex flex-wrap gap-1.5">
                    {objectIds.length === 0 ? (
                        <div className="text-[10px] text-gray-400 dark:text-gray-500 italic py-1">
                            All objects assigned to rows
                        </div>
                    ) : (
                        objectIds.map(objId => {
                            const obj = allObjects.find(o => o.id === objId);
                            return (
                                <DraggableObject
                                    key={objId}
                                    id={objId}
                                    label={obj?.label || obj?.id || objId}
                                    isInPool
                                />
                            );
                        })
                    )}
                </div>
            </SortableContext>
        </div>
    );
};

// Fixed 3-row layout for mixed mode
const FIXED_ROWS = ['row1', 'row2', 'row3'] as const;
const ROW_LABELS: Record<string, string> = {
    row1: 'Row 1 (Top)',
    row2: 'Row 2 (Middle)',
    row3: 'Row 3 (Bottom)',
};

export const ObjectLayoutSection: React.FC<ObjectLayoutSectionProps> = ({
    component,
    structure,
    onPropsChange,
    globalStyles,
}) => {
    const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);
    
    // Determine if component has object layout override
    const hasObjectLayoutOverride = component.props.objectLayout !== undefined || 
                                     component.props.layoutGroups !== undefined;
    
    // Get effective layout: component override > global default > structure default > 'vertical'
    const currentLayout = component.props.objectLayout || 
                         globalStyles?.defaultObjectLayout || 
                         structure.defaultLayout || 
                         'vertical';
    
    // Get effective row alignment: component override > structure default > 'center'
    const currentRowAlignment = component.props.rowAlignment || 
                               structure.defaultRowAlignment || 
                               'center';
    
    // Get effective groups: component override > global default > structure default > {}
    const currentGroups = component.props.layoutGroups || 
                         globalStyles?.defaultLayoutGroups || 
                         structure.layoutGroups || 
                         {};
    
    // Objects available to the layout editor.
    //
    // Framework rule:
    // - Keep `validation` available for layout even though it is conditionally rendered at runtime.
    // - Hide "Other" input objects unless `allowOther` is enabled, to avoid confusing layouts.
    const visibleObjects = useMemo(() => {
        return structure.objects.filter(obj => {
            if (obj.type === 'validation') return true;
            if (obj.required) return true;
            const cond = obj.conditional;
            if (!cond) return true;
            if (cond.type === 'prop' && cond.prop === 'allowOther') {
                return Boolean((component.props as any)?.allowOther);
            }
            return true;
        });
    }, [structure.objects, component.props]);
    
    // Get all object IDs currently in groups
    const usedObjectIds = useMemo(() => 
        new Set(Object.values(currentGroups).flat()),
        [currentGroups]
    );
    
    // Get available objects (not yet in any group)
    const availableObjects = useMemo(() =>
        visibleObjects.filter(obj => !usedObjectIds.has(obj.id)),
        [visibleObjects, usedObjectIds]
    );
    
    // Get object labels map
    const objectLabels = useMemo(() => {
        const labels: Record<string, string> = {};
        visibleObjects.forEach(obj => {
            labels[obj.id] = obj.label || obj.id;
        });
        return labels;
    }, [visibleObjects]);
    
    // Sensors for drag and drop
    const sensors = useSensors(
        useSensor(PointerSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );
    
    const handleLayoutChange = (layout: ObjectLayoutType) => {
        const oldLayout =
            component.props.objectLayout ||
            globalStyles?.defaultObjectLayout ||
            structure.defaultLayout;
        
        // Log layout type change
        devLogger.info('objectlayout.type.changed', {
            componentId: component.id,
            from: oldLayout,
            to: layout,
        });
        
        devLogger.info('fieldshell.properties.layout.changed', {
            componentId: component.id,
            property: 'objectLayout',
            oldValue: oldLayout,
            newValue: layout
        });
        
        onPropsChange({ objectLayout: layout });
    };
    
    const handleGroupsChange = (groups: Record<string, string[]>) => {
        const oldGroups = component.props.layoutGroups || structure.layoutGroups || {};
        
        devLogger.info('fieldshell.properties.layout.changed', {
            componentId: component.id,
            property: 'layoutGroups',
            oldValue: oldGroups,
            newValue: groups
        });
        
        onPropsChange({ layoutGroups: groups });
    };
    
    const handleDragStart = (event: DragStartEvent) => {
        setActiveId(event.active.id);
    };
    
    const handleDragEnd = (event: DragEndEvent) => {
        const { active, over } = event;
        setActiveId(null);
        
        if (!over) return;
        
        const activeIdStr = String(active.id);
        const overIdStr = String(over.id);
        
        // Find which row the object is currently in
        let fromRow: string | null = null;
        for (const [rowKey, objectIds] of Object.entries(currentGroups)) {
            if (objectIds.includes(activeIdStr)) {
                fromRow = rowKey;
                break;
            }
        }
        // If not in any row, it's in the available pool
        if (!fromRow && availableObjects.some(obj => obj.id === activeIdStr)) {
            fromRow = 'available-pool';
        }
        
        // Determine target row
        let toRow: string | null = null;
        if (overIdStr === 'available-pool') {
            toRow = 'available-pool';
        } else if (FIXED_ROWS.includes(overIdStr as any)) {
            toRow = overIdStr;
        } else {
            // Check if dropped on another object (find its row)
            for (const [rowKey, objectIds] of Object.entries(currentGroups)) {
                if (objectIds.includes(overIdStr)) {
                    toRow = rowKey;
                    break;
                }
            }
        }
        
        if (!toRow) return;
        
        // Handle move between rows or to/from pool
        const updatedGroups = { ...currentGroups };

        // Ensure an object cannot exist in multiple rows at once.
        // Duplicates cause "snap back" behavior because the UI can still render it in its old row.
        const removeFromAllRows = (objectId: string) => {
            for (const rowKey of Object.keys(updatedGroups)) {
                updatedGroups[rowKey] = (updatedGroups[rowKey] || []).filter(id => id !== objectId);
                if (updatedGroups[rowKey].length === 0) {
                    delete updatedGroups[rowKey];
                }
            }
        };
        
        // If moving within the same row, use arrayMove for reordering
        if (fromRow === toRow && fromRow !== 'available-pool' && fromRow !== null) {
            const currentOrder = updatedGroups[fromRow] || [];
            const oldIndex = currentOrder.indexOf(activeIdStr);
            const newIndex = currentOrder.indexOf(overIdStr);
            
            if (oldIndex !== -1 && newIndex !== -1 && oldIndex !== newIndex) {
                updatedGroups[fromRow] = arrayMove(currentOrder, oldIndex, newIndex);
            }
        } else {
            // Moving between different rows or to/from pool
            // Remove from ALL rows first to guarantee uniqueness
            removeFromAllRows(activeIdStr);
            
            // Add to target row
            if (toRow !== 'available-pool') {
                if (!updatedGroups[toRow]) {
                    updatedGroups[toRow] = [];
                }
                if (!updatedGroups[toRow].includes(activeIdStr)) {
                    // Insert at position of the object it was dropped on, or append
                    const targetIndex = updatedGroups[toRow].indexOf(overIdStr);
                    if (targetIndex !== -1) {
                        updatedGroups[toRow].splice(targetIndex, 0, activeIdStr);
                    } else {
                        updatedGroups[toRow].push(activeIdStr);
                    }
                }
            }
        }
        
        // Log object move
        devLogger.info('objectlayout.object.moved', {
            componentId: component.id,
            objectId: activeIdStr,
            fromRow: fromRow || null,
            toRow: toRow === 'available-pool' ? null : toRow,
        });
        
        handleGroupsChange(updatedGroups);
    };
    
    const handleAddNewGroup = () => {
        if (availableObjects.length === 0) return;
        
        // Find next available group key (use fixed row keys)
        let groupNum = 1;
        while (currentGroups[`row${groupNum}`] || groupNum > 3) {
            groupNum++;
        }
        if (groupNum > 3) return; // Max 3 rows
        
        const newGroupKey = `row${groupNum}`;
        
        // Add first available object to new group
        const updatedGroups = {
            ...currentGroups,
            [newGroupKey]: [availableObjects[0].id]
        };
        
        // Log group creation
        devLogger.info('objectlayout.group.created', {
            componentId: component.id,
            rowKey: newGroupKey,
        });
        
        handleGroupsChange(updatedGroups);
    };
    
    // Get all object IDs for sortable context (all objects in rows + available pool)
    const allSortableIds = useMemo(() => {
        const rowIds = Object.values(currentGroups).flat();
        const poolIds = availableObjects.map(obj => obj.id);
        return [...rowIds, ...poolIds];
    }, [currentGroups, availableObjects]);
    
    return (
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <LayoutGrid size={16} className="text-gray-500" />
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Object Layout
                    </h4>
                </div>
                <div className="flex items-center gap-2">
                    {hasObjectLayoutOverride && (
                        <button
                            type="button"
                            onClick={() => onPropsChange({ objectLayout: undefined, layoutGroups: undefined })}
                            className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 underline"
                            title="Reset to global default"
                        >
                            Reset to Global
                        </button>
                    )}
                    <label className="flex items-center gap-1.5 text-xs text-gray-600 dark:text-gray-400">
                        <input
                            type="checkbox"
                            checked={hasObjectLayoutOverride}
                            onChange={(e) => {
                                if (e.target.checked) {
                                    // Enable override: use current effective values
                                    onPropsChange({ 
                                        objectLayout: currentLayout,
                                        layoutGroups: Object.keys(currentGroups).length > 0 ? currentGroups : undefined
                                    });
                                } else {
                                    // Disable override: clear component props
                                    onPropsChange({ objectLayout: undefined, layoutGroups: undefined });
                                }
                            }}
                            className="w-3 h-3 rounded border-gray-300 text-teal-600 focus:ring-teal-500"
                        />
                        <span>Override Global</span>
                    </label>
                </div>
            </div>
            {!hasObjectLayoutOverride && (
                <div className="mb-2 text-xs text-gray-500 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 p-2 rounded">
                    Using global default: <span className="font-medium">{currentLayout}</span>
                </div>
            )}
            
            {/* Layout Type Selector */}
            <div className="space-y-2 mb-4">
                <label className="text-xs text-gray-600 dark:text-gray-400 mb-2 block">
                    Layout Type
                </label>
                <div className="grid grid-cols-3 gap-2">
                    <button
                        onClick={() => handleLayoutChange('vertical')}
                        className={`p-2 rounded border-2 transition-colors flex flex-col items-center gap-1 ${
                            currentLayout === 'vertical'
                                ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                        }`}
                        title="Vertical: Objects stacked vertically"
                    >
                        <ArrowUpDown size={16} className={currentLayout === 'vertical' ? 'text-teal-600' : 'text-gray-400'} />
                        <span className="text-[10px] font-medium">Vertical</span>
                    </button>
                    
                    <button
                        onClick={() => handleLayoutChange('horizontal')}
                        className={`p-2 rounded border-2 transition-colors flex flex-col items-center gap-1 ${
                            currentLayout === 'horizontal'
                                ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                        }`}
                        title="Horizontal: Objects arranged in a row"
                    >
                        <ArrowLeftRight size={16} className={currentLayout === 'horizontal' ? 'text-teal-600' : 'text-gray-400'} />
                        <span className="text-[10px] font-medium">Horizontal</span>
                    </button>
                    
                    <button
                        onClick={() => handleLayoutChange('mixed')}
                        className={`p-2 rounded border-2 transition-colors flex flex-col items-center gap-1 ${
                            currentLayout === 'mixed'
                                ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                        }`}
                        title="Mixed: Custom grouping with rows"
                    >
                        <Grid3x3 size={16} className={currentLayout === 'mixed' ? 'text-teal-600' : 'text-gray-400'} />
                        <span className="text-[10px] font-medium">Mixed</span>
                    </button>
                </div>
            </div>

            {/* Row Alignment Control (Only for Horizontal/Mixed) */}
            {(currentLayout === 'horizontal' || currentLayout === 'mixed') && (
                <div className="space-y-2 mb-4">
                    <PropertySelect
                        label="Vertical Alignment"
                        value={currentRowAlignment}
                        onChange={(value) => onPropsChange({ rowAlignment: value as RowAlignment })}
                        options={ROW_ALIGNMENT_OPTIONS}
                        helpText="Align items vertically within their row (Top, Center, Bottom)"
                    />
                </div>
            )}
            
            {/* Layout Groups Editor (for mixed layout) */}
            {currentLayout === 'mixed' && visibleObjects.length > 1 && (
                <DndContext
                    sensors={sensors}
                    collisionDetection={rectIntersection}
                    onDragStart={handleDragStart}
                    onDragEnd={handleDragEnd}
                >
                    <div className="space-y-2">
                        <div className="flex items-center justify-between">
                            <label className="text-xs text-gray-600 dark:text-gray-400 mb-2 block">
                                Layout Groups
                            </label>
                            {availableObjects.length > 0 && (
                                <button
                                    onClick={handleAddNewGroup}
                                    className="text-[10px] text-teal-600 hover:text-teal-700 dark:text-teal-400 dark:hover:text-teal-300 flex items-center gap-1"
                                    type="button"
                                    title="Add new row group"
                                >
                                    <Plus size={10} />
                                    New Row
                                </button>
                            )}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded mb-2">
                            Drag objects between rows or to the available pool. Objects in the same row appear horizontally.
                        </div>
                        <SortableContext items={allSortableIds} strategy={horizontalListSortingStrategy}>
                            <div className="space-y-2">
                                {/* Fixed 3-row grid layout */}
                                {FIXED_ROWS.map(rowKey => (
                                    <DroppableRow
                                        key={rowKey}
                                        rowId={rowKey}
                                        rowLabel={ROW_LABELS[rowKey]}
                                        objectIds={currentGroups[rowKey] || []}
                                        allObjects={visibleObjects}
                                    />
                                ))}
                                
                                {/* Available Objects Pool */}
                                <AvailableObjectsPool
                                    objectIds={availableObjects.map(obj => obj.id)}
                                    allObjects={visibleObjects}
                                />
                            </div>
                        </SortableContext>
                        
                        <DragOverlay>
                            {activeId ? (
                                <DraggableObject
                                    id={String(activeId)}
                                    label={objectLabels[String(activeId)] || String(activeId)}
                                />
                            ) : null}
                        </DragOverlay>
                    </div>
                </DndContext>
            )}
            
            {/* Object Visibility Toggles (for conditional objects) */}
            {structure.objects.some(obj => obj.conditional && !obj.required) && (
                <div className="mt-4 space-y-2">
                    <label className="text-xs text-gray-600 dark:text-gray-400 mb-2 block">
                        Object Visibility
                    </label>
                    <div className="space-y-1">
                        {structure.objects.map(obj => {
                            if (obj.required) return null;
                            if (!obj.conditional) return null;
                            
                            return (
                                <div key={obj.id} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
                                    <span className="text-xs text-gray-600 dark:text-gray-400">
                                        {obj.id}
                                    </span>
                                    <span className="text-[10px] text-gray-500 dark:text-gray-500">
                                        Conditional
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};
