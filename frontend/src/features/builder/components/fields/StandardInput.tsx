import React, { useEffect, useRef, useState } from 'react';
import { AlertCircle, HelpCircle, LucideIcon } from 'lucide-react';
import { SmartBorder } from '../ui/SmartBorder';
import { AlignType, LayoutType, ValidationRules } from '../../types/builder.types';
import { ComputedFieldStyles, computeFieldStyles, calculateInputWidth, estimateRequiredInputWidth } from '../../utils/styleUtils';

interface StandardInputProps {
    label: string;
    icon?: LucideIcon | React.ReactNode;
    placeholder?: string;
    validationMessage?: string;
    helpText?: string;
    required?: boolean;
    type?: 'text' | 'number' | 'email' | 'textarea' | 'select' | 'date';
    options?: { label: string; value: string }[];
    layout?: LayoutType;
    isSelected?: boolean;
    // Global styles passed from parent
    fieldStyles?: ComputedFieldStyles;
    // Validation rules for smart sizing
    validation?: ValidationRules;
    // Container width from parent (for responsive input)
    containerWidth?: string;
    // Input width mode: 'fill' = stretch to container, 'fixed' = explicit width, 'auto' = from maxLength
    inputWidthMode?: 'fill' | 'fixed' | 'auto';
    // Explicit input width (when mode = 'fixed')
    inputWidth?: number;
    // Allow label to wrap (default: true)
    labelWrap?: boolean;
    // Explicit height for textarea
    height?: number;
    // Text alignment
    textAlign?: AlignType;
    // Drag props from dnd-kit
    dragListeners?: unknown;
    dragAttributes?: unknown;
    setNodeRef?: (node: HTMLElement | null) => void;
}

