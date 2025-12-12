import React from 'react';
import { Palette, Type, Columns, Tag, MessageSquare, Focus, ArrowUpDown, ArrowLeftRight } from 'lucide-react';
import { PropertyNumberInput, PropertyColorPicker, PropertySelect, TypographyCard } from './inputs';
import { 
    GlobalStyles, 
    LayoutType, 
    FontStyleType,
    FontWeightValue,
} from '../../types/builder.types';

interface GlobalStylesPanelProps {
    globalStyles: GlobalStyles;
    onGlobalStylesChange: (updates: Partial<GlobalStyles>) => void;
}

const LAYOUT_OPTIONS = [
    { value: 'vertical', label: 'Vertical (Label Above)' },
    { value: 'horizontal', label: 'Horizontal (Label Left)' },
];

/**
 * Inline spacing control shown between Typography cards
 */
const SpacingDivider: React.FC<{
    label: string;
    value: number;
    onChange: (value: number) => void;
    baseSpacing: number;
    icon?: 'vertical' | 'horizontal';
}> = ({ label, value, onChange, baseSpacing, icon = 'vertical' }) => (
    <div className="flex items-center gap-2 py-2 px-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-dashed border-gray-200 dark:border-gray-700">
        {icon === 'vertical' ? (
            <ArrowUpDown size={12} className="text-gray-400" />
        ) : (
            <ArrowLeftRight size={12} className="text-gray-400" />
        )}
        <span className="text-[10px] text-gray-500 dark:text-gray-400 flex-1">{label}</span>
        <div className="flex items-center gap-1">
            <input
                type="range"
                min={0}
                max={4}
                step={0.5}
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
                className="w-16 h-1 accent-blue-500"
            />
            <span className="text-[10px] font-mono text-gray-600 dark:text-gray-300 w-8 text-right">
                {Math.round(value * baseSpacing)}px
            </span>
        </div>
    </div>
);

