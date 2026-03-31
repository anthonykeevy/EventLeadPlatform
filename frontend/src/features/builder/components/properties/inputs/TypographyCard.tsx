/**
 * TypographyCard - Story 3.5
 * 
 * Collapsible card for typography settings that shows:
 * - Summary view: Font name • Size • Weight with color swatches
 * - Expanded view: Font, Size/Weight/Style, Text & Background colors, optional borders
 * 
 * Each text type (Input, Label, Help) gets its own card.
 */

import React, { useState, useRef } from 'react';
import { ChevronDown, ChevronUp, LucideIcon } from 'lucide-react';
import { CategoryFontSelect } from './CategoryFontSelect';
import { FontWeightControl } from './FontWeightControl';
import { FontWeightValue, FontStyleType, FONT_WEIGHT_LABELS } from '../../../types/builder.types';
import { RuleEducationalInfo } from '../../../types/validationRule.types';
import { InfoTooltip } from '../../ui/InfoTooltip';

interface TypographyCardProps {
    /** Title for the card (e.g., "Input Text") */
    title: string;
    /**
     * Same pattern as Export Field Name: structured help via HelpCircle + portal tooltip
     * (`InfoTooltip` / `RuleEducationalInfo`). Omit for cards that do not need inline help.
     */
    titleInfo?: RuleEducationalInfo;
    /** Icon to display next to title */
    icon: LucideIcon;
    /** Icon color class (e.g., "text-blue-500") */
    iconColor: string;
    /** Current font family */
    fontFamily: string;
    /** Current font size */
    fontSize: number;
    /** Current font weight */
    fontWeight: FontWeightValue;
    /** Current font style */
    fontStyle: FontStyleType;
    /** Current text color */
    color?: string;
    /** Current background color */
    backgroundColor?: string;
    /** Border color (optional) */
    borderColor?: string;
    /** Border width (optional) */
    borderWidth?: number;
    /** Border radius (optional) */
    borderRadius?: number;
    /** Show border controls? */
    showBorderOptions?: boolean;
    /** Controlled border visibility (when set, overrides derived state from border props) */
    hasBorder?: boolean;
    /** Callback when border visibility toggle changes */
    onHasBorderChange?: (hasBorder: boolean) => void;
    /** Input height (optional - for Input Text card) */
    inputHeight?: number;
    /** Callback when font family changes */
    onFontFamilyChange: (fontFamily: string) => void;
    /** Callback when font size changes */
    onFontSizeChange: (size: number) => void;
    /** Callback when font weight changes */
    onFontWeightChange: (weight: FontWeightValue) => void;
    /** Callback when font style changes */
    onFontStyleChange: (style: FontStyleType) => void;
    /** Callback when text color changes */
    onColorChange?: (color: string) => void;
    /** Callback when background color changes */
    onBackgroundColorChange?: (color: string | undefined) => void;
    /** Callback when border color changes */
    onBorderColorChange?: (color: string | undefined) => void;
    /** Callback when border width changes */
    onBorderWidthChange?: (width: number | undefined) => void;
    /** Callback when border radius changes */
    onBorderRadiusChange?: (radius: number | undefined) => void;
    /** Callback when input height changes */
    onInputHeightChange?: (height: number) => void;
    /** Min font size allowed */
    minSize?: number;
    /** Max font size allowed */
    maxSize?: number;
    /** Start expanded? */
    defaultExpanded?: boolean;
}

// Common font sizes for the compact dropdown
const FONT_SIZE_OPTIONS = [
    { value: '8', label: '8' },
    { value: '9', label: '9' },
    { value: '10', label: '10' },
    { value: '11', label: '11' },
    { value: '12', label: '12' },
    { value: '13', label: '13' },
    { value: '14', label: '14' },
    { value: '16', label: '16' },
    { value: '18', label: '18' },
    { value: '20', label: '20' },
    { value: '24', label: '24' },
    { value: '28', label: '28' },
    { value: '32', label: '32' },
    { value: '36', label: '36' },
    { value: '48', label: '48' },
];

