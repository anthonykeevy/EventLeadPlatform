import React from 'react';

interface PropertyToggleProps {
    label: React.ReactNode;
    checked: boolean;
    onChange: (checked: boolean) => void;
    helpText?: string;
    disabled?: boolean;
}

export const PropertyToggle: React.FC<PropertyToggleProps> = ({
    label,
    checked,
    onChange,
    helpText,
    disabled = false,
}) => {
    return (
        <div className="flex items-center justify-between py-1">
            <div className="flex flex-col">
                <span className="text-xs font-medium text-gray-600 dark:text-gray-400">
                    {label}
                </span>
                {helpText && (
                    <span className="text-xs text-gray-400 dark:text-gray-500">{helpText}</span>
                )}
            </div>
            <button
                type="button"
                role="switch"
                aria-checked={checked}
                disabled={disabled}
                onClick={() => onChange(!checked)}
                className={`
                    relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent 
                    transition-colors duration-200 ease-in-out 
                    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                    disabled:opacity-50 disabled:cursor-not-allowed
                    ${checked ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'}
                `}
            >
                <span
                    className={`
                        pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 
                        transition duration-200 ease-in-out
                        ${checked ? 'translate-x-4' : 'translate-x-0'}
                    `}
                />
            </button>
        </div>
    );
};

