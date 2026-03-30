/**
 * Collision Detection Utilities
 * 
 * Utilities for detecting collisions between components using SmartBorder container bounds.
 * Also includes canvas boundary detection to prevent components from being dragged outside.
 */

import React from 'react';
import { FormComponent } from '../types/builder.types';
import { captureComponentSnapshot, ComponentSnapshot } from './componentSnapshot';
import { devLogger } from './devLogger';

/**
 * Canvas boundary result
 */
export interface CanvasBoundaryResult {
    isOutOfBounds: boolean;
    constrainedPosition: { x: number; y: number };
    violations: {
        left: boolean;
        right: boolean;
        top: boolean;
        bottom: boolean;
    };
}

/**
 * Check if a component would be out of canvas bounds and constrain position
 * @param newX - Proposed new X position (in canvas coordinates, not screen pixels)
 * @param newY - Proposed new Y position (in canvas coordinates, not screen pixels)
 * @param componentWidth - Width of the component in base pixels (before scale)
 * @param componentHeight - Height of the component in base pixels (before scale)
 * @param canvasWidth - Canvas width in base pixels
 * @param canvasHeight - Canvas height in base pixels
 * @param padding - Optional padding from canvas edges (default: 0)
 */
export function checkCanvasBoundary(
    newX: number,
    newY: number,
    componentWidth: number,
    componentHeight: number,
    canvasWidth: number,
    canvasHeight: number,
    padding: number = 0
): CanvasBoundaryResult {
    const minX = padding;
    const maxX = canvasWidth - componentWidth - padding;
    const minY = padding;
    const maxY = canvasHeight - componentHeight - padding;
    
    const violations = {
        left: newX < minX,
        right: newX > maxX,
        top: newY < minY,
        bottom: newY > maxY,
    };
    
    const isOutOfBounds = violations.left || violations.right || violations.top || violations.bottom;
    
    // Constrain position to canvas bounds
    const constrainedX = Math.max(minX, Math.min(maxX, newX));
    const constrainedY = Math.max(minY, Math.min(maxY, newY));
    
    if (isOutOfBounds) {
        // Calculate edge positions relative to canvas
        const proposedWestEdge = newX;
        const proposedEastEdge = newX + componentWidth;
        const proposedNorthEdge = newY;
        const proposedSouthEdge = newY + componentHeight;
        
        const constrainedWestEdge = constrainedX;
        const constrainedEastEdge = constrainedX + componentWidth;
        const constrainedNorthEdge = constrainedY;
        const constrainedSouthEdge = constrainedY + componentHeight;
        
        // Calculate gaps from canvas edges
        const gapFromLeft = constrainedWestEdge - minX;
        const gapFromRight = maxX + componentWidth - constrainedEastEdge;
        const gapFromTop = constrainedNorthEdge - minY;
        const gapFromBottom = maxY + componentHeight - constrainedSouthEdge;
        
        devLogger.info('collision.boundary.check', {
            proposedPosition: { x: newX, y: newY },
            constrainedPosition: { x: constrainedX, y: constrainedY },
            componentSize: { width: componentWidth, height: componentHeight },
            canvasSize: { width: canvasWidth, height: canvasHeight },
            violations,
            edgePositions: {
                proposed: {
                    west: proposedWestEdge,
                    east: proposedEastEdge,
                    north: proposedNorthEdge,
                    south: proposedSouthEdge
                },
                constrained: {
                    west: constrainedWestEdge,
                    east: constrainedEastEdge,
                    north: constrainedNorthEdge,
                    south: constrainedSouthEdge
                },
                canvas: {
                    left: minX,
                    right: maxX + componentWidth,
                    top: minY,
                    bottom: maxY + componentHeight
                }
            },
            gapsFromCanvasEdges: {
                left: gapFromLeft,
                right: gapFromRight,
                top: gapFromTop,
                bottom: gapFromBottom
            }
        });
    }
    
    return {
        isOutOfBounds,
        constrainedPosition: { x: constrainedX, y: constrainedY },
        violations,
    };
}

/**
 * Get component dimensions from DOM element or estimate from props
 * @param component - The form component
 * @param componentElement - Optional DOM element to measure
 * @param scale - Current canvas scale (percentage, e.g., 100 for 100%)
 */
