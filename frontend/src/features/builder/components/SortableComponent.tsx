import { useCallback, useState, useEffect, useRef, useMemo } from 'react';
import { useDraggable } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';
import { FormComponent } from '../types/builder.types';
import { SubmitButtonField } from './fields/SubmitButtonField';
import { ComponentRegistry } from '../registry/ComponentRegistry';
import { useBuilderStore } from '../stores/useBuilderStore';
import { computeFieldStyles } from '../utils/styleUtils';
import { ResizeHandles, HandlePosition, ResizePointerMeta } from './ui/ResizeHandles';
import { InputWidthHandles } from './ui/InputWidthHandles';
import { devLogger } from '../utils/devLogger';
import { UniversalFieldShell } from './UniversalFieldShell';
import { getRenderersForComponent } from '../utils/componentRenderers';
import { getDefaultStructure } from '../utils/structureDefaults';
import { captureComponentSnapshot } from '../utils/componentSnapshot';
import { estimateCharacterWidth, measureTextWidth } from '../utils/widthCalculator';
import { getComponentSurfaceCapabilities } from '../utils/componentSurfaceCapabilities';
import { useToastNotifications } from '../../ux/components/ToastProvider';
import { buildCanvasRectsForComponents, getComponentDimensions, resolveResizeConstraints } from '../utils/collisionDetection';
import { cornerToEdges, isCornerHandle } from '../utils/cornerResizeUtils';
import { getEffectiveGridLayout, resolveComponentDefaultGridLayout } from '../utils/gridLayoutUtils';

interface SortableComponentProps {
    component: FormComponent;
}

/**
 * ResizeHandlesWrapper - Positions ResizeHandles relative to SmartBorder container
 * 
 * When inputWidthOverride changes, the SmartBorder can be wider than the outer container.
 * This wrapper ensures ResizeHandles are positioned relative to the SmartBorder container,
 * not the outer container, so they always align with the SmartBorder shape.
 */
const ResizeHandlesWrapper: React.FC<{
    smartBorderContainerRef: React.RefObject<HTMLDivElement | null>;
    outerContainerRef: React.RefObject<HTMLDivElement | null>;
    componentId?: string;
    children: React.ReactNode;
    /** Key that changes when component dimensions change, forcing position recalculation */
    forceUpdateKey?: string | number;
}> = ({ smartBorderContainerRef, outerContainerRef, componentId, children, forceUpdateKey }) => {
    const [position, setPosition] = useState<{ top: number; left: number; width: number; height: number } | null>(null);
    const rafIdRef = useRef<number | null>(null);
    // Track mounted state to handle delayed ref population
    const [mounted, setMounted] = useState(false);
    // Track forceUpdateKey changes to trigger recalculation
    const [updateTrigger, setUpdateTrigger] = useState(0);
    
    // When forceUpdateKey changes, increment trigger to force recalculation
    // Use a delayed update to ensure DOM has updated after prop changes
    useEffect(() => {
        if (forceUpdateKey !== undefined) {
            // Immediate trigger for quick response
            setUpdateTrigger(prev => prev + 1);
            
            // Delayed triggers to catch DOM updates after React re-render
            // The SmartBorder path recalculates via ResizeObserver, which may take a frame
            const timer1 = setTimeout(() => setUpdateTrigger(prev => prev + 1), 50);
            const timer2 = setTimeout(() => setUpdateTrigger(prev => prev + 1), 150);
            
            return () => {
                clearTimeout(timer1);
                clearTimeout(timer2);
            };
        }
    }, [forceUpdateKey]);
    
    // Force remount check after initial render to handle ref population timing
    useEffect(() => {
        const timer = setTimeout(() => setMounted(true), 50);
        return () => clearTimeout(timer);
    }, []);
    
    useEffect(() => {
        const updatePosition = () => {
            const smartBorder = smartBorderContainerRef.current;
            const outer = outerContainerRef.current;
            
            if (!smartBorder || !outer) {
                devLogger.debug('resize.wrapper.refs.missing', {
                    smartBorder: !!smartBorder,
                    outer: !!outer,
                });
                setPosition(null);
                return;
            }
            
            const outerRect = outer.getBoundingClientRect();
            
            // The SmartBorder's visual extent is defined by the SVG path
            // The path traces an L-shape around the actual visible objects
            // We need to get the path's bounding box and convert to screen coordinates
            const svgPath = smartBorder.querySelector('svg path') as SVGPathElement | null;
            const svg = smartBorder.querySelector('svg') as SVGSVGElement | null;
            
            let visualRect: { top: number; left: number; width: number; height: number };
            
            if (svgPath && svg) {
                try {
                    // Get the path's bounding box in SVG/CSS coordinate space
                    // This is the actual visual extent of the SmartBorder path
                    const pathBBox = svgPath.getBBox();
                    
                    // The ResizeHandlesWrapper is positioned inside the same scaled container
                    // as the SVG, so we use the path's raw CSS dimensions directly.
                    // The canvas transform will scale both equally, maintaining alignment.
                    visualRect = {
                        top: pathBBox.y,
                        left: pathBBox.x,
                        width: pathBBox.width,
                        height: pathBBox.height,
                    };
                } catch {
                    // Fallback if getBBox fails
                    const rect = smartBorder.getBoundingClientRect();
                    visualRect = {
                        top: rect.top - outerRect.top,
                        left: rect.left - outerRect.left,
                        width: rect.width,
                        height: rect.height,
                    };
                }
            } else {
                // Fallback to container if no SVG found
                const rect = smartBorder.getBoundingClientRect();
                visualRect = {
                    top: rect.top - outerRect.top,
                    left: rect.left - outerRect.left,
                    width: rect.width,
                    height: rect.height,
                };
            }
            
            // Calculate position relative to outer container
            const newPosition = {
                top: visualRect.top,
                left: visualRect.left,
                width: visualRect.width,
                height: visualRect.height,
            };
            
            // Track position changes with delta calculation
            setPosition(prev => {
                if (!prev) {
                    devLogger.debug('resize.wrapper.position.calculated', {
                        componentId,
                        visualRect,
                        outerRect: { width: outerRect.width, height: outerRect.height, top: outerRect.top, left: outerRect.left },
                        calculatedPosition: newPosition,
                        usedPathBBox: !!svgPath,
                        change: 'initial',
                    });
                    return newPosition;
                }
                
                // Calculate deltas
                const deltaTop = newPosition.top - prev.top;
                const deltaLeft = newPosition.left - prev.left;
                const deltaWidth = newPosition.width - prev.width;
                const deltaHeight = newPosition.height - prev.height;
                
                // Use 0.5px threshold to avoid micro-adjustments that cause re-render loops
                const threshold = 0.5;
                const hasSignificantChange = 
                    Math.abs(deltaTop) >= threshold ||
                    Math.abs(deltaLeft) >= threshold ||
                    Math.abs(deltaWidth) >= threshold ||
                    Math.abs(deltaHeight) >= threshold;
                
                if (hasSignificantChange) {
                    devLogger.debug('resize.wrapper.position.calculated', {
                        componentId,
                        visualRect,
                        outerRect: { width: outerRect.width, height: outerRect.height, top: outerRect.top, left: outerRect.left },
                        calculatedPosition: newPosition,
                        usedPathBBox: !!svgPath,
                        change: 'updated',
                        previousPosition: prev,
                        deltas: {
                            top: deltaTop,
                            left: deltaLeft,
                            width: deltaWidth,
                            height: deltaHeight,
                        },
                    });
                    return newPosition;
                }
                
                // No significant change, prevent re-render
                return prev;
            });
        };
        
        // Batch updates via requestAnimationFrame to prevent excessive recalculations
        const scheduleUpdate = () => {
            if (rafIdRef.current !== null) {
                cancelAnimationFrame(rafIdRef.current);
            }
            rafIdRef.current = requestAnimationFrame(updatePosition);
        };
        
        scheduleUpdate();
        
        // Update on resize/scroll - batched via RAF
        const resizeObserver = new ResizeObserver(scheduleUpdate);
        if (smartBorderContainerRef.current) {
            resizeObserver.observe(smartBorderContainerRef.current);
        }
        // Also observe the outer container for size changes
        if (outerContainerRef.current) {
            resizeObserver.observe(outerContainerRef.current);
        }
        
        window.addEventListener('resize', scheduleUpdate);
        window.addEventListener('scroll', scheduleUpdate, true);
        
        return () => {
            if (rafIdRef.current !== null) {
                cancelAnimationFrame(rafIdRef.current);
            }
            resizeObserver.disconnect();
            window.removeEventListener('resize', scheduleUpdate);
            window.removeEventListener('scroll', scheduleUpdate, true);
        };
    }, [smartBorderContainerRef, outerContainerRef, mounted, componentId, updateTrigger]);
    
    if (!position) {
        return <>{children}</>;
    }
    
    return (
        <div
            style={{
                position: 'absolute',
                top: `${position.top}px`,
                left: `${position.left}px`,
                width: `${position.width}px`,
                height: `${position.height}px`,
                pointerEvents: 'none',
            }}
        >
            {children}
        </div>
    );
};

