/**
 * StyledInput Component
 * 
 * Generic input component that automatically applies resolved styles.
 * Handles focus/blur styling with primary color.
 * 
 * This component ensures consistent styling across all input types
 * and eliminates the need for manual style application in each component.
 */

import React, { useState, forwardRef } from 'react';

export interface StyledInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Resolved input styles from useComponentStyles hook */
  styles: React.CSSProperties;
  /** Primary color for focus styling */
  primaryColor?: string;
  /** Disabled state */
  disabled?: boolean;
  /** Error message - when present, shows error styling */
  error?: string;
  /** Component ID for ARIA linking */
  componentId?: string;
  /** When true, always show focus styling (for demo/preview e.g. Focus Color cycling) */
  simulateFocus?: boolean;
}

/**
 * StyledInput - Generic input with automatic style application
 * 
 * Automatically applies:
 * - Resolved styles (font, color, border, etc.)
 * - Focus styling with primary color
 * - Blur styling to restore default border
 * - Disabled state styling
 */
export const StyledInput = forwardRef<HTMLInputElement, StyledInputProps>(
  ({ styles, primaryColor, disabled, error, componentId, simulateFocus, onFocus, onBlur, id, ...inputProps }, ref) => {
    const [isFocused, setIsFocused] = useState(false);
    const effectiveFocused = isFocused || !!simulateFocus;
    
    const defaultBorderColor = styles.borderColor as string;
    const inputId = id || (componentId ? `${componentId}-input` : undefined);
    const errorId = error && componentId ? `${componentId}-error` : undefined;
    
    // Determine border color: error > focus > default
    const borderColor = error 
      ? '#DC2626' // Red for errors
      : (effectiveFocused && primaryColor ? primaryColor : defaultBorderColor);
    
    // Determine box shadow: error > focus > none
    const boxShadow = error
      ? '0 0 0 2px rgba(220, 38, 38, 0.1)' // Subtle red glow for errors
      : (effectiveFocused && primaryColor 
          ? `0 0 0 2px ${primaryColor}33, 0 0 0 4px ${primaryColor}11` // Double ring for better visibility
          : undefined);
    
    const inputStyle: React.CSSProperties = {
      ...styles,
      display: 'block', // prevents baseline/line-box extra height in wrappers (keeps overlays aligned to the control)
      backgroundColor: disabled ? '#F3F4F6' : styles.backgroundColor,
      color: disabled ? '#6B7280' : styles.color,
      cursor: disabled ? 'not-allowed' : 'text',
      borderColor,
      boxShadow,
      outline: effectiveFocused && primaryColor ? `2px solid ${primaryColor}` : 'none', // Fallback for browsers that don't support boxShadow
      outlineOffset: '2px', // Prevents outline from overlapping border
      transition: 'border-color 0.2s ease, box-shadow 0.2s ease', // Smooth transitions
    };
    
    const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(true);
      onFocus?.(e);
    };
    
    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(false);
      onBlur?.(e);
    };
    
    return (
      <input
        ref={ref}
        {...inputProps}
        id={inputId}
        disabled={disabled}
        style={inputStyle}
        onFocus={handleFocus}
        onBlur={handleBlur}
        aria-invalid={!!error}
        aria-describedby={errorId}
        aria-required={inputProps.required}
      />
    );
  }
);

StyledInput.displayName = 'StyledInput';
