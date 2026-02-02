/**
 * GridLayoutEditor Component
 * 
 * Visual grid preview for the Grid Layout system.
 * Displays a grid structure with configurable rows, columns, and gaps.
 * Supports drag-and-drop object assignment to cells.
 * 
 * @story 3.10 - Grid Layout System
 * @task T03 - Basic Grid Editor UI
 * @task T04 - Object Drag-and-Drop
 */

import React from 'react';
import { useDroppable } from '@dnd-kit/core';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical, X } from 'lucide-react';
import type { GridLayoutConfig, ComponentStructure } from '../../types/builder.types';
import { 
    generateGridStyles, 
    cellKey, 
    getCellOccupant, 
    getMergeGroupForCell,
    getObjectGridArea 
} from '../../utils/gridLayoutUtils';

interface GridLayoutEditorProps {
    /** Current grid configuration */
    config: GridLayoutConfig;
    /** Component structure (for object labels) */
    structure?: ComponentStructure;
    /** Whether to show cell coordinates (for debugging) */
    showCoordinates?: boolean;
    /** Maximum height for the preview container */
    maxHeight?: number;
    /** Selected cells (for selection highlighting) */
    selectedCells?: Set<string>;
    /** Callback when a cell is clicked */
    onCellClick?: (cellKey: string, event: React.MouseEvent) => void;
    /** Callback to remove an object from a cell */
    onRemoveObject?: (cellKey: string) => void;
    /** Callback to unmerge a merged cell group */
    onUnmerge?: (mergeId: string) => void;
}

/**
 * Individual grid cell component with droppable support
 */
interface GridCellProps {
    row: number;
    col: number;
    cellKey: string;
    objectId: string | null;
    objectLabel?: string;
    showCoordinates?: boolean;
    isSelected?: boolean;
    isMerged?: boolean;
    mergeGroupId?: string;
    onRemove?: () => void;
    onClick?: (event: React.MouseEvent) => void;
    onUnmerge?: (mergeId: string) => void;
}

/**
 * Draggable object inside a grid cell
 */
interface CellObjectProps {
    id: string;
    label: string;
    onRemove?: () => void;
}

const CellObject: React.FC<CellObjectProps> = ({ id, label, onRemove }) => {
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
    };

    return (
        <div
            ref={setNodeRef}
            style={style}
            className="flex items-center gap-1 px-1.5 py-1 rounded bg-white dark:bg-gray-700 border border-indigo-300 dark:border-indigo-600 max-w-full"
        >
            <div {...attributes} {...listeners} className="flex items-center gap-1 flex-1 cursor-grab min-w-0">
                <GripVertical size={10} className="text-gray-400 flex-shrink-0" />
                <span className="text-[9px] font-medium text-indigo-700 dark:text-indigo-300 truncate">{label}</span>
            </div>
            {onRemove && (
                <button
                    type="button"
                    onClick={(e) => {
                        e.stopPropagation();
                        onRemove();
                    }}
                    className="p-0.5 rounded hover:bg-red-100 dark:hover:bg-red-900/30 text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
                    title="Remove from cell"
                >
                    <X size={10} />
                </button>
            )}
        </div>
    );
};

const GridCell: React.FC<GridCellProps> = ({ 
    row, 
    col, 
    cellKey: key, 
    objectId, 
    objectLabel,
    showCoordinates,
    isSelected,
    isMerged,
    mergeGroupId,
    onRemove,
    onClick,
    onUnmerge
}) => {
    const { setNodeRef, isOver } = useDroppable({
        id: `cell-${key}`,
    });
    
    const isEmpty = !objectId;
    
    return (
        <div
            ref={setNodeRef}
            onClick={onClick}
            className={`
                border rounded transition-colors min-h-[40px] flex items-center justify-center p-1 relative
                ${isSelected 
                    ? 'border-solid border-blue-500 bg-blue-100 dark:bg-blue-900/40 ring-2 ring-blue-300 dark:ring-blue-700'
                    : isEmpty 
                        ? isOver
                            ? 'border-solid border-indigo-400 bg-indigo-50 dark:bg-indigo-900/30'
                            : 'border-dashed border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50' 
                        : isOver
                            ? 'border-solid border-indigo-400 bg-indigo-50 dark:bg-indigo-900/30'
                            : 'border-solid border-indigo-300 dark:border-indigo-600 bg-indigo-50/50 dark:bg-indigo-900/20'
                }
                ${isMerged ? 'border-2 border-teal-500 dark:border-teal-400' : ''}
                ${onClick ? 'cursor-pointer' : ''}
            `}
            title={objectId ? `Object: ${objectId}${isMerged ? ' (Merged)' : ''}` : `Empty cell (${row}, ${col}) - Drop here`}
        >
            {isMerged && (
                <div className="absolute top-0 right-0 bg-teal-500 dark:bg-teal-400 text-white text-[8px] px-1 rounded-bl">
                    ⧉
                </div>
            )}
            {objectId ? (
                <CellObject 
                    id={objectId} 
                    label={objectLabel || objectId} 
                    onRemove={onRemove}
                />
            ) : showCoordinates ? (
                <span className={`text-[8px] ${isOver ? 'text-indigo-500' : 'text-gray-400 dark:text-gray-500'}`}>
                    {isOver ? 'Drop here' : `${row},${col}`}
                </span>
            ) : isOver ? (
                <span className="text-[8px] text-indigo-500">Drop</span>
            ) : null}
            {isMerged && mergeGroupId && onUnmerge && (
                <button
                    type="button"
                    onClick={(e) => {
                        e.stopPropagation();
                        onUnmerge(mergeGroupId);
                    }}
                    className="absolute bottom-0 left-0 right-0 text-[8px] bg-teal-600 dark:bg-teal-500 text-white hover:bg-teal-700 dark:hover:bg-teal-600 rounded-b px-1 py-0.5"
                    title="Unmerge cells"
                >
                    Unmerge
                </button>
            )}
        </div>
    );
};

