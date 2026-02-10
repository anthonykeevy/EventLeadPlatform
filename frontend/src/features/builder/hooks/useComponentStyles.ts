/**
 * useComponentStyles Hook
 * 
 * Centralized style resolution for all form components.
 * Resolves styles with proper precedence: component override > global > default
 * 
 * This hook ensures consistent styling across all components and guarantees
 * WYSIWYG between builder and preview.
 */

import { useMemo } from 'react';
import type { StyleOverrides, GlobalStyles } from '../types/builder.types';
import { DEFAULT_GLOBAL_STYLES, resolveStyleProperty } from '../types/builder.types';

export interface ResolvedStyles {
  label: React.CSSProperties;
  input: React.CSSProperties;
  helpText: React.CSSProperties;
  gap: {
    labelGap: number;
    inputHelpGap: number;
  };
}

/**
 * Resolve a style property with proper precedence
 */
function resolveStyle<K extends keyof StyleOverrides>(
  styleOverrides: StyleOverrides | undefined,
  globalStyles: GlobalStyles | undefined,
  property: K
): StyleOverrides[K] | GlobalStyles[keyof GlobalStyles] | undefined {
  const effectiveGlobalStyles = globalStyles ?? DEFAULT_GLOBAL_STYLES;
  return resolveStyleProperty(styleOverrides, effectiveGlobalStyles, property);
}

/**
 * Build label styles from styleOverrides and globalStyles
 */
function buildLabelStyles(
  styleOverrides: StyleOverrides | undefined,
  globalStyles: GlobalStyles | undefined
): React.CSSProperties {
  const fontFamily = resolveStyle(styleOverrides, globalStyles, 'labelFontFamily') as string | undefined;
  const fontSize = resolveStyle(styleOverrides, globalStyles, 'labelFontSize') as number | undefined;
  const fontWeight = resolveStyle(styleOverrides, globalStyles, 'labelFontWeight') as number | undefined;
  const fontStyle = resolveStyle(styleOverrides, globalStyles, 'labelFontStyle') as string | undefined;
  const color = resolveStyle(styleOverrides, globalStyles, 'labelColor') as string | undefined;
  const backgroundColor = resolveStyle(styleOverrides, globalStyles, 'labelBackgroundColor') as string | undefined;
  const borderColor = resolveStyle(styleOverrides, globalStyles, 'labelBorderColor') as string | undefined;
  const borderWidth = resolveStyle(styleOverrides, globalStyles, 'labelBorderWidth') as number | undefined;
  const borderRadius = resolveStyle(styleOverrides, globalStyles, 'labelBorderRadius') as number | undefined;
  
  return {
    fontFamily: fontFamily,
    fontSize: fontSize ? `${fontSize}px` : undefined,
    fontWeight: fontWeight,
    fontStyle: fontStyle,
    color: color,
    backgroundColor: backgroundColor,
    borderColor: borderColor,
    borderWidth: borderWidth ? `${borderWidth}px` : undefined,
    borderRadius: borderRadius ? `${borderRadius}px` : undefined,
    borderStyle: borderWidth ? 'solid' : undefined,
    padding: borderWidth ? '2px 4px' : undefined,
  };
}

/**
 * Build input styles from styleOverrides and globalStyles
 */
function buildInputStyles(
  styleOverrides: StyleOverrides | undefined,
  globalStyles: GlobalStyles | undefined,
  disabled: boolean
): React.CSSProperties {
  const _effectiveGlobalStyles = globalStyles ?? DEFAULT_GLOBAL_STYLES;
  
  const fontFamily = resolveStyle(styleOverrides, globalStyles, 'fontFamily') as string | undefined;
  const fontSize = resolveStyle(styleOverrides, globalStyles, 'fontSize') as number | undefined;
  const fontWeight = resolveStyle(styleOverrides, globalStyles, 'fontWeight') as number | undefined;
  const fontStyle = resolveStyle(styleOverrides, globalStyles, 'fontStyle') as string | undefined;
  const textColor = resolveStyle(styleOverrides, globalStyles, 'textColor') as string | undefined;
  const textBackgroundColor = resolveStyle(styleOverrides, globalStyles, 'textBackgroundColor') as string | undefined;
  const borderColor = resolveStyle(styleOverrides, globalStyles, 'borderColor') as string | undefined;
  const borderWidth = resolveStyle(styleOverrides, globalStyles, 'borderWidth') as number | undefined;
  const borderRadius = resolveStyle(styleOverrides, globalStyles, 'borderRadius') as number | undefined;
  const inputHeight = resolveStyle(styleOverrides, globalStyles, 'inputHeight') as number | undefined;
  const inputPaddingX = _effectiveGlobalStyles.inputPaddingX * _effectiveGlobalStyles.baseSpacing;
  const inputPaddingY = _effectiveGlobalStyles.inputPaddingY * _effectiveGlobalStyles.baseSpacing;
  
  const defaultBorderColor = borderColor ?? _effectiveGlobalStyles.borderColor;
  const defaultBorderWidth = borderWidth ?? _effectiveGlobalStyles.borderWidth;
  const defaultBorderRadius = borderRadius ?? _effectiveGlobalStyles.borderRadius;
  
  return {
    fontFamily: fontFamily,
    fontSize: fontSize ? `${fontSize}px` : undefined,
    fontWeight: fontWeight,
    fontStyle: fontStyle,
    color: textColor,
    backgroundColor: textBackgroundColor ?? (disabled ? '#F3F4F6' : _effectiveGlobalStyles.backgroundColor),
    borderColor: defaultBorderColor,
    borderWidth: `${defaultBorderWidth}px`,
    borderRadius: `${defaultBorderRadius}px`,
    borderStyle: 'solid',
    height: inputHeight ? `${inputHeight}px` : undefined,
    padding: `${inputPaddingY}px ${inputPaddingX}px`,
    width: '100%',
    outline: 'none',
  };
}

