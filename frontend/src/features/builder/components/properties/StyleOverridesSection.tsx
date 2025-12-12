/**
 * StyleOverridesSection - Story 3.5
 * 
 * Mirrors the Global Typography section but with chain link indicators
 * to show which properties are using global values vs custom overrides.
 * 
 * Order matches visual component layout:
 * 1. Label Text
 * 2. [Label Gap spacing]
 * 3. Input Text  
 * 4. [Input-to-Help spacing]
 * 5. Help & Validation
 */

import React from 'react';
import { ChevronDown, Link, Unlink, Tag, Type, MessageSquare, ArrowUpDown } from 'lucide-react';
import { TypographyCard } from './inputs';
import { StyleOverrides, GlobalStyles, FontWeightValue, FontStyleType } from '../../types/builder.types';

interface StyleOverridesSectionProps {
    overrides: StyleOverrides | undefined;
    globalStyles: GlobalStyles;
    onOverridesChange: (updates: Partial<StyleOverrides>) => void;
    /** Current layout for spacing control direction */
    currentLayout?: 'vertical' | 'horizontal';
}

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

export const StyleOverridesSection: React.FC<StyleOverridesSectionProps> = ({
    overrides = {},
    globalStyles,
    onOverridesChange,
    currentLayout = 'vertical',
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);

    // Count overrides for each category (check if key EXISTS in overrides, not just if value is defined)
    const labelOverrides = ['labelFontFamily', 'labelFontSize', 'labelFontWeight', 'labelFontStyle', 'labelColor', 'labelBackgroundColor', 'labelBorderColor', 'labelBorderWidth', 'labelBorderRadius']
        .filter(key => key in overrides).length;
    
    const inputOverrides = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'textColor', 'textBackgroundColor', 'textBorderColor', 'textBorderWidth', 'textBorderRadius']
        .filter(key => key in overrides).length;
    
    const helpOverrides = ['helpTextFontFamily', 'helpTextFontSize', 'helpTextFontWeight', 'helpTextFontStyle', 'helpTextColor', 'helpTextBackgroundColor', 'helpTextBorderColor', 'helpTextBorderWidth', 'helpTextBorderRadius']
        .filter(key => key in overrides).length;

    const totalOverrides = Object.keys(overrides).length;

    // Helper to get effective value - checks if key EXISTS in overrides (not just if value is defined)
    const getEffective = <K extends keyof StyleOverrides>(key: K, fallbackKey?: keyof GlobalStyles): NonNullable<StyleOverrides[K]> => {
        if (key in overrides) return overrides[key] as NonNullable<StyleOverrides[K]>;
        const gKey = fallbackKey || (key as keyof GlobalStyles);
        return globalStyles[gKey] as NonNullable<StyleOverrides[K]>;
    };
    
    // Helper to get value for display - respects undefined as "transparent" for backgrounds
    const getDisplayValue = <K extends keyof StyleOverrides>(key: K, fallbackKey?: keyof GlobalStyles): StyleOverrides[K] | undefined => {
        if (key in overrides) return overrides[key];
        const gKey = fallbackKey || (key as keyof GlobalStyles);
        return globalStyles[gKey] as StyleOverrides[K];
    };

    // Reset helpers for each category
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

    // Helper for border changes
    // - Setting a value (including 0) = explicit override
    // - Reset is handled by the chain link reset buttons (DELETE keys)
    const handleBorderChange = (
        colorKey: keyof StyleOverrides,
        widthKey: keyof StyleOverrides,
        radiusKey: keyof StyleOverrides
    ) => ({
        onColorChange: (v: string | undefined) => {
            // undefined = transparent (explicit override), null would mean "delete"
            onOverridesChange({ [colorKey]: v } as Partial<StyleOverrides>);
        },
        onWidthChange: (v: number | undefined) => {
            // 0 = "no border" (explicit override)
            // Any positive number = visible border
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
                    <Type size={14} className="text-gray-400" />
                    <span>Typography & Spacing</span>
                    {totalOverrides > 0 && (
                        <span className="text-xs bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 px-1.5 py-0.5 rounded">
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
                <div className="px-4 pb-4">
                    {/* Info Banner */}
                    <div className="text-xs text-gray-500 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 p-3 rounded mb-4">
                        <div className="font-medium text-blue-700 dark:text-blue-300 mb-1">
                            How to customize this component:
                        </div>
                        <ul className="space-y-1 text-[11px]">
                            <li>• <strong>Click any card</strong> to expand and edit its values</li>
                            <li>• <Link size={10} className="inline text-gray-400" /> <span className="text-gray-400">global</span> = using global values</li>
                            <li>• <Unlink size={10} className="inline text-amber-500" /> <span className="text-amber-500">N overrides</span> = has custom values (click to reset)</li>
                        </ul>
                    </div>

                    <div className="space-y-2">
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
                    </div>

                    {/* Reset All Button */}
                    {totalOverrides > 0 && (
                        <button
                            onClick={() => onOverridesChange({})}
                            className="w-full mt-4 py-2 text-xs text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/20 rounded border border-amber-200 dark:border-amber-800 transition-colors"
                        >
                            Reset All to Global Defaults
                        </button>
                    )}
                </div>
            )}
        </div>
    );
};
