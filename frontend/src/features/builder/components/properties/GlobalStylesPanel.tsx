import React from 'react';
import { Palette, Type, Tag, MessageSquare, Focus, Minus, Grid3x3 } from 'lucide-react';
import { PropertyNumberInput, PropertyColorPicker, PropertySelect, TypographyCard } from './inputs';
import { 
    GlobalStyles, 
    ObjectLayoutType,
    DEFAULT_GLOBAL_STYLES,
} from '../../types/builder.types';

interface GlobalStylesPanelProps {
    globalStyles: GlobalStyles;
    onGlobalStylesChange: (updates: Partial<GlobalStyles>) => void;
}

const OBJECT_LAYOUT_OPTIONS = [
    { value: 'vertical', label: 'Vertical' },
    { value: 'horizontal', label: 'Horizontal' },
];

/** Props shared by all GlobalStyles section components */
export interface GlobalStylesSectionProps {
    globalStyles: GlobalStyles;
    onGlobalStylesChange: (updates: Partial<GlobalStyles>) => void;
}

/**
 * Focus Color section - standalone for accordion use
 */
export const FocusColorSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="p-4">
        <p className="text-[10px] text-gray-500 dark:text-gray-400 mb-3">
            Highlight color for focused inputs and interactive elements.
        </p>
        <PropertyColorPicker
            label="Primary"
            value={globalStyles.primaryColor}
            onChange={(value) => onGlobalStylesChange({ primaryColor: value })}
        />
    </div>
);

/**
 * Typography & Spacing section - standalone for accordion use
 * Note: Label↔Input and Input↓Help gaps are now controlled by Grid Layout Defaults (Default Row Gap)
 */
