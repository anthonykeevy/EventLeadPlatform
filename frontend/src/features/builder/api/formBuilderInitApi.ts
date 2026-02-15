/**
 * Form Builder Init API — Story 5.2 T05
 * Single payload: merged defaults + component catalog + DefinitionJSON skeleton
 * @see docs/stories/STORY-5.2-FORM-BUILDER-INIT-API.md
 */

import { apiClient } from '../../../lib/apiClient';

export interface FormBuilderInitRequest {
  companyId: number;
  eventId: number;
}

export interface FormBuilderInitContext {
  companyId: number;
  eventId: number;
  countryId?: number | null;
}

export interface FormBuilderInitDefaults {
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
  defaultGridLayoutsByComponent?: Record<string, { vertical?: unknown; horizontal?: unknown }> | null;
}

export interface FormBuilderInitComponent {
  componentCode: string;
  displayName: string;
  category?: string;
  sortOrder?: number;
  propertiesSchema?: Record<string, unknown> | null;
  structure?: Record<string, unknown> | null;
  defaultGridLayoutVertical?: Record<string, unknown> | null;
  defaultGridLayoutHorizontal?: Record<string, unknown> | null;
  validationConfig?: Record<string, unknown> | null;
}

export interface FormBuilderInitResponse {
  schemaVersion?: number;
  context: FormBuilderInitContext;
  defaults: FormBuilderInitDefaults;
  components: FormBuilderInitComponent[];
  definitionJSON: Record<string, unknown>;
}

/**
 * Call POST /api/form-builder/init to get merged defaults, component catalog, and initial definition skeleton.
 * Returns null if the API is not available (404/5xx) — caller should fall back to hardcoded defaults.
 */
export async function formBuilderInit(
  request: FormBuilderInitRequest
): Promise<FormBuilderInitResponse | null> {
  try {
    const res = await apiClient.post<FormBuilderInitResponse>(
      '/api/form-builder/init',
      { companyId: request.companyId, eventId: request.eventId }
    );
    return res.data ?? null;
  } catch (err: unknown) {
    const axiosErr = err as { response?: { status?: number } };
    const status = axiosErr?.response?.status;
    // 404 = endpoint not deployed yet (T03 not merged); 5xx = server error
    if (status === 404 || (status && status >= 500)) {
      return null;
    }
    throw err;
  }
}
