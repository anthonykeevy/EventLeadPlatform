/**
 * ResizeHandles - Story 3.5
 * 
 * Visual resize handles displayed around selected components.
 * Different handles have different behaviors:
 * 
 * Handle positions and behaviors:
 *   nw ─── n ─── ne       Corners (nw, ne, se, sw): 2-axis resize (width + vertical behavior)
 *   │             │       E/W edges: Width adjustment
 *   w             e       N edge: Label spacing (labelGap)
 *   │             │       S edge: Textarea height OR help spacing
 *   sw ─── s ─── se
 */

import React, { useCallback, useRef, useState } from 'react';
import { devLogger } from '../../utils/devLogger';

export type HandlePosition = 'nw' | 'n' | 'ne' | 'e' | 'se' | 's' | 'sw' | 'w';

/** Type of action for each handle */
export type HandleAction = 'corner' | 'width' | 'labelGap' | 'heightOrHelpGap';

export type ResizePointerMeta = {
    /** Pointer location in screen coordinates */
    client: { x: number; y: number };
    /** Pointer start position (pointerdown) */
    start: { x: number; y: number };
    /** Raw mouse delta from start (screen px) */
    delta: { x: number; y: number };
    /** Timestamp for ordering/correlation */
    ts: number;
};

interface ResizeHandlesProps {
    /** Is the component selected? Handles only show when selected */
    isSelected: boolean;
    /** Current width of the component (px or %) */
    currentWidth?: string;
    /** Current height of the component (px) - used for textarea */
    currentHeight?: number;
    /** Current component scale (50-200) */
    currentScale?: number;
    /** Current label gap in pixels */
    currentLabelGap?: number;
    /** Current input-help gap in pixels */
    currentInputHelpGap?: number;
    /** Component type - affects S handle behavior */
    componentType?: string;
    /** Component ID for capture/log correlation */
    componentId?: string;
    /** Hide corner handles (NWSE) - for components that don't support proportional scaling */
    hideCornerHandles?: boolean;
    /** Callback when resize starts */
    onResizeStart?: (handle: HandlePosition, meta?: ResizePointerMeta) => void;
    /** Callback during resize with delta values (for live preview) */
    onResize?: (deltaWidth: number, deltaHeight: number, handle: HandlePosition, meta?: ResizePointerMeta) => void;
    /** Callback when width changes (E/W handles) */
    onWidthChange?: (newWidth: number, meta?: ResizePointerMeta) => void;
    /**
     * Callback when a corner resize completes (NW/NE/SE/SW).
     * Deltas are in SCREEN pixels, already signed for the handle direction:
     * - `deltaX`: positive means expand width to the right
     * - `deltaY`: positive means expand height downward
     */
    onCornerResizeEnd?: (handle: HandlePosition, deltaX: number, deltaY: number, meta?: ResizePointerMeta) => void;
    /** Callback when spacing changes (N/S handles) */
    onSpacingChange?: (spacingType: 'labelGap' | 'inputHelpGap', newValue: number) => void;
    /** Callback when height changes (S handle for textarea) */
    onHeightChange?: (newHeight: number) => void;
    /** Callback for vertical resize end (N/S) to allow custom height-first logic */
    onVerticalResizeEnd?: (handle: 'n' | 's', deltaY: number, meta?: ResizePointerMeta) => void;
    /** Current input height in pixels (for N/S two-phase logic; optional if handled upstream) */
    currentInputHeight?: number;
    /** Minimum input height in pixels (optional if handled upstream) */
    minInputHeight?: number;
    /** Maximum input height in pixels (optional if handled upstream) */
    maxInputHeight?: number;
    /** Minimum label gap in pixels (optional if handled upstream) */
    labelGapMin?: number;
    /** Maximum label gap in pixels (optional if handled upstream) */
    labelGapMax?: number;
    /** Minimum input-help gap in pixels (optional if handled upstream) */
    inputHelpGapMin?: number;
    /** Maximum input-help gap in pixels (optional if handled upstream) */
    inputHelpGapMax?: number;
    /** Minimum width in pixels */
    minWidth?: number;
    /** Minimum height in pixels */
    minHeight?: number;
    /** Maximum width in pixels */
    maxWidth?: number;
    /** Maximum height in pixels */
    maxHeight?: number;
}

