/**
 * Form Defaults API — Story 5.2 T05
 * Company form branding defaults (used for Save to Company Defaults)
 * @see docs/stories/STORY-5.2-DATA-SCHEMA.md
 */

import { apiClient } from '../../../lib/apiClient';

export interface FormDefaultsPayload {
  theme?: {
    primaryColor?: string;
    backgroundColor?: string;
    fontFamily?: string;
  } | null;
  globalStyles?: Record<string, unknown> | null;
  canvasSettings?: {
    width?: number;
    height?: number;
    gridSize?: number;
  } | null;
  defaultGridLayoutsByComponent?: Record<string, unknown> | null;
}

/**
 * Get merged company defaults (Global + Company). Used by Form Branding Defaults page.
 */
export async function getCompanyFormDefaults(
  companyId: number
): Promise<FormDefaultsPayload> {
  const res = await apiClient.get<FormDefaultsPayload>(
    `/api/companies/${companyId}/form-defaults`
  );
  return res.data ?? {};
}

/**
 * Update company form defaults. Used by "Save to Company Defaults" in Builder.
 */
export async function putCompanyFormDefaults(
  companyId: number,
  payload: FormDefaultsPayload
): Promise<FormDefaultsPayload> {
  const res = await apiClient.put<FormDefaultsPayload>(
    `/api/companies/${companyId}/form-defaults`,
    payload
  );
  return res.data ?? {};
}
