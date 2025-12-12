/**
 * AppearanceSection - Story 3.5
 * 
 * Combines typography/spacing overrides with dimensions settings.
 * Renamed from StyleOverridesSection for clarity.
 * 
 * Order matches visual component layout:
 * 1. Dimensions (Width, Height, Alignment)
 * 2. Label Text
 * 3. [Label Gap spacing]
 * 4. Input Text  
 * 5. [Input-to-Help spacing]
 * 6. Help & Validation
 */

import React from 'react';
import { 
    ChevronDown, Link, Unlink, Tag, Type, MessageSquare, 
    ArrowUpDown, Palette, Maximize2, Wand2 
} from 'lucide-react';
import { TypographyCard, PropertySelect, PropertyNumberInput } from './inputs';
import { StyleOverrides, GlobalStyles, FontWeightValue, FontStyleType, ComponentProps, AlignType } from '../../types/builder.types';

interface AppearanceSectionProps {
    overrides: StyleOverrides | undefined;
    globalStyles: GlobalStyles;
    onOverridesChange: (updates: Partial<StyleOverrides>) => void;
    /** Current layout for spacing control direction */
    currentLayout?: 'vertical' | 'horizontal';
    /** Component props for dimensions */
    props?: ComponentProps;
    /** Handler for component props changes */
    onPropsChange?: (updates: Partial<ComponentProps>) => void;
    /** Component type for conditional rendering */
    componentType?: string;
}

const WIDTH_PRESET_OPTIONS = [
    { value: 'auto', label: 'Auto' },
    { value: '25%', label: '25%' },
    { value: '33%', label: '33%' },
    { value: '50%', label: '50%' },
    { value: '66%', label: '66%' },
    { value: '75%', label: '75%' },
    { value: '100%', label: '100%' },
    { value: 'custom', label: 'Custom (px)' },
];

const ALIGN_OPTIONS = [
    { value: 'left', label: 'Left' },
    { value: 'center', label: 'Center' },
    { value: 'right', label: 'Right' },
];

/**
 * Chain link indicator component - shows global/override status
 */
const ChainIndicator: React.FC<{
    isOverridden: boolean;
    onReset: () => void;
    overrideCount?: number;
}> = ({ isOverridden, onReset, overrideCount = 0 }) => (
    <button
        onClick={(e) => {
            e.stopPropagation();
            if (isOverridden) onReset();
        }}
        className={`flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] transition-colors ${
            isOverridden 
                ? 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 hover:bg-amber-100 dark:hover:bg-amber-900/30 cursor-pointer' 
                : 'text-gray-400 bg-gray-50 dark:bg-gray-800 cursor-default'
        }`}
        title={isOverridden ? 'Custom overrides - click to reset to global' : 'Using global values'}
    >
        {isOverridden ? (
            <>
                <Unlink size={10} />
                <span>{overrideCount} override{overrideCount !== 1 ? 's' : ''}</span>
            </>
        ) : (
            <>
                <Link size={10} />
                <span>global</span>
            </>
        )}
    </button>
);

/**
 * Inline spacing control with chain indicator
 */
const SpacingOverride: React.FC<{
    label: string;
    value: number;
    globalValue: number;
    baseSpacing: number;
    onChange: (value: number) => void;
    onReset: () => void;
    isOverridden: boolean;
}> = ({ label, value, globalValue, baseSpacing, onChange, onReset, isOverridden }) => (
    <div className="flex items-center gap-2 py-2 px-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-dashed border-gray-200 dark:border-gray-700">
        <ArrowUpDown size={12} className="text-gray-400" />
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
        <ChainIndicator 
            isOverridden={isOverridden} 
            onReset={onReset}
            overrideCount={1}
        />
    </div>
);

/**
 * Collapsible sub-section within Appearance
 */
const SubSection: React.FC<{
    title: string;
    icon: React.ElementType;
    iconColor: string;
    isExpanded: boolean;
    onToggle: () => void;
    children: React.ReactNode;
    badge?: React.ReactNode;
}> = ({ title, icon: Icon, iconColor, isExpanded, onToggle, children, badge }) => (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <button
            onClick={onToggle}
            className="w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800"
        >
            <div className="flex items-center gap-2">
                <Icon size={12} className={iconColor} />
                <span>{title}</span>
                {badge}
            </div>
            <ChevronDown 
                size={14} 
                className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            />
        </button>
        {isExpanded && (
            <div className="px-3 pb-3 pt-1 border-t border-gray-100 dark:border-gray-800">
                {children}
            </div>
        )}
    </div>
);

