/**
 * Style Utilities - Story 3.5
 * 
 * Utilities for computing effective styles from global defaults and component overrides.
 * Supports the "Brand DNA" cascade: Global Styles → Component Overrides → Final Render
 * 
 * CASCADE LOGIC:
 * 1. GlobalStyles are the "brand defaults" - set once, apply everywhere
 * 2. StyleOverrides on individual components ONLY override what's explicitly set
 * 3. Toolbox always shows GlobalStyles (pure brand preview)
 * 4. Canvas components show effective style (merged global + overrides)
 */

import { 
    GlobalStyles, 
    StyleOverrides, 
    DEFAULT_GLOBAL_STYLES,
    FontStyleType,
    StyleArchetype,
} from '../types/builder.types';

/**
 * Computed styles that can be applied directly to DOM elements
 */
export interface ComputedFieldStyles {
    // Container
    containerStyle: React.CSSProperties;
    
    // Label (PrimaryLabel)
    labelStyle: React.CSSProperties;
    
    // Input (InputControl)
    inputStyle: React.CSSProperties;
    inputWrapperStyle: React.CSSProperties;
    
    // Help/Validation text (HelperText)
    helpTextStyle: React.CSSProperties;
    errorTextStyle: React.CSSProperties;
    
    // Action/Button (Action)
    actionStyle?: React.CSSProperties; // Optional, added for Action archetype

    // Computed values for reference (useful for programmatic access)
    computed: {
        // ... (existing computed values)
        // Add new computed values if needed for archetypes
        
        // Input typography
        fontFamily: string;
        fontSize: number;
        fontWeight: number;
        fontStyle: FontStyleType;
        
        // Label typography
        labelFontFamily: string;
        labelFontSize: number;
        labelFontWeight: number;
        labelFontStyle: FontStyleType;
        
        // Help text typography
        helpTextFontFamily: string;
        helpTextFontSize: number;
        helpTextFontWeight: number;
        helpTextFontStyle: FontStyleType;
        
        // Action typography
        actionFontFamily: string;
        actionFontSize: number;
        actionFontWeight: number;
        actionFontStyle: FontStyleType;
        actionTextColor: string;
        actionBackgroundColor: string;

        // Divider styles
        dividerBorderColor: string;
        dividerBorderWidth: number;
        dividerWidth: string;

        // Colors
        primaryColor: string;
        textColor: string;
        labelColor: string;
        placeholderColor: string;
        helpTextColor: string;
        errorColor: string;
        backgroundColor: string;
        borderColor: string;
        
        // Text backgrounds (from Typography cards)
        textBackgroundColor?: string;
        labelBackgroundColor?: string;
        helpTextBackgroundColor?: string;
        
        // Text borders (from Typography cards "Add Border")
        textBorderColor?: string;
        textBorderWidth?: number;
        textBorderRadius?: number;
        
        // Borders & Sizing
        borderRadius: number;
        borderWidth: number;
        inputHeight: number;
        
        // Spacing
        baseSpacing: number;
        labelGap: number;      // Computed px value for label-to-input gap
        inputHelpGap: number;  // Computed px value for input-to-help gap
        paddingX: number;
        paddingY: number;
    };
}

/**
 * Effective styles after merging global with component overrides.
 * This is what actually gets rendered.
 */
export interface EffectiveStyles {
    // Input typography
    fontFamily: string;
    fontSize: number;
    fontWeight: number;
    fontStyle: FontStyleType;
    
    // Label typography (can have different font)
    labelFontFamily: string;
    labelFontSize: number;
    labelFontWeight: number;
    labelFontStyle: FontStyleType;
    
    // Help text typography (can have different font)
    helpTextFontFamily: string;
    helpTextFontSize: number;
    helpTextFontWeight: number;
    helpTextFontStyle: FontStyleType;
    
    // Colors
    primaryColor: string;
    textColor: string;
    labelColor: string;
    placeholderColor: string;
    helpTextColor: string;
    backgroundColor: string;
    borderColor: string;
    errorColor: string;
    
    // Text backgrounds (optional - per text type)
    textBackgroundColor?: string;
    labelBackgroundColor?: string;
    helpTextBackgroundColor?: string;
    
