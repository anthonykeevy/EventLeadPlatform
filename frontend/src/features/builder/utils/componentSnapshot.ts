/**
 * Component Snapshot Utility
 * 
 * Utility to capture complete component state for logging drag, resize, and collision operations.
 */

import { FormComponent, ComponentProps } from '../types/builder.types';
import { useBuilderStore } from '../stores/useBuilderStore';
import React from 'react';

export interface ComponentSnapshot {
    componentId: string;
    componentType: string;
    position: { x: number; y: number };
    dimensions: { width?: string; height?: number; scale?: number };
    props: Partial<ComponentProps>;
    objectWidths?: Record<string, number>;
    objectWidthsSource?: 'dom-grid' | 'dom-groups' | 'unknown';
    objectMetrics?: Record<string, ObjectMetrics>;
    gridMetrics?: {
        containerWidth: number;
        containerHeight: number;
        containerWidthCanvas?: number;
        gridTemplateColumns: string;
        gridTemplateRows: string;
        templateColumnsPx?: Array<number | string>;
        templateRowsPx?: Array<number | string>;
        columnGap: string;
        rowGap: string;
        columnGapPx?: number;
        rowGapPx?: number;
        paddingLeft: string;
        paddingRight: string;
        paddingTop: string;
        paddingBottom: string;
        paddingLeftPx?: number;
        paddingRightPx?: number;
        paddingTopPx?: number;
        paddingBottomPx?: number;
        borderLeft: string;
        borderRight: string;
        borderTop: string;
        borderBottom: string;
        borderLeftPx?: number;
        borderRightPx?: number;
        borderTopPx?: number;
        borderBottomPx?: number;
        boxSizing: string;
        alignItems?: string;
        justifyItems?: string;
        alignContent?: string;
        justifyContent?: string;
    };
    bounds: DOMRectLike | null;
    smartBorderBounds: DOMRectLike | null;
    canvasMetrics?: CanvasMetrics;
    canvasBounds?: DOMRectLike | null;
    canvasSmartBorderBounds?: DOMRectLike | null;
    timestamp: number;
}

export interface ObjectMetrics {
    objectId: string;
    rect: DOMRectLike;
    relativeRect?: DOMRectLike;
    canvasRect?: DOMRectLike;
    canvasRelativeRect?: DOMRectLike;
    padding: BoxEdges;
    border: BoxEdges;
    alignSelf?: string;
    justifySelf?: string;
    gridRow?: string;
    gridColumn?: string;
    source?: 'grid' | 'layout';
    // Text wrapping detection
    isTextWrapped?: boolean;
    scrollWidth?: number;
    clientWidth?: number;
    lineCount?: number;
    isMultiLine?: boolean;
}

export interface CanvasMetrics {
    canvasWidth: number;
    canvasHeight: number;
    canvasScale: number;
    screenToCanvasRatio: number;
    canvasToScreenRatio: number;
}

export interface BoxEdges {
    top: number;
    right: number;
    bottom: number;
    left: number;
}

export interface DOMRectLike {
    x: number;
    y: number;
    width: number;
    height: number;
    top: number;
    right: number;
    bottom: number;
    left: number;
}

/**
 * Capture a snapshot of a component's current state.
 * Includes position, dimensions, props, and DOM bounds.
 */
