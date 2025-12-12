import React from 'react';

interface PropertyTextInputProps {
    label: string;
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    helpText?: string;
    disabled?: boolean;
}

export const PropertyTextInput: React.FC<PropertyTextInputProps> = ({
    label,
    value,
    onChange,
    placeholder = '',
    helpText,
    disabled = false,
}) => {
    return (
        <div className="space-y-1">
            <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                {label}
            </label>
            <input
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder}
                disabled={disabled}
                className="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md 
                    bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                    focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                    disabled:bg-gray-100 dark:disabled:bg-gray-700 disabled:cursor-not-allowed
                    placeholder:text-gray-400 dark:placeholder:text-gray-500"
            />
            {helpText && (
                <p className="text-xs text-gray-500 dark:text-gray-400">{helpText}</p>
            )}
        </div>
    );
};