    // Text borders (optional - per text type)
    textHasBorder?: boolean;
    textBorderColor?: string;
    textBorderWidth?: number;
    textBorderRadius?: number;
    labelBorderColor?: string;
    labelBorderWidth?: number;
    labelBorderRadius?: number;
    helpTextBorderColor?: string;
    helpTextBorderWidth?: number;
    helpTextBorderRadius?: number;
    helpTextHasBorder?: boolean;
    
    // Spacing
    baseSpacing: number;
    labelGap: number;
    inputHelpGap: number;
    inputPaddingX: number;
    inputPaddingY: number;
    
    // Borders & Sizing
    borderRadius: number;
    borderWidth: number;
    inputHeight: number;

    // Action/Button typography and styling
    actionFontFamily: string;
    actionFontSize: number;
    actionFontWeight: number;
    actionFontStyle: FontStyleType;
    actionTextColor: string;
    actionBackgroundColor: string;
    actionBorderColor?: string;
    actionBorderWidth?: number;
    actionBorderRadius?: number;

    // Divider
    dividerWidth: string;
    dividerBorderColor?: string;
    dividerBorderWidth?: number;
}

/**
 * Merge global styles with component overrides to get effective values.
 * Uses nullish coalescing (??) to allow falsy values like 0.
 */
export function getEffectiveStyles(
    globalStyles: GlobalStyles | undefined,
    overrides: StyleOverrides | undefined
): EffectiveStyles {
    const base = globalStyles || DEFAULT_GLOBAL_STYLES;
    
    return {
        // Input typography
        fontFamily: overrides?.fontFamily ?? base.fontFamily,
        fontSize: overrides?.fontSize ?? base.fontSize,
        fontWeight: overrides?.fontWeight ?? base.fontWeight,
        fontStyle: overrides?.fontStyle ?? base.fontStyle,
        
        // Label typography (can have different font)
        labelFontFamily: overrides?.labelFontFamily ?? base.labelFontFamily,
        labelFontSize: overrides?.labelFontSize ?? base.labelFontSize,
        labelFontWeight: overrides?.labelFontWeight ?? base.labelFontWeight,
        labelFontStyle: overrides?.labelFontStyle ?? base.labelFontStyle,
        
        // Help text typography (can have different font)
        helpTextFontFamily: overrides?.helpTextFontFamily ?? base.helpTextFontFamily,
        helpTextFontSize: overrides?.helpTextFontSize ?? base.helpTextFontSize,
        helpTextFontWeight: overrides?.helpTextFontWeight ?? base.helpTextFontWeight,
        helpTextFontStyle: overrides?.helpTextFontStyle ?? base.helpTextFontStyle,
        
        // Action/Button typography
        actionFontFamily: overrides?.actionFontFamily ?? base.actionFontFamily,
        actionFontSize: overrides?.actionFontSize ?? base.actionFontSize,
        actionFontWeight: overrides?.actionFontWeight ?? base.actionFontWeight,
        actionFontStyle: overrides?.actionFontStyle ?? base.actionFontStyle,
        actionTextColor: overrides?.actionTextColor ?? base.actionTextColor,
        actionBackgroundColor: overrides?.actionBackgroundColor ?? base.actionBackgroundColor,
        actionBorderColor: overrides?.actionBorderColor ?? base.actionBorderColor,
        actionBorderWidth: overrides?.actionBorderWidth ?? base.actionBorderWidth,
        actionBorderRadius: overrides?.actionBorderRadius ?? base.actionBorderRadius,

        // Divider styles
        dividerBorderColor: overrides?.dividerBorderColor ?? base.dividerBorderColor,
        dividerBorderWidth: overrides?.dividerBorderWidth ?? base.dividerBorderWidth,
        dividerWidth: base.dividerWidth,

        // Colors
        primaryColor: base.primaryColor,
        textColor: overrides?.textColor ?? base.textColor,
        labelColor: overrides?.labelColor ?? base.labelColor,
        placeholderColor: overrides?.placeholderColor ?? base.placeholderColor,
        helpTextColor: overrides?.helpTextColor ?? base.helpTextColor,
        backgroundColor: overrides?.backgroundColor ?? base.backgroundColor,
        borderColor: overrides?.borderColor ?? base.borderColor,
        errorColor: base.errorColor,
        
        // Text backgrounds (allow component overrides - respects undefined as "transparent")
        textBackgroundColor: overrides && 'textBackgroundColor' in overrides ? overrides.textBackgroundColor : base.textBackgroundColor,
        labelBackgroundColor: overrides && 'labelBackgroundColor' in overrides ? overrides.labelBackgroundColor : base.labelBackgroundColor,
        helpTextBackgroundColor: overrides && 'helpTextBackgroundColor' in overrides ? overrides.helpTextBackgroundColor : base.helpTextBackgroundColor,
        
        // Text borders (allow component overrides - respects undefined as "no border")
        textHasBorder: overrides && 'textHasBorder' in overrides ? Boolean(overrides.textHasBorder) : base.textHasBorder,
        textBorderColor: overrides && 'textBorderColor' in overrides ? overrides.textBorderColor : base.textBorderColor,
        textBorderWidth: overrides && 'textBorderWidth' in overrides ? overrides.textBorderWidth : base.textBorderWidth,
        textBorderRadius: overrides && 'textBorderRadius' in overrides ? overrides.textBorderRadius : base.textBorderRadius,
        labelBorderColor: overrides && 'labelBorderColor' in overrides ? overrides.labelBorderColor : base.labelBorderColor,
        labelBorderWidth: overrides && 'labelBorderWidth' in overrides ? overrides.labelBorderWidth : base.labelBorderWidth,
        labelBorderRadius: overrides && 'labelBorderRadius' in overrides ? overrides.labelBorderRadius : base.labelBorderRadius,
        helpTextBorderColor: overrides && 'helpTextBorderColor' in overrides ? overrides.helpTextBorderColor : base.helpTextBorderColor,
        helpTextBorderWidth: overrides && 'helpTextBorderWidth' in overrides ? overrides.helpTextBorderWidth : base.helpTextBorderWidth,
        helpTextBorderRadius: overrides && 'helpTextBorderRadius' in overrides ? overrides.helpTextBorderRadius : base.helpTextBorderRadius,
        helpTextHasBorder: overrides && 'helpTextHasBorder' in overrides ? Boolean(overrides.helpTextHasBorder) : base.helpTextHasBorder,
        
        // Spacing
        baseSpacing: base.baseSpacing,
        labelGap: overrides?.labelGap ?? base.labelGap,
        inputHelpGap: overrides?.inputHelpGap ?? base.inputHelpGap,
        inputPaddingX: base.inputPaddingX,
        inputPaddingY: base.inputPaddingY,
        
        // Borders & Sizing
        borderRadius: overrides?.borderRadius ?? base.borderRadius,
        borderWidth: overrides?.borderWidth ?? base.borderWidth,
        inputHeight: overrides?.inputHeight ?? base.inputHeight,
    };
}