/**
 * GridLayoutEditor - Visual preview of grid structure with drag-and-drop support
 * 
 * Displays:
 * - Grid cells in a rows × columns layout (droppable targets)
 * - Visual gap representation
 * - Object assignments with draggable objects
 * - Empty cell indicators with drop zone highlighting
 */
export const GridLayoutEditor: React.FC<GridLayoutEditorProps> = ({
    config,
    structure,
    showCoordinates = false,
    maxHeight = 250,
    selectedCells = new Set(),
    onCellClick,
    onRemoveObject,
    onUnmerge,
}) => {
    // Generate CSS grid styles from config
    const gridStyles = generateGridStyles(config);
    const previewGridStyles: React.CSSProperties = {
        ...gridStyles,
        // Keep the preview grid cells stretched so merged cells render as a single block.
        display: 'grid',
        alignItems: 'stretch',
        justifyItems: 'stretch',
    };
    
    // Build object labels map from structure
    const objectLabels: Record<string, string> = {};
    if (structure) {
        structure.objects.forEach(obj => {
            objectLabels[obj.id] = obj.label || obj.id;
        });
    }
    
    // Track which cells are part of merged groups (to skip rendering)
    const mergedCellKeys = new Set<string>();
    const mergeGroupMap = new Map<string, { mergeId: string; group: { cells: string[]; objectId: string } }>();
    
    if (config.mergedCells) {
        for (const [mergeId, group] of Object.entries(config.mergedCells)) {
            for (const cellKey of group.cells) {
                mergedCellKeys.add(cellKey);
                mergeGroupMap.set(cellKey, { mergeId, group });
            }
        }
    }
    
    // Build the grid cells
    const cells: React.ReactNode[] = [];
    for (let row = 0; row < config.rows; row++) {
        for (let col = 0; col < config.columns; col++) {
            const key = cellKey(row, col);
            const mergeInfo = getMergeGroupForCell(key, config);
            
            // Skip rendering cells that are part of a merge (except the first cell)
            if (mergeInfo && mergeInfo.group.cells[0] !== key) {
                continue;
            }
            
            // For merged cells, get object from merge group, otherwise from cell assignments
            let objectId: string | null = null;
            if (mergeInfo && mergeInfo.group.objectId) {
                objectId = mergeInfo.group.objectId;
            } else {
                objectId = getCellOccupant(row, col, config);
            }
            
            // Calculate grid position and span
            let gridRowStart: number;
            let gridRowEnd: number;
            let gridColStart: number;
            let gridColEnd: number;
            
            if (mergeInfo) {
                // Merged cell: calculate span from merged cells
                const positions = mergeInfo.group.cells.map(k => {
                    const parts = k.split('-');
                    return { row: parseInt(parts[0], 10), col: parseInt(parts[1], 10) };
                });
                const minRow = Math.min(...positions.map(p => p.row));
                const maxRow = Math.max(...positions.map(p => p.row));
                const minCol = Math.min(...positions.map(p => p.col));
                const maxCol = Math.max(...positions.map(p => p.col));
                
                // Convert to CSS grid lines (accounting for gap tracks)
                gridRowStart = minRow * 2 + 1;
                gridRowEnd = maxRow * 2 + 2;
                gridColStart = minCol * 2 + 1;
                gridColEnd = maxCol * 2 + 2;
            } else {
                // Regular cell
                gridRowStart = row * 2 + 1;
                gridRowEnd = row * 2 + 2;
                gridColStart = col * 2 + 1;
                gridColEnd = col * 2 + 2;
            }
            
            const isSelected = selectedCells.has(key);
            const isMerged = mergeInfo !== null;
            
            cells.push(
                <div
                    key={key}
                    style={{
                        gridRow: `${gridRowStart} / ${gridRowEnd}`,
                        gridColumn: `${gridColStart} / ${gridColEnd}`,
                    }}
                >
                    <GridCell
                        row={row}
                        col={col}
                        cellKey={key}
                        objectId={objectId}
                        objectLabel={objectId ? objectLabels[objectId] : undefined}
                        showCoordinates={showCoordinates}
                        isSelected={isSelected}
                        isMerged={isMerged}
                        mergeGroupId={mergeInfo?.mergeId}
                        onRemove={objectId && onRemoveObject ? () => onRemoveObject(key) : undefined}
                        onClick={onCellClick ? (e) => onCellClick(key, e) : undefined}
                        onUnmerge={onUnmerge}
                    />
                </div>
            );
        }
    }
    
    return (
        <div className="grid-layout-editor">
            {/* Grid Preview Container */}
            <div 
                className="border border-gray-200 dark:border-gray-700 rounded-lg p-3 bg-white dark:bg-gray-900 overflow-auto"
                style={{ maxHeight }}
            >
                {/* Row/Column Labels */}
                <div className="flex justify-between items-center mb-2 text-[10px] text-gray-400 dark:text-gray-500">
                    <span>{config.rows} row{config.rows !== 1 ? 's' : ''} × {config.columns} col{config.columns !== 1 ? 's' : ''}</span>
                    <span>Gap: {config.rowGap}px / {config.columnGap}px</span>
                </div>
                
                {/* The Grid */}
                <div
                    style={{
                        ...previewGridStyles,
                        minWidth: '100%',
                    }}
                >
                    {cells}
                </div>
            </div>
            
            {/* Tips */}
            <div className="mt-2 text-[10px] text-gray-400 dark:text-gray-500">
                💡 Drag objects from the pool above to grid cells. Click × to remove.
            </div>
        </div>
    );
};

export default GridLayoutEditor;
