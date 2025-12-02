# Story 3.5 Integration Guide - Font Properties Panel

This guide provides TypeScript types, React hooks, and implementation examples for integrating the Google Fonts domain into the Form Builder's Properties Panel.

## Overview

Story 3.5 focuses on implementing a comprehensive font properties panel that allows users to:
- Select fonts from Google Fonts or custom uploaded fonts
- Customize font weight, size, style, and color
- Preview font changes in real-time
- Access company-specific fonts with custom display names

---

## TypeScript Types

### Font API Types

```typescript
// Font Family Summary (for list views)
interface FontFamilySummary {
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
  variant_list: string | null;
}

// Font Category
type FontCategory = 'serif' | 'sans-serif' | 'display' | 'handwriting' | 'monospace';

// Font Source
type FontSource = 'Google' | 'Custom' | 'System';

// Font Variant
interface FontVariant {
  font_variant_id: number;
  variant_name: string;
  weight: number;
  weight_name: string | null;
  is_italic: boolean;
  ttf_file_url: string | null;
  display_order: number;
  is_default: boolean;
}

// Font Axis (for variable fonts)
interface FontAxis {
  font_axis_id: number;
  axis_tag: string;
  axis_name: string;
  min_value: number;
  max_value: number;
  default_value: number | null;
  is_standard: boolean;
  css_property: string | null;
}

// Complete Font Details
interface FontFamilyDetail extends FontFamilySummary {
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

// Company Font (with effective display name)
interface CompanyFont {
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

// Font List Response
interface FontListResponse {
  fonts: FontFamilySummary[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Company Font List Response
interface CompanyFontListResponse {
  fonts: CompanyFont[];
  custom_font_count: number;
  google_font_count: number;
  total: number;
}

// Font Category with count
interface FontCategoryInfo {
  category_code: FontCategory;
  category_name: string;
  description: string | null;
  icon_class: string | null;
  display_order: number;
  font_count: number;
}
```

### Font Properties State

```typescript
// Font properties for a form element
interface FontProperties {
  fontFamily: string;
  fontFamilyId?: number;
  fontSize: number;
  fontSizeUnit: 'px' | 'pt' | 'em' | 'rem';
  fontWeight: number;
  fontStyle: 'normal' | 'italic';
  lineHeight: number;
  letterSpacing: number;
  textAlign: 'left' | 'center' | 'right' | 'justify';
  textDecoration: 'none' | 'underline' | 'line-through';
  textTransform: 'none' | 'uppercase' | 'lowercase' | 'capitalize';
  color: string;
}

// Default font properties
const defaultFontProperties: FontProperties = {
  fontFamily: 'Roboto',
  fontSize: 16,
  fontSizeUnit: 'px',
  fontWeight: 400,
  fontStyle: 'normal',
  lineHeight: 1.5,
  letterSpacing: 0,
  textAlign: 'left',
  textDecoration: 'none',
  textTransform: 'none',
  color: '#1a1a1a',
};
```

---

## API Client