/**
 * Helper to get style properties for a specific archetype.
 * This allows resolving styles based on the object's archetype rather than just context.
 * 
 * @param archetype - The style archetype to resolve
 * @param effective - The effective styles (merged global + overrides)
 * @param scaleFactor - Current scale factor
 * @returns CSSProperties for the requested archetype
 */
export function getArchetypeStyle(
    archetype: StyleArchetype,
    effective: EffectiveStyles,
    scaleFactor: number
): React.CSSProperties {
    switch (archetype) {
        case 'PrimaryLabel':
            return {
                fontFamily: effective.labelFontFamily,
                fontSize: `${Math.round(effective.labelFontSize * scaleFactor)}px`,
                fontWeight: effective.labelFontWeight,
                fontStyle: effective.labelFontStyle,
                color: effective.labelColor,
                // Optional background and border for labels
                backgroundColor: effective.labelBackgroundColor || 'transparent',
                ...(effective.labelBorderColor && (effective.labelBorderWidth ?? 1) > 0 && {
                    borderColor: effective.labelBorderColor,
                    borderWidth: `${Math.round((effective.labelBorderWidth || 1) * scaleFactor)}px`,
                    borderStyle: 'solid',
                    borderRadius: `${Math.round((effective.labelBorderRadius || 4) * scaleFactor)}px`,
                    padding: `${Math.round(2 * scaleFactor)}px ${Math.round(6 * scaleFactor)}px`,
                    display: 'inline-block',
                }),
            };
            
        case 'HelperText':
            return {
                fontFamily: effective.helpTextFontFamily,
                fontSize: `${Math.round(effective.helpTextFontSize * scaleFactor)}px`,
                fontWeight: effective.helpTextFontWeight,
                fontStyle: effective.helpTextFontStyle,
                color: effective.helpTextColor,
                // Optional background and border for help text
                backgroundColor: effective.helpTextBackgroundColor || 'transparent',
                ...(effective.helpTextHasBorder && effective.helpTextBorderColor && (effective.helpTextBorderWidth ?? 1) > 0 && {
                    borderColor: effective.helpTextBorderColor,
                    borderWidth: `${Math.round((effective.helpTextBorderWidth || 1) * scaleFactor)}px`,
                    borderStyle: 'solid',
                    borderRadius: `${Math.round((effective.helpTextBorderRadius || 4) * scaleFactor)}px`,
                    padding: `${Math.round(2 * scaleFactor)}px ${Math.round(6 * scaleFactor)}px`,
                    display: 'inline-block',
                }),
            };
            
        case 'InputControl':
            // Base input text style (without container/border chrome)
            return {
                fontFamily: effective.fontFamily,
                fontSize: `${Math.round(effective.fontSize * scaleFactor)}px`,
                fontWeight: effective.fontWeight,
                fontStyle: effective.fontStyle,
                color: effective.textColor,
                backgroundColor: effective.textBackgroundColor || 'transparent',
            };

        case 'Action':
             // Button/Action style
             return {
                fontFamily: effective.actionFontFamily,
                fontSize: `${Math.round(effective.actionFontSize * scaleFactor)}px`,
                fontWeight: effective.actionFontWeight,
                fontStyle: effective.actionFontStyle,
                color: effective.actionTextColor,
                backgroundColor: effective.actionBackgroundColor,
                borderRadius: `${Math.round((effective.actionBorderRadius ?? effective.borderRadius) * scaleFactor)}px`,
                padding: `${Math.round(10 * scaleFactor)}px ${Math.round(24 * scaleFactor)}px`,
                ...(effective.actionBorderColor && (effective.actionBorderWidth ?? 1) > 0 && {
                    border: `${Math.round((effective.actionBorderWidth || 1) * scaleFactor)}px solid ${effective.actionBorderColor}`,
                }),
             };

        case 'Divider':
            return {
                borderTopWidth: `${Math.round((effective.dividerBorderWidth || 1) * scaleFactor)}px`,
                borderTopColor: effective.dividerBorderColor,
                borderTopStyle: 'solid',
                width: '100%',
                margin: '0',
            };
            
        default:
            return {};
    }
}

