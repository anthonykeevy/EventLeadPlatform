import React, { forwardRef, useMemo } from 'react';
import { SmartBorder } from './ui/SmartBorder';
import { 
    FormComponent, 
    GlobalStyles, 
    StyleOverrides, 
    SpacingOverrides, 
    ComponentStructure,
    ObjectLayoutType,
    ComponentObject,
} from '../types/builder.types';
import { ComponentSurface, getComponentSurfaceCapabilities } from '../utils/componentSurfaceCapabilities';
import { ObjectRenderer, ObjectRendererProps } from '../utils/objectRenderers';
import { computeFieldStyles, ComputedFieldStyles } from '../utils/styleUtils';
import { calculateSpacing } from '../utils/spacingCalculation';

export interface PreviewObjectWidthOverrides {
    labelWidthOverride?: number;
    inputWidthOverride?: number;
    helpWidthOverride?: number;
    actionWidthOverride?: number;
}

export interface UniversalFieldShellProps {
    structure: ComponentStructure;
    renderers: Record<string, ObjectRenderer>;
    surface: ComponentSurface;
    objectLayout?: ObjectLayoutType;
    layoutGroups?: Record<string, string[]>;
    styleOverrides?: StyleOverrides;
    globalStyles?: GlobalStyles;
    componentId?: string;
    component?: FormComponent;
    previewWidth?: number;
    currentWidthPx?: number;
    previewObjectWidthOverrides?: PreviewObjectWidthOverrides;
    previewStyleOverrides?: StyleOverrides;
    previewSpacingOverrides?: SpacingOverrides;
    previewScale?: number;
    frozenGridTemplateColumns?: string;
    builderMode?: {
        showBorder?: boolean;
        borderPadding?: number;
        smartBorderLayout?: 'fill' | 'shrink';
        isSelected?: boolean;
        isDragging?: boolean;
        isResizing?: boolean;
        dragListeners?: any;
        dragAttributes?: any;
        containerRef?: React.RefObject<HTMLDivElement | null>;
    };
    // Runtime props
    value?: any;
    onChange?: (value: any) => void;
    disabled?: boolean;
    error?: string;
    validationErrors?: string[];
    allFormErrors?: Record<string, string[]>;
    isLoading?: boolean;
    formValidationContext?: any;
}

/**
 * Group objects by layout type
 */
function groupObjectsByLayout(
    objects: ComponentObject[],
    layout: ObjectLayoutType,
    layoutGroups?: Record<string, string[]>
): Array<{ rowId: string; objects: ComponentObject[] }> {
    if (layout === 'mixed' && layoutGroups) {
        // Mixed layout: use explicit groups
        return Object.entries(layoutGroups).map(([rowId, objectIds]) => ({
            rowId,
            objects: objectIds
                .map(id => objects.find(o => o.id === id))
                .filter((o): o is ComponentObject => !!o),
        }));
    }
    
    if (layout === 'horizontal') {
        // All objects in one row
        return [{ rowId: 'row-0', objects }];
    }
    
    // Vertical: each object is its own row
    return objects.map((obj, i) => ({
        rowId: `row-${i}`,
        objects: [obj],
    }));
}

/**
 * UniversalFieldShell - Component Framework Renderer
 * 
 * The universal wrapper for all form components. Manages:
 * - Layout (vertical/horizontal/mixed)
 * - Spacing (using calculateSpacing)
 * - Conditional visibility
 * - SmartBorder integration (canvas)
 * - Object rendering via shared renderers
 */
