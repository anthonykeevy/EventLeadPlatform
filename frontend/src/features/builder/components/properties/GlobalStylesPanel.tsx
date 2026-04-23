import React from 'react';
import { Link } from 'react-router-dom';
import { Palette, Type, Tag, MessageSquare, Focus, ArrowUpDown, ArrowLeftRight, Minus, Grid3x3, ExternalLink, Save } from 'lucide-react';
import { useToastNotifications } from '../../../ux';
import { PropertyNumberInput, PropertyColorPicker, PropertySelect, TypographyCard } from './inputs';
import { 
    GlobalStyles, 
    ObjectLayoutType,
    HorizontalInputBandPreset,
    DEFAULT_GLOBAL_STYLES,
} from '../../types/builder.types';

interface GlobalStylesPanelProps {
    globalStyles: GlobalStyles;
    onGlobalStylesChange: (updates: Partial<GlobalStyles>) => void;
    /** Story 5.2 T05: Company context for Edit defaults link and Save to Company Defaults */
    companyId?: number | null;
    /** Story 5.2 T05: Whether current user is Company Admin (shows Save to Company Defaults) */
    isCompanyAdmin?: boolean;
    /** Story 5.2 T05: Save current form overrides to company defaults */
    onSaveToCompanyDefaults?: (companyId: number) => Promise<boolean>;
}

const OBJECT_LAYOUT_OPTIONS = [
    { value: 'vertical', label: 'Vertical' },
    { value: 'horizontal', label: 'Horizontal' },
];

// Story 6.3.1 (UAT round 6) — Fix D item 4: form-wide input-band density
// preset. Scales the per-type comfortable character counts on the backend
// when the AI compiler stamps `props.inputWidthOverride`. Per-component
// overrides (Appearance → Dimensions) always win.
const INPUT_BAND_PRESET_OPTIONS = [
    { value: 'compact', label: 'Compact (denser inputs)' },
    { value: 'standard', label: 'Standard (recommended)' },
    { value: 'spacious', label: 'Spacious (roomier inputs)' },
];

/** Props for section components shared with FormBrandingDefaultsPage */
export interface GlobalStylesSectionProps {
    globalStyles: GlobalStyles;
    onGlobalStylesChange: (updates: Partial<GlobalStyles>) => void;
}

/** Focus Color section - exported for FormBrandingDefaultsPage accordion */
export const FocusColorSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="px-4 pb-4 pt-0">
        <PropertyColorPicker
            label="Primary"
            value={globalStyles.primaryColor}
            onChange={(value) => onGlobalStylesChange({ primaryColor: value })}
        />
    </div>
);

/** Typography & Spacing section - exported for FormBrandingDefaultsPage accordion */
export const TypographySpacingSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="px-4 pb-4 pt-0 space-y-2">
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
            hasBorder={globalStyles.labelHasBorder}
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
            onHasBorderChange={(labelHasBorder) => onGlobalStylesChange({ labelHasBorder })}
            onBorderColorChange={(labelBorderColor) => onGlobalStylesChange({ labelBorderColor })}
            onBorderWidthChange={(labelBorderWidth) => onGlobalStylesChange({ labelBorderWidth })}
            onBorderRadiusChange={(labelBorderRadius) => onGlobalStylesChange({ labelBorderRadius })}
            minSize={10}
            maxSize={28}
        />
        <SpacingDivider
            label="Label ↔ Input gap"
            value={globalStyles.labelGap}
            onChange={(value) => onGlobalStylesChange({ labelGap: value })}
            baseSpacing={globalStyles.baseSpacing}
            icon={globalStyles.defaultObjectLayout === 'horizontal' ? 'horizontal' : 'vertical'}
        />
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
            hasBorder={globalStyles.textHasBorder}
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
            onHasBorderChange={(textHasBorder) => onGlobalStylesChange({ textHasBorder })}
            onBorderColorChange={(textBorderColor) => onGlobalStylesChange({ textBorderColor })}
            onBorderWidthChange={(textBorderWidth) => onGlobalStylesChange({ textBorderWidth })}
            onBorderRadiusChange={(textBorderRadius) => onGlobalStylesChange({ textBorderRadius })}
            minSize={10}
            maxSize={32}
            inputHeight={globalStyles.inputHeight}
            onInputHeightChange={(inputHeight) => onGlobalStylesChange({ inputHeight })}
        />
        <SpacingDivider
            label="Input ↓ Help text"
            value={globalStyles.inputHelpGap}
            onChange={(value) => onGlobalStylesChange({ inputHelpGap: value })}
            baseSpacing={globalStyles.baseSpacing}
            icon="vertical"
        />
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
            hasBorder={globalStyles.helpTextHasBorder}
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
            onHasBorderChange={(helpTextHasBorder) => onGlobalStylesChange({ helpTextHasBorder })}
            onBorderColorChange={(helpTextBorderColor) => onGlobalStylesChange({ helpTextBorderColor })}
            onBorderWidthChange={(helpTextBorderWidth) => onGlobalStylesChange({ helpTextBorderWidth })}
            onBorderRadiusChange={(helpTextBorderRadius) => onGlobalStylesChange({ helpTextBorderRadius })}
            minSize={8}
            maxSize={20}
        />
    </div>
);