export const AppearanceSection: React.FC<AppearanceSectionProps> = ({
    overrides = {},
    globalStyles,
    onOverridesChange,
    currentLayout = 'vertical',
    props,
    onPropsChange,
    componentType = 'text',
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);
    const [isDimensionsExpanded, setIsDimensionsExpanded] = React.useState(true);
    const [isTypographyExpanded, setIsTypographyExpanded] = React.useState(false);
    const [customWidth, setCustomWidth] = React.useState<number>(300);

    // Dimensions logic
    const isCustomWidth = props?.width?.endsWith('px');
    const currentPreset = isCustomWidth ? 'custom' : (props?.width || 'auto');
    const supportsHeight = ['textarea'].includes(componentType);
    const supportsAutoFit = ['text', 'email', 'number', 'select', 'phone'].includes(componentType);

    const handleWidthPresetChange = (value: string) => {
        if (!onPropsChange) return;
        if (value === 'custom') {
            onPropsChange({ width: `${customWidth}px` });
        } else {
            onPropsChange({ width: value });
        }
    };

    const handleCustomWidthChange = (value: number) => {
        if (!onPropsChange) return;
        setCustomWidth(value);
        onPropsChange({ width: `${value}px` });
    };

    // Count overrides for each category
    const labelOverrides = ['labelFontFamily', 'labelFontSize', 'labelFontWeight', 'labelFontStyle', 'labelColor', 'labelBackgroundColor', 'labelBorderColor', 'labelBorderWidth', 'labelBorderRadius']
        .filter(key => key in overrides).length;
    
    const inputOverrides = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'textColor', 'textBackgroundColor', 'textBorderColor', 'textBorderWidth', 'textBorderRadius']
        .filter(key => key in overrides).length;
    
    const helpOverrides = ['helpTextFontFamily', 'helpTextFontSize', 'helpTextFontWeight', 'helpTextFontStyle', 'helpTextColor', 'helpTextBackgroundColor', 'helpTextBorderColor', 'helpTextBorderWidth', 'helpTextBorderRadius']
        .filter(key => key in overrides).length;

    const totalOverrides = Object.keys(overrides).length;

    // Helper to get effective value
    const getEffective = <K extends keyof StyleOverrides>(key: K, fallbackKey?: keyof GlobalStyles): NonNullable<StyleOverrides[K]> => {
        if (key in overrides) return overrides[key] as NonNullable<StyleOverrides[K]>;
        const gKey = fallbackKey || (key as keyof GlobalStyles);
        return globalStyles[gKey] as NonNullable<StyleOverrides[K]>;
    };
    
    const getDisplayValue = <K extends keyof StyleOverrides>(key: K, fallbackKey?: keyof GlobalStyles): StyleOverrides[K] | undefined => {
        if (key in overrides) return overrides[key];
        const gKey = fallbackKey || (key as keyof GlobalStyles);
        return globalStyles[gKey] as StyleOverrides[K];
    };

    // Reset helpers
    const resetLabelStyles = () => {
        const updates = { ...overrides };
        ['labelFontFamily', 'labelFontSize', 'labelFontWeight', 'labelFontStyle', 'labelColor', 'labelBackgroundColor', 'labelBorderColor', 'labelBorderWidth', 'labelBorderRadius']
            .forEach(key => delete updates[key as keyof StyleOverrides]);
        onOverridesChange(updates);
    };

    const resetInputStyles = () => {
        const updates = { ...overrides };
        ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'textColor', 'textBackgroundColor', 'textBorderColor', 'textBorderWidth', 'textBorderRadius']
            .forEach(key => delete updates[key as keyof StyleOverrides]);
        onOverridesChange(updates);
    };

    const resetHelpStyles = () => {
        const updates = { ...overrides };
        ['helpTextFontFamily', 'helpTextFontSize', 'helpTextFontWeight', 'helpTextFontStyle', 'helpTextColor', 'helpTextBackgroundColor', 'helpTextBorderColor', 'helpTextBorderWidth', 'helpTextBorderRadius']
            .forEach(key => delete updates[key as keyof StyleOverrides]);
        onOverridesChange(updates);
    };

    // Border change handlers
    const handleBorderChange = (
        colorKey: keyof StyleOverrides,
        widthKey: keyof StyleOverrides,
        radiusKey: keyof StyleOverrides
    ) => ({
        onColorChange: (v: string | undefined) => {
            onOverridesChange({ [colorKey]: v } as Partial<StyleOverrides>);
        },
        onWidthChange: (v: number | undefined) => {
            onOverridesChange({ [widthKey]: v } as Partial<StyleOverrides>);
        },
        onRadiusChange: (v: number | undefined) => {
            onOverridesChange({ [radiusKey]: v } as Partial<StyleOverrides>);
        },
    });

    const labelBorderHandlers = handleBorderChange('labelBorderColor', 'labelBorderWidth', 'labelBorderRadius');
    const inputBorderHandlers = handleBorderChange('textBorderColor', 'textBorderWidth', 'textBorderRadius');
    const helpBorderHandlers = handleBorderChange('helpTextBorderColor', 'helpTextBorderWidth', 'helpTextBorderRadius');

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Palette size={14} className="text-purple-500" />
                    <span>Appearance</span>
                    {totalOverrides > 0 && (
                        <span className="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 px-1.5 py-0.5 rounded">
                            {totalOverrides} custom
                        </span>
                    )}
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* DIMENSIONS SUB-SECTION */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {props && onPropsChange && (
                        <SubSection
                            title="Dimensions"
                            icon={Maximize2}
                            iconColor="text-blue-500"
                            isExpanded={isDimensionsExpanded}
                            onToggle={() => setIsDimensionsExpanded(!isDimensionsExpanded)}
                        >
                            <div className="space-y-3">
                                {/* Width Preset */}
                                <PropertySelect
                                    label="Width"
                                    value={currentPreset}
                                    onChange={handleWidthPresetChange}
                                    options={WIDTH_PRESET_OPTIONS}
                                    helpText="Component width"
                                />

                                {/* Custom Width Input */}
                                {isCustomWidth && (
                                    <PropertyNumberInput
                                        label="Custom Width"
                                        value={parseInt(props.width || '300')}
                                        onChange={handleCustomWidthChange}
                                        min={50}
                                        max={2000}
                                        step={10}
                                        unit="px"
                                    />
                                )}

                                {/* Auto-fit to Content */}
                                {supportsAutoFit && (
                                    <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-2">
                                                <Wand2 size={12} className="text-blue-500" />
                                                <span className="text-xs text-blue-700 dark:text-blue-300">
                                                    Auto-fit Width
                                                </span>
                                            </div>
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    onPropsChange({ width: '90%', inputWidthMode: 'fill' });
                                                }}
                                                className="px-2 py-1 text-[10px] bg-blue-600 text-white rounded hover:bg-blue-700"
                                            >
                                                Calculate
                                            </button>
                                        </div>
                                    </div>
                                )}

                                {/* Height (for textarea) */}
                                {supportsHeight && (
                                    <PropertyNumberInput
                                        label="Height"
                                        value={props.height || 100}
                                        onChange={(value) => onPropsChange({ height: value })}
                                        min={40}
                                        max={500}
                                        step={10}
                                        unit="px"
                                    />
                                )}

                                {/* Text Alignment */}
                                <PropertySelect
                                    label="Text Alignment"
                                    value={props.textAlign || 'left'}
                                    onChange={(value) => onPropsChange({ textAlign: value as AlignType })}
                                    options={ALIGN_OPTIONS}
                                />

                                {/* Component Scale - Proportional scaling */}
                                <div className="space-y-1 pt-2 border-t border-gray-100 dark:border-gray-700">
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                                            Component Scale
                                        </span>
                                        <span className="text-xs font-mono text-gray-500 dark:text-gray-400">
                                            {props.componentScale ?? 100}%
                                        </span>
                                    </div>
                                    <input
                                        type="range"
                                        min={50}
                                        max={200}
                                        step={5}
                                        value={props.componentScale ?? 100}
                                        onChange={(e) => onPropsChange({ componentScale: parseInt(e.target.value) })}
                                        className="w-full h-1.5 accent-blue-500"
                                    />
                                    <div className="flex justify-between text-[9px] text-gray-400">
                                        <span>50%</span>
                                        <span className="text-blue-500">100%</span>
                                        <span>200%</span>
                                    </div>
                                    <p className="text-[10px] text-gray-400 dark:text-gray-500 mt-1">
                                        Proportionally scales font, height, padding, and border radius
                                    </p>
                                    {(props.componentScale ?? 100) !== 100 && (
                                        <button
                                            type="button"
                                            onClick={() => onPropsChange({ componentScale: 100 })}
                                            className="w-full mt-1 py-1 text-[10px] text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded border border-blue-200 dark:border-blue-800"
                                        >
                                            Reset to 100%
                                        </button>
                                    )}
                                </div>
                            </div>
                        </SubSection>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* TYPOGRAPHY SUB-SECTION */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    <SubSection
                        title="Typography & Colors"
                        icon={Type}
                        iconColor="text-orange-500"
                        isExpanded={isTypographyExpanded}
                        onToggle={() => setIsTypographyExpanded(!isTypographyExpanded)}
                        badge={totalOverrides > 0 ? (
                            <span className="text-[10px] bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 px-1 py-0.5 rounded">
                                {totalOverrides}
                            </span>
                        ) : undefined}
                    >
                        <div className="space-y-2">
                            {/* Info Banner */}
                            <div className="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded mb-2">
                                <Link size={8} className="inline text-gray-400" /> global | 
                                <Unlink size={8} className="inline text-amber-500 ml-1" /> custom (click to reset)
                            </div>

                            {/* 1. Label Text Card */}
                            <div className="relative">
                                <div className="absolute -top-1 right-2 z-10">
                                    <ChainIndicator 
                                        isOverridden={labelOverrides > 0} 
                                        onReset={resetLabelStyles}
                                        overrideCount={labelOverrides}
                                    />
                                </div>
                                <TypographyCard
                                    title="Label Text"
                                    icon={Tag}
                                    iconColor="text-green-500"
                                    fontFamily={getEffective('labelFontFamily', 'labelFontFamily')}
                                    fontSize={getEffective('labelFontSize', 'labelFontSize') ?? 14}
                                    fontWeight={getEffective('labelFontWeight', 'labelFontWeight') ?? '500'}
                                    fontStyle={getEffective('labelFontStyle', 'labelFontStyle') ?? 'normal'}
                                    color={getEffective('labelColor', 'labelColor')}
                                    backgroundColor={getDisplayValue('labelBackgroundColor', 'labelBackgroundColor')}
                                    borderColor={getDisplayValue('labelBorderColor', 'labelBorderColor')}
                                    borderWidth={getDisplayValue('labelBorderWidth', 'labelBorderWidth')}
                                    borderRadius={getDisplayValue('labelBorderRadius', 'labelBorderRadius')}
                                    showBorderOptions={true}
                                    onFontFamilyChange={(v) => onOverridesChange({ labelFontFamily: v })}
                                    onFontSizeChange={(v) => onOverridesChange({ labelFontSize: v })}
                                    onFontWeightChange={(v) => onOverridesChange({ labelFontWeight: v as FontWeightValue })}
                                    onFontStyleChange={(v) => onOverridesChange({ labelFontStyle: v as FontStyleType })}
                                    onColorChange={(v) => onOverridesChange({ labelColor: v })}
                                    onBackgroundColorChange={(v) => onOverridesChange({ labelBackgroundColor: v })}
                                    onBorderColorChange={labelBorderHandlers.onColorChange}
                                    onBorderWidthChange={labelBorderHandlers.onWidthChange}
                                    onBorderRadiusChange={labelBorderHandlers.onRadiusChange}
                                    minSize={10}
                                    maxSize={28}
                                />
                            </div>

                            {/* Spacing: Label to Input */}
                            <SpacingOverride
                                label={currentLayout === 'horizontal' ? 'Label → Input' : 'Label ↓ Input'}
                                value={'labelGap' in overrides ? overrides.labelGap! : globalStyles.labelGap}
                                globalValue={globalStyles.labelGap}
                                baseSpacing={globalStyles.baseSpacing}
                                onChange={(v) => onOverridesChange({ labelGap: v })}
                                onReset={() => {
                                    const updates = { ...overrides };
                                    delete updates.labelGap;
                                    onOverridesChange(updates);
                                }}
                                isOverridden={'labelGap' in overrides}
                            />

                            {/* 2. Input Text Card */}
                            <div className="relative">
                                <div className="absolute -top-1 right-2 z-10">
                                    <ChainIndicator 
                                        isOverridden={inputOverrides > 0} 
                                        onReset={resetInputStyles}
                                        overrideCount={inputOverrides}
                                    />
                                </div>
                                <TypographyCard
                                    title="Input Text"
                                    icon={Type}
                                    iconColor="text-blue-500"
                                    fontFamily={getEffective('fontFamily', 'fontFamily')}
                                    fontSize={getEffective('fontSize', 'fontSize') ?? 14}
                                    fontWeight={getEffective('fontWeight', 'fontWeight') ?? '400'}
                                    fontStyle={getEffective('fontStyle', 'fontStyle') ?? 'normal'}
                                    color={getEffective('textColor', 'textColor')}
                                    backgroundColor={getDisplayValue('textBackgroundColor', 'textBackgroundColor')}
                                    borderColor={getDisplayValue('textBorderColor', 'textBorderColor')}
                                    borderWidth={getDisplayValue('textBorderWidth', 'textBorderWidth')}
                                    borderRadius={getDisplayValue('textBorderRadius', 'textBorderRadius')}
                                    showBorderOptions={true}
                                    inputHeight={overrides.inputHeight ?? globalStyles.inputHeight}
                                    onFontFamilyChange={(v) => onOverridesChange({ fontFamily: v })}
                                    onFontSizeChange={(v) => onOverridesChange({ fontSize: v })}
                                    onFontWeightChange={(v) => onOverridesChange({ fontWeight: v as FontWeightValue })}
                                    onFontStyleChange={(v) => onOverridesChange({ fontStyle: v as FontStyleType })}
                                    onColorChange={(v) => onOverridesChange({ textColor: v })}
                                    onBackgroundColorChange={(v) => onOverridesChange({ textBackgroundColor: v })}
                                    onBorderColorChange={inputBorderHandlers.onColorChange}
                                    onBorderWidthChange={inputBorderHandlers.onWidthChange}
                                    onBorderRadiusChange={inputBorderHandlers.onRadiusChange}
                                    onInputHeightChange={(v) => onOverridesChange({ inputHeight: v })}
                                    minSize={10}
                                    maxSize={32}
                                />
                            </div>

                            {/* Spacing: Input to Help */}
                            <SpacingOverride
                                label="Input ↓ Help text"
                                value={'inputHelpGap' in overrides ? overrides.inputHelpGap! : globalStyles.inputHelpGap}
                                globalValue={globalStyles.inputHelpGap}
                                baseSpacing={globalStyles.baseSpacing}
                                onChange={(v) => onOverridesChange({ inputHelpGap: v })}
                                onReset={() => {
                                    const updates = { ...overrides };
                                    delete updates.inputHelpGap;
                                    onOverridesChange(updates);
                                }}
                                isOverridden={'inputHelpGap' in overrides}
                            />

                            {/* 3. Help & Validation Card */}
                            <div className="relative">
                                <div className="absolute -top-1 right-2 z-10">
                                    <ChainIndicator 
                                        isOverridden={helpOverrides > 0} 
                                        onReset={resetHelpStyles}
                                        overrideCount={helpOverrides}
                                    />
                                </div>
                                <TypographyCard
                                    title="Help & Validation"
                                    icon={MessageSquare}
                                    iconColor="text-orange-500"
                                    fontFamily={getEffective('helpTextFontFamily', 'helpTextFontFamily')}
                                    fontSize={getEffective('helpTextFontSize', 'helpTextFontSize') ?? 12}
                                    fontWeight={getEffective('helpTextFontWeight', 'helpTextFontWeight') ?? '400'}
                                    fontStyle={getEffective('helpTextFontStyle', 'helpTextFontStyle') ?? 'normal'}
                                    color={getEffective('helpTextColor', 'helpTextColor')}
                                    backgroundColor={getDisplayValue('helpTextBackgroundColor', 'helpTextBackgroundColor')}
                                    borderColor={getDisplayValue('helpTextBorderColor', 'helpTextBorderColor')}
                                    borderWidth={getDisplayValue('helpTextBorderWidth', 'helpTextBorderWidth')}
                                    borderRadius={getDisplayValue('helpTextBorderRadius', 'helpTextBorderRadius')}
                                    showBorderOptions={true}
                                    onFontFamilyChange={(v) => onOverridesChange({ helpTextFontFamily: v })}
                                    onFontSizeChange={(v) => onOverridesChange({ helpTextFontSize: v })}
                                    onFontWeightChange={(v) => onOverridesChange({ helpTextFontWeight: v as FontWeightValue })}
                                    onFontStyleChange={(v) => onOverridesChange({ helpTextFontStyle: v as FontStyleType })}
                                    onColorChange={(v) => onOverridesChange({ helpTextColor: v })}
                                    onBackgroundColorChange={(v) => onOverridesChange({ helpTextBackgroundColor: v })}
                                    onBorderColorChange={helpBorderHandlers.onColorChange}
                                    onBorderWidthChange={helpBorderHandlers.onWidthChange}
                                    onBorderRadiusChange={helpBorderHandlers.onRadiusChange}
                                    minSize={8}
                                    maxSize={20}
                                />
                            </div>

                            {/* Reset All Button */}
                            {totalOverrides > 0 && (
                                <button
                                    onClick={() => onOverridesChange({})}
                                    className="w-full mt-2 py-1.5 text-[10px] text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/20 rounded border border-amber-200 dark:border-amber-800 transition-colors"
                                >
                                    Reset All Typography to Global
                                </button>
                            )}
                        </div>
                    </SubSection>
                </div>
            )}
        </div>
    );
};

// Also export as StyleOverridesSection for backwards compatibility
export const StyleOverridesSection = AppearanceSection;