/**
 * Compute CSS styles for field components from global styles and optional overrides.
 * 
 * Returns ready-to-use React CSSProperties for each part of a field component:
 * - Container: Overall wrapper
 * - Label: Field label text
 * - Input: The actual input element
 * - Help Text: Assistive text below input
 * - Error Text: Validation error messages
 * 
 * @param globalStyles - The global styles from form definition
 * @param overrides - Component-level style overrides
 * @param componentScale - Proportional scale factor (50-200%, default 100)
 * @param spacingOverrides - Direct pixel overrides for spacing (from resize handles)
 */
export function computeFieldStyles(
    globalStyles: GlobalStyles | undefined,
    overrides?: StyleOverrides,
    componentScale: number = 100,
    spacingOverrides?: { labelGapOverride?: number; inputHelpGapOverride?: number }
): ComputedFieldStyles {
    const effective = getEffectiveStyles(globalStyles, overrides);
    
    // Calculate scale factor (convert percentage to decimal)
    const scaleFactor = Math.max(0.5, Math.min(2, componentScale / 100));
    
    // Compute spacing values (multipliers × base spacing) - apply scale factor
    // If spacing overrides are provided (from resize handles), use them directly
    const baseSpacing = effective.baseSpacing;
    const labelGapPx = spacingOverrides?.labelGapOverride ?? (effective.labelGap * baseSpacing * scaleFactor);
    const inputHelpGapPx = spacingOverrides?.inputHelpGapOverride ?? (effective.inputHelpGap * baseSpacing * scaleFactor);
    const paddingX = effective.inputPaddingX * baseSpacing * scaleFactor;
    const paddingY = effective.inputPaddingY * baseSpacing * scaleFactor;
    
    // Apply scale factor to font sizes
    const scaledFontSize = Math.round(effective.fontSize * scaleFactor);
    const scaledLabelFontSize = Math.round(effective.labelFontSize * scaleFactor);
    const scaledHelpTextFontSize = Math.round(effective.helpTextFontSize * scaleFactor);
    
    // Apply scale factor to input height and border radius
    const scaledInputHeight = Math.round(effective.inputHeight * scaleFactor);
    const scaledBorderRadius = Math.round(effective.borderRadius * scaleFactor);
    
    return {
        containerStyle: {
            fontFamily: effective.fontFamily,
        },
        
        labelStyle: {
            ...getArchetypeStyle('PrimaryLabel', effective, scaleFactor),
            marginBottom: `${labelGapPx}px`,
        },
        
        inputStyle: {
            fontFamily: effective.fontFamily,
            fontSize: `${scaledFontSize}px`,
            fontWeight: effective.fontWeight,
            fontStyle: effective.fontStyle,
            color: effective.textColor,
            position: 'relative',
            zIndex: 1,
            // Default to 100% width so input fills its container (grid cell)
            width: '100%',
            boxSizing: 'border-box', // Ensure padding/border are included in width
            // Apply text background if set in Typography > Input Text
            backgroundColor: effective.textBackgroundColor || 'transparent',
            // Border rules:
            // - When textHasBorder is false, no border (borderWidth 0).
            // - Prefer Typography > Input Text border overrides when provided (textBorder*).
            // - Otherwise fall back to the global/default input border (borderColor/borderWidth/borderRadius).
            // - Never use `border` shorthand here; mixing shorthand/non-shorthand triggers React warnings
            //   when callers spread and override border* fields (e.g. dropdown styles).
            borderColor: effective.textHasBorder ? (effective.textBorderColor ?? effective.borderColor) : 'transparent',
            borderWidth: effective.textHasBorder
                ? `${Math.max(0, Math.round(((effective.textBorderWidth ?? effective.borderWidth) || 0) * scaleFactor))}px`
                : '0px',
            borderStyle: 'solid',
            borderRadius: `${Math.round((effective.textBorderRadius ?? effective.borderRadius) * scaleFactor)}px`,
            height: `${scaledInputHeight}px`,
            paddingLeft: `${paddingX}px`,
            paddingRight: `${paddingX}px`,
            paddingTop: `${paddingY}px`,
            paddingBottom: `${paddingY}px`,
            outline: 'none', // Remove outline
            appearance: 'none', // Remove native browser styling
            WebkitAppearance: 'none', // Safari support
            boxShadow: 'none', // Remove any remaining shadows
        } as React.CSSProperties,
        
        inputWrapperStyle: {
            // For inputs with icons, we add extra left padding
        },
        
        helpTextStyle: {
            ...getArchetypeStyle('HelperText', effective, scaleFactor),
            marginTop: `${inputHelpGapPx}px`,
        },
        
        errorTextStyle: {
            ...getArchetypeStyle('HelperText', effective, scaleFactor),
            color: effective.errorColor,
            marginTop: `${baseSpacing * scaleFactor * 0.5}px`,
        },
        
        // New Action Style exposed for use
        actionStyle: getArchetypeStyle('Action', effective, scaleFactor),
        
        computed: {
            // Input typography (scaled)
            fontFamily: effective.fontFamily,
            fontSize: scaledFontSize,
            fontWeight: effective.fontWeight,
            fontStyle: effective.fontStyle,
            
            // Label typography (scaled)
            labelFontFamily: effective.labelFontFamily,
            labelFontSize: scaledLabelFontSize,
            labelFontWeight: effective.labelFontWeight,
            labelFontStyle: effective.labelFontStyle,
            
            // Help text typography (scaled)
            helpTextFontFamily: effective.helpTextFontFamily,
            helpTextFontSize: scaledHelpTextFontSize,
            helpTextFontWeight: effective.helpTextFontWeight,
            helpTextFontStyle: effective.helpTextFontStyle,
            
            // Action typography (scaled)
            actionFontFamily: effective.actionFontFamily,
            actionFontSize: Math.round(effective.actionFontSize * scaleFactor),
            actionFontWeight: effective.actionFontWeight,
            actionFontStyle: effective.actionFontStyle,
            actionTextColor: effective.actionTextColor,
            actionBackgroundColor: effective.actionBackgroundColor,

            // Divider styles
            dividerBorderColor: effective.dividerBorderColor ?? '',
            dividerBorderWidth: Math.round((effective.dividerBorderWidth ?? 1) * scaleFactor),
            dividerWidth: effective.dividerWidth,

            // Colors
            primaryColor: effective.primaryColor,
            textColor: effective.textColor,
            labelColor: effective.labelColor,
            placeholderColor: effective.placeholderColor,
            helpTextColor: effective.helpTextColor,
            errorColor: effective.errorColor,
            backgroundColor: effective.backgroundColor,
            borderColor: effective.borderColor,
            
            // Text backgrounds (from Typography cards)
            textBackgroundColor: effective.textBackgroundColor,
            labelBackgroundColor: effective.labelBackgroundColor,
            helpTextBackgroundColor: effective.helpTextBackgroundColor,
            
            // Text borders (from Typography cards "Add Border")
            textBorderColor: effective.textBorderColor,
            textBorderWidth: effective.textBorderWidth ? Math.round(effective.textBorderWidth * scaleFactor) : undefined,
            textBorderRadius: effective.textBorderRadius ? Math.round(effective.textBorderRadius * scaleFactor) : undefined,
            
            // Borders & Sizing (scaled)
            borderRadius: scaledBorderRadius,
            borderWidth: Math.round(effective.borderWidth * scaleFactor),
            inputHeight: scaledInputHeight,
            
            // Spacing (scaled)
            baseSpacing: effective.baseSpacing,
            labelGap: labelGapPx,
            inputHelpGap: inputHelpGapPx,
            paddingX: paddingX,
            paddingY: paddingY,
        },
    };
}