/** Dividers & Lines section - exported for FormBrandingDefaultsPage accordion */
export const DividersLinesSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="px-4 pb-4 pt-0">
        <div className="flex items-end gap-3">
            <div className="flex flex-col gap-1">
                <span className="text-[10px] text-gray-500 dark:text-gray-400">Color</span>
                <input
                    type="color"
                    value={globalStyles.dividerBorderColor}
                    onChange={(e) => onGlobalStylesChange({ dividerBorderColor: e.target.value })}
                    className="w-8 h-8 rounded cursor-pointer border border-gray-300"
                />
            </div>
            <div className="flex flex-col gap-1 flex-1">
                <span className="text-[10px] text-gray-500 dark:text-gray-400">Thickness ({globalStyles.dividerBorderWidth ?? 1}px)</span>
                <input
                    type="range"
                    min={1}
                    max={10}
                    step={1}
                    value={globalStyles.dividerBorderWidth ?? 1}
                    onChange={(e) => onGlobalStylesChange({ dividerBorderWidth: parseInt(e.target.value) })}
                    className="w-full h-1 accent-gray-500"
                />
            </div>
            <div className="flex flex-col gap-1 w-[110px]">
                <span className="text-[10px] text-gray-500 dark:text-gray-400">Length</span>
                <input
                    type="text"
                    value={globalStyles.dividerWidth}
                    onChange={(e) => onGlobalStylesChange({ dividerWidth: e.target.value })}
                    placeholder="380px or 100%"
                    className="px-2 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
            </div>
        </div>
    </div>
);

