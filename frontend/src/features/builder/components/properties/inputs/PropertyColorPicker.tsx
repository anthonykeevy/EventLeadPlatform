import React, { useState, useRef, useEffect } from 'react';
import { Pipette } from 'lucide-react';

interface PropertyColorPickerProps {
    label: string;
    value: string;
    onChange: (value: string) => void;
    helpText?: string;
    disabled?: boolean;
}

// Common colors for quick selection
const PRESET_COLORS = [
    '#000000', '#FFFFFF', '#1F2937', '#374151', '#6B7280', '#9CA3AF',
    '#DC2626', '#EA580C', '#F59E0B', '#10B981', '#0EA5E9', '#6366F1',
    '#8B5CF6', '#EC4899', '#0055FF', '#059669', '#0284C7', '#7C3AED',
];

export const PropertyColorPicker: React.FC<PropertyColorPickerProps> = ({
    label,
    value,
    onChange,
    helpText,
    disabled = false,
}) => {
    const [showPicker, setShowPicker] = useState(false);
    const pickerRef = useRef<HTMLDivElement>(null);

    // Close picker when clicking outside
    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (pickerRef.current && !pickerRef.current.contains(e.target as Node)) {
                setShowPicker(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <div className="space-y-1" ref={pickerRef}>
            <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                {label}
            </label>
            
            <div className="flex items-center gap-2">
                {/* Color Swatch Button - Larger for better visibility */}
                <button
                    type="button"
                    onClick={() => !disabled && setShowPicker(!showPicker)}
                    disabled={disabled}
                    className="w-10 h-8 rounded-md border-2 border-gray-300 dark:border-gray-600 
                        shadow-sm cursor-pointer disabled:cursor-not-allowed disabled:opacity-50
                        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1
                        flex-shrink-0"
                    style={{ backgroundColor: value }}
                    title={value}
                />

                {/* Hex Input - Fixed width for 7-char codes */}
                <input
                    type="text"
                    value={value}
                    onChange={(e) => {
                        const val = e.target.value;
                        // Allow typing, validate on blur or if it looks like a valid hex
                        if (/^#[0-9A-Fa-f]{0,6}$/.test(val) || val === '') {
                            onChange(val);
                        }
                    }}
                    disabled={disabled}
                    placeholder="#000000"
                    className="w-20 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md 
                        bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-mono
                        focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                        disabled:bg-gray-100 dark:disabled:bg-gray-700 disabled:cursor-not-allowed
                        flex-shrink-0"
                />

                {/* Native Color Picker */}
                <label className="p-1.5 border border-gray-300 dark:border-gray-600 rounded-md 
                    bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700
                    cursor-pointer transition-colors flex-shrink-0">
                    <Pipette size={14} className="text-gray-500" />
                    <input
                        type="color"
                        value={value}
                        onChange={(e) => onChange(e.target.value)}
                        disabled={disabled}
                        className="sr-only"
                    />
                </label>
            </div>

            {/* Preset Colors Dropdown */}
            {showPicker && (
                <div className="absolute z-50 mt-1 p-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 
                    rounded-lg shadow-lg">
                    <div className="grid grid-cols-6 gap-1">
                        {PRESET_COLORS.map((color) => (
                            <button
                                key={color}
                                type="button"
                                onClick={() => {
                                    onChange(color);
                                    setShowPicker(false);
                                }}
                                className={`w-6 h-6 rounded border transition-transform hover:scale-110
                                    ${value === color ? 'ring-2 ring-blue-500 ring-offset-1' : 'border-gray-300 dark:border-gray-600'}`}
                                style={{ backgroundColor: color }}
                                title={color}
                            />
                        ))}
                    </div>
                </div>
            )}

            {helpText && (
                <p className="text-xs text-gray-500 dark:text-gray-400">{helpText}</p>
            )}
        </div>
    );
};

