/**
 * Scale Utilities - Component Scaling with Anchor Points
 * 
 * Provides unified scaling logic for corner handles and Properties Panel slider.
 * Supports anchoring at any corner (NW, NE, SE, SW) to maintain position of the opposite corner.
 * 
 * ANCHOR POINT LOGIC:
 * - SE anchor (NW handle): component grows/shrinks toward NW, SE stays fixed
 * - SW anchor (NE handle): component grows/shrinks toward NE, SW stays fixed  
 * - NE anchor (SW handle): component grows/shrinks toward SW, NE stays fixed
 * - NW anchor (SE handle): component grows/shrinks toward SE, NW stays fixed (default for slider)
 */

import { devLogger } from './devLogger';

/** Valid anchor points for scaling operations */
export type ScaleAnchor = 'nw' | 'ne' | 'se' | 'sw';

/** Component dimensions needed for scale calculations */
export interface ComponentDimensions {
    /** Current width in pixels (at 100% scale) */
    baseWidthPx: number;
    /** Current height in pixels (at 100% scale, or measured from DOM) */
    baseHeightPx: number;
    /** Current component scale (50-200) */
    currentScale: number;
}

/** Position of the component on canvas */
export interface ComponentPosition {
    x: number;
    y: number;
}

/** Result of scale calculation */
export interface ScaleChangeResult {
    /** New scale value (clamped to 50-200) */
    newScale: number;
    /** Horizontal position shift needed to maintain anchor (negative = move left) */
    leftShift: number;
    /** Vertical position shift needed to maintain anchor (negative = move up) */
    topShift: number;
    /** New position after applying shifts */
    newPosition: ComponentPosition;
    /** Whether the scale was clamped to min/max bounds */
    wasClamped: boolean;
}

/** Options for scale calculation */
export interface ScaleCalculationOptions {
    /** Current component dimensions */
    dimensions: ComponentDimensions;
    /** Current component position */
    position: ComponentPosition;
    /** Target scale value (will be clamped to 50-200) */
    targetScale: number;
    /** Which corner to anchor (opposite corner moves) */
    anchor: ScaleAnchor;
    /** Canvas scale factor (for converting between coordinate systems) */
    canvasScale?: number;
    /** Whether to log debug info */
    debug?: boolean;
}

/** Minimum allowed scale (50%) */
export const MIN_SCALE = 50;
/** Maximum allowed scale (200%) */
export const MAX_SCALE = 200;

/**
 * Calculate scale change with position shift to maintain anchor point.
 * 
 * This is the core scaling function used by both corner handles and Properties Panel.
 * 
 * @param options - Scale calculation options
 * @returns ScaleChangeResult with new scale, shifts, and new position
 * 
 * @example
 * // Properties Panel slider (always anchors NW)
 * const result = calculateScaleChange({
 *     dimensions: { baseWidthPx: 400, baseHeightPx: 50, currentScale: 100 },
 *     position: { x: 100, y: 200 },
 *     targetScale: 120,
 *     anchor: 'nw', // NW stays fixed, component grows toward SE
 * });
 * 
 * @example
 * // Corner handle NW (anchors SE)
 * const result = calculateScaleChange({
 *     dimensions: { baseWidthPx: 400, baseHeightPx: 50, currentScale: 100 },
 *     position: { x: 100, y: 200 },
 *     targetScale: 120,
 *     anchor: 'se', // SE stays fixed, component grows toward NW
 * });
 */