/**
 * Generate placeholder CSS with the correct color
 */
export function getPlaceholderStyle(placeholderColor: string): string {
    return `
        ::placeholder {
            color: ${placeholderColor};
            opacity: 1;
        }
    `;
}

/**
 * Generate focus styles based on primary color
 */
export function getFocusStyles(primaryColor: string): React.CSSProperties {
    return {
        outline: 'none',
        borderColor: primaryColor,
        boxShadow: `0 0 0 2px ${primaryColor}33`, // 20% opacity
    };
}

/**
 * Check if a component has any style overrides.
 * Used to determine if warning should be shown on global style changes.
 */
export function hasStyleOverrides(overrides: StyleOverrides | undefined): boolean {
    if (!overrides) return false;
    return Object.values(overrides).some(value => value !== undefined);
}

/**
 * Get list of property names that have been overridden on a component.
 * Useful for displaying which properties will be affected by global changes.
 */
export function getOverriddenProperties(overrides: StyleOverrides | undefined): string[] {
    if (!overrides) return [];
    return Object.entries(overrides)
        .filter(([, value]) => value !== undefined)
        .map(([key]) => key);
}

/**
 * Human-readable labels for style override properties
 */
export const OVERRIDE_PROPERTY_LABELS: Record<string, string> = {
    // Input typography
    fontFamily: 'Input Font Family',
    fontSize: 'Input Font Size',
    fontWeight: 'Input Font Weight',
    fontStyle: 'Input Font Style',
    
    // Label typography
    labelFontFamily: 'Label Font Family',
    labelFontSize: 'Label Font Size',
    labelFontWeight: 'Label Font Weight',
    labelFontStyle: 'Label Font Style',
    
    // Help text typography
    helpTextFontFamily: 'Help Text Font Family',
    helpTextFontSize: 'Help Text Font Size',
    helpTextFontWeight: 'Help Text Font Weight',
    helpTextFontStyle: 'Help Text Font Style',
    
    // Action/Button styles
    actionFontFamily: 'Button Font Family',
    actionFontSize: 'Button Font Size',
    actionFontWeight: 'Button Font Weight',
    actionFontStyle: 'Button Font Style',
    actionTextColor: 'Button Text Color',
    actionBackgroundColor: 'Button Background Color',
    actionBorderColor: 'Button Border Color',
    actionBorderWidth: 'Button Border Width',
    actionBorderRadius: 'Button Border Radius',

    // Divider styles
    dividerBorderColor: 'Divider Color',
    dividerBorderWidth: 'Divider Thickness',

    // Colors
    textColor: 'Input Text Color',
    labelColor: 'Label Color',
    placeholderColor: 'Placeholder Color',
    helpTextColor: 'Help Text Color',
    backgroundColor: 'Background Color',
    borderColor: 'Border Color',
    
    // Borders & Sizing
    borderRadius: 'Border Radius',
    borderWidth: 'Border Width',
    inputHeight: 'Input Height',
};