export function getComponentDimensions(
    component: FormComponent,
    componentElement?: HTMLElement | null,
    scale: number = 100
): { width: number; height: number } {
    const scaleFactor = scale / 100;
    
    // Try to get from DOM element first
    if (componentElement) {
        // The canvas has a CSS transform: scale(scaleFactor) applied.
        // offsetWidth/offsetHeight return CSS dimensions, which are NOT affected by parent transforms.
        // So offsetWidth is already in canvas coordinates (not screen pixels).
        // 
        // Option 1: Use getBoundingClientRect().width (screen pixels) and divide by scale
        // Option 2: Use offsetWidth directly (already in canvas coordinates)
        //
        // Using getBoundingClientRect is more accurate as it includes any transforms on the element itself.
        const rect = componentElement.getBoundingClientRect();
        const screenWidth = rect.width;
        const screenHeight = rect.height;
        
        // Convert screen pixels to canvas coordinates by dividing by scale
        const calculatedWidth = screenWidth / scaleFactor;
        const calculatedHeight = screenHeight / scaleFactor;
        
        // Log dimension calculation for debugging
        devLogger.info('collision.dimension.calculated', {
            componentId: component.id,
            componentType: component.type,
            propsWidth: component.props.width,
            domMeasurement: {
                offsetWidth: componentElement.offsetWidth,
                offsetHeight: componentElement.offsetHeight,
                getBoundingClientRect: {
                    width: screenWidth,
                    height: screenHeight
                }
            },
            scale,
            scaleFactor,
            calculatedDimensions: {
                width: calculatedWidth,
                height: calculatedHeight
            },
            note: 'Using getBoundingClientRect (screen pixels) / scaleFactor for accurate canvas coordinates'
        });
        
        return {
            width: calculatedWidth,
            height: calculatedHeight,
        };
    }
    
    // Fallback: estimate from component props
    const widthProp = component.props.width;
    let width = 300; // default
    
    if (widthProp) {
        if (widthProp.endsWith('px')) {
            width = parseInt(widthProp, 10);
        } else if (widthProp.endsWith('%')) {
            // Percentage - use a reasonable default
            width = 300;
        }
    }
    
    // Estimate height based on component type
    const heightEstimates: Record<string, number> = {
        'divider': 20,
        'header': 40,
        'submit-button': 60,
        // Input fields (label + input + validation)
        'first-name': 100,
        'text': 100,
        'email': 100,
        'phone': 100,
        'number': 100,
        'date': 100,
        'dropdown': 200,
        'checkbox': 60,
        'radio': 80,
        'textarea': 150,
        'address': 100,
        'terms': 60,
    };
    
    const height = heightEstimates[component.type] || 100;
    
    return { width, height };
}

/**
 * Check if two DOM rectangles overlap
 */
export function boxesOverlap(rect1: DOMRect, rect2: DOMRect): boolean {
    return !(
        rect1.right < rect2.left ||
        rect1.left > rect2.right ||
        rect1.bottom < rect2.top ||
        rect1.top > rect2.bottom
    );
}

/**
 * Calculate overlap area between two rectangles
 */
export function calculateOverlapArea(rect1: DOMRect, rect2: DOMRect): number {
    const overlapLeft = Math.max(rect1.left, rect2.left);
    const overlapRight = Math.min(rect1.right, rect2.right);
    const overlapTop = Math.max(rect1.top, rect2.top);
    const overlapBottom = Math.min(rect1.bottom, rect2.bottom);
    
    if (overlapRight <= overlapLeft || overlapBottom <= overlapTop) {
        return 0;
    }
    
    return (overlapRight - overlapLeft) * (overlapBottom - overlapTop);
}

/**
 * Get component bounds from SmartBorder container element
 */
export function getComponentBounds(componentElement: HTMLElement): DOMRect | null {
    const resolveFromSmartBorder = (container: HTMLElement): DOMRect | null => {
        // Prefer the SmartBorder SVG path bounds (closer to the visible border) over the wrapper rect.
        // Note: this is still an axis-aligned bounding box, but matches the SmartBorder geometry better than the container box.
        const smartPath = container.querySelector('svg > path[stroke="currentColor"][fill="transparent"]') as SVGPathElement | null;
        const pathRect = smartPath?.getBoundingClientRect();
        if (pathRect && pathRect.width > 0 && pathRect.height > 0) return pathRect;
        return container.getBoundingClientRect();
    };

    // SmartBorder container is the outermost element with data-component-id
    if (componentElement.hasAttribute('data-component-id')) {
        return resolveFromSmartBorder(componentElement);
    }

    // Fallback: find SmartBorder container by data-component-id
    const smartBorderContainer = componentElement.querySelector('[data-component-id]') as HTMLElement | null;
    if (smartBorderContainer) return resolveFromSmartBorder(smartBorderContainer);
    return componentElement.getBoundingClientRect();
}

/**
 * Check for collisions between a dragged component and all other components
 * Uses SmartBorder container bounds for accurate collision detection
 */
