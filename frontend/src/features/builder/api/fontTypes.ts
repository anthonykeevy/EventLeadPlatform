/**
 * Font API Types - Story 3.5
 * 
 * TypeScript interfaces matching the Google Fonts backend API responses.
 * Based on: docs/data-domains/GoogleFonts/story-3.5-integration.md
 */

// ═══════════════════════════════════════════════════════════════════════════
// ENUMS & BASIC TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Font category types matching Google Fonts categories
 */
export type FontCategory = 'serif' | 'sans-serif' | 'display' | 'handwriting' | 'monospace';

/**
 * Font source - where the font came from
 */
export type FontSource = 'Google' | 'Custom' | 'System';

/**
 * Font usage context for analytics
 */
export type FontUsageContext = 'FormBuilder' | 'TemplateCreation' | 'Preview' | 'Export' | 'Settings';

/**
 * Font usage action for analytics
 */
export type FontUsageAction = 'Selected' | 'Applied' | 'Previewed' | 'Removed' | 'Downloaded';

// ═══════════════════════════════════════════════════════════════════════════
// FONT FAMILY TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Font family summary for list views
 * Returned by GET /api/fonts
 */
export interface FontFamilySummary {
    font_family_id: number;
    google_font_id: string | null;  // null for custom fonts
    family_name: string;
    category: FontCategory;
    version: string;
    is_variable_font: boolean;
    min_weight: number | null;
    max_weight: number | null;
    has_italic: boolean;
    total_variants: number;
    total_subsets: number;
    menu_file_url: string | null;
    popularity_rank: number | null;
    usage_count: number;
    is_featured: boolean;
    is_recommended: boolean;
    variant_list: string | null;  // e.g., "100,300,400,500,700,900,100italic,..."
}

/**
 * Font variant (weight/style combination)
 * Included in FontFamilyDetail
 */
export interface FontVariant {
    font_variant_id: number;
    variant_name: string;
    weight: number;
    weight_name: string | null;
    is_italic: boolean;
    ttf_file_url: string | null;
    display_order: number;
    is_default: boolean;
}

/**
 * Font subset (language/script support)
 * Included in FontFamilyDetail
 */
export interface FontSubset {
    font_subset_id: number;
    subset_code: string;
    subset_name: string;
    subset_group: string;
    is_extended: boolean;
}

/**
 * Font axis for variable fonts
 * Included in FontFamilyDetail
 */
export interface FontAxis {
    font_axis_id: number;
    axis_tag: string;      // e.g., "wght", "wdth", "slnt"
    axis_name: string;     // e.g., "Weight", "Width", "Slant"
    min_value: number;
    max_value: number;
    default_value: number | null;
    is_standard: boolean;
    css_property: string | null;  // e.g., "font-weight"
}

/**
 * Complete font family details with variants, subsets, and axes
 * Returned by GET /api/fonts/{font_family_id}
 */
export interface FontFamilyDetail extends FontFamilySummary {
    sub_category: string | null;
    version_number: number | null;
    last_modified_date: string;
    specimen_url: string | null;
    has_color_capabilities: boolean;
    has_regular: boolean;
    supports_latin: boolean;
    supports_cyrillic: boolean;
    supports_greek: boolean;
    supports_arabic: boolean;
    supports_hebrew: boolean;
    supports_asian: boolean;
    display_order: number | null;
    license_type: string | null;
    license_url: string | null;
    designer: string | null;
    designer_url: string | null;
    foundry: string | null;
    last_sync_date: string;
    variants: FontVariant[];
    subsets: FontSubset[];
    axes: FontAxis[];
}

// ═══════════════════════════════════════════════════════════════════════════
// COMPANY FONT TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Company font with effective display name
 * Returned by GET /api/fonts/custom
 */
export interface CompanyFont {
    font_family_id: number;
    display_name: string;           // Effective display name (company override or original)
    internal_name: string | null;   // Name extracted from font file
    original_name: string;          // Original family name
    font_source: FontSource;
    category: FontCategory;
    is_variable_font: boolean;
    min_weight: number | null;
    max_weight: number | null;
    has_italic: boolean;
    total_variants: number;
    is_owner: boolean;
    is_shared: boolean;
    license_type: string | null;
    license_expiry_date: string | null;
    company_font_id: number | null;
}

// ═══════════════════════════════════════════════════════════════════════════
// CATEGORY TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Font category with count
 * Returned by GET /api/fonts/categories
 */
export interface FontCategoryInfo {
    category_code: FontCategory;
    category_name: string;
    description: string | null;
    icon_class: string | null;
    display_order: number;
    font_count: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// API RESPONSE TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Paginated font list response
 * Returned by GET /api/fonts
 */
export interface FontListResponse {
    fonts: FontFamilySummary[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
}

/**
 * Company font list response
 * Returned by GET /api/fonts/custom
 */
export interface CompanyFontListResponse {
    fonts: CompanyFont[];
    custom_font_count: number;
    google_font_count: number;
    total: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// REQUEST TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Parameters for listing fonts
 */
export interface FontListParams {
    query?: string;
    category?: FontCategory;
    subset?: string;
    is_variable?: boolean;
    has_italic?: boolean;
    is_featured?: boolean;
    sort_by?: 'popularity' | 'name' | 'date' | 'featured';
    page?: number;
    page_size?: number;
}

/**
 * Font usage log request
 */
export interface FontUsageLogRequest {
    context: FontUsageContext;
    action: FontUsageAction;
    font_variant_id?: number;
    context_entity_type?: string;
    context_entity_id?: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// HELPER TYPES FOR UI
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Recently used font stored in localStorage
 */
export interface RecentlyUsedFont {
    font_family_id: number;
    family_name: string;
    category: FontCategory;
    is_variable_font: boolean;
    timestamp: number;
}

/**
 * Font weight option for dropdowns/sliders
 */
export interface FontWeightOption {
    value: number;
    label: string;
    is_default?: boolean;
}

/**
 * Standard weight labels
 */
export const WEIGHT_LABELS: Record<number, string> = {
    100: 'Thin',
    200: 'Extra Light',
    300: 'Light',
    400: 'Regular',
    500: 'Medium',
    600: 'Semi-Bold',
    700: 'Bold',
    800: 'Extra-Bold',
    900: 'Black',
};

/**
 * Get weight label for a given weight value
 */
export function getWeightLabel(weight: number): string {
    // For standard weights, use the label
    if (WEIGHT_LABELS[weight]) {
        return WEIGHT_LABELS[weight];
    }
    // For variable font weights between standard values, interpolate
    return `Weight ${weight}`;
}

/**
 * Language/script display info for UI chips
 */
export const LANGUAGE_SUPPORT_INFO: Record<string, { label: string; flag?: string }> = {
    latin: { label: 'Latin', flag: '🌍' },
    cyrillic: { label: 'Cyrillic', flag: '🇷🇺' },
    greek: { label: 'Greek', flag: '🇬🇷' },
    arabic: { label: 'Arabic', flag: '🇸🇦' },
    hebrew: { label: 'Hebrew', flag: '🇮🇱' },
    asian: { label: 'CJK', flag: '🇯🇵' },
};

