import { apiClient } from '../../../lib/apiClient'

export interface FormVersionDto {
  formVersionId: number
  formId: number
  versionNumber: number
  status: 'DRAFT' | 'PUBLISHED' | 'ARCHIVED' | string
  isActive: boolean
  createdDate: string
  createdBy?: number | null
  publishedDate?: string | null
  publishedBy?: number | null
  definition: Record<string, unknown>
  versionComment?: string | null
}

export interface FormVersionListResponse {
  versions: FormVersionDto[]
}

function getDetailMessage(err: any): string {
  const detail = err?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (detail?.message && Array.isArray(detail?.errors)) {
    return `${detail.message}: ${detail.errors.join(' | ')}`
  }
  return err?.message || 'An unexpected error occurred.'
}

export async function listFormVersions(formId: string | number): Promise<FormVersionDto[]> {
  const res = await apiClient.get<FormVersionListResponse>(`/api/forms/${formId}/versions`)
  return res.data?.versions ?? []
}

export async function createDraftVersion(
  formId: string | number,
  definition: Record<string, unknown>,
  versionComment?: string,
): Promise<FormVersionDto> {
  const res = await apiClient.post<FormVersionDto>(`/api/forms/${formId}/versions`, {
    definition,
    versionComment,
  })
  return res.data
}

export async function updateDraftVersion(
  formId: string | number,
  versionNumber: number,
  definition: Record<string, unknown>,
  versionComment?: string,
): Promise<FormVersionDto> {
  const res = await apiClient.put<FormVersionDto>(`/api/forms/${formId}/versions/${versionNumber}`, {
    definition,
    versionComment,
  })
  return res.data
}

export function formatFormVersionError(err: unknown): string {
  return getDetailMessage(err as any)
}