export const UniversalFieldShell = forwardRef<HTMLDivElement, UniversalFieldShellProps>(
    (props, ref) => {
        const {
            structure,
            renderers,
            surface,
            objectLayout,
            layoutGroups,
            styleOverrides,
            globalStyles,
            componentId,
            component,
            previewWidth,
            currentWidthPx,
            previewObjectWidthOverrides,
            previewStyleOverrides,
            previewSpacingOverrides,
            previewScale,
            frozenGridTemplateColumns,
            builderMode,
            // Runtime props
            value,
            onChange,
            disabled,
            error,
            validationErrors,
            allFormErrors,
            isLoading,
            formValidationContext,
        } = props;

        // Determine effective layout
        const effectiveLayout = objectLayout || structure.defaultLayout || 'vertical';
        const effectiveLayoutGroups = layoutGroups || structure.layoutGroups;
        
        // Compute field styles
        const componentScale = component?.props.componentScale ?? 100;
        const spacingOverrides = previewSpacingOverrides || {
            labelGapOverride: component?.props.labelGapOverride,
            inputHelpGapOverride: component?.props.inputHelpGapOverride,
        };
        const effectiveStyleOverrides = previewStyleOverrides || styleOverrides;
        const fieldStyles = useMemo(() => 
            computeFieldStyles(globalStyles, effectiveStyleOverrides, componentScale, spacingOverrides),
            [globalStyles, effectiveStyleOverrides, componentScale, spacingOverrides]
        );

        // Calculate spacing
        const spacing = useMemo(() => 
            calculateSpacing(effectiveLayout, effectiveLayoutGroups, undefined, globalStyles),
            [effectiveLayout, effectiveLayoutGroups, globalStyles]
        );

        // Group objects by layout
        const rows = useMemo(() => 
            groupObjectsByLayout(structure.objects, effectiveLayout, effectiveLayoutGroups),
            [structure.objects, effectiveLayout, effectiveLayoutGroups]
        );

        // Get width override for an object
        const getWidthOverride = (objectId: string): number | undefined => {
            if (!previewObjectWidthOverrides) return undefined;
            
            // Map object ID to override key
            const overrideMap: Record<string, keyof PreviewObjectWidthOverrides> = {
                label: 'labelWidthOverride',
                input: 'inputWidthOverride',
                validation: 'helpWidthOverride',
                help: 'helpWidthOverride',
                action: 'actionWidthOverride',
                button: 'actionWidthOverride',
            };
            
            const key = overrideMap[objectId];
            return key ? previewObjectWidthOverrides[key] : undefined;
        };

        // Render a single object
        const renderObject = (obj: ComponentObject, inRowGroup: boolean) => {
            const renderer = renderers[obj.id];
            if (!renderer) return null;

            const widthOverride = getWidthOverride(obj.id);
            
            // Build renderer props
            const rendererProps: ObjectRendererProps = {
                object: obj,
                component: component!,
                styles: fieldStyles,
                layout: effectiveLayout,
                componentId,
                surface,
                builderMode: !!builderMode,
                // Width overrides
                labelWidthOverride: obj.type === 'label' ? widthOverride : undefined,
                inputWidthOverride: obj.type === 'input' ? widthOverride : undefined,
                helpWidthOverride: obj.type === 'validation' ? widthOverride : undefined,
                actionWidthOverride: obj.type === 'action' ? widthOverride : undefined,
                // Runtime props
                value,
                onChange,
                disabled,
                error,
                validationErrors,
                allFormErrors,
                isLoading,
                required: component?.props.required,
                formValidationContext,
                // Layout context
                inRowGroup,
            };

            return renderer(rendererProps);
        };

        // Render a row of objects
        const renderRow = (row: { rowId: string; objects: ComponentObject[] }, isLastRow: boolean) => {
            const isMultiObject = row.objects.length > 1;
            const rowAlignment = structure.defaultRowAlignment || 'center';
            
            // Row styles - use inline-flex for shrink-wrap behavior
            const rowStyle: React.CSSProperties = {
                display: 'inline-flex',
                flexDirection: isMultiObject ? 'row' : 'column',
                alignItems: isMultiObject ? (
                    rowAlignment === 'top' ? 'flex-start' :
                    rowAlignment === 'bottom' ? 'flex-end' : 'center'
                ) : 'flex-start',
                gap: isMultiObject ? `${spacing.horizontalGap}px` : undefined,
                marginBottom: !isLastRow ? `${spacing.verticalSpacing}px` : undefined,
            };

            return (
                <div key={row.rowId} style={rowStyle} data-row-id={row.rowId} data-layout-group={row.rowId}>
                    {row.objects.map(obj => (
                        <div 
                            key={obj.id} 
                            data-object-id={obj.id}
                            data-grid-object={obj.id}
                            style={{ 
                                display: 'inline-block',
                                verticalAlign: 'top',
                            }}
                        >
                            {renderObject(obj, isMultiObject)}
                        </div>
                    ))}
                </div>
            );
        };

        // Container styles - inline-flex allows content to shrink-wrap
        const containerStyle: React.CSSProperties = {
            width: previewWidth ? `${previewWidth}px` : undefined,
            display: 'inline-flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
        };

        // Main content
        const content = (
            <div style={containerStyle} data-component-id={componentId}>
                {rows.map((row, index) => renderRow(row, index === rows.length - 1))}
            </div>
        );

        // Wrap with SmartBorder if in builder mode
        if (builderMode?.showBorder) {
            return (
                <SmartBorder
                    ref={ref}
                    padding={builderMode.borderPadding ?? 10}
                    layout={builderMode.smartBorderLayout ?? 'shrink'}
                    isSelected={builderMode.isSelected}
                    isDragging={builderMode.isDragging}
                    isResizing={builderMode.isResizing}
                    dragListeners={builderMode.dragListeners}
                    dragAttributes={builderMode.dragAttributes}
                    componentId={componentId}
                    previewWidth={previewWidth}
                >
                    {content}
                </SmartBorder>
            );
        }

        return (
            <div ref={ref}>
                {content}
            </div>
        );
    }
);

UniversalFieldShell.displayName = 'UniversalFieldShell';
