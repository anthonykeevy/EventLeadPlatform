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

        // Story 6.3.1 (UAT round 6) — Fix B: persisted ``*WidthOverride`` props
        // are now honoured outside the resize-preview path.
        //
        // Background: ``previewObjectWidthOverrides`` is a transient prop set
        // ONLY while the user is actively dragging a resize handle (see
        // ``SortableComponent.tsx`` — only populated when ``resizePreview`` is
        // active). The ``AppearanceSection`` writes the slider values to
        // ``component.props.{label,input,help,action}WidthOverride`` and those
        // values were silently ignored at render time because this lookup
        // short-circuited on ``!previewObjectWidthOverrides``. That regression
        // explains the user-reported "Appearance → Dimensions sliders no
        // longer change the object widths".
        //
        // Resolution order for an object's width override:
        //   1. Active resize preview (``previewObjectWidthOverrides``) — wins
        //      so the user sees real-time geometry while dragging.
        //   2. Persisted props (``component.props.*WidthOverride``) — applied
        //      always, including in the static rendered state.
        //   3. ``undefined`` — let the renderer/grid track decide (current
        //      behaviour for unspecified objects).
        const overrideKeyForObjectId = (objectId: string): keyof PreviewObjectWidthOverrides | undefined => {
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
            return overrideMap[objectId];
        };

        const getWidthOverride = (objectId: string): number | undefined => {
            const key = overrideKeyForObjectId(objectId);
            if (!key) return undefined;

            const previewValue = previewObjectWidthOverrides?.[key];
            if (typeof previewValue === 'number' && Number.isFinite(previewValue)) {
                return previewValue;
            }

            const persistedValue = component?.props?.[key];
            if (typeof persistedValue === 'number' && Number.isFinite(persistedValue)) {
                return persistedValue;
            }

            return undefined;
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
            // Story 6.3.1 (UAT round 6) — Fix A/B/C support: walk every cell so
            // the column-template builder can answer "which object lives in
            // column N?" in one place instead of re-scanning later.
            const objectIdByColumn = new Map<number, string>();
            const objectTypeByColumn = new Map<number, ComponentObject['type']>();
            for (const [key, objectId] of Object.entries(effectiveGridLayout.cellAssignments || {})) {
                const obj = structure.objects.find(o => o.id === objectId);
                const [rowStr, colStr] = key.split('-');
                void rowStr;
                const col = Number.parseInt(colStr, 10);
                if (!Number.isFinite(col)) continue;
                const span = effectiveGridLayout.objectSpans?.[objectId]?.colSpan ?? 1;

                // Track the *first* object placed in each column so the gap /
                // width fallback chains can introspect column membership. If
                // multiple objects share a column (overlay use-case) the first
                // one wins — that's the column the renderer actually paints.
                for (let i = 0; i < Math.max(1, span); i += 1) {
                    const c = col + i;
                    if (!objectIdByColumn.has(c)) {
                        objectIdByColumn.set(c, objectId);
                        if (obj?.type) objectTypeByColumn.set(c, obj.type);
                    }
                }

                const isFlexObj = obj && (obj.type === 'input' || obj.type === 'display' || obj.type === 'divider');
                if (!isFlexObj && objectId !== 'input') continue;
                for (let i = 0; i < Math.max(1, span); i += 1) {
                    flexColumnSet.add(col + i);
                }
            }

            // Story 6.3.1 (UAT round 6) — Fix A: bridge the Typography & Colors
            // ``labelGap`` / ``inputHelpGap`` (Layer 2 spacing) into Grid mode
            // so the slider users adjust to set "gap between label and input"
            // is no longer silently ignored when the form switches to Grid
            // layout (the regression that triggered the user's "I think this
            // happened when we switched from object layout to grid layout"
            // observation).
            //
            // Resolution order for the gap track between columns ``c`` and
            // ``c+1``:
            //   1. ``effectiveGridLayout.columnGaps[c]`` — explicit per-column
            //      override from Grid Layout → "Individual Column Spacing".
            //      Wins because the user set it directly for this gap track.
            //   2. ``labelGapPx`` (Typography & Colors) — when columns ``c``
            //      and ``c+1`` host a label↔input/display pair (the original
            //      Layer 2 semantics).
            //   3. ``inputHelpGapPx`` — when columns host an input↔validation
            //      / input↔help pair.
            //   4. ``effectiveGridLayout.columnGap`` — generic grid default.
            const labelGapPx = fieldStyles.computed.labelGap;
            const inputHelpGapPx = fieldStyles.computed.inputHelpGap;

            const isLabelType = (t: ComponentObject['type'] | undefined) => t === 'label';
            const isInputLikeType = (t: ComponentObject['type'] | undefined) =>
                t === 'input' || t === 'display' || t === 'action';
            const isHelpLikeType = (t: ComponentObject['type'] | undefined) =>
                t === 'validation' || t === 'help';

            const resolveLayer2GapPx = (
                leftType: ComponentObject['type'] | undefined,
                rightType: ComponentObject['type'] | undefined
            ): number | undefined => {
                if (
                    (isLabelType(leftType) && isInputLikeType(rightType)) ||
                    (isInputLikeType(leftType) && isLabelType(rightType))
                ) {
                    return labelGapPx;
                }
                if (
                    (isInputLikeType(leftType) && isHelpLikeType(rightType)) ||
                    (isHelpLikeType(leftType) && isInputLikeType(rightType))
                ) {
                    return inputHelpGapPx;
                }
                return undefined;
            };

            // Story 6.3.1 (UAT round 6) — Fix B+C: per-column track resolution.
            //
            // For LABEL columns the resolution order is:
            //   1. ``getWidthOverride('label')`` — already merges resize-preview
            //      and persisted ``props.labelWidthOverride`` (Fix B).
            //   2. ``globalStyles.horizontalLabelBandPx`` — form-wide label
            //      band so every component lines up at the same input
            //      left-edge (Fix C — the AI compiler stamps this for
            //      horizontal-mode forms).
            //   3. ``'auto'`` — original content-sized behaviour.
            //
            // For INPUT-like columns the resolution order is:
            //   1. Persisted ``props.{input,help,action}WidthOverride`` (Fix B)
            //      pinned as an absolute px track when set — otherwise the
            //      explicit slider value gets swallowed by the ``1fr``
            //      flex-track fallback below.
            //   2. The original flex/auto branches (unchanged).
            const resolveColumnTrack = (col: number): string => {
                const objectId = objectIdByColumn.get(col);
                const objectType = objectTypeByColumn.get(col);

                if (isLabelType(objectType)) {
                    const explicitLabelPx = getWidthOverride(objectId ?? 'label');
                    if (typeof explicitLabelPx === 'number' && explicitLabelPx > 0) {
                        // Story 6.3.1 (UAT round 11) — terms label uses
                        // ``fit-content(px)`` so the track is content-sized
                        // up to the override cap.
                        //
                        // The AI compiler stamps ``labelWidthOverride`` only
                        // for the terms component (Fix G item 3). The value
                        // is a WORST-CASE estimate (consent_chars *
                        // AVG_CHAR_PX + padding); the actual rendered text
                        // is usually narrower. A previous attempt used
                        // ``minmax(0, ${px}px)`` to let the track shrink,
                        // but Grid's default ``justify-self: stretch`` keeps
                        // the label filling whatever the track sizes to —
                        // and the track resolves to its max via the
                        // standard intrinsic-sizing pass, so the gap
                        // persisted (UAT round 11 #3 — "Even after a
                        // refresh it still looks the same").
                        //
                        // ``fit-content(${px}px)`` is the right primitive:
                        // it sizes the track to ``min(max-content, ${px}px)``
                        // without depending on item ``justify-self``. So the
                        // consent text gets a track exactly its rendered
                        // width, and the validation column slides up next
                        // to it with no trailing whitespace. The cap still
                        // protects against pathologically long consent
                        // copy (rare, but possible — guarantees the
                        // validation column never gets pushed off-screen).
                        //
                        // For NON-terms components the override is user-set
                        // (Properties Panel → Appearance → Dimensions) and
                        // expresses an intentional pin; we keep the
                        // original fixed-px track so manual sizing still
                        // works.
                        if (component?.type === 'terms') {
                            return `fit-content(${explicitLabelPx}px)`;
                        }
                        return `${explicitLabelPx}px`;
                    }
                    const formWideBand = globalStyles?.horizontalLabelBandPx;
                    if (typeof formWideBand === 'number' && formWideBand > 0) {
                        return `${formWideBand}px`;
                    }
                    return 'auto';
                }

                // Non-label columns: a persisted ``*WidthOverride`` from
                // Appearance → Dimensions should pin the column track even
                // when the column would otherwise stretch as 1fr.
                if (objectId) {
                    const explicitObjectPx = getWidthOverride(objectId);
                    if (typeof explicitObjectPx === 'number' && explicitObjectPx > 0) {
                        return `${explicitObjectPx}px`;
                    }
                }

                // Story 6.3.1 (UAT round 11) — rating intrinsic-content floor.
                //
                // CSS Grid sizes columns by the track rule, NOT by the inner
                // content's overflow. ``minmax(0, 1fr)`` means "0 floor, take
                // a share of leftover space" — when the rating renderer holds
                // 10 stars (~300 px wide) inside a 1fr-of-leftover track that
                // only got ~200 px, the ``flex-wrap: nowrap`` row visually
                // overflows RIGHTWARD into the validation column, causing the
                // overlap the UAT-round-11 preview screenshot shows.
                //
                // Resolution: for ``rating`` only, raise the input-track floor
                // to ``max-content`` so the column itself grows to the actual
                // star-row width and the validation column is pushed past it.
                // The wrapper may overflow horizontally if the user added
                // stars beyond the AI-reserved bounding box (an honest cue
                // that the component needs more room), but the validation
                // pill no longer collides with the stars.
                //
                // Other input-like components (text, dropdown, paragraph,
                // textarea) keep the ``minmax(0, 1fr)`` track because their
                // ``max-content`` would over-claim space (long placeholder /
                // dropdown options / paragraph text) and squeeze validation
                // off-screen. They naturally absorb-or-shrink with the
                // wrapper which is the correct framework-first behaviour.
                if (flexColumnSet.has(col)) {
                    if (
                        component?.type === 'rating' &&
                        isInputLikeType(objectType)
                    ) {
                        return shouldFillWidth
                            ? 'minmax(max-content, 1fr)'
                            : 'max-content';
                    }
                    return shouldFillWidth ? 'minmax(0, 1fr)' : 'auto';
                }
                return shouldFillWidth ? 'minmax(0, max-content)' : 'auto';
            };

            const columnTemplate: string[] = [];
            for (let col = 0; col < effectiveGridLayout.columns; col += 1) {
                columnTemplate.push(resolveColumnTrack(col));
                if (col < effectiveGridLayout.columns - 1) {
                    const explicitColumnGap = effectiveGridLayout.columnGaps?.[col];
                    let gap: number;
                    if (typeof explicitColumnGap === 'number' && Number.isFinite(explicitColumnGap)) {
                        gap = explicitColumnGap;
                    } else {
                        const layer2Gap = resolveLayer2GapPx(
                            objectTypeByColumn.get(col),
                            objectTypeByColumn.get(col + 1)
                        );
                        gap = typeof layer2Gap === 'number' ? layer2Gap : effectiveGridLayout.columnGap;
                    }
                    columnTemplate.push(`${gap}px`);
                }
            }

            // Rows: keep as auto (with explicit gap tracks) so the shell height matches content.
            // Story 6.3.1 (UAT round 6) — Fix A also bridges Layer 2 spacing
            // into the row-gap chain. Same precedence as columnGaps: explicit
            // per-row override → label/input/validation Layer 2 gap (when the
            // adjacent rows host the matching object pair) → grid default.
            const objectTypeByRow = new Map<number, ComponentObject['type']>();
            for (const [key, objectId] of Object.entries(effectiveGridLayout.cellAssignments || {})) {
                const obj = structure.objects.find(o => o.id === objectId);
                const [rowStr] = key.split('-');
                const r = Number.parseInt(rowStr, 10);
                if (!Number.isFinite(r)) continue;
                if (!objectTypeByRow.has(r) && obj?.type) objectTypeByRow.set(r, obj.type);
            }

            const rowTemplate: string[] = [];
            for (let row = 0; row < effectiveGridLayout.rows; row += 1) {
                rowTemplate.push('auto');
                if (row < effectiveGridLayout.rows - 1) {
                    const explicitRowGap = effectiveGridLayout.rowGaps?.[row];
                    let gap: number;
                    if (typeof explicitRowGap === 'number' && Number.isFinite(explicitRowGap)) {
                        gap = explicitRowGap;
                    } else {
                        const layer2Gap = resolveLayer2GapPx(
                            objectTypeByRow.get(row),
                            objectTypeByRow.get(row + 1)
                        );
                        gap = typeof layer2Gap === 'number' ? layer2Gap : effectiveGridLayout.rowGap;
                    }
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
                        // Story 6.3.1 (UAT round 6) — Fix B/C: when a label /
                        // validation column has an explicit pixel track (per-
                        // component override or form-wide ``horizontalLabelBandPx``)
                        // the wrapper should fill the column band so the inner
                        // label/help text wraps cleanly within the reserved
                        // width instead of shrink-wrapping to its intrinsic
                        // length and leaving the band visually empty on the
                        // right.
                        const hasExplicitObjectWidth = (() => {
                            const persisted = getWidthOverride(obj.id);
                            if (typeof persisted === 'number' && persisted > 0) return true;
                            if (
                                obj.type === 'label' &&
                                typeof globalStyles?.horizontalLabelBandPx === 'number' &&
                                globalStyles.horizontalLabelBandPx > 0
                            ) {
                                return true;
                            }
                            return false;
                        })();
                        const wrapperStyle: React.CSSProperties = {
                            gridRow: area.gridRow,
                            gridColumn: area.gridColumn,
                            // Important for grid children with long text: allow shrinking/wrapping instead of overflow.
                            minWidth: 0,
                            justifySelf: isFlexObj || hasExplicitObjectWidth ? 'stretch' : 'start',
                            alignSelf: isFlexObj ? 'stretch' : 'start',
                            ...(isFlexObj || hasExplicitObjectWidth
                                ? { width: '100%' }
                                : { display: 'inline-block' }),
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