// Handle configuration with cursor styles and resize behavior
const HANDLE_CONFIG: Record<HandlePosition, {
    cursor: string;
    position: React.CSSProperties;
    resizeX: -1 | 0 | 1; // -1 = left edge, 0 = no horizontal, 1 = right edge
    resizeY: -1 | 0 | 1; // -1 = top edge, 0 = no vertical, 1 = bottom edge
    action: HandleAction;
}> = {
    nw: { cursor: 'nwse-resize', position: { top: -4, left: -4 }, resizeX: -1, resizeY: -1, action: 'corner' },
    n:  { cursor: 'ns-resize',   position: { top: -4, left: '50%', transform: 'translateX(-50%)' }, resizeX: 0, resizeY: -1, action: 'labelGap' },
    ne: { cursor: 'nesw-resize', position: { top: -4, right: -4 }, resizeX: 1, resizeY: -1, action: 'corner' },
    e:  { cursor: 'ew-resize',   position: { top: '50%', right: -4, transform: 'translateY(-50%)' }, resizeX: 1, resizeY: 0, action: 'width' },
    se: { cursor: 'nwse-resize', position: { bottom: -4, right: -4 }, resizeX: 1, resizeY: 1, action: 'corner' },
    s:  { cursor: 'ns-resize',   position: { bottom: -4, left: '50%', transform: 'translateX(-50%)' }, resizeX: 0, resizeY: 1, action: 'heightOrHelpGap' },
    sw: { cursor: 'nesw-resize', position: { bottom: -4, left: -4 }, resizeX: -1, resizeY: 1, action: 'corner' },
    w:  { cursor: 'ew-resize',   position: { top: '50%', left: -4, transform: 'translateY(-50%)' }, resizeX: -1, resizeY: 0, action: 'width' },
};

// Corner handles for 2-axis resize
const CORNER_HANDLES: HandlePosition[] = ['nw', 'ne', 'se', 'sw'];

/**
 * Get tooltip text for handle based on its action
 */
const getHandleTooltip = (position: HandlePosition, componentType?: string): string => {
    const config = HANDLE_CONFIG[position];
    switch (config.action) {
        case 'corner':
            return `Corner resize (${position.toUpperCase()})`;
        case 'width':
            return `Adjust width (${position.toUpperCase()})`;
        case 'labelGap':
            return 'Adjust label spacing';
        case 'heightOrHelpGap':
            return componentType === 'textarea' ? 'Adjust height' : 'Adjust help text spacing';
        default:
            return `Drag to resize (${position.toUpperCase()})`;
    }
};

/**
 * Individual resize handle component
 */