```typescript
// api/fonts.ts
import { api } from './client';

const FONTS_BASE = '/api/fonts';

export const fontsApi = {
  // List fonts with filters
  list: async (params?: {
    query?: string;
    category?: FontCategory;
    subset?: string;
    is_variable?: boolean;
    has_italic?: boolean;
    is_featured?: boolean;
    sort_by?: 'popularity' | 'name' | 'date' | 'featured';
    page?: number;
    page_size?: number;
  }): Promise<FontListResponse> => {
    const response = await api.get(FONTS_BASE, { params });
    return response.data;
  },

  // Get featured fonts
  getFeatured: async (): Promise<FontFamilySummary[]> => {
    const response = await api.get(`${FONTS_BASE}/featured`);
    return response.data;
  },

  // Get font categories
  getCategories: async (): Promise<FontCategoryInfo[]> => {
    const response = await api.get(`${FONTS_BASE}/categories`);
    return response.data;
  },

  // Get popular fonts
  getPopular: async (limit = 20, category?: FontCategory): Promise<FontFamilySummary[]> => {
    const response = await api.get(`${FONTS_BASE}/popular`, { 
      params: { limit, category } 
    });
    return response.data;
  },

  // Get font details
  getDetails: async (fontFamilyId: number): Promise<FontFamilyDetail> => {
    const response = await api.get(`${FONTS_BASE}/${fontFamilyId}`);
    return response.data;
  },

  // Get font by name
  getByName: async (familyName: string): Promise<FontFamilyDetail> => {
    const response = await api.get(`${FONTS_BASE}/by-name/${encodeURIComponent(familyName)}`);
    return response.data;
  },

  // Log font usage
  logUsage: async (fontFamilyId: number, data: {
    context: 'FormBuilder' | 'TemplateCreation' | 'Preview' | 'Export' | 'Settings';
    action: 'Selected' | 'Applied' | 'Previewed' | 'Removed' | 'Downloaded';
    font_variant_id?: number;
    context_entity_type?: string;
    context_entity_id?: number;
  }) => {
    await api.post(`${FONTS_BASE}/${fontFamilyId}/usage`, data);
  },

  // Custom font endpoints
  custom: {
    // List company fonts
    list: async (includeGoogleFonts = true): Promise<CompanyFontListResponse> => {
      const response = await api.get(`${FONTS_BASE}/custom`, {
        params: { include_google_fonts: includeGoogleFonts }
      });
      return response.data;
    },

    // Upload custom font
    upload: async (file: File, displayName?: string, category?: FontCategory) => {
      const formData = new FormData();
      formData.append('file', file);
      if (displayName) formData.append('display_name', displayName);
      if (category) formData.append('category', category);

      const response = await api.post(`${FONTS_BASE}/custom`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    },

    // Update display name
    updateName: async (companyFontId: number, displayName: string) => {
      const response = await api.put(`${FONTS_BASE}/custom/${companyFontId}/name`, {
        display_name: displayName
      });
      return response.data;
    },

    // Get font file URL
    getFileUrl: (fontVariantId: number): string => {
      return `${FONTS_BASE}/file/${fontVariantId}`;
    }
  }
};
```

---

## React Hooks

### useFonts Hook

```typescript
// hooks/useFonts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fontsApi } from '../api/fonts';

interface UseFontsOptions {
  query?: string;
  category?: FontCategory;
  page?: number;
  pageSize?: number;
  enabled?: boolean;
}

export function useFonts(options: UseFontsOptions = {}) {
  const { query, category, page = 1, pageSize = 50, enabled = true } = options;

  return useQuery({
    queryKey: ['fonts', { query, category, page, pageSize }],
    queryFn: () => fontsApi.list({ query, category, page, page_size: pageSize }),
    enabled,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useFeaturedFonts() {
  return useQuery({
    queryKey: ['fonts', 'featured'],
    queryFn: () => fontsApi.getFeatured(),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useFontCategories() {
  return useQuery({
    queryKey: ['fonts', 'categories'],
    queryFn: () => fontsApi.getCategories(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
}

export function useFontDetails(fontFamilyId: number | null) {
  return useQuery({
    queryKey: ['fonts', 'details', fontFamilyId],
    queryFn: () => fontsApi.getDetails(fontFamilyId!),
    enabled: fontFamilyId !== null,
    staleTime: 5 * 60 * 1000,
  });
}

export function useCompanyFonts(includeGoogleFonts = true) {
  return useQuery({
    queryKey: ['fonts', 'company', { includeGoogleFonts }],
    queryFn: () => fontsApi.custom.list(includeGoogleFonts),
    staleTime: 5 * 60 * 1000,
  });
}

export function useUploadFont() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ file, displayName, category }: { 
      file: File; 
      displayName?: string; 
      category?: FontCategory;
    }) => fontsApi.custom.upload(file, displayName, category),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fonts', 'company'] });
    },
  });
}

export function useLogFontUsage() {
  return useMutation({
    mutationFn: ({ fontFamilyId, ...data }: { 
      fontFamilyId: number;
      context: 'FormBuilder' | 'TemplateCreation' | 'Preview' | 'Export' | 'Settings';
      action: 'Selected' | 'Applied' | 'Previewed' | 'Removed' | 'Downloaded';
      font_variant_id?: number;
    }) => fontsApi.logUsage(fontFamilyId, data),
  });
}
```

