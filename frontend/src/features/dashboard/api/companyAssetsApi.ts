/**
 * Company Assets API - Story 5.7
 * Company Settings → Assets → Images (etc.)
 */

import { apiClient } from '../../../lib/apiClient'
import type { BackgroundAssetMetadata } from '../../builder/types/builder.types'

function transformAsset(data: Record<string, unknown>): BackgroundAssetMetadata {
  return {
    assetId: (data.assetId ?? data.asset_id) as number,
    assetKey: (data.assetKey ?? data.asset_key ?? `asset:${data.assetId ?? data.asset_id}`) as string,
    displayName: (data.displayName ?? data.display_name) as string | undefined,
    originalFilename: (data.originalFilename ?? data.original_filename ?? '') as string,
    mimeType: (data.mimeType ?? data.mime_type ?? '') as string,
    byteSize: (data.byteSize ?? data.byte_size ?? 0) as number,
    widthPx: (data.widthPx ?? data.width_px) as number | undefined,
    heightPx: (data.heightPx ?? data.height_px) as number | undefined,
    checksumSha256: (data.checksumSha256 ?? data.checksum_sha256) as string | undefined,
    createdAt: data.createdAt ?? data.created_at ? new Date((data.createdAt ?? data.created_at) as string).toISOString() : undefined,
    updatedAt: data.updatedAt ?? data.updated_at ? new Date((data.updatedAt ?? data.updated_at) as string).toISOString() : undefined,
  }
}

export async function getCompanyImageAssets(companyId: number): Promise<BackgroundAssetMetadata[]> {
  const response = await apiClient.get<{ assets: unknown[] }>(`/api/companies/${companyId}/assets`)
  const assets = response.data?.assets ?? []
  return Array.isArray(assets) ? assets.map((a) => transformAsset(a as Record<string, unknown>)) : []
}

export async function updateAssetDisplayName(
  assetId: number,
  displayName: string
): Promise<BackgroundAssetMetadata> {
  const response = await apiClient.patch<Record<string, unknown>>(`/api/assets/${assetId}`, {
    display_name: displayName || null
  })
  return transformAsset(response.data)
}

export async function deleteAsset(assetId: number): Promise<void> {
  await apiClient.delete(`/api/assets/${assetId}`)
}

/**
 * Fetch asset image content with auth (Bearer token) and return blob URL for <img src>.
 * Must revoke the blob URL when done to avoid memory leaks.
 * Use this instead of raw /api/assets/{id}/content — img tags don't send auth headers.
 * @param preferThumbnail - when true, fetches 300x300 thumbnail when available (grid, picker)
 */
export async function fetchAssetContentBlobUrl(
  assetId: number,
  preferThumbnail = false
): Promise<string> {
  const url = preferThumbnail
    ? `/api/assets/${assetId}/content?size=thumb`
    : `/api/assets/${assetId}/content`
  const response = await apiClient.get(url, { responseType: 'blob' })
  const blob = response.data as Blob
  return URL.createObjectURL(blob)
}

export async function uploadAssetImage(
  file: File,
  displayName?: string
): Promise<BackgroundAssetMetadata> {
  const formData = new FormData()
  formData.append('file', file)
  if (displayName) {
    formData.append('display_name', displayName)
  }
  // Do NOT set Content-Type: let the client set multipart/form-data with boundary
  const response = await apiClient.post<{ asset: Record<string, unknown>; isDuplicate?: boolean }>(
    '/api/assets/backgrounds/upload',
    formData
  )
  return transformAsset(response.data?.asset ?? response.data)
}

// -------------------------------------------------------------------------
// Terms Assets (Story 5.7)
// -------------------------------------------------------------------------

export interface TermsAssetMetadata {
  assetId: number
  assetKey: string
  displayName?: string
  sourceType: 'upload' | 'url'
  sourceUrl?: string
  mimeType: string
  byteSize: number
  embeddable?: boolean
  termsDisplayMode?: 'popup' | 'new_tab'
  displayWidthPx?: number
  displayHeightPx?: number
  displayRotationDegrees?: number
  createdAt?: string
  updatedAt?: string
}


export interface TermsUrlValidateResult {
  embeddable: boolean
  reason?: string
  blocker_type?: 'embedding' | 'reachability' | 'content' | 'unknown'
  next_action?: string
}

export interface TermsAssetsResponse {
  assets: TermsAssetMetadata[]
  defaultTermsAssetId?: number | null
}

export async function getCompanyTermsAssets(companyId: number): Promise<TermsAssetsResponse> {
  const response = await apiClient.get<TermsAssetsResponse>(
    `/api/companies/${companyId}/terms-assets`
  )
  return {
    assets: response.data?.assets ?? [],
    defaultTermsAssetId: response.data?.defaultTermsAssetId ?? null,
  }
}

export async function setDefaultTermsAsset(
  companyId: number,
  assetId: number
): Promise<void> {
  await apiClient.put(`/api/companies/${companyId}/terms-assets/default`, { assetId })
}

export async function uploadTermsPdf(
  file: File,
  displayName?: string
): Promise<TermsAssetMetadata> {
  const formData = new FormData()
  formData.append('file', file)
  if (displayName) formData.append('display_name', displayName)
  // Do NOT set Content-Type: let the client set multipart/form-data with boundary
  const response = await apiClient.post<{ asset: TermsAssetMetadata }>(
    '/api/assets/terms/upload',
    formData
  )
  return response.data!.asset
}

export async function addTermsUrl(
  url: string,
  displayName?: string,
  displayMode: 'popup' | 'new_tab' = 'popup'
): Promise<TermsAssetMetadata> {
  const response = await apiClient.post<TermsAssetMetadata>('/api/assets/terms/url', {
    url,
    display_name: displayName || null,
    display_mode: displayMode,
  })
  return response.data!
}

export async function validateTermsUrl(url: string): Promise<TermsUrlValidateResult> {
  const response = await apiClient.post<TermsUrlValidateResult>(
    '/api/assets/terms/validate-url',
    { url }
  )
  return response.data!
}

export async function updateTermsDisplaySettings(
  assetId: number,
  settings: { display_width_px?: number; display_height_px?: number; display_rotation_degrees?: number }
): Promise<void> {
  await apiClient.patch(`/api/assets/${assetId}`, settings)
}