/**
 * Calculate optimal input width based on maxLength validation
 * 
 * This creates a more professional appearance by sizing inputs
 * appropriately for their expected content.
 * 
 * @param maxLength - Maximum character length from validation rules
 * @param fontSize - Font size in pixels
 * @param defaultWidth - Default width if no maxLength specified
 * @returns Calculated width in pixels
 */
export function calculateInputWidth(
    maxLength: number | undefined,
    fontSize: number = 14,
    defaultWidth: number = 320
): number {
    if (!maxLength || maxLength <= 0) {
        return defaultWidth;
    }
    
    // Average character width is approximately 0.55 of font size for most fonts
    // This varies by font but works well for common UI fonts
    const avgCharWidth = fontSize * 0.55;
    
    // Add padding for cursor, borders, and breathing room
    const horizontalPadding = 24; // 12px each side
    
    // Calculate the width needed
    const calculatedWidth = (maxLength * avgCharWidth) + horizontalPadding;
    
    // Clamp between reasonable min and max values
    const minWidth = 80;  // Minimum usable input width
    const maxWidth = 600; // Maximum before it becomes unwieldy
    
    return Math.min(Math.max(calculatedWidth, minWidth), maxWidth);
}

/**
 * Get input width style string based on maxLength
 * Returns 'auto' or a pixel value
 */
