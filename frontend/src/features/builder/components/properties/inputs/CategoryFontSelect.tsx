/**
 * CategoryFontSelect - Story 3.5 (Rewritten)
 * 
 * Advanced font picker with:
 * - Featured fonts section
 * - Recently used fonts (localStorage)
 * - Category tabs with counts from API
 * - Popular fonts highlighting
 * - Language support indicators
 * - Variable font badges
 * - Icon fonts hidden by default (separate tab)
 * 
 * Uses the Google Fonts backend API via React Query hooks.
 */

import React, { useState, useMemo, useCallback } from 'react';
import { 
    ChevronDown, 
    Globe, 
    Search, 
    X, 
    Star, 
    Crown, 
    Clock,
    Loader2,
} from 'lucide-react';

// ═══════════════════════════════════════════════════════════════════════════
// ICON FONT DETECTION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Known icon font families that should be hidden from main text font list
 * These are fonts where characters map to icons, not text glyphs
 */
const ICON_FONT_PATTERNS = [
    'Material Icons',
    'Material Symbols',
    'Noto Color Emoji',
    'Noto Emoji',
    'Font Awesome',
    'Ionicons',
    'Feather',
];

/**
 * Check if a font is an icon font
 */
function isIconFont(familyName: string): boolean {
    return ICON_FONT_PATTERNS.some(pattern => 
        familyName.toLowerCase().includes(pattern.toLowerCase())
    );
}
import { 
    useFontPickerData, 
    useLogFontUsage,
} from '../../../hooks/useFonts';
import { 
    FontFamilySummary, 
    FontCategory,
    FontCategoryInfo,
    LANGUAGE_SUPPORT_INFO,
    RecentlyUsedFont,
} from '../../../api/fontTypes';
import { loadGoogleFont } from '../../../utils/fontLoader';

interface CategoryFontSelectProps {
    label: string;
    value: string;
    onChange: (fontFamily: string, fontFamilyId?: number) => void;
    helpText?: string;
}

/**
 * Advanced font picker with API-driven data
 */