/**
 * Build help text/validation styles from styleOverrides and globalStyles
 */
function buildHelpTextStyles(
  styleOverrides: StyleOverrides | undefined,
  globalStyles: GlobalStyles | undefined
): React.CSSProperties {
  const fontFamily = resolveStyle(styleOverrides, globalStyles, 'helpTextFontFamily') as string | undefined;
  const fontSize = resolveStyle(styleOverrides, globalStyles, 'helpTextFontSize') as number | undefined;
  const fontWeight = resolveStyle(styleOverrides, globalStyles, 'helpTextFontWeight') as number | undefined;
  const fontStyle = resolveStyle(styleOverrides, globalStyles, 'helpTextFontStyle') as string | undefined;
  const color = resolveStyle(styleOverrides, globalStyles, 'helpTextColor') as string | undefined;
  const backgroundColor = resolveStyle(styleOverrides, globalStyles, 'helpTextBackgroundColor') as string | undefined;
  const borderColor = resolveStyle(styleOverrides, globalStyles, 'helpTextBorderColor') as string | undefined;
  const borderWidth = resolveStyle(styleOverrides, globalStyles, 'helpTextBorderWidth') as number | undefined;
  const borderRadius = resolveStyle(styleOverrides, globalStyles, 'helpTextBorderRadius') as number | undefined;
  
  return {
    fontFamily: fontFamily,
    fontSize: fontSize ? `${fontSize}px` : undefined,
    fontWeight: fontWeight,
    fontStyle: fontStyle,
    color: color,
    backgroundColor: backgroundColor,
    borderColor: borderColor,
    borderWidth: borderWidth ? `${borderWidth}px` : undefined,
    borderRadius: borderRadius ? `${borderRadius}px` : undefined,
    borderStyle: borderWidth ? 'solid' : undefined,
    padding: borderWidth ? '2px 4px' : undefined,
  };
}

/**
 * Hook to resolve all component styles
 * 
 * @param styleOverrides Component-level style overrides
 * @param globalStyles Global styles from form definition
 * @returns Resolved styles for label, input, help text, and gaps
 * 
 * @example
 * ```tsx
 * const styles = useComponentStyles(component.props.styleOverrides, definition.globalStyles);
 * 
 * return (
 *   <label style={styles.label}>Label</label>
 *   <input style={styles.input} />
 *   <div style={styles.helpText}>Help text</div>
 * );
 * ```
 */
export function useComponentStyles(
  styleOverrides: StyleOverrides | undefined,
  globalStyles: GlobalStyles | undefined
): ResolvedStyles {
  return useMemo(() => {
    const effectiveGlobalStyles = globalStyles ?? DEFAULT_GLOBAL_STYLES;
    
    const labelGap = resolveStyle(styleOverrides, globalStyles, 'labelGap') as number | undefined;
    const inputHelpGap = resolveStyle(styleOverrides, globalStyles, 'inputHelpGap') as number | undefined;
    
    return {
      label: buildLabelStyles(styleOverrides, globalStyles),
      input: buildInputStyles(styleOverrides, globalStyles, false), // disabled handled separately
      helpText: buildHelpTextStyles(styleOverrides, globalStyles),
      gap: {
        labelGap: labelGap !== undefined 
          ? effectiveGlobalStyles.baseSpacing * labelGap 
          : effectiveGlobalStyles.baseSpacing * effectiveGlobalStyles.labelGap,
        inputHelpGap: inputHelpGap !== undefined
          ? effectiveGlobalStyles.baseSpacing * inputHelpGap
          : effectiveGlobalStyles.baseSpacing * effectiveGlobalStyles.inputHelpGap,
      },
    };
  }, [styleOverrides, globalStyles]);
}