export function getInputWidthStyle(
    maxLength: number | undefined,
    fontSize: number = 14,
    defaultWidth: number = 320
): string {
    const width = calculateInputWidth(maxLength, fontSize, defaultWidth);
    return `${width}px`;
}

/**
 * Measure average character width for a given font using an offscreen canvas.
 * This is used for design-time width guidance (not rendered in production).
 */
export function measureAverageCharWidth(
    fontFamily: string,
    fontSize: number,
    fontWeight: number
): number {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        // Fallback heuristic if canvas is unavailable
        return fontSize * 0.55;
    }

    // Build a synthetic sample with mixed characters (100 chars)
    const sampleChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !?.,:-';
    let sample = '';
    for (let i = 0; i < 100; i++) {
        sample += sampleChars[Math.floor(Math.random() * sampleChars.length)];
    }

    ctx.font = `${fontWeight} ${fontSize}px ${fontFamily}`;
    const width = ctx.measureText(sample).width;
    return width / sample.length;
}

/**
 * Estimate required visible width for an input given max chars and padding/border.
 */
export function estimateRequiredInputWidth(opts: {
    maxChars: number;
    fontFamily: string;
    fontSize: number;
    fontWeight: number;
    paddingX: number;
    borderWidth: number;
}): number {
    const { maxChars, fontFamily, fontSize, fontWeight, paddingX, borderWidth } = opts;
    const avgCharWidth = measureAverageCharWidth(fontFamily, fontSize, fontWeight);
    const contentWidth = avgCharWidth * maxChars;
    const horizontalChrome = (paddingX * 2) + (borderWidth * 2);
    // Clamp to a reasonable range for design-time guidance
    const minWidth = 80;
    const maxWidth = 1200;
    return Math.min(Math.max(contentWidth + horizontalChrome, minWidth), maxWidth);
}

export default {
    getEffectiveStyles,
    computeFieldStyles,
    getPlaceholderStyle,
    getFocusStyles,
    hasStyleOverrides,
    getOverriddenProperties,
    OVERRIDE_PROPERTY_LABELS,
    calculateInputWidth,
    getInputWidthStyle,
    measureAverageCharWidth,
    estimateRequiredInputWidth,
};