export const CategoryFontSelect: React.FC<CategoryFontSelectProps> = ({
    label,
    value,
    onChange,
    helpText,
}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState<FontCategory | null>(null);
    // Icon fonts are filtered out but not shown in a separate tab yet
    // (feature deferred - no UI to use icon fonts in form builder)
    const showIconFonts = false;

    // Fetch all font data
    const {
        categories,
        featuredFonts,
        popularFonts,
        searchResults,
        recentFonts,
        isLoadingCategories,
        isLoadingFeatured,
        isLoadingPopular,
        isSearching,
        addToRecentlyUsed,
    } = useFontPickerData({
        searchQuery: searchQuery.trim() || undefined,
        selectedCategory,
    });

    const { mutate: logUsage } = useLogFontUsage();

    // Filter out icon fonts from text fonts, or show only icon fonts
    const filterFonts = useCallback((fonts: FontFamilySummary[]) => {
        if (showIconFonts) {
            return fonts.filter(f => isIconFont(f.family_name));
        }
        return fonts.filter(f => !isIconFont(f.family_name));
    }, [showIconFonts]);

    // Determine which fonts to show based on search/filter state
    const displayedFonts = useMemo(() => {
        let fonts: FontFamilySummary[];
        if (searchQuery.trim() || selectedCategory) {
            fonts = searchResults;
        } else {
            fonts = popularFonts;
        }
        return filterFonts(fonts);
    }, [searchQuery, selectedCategory, searchResults, popularFonts, filterFonts]);

    // Handle font selection
    const handleSelect = useCallback((font: FontFamilySummary) => {
        // Load the Google Font
        loadGoogleFont(font.family_name, font.is_variable_font, font.min_weight, font.max_weight);
        
        // Notify parent
        onChange(font.family_name, font.font_family_id);
        
        // Add to recently used
        addToRecentlyUsed(font);
        
        // Log usage for analytics (fire and forget)
        logUsage({
            fontFamilyId: font.font_family_id,
            context: 'FormBuilder',
            action: 'Selected',
        });
        
        // Close dropdown
        setIsOpen(false);
        setSearchQuery('');
    }, [onChange, addToRecentlyUsed, logUsage]);

    // Handle recently used font selection (has less data)
    const handleSelectRecent = useCallback((font: RecentlyUsedFont) => {
        loadGoogleFont(font.family_name, font.is_variable_font);
        onChange(font.family_name, font.font_family_id);
        logUsage({
            fontFamilyId: font.font_family_id,
            context: 'FormBuilder',
            action: 'Selected',
        });
        setIsOpen(false);
        setSearchQuery('');
    }, [onChange, logUsage]);

    const isLoading = isLoadingCategories || isLoadingFeatured || isLoadingPopular;

    return (
        <div className="space-y-1.5">
            <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                {label}
            </label>
            
            {/* Selected Font Button */}
            <div className="relative">
                <button
                    type="button"
                    onClick={() => setIsOpen(!isOpen)}
                    className="w-full flex items-center justify-between px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                >
                    <span 
                        className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate"
                        style={{ fontFamily: value }}
                    >
                        {value || 'Select font...'}
                    </span>
                    <ChevronDown 
                        size={16} 
                        className={`text-gray-400 transition-transform flex-shrink-0 ${isOpen ? 'rotate-180' : ''}`} 
                    />
                </button>

                {/* Dropdown Panel */}
                {isOpen && (
                    <div className="absolute z-50 mt-1 w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl max-h-[450px] overflow-hidden flex flex-col">
                        {/* Search Input */}
                        <div className="p-2 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
                            <div className="relative">
                                <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Search 1,900+ fonts..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full pl-8 pr-8 py-1.5 text-sm bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-600 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                                    autoFocus
                                />
                                {searchQuery && (
                                    <button
                                        onClick={() => setSearchQuery('')}
                                        className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                    >
                                        <X size={14} />
                                    </button>
                                )}
                            </div>
                        </div>

                        {/* Category Tabs */}
                        <div className="flex gap-1 p-2 border-b border-gray-200 dark:border-gray-700 overflow-x-auto flex-shrink-0">
                            <CategoryTab
                                label="All"
                                count={categories.reduce((sum, c) => sum + c.font_count, 0)}
                                isActive={selectedCategory === null}
                                onClick={() => setSelectedCategory(null)}
                            />
                            {categories.map(cat => (
                                <CategoryTab
                                    key={cat.category_code}
                                    label={cat.category_name}
                                    count={cat.font_count}
                                    isActive={selectedCategory === cat.category_code}
                                    onClick={() => setSelectedCategory(cat.category_code)}
                                />
                            ))}
                            {/* Note: Icon fonts tab removed - no UI to use them yet */}
                        </div>

                        {/* Font List */}
                        <div className="overflow-y-auto flex-1">
                            {isLoading ? (
                                <div className="flex items-center justify-center py-8">
                                    <Loader2 className="w-6 h-6 text-blue-500 animate-spin" />
                                </div>
                            ) : (
                                <>
                                    {/* Featured Section */}
                                    {!searchQuery && !selectedCategory && featuredFonts.length > 0 && (
                                        <FontSection
                                            icon={<Crown size={12} className="text-amber-500" />}
                                            title="Featured"
                                            fonts={filterFonts(featuredFonts).slice(0, 5)}
                                            selectedValue={value}
                                            onSelect={handleSelect}
                                            popularFonts={popularFonts}
                                        />
                                    )}

                                    {/* Recently Used Section */}
                                    {!searchQuery && !selectedCategory && recentFonts.length > 0 && (
                                        <div className="border-b border-gray-100 dark:border-gray-700">
                                            <div className="sticky top-0 px-3 py-1.5 bg-gray-50 dark:bg-gray-900 flex items-center gap-1.5">
                                                <Clock size={12} className="text-gray-400" />
                                                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">
                                                    Recently Used
                                                </span>
                                            </div>
                                            {recentFonts
                                                .filter(f => !isIconFont(f.family_name))
                                                .map(font => (
                                                    <RecentFontOption
                                                        key={font.font_family_id}
                                                        font={font}
                                                        isSelected={font.family_name === value}
                                                        onSelect={() => handleSelectRecent(font)}
                                                    />
                                                ))}
                                        </div>
                                    )}

                                    {/* Main Font List */}
                                    {displayedFonts.length > 0 ? (
                                        <FontSection
                                            icon={searchQuery || selectedCategory ? <Search size={12} className="text-gray-400" /> : <Star size={12} className="text-blue-500" />}
                                            title={searchQuery || selectedCategory ? 'Results' : 'Popular'}
                                            fonts={displayedFonts}
                                            selectedValue={value}
                                            onSelect={handleSelect}
                                            popularFonts={popularFonts}
                                            showCount
                                        />
                                    ) : isSearching ? (
                                        <div className="flex items-center justify-center py-8">
                                            <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
                                        </div>
                                    ) : searchQuery ? (
                                        <div className="p-4 text-center text-sm text-gray-500">
                                            No fonts found for "{searchQuery}"
                                        </div>
                                    ) : null}
                                </>
                            )}
                        </div>
                    </div>
                )}
            </div>

            {helpText && (
                <p className="text-[10px] text-gray-500 dark:text-gray-400">{helpText}</p>
            )}

            {/* Click outside to close */}
            {isOpen && (
                <div 
                    className="fixed inset-0 z-40" 
                    onClick={() => setIsOpen(false)}
                />
            )}
        </div>
    );
};

// ═══════════════════════════════════════════════════════════════════════════
// SUB-COMPONENTS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Category tab button
 */
