import React, { useState, forwardRef, useEffect, useCallback } from 'react';
import { 
    useDroppable,
} from '@dnd-kit/core';
import { Monitor, Tablet, Smartphone, Grid as GridIcon, Image as ImageIcon, Settings } from 'lucide-react';

import { useBuilderStore } from '../stores/useBuilderStore';
import { SortableComponent } from './SortableComponent';
import { DEVICE_DIMENSIONS } from '../types/builder.types';
import { useBackgroundImageUrl } from '../hooks/useBackgroundImageUrl';
import { isBackgroundFullyOffCanvas, createDefaultPlacement } from '../utils/backgroundPlacementUtils';
import { BackgroundImageCanvas } from './BackgroundImageCanvas';

interface FormBuilderCanvasProps {
    // No props needed if we use forwardRef correctly
}

// Use forwardRef to properly expose the DOM node
export const FormBuilderCanvas = forwardRef<HTMLDivElement, FormBuilderCanvasProps>((_props, ref) => {
    const { 
        formDefinition, 
        activePageId, 
        setScale, 
        scale, 
        showGrid, 
        setShowGrid,
        activeLayer,
        setActiveLayer,
        clearSelection, // Story 3.5
        selectedComponentIds // Story 3.5
    } = useBuilderStore();
    const [previewMode, setPreviewMode] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');

    const authoredPages = formDefinition?.desktopPages?.length
        ? formDefinition.desktopPages
        : formDefinition?.pages ?? [];
    const activePage = authoredPages.find(p => p.id === activePageId);
    const components = activePage?.components || [];

    const bg = activePage?.background;
    const { url: canvasBgImageUrl, isLoading: canvasBgLoading } = useBackgroundImageUrl(bg);
    const themeBgColor = formDefinition?.theme?.backgroundColor ?? '#FFFFFF';
    
    const { setNodeRef: setDndRef, isOver } = useDroppable({
        id: 'canvas-stage',
        data: { 
            type: 'stage',
            isContainer: true,
            scale: scale 
        }
    });

    // Container Ref for auto-scaling calculation
    const containerRef = React.useRef<HTMLDivElement>(null);

    // Merge Refs safely
    const setRefs = (element: HTMLDivElement | null) => {
        setDndRef(element);
        
        // Handle forwarded ref
        if (ref) {
            if (typeof ref === 'function') {
                ref(element);
            } else {
                ref.current = element;
            }
        }
    };

    // Story 3.5: Deselect on canvas click (clicking empty space)
    const handleCanvasClick = useCallback((e: React.MouseEvent) => {
        // Check if the click target is NOT a component or interactive element
        const target = e.target as HTMLElement;
        
        // Don't deselect if clicking on a component (has data-component-id or is inside one)
        const isComponentClick = target.closest('[data-component-id]') !== null;
        
        // Don't deselect if clicking on form elements or buttons
        const isInteractiveElement = ['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'].includes(target.tagName);
        
        if (!isComponentClick && !isInteractiveElement) {
            clearSelection();
        }
    }, [clearSelection]);

    // Story 3.5: Escape key to deselect
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'Escape' && selectedComponentIds.length > 0) {
                clearSelection();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [selectedComponentIds, clearSelection]);

    // Auto-Scale Logic - recalculates when container size changes (including panel resizes)
    useEffect(() => {
        const calculateScale = () => {
            if (!containerRef.current) return;
            
            const availableWidth = containerRef.current.clientWidth - 64; // Padding
            const availableHeight = containerRef.current.clientHeight - 64;
            
            const targetDim = DEVICE_DIMENSIONS[previewMode];
            
            const scaleX = availableWidth / targetDim.width;
            const scaleY = availableHeight / targetDim.height;
            
            // Use the smaller scale to fit both dimensions, capped at 1 (don't upscale pixelated)
            const newScale = Math.min(scaleX, scaleY, 1);
            
            // Use Store Action
            setScale(Math.max(0.2, Math.min(1, newScale)));
        };

        calculateScale();
        
        // Use ResizeObserver to detect container size changes (e.g., when panels are resized)
        const resizeObserver = new ResizeObserver(() => {
            // Debounce the calculation slightly for smoother resizing
            requestAnimationFrame(calculateScale);
        });
        
        if (containerRef.current) {
            resizeObserver.observe(containerRef.current);
        }
        
        // Also listen to window resize as fallback
        window.addEventListener('resize', calculateScale);
        
        return () => {
            resizeObserver.disconnect();
            window.removeEventListener('resize', calculateScale);
        };
    }, [previewMode, setScale]);

    const targetDim = DEVICE_DIMENSIONS[previewMode];

    if (!formDefinition) return <div>Loading Canvas...</div>;

    return (
        <div className="flex flex-col flex-1 h-full bg-gray-200 overflow-hidden">
            {/* Top Toolbar */}
            <div className="h-12 bg-white border-b flex items-center justify-between px-4 shadow-sm z-20 flex-shrink-0">
                <div className="flex items-center gap-4">
                    <span className="text-sm font-bold text-gray-600">{activePage?.title}</span>
                    
                    {/* Layer Switcher (Mini Toolbar) */}
                    <div className="flex bg-gray-100 rounded-md p-0.5 border border-gray-200">
                        <button
                            onClick={() => setActiveLayer(1)}
                            className={`px-3 py-1 text-xs font-medium rounded-sm flex items-center gap-1 ${activeLayer === 1 ? 'bg-white shadow-sm text-teal-600' : 'text-gray-500 hover:text-gray-700'}`}
                        >
                            <Settings size={12} /> Elements
                        </button>
                        <button
                            onClick={() => setActiveLayer(0)}
                            className={`px-3 py-1 text-xs font-medium rounded-sm flex items-center gap-1 ${activeLayer === 0 ? 'bg-white shadow-sm text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                        >
                            <ImageIcon size={12} /> Background
                        </button>
                    </div>
                    
                    <span className="text-xs text-gray-400 border-l pl-3 ml-2">
                        {Math.round(scale * 100)}% • {targetDim.width}x{targetDim.height}
                    </span>
                </div>
                
                <div className="flex items-center space-x-2 bg-gray-100 p-1 rounded-lg">
                    <button 
                        onClick={() => setPreviewMode('desktop')}
                        className={`p-1.5 rounded ${previewMode === 'desktop' ? 'bg-white shadow text-teal-600' : 'text-gray-500 hover:text-gray-700'}`}
                        title="Desktop (1920x980)"
                    >
                        <Monitor size={16} />
                    </button>
                    <button 
                        onClick={() => setPreviewMode('tablet')}
                        className={`p-1.5 rounded ${previewMode === 'tablet' ? 'bg-white shadow text-teal-600' : 'text-gray-500 hover:text-gray-700'}`}
                        title="Tablet (768x1024)"
                    >
                        <Tablet size={16} />
                    </button>
                    <button 
                        onClick={() => setPreviewMode('mobile')}
                        className={`p-1.5 rounded ${previewMode === 'mobile' ? 'bg-white shadow text-teal-600' : 'text-gray-500 hover:text-gray-700'}`}
                        title="Mobile (375x667)"
                    >
                        <Smartphone size={16} />
                    </button>
                </div>

                <button 
                    onClick={() => setShowGrid(!showGrid)}
                    className={`p-1.5 rounded ${showGrid ? 'bg-teal-50 text-teal-600' : 'text-gray-400 hover:text-gray-600'}`}
                    title="Toggle Grid"
                >
                    <GridIcon size={18} />
                </button>
            </div>

            {/* Canvas Viewport (Scrollable Area) */}
            <div 
                ref={containerRef}
                className="flex-1 overflow-hidden p-8 flex justify-center items-center relative bg-gray-200"
                onClick={handleCanvasClick} // Story 3.5: Deselect on background click
            >
                
                {/* THE STAGE */}
                <div 
                    ref={setRefs}
                    style={{
                        width: targetDim.width,
                        height: targetDim.height,
                        transform: `scale(${scale})`,
                        transformOrigin: 'center center'
                    }}
                    className={`
                        relative bg-white shadow-2xl transition-shadow duration-300 ease-in-out flex-shrink-0
                        ${isOver ? 'ring-4 ring-teal-400' : ''}
                        ${activeLayer === 0 ? 'ring-4 ring-indigo-400' : ''}
                    `}
                    onClick={handleCanvasClick} // Story 3.5: Deselect on stage click
                >
                    {/* LAYER 0: Background - T06 WYSIWYG. overflow-visible when Background mode so full image (including off-canvas) and handles are visible; no SmartBorder. */}
                    <div className={`absolute inset-0 z-0 ${activeLayer === 0 ? 'overflow-visible' : 'overflow-hidden'} ${activeLayer === 0 ? '' : 'pointer-events-none'}`}>
                        {activePage?.background ? (
                            activePage.background.type === 'image' ? (
                                (() => {
                                    const imageUrl = canvasBgImageUrl;
                                    const placement = activePage.background.placement ?? createDefaultPlacement(targetDim.width, targetDim.height);
                                    const canvasW = targetDim.width;
                                    const canvasH = targetDim.height;
                                    const fullyOffCanvas = isBackgroundFullyOffCanvas(placement, canvasW, canvasH);
                                    if (fullyOffCanvas) return null;
                                    const isInteractive = activeLayer === 0 && !!imageUrl;
                                    if (isInteractive && placement) {
                                        return (
                                            <BackgroundImageCanvas
                                                imageUrl={imageUrl}
                                                background={activePage.background}
                                                canvasWidth={canvasW}
                                                canvasHeight={canvasH}
                                                scale={scale}
                                                isBackgroundMode={activeLayer === 0}
                                                isLoading={canvasBgLoading}
                                            />
                                        );
                                    }
                                    const size = activePage.background.imageSize || 'contain';
                                    const position = activePage.background.imagePosition || 'center';
                                    const objectFit = (size === 'tile' || size === 'auto') ? 'cover' : (size === 'fill' ? 'fill' : size);
                                    const opacity = activePage.background.opacity ?? 1;
                                    if (!imageUrl) {
                                        return canvasBgLoading ? (
                                            <div className="w-full h-full animate-pulse" style={{ backgroundColor: themeBgColor }} />
                                        ) : (
                                            <div className="w-full h-full" style={{ backgroundColor: themeBgColor }} />
                                        );
                                    }
                                    const { position: pos, size: sz, crop } = placement;
                                    const assetW = activePage.background.asset?.widthPx ?? 1;
                                    const assetH = activePage.background.asset?.heightPx ?? 1;
                                    if (crop && assetW > 0 && assetH > 0) {
                                        const sx = sz.width / crop.width;
                                        const sy = sz.height / crop.height;
                                        return (
                                            <div
                                                className="absolute overflow-hidden pointer-events-none"
                                                style={{ left: pos.x, top: pos.y, width: sz.width, height: sz.height, opacity }}
                                            >
                                                <div
                                                    className="w-full h-full"
                                                    style={{
                                                        backgroundImage: `url(${imageUrl})`,
                                                        backgroundSize: `${assetW * sx}px ${assetH * sy}px`,
                                                        backgroundPosition: `${-crop.x * sx}px ${-crop.y * sy}px`,
                                                    }}
                                                />
                                            </div>
                                        );
                                    }
                                    return (
                                        <div
                                            className="absolute overflow-hidden pointer-events-none"
                                            style={{ left: pos.x, top: pos.y, width: sz.width, height: sz.height, opacity }}
                                        >
                                            <img
                                                src={imageUrl}
                                                className="w-full h-full"
                                                style={{
                                                    objectFit: objectFit as React.CSSProperties['objectFit'],
                                                    objectPosition: position,
                                                }}
                                                alt="Background"
                                            />
                                        </div>
                                    );
                                })()
                            ) : (
                                <div
                                    className="w-full h-full"
                                    style={{ backgroundColor: activePage.background.value || themeBgColor }}
                                />
                            )
                        ) : (
                            <div className="w-full h-full" style={{ backgroundColor: themeBgColor }} />
                        )}
                    </div>

                    {/* Grid Overlay */}
                    {showGrid && (
                        <div 
                            className="absolute inset-0 pointer-events-none z-50 opacity-20"
                            style={{
                                backgroundImage: `
                                    linear-gradient(to right, #ddd 1px, transparent 1px),
                                    linear-gradient(to bottom, #ddd 1px, transparent 1px)
                                `,
                                backgroundSize: '8px 8px'
                            }}
                        />
                    )}

                    {/* LAYER 1: Functional Components */}
                    <div className={`absolute inset-0 z-10 ${activeLayer === 0 ? 'opacity-50 pointer-events-none grayscale' : ''}`}>
                        {components.length === 0 && activeLayer === 1 ? (
                            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                <div className="text-gray-300 text-lg font-medium">
                                    Drag components here
                                </div>
                            </div>
                        ) : (
                            components.map((component) => (
                                <SortableComponent 
                                    key={component.id} 
                                    component={component} 
                                />
                            ))
                        )}
                    </div>

                    {/* Layer 0 Interaction Overlay */}
                    {activeLayer === 0 && (
                        <div className="absolute inset-0 z-20 border-4 border-indigo-400 pointer-events-none">
                            <div className="absolute top-2 left-2 bg-indigo-600 text-white px-3 py-1 text-xs font-bold rounded shadow">
                                Background Mode
                            </div>
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
});

// Display Name for Debugging
FormBuilderCanvas.displayName = 'FormBuilderCanvas';
