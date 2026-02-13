/**
 * useBackgroundImageUrl - Story 5.1 Task T05
 *
 * Shared hook for resolving and displaying background images.
 * Used by builder preview (FormBuilderCanvas) and public renderer (PublicFormArtboard)
 * to ensure identical resolution logic and display parity.
 */

import { useState, useEffect } from 'react';
import type { BackgroundDefinition } from '../types/builder.types';
import { resolveAssetContentUrl } from '../utils/backgroundAssetResolver';
import { assetsApi } from '../api/assetsApi';

export interface UseBackgroundImageUrlResult {
  /** Displayable URL (blob for assets when auth available, or content/external URL) */
  url: string | null;
  isLoading: boolean;
}

/**
 * Resolve background to displayable image URL.
 * - Asset ref: fetches via API with auth, returns blob URL when possible.
 * - External URL: returns as-is.
 * - Fallback: content URL for assets when blob fetch fails (e.g. anonymous).
 */
export function useBackgroundImageUrl(
  background: BackgroundDefinition | undefined
): UseBackgroundImageUrlResult {
  const assetId =
    background?.type === 'image' && background?.asset
      ? background.asset.assetId
      : null;
  const externalUrl =
    background?.type === 'image' &&
    background?.value &&
    !background.value.startsWith('data:')
      ? background.value
      : null;

  const [url, setUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(!!assetId);

  useEffect(() => {
    if (assetId != null) {
      let revoked = false;
      const ref = { current: null as string | null };
      setIsLoading(true);
      assetsApi
        .fetchAssetContentBlobUrl(assetId)
        .then((blobUrl) => {
          if (!revoked) {
            ref.current = blobUrl;
            setUrl(blobUrl);
          } else {
            URL.revokeObjectURL(blobUrl);
          }
        })
        .catch(() => {
          if (!revoked) {
            setUrl(resolveAssetContentUrl(assetId));
          }
        })
        .finally(() => {
          if (!revoked) setIsLoading(false);
        });
      return () => {
        revoked = true;
        if (ref.current) {
          URL.revokeObjectURL(ref.current);
          ref.current = null;
        }
        setUrl(null);
      };
    }
    if (externalUrl) {
      setUrl(externalUrl);
      setIsLoading(false);
      return () => setUrl(null);
    }
    setUrl(null);
    setIsLoading(false);
    return undefined;
  }, [assetId, externalUrl]);

  return { url, isLoading };
}
