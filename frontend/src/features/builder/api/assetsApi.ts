/**
 * Assets API Client - Story 5.1 Task T04
 * 
 * API client for background asset upload and management at /api/assets.
 * Uses the shared apiClient with authentication.
 */

import { apiClient } from '../../../lib/apiClient';
import { BackgroundAssetMetadata } from '../types/builder.types';

const ASSETS_BASE = '/api/assets';

// ═══════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════

export interface BackgroundAssetUploadResponse {
    asset: BackgroundAssetMetadata;
    isDuplicate: boolean;
}

export interface AssetResolveResponse {
    url: string;
}

export interface BackgroundAssetListResponse {
    assets: BackgroundAssetMetadata[];
}

// ═══════════════════════════════════════════════════════════════════════════
// TRANSFORMERS: Backend to Frontend
// ═══════════════════════════════════════════════════════════════════════════

function transformAssetMetadata(data: any): BackgroundAssetMetadata {
    return {
        assetId: data.assetId ?? data.asset_id ?? 0,
        assetKey: data.assetKey ?? data.asset_key ?? '',
        displayName: data.displayName ?? data.display_name ?? undefined,
        originalFilename: data.originalFilename ?? data.original_filename ?? '',
        mimeType: data.mimeType ?? data.mime_type ?? '',
        byteSize: data.byteSize ?? data.byte_size ?? 0,
        widthPx: data.widthPx ?? data.width_px ?? undefined,
        heightPx: data.heightPx ?? data.height_px ?? undefined,
        checksumSha256: data.checksumSha256 ?? data.checksum_sha256 ?? undefined,
        createdAt: data.createdAt ?? data.created_at ? new Date(data.createdAt ?? data.created_at).toISOString() : undefined,
        updatedAt: data.updatedAt ?? data.updated_at ? new Date(data.updatedAt ?? data.updated_at).toISOString() : undefined,
    };
}

function transformUploadResponse(data: any): BackgroundAssetUploadResponse {
    return {
        asset: transformAssetMetadata(data.asset),
        isDuplicate: data.isDuplicate ?? data.is_duplicate ?? false,
    };
}

// ═══════════════════════════════════════════════════════════════════════════
// API CLIENT
// ═══════════════════════════════════════════════════════════════════════════

export const assetsApi = {
    /**
     * List all background assets for the current user's company (shared library).
     * GET /api/assets/backgrounds
     */
    listBackgrounds: async (): Promise<BackgroundAssetMetadata[]> => {
        const response = await apiClient.get<{ assets: unknown[] }>(
            `${ASSETS_BASE}/backgrounds`
        );
        const assets = response.data?.assets ?? [];
        return Array.isArray(assets) ? assets.map(transformAssetMetadata) : [];
    },

    /**
     * Upload a background image asset
     * POST /api/assets/backgrounds/upload
     */
    uploadBackground: async (
        file: File,
        displayName?: string
    ): Promise<BackgroundAssetUploadResponse> => {
        const formData = new FormData();
        formData.append('file', file);
        if (displayName) {
            formData.append('display_name', displayName);
        }

        const response = await apiClient.post(
            `${ASSETS_BASE}/backgrounds/upload`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        );
        return transformUploadResponse(response.data);
    },

    /**
     * Resolve asset URL for runtime access
     * GET /api/assets/{asset_id}/resolve
     */
    resolveAssetUrl: async (assetId: number): Promise<string> => {
        const response = await apiClient.get<AssetResolveResponse>(
            `${ASSETS_BASE}/${assetId}/resolve`
        );
        return response.data.url;
    },

    /**
     * Get asset content URL (for direct image src).
     * Only works when the request can send auth (e.g. same-origin with cookies).
     * For authenticated endpoints prefer fetchAssetContentBlobUrl so the axios client sends the token.
     */
    getAssetContentUrl: (assetId: number): string => {
        return `${ASSETS_BASE}/${assetId}/content`;
    },

    /**
     * Fetch asset content with auth and return a blob URL suitable for <img src={...}>.
     * Caller must call URL.revokeObjectURL(url) when done to avoid leaks.
     */
    fetchAssetContentBlobUrl: async (assetId: number): Promise<string> => {
        const response = await apiClient.get(`${ASSETS_BASE}/${assetId}/content`, {
            responseType: 'blob',
        });
        const blob = response.data as Blob;
        return URL.createObjectURL(blob);
    },
};

export default assetsApi;
