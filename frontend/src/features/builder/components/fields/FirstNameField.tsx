import React from 'react';
import { AlertCircle } from 'lucide-react';
import { SmartBorder } from '../ui/SmartBorder';
import { LayoutType } from '../../types/builder.types';
import { ComputedFieldStyles, computeFieldStyles, estimateRequiredInputWidth } from '../../utils/styleUtils';

interface FirstNameFieldProps {
    // Dynamic props from component schema
    label?: string;
    placeholder?: string;
    required?: boolean;
    helpText?: string;
    // Drag props passed from dnd-kit
    dragListeners?: unknown;
    dragAttributes?: unknown;
    setNodeRef?: (node: HTMLElement | null) => void;
    isSelected?: boolean;
    layout?: LayoutType;
    // Global styles passed from parent
    fieldStyles?: ComputedFieldStyles;
    // Container width from parent (for responsive input)
    containerWidth?: string;
    // Input width mode: 'fill' = stretch to container, 'fixed' = explicit width, 'auto' = from maxLength
    inputWidthMode?: 'fill' | 'fixed' | 'auto';
    // Allow label to wrap (default: true)
    labelWrap?: boolean;
    // Text alignment
    textAlign?: 'left' | 'center' | 'right';
}

export const FirstNameField: React.FC<FirstNameFieldProps> = ({ 
    label = 'First Name',
    placeholder = 'Enter your first name',
    required = true,
    helpText: _helpText,
    dragListeners, 
    dragAttributes, 
    setNodeRef,
    isSelected = false,
    layout = 'vertical',
    fieldStyles: externalStyles,
    containerWidth,
    inputWidthMode = 'fill', // Default to fill mode for responsive behavior
    labelWrap = true, // Default to allow wrapping
    textAlign = 'left',
}) => {
    // Use provided styles or compute defaults
    const fieldStyles = externalStyles || computeFieldStyles(undefined);
    const { computed } = fieldStyles;

    const containerWidthPx = containerWidth && containerWidth.endsWith('px')
        ? parseInt(containerWidth, 10)
        : undefined;
    
    // Validation Messages
    const validationMessages = [
        "We only accept names less than 30 Characters",
        "Numbers and Special characters are not allowed"
    ];

    const longestMessage = validationMessages.reduce((a, b) => a.length > b.length ? a : b);

    // Calculate input width based on mode
    const getInputWidth = (): string => {
        switch (inputWidthMode) {
            case 'fill':
                return '100%'; // Fill container width
            case 'fixed':
            case 'auto':
            default:
                return '320px'; // Default width for first name
        }
    };

    const inputWidthValue = getInputWidth();
    const appliedInputWidth = containerWidth || inputWidthValue;

    // Layout classes based on vertical/horizontal
    const isHorizontal = layout === 'horizontal';

    // Build input style with global styles
    const padX = Math.max(1, (computed.paddingX ?? 0) * 0.15);
    const inputStyle: React.CSSProperties = {
        ...fieldStyles.inputStyle,
        width: '100%', // Input fills its container
        paddingLeft: `${padX}px`,
        paddingRight: `${padX}px`,
        textAlign,
    };

    // Width guide (design-time only)
    const maxChars = 30;
    const guideRequiredWidth = estimateRequiredInputWidth({
        maxChars,
        fontFamily: computed.fontFamily,
        fontSize: computed.fontSize,
        fontWeight: computed.fontWeight,
        paddingX: computed.paddingX ?? 0,
        borderWidth: computed.borderWidth ?? 0,
    });
    const guideDisplayWidth = containerWidthPx
        ? Math.min(guideRequiredWidth, containerWidthPx)
        : guideRequiredWidth;
    const guideFill = 'rgba(34, 197, 94, 0.6)';
    const guideBorder = 'rgba(0,0,0,0.35)';

    // Label style from global - with conditional wrapping
    const labelStyle: React.CSSProperties = {
        ...fieldStyles.labelStyle,
        whiteSpace: labelWrap ? 'normal' : 'nowrap',
        wordBreak: labelWrap ? 'break-word' : 'normal',
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

    // Container style - DO NOT apply width here (let SmartBorder hug content)
    const containerStyle: React.CSSProperties = {
        ...fieldStyles.containerStyle,
        display: 'inline-block',
        ...(containerWidth ? { width: containerWidth, maxWidth: containerWidth } : {}),
    };

    // For horizontal layout, use a wrapper since items are side-by-side
    if (isHorizontal) {
        return (
            <div 
                ref={setNodeRef ? (node) => setNodeRef(node as HTMLElement | null) : undefined} 
                style={containerStyle}
            > 
                <SmartBorder key="horizontal" padding={5} dragListeners={dragListeners} dragAttributes={dragAttributes} isSelected={isSelected}>
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
                                    {label} {required && <span style={{ color: computed.errorColor }}>*</span>}
                                </label>
                            </div>
                            <div 
                                className="relative flex-1" 
                                style={{ 
                                    width: inputWidthMode === 'fill' ? undefined : inputWidthValue,
                                    borderRadius: `${computed.borderRadius}px` 
                                }}
                            >
                                {/* Width guide bar (design-time only) */}
                                <div 
                                    style={{ 
                                        position: 'absolute',
                                        left: `${padX + (computed.borderWidth ?? 0)}px`,
                                        right: `${padX + (computed.borderWidth ?? 0)}px`,
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
                                <input type="text" name="first-name" style={inputStyle} className="block w-full focus:outline-none border-0" placeholder={placeholder} disabled readOnly />
                            </div>
                        </div>
                        {/* Bottom row: Help/Validation aligned with input */}
                        <div className="flex flex-row w-full" style={{ gap: `${computed.labelGap}px`, marginTop: `${computed.inputHelpGap}px` }}>
                            {/* Spacer for label column - matches label width */}
                            <div className="flex-shrink-0" style={{ minWidth: '80px' }} />
                            <div className="flex-1">
                                <div style={validationStyle}>
                                    <AlertCircle size={14} className="mr-1 mt-0.5 flex-shrink-0" style={{ color: computed.helpTextColor }} />
                                    <span>{longestMessage}</span>
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
                        {label} {required && <span style={{ color: computed.errorColor }}>*</span>}
                    </label>
                </div>

                {/* 2. Input Area - respects inputWidthMode */}
                <div 
                    className="relative" 
                    style={{ 
                        width: inputWidthMode === 'fill' ? appliedInputWidth : inputWidthValue, 
                        borderRadius: `${computed.borderRadius}px` 
                    }}
                >
                    {/* Width guide bar (design-time only) */}
                    <div 
                        style={{ 
                            position: 'absolute',
                            left: `${padX + (computed.borderWidth ?? 0)}px`,
                            right: `${padX + (computed.borderWidth ?? 0)}px`,
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
                    <input
                        type="text"
                        name="first-name"
                        style={inputStyle}
                        className="block w-full focus:outline-none border-0"
                        placeholder={placeholder}
                        disabled
                        readOnly
                    />
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
                        <span>{longestMessage}</span>
                    </div>
                </div>
            </SmartBorder>
        </div>
    );
};