// Renamed to DraggableComponent since we aren't sorting anymore
export const SortableComponent: React.FC<SortableComponentProps> = ({ component }) => {
    const toast = useToastNotifications();
    // Seed default maxLength for text-like components (applies once per component)
    useEffect(() => {
        const typeDefaults: Record<string, number> = {
            'first-name': 30,
            text: 50,
            number: 12, // digit count heuristic
            email: 254,
            textarea: 500,
            phone: 20,
        };
        const target = typeDefaults[component.type];
        if (!target) return;
        const currentMax = component.props.validation?.maxLength;
        if (currentMax && currentMax > 0) return;
        // Merge validation with default maxLength
        const nextValidation = { ...(component.props.validation || {}), maxLength: target };
        useBuilderStore.getState().updateComponentProps(component.id, { validation: nextValidation });
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [component.id, component.type]);
    // Get the current Canvas Scale, Layer, Selection state, and Global Styles from store
    const { scale, activeLayer, selectedComponentIds, selectComponent, globalStyles, canvasSettings, updateComponentProps, updateComponent, activeId, dragPosition } = useBuilderStore(state => ({ 
        scale: state.scale, 
        activeLayer: state.activeLayer,
        selectedComponentIds: state.selectedComponentIds,
        selectComponent: state.selectComponent,
        globalStyles: state.formDefinition?.globalStyles,
        canvasSettings: state.formDefinition?.canvasSettings,
        updateComponentProps: state.updateComponentProps,
        updateComponent: state.updateComponent,
        activeId: state.activeId,
        dragPosition: state.dragPosition,
    }));
    
    // Local state for live resize preview
    const [resizePreview, setResizePreview] = useState<{ 
        width?: number; 
        height?: number; 
        scale?: number;
        labelGap?: number;
        inputHelpGap?: number;
        inputHeight?: number;
        inputWidthOverride?: number;
        topShift?: number;
        leftShift?: number;
        horizontalHandle?: 'e' | 'w'; // Track which horizontal handle was used
        startWidth?: number;
        startHeight?: number;
        // Preview object width overrides for E/W resize (input-only adjustment)
        previewLabelWidth?: number;
        previewInputWidth?: number;
        previewHelpWidth?: number;
        previewActionWidth?: number;
    } | null>(null);
    const lastVerticalPreviewRef = useRef<{ inputHeight?: number; labelGap?: number; inputHelpGap?: number; topShift?: number } | null>(null);
    
    // ═══════════════════════════════════════════════════════════════
    // Ref to store original start width for corner resizes
    // Ensures we always use the correct base width for calculations
    // ═══════════════════════════════════════════════════════════════
    const cornerResizeStartWidthRef = useRef<number | null>(null);

    // Store original submit button height for N/S + corner resizes
    const submitButtonStartHeightRef = useRef<number | null>(null);
    
    // ═══════════════════════════════════════════════════════════════
    // Ref to store initial object widths captured at E/W resize start
    // Used to calculate preview object widths that match commit behavior
    // ═══════════════════════════════════════════════════════════════
    const resizeStartObjectWidthsRef = useRef<{
        labelWidth: number;
        inputWidth: number;
        helpWidth: number;
        columnGapPx: number;
        totalExtras: number;
        // Layout context for width budgeting (only the objects in the same row as input participate)
        labelInInputRow: boolean;
        helpInInputRow: boolean;
        inputRowGapCount: number;
    } | null>(null);
    
    // Track actual DOM width when component.props.width is undefined (Auto) or percentage
    // This is needed for ResizeHandles to calculate correctly - parseWidth() returns 300 for percentages/undefined
    // MUST be declared before resize handlers that use it
    const [actualDomWidth, setActualDomWidth] = useState<number | null>(null);
    
    // Compute effective styles (global + any component overrides + scale + spacing overrides)
    const componentScale = component.props.componentScale ?? 100;
    const spacingOverrides = {
        labelGapOverride: component.props.labelGapOverride,
        inputHelpGapOverride: component.props.inputHelpGapOverride,
    };
    // IMPORTANT: Pass scale=100 to computeFieldStyles to render content at BASE size.
    // CSS transform: scale() handles ALL visual scaling.
    // Previously, both computeFieldStyles AND transform applied scale, causing double-scaling
    // which broke anchor positioning calculations.
    const fieldStyles = computeFieldStyles(globalStyles, component.props.styleOverrides, 100, spacingOverrides);

    // Get current spacing values (from computed - already includes overrides)
    const currentLabelGap = fieldStyles.computed.labelGap;
    const currentInputHelpGap = fieldStyles.computed.inputHelpGap;

    // Check if this component is currently selected (supports multi-select)
    const isSelected = selectedComponentIds.includes(component.id);

    // Determine if interaction should be disabled
    // For now, all components are on Layer 1 (Elements)
    // If Active Layer is 0 (Background), then Layer 1 is locked.
    const isLocked = activeLayer === 0;

    // ═══════════════════════════════════════════════════════════════
    // RESIZE HANDLERS - Different behavior per handle type
    // ═══════════════════════════════════════════════════════════════

    const handleResizeStart = useCallback((handle?: HandlePosition) => {
        // Set resizing state to enable visual preview feedback
        setIsResizingState(true);
        useBuilderStore.getState().setResizingComponentId(component.id);
        
        // Clear corner resize start width ref when starting a new resize
        if (handle && isCornerHandle(handle)) {
            cornerResizeStartWidthRef.current = null;
        }

        if (component.type === 'submit-button' && handle) {
            const snapshot = captureComponentSnapshot(component, smartBorderContainerRef);
            const measuredButtonHeightScreen =
                snapshot?.objectMetrics?.button?.rect?.height ??
                smartBorderContainerRef.current?.getBoundingClientRect()?.height ??
                fieldStyles.computed.inputHeight;
            const canvasScaleFactor = scale || 1.0;
            const scaleFactor = componentScale / 100;
            const effectiveScaleFactor = canvasScaleFactor * scaleFactor;
            const measuredButtonHeight =
                effectiveScaleFactor > 0
                    ? measuredButtonHeightScreen / effectiveScaleFactor
                    : measuredButtonHeightScreen;
            submitButtonStartHeightRef.current = component.props.height ?? measuredButtonHeight;
        }

        devLogger.debug('resize.handle.start', {
            componentId: component.id,
            handle: handle || 'unknown',
            isResizingState: true,
        });

        const isHorizontalHandle = handle === 'e' || handle === 'w';
        const isCornerHandleLocal = handle === 'nw' || handle === 'ne' || handle === 'sw' || handle === 'se';
        if (isHorizontalHandle || isCornerHandleLocal) {
            const gridContainer = smartBorderContainerRef.current?.querySelector('[data-layout-type="grid"]') as HTMLElement | null;
            if (gridContainer) {
                const computed = window.getComputedStyle(gridContainer);
                const templateColumns = computed.gridTemplateColumns;
                setFrozenGridTemplateColumns(templateColumns);
                devLogger.info('resize.grid.freeze', {
                    componentId: component.id,
                    handle,
                    gridTemplateColumns: templateColumns,
                    source: 'handleResizeStart',
                });
            }
            
            // ═══════════════════════════════════════════════════════════════
            // CAPTURE INITIAL OBJECT WIDTHS FOR PREVIEW (input-only resize)
            // This ensures preview matches commit behavior
            // DOM measurements are in screen pixels - convert to base pixels
            // ═══════════════════════════════════════════════════════════════
            const preSnapshot = captureComponentSnapshot(component, smartBorderContainerRef);
            const measuredWidths = preSnapshot?.objectMetrics || {};
            const gridMetrics = preSnapshot?.gridMetrics;
            
            // Calculate effective scale factor (canvas scale * component scale)
            // DOM measurements are in screen pixels, need to convert to base pixels
            const componentScaleFactor = componentScale / 100;
            const canvasScaleFactor = scale || 1.0;
            const effectiveScaleFactor = componentScaleFactor * canvasScaleFactor;
            
            // Get current object widths from props (already in base pixels) or DOM (convert from screen pixels)
            const measuredLabelWidthScreen = measuredWidths.label?.rect?.width ?? 0;
            const measuredHelpWidthScreen = measuredWidths.validation?.rect?.width ?? 0;
            const measuredInputWidthScreen = measuredWidths.input?.rect?.width ?? 0;
            
            // Convert screen pixels to base pixels by dividing by effective scale
            const measuredLabelWidthBase = effectiveScaleFactor > 0 ? measuredLabelWidthScreen / effectiveScaleFactor : measuredLabelWidthScreen;
            const measuredHelpWidthBase = effectiveScaleFactor > 0 ? measuredHelpWidthScreen / effectiveScaleFactor : measuredHelpWidthScreen;
            const measuredInputWidthBase = effectiveScaleFactor > 0 ? measuredInputWidthScreen / effectiveScaleFactor : measuredInputWidthScreen;
            
            // Use props if set (already in base pixels), otherwise use converted DOM measurements
            const labelWidth = component.props.labelWidthOverride ?? measuredLabelWidthBase;
            const helpWidth = component.props.helpWidthOverride ?? measuredHelpWidthBase;
            const inputWidth = component.props.inputWidthOverride ?? measuredInputWidthBase;
            
            // Determine which objects are in the same row as the input for width budgeting.
            // Rule: Only objects in the same row as the input "consume" horizontal space during E/W resize.
            const structureObjectIds = componentDef?.structure?.objects?.map(o => o.id) ?? [];
            const hasLabelObject = structureObjectIds.includes('label');
            const hasHelpObject = structureObjectIds.includes('validation') || structureObjectIds.includes('help');

            const getInputRowInfo = (): { labelInInputRow: boolean; helpInInputRow: boolean; inputRowGapCount: number } => {
                const effectiveGridLayout = getEffectiveGridLayout(
                    component.props.gridLayout,
                    resolveComponentDefaultGridLayout({
                        structure: componentDef?.structure ?? getDefaultStructure(component.type),
                        componentType: component.type,
                        globalStyles,
                    }),
                    globalStyles?.defaultGridLayout
                );

                if (effectiveGridLayout && typeof effectiveGridLayout.cellAssignments === 'object') {
                    const rowByObjectId: Record<string, number> = {};
                    for (const [key, objectId] of Object.entries(effectiveGridLayout.cellAssignments as Record<string, unknown>)) {
                        if (typeof objectId !== 'string') continue;
                        const [rowStr] = key.split('-');
                        const row = Number.parseInt(rowStr, 10);
                        if (!Number.isFinite(row)) continue;
                        rowByObjectId[objectId] = row;
                    }

                    const inputRow = rowByObjectId.input;
                    if (typeof inputRow === 'number') {
                        const objectsInRow = Object.entries(rowByObjectId)
                            .filter(([, row]) => row === inputRow)
                            .map(([objectId]) => objectId);
                        const labelInInputRow = hasLabelObject && objectsInRow.includes('label');
                        const helpInInputRow = hasHelpObject && (objectsInRow.includes('validation') || objectsInRow.includes('help'));
                        const objectCount = 1 + (labelInInputRow ? 1 : 0) + (helpInInputRow ? 1 : 0);
                        return {
                            labelInInputRow,
                            helpInInputRow,
                            inputRowGapCount: Math.max(0, objectCount - 1),
                        };
                    }
                }

                const layout = component.props.objectLayout ?? componentDef?.structure?.defaultLayout ?? 'vertical';
                if (layout === 'vertical') {
                    return { labelInInputRow: false, helpInInputRow: false, inputRowGapCount: 0 };
                }

                if (layout === 'mixed') {
                    const groups = component.props.layoutGroups ?? componentDef?.structure?.layoutGroups;
                    if (groups && typeof groups === 'object') {
                        const row = Object.values(groups).find(ids => Array.isArray(ids) && ids.includes('input')) as string[] | undefined;
                        if (row) {
                            const labelInInputRow = hasLabelObject && row.includes('label');
                            const helpInInputRow = hasHelpObject && (row.includes('validation') || row.includes('help'));
                            const objectCount = 1 + (labelInInputRow ? 1 : 0) + (helpInInputRow ? 1 : 0);
                            return {
                                labelInInputRow,
                                helpInInputRow,
                                inputRowGapCount: Math.max(0, objectCount - 1),
                            };
                        }
                    }
                }

                // Horizontal (or fallback): assume label + input + validation when present.
                const labelInInputRow = hasLabelObject;
                const helpInInputRow = hasHelpObject;
                const objectCount = 1 + (labelInInputRow ? 1 : 0) + (helpInInputRow ? 1 : 0);
                return {
                    labelInInputRow,
                    helpInInputRow,
                    inputRowGapCount: Math.max(0, objectCount - 1),
                };
            };

            const inputRowInfo = getInputRowInfo();

            // Get gap and extras - gap/padding/border are measured in screen px; convert to base px.
            // If DOM gap is unavailable (e.g. gap tracks), fall back to global spacing (already base px).
            const gapFallbackBase = globalStyles?.objectColumnGapPx ?? globalStyles?.baseSpacing ?? 8;
            const rawGapScreen = typeof gridMetrics?.columnGapPx === 'number'
                ? gridMetrics.columnGapPx
                : (typeof gridMetrics?.columnGap === 'string' ? parseFloat(gridMetrics.columnGap) : NaN);
            const columnGapPx =
                Number.isFinite(rawGapScreen)
                    ? (effectiveScaleFactor > 0 ? rawGapScreen / effectiveScaleFactor : rawGapScreen)
                    : gapFallbackBase;
            
            const paddingLeftPxScreen = typeof gridMetrics?.paddingLeftPx === 'number' ? gridMetrics.paddingLeftPx : 0;
            const paddingRightPxScreen = typeof gridMetrics?.paddingRightPx === 'number' ? gridMetrics.paddingRightPx : 0;
            const borderLeftPxScreen = typeof gridMetrics?.borderLeftPx === 'number' ? gridMetrics.borderLeftPx : 0;
            const borderRightPxScreen = typeof gridMetrics?.borderRightPx === 'number' ? gridMetrics.borderRightPx : 0;
            // Convert padding/border from screen to base pixels
            const paddingLeftPx = effectiveScaleFactor > 0 ? paddingLeftPxScreen / effectiveScaleFactor : paddingLeftPxScreen;
            const paddingRightPx = effectiveScaleFactor > 0 ? paddingRightPxScreen / effectiveScaleFactor : paddingRightPxScreen;
            const borderLeftPx = effectiveScaleFactor > 0 ? borderLeftPxScreen / effectiveScaleFactor : borderLeftPxScreen;
            const borderRightPx = effectiveScaleFactor > 0 ? borderRightPxScreen / effectiveScaleFactor : borderRightPxScreen;
            
            // SmartBorder has default 5px padding on each side (wraps the grid content)
            const smartBorderPadding = 5;
            const smartBorderPaddingTotal = smartBorderPadding * 2;
            
            const baseExtras = paddingLeftPx + paddingRightPx + borderLeftPx + borderRightPx + smartBorderPaddingTotal;
            const totalExtras = (columnGapPx * inputRowInfo.inputRowGapCount) + baseExtras;
            
            resizeStartObjectWidthsRef.current = {
                labelWidth,
                inputWidth,
                helpWidth,
                columnGapPx,
                totalExtras,
                ...inputRowInfo,
            };
            
            devLogger.info('resize.start.objectWidths.captured', {
                componentId: component.id,
                handle,
                scaling: {
                    componentScale,
                    canvasScale: scale,
                    effectiveScaleFactor,
                },
                screenPixels: {
                    label: measuredLabelWidthScreen,
                    input: measuredInputWidthScreen,
                    help: measuredHelpWidthScreen,
                    columnGap: rawGapScreen,
                },
                basePixels: {
                    label: labelWidth,
                    input: inputWidth,
                    help: helpWidth,
                    columnGap: columnGapPx,
                    totalExtras,
                },
                inputRowInfo,
                gapFallbackBase,
                propsOverrides: {
                    label: component.props.labelWidthOverride,
                    input: component.props.inputWidthOverride,
                    help: component.props.helpWidthOverride,
                },
            });
        }
        
        // Capture initial state for tracking
        const snapshot = captureComponentSnapshot(component, smartBorderContainerRef);
        const outerRect = outerContainerRef.current?.getBoundingClientRect();
        const smartBorderRect = smartBorderContainerRef.current?.getBoundingClientRect();
        const svgPath = smartBorderContainerRef.current?.querySelector('svg path') as SVGPathElement | null;
        let pathBBox = null;
        if (svgPath) {
            try {
                pathBBox = svgPath.getBBox();
            } catch {
                // Ignore
            }
        }
        
        // Get nearby components for collision context
        const state = useBuilderStore.getState();
        const def = state.formDefinition;
        const pages = def?.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def?.pages ?? []);
        const activePage = pages.find(p => p.id === state.activePageId);
        const allComponents = activePage?.components ?? [];
        const nearbyComponents = allComponents
            .filter(c => c.id !== component.id)
            .map(c => ({
                id: c.id,
                type: c.type,
                position: c.position,
                width: c.props.width,
                height: c.props.height,
            }))
            .slice(0, 10); // Limit to 10 for logging
        
        // Log comprehensive resize start with structure tracking
        devLogger.info('resize.start.comprehensive', {
            componentId: component.id,
            componentType: component.type,
            handle: handle || 'unknown',
            action: 'grab',
            initialPosition: {
                x: component.position?.x ?? 0,
                y: component.position?.y ?? 0,
            },
            initialDimensions: {
                width: component.props.width,
                height: component.props.height,
                scale: component.props.componentScale,
            },
            initialStructure: {
                objectLayout: component.props.objectLayout,
                labelWidthOverride: component.props.labelWidthOverride,
                inputWidthOverride: component.props.inputWidthOverride,
                helpWidthOverride: component.props.helpWidthOverride,
                labelGapOverride: component.props.labelGapOverride,
                inputHelpGapOverride: component.props.inputHelpGapOverride,
            },
            initialBounds: {
                outer: outerRect ? {
                    x: outerRect.x,
                    y: outerRect.y,
                    width: outerRect.width,
                    height: outerRect.height,
                } : null,
                smartBorder: smartBorderRect ? {
                    x: smartBorderRect.x,
                    y: smartBorderRect.y,
                    width: smartBorderRect.width,
                    height: smartBorderRect.height,
                } : null,
                pathBBox: pathBBox ? {
                    x: pathBBox.x,
                    y: pathBBox.y,
                    width: pathBBox.width,
                    height: pathBBox.height,
                } : null,
            },
            nearbyComponents,
            snapshot,
        });
        
        // Also log the standard event for compatibility
        devLogger.info('fieldshell.resize.start', {
            component: snapshot,
            handle: handle || 'unknown',
            action: 'grab'
        });
    }, [component, componentScale, fieldStyles, scale]); // Refs don't need to be in dependencies - they're stable

    // Live preview during resize (for visual feedback)
    const handleResize = useCallback((deltaWidth: number, deltaHeight: number, handle: HandlePosition) => {
        // Log resize grabbed (after initial grab)
        if (!resizePreview) {
            const snapshot = captureComponentSnapshot(component, smartBorderContainerRef);
            devLogger.info('fieldshell.resize.grabbed', {
                component: snapshot,
                handle,
                initialBounds: smartBorderContainerRef.current?.getBoundingClientRect() || null,
                initialProps: { 
                    width: component.props.width, 
                    height: component.props.height,
                    scale: component.props.componentScale 
                },
                layoutContext: {
                    objectLayout: component.props.objectLayout,
                    layoutGroups: component.props.layoutGroups,
                    rowAlignment: component.props.rowAlignment,
                    objectSpacing: component.props.objectSpacing,
                    gridLayout: component.props.gridLayout,
                    defaultGridLayout: globalStyles?.defaultGridLayout,
                },
            });
        }
        devLogger.debug('resize.handle.move', {
            componentId: component.id,
            handle,
            deltaWidth,
            deltaHeight,
            hasPreview: !!resizePreview,
        });
        
        // Get actual rendered width from DOM, not parsed percentage
        // This is critical: when width is "50%", we need the actual rendered width (e.g., 956px),
        // not the parsed percentage value (300px), otherwise resize calculations will be wrong
        let currentWidthPx: number;
        let widthSource: 'px-prop' | 'dom-measurement' | 'parsed-percentage' | 'default-fallback';
        if (component.props.width?.endsWith('px')) {
            currentWidthPx = parseInt(component.props.width, 10);
            widthSource = 'px-prop';
        } else {
            // For percentage or undefined width, use actualDomWidth state (calculated/measured)
            // This ensures we use the correct calculated value for percentages, not DOM measurement
            // which may be wrong due to canvas scale or inputWidthOverride expansion
            if (actualDomWidth !== null) {
                currentWidthPx = actualDomWidth;
                widthSource = component.props.width?.endsWith('%') ? 'percentage-calculated' : 'dom-measured';
            } else {
                // Fallback: calculate percentage or use default
                const canvasWidth = useBuilderStore.getState().formDefinition?.canvasSettings?.width || 1920;
                if (component.props.width?.endsWith('%')) {
                    const pct = parseFloat(component.props.width);
                    currentWidthPx = Math.max(50, Math.round((pct / 100) * canvasWidth));
                    widthSource = 'parsed-percentage-fallback';
                } else {
                    currentWidthPx = 300; // Default fallback
                    widthSource = 'default-fallback';
                }
            }
        }
        
        // Log width source for debugging
        if (!resizePreview) {
            devLogger.debug('resize.width.source', {
                componentId: component.id,
                propsWidth: component.props.width,
                currentWidthPx,
                widthSource,
                domWidth: outerContainerRef.current?.offsetWidth,
            });
            const gridContainer = smartBorderContainerRef.current?.querySelector('[data-layout-type="grid"]') as HTMLElement | null;
            devLogger.info('resize.width.chain', {
                componentId: component.id,
                deltaWidth,
                deltaHeight,
                widthSource,
                propsWidth: component.props.width,
                currentWidthPx,
                actualDomWidth,
                outerWidth: outerContainerRef.current?.offsetWidth,
                smartBorderWidth: smartBorderContainerRef.current?.getBoundingClientRect()?.width,
                gridWidth: gridContainer?.getBoundingClientRect().width,
            });
            if (Math.abs(deltaWidth) < 1 && Math.abs(deltaHeight) < 1) {
                devLogger.debug('resize.preview.skip', {
                    componentId: component.id,
                    reason: 'zero-delta',
                    deltaWidth,
                    deltaHeight,
                });
                return;
            }
        }
        const currentInputHeight = fieldStyles.computed.inputHeight;
        const scaleFactor = componentScale / 100;
        const minInputHeight = 28 * scaleFactor;
        const maxInputHeight = 240 * scaleFactor;

        // Calculate preview dimensions based on handle type
        const isCorner = isCornerHandle(handle);
        
        if (isCorner) {
            // Corner handles: non-proportional 2-axis resize (equivalent to E/W + N/S combined).
            // We preview width (like E/W) and vertical adjustments (like N/S) at the same time.
            const { horizontal: horizontalHandle, vertical: verticalHandle } = cornerToEdges(handle);

            // ───────────────────────────────────────────────────────────────
            // WIDTH PREVIEW (same math as E/W branch)
            // ───────────────────────────────────────────────────────────────
            const componentScaleFactor = componentScale / 100;
            const canvasScaleFactor = scale || 1.0;
            const effectiveScaleFactor = componentScaleFactor * canvasScaleFactor;
            const baseWidthDelta = effectiveScaleFactor !== 0 ? deltaWidth / effectiveScaleFactor : deltaWidth;

            // Capture startWidth on first corner drag event if not already set
            // Use ref to ensure we always have the original start width, not preview width
            if (!resizePreview && cornerResizeStartWidthRef.current === null) {
                cornerResizeStartWidthRef.current = currentWidthPx;
                devLogger.debug('resize.corner.startWidth.captured', {
                    componentId: component.id,
                    handle,
                    startWidth: currentWidthPx,
                });
            }
            
            // Use startWidth from preview if available, otherwise use ref, otherwise fallback to current
            const startWidth = resizePreview?.startWidth ?? cornerResizeStartWidthRef.current ?? currentWidthPx;
            const baseWidth = startWidth;
            
            // Validate baseWidthDelta matches expected direction
            if (horizontalHandle === 'e' && baseWidthDelta < 0) {
                devLogger.warn('resize.corner.unexpected.negative.delta', {
                    componentId: component.id,
                    handle,
                    horizontalHandle,
                    deltaWidth,
                    baseWidthDelta,
                    effectiveScaleFactor,
                    componentScaleFactor,
                    canvasScaleFactor,
                });
            } else if (horizontalHandle === 'w' && baseWidthDelta > 0) {
                devLogger.warn('resize.corner.unexpected.positive.delta', {
                    componentId: component.id,
                    handle,
                    horizontalHandle,
                    deltaWidth,
                    baseWidthDelta,
                    effectiveScaleFactor,
                    componentScaleFactor,
                    canvasScaleFactor,
                });
            }
            const minWidthPx = computeSelectionMinWidthPx() ?? 100;
            const unclampedWidth = baseWidth + baseWidthDelta;
            let nextWidth = Math.max(minWidthPx, unclampedWidth);
            
            // Track width constraints for corner handles
            const widthConstraints: string[] = [];
            if (unclampedWidth < minWidthPx) {
                widthConstraints.push(`componentWidth: ${unclampedWidth.toFixed(1)}px -> ${nextWidth.toFixed(1)}px (MIN: ${minWidthPx}px)`);
            }

            const caps = getComponentSurfaceCapabilities(component.type as any, 'canvas');
            const currentPositionX = component.position?.x ?? 0;
            if (horizontalHandle === 'e' && caps.resizeConstraints.enabled && caps.resizeConstraints.canvasBoundary) {
                const canvasWidth = useBuilderStore.getState().formDefinition?.canvasSettings?.width || 1920;
                const boundaryPadding = caps.resizeConstraints.boundaryPaddingPx || 0;
                const maxAllowedDisplayWidth = canvasWidth - (currentPositionX + boundaryPadding);
                const maxAllowedBaseWidth = Math.floor(maxAllowedDisplayWidth / (componentScale / 100));
                if (nextWidth > maxAllowedBaseWidth) {
                    const constrainedWidth = Math.max(minWidthPx, maxAllowedBaseWidth);
                    widthConstraints.push(`componentWidth: ${nextWidth.toFixed(1)}px -> ${constrainedWidth.toFixed(1)}px (canvas boundary)`);
                    nextWidth = constrainedWidth;
                }
            }

            const effectiveWidthDelta = nextWidth - baseWidth;
            const leftShift = horizontalHandle === 'w' ? -effectiveWidthDelta : 0;

            const capturedWidths = resizeStartObjectWidthsRef.current;
            let previewLabelWidth: number | undefined;
            let previewInputWidth: number | undefined;
            let previewHelpWidth: number | undefined;
            if (capturedWidths) {
                previewLabelWidth = capturedWidths.labelWidth;
                previewHelpWidth = capturedWidths.helpWidth;
                const fixedLabel = capturedWidths.labelInInputRow ? capturedWidths.labelWidth : 0;
                const fixedHelp = capturedWidths.helpInInputRow ? capturedWidths.helpWidth : 0;
                const availableForInput = nextWidth - fixedLabel - fixedHelp - capturedWidths.totalExtras;
                previewInputWidth = Math.max(60, availableForInput);
            }

            const widthPreview: typeof resizePreview = {
                width: nextWidth,
                startWidth,
                horizontalHandle: horizontalHandle,
                leftShift: leftShift !== 0 ? leftShift : undefined,
                previewLabelWidth,
                previewInputWidth,
                previewHelpWidth,
                ...(component.type === 'submit-button' ? { previewActionWidth: nextWidth } : {}),
            };

            // ───────────────────────────────────────────────────────────────
            // VERTICAL PREVIEW (same math as N/S branch)
            // deltaHeight is already normalized by ResizeHandles for corners.
            // ───────────────────────────────────────────────────────────────
            if (component.type === 'submit-button') {
                const canvasScaleFactor = scale || 1.0;
                const scaleFactor = componentScale / 100;
                const effectiveScaleFactor = canvasScaleFactor * scaleFactor;
                const baseHeightDelta = effectiveScaleFactor !== 0 ? deltaHeight / effectiveScaleFactor : deltaHeight;

                const measuredButtonHeightScreen =
                    captureComponentSnapshot(component, smartBorderContainerRef)?.objectMetrics?.button?.rect?.height ??
                    smartBorderContainerRef.current?.getBoundingClientRect()?.height ??
                    fieldStyles.computed.inputHeight;
                const measuredButtonHeight =
                    effectiveScaleFactor > 0
                        ? measuredButtonHeightScreen / effectiveScaleFactor
                        : measuredButtonHeightScreen;

                const startHeight =
                    resizePreview?.startHeight ??
                    submitButtonStartHeightRef.current ??
                    component.props.height ??
                    measuredButtonHeight;

                if (submitButtonStartHeightRef.current === null) {
                    submitButtonStartHeightRef.current = startHeight;
                }

                const minHeightPx = 28;
                const maxHeightPx = 240;
                const unclampedHeight = startHeight + baseHeightDelta;
                const nextHeight = Math.max(minHeightPx, Math.min(maxHeightPx, unclampedHeight));

                const mergedPreview: typeof resizePreview = {
                    ...widthPreview,
                    height: nextHeight,
                    startHeight,
                };

                setResizePreview(mergedPreview);
                return;
            }
            // Track vertical constraints for corner handles
            const verticalConstraints: string[] = [];
            
            let remainingDelta = deltaHeight;
            const requestedInputHeight = currentInputHeight + remainingDelta;
            let newInputHeight = Math.max(minInputHeight, Math.min(maxInputHeight, requestedInputHeight));
            
            // Track height constraints
            if (requestedInputHeight < minInputHeight) {
                verticalConstraints.push(`inputHeight: ${requestedInputHeight.toFixed(1)}px -> ${newInputHeight.toFixed(1)}px (MIN: ${minInputHeight.toFixed(1)}px)`);
            } else if (requestedInputHeight > maxInputHeight) {
                verticalConstraints.push(`inputHeight: ${requestedInputHeight.toFixed(1)}px -> ${newInputHeight.toFixed(1)}px (MAX: ${maxInputHeight.toFixed(1)}px)`);
            }
            
            remainingDelta -= (newInputHeight - currentInputHeight);

            const verticalPreview: typeof resizePreview = { inputHeight: newInputHeight };
            if (Math.abs(remainingDelta) > 0.1) {
                if (verticalHandle === 'n') {
                    const requestedGap = currentLabelGap + remainingDelta;
                    const newGap = Math.max(0, Math.min(48, requestedGap));
                    verticalPreview.labelGap = newGap;
                    
                    // Track gap constraints
                    if (requestedGap < 0) {
                        verticalConstraints.push(`labelGap: ${requestedGap.toFixed(1)}px -> ${newGap}px (MIN: 0px)`);
                    } else if (requestedGap > 48) {
                        verticalConstraints.push(`labelGap: ${requestedGap.toFixed(1)}px -> ${newGap}px (MAX: 48px)`);
                    }
                } else {
                    const requestedGap = currentInputHelpGap + remainingDelta;
                    const newGap = Math.max(0, Math.min(48, requestedGap));
                    verticalPreview.inputHelpGap = newGap;
                    
                    // Track gap constraints
                    if (requestedGap < 0) {
                        verticalConstraints.push(`inputHelpGap: ${requestedGap.toFixed(1)}px -> ${newGap}px (MIN: 0px)`);
                    } else if (requestedGap > 48) {
                        verticalConstraints.push(`inputHelpGap: ${requestedGap.toFixed(1)}px -> ${newGap}px (MAX: 48px)`);
                    }
                }
            }

            if (verticalHandle === 'n') {
                // Live top shift so south edge stays anchored during preview (same as N handle behavior)
                const heightUsed = newInputHeight - currentInputHeight;
                const spacingDelta = verticalPreview.labelGap !== undefined ? (verticalPreview.labelGap - currentLabelGap) : 0;
                verticalPreview.topShift = -(heightUsed + spacingDelta);
            }

            const mergedPreview: typeof resizePreview = {
                ...widthPreview,
                ...verticalPreview,
            };

            setResizePreview(mergedPreview);
            lastVerticalPreviewRef.current = {
                inputHeight: mergedPreview.inputHeight,
                labelGap: mergedPreview.labelGap,
                inputHelpGap: mergedPreview.inputHelpGap,
                topShift: mergedPreview.topShift,
            };
            
            // Log constraints if any were applied during preview calculation (Agent Logging System)
            if (widthConstraints.length > 0) {
                devLogger.info('resize.constraints.width', {
                    componentId: component.id,
                    componentType: component.type,
                    handle,
                    horizontalHandle,
                    constraintsApplied: widthConstraints,
                    requested: {
                        width: unclampedWidth,
                        widthDelta: baseWidthDelta,
                    },
                    final: {
                        width: nextWidth,
                        widthDelta: nextWidth - baseWidth,
                    },
                    reason: 'Corner handle width preview limited by constraints',
                });
            }
            
            if (verticalConstraints.length > 0) {
                devLogger.info('resize.constraints.vertical', {
                    componentId: component.id,
                    componentType: component.type,
                    handle,
                    verticalHandle,
                    constraintsApplied: verticalConstraints,
                    requested: {
                        deltaY: deltaHeight,
                    },
                    actual: {
                        heightChange: newInputHeight - currentInputHeight,
                        gapChange: {
                            labelGap: verticalPreview.labelGap !== undefined ? verticalPreview.labelGap - currentLabelGap : 0,
                            inputHelpGap: verticalPreview.inputHelpGap !== undefined ? verticalPreview.inputHelpGap - currentInputHelpGap : 0,
                        },
                    },
                    reason: 'Corner handle vertical preview limited by constraints',
                });
            }

            devLogger.debug('resize.corner.preview', {
                componentId: component.id,
                componentType: component.type,
                handle,
                horizontalHandle,
                verticalHandle,
                deltaWidth,
                deltaHeight,
                widthPreview: {
                    nextWidth,
                    leftShift,
                    startWidth,
                    previewLabelWidth,
                    previewInputWidth,
                    previewHelpWidth,
                },
                verticalPreview: {
                    inputHeight: mergedPreview.inputHeight,
                    labelGap: mergedPreview.labelGap,
                    inputHelpGap: mergedPreview.inputHelpGap,
                    topShift: mergedPreview.topShift,
                },
            });
        } else if (handle === 'e' || handle === 'w') {
            // Edge handles: show width preview
            // Also store which handle and left shift for W handle position adjustment
            // NOTE: deltaWidth is in SCREEN pixels from mouse movement
            // We need to convert to base pixels accounting for both component scale AND canvas zoom
            const componentScaleFactor = componentScale / 100;
            // Canvas scale is stored as a decimal (e.g., 0.5 for 50%, 1.0 for 100%, 2.0 for 200%)
            // Evidence: scale * 100 is used in getComponentDimensions calls to convert to percentage
            // deltaWidth is in screen pixels, so we divide by canvas scale to get base pixels
            // Then divide by component scale to account for component's own scaling
            const canvasScaleFactor = scale || 1.0; // scale is already a decimal (0.5 = 50%, 1.0 = 100%, 2.0 = 200%)
            const effectiveScaleFactor = componentScaleFactor * canvasScaleFactor;
            const baseWidthDelta = effectiveScaleFactor !== 0 ? deltaWidth / effectiveScaleFactor : deltaWidth;
            
            // Use a fixed start width so drag delta maps 1:1 to width changes.
            // This prevents cumulative drift when deltaWidth is already from the drag origin.
            const startWidth = resizePreview?.startWidth ?? currentWidthPx;
            const baseWidth = startWidth;
            const minWidthPx = computeSelectionMinWidthPx() ?? 100;
            const unclampedWidth = baseWidth + baseWidthDelta;
            let nextWidth = Math.max(minWidthPx, unclampedWidth);

            const caps = getComponentSurfaceCapabilities(component.type as any, 'canvas');
            const currentPositionX = component.position?.x ?? 0;
            if (handle === 'e' && caps.resizeConstraints.enabled && caps.resizeConstraints.canvasBoundary) {
                const canvasWidth = useBuilderStore.getState().formDefinition?.canvasSettings?.width || 1920;
                const boundaryPadding = caps.resizeConstraints.boundaryPaddingPx || 0;
                const maxAllowedDisplayWidth = canvasWidth - (currentPositionX + boundaryPadding);
                const maxAllowedBaseWidth = Math.floor(maxAllowedDisplayWidth / (componentScale / 100));
                if (nextWidth > maxAllowedBaseWidth) {
                    devLogger.warn('resize.preview.width.constrained', {
                        componentId: component.id,
                        handle,
                        reason: 'Preview width exceeds canvas bounds for E handle',
                        requestedWidth: nextWidth,
                        constrainedWidth: maxAllowedBaseWidth,
                        maxAllowedBaseWidth,
                        maxAllowedDisplayWidth,
                        position: { x: currentPositionX, y: component.position?.y ?? 0 },
                        canvasWidth,
                        componentScale,
                    });
                    nextWidth = Math.max(minWidthPx, maxAllowedBaseWidth);
                }
            }

            const effectiveWidthDelta = nextWidth - baseWidth;
            
            // Log the conversion for debugging
            devLogger.debug('resize.delta.conversion', {
                componentId: component.id,
                handle,
                deltaWidthScreenPx: deltaWidth,
                componentScale,
                canvasScaleDecimal: scale,
                canvasScaleFactor,
                componentScaleFactor,
                effectiveScaleFactor,
                baseWidthDelta,
                unclampedWidth,
                minWidthPx,
                effectiveWidthDelta,
                originalWidthPx: currentWidthPx,
                baseWidthUsed: baseWidth,
                nextWidth
            });
            // leftShift must be in CANVAS coordinates (same as position.x)
            // For W handle: shift left by the same amount the width increased to keep East edge anchored
            const leftShift = handle === 'w' ? -effectiveWidthDelta : 0;
            
            // Calculate edge positions for logging
            const westEdgeBefore = currentPositionX;
            const eastEdgeBefore = currentPositionX + baseWidth; // Use baseWidth (preview or original)
            const westEdgeAfter = handle === 'w' ? currentPositionX + leftShift : currentPositionX;
            const eastEdgeAfter = handle === 'w' ? currentPositionX + leftShift + nextWidth : currentPositionX + nextWidth;
            const eastEdgeDelta = eastEdgeAfter - eastEdgeBefore;
            
            // ═══════════════════════════════════════════════════════════════
            // CALCULATE PREVIEW OBJECT WIDTHS (input-only adjustment)
            // Keep label and help widths fixed, adjust input to fill remaining space
            // This ensures preview matches commit behavior
            // ═══════════════════════════════════════════════════════════════
            const capturedWidths = resizeStartObjectWidthsRef.current;
            let previewLabelWidth: number | undefined;
            let previewInputWidth: number | undefined;
            let previewHelpWidth: number | undefined;
            
            if (capturedWidths) {
                // Keep label and help fixed at their captured widths
                previewLabelWidth = capturedWidths.labelWidth;
                previewHelpWidth = capturedWidths.helpWidth;
                
                // Input fills the remaining space
                // nextWidth is the total component width, so input = total - label - help - gaps
                const fixedLabel = capturedWidths.labelInInputRow ? capturedWidths.labelWidth : 0;
                const fixedHelp = capturedWidths.helpInInputRow ? capturedWidths.helpWidth : 0;
                const availableForInput = nextWidth - fixedLabel - fixedHelp - capturedWidths.totalExtras;
                previewInputWidth = Math.max(60, availableForInput); // Minimum 60px for input
                
                devLogger.debug('resize.preview.objectWidths', {
                    componentId: component.id,
                    handle,
                    nextWidth,
                    capturedWidths,
                    calculatedInputWidth: previewInputWidth,
                    availableForInput,
                });
            }
            
            const previewUpdate = { 
                width: nextWidth, 
                startWidth,
                horizontalHandle: handle,
                leftShift: leftShift !== 0 ? leftShift : undefined,
                previewLabelWidth,
                previewInputWidth,
                previewHelpWidth,
                ...(component.type === 'submit-button' ? { previewActionWidth: nextWidth } : {}),
            } as typeof resizePreview & { horizontalHandle?: string; leftShift?: number };
            
            setResizePreview(previewUpdate);
            
            // Log resize preview state update (for E/W handles)
            devLogger.debug('resize.handle.move', {
                componentId: component.id,
                handle,
                deltaWidth,
                deltaHeight: 0,
                currentWidthPx,
                nextWidth,
                baseWidthDelta,
                effectiveWidthDelta,
                leftShift,
                previewWidth: nextWidth
            });
            
            devLogger.debug('fieldshell.resize.preview', {
                componentId: component.id,
                handle,
                deltaWidth,
                deltaHeight,
                scaleFactor,
                baseWidthDelta,
                startWidth,
                currentWidthPx,
                previewProps: { 
                    width: nextWidth, 
                    displayWidth: nextWidth * scaleFactor,
                    leftShift 
                }
            });
            
            // Enhanced edge position logging
            devLogger.info('resize.preview.edge.position', {
                componentId: component.id,
                handle,
                westEdge: { before: westEdgeBefore, after: westEdgeAfter },
                eastEdge: { before: eastEdgeBefore, after: eastEdgeAfter },
                eastEdgeDelta,
                expectedEastEdgeDelta: handle === 'w' ? 0 : baseWidthDelta, // W should anchor East, E should move East
                actualEastEdgeDelta: eastEdgeDelta,
                position: { x: currentPositionX, y: component.position?.y ?? 0 },
                width: { before: currentWidthPx, after: nextWidth }
            });
            
            // Track structure changes during resize preview
            const currentBounds = smartBorderContainerRef.current?.getBoundingClientRect();
            const svgPath = smartBorderContainerRef.current?.querySelector('svg path') as SVGPathElement | null;
            let pathBBox = null;
            if (svgPath) {
                try {
                    pathBBox = svgPath.getBBox();
                } catch {
                    // Ignore
                }
            }
            
            devLogger.debug('resize.preview.structure', {
                componentId: component.id,
                handle,
                    widthChange: {
                    before: currentWidthPx,
                    after: nextWidth,
                        delta: effectiveWidthDelta,
                },
                positionChange: {
                    before: { x: currentPositionX, y: component.position?.y ?? 0 },
                    after: { x: westEdgeAfter, y: component.position?.y ?? 0 },
                    leftShift,
                },
                bounds: currentBounds ? {
                    x: currentBounds.x,
                    y: currentBounds.y,
                    width: currentBounds.width,
                    height: currentBounds.height,
                } : null,
                pathBBox: pathBBox ? {
                    x: pathBBox.x,
                    y: pathBBox.y,
                    width: pathBBox.width,
                    height: pathBBox.height,
                } : null,
            });
        } else if (handle === 'n' || handle === 's') {
            // Height-first logic: adjust input height within bounds, then spacing with any remaining delta
            // deltaHeight here is already normalized (positive = drag down on S, drag up on N)
            if (component.type === 'submit-button') {
                const canvasScaleFactor = scale || 1.0;
                const scaleFactor = componentScale / 100;
                const effectiveScaleFactor = canvasScaleFactor * scaleFactor;
                const baseHeightDelta = effectiveScaleFactor !== 0 ? deltaHeight / effectiveScaleFactor : deltaHeight;

                const measuredButtonHeightScreen =
                    captureComponentSnapshot(component, smartBorderContainerRef)?.objectMetrics?.button?.rect?.height ??
                    smartBorderContainerRef.current?.getBoundingClientRect()?.height ??
                    fieldStyles.computed.inputHeight;
                const measuredButtonHeight =
                    effectiveScaleFactor > 0
                        ? measuredButtonHeightScreen / effectiveScaleFactor
                        : measuredButtonHeightScreen;

                const startHeight =
                    resizePreview?.startHeight ??
                    submitButtonStartHeightRef.current ??
                    component.props.height ??
                    measuredButtonHeight;

                if (submitButtonStartHeightRef.current === null) {
                    submitButtonStartHeightRef.current = startHeight;
                }

                const minHeightPx = 28;
                const maxHeightPx = 240;
                const unclampedHeight = startHeight + baseHeightDelta;
                const nextHeight = Math.max(minHeightPx, Math.min(maxHeightPx, unclampedHeight));

                const preview: typeof resizePreview = {
                    height: nextHeight,
                    startHeight,
                };

                setResizePreview(preview);
                return;
            }
            let remainingDelta = deltaHeight;
            let newInputHeight = Math.max(minInputHeight, Math.min(maxInputHeight, currentInputHeight + remainingDelta));
            remainingDelta -= (newInputHeight - currentInputHeight);

            const preview: typeof resizePreview = { inputHeight: newInputHeight };
            const clampedHeight = newInputHeight === minInputHeight || newInputHeight === maxInputHeight;

            if (Math.abs(remainingDelta) > 0.1) {
                if (handle === 'n') {
                    const newGap = Math.max(0, Math.min(48, currentLabelGap + remainingDelta));
                    preview.labelGap = newGap;
                } else {
                    const newGap = Math.max(0, Math.min(48, currentInputHelpGap + remainingDelta));
                    preview.inputHelpGap = newGap;
                }
            }

            if (handle === 'n') {
                // Live top shift so south edge stays anchored during preview
                const heightUsed = newInputHeight - currentInputHeight;
                const spacingDelta = preview.labelGap !== undefined ? (preview.labelGap - currentLabelGap) : 0;
                preview.topShift = -(heightUsed + spacingDelta);
            }

            setResizePreview(preview);
            lastVerticalPreviewRef.current = {
                inputHeight: preview.inputHeight,
                labelGap: preview.labelGap,
                inputHelpGap: preview.inputHelpGap,
                topShift: preview.topShift,
            };
            
            const bounds = smartBorderContainerRef.current?.getBoundingClientRect();
            devLogger.debug('resize.preview', {
                componentId: component.id,
                componentType: component.type,
                handle,
                deltaHeight,
                scaleFactor,
                position: component.position,
                bounds: bounds ? { x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height } : null,
                before: {
                    inputHeight: currentInputHeight,
                    labelGap: currentLabelGap,
                    inputHelpGap: currentInputHelpGap,
                },
                after: {
                    inputHeight: newInputHeight,
                    labelGap: preview.labelGap,
                    inputHelpGap: preview.inputHelpGap,
                    topShift: preview.topShift,
                },
                clampedHeight,
            });
        }
    }, [component.props.width, component.props.height, component.type, componentScale, fieldStyles.computed.inputHeight, currentLabelGap, currentInputHelpGap, actualDomWidth, resizePreview, scale]);

    // Width change handler (E/W handles)
    const handleWidthChange = useCallback((newWidth: number) => {
        const caps = getComponentSurfaceCapabilities(component.type as any, 'canvas');
        // Selection components with per-option extra text can visually distort if resized too small.
        // Clamp to a min width based on longest option label + required extra input chars.
        if (component.type === 'checkbox' || component.type === 'radio' || component.type === 'dropdown') {
            const opts = Array.isArray(component.props.options) ? component.props.options : [];
            const hasExtra = opts.some(o => Boolean((o as any).hasExtraText));
            if (hasExtra && fieldStyles?.computed) {
                const fontFamily = fieldStyles.computed.fontFamily;
                const fontSize = fieldStyles.computed.fontSize;
                const fontWeight = fieldStyles.computed.fontWeight;
                const paddingX = fieldStyles.computed.paddingX ?? 12;
                const borderW = fieldStyles.computed.borderWidth ?? 1;

                const charsWidth = (n: number) =>
                    Math.round(
                        measureTextWidth('W'.repeat(n), fontFamily, fontSize, fontWeight) +
                            (paddingX * 2) +
                            (borderW * 2)
                    );

                const longestLabelW = Math.max(
                    0,
                    ...opts.map(o =>
                        measureTextWidth(
                            String((o as any).label ?? (o as any).value ?? ''),
                            fontFamily,
                            fontSize,
                            fontWeight
                        )
                    )
                );

                let minWidthPx = 0;
                if (component.type === 'dropdown') {
                    const arrowSpace = 40;
                    const minDropdown = Math.max(
                        Math.round(longestLabelW + (paddingX * 2) + (borderW * 2) + arrowSpace),
                        Math.round(charsWidth(10) + arrowSpace)
                    );
                    const minExtra = charsWidth(10);
                    const gap = 8;
                    minWidthPx = Math.round(minDropdown + gap + minExtra);
                } else {
                    // checkbox/radio: longest label + 5-char input
                    const controlW = 14;
                    const controlGap = 8;
                    const rowGap = 10;
                    const minExtra = charsWidth(5);
                    const labelCol = Math.round(controlW + controlGap + longestLabelW);
                    minWidthPx = Math.round((paddingX * 2) + labelCol + rowGap + minExtra);
                }

                if (minWidthPx > 0) newWidth = Math.max(newWidth, minWidthPx);
            }
        }

        const opts = Array.isArray(component.props.options) ? component.props.options : [];
        const hasExtra = opts.some(o => Boolean((o as any).hasExtraText));
        const isDropdownSplit = component.type === 'dropdown' && hasExtra;
        // Check if W handle was used - need to adjust X position to anchor East edge
        const previewData = resizePreview as (typeof resizePreview) & { horizontalHandle?: string; leftShift?: number };
        const isWestHandle = previewData?.horizontalHandle === 'w';
        const leftShift = previewData?.leftShift ?? 0;
        
        // Capture before state for logging
        const oldWidth = component.props.width;
        // ═══════════════════════════════════════════════════════════════
        // ATTEMPT 12 FIX: Use startWidth from preview, not current DOM
        // During resize, the DOM shows the preview state. We need the 
        // ORIGINAL width from when the resize started (captured at pointer down).
        // For corner handles, also check cornerResizeStartWidthRef as fallback.
        // ═══════════════════════════════════════════════════════════════
        let oldWidthPx: number;
        const startWidthFromPreview = (previewData as any)?.startWidth;
        
        if (startWidthFromPreview !== undefined && startWidthFromPreview > 0) {
            // Best source: use the startWidth captured at pointer down
            oldWidthPx = startWidthFromPreview;
            devLogger.debug('resize.oldWidthPx.source', {
                componentId: component.id,
                source: 'startWidthFromPreview',
                startWidthFromPreview,
                propsWidth: oldWidth,
                actualDomWidth,
            });
        } else if (cornerResizeStartWidthRef.current !== null && cornerResizeStartWidthRef.current !== undefined) {
            // Fallback for corner handles: use cornerResizeStartWidthRef
            oldWidthPx = cornerResizeStartWidthRef.current;
            devLogger.debug('resize.oldWidthPx.source', {
                componentId: component.id,
                source: 'cornerResizeStartWidthRef',
                startWidth: cornerResizeStartWidthRef.current,
                propsWidth: oldWidth,
                actualDomWidth,
            });
        } else if (oldWidth?.endsWith('px')) {
            oldWidthPx = parseInt(oldWidth, 10);
        } else {
            // For percentage or undefined width, use actualDomWidth state (calculated/measured)
            // This ensures we use the correct calculated value for percentages
            if (actualDomWidth !== null) {
                oldWidthPx = actualDomWidth;
            } else {
                // Fallback: calculate percentage or use default
                const canvasWidth = useBuilderStore.getState().formDefinition?.canvasSettings?.width || 1920;
                if (oldWidth?.endsWith('%')) {
                    const pct = parseFloat(oldWidth);
                    oldWidthPx = Math.max(50, Math.round((pct / 100) * canvasWidth));
                } else {
                    oldWidthPx = 300; // Default fallback
                }
            }
        }
        const oldPosition = { ...component.position };
        const currentX = component.position?.x ?? 0;
        const currentY = component.position?.y ?? 0;
        const snapshotBefore = captureComponentSnapshot(component, smartBorderContainerRef);
        let finalPosition = component.position;
        const bounds = smartBorderContainerRef.current?.getBoundingClientRect();
        
        // ═══════════════════════════════════════════════════════════════
        // E HANDLE CANVAS BOUNDARY CHECK (before object width calculations)
        // For E handle: position must stay fixed, so constrain width if needed
        // ═══════════════════════════════════════════════════════════════
        const isEastHandle = !isWestHandle && previewData?.horizontalHandle === 'e';
        if (isEastHandle && caps.resizeConstraints.enabled && caps.resizeConstraints.canvasBoundary) {
            const canvasWidth = useBuilderStore.getState().formDefinition?.canvasSettings?.width || 1920;
            const maxAllowedDisplayWidth = canvasWidth - (currentX + (caps.resizeConstraints.boundaryPaddingPx || 0));
            const maxAllowedBaseWidth = Math.floor(maxAllowedDisplayWidth / (componentScale / 100));
            
            if (newWidth > maxAllowedBaseWidth) {
                const constrainedWidth = Math.max(50, maxAllowedBaseWidth);
                devLogger.warn('resize.east.handle.width.constrained', {
                    componentId: component.id,
                    reason: 'E handle resize would exceed canvas bounds - constraining width to keep position fixed',
                    requestedWidth: newWidth,
                    constrainedWidth,
                    maxAllowedBaseWidth,
                    maxAllowedDisplayWidth,
                    position: { x: currentX, y: component.position?.y ?? 0 },
                    canvasWidth,
                    componentScale,
                });
                newWidth = constrainedWidth;
            }
        }
        
        // ═══════════════════════════════════════════════════════════════
        // INPUT-ONLY WIDTH ADJUSTMENT
        // Label and Help widths stay FIXED, only Input width changes
        // DOM measurements are in screen pixels - convert to base pixels
        // ═══════════════════════════════════════════════════════════════
        const scaleFactor = componentScale / 100;
        
        // Calculate effective scale factor (canvas scale * component scale)
        // DOM measurements are in screen pixels, need to convert to base pixels
        const canvasScaleFactor = scale || 1.0;
        const effectiveScaleFactor = scaleFactor * canvasScaleFactor;

        const measuredWidths = snapshotBefore?.objectMetrics || {};
        
        // DOM measurements are in screen pixels - convert to base pixels
        const measuredLabelWidthScreen = measuredWidths.label?.rect?.width ?? 0;
        const measuredInputWidthScreen = measuredWidths.input?.rect?.width ?? 0;
        const measuredHelpWidthScreen = measuredWidths.validation?.rect?.width ?? 0;
        
        const measuredLabelWidth = effectiveScaleFactor > 0 
            ? measuredLabelWidthScreen / effectiveScaleFactor 
            : measuredLabelWidthScreen;
        const measuredInputWidth = effectiveScaleFactor > 0 
            ? measuredInputWidthScreen / effectiveScaleFactor 
            : measuredInputWidthScreen;
        const measuredHelpWidth = effectiveScaleFactor > 0 
            ? measuredHelpWidthScreen / effectiveScaleFactor 
            : measuredHelpWidthScreen;
        
        // Get current width overrides or use converted DOM measurements
        // Props are already in base pixels, DOM measurements have been converted
        const currentLabelWidth = component.props.labelWidthOverride ?? measuredLabelWidth ?? oldWidthPx;
        const currentHelpWidth = component.props.helpWidthOverride ?? measuredHelpWidth ?? oldWidthPx;
        
        // For input, estimate based on maxLength if available, otherwise use component width
        const maxLength = component.props.validation?.maxLength;
        let currentInputWidth = component.props.inputWidthOverride ?? measuredInputWidth;
        if (!currentInputWidth) {
            if (!isDropdownSplit && maxLength && fieldStyles?.computed) {
                // Estimate input width based on text length using actual measurement
                // measureCharacterWidth measures 100 random characters and calculates per-character width
                currentInputWidth = estimateCharacterWidth(maxLength, {
                    fontFamily: fieldStyles.computed.fontFamily,
                    fontSize: fieldStyles.computed.fontSize,
                    fontWeight: fieldStyles.computed.fontWeight,
                }, 1.0);
                // Note: estimateCharacterWidth already includes padding (40px), so we just clamp to old width
                currentInputWidth = Math.min(currentInputWidth, oldWidthPx);
            } else {
                currentInputWidth = oldWidthPx;
            }
        }
        
        const gridMetrics = snapshotBefore?.gridMetrics;

        // Width budgeting is row-aware: only objects in the same row as the input participate.
        // We capture this context at resize start so preview and commit match.
        const capturedWidths = resizeStartObjectWidthsRef.current;
        const inputRowGapCount = capturedWidths?.inputRowGapCount ?? 2;
        const labelInInputRow = capturedWidths?.labelInInputRow ?? true;
        const helpInInputRow = capturedWidths?.helpInInputRow ?? true;

        // Gap: prefer captured DOM-derived gap (converted to base px) when available.
        // Fallback to global spacing (already base px).
        const gapFallbackBase = globalStyles?.objectColumnGapPx ?? globalStyles?.baseSpacing ?? 8;
        const columnGapPx = capturedWidths?.columnGapPx ?? gapFallbackBase;
        
        const paddingLeftPxScreen = typeof gridMetrics?.paddingLeftPx === 'number' ? gridMetrics.paddingLeftPx : 0;
        const paddingRightPxScreen = typeof gridMetrics?.paddingRightPx === 'number' ? gridMetrics.paddingRightPx : 0;
        const borderLeftPxScreen = typeof gridMetrics?.borderLeftPx === 'number' ? gridMetrics.borderLeftPx : 0;
        const borderRightPxScreen = typeof gridMetrics?.borderRightPx === 'number' ? gridMetrics.borderRightPx : 0;
        
        // Convert padding/border from screen to base pixels
        const paddingLeftPx = effectiveScaleFactor > 0 ? paddingLeftPxScreen / effectiveScaleFactor : paddingLeftPxScreen;
        const paddingRightPx = effectiveScaleFactor > 0 ? paddingRightPxScreen / effectiveScaleFactor : paddingRightPxScreen;
        const borderLeftPx = effectiveScaleFactor > 0 ? borderLeftPxScreen / effectiveScaleFactor : borderLeftPxScreen;
        const borderRightPx = effectiveScaleFactor > 0 ? borderRightPxScreen / effectiveScaleFactor : borderRightPxScreen;
        
        // SmartBorder has default 5px padding on each side (wraps the grid content)
        // This padding is OUTSIDE the grid container but INSIDE the component
        const smartBorderPadding = 5; // Default SmartBorder padding
        const smartBorderPaddingTotal = smartBorderPadding * 2; // Left + Right
        
        const totalExtras =
            (columnGapPx * inputRowGapCount) +
            paddingLeftPx +
            paddingRightPx +
            borderLeftPx +
            borderRightPx +
            smartBorderPaddingTotal;
        
        // Debug: Log totalExtras breakdown
        devLogger.info('resize.totalExtras.breakdown', {
            componentId: component.id,
            effectiveScaleFactor,
            componentScale,
            canvasScale: scale,
            gapSource: capturedWidths?.columnGapPx ? 'captured(DOM→base)' : 'globalStyles(default)',
            gapFallbackBase,
            columnGapPx,
            inputRowContext: {
                labelInInputRow,
                helpInInputRow,
                inputRowGapCount,
            },
            screenPixels: {
                paddingLeftPxScreen,
                paddingRightPxScreen,
                borderLeftPxScreen,
                borderRightPxScreen,
            },
            basePixels: {
                paddingLeftPx,
                paddingRightPx,
                borderLeftPx,
                borderRightPx,
                smartBorderPaddingTotal,
            },
            calculation: {
                columnGaps: columnGapPx * inputRowGapCount,
                gridPadding: paddingLeftPx + paddingRightPx,
                gridBorder: borderLeftPx + borderRightPx,
                smartBorder: smartBorderPaddingTotal,
                totalExtras,
            },
        });

        const labelText = component.props.label ?? '';
        const helpText = component.props.helpText ?? component.props.validationMessage ?? '';
        const labelMetrics = measuredWidths.label;
        const helpMetrics = measuredWidths.validation;
        const inputMetrics = measuredWidths.input;
        const labelPadding = labelMetrics?.padding ? (labelMetrics.padding.left + labelMetrics.padding.right) : 0;
        const labelBorder = labelMetrics?.border ? (labelMetrics.border.left + labelMetrics.border.right) : 0;
        const helpPadding = helpMetrics?.padding ? (helpMetrics.padding.left + helpMetrics.padding.right) : 0;
        const helpBorder = helpMetrics?.border ? (helpMetrics.border.left + helpMetrics.border.right) : 0;
        const inputPadding = inputMetrics?.padding ? (inputMetrics.padding.left + inputMetrics.padding.right) : 0;
        const inputBorder = inputMetrics?.border ? (inputMetrics.border.left + inputMetrics.border.right) : 0;

        const labelFontFamily = fieldStyles?.computed?.labelFontFamily || fieldStyles?.computed?.fontFamily;
        const labelFontSize = fieldStyles?.computed?.labelFontSize || fieldStyles?.computed?.fontSize;
        const labelFontWeight = fieldStyles?.computed?.labelFontWeight || fieldStyles?.computed?.fontWeight;
        const helpFontFamily = fieldStyles?.computed?.helpTextFontFamily || fieldStyles?.computed?.fontFamily;
        const helpFontSize = fieldStyles?.computed?.helpTextFontSize || 12;
        const helpFontWeight = fieldStyles?.computed?.helpTextFontWeight || 400;

        // Measure text width using canvas API
        // Add a small safety margin (2px) to account for sub-pixel rendering differences
        // between canvas measureText and actual DOM rendering (font hinting, kerning, etc.)
        const TEXT_WIDTH_SAFETY_MARGIN = 2;
        
        const labelTextWidth = labelText
            ? measureTextWidth(labelText, labelFontFamily, labelFontSize, labelFontWeight) + TEXT_WIDTH_SAFETY_MARGIN
            : 0;
        const helpTextWidth = helpText
            ? measureTextWidth(helpText, helpFontFamily, helpFontSize, helpFontWeight) + TEXT_WIDTH_SAFETY_MARGIN
            : 0;
        // Use the larger of: calculated text width OR DOM-measured width
        // The calculated width uses canvas measureText which may not have the actual font loaded
        // The DOM-measured width might be the wrapped/constrained width
        // 
        // Strategy: Use Math.ceil to avoid sub-pixel rounding issues that cause wrapping
        // If text is currently wrapped (detected via lineCount/height), add safety margin
        const calculatedMinLabelWidth = Math.round(labelTextWidth + labelPadding + labelBorder);
        // Use Math.ceil to prevent sub-pixel precision loss (e.g., 70.29 -> 71, not 70)
        const domMinLabelWidth = Math.ceil(currentLabelWidth);
        // Check if label text is currently wrapped (from snapshot)
        const isLabelWrapped = labelMetrics?.isTextWrapped === true;
        const labelSafetyMargin = isLabelWrapped ? TEXT_WIDTH_SAFETY_MARGIN : 0;
        const minLabelWidth = Math.max(10, calculatedMinLabelWidth, domMinLabelWidth + labelSafetyMargin);
        
        const calculatedMinHelpWidth = Math.round(helpTextWidth + helpPadding + helpBorder);
        // Use Math.ceil for help width too
        const domMinHelpWidth = Math.ceil(currentHelpWidth);
        // Check if help text is currently wrapped (from snapshot)
        const isHelpWrapped = helpMetrics?.isTextWrapped === true;
        const helpSafetyMargin = isHelpWrapped ? TEXT_WIDTH_SAFETY_MARGIN : 0;
        const minHelpWidth = Math.max(10, calculatedMinHelpWidth, domMinHelpWidth + helpSafetyMargin);
        
        devLogger.info('resize.minWidth.calculated', {
            componentId: component.id,
            label: {
                text: labelText,
                textWidth: labelTextWidth,
                padding: labelPadding,
                border: labelBorder,
                calculatedMin: calculatedMinLabelWidth,
                domMin: domMinLabelWidth,
                domCurrent: currentLabelWidth,
                isWrapped: isLabelWrapped,
                lineCount: labelMetrics?.lineCount,
                isMultiLine: labelMetrics?.isMultiLine,
                safetyMargin: labelSafetyMargin,
                minWidth: minLabelWidth,
                fontFamily: labelFontFamily,
                fontSize: labelFontSize,
                fontWeight: labelFontWeight,
            },
            help: {
                text: helpText,
                textWidth: helpTextWidth,
                padding: helpPadding,
                border: helpBorder,
                calculatedMin: calculatedMinHelpWidth,
                domMin: domMinHelpWidth,
                domCurrent: currentHelpWidth,
                isWrapped: isHelpWrapped,
                lineCount: helpMetrics?.lineCount,
                isMultiLine: helpMetrics?.isMultiLine,
                safetyMargin: helpSafetyMargin,
                minWidth: minHelpWidth,
            },
        });

        let minInputWidth = 80;
        if (fieldStyles?.computed) {
            minInputWidth = Math.round(
                measureTextWidth(
                    'W'.repeat(10),
                    fieldStyles.computed.fontFamily,
                    fieldStyles.computed.fontSize,
                    fieldStyles.computed.fontWeight
                ) + inputPadding + inputBorder
            );
        }
        minInputWidth = Math.max(60, minInputWidth);

        let adjustedWidth = newWidth;
        let available = adjustedWidth - totalExtras;
        if (!Number.isFinite(available)) {
            available = currentLabelWidth + currentHelpWidth + currentInputWidth;
        }

        const shrinking = adjustedWidth < oldWidthPx;
        // Use Math.ceil to prevent sub-pixel precision loss
        let targetLabelWidth = Math.ceil(currentLabelWidth);
        let targetHelpWidth = Math.ceil(currentHelpWidth);
        let targetInputWidth = Math.round(isDropdownSplit ? currentInputWidth : (available - targetLabelWidth - targetHelpWidth));

        if (!isDropdownSplit) {
            if (shrinking && targetInputWidth < minInputWidth) {
                const remaining = Math.max(minLabelWidth + minHelpWidth, available - minInputWidth);
                targetLabelWidth = Math.min(Math.max(minLabelWidth, targetLabelWidth), remaining - minHelpWidth);
                targetHelpWidth = Math.min(Math.max(minHelpWidth, targetHelpWidth), remaining - targetLabelWidth);
                targetInputWidth = Math.max(minInputWidth, available - targetLabelWidth - targetHelpWidth);
            } else if (targetInputWidth < minInputWidth) {
                targetInputWidth = minInputWidth;
            }
        }

        // Track which constraints were applied
        const constraintsApplied: string[] = [];
        
        if (targetInputWidth < minInputWidth) {
            constraintsApplied.push(`inputWidth: ${targetInputWidth.toFixed(1)}px -> ${minInputWidth}px (MIN)`);
            targetInputWidth = minInputWidth;
        }
        if (targetLabelWidth < minLabelWidth) {
            constraintsApplied.push(`labelWidth: ${targetLabelWidth.toFixed(1)}px -> ${minLabelWidth}px (MIN)`);
            targetLabelWidth = minLabelWidth;
        }
        if (targetHelpWidth < minHelpWidth) {
            constraintsApplied.push(`helpWidth: ${targetHelpWidth.toFixed(1)}px -> ${minHelpWidth}px (MIN)`);
            targetHelpWidth = minHelpWidth;
        }

        const maxObjectWidth = Math.max(10, Math.round(adjustedWidth));
        const newLabelWidth = Math.min(maxObjectWidth, targetLabelWidth);
        const newHelpWidth = Math.min(maxObjectWidth, targetHelpWidth);
        const newInputWidth = Math.min(maxObjectWidth, Math.round(targetInputWidth));
        
        // Track max width constraints
        if (newLabelWidth < targetLabelWidth) {
            constraintsApplied.push(`labelWidth: ${targetLabelWidth.toFixed(1)}px -> ${newLabelWidth}px (MAX)`);
        }
        if (newHelpWidth < targetHelpWidth) {
            constraintsApplied.push(`helpWidth: ${targetHelpWidth.toFixed(1)}px -> ${newHelpWidth}px (MAX)`);
        }
        if (newInputWidth < targetInputWidth) {
            constraintsApplied.push(`inputWidth: ${targetInputWidth.toFixed(1)}px -> ${newInputWidth}px (MAX)`);
        }

        const minTotal = newLabelWidth + newHelpWidth + newInputWidth + totalExtras;
        if (minTotal > adjustedWidth) {
            constraintsApplied.push(`componentWidth: ${adjustedWidth.toFixed(1)}px -> ${minTotal.toFixed(1)}px (expanded to fit min objects)`);
            adjustedWidth = minTotal;
        }

        newWidth = Math.round(adjustedWidth);
        const widthRatio = newWidth / oldWidthPx;
        const widthDelta = Math.round(newWidth - oldWidthPx);
        const hasWidthChange = Math.abs(widthDelta) >= 1;
        
        // Log constraint violations if any occurred (Agent Logging System)
        if (constraintsApplied.length > 0) {
            devLogger.info('resize.constraints.width', {
                componentId: component.id,
                componentType: component.type,
                handle: isWestHandle ? 'w' : 'e',
                constraintsApplied,
                requested: {
                    width: newWidth,
                    widthDelta: newWidth - oldWidthPx,
                },
                final: {
                    width: newWidth,
                    widthDelta: newWidth - oldWidthPx,
                },
                reason: 'Width change limited by min/max constraints',
            });
        }
        // ───────────────────────────────────────────────────────────────
        // Collision/boundary constraints (commit)
        // Keep requested size, then auto-adjust position; otherwise reject with toast.
        // ───────────────────────────────────────────────────────────────
        if (caps.resizeConstraints.enabled && (caps.resizeConstraints.canvasBoundary || caps.resizeConstraints.collisionAvoidance)) {
            const state = useBuilderStore.getState();
            const def = state.formDefinition;
            const pages = def?.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def?.pages ?? []);
            const activePage = pages.find(p => p.id === state.activePageId);
            const allComponents = activePage?.components ?? [];
            const canvasWidth = def?.canvasSettings?.width || 1920;
            const canvasHeight = def?.canvasSettings?.height || 980;

            const el = document.querySelector(`[data-component-id="${component.id}"]`) as HTMLElement | null;
            const currentDims = getComponentDimensions(component, el, scale * 100);
            const proposedDims = {
                width: Math.max(10, Math.round(newWidth * (componentScale / 100))),
                height: currentDims.height,
            };
            const currentX = component.position?.x ?? 0;
            const currentY = component.position?.y ?? 0;
            const proposedPos = { x: currentX + (isWestHandle ? leftShift : 0), y: currentY };
            const ignore = new Set<string>([component.id]);
            const others = buildCanvasRectsForComponents(allComponents, scale, ignore).map(o => ({ id: o.id, rect: o.rect, shape: o.shape }));

            // Log collision detection input
            devLogger.info('resize.collision.check', {
                componentId: component.id,
                currentPosition: { x: currentX, y: currentY },
                proposedPosition: proposedPos,
                proposedSize: proposedDims,
                currentSize: currentDims,
                widthChange: {
                    before: oldWidthPx,
                    after: newWidth,
                    delta: newWidth - oldWidthPx,
                },
                positionChange: {
                    before: oldPosition,
                    proposed: proposedPos,
                    delta: {
                        x: proposedPos.x - oldPosition.x,
                        y: proposedPos.y - oldPosition.y,
                    },
                },
                otherComponentsCount: others.length,
            });

            const resolved = resolveResizeConstraints({
                componentId: component.id,
                currentPosition: { x: currentX, y: currentY },
                proposedPosition: proposedPos,
                proposedSize: proposedDims,
                canvas: { width: canvasWidth, height: canvasHeight },
                others,
                config: {
                    boundaryPaddingPx: caps.resizeConstraints.boundaryPaddingPx,
                    collisionPaddingPx: caps.resizeConstraints.collisionPaddingPx,
                },
                mode: caps.resizeConstraints.mode,
                allowMoveOutOfExistingOverlap: true,
            });

            // Log collision detection result
            devLogger.info('resize.collision.result', {
                componentId: component.id,
                accepted: resolved.accepted,
                positionAdjustment: {
                    proposed: proposedPos,
                    resolved: resolved.position,
                    adjusted: resolved.position.x !== proposedPos.x || resolved.position.y !== proposedPos.y,
                    delta: {
                        x: resolved.position.x - proposedPos.x,
                        y: resolved.position.y - proposedPos.y,
                    },
                },
            });

            if (!resolved.accepted) {
                toast.warning('Resize not possible: it would overlap another component or exceed the canvas.', 'Resize blocked');
                setResizePreview(null);
                resizeStartObjectWidthsRef.current = null; // Clear captured widths
                return;
            }

            // For E handle (east/right): position should NEVER change - anchor west edge
            // If collision resolver adjusted position, reject the adjustment (width was already constrained above)
            if (isEastHandle && (resolved.position.x !== proposedPos.x || resolved.position.y !== proposedPos.y)) {
                devLogger.warn('resize.east.handle.position.adjustment.rejected', {
                    componentId: component.id,
                    reason: 'E handle resize should not adjust position - position change rejected',
                    proposedPosition: proposedPos,
                    resolvedPosition: resolved.position,
                    note: 'Width was already constrained to fit within canvas bounds',
                });
                // Don't apply position adjustment for E handle - position stays fixed
            } else if (!isEastHandle && (resolved.position.x !== proposedPos.x || resolved.position.y !== proposedPos.y)) {
                // For W handle or other handles: allow position adjustment
                devLogger.warn('resize.collision.position.adjusted', {
                    componentId: component.id,
                    reason: 'Collision detection adjusted position',
                    handle: isWestHandle ? 'w' : 'other',
                    before: proposedPos,
                    after: resolved.position,
                    delta: {
                        x: resolved.position.x - proposedPos.x,
                        y: resolved.position.y - proposedPos.y,
                    },
                });
                finalPosition = resolved.position;
                updateComponent(component.id, { position: resolved.position });
            }
        }
        
        // Log width calculation for debugging
        devLogger.info('resize.width.calculated', {
            componentId: component.id,
            componentType: component.type,
            widthRatio,
            before: {
                componentWidth: oldWidthPx,
                labelWidth: currentLabelWidth,
                inputWidth: currentInputWidth,
                helpWidth: currentHelpWidth,
            },
            after: {
                componentWidth: newWidth,
                labelWidth: newLabelWidth,
                inputWidth: newInputWidth,
                helpWidth: newHelpWidth,
            },
            maxLength,
            scaleFactor,
            widthDelta,
        });
        
        if (!hasWidthChange) {
            setResizePreview(null);
            resizeStartObjectWidthsRef.current = null; // Clear captured widths
            setTimeout(() => {
                const snapshotAfter = captureComponentSnapshot(component, smartBorderContainerRef);
                devLogger.info('fieldshell.resize.commit', {
                    componentBefore: snapshotBefore,
                    componentAfter: snapshotAfter,
                    handle: isWestHandle ? 'w' : 'e',
                    finalProps: {
                        width: component.props.width,
                        labelWidthOverride: component.props.labelWidthOverride,
                        inputWidthOverride: component.props.inputWidthOverride,
                        helpWidthOverride: component.props.helpWidthOverride,
                    },
                    duration: 0,
                    note: 'noop-resize: width unchanged',
                });
            }, 0);
            return;
        }

        // ═══════════════════════════════════════════════════════════════
        // ATTEMPT 12 (v2): INPUT-ONLY WIDTH ADJUSTMENT WITH LOCKED LABEL/HELP
        // E/W resize should ONLY adjust input width, keeping label/help fixed.
        // We must SET labelWidthOverride/helpWidthOverride to current DOM values
        // to lock them in place, otherwise grid columns use 1fr and redistribute.
        // ═══════════════════════════════════════════════════════════════
        
        // widthDelta is already calculated above as: newWidth - oldWidthPx
        
        // Get current widths from DOM or existing overrides (use existing override if set, else measured)
        // Ensure label/help widths are at least minLabelWidth/minHelpWidth to prevent text wrapping
        // Use Math.ceil to prevent sub-pixel precision loss that causes text wrapping
        const rawLabelWidth = component.props.labelWidthOverride ?? Math.ceil(measuredLabelWidth ?? currentLabelWidth);
        const rawHelpWidth = component.props.helpWidthOverride ?? Math.ceil(measuredHelpWidth ?? currentHelpWidth);
        const lockedLabelWidth = Math.max(rawLabelWidth, minLabelWidth);
        const lockedHelpWidth = Math.max(rawHelpWidth, minHelpWidth);
        const currentInputWidthPx = component.props.inputWidthOverride ?? measuredInputWidth ?? currentInputWidth;
        
        devLogger.info('resize.lockedWidths.calculated', {
            componentId: component.id,
            label: {
                propsOverride: component.props.labelWidthOverride,
                measured: measuredLabelWidth,
                current: currentLabelWidth,
                raw: rawLabelWidth,
                min: minLabelWidth,
                locked: lockedLabelWidth,
                usedMin: lockedLabelWidth === minLabelWidth,
            },
            help: {
                propsOverride: component.props.helpWidthOverride,
                measured: measuredHelpWidth,
                current: currentHelpWidth,
                raw: rawHelpWidth,
                min: minHelpWidth,
                locked: lockedHelpWidth,
                usedMin: lockedHelpWidth === minHelpWidth,
            },
        });

        const fixedLabelWidth = labelInInputRow ? lockedLabelWidth : 0;
        const fixedHelpWidth = helpInInputRow ? lockedHelpWidth : 0;
        
        // ═══════════════════════════════════════════════════════════════
        // ATTEMPT 12 v8.3: Calculate input to fill remaining space
        // Input = newWidth - fixedObjectsInInputRow - totalExtras
        // totalExtras includes: column gaps + grid padding + border + SmartBorder padding
        // This ensures input fills exactly the space between label and help.
        // ═══════════════════════════════════════════════════════════════
        const remainingForInput = newWidth - fixedLabelWidth - fixedHelpWidth - totalExtras;
        const adjustedInputWidth = Math.max(minInputWidth, Math.round(remainingForInput));
        
        // Calculate what the sum of overrides would be
        const calculatedWidth = fixedLabelWidth + adjustedInputWidth + fixedHelpWidth + totalExtras;
        
        // If input hit minimum and sum exceeds target width, expand component to fit
        if (calculatedWidth > newWidth) {
            devLogger.info('resize.width.minInputAdjustment', {
                componentId: component.id,
                reason: 'Input hit minimum, expanding component to fit',
                before: newWidth,
                after: calculatedWidth,
                inputHitMinimum: true,
                minInputWidth,
                adjustedInputWidth,
            });
            newWidth = Math.round(calculatedWidth);
        }
        
        // ═══════════════════════════════════════════════════════════════
        // COMPREHENSIVE WIDTH COMPARISON LOG
        // Shows BEFORE vs AFTER with sum verification
        // ═══════════════════════════════════════════════════════════════
        const beforeSum =
            (labelInInputRow ? currentLabelWidth : 0) +
            currentInputWidth +
            (helpInInputRow ? currentHelpWidth : 0) +
            totalExtras;
        const afterSum = fixedLabelWidth + adjustedInputWidth + fixedHelpWidth + totalExtras;
        // Note: afterSum should now always equal newWidth (after minInput adjustment)
        
        devLogger.info('resize.width.comparison', {
            componentId: component.id,
            direction: widthDelta > 0 ? 'EXPAND' : 'SHRINK',
            widthDelta,
            
            BEFORE: {
                componentWidth: oldWidthPx,
                labelWidth: labelInInputRow ? currentLabelWidth : 0,
                inputWidth: currentInputWidth,
                helpWidth: helpInInputRow ? currentHelpWidth : 0,
                totalExtras: totalExtras,
                SUM: beforeSum,
                sumMatchesComponent: Math.abs(beforeSum - oldWidthPx) < 1,
            },
            
            AFTER: {
                componentWidth: newWidth,
                labelWidth: fixedLabelWidth,
                inputWidth: adjustedInputWidth,
                helpWidth: fixedHelpWidth,
                totalExtras: totalExtras,
                SUM: afterSum,
                sumMatchesComponent: Math.abs(afterSum - newWidth) < 1,
            },
            
            EXTRAS_BREAKDOWN: {
                columnGaps: columnGapPx * inputRowGapCount,
                smartBorderPadding: 10, // 5px each side
                gridPaddingLeft: paddingLeftPx,
                gridPaddingRight: paddingRightPx,
                borderLeft: borderLeftPx,
                borderRight: borderRightPx,
                totalExtras: totalExtras,
            },
            
            CHANGES: {
                labelChange: labelInInputRow ? (lockedLabelWidth - currentLabelWidth) : 0,
                inputChange: adjustedInputWidth - currentInputWidth,
                helpChange: helpInInputRow ? (lockedHelpWidth - currentHelpWidth) : 0,
            },
            
            remainingForInput,
            minInputWidth,
        });
        
        // Update component width (use preview width - matches user drag position)
        // Grid will use explicit column widths from overrides
        // NOTE: Do NOT set inputWidthMode here - it conflicts with inputWidthOverride.
        // When inputWidthMode is 'fill', the input renderer ignores inputWidthOverride.
        // Instead, we rely on explicit width overrides for all objects.
        const updates: any = { 
            width: `${newWidth}px`,  // Use preview width (matches drag position)
            // LOCK label/help widths to current DOM values (not recalculated)
            labelWidthOverride: lockedLabelWidth,
            helpWidthOverride: lockedHelpWidth,
        };

        if (component.type === 'submit-button') {
            updates.actionWidthOverride = Math.round(newWidth);
        }

        if (!isDropdownSplit) {
            // Input absorbs all width change
            updates.inputWidthOverride = adjustedInputWidth;
        } else if (component.props.inputWidthOverride !== undefined) {
            // Preserve explicit dropdown width (set via input-only handle).
            updates.inputWidthOverride = component.props.inputWidthOverride;
        }

        updateComponentProps(component.id, updates);
        
        // For W handle: adjust position to keep East edge anchored
        if (isWestHandle && leftShift !== 0) {
            const newX = currentX + leftShift;
            
            // Calculate edge positions for logging
            const westEdgeBefore = oldPosition.x ?? 0;
            const eastEdgeBefore = (oldPosition.x ?? 0) + oldWidthPx;
            const westEdgeAfter = newX;
            const eastEdgeAfter = newX + newWidth;
            const previewEastEdge = previewData?.leftShift !== undefined ? (oldPosition.x ?? 0) + previewData.leftShift + (previewData.width ?? oldWidthPx) : eastEdgeBefore;
            const eastEdgeSnapDelta = eastEdgeAfter - previewEastEdge;
            
            finalPosition = { x: newX, y: currentY };
            updateComponent(component.id, { position: finalPosition });
            
            // Get canvas boundaries for logging
            const canvasSettings = useBuilderStore.getState().formDefinition?.canvasSettings;
            const canvasWidth = canvasSettings?.width || 1920;
            const gapFromRightAfter = canvasWidth - eastEdgeAfter;
            const gapFromLeftAfter = westEdgeAfter;
            
            // Log commit edge position with canvas boundaries
            devLogger.info('resize.commit.edge.position', {
                componentId: component.id,
                handle: 'w',
                westEdge: { before: westEdgeBefore, after: westEdgeAfter },
                eastEdge: { before: eastEdgeBefore, after: eastEdgeAfter },
                previewEastEdge,
                eastEdgeSnapDelta,
                expectedEastEdgeDelta: 0, // Should stay anchored
                actualEastEdgeDelta: eastEdgeAfter - eastEdgeBefore,
                canvasBoundaries: {
                    left: 0,
                    right: canvasWidth
                },
                gapsFromCanvasEdges: {
                    left: gapFromLeftAfter,
                    right: gapFromRightAfter
                }
            });
            
            devLogger.info('resize.commit.width', {
                componentId: component.id,
                componentType: component.type,
                handle: 'w',
                before: {
                    width: oldWidthPx,
                    position: oldPosition,
                    bounds: bounds ? { x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height } : null,
                },
                after: {
                    width: newWidth,
                    position: { x: newX, y: currentY },
                    expectedDisplayWidth: newWidth * (componentScale / 100),
                    objectWidths: { label: newLabelWidth, input: newInputWidth, help: newHelpWidth },
                },
                scale: componentScale,
                positionAdjustment: { oldX: currentX, newX, leftShift },
            });
        } else {
            // E handle: log edge positions
            const westEdgeBefore = oldPosition.x ?? 0;
            const eastEdgeBefore = (oldPosition.x ?? 0) + oldWidthPx;
            const westEdgeAfter = oldPosition.x ?? 0;
            const eastEdgeAfter = (oldPosition.x ?? 0) + newWidth;
            
            // Get canvas boundaries for logging
            const canvasSettings = useBuilderStore.getState().formDefinition?.canvasSettings;
            const canvasWidth = canvasSettings?.width || 1920;
            const gapFromRightBefore = canvasWidth - eastEdgeBefore;
            const gapFromRightAfter = canvasWidth - eastEdgeAfter;
            const gapFromLeftAfter = westEdgeAfter;
            
            devLogger.info('resize.commit.edge.position', {
                componentId: component.id,
                handle: 'e',
                westEdge: { before: westEdgeBefore, after: westEdgeAfter },
                eastEdge: { before: eastEdgeBefore, after: eastEdgeAfter },
                expectedEastEdgeDelta: newWidth - oldWidthPx,
                actualEastEdgeDelta: eastEdgeAfter - eastEdgeBefore,
                canvasBoundaries: {
                    left: 0,
                    right: canvasWidth
                },
                gapsFromCanvasEdges: {
                    before: {
                        left: westEdgeBefore,
                        right: gapFromRightBefore
                    },
                    after: {
                        left: gapFromLeftAfter,
                        right: gapFromRightAfter
                    }
                }
            });
            
            devLogger.info('resize.commit.width', {
                componentId: component.id,
                componentType: component.type,
                handle: 'e',
                before: {
                    width: oldWidthPx,
                    position: oldPosition,
                    bounds: bounds ? { x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height } : null,
                },
                after: {
                    width: newWidth,
                    expectedDisplayWidth: newWidth * (componentScale / 100),
                    objectWidths: { label: newLabelWidth, input: newInputWidth, help: newHelpWidth },
                },
                scale: componentScale,
            });
        }
        
        setResizePreview(null);
        resizeStartObjectWidthsRef.current = null; // Clear captured widths
        setTimeout(() => {
            const updatedComponent = {
                ...component,
                props: { ...component.props, ...updates },
                position: finalPosition,
            };
            const snapshotAfter = captureComponentSnapshot(updatedComponent, smartBorderContainerRef);
            devLogger.info('fieldshell.resize.commit', {
                componentBefore: snapshotBefore,
                componentAfter: snapshotAfter,
                handle: isWestHandle ? 'w' : 'e',
                finalProps: {
                    width: `${newWidth}px`,
                    // ATTEMPT 12 v2: Label/help locked to current DOM, input absorbs delta
                    labelWidthOverride: updates.labelWidthOverride,   // Locked to current DOM
                    inputWidthOverride: updates.inputWidthOverride,   // Adjusted by delta
                    helpWidthOverride: updates.helpWidthOverride,     // Locked to current DOM
                },
                attempt12Note: 'Label/help locked to current DOM values; input absorbs all width delta',
                duration: 0,
            });
        }, 0);
    }, [component.id, component.position, component.props, resizePreview, updateComponentProps, updateComponent, componentScale, fieldStyles, scale, toast, actualDomWidth]);

    // Spacing change handler (N/S handles for non-textarea)
    const handleSpacingChange = useCallback((spacingType: 'labelGap' | 'inputHelpGap', newValue: number) => {
        const bounds = smartBorderContainerRef.current?.getBoundingClientRect();
        devLogger.info('resize.commit.spacing', {
            componentId: component.id,
            componentType: component.type,
            spacingType,
            handle: spacingType === 'labelGap' ? 'n' : 's',
            before: {
                labelGap: currentLabelGap,
                inputHelpGap: currentInputHelpGap,
                position: component.position,
                bounds: bounds ? { x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height } : null,
            },
            after: {
                [spacingType]: newValue,
            },
        });
        
        if (spacingType === 'labelGap') {
            updateComponentProps(component.id, { labelGapOverride: newValue });
        } else {
            updateComponentProps(component.id, { inputHelpGapOverride: newValue });
        }
        setResizePreview(null);
    }, [component.id, component.type, component.position, currentLabelGap, currentInputHelpGap, updateComponentProps]);

    // Height change handler (S handle for textarea)
    const handleHeightChange = useCallback((newHeight: number) => {
        const bounds = smartBorderContainerRef.current?.getBoundingClientRect();
        devLogger.info('resize.commit.height', {
            componentId: component.id,
            componentType: component.type,
            handle: 's',
            before: {
                height: component.props.height,
                position: component.position,
                bounds: bounds ? { x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height } : null,
            },
            after: {
                height: newHeight,
            },
        });
        
        updateComponentProps(component.id, { height: newHeight });
        setResizePreview(null);
    }, [component.id, component.type, component.position, component.props.height, updateComponentProps]);

    // Vertical resize commit (N/S) with height-first then spacing behavior
    const handleVerticalResizeEnd = useCallback((handle: 'n' | 's', deltaY: number) => {
        if (component.type === 'submit-button') {
            const canvasScaleFactor = scale || 1.0;
            const scaleFactor = componentScale / 100;
            const effectiveScaleFactor = canvasScaleFactor * scaleFactor;
            const baseHeightDelta = effectiveScaleFactor !== 0 ? deltaY / effectiveScaleFactor : deltaY;

            const measuredButtonHeightScreen =
                captureComponentSnapshot(component, smartBorderContainerRef)?.objectMetrics?.button?.rect?.height ??
                smartBorderContainerRef.current?.getBoundingClientRect()?.height ??
                fieldStyles.computed.inputHeight;
            const measuredButtonHeight =
                effectiveScaleFactor > 0
                    ? measuredButtonHeightScreen / effectiveScaleFactor
                    : measuredButtonHeightScreen;

            const startHeight =
                resizePreview?.startHeight ??
                submitButtonStartHeightRef.current ??
                component.props.height ??
                measuredButtonHeight;

            const minHeightPx = 28;
            const maxHeightPx = 240;
            const unclampedHeight = startHeight + baseHeightDelta;
            const finalHeight = resizePreview?.height ?? Math.max(minHeightPx, Math.min(maxHeightPx, unclampedHeight));

            const currentX = component.position?.x ?? 0;
            const currentY = component.position?.y ?? 0;
            const appliedShift = 0;

            updateComponent(component.id, {
                props: { ...component.props, height: Math.round(finalHeight) },
                position: component.position,
            });

            setResizePreview(null);
            submitButtonStartHeightRef.current = null;
            return;
        }

        const scaleFactor = componentScale / 100;
        const currentInputHeight = fieldStyles.computed.inputHeight;
        const minInputHeight = 28 * scaleFactor;
        const maxInputHeight = 240 * scaleFactor;
        
        // Track which constraints were applied
        const constraintsApplied: string[] = [];

        // Prefer the last preview state to avoid losing the peak value when user drags back before releasing
        const previewState = lastVerticalPreviewRef.current;
        const requestedInputHeight = currentInputHeight + deltaY;
        const finalInputHeight = previewState?.inputHeight ?? Math.max(minInputHeight, Math.min(maxInputHeight, requestedInputHeight));
        
        // Track height constraints
        if (requestedInputHeight < minInputHeight) {
            constraintsApplied.push(`inputHeight: ${requestedInputHeight.toFixed(1)}px -> ${finalInputHeight.toFixed(1)}px (MIN: ${minInputHeight}px)`);
        } else if (requestedInputHeight > maxInputHeight) {
            constraintsApplied.push(`inputHeight: ${requestedInputHeight.toFixed(1)}px -> ${finalInputHeight.toFixed(1)}px (MAX: ${maxInputHeight}px)`);
        }

        const unscaledHeight = Math.round(finalInputHeight / scaleFactor);
        const newStyleOverrides = {
            ...(component.props.styleOverrides || {}),
            inputHeight: unscaledHeight,
        };
        const nextProps: FormComponent['props'] = {
            ...component.props,
            styleOverrides: newStyleOverrides,
        };

        let appliedLabelGap: number | undefined = previewState?.labelGap;
        let appliedInputHelpGap: number | undefined = previewState?.inputHelpGap;
        const heightDeltaUsed = finalInputHeight - currentInputHeight;
        const previewTopShift = previewState?.topShift;
        const currentX = component.position?.x ?? 0;
        const currentY = component.position?.y ?? 0;
        let appliedShift = 0;

        // If no preview spacing captured, compute from remaining delta
        if (appliedLabelGap === undefined && appliedInputHelpGap === undefined) {
            let remainingDelta = deltaY - (finalInputHeight - currentInputHeight);
            if (Math.abs(remainingDelta) > 0.1) {
                if (handle === 'n') {
                    const requestedGap = currentLabelGap + remainingDelta;
                    const newGap = Math.max(0, Math.min(48, requestedGap));
                    appliedLabelGap = Math.round(newGap);
                    nextProps.labelGapOverride = appliedLabelGap;
                    
                    // Track gap constraints
                    if (requestedGap < 0) {
                        constraintsApplied.push(`labelGap: ${requestedGap.toFixed(1)}px -> ${appliedLabelGap}px (MIN: 0px)`);
                    } else if (requestedGap > 48) {
                        constraintsApplied.push(`labelGap: ${requestedGap.toFixed(1)}px -> ${appliedLabelGap}px (MAX: 48px)`);
                    }
                    
                    // Log phase transition to gap
                    devLogger.info('resize.phase.transition', {
                        handle: 'n',
                        phase: 'gap',
                        gapType: 'labelGap',
                        value: appliedLabelGap,
                        componentId: component.id,
                    });
                } else {
                    const requestedGap = currentInputHelpGap + remainingDelta;
                    const newGap = Math.max(0, Math.min(48, requestedGap));
                    appliedInputHelpGap = Math.round(newGap);
                    nextProps.inputHelpGapOverride = appliedInputHelpGap;
                    
                    // Track gap constraints
                    if (requestedGap < 0) {
                        constraintsApplied.push(`inputHelpGap: ${requestedGap.toFixed(1)}px -> ${appliedInputHelpGap}px (MIN: 0px)`);
                    } else if (requestedGap > 48) {
                        constraintsApplied.push(`inputHelpGap: ${requestedGap.toFixed(1)}px -> ${appliedInputHelpGap}px (MAX: 48px)`);
                    }
                    
                    // Log phase transition to gap
                    devLogger.info('resize.phase.transition', {
                        handle: 's',
                        phase: 'gap',
                        gapType: 'inputHelpGap',
                        value: appliedInputHelpGap,
                        componentId: component.id,
                    });
                }
            }
        } else {
            if (appliedLabelGap !== undefined) {
                nextProps.labelGapOverride = Math.round(appliedLabelGap);
                // Log phase transition to gap
                devLogger.info('resize.phase.transition', {
                    handle: 'n',
                    phase: 'gap',
                    gapType: 'labelGap',
                    value: appliedLabelGap,
                    componentId: component.id,
                });
            }
            if (appliedInputHelpGap !== undefined) {
                nextProps.inputHelpGapOverride = Math.round(appliedInputHelpGap);
                // Log phase transition to gap
                devLogger.info('resize.phase.transition', {
                    handle: 's',
                    phase: 'gap',
                    gapType: 'inputHelpGap',
                    value: appliedInputHelpGap,
                    componentId: component.id,
                });
            }
        }
        
        // Log phase transition to height (if height changed)
        if (Math.abs(finalInputHeight - currentInputHeight) > 0.1) {
            devLogger.info('resize.phase.transition', {
                handle,
                phase: 'height',
                value: unscaledHeight,
                componentId: component.id,
            });
        }
        
        // Log constraint violations if any occurred (Agent Logging System)
        if (constraintsApplied.length > 0) {
            devLogger.info('resize.constraints.vertical', {
                componentId: component.id,
                componentType: component.type,
                handle,
                constraintsApplied,
                requested: {
                    deltaY,
                },
                actual: {
                    heightChange: finalInputHeight - currentInputHeight,
                    gapChange: {
                        labelGap: appliedLabelGap !== undefined ? appliedLabelGap - currentLabelGap : 0,
                        inputHelpGap: appliedInputHelpGap !== undefined ? appliedInputHelpGap - currentInputHelpGap : 0,
                    },
                },
                reason: 'Height/gap change limited by min/max constraints',
            });
        }

        // Anchor south: adjust y when north handle used (prefer preview topShift for exact visual match)
        if (handle === 'n') {
            const spacingDeltaUsed = appliedLabelGap !== undefined ? appliedLabelGap - currentLabelGap : 0;
            const fallbackShift = -(heightDeltaUsed + spacingDeltaUsed);
            appliedShift = previewTopShift ?? fallbackShift;
        }

        // Log before drop snapshot
        const snapshotBefore = captureComponentSnapshot(component, smartBorderContainerRef);
        devLogger.info('fieldshell.resize.beforeDrop', {
            component: snapshotBefore,
            handle,
            previewProps: { 
                height: finalInputHeight,
                labelGap: appliedLabelGap,
                inputHelpGap: appliedInputHelpGap
            }
        });
        
        if (handle === 'n') {
            // North: update props + position (anchor south)
            const nextPosition = appliedShift !== 0
                ? { x: currentX, y: currentY + appliedShift }
                : { x: currentX, y: currentY };
            useBuilderStore.getState().updateComponent(component.id, { props: nextProps, position: nextPosition });
        } else {
            // South: only props
            useBuilderStore.getState().updateComponentProps(component.id, nextProps);
        }
        
        // Log after drop snapshot
        setTimeout(() => {
            const updatedComponent = {
                ...component,
                props: nextProps,
                position: handle === 'n' && appliedShift !== 0 
                    ? { x: currentX, y: currentY + appliedShift }
                    : component.position
            };
            const snapshotAfter = captureComponentSnapshot(updatedComponent, smartBorderContainerRef);
            devLogger.info('fieldshell.resize.commit', {
                componentBefore: snapshotBefore,
                componentAfter: snapshotAfter,
                handle,
                finalProps: {
                    height: finalInputHeight,
                    labelGap: appliedLabelGap,
                    inputHelpGap: appliedInputHelpGap
                },
                duration: 0 // TODO: Calculate actual duration
            });
        }, 0);
        
        setResizePreview(null);
        lastVerticalPreviewRef.current = null;
    }, [component, componentScale, currentLabelGap, currentInputHelpGap, fieldStyles.computed.inputHeight, resizePreview, scale, updateComponent, updateComponentProps]);

    // Corner resize commit (NW/NE/SE/SW): non-proportional 2-axis resize
    // Equivalent to committing E/W width resize + N/S vertical resize.
    const handleCornerResizeEnd = useCallback((handle: HandlePosition, deltaX: number, deltaY: number, meta?: ResizePointerMeta) => {
        if (!isCornerHandle(handle)) return;
        const { horizontal: horizontalHandle, vertical: verticalHandle } = cornerToEdges(handle);

        // Capture current component geometry for comparison
        const currentPosition = component.position;
        const currentWidth = parseFloat(component.props.width || '300px');
        const currentHeight = component.props.inputHeight ? parseFloat(component.props.inputHeight) : undefined;

        // Preserve vertical preview state BEFORE handleWidthChange clears resizePreview
        const verticalPreviewState = lastVerticalPreviewRef.current ? {
            inputHeight: lastVerticalPreviewRef.current.inputHeight,
            labelGap: lastVerticalPreviewRef.current.labelGap,
            inputHelpGap: lastVerticalPreviewRef.current.inputHelpGap,
            topShift: lastVerticalPreviewRef.current.topShift,
        } : null;

        const widthToCommit = resizePreview?.width;
        const startWidthForFallback = resizePreview?.startWidth ?? cornerResizeStartWidthRef.current;
        const oldWidthBeforeCommit = component.props.width;

        // Calculate expected final position/size based on mouse movement
        const expectedPosition = { ...currentPosition };
        const expectedWidth = currentWidth + deltaX * (horizontalHandle === 'w' ? -1 : 1);
        
        // For W handles, position should shift left by deltaX
        if (horizontalHandle === 'w') {
            expectedPosition.x = currentPosition.x + deltaX;
        }
        
        // For N handles, position should shift up by deltaY
        if (verticalHandle === 'n') {
            expectedPosition.y = currentPosition.y + deltaY;
        }

        devLogger.info('resize.corner.commit.start', {
            componentId: component.id,
            componentType: component.type,
            handle,
            equivalent: { horizontalHandle, verticalHandle },
            mouse: {
                deltaX,
                deltaY,
                client: meta?.client,
                deltaFromStart: meta?.delta,
            },
            current: {
                position: currentPosition,
                width: currentWidth,
                height: currentHeight,
            },
            expected: {
                position: expectedPosition,
                width: expectedWidth,
                positionShift: {
                    x: expectedPosition.x - currentPosition.x,
                    y: expectedPosition.y - currentPosition.y,
                },
                widthChange: expectedWidth - currentWidth,
            },
            // Important invariant: corners must NOT change componentScale
            componentScale,
            preview: {
                width: widthToCommit,
                startWidth: startWidthForFallback,
                horizontalHandle: (resizePreview as any)?.horizontalHandle,
                leftShift: (resizePreview as any)?.leftShift,
                inputHeight: resizePreview?.inputHeight,
                labelGap: resizePreview?.labelGap,
                inputHelpGap: resizePreview?.inputHelpGap,
                topShift: (resizePreview as any)?.topShift,
            },
            verticalPreviewState,
            oldWidthBeforeCommit,
        });

        // Commit width first (uses resizePreview.horizontalHandle/leftShift/startWidth)
        let widthCommitted = false;
        if (widthToCommit !== undefined) {
            // Calculate expected width delta if we have start width for validation
            let expectedWidthDelta: number | null = null;
            if (startWidthForFallback !== null && startWidthForFallback !== undefined) {
                expectedWidthDelta = widthToCommit - startWidthForFallback;
            }
            
            devLogger.debug('resize.corner.width.commit.attempt', {
                componentId: component.id,
                handle,
                widthToCommit,
                startWidth: startWidthForFallback,
                expectedDelta: expectedWidthDelta,
                oldWidth: oldWidthBeforeCommit,
            });
            
            // Commit width if:
            // 1. We have a start width and the delta is meaningful (>= 0.5px), OR
            // 2. We don't have a start width but widthToCommit is set (let handleWidthChange validate)
            const shouldCommit = expectedWidthDelta === null || Math.abs(expectedWidthDelta) >= 0.5;
            
            if (shouldCommit) {
                handleWidthChange(widthToCommit);
                widthCommitted = true;
            } else {
                devLogger.warn('resize.corner.width.skip.small.delta', {
                    componentId: component.id,
                    handle,
                    widthToCommit,
                    startWidth: startWidthForFallback,
                    expectedDelta: expectedWidthDelta,
                    reason: 'Width change too small to commit',
                });
            }
        } else {
            // Fallback: calculate width from deltaX if preview is missing
            if (Math.abs(deltaX) >= 1 && startWidthForFallback !== null && startWidthForFallback !== undefined) {
                devLogger.warn('resize.corner.missing.width.fallback', {
                    componentId: component.id,
                    handle,
                    resizePreview,
                    deltaX,
                    startWidthForFallback,
                });
                
                const componentScaleFactor = componentScale / 100;
                const canvasScaleFactor = scale || 1.0;
                const effectiveScaleFactor = componentScaleFactor * canvasScaleFactor;
                const baseWidthDelta = effectiveScaleFactor !== 0 ? deltaX / effectiveScaleFactor : deltaX;
                // Use a simple min width for fallback (computeSelectionMinWidthPx is defined later)
                // This fallback path is rare - normally resizePreview.width should be set
                const minWidthPx = 100;
                const newWidth = Math.max(minWidthPx, startWidthForFallback + baseWidthDelta);
                
                devLogger.debug('resize.corner.width.fallback.calculated', {
                    componentId: component.id,
                    handle,
                    deltaX,
                    baseWidthDelta,
                    startWidthForFallback,
                    newWidth,
                });
                
                handleWidthChange(newWidth);
                widthCommitted = true;
            } else {
                devLogger.warn('resize.corner.missing.width.no.fallback', {
                    componentId: component.id,
                    handle,
                    resizePreview,
                    deltaX,
                    startWidthForFallback,
                    reason: 'deltaX too small or startWidth missing',
                });
            }
        }

        // Commit vertical second (uses preserved verticalPreviewState)
        // Only commit if we had any vertical preview or a meaningful delta.
        const hasVerticalPreview = verticalPreviewState?.inputHeight !== undefined
            || verticalPreviewState?.labelGap !== undefined
            || verticalPreviewState?.inputHelpGap !== undefined;
        if (hasVerticalPreview || Math.abs(deltaY) >= 1) {
            // Temporarily restore lastVerticalPreviewRef for handleVerticalResizeEnd
            const originalVerticalRef = lastVerticalPreviewRef.current;
            if (verticalPreviewState) {
                lastVerticalPreviewRef.current = verticalPreviewState;
            }
            handleVerticalResizeEnd(verticalHandle, deltaY);
            // Restore original ref (handleVerticalResizeEnd clears it)
            lastVerticalPreviewRef.current = originalVerticalRef;
        }

        // Clear corner resize start width ref after commit
        cornerResizeStartWidthRef.current = null;

        // Capture final state and compare to expected
        const finalPosition = component.position;
        const finalWidth = parseFloat(component.props.width || '300px');
        const finalHeight = component.props.inputHeight ? parseFloat(component.props.inputHeight) : undefined;

        devLogger.info('resize.corner.commit.complete', {
            componentId: component.id,
            handle,
            widthCommitted,
            verticalCommitted: hasVerticalPreview || Math.abs(deltaY) >= 1,
            final: {
                position: finalPosition,
                width: finalWidth,
                height: finalHeight,
            },
            expected: {
                position: expectedPosition,
                width: expectedWidth,
            },
            discrepancy: {
                position: {
                    x: finalPosition.x - expectedPosition.x,
                    y: finalPosition.y - expectedPosition.y,
                },
                width: finalWidth - expectedWidth,
            },
            match: {
                positionX: Math.abs(finalPosition.x - expectedPosition.x) < 1,
                positionY: Math.abs(finalPosition.y - expectedPosition.y) < 1,
                width: Math.abs(finalWidth - expectedWidth) < 1,
            },
        });
    }, [component.id, component.type, component.props.width, component.position, componentScale, handleWidthChange, handleVerticalResizeEnd, resizePreview, scale]);

    const [parentWidth, setParentWidth] = useState<number | null>(null);
    const componentRef = useRef<HTMLElement | null>(null);

    useEffect(() => {
        const node = componentRef.current;
        const parent = node?.parentElement;
        if (!parent) return;

        const measure = () => setParentWidth(parent.getBoundingClientRect().width);
        measure();

        const ro = new ResizeObserver(measure);
        ro.observe(parent);
        window.addEventListener('resize', measure);
        return () => {
            ro.disconnect();
            window.removeEventListener('resize', measure);
        };
    }, [scale]);

    // Track if we're currently resizing to disable dragging during resize
    const [isResizingState, setIsResizingState] = React.useState(false);
    const [frozenGridTemplateColumns, setFrozenGridTemplateColumns] = React.useState<string | null>(null);

    // Ref to the outer component wrapper (relative). Used for object-level (input) resize handle positioning.
    const outerContainerRef = useRef<HTMLDivElement | null>(null);
    
    // NEW: Ref for SmartBorder container (used for ResizeHandles and collision detection)
    const smartBorderContainerRef = useRef<HTMLDivElement | null>(null);

    const clearFrozenGridColumns = useCallback((reason: string) => {
        if (!frozenGridTemplateColumns) return;
        devLogger.debug('resize.grid.freeze.clear', {
            componentId: component.id,
            reason,
            gridTemplateColumns: frozenGridTemplateColumns,
        });
        setFrozenGridTemplateColumns(null);
    }, [component.id, frozenGridTemplateColumns]);
    
    // Calculate actual pixel width when width is Auto (undefined) or percentage
    // This is critical: ResizeHandles needs actual pixel width, not percentage or undefined
    useEffect(() => {
        const widthProp = component.props.width;
        const isPercentage = widthProp?.endsWith('%');
        const isAuto = !widthProp || widthProp.trim() === '' || widthProp.toLowerCase() === 'auto';
        const isPixelWidth = widthProp?.endsWith('px');
        
        // For explicit pixel widths, don't measure
        if (isPixelWidth) {
            setActualDomWidth(null);
            return;
        }
        
        // For percentage widths, calculate from canvas width (don't measure DOM - it may be wrong due to scale/expansion)
        if (isPercentage) {
            const formDef = useBuilderStore.getState().formDefinition;
            const canvasWidth = formDef?.canvasSettings?.width || 1920;
            const percentage = parseFloat(widthProp);
            if (!isNaN(percentage)) {
                const calculatedWidth = Math.round((canvasWidth * percentage) / 100);
                setActualDomWidth(calculatedWidth);
                devLogger.debug('resize.handle.width.percentage.calculated', {
                    componentId: component.id,
                    propsWidth: widthProp,
                    canvasWidth,
                    percentage,
                    calculatedWidth,
                });
                return;
            }
        }
        
        // For Auto (undefined) widths, measure actual DOM width
        // Note: This measures the outer container, which may be expanded for inputWidthOverride
        // But for Auto width, we want the actual rendered width
        const outerElement = outerContainerRef.current;
        if (!outerElement) {
            // Ref not ready yet, try again after a short delay
            const timer = setTimeout(() => {
                const el = outerContainerRef.current;
                if (el && el.offsetWidth > 0) {
                    setActualDomWidth(el.offsetWidth);
                }
            }, 100);
            return () => clearTimeout(timer);
        }
        
        const measure = () => {
            if (outerElement.offsetWidth > 0) {
                setActualDomWidth(outerElement.offsetWidth);
            }
        };
        
        measure();
        
        // Update when component resizes (e.g., content changes, canvas resize)
        const resizeObserver = new ResizeObserver(measure);
        resizeObserver.observe(outerElement);
        
        return () => {
            resizeObserver.disconnect();
        };
    }, [component.props.width, component.id]); // Re-measure when width prop changes
    
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        isDragging,
    } = useDraggable({ 
        id: component.id,
        data: {
            type: component.type,
            component 
        },
        disabled: isLocked || isResizingState // Disable drag if locked or resizing
    });

    // Handle mouse down for selection (captures Ctrl/Cmd before child handlers)
    // Ctrl+Click (or Cmd+Click on Mac) for additive selection
    const handleMouseDown = (e: React.MouseEvent) => {
        e.stopPropagation(); // Prevent canvas deselection
        if (!isLocked) {
            const isCtrlClick = e.ctrlKey || e.metaKey;
            selectComponent(component.id, isCtrlClick);
        }
    };

    // Inverse-Scale the Transform
    const combinedRef = useCallback((node: HTMLElement | null) => {
        componentRef.current = node;
        setNodeRef(node);
    }, [setNodeRef]);
    
    // NEW: Combined ref for SmartBorder container (merges with componentRef for dnd-kit)
    const smartBorderRef = useCallback((node: HTMLDivElement | null) => {
        smartBorderContainerRef.current = node;
        // Also set as componentRef for dnd-kit if needed
        if (node) {
            componentRef.current = node;
            setNodeRef(node);
        }
    }, [setNodeRef]);

    const outerRef = useCallback((node: HTMLDivElement | null) => {
        outerContainerRef.current = node;
        combinedRef(node as unknown as HTMLElement | null);
    }, [combinedRef]);
    
    // Log ResizeHandles attachment
    useEffect(() => {
        if (isSelected && smartBorderContainerRef.current) {
            devLogger.info('fieldshell.resizehandles.attached', {
                componentId: component.id,
                containerRef: !!smartBorderContainerRef.current,
                handleCount: 8, // Standard handle count
                handles: ['n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se']
            });
        }
    }, [isSelected, component.id]);

    const scaledTransform = transform ? {
        ...transform,
        x: transform.x / scale,
        y: transform.y / scale
    } : null;

    // Parse component width to px (percentages mapped to canvas width from settings)
    // Uses canvasSettings.width to match runtime behavior (PublicFormArtboard)
    const canvasWidth = canvasSettings?.width ?? 1920;
    const parseComponentWidthPx = (val?: string): number => {
        if (!val) return 300;
        if (val.endsWith('%')) {
            const pct = parseInt(val, 10);
            // Use canvasWidth from settings (matches runtime) instead of measured parentWidth
            return Math.max(50, Math.round((pct / 100) * canvasWidth));
        }
        if (val.endsWith('px')) return parseInt(val, 10);
        const n = parseInt(val, 10);
        return Number.isFinite(n) ? n : 300;
    };

    const computeSelectionMinWidthPx = useCallback((): number | undefined => {
        const opts = Array.isArray(component.props.options) ? component.props.options : [];
        const hasExtra = opts.some(o => Boolean((o as any).hasExtraText));
        if (!hasExtra || !fieldStyles?.computed) return undefined;

        const fontFamily = fieldStyles.computed.fontFamily;
        const fontSize = fieldStyles.computed.fontSize;
        const fontWeight = fieldStyles.computed.fontWeight;
        const paddingX = fieldStyles.computed.paddingX ?? 12;
        const borderW = fieldStyles.computed.borderWidth ?? 1;

        const charsWidth = (n: number) =>
            Math.round(
                measureTextWidth('W'.repeat(n), fontFamily, fontSize, fontWeight) +
                    (paddingX * 2) +
                    (borderW * 2)
            );

        const longestLabelW = Math.max(
            0,
            ...opts.map(o =>
                measureTextWidth(
                    String((o as any).label ?? (o as any).value ?? ''),
                    fontFamily,
                    fontSize,
                    fontWeight
                )
            )
        );

        if (component.type === 'dropdown') {
            const arrowSpace = 40;
            const minDropdown = Math.max(
                Math.round(longestLabelW + (paddingX * 2) + (borderW * 2) + arrowSpace),
                Math.round(charsWidth(10) + arrowSpace)
            );
            const minExtra = charsWidth(10);
            const gap = 8;
            return Math.max(120, Math.round(minDropdown + gap + minExtra));
        }

        if (component.type === 'checkbox' || component.type === 'radio') {
            const controlW = 14;
            const controlGap = 8;
            const rowGap = 10;
            const minExtra = charsWidth(5);
            const labelCol = Math.round(controlW + controlGap + longestLabelW);
            return Math.max(120, Math.round((paddingX * 2) + labelCol + rowGap + minExtra));
        }

        return undefined;
    }, [component.props.options, component.type, fieldStyles?.computed]);

    // Calculate dimensions (scale is only controlled by the Component Scale slider now)
    const displayScale = componentScale;
    // Only calculate width if component.props.width is explicitly set (not "Auto" or undefined)
    // This matches runtime behavior in PublicFormArtboard.tsx
    // Robust check: handle undefined, null, empty string, whitespace, and case variations
    const widthValue = component.props.width;
    const hasExplicitWidth = Boolean(
        widthValue && 
        typeof widthValue === 'string' && 
        widthValue.trim() !== '' && 
        widthValue.trim().toLowerCase() !== 'auto'
    );
    
    // Debug logging for width issues
    if (isSelected) {
        devLogger.debug('component.width.check', {
            componentId: component.id,
            widthValue,
            widthType: typeof widthValue,
            hasExplicitWidth,
            smartBorderLayout: hasExplicitWidth ? 'fill' : 'shrink',
        });
    }
    // During horizontal resize, ALWAYS use resizePreview.width if available
    // This ensures the container width updates during drag
    const baseWidthPx = resizePreview?.width ?? (hasExplicitWidth ? parseComponentWidthPx(component.props.width) : undefined);
    // NOTE: DO NOT multiply by displayScale here - the CSS transform: scale() handles visual scaling
    // Multiplying here causes double-scaling which breaks anchor positioning
    const displayWidthPx = baseWidthPx;
    
    // If inputWidthOverride is set and makes SmartBorder wider than component width, expand outer container
    // to match SmartBorder width so resize handles align properly
    // SmartBorder includes 5px padding on each side, so we need to account for that
    const effectiveInputWidthOverride = resizePreview?.inputWidthOverride ?? component.props.inputWidthOverride;
    const smartBorderPadding = 5; // SmartBorder default padding
    const expectedSmartBorderWidth = effectiveInputWidthOverride && baseWidthPx && effectiveInputWidthOverride > baseWidthPx
        ? effectiveInputWidthOverride + (smartBorderPadding * 2) // Add padding on both sides
        : baseWidthPx;
    const shouldExpandForInputWidth = effectiveInputWidthOverride && 
                                       baseWidthPx && 
                                       effectiveInputWidthOverride > baseWidthPx &&
                                       !isResizingState; // Don't expand during resize preview to avoid flicker
    // NOTE: DO NOT multiply by displayScale - CSS transform handles scaling
    const finalDisplayWidthPx = shouldExpandForInputWidth && expectedSmartBorderWidth
        ? expectedSmartBorderWidth
        : displayWidthPx;
    const displayWidth = finalDisplayWidthPx ? `${finalDisplayWidthPx}px` : undefined;
    
    // Log display width calculation during horizontal resize
    if (isResizingState && resizePreview?.width) {
        devLogger.debug('resize.width.calculated', {
            componentId: component.id,
            handle: (resizePreview as any).horizontalHandle,
            previewWidth: resizePreview.width,
            baseWidthPx,
            displayScale,
            displayWidthPx,
            finalDisplayWidthPx,
            displayWidth,
            propsWidth: component.props.width
        });
    }
    const displayHeight = resizePreview?.height ?? component.props.height;
    const previewTopShift = resizePreview?.topShift ?? 0;
    const displayTop = (component.position?.y ?? 0) + previewTopShift;
    // For W handle resize: shift left to keep East edge anchored during preview
    const previewLeftShift = (resizePreview as (typeof resizePreview) & { leftShift?: number })?.leftShift ?? 0;
    const displayLeft = (component.position?.x ?? 0) + previewLeftShift;

    // Recompute styles if scale, spacing, or input height is being previewed
    const previewSpacingOverrides = {
        labelGapOverride: resizePreview?.labelGap ?? spacingOverrides.labelGapOverride,
        inputHelpGapOverride: resizePreview?.inputHelpGap ?? spacingOverrides.inputHelpGapOverride,
    };
    const previewStyleOverrides = {
        ...(component.props.styleOverrides || {}),
        ...(resizePreview?.inputHeight !== undefined
            ? { inputHeight: Math.round(resizePreview.inputHeight / (displayScale / 100)) }
            : {}),
    };

    // Pass scale=100 to render at BASE size; CSS transform handles visual scaling
    const previewFieldStyles = (resizePreview?.scale !== undefined || resizePreview?.labelGap !== undefined || resizePreview?.inputHelpGap !== undefined || resizePreview?.inputHeight !== undefined)
        ? computeFieldStyles(globalStyles, previewStyleOverrides, 100, previewSpacingOverrides)
        : fieldStyles;

    // Log preview application to DOM
    useEffect(() => {
        if (resizePreview && smartBorderContainerRef.current) {
            const bounds = smartBorderContainerRef.current.getBoundingClientRect();
            const previewData = resizePreview as (typeof resizePreview) & { horizontalHandle?: string; leftShift?: number };
            const handle = previewData?.horizontalHandle || (resizePreview?.inputHeight ? 'n/s' : 'unknown');
            
            devLogger.info('resize.preview.applied', {
                componentId: component.id,
                handle,
                previewState: resizePreview,
                layoutContext: {
                    objectLayout: component.props.objectLayout,
                    layoutGroups: component.props.layoutGroups,
                    rowAlignment: component.props.rowAlignment,
                    objectSpacing: component.props.objectSpacing,
                    smartBorderLayout: hasExplicitWidth ? 'fill' : 'shrink',
                },
                appliedStyles: {
                    width: displayWidth,
                    left: displayLeft,
                    top: displayTop,
                    transform: (scaledTransform && !isResizingState) ? CSS.Translate.toString(scaledTransform) : undefined
                },
                domBounds: bounds ? { x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height } : null,
                isVisible: bounds && bounds.width > 0 && bounds.height > 0
            });
        }
    }, [resizePreview, displayWidth, displayLeft, displayTop, component.id, scaledTransform, isResizingState]);

    // Absolute Positioning Logic
    // During resize, disable dnd-kit transform to prevent position interference
    // The transform from dnd-kit can have residual values that cause visual "shake"
    // Check if we're doing a horizontal resize (E/W handle) or vertical resize (N/S handle)
    const previewData = resizePreview as (typeof resizePreview) & { horizontalHandle?: string; leftShift?: number };
    const isHorizontalResize = isResizingState && previewData?.horizontalHandle;
    const isVerticalResize = isResizingState && (resizePreview?.inputHeight !== undefined || resizePreview?.labelGap !== undefined || resizePreview?.inputHelpGap !== undefined);
    
    // Calculate current width for preview ratio calculation (needed for percentage-width components)
    // Must be calculated AFTER isHorizontalResize is defined
    const currentWidthPxForPreview = useMemo(() => {
        const previewDataLocal = resizePreview as (typeof resizePreview) & { horizontalHandle?: string };
        const isHorizontalResizeLocal = isResizingState && previewDataLocal?.horizontalHandle;
        if (isHorizontalResizeLocal && resizePreview?.width) {
            // During resize preview, we need the "before" width to calculate ratio
            if (component.props.width?.endsWith('px')) {
                return parseInt(component.props.width, 10);
            } else if (actualDomWidth !== null) {
                return actualDomWidth;
            } else if (component.props.width?.endsWith('%')) {
                const canvasWidth = useBuilderStore.getState().formDefinition?.canvasSettings?.width || 1920;
                const pct = parseFloat(component.props.width);
                return Math.max(50, Math.round((pct / 100) * canvasWidth));
            }
        }
        return undefined;
    }, [isResizingState, resizePreview, component.props.width, actualDomWidth]);
    
    // For horizontal resize visual preview:
    // Instead of using scaleX (which distorts text), we pass the previewWidth to the component
    // so it actually re-renders at the new width. SmartBorder will automatically adapt.
    // For W handle, we need to adjust position to anchor the East edge.
    let previewPositionLeft = component.position?.x ?? 0;
    
    if (isHorizontalResize && resizePreview?.width) {
        // For W handle: shift left by the width change to anchor East edge
        if (previewData?.horizontalHandle === 'w') {
            const currentWidthPx = parseComponentWidthPx(component.props.width);
            const widthDelta = resizePreview.width - currentWidthPx;
            previewPositionLeft = (component.position?.x ?? 0) - widthDelta;
        }
    }
    
    // Check if component is initially hidden (show with reduced opacity on canvas)
    const isInitiallyHidden = component.props.initialVisibility === 'hidden';

    const style: React.CSSProperties = {
        // No transform during horizontal resize - component re-renders at new width
        // During drag we render from BuilderPage's constrained dragPosition (parity with collision/boundary constraints)
        transform: (!isHorizontalResize && scaledTransform && !isResizingState && !(isDragging && activeId === component.id && !!dragPosition))
            ? CSS.Translate.toString(scaledTransform)
            : undefined,
        position: 'absolute',
        // During horizontal resize preview, adjust position for W handle anchoring
        left: (isDragging && activeId === component.id && dragPosition) ? dragPosition.x : (isHorizontalResize ? previewPositionLeft : displayLeft),
        top: (isDragging && activeId === component.id && dragPosition) ? dragPosition.y : displayTop,
        // Only set width when explicitly defined (matches runtime behavior)
        // When width is "Auto" or undefined, container auto-sizes to content (like SmartBorder)
        width: displayWidth,
        zIndex: isDragging ? 100 : (component.style?.zIndex ?? 10),
        // Show hidden components at 50% opacity on canvas (they're invisible in runtime)
        opacity: isInitiallyHidden ? 0.5 : 1,
        // Visual feedback for locked state
        cursor: isLocked ? 'not-allowed' : 'pointer',
    };
    
    // Log preview width and style application during horizontal resize
    if (isHorizontalResize && resizePreview?.width) {
        devLogger.debug('resize.preview.width.applied', {
            componentId: component.id,
            handle: previewData?.horizontalHandle,
            previewWidth: resizePreview.width,
            displayWidth,
            styleWidth: style.width,
            previewPositionLeft,
            displayLeft,
            originalLeft: component.position?.x ?? 0
        });
    }

    // Selection is now handled by SmartBorder - no additional ring needed

    // Legacy layout removed from UI; use Object Layout defaults for any remaining fallback render paths.
    const effectiveLayout = component.props.objectLayout || globalStyles?.defaultObjectLayout || 'vertical';

    // Common resize handles props
    // Use displayWidth (which includes expansion for inputWidthOverride) so handles align with SmartBorder
    // When width is "Auto" (undefined) or percentage, use actual DOM width for resize calculations
    // This is critical: ResizeHandles.parseWidth() returns 300 for percentages, which causes wrong calculations
    const actualWidthForResize = useMemo(() => {
        // If we have an explicit pixel width, use it
        if (displayWidth && displayWidth.endsWith('px')) return displayWidth;
        if (component.props.width && component.props.width.endsWith('px')) return component.props.width;
        
        // For percentage or undefined (Auto), we MUST use calculated/measured width
        // Otherwise ResizeHandles will use 300px default, causing massive calculation errors
        if (actualDomWidth !== null) {
            const widthStr = `${actualDomWidth}px`;
            const isPercentage = component.props.width?.endsWith('%');
            devLogger.debug('resize.handle.width.calculated', {
                componentId: component.id,
                propsWidth: component.props.width,
                actualDomWidth,
                currentWidthForResize: widthStr,
                source: isPercentage ? 'percentage-calculation' : 'dom-measurement',
                reason: isPercentage 
                    ? 'Percentage width - calculated from canvas width' 
                    : 'Auto width - measured from DOM',
            });
            return widthStr;
        }
        
        // Fallback warning if DOM not measured yet
        devLogger.warn('resize.handle.width.measured.fallback', {
            componentId: component.id,
            propsWidth: component.props.width,
            actualDomWidth,
            reason: 'DOM width not measured yet, ResizeHandles will use default (300px) - resize may be incorrect',
        });
        return component.props.width || undefined; // Return percentage if available, otherwise undefined
    }, [displayWidth, component.props.width, actualDomWidth, component.id]);
    
    type ResizeCapturePhase =
        | 'start.beforeGrab'
        | 'start.afterGrab'
        | 'sample'
        | 'beforeDrop'
        | 'afterDrop';

    const resizeCaptureRef = useRef<{
        runId: string;
        handle: HandlePosition;
        start: { x: number; y: number };
        lastLoggedClient?: { x: number; y: number };
        sampleIndex: number;
    } | null>(null);

    const getComponentFromStore = useCallback((id: string): FormComponent | null => {
        try {
            const state = useBuilderStore.getState();
            const def = state.formDefinition;
            if (!def) return null;
            const pages = def.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def.pages ?? []);
            const activePage = pages.find(p => p.id === state.activePageId) || pages[0];
            if (!activePage) return null;
            const findRecursive = (list: FormComponent[]): FormComponent | null => {
                for (const c of list) {
                    if (c.id === id) return c;
                    if (c.children) {
                        const found = findRecursive(c.children);
                        if (found) return found;
                    }
                }
                return null;
            };
            return findRecursive(activePage.components);
        } catch {
            return null;
        }
    }, []);

    const captureHandleRects = useCallback((componentId: string) => {
        if (typeof document === 'undefined') return null;
        const nodes = Array.from(
            document.querySelectorAll(`[data-resize-component-id="${componentId}"][data-resize-handle]`),
        ) as HTMLElement[];
        if (nodes.length === 0) return null;
        const out: Record<string, { x: number; y: number; width: number; height: number }> = {};
        for (const node of nodes) {
            const key = node.getAttribute('data-resize-handle') || 'unknown';
            const r = node.getBoundingClientRect();
            out[key] = { x: r.x, y: r.y, width: r.width, height: r.height };
        }
        return out;
    }, []);

    const captureSmartBorderGeometry = useCallback((componentId: string) => {
        if (typeof document === 'undefined') return null;
        const root = document.querySelector(`[data-component-id="${componentId}"]`) as HTMLElement | null;
        const container = smartBorderContainerRef.current ?? root;
        if (!container) return null;
        const svgPath = container.querySelector('svg path') as SVGPathElement | null;
        const bbox = svgPath
            ? (() => {
                try {
                    const b = svgPath.getBBox();
                    return { x: b.x, y: b.y, width: b.width, height: b.height };
                } catch {
                    return null;
                }
            })()
            : null;
        const pathRect = svgPath ? svgPath.getBoundingClientRect() : null;
        return {
            pathBBox: bbox,
            pathClientRect: pathRect ? { x: pathRect.x, y: pathRect.y, width: pathRect.width, height: pathRect.height } : null,
        };
    }, [smartBorderContainerRef]);

    const beginResizeCapture = useCallback((handle: HandlePosition, meta: ResizePointerMeta | undefined) => {
        if (!meta) return;
        const runId = `cap_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
        resizeCaptureRef.current = {
            runId,
            handle,
            start: { x: meta.client.x, y: meta.client.y },
            lastLoggedClient: undefined,
            sampleIndex: 0,
        };
    }, []);

    const endResizeCapture = useCallback(() => {
        resizeCaptureRef.current = null;
    }, []);

    const scheduleResizeCapture = useCallback((
        phase: ResizeCapturePhase,
        meta: ResizePointerMeta | undefined,
        opts?: { force?: boolean; reason?: string }
    ) => {
        const run = resizeCaptureRef.current;
        if (!run || !meta) return;

        const prev = run.lastLoggedClient ?? run.start;
        const dxPrev = meta.client.x - prev.x;
        const dyPrev = meta.client.y - prev.y;
        const distPrev = Math.sqrt(dxPrev * dxPrev + dyPrev * dyPrev);
        if (phase === 'sample' && !opts?.force && distPrev < 5) return;

        const sampleIndex = phase === 'sample' ? (run.sampleIndex + 1) : run.sampleIndex;
        if (phase === 'sample') run.sampleIndex = sampleIndex;

        const dxStart = meta.client.x - run.start.x;
        const dyStart = meta.client.y - run.start.y;

        // Update last logged client immediately (so next deltaFromPrev is correct)
        run.lastLoggedClient = { x: meta.client.x, y: meta.client.y };

        const widthSource = (() => {
            if (component.props.width?.endsWith('px')) return 'px-prop';
            if (actualDomWidth !== null) {
                return component.props.width?.endsWith('%') ? 'percentage-calculated' : 'dom-measured';
            }
            if (component.props.width?.endsWith('%')) return 'parsed-percentage-fallback';
            return 'default-fallback';
        })();

        const payload = {
            captureRunId: run.runId,
            phase,
            handle: run.handle,
            sampleIndex: phase === 'sample' ? sampleIndex : undefined,
            reason: opts?.reason,
            mouse: {
                client: meta.client,
                start: run.start,
                deltaFromPrev: { x: dxPrev, y: dyPrev },
                deltaFromStart: { x: dxStart, y: dyStart },
                rawDeltaFromPointerdown: meta.delta,
                ts: meta.ts,
            },
            sizing: {
                componentScale,
                canvasScale: scale ?? 1,
                propsWidth: component.props.width,
                labelWidthOverride: component.props.labelWidthOverride,
                inputWidthOverride: component.props.inputWidthOverride,
                helpWidthOverride: component.props.helpWidthOverride,
                inputWidthMode: (component.props as any)?.inputWidthMode,
                actualDomWidth,
                widthSource,
                resizePreview: {
                    width: resizePreview?.width,
                    startWidth: (resizePreview as any)?.startWidth,
                    horizontalHandle: (resizePreview as any)?.horizontalHandle,
                    leftShift: (resizePreview as any)?.leftShift,
                },
                cornerStartWidth: cornerResizeStartWidthRef.current,
            },
            layout: {
                objectLayout: component.props.objectLayout,
                layoutGroups: component.props.layoutGroups,
                gridLayout: component.props.gridLayout,
            },
        };

        // Ensure DOM has time to update before capturing measurements
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                const liveComponent = getComponentFromStore(component.id) ?? component;
                const snapshot = captureComponentSnapshot(liveComponent, smartBorderContainerRef);
                const handleRects = captureHandleRects(component.id);
                const smartBorderGeo = captureSmartBorderGeometry(component.id);

                devLogger.info('resize.capture', {
                    ...payload,
                    componentId: component.id,
                    componentType: component.type,
                    geometry: {
                        smartBorder: smartBorderGeo,
                        handles: handleRects,
                    },
                    snapshot,
                });
            });
        });
    }, [captureHandleRects, captureSmartBorderGeometry, component, getComponentFromStore, smartBorderContainerRef]);

    const resizeHandleProps = {
        isSelected: isSelected && !isLocked,
        currentWidth: actualWidthForResize, // Use actual DOM width when Auto
        currentHeight: fieldStyles.computed.inputHeight,
        currentScale: componentScale,
        currentLabelGap,
        currentInputHelpGap,
        // Two-phase N/S resize context (optional; handled in SortableComponent callbacks)
        currentInputHeight: fieldStyles.computed.inputHeight,
        minInputHeight: 28 * (componentScale / 100),
        maxInputHeight: 240 * (componentScale / 100),
        labelGapMin: 0,
        labelGapMax: 48,
        inputHelpGapMin: 0,
        inputHelpGapMax: 48,
        componentType: component.type,
        componentId: component.id,
        onResizeStart: (handle: HandlePosition, meta?: ResizePointerMeta) => {
            beginResizeCapture(handle, meta);
            scheduleResizeCapture('start.beforeGrab', meta, { force: true, reason: 'before handleResizeStart' });
            handleResizeStart(handle);
            scheduleResizeCapture('start.afterGrab', meta, { force: true, reason: 'after handleResizeStart' });
        },
        onResize: (deltaWidth: number, deltaHeight: number, handle: HandlePosition, meta?: ResizePointerMeta) => {
            handleResize(deltaWidth, deltaHeight, handle);
            scheduleResizeCapture('sample', meta);
        },
        onWidthChange: (newWidth: number, meta?: ResizePointerMeta) => {
            scheduleResizeCapture('beforeDrop', meta, { force: true, reason: 'before width commit' });
            // Commit using preview width when available (accounts for canvas scale)
            const commitWidth = resizePreview?.width ?? newWidth;
            handleWidthChange(commitWidth);
            setIsResizingState(false);
            useBuilderStore.getState().setResizingComponentId(null); // Clear to re-enable drag
            setTimeout(() => clearFrozenGridColumns('width-commit'), 50);
            scheduleResizeCapture('afterDrop', meta, { force: true, reason: 'after width commit' });
            endResizeCapture();
        },
        onCornerResizeEnd: (handle: HandlePosition, deltaX: number, deltaY: number, meta?: ResizePointerMeta) => {
            scheduleResizeCapture('beforeDrop', meta, { force: true, reason: 'before corner commit' });
            handleCornerResizeEnd(handle, deltaX, deltaY, meta);
            setIsResizingState(false);
            useBuilderStore.getState().setResizingComponentId(null); // Clear to re-enable drag
            setTimeout(() => clearFrozenGridColumns('corner-commit'), 50);
            scheduleResizeCapture('afterDrop', meta, { force: true, reason: 'after corner commit' });
            endResizeCapture();
        },
        onSpacingChange: handleSpacingChange,
        onHeightChange: (newHeight: number) => {
            handleHeightChange(newHeight);
            setIsResizingState(false);
            useBuilderStore.getState().setResizingComponentId(null); // Clear to re-enable drag
        },
        onVerticalResizeEnd: (handle: 'n' | 's', deltaY: number, meta?: ResizePointerMeta) => {
            scheduleResizeCapture('beforeDrop', meta, { force: true, reason: 'before vertical commit' });
            handleVerticalResizeEnd(handle, deltaY);
            setIsResizingState(false);
            useBuilderStore.getState().setResizingComponentId(null); // Clear to re-enable drag
            scheduleResizeCapture('afterDrop', meta, { force: true, reason: 'after vertical commit' });
            endResizeCapture();
        },
        minWidth: (() => {
            // Compute min width inline to avoid initialization order issues
            // This matches the logic in computeSelectionMinWidthPx but avoids the dependency
            const opts = Array.isArray(component.props.options) ? component.props.options : [];
            const hasExtra = opts.some(o => Boolean((o as any).hasExtraText));
            if (!hasExtra || !fieldStyles?.computed) return 100;
            
            const fontFamily = fieldStyles.computed.fontFamily;
            const fontSize = fieldStyles.computed.fontSize;
            const fontWeight = fieldStyles.computed.fontWeight;
            const paddingX = fieldStyles.computed.paddingX ?? 12;
            const borderW = fieldStyles.computed.borderWidth ?? 1;
            
            const charsWidth = (n: number) =>
                Math.round(
                    measureTextWidth('W'.repeat(n), fontFamily, fontSize, fontWeight) +
                        (paddingX * 2) +
                        (borderW * 2)
                );
            
            const longestLabelW = Math.max(
                0,
                ...opts.map(o =>
                    measureTextWidth(
                        String((o as any).label ?? (o as any).value ?? ''),
                        fontFamily,
                        fontSize,
                        fontWeight
                    )
                )
            );
            
            if (component.type === 'dropdown') {
                const arrowSpace = 40;
                const minDropdown = Math.max(
                    Math.round(longestLabelW + (paddingX * 2) + (borderW * 2) + arrowSpace),
                    Math.round(charsWidth(10) + arrowSpace)
                );
                const minExtra = charsWidth(10);
                const gap = 8;
                return Math.max(120, Math.round(minDropdown + gap + minExtra));
            } else if (component.type === 'checkbox' || component.type === 'radio') {
                const controlW = 14;
                const controlGap = 8;
                const rowGap = 10;
                const minExtra = charsWidth(5);
                const labelCol = Math.round(controlW + controlGap + longestLabelW);
                return Math.max(120, Math.round((paddingX * 2) + labelCol + rowGap + minExtra));
            }
            
            return 100;
        })(),
        minHeight: 40,
    };
    
    // Submit button should support full resize (NSWE) so users can size it accurately.
    const buttonResizeHandleProps = resizeHandleProps;

    // ───────────────────────────────────────────────────────────────
    // Input-only width resize (object-level)
    // ───────────────────────────────────────────────────────────────

    const handleInputWidthResizeStart = useCallback(() => {
        setIsResizingState(true);
        useBuilderStore.getState().setResizingComponentId(component.id);
        devLogger.info('resize.input.start', { componentId: component.id });
    }, [component.id]);

    const handleInputWidthResizePreview = useCallback((nextWidthPx: number) => {
        setResizePreview(prev => ({ ...(prev || {}), inputWidthOverride: nextWidthPx }));
        devLogger.debug('resize.input.preview', { componentId: component.id, inputWidthOverride: nextWidthPx });
    }, [component.id]);

    const handleInputWidthResizeCommit = useCallback((finalWidthPx: number) => {
        let next = finalWidthPx;

        // Dropdown: clamp input-only resize so the component width stays fixed and the extra input still has space.
        if (component.type === 'dropdown' && fieldStyles?.computed) {
            const opts = Array.isArray(component.props.options) ? component.props.options : [];
            const hasExtra = opts.some(o => Boolean((o as any).hasExtraText));
            const fontFamily = fieldStyles.computed.fontFamily;
            const fontSize = fieldStyles.computed.fontSize;
            const fontWeight = fieldStyles.computed.fontWeight;
            const paddingX = fieldStyles.computed.paddingX ?? 12;
            const borderW = fieldStyles.computed.borderWidth ?? 1;
            const gap = 8;
            const arrowSpace = 40;

            const charsWidth = (n: number) =>
                Math.round(
                    measureTextWidth('W'.repeat(n), fontFamily, fontSize, fontWeight) +
                        (paddingX * 2) +
                        (borderW * 2)
                );
            const longestLabelW = Math.max(
                0,
                ...opts.map(o =>
                    measureTextWidth(
                        String((o as any).label ?? (o as any).value ?? ''),
                        fontFamily,
                        fontSize,
                        fontWeight
                    )
                )
            );
            const minDropdown = Math.max(
                Math.round(longestLabelW + (paddingX * 2) + (borderW * 2) + arrowSpace),
                Math.round(charsWidth(10) + arrowSpace)
            );
            const minExtra = charsWidth(10);

            next = Math.max(next, minDropdown);
            if (hasExtra) {
                const componentW = parseComponentWidthPx(component.props.width);
                const maxAllowed = Math.max(minDropdown, componentW - gap - minExtra);
                next = Math.min(next, maxAllowed);
            }
        }

        updateComponentProps(component.id, { inputWidthOverride: next });
        devLogger.info('resize.input.commit', { componentId: component.id, inputWidthOverride: next });
        setResizePreview(null);
        setIsResizingState(false);
        useBuilderStore.getState().setResizingComponentId(null);
        // Post-commit: auto-adjust position if expanded/shrank into overlap/boundary.
        const caps = getComponentSurfaceCapabilities(component.type as any, 'canvas');
        if (caps.resizeConstraints.enabled && (caps.resizeConstraints.canvasBoundary || caps.resizeConstraints.collisionAvoidance)) {
            window.setTimeout(() => {
                const state = useBuilderStore.getState();
                const def = state.formDefinition;
                const pages = def?.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def?.pages ?? []);
                const activePage = pages.find(p => p.id === state.activePageId);
                const allComponents = activePage?.components ?? [];
                const canvasWidth = def?.canvasSettings?.width || 1920;
                const canvasHeight = def?.canvasSettings?.height || 980;
                const el = document.querySelector(`[data-component-id="${component.id}"]`) as HTMLElement | null;
                const dims = getComponentDimensions(component, el, state.scale * 100);
                const currentX = component.position?.x ?? 0;
                const currentY = component.position?.y ?? 0;
                const ignore = new Set<string>([component.id]);
                const others = buildCanvasRectsForComponents(allComponents, state.scale, ignore).map(o => ({ id: o.id, rect: o.rect, shape: o.shape }));
                const resolved = resolveResizeConstraints({
                    componentId: component.id,
                    currentPosition: { x: currentX, y: currentY },
                    proposedPosition: { x: currentX, y: currentY },
                    proposedSize: { width: dims.width, height: dims.height },
                    canvas: { width: canvasWidth, height: canvasHeight },
                    others,
                    config: {
                        boundaryPaddingPx: caps.resizeConstraints.boundaryPaddingPx,
                        collisionPaddingPx: caps.resizeConstraints.collisionPaddingPx,
                    },
                    mode: caps.resizeConstraints.mode,
                    allowMoveOutOfExistingOverlap: true,
                });
                if (resolved.accepted && (resolved.position.x !== currentX || resolved.position.y !== currentY)) {
                    useBuilderStore.getState().updateComponent(component.id, { position: resolved.position });
                }
            }, 0);
        }
    }, [component.id, component.position, component.type, updateComponentProps]);

    // ═══════════════════════════════════════════════════════════════
    // UNIVERSAL FIELDSHELL COMPONENTS
    // All input components should use UniversalFieldShell for consistency
    // ═══════════════════════════════════════════════════════════════
    
    // Check if component has structure defined in registry (use UniversalFieldShell)
    const componentDef = ComponentRegistry[component.type];
    const hasUniversalStructure = !!componentDef?.structure;
    
    // Components that should use UniversalFieldShell
    const universalFieldShellTypes = ['first-name', 'last-name', 'email', 'phone', 'text', 'textarea', 'number', 'date', 'dropdown', 'address'];
    
    // Divider uses a special canvas wrapper (absolute + width handling) so that percentage widths
    // (e.g. "100%") resolve against the stage, matching public preview behavior.
    if ((hasUniversalStructure && component.type !== 'divider') || universalFieldShellTypes.includes(component.type)) {
        const caps = getComponentSurfaceCapabilities(component.type as any, 'canvas');
        const structure = componentDef?.structure || getDefaultStructure(component.type);
        const renderers = getRenderersForComponent(component.type, structure, component);
        
        // ARCHITECTURE NOTE (from EPIC-3-ARCHITECTURE-REF.md):
        // "The SVG path serves as the draggable hitbox"
        // Drag listeners are passed to SmartBorder via builderMode, NOT the outer div
        // This ensures drag works via the SmartBorder path, not the container
        
        // Apply component scale transform (use displayScale for preview during corner handle drag)
        const scaleTransform = displayScale !== 100 ? `scale(${displayScale / 100})` : undefined;
        // When componentScaleAnchor is explicitly set, AppearanceSection handles position adjustment
        // to keep the anchor corner fixed. We use transform-origin: top left to avoid double transformation.
        // Only use textAlign-based origin when no explicit anchor is set.
        const anchor = component.props.componentScaleAnchor;
        const scaleOrigin = anchor !== undefined ? 'top left' : // Explicit anchor: position handles anchoring
                           component.props.textAlign === 'right' ? 'top right' : 
                           component.props.textAlign === 'center' ? 'top center' : 'top left';
        
        return (
            <div
                ref={outerRef}
                style={style}
                className="group touch-none relative"
                onMouseDown={handleMouseDown}
                // NOTE: Do NOT spread {...listeners} {...attributes} here
                // Drag is handled by SmartBorder's SVG path (via builderMode.dragListeners)
            >
                <div
                    style={{
                        width: displayWidth,
                        transform: scaleTransform,
                        transformOrigin: scaleOrigin,
                    }}
                >
                    <UniversalFieldShell
                    ref={smartBorderRef}
                    structure={structure}
                    renderers={renderers}
                    surface="canvas"
                    objectLayout={component.props.objectLayout}
                    layoutGroups={component.props.layoutGroups}
                    styleOverrides={component.props.styleOverrides}
                    globalStyles={globalStyles}
                    componentId={component.id}
                    component={component}
                    // For E/W resize: Pass previewWidth for border visual update
                    // frozenGridTemplateColumns prevents internal grid layout changes
                    previewWidth={isHorizontalResize ? resizePreview?.width : undefined}
                    previewHeight={resizePreview?.height}
                    currentWidthPx={currentWidthPxForPreview}
                    previewObjectWidthOverrides={
                        // For E/W resize: pass preview object widths to update grid columns dynamically
                        isHorizontalResize && (resizePreview?.previewLabelWidth !== undefined || 
                                               resizePreview?.previewInputWidth !== undefined || 
                                               resizePreview?.previewHelpWidth !== undefined ||
                                               resizePreview?.previewActionWidth !== undefined)
                            ? {
                                labelWidthOverride: resizePreview.previewLabelWidth,
                                inputWidthOverride: resizePreview.previewInputWidth,
                                helpWidthOverride: resizePreview.previewHelpWidth,
                                actionWidthOverride: resizePreview.previewActionWidth,
                            }
                            // For input-only resize handles (not E/W component resize)
                            : resizePreview?.inputWidthOverride !== undefined
                                ? { inputWidthOverride: resizePreview.inputWidthOverride }
                                : undefined
                    }
                    previewStyleOverrides={isVerticalResize ? previewStyleOverrides : undefined}
                    previewSpacingOverrides={isVerticalResize ? previewSpacingOverrides : undefined}
                    previewScale={undefined}
                    builderMode={{
                        showBorder: true,
                        borderPadding: 5,
                        // Use 'fill' during horizontal resize so SmartBorder expands with container
                        smartBorderLayout: (isHorizontalResize || hasExplicitWidth) ? 'fill' : 'shrink',
                        isSelected: isSelected,
                        isDragging: isDragging,
                        isResizing: isResizingState,
                        dragListeners: listeners,
                        dragAttributes: attributes,
                        containerRef: smartBorderContainerRef,
                        frozenGridTemplateColumns: frozenGridTemplateColumns,
                    }}
                />
                </div>
                {/* Input-only resize handle (does not affect label/help widths) */}
                <InputWidthHandles
                    enabled={isSelected && !isLocked && caps.objectResizeHandles.inputWidthHandle}
                    canvasScale={scale}
                    outerRef={outerContainerRef as unknown as React.RefObject<HTMLElement | null>}
                    inputElementId={`${component.id}-input`}
                    onResizeStart={handleInputWidthResizeStart}
                    onResizePreview={handleInputWidthResizePreview}
                    onResizeCommit={handleInputWidthResizeCommit}
                />
                {/* Resize Handles - positioned relative to SmartBorder container */}
                {isSelected && !isLocked && (
                    <ResizeHandlesWrapper 
                        smartBorderContainerRef={smartBorderContainerRef}
                        outerContainerRef={outerContainerRef}
                        componentId={component.id}
                        forceUpdateKey={`${component.props.width}-${component.props.inputWidthOverride}-${component.props.labelWidthOverride}-${component.props.helpWidthOverride}`}
                    >
                        <ResizeHandles 
                            {...resizeHandleProps}
                        />
                    </ResizeHandlesWrapper>
                )}
            </div>
        );
    }

    // 2. Divider Component - Uses UniversalFieldShell with SmartBorder for collision detection
    if (component.type === 'divider') {
        const componentDef = ComponentRegistry[component.type];
        const structure = componentDef?.structure || getDefaultStructure(component.type);
        const renderers = getRenderersForComponent(component.type, structure, component);
        
        // Divider-specific style calculations for resize preview
        // Use scale=100; CSS transform handles visual scaling
        const styles = computeFieldStyles(globalStyles, component.props.styleOverrides, 100, spacingOverrides);
        const currentBorderWidth = styles.computed.textBorderWidth ?? styles.computed.borderWidth ?? 1;
        const dividerWidth = (component.props.width ?? styles.computed.dividerWidth ?? '100%') as string;
        
        // Parse width (length)
        const currentWidthPx = component.props.width?.endsWith('px') 
            ? parseInt(component.props.width, 10) 
            : (component.props.width?.endsWith('%') 
                ? parseFloat(component.props.width) 
                : 300);
        
        // Custom resize handlers for divider with proper anchoring
        const dividerHandleResize = useCallback((deltaWidth: number, deltaHeight: number, handle: HandlePosition) => {
            if (handle === 'n' || handle === 's') {
                const newBorderWidth = Math.max(1, Math.min(10, currentBorderWidth + (handle === 's' ? deltaHeight : -deltaHeight)));
                const topShift = handle === 'n' ? -deltaHeight : 0;
                setResizePreview({ inputHeight: newBorderWidth, topShift, width: undefined });
                lastVerticalPreviewRef.current = { inputHeight: newBorderWidth, topShift };
            } else if (handle === 'e' || handle === 'w') {
                const baseWidth = currentWidthPx ?? 300;
                const newWidth = baseWidth + deltaWidth;
                const clampedWidth = Math.max(50, newWidth);
                const previewState: any = { width: clampedWidth, horizontalHandle: handle };
                if (handle === 'w') {
                    previewState.leftShift = -(clampedWidth - baseWidth);
                }
                setResizePreview(previewState);
            }
        }, [currentBorderWidth, currentWidthPx]);
        
        const dividerHandleWidthChange = useCallback((newWidth: number) => {
            const currentX = component.position?.x ?? 0;
            const currentY = component.position?.y ?? 0;
            const previewLeftShift = (resizePreview as any)?.leftShift;
            const horizontalHandle = (resizePreview as any)?.horizontalHandle;
            
            if (horizontalHandle === 'w' && previewLeftShift !== undefined && previewLeftShift !== 0) {
                const newX = currentX + previewLeftShift;
                updateComponent(component.id, {
                    props: { width: `${newWidth}px` },
                    position: { x: newX, y: currentY }
                });
            } else {
                updateComponent(component.id, {
                    props: { width: `${newWidth}px` },
                    position: { x: currentX, y: currentY }
                });
            }
            setResizePreview(null);
        }, [component.id, component.position, resizePreview, updateComponent]);
        
        const dividerHandleBorderWidthChange = useCallback((handle: 'n' | 's', deltaY: number) => {
            const previewBorderWidth = lastVerticalPreviewRef.current?.inputHeight;
            const previewTopShift = lastVerticalPreviewRef.current?.topShift;
            const finalBorderWidth = previewBorderWidth ?? Math.max(1, Math.min(10, currentBorderWidth + (handle === 's' ? deltaY : -deltaY)));
            
            const newStyleOverrides = {
                ...(component.props.styleOverrides || {}),
                textBorderWidth: finalBorderWidth,
            };
            
            const currentX = component.position?.x ?? 0;
            const currentY = component.position?.y ?? 0;
            
            if (handle === 'n' && previewTopShift !== undefined) {
                updateComponent(component.id, {
                    props: { styleOverrides: newStyleOverrides },
                    position: { x: currentX, y: currentY + previewTopShift }
                });
            } else {
                updateComponentProps(component.id, { styleOverrides: newStyleOverrides });
            }
            
            setResizePreview(null);
            lastVerticalPreviewRef.current = null;
        }, [component.id, component.position, component.props.styleOverrides, currentBorderWidth, updateComponent, updateComponentProps]);
        
        // Apply position shift from preview during resize
        const previewLeftShift = (resizePreview as any)?.leftShift;
        const previewTopShift = resizePreview?.topShift;
        const displayX = previewLeftShift !== undefined ? (component.position?.x ?? 0) + previewLeftShift : (component.position?.x ?? 0);
        const displayY = previewTopShift !== undefined ? (component.position?.y ?? 0) + previewTopShift : (component.position?.y ?? 0);
        
        // Divider container style - use left/top positioning
        const dividerContainerStyle: React.CSSProperties = {
            position: 'absolute',
            left: displayX,
            top: displayY,
            width: dividerWidth,
            zIndex: isDragging ? 100 : (component.style?.zIndex ?? 10),
            opacity: 1,
            cursor: isLocked ? 'not-allowed' : 'pointer',
            transform: undefined, // Disable dnd-kit transform for divider
        };
        
        const displayWidthPx = resizePreview?.width ?? currentWidthPx;
        const borderWidth = resizePreview?.inputHeight ?? currentBorderWidth;
        
        return (
            <div
                ref={combinedRef}
                style={dividerContainerStyle}
                className="group touch-none relative"
                onMouseDown={handleMouseDown}
                data-component-id={component.id}
                // Drag handled by SmartBorder via builderMode.dragListeners
            >
                <UniversalFieldShell
                    ref={smartBorderRef}
                    structure={structure}
                    renderers={renderers}
                    surface="canvas"
                    objectLayout={component.props.objectLayout}
                    layoutGroups={component.props.layoutGroups}
                    styleOverrides={component.props.styleOverrides}
                    globalStyles={globalStyles}
                    componentId={component.id}
                    component={component}
                    previewWidth={isHorizontalResize ? resizePreview?.width : undefined}
                    previewStyleOverrides={isVerticalResize ? previewStyleOverrides : undefined}
                    previewSpacingOverrides={isVerticalResize ? previewSpacingOverrides : undefined}
                    previewScale={undefined}
                    builderMode={{
                        showBorder: true,
                        borderPadding: 3, // Smaller padding for divider
                        smartBorderLayout: 'fill',
                        isSelected: isSelected,
                        isDragging: isDragging,
                        isResizing: isResizingState,
                        dragListeners: listeners,
                        dragAttributes: attributes,
                        containerRef: smartBorderContainerRef,
                    }}
                />
                {/* Resize Handles - Custom handlers for divider */}
                {isSelected && !isLocked && (
                    <ResizeHandles 
                        {...resizeHandleProps}
                        componentType="divider"
                        hideCornerHandles={true}
                        currentWidth={`${displayWidthPx}px`}
                        currentHeight={borderWidth}
                        onResize={dividerHandleResize}
                        onResizeStart={() => {
                            setIsResizingState(true);
                            useBuilderStore.getState().setResizingComponentId(component.id);
                        }}
                        onWidthChange={(newWidth: number) => {
                            dividerHandleWidthChange(newWidth);
                            setIsResizingState(false);
                            useBuilderStore.getState().setResizingComponentId(null);
                        }}
                        onHeightChange={undefined}
                        onVerticalResizeEnd={(handle: 'n' | 's', deltaY: number) => {
                            dividerHandleBorderWidthChange(handle, deltaY);
                            setIsResizingState(false);
                            useBuilderStore.getState().setResizingComponentId(null);
                        }}
                    />
                )}
            </div>
        );
    }

    // 3. Submit Button - Use UniversalFieldShell if structure available
    if (component.type === 'submit-button') {
        const componentDef = ComponentRegistry[component.type];
        const structure = componentDef?.structure || getDefaultStructure(component.type);
        
        // Check if we should use UniversalFieldShell (when structure is defined)
        if (structure && componentDef?.structure) {
            // Use shared object renderers + surface capabilities (no special casing).
            const renderers = getRenderersForComponent(component.type, structure, component);
            
            // Apply component scale transform (use displayScale for preview during corner handle drag)
            const scaleTransform = displayScale !== 100 ? `scale(${displayScale / 100})` : undefined;
            // Use componentScaleAnchor if set, otherwise fall back to textAlign-based origin
            // This ensures the transform-origin matches the selected anchor for stable scaling
            const anchor = component.props.componentScaleAnchor;
            const scaleOrigin = anchor === 'ne' ? 'top right' :
                               anchor === 'se' ? 'bottom right' :
                               anchor === 'sw' ? 'bottom left' :
                               anchor === 'nw' ? 'top left' :
                               component.props.textAlign === 'right' ? 'top right' : 
                               component.props.textAlign === 'center' ? 'top center' : 'top left';
            
            // Container alignment classes
            const containerAlignClass = component.props.textAlign === 'right' ? 'flex justify-end' :
                                       component.props.textAlign === 'center' ? 'flex justify-center' :
                                       'flex justify-start';
            
            return (
                <div
                    ref={combinedRef}
                    style={style}
                    className="group touch-none relative"
                    onMouseDown={handleMouseDown}
                    // NOTE: Do NOT spread {...listeners} {...attributes} here
                    // Drag is handled by SmartBorder's SVG path (via builderMode.dragListeners)
                >
                    <div 
                        className={containerAlignClass}
                        style={{ 
                            width: displayWidth,
                            transform: scaleTransform,
                            transformOrigin: scaleOrigin,
                        }}
                    >
                        <UniversalFieldShell
                            ref={smartBorderRef}
                            structure={structure}
                            renderers={renderers}
                            surface="canvas"
                            objectLayout={component.props.objectLayout}
                            layoutGroups={component.props.layoutGroups}
                            styleOverrides={component.props.styleOverrides}
                            globalStyles={globalStyles}
                            componentId={component.id}
                            component={component}
                            // For E/W resize: DON'T pass previewWidth - keep component frozen during drag
                            previewWidth={undefined}
                            currentWidthPx={currentWidthPxForPreview}
                            previewStyleOverrides={isVerticalResize ? previewStyleOverrides : undefined}
                            previewSpacingOverrides={isVerticalResize ? previewSpacingOverrides : undefined}
                            previewScale={undefined}
                            builderMode={{
                                showBorder: true,
                                borderPadding: 5,
                                // Use 'fill' layout only when width is explicitly set (not "Auto")
                                smartBorderLayout: hasExplicitWidth ? 'fill' : 'shrink',
                                isSelected: isSelected,
                                isDragging: isDragging,
                                isResizing: isResizingState,
                                dragListeners: listeners,
                                dragAttributes: attributes,
                                containerRef: smartBorderContainerRef,
                            }}
                        />
                    </div>
                    {/* Resize Handles - Only proportional scaling for buttons */}
                            {isSelected && !isLocked && (
                                <ResizeHandles {...buttonResizeHandleProps} />
                            )}
                </div>
            );
        }
        
        // Fallback to original SubmitButtonField rendering
        // Apply component scale transform (use displayScale for preview during corner handle drag)
        const scaleTransform = displayScale !== 100 ? `scale(${displayScale / 100})` : undefined;
        // Use componentScaleAnchor if set, otherwise fall back to textAlign-based origin
        // This ensures the transform-origin matches the selected anchor for stable scaling
        const anchor = component.props.componentScaleAnchor;
        const scaleOrigin = anchor === 'ne' ? 'top right' :
                           anchor === 'se' ? 'bottom right' :
                           anchor === 'sw' ? 'bottom left' :
                           anchor === 'nw' ? 'top left' :
                           component.props.textAlign === 'right' ? 'top right' : 
                           component.props.textAlign === 'center' ? 'top center' : 'top left';
        
        // Container alignment classes
        const containerAlignClass = component.props.textAlign === 'right' ? 'flex justify-end' :
                                   component.props.textAlign === 'center' ? 'flex justify-center' :
                                   'flex justify-start';
        
        return (
            <div
                ref={combinedRef}
                style={style}
                className="group touch-none relative"
                onMouseDown={handleMouseDown}
                {...listeners}
                {...attributes}
            >
                <div 
                    className={containerAlignClass}
                    style={{ 
                        width: displayWidth,
                        transform: scaleTransform,
                        transformOrigin: scaleOrigin,
                    }}
                    data-component-id={component.id}
                >
                    <SubmitButtonField
                        buttonText={component.props.buttonText}
                        buttonAction={component.props.buttonAction}
                        buttonWidth={component.props.buttonWidth}
                        buttonAlign={component.props.buttonAlign}
                        showLoadingState={component.props.showLoadingState}
                        disableUntilValid={component.props.disableUntilValid}
                        showIcon={component.props.showIcon}
                        fieldStyles={previewFieldStyles}
                    />
                </div>
                {/* Resize Handles - Only proportional scaling for buttons */}
                {isSelected && !isLocked && (
                    <ResizeHandles {...buttonResizeHandleProps} />
                )}
            </div>
        );
    }

    // 4. Header Component
    if (component.type === 'header') {
        // Use scale=100; CSS transform handles visual scaling
        const styles = computeFieldStyles(globalStyles, component.props.styleOverrides, 100, spacingOverrides);
        return (
            <div
                ref={combinedRef}
                style={style}
                className="group touch-none relative"
                onMouseDown={handleMouseDown}
                data-component-id={component.id}
                {...listeners}
                {...attributes}
            >
                <h3 style={styles.labelStyle}>
                    {component.props.label || 'Header'}
                </h3>
                {/* Resize Handles */}
                <ResizeHandles {...resizeHandleProps} />
            </div>
        );
    }

    // 5. Standard Inputs (Gold Standard) - All other input components
    const def = ComponentRegistry[component.type];

    // Fallback: if a component somehow has no registry structure (legacy/unknown),
    // still render through UniversalFieldShell using the default structure.
    const fallbackStructure = def?.structure || getDefaultStructure(component.type);
    const fallbackRenderers = getRenderersForComponent(component.type, fallbackStructure, component);
    
    // Log when fallback path is used - this should be rare and indicates a component
    // that should be added to universalFieldShellTypes or have a proper structure
    devLogger.warn('component.rendering.fallback', {
        componentId: component.id,
        componentType: component.type,
        hasRegistryStructure: !!def?.structure,
        reason: !universalFieldShellTypes.includes(component.type) && !hasUniversalStructure 
            ? 'Not in universalFieldShellTypes and no universal structure'
            : 'Unknown reason',
        recommendation: `Add '${component.type}' to universalFieldShellTypes or ensure it has a proper structure`
    });

    return (
        <div
            ref={outerRef}
            style={style}
            className="group touch-none relative"
            onMouseDown={handleMouseDown}
            data-component-id={component.id}
            // Drag handled by SmartBorder via builderMode.dragListeners when present
        >
            <UniversalFieldShell
                ref={smartBorderRef}
                structure={fallbackStructure}
                renderers={fallbackRenderers}
                surface="canvas"
                objectLayout={component.props.objectLayout}
                layoutGroups={component.props.layoutGroups}
                styleOverrides={component.props.styleOverrides}
                globalStyles={globalStyles}
                componentId={component.id}
                component={component}
                // For E/W resize: DON'T pass previewWidth - keep component frozen during drag
                previewWidth={undefined}
                currentWidthPx={currentWidthPxForPreview}
                previewObjectWidthOverrides={
                    // For input-only resize handles (not E/W component resize)
                    resizePreview?.inputWidthOverride !== undefined
                        ? { inputWidthOverride: resizePreview.inputWidthOverride }
                        : undefined
                }
                previewStyleOverrides={isVerticalResize ? previewStyleOverrides : undefined}
                previewSpacingOverrides={isVerticalResize ? previewSpacingOverrides : undefined}
                previewScale={undefined}
                builderMode={{
                    showBorder: true,
                    borderPadding: 5,
                    smartBorderLayout: hasExplicitWidth ? 'fill' : 'shrink', // Match primary path behavior
                    isSelected: isSelected,
                    isDragging: isDragging,
                    isResizing: isResizingState,
                    dragListeners: listeners,
                    dragAttributes: attributes,
                    containerRef: smartBorderContainerRef,
                }}
            />
            {/* Resize Handles - Use ResizeHandlesWrapper to match primary path behavior */}
            {isSelected && !isLocked && (
                <ResizeHandlesWrapper 
                    smartBorderContainerRef={smartBorderContainerRef}
                    outerContainerRef={outerRef}
                    componentId={component.id}
                    forceUpdateKey={`${component.props.width}-${component.props.inputWidthOverride}-${component.props.labelWidthOverride}-${component.props.helpWidthOverride}`}
                >
                    <ResizeHandles {...resizeHandleProps} />
                </ResizeHandlesWrapper>
            )}
            {/* Hidden badge for initially hidden components */}
            {isInitiallyHidden && (
                <div
                    className="absolute -top-5 left-0 px-1.5 py-0.5 text-[10px] font-medium bg-gray-700 text-white rounded-sm"
                    style={{ pointerEvents: 'none' }}
                >
                    Hidden
                </div>
            )}
        </div>
    );
};
