import React from 'react';
import { Minus, Plus } from 'lucide-react';

interface PropertyNumberInputProps {
    label: string;
    value: number;
    onChange: (value: number) => void;
    min?: number;
    max?: number;
    step?: number;
    unit?: string;
    helpText?: string;
    disabled?: boolean;
}

export const PropertyNumberInput: React.FC<PropertyNumberInputProps> = ({
    label,
    value,
    onChange,
    min = 0,
    max = 999,
    step = 1,
    unit = '',
    helpText,
    disabled = false,
}) => {
    const handleIncrement = () => {
        const newValue = Math.min(max, value + step);
        onChange(newValue);
    };

    const handleDecrement = () => {
        const newValue = Math.max(min, value - step);
        onChange(newValue);
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = parseFloat(e.target.value) || 0;
        onChange(Math.min(max, Math.max(min, newValue)));
    };

    return (
        <div className="space-y-1">
            <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                {label}
            </label>
            <div className="flex items-center gap-1">
                <button
                    type="button"
                    onClick={handleDecrement}
                    disabled={disabled || value <= min}
                    className="p-1.5 border border-gray-300 dark:border-gray-600 rounded-md 
                        bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700
                        disabled:opacity-50 disabled:cursor-not-allowed
                        transition-colors"
                >
                    <Minus size={12} className="text-gray-500" />
                </button>
                
                <div className="relative flex-1">
                    <input
                        type="number"
                        value={value}
                        onChange={handleChange}
                        min={min}
                        max={max}
                        step={step}
                        disabled={disabled}
                        className="w-full px-2 py-1.5 text-sm text-center border border-gray-300 dark:border-gray-600 rounded-md 
                            bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                            focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                            disabled:bg-gray-100 dark:disabled:bg-gray-700 disabled:cursor-not-allowed
                            [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    />
                    {unit && (
                        <span className="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">
                            {unit}
                        </span>
                    )}
                </div>

                <button
                    type="button"
                    onClick={handleIncrement}
                    disabled={disabled || value >= max}
                    className="p-1.5 border border-gray-300 dark:border-gray-600 rounded-md 
                        bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700
                        disabled:opacity-50 disabled:cursor-not-allowed
                        transition-colors"
                >
                    <Plus size={12} className="text-gray-500" />
                </button>
            </div>
            {helpText && (
                <p className="text-xs text-gray-500 dark:text-gray-400">{helpText}</p>
            )}
        </div>
    );
};