const Handle: React.FC<{
    position: HandlePosition;
    onMouseDown: (e: React.MouseEvent, position: HandlePosition) => void;
    isCorner: boolean;
    componentType?: string;
    componentId?: string;
}> = ({ position, onMouseDown, isCorner, componentType, componentId }) => {
    const config = HANDLE_CONFIG[position];
    
    // Different colors for different actions
    const getHandleColor = () => {
        switch (config.action) {
            case 'corner':
                return '#3B82F6'; // blue-500 for corners
            case 'width':
                return '#10B981'; // emerald-500 for width
            case 'labelGap':
            case 'heightOrHelpGap':
                return '#8B5CF6'; // violet-500 for spacing
            default:
                return '#3B82F6';
        }
    };
    
    // Handle pointer/mouse down - must stop propagation to prevent dnd-kit drag
    const handlePointerDown = (e: React.PointerEvent) => {
        // Stop propagation for both pointer and mouse events to prevent drag
        e.stopPropagation();
        e.preventDefault();
        if (typeof (e.currentTarget as HTMLElement).setPointerCapture === 'function') {
            try {
                (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
            } catch {
                // Ignore capture failures (e.g. synthetic events / browser quirks)
            }
        }
        // Convert to mouse event-like object for the handler
        onMouseDown(e as unknown as React.MouseEvent, position);
    };
    
    return (
        <div
            onPointerDown={handlePointerDown}
            onMouseDown={(e) => {
                // Also stop mouse events for browsers that fire both
                e.stopPropagation();
                e.preventDefault();
            }}
            style={{
                position: 'absolute',
                ...config.position,
                width: isCorner ? 8 : 6,
                height: isCorner ? 8 : 6,
                backgroundColor: getHandleColor(),
                border: '1px solid white',
                borderRadius: isCorner ? 2 : 1,
                cursor: config.cursor,
                zIndex: 50,
                boxShadow: '0 1px 2px rgba(0,0,0,0.2)',
                // Ensure handles capture pointer events (override parent's pointerEvents: none)
                pointerEvents: 'auto',
                touchAction: 'none',
            }}
            title={getHandleTooltip(position, componentType)}
            data-resize-handle={position}
            data-resize-action={config.action}
            data-resize-component-id={componentId}
        />
    );
};

export const ResizeHandles: React.FC<ResizeHandlesProps> = ({
    isSelected,
    currentWidth,
    currentHeight,
    currentScale = 100,
    currentLabelGap = 8,
    currentInputHelpGap = 8,
    componentType,
    componentId,
    hideCornerHandles = false,
    onResizeStart,
    onResize,
    onWidthChange,
    onCornerResizeEnd,
    onSpacingChange,
    onHeightChange,
    onVerticalResizeEnd,
    minWidth = 50,
    minHeight = 30,
    maxWidth = 2000,
    maxHeight = 1000,
}) => {
    const [isResizing, setIsResizing] = useState(false);
    const startPosRef = useRef({ x: 0, y: 0 });
    const startSizeRef = useRef({ width: 0, height: 0, scale: 100, labelGap: 8, inputHelpGap: 8 });
    const activeHandleRef = useRef<HandlePosition | null>(null);
    const lastPointerRef = useRef<{ x: number; y: number } | null>(null);
    
    // Store callbacks in refs so event listeners always have current values
    const onResizeRef = useRef(onResize);
    const onWidthChangeRef = useRef(onWidthChange);
    const onCornerResizeEndRef = useRef(onCornerResizeEnd);
    const onSpacingChangeRef = useRef(onSpacingChange);
    const onHeightChangeRef = useRef(onHeightChange);
    const onVerticalResizeEndRef = useRef(onVerticalResizeEnd);
    
    // Update refs when props change
    onResizeRef.current = onResize;
    onWidthChangeRef.current = onWidthChange;
    onCornerResizeEndRef.current = onCornerResizeEnd;
    onSpacingChangeRef.current = onSpacingChange;
    onHeightChangeRef.current = onHeightChange;
    onVerticalResizeEndRef.current = onVerticalResizeEnd;
    
    // Parse current width to pixels (handle percentage or px)
    const parseWidth = useCallback((): number => {
        if (!currentWidth) return 300; // default
        if (currentWidth.endsWith('px')) {
            return parseInt(currentWidth, 10);
        }
        if (currentWidth.endsWith('%')) {
            // For percentage, we'd need parent width - fallback to reasonable default
            return 300;
        }
        return 300;
    }, [currentWidth]);

    // Define event handlers that use refs for current callback values
    // Use PointerEvent for cross-browser support and to match dnd-kit's event system
    const handlePointerMove = useCallback((e: PointerEvent) => {
        if (!activeHandleRef.current) return;
        
        const config = HANDLE_CONFIG[activeHandleRef.current];
        const deltaX = e.clientX - startPosRef.current.x;
        const deltaY = e.clientY - startPosRef.current.y;
        lastPointerRef.current = { x: e.clientX, y: e.clientY };
        const meta: ResizePointerMeta = {
            client: { x: e.clientX, y: e.clientY },
            start: { x: startPosRef.current.x, y: startPosRef.current.y },
            delta: { x: deltaX, y: deltaY },
            ts: Date.now(),
        };
        
        devLogger.debug('resize.pointer.move', {
            componentId,
            handle: activeHandleRef.current,
            action: config.action,
            client: { x: e.clientX, y: e.clientY },
            start: { x: startPosRef.current.x, y: startPosRef.current.y },
            delta: { x: deltaX, y: deltaY },
        });
        
        // Calculate new dimensions based on handle position
        let newWidth = startSizeRef.current.width;
        let newHeight = startSizeRef.current.height;
        
        // Call generic resize callback for live preview
        if (config.action === 'labelGap' || config.action === 'heightOrHelpGap') {
            // For vertical handles, pass raw normalized deltaY so downstream can allocate height vs spacing
            const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
            onResizeRef.current?.(0, heightDelta, activeHandleRef.current, meta);
        } else if (config.action === 'width') {
            // For E/W handles, pass raw screen pixel delta - SortableComponent will convert to base pixels
            // CRITICAL: Do NOT mix screen pixels (deltaX) with base pixels (startSizeRef.current.width)
            // Pass raw deltaX so SortableComponent can properly convert accounting for canvas zoom and component scale
            const widthDelta = config.resizeX === -1 ? -deltaX : deltaX;
            devLogger.debug('resize.pointer.delta', {
                handle: activeHandleRef.current,
                resizeX: config.resizeX,
                deltaX,
                widthDelta,
            });
            const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
            onResizeRef.current?.(widthDelta, heightDelta, activeHandleRef.current, meta);
        } else {
            // Corner handles: pass signed raw screen deltas (SortableComponent converts to base px)
            const widthDelta = config.resizeX !== 0 ? (config.resizeX === -1 ? -deltaX : deltaX) : 0;
            const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
            onResizeRef.current?.(widthDelta, heightDelta, activeHandleRef.current, meta);
        }
    }, [minWidth, maxWidth, minHeight, maxHeight]);

    const handlePointerUp = useCallback((e: PointerEvent) => {
        if (!activeHandleRef.current) return;
        
        const handle = activeHandleRef.current;
        const config = HANDLE_CONFIG[handle];
        const deltaX = e.clientX - startPosRef.current.x;
        const deltaY = e.clientY - startPosRef.current.y;
        const meta: ResizePointerMeta = {
            client: { x: e.clientX, y: e.clientY },
            start: { x: startPosRef.current.x, y: startPosRef.current.y },
            delta: { x: deltaX, y: deltaY },
            ts: Date.now(),
        };
        devLogger.info('resize.pointer.up', {
            componentId,
            handle,
            action: config.action,
            client: { x: e.clientX, y: e.clientY },
            start: { x: startPosRef.current.x, y: startPosRef.current.y },
            delta: { x: deltaX, y: deltaY },
            startSize: { ...startSizeRef.current },
            componentType,
        });
        
        // Calculate final values based on handle action
        switch (config.action) {
            case 'corner': {
                const widthDelta = config.resizeX !== 0 ? (config.resizeX === -1 ? -deltaX : deltaX) : 0;
                const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
                if (Math.abs(widthDelta) < 1 && Math.abs(heightDelta) < 1) {
                    devLogger.info('resize.pointer.up.noop', {
                        handle,
                        action: config.action,
                        delta: { x: deltaX, y: deltaY },
                        reason: 'no-drag corner commit suppressed',
                    });
                    break;
                }
                onCornerResizeEndRef.current?.(handle, widthDelta, heightDelta, meta);
                break;
            }
            
            case 'width': {
                // E/W handles: update width
                // widthDelta is in SCREEN pixels, but we store BASE width
                // Need to convert screen delta to base delta when scale != 100%
                const widthDelta = config.resizeX === -1 ? -deltaX : deltaX;
                if (Math.abs(widthDelta) < 1 && Math.abs(deltaY) < 1) {
                    devLogger.info('resize.pointer.up.noop', {
                        handle,
                        action: config.action,
                        delta: { x: deltaX, y: deltaY },
                        reason: 'no-drag width commit suppressed',
                    });
                    break;
                }
                const scaleFactor = startSizeRef.current.scale / 100;
                const baseWidthDelta = scaleFactor !== 0 ? widthDelta / scaleFactor : widthDelta;
                const newWidth = Math.max(minWidth, Math.min(maxWidth, startSizeRef.current.width + baseWidthDelta));
                onWidthChangeRef.current?.(Math.round(newWidth), meta);
                break;
            }
            
            case 'labelGap': {
                // N handle: delegate to vertical resize end for height-first logic with normalized delta
                // Convert raw mouse deltaY into height delta (top handle inverts sign)
                const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
                onVerticalResizeEndRef.current?.('n', heightDelta, meta);
                break;
            }
            
            case 'heightOrHelpGap': {
                // S handle: delegate with normalized delta
                const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
                onVerticalResizeEndRef.current?.('s', heightDelta, meta);
                break;
            }
        }
        
        // Cleanup
        setIsResizing(false);
        activeHandleRef.current = null;
        lastPointerRef.current = null;
        document.removeEventListener('pointermove', handlePointerMove);
        document.removeEventListener('pointerup', handlePointerUp);
    }, [minWidth, maxWidth, minHeight, maxHeight, handlePointerMove]);

    const handleMouseDown = useCallback((e: React.MouseEvent, position: HandlePosition) => {
        e.preventDefault();
        e.stopPropagation();
        
        setIsResizing(true);
        activeHandleRef.current = position;
        startPosRef.current = { x: e.clientX, y: e.clientY };
        lastPointerRef.current = { x: e.clientX, y: e.clientY };
        startSizeRef.current = { 
            width: parseWidth(), 
            height: currentHeight || 100,
            scale: currentScale,
            labelGap: currentLabelGap,
            inputHelpGap: currentInputHelpGap,
        };
        devLogger.info('resize.pointer.down', {
            componentId,
            handle: position,
            action: HANDLE_CONFIG[position]?.action,
            client: { x: e.clientX, y: e.clientY },
            startSize: { ...startSizeRef.current },
            componentType,
        });
        
        onResizeStart?.(position, {
            client: { x: e.clientX, y: e.clientY },
            start: { x: e.clientX, y: e.clientY },
            delta: { x: 0, y: 0 },
            ts: Date.now(),
        });
        
        // Add global pointer listeners (works with both mouse and touch)
        document.addEventListener('pointermove', handlePointerMove);
        document.addEventListener('pointerup', handlePointerUp);
    }, [parseWidth, currentHeight, currentScale, currentLabelGap, currentInputHelpGap, onResizeStart, handlePointerMove, handlePointerUp]);

    // Don't render if not selected
    if (!isSelected) return null;

    // Determine which edge handles to show based on available callbacks
    // E/W handles require onWidthChange
    // N handle requires onSpacingChange or onVerticalResizeEnd (for labelGap)
    // S handle requires onHeightChange or onSpacingChange or onVerticalResizeEnd
    const showEWHandles = onWidthChange !== undefined;
    const showNHandle = onSpacingChange !== undefined || onVerticalResizeEnd !== undefined;
    const showSHandle = onHeightChange !== undefined || onSpacingChange !== undefined || onVerticalResizeEnd !== undefined;
    
    // Build the list of edge handles to show
    const edgeHandles: HandlePosition[] = [];
    if (showNHandle) edgeHandles.push('n');
    if (showEWHandles) {
        edgeHandles.push('e');
        edgeHandles.push('w');
    }
    if (showSHandle) edgeHandles.push('s');

    return (
        <>
            {/* Corner handles (2-axis resize) - hidden if hideCornerHandles is true */}
            {!hideCornerHandles && CORNER_HANDLES.map((pos) => (
                <Handle
                    key={pos}
                    position={pos}
                    onMouseDown={handleMouseDown}
                    isCorner={true}
                    componentType={componentType}
                    componentId={componentId}
                />
            ))}
            
            {/* Edge handles (for width/spacing) - shown based on available callbacks */}
            {edgeHandles.map((pos) => (
                <Handle
                    key={pos}
                    position={pos}
                    onMouseDown={handleMouseDown}
                    isCorner={false}
                    componentType={componentType}
                    componentId={componentId}
                />
            ))}
            
            {/* Resize overlay during drag */}
            {isResizing && (
                <div 
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        zIndex: 9999,
                        cursor: activeHandleRef.current 
                            ? HANDLE_CONFIG[activeHandleRef.current].cursor 
                            : 'default',
                    }}
                />
            )}
        </>
    );
};

export default ResizeHandles;
