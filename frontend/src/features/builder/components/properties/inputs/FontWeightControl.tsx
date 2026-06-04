/**
 * FontWeightControl - Story 3.5
 * 
 * Adaptive font weight control that uses:
 * - Continuous slider for variable fonts (100-900)
 * - Dropdown for static fonts (only available weights)
 * 
 * Uses useFontDetails to fetch weight information from the API.
 */

import React, { useMemo } from 'react';
import { useFontDetailsByName } from '../../../hooks/useFonts';
import { WEIGHT_LABELS, getWeightLabel } from '../../../api/fontTypes';

interface FontWeightControlProps {
    label: string;
    value: number | string;
    onChange: (weight: number) => void;
    fontFamily?: string | null;  // Font family name to look up details
    disabled?: boolean;
}

/**
 * Font weight control that adapts based on font type
 */
export const FontWeightControl: React.FC<FontWeightControlProps> = ({
    label,
    value,
    onChange,
    fontFamily,
    disabled = false,
}) => {
    const safeFontFamily = (fontFamily ?? '').trim();
    const numericValue =
        typeof value === 'number' && Number.isFinite(value)
            ? value
            : parseInt(String(value ?? ''), 10) || 400;

    // Fetch font details to determine if variable and get available weights
    const { data: fontDetails, isLoading } = useFontDetailsByName(safeFontFamily);

    // Determine if font is variable
    const isVariable = fontDetails?.is_variable_font ?? false;
    const minWeight = fontDetails?.min_weight ?? 100;
    const maxWeight = fontDetails?.max_weight ?? 900;

    // Get available weights for static fonts
    const availableWeights = useMemo(() => {
        const variants = fontDetails?.variants;
        if (!Array.isArray(variants) || variants.length === 0) {
            return [400];
        }

        // Extract unique weights from non-italic variants
        const weights = variants
            .filter(v => !v.is_italic)
            .map(v => v.weight)
            .filter((w): w is number => typeof w === 'number' && Number.isFinite(w))
            .filter((w, i, arr) => arr.indexOf(w) === i)
            .sort((a, b) => a - b);

        return weights.length > 0 ? weights : [400];
    }, [fontDetails]);

    // Ensure current value is valid for static fonts
    const effectiveValue = useMemo(() => {
        if (isVariable) return numericValue;
        
        // For static fonts, snap to nearest available weight
        if (!availableWeights.includes(numericValue)) {
            return availableWeights.reduce((prev, curr) =>
                Math.abs(curr - numericValue) < Math.abs(prev - numericValue) ? curr : prev
            );
        }
        return numericValue;
    }, [numericValue, isVariable, availableWeights]);

    if (!safeFontFamily) {
        return (
            <SimpleWeightSelect
                label={label}
                value={numericValue}
                onChange={onChange}
                disabled={disabled}
            />
        );
    }

    // Handle slider change for variable fonts
    const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = parseInt(e.target.value, 10);
        // Round to nearest 10 for cleaner values
        onChange(Math.round(newValue / 10) * 10);
    };

    // Handle dropdown change for static fonts
    const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        onChange(parseInt(e.target.value, 10));
    };

    // Loading state
    if (isLoading) {
        return (
            <div className="space-y-1">
                <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                    {label}
                </label>
                <div className="h-8 bg-gray-100 dark:bg-gray-700 rounded animate-pulse" />
            </div>
        );
    }

    // Variable font: Show slider
    if (isVariable) {
        return (
            <div className="space-y-1">
                <div className="flex items-center justify-between">
                    <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                        {label}
                    </label>
                    <span className="text-xs font-medium text-gray-900 dark:text-gray-100">
                        {getWeightLabel(effectiveValue)}
                    </span>
                </div>
                
                <div className="relative">
                    <input
                        type="range"
                        min={minWeight}
                        max={maxWeight}
                        step={10}
                        value={effectiveValue}
                        onChange={handleSliderChange}
                        disabled={disabled}
                        className="w-full h-1.5 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                    
                    {/* Weight markers */}
                    <div className="flex justify-between mt-1 px-0.5">
                        {[100, 400, 700, 900].filter(w => w >= minWeight && w <= maxWeight).map(w => (
                            <button
                                key={w}
                                type="button"
                                onClick={() => onChange(w)}
                                disabled={disabled}
                                className={`w-1.5 h-1.5 rounded-full transition-colors ${
                                    effectiveValue === w 
                                        ? 'bg-blue-500' 
                                        : 'bg-gray-300 dark:bg-gray-600 hover:bg-gray-400'
                                }`}
                                title={getWeightLabel(w)}
                            />
                        ))}
                    </div>
                </div>
                
                <p className="text-[10px] text-gray-500 dark:text-gray-400">
                    Variable font: {minWeight} - {maxWeight}
                </p>
            </div>
        );
    }

    // Static font: Show dropdown
    return (
        <div className="space-y-1">
            <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                {label}
            </label>
            
            <div className="relative">
                <select
                    value={effectiveValue}
                    onChange={handleSelectChange}
                    disabled={disabled}
                    className="w-full px-2 py-1.5 pr-8 text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed appearance-none"
                >
                    {availableWeights.map(weight => (
                        <option key={weight} value={weight}>
                            {WEIGHT_LABELS[weight] || `Weight ${weight}`} ({weight})
                        </option>
                    ))}
                </select>
                
                {/* Dropdown arrow */}
                <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </div>
            </div>
            
            {availableWeights.length === 1 && (
                <p className="text-[10px] text-gray-500 dark:text-gray-400">
                    This font only has one weight
                </p>
            )}
        </div>
    );
};

/**
 * Simplified weight dropdown when font details aren't needed
 * Uses standard weight options (100-900)
 */
export const SimpleWeightSelect: React.FC<{
    label: string;
    value: number;
    onChange: (weight: number) => void;
    availableWeights?: number[];
    disabled?: boolean;
}> = ({
    label,
    value,
    onChange,
    availableWeights = [100, 200, 300, 400, 500, 600, 700, 800, 900],
    disabled = false,
}) => {
    return (
        <div className="space-y-1">
            <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                {label}
            </label>
            
            <div className="relative">
                <select
                    value={value}
                    onChange={(e) => onChange(parseInt(e.target.value, 10))}
                    disabled={disabled}
                    className="w-full px-2 py-1.5 pr-8 text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed appearance-none"
                >
                    {availableWeights.map(weight => (
                        <option key={weight} value={weight}>
                            {WEIGHT_LABELS[weight] || `Weight ${weight}`} ({weight})
                        </option>
                    ))}
                </select>
                
                <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </div>
            </div>
        </div>
    );
};

export default FontWeightControl;