---

## Font Picker Component

```tsx
// components/FontPicker.tsx
import React, { useState, useMemo, useCallback } from 'react';
import { useFonts, useFontCategories, useCompanyFonts, useLogFontUsage } from '../hooks/useFonts';
import { loadGoogleFont } from '../utils/fontLoader';

interface FontPickerProps {
  value: string;
  onChange: (fontFamily: string, fontFamilyId?: number) => void;
  showCustomFonts?: boolean;
  categories?: FontCategory[];
}

export function FontPicker({ 
  value, 
  onChange, 
  showCustomFonts = true,
  categories 
}: FontPickerProps) {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<FontCategory | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const { data: fontCategories } = useFontCategories();
  const { data: companyFonts } = useCompanyFonts(true);
  const { mutate: logUsage } = useLogFontUsage();

  // Filter fonts based on search and category
  const filteredFonts = useMemo(() => {
    if (!companyFonts) return [];
    
    return companyFonts.fonts.filter(font => {
      const matchesSearch = !search || 
        font.display_name.toLowerCase().includes(search.toLowerCase());
      const matchesCategory = !selectedCategory || 
        font.category === selectedCategory;
      const matchesAllowedCategories = !categories || 
        categories.includes(font.category);
      
      return matchesSearch && matchesCategory && matchesAllowedCategories;
    });
  }, [companyFonts, search, selectedCategory, categories]);

  // Group fonts by source
  const groupedFonts = useMemo(() => {
    const custom = filteredFonts.filter(f => f.font_source === 'Custom');
    const google = filteredFonts.filter(f => f.font_source === 'Google');
    return { custom, google };
  }, [filteredFonts]);

  const handleSelect = useCallback((font: CompanyFont) => {
    // Load font for preview
    if (font.font_source === 'Google') {
      loadGoogleFont(font.original_name);
    }
    
    onChange(font.display_name, font.font_family_id);
    
    // Log usage
    logUsage({
      fontFamilyId: font.font_family_id,
      context: 'FormBuilder',
      action: 'Selected'
    });
    
    setIsOpen(false);
  }, [onChange, logUsage]);

  return (
    <div className="font-picker">
      <button 
        className="font-picker-trigger"
        onClick={() => setIsOpen(!isOpen)}
        style={{ fontFamily: value }}
      >
        {value}
        <span className="chevron">▼</span>
      </button>

      {isOpen && (
        <div className="font-picker-dropdown">
          {/* Search */}
          <input
            type="text"
            placeholder="Search fonts..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="font-search"
          />

          {/* Category tabs */}
          <div className="category-tabs">
            <button
              className={!selectedCategory ? 'active' : ''}
              onClick={() => setSelectedCategory(null)}
            >
              All
            </button>
            {fontCategories?.map(cat => (
              <button
                key={cat.category_code}
                className={selectedCategory === cat.category_code ? 'active' : ''}
                onClick={() => setSelectedCategory(cat.category_code)}
              >
                {cat.category_name}
              </button>
            ))}
          </div>

          {/* Custom fonts section */}
          {showCustomFonts && groupedFonts.custom.length > 0 && (
            <div className="font-section">
              <h4>Custom Fonts</h4>
              {groupedFonts.custom.map(font => (
                <FontOption
                  key={font.font_family_id}
                  font={font}
                  selected={font.display_name === value}
                  onSelect={() => handleSelect(font)}
                />
              ))}
            </div>
          )}

          {/* Google fonts section */}
          <div className="font-section">
            <h4>Google Fonts</h4>
            {groupedFonts.google.slice(0, 50).map(font => (
              <FontOption
                key={font.font_family_id}
                font={font}
                selected={font.display_name === value}
                onSelect={() => handleSelect(font)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function FontOption({ 
  font, 
  selected, 
  onSelect 
}: { 
  font: CompanyFont; 
  selected: boolean; 
  onSelect: () => void;
}) {
  // Load font on hover for preview
  const handleMouseEnter = () => {
    if (font.font_source === 'Google') {
      loadGoogleFont(font.original_name);
    }
  };

  return (
    <button
      className={`font-option ${selected ? 'selected' : ''}`}
      onClick={onSelect}
      onMouseEnter={handleMouseEnter}
      style={{ fontFamily: font.original_name }}
    >
      <span className="font-name">{font.display_name}</span>
      {font.font_source === 'Custom' && (
        <span className="font-badge custom">Custom</span>
      )}
      {font.is_variable_font && (
        <span className="font-badge variable">Variable</span>
      )}
    </button>
  );
}
```

