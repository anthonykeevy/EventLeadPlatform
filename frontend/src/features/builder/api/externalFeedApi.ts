/**
 * External data feed API (Story 6.5d) — address-au + company-abr proxies.
 */
import axios from 'axios';
import { apiClient } from '../../../lib/apiClient';
import {
  searchCompanies,
  type CompanySearchError,
  type CompanySearchResponse,
} from '../../companies/api/companiesApi';

export interface AddressAuSuggestion {
  id: string;
  label: string;
  raw?: unknown;
}

export interface AddressAuSearchResponse {
  items: AddressAuSuggestion[];
  source?: string;
}

export interface AddressAuResolvedValue {
  displayText: string;
  psmaAddressId: string | null;
  validationSource: 'geoscape' | 'manual';
  resolvedFields?: {
    line1?: string;
    line2?: string;
    suburb?: string;
    state?: string;
    postcode?: string;
    formattedAddress?: string;
    psmaAddressId?: string;
  };
  addressModifiedAfterResolve?: boolean;
}

export interface CompanyAbrResolvedValue {
  displayText: string;
  validationSource: 'abr' | 'manual';
  legalEntityName?: string;
  abn?: string | null;
  acn?: string | null;
  entityType?: string | null;
  abnStatus?: string | null;
  gstRegistered?: boolean | null;
  tradingAs?: string | null;
  matchType?: string;
}

function normalizeSuggestion(item: Record<string, unknown>): AddressAuSuggestion {
  const id = String(item.id ?? item.psmaAddressId ?? '');
  const label = String(item.label ?? item.address ?? id);
  return { id, label, raw: item.raw ?? item };
}

function apiErrorMessage(err: unknown, fallback: string): string {
  if (axios.isAxiosError(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === 'string') return detail;
    if (typeof detail === 'object' && detail !== null && 'message' in detail) {
      return String((detail as { message: unknown }).message);
    }
    if (err.message) return err.message;
  }
  if (err instanceof Error) return err.message;
  return fallback;
}

export async function searchAddressAu(
  query: string,
  limit = 8
): Promise<AddressAuSearchResponse> {
  try {
    const response = await apiClient.get<AddressAuSearchResponse>(
      '/api/external-feed/address-au/search',
      { params: { q: query.trim(), limit } }
    );
    const items = (response.data?.items ?? []).map((item) =>
      normalizeSuggestion(item as Record<string, unknown>)
    );
    return { items, source: response.data?.source };
  } catch (err) {
    throw new Error(apiErrorMessage(err, 'Address search failed'));
  }
}

export async function resolveAddressAu(
  psmaAddressId: string,
  selectedLabel?: string
): Promise<AddressAuResolvedValue> {
  const response = await apiClient.post<{
    psmaAddressId: string;
    resolvedFields?: AddressAuResolvedValue['resolvedFields'];
    validationSource?: string;
  }>('/api/external-feed/address-au/resolve', { psmaAddressId });

  const fields = response.data.resolvedFields ?? {};
  const formatted =
    fields.formattedAddress ||
    [fields.line1, fields.suburb, fields.state, fields.postcode].filter(Boolean).join(', ');
  const labelFallback = (selectedLabel || '').trim();

  return {
    displayText: formatted || labelFallback || psmaAddressId,
    psmaAddressId,
    validationSource: 'geoscape',
    resolvedFields: {
      ...fields,
      formattedAddress: formatted || labelFallback || fields.formattedAddress,
    },
  };
}

export async function searchCompanyAbr(
  query: string,
  maxResults = 10
): Promise<CompanySearchResponse> {
  try {
    const response = await apiClient.post<{
      search_type: string;
      query: string;
      results: unknown[];
      result_count: number;
      cached: boolean;
      response_time_ms: number;
    }>('/api/external-feed/company-abr/search', {
      query: query.trim(),
      max_results: maxResults,
    });
    const data = response.data;
    return {
      searchType: data.search_type as CompanySearchResponse['searchType'],
      query: data.query,
      results: (data.results as Array<Record<string, unknown>>).map((r) => ({
        companyName: String(r.company_name ?? ''),
        abn: (r.abn as string) ?? null,
        acn: (r.acn as string) ?? null,
        abnFormatted: (r.abn_formatted as string) ?? null,
        gstRegistered: (r.gst_registered as boolean) ?? null,
        entityType: (r.entity_type as string) ?? null,
        businessAddress: (r.business_address as string) ?? null,
        status: (r.status as string) ?? null,
        businessNames: (r.business_names as string[] | undefined) ?? null,
        matchedName: (r.matched_name as string) ?? null,
        matchType: (r.match_type as string) ?? null,
      })),
      resultCount: data.result_count,
      cached: data.cached,
      responseTimeMs: data.response_time_ms,
    };
  } catch (err) {
    if (axios.isAxiosError(err) && (err.code === 'ERR_NETWORK' || !err.response)) {
      return searchCompanies(query, maxResults);
    }
    throw new Error(apiErrorMessage(err, 'Company search failed'));
  }
}

export type { CompanySearchError, CompanySearchResponse };

export function displayTextFromFieldValue(value: unknown): string {
  if (value == null) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'object' && value !== null && 'displayText' in value) {
    return String((value as { displayText?: string }).displayText ?? '');
  }
  return '';
}