export const StandardInput: React.FC<StandardInputProps> = ({ 
    label, 
    icon: _Icon, 
    placeholder = "Input text...", 
    validationMessage = "Validation error message",
    helpText,
    required = false,
    type = 'text',
    options,
    layout = 'vertical',
    isSelected = false,
    fieldStyles: externalStyles,
    validation,
    containerWidth,
    inputWidthMode = 'fill', // Default to fill mode for responsive behavior
    inputWidth: explicitInputWidth,
    labelWrap = true, // Default to allow wrapping
    height,
    textAlign,
    dragListeners,
    dragAttributes,
    setNodeRef
}) => {
    // Use provided styles or compute defaults
    const fieldStyles = externalStyles || computeFieldStyles(undefined);
    const { computed } = fieldStyles;

    const alignValue = textAlign ?? 'left';
    // Temporarily disable icons to rule out phantom spacing issues
    const iconForRender = undefined;
    const hasIcon = !!iconForRender;
    // Visual padding applied to inputs; keep minimal unless an icon is present
    const visualPaddingX = hasIcon ? 40 : Math.max(1, (computed.paddingX ?? 0) * 0.15);
    // State for showing help text tooltip
    const [showHelpTooltip, setShowHelpTooltip] = useState(false);
    const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>(null);
    const [inputRenderedWidth, setInputRenderedWidth] = useState(0);

    // Parse numeric container width if provided (px only)
    const containerWidthPx = containerWidth && containerWidth.endsWith('px')
        ? parseInt(containerWidth, 10)
        : undefined;

    // Calculate input width based on mode
    const getInputWidth = (): string => {
        switch (inputWidthMode) {
            case 'fill':
                return '100%'; // Fill container width
            case 'fixed':
                return `${explicitInputWidth || 300}px`;
            case 'auto':
            default:
                // Calculate from maxLength or default
                const smartWidth = calculateInputWidth(validation?.maxLength, computed.fontSize, 320);
                return `${smartWidth}px`;
        }
    };

    const inputWidthValue = getInputWidth();
    const appliedInputWidth = containerWidth || inputWidthValue;
    const effectiveHeightForRender = type === 'textarea'
        ? (height ?? computed.inputHeight)
        : height;

    const defaultMaxLengthMap: Record<string, number> = {
        'first-name': 30,
        text: 50,
        number: 12,
        email: 254,
        textarea: 500,
        phone: 20,
    };

    // Width guide (design-time only)
    const maxChars = validation?.maxLength && validation.maxLength > 0
        ? validation.maxLength
        : (defaultMaxLengthMap[type] ?? 30);
    const effectiveMaxLength = maxChars > 0 ? maxChars : undefined;

    const guideRequiredWidth = estimateRequiredInputWidth({
        maxChars,
        fontFamily: computed.fontFamily,
        fontSize: computed.fontSize,
        fontWeight: computed.fontWeight,
        paddingX: computed.paddingX ?? 0,
        borderWidth: computed.borderWidth ?? 0,
    });

    // Track rendered input width for guides/line estimation
    useEffect(() => {
        if (inputRef.current) {
            setInputRenderedWidth(inputRef.current.offsetWidth);
        }
    }, [inputWidthValue, containerWidth, computed.inputHeight]);

    // Long text line estimation (for textarea)
    const approximateCharWidth = (computed.fontSize || 14) * 0.55;
    const chromeWidth = (visualPaddingX + (computed.borderWidth ?? 0)) * 2;
    const usableWidth = Math.max(40, (inputRenderedWidth || parseInt(appliedInputWidth) || 320) - chromeWidth);
    const charsPerLine = Math.max(1, Math.floor(usableWidth / approximateCharWidth));
    const lineEstimate = type === 'textarea'
        ? {
            needed: Math.max(1, Math.ceil(maxChars / charsPerLine)),
            fits: (() => {
                const lineHeight = (computed.fontSize || 14) * 1.4;
                const effectiveHeight = height ?? computed.inputHeight ?? 100;
                return Math.max(0, Math.floor(effectiveHeight / lineHeight));
            })(),
        }
        : undefined;

    const guideDisplayWidth = containerWidthPx
        ? Math.min(guideRequiredWidth, containerWidthPx)
        : guideRequiredWidth;

    const hexToRgb = (hex?: string) => {
        if (!hex) return null;
        const normalized = hex.replace('#', '');
        if (normalized.length === 3) {
            const r = parseInt(normalized[0] + normalized[0], 16);
            const g = parseInt(normalized[1] + normalized[1], 16);
            const b = parseInt(normalized[2] + normalized[2], 16);
            return { r, g, b };
        }
        if (normalized.length === 6) {
            const r = parseInt(normalized.slice(0, 2), 16);
            const g = parseInt(normalized.slice(2, 4), 16);
            const b = parseInt(normalized.slice(4, 6), 16);
            return { r, g, b };
        }
        return null;
    };

    const luminance = (rgb: { r: number; g: number; b: number } | null) => {
        if (!rgb) return 0;
        const toLin = (c: number) => {
            const v = c / 255;
            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        };
        return 0.2126 * toLin(rgb.r) + 0.7152 * toLin(rgb.g) + 0.0722 * toLin(rgb.b);
    };

    const guideRgb = hexToRgb('#22c55e');
    const bgRgb = hexToRgb(computed.textBackgroundColor || computed.backgroundColor || '');
    const contrast = Math.abs(luminance(guideRgb) - luminance(bgRgb));
    const guideFill = contrast < 0.2 ? 'rgba(34, 197, 94, 0.3)' : 'rgba(34, 197, 94, 0.6)';
    const guideBorder = 'rgba(0,0,0,0.35)';

    // Layout classes based on vertical/horizontal
    const isHorizontal = layout === 'horizontal';

    // Label style from global - now with conditional wrapping
    const labelStyle: React.CSSProperties = {
        ...fieldStyles.labelStyle,
        whiteSpace: labelWrap ? 'normal' : 'nowrap',
        wordBreak: labelWrap ? 'break-word' : 'normal',
        display: 'flex',
        flexWrap: labelWrap ? 'wrap' : 'nowrap',
        alignItems: 'center',
        gap: '4px',
        marginBottom: isHorizontal ? 0 : `${computed.labelGap}px`,
    };

    // Validation/help text style - also with wrapping support
    const validationStyle: React.CSSProperties = {
        ...fieldStyles.helpTextStyle,
        opacity: 0.7,
        display: 'flex',
        alignItems: 'flex-start',
        wordBreak: 'break-word',
    };

    // Debug logging for spacing/alignment inspection
    useEffect(() => {
        console.log('[debug.input.structure]', {
            label,
            type,
            hasIcon,
            visualPaddingX,
            textAlign: alignValue,
            labelStyle,
            inputPaddingX: visualPaddingX,
        });
    }, [label, type, hasIcon, visualPaddingX, alignValue, labelStyle]);
    
    // Help text tooltip style
    const helpTooltipStyle: React.CSSProperties = {
        ...fieldStyles.helpTextStyle,
        position: 'absolute',
        bottom: '100%',
        left: '0',
        marginBottom: '4px',
        padding: '6px 10px',
        backgroundColor: '#1F2937',
        color: '#F9FAFB',
        borderRadius: '6px',
        fontSize: '12px',
        whiteSpace: 'nowrap',
        zIndex: 50,
        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
        opacity: showHelpTooltip ? 1 : 0,
        visibility: showHelpTooltip ? 'visible' : 'hidden',
        transition: 'opacity 0.2s, visibility 0.2s',
    };

    // Container style - DO NOT apply width here (let SmartBorder hug content)
    const containerStyle: React.CSSProperties = {
        ...fieldStyles.containerStyle,
        display: 'inline-block',
        ...(containerWidth ? { width: containerWidth, maxWidth: containerWidth } : {}),
    };

    // For vertical layout, pass children separately so SmartBorder can "hug" each section
    // For horizontal layout, use a wrapper since items are side-by-side
    if (isHorizontal) {
        return (
            <div 
                ref={setNodeRef ? (node) => setNodeRef(node as HTMLElement | null) : undefined} 
                style={containerStyle}
            > 
                <SmartBorder key="horizontal" padding={5} dragListeners={dragListeners} dragAttributes={dragAttributes} isSelected={isSelected}>
                    {/* Horizontal: Label and Input side by side */}
                    <div className="flex flex-col">
                        {/* Top row: Label + Input aligned */}
                        <div className="flex flex-row items-center w-full" style={{ gap: `${computed.labelGap}px` }}>
                            <div 
                                className="flex items-center flex-shrink-0" 
                                style={{ 
                                    minWidth: '80px',
                                    height: `${computed.inputHeight}px` 
                                }}
                            >
                                <label style={labelStyle}>
                                    {label}
                                    {required && <span style={{ color: computed.errorColor }}>*</span>}
                                    {helpText && (
                                        <HelpCircle 
                                            size={12} 
                                            className="ml-1 text-gray-400 cursor-help flex-shrink-0" 
                                            title={helpText}
                                        />
                                    )}
                                </label>
                            </div>
                            <div 
                                className="relative flex-1" 
                                style={{ 
                                    width: inputWidthMode === 'fill' ? undefined : inputWidthValue,
                                    borderRadius: `${computed.borderRadius}px` 
                                }}
                                onMouseEnter={() => helpText && setShowHelpTooltip(true)}
                                onMouseLeave={() => setShowHelpTooltip(false)}
                                onFocus={() => helpText && setShowHelpTooltip(true)}
                                onBlur={() => setShowHelpTooltip(false)}
                            >
                                {/* Help text tooltip */}
                                {helpText && (
                                    <div style={helpTooltipStyle}>
                                        {helpText}
                                    </div>
                                )}
                                {renderInputControl(
                                    type,
                                    placeholder,
                                    iconForRender,
                                    options,
                                    fieldStyles,
                                    effectiveHeightForRender,
                                    effectiveMaxLength,
                                    lineEstimate,
                                    inputRef,
                                    alignValue,
                                    visualPaddingX
                                )}
                                {/* Width guide bar (design-time only) */}
                                <div 
                                    style={{ 
                                        position: 'absolute',
                                        left: `${visualPaddingX + (computed.borderWidth ?? 0)}px`,
                                        right: `${visualPaddingX + (computed.borderWidth ?? 0)}px`,
                                        bottom: `${Math.max(2, (computed.paddingY ?? 0) * 0.3)}px`,
                                        pointerEvents: 'none',
                                        height: 8,
                                        border: `1px solid ${guideBorder}`,
                                        borderRadius: 4,
                                        overflow: 'hidden',
                                        backgroundColor: 'transparent',
                                        zIndex: 3,
                                    }}
                                >
                                    <div 
                                        style={{ 
                                            height: '100%',
                                            width: `${guideDisplayWidth}px`,
                                            maxWidth: '100%',
                                            backgroundColor: guideFill,
                                        }}
                                    />
                                </div>
                            </div>
                        </div>
                        {/* Bottom row: Help/Validation aligned with input */}
                        <div className="flex flex-row w-full" style={{ gap: `${computed.labelGap}px`, marginTop: `${computed.inputHelpGap}px` }}>
                            {/* Spacer for label column - matches label width */}
                            <div className="flex-shrink-0" style={{ minWidth: '80px' }} />
                            <div className="flex-1">
                                <div style={validationStyle}>
                                    <AlertCircle size={14} className="mr-1 mt-0.5 flex-shrink-0" style={{ color: computed.helpTextColor }} />
                                    <span>{validationMessage}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </SmartBorder>
            </div>
        );
    }

    // Vertical layout: Pass each section as separate child for smart hugging border
    return (
        <div 
            ref={setNodeRef ? (node) => setNodeRef(node as HTMLElement | null) : undefined} 
            style={containerStyle}
        > 
            <SmartBorder key="vertical" padding={5} dragListeners={dragListeners} dragAttributes={dragAttributes} isSelected={isSelected}>
                {/* 1. Label Area - allow wrapping when container is narrow */}
                <div style={{ width: 'auto' }}>
                    <label style={labelStyle}>
                        {label}
                        {required && <span style={{ color: computed.errorColor }}>*</span>}
                        {helpText && (
                            <HelpCircle 
                                size={12} 
                                className="ml-1 text-gray-400 cursor-help flex-shrink-0" 
                                title={helpText}
                            />
                        )}
                    </label>
                </div>

                {/* 2. Input Area - respects inputWidthMode */}
                <div 
                    className="relative" 
                    style={{ 
                        width: inputWidthMode === 'fill' ? appliedInputWidth : inputWidthValue,
                        borderRadius: `${computed.borderRadius}px` 
                    }}
                    onMouseEnter={() => helpText && setShowHelpTooltip(true)}
                    onMouseLeave={() => setShowHelpTooltip(false)}
                    onFocus={() => helpText && setShowHelpTooltip(true)}
                    onBlur={() => setShowHelpTooltip(false)}
                >
                    {/* Help text tooltip */}
                    {helpText && (
                        <div style={helpTooltipStyle}>
                            {helpText}
                        </div>
                    )}
                    {renderInputControl(
                        type,
                        placeholder,
                        iconForRender,
                        options,
                        fieldStyles,
                        effectiveHeightForRender,
                        effectiveMaxLength,
                        lineEstimate,
                        inputRef,
                        alignValue,
                        visualPaddingX
                    )}
                    {/* Width guide bar (design-time only) */}
                    <div 
                        style={{ 
                            position: 'absolute',
                            left: `${visualPaddingX + (computed.borderWidth ?? 0)}px`,
                            right: `${visualPaddingX + (computed.borderWidth ?? 0)}px`,
                            bottom: `${Math.max(2, (computed.paddingY ?? 0) * 0.3)}px`,
                            pointerEvents: 'none',
                            height: 8,
                            border: `1px solid ${guideBorder}`,
                            borderRadius: 4,
                            overflow: 'hidden',
                            backgroundColor: 'transparent',
                            zIndex: 3,
                        }}
                    >
                        <div 
                            style={{ 
                                height: '100%',
                                width: `${guideDisplayWidth}px`,
                                maxWidth: '100%',
                                backgroundColor: guideFill,
                            }}
                        />
                    </div>
                </div>

                {/* 3. Validation Area - also respects container width */}
                <div style={{ 
                    width: 'auto',
                    maxWidth: appliedInputWidth,
                    marginTop: `${computed.inputHelpGap}px` 
                }}>
                    <div style={validationStyle}>
                        <AlertCircle 
                            size={14} 
                            className="mr-1 mt-0.5 flex-shrink-0" 
                            style={{ color: computed.helpTextColor }}
                        />
                        <span>{validationMessage}</span>
                    </div>
                </div>
            </SmartBorder>
        </div>
    );
};