export function calculateScaleChange(options: ScaleCalculationOptions): ScaleChangeResult {
    const { dimensions, position, targetScale, anchor, canvasScale: _canvasScale = 1, debug = false } = options;
    const { baseWidthPx, baseHeightPx, currentScale } = dimensions;
    
    // Clamp target scale to valid range
    const clampedScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, Math.round(targetScale)));
    const wasClamped = clampedScale !== Math.round(targetScale);
    
    // Calculate scale ratio
    const scaleRatio = clampedScale / currentScale;
    
    // Calculate dimension changes
    // Width: baseWidthPx is at 100% scale, so multiply by scale/100 to get displayed size
    const displayedWidthBefore = baseWidthPx * (currentScale / 100);
    const displayedWidthAfter = baseWidthPx * (clampedScale / 100);
    const widthChange = displayedWidthAfter - displayedWidthBefore;
    
    // Height: baseHeightPx is the CURRENT displayed height (from DOM), so use ratio for scaling
    // This matches how SortableComponent calculates it from bounds.height
    const displayedHeightBefore = baseHeightPx; // Already at current displayed size
    const displayedHeightAfter = baseHeightPx * scaleRatio;
    const heightChange = displayedHeightAfter - displayedHeightBefore;
    
    // Determine which shifts are needed based on anchor point
    // NW anchor: no shifts needed (component grows toward SE - default behavior)
    // NE anchor: need leftShift (component grows toward SW)
    // SE anchor: need leftShift AND topShift (component grows toward NW)
    // SW anchor: need topShift (component grows toward NE)
    const needsLeftShift = anchor === 'ne' || anchor === 'se';
    const needsTopShift = anchor === 'se' || anchor === 'sw';
    
    // Calculate position shifts
    // Negative shift moves component left/up to compensate for growth
    const leftShift = needsLeftShift ? -widthChange : 0;
    const topShift = needsTopShift ? -heightChange : 0;
    
    // Calculate new position
    const newPosition: ComponentPosition = {
        x: position.x + leftShift,
        y: position.y + topShift,
    };
    
    const result: ScaleChangeResult = {
        newScale: clampedScale,
        leftShift,
        topShift,
        newPosition,
        wasClamped,
    };
    
    if (debug) {
        devLogger.debug('scale.calculate', {
            input: { currentScale, targetScale, anchor },
            dimensions: { widthBefore: displayedWidthBefore, widthAfter: displayedWidthAfter, widthChange },
            heightCalc: { heightBefore: displayedHeightBefore, heightAfter: displayedHeightAfter, heightChange },
            shifts: { needsLeftShift, needsTopShift, leftShift, topShift },
            result,
        });
    }
    
    return result;
}

/**
 * Convert corner handle to anchor point.
 * The anchor is the OPPOSITE corner from the handle being dragged.
 * 
 * @param handle - The corner handle being dragged
 * @returns The anchor point (opposite corner)
 */
export function handleToAnchor(handle: 'nw' | 'ne' | 'se' | 'sw'): ScaleAnchor {
    const anchorMap: Record<string, ScaleAnchor> = {
        'nw': 'se', // NW handle → SE anchor
        'ne': 'sw', // NE handle → SW anchor
        'se': 'nw', // SE handle → NW anchor
        'sw': 'ne', // SW handle → NE anchor
    };
    return anchorMap[handle];
}

/**
 * Calculate scale from mouse delta (for corner handles).
 * 
 * @param deltaWidth - Mouse delta X (adjusted for scale)
 * @param currentWidthPx - Current component width in pixels
 * @param currentScale - Current component scale (50-200)
 * @returns Target scale value (not yet clamped)
 */
export function calculateScaleFromDelta(
    deltaWidth: number,
    currentWidthPx: number,
    currentScale: number
): number {
    const startWidth = currentWidthPx;
    const newWidth = startWidth + deltaWidth;
    const scaleRatio = newWidth / startWidth;
    return scaleRatio * currentScale;
}

/**
 * Apply scale change to component (for Properties Panel with anchor support).
 * 
 * This function provides a unified way to apply scale changes from the Properties Panel
 * with support for different anchor points (currently always NW for slider).
 * 
 * @param currentPosition - Current component position
 * @param currentScale - Current component scale
 * @param newScale - Target scale value
 * @param componentElement - DOM element for measuring dimensions
 * @param anchor - Anchor point (default 'nw' for Properties Panel)
 * @returns Object with new scale and position updates
 */
export function prepareScaleUpdate(
    currentPosition: ComponentPosition,
    currentScale: number,
    newScale: number,
    componentElement: HTMLElement | null,
    anchor: ScaleAnchor = 'nw'
): { scale: number; position?: ComponentPosition } {
    // Get current dimensions from DOM
    const rect = componentElement?.getBoundingClientRect();
    if (!rect) {
        // No DOM element, just return scale change with NW anchor (no position change)
        return { scale: Math.max(MIN_SCALE, Math.min(MAX_SCALE, newScale)) };
    }
    
    // Calculate base dimensions (at 100% scale)
    const baseWidthPx = (rect.width / currentScale) * 100;
    const baseHeightPx = (rect.height / currentScale) * 100;
    
    const result = calculateScaleChange({
        dimensions: { baseWidthPx, baseHeightPx, currentScale },
        position: currentPosition,
        targetScale: newScale,
        anchor,
    });
    
    // Only return position if it changed
    if (result.leftShift !== 0 || result.topShift !== 0) {
        return { scale: result.newScale, position: result.newPosition };
    }
    
    return { scale: result.newScale };
}