/**
 * Format weight for display (e.g., 400 -> "Regular")
 */
function formatWeight(weight: FontWeightValue): string {
    return FONT_WEIGHT_LABELS[weight] || `${weight}`;
}

/**
 * Format style for display
 */
function formatStyle(style: FontStyleType): string {
    return style === 'italic' ? 'Italic' : '';
}

/**
 * Text color picker - label inside the swatch
 */
const TextColorPicker: React.FC<{
    color: string;
    onChange: (color: string) => void;
}> = ({ color, onChange }) => {
    const inputRef = useRef<HTMLInputElement>(null);
    
    // Determine if text should be light or dark based on background
    const isLight = isLightColor(color);
    
    return (
        <div className="relative">
            <button
                type="button"
                onClick={() => inputRef.current?.click()}
                className="w-14 h-14 rounded-lg border-2 border-gray-300 dark:border-gray-500 shadow-md 
                    hover:border-blue-500 transition-all cursor-pointer flex items-center justify-center"
                style={{ backgroundColor: color }}
                title={`Text color: ${color}`}
            >
                <span 
                    className="text-[10px] font-bold uppercase tracking-wide"
                    style={{ color: isLight ? '#374151' : '#F9FAFB' }}
                >
                    Text
                </span>
            </button>
            <input
                ref={inputRef}
                type="color"
                value={color}
                onChange={(e) => onChange(e.target.value)}
                className="absolute inset-0 opacity-0 cursor-pointer"
            />
        </div>
    );
};

/**
 * Background color picker with transparent toggle inside
 */
const BackgroundColorPicker: React.FC<{
    color: string | undefined;
    defaultColor: string;
    onChange: (color: string | undefined) => void;
}> = ({ color, defaultColor, onChange }) => {
    const inputRef = useRef<HTMLInputElement>(null);
    const isTransparent = color === 'transparent';
    const hasColor = color !== undefined && !isTransparent;
    const displayColor = isTransparent ? defaultColor : (color || defaultColor);
    const isLight = isTransparent ? true : isLightColor(displayColor);
    
    const handleClick = (e: React.MouseEvent) => {
        // Only open color picker if not clicking the transparent toggle
        const target = e.target as HTMLElement;
        if (!target.closest('[data-transparent-toggle]')) {
            inputRef.current?.click();
        }
    };
    
    return (
        <div className="relative">
            {/* Use div instead of button to avoid nested buttons */}
            <div
                role="button"
                tabIndex={0}
                onClick={handleClick}
                onKeyDown={(e) => e.key === 'Enter' && handleClick(e as React.MouseEvent)}
                className={`w-14 h-14 rounded-lg border-2 shadow-md transition-all cursor-pointer 
                    flex flex-col items-center justify-center gap-0.5
                    ${(hasColor || isTransparent) 
                        ? 'border-gray-300 dark:border-gray-500 hover:border-blue-500' 
                        : 'border-dashed border-gray-300 dark:border-gray-600 hover:border-gray-400'
                    }`}
                style={{ 
                    backgroundColor: isTransparent ? 'transparent' : (hasColor ? displayColor : 'transparent'),
                    backgroundImage: isTransparent 
                        ? 'linear-gradient(45deg, #e5e5e5 25%, transparent 25%, transparent 75%, #e5e5e5 75%, #e5e5e5), linear-gradient(45deg, #e5e5e5 25%, transparent 25%, transparent 75%, #e5e5e5 75%, #e5e5e5)'
                        : (!hasColor ? 'linear-gradient(45deg, #e5e5e5 25%, transparent 25%, transparent 75%, #e5e5e5 75%, #e5e5e5), linear-gradient(45deg, #e5e5e5 25%, transparent 25%, transparent 75%, #e5e5e5 75%, #e5e5e5)' : undefined),
                    backgroundSize: (isTransparent || !hasColor) ? '8px 8px' : undefined,
                    backgroundPosition: (isTransparent || !hasColor) ? '0 0, 4px 4px' : undefined,
                }}
                title={isTransparent ? 'Transparent background' : (hasColor ? `Background: ${displayColor}` : 'Transparent background')}
            >
                <span 
                    className="text-[9px] font-bold uppercase tracking-wide"
                    style={{ color: isLight ? '#374151' : '#F9FAFB' }}
                >
                    {isTransparent ? 'TRANS' : 'BG'}
                </span>
                {/* Transparent toggle inside */}
                <button
                    data-transparent-toggle
                    type="button"
                    onClick={(e) => {
                        e.stopPropagation();
                        if (isTransparent) {
                            onChange(defaultColor);
                        } else {
                            onChange('transparent');
                        }
                    }}
                    className={`text-[7px] px-1 py-0.5 rounded transition-all
                        ${isTransparent 
                            ? 'bg-blue-500 text-white font-medium' 
                            : 'bg-white/80 text-gray-600 hover:bg-red-100 hover:text-red-600'
                        }`}
                    title={isTransparent ? 'Click to restore color' : 'Transparent (click BG area for color)'}
                >
                    {isTransparent ? '✓' : '✕'} trans
                </button>
            </div>
            <input
                ref={inputRef}
                type="color"
                value={displayColor}
                onChange={(e) => onChange(e.target.value)}
                className="absolute inset-0 opacity-0 cursor-pointer pointer-events-none"
            />
        </div>
    );
};

