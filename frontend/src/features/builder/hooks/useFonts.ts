/**
 * Font Hooks - Story 3.5
 * 
 * React Query hooks for fetching font data from the backend API.
 * Includes recently used fonts management via localStorage.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useState, useCallback, useEffect } from 'react';
import { fontsApi } from '../api/fontsApi';
import {
    FontFamilySummary,
    FontFamilyDetail,
    FontCategoryInfo,
    FontCategory,
    FontUsageContext,
    FontUsageAction,
    RecentlyUsedFont,
} from '../api/fontTypes';

// ═══════════════════════════════════════════════════════════════════════════
// QUERY KEYS
// ═══════════════════════════════════════════════════════════════════════════

export const fontQueryKeys = {
    all: ['fonts'] as const,
    list: (params?: { query?: string; category?: FontCategory }) => 
        [...fontQueryKeys.all, 'list', params] as const,
    featured: () => [...fontQueryKeys.all, 'featured'] as const,
    popular: (limit?: number, category?: FontCategory) => 
        [...fontQueryKeys.all, 'popular', { limit, category }] as const,
    categories: () => [...fontQueryKeys.all, 'categories'] as const,
    detail: (fontFamilyId: number | null) => 
        [...fontQueryKeys.all, 'detail', fontFamilyId] as const,
    byName: (familyName: string) => 
        [...fontQueryKeys.all, 'byName', familyName] as const,
};

// ═══════════════════════════════════════════════════════════════════════════
// FONT LIST HOOKS
// ═══════════════════════════════════════════════════════════════════════════

interface UseFontsOptions {
    query?: string;
    category?: FontCategory;
    page?: number;
    pageSize?: number;
    enabled?: boolean;
}

/**
 * Hook to fetch fonts with search and category filtering
 */
export function useFonts(options: UseFontsOptions = {}) {
    const { query, category, page = 1, pageSize = 50, enabled = true } = options;

    return useQuery({
        queryKey: fontQueryKeys.list({ query, category }),
        queryFn: () => fontsApi.list({ 
            query, 
            category, 
            page, 
            page_size: pageSize,
            sort_by: 'popularity',
        }),
        enabled,
        staleTime: 5 * 60 * 1000, // 5 minutes
        gcTime: 30 * 60 * 1000,   // 30 minutes (formerly cacheTime)
    });
}

/**
 * Hook to fetch featured fonts
 */
export function useFeaturedFonts() {
    return useQuery({
        queryKey: fontQueryKeys.featured(),
        queryFn: () => fontsApi.getFeatured(),
        staleTime: 10 * 60 * 1000, // 10 minutes
        gcTime: 60 * 60 * 1000,    // 1 hour
    });
}

/**
 * Hook to fetch popular fonts
 */
export function usePopularFonts(limit = 20, category?: FontCategory) {
    return useQuery({
        queryKey: fontQueryKeys.popular(limit, category),
        queryFn: () => fontsApi.getPopular(limit, category),
        staleTime: 5 * 60 * 1000,
        gcTime: 30 * 60 * 1000,
    });
}

/**
 * Hook to fetch font categories with counts
 */
export function useFontCategories() {
    return useQuery({
        queryKey: fontQueryKeys.categories(),
        queryFn: () => fontsApi.getCategories(),
        staleTime: 30 * 60 * 1000, // 30 minutes (categories rarely change)
        gcTime: 60 * 60 * 1000,
    });
}

// ═══════════════════════════════════════════════════════════════════════════
// FONT DETAIL HOOKS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Hook to fetch complete font details including variants and axes
 */
export function useFontDetails(fontFamilyId: number | null) {
    return useQuery({
        queryKey: fontQueryKeys.detail(fontFamilyId),
        queryFn: () => fontsApi.getDetails(fontFamilyId!),
        enabled: fontFamilyId !== null,
        staleTime: 5 * 60 * 1000,
        gcTime: 30 * 60 * 1000,
    });
}

/**
 * Hook to fetch font details by family name
 */
export function useFontDetailsByName(familyName: string | null) {
    return useQuery({
        queryKey: fontQueryKeys.byName(familyName ?? ''),
        queryFn: () => fontsApi.getByName(familyName!),
        enabled: familyName !== null && familyName.length > 0,
        staleTime: 5 * 60 * 1000,
        gcTime: 30 * 60 * 1000,
    });
}

// ═══════════════════════════════════════════════════════════════════════════
// FONT USAGE LOGGING
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Hook for logging font usage analytics
 */
