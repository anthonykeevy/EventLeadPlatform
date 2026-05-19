/**
 * Shared Background Asset Resolver - Story 5.1 Task T05
 *
 * Centralized resolver for background asset references.
 * Builder preview and public renderer use the same rules and URL generation
 * to ensure parity. Runtime URL format matches backend contract.
 */

import type { BackgroundDefinition } from '../types/builder.types';
import { getApiBaseUrl } from '../../../lib/apiBaseUrl';

/**
 * Resolve asset ID to content URL per backend contract.
 * Format: {base}/api/assets/{asset_id}/content
 */
export function resolveAssetContentUrl(assetId: number): string {
  const base = getApiBaseUrl().replace(/\/$/, '');
  return `${base}/api/assets/${assetId}/content`;
}

/**
 * Get relative content path for an asset (works with Vite proxy / same-origin).
 * Use when img src can use relative path.
 */
export function getAssetContentPath(assetId: number): string {
  return `/api/assets/${assetId}/content`;
}

/**
 * Returns the image display source for a background definition.
 * - For asset refs: returns content URL (resolver output).
 * - For external URLs: returns value if not a data URL.
 * - For color or invalid: returns null.
 */
export function getBackgroundImageSource(
  background: BackgroundDefinition | undefined
): string | null {
  if (!background || background.type !== 'image') return null;
  if (background.asset?.assetId != null) {
    return resolveAssetContentUrl(background.asset.assetId);
  }
  const v = background.value?.trim();
  if (!v || v.startsWith('data:')) return null;
  return v;
}
