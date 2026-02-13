/**
 * Background placement utilities - Story 5.1 Task T06
 * Intersection rules, off-canvas detection, default placement.
 */
import type { BackgroundPlacement } from '../types/builder.types';

/** Rect A [ax, ay, aw, ah] does not intersect Rect B [0, 0, bw, bh] */
export function isBackgroundFullyOffCanvas(
  placement: BackgroundPlacement,
  canvasWidth: number,
  canvasHeight: number
): boolean {
  const { position, size } = placement;
  const right = position.x + size.width;
  const bottom = position.y + size.height;
  return (
    right <= 0 ||
    position.x >= canvasWidth ||
    bottom <= 0 ||
    position.y >= canvasHeight
  );
}

/** Default placement covering the full canvas */
export function createDefaultPlacement(
  canvasWidth: number,
  canvasHeight: number
): BackgroundPlacement {
  return {
    position: { x: 0, y: 0 },
    size: { width: canvasWidth, height: canvasHeight },
  };
}

/** True if placement matches default canvas coverage (user has not moved/resized). */
export function isDefaultPlacement(
  placement: BackgroundPlacement,
  canvasWidth: number,
  canvasHeight: number
): boolean {
  const { position, size } = placement;
  return (
    Math.abs(position.x) < 1 &&
    Math.abs(position.y) < 1 &&
    Math.abs(size.width - canvasWidth) < 1 &&
    Math.abs(size.height - canvasHeight) < 1
  );
}
