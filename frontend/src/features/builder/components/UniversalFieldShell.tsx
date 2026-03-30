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
import { computeFieldStyles } from '../utils/styleUtils';
import { calculateSpacing } from '../utils/spacingCalculation';
import { getEffectiveGridLayout, getObjectGridArea, resolveComponentDefaultGridLayout } from '../utils/gridLayoutUtils';

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
    previewHeight?: number;
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
        dragListeners?: Record<string, unknown>;
        dragAttributes?: Record<string, unknown>;
        containerRef?: React.RefObject<HTMLDivElement | null>;
        frozenGridTemplateColumns?: string | null;
    };
    // Runtime props (individual)
    value?: unknown;
    onChange?: (value: unknown) => void;
    disabled?: boolean;
    error?: string;
    validationErrors?: string[];
    allFormErrors?: Record<string, string[]>;
    isLoading?: boolean;
    formValidationContext?: Record<string, unknown>;
    /** When true, input objects render with focus styling (e.g. Focus Color cycling in Form Branding Defaults) */
    simulateFocus?: boolean;
    // Runtime mode (bundled) - used by ComponentRegistry
    runtimeMode?: {
        value?: unknown;
        onChange?: (value: unknown) => void;
        disabled?: boolean;
        required?: boolean;
        error?: string;
        primaryColor?: string;
        tabIndex?: number;
        inputRef?: React.RefObject<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | null>;
        onClick?: () => void;
        isLoading?: boolean;
        validationErrors?: Record<string, string>;
        allFormErrors?: Record<string, string>;
        formValidationContext?: Record<string, unknown>;
        componentState?: Record<string, unknown>;
        buttonText?: string;
    };
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
            previewHeight,
            currentWidthPx,
            previewObjectWidthOverrides,
            previewStyleOverrides,
            previewSpacingOverrides,
            previewScale: _previewScale,
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
            runtimeMode,
            simulateFocus,
        } = props;

        const effectiveFrozenGridTemplateColumns =
            builderMode?.frozenGridTemplateColumns ?? frozenGridTemplateColumns;

        const effectiveSurface: ComponentSurface = surface ?? (builderMode ? 'canvas' : 'runtime');
        const surfaceCaps = component
            ? getComponentSurfaceCapabilities(component.type, effectiveSurface)
            : getComponentSurfaceCapabilities('text', effectiveSurface);

        // Determine effective layout
        const effectiveLayout = objectLayout || structure.defaultLayout || 'vertical';
        const effectiveLayoutGroups = layoutGroups || structure.layoutGroups;

        // Grid Layout resolution (component override > global defaults). If enabled, render as CSS grid.
        const effectiveGridLayout = useMemo(() => {
            const componentDefault = resolveComponentDefaultGridLayout({
                structure,
                componentType: component?.type,
                globalStyles,
            });
            const base = getEffectiveGridLayout(
                component?.props.gridLayout,
                componentDefault,
                globalStyles?.defaultGridLayout
            );
            if (!base) return null;

            // If grid layout is enabled but assignments are missing, auto-assign objects row-major
            // so the component still renders something usable (especially for global defaults).
            const hasAssignments = base.cellAssignments && Object.keys(base.cellAssignments).length > 0;
            if (hasAssignments) return base;

            const orderedIds = structure.objects.map(o => o.id);
            const cellAssignments: Record<string, string> = {};
            let idx = 0;
            for (let r = 0; r < base.rows; r += 1) {
                for (let c = 0; c < base.columns; c += 1) {
                    const objectId = orderedIds[idx];
                    if (!objectId) break;
                    cellAssignments[`${r}-${c}`] = objectId;
                    idx += 1;
                }
            }

            return {
                ...base,
                cellAssignments,
            };
        }, [
            component?.props.gridLayout,
            component?.type,
            globalStyles?.defaultGridLayoutsByComponent,
            globalStyles?.defaultObjectLayout,
            globalStyles?.defaultGridLayout,
            structure.objects,
        ]);

        const isGridLayoutEnabled = !!effectiveGridLayout;
        const layoutForRender: ObjectLayoutType = isGridLayoutEnabled ? 'mixed' : effectiveLayout;
        
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
                display: 'inputWidthOverride',
                content: 'inputWidthOverride', // Fallback for display object ids
                line: 'inputWidthOverride',    // Divider uses line id
            };
            
            const key = overrideMap[objectId] || overrideMap[obj.type];
            
            return key ? previewObjectWidthOverrides[key] : undefined;
        };

        // Render a single object
        const runtimeValue = runtimeMode?.value ?? value;
        const runtimeOnChange = runtimeMode?.onChange ?? onChange;
        const runtimeDisabled = runtimeMode?.disabled ?? disabled;
        const runtimeRequired = runtimeMode?.required;
        const runtimeError = runtimeMode?.error ?? error;
        const runtimePrimaryColor = runtimeMode?.primaryColor;
        const runtimeTabIndex = runtimeMode?.tabIndex;
        const runtimeInputRef = runtimeMode?.inputRef;
        const runtimeOnClick = runtimeMode?.onClick;
        const runtimeIsLoading = runtimeMode?.isLoading ?? isLoading;
        const runtimeValidationErrors = runtimeMode?.validationErrors ?? validationErrors;
        const runtimeAllFormErrors = runtimeMode?.allFormErrors ?? allFormErrors;
        const runtimeFormValidationContext = runtimeMode?.formValidationContext ?? formValidationContext;

        const renderObject = (obj: ComponentObject, inRowGroup: boolean) => {
            const renderer = renderers[obj.id];
            if (!renderer) return null;

            const widthOverride = getWidthOverride(obj.id);
            
            // Build renderer props
            const rendererProps: ObjectRendererProps = {
                object: obj,
                component: component!,
                styles: fieldStyles,
                layout: layoutForRender,
                componentId,
                surface: effectiveSurface,
                builderMode: !!builderMode,
                // Width overrides
                labelWidthOverride: obj.type === 'label' && surfaceCaps.surfaceStyles.applyLabelWidth ? widthOverride : undefined,
                inputWidthOverride: (obj.type === 'input' || obj.type === 'display') && surfaceCaps.surfaceStyles.applyInputWidthOverride ? widthOverride : undefined,
                helpWidthOverride: obj.type === 'validation' ? widthOverride : undefined,
                actionWidthOverride: obj.type === 'action' && surfaceCaps.surfaceStyles.applyButtonStyling ? widthOverride : undefined,
                // Runtime props
                value: runtimeValue,
                onChange: runtimeOnChange,
                disabled: runtimeDisabled,
                error: runtimeError,
                validationErrors: runtimeValidationErrors,
                allFormErrors: runtimeAllFormErrors,
                isLoading: runtimeIsLoading,
                required: runtimeRequired ?? component?.props.required,
                formValidationContext: runtimeFormValidationContext,
                onClick: runtimeOnClick,
                primaryColor: runtimePrimaryColor,
                tabIndex: runtimeTabIndex,
                inputRef: runtimeInputRef,
                simulateFocus: obj.type === 'input' ? simulateFocus : undefined,
                // Layout context
                inRowGroup,
                isGridLayout: isGridLayoutEnabled,
                actionHeightOverride:
                    obj.type === 'action' && surfaceCaps.surfaceStyles.applyButtonStyling
                        ? (previewHeight ?? component?.props.height)
                        : undefined,
                displayHeightOverride:
                    obj.type === 'display'
                        ? (previewHeight ?? component?.props.height)
                        : undefined,
            };

            return renderer(rendererProps);
        };

        // Render a row of objects
        const renderRow = (row: { rowId: string; objects: ComponentObject[] }, isLastRow: boolean) => {
            const isMultiObject = row.objects.length > 1;
            const rowAlignment = structure.defaultRowAlignment || 'center';
            const isSubmitButton = component?.type === 'submit-button';
            const isFullWidthComponent = ['submit-button', 'divider'].includes(component?.type || '') || row.objects.some(obj => obj.type === 'display');
            const shouldStretchRow = isFullWidthComponent && (previewWidth || component?.props.width || row.objects.some(obj => obj.type === 'display'));
            
            // Row styles - use inline-flex for shrink-wrap behavior
            const rowStyle: React.CSSProperties = {
                display: shouldStretchRow ? 'flex' : 'inline-flex',
                flexDirection: isMultiObject ? 'row' : 'column',
                alignItems: isMultiObject ? (
                    rowAlignment === 'top' ? 'flex-start' :
                    rowAlignment === 'bottom' ? 'flex-end' : 'center'
                ) : 'flex-start',
                gap: isMultiObject ? `${spacing.columnGap}px` : undefined,
                marginBottom: !isLastRow ? `${spacing.rowGap}px` : undefined,
                ...(shouldStretchRow ? { width: '100%' } : {}),
            };

            return (
                <div key={row.rowId} style={rowStyle} data-row-id={row.rowId} data-layout-group={row.rowId}>
                    {row.objects.map(obj => (
                        <div 
                            key={obj.id} 
                            data-object-id={obj.id}
                            data-grid-object={obj.id}
                            style={{ 
                                display: (isSubmitButton && obj.type === 'action') || obj.type === 'display' ? 'block' : 'inline-block',
                                verticalAlign: 'top',
                                flex: obj.type === 'display' ? 1 : undefined,
                                ...((isSubmitButton && obj.type === 'action') || obj.type === 'display' ? { width: '100%' } : {}),
                            }}
                        >
                            {renderObject(obj, isMultiObject)}
                        </div>
                    ))}
                </div>
            );
        };

        const resolvedContainerWidth = (() => {
            if (!surfaceCaps.surfaceStyles.applyComponentWidth) return undefined;
            if (previewWidth !== undefined) return `${previewWidth}px`;
            const widthValue = component?.props.width;
            if (!widthValue || widthValue.trim().toLowerCase() === 'auto') return undefined;
            if (widthValue.endsWith('%')) {
                return currentWidthPx ? `${currentWidthPx}px` : widthValue;
            }
            return widthValue;
        })();

        // Container styles - inline-flex allows content to shrink-wrap
        const containerStyle: React.CSSProperties = {
            width: resolvedContainerWidth,
            display: 'inline-flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
        };

        // ───────────────────────────────────────────────────────────────
        // Grid Layout rendering (when enabled)
        // ───────────────────────────────────────────────────────────────
        const gridContent = (() => {
            if (!effectiveGridLayout) return null;

            // Determine if the component should fill available width (explicit width or active resize preview).
            const hasExplicitWidth =
                surfaceCaps.surfaceStyles.applyComponentWidth &&
                typeof component?.props.width === 'string' &&
                (component.props.width.endsWith('px') || component.props.width.endsWith('%'));
            const shouldFillWidth = Boolean(previewWidth || hasExplicitWidth || builderMode?.smartBorderLayout === 'fill');

            // Build an object-aware gridTemplateColumns:
            // - Columns containing an input, display, or divider object become flexible: minmax(0, 1fr)
            // - Other columns remain content-sized (but shrinkable): minmax(0, max-content)
            const flexColumnSet = new Set<number>();
            for (const [key, objectId] of Object.entries(effectiveGridLayout.cellAssignments || {})) {
                const obj = structure.objects.find(o => o.id === objectId);
                const isFlexObj = obj && (obj.type === 'input' || obj.type === 'display' || obj.type === 'divider');
                if (!isFlexObj && objectId !== 'input') continue;
                
                const [rowStr, colStr] = key.split('-');
                void rowStr;
                const col = Number.parseInt(colStr, 10);
                if (!Number.isFinite(col)) continue;
                const span = effectiveGridLayout.objectSpans?.[objectId]?.colSpan ?? 1;
                for (let i = 0; i < Math.max(1, span); i += 1) {
                    flexColumnSet.add(col + i);
                }
            }

            const columnTemplate: string[] = [];
            for (let col = 0; col < effectiveGridLayout.columns; col += 1) {
                const track = shouldFillWidth && flexColumnSet.has(col) ? 'minmax(0, 1fr)' : 'auto';
                const nonInputTrack = shouldFillWidth ? 'minmax(0, max-content)' : 'auto';
                columnTemplate.push(flexColumnSet.has(col) ? track : nonInputTrack);
                if (col < effectiveGridLayout.columns - 1) {
                    const gap = effectiveGridLayout.columnGaps?.[col] ?? effectiveGridLayout.columnGap;
                    columnTemplate.push(`${gap}px`);
                }
            }

            // Rows: keep as auto (with explicit gap tracks) so the shell height matches content.
            const rowTemplate: string[] = [];
            for (let row = 0; row < effectiveGridLayout.rows; row += 1) {
                rowTemplate.push('auto');
                if (row < effectiveGridLayout.rows - 1) {
                    const gap = effectiveGridLayout.rowGaps?.[row] ?? effectiveGridLayout.rowGap;
                    rowTemplate.push(`${gap}px`);
                }
            }

            // Build row membership so renderers can treat multi-object rows like "inRowGroup".
            const rowByObjectId = new Map<string, number>();
            for (const [key, objectId] of Object.entries(effectiveGridLayout.cellAssignments || {})) {
                const [rowStr] = key.split('-');
                const row = Number.parseInt(rowStr, 10);
                if (!Number.isFinite(row)) continue;
                rowByObjectId.set(objectId, row);
            }
            const rowCounts = new Map<number, number>();
            for (const row of rowByObjectId.values()) {
                rowCounts.set(row, (rowCounts.get(row) ?? 0) + 1);
            }

            const baseGridStyle: React.CSSProperties = {
                display: shouldFillWidth ? 'grid' : 'inline-grid',
                width: shouldFillWidth ? '100%' : undefined,
                gridTemplateColumns: effectiveFrozenGridTemplateColumns ?? columnTemplate.join(' '),
                gridTemplateRows: rowTemplate.join(' '),
                justifyContent: effectiveGridLayout.gridJustification || 'start',
                alignItems: effectiveGridLayout.cellAlignment === 'stretch' ? 'start' : (effectiveGridLayout.cellAlignment || 'start'),
                justifyItems: effectiveGridLayout.cellAlignment === 'stretch' ? 'start' : (effectiveGridLayout.cellAlignment || 'start'),
            };

            return (
                <div
                    data-layout-type="grid"
                    data-component-id={componentId}
                    style={{
                        ...baseGridStyle,
                        ...(previewWidth ? { width: `${previewWidth}px` } : {}),
                    }}
                >
                    {structure.objects.map((obj) => {
                        const area = getObjectGridArea(obj.id, effectiveGridLayout);
                        if (!area) return null;

                        const rowIndex = rowByObjectId.get(obj.id);
                        const inRowGroup = rowIndex !== undefined ? (rowCounts.get(rowIndex) ?? 0) > 1 : false;

                        const isFlexObj = obj.type === 'input' || obj.type === 'display' || obj.type === 'divider';
                        const wrapperStyle: React.CSSProperties = {
                            gridRow: area.gridRow,
                            gridColumn: area.gridColumn,
                            // Important for grid children with long text: allow shrinking/wrapping instead of overflow.
                            minWidth: 0,
                            justifySelf: isFlexObj ? 'stretch' : 'start',
                            alignSelf: isFlexObj ? 'stretch' : 'start',
                            ...(isFlexObj ? { width: '100%' } : { display: 'inline-block' }),
                        };

                        return (
                            <div
                                key={obj.id}
                                data-object-id={obj.id}
                                data-grid-object={obj.id}
                                style={wrapperStyle}
                            >
                                {renderObject(obj, inRowGroup)}
                            </div>
                        );
                    })}
                </div>
            );
        })();

        // Main content
        const content = (
            isGridLayoutEnabled ? (
                gridContent
            ) : (
                <div style={containerStyle} data-component-id={componentId}>
                    {rows.map((row, index) => renderRow(row, index === rows.length - 1))}
                </div>
            )
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