// Helper to render different input types with global styles
const renderInputControl = (
    type: string, 
    placeholder: string, 
    Icon: LucideIcon | React.ReactNode | undefined, 
    _options: { label: string; value: string }[] | undefined,
    fieldStyles: ComputedFieldStyles,
    explicitHeight?: number,
    maxLength?: number,
    lineEstimate?: { needed: number; fits: number },
    inputRef?: React.RefObject<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
    align?: AlignType,
    visualPaddingX?: number
) => {
    const { computed, inputStyle } = fieldStyles;
    
    // Build input style with conditional padding for icon
    const hasIcon = !!Icon;
    const padX = visualPaddingX ?? (hasIcon ? 40 : Math.max(1, (computed.paddingX ?? 0) * 0.15));
    const inputWithIconStyle: React.CSSProperties = {
        ...inputStyle,
        width: '100%',
        paddingLeft: `${padX}px`,
        paddingRight: `${padX}px`,
        display: 'block',
        position: 'relative',
        zIndex: 1,
        textAlign: align ?? 'left',
    };
    
    // Handle Icon rendering safely
    const iconElement = Icon && (React.isValidElement(Icon) 
        ? Icon 
        : typeof Icon === 'function' 
            ? React.createElement(Icon as LucideIcon, { 
                className: "h-4 w-4",
                style: { color: computed.placeholderColor }
              })
            : null
    );

    if (type === 'textarea') {
        const textareaHeight = explicitHeight || computed.inputHeight || 100;
        return (
            <div className="relative">
                {iconElement && (
                    <div 
                        className="absolute top-3 left-3 pointer-events-none"
                        style={{ color: computed.placeholderColor }}
                    >
                        {iconElement}
                    </div>
                )}
                <textarea
                    ref={inputRef as React.RefObject<HTMLTextAreaElement>}
                    style={{ ...inputWithIconStyle, height: `${textareaHeight}px`, resize: 'none' }}
                    className="focus:outline-none border-0"
                    placeholder={placeholder}
                    maxLength={maxLength && maxLength > 0 ? maxLength : undefined}
                    readOnly
                    disabled
                />
                {lineEstimate && (
                    <div
                        style={{
                            position: 'absolute',
                            right: 6,
                            bottom: 6,
                            fontSize: Math.max(10, computed.fontSize - 2),
                            color: lineEstimate.fits >= lineEstimate.needed ? '#166534' : '#0f172a',
                            backgroundColor: lineEstimate.fits >= lineEstimate.needed
                                ? 'rgba(34,197,94,0.15)'
                                : 'rgba(255,255,255,0.9)',
                            border: lineEstimate.fits >= lineEstimate.needed
                                ? '1px solid rgba(34,197,94,0.45)'
                                : '1px solid rgba(0,0,0,0.15)',
                            borderRadius: 6,
                            padding: '2px 6px',
                            pointerEvents: 'none',
                            zIndex: 4,
                        }}
                    >
                        ~ {lineEstimate.needed} lines for max length{lineEstimate.fits > 0 ? ` (fits ~${lineEstimate.fits})` : ''}
                    </div>
                )}
            </div>
        );
    }

    if (type === 'select') {
        return (
            <div className="relative">
                {iconElement && (
                    <div 
                        className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
                        style={{ color: computed.placeholderColor }}
                    >
                        {iconElement}
                    </div>
                )}
                <div 
                    style={{ ...inputWithIconStyle, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                >
                    <span style={{ color: computed.placeholderColor }}>{placeholder}</span>
                    <span style={{ color: computed.placeholderColor }}>{'\u25BC'}</span>
                </div>
            </div>
        );
    }

    // Default Text/Number/Date
    return (
        <div className="relative">
            {iconElement && (
                <div 
                    className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
                    style={{ color: computed.placeholderColor }}
                >
                    {iconElement}
                </div>
            )}
            <input
                ref={inputRef as React.RefObject<HTMLInputElement>}
                type={type === 'number' ? 'text' : type}
                style={inputWithIconStyle}
                className="focus:outline-none border-0"
                placeholder={placeholder}
                maxLength={maxLength && maxLength > 0 ? maxLength : undefined}
                readOnly
                disabled
            />
        </div>
    );
};