---

## Font Weight Slider

```tsx
// components/FontWeightSlider.tsx
import React from 'react';
import { useFontDetails } from '../hooks/useFonts';

interface FontWeightSliderProps {
  fontFamilyId?: number;
  value: number;
  onChange: (weight: number) => void;
}

const WEIGHT_NAMES: Record<number, string> = {
  100: 'Thin',
  200: 'Extra Light',
  300: 'Light',
  400: 'Regular',
  500: 'Medium',
  600: 'Semi Bold',
  700: 'Bold',
  800: 'Extra Bold',
  900: 'Black',
};

export function FontWeightSlider({ fontFamilyId, value, onChange }: FontWeightSliderProps) {
  const { data: fontDetails } = useFontDetails(fontFamilyId ?? null);

  // Get available weights from font details or use standard weights
  const minWeight = fontDetails?.min_weight ?? 100;
  const maxWeight = fontDetails?.max_weight ?? 900;
  const isVariable = fontDetails?.is_variable_font ?? false;

  // For variable fonts, use continuous slider
  // For static fonts, snap to available weights
  const availableWeights = isVariable
    ? null
    : fontDetails?.variants
        .filter(v => !v.is_italic)
        .map(v => v.weight)
        .sort((a, b) => a - b) ?? [400];

  const handleChange = (newValue: number) => {
    if (availableWeights) {
      // Snap to nearest available weight
      const closest = availableWeights.reduce((prev, curr) =>
        Math.abs(curr - newValue) < Math.abs(prev - newValue) ? curr : prev
      );
      onChange(closest);
    } else {
      // Round to nearest 10 for variable fonts
      onChange(Math.round(newValue / 10) * 10);
    }
  };

  return (
    <div className="font-weight-slider">
      <div className="slider-header">
        <label>Weight</label>
        <span className="weight-value">
          {WEIGHT_NAMES[value] ?? value}
        </span>
      </div>
      
      <input
        type="range"
        min={minWeight}
        max={maxWeight}
        step={isVariable ? 10 : 100}
        value={value}
        onChange={(e) => handleChange(Number(e.target.value))}
        className="weight-slider"
      />
      
      {!isVariable && availableWeights && (
        <div className="weight-marks">
          {availableWeights.map(weight => (
            <button
              key={weight}
              className={weight === value ? 'active' : ''}
              onClick={() => onChange(weight)}
              title={WEIGHT_NAMES[weight]}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## Font Loader Utility

```typescript
// utils/fontLoader.ts
const loadedFonts = new Set<string>();

