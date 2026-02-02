import React from 'react';
import { ChevronDown, Minus, Link, Unlink } from 'lucide-react';
import { PropertyColorPicker, PropertyNumberInput } from './inputs';
import { GlobalStyles, StyleOverrides } from '../../types/builder.types';

interface DividerPropertiesSectionProps {
    styleOverrides?: StyleOverrides;
    onStyleOverridesChange: (updates: Partial<StyleOverrides>) => void;
    props?: { width?: string };
    onPropsChange?: (updates: { width?: string }) => void;
    globalStyles: GlobalStyles;
}

const ChainIndicator: React.FC<{
    isOverridden: boolean;
    onReset: () => void;
    label: string;
}> = ({ isOverridden, onReset, label }) => (
    <button
        type="button"
        onClick={(e) => {
            e.stopPropagation();
            if (isOverridden) onReset();
        }}
        className={`flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] transition-colors ${
            isOverridden
                ? 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 hover:bg-amber-100 dark:hover:bg-amber-900/30 cursor-pointer'
                : 'text-gray-400 bg-gray-50 dark:bg-gray-800 cursor-default'
        }`}
        title={isOverridden ? `Custom override - click to reset to global ${label}` : `Using global ${label}`}
    >
        {isOverridden ? <Unlink size={10} /> : <Link size={10} />}
        <span>{isOverridden ? 'override' : 'global'}</span>
    </button>
);

/**
 * DividerPropertiesSection - Properties specific to Divider component
 *
 * Includes:
 * - Border color (styleOverrides.dividerBorderColor)
 * - Border width (styleOverrides.dividerBorderWidth)
 * - Length override (props.width) which falls back to GlobalStyles.dividerWidth
 */
export const DividerPropertiesSection: React.FC<DividerPropertiesSectionProps> = ({
    styleOverrides,
    onStyleOverridesChange,
    props,
    onPropsChange,
    globalStyles,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(true);

    const borderColor = styleOverrides?.dividerBorderColor || '#E5E7EB';
    const borderWidth = styleOverrides?.dividerBorderWidth || 1;
    const globalLength = globalStyles.dividerWidth || '100%';
    const isLengthOverridden = typeof props?.width === 'string' && props.width.trim().length > 0;
    const length = (props?.width && props.width.trim().length > 0) ? props.width : globalLength;
    const isBorderColorOverridden = styleOverrides ? ('dividerBorderColor' in styleOverrides) : false;
    const isBorderWidthOverridden = styleOverrides ? ('dividerBorderWidth' in styleOverrides) : false;

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Minus size={14} className="text-gray-500" />
                    <span>Divider Settings</span>
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-4">
                    {/* Border Color */}
                    <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                            <PropertyColorPicker
                                label="Border Color"
                                value={borderColor}
                                onChange={(value) => onStyleOverridesChange({ dividerBorderColor: value })}
                                helpText="Color of the divider line"
                            />
                        </div>
                        <ChainIndicator
                            isOverridden={isBorderColorOverridden}
                            onReset={() => onStyleOverridesChange({ dividerBorderColor: undefined })}
                            label="border color"
                        />
                    </div>

                    {/* Border Width */}
                    <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                            <PropertyNumberInput
                                label="Border Width"
                                value={borderWidth}
                                onChange={(value) => onStyleOverridesChange({ dividerBorderWidth: value })}
                                min={1}
                                max={10}
                                helpText="Thickness of the divider line (1-10px)"
                            />
                        </div>
                        <ChainIndicator
                            isOverridden={isBorderWidthOverridden}
                            onReset={() => onStyleOverridesChange({ dividerBorderWidth: undefined })}
                            label="border width"
                        />
                    </div>

                    {/* Length (Width) */}
                    <div>
                        <div className="flex items-center justify-between mb-1">
                            <label className="block text-xs font-medium text-gray-600 dark:text-gray-400">
                                Length
                            </label>
                            <ChainIndicator
                                isOverridden={isLengthOverridden}
                                onReset={() => onPropsChange?.({ width: undefined })}
                                label="length"
                            />
                        </div>
                        <div className="flex items-center gap-2">
                            <input
                                type="text"
                                value={length}
                                onChange={(e) => onPropsChange?.({ width: e.target.value })}
                                placeholder={globalLength}
                                className="flex-1 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md 
                                    bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                                    focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                            Uses Global length by default ({globalLength}). Set a value here to override (e.g., 100%, 200px).
                        </p>
                    </div>

                    {/* Preview */}
                    <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                        <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                            Preview
                        </div>
                        <div className="w-full py-2">
                            <hr 
                                style={{
                                    borderTopWidth: `${borderWidth}px`,
                                    borderTopColor: borderColor,
                                    borderTopStyle: 'solid',
                                    width: length,
                                    margin: '0',
                                }}
                            />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DividerPropertiesSection;