export function checkCollision(
    draggedComponent: FormComponent,
    allComponents: FormComponent[],
    componentRefs: Map<string, React.RefObject<HTMLDivElement>> | null | undefined
): { hasCollision: boolean; collidingComponents: ComponentSnapshot[] } {
    if (!componentRefs) return { hasCollision: false, collidingComponents: [] };
    // Try to get dragged component bounds from ref first, then fall back to DOM query
    let draggedBounds: DOMRect | null = null;
    const draggedRef = componentRefs.get(draggedComponent.id);
    
    if (draggedRef?.current) {
        draggedBounds = getComponentBounds(draggedRef.current);
    } else if (typeof document !== 'undefined') {
        // Fallback: find element by data-component-id
        const draggedElement = document.querySelector(`[data-component-id="${draggedComponent.id}"]`) as HTMLElement;
        if (draggedElement) {
            draggedBounds = getComponentBounds(draggedElement);
        }
    }
    
    if (!draggedBounds) {
        devLogger.debug('fieldshell.collision.checked', {
            componentId: draggedComponent.id,
            reason: 'no-bounds-found',
            hasRef: !!draggedRef?.current,
            hasElement: typeof document !== 'undefined' && !!document.querySelector(`[data-component-id="${draggedComponent.id}"]`)
        });
        return { hasCollision: false, collidingComponents: [] };
    }
    
    const collidingComponents: ComponentSnapshot[] = [];
    
    for (const other of allComponents) {
        if (other.id === draggedComponent.id) continue;
        
        // Try to get other component bounds from ref first, then fall back to DOM query
        let otherBounds: DOMRect | null = null;
        const otherRef = componentRefs.get(other.id);
        
        if (otherRef?.current) {
            otherBounds = getComponentBounds(otherRef.current);
        } else if (typeof document !== 'undefined') {
            // Fallback: find element by data-component-id
            const otherElement = document.querySelector(`[data-component-id="${other.id}"]`) as HTMLElement;
            if (otherElement) {
                otherBounds = getComponentBounds(otherElement);
            }
        }
        
        if (!otherBounds) continue;
        
        if (boxesOverlap(draggedBounds, otherBounds)) {
            const snapshot = captureComponentSnapshot(other, otherRef || null);
            collidingComponents.push(snapshot);
        }
    }
    
    // Log collision check
    devLogger.debug('fieldshell.collision.checked', {
        componentId: draggedComponent.id,
        otherComponentIds: collidingComponents.map(c => c.componentId),
        hasCollision: collidingComponents.length > 0,
        bounds: {
            x: draggedBounds.x,
            y: draggedBounds.y,
            width: draggedBounds.width,
            height: draggedBounds.height
        },
        method: 'smartborder-container'
    });
    
    // Log collision detected (WARN level) with detailed snapshots
    if (collidingComponents.length > 0) {
        const draggedSnapshot = captureComponentSnapshot(draggedComponent, draggedRef ?? null);
        const overlapAreas = collidingComponents.map(colliding => {
            const collidingBounds = colliding.bounds;
            if (!collidingBounds || !draggedBounds) return 0;
            return calculateOverlapArea(
                {
                    x: draggedBounds.x,
                    y: draggedBounds.y,
                    width: draggedBounds.width,
                    height: draggedBounds.height,
                    top: draggedBounds.top,
                    right: draggedBounds.right,
                    bottom: draggedBounds.bottom,
                    left: draggedBounds.left
                } as DOMRect,
                {
                    x: collidingBounds.x,
                    y: collidingBounds.y,
                    width: collidingBounds.width,
                    height: collidingBounds.height,
                    top: collidingBounds.top,
                    right: collidingBounds.right,
                    bottom: collidingBounds.bottom,
                    left: collidingBounds.left
                } as DOMRect
            );
        });
        
        devLogger.warn('fieldshell.collision.detected', {
            draggedComponent: draggedSnapshot,
            collidingComponents,
            collisionDetails: {
                draggedBounds: {
                    x: draggedBounds.x,
                    y: draggedBounds.y,
                    width: draggedBounds.width,
                    height: draggedBounds.height,
                    top: draggedBounds.top,
                    right: draggedBounds.right,
                    bottom: draggedBounds.bottom,
                    left: draggedBounds.left
                },
                collidingBounds: collidingComponents.map(c => c.bounds).filter(Boolean),
                overlapArea: overlapAreas
            }
        });
    }
    
    return {
        hasCollision: collidingComponents.length > 0,
        collidingComponents
    };
}

// ============================================================================
// Drag/Resize Constraint Solver (canvas coordinates)
// ============================================================================

export interface CanvasRect {
    x: number;
    y: number;
    width: number;
    height: number;
}

export interface CanvasPoint {
    x: number;
    y: number;
}

export interface CanvasShape {
    /**
     * SmartBorder polygon in canvas coordinates (absolute).
     * Note: SmartBorder can be concave, so intersection is general polygon intersection (not SAT-only).
     */
    polygon: CanvasPoint[];
    source: 'smartborder-path';
}

export interface CanvasRectWithShape {
    rect: CanvasRect;
    shape?: CanvasShape;
}