export function loadGoogleFont(fontFamily: string, weights: number[] = [400, 700]) {
  const normalizedName = fontFamily.replace(/\s+/g, '+');
  
  if (loadedFonts.has(normalizedName)) return;
  
  const weightString = weights.join(';');
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = `https://fonts.googleapis.com/css2?family=${normalizedName}:wght@${weightString}&display=swap`;
  
  document.head.appendChild(link);
  loadedFonts.add(normalizedName);
}

export function loadCustomFontFile(fontVariantId: number, fontFamily: string) {
  if (loadedFonts.has(`custom-${fontVariantId}`)) return;
  
  const fontUrl = `/api/fonts/file/${fontVariantId}`;
  
  const fontFace = new FontFace(fontFamily, `url(${fontUrl})`);
  fontFace.load().then((loaded) => {
    document.fonts.add(loaded);
    loadedFonts.add(`custom-${fontVariantId}`);
  });
}
```

---

## CSS for Font Picker

```css
/* styles/font-picker.css */

.font-picker {
  position: relative;
}

.font-picker-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 8px 12px;
  background: var(--input-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.font-picker-trigger:hover {
  border-color: var(--primary-color);
}

.font-picker-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 400px;
  overflow-y: auto;
  background: var(--dropdown-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

.font-search {
  width: 100%;
  padding: 10px 12px;
  border: none;
  border-bottom: 1px solid var(--border-color);
  font-size: 14px;
}

.category-tabs {
  display: flex;
  gap: 4px;
  padding: 8px;
  border-bottom: 1px solid var(--border-color);
  overflow-x: auto;
}

.category-tabs button {
  padding: 4px 8px;
  background: none;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  cursor: pointer;
}

.category-tabs button.active {
  background: var(--primary-color);
  color: white;
}

.font-section {
  padding: 8px;
}

.font-section h4 {
  font-size: 11px;
  text-transform: uppercase;
  color: var(--muted-text);
  margin: 0 0 8px;
}

.font-option {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 8px;
  background: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: left;
}

.font-option:hover {
  background: var(--hover-bg);
}

.font-option.selected {
  background: var(--primary-light);
}

.font-badge {
  margin-left: auto;
  padding: 2px 6px;
  font-size: 10px;
  border-radius: 3px;
}

.font-badge.custom {
  background: #e8f5e9;
  color: #2e7d32;
}

.font-badge.variable {
  background: #e3f2fd;
  color: #1565c0;
}

/* Weight Slider */
.font-weight-slider {
  padding: 12px 0;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.weight-slider {
  width: 100%;
  height: 4px;
  appearance: none;
  background: var(--slider-track);
  border-radius: 2px;
}

.weight-slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  background: var(--primary-color);
  border-radius: 50%;
  cursor: pointer;
}

.weight-marks {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
}

.weight-marks button {
  width: 8px;
  height: 8px;
  padding: 0;
  background: var(--muted-color);
  border: none;
  border-radius: 50%;
  cursor: pointer;
}

.weight-marks button.active {
  background: var(--primary-color);
  width: 10px;
  height: 10px;
}
```

---

## Best Practices

### 1. Font Loading Strategy

- **Lazy load fonts**: Only load fonts when user hovers or selects them
- **Cache loaded fonts**: Track which fonts are already loaded to avoid duplicates
- **Use `font-display: swap`**: Prevent invisible text during font loading

### 2. Performance

- **Paginate font lists**: Limit to 50-100 fonts per request
- **Use virtualized lists**: For large font catalogs, use `react-virtualized` or similar
- **Cache API responses**: Use React Query with appropriate stale times

### 3. Accessibility

- **Keyboard navigation**: Ensure font picker is fully keyboard accessible
- **ARIA labels**: Add proper labels for screen readers
- **Preview text**: Show consistent sample text for all fonts

### 4. Custom Font Handling

- **Validate file size**: Enforce 10MB limit on frontend
- **Show upload progress**: Use a progress indicator for large files
- **Handle duplicates gracefully**: Show message when font already exists

