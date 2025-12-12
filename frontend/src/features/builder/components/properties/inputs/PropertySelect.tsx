import React from 'react';
import { ChevronDown } from 'lucide-react';

interface PropertySelectProps {
    label: string;
    value: string;
    onChange: (value: string) => void;
    options: Array<{ value: string; label: string }>;
    helpText?: string;
    disabled?: boolean;
}

export const PropertySelect: React.FC<PropertySelectProps> = ({
    label,
    value,
    onChange,
    options,
    helpText,
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
                    onChange={(e) => onChange(e.target.value)}
                    disabled={disabled}
                    className="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md 
                        bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                        focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                        disabled:bg-gray-100 dark:disabled:bg-gray-700 disabled:cursor-not-allowed
                        appearance-none cursor-pointer pr-8"
                >
                    {options.map((option) => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}
                </select>
                <ChevronDown 
                    size={14} 
                    className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" 
                />
            </div>
            {helpText && (
                <p className="text-xs text-gray-500 dark:text-gray-400">{helpText}</p>
            )}
        </div>
    );
};

