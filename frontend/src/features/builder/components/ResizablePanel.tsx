/**
 * ResizablePanel.tsx - Story 3.5
 * A panel component that can be resized by dragging its edge
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';

interface ResizablePanelProps {
    children: React.ReactNode;
    /** Which side has the resize handle */
    resizeFrom: 'left' | 'right';
    /** Default width in pixels */
    defaultWidth: number;
    /** Minimum width in pixels */
    minWidth?: number;
    /** Maximum width in pixels */
    maxWidth?: number;
    /** Storage key for persisting width */
    storageKey?: string;
    /** Additional className for the panel */
    className?: string;
    /** Called when width changes */
    onWidthChange?: (width: number) => void;
}

export const ResizablePanel: React.FC<ResizablePanelProps> = ({
    children,
    resizeFrom,
    defaultWidth,
    minWidth = 240,
    maxWidth = 480,
    storageKey,
    className = '',
    onWidthChange,
}) => {
    // Initialize width from localStorage or default
    const [width, setWidth] = useState(() => {
        if (storageKey) {
            const stored = localStorage.getItem(storageKey);
            if (stored) {
                const parsed = parseInt(stored, 10);
                if (!isNaN(parsed) && parsed >= minWidth && parsed <= maxWidth) {
                    return parsed;
                }
            }
        }
        return defaultWidth;
    });

    const [isResizing, setIsResizing] = useState(false);
    const panelRef = useRef<HTMLDivElement>(null);
    const startXRef = useRef(0);
    const startWidthRef = useRef(0);

    // Handle mouse down on resize handle
    const handleMouseDown = useCallback((e: React.MouseEvent) => {
        e.preventDefault();
        setIsResizing(true);
        startXRef.current = e.clientX;
        startWidthRef.current = width;
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
    }, [width]);

    // Handle mouse move while resizing
    useEffect(() => {
        if (!isResizing) return;

        const handleMouseMove = (e: MouseEvent) => {
            const delta = resizeFrom === 'right' 
                ? e.clientX - startXRef.current
                : startXRef.current - e.clientX;
            
            const newWidth = Math.min(maxWidth, Math.max(minWidth, startWidthRef.current + delta));
            setWidth(newWidth);
            onWidthChange?.(newWidth);
        };

        const handleMouseUp = () => {
            setIsResizing(false);
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
            
            // Persist to localStorage
            if (storageKey) {
                localStorage.setItem(storageKey, width.toString());
            }
        };

        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, [isResizing, resizeFrom, minWidth, maxWidth, storageKey, width, onWidthChange]);

    // Save width to localStorage when it changes (debounced via mouseup)
    useEffect(() => {
        if (storageKey && !isResizing) {
            localStorage.setItem(storageKey, width.toString());
        }
    }, [width, storageKey, isResizing]);

    const handleStyle = resizeFrom === 'right' 
        ? 'right-0 cursor-col-resize' 
        : 'left-0 cursor-col-resize';

    return (
        <div
            ref={panelRef}
            className={`relative flex-shrink-0 ${className}`}
            style={{ width: `${width}px`, minWidth: `${width}px`, maxWidth: `${width}px` }}
        >
            {children}
            
            {/* Resize Handle */}
            <div
                className={`absolute top-0 ${handleStyle} w-1 h-full z-10 group`}
                onMouseDown={handleMouseDown}
            >
                {/* Visible handle indicator */}
                <div 
                    className={`
                        absolute top-0 ${resizeFrom === 'right' ? 'right-0' : 'left-0'} 
                        w-1 h-full 
                        bg-transparent 
                        group-hover:bg-blue-400 
                        transition-colors duration-150
                        ${isResizing ? 'bg-blue-500' : ''}
                    `}
                />
                {/* Wider invisible hit area */}
                <div 
                    className={`
                        absolute top-0 
                        ${resizeFrom === 'right' ? '-right-1' : '-left-1'} 
                        w-3 h-full
                    `}
                />
            </div>
            
            {/* Resize overlay to prevent iframe/canvas interference */}
            {isResizing && (
                <div className="fixed inset-0 z-50 cursor-col-resize" />
            )}
        </div>
    );
};

export default ResizablePanel;



