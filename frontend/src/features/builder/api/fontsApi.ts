/**
 * Fonts API Client - Story 3.5
 * 
 * API client for the Google Fonts backend at /api/fonts.
 * Uses the shared apiClient with authentication.
 */

import { apiClient } from '../../../lib/apiClient';
import {
    FontListResponse,
    FontListParams,
    FontFamilySummary,
    FontFamilyDetail,
    FontCategoryInfo,
    FontUsageLogRequest,
    FontCategory,
} from './fontTypes';

const FONTS_BASE = '/api/fonts';

// ═══════════════════════════════════════════════════════════════════════════
// TRANSFORMERS: Backend snake_case to Frontend (already snake_case in this API)
// ═══════════════════════════════════════════════════════════════════════════

// Note: The fonts API already uses snake_case which matches our TypeScript interfaces,
// so minimal transformation is needed. We just ensure proper typing.

function transformFontSummary(data: any): FontFamilySummary {
    return {
        font_family_id: data.font_family_id,
        google_font_id: data.google_font_id ?? null,
        family_name: data.family_name ?? '',
        category: data.category ?? 'sans-serif',
        version: data.version ?? '',
        is_variable_font: data.is_variable_font ?? false,
        min_weight: data.min_weight ?? null,
        max_weight: data.max_weight ?? null,
        has_italic: data.has_italic ?? false,
        total_variants: data.total_variants ?? 0,
        total_subsets: data.total_subsets ?? 0,
        menu_file_url: data.menu_file_url ?? null,
        popularity_rank: data.popularity_rank ?? null,
        usage_count: data.usage_count ?? 0,
        is_featured: data.is_featured ?? false,
        is_recommended: data.is_recommended ?? false,
        variant_list: data.variant_list ?? null,
    };
}

function transformFontListResponse(data: any): FontListResponse {
    return {
        fonts: (data.fonts ?? []).map(transformFontSummary),
        total: data.total ?? 0,
        page: data.page ?? 1,
        page_size: data.page_size ?? 20,
        total_pages: data.total_pages ?? 1,
    };
}

function transformFontDetail(data: any): FontFamilyDetail {
    return {
        ...transformFontSummary(data),
        sub_category: data.sub_category ?? null,
        version_number: data.version_number ?? null,
        last_modified_date: data.last_modified_date ?? '',
        specimen_url: data.specimen_url ?? null,
        has_color_capabilities: data.has_color_capabilities ?? false,
        has_regular: data.has_regular ?? true,
        supports_latin: data.supports_latin ?? true,
        supports_cyrillic: data.supports_cyrillic ?? false,
        supports_greek: data.supports_greek ?? false,
        supports_arabic: data.supports_arabic ?? false,
        supports_hebrew: data.supports_hebrew ?? false,
        supports_asian: data.supports_asian ?? false,
        display_order: data.display_order ?? null,
        license_type: data.license_type ?? null,
        license_url: data.license_url ?? null,
        designer: data.designer ?? null,
        designer_url: data.designer_url ?? null,
        foundry: data.foundry ?? null,
        last_sync_date: data.last_sync_date ?? '',
        variants: (data.variants ?? []).map((v: any) => ({
            font_variant_id: v.font_variant_id,
            variant_name: v.variant_name ?? '',
            weight: v.weight ?? 400,
            weight_name: v.weight_name ?? null,
            is_italic: v.is_italic ?? false,
            ttf_file_url: v.ttf_file_url ?? null,
            display_order: v.display_order ?? 0,
            is_default: v.is_default ?? false,
        })),
        subsets: (data.subsets ?? []).map((s: any) => ({
            font_subset_id: s.font_subset_id,
            subset_code: s.subset_code ?? '',
            subset_name: s.subset_name ?? '',
            subset_group: s.subset_group ?? '',
            is_extended: s.is_extended ?? false,
        })),
        axes: (data.axes ?? []).map((a: any) => ({
            font_axis_id: a.font_axis_id,
            axis_tag: a.axis_tag ?? '',
            axis_name: a.axis_name ?? '',
            min_value: a.min_value ?? 100,
            max_value: a.max_value ?? 900,
            default_value: a.default_value ?? null,
            is_standard: a.is_standard ?? true,
            css_property: a.css_property ?? null,
        })),
    };
}

function transformCategoryInfo(data: any): FontCategoryInfo {
    return {
        category_code: data.category_code ?? 'sans-serif',
        category_name: data.category_name ?? '',
        description: data.description ?? null,
        icon_class: data.icon_class ?? null,
        display_order: data.display_order ?? 0,
        font_count: data.font_count ?? 0,
    };
}

// ═══════════════════════════════════════════════════════════════════════════
// API CLIENT
// ═══════════════════════════════════════════════════════════════════════════

export const fontsApi = {
    /**
     * List fonts with filtering and pagination
     * GET /api/fonts
     */
    list: async (params?: FontListParams): Promise<FontListResponse> => {
        const response = await apiClient.get(FONTS_BASE, { params });
        return transformFontListResponse(response.data);
    },

    /**
     * Get featured fonts
     * GET /api/fonts/featured
     */
    getFeatured: async (): Promise<FontFamilySummary[]> => {
        const response = await apiClient.get(`${FONTS_BASE}/featured`);
        return (response.data ?? []).map(transformFontSummary);
    },

    /**
     * Get font categories with counts
     * GET /api/fonts/categories
     */
    getCategories: async (): Promise<FontCategoryInfo[]> => {
        const response = await apiClient.get(`${FONTS_BASE}/categories`);
        return (response.data ?? []).map(transformCategoryInfo);
    },

    /**
     * Get popular fonts
     * GET /api/fonts/popular
     */
    getPopular: async (limit = 20, category?: FontCategory): Promise<FontFamilySummary[]> => {
        const response = await apiClient.get(`${FONTS_BASE}/popular`, {
            params: { limit, category },
        });
        return (response.data ?? []).map(transformFontSummary);
    },

    /**
     * Get font details with variants and axes
     * GET /api/fonts/{font_family_id}
     */
    getDetails: async (fontFamilyId: number): Promise<FontFamilyDetail> => {
        const response = await apiClient.get(`${FONTS_BASE}/${fontFamilyId}`);
        return transformFontDetail(response.data);
    },

    /**
     * Get font by family name
     * GET /api/fonts/by-name/{family_name}
     */
    getByName: async (familyName: string): Promise<FontFamilyDetail> => {
        const response = await apiClient.get(
            `${FONTS_BASE}/by-name/${encodeURIComponent(familyName)}`
        );
        return transformFontDetail(response.data);
    },

    /**
     * Log font usage for analytics
     * POST /api/fonts/{font_family_id}/usage
     */
    logUsage: async (fontFamilyId: number, data: FontUsageLogRequest): Promise<void> => {
        await apiClient.post(`${FONTS_BASE}/${fontFamilyId}/usage`, data);
    },

    /**
     * Search fonts by query
     * Convenience method that wraps list() with search parameters
     */
    search: async (query: string, category?: FontCategory): Promise<FontFamilySummary[]> => {
        const response = await fontsApi.list({
            query,
            category,
            page_size: 50,
            sort_by: 'popularity',
        });
        return response.fonts;
    },
};

export default fontsApi;