export interface ConstraintConfig {
    boundaryPaddingPx: number;
    collisionPaddingPx: number;
}

export type ConstraintModeMove = 'slide';
export type ConstraintModeResize = 'autoAdjustSlide';

export interface ConstraintResult {
    accepted: boolean;
    position: { x: number; y: number };
    /** Present when the caller is proposing a resize and wants a validated position result. */
    size?: { width: number; height: number };
    reason?: 'collision' | 'boundary' | 'no-bounds' | 'no-solution';
    collidingComponentIds?: string[];
}

function rectRight(r: CanvasRect) {
    return r.x + r.width;
}
function rectBottom(r: CanvasRect) {
    return r.y + r.height;
}
function inflateRect(r: CanvasRect, pad: number): CanvasRect {
    if (!pad) return r;
    return { x: r.x - pad, y: r.y - pad, width: r.width + pad * 2, height: r.height + pad * 2 };
}
function overlapOnAxis(a0: number, a1: number, b0: number, b1: number): number {
    return Math.min(a1, b1) - Math.max(a0, b0);
}

function overlapAreaCanvas(a: CanvasRect, b: CanvasRect, epsilonPx: number = 0): number {
    const ox = overlapOnAxis(a.x, rectRight(a), b.x, rectRight(b));
    const oy = overlapOnAxis(a.y, rectBottom(a), b.y, rectBottom(b));
    if (ox <= epsilonPx || oy <= epsilonPx) return 0;
    return ox * oy;
}

function pointInPolygon(p: CanvasPoint, poly: CanvasPoint[]): boolean {
    // Ray casting algorithm (works for concave polygons)
    let inside = false;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
        const xi = poly[i].x, yi = poly[i].y;
        const xj = poly[j].x, yj = poly[j].y;
        const intersect = ((yi > p.y) !== (yj > p.y)) &&
            (p.x < (xj - xi) * (p.y - yi) / ((yj - yi) || 1e-9) + xi);
        if (intersect) inside = !inside;
    }
    return inside;
}

