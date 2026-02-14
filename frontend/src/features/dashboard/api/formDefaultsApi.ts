/**
 * Form Defaults API - Story 5.2 T04
 * Company form branding defaults (merged Global + Company)
 */

import { apiClient } from '../../../lib/apiClient'

export interface FormDefaultsPayload {
  theme?: {
    primaryColor?: string
    backgroundColor?: string
    fontFamily?: string
  }
  globalStyles?: Record<string, unknown>
  canvasSettings?: {
    width?: number
    height?: number
    gridSize?: number
  }
  defaultGridLayoutsByComponent?: Record<string, unknown>
  [key: string]: unknown
}

export interface FormDefaultsResponse {
  defaults: FormDefaultsPayload
  versionNumber?: number
}

export interface FormDefaultsVersionEntry {
  versionNumber: number
  defaults: FormDefaultsPayload
  changeSummary?: string | null
  createdDate: string
  createdBy?: number | null
}

export interface FormDefaultsHistoryResponse {
  items: FormDefaultsVersionEntry[]
  total: number
}

/**
 * GET /api/companies/{id}/form-defaults
 * Merged defaults (Global + Company)
 */
export async function getCompanyFormDefaults(companyId: number): Promise<FormDefaultsResponse> {
  const response = await apiClient.get<FormDefaultsResponse>(
    `/api/companies/${companyId}/form-defaults`
  )
  return response.data
}

/**
 * PUT /api/companies/{id}/form-defaults
 * Update company defaults (Company Admin only)
 */
export async function putCompanyFormDefaults(
  companyId: number,
  defaults: FormDefaultsPayload,
  changeSummary?: string
): Promise<FormDefaultsResponse> {
  const response = await apiClient.put<FormDefaultsResponse>(
    `/api/companies/${companyId}/form-defaults`,
    { defaults, changeSummary: changeSummary ?? null }
  )
  return response.data
}

/**
 * GET /api/companies/{id}/form-defaults/history
 * Version history / audit trail (Company Admin only)
 */
export async function getCompanyFormDefaultsHistory(
  companyId: number,
  limit = 50
): Promise<FormDefaultsHistoryResponse> {
  const response = await apiClient.get<FormDefaultsHistoryResponse>(
    `/api/companies/${companyId}/form-defaults/history`,
    { params: { limit } }
  )
  return response.data
}
