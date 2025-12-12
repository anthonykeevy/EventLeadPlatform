/**
 * ResizeHandles - Story 3.5
 * 
 * Visual resize handles displayed around selected components.
 * Different handles have different behaviors:
 * 
 * Handle positions and behaviors:
 *   nw ─── n ─── ne       Corners (nw, ne, se, sw): Proportional scale
 *   │             │       E/W edges: Width adjustment
 *   w             e       N edge: Label spacing (labelGap)
 *   │             │       S edge: Textarea height OR help spacing
 *   sw ─── s ─── se
 */

import React, { useCallback, useRef, useState } from 'react';

export type HandlePosition = 'nw' | 'n' | 'ne' | 'e' | 'se' | 's' | 'sw' | 'w';

/** Type of action for each handle */
export type HandleAction = 'scale' | 'width' | 'labelGap' | 'heightOrHelpGap';

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
    /** Callback when resize starts */
    onResizeStart?: () => void;
    /** Callback during resize with delta values (for live preview) */
    onResize?: (deltaWidth: number, deltaHeight: number, handle: HandlePosition) => void;
    /** Callback when width changes (E/W handles) */
    onWidthChange?: (newWidth: number) => void;
    /** Callback when scale changes (corner handles) */
    onScaleChange?: (newScale: number) => void;
    /** Callback when spacing changes (N/S handles) */
    onSpacingChange?: (spacingType: 'labelGap' | 'inputHelpGap', newValue: number) => void;
    /** Callback when height changes (S handle for textarea) */
    onHeightChange?: (newHeight: number) => void;
    /** Callback for vertical resize end (N/S) to allow custom height-first logic */
    onVerticalResizeEnd?: (handle: 'n' | 's', deltaY: number) => void;
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
    nw: { cursor: 'nwse-resize', position: { top: -4, left: -4 }, resizeX: -1, resizeY: -1, action: 'scale' },
    n:  { cursor: 'ns-resize',   position: { top: -4, left: '50%', transform: 'translateX(-50%)' }, resizeX: 0, resizeY: -1, action: 'labelGap' },
    ne: { cursor: 'nesw-resize', position: { top: -4, right: -4 }, resizeX: 1, resizeY: -1, action: 'scale' },
    e:  { cursor: 'ew-resize',   position: { top: '50%', right: -4, transform: 'translateY(-50%)' }, resizeX: 1, resizeY: 0, action: 'width' },
    se: { cursor: 'nwse-resize', position: { bottom: -4, right: -4 }, resizeX: 1, resizeY: 1, action: 'scale' },
    s:  { cursor: 'ns-resize',   position: { bottom: -4, left: '50%', transform: 'translateX(-50%)' }, resizeX: 0, resizeY: 1, action: 'heightOrHelpGap' },
    sw: { cursor: 'nesw-resize', position: { bottom: -4, left: -4 }, resizeX: -1, resizeY: 1, action: 'scale' },
    w:  { cursor: 'ew-resize',   position: { top: '50%', left: -4, transform: 'translateY(-50%)' }, resizeX: -1, resizeY: 0, action: 'width' },
};

// Corner handles for proportional scale
const CORNER_HANDLES: HandlePosition[] = ['nw', 'ne', 'se', 'sw'];

/**
 * Get tooltip text for handle based on its action
 */