export const GlobalStylesPanel: React.FC<GlobalStylesPanelProps> = ({
    globalStyles,
    onGlobalStylesChange,
}) => {
    return (
        <>
            {/* Header - Fixed at top */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 flex-shrink-0">
                <div className="flex items-center gap-2">
                    <Palette className="text-blue-500" size={18} />
                    <h3 className="font-semibold text-gray-800 dark:text-gray-200">Global Styles</h3>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    These settings apply to all components. Individual components can override these values.
                </p>
            </div>

            {/* Scrollable Content - using scroll to always reserve scrollbar space */}
            <div className="flex-1 overflow-y-scroll overflow-x-hidden">
            
            {/* Focus Color Section - At the top for prominence */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2 mb-2">
                    <Focus size={14} className="text-blue-500" />
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Focus Color</h4>
                </div>
                <p className="text-[10px] text-gray-500 dark:text-gray-400 mb-3">
                    Highlight color for focused inputs and interactive elements.
                </p>
                <PropertyColorPicker
                    label="Primary"
                    value={globalStyles.primaryColor}
                    onChange={(value) => onGlobalStylesChange({ primaryColor: value })}
                />
            </div>

            {/* Typography Section - Ordered to match component layout */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2 mb-4">
                    <Type size={14} className="text-gray-400" />
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Typography & Spacing</h4>
                </div>
                <p className="text-[10px] text-gray-500 dark:text-gray-400 mb-4">
                    Ordered to match component layout. Spacing controls show distance between elements.
                </p>
                
                <div className="space-y-2">
                    {/* 1. Label Text Card (Top - matches label position) */}
                    <TypographyCard
                        title="Label Text"
                        icon={Tag}
                        iconColor="text-green-500"
                        fontFamily={globalStyles.labelFontFamily}
                        fontSize={globalStyles.labelFontSize}
                        fontWeight={globalStyles.labelFontWeight}
                        fontStyle={globalStyles.labelFontStyle}
                        color={globalStyles.labelColor}
                        backgroundColor={globalStyles.labelBackgroundColor}
                        borderColor={globalStyles.labelBorderColor}
                        borderWidth={globalStyles.labelBorderWidth}
                        borderRadius={globalStyles.labelBorderRadius}
                        showBorderOptions={true}
                        onFontFamilyChange={(labelFontFamily) => onGlobalStylesChange({ labelFontFamily })}
                        onFontSizeChange={(labelFontSize) => onGlobalStylesChange({ labelFontSize })}
                        onFontWeightChange={(labelFontWeight) => onGlobalStylesChange({ labelFontWeight })}
                        onFontStyleChange={(labelFontStyle) => onGlobalStylesChange({ labelFontStyle })}
                        onColorChange={(labelColor) => onGlobalStylesChange({ labelColor })}
                        onBackgroundColorChange={(labelBackgroundColor) => onGlobalStylesChange({ labelBackgroundColor })}
                        onBorderColorChange={(labelBorderColor) => onGlobalStylesChange({ labelBorderColor })}
                        onBorderWidthChange={(labelBorderWidth) => onGlobalStylesChange({ labelBorderWidth })}
                        onBorderRadiusChange={(labelBorderRadius) => onGlobalStylesChange({ labelBorderRadius })}
                        minSize={10}
                        maxSize={28}
                    />

                    {/* Spacing: Label to Input */}
                    <SpacingDivider
                        label={globalStyles.defaultLayout === 'horizontal' ? 'Label → Input (horizontal)' : 'Label ↓ Input (vertical)'}
                        value={globalStyles.labelGap}
                        onChange={(value) => onGlobalStylesChange({ labelGap: value })}
                        baseSpacing={globalStyles.baseSpacing}
                        icon={globalStyles.defaultLayout === 'horizontal' ? 'horizontal' : 'vertical'}
                    />

                    {/* 2. Input Text Card (Middle - matches input position) */}
                    <TypographyCard
                        title="Input Text"
                        icon={Type}
                        iconColor="text-blue-500"
                        fontFamily={globalStyles.fontFamily}
                        fontSize={globalStyles.fontSize}
                        fontWeight={globalStyles.fontWeight}
                        fontStyle={globalStyles.fontStyle}
                        color={globalStyles.textColor}
                        backgroundColor={globalStyles.textBackgroundColor}
                        borderColor={globalStyles.textBorderColor}
                        borderWidth={globalStyles.textBorderWidth}
                        borderRadius={globalStyles.textBorderRadius}
                        showBorderOptions={true}
                        onFontFamilyChange={(fontFamily) => onGlobalStylesChange({ fontFamily })}
                        onFontSizeChange={(fontSize) => onGlobalStylesChange({ fontSize })}
                        onFontWeightChange={(fontWeight) => onGlobalStylesChange({ fontWeight })}
                        onFontStyleChange={(fontStyle) => onGlobalStylesChange({ fontStyle })}
                        onColorChange={(textColor) => onGlobalStylesChange({ textColor })}
                        onBackgroundColorChange={(textBackgroundColor) => onGlobalStylesChange({ textBackgroundColor })}
                        onBorderColorChange={(textBorderColor) => onGlobalStylesChange({ textBorderColor })}
                        onBorderWidthChange={(textBorderWidth) => onGlobalStylesChange({ textBorderWidth })}
                        onBorderRadiusChange={(textBorderRadius) => onGlobalStylesChange({ textBorderRadius })}
                        minSize={10}
                        maxSize={32}
                        // Include Input Height in this card
                        inputHeight={globalStyles.inputHeight}
                        onInputHeightChange={(inputHeight) => onGlobalStylesChange({ inputHeight })}
                    />

                    {/* Spacing: Input to Help */}
                    <SpacingDivider
                        label="Input ↓ Help text"
                        value={globalStyles.inputHelpGap}
                        onChange={(value) => onGlobalStylesChange({ inputHelpGap: value })}
                        baseSpacing={globalStyles.baseSpacing}
                        icon="vertical"
                    />

                    {/* 3. Help & Validation Text Card (Bottom - matches help text position) */}
                    <TypographyCard
                        title="Help & Validation"
                        icon={MessageSquare}
                        iconColor="text-orange-500"
                        fontFamily={globalStyles.helpTextFontFamily}
                        fontSize={globalStyles.helpTextFontSize}
                        fontWeight={globalStyles.helpTextFontWeight}
                        fontStyle={globalStyles.helpTextFontStyle}
                        color={globalStyles.helpTextColor}
                        backgroundColor={globalStyles.helpTextBackgroundColor}
                        borderColor={globalStyles.helpTextBorderColor}
                        borderWidth={globalStyles.helpTextBorderWidth}
                        borderRadius={globalStyles.helpTextBorderRadius}
                        showBorderOptions={true}
                        onFontFamilyChange={(helpTextFontFamily) => onGlobalStylesChange({ helpTextFontFamily })}
                        onFontSizeChange={(helpTextFontSize) => onGlobalStylesChange({ helpTextFontSize })}
                        onFontWeightChange={(helpTextFontWeight) => onGlobalStylesChange({ helpTextFontWeight })}
                        onFontStyleChange={(helpTextFontStyle) => onGlobalStylesChange({ helpTextFontStyle })}
                        onColorChange={(helpTextColor) => onGlobalStylesChange({ helpTextColor })}
                        onBackgroundColorChange={(helpTextBackgroundColor) => onGlobalStylesChange({ helpTextBackgroundColor })}
                        onBorderColorChange={(helpTextBorderColor) => onGlobalStylesChange({ helpTextBorderColor })}
                        onBorderWidthChange={(helpTextBorderWidth) => onGlobalStylesChange({ helpTextBorderWidth })}
                        onBorderRadiusChange={(helpTextBorderRadius) => onGlobalStylesChange({ helpTextBorderRadius })}
                        minSize={8}
                        maxSize={20}
                    />
                </div>
            </div>

            {/* Layout Section */}
            <div className="p-4">
                <div className="flex items-center gap-2 mb-4">
                    <Columns size={14} className="text-gray-400" />
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Layout</h4>
                </div>
                
                <PropertySelect
                    label="Default Layout"
                    value={globalStyles.defaultLayout}
                    onChange={(value) => onGlobalStylesChange({ defaultLayout: value as LayoutType })}
                    options={LAYOUT_OPTIONS}
                    helpText="Default label position for new components"
                />
            </div>
            </div>
        </>
    );
};

