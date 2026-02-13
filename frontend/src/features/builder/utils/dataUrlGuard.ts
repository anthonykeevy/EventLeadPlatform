/**
 * Data URL Guard - Story 5.1 Task T07
 *
 * Prevents Data URL backgrounds from entering builder definitions and strips
 * any legacy Data URLs on load. Data URLs (data:image/...;base64,...) bloat
 * definitions and are not supported for persistence.
 */

import type { BackgroundDefinition } from '../types/builder.types';

/** User-facing error message when Data URL is rejected */
export const DATA_URL_ERROR_MESSAGE =
  'Data URLs (base64 images) are not supported. Please use an external URL or upload an image from the library.';

/**
 * Returns true if the value looks like a Data URL.
 */
export function isDataUrl(value: string | undefined): boolean {
  return !!value && value.trim().toLowerCase().startsWith('data:');
}

/**
 * Strips Data URL from a background definition.
 * If value is a Data URL and there is no asset reference, returns undefined (remove background).
 * If value is a Data URL but asset exists, clears value and keeps asset.
 */
export function stripDataUrlFromBackground(
  background?: BackgroundDefinition
): BackgroundDefinition | undefined {
  if (!background) return undefined;

  if (background.value && isDataUrl(background.value)) {
    if (background.asset) {
      return {
        ...background,
        value: '',
      };
    }
    return undefined;
  }

  return background;
}