export function captureComponentSnapshot(
    component: FormComponent,
    containerRef: React.RefObject<HTMLDivElement> | null
): ComponentSnapshot {
    // Try to get bounds from ref first
    let bounds: DOMRect | null = containerRef?.current?.getBoundingClientRect() || null;
    let element: HTMLElement | null = containerRef?.current || null;
    
    // If no ref provided, try to find element by data-component-id attribute
    if (!bounds && typeof document !== 'undefined') {
        element = document.querySelector(`[data-component-id="${component.id}"]`) as HTMLElement;
        bounds = element?.getBoundingClientRect() || null;
    }

    const parsePx = (value: string | null) => {
        if (!value) return 0;
        const parsed = parseFloat(value);
        return Number.isFinite(parsed) ? parsed : 0;
    };

    const parseTrackSizes = (value: string) => {
        if (!value) return [];
        return value.split(' ').map(track => {
            if (track.endsWith('px')) return parseFloat(track);
            return track;
        });
    };

    const getMeasurementElement = (node: HTMLElement) => {
        const style = typeof window !== 'undefined' ? window.getComputedStyle(node) : null;
        if (style?.display === 'contents' && node.firstElementChild instanceof HTMLElement) {
            return node.firstElementChild as HTMLElement;
        }
        return node;
    };

    const getCanvasMetrics = (): CanvasMetrics | null => {
        if (typeof window === 'undefined') return null;
        try {
            const state = useBuilderStore.getState();
            const canvasSettings = state.formDefinition?.canvasSettings;
            const canvasWidth = canvasSettings?.width || 1920;
            const canvasHeight = canvasSettings?.height || 980;
            const canvasScale = state.scale || 1;
            const screenToCanvasRatio = canvasScale ? 1 / canvasScale : 1;
            return {
                canvasWidth,
                canvasHeight,
                canvasScale,
                screenToCanvasRatio,
                canvasToScreenRatio: canvasScale || 1,
            };
        } catch {
            return null;
        }
    };

    const canvasMetrics = getCanvasMetrics();
    const toCanvasRect = (rect: DOMRectLike): DOMRectLike => {
        if (!canvasMetrics) return rect;
        const ratio = canvasMetrics.screenToCanvasRatio || 1;
        return {
            x: rect.x * ratio,
            y: rect.y * ratio,
            width: rect.width * ratio,
            height: rect.height * ratio,
            top: rect.top * ratio,
            right: rect.right * ratio,
            bottom: rect.bottom * ratio,
            left: rect.left * ratio,
        };
    };

    let objectWidths: Record<string, number> | undefined;
    let objectWidthsSource: ComponentSnapshot['objectWidthsSource'] = 'unknown';
    let objectMetrics: Record<string, ObjectMetrics> | undefined;
    const root = element ?? null;
    if (root && typeof window !== 'undefined') {
        const gridObjects = Array.from(
            root.querySelectorAll('[data-grid-object]'),
        ) as HTMLElement[];
        if (gridObjects.length > 0) {
            objectWidths = {};
            objectMetrics = {};
            gridObjects.forEach(node => {
                const objectId = node.getAttribute('data-grid-object') || node.getAttribute('data-object-id') || 'unknown';
                const target = getMeasurementElement(node);
                const rect = target.getBoundingClientRect();
                const styles = window.getComputedStyle(target);
                objectWidths![objectId] = Math.round(rect.width);
                
                // Detect if text is wrapped by checking if element has multiple lines
                // Method 1: getClientRects() returns one rect per line of inline content
                // Method 2: Check if actual height > expected single-line height
                const scrollWidth = target.scrollWidth;
                const clientWidth = target.clientWidth;
                const clientRects = target.getClientRects();
                const lineCount = clientRects.length;
                
                // Text is wrapped if there's more than one line rect
                // Also check height vs line-height as a fallback
                const computedLineHeight = parseFloat(styles.lineHeight) || parseFloat(styles.fontSize) * 1.2;
                const actualHeight = rect.height;
                const expectedSingleLineHeight = computedLineHeight + parsePx(styles.paddingTop) + parsePx(styles.paddingBottom);
                const isMultiLine = actualHeight > expectedSingleLineHeight * 1.2; // 20% tolerance
                
                const isTextWrapped = lineCount > 1 || isMultiLine;
                
                objectMetrics![objectId] = {
                    objectId,
                    isTextWrapped,
                    scrollWidth,
                    clientWidth,
                    lineCount,
                    isMultiLine,
                    rect: {
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height,
                        top: rect.top,
                        right: rect.right,
                        bottom: rect.bottom,
                        left: rect.left,
                    },
                    canvasRect: canvasMetrics ? toCanvasRect({
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height,
                        top: rect.top,
                        right: rect.right,
                        bottom: rect.bottom,
                        left: rect.left,
                    }) : undefined,
                    relativeRect: bounds
                        ? {
                            x: rect.x - bounds.x,
                            y: rect.y - bounds.y,
                            width: rect.width,
                            height: rect.height,
                            top: rect.top - bounds.top,
                            right: rect.right - bounds.left,
                            bottom: rect.bottom - bounds.top,
                            left: rect.left - bounds.left,
                        }
                        : undefined,
                    canvasRelativeRect: bounds && canvasMetrics
                        ? toCanvasRect({
                            x: rect.x - bounds.x,
                            y: rect.y - bounds.y,
                            width: rect.width,
                            height: rect.height,
                            top: rect.top - bounds.top,
                            right: rect.right - bounds.left,
                            bottom: rect.bottom - bounds.top,
                            left: rect.left - bounds.left,
                        })
                        : undefined,
                    padding: {
                        top: parsePx(styles.paddingTop),
                        right: parsePx(styles.paddingRight),
                        bottom: parsePx(styles.paddingBottom),
                        left: parsePx(styles.paddingLeft),
                    },
                    border: {
                        top: parsePx(styles.borderTopWidth),
                        right: parsePx(styles.borderRightWidth),
                        bottom: parsePx(styles.borderBottomWidth),
                        left: parsePx(styles.borderLeftWidth),
                    },
                    alignSelf: styles.alignSelf,
                    justifySelf: styles.justifySelf,
                    gridRow: styles.gridRow,
                    gridColumn: styles.gridColumn,
                    source: 'grid',
                };
            });
            objectWidthsSource = 'dom-grid';
        } else {
            const layoutObjects = Array.from(
                root.querySelectorAll('[data-object-id]'),
            ) as HTMLElement[];
            if (layoutObjects.length > 0) {
                objectMetrics = {};
                layoutObjects.forEach(node => {
                    const objectId = node.getAttribute('data-object-id') || 'unknown';
                    const target = getMeasurementElement(node);
                    const rect = target.getBoundingClientRect();
                    const styles = window.getComputedStyle(target);
                    objectMetrics![objectId] = {
                        objectId,
                        rect: {
                            x: rect.x,
                            y: rect.y,
                            width: rect.width,
                            height: rect.height,
                            top: rect.top,
                            right: rect.right,
                            bottom: rect.bottom,
                            left: rect.left,
                        },
                        canvasRect: canvasMetrics ? toCanvasRect({
                            x: rect.x,
                            y: rect.y,
                            width: rect.width,
                            height: rect.height,
                            top: rect.top,
                            right: rect.right,
                            bottom: rect.bottom,
                            left: rect.left,
                        }) : undefined,
                        relativeRect: bounds
                            ? {
                                x: rect.x - bounds.x,
                                y: rect.y - bounds.y,
                                width: rect.width,
                                height: rect.height,
                                top: rect.top - bounds.top,
                                right: rect.right - bounds.left,
                                bottom: rect.bottom - bounds.top,
                                left: rect.left - bounds.left,
                            }
                            : undefined,
                        canvasRelativeRect: bounds && canvasMetrics
                            ? toCanvasRect({
                                x: rect.x - bounds.x,
                                y: rect.y - bounds.y,
                                width: rect.width,
                                height: rect.height,
                                top: rect.top - bounds.top,
                                right: rect.right - bounds.left,
                                bottom: rect.bottom - bounds.top,
                                left: rect.left - bounds.left,
                            })
                            : undefined,
                        padding: {
                            top: parsePx(styles.paddingTop),
                            right: parsePx(styles.paddingRight),
                            bottom: parsePx(styles.paddingBottom),
                            left: parsePx(styles.paddingLeft),
                        },
                        border: {
                            top: parsePx(styles.borderTopWidth),
                            right: parsePx(styles.borderRightWidth),
                            bottom: parsePx(styles.borderBottomWidth),
                            left: parsePx(styles.borderLeftWidth),
                        },
                        alignSelf: styles.alignSelf,
                        justifySelf: styles.justifySelf,
                        source: 'layout',
                    };
                });
                objectWidthsSource = 'dom-groups';
            }
        }
    }

    let gridMetrics: ComponentSnapshot['gridMetrics'];
    if (root && typeof window !== 'undefined') {
        const gridContainer = root.querySelector('[data-layout-type="grid"]') as HTMLElement | null;
        if (gridContainer) {
            const styles = window.getComputedStyle(gridContainer);
            const gridBounds = gridContainer.getBoundingClientRect();
            const resolvedColumnGap = parsePx(styles.columnGap);
            const resolvedRowGap = parsePx(styles.rowGap);
            let computedColumnGap: number | undefined;
            if (objectMetrics && (styles.columnGap === 'normal' || resolvedColumnGap === 0)) {
                const entries = Object.values(objectMetrics)
                    .map(metric => metric.relativeRect || metric.rect)
                    .filter(Boolean)
                    .sort((a, b) => (a.left ?? 0) - (b.left ?? 0));
                const gaps: number[] = [];
                for (let i = 0; i < entries.length - 1; i += 1) {
                    const current = entries[i];
                    const next = entries[i + 1];
                    const gap = (next.left ?? 0) - ((current.left ?? 0) + (current.width ?? 0));
                    if (Number.isFinite(gap) && gap >= 0) gaps.push(gap);
                }
                if (gaps.length) {
                    computedColumnGap = gaps.reduce((sum, value) => sum + value, 0) / gaps.length;
                }
            }
            gridMetrics = {
                containerWidth: Math.round(gridBounds.width),
                containerHeight: Math.round(gridBounds.height),
                containerWidthCanvas: canvasMetrics ? Math.round(gridBounds.width * (canvasMetrics.screenToCanvasRatio || 1)) : undefined,
                gridTemplateColumns: styles.gridTemplateColumns,
                gridTemplateRows: styles.gridTemplateRows,
                templateColumnsPx: parseTrackSizes(styles.gridTemplateColumns),
                templateRowsPx: parseTrackSizes(styles.gridTemplateRows),
                columnGap: styles.columnGap,
                rowGap: styles.rowGap,
                columnGapPx: resolvedColumnGap || computedColumnGap,
                rowGapPx: resolvedRowGap || undefined,
                paddingLeft: styles.paddingLeft,
                paddingRight: styles.paddingRight,
                paddingTop: styles.paddingTop,
                paddingBottom: styles.paddingBottom,
                paddingLeftPx: parsePx(styles.paddingLeft),
                paddingRightPx: parsePx(styles.paddingRight),
                paddingTopPx: parsePx(styles.paddingTop),
                paddingBottomPx: parsePx(styles.paddingBottom),
                borderLeft: styles.borderLeftWidth,
                borderRight: styles.borderRightWidth,
                borderTop: styles.borderTopWidth,
                borderBottom: styles.borderBottomWidth,
                borderLeftPx: parsePx(styles.borderLeftWidth),
                borderRightPx: parsePx(styles.borderRightWidth),
                borderTopPx: parsePx(styles.borderTopWidth),
                borderBottomPx: parsePx(styles.borderBottomWidth),
                boxSizing: styles.boxSizing,
                alignItems: styles.alignItems,
                justifyItems: styles.justifyItems,
                alignContent: styles.alignContent,
                justifyContent: styles.justifyContent,
            };
        }
    }
    
    return {
        componentId: component.id,
        componentType: component.type,
        position: component.position || { x: 0, y: 0 },
        dimensions: {
            width: component.props.width,
            height: component.props.height,
            scale: component.props.componentScale
        },
        props: {
            objectLayout: component.props.objectLayout,
            layoutGroups: component.props.layoutGroups,
            objectSpacing: component.props.objectSpacing,
            styleOverrides: component.props.styleOverrides,
            required: component.props.required,
            label: component.props.label,
            gridLayout: component.props.gridLayout,
            rowAlignment: component.props.rowAlignment,
            labelGapOverride: component.props.labelGapOverride,
            inputHelpGapOverride: component.props.inputHelpGapOverride,
            labelWidthOverride: component.props.labelWidthOverride,
            inputWidthOverride: component.props.inputWidthOverride,
            helpWidthOverride: component.props.helpWidthOverride,
        },
        objectWidths,
        objectWidthsSource,
        objectMetrics,
        gridMetrics,
        bounds: bounds ? {
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            top: bounds.top,
            right: bounds.right,
            bottom: bounds.bottom,
            left: bounds.left
        } : null,
        smartBorderBounds: bounds ? {
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            top: bounds.top,
            right: bounds.right,
            bottom: bounds.bottom,
            left: bounds.left
        } : null,
        canvasMetrics: canvasMetrics || undefined,
        canvasBounds: bounds && canvasMetrics ? toCanvasRect({
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            top: bounds.top,
            right: bounds.right,
            bottom: bounds.bottom,
            left: bounds.left
        }) : null,
        canvasSmartBorderBounds: bounds && canvasMetrics ? toCanvasRect({
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            top: bounds.top,
            right: bounds.right,
            bottom: bounds.bottom,
            left: bounds.left
        }) : null,
        timestamp: Date.now()
    };
}

/**
 * Capture snapshots for all components.
 * Useful for collision detection logging.
 */
export function captureAllComponentsSnapshot(
    components: FormComponent[],
    componentRefs: Map<string, React.RefObject<HTMLDivElement>>
): ComponentSnapshot[] {
    return components.map(component => {
        const ref = componentRefs.get(component.id);
        return captureComponentSnapshot(component, ref || null);
    });
}



