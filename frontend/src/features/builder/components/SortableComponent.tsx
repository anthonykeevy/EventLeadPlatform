import React, { useCallback, useState, useEffect, useRef } from 'react';
import { useDraggable } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';
import { FormComponent } from '../types/builder.types';
import { FirstNameField } from './fields/FirstNameField';
import { StandardInput } from './fields/StandardInput';
import { ComponentRegistry } from '../registry/ComponentRegistry';
import { useBuilderStore } from '../stores/useBuilderStore';
import { computeFieldStyles } from '../utils/styleUtils';
import { ResizeHandles, HandlePosition } from './ui/ResizeHandles';
import { devLogger } from '../utils/devLogger';

interface SortableComponentProps {
    component: FormComponent;
}

// Renamed to DraggableComponent since we aren't sorting anymore
export const SortableComponent: React.FC<SortableComponentProps> = ({ component }) => {
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
    const { scale, activeLayer, selectedComponentIds, selectComponent, globalStyles, updateComponentProps } = useBuilderStore(state => ({ 
        scale: state.scale, 
        activeLayer: state.activeLayer,
        selectedComponentIds: state.selectedComponentIds,
        selectComponent: state.selectComponent,
        globalStyles: state.formDefinition?.globalStyles,
        updateComponentProps: state.updateComponentProps,
    }));
    
    // Local state for live resize preview
    const [resizePreview, setResizePreview] = useState<{ 
        width?: number; 
        height?: number; 
        scale?: number;
        labelGap?: number;
        inputHelpGap?: number;
        inputHeight?: number;
        topShift?: number;
    } | null>(null);
    const lastVerticalPreviewRef = useRef<{ inputHeight?: number; labelGap?: number; inputHelpGap?: number; topShift?: number } | null>(null);
    
    // Compute effective styles (global + any component overrides + scale + spacing overrides)
    const componentScale = component.props.componentScale ?? 100;
    const spacingOverrides = {
        labelGapOverride: component.props.labelGapOverride,
        inputHelpGapOverride: component.props.inputHelpGapOverride,
    };
    const fieldStyles = computeFieldStyles(globalStyles, component.props.styleOverrides, componentScale, spacingOverrides);

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

    const handleResizeStart = useCallback(() => {
        // Could add visual feedback here
    }, []);

    // Live preview during resize (for visual feedback)
    const handleResize = useCallback((deltaWidth: number, deltaHeight: number, handle: HandlePosition) => {
        const currentWidthPx = component.props.width?.endsWith('px') 
            ? parseInt(component.props.width, 10) 
            : 300;
        const currentInputHeight = fieldStyles.computed.inputHeight;
        const scaleFactor = componentScale / 100;
        const minInputHeight = 28 * scaleFactor;
        const maxInputHeight = 240 * scaleFactor;

        // Calculate preview dimensions based on handle type
        const isCorner = ['nw', 'ne', 'se', 'sw'].includes(handle);
        
        if (isCorner) {
            // Corner handles: show scale preview
            const startWidth = currentWidthPx;
            const newWidth = startWidth + deltaWidth;
            const scaleFactorLocal = (newWidth / startWidth) * componentScale;
            const nextScale = Math.max(50, Math.min(200, scaleFactorLocal));
            setResizePreview({ scale: nextScale });
            devLogger.debug('resize.preview', {
                componentId: component.id,
                componentType: component.type,
                handle,
                widthDelta: deltaWidth,
                previewScale: nextScale,
            });
        } else if (handle === 'e' || handle === 'w') {
            // Edge handles: show width preview
            const nextWidth = currentWidthPx + deltaWidth;
            setResizePreview({ width: nextWidth });
            devLogger.debug('resize.preview', {
                componentId: component.id,
                componentType: component.type,
                handle,
                widthDelta: deltaWidth,
                previewWidth: nextWidth,
            });
        } else if (handle === 'n' || handle === 's') {
            // Height-first logic: adjust input height within bounds, then spacing with any remaining delta
            // deltaHeight here is already normalized (positive = drag down on S, drag up on N)
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
            devLogger.debug('resize.preview', {
                componentId: component.id,
                componentType: component.type,
                handle,
                deltaHeight,
                previewInputHeight: newInputHeight,
                clampedHeight,
                previewLabelGap: preview.labelGap,
                previewInputHelpGap: preview.inputHelpGap,
                topShift: preview.topShift,
            });
        }
    }, [component.props.width, component.type, componentScale, fieldStyles.computed.inputHeight, currentLabelGap, currentInputHelpGap]);

    // Width change handler (E/W handles)
    const handleWidthChange = useCallback((newWidth: number) => {
        updateComponentProps(component.id, { 
            width: `${newWidth}px`,
            // When width is explicitly set, default to 'fill' mode so input responds
            inputWidthMode: 'fill',
        });
        devLogger.info('resize.commit.width', {
            componentId: component.id,
            componentType: component.type,
            newWidth,
        });
        setResizePreview(null);
    }, [component.id, updateComponentProps]);

    // Scale change handler (corner handles)
    const handleScaleChange = useCallback((newScale: number) => {
        updateComponentProps(component.id, { componentScale: newScale });
        devLogger.info('resize.commit.scale', {
            componentId: component.id,
            componentType: component.type,
            newScale,
        });
        setResizePreview(null);
    }, [component.id, updateComponentProps]);

    // Spacing change handler (N/S handles for non-textarea)
    const handleSpacingChange = useCallback((spacingType: 'labelGap' | 'inputHelpGap', newValue: number) => {
        if (spacingType === 'labelGap') {
            updateComponentProps(component.id, { labelGapOverride: newValue });
        } else {
            updateComponentProps(component.id, { inputHelpGapOverride: newValue });
        }
        setResizePreview(null);
    }, [component.id, updateComponentProps]);

    // Height change handler (S handle for textarea)
    const handleHeightChange = useCallback((newHeight: number) => {
        updateComponentProps(component.id, { height: newHeight });
        setResizePreview(null);
    }, [component.id, updateComponentProps]);

    // Vertical resize commit (N/S) with height-first then spacing behavior
    const handleVerticalResizeEnd = useCallback((handle: 'n' | 's', deltaY: number) => {
        const scaleFactor = componentScale / 100;
        const currentInputHeight = fieldStyles.computed.inputHeight;
        const minInputHeight = 28 * scaleFactor;
        const maxInputHeight = 240 * scaleFactor;

        // Prefer the last preview state to avoid losing the peak value when user drags back before releasing
        const previewState = lastVerticalPreviewRef.current;
        const finalInputHeight = previewState?.inputHeight ?? Math.max(minInputHeight, Math.min(maxInputHeight, currentInputHeight + deltaY));

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
                    const newGap = Math.max(0, Math.min(48, currentLabelGap + remainingDelta));
                    appliedLabelGap = Math.round(newGap);
                    nextProps.labelGapOverride = appliedLabelGap;
                } else {
                    const newGap = Math.max(0, Math.min(48, currentInputHelpGap + remainingDelta));
                    appliedInputHelpGap = Math.round(newGap);
                    nextProps.inputHelpGapOverride = appliedInputHelpGap;
                }
            }
        } else {
            if (appliedLabelGap !== undefined) nextProps.labelGapOverride = Math.round(appliedLabelGap);
            if (appliedInputHelpGap !== undefined) nextProps.inputHelpGapOverride = Math.round(appliedInputHelpGap);
        }

        // Anchor south: adjust y when north handle used (prefer preview topShift for exact visual match)
        if (handle === 'n') {
            const spacingDeltaUsed = appliedLabelGap !== undefined ? appliedLabelGap - currentLabelGap : 0;
            const fallbackShift = -(heightDeltaUsed + spacingDeltaUsed);
            appliedShift = previewTopShift ?? fallbackShift;
        }

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

        devLogger.info('resize.commit.vertical', {
            componentId: component.id,
            componentType: component.type,
            handle,
            deltaY,
            inputHeight: {
                current: currentInputHeight,
                new: finalInputHeight,
                min: minInputHeight,
                max: maxInputHeight,
                clamped: finalInputHeight === minInputHeight || finalInputHeight === maxInputHeight,
                unscaledApplied: unscaledHeight,
            },
            spacing: {
                labelGap: appliedLabelGap,
                inputHelpGap: appliedInputHelpGap,
            },
            position: {
                before: { x: currentX, y: currentY },
                after: handle === 'n' && appliedShift !== 0 ? { x: currentX, y: currentY + appliedShift } : { x: currentX, y: currentY },
                appliedShift,
                previewTopShift,
            },
        });
        setResizePreview(null);
        lastVerticalPreviewRef.current = null;
    }, [component.id, component.props.styleOverrides, componentScale, currentLabelGap, currentInputHelpGap, fieldStyles.computed.inputHeight, updateComponentProps]);

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
        disabled: isLocked // Disable drag if locked
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

    const scaledTransform = transform ? {
        ...transform,
        x: transform.x / scale,
        y: transform.y / scale
    } : null;

    // Parse component width to px (percentages mapped to a base canvas width)
    const parseComponentWidthPx = (val?: string): number => {
        if (!val) return 300;
        if (val.endsWith('%')) {
            const pct = parseInt(val, 10);
            const measured = parentWidth ?? 800;
            const base = scale > 0 ? measured / scale : measured;
            return Math.max(50, Math.round((pct / 100) * base));
        }
        if (val.endsWith('px')) return parseInt(val, 10);
        const n = parseInt(val, 10);
        return Number.isFinite(n) ? n : 300;
    };

    // Calculate dimensions (use preview during resize, otherwise actual props)
    const displayScale = resizePreview?.scale ?? componentScale;
    const baseWidthPx = resizePreview?.width ?? parseComponentWidthPx(component.props.width);
    const displayWidthPx = baseWidthPx * (displayScale / 100);
    const displayWidth = `${displayWidthPx}px`;
    const displayHeight = resizePreview?.height ?? component.props.height;
    const displayTop = (component.position?.y ?? 0) + (resizePreview?.topShift ?? 0);

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

    const previewFieldStyles = (resizePreview?.scale !== undefined || resizePreview?.labelGap !== undefined || resizePreview?.inputHelpGap !== undefined || resizePreview?.inputHeight !== undefined)
        ? computeFieldStyles(globalStyles, previewStyleOverrides, displayScale, previewSpacingOverrides)
        : fieldStyles;

    // Absolute Positioning Logic
    const style: React.CSSProperties = {
        transform: scaledTransform ? CSS.Translate.toString(scaledTransform) : undefined,
        position: 'absolute',
        left: component.position?.x ?? 0,
        top: displayTop,
        zIndex: isDragging ? 100 : (component.style?.zIndex ?? 10),
        opacity: isDragging ? 0.5 : 1,
        // Visual feedback for locked state
        cursor: isLocked ? 'not-allowed' : 'pointer',
    };

    // Selection is now handled by SmartBorder - no additional ring needed

    // Get effective layout: component override > global default > 'vertical'
    const effectiveLayout = component.props.layout || globalStyles?.defaultLayout || 'vertical';

    // Common resize handles props
    const resizeHandleProps = {
        isSelected: isSelected && !isLocked,
        currentWidth: component.props.width,
        currentHeight: fieldStyles.computed.inputHeight,
        currentScale: componentScale,
        currentLabelGap,
        currentInputHelpGap,
        componentType: component.type,
        onResizeStart: handleResizeStart,
        onResize: handleResize,
        onWidthChange: handleWidthChange,
        onScaleChange: handleScaleChange,
        onSpacingChange: handleSpacingChange,
        onHeightChange: handleHeightChange,
        onVerticalResizeEnd: handleVerticalResizeEnd,
        minWidth: 100,
        minHeight: 40,
    };

    // 1. First Name (POC)
    if (component.type === 'first-name') {
        return (
            <div
                ref={combinedRef} 
                style={style}
                className="group touch-none relative"
                onMouseDown={handleMouseDown}
                data-component-id={component.id}
            >
                <FirstNameField 
                    label={component.props.label}
                    placeholder={component.props.placeholder}
                    required={component.props.required}
                    helpText={component.props.helpText}
                    layout={effectiveLayout}
                    dragListeners={listeners} 
                    dragAttributes={attributes}
                    isSelected={isSelected}
                    fieldStyles={previewFieldStyles}
                    containerWidth={displayWidth}
                    inputWidthMode={component.props.inputWidthMode}
                    labelWrap={component.props.labelWrap}
                textAlign={component.props.textAlign}
                />
                {/* Resize Handles */}
                <ResizeHandles {...resizeHandleProps} />
            </div>
        );
    }

    // 2. Standard Inputs (Gold Standard)
    const def = ComponentRegistry[component.type];
    
    return (
            <div
                ref={combinedRef} 
            style={style}
            className="group touch-none relative"
            onMouseDown={handleMouseDown}
            data-component-id={component.id}
        >
            <StandardInput 
                label={component.props.label || 'Unknown'}
                icon={def?.icon}
                placeholder={component.props.placeholder}
                validationMessage={component.props.validationMessage || "Validation message here"}
                helpText={component.props.helpText}
                required={component.props.required}
                type={component.type as 'text' | 'number' | 'email' | 'textarea' | 'select' | 'date'}
                options={component.props.options}
                dragListeners={listeners}
                dragAttributes={attributes}
                isSelected={isSelected}
                layout={effectiveLayout}
                fieldStyles={previewFieldStyles}
                validation={component.props.validation}
                containerWidth={displayWidth}
                inputWidthMode={component.props.inputWidthMode}
                labelWrap={component.props.labelWrap}
                height={displayHeight}
                textAlign={component.props.textAlign}
            />
            {/* Resize Handles */}
            <ResizeHandles {...resizeHandleProps} />
        </div>
    );
};