/** Grid Layout Defaults section - exported for FormBrandingDefaultsPage accordion */
export const GridLayoutDefaultsSection: React.FC<GlobalStylesSectionProps> = ({ globalStyles, onGlobalStylesChange }) => (
    <div className="px-4 pb-4 pt-0 space-y-3">
        <PropertySelect
            label="Default Object Layout"
            value={globalStyles.defaultObjectLayout || 'vertical'}
            onChange={(value) => onGlobalStylesChange({ defaultObjectLayout: value as ObjectLayoutType })}
            options={OBJECT_LAYOUT_OPTIONS}
            helpText="Default object layout for components with structure (vertical/horizontal/mixed)"
        />
        {globalStyles.defaultObjectLayout === 'horizontal' && (
            <PropertySelect
                label="Input Band Preset"
                value={globalStyles.horizontalInputBandPreset || 'standard'}
                onChange={(value) => onGlobalStylesChange({ horizontalInputBandPreset: value as HorizontalInputBandPreset })}
                options={INPUT_BAND_PRESET_OPTIONS}
                helpText="Density of input fields when AI compiles a horizontal layout. Per-component widths still win."
            />
        )}
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 dark:text-gray-400 w-24">Default Rows</span>
            <PropertyNumberInput
                label=""
                value={globalStyles.defaultGridLayout?.rows ?? 3}
                onChange={(value) => onGlobalStylesChange({ defaultGridLayout: { ...(globalStyles.defaultGridLayout ?? {}), rows: value } })}
                min={1}
                max={12}
            />
        </div>
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 dark:text-gray-400 w-24">Default Columns</span>
            <PropertyNumberInput
                label=""
                value={globalStyles.defaultGridLayout?.columns ?? 1}
                onChange={(value) => onGlobalStylesChange({ defaultGridLayout: { ...(globalStyles.defaultGridLayout ?? {}), columns: value } })}
                min={1}
                max={12}
            />
        </div>
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 dark:text-gray-400 w-24">Default Row Gap</span>
            <input
                type="range"
                min={0}
                max={48}
                value={globalStyles.defaultGridLayout?.rowGap ?? 8}
                onChange={(e) => onGlobalStylesChange({ defaultGridLayout: { ...(globalStyles.defaultGridLayout ?? {}), rowGap: parseInt(e.target.value) } })}
                className="flex-1 h-1.5 accent-indigo-500"
            />
            <span className="text-[10px] text-gray-600 dark:text-gray-300 w-10">{globalStyles.defaultGridLayout?.rowGap ?? 8}px</span>
        </div>
        <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 dark:text-gray-400 w-24">Default Col Gap</span>
            <input
                type="range"
                min={0}
                max={48}
                value={globalStyles.defaultGridLayout?.columnGap ?? 8}
                onChange={(e) => onGlobalStylesChange({ defaultGridLayout: { ...(globalStyles.defaultGridLayout ?? {}), columnGap: parseInt(e.target.value) } })}
                className="flex-1 h-1.5 accent-indigo-500"
            />
            <span className="text-[10px] text-gray-600 dark:text-gray-300 w-10">{globalStyles.defaultGridLayout?.columnGap ?? 8}px</span>
        </div>
    </div>
);

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
    companyId,
    isCompanyAdmin,
    onSaveToCompanyDefaults,
}) => {
    const toast = useToastNotifications();
    const [isSavingToCompany, setIsSavingToCompany] = React.useState(false);
    const handleSaveToCompany = React.useCallback(async () => {
        if (!companyId || !onSaveToCompanyDefaults) return;
        setIsSavingToCompany(true);
        try {
            const ok = await onSaveToCompanyDefaults(companyId);
            if (ok) {
                toast.success('Form branding defaults saved', 'Saved');
            } else {
                toast.error('Failed to save company defaults', 'Error');
            }
        } catch {
            toast.error('Failed to save company defaults', 'Error');
        } finally {
            setIsSavingToCompany(false);
        }
    }, [companyId, onSaveToCompanyDefaults, toast]);
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
                    {companyId != null && (
                        <span className="block mt-1"> Values can be inherited from company defaults or overridden for this form.</span>
                    )}
                </p>
                {/* Story 5.2 T05: Inheritance actions */}
                {companyId != null && (
                    <div className="mt-3 space-y-2">
                        <Link
                            to={`/dashboard/companies/${companyId}/form-branding-defaults`}
                            className="inline-flex items-center gap-1.5 text-xs text-teal-600 hover:text-teal-700 dark:text-teal-400"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <ExternalLink size={12} />
                            Edit company defaults
                        </Link>
                        {isCompanyAdmin && onSaveToCompanyDefaults && (
                            <button
                                type="button"
                                onClick={handleSaveToCompany}
                                disabled={isSavingToCompany}
                                className="flex items-center gap-1.5 px-2 py-1.5 text-xs font-medium text-teal-700 bg-teal-50 hover:bg-teal-100 rounded-md disabled:opacity-50"
                            >
                                <Save size={12} />
                                {isSavingToCompany ? 'Saving…' : 'Save to Company Defaults'}
                            </button>
                        )}
                    </div>
                )}
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
                    value={effectiveGlobalStyles.primaryColor}
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
                        fontFamily={effectiveGlobalStyles.labelFontFamily}
                        fontSize={effectiveGlobalStyles.labelFontSize}
                        fontWeight={effectiveGlobalStyles.labelFontWeight}
                        fontStyle={effectiveGlobalStyles.labelFontStyle}
                        color={effectiveGlobalStyles.labelColor}
                        backgroundColor={effectiveGlobalStyles.labelBackgroundColor}
                        hasBorder={effectiveGlobalStyles.labelHasBorder}
                        borderColor={effectiveGlobalStyles.labelBorderColor}
                        borderWidth={effectiveGlobalStyles.labelBorderWidth}
                        borderRadius={effectiveGlobalStyles.labelBorderRadius}
                        showBorderOptions={true}
                        onFontFamilyChange={(labelFontFamily) => onGlobalStylesChange({ labelFontFamily })}
                        onFontSizeChange={(labelFontSize) => onGlobalStylesChange({ labelFontSize })}
                        onFontWeightChange={(labelFontWeight) => onGlobalStylesChange({ labelFontWeight })}
                        onFontStyleChange={(labelFontStyle) => onGlobalStylesChange({ labelFontStyle })}
                        onColorChange={(labelColor) => onGlobalStylesChange({ labelColor })}
                        onBackgroundColorChange={(labelBackgroundColor) => onGlobalStylesChange({ labelBackgroundColor })}
                        onHasBorderChange={(labelHasBorder) => onGlobalStylesChange({ labelHasBorder })}
                        onBorderColorChange={(labelBorderColor) => onGlobalStylesChange({ labelBorderColor })}
                        onBorderWidthChange={(labelBorderWidth) => onGlobalStylesChange({ labelBorderWidth })}
                        onBorderRadiusChange={(labelBorderRadius) => onGlobalStylesChange({ labelBorderRadius })}
                        minSize={10}
                        maxSize={28}
                    />

                    {/* Spacing: Label to Input */}
                    <SpacingDivider
                        label="Label ↔ Input gap"
                        value={effectiveGlobalStyles.labelGap}
                        onChange={(value) => onGlobalStylesChange({ labelGap: value })}
                        baseSpacing={effectiveGlobalStyles.baseSpacing}
                        icon={effectiveGlobalStyles.defaultObjectLayout === 'horizontal' ? 'horizontal' : 'vertical'}
                    />

                    {/* 2. Input Text Card (Middle - matches input position) */}
                    <TypographyCard
                        title="Input Text"
                        icon={Type}
                        iconColor="text-blue-500"
                        fontFamily={effectiveGlobalStyles.fontFamily}
                        fontSize={effectiveGlobalStyles.fontSize}
                        fontWeight={effectiveGlobalStyles.fontWeight}
                        fontStyle={effectiveGlobalStyles.fontStyle}
                        color={effectiveGlobalStyles.textColor}
                        backgroundColor={effectiveGlobalStyles.textBackgroundColor}
                        hasBorder={effectiveGlobalStyles.textHasBorder}
                        borderColor={effectiveGlobalStyles.textBorderColor}
                        borderWidth={effectiveGlobalStyles.textBorderWidth}
                        borderRadius={effectiveGlobalStyles.textBorderRadius}
                        showBorderOptions={true}
                        onFontFamilyChange={(fontFamily) => onGlobalStylesChange({ fontFamily })}
                        onFontSizeChange={(fontSize) => onGlobalStylesChange({ fontSize })}
                        onFontWeightChange={(fontWeight) => onGlobalStylesChange({ fontWeight })}
                        onFontStyleChange={(fontStyle) => onGlobalStylesChange({ fontStyle })}
                        onColorChange={(textColor) => onGlobalStylesChange({ textColor })}
                        onBackgroundColorChange={(textBackgroundColor) => onGlobalStylesChange({ textBackgroundColor })}
                        onHasBorderChange={(textHasBorder) => onGlobalStylesChange({ textHasBorder })}
                        onBorderColorChange={(textBorderColor) => onGlobalStylesChange({ textBorderColor })}
                        onBorderWidthChange={(textBorderWidth) => onGlobalStylesChange({ textBorderWidth })}
                        onBorderRadiusChange={(textBorderRadius) => onGlobalStylesChange({ textBorderRadius })}
                        minSize={10}
                        maxSize={32}
                        // Include Input Height in this card
                        inputHeight={effectiveGlobalStyles.inputHeight}
                        onInputHeightChange={(inputHeight) => onGlobalStylesChange({ inputHeight })}
                    />

                    {/* Spacing: Input to Help */}
                    <SpacingDivider
                        label="Input ↓ Help text"
                        value={effectiveGlobalStyles.inputHelpGap}
                        onChange={(value) => onGlobalStylesChange({ inputHelpGap: value })}
                        baseSpacing={effectiveGlobalStyles.baseSpacing}
                        icon="vertical"
                    />

                    {/* 3. Help & Validation Text Card (Bottom - matches help text position) */}
                    <TypographyCard
                        title="Help & Validation"
                        icon={MessageSquare}
                        iconColor="text-orange-500"
                        fontFamily={effectiveGlobalStyles.helpTextFontFamily}
                        fontSize={effectiveGlobalStyles.helpTextFontSize}
                        fontWeight={effectiveGlobalStyles.helpTextFontWeight}
                        fontStyle={effectiveGlobalStyles.helpTextFontStyle}
                        color={effectiveGlobalStyles.helpTextColor}
                        backgroundColor={effectiveGlobalStyles.helpTextBackgroundColor}
                        hasBorder={effectiveGlobalStyles.helpTextHasBorder}
                        borderColor={effectiveGlobalStyles.helpTextBorderColor}
                        borderWidth={effectiveGlobalStyles.helpTextBorderWidth}
                        borderRadius={effectiveGlobalStyles.helpTextBorderRadius}
                        showBorderOptions={true}
                        onFontFamilyChange={(helpTextFontFamily) => onGlobalStylesChange({ helpTextFontFamily })}
                        onFontSizeChange={(helpTextFontSize) => onGlobalStylesChange({ helpTextFontSize })}
                        onFontWeightChange={(helpTextFontWeight) => onGlobalStylesChange({ helpTextFontWeight })}
                        onFontStyleChange={(helpTextFontStyle) => onGlobalStylesChange({ helpTextFontStyle })}
                        onColorChange={(helpTextColor) => onGlobalStylesChange({ helpTextColor })}
                        onBackgroundColorChange={(helpTextBackgroundColor) => onGlobalStylesChange({ helpTextBackgroundColor })}
                        onHasBorderChange={(helpTextHasBorder) => onGlobalStylesChange({ helpTextHasBorder })}
                        onBorderColorChange={(helpTextBorderColor) => onGlobalStylesChange({ helpTextBorderColor })}
                        onBorderWidthChange={(helpTextBorderWidth) => onGlobalStylesChange({ helpTextBorderWidth })}
                        onBorderRadiusChange={(helpTextBorderRadius) => onGlobalStylesChange({ helpTextBorderRadius })}
                        minSize={8}
                        maxSize={20}
                    />

                    {/* 4. Dividers & Lines Card */}
                    {/* Reuse TypographyCard but simplified for lines */}
                    <div className="border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 shadow-sm p-3">
                        <div className="flex items-center gap-2 mb-3">
                            <Minus size={14} className="text-gray-500" />
                            <span className="text-sm font-medium text-gray-800 dark:text-gray-200">Dividers & Lines</span>
                        </div>
                        
                        <div className="flex items-end gap-3">
                            {/* Line Color */}
                            <div className="flex flex-col gap-1">
                                <span className="text-[10px] text-gray-500">Color</span>
                                <div className="flex items-center gap-1">
                                    <input
                                        type="color"
                                        value={effectiveGlobalStyles.dividerBorderColor}
                                        onChange={(e) => onGlobalStylesChange({ dividerBorderColor: e.target.value })}
                                        className="w-8 h-8 rounded cursor-pointer border border-gray-300"
                                    />
                                </div>
                            </div>

                            {/* Line Thickness */}
                            <div className="flex flex-col gap-1 flex-1">
                                <span className="text-[10px] text-gray-500">Thickness ({globalStyles.dividerBorderWidth}px)</span>
                                <input
                                    type="range"
                                    min={1}
                                    max={10}
                                    step={1}
                                    value={effectiveGlobalStyles.dividerBorderWidth}
                                    onChange={(e) => onGlobalStylesChange({ dividerBorderWidth: parseInt(e.target.value) })}
                                    className="w-full h-1 accent-gray-500"
                                />
                            </div>

                            {/* Divider Length */}
                            <div className="flex flex-col gap-1 w-[110px]">
                                <span className="text-[10px] text-gray-500">Length</span>
                                <input
                                    type="text"
                                    value={effectiveGlobalStyles.dividerWidth}
                                    onChange={(e) => onGlobalStylesChange({ dividerWidth: e.target.value })}
                                    placeholder="380px or 100%"
                                    className="px-2 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded-md 
                                        bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                                        focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Grid Layout Defaults Section */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-2 mb-3">
                    <Grid3x3 size={16} className="text-gray-500" />
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Grid Layout Defaults
                    </h4>
                </div>
                <p className="text-[10px] text-gray-400 mb-3">
                    Default grid settings for components using Grid Layout mode
                </p>
                
                <div className="space-y-3">
                    <PropertySelect
                        label="Default Object Layout"
                        value={effectiveGlobalStyles.defaultObjectLayout || 'vertical'}
                        onChange={(value) => onGlobalStylesChange({ defaultObjectLayout: value as ObjectLayoutType })}
                        options={OBJECT_LAYOUT_OPTIONS}
                        helpText="Default object layout for components with structure (vertical/horizontal/mixed)"
                    />

                    {effectiveGlobalStyles.defaultObjectLayout === 'horizontal' && (
                        <PropertySelect
                            label="Input Band Preset"
                            value={effectiveGlobalStyles.horizontalInputBandPreset || 'standard'}
                            onChange={(value) => onGlobalStylesChange({ horizontalInputBandPreset: value as HorizontalInputBandPreset })}
                            options={INPUT_BAND_PRESET_OPTIONS}
                            helpText="Density of input fields when AI compiles a horizontal layout. Per-component widths still win."
                        />
                    )}

                    {/* Default Rows */}
                    <div className="flex items-center gap-3">
                        <span className="text-[10px] text-gray-500 w-24">Default Rows</span>
                        <PropertyNumberInput
                            label=""
                            value={effectiveGlobalStyles.defaultGridLayout?.rows ?? 3}
                            onChange={(value) => onGlobalStylesChange({
                                defaultGridLayout: {
                                    ...effectiveGlobalStyles.defaultGridLayout,
                                    rows: value
                                }
                            })}
                            min={1}
                            max={12}
                        />
                    </div>
                    
                    {/* Default Columns */}
                    <div className="flex items-center gap-3">
                        <span className="text-[10px] text-gray-500 w-24">Default Columns</span>
                        <PropertyNumberInput
                            label=""
                            value={effectiveGlobalStyles.defaultGridLayout?.columns ?? 1}
                            onChange={(value) => onGlobalStylesChange({
                                defaultGridLayout: {
                                    ...effectiveGlobalStyles.defaultGridLayout,
                                    columns: value
                                }
                            })}
                            min={1}
                            max={12}
                        />
                    </div>
                    
                    {/* Default Row Gap */}
                    <div className="flex items-center gap-3">
                        <span className="text-[10px] text-gray-500 w-24">Default Row Gap</span>
                        <input
                            type="range"
                            min={0}
                            max={48}
                            value={effectiveGlobalStyles.defaultGridLayout?.rowGap ?? 8}
                            onChange={(e) => onGlobalStylesChange({
                                defaultGridLayout: {
                                    ...effectiveGlobalStyles.defaultGridLayout,
                                    rowGap: parseInt(e.target.value)
                                }
                            })}
                            className="flex-1 h-1.5 accent-indigo-500"
                        />
                        <span className="text-[10px] text-gray-600 w-10">
                            {effectiveGlobalStyles.defaultGridLayout?.rowGap ?? 8}px
                        </span>
                    </div>
                    
                    {/* Default Column Gap */}
                    <div className="flex items-center gap-3">
                        <span className="text-[10px] text-gray-500 w-24">Default Col Gap</span>
                        <input
                            type="range"
                            min={0}
                            max={48}
                            value={effectiveGlobalStyles.defaultGridLayout?.columnGap ?? 8}
                            onChange={(e) => onGlobalStylesChange({
                                defaultGridLayout: {
                                    ...effectiveGlobalStyles.defaultGridLayout,
                                    columnGap: parseInt(e.target.value)
                                }
                            })}
                            className="flex-1 h-1.5 accent-indigo-500"
                        />
                        <span className="text-[10px] text-gray-600 w-10">
                            {effectiveGlobalStyles.defaultGridLayout?.columnGap ?? 8}px
                        </span>
                    </div>
                </div>
            </div>

            </div>
        </>
    );
};