/**
 * Check if a color is light (for contrast text)
 */
function isLightColor(hex: string): boolean {
    const c = hex.replace('#', '');
    const r = parseInt(c.substring(0, 2), 16);
    const g = parseInt(c.substring(2, 4), 16);
    const b = parseInt(c.substring(4, 6), 16);
    const brightness = (r * 299 + g * 587 + b * 114) / 1000;
    return brightness > 128;
}

export const TypographyCard: React.FC<TypographyCardProps> = ({
    title,
    titleInfo,
    icon: Icon,
    iconColor,
    fontFamily,
    fontSize,
    fontWeight,
    fontStyle,
    color,
    backgroundColor,
    borderColor,
    borderWidth,
    borderRadius,
    showBorderOptions = false,
    hasBorder: hasBorderProp,
    onHasBorderChange,
    inputHeight,
    onFontFamilyChange,
    onFontSizeChange,
    onFontWeightChange,
    onFontStyleChange,
    onColorChange,
    onBackgroundColorChange,
    onBorderColorChange,
    onBorderWidthChange,
    onBorderRadiusChange,
    onInputHeightChange,
    defaultExpanded = false,
}) => {
    const [isExpanded, setIsExpanded] = useState(defaultExpanded);
    // Derive showBorders from props - show if any border property has a value (when hasBorder prop not provided)
    const hasBorderProps = borderColor !== undefined || (borderWidth !== undefined && borderWidth > 0);
    const [showBorders, setShowBorders] = useState(hasBorderProp ?? hasBorderProps);
    const effectiveShowBorders = hasBorderProp !== undefined ? hasBorderProp : showBorders;

    // Sync showBorders state with props (when parent resets values or when controlled)
    React.useEffect(() => {
        if (hasBorderProp !== undefined) {
            setShowBorders(hasBorderProp);
        } else {
            setShowBorders(hasBorderProps);
        }
    }, [hasBorderProp, hasBorderProps]);

    // Build summary string
    const summaryParts = [
        fontFamily,
        `${fontSize}px`,
        formatWeight(fontWeight),
        formatStyle(fontStyle),
    ].filter(Boolean);
    const summary = summaryParts.join(' • ');

    return (
        <div className="border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 shadow-sm">
            {/* Header: title toggles expand; right cluster matches Export Field Name (label + gap-1.5 + InfoTooltip). Nested buttons avoided. */}
            <div className="w-full flex items-center justify-between px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-750 transition-colors gap-2">
                <button
                    type="button"
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="flex items-center gap-2 min-w-0 flex-1 text-left rounded-md -mx-1 px-1 py-0.5 hover:bg-gray-100/80 dark:hover:bg-gray-700/50 transition-colors"
                >
                    <Icon size={14} className={`shrink-0 ${iconColor}`} />
                    <span className="text-sm font-medium text-gray-800 dark:text-gray-200 truncate">{title}</span>
                </button>
                <div className="flex items-center gap-1.5 shrink-0">
                    {titleInfo ? <InfoTooltip info={titleInfo} size={12} /> : null}
                    {color && (
                        <div
                            className="w-4 h-4 rounded border border-gray-300 dark:border-gray-500 shadow-sm"
                            style={{ backgroundColor: color }}
                            title="Text color"
                        />
                    )}
                    {backgroundColor && (
                        <div
                            className="w-4 h-4 rounded border border-gray-300 dark:border-gray-500 shadow-sm"
                            style={{
                                backgroundColor: backgroundColor === 'transparent' ? 'transparent' : backgroundColor,
                                backgroundImage:
                                    backgroundColor === 'transparent'
                                        ? 'linear-gradient(45deg, #e5e5e5 25%, transparent 25%, transparent 75%, #e5e5e5 75%, #e5e5e5), linear-gradient(45deg, #e5e5e5 25%, transparent 25%, transparent 75%, #e5e5e5 75%, #e5e5e5)'
                                        : undefined,
                                backgroundSize: backgroundColor === 'transparent' ? '6px 6px' : undefined,
                                backgroundPosition: backgroundColor === 'transparent' ? '0 0, 3px 3px' : undefined,
                            }}
                            title={backgroundColor === 'transparent' ? 'Background: transparent' : 'Background color'}
                        />
                    )}
                    <button
                        type="button"
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="p-0.5 rounded text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                        aria-expanded={isExpanded}
                        aria-label={isExpanded ? 'Collapse typography' : 'Expand typography'}
                    >
                        {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    </button>
                </div>
            </div>

            {/* Summary - Only visible when collapsed */}
            {!isExpanded && (
                <div 
                    className="px-3 pb-2 -mt-0.5 cursor-pointer"
                    onClick={() => setIsExpanded(true)}
                >
                    <p 
                        className="text-[11px] text-gray-500 dark:text-gray-400 truncate"
                        style={{ fontFamily }}
                        title={summary}
                    >
                        {summary}
                    </p>
                </div>
            )}

            {/* Expanded Controls */}
            {isExpanded && (
                <div className="px-3 pb-3 space-y-3 border-t border-gray-100 dark:border-gray-700 pt-3">
                    {/* Font Family - Full width */}
                    <div className="relative z-20">
                        <CategoryFontSelect
                            label="Font"
                            value={fontFamily}
                            onChange={(family) => onFontFamilyChange(family)}
                        />
                    </div>

                    {/* Size, Weight, Style - Optimized widths */}
                    <div className="flex items-end gap-1.5">
                        {/* Size - Compact */}
                        <div className="w-[52px]">
                            <label className="block text-[9px] font-medium text-gray-500 dark:text-gray-400 mb-1 uppercase tracking-wide">
                                Size
                            </label>
                            <select
                                value={fontSize.toString()}
                                onChange={(e) => onFontSizeChange(parseInt(e.target.value))}
                                className="w-full px-1 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded 
                                    bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200
                                    focus:ring-1 focus:ring-blue-500 focus:border-blue-500 cursor-pointer"
                            >
                                {FONT_SIZE_OPTIONS.map(opt => (
                                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                                ))}
                            </select>
                        </div>

                        {/* Weight - Flexible (takes remaining space) */}
                        <div className="flex-1 min-w-0">
                            <FontWeightControl
                                label="Weight"
                                value={fontWeight}
                                onChange={(w) => onFontWeightChange(w as FontWeightValue)}
                                fontFamily={fontFamily}
                            />
                        </div>

                        {/* Style - Compact */}
                        <div className="w-[48px]">
                            <label className="block text-[9px] font-medium text-gray-500 dark:text-gray-400 mb-1 uppercase tracking-wide">
                                Style
                            </label>
                            <select
                                value={fontStyle}
                                onChange={(e) => onFontStyleChange(e.target.value as FontStyleType)}
                                className="w-full px-1 py-1.5 text-xs border border-gray-300 dark:border-gray-600 rounded 
                                    bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200
                                    focus:ring-1 focus:ring-blue-500 focus:border-blue-500 cursor-pointer"
                            >
                                <option value="normal">Aa</option>
                                <option value="italic">It</option>
                            </select>
                        </div>
                    </div>

                    {/* Colors Section - Equation layout: Text + Background = Preview */}
                    {onColorChange && (
                        <div className="pt-2 border-t border-gray-100 dark:border-gray-700">
                            <div className="flex items-center justify-center gap-1">
                                {/* Text Color */}
                                <TextColorPicker
                                    color={color || '#1F2937'}
                                    onChange={(c) => onColorChange(c)}
                                />

                                {/* Plus sign */}
                                {onBackgroundColorChange && (
                                    <span className="text-lg font-light text-gray-300 dark:text-gray-600 mx-0.5">+</span>
                                )}

                                {/* Background Color */}
                                {onBackgroundColorChange && (
                                    <BackgroundColorPicker
                                        color={backgroundColor}
                                        defaultColor="#FFFF00"
                                        onChange={onBackgroundColorChange}
                                    />
                                )}

                                {/* Equals sign */}
                                <span className="text-lg font-light text-gray-300 dark:text-gray-600 mx-0.5">=</span>

                                {/* Live Preview */}
                                <div 
                                    className="w-14 h-14 flex items-center justify-center text-center shadow-inner"
                                    style={{ 
                                        fontFamily,
                                        fontSize: `${Math.min(fontSize, 12)}px`,
                                        fontWeight,
                                        fontStyle,
                                        color: color || '#1F2937',
                                        backgroundColor: backgroundColor === 'transparent' ? 'transparent' : (backgroundColor || 'transparent'),
                                        backgroundImage: (!backgroundColor || backgroundColor === 'transparent')
                                            ? 'linear-gradient(45deg, #f3f4f6 25%, transparent 25%, transparent 75%, #f3f4f6 75%, #f3f4f6), linear-gradient(45deg, #f3f4f6 25%, transparent 25%, transparent 75%, #f3f4f6 75%, #f3f4f6)'
                                            : undefined,
                                        backgroundSize: (!backgroundColor || backgroundColor === 'transparent') ? '8px 8px' : undefined,
                                        backgroundPosition: (!backgroundColor || backgroundColor === 'transparent') ? '0 0, 4px 4px' : undefined,
                                        // Border styling - use explicit values when borders are configured
                                        borderStyle: borderColor || borderWidth ? 'solid' : 'solid',
                                        borderColor: borderColor || '#E5E7EB',
                                        borderWidth: borderWidth ? `${borderWidth}px` : '2px',
                                        borderRadius: `${borderRadius ?? 8}px`,
                                    }}
                                    title="Preview"
                                >
                                    <span className="text-[9px] font-bold uppercase tracking-wide">
                                        Preview
                                    </span>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Input Height - Only shown for Input Text card */}
                    {onInputHeightChange && inputHeight !== undefined && (
                        <div className="pt-2 border-t border-gray-100 dark:border-gray-700">
                            <div className="flex items-center gap-2">
                                <span className="text-[10px] font-medium text-gray-600 dark:text-gray-400 flex-1">
                                    Input Height
                                </span>
                                <div className="flex items-center gap-1">
                                    <input
                                        type="range"
                                        min={28}
                                        max={56}
                                        value={inputHeight}
                                        onChange={(e) => onInputHeightChange(parseInt(e.target.value))}
                                        className="w-20 h-1 accent-blue-500"
                                    />
                                    <span className="text-[10px] font-mono text-gray-600 dark:text-gray-300 w-10 text-right">
                                        {inputHeight}px
                                    </span>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Border Section - Optional */}
                    {showBorderOptions && (
                        <div className="pt-2 border-t border-gray-100 dark:border-gray-700">
                            <div className="flex items-center gap-2 mb-2">
                                <button
                                    type="button"
                                    onClick={() => {
                                        const newShow = !effectiveShowBorders;
                                        setShowBorders(newShow);
                                        onHasBorderChange?.(newShow);
                                        if (newShow) {
                                            // Set default values when enabling border
                                            if (!borderColor) onBorderColorChange?.('#D1D5DB');
                                            if (!borderWidth) onBorderWidthChange?.(1);
                                            if (!borderRadius) onBorderRadiusChange?.(4);
                                        } else {
                                            // Explicitly set to "no border" (borderWidth: 0)
                                            // This is an OVERRIDE meaning "I want no border"
                                            // Different from RESET which returns to global
                                            onBorderWidthChange?.(0);
                                            // Keep color/radius values in case user re-enables
                                        }
                                    }}
                                    className={`w-4 h-4 rounded border-2 flex items-center justify-center transition-colors
                                        ${effectiveShowBorders
                                            ? 'bg-blue-500 border-blue-500 text-white'
                                            : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800'
                                        }`}
                                >
                                    {effectiveShowBorders && <span className="text-[10px]">✓</span>}
                                </button>
                                <span className="text-[10px] font-medium text-gray-600 dark:text-gray-400">
                                    Add Border
                                </span>
                            </div>

                            {effectiveShowBorders && (
                                <div className="flex items-end gap-2 pl-6">
                                    {/* Border Color */}
                                    <div className="flex flex-col items-center gap-1">
                                        <span className="text-[8px] text-gray-400">Color</span>
                                        <div className="relative">
                                            <input
                                                type="color"
                                                value={borderColor || '#D1D5DB'}
                                                onChange={(e) => onBorderColorChange?.(e.target.value)}
                                                className="w-6 h-6 rounded cursor-pointer border border-gray-300"
                                            />
                                        </div>
                                    </div>

                                    {/* Border Width */}
                                    <div className="flex flex-col gap-1">
                                        <span className="text-[8px] text-gray-400">Width</span>
                                        <select
                                            value={borderWidth?.toString() || '1'}
                                            onChange={(e) => onBorderWidthChange?.(parseInt(e.target.value))}
                                            className="w-12 px-1 py-0.5 text-[10px] border border-gray-300 rounded bg-white"
                                        >
                                            <option value="1">1px</option>
                                            <option value="2">2px</option>
                                            <option value="3">3px</option>
                                            <option value="4">4px</option>
                                        </select>
                                    </div>

                                    {/* Border Radius */}
                                    <div className="flex flex-col gap-1">
                                        <span className="text-[8px] text-gray-400">Radius</span>
                                        <select
                                            value={borderRadius?.toString() || '4'}
                                            onChange={(e) => onBorderRadiusChange?.(parseInt(e.target.value))}
                                            className="w-12 px-1 py-0.5 text-[10px] border border-gray-300 rounded bg-white"
                                        >
                                            <option value="0">0</option>
                                            <option value="2">2</option>
                                            <option value="4">4</option>
                                            <option value="6">6</option>
                                            <option value="8">8</option>
                                        </select>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default TypographyCard;