export function useLogFontUsage() {
    return useMutation({
        mutationFn: ({ 
            fontFamilyId, 
            context, 
            action,
            fontVariantId,
        }: {
            fontFamilyId: number;
            context: FontUsageContext;
            action: FontUsageAction;
            fontVariantId?: number;
        }) => fontsApi.logUsage(fontFamilyId, {
            context,
            action,
            font_variant_id: fontVariantId,
        }),
        // Silent failure - analytics shouldn't block UI
        onError: (error) => {
            console.warn('[FontUsage] Failed to log usage:', error);
        },
    });
}

// ═══════════════════════════════════════════════════════════════════════════
// RECENTLY USED FONTS (LocalStorage)
// ═══════════════════════════════════════════════════════════════════════════

const RECENTLY_USED_KEY = 'builder_recently_used_fonts';
const MAX_RECENTLY_USED = 5;

/**
 * Get recently used fonts from localStorage
 */
function getRecentlyUsedFromStorage(): RecentlyUsedFont[] {
    try {
        const stored = localStorage.getItem(RECENTLY_USED_KEY);
        if (!stored) return [];
        const parsed = JSON.parse(stored);
        return Array.isArray(parsed) ? parsed : [];
    } catch {
        return [];
    }
}

/**
 * Save recently used fonts to localStorage
 */
function saveRecentlyUsedToStorage(fonts: RecentlyUsedFont[]): void {
    try {
        localStorage.setItem(RECENTLY_USED_KEY, JSON.stringify(fonts));
    } catch (error) {
        console.warn('[RecentlyUsed] Failed to save:', error);
    }
}

/**
 * Hook to manage recently used fonts
 */
export function useRecentlyUsedFonts() {
    const [recentFonts, setRecentFonts] = useState<RecentlyUsedFont[]>([]);

    // Load from localStorage on mount
    useEffect(() => {
        setRecentFonts(getRecentlyUsedFromStorage());
    }, []);

    /**
     * Add a font to recently used list
     */
    const addToRecentlyUsed = useCallback((font: FontFamilySummary) => {
        setRecentFonts((prev) => {
            // Remove if already exists
            const filtered = prev.filter(f => f.font_family_id !== font.font_family_id);
            
            // Add to beginning
            const newEntry: RecentlyUsedFont = {
                font_family_id: font.font_family_id,
                family_name: font.family_name,
                category: font.category,
                is_variable_font: font.is_variable_font,
                timestamp: Date.now(),
            };
            
            const updated = [newEntry, ...filtered].slice(0, MAX_RECENTLY_USED);
            
            // Save to localStorage
            saveRecentlyUsedToStorage(updated);
            
            return updated;
        });
    }, []);

    /**
     * Clear all recently used fonts
     */
    const clearRecentlyUsed = useCallback(() => {
        setRecentFonts([]);
        localStorage.removeItem(RECENTLY_USED_KEY);
    }, []);

    return {
        recentFonts,
        addToRecentlyUsed,
        clearRecentlyUsed,
    };
}

// ═══════════════════════════════════════════════════════════════════════════
// COMBINED FONT DATA HOOK
// ═══════════════════════════════════════════════════════════════════════════

interface UseFontPickerDataOptions {
    searchQuery?: string;
    selectedCategory?: FontCategory | null;
}

/**
 * Combined hook for font picker that fetches all needed data
 */
export function useFontPickerData(options: UseFontPickerDataOptions = {}) {
    const { searchQuery, selectedCategory } = options;

    const categoriesQuery = useFontCategories();
    const featuredQuery = useFeaturedFonts();
    const popularQuery = usePopularFonts(20);
    const { recentFonts, addToRecentlyUsed, clearRecentlyUsed } = useRecentlyUsedFonts();

    // Only fetch search results if there's a query or category filter
    const shouldSearch = Boolean(searchQuery || selectedCategory);
    const searchQuery_ = useFonts({
        query: searchQuery,
        category: selectedCategory ?? undefined,
        enabled: shouldSearch,
    });

    return {
        // Data
        categories: categoriesQuery.data ?? [],
        featuredFonts: featuredQuery.data ?? [],
        popularFonts: popularQuery.data ?? [],
        searchResults: searchQuery_.data?.fonts ?? [],
        recentFonts,

        // Loading states
        isLoadingCategories: categoriesQuery.isLoading,
        isLoadingFeatured: featuredQuery.isLoading,
        isLoadingPopular: popularQuery.isLoading,
        isSearching: searchQuery_.isLoading,

        // Errors
        hasError: categoriesQuery.isError || featuredQuery.isError || popularQuery.isError,

        // Actions
        addToRecentlyUsed,
        clearRecentlyUsed,
    };
}

export default {
    useFonts,
    useFeaturedFonts,
    usePopularFonts,
    useFontCategories,
    useFontDetails,
    useFontDetailsByName,
    useLogFontUsage,
    useRecentlyUsedFonts,
    useFontPickerData,
};