const CategoryTab: React.FC<{
    label: string;
    count: number;
    isActive: boolean;
    onClick: () => void;
}> = ({ label, count, isActive, onClick }) => (
    <button
        type="button"
        onClick={onClick}
        className={`px-2 py-1 text-xs rounded-md whitespace-nowrap transition-colors ${
            isActive
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
        }`}
    >
        {label}
        <span className={`ml-1 ${isActive ? 'text-blue-200' : 'text-gray-400'}`}>
            ({count})
        </span>
    </button>
);

/**
 * Font section with header
 */
const FontSection: React.FC<{
    icon: React.ReactNode;
    title: string;
    fonts: FontFamilySummary[];
    selectedValue: string;
    onSelect: (font: FontFamilySummary) => void;
    popularFonts: FontFamilySummary[];
    showCount?: boolean;
}> = ({ icon, title, fonts, selectedValue, onSelect, popularFonts, showCount }) => {
    const popularIds = useMemo(() => 
        new Set(popularFonts.slice(0, 20).map(f => f.font_family_id)),
        [popularFonts]
    );

    return (
        <div className="border-b border-gray-100 dark:border-gray-700 last:border-b-0">
            <div className="sticky top-0 px-3 py-1.5 bg-gray-50 dark:bg-gray-900 flex items-center gap-1.5">
                {icon}
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">
                    {title}
                </span>
                {showCount && (
                    <span className="text-[10px] text-gray-400">
                        ({fonts.length})
                    </span>
                )}
            </div>
            {fonts.map(font => (
                <FontOption
                    key={font.font_family_id}
                    font={font}
                    isSelected={font.family_name === selectedValue}
                    isPopular={popularIds.has(font.font_family_id)}
                    onSelect={() => onSelect(font)}
                />
            ))}
        </div>
    );
};

/**
 * Individual font option in the dropdown
 */
const FontOption: React.FC<{
    font: FontFamilySummary;
    isSelected: boolean;
    isPopular?: boolean;
    onSelect: () => void;
}> = ({ font, isSelected, isPopular, onSelect }) => {
    // Preload font on hover
    const handleMouseEnter = () => {
        loadGoogleFont(font.family_name, font.is_variable_font, font.min_weight, font.max_weight);
    };

    // Get language support indicators
    const languageChips = useMemo(() => {
        const chips: string[] = [];
        // We don't have full language support in summary, but we can show i18n indicator
        // based on the presence of non-Latin subsets
        if (font.total_subsets > 2) {
            chips.push('i18n');
        }
        return chips;
    }, [font]);

    return (
        <button
            type="button"
            onClick={onSelect}
            onMouseEnter={handleMouseEnter}
            className={`w-full flex items-center justify-between px-3 py-2 text-left hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors ${
                isSelected ? 'bg-blue-50 dark:bg-blue-900/30' : ''
            }`}
        >
            <div className="flex items-center gap-2 min-w-0">
                <span 
                    className="text-sm text-gray-900 dark:text-gray-100 truncate"
                    style={{ fontFamily: font.family_name }}
                >
                    {font.family_name}
                </span>
                
                {/* Badges */}
                <div className="flex items-center gap-1 flex-shrink-0">
                    {font.is_featured && (
                        <Crown size={10} className="text-amber-500" aria-label="Featured" />
                    )}
                    {isPopular && !font.is_featured && (
                        <Star size={10} className="text-blue-500" aria-label="Popular" />
                    )}
                    {font.is_variable_font && (
                        <span className="px-1 py-0.5 text-[8px] font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded" title="Variable font">
                            VAR
                        </span>
                    )}
                    {languageChips.includes('i18n') && (
                        <Globe size={10} className="text-green-500" aria-label="International support" />
                    )}
                </div>
            </div>

            <span className="text-[10px] text-gray-400 flex-shrink-0 ml-2">
                {font.total_variants} {font.total_variants === 1 ? 'style' : 'styles'}
            </span>
        </button>
    );
};

/**
 * Recently used font option (simplified data)
 */
const RecentFontOption: React.FC<{
    font: RecentlyUsedFont;
    isSelected: boolean;
    onSelect: () => void;
}> = ({ font, isSelected, onSelect }) => {
    const handleMouseEnter = () => {
        loadGoogleFont(font.family_name, font.is_variable_font);
    };

    return (
        <button
            type="button"
            onClick={onSelect}
            onMouseEnter={handleMouseEnter}
            className={`w-full flex items-center justify-between px-3 py-2 text-left hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors ${
                isSelected ? 'bg-blue-50 dark:bg-blue-900/30' : ''
            }`}
        >
            <span 
                className="text-sm text-gray-900 dark:text-gray-100"
                style={{ fontFamily: font.family_name }}
            >
                {font.family_name}
            </span>
            {font.is_variable_font && (
                <span className="px-1 py-0.5 text-[8px] font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded">
                    VAR
                </span>
            )}
        </button>
    );
};

export default CategoryFontSelect;
