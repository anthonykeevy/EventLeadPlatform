import React from 'react';
import { MapPin, Search, Sparkles } from 'lucide-react';
import { ComputedFieldStyles } from '../../utils/styleUtils';

interface AddressFieldProps {
    label?: string;
    placeholder?: string;
    required?: boolean;
    helpText?: string;
    enableAutocomplete?: boolean;
    fieldStyles?: ComputedFieldStyles;
}

/**
 * Address Field Component (Placeholder)
 * 
 * This is a placeholder for the future address autocomplete feature.
 * Currently displays as a text input with a "Coming Soon" badge.
 * 
 * Future features:
 * - Google Places autocomplete integration
 * - Address decomposition into subfields
 * - Address validation
 */
export const AddressField: React.FC<AddressFieldProps> = ({
    label = 'Address',
    placeholder = 'Start typing your address...',
    required = false,
    helpText,
    enableAutocomplete = true,
    fieldStyles,
}) => {
    const labelStyle = fieldStyles?.labelStyle || {};
    const inputStyle = fieldStyles?.inputStyle || {};
    const helpTextStyle = fieldStyles?.helpTextStyle || {};

    return (
        <div
            className="border border-dashed border-gray-300 rounded-lg p-3 bg-white hover:border-blue-400 
                transition-colors group relative"
        >
            {/* Drag Handle */}
            <div className="absolute -left-1 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
                <MapPin size={14} className="text-gray-400" />
            </div>

            {/* Label */}
            <div className="mb-2">
                <label 
                    className="text-sm font-medium text-gray-700 flex items-center gap-1"
                    style={labelStyle}
                >
                    {label}
                    {required && <span className="text-red-500">*</span>}
                </label>
            </div>

            {/* Input with search icon */}
            <div className="relative">
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                    <Search size={16} />
                </div>
                <input
                    type="text"
                    disabled
                    placeholder={placeholder}
                    className="w-full pl-10 pr-4 py-2 border rounded-md text-sm
                        bg-gray-50 text-gray-500 cursor-not-allowed"
                    style={{
                        ...inputStyle,
                        backgroundColor: '#F9FAFB',
                    }}
                />
            </div>

            {/* Help text or Coming Soon message */}
            <div className="mt-2 flex items-center justify-between">
                <p 
                    className="text-xs text-gray-500 flex items-center gap-1"
                    style={helpTextStyle}
                >
                    <MapPin size={10} />
                    {helpText || 'Enter your full address'}
                </p>
                
                {enableAutocomplete && (
                    <div className="flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full">
                        <Sparkles size={10} />
                        <span>Autocomplete Coming Soon</span>
                    </div>
                )}
            </div>

            {/* Component type badge */}
            <div className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="text-[9px] bg-teal-100 text-teal-600 px-1.5 py-0.5 rounded font-medium">
                    ADDRESS
                </span>
            </div>
        </div>
    );
};

export default AddressField;

