import { apiClient, formatError } from "../../../lib/apiClient";

export interface ClarificationRefItem {
  code: string;
  displayName: string;
  description?: string | null;
  flagEmoji?: string | null;
  promptHint?: string | null;
  clarificationSummary?: string | null;
}

export interface ClarificationRefListResponse {
  items: ClarificationRefItem[];
  defaultCode: string;
  resolvedDefault: ClarificationRefItem;
}

export interface ClarificationSelections {
  audienceLocaleCode: string | null;
  formPurposeCode: string | null;
  respondentTypeCode: string | null;
}

async function fetchRefList(
  path: string,
  formId?: number | null
): Promise<ClarificationRefListResponse> {
  const params: Record<string, string | number> = {};
  if (formId != null) params.formId = formId;
  const response = await apiClient.get<ClarificationRefListResponse>(path, { params });
  return response.data;
}

export async function fetchAudienceLocales(
  formId?: number | null
): Promise<ClarificationRefListResponse> {
  return fetchRefList("/api/ref/audience-locales", formId);
}

export async function fetchFormPurposes(
  formId?: number | null
): Promise<ClarificationRefListResponse> {
  return fetchRefList("/api/ref/form-purposes", formId);
}

export async function fetchRespondentTypes(
  formId?: number | null
): Promise<ClarificationRefListResponse> {
  return fetchRefList("/api/ref/respondent-types", formId);
}

export async function loadClarificationDefaults(
  formId?: number | null
): Promise<ClarificationSelections> {
  try {
    const [locales, purposes, respondents] = await Promise.all([
      fetchAudienceLocales(formId),
      fetchFormPurposes(formId),
      fetchRespondentTypes(formId),
    ]);
    return {
      audienceLocaleCode: locales.resolvedDefault.code,
      formPurposeCode: purposes.resolvedDefault.code,
      respondentTypeCode: respondents.resolvedDefault.code,
    };
  } catch (error) {
    throw new Error(formatError(error));
  }
}