function segmentsIntersect(a1: CanvasPoint, a2: CanvasPoint, b1: CanvasPoint, b2: CanvasPoint): boolean {
    const orient = (p: CanvasPoint, q: CanvasPoint, r: CanvasPoint) =>
        (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
    const onSeg = (p: CanvasPoint, q: CanvasPoint, r: CanvasPoint) =>
        Math.min(p.x, r.x) <= q.x && q.x <= Math.max(p.x, r.x) &&
        Math.min(p.y, r.y) <= q.y && q.y <= Math.max(p.y, r.y);
    const o1 = orient(a1, a2, b1);
    const o2 = orient(a1, a2, b2);
    const o3 = orient(b1, b2, a1);
    const o4 = orient(b1, b2, a2);
    if ((o1 > 0 && o2 < 0 || o1 < 0 && o2 > 0) && (o3 > 0 && o4 < 0 || o3 < 0 && o4 > 0)) return true;
    if (o1 === 0 && onSeg(a1, b1, a2)) return true;
    if (o2 === 0 && onSeg(a1, b2, a2)) return true;
    if (o3 === 0 && onSeg(b1, a1, b2)) return true;
    if (o4 === 0 && onSeg(b1, a2, b2)) return true;
    return false;
}

function polygonsIntersect(polyA: CanvasPoint[], polyB: CanvasPoint[]): boolean {
    if (polyA.length < 3 || polyB.length < 3) return false;
    // Edge intersections
    for (let i = 0; i < polyA.length; i++) {
        const a1 = polyA[i];
        const a2 = polyA[(i + 1) % polyA.length];
        for (let j = 0; j < polyB.length; j++) {
            const b1 = polyB[j];
            const b2 = polyB[(j + 1) % polyB.length];
            if (segmentsIntersect(a1, a2, b1, b2)) return true;
        }
    }
    // Containment
    if (pointInPolygon(polyA[0], polyB)) return true;
    if (pointInPolygon(polyB[0], polyA)) return true;
    return false;
}

function clampAxisToCanvas(
    axis: 'x' | 'y',
    value: number,
    rect: { width: number; height: number },
    canvas: { width: number; height: number },
    boundaryPaddingPx: number
): number {
    if (axis === 'x') {
        const min = boundaryPaddingPx;
        const max = canvas.width - rect.width - boundaryPaddingPx;
        return Math.max(min, Math.min(value, max));
    }
    const min = boundaryPaddingPx;
    const max = canvas.height - rect.height - boundaryPaddingPx;
    return Math.max(min, Math.min(value, max));
}

function findMinimalSeparationAlongAxis(args: {
    axis: 'x' | 'y';
    direction: -1 | 1;
    baseRect: CanvasRect;
    canvas: { width: number; height: number };
    boundaryPaddingPx: number;
    collisionPaddingPx: number;
    others: Array<{ id: string; rect: CanvasRect; shape?: CanvasShape }>;
    ignoreIds: Set<string>;
    shapeForRect?: (pos: { x: number; y: number }) => CanvasShape | undefined;
    /**
     * Upper bound that is guaranteed to resolve AABB overlap (may be larger than needed for polygon),
     * so we binary-search inside it to find the smallest polygon-safe movement.
     */
    initialHi: number;
}): { rect: CanvasRect } | null {
    const {
        axis,
        direction,
        baseRect,
        canvas,
        boundaryPaddingPx,
        collisionPaddingPx,
        others,
        ignoreIds,
        shapeForRect,
    } = args;

    const maxDelta =
        axis === 'x'
            ? (direction < 0 ? baseRect.x - boundaryPaddingPx : (canvas.width - boundaryPaddingPx - baseRect.width) - baseRect.x)
            : (direction < 0 ? baseRect.y - boundaryPaddingPx : (canvas.height - boundaryPaddingPx - baseRect.height) - baseRect.y);

    if (maxDelta <= 0) return null;

    const isFreeAt = (delta: number) => {
        const next: CanvasRect =
            axis === 'x'
                ? {
                      ...baseRect,
                      x: clampAxisToCanvas('x', baseRect.x + direction * delta, baseRect, canvas, boundaryPaddingPx),
                  }
                : {
                      ...baseRect,
                      y: clampAxisToCanvas('y', baseRect.y + direction * delta, baseRect, canvas, boundaryPaddingPx),
                  };
        const shape = shapeForRect ? shapeForRect({ x: next.x, y: next.y }) : undefined;
        const ov = sumOverlapArea(next, others, collisionPaddingPx, ignoreIds, shape);
        return { ok: ov.total === 0, rect: next };
    };

    // Ensure we can find a "free" point within bounds; start from AABB hi (should be free) but clamp to maxDelta.
    let hi = Math.min(Math.max(args.initialHi, 0.5), maxDelta);
    let probe = isFreeAt(hi);
    // If AABB-hi doesn't resolve polygon collision (possible due to canvas clamp / multiple obstacles), expand until free or bounded.
    if (!probe.ok) {
        let tries = 0;
        while (tries < 6 && hi < maxDelta) {
            hi = Math.min(maxDelta, hi * 1.75);
            probe = isFreeAt(hi);
            if (probe.ok) break;
            tries++;
        }
        if (!probe.ok) return null;
    }

    // Binary search for smallest delta that is collision-free.
    let lo = 0;
    let best = probe.rect;
    for (let i = 0; i < 10; i++) {
        const mid = (lo + hi) / 2;
        const m = isFreeAt(mid);
        if (m.ok) {
            hi = mid;
            best = m.rect;
        } else {
            lo = mid;
        }
        if (hi - lo < 0.25) break;
    }

    return { rect: best };
}

function sumOverlapArea(
    r: CanvasRect,
    others: Array<{ id: string; rect: CanvasRect; shape?: CanvasShape }>,
    pad: number,
    ignoreIds?: Set<string>,
    shape?: CanvasShape,
    overlapEpsilonPx: number = 0
): { total: number; collidingIds: string[] } {
    const padded = inflateRect(r, pad);
    let total = 0;
    const ids: string[] = [];
    for (const o of others) {
        if (ignoreIds?.has(o.id)) continue;
        const op = inflateRect(o.rect, pad);
        // Broad-phase AABB check first
        const aabbArea = overlapAreaCanvas(padded, op, overlapEpsilonPx);
        if (aabbArea <= 0) continue;

        // Narrow-phase: if we have SmartBorder polygons for both sides, use true polygon intersection
        let intersects = true;
        if (shape?.polygon && o.shape?.polygon) {
            intersects = polygonsIntersect(shape.polygon, o.shape.polygon);
        }

        const area = intersects ? aabbArea : 0;
        if (area > 0) {
            total += area;
            ids.push(o.id);
        }
    }
    return { total, collidingIds: ids };
}

function clampToCanvas(
    pos: { x: number; y: number },
    size: { width: number; height: number },
    canvas: { width: number; height: number },
    padding: number
): { x: number; y: number; boundary: CanvasBoundaryResult } {
    const boundary = checkCanvasBoundary(
        pos.x,
        pos.y,
        size.width,
        size.height,
        canvas.width,
        canvas.height,
        padding
    );
    return { x: boundary.constrainedPosition.x, y: boundary.constrainedPosition.y, boundary };
}

/**
 * Build component rectangles in canvas coordinates using DOM measurement for size.
 * Uses component.position for x/y (authoritative) and measured SmartBorder bounds for width/height.
 */
export function buildCanvasRectsForComponents(
    components: FormComponent[],
    scale: number,
    ignoreIds?: Set<string>
): Array<{ id: string; rect: CanvasRect; component: FormComponent; shape?: CanvasShape }> {
    const out: Array<{ id: string; rect: CanvasRect; component: FormComponent; shape?: CanvasShape }> = [];
    for (const c of components) {
        if (ignoreIds?.has(c.id)) continue;
        const el = typeof document !== 'undefined'
            ? (document.querySelector(`[data-component-id="${c.id}"]`) as HTMLElement | null)
            : null;
        const dims = getComponentDimensions(c, el, scale * 100);
        let shape: CanvasShape | undefined;
        try {
            const pathEl = el?.querySelector('svg > path') as SVGPathElement | null;
            const d = pathEl?.getAttribute('d') || '';
            if (d) {
                const nums = d.match(/-?\d*\.?\d+/g)?.map(n => Number(n)) || [];
                // d is "M x y L x y ... Z" from SmartBorder; parse pairs
                const local: CanvasPoint[] = [];
                for (let i = 0; i + 1 < nums.length; i += 2) {
                    local.push({ x: nums[i], y: nums[i + 1] });
                }
                if (local.length >= 3) {
                    const baseX = c.position?.x ?? 0;
                    const baseY = c.position?.y ?? 0;
                    shape = {
                        source: 'smartborder-path',
                        polygon: local.map(p => ({ x: baseX + p.x, y: baseY + p.y })),
                    };
                }
            }
        } catch {
            shape = undefined;
        }
        out.push({
            id: c.id,
            component: c,
            rect: {
                x: c.position?.x ?? 0,
                y: c.position?.y ?? 0,
                width: dims.width,
                height: dims.height,
            },
            shape,
        });
    }
    return out;
}

/**
 * Resolve a move (drag) with canvas clamp + collision slide behavior.
 * Coordinates are in canvas space.
 */
export function resolveMoveConstraints(args: {
    componentId: string;
    currentPosition: { x: number; y: number };
    proposedPosition: { x: number; y: number };
    size: { width: number; height: number };
    canvas: { width: number; height: number };
    others: Array<{ id: string; rect: CanvasRect; shape?: CanvasShape }>;
    /** SmartBorder local polygon points (relative to component origin). If provided, enables true SmartBorder shape collision. */
    shapeLocal?: CanvasPoint[];
    /**
     * Hint for stabilizing collision resolution across frames (typically the last constrained drag position).
     * When multiple resolutions are possible, we prefer the one closer to this position to reduce "jumping".
     */
    preferredPosition?: { x: number; y: number };
    config: ConstraintConfig;
    mode: ConstraintModeMove;
    /** If currently overlapping, allow moves that reduce total overlap even if not fully resolved. */
    allowMoveOutOfExistingOverlap: boolean;
}): ConstraintResult {
    const ignore = new Set<string>([args.componentId]);
    const startRect: CanvasRect = {
        x: args.currentPosition.x,
        y: args.currentPosition.y,
        width: args.size.width,
        height: args.size.height,
    };
    const shapeForRect = (pos: { x: number; y: number }): CanvasShape | undefined => {
        if (!args.shapeLocal || args.shapeLocal.length < 3) return undefined;
        return {
            source: 'smartborder-path',
            polygon: args.shapeLocal.map(p => ({ x: pos.x + p.x, y: pos.y + p.y })),
        };
    };
    const startShape = shapeForRect({ x: startRect.x, y: startRect.y });
    const startOverlap = sumOverlapArea(startRect, args.others, args.config.collisionPaddingPx, ignore, startShape).total;

    // 1) Clamp to canvas
    const clamped = clampToCanvas(args.proposedPosition, args.size, args.canvas, args.config.boundaryPaddingPx);
    const desiredRect: CanvasRect = { ...startRect, x: clamped.x, y: clamped.y };
    let rect: CanvasRect = { ...desiredRect };
    const desiredShape = shapeForRect({ x: desiredRect.x, y: desiredRect.y });
    const targetOverlap = sumOverlapArea(desiredRect, args.others, args.config.collisionPaddingPx, ignore, desiredShape);
    const boundaryConstrained = clamped.boundary.isOutOfBounds;

    if (targetOverlap.total === 0) {
        return {
            accepted: true,
            position: { x: rect.x, y: rect.y },
            ...(boundaryConstrained ? { reason: 'boundary' as const } : {}),
        };
    }

    // If we started overlapped, allow moves that reduce overlap
    if (args.allowMoveOutOfExistingOverlap && startOverlap > 0 && targetOverlap.total < startOverlap) {
        return {
            accepted: true,
            position: { x: rect.x, y: rect.y },
            reason: 'collision',
            collidingComponentIds: targetOverlap.collidingIds,
        };
    }

    // Slide mode: iterative minimal-translation resolution (allows diagonal "around" moves when space exists)
    const maxIter = 10;
    let bestRect = { ...rect };
    let best = sumOverlapArea(rect, args.others, args.config.collisionPaddingPx, ignore, desiredShape);
    const preferred = args.preferredPosition ?? args.currentPosition;

    for (let i = 0; i < maxIter; i++) {
        const rectShape = shapeForRect({ x: rect.x, y: rect.y });
        const ov = sumOverlapArea(rect, args.others, args.config.collisionPaddingPx, ignore, rectShape);
        if (ov.total === 0) {
            return {
                accepted: true,
                position: { x: rect.x, y: rect.y },
                reason: 'collision',
                collidingComponentIds: targetOverlap.collidingIds,
            };
        }

        if (ov.total < best.total) {
            best = ov;
            bestRect = { ...rect };
        }

        const collideId = ov.collidingIds[0];
        const other = args.others.find(o => o.id === collideId);
        if (!other) break;

        const a = inflateRect(rect, args.config.collisionPaddingPx);
        const b = inflateRect(other.rect, args.config.collisionPaddingPx);
        const ox = overlapOnAxis(a.x, rectRight(a), b.x, rectRight(b));
        const oy = overlapOnAxis(a.y, rectBottom(a), b.y, rectBottom(b));
        if (ox <= 0 || oy <= 0) break;

        // Candidate translations (axis-only), but compute *minimal* polygon-safe displacement along that axis.
        const axisCandidates: Array<{ rect: CanvasRect } | null> = [
            findMinimalSeparationAlongAxis({
                axis: 'x',
                direction: -1,
                baseRect: rect,
                canvas: args.canvas,
                boundaryPaddingPx: args.config.boundaryPaddingPx,
                collisionPaddingPx: args.config.collisionPaddingPx,
                others: args.others,
                ignoreIds: ignore,
                shapeForRect,
                initialHi: ox + 1,
            }),
            findMinimalSeparationAlongAxis({
                axis: 'x',
                direction: 1,
                baseRect: rect,
                canvas: args.canvas,
                boundaryPaddingPx: args.config.boundaryPaddingPx,
                collisionPaddingPx: args.config.collisionPaddingPx,
                others: args.others,
                ignoreIds: ignore,
                shapeForRect,
                initialHi: ox + 1,
            }),
            findMinimalSeparationAlongAxis({
                axis: 'y',
                direction: -1,
                baseRect: rect,
                canvas: args.canvas,
                boundaryPaddingPx: args.config.boundaryPaddingPx,
                collisionPaddingPx: args.config.collisionPaddingPx,
                others: args.others,
                ignoreIds: ignore,
                shapeForRect,
                initialHi: oy + 1,
            }),
            findMinimalSeparationAlongAxis({
                axis: 'y',
                direction: 1,
                baseRect: rect,
                canvas: args.canvas,
                boundaryPaddingPx: args.config.boundaryPaddingPx,
                collisionPaddingPx: args.config.collisionPaddingPx,
                others: args.others,
                ignoreIds: ignore,
                shapeForRect,
                initialHi: oy + 1,
            }),
        ];

        const candidates = axisCandidates
            .filter((c): c is { rect: CanvasRect } => !!c)
            .map(({ rect: rr }) => {
                const rrShape = shapeForRect({ x: rr.x, y: rr.y });
                const overlap = sumOverlapArea(rr, args.others, args.config.collisionPaddingPx, ignore, rrShape);
                const distFromDesired = Math.abs(rr.x - desiredRect.x) + Math.abs(rr.y - desiredRect.y);
                const distFromPreferred = Math.abs(rr.x - preferred.x) + Math.abs(rr.y - preferred.y);
                return { rr, overlap, distFromDesired, distFromPreferred };
            });

        candidates.sort(
            (p, q) =>
                (p.overlap.total - q.overlap.total) ||
                // First: stay close to user's intended point (cursor)
                (p.distFromDesired - q.distFromDesired) ||
                // Then: stabilize against frame-to-frame flips ("jumping")
                (p.distFromPreferred - q.distFromPreferred)
        );
        if (candidates.length === 0) break;
        rect = candidates[0].rr;
    }

    // If we started overlapped, allow best reduction
    if (args.allowMoveOutOfExistingOverlap && startOverlap > 0 && best.total < startOverlap) {
        return {
            accepted: true,
            position: { x: bestRect.x, y: bestRect.y },
            reason: 'collision',
            collidingComponentIds: best.collidingIds,
        };
    }

    // Otherwise: keep current position (hard stop)
    return {
        accepted: true,
        position: { x: startRect.x, y: startRect.y },
        reason: boundaryConstrained ? 'boundary' : 'collision',
        collidingComponentIds: targetOverlap.collidingIds,
    };
}

/**
 * Resolve a resize/panel change by keeping requested size and auto-adjusting position (slide) to avoid overlap.
 * If impossible within iteration limit, reject.
 */
export function resolveResizeConstraints(args: {
    componentId: string;
    currentPosition: { x: number; y: number };
    proposedPosition: { x: number; y: number };
    proposedSize: { width: number; height: number };
    canvas: { width: number; height: number };
    others: Array<{ id: string; rect: CanvasRect; shape?: CanvasShape }>;
    config: ConstraintConfig;
    mode: ConstraintModeResize;
    allowMoveOutOfExistingOverlap: boolean;
    maxIterations?: number;
    overlapEpsilonPx?: number;
}): ConstraintResult {
    const ignore = new Set<string>([args.componentId]);
    const maxIter = args.maxIterations ?? 12;
    const overlapEpsilonPx = args.overlapEpsilonPx ?? 0;

    const startRect: CanvasRect = {
        x: args.currentPosition.x,
        y: args.currentPosition.y,
        width: args.proposedSize.width,
        height: args.proposedSize.height,
    };
    const startOverlap = sumOverlapArea(startRect, args.others, args.config.collisionPaddingPx, ignore, undefined, overlapEpsilonPx).total;

    // Start from proposed position, clamped to canvas.
    const clamped = clampToCanvas(args.proposedPosition, args.proposedSize, args.canvas, args.config.boundaryPaddingPx);
    let rect: CanvasRect = {
        x: clamped.x,
        y: clamped.y,
        width: args.proposedSize.width,
        height: args.proposedSize.height,
    };

    let bestRect = { ...rect };
    let bestOverlap = sumOverlapArea(rect, args.others, args.config.collisionPaddingPx, ignore, undefined, overlapEpsilonPx);

    if (bestOverlap.total === 0) {
        return { accepted: true, position: { x: rect.x, y: rect.y }, size: args.proposedSize };
    }

    for (let i = 0; i < maxIter; i++) {
        const overlap = sumOverlapArea(rect, args.others, args.config.collisionPaddingPx, ignore, undefined, overlapEpsilonPx);
        if (overlap.total === 0) {
            return { accepted: true, position: { x: rect.x, y: rect.y }, size: args.proposedSize };
        }

        // Track best reduction (for existing overlap escape)
        if (overlap.total < bestOverlap.total) {
            bestOverlap = overlap;
            bestRect = { ...rect };
        }

        // Pick first colliding rect to resolve against.
        const collideId = overlap.collidingIds[0];
        const other = args.others.find(o => o.id === collideId);
        if (!other) break;

        const a = inflateRect(rect, args.config.collisionPaddingPx);
        const b = inflateRect(other.rect, args.config.collisionPaddingPx);
        const ox = overlapOnAxis(a.x, rectRight(a), b.x, rectRight(b));
        const oy = overlapOnAxis(a.y, rectBottom(a), b.y, rectBottom(b));
        if (ox <= 0 || oy <= 0) break;

        // Candidate translations: push out along each axis (both directions), choose minimal displacement.
        const pushLeft = { x: rect.x - ox, y: rect.y };
        const pushRight = { x: rect.x + ox, y: rect.y };
        const pushUp = { x: rect.x, y: rect.y - oy };
        const pushDown = { x: rect.x, y: rect.y + oy };
        const candidates = [pushLeft, pushRight, pushUp, pushDown].map(pos => {
            const c = clampToCanvas(pos, args.proposedSize, args.canvas, args.config.boundaryPaddingPx);
            const rr: CanvasRect = { x: c.x, y: c.y, width: rect.width, height: rect.height };
            const ov = sumOverlapArea(rr, args.others, args.config.collisionPaddingPx, ignore, undefined, overlapEpsilonPx);
            const dist = Math.abs(c.x - rect.x) + Math.abs(c.y - rect.y);
            return { rr, ov, dist };
        });
        candidates.sort((p, q) => (p.ov.total - q.ov.total) || (p.dist - q.dist));
        rect = candidates[0].rr;
    }

    // Accept if we can reduce existing overlap (escape), otherwise reject.
    if (args.allowMoveOutOfExistingOverlap && startOverlap > 0 && bestOverlap.total < startOverlap) {
        return {
            accepted: true,
            position: { x: bestRect.x, y: bestRect.y },
            size: args.proposedSize,
            reason: 'collision',
            collidingComponentIds: bestOverlap.collidingIds,
        };
    }

    return {
        accepted: false,
        position: { x: args.currentPosition.x, y: args.currentPosition.y },
        size: args.proposedSize,
        reason: bestOverlap.total > 0 ? 'no-solution' : 'collision',
        collidingComponentIds: bestOverlap.collidingIds,
    };
}