export const TypographySpacingSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="p-4 space-y-2">
        <p className="text-[10px] text-gray-500 dark:text-gray-400 mb-4">
            Ordered to match component layout. Spacing controls show distance between elements.
        </p>
        <TypographyCard title="Label Text" icon={Tag} iconColor="text-green-500"
            fontFamily={globalStyles.labelFontFamily} fontSize={globalStyles.labelFontSize}
            fontWeight={globalStyles.labelFontWeight} fontStyle={globalStyles.labelFontStyle}
            color={globalStyles.labelColor} backgroundColor={globalStyles.labelBackgroundColor}
            hasBorder={globalStyles.labelHasBorder} borderColor={globalStyles.labelBorderColor}
            borderWidth={globalStyles.labelBorderWidth} borderRadius={globalStyles.labelBorderRadius}
            showBorderOptions={true}
            onFontFamilyChange={(v) => onGlobalStylesChange({ labelFontFamily: v })}
            onFontSizeChange={(v) => onGlobalStylesChange({ labelFontSize: v })}
            onFontWeightChange={(v) => onGlobalStylesChange({ labelFontWeight: v })}
            onFontStyleChange={(v) => onGlobalStylesChange({ labelFontStyle: v })}
            onColorChange={(v) => onGlobalStylesChange({ labelColor: v })}
            onBackgroundColorChange={(v) => onGlobalStylesChange({ labelBackgroundColor: v })}
            onHasBorderChange={(v) => onGlobalStylesChange({ labelHasBorder: v })}
            onBorderColorChange={(v) => onGlobalStylesChange({ labelBorderColor: v })}
            onBorderWidthChange={(v) => onGlobalStylesChange({ labelBorderWidth: v })}
            onBorderRadiusChange={(v) => onGlobalStylesChange({ labelBorderRadius: v })}
            minSize={10} maxSize={28} />
        <TypographyCard title="Input Text" icon={Type} iconColor="text-blue-500"
            fontFamily={globalStyles.fontFamily} fontSize={globalStyles.fontSize}
            fontWeight={globalStyles.fontWeight} fontStyle={globalStyles.fontStyle}
            color={globalStyles.textColor} backgroundColor={globalStyles.textBackgroundColor}
            hasBorder={globalStyles.textHasBorder} borderColor={globalStyles.textBorderColor}
            borderWidth={globalStyles.textBorderWidth} borderRadius={globalStyles.textBorderRadius}
            showBorderOptions={true}
            onFontFamilyChange={(v) => onGlobalStylesChange({ fontFamily: v })}
            onFontSizeChange={(v) => onGlobalStylesChange({ fontSize: v })}
            onFontWeightChange={(v) => onGlobalStylesChange({ fontWeight: v })}
            onFontStyleChange={(v) => onGlobalStylesChange({ fontStyle: v })}
            onColorChange={(v) => onGlobalStylesChange({ textColor: v })}
            onBackgroundColorChange={(v) => onGlobalStylesChange({ textBackgroundColor: v })}
            onHasBorderChange={(v) => onGlobalStylesChange({ textHasBorder: v })}
            onBorderColorChange={(v) => onGlobalStylesChange({ textBorderColor: v })}
            onBorderWidthChange={(v) => onGlobalStylesChange({ textBorderWidth: v })}
            onBorderRadiusChange={(v) => onGlobalStylesChange({ textBorderRadius: v })}
            minSize={10} maxSize={32}
            inputHeight={globalStyles.inputHeight}
            onInputHeightChange={(v) => onGlobalStylesChange({ inputHeight: v })} />
        <TypographyCard title="Help & Validation" icon={MessageSquare} iconColor="text-orange-500"
            fontFamily={globalStyles.helpTextFontFamily} fontSize={globalStyles.helpTextFontSize}
            fontWeight={globalStyles.helpTextFontWeight} fontStyle={globalStyles.helpTextFontStyle}
            color={globalStyles.helpTextColor} backgroundColor={globalStyles.helpTextBackgroundColor}
            hasBorder={globalStyles.helpTextHasBorder} borderColor={globalStyles.helpTextBorderColor}
            borderWidth={globalStyles.helpTextBorderWidth} borderRadius={globalStyles.helpTextBorderRadius}
            showBorderOptions={true}
            onFontFamilyChange={(v) => onGlobalStylesChange({ helpTextFontFamily: v })}
            onFontSizeChange={(v) => onGlobalStylesChange({ helpTextFontSize: v })}
            onFontWeightChange={(v) => onGlobalStylesChange({ helpTextFontWeight: v })}
            onFontStyleChange={(v) => onGlobalStylesChange({ helpTextFontStyle: v })}
            onColorChange={(v) => onGlobalStylesChange({ helpTextColor: v })}
            onBackgroundColorChange={(v) => onGlobalStylesChange({ helpTextBackgroundColor: v })}
            onHasBorderChange={(v) => onGlobalStylesChange({ helpTextHasBorder: v })}
            onBorderColorChange={(v) => onGlobalStylesChange({ helpTextBorderColor: v })}
            onBorderWidthChange={(v) => onGlobalStylesChange({ helpTextBorderWidth: v })}
            onBorderRadiusChange={(v) => onGlobalStylesChange({ helpTextBorderRadius: v })}
            minSize={8} maxSize={20} />
    </div>
);

/**
 * Dividers & Lines section - standalone for accordion use
 */
export const DividersLinesSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="p-4">
        <div className="flex items-end gap-3">
            <div className="flex flex-col gap-1">
                <span className="text-[10px] text-gray-500">Color</span>
                <input type="color" value={globalStyles.dividerBorderColor}
                    onChange={(e) => onGlobalStylesChange({ dividerBorderColor: e.target.value })}
                    className="w-8 h-8 rounded cursor-pointer border border-gray-300" />
            </div>
            <div className="flex flex-col gap-1 flex-1">
                <span className="text-[10px] text-gray-500">Thickness ({globalStyles.dividerBorderWidth}px)</span>
                <input type="range" min={1} max={10} step={1} value={globalStyles.dividerBorderWidth}
                    onChange={(e) => onGlobalStylesChange({ dividerBorderWidth: parseInt(e.target.value) })}
                    className="w-full h-1 accent-gray-500" />
            </div>
            <div className="flex flex-col gap-1 w-[110px]">
                <span className="text-[10px] text-gray-500">Length</span>
                <input type="text" value={globalStyles.dividerWidth}
                    onChange={(e) => onGlobalStylesChange({ dividerWidth: e.target.value })}
                    placeholder="380px or 100%"
                    className="px-2 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
            </div>
        </div>
    </div>
);