const getHandleTooltip = (position: HandlePosition, componentType?: string): string => {
    const config = HANDLE_CONFIG[position];
    switch (config.action) {
        case 'scale':
            return `Proportional scale (${position.toUpperCase()})`;
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
}> = ({ position, onMouseDown, isCorner, componentType }) => {
    const config = HANDLE_CONFIG[position];
    
    // Different colors for different actions
    const getHandleColor = () => {
        switch (config.action) {
            case 'scale':
                return '#3B82F6'; // blue-500 for scale
            case 'width':
                return '#10B981'; // emerald-500 for width
            case 'labelGap':
            case 'heightOrHelpGap':
                return '#8B5CF6'; // violet-500 for spacing
            default:
                return '#3B82F6';
        }
    };
    
    return (
        <div
            onMouseDown={(e) => onMouseDown(e, position)}
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
            }}
            title={getHandleTooltip(position, componentType)}
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
    onResizeStart,
    onResize,
    onWidthChange,
    onScaleChange,
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
    
    // Store callbacks in refs so event listeners always have current values
    const onResizeRef = useRef(onResize);
    const onWidthChangeRef = useRef(onWidthChange);
    const onScaleChangeRef = useRef(onScaleChange);
    const onSpacingChangeRef = useRef(onSpacingChange);
    const onHeightChangeRef = useRef(onHeightChange);
    const onVerticalResizeEndRef = useRef(onVerticalResizeEnd);
    
    // Update refs when props change
    onResizeRef.current = onResize;
    onWidthChangeRef.current = onWidthChange;
    onScaleChangeRef.current = onScaleChange;
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
    const handleMouseMove = useCallback((e: MouseEvent) => {
        if (!activeHandleRef.current) return;
        
        const config = HANDLE_CONFIG[activeHandleRef.current];
        const deltaX = e.clientX - startPosRef.current.x;
        const deltaY = e.clientY - startPosRef.current.y;
        
        // Calculate new dimensions based on handle position
        let newWidth = startSizeRef.current.width;
        let newHeight = startSizeRef.current.height;
        
        if (config.resizeX !== 0) {
            const widthDelta = config.resizeX === -1 ? -deltaX : deltaX;
            newWidth = Math.max(minWidth, Math.min(maxWidth, startSizeRef.current.width + widthDelta));
        }
        
        if (config.resizeY !== 0) {
            const heightDelta = config.resizeY === -1 ? -deltaY : deltaY;
            newHeight = Math.max(minHeight, Math.min(maxHeight, startSizeRef.current.height + heightDelta));
        }
        
        // Call generic resize callback for live preview
        if (config.action === 'labelGap' || config.action === 'heightOrHelpGap') {
            // For vertical handles, pass raw normalized deltaY so downstream can allocate height vs spacing
            const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
            onResizeRef.current?.(0, heightDelta, activeHandleRef.current);
        } else {
            onResizeRef.current?.(
                newWidth - startSizeRef.current.width,
                newHeight - startSizeRef.current.height,
                activeHandleRef.current
            );
        }
    }, [minWidth, maxWidth, minHeight, maxHeight]);

    const handleMouseUp = useCallback((e: MouseEvent) => {
        if (!activeHandleRef.current) return;
        
        const handle = activeHandleRef.current;
        const config = HANDLE_CONFIG[handle];
        const deltaX = e.clientX - startPosRef.current.x;
        const deltaY = e.clientY - startPosRef.current.y;
        
        // Calculate final values based on handle action
        switch (config.action) {
            case 'scale': {
                // Corner handles: calculate scale factor from width change
                const widthDelta = config.resizeX === -1 ? -deltaX : deltaX;
                const newWidth = Math.max(minWidth, Math.min(maxWidth, startSizeRef.current.width + widthDelta));
                const scaleFactor = (newWidth / startSizeRef.current.width) * startSizeRef.current.scale;
                // Clamp scale between 50% and 200%
                const clampedScale = Math.max(50, Math.min(200, Math.round(scaleFactor)));
                onScaleChangeRef.current?.(clampedScale);
                break;
            }
            
            case 'width': {
                // E/W handles: just update width
                const widthDelta = config.resizeX === -1 ? -deltaX : deltaX;
                const newWidth = Math.max(minWidth, Math.min(maxWidth, startSizeRef.current.width + widthDelta));
                onWidthChangeRef.current?.(Math.round(newWidth));
                break;
            }
            
            case 'labelGap': {
                // N handle: delegate to vertical resize end for height-first logic with normalized delta
                // Convert raw mouse deltaY into height delta (top handle inverts sign)
                const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
                onVerticalResizeEndRef.current?.('n', heightDelta);
                break;
            }
            
            case 'heightOrHelpGap': {
                // S handle: delegate with normalized delta
                const heightDelta = config.resizeY !== 0 ? (config.resizeY === -1 ? -deltaY : deltaY) : 0;
                onVerticalResizeEndRef.current?.('s', heightDelta);
                break;
            }
        }
        
        // Cleanup
        setIsResizing(false);
        activeHandleRef.current = null;
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
    }, [minWidth, maxWidth, minHeight, maxHeight, componentType, handleMouseMove]);

    const handleMouseDown = useCallback((e: React.MouseEvent, position: HandlePosition) => {
        e.preventDefault();
        e.stopPropagation();
        
        setIsResizing(true);
        activeHandleRef.current = position;
        startPosRef.current = { x: e.clientX, y: e.clientY };
        startSizeRef.current = { 
            width: parseWidth(), 
            height: currentHeight || 100,
            scale: currentScale,
            labelGap: currentLabelGap,
            inputHelpGap: currentInputHelpGap,
        };
        
        onResizeStart?.();
        
        // Add global mouse listeners
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
    }, [parseWidth, currentHeight, currentScale, currentLabelGap, currentInputHelpGap, onResizeStart, handleMouseMove, handleMouseUp]);

    // Don't render if not selected
    if (!isSelected) return null;

    const edgeHandles: HandlePosition[] = ['n', 'e', 's', 'w'];

    return (
        <>
            {/* Corner handles (for proportional scale) */}
            {CORNER_HANDLES.map((pos) => (
                <Handle
                    key={pos}
                    position={pos}
                    onMouseDown={handleMouseDown}
                    isCorner={true}
                    componentType={componentType}
                />
            ))}
            
            {/* Edge handles (for width/spacing) */}
            {edgeHandles.map((pos) => (
                <Handle
                    key={pos}
                    position={pos}
                    onMouseDown={handleMouseDown}
                    isCorner={false}
                    componentType={componentType}
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