/**
 * Grid Layout Defaults section - standalone for accordion use
 */
export const GridLayoutDefaultsSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="p-4 space-y-3">
        <p className="text-[10px] text-gray-400 mb-3">
            Default grid settings for components using Grid Layout mode
        </p>
        <PropertySelect label="Default Object Layout"
            value={globalStyles.defaultObjectLayout || 'vertical'}
            onChange={(value) => onGlobalStylesChange({ defaultObjectLayout: value as ObjectLayoutType })}
            options={OBJECT_LAYOUT_OPTIONS}
            helpText="Default object layout for components with structure (vertical/horizontal/mixed)" />
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 w-24">Default Row Gap</span>
            <input type="range" min={0} max={48} value={globalStyles.defaultGridLayout?.rowGap ?? 8}
                onChange={(e) => onGlobalStylesChange({ defaultGridLayout: { ...(globalStyles.defaultGridLayout ?? {}), rowGap: parseInt(e.target.value) } })}
                className="flex-1 h-1.5 accent-indigo-500" />
            <span className="text-[10px] text-gray-600 w-10">{globalStyles.defaultGridLayout?.rowGap ?? 8}px</span>
        </div>
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 w-24">Default Col Gap</span>
            <input type="range" min={0} max={48} value={globalStyles.defaultGridLayout?.columnGap ?? 8}
                onChange={(e) => onGlobalStylesChange({ defaultGridLayout: { ...(globalStyles.defaultGridLayout ?? {}), columnGap: parseInt(e.target.value) } })}
                className="flex-1 h-1.5 accent-indigo-500" />
            <span className="text-[10px] text-gray-600 w-10">{globalStyles.defaultGridLayout?.columnGap ?? 8}px</span>
        </div>
    </div>
);

export const GlobalStylesPanel: React.FC<GlobalStylesPanelProps> = ({
    globalStyles,
    onGlobalStylesChange,
}) => {
    // Prevent uncontrolled→controlled warnings:
    // When global styles are loaded/rehydrated, some keys may be temporarily missing (undefined).
    // Any <input value={undefined}> will mount uncontrolled and later become controlled.
    // Merge with defaults so all inputs always receive stable defined values.
    const effectiveGlobalStyles = React.useMemo(
        () => ({ ...DEFAULT_GLOBAL_STYLES, ...globalStyles }),
        [globalStyles]
    );

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
            <div className="border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2 p-4 pb-0">
                    <Focus size={14} className="text-blue-500" />
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Focus Color</h4>
                </div>
                <FocusColorSection globalStyles={effectiveGlobalStyles} onGlobalStylesChange={onGlobalStylesChange} />
            </div>
            <div className="border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2 p-4 pb-0">
                    <Type size={14} className="text-gray-400" />
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Typography & Spacing</h4>
                </div>
                <TypographySpacingSection globalStyles={effectiveGlobalStyles} onGlobalStylesChange={onGlobalStylesChange} />
            </div>
            <div className="border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2 p-4 pb-0">
                    <Minus size={14} className="text-gray-500" />
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Dividers & Lines</h4>
                </div>
                <DividersLinesSection globalStyles={effectiveGlobalStyles} onGlobalStylesChange={onGlobalStylesChange} />
            </div>
            <div className="border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2 p-4 pb-0">
                    <Grid3x3 size={16} className="text-gray-500" />
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Grid Layout Defaults</h4>
                </div>
                <GridLayoutDefaultsSection globalStyles={effectiveGlobalStyles} onGlobalStylesChange={onGlobalStylesChange} />
            </div>
            </div>
        </>
    );
};

