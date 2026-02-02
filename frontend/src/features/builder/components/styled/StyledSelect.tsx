/**
 * StyledSelect Component
 * 
 * Generic select component that automatically applies resolved styles.
 * Handles focus/blur styling with primary color.
 */

import React, { useState, forwardRef } from 'react';

export interface StyledSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
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
  /** Options array */
  options?: Array<{ label: string; value: string; disabled?: boolean; group?: string }>;
  /** Placeholder text */
  placeholder?: string;
}

/**
 * StyledSelect - Generic select with automatic style application
 */
export const StyledSelect = forwardRef<HTMLSelectElement, StyledSelectProps>(
  ({ styles, primaryColor, disabled, error, componentId, onFocus, onBlur, options = [], placeholder, id, ...selectProps }, ref) => {
    const [isFocused, setIsFocused] = useState(false);
    
    const defaultBorderColor = styles.borderColor as string;
    const selectId = id || (componentId ? `${componentId}-input` : undefined);
    const errorId = error && componentId ? `${componentId}-error` : undefined;
    
    // Determine border color: error > focus > default
    const borderColor = error 
      ? '#DC2626' // Red for errors
      : (isFocused && primaryColor ? primaryColor : defaultBorderColor);
    
    // Determine box shadow: error > focus > none
    const boxShadow = error
      ? '0 0 0 2px rgba(220, 38, 38, 0.1)' // Subtle red glow for errors
      : (isFocused && primaryColor 
          ? `0 0 0 2px ${primaryColor}33, 0 0 0 4px ${primaryColor}11` // Double ring for better visibility
          : undefined);
    
    // If height is explicitly set, ensure padding/line-height do not cause text truncation.
    // This is especially visible on <select>, where large padding + small height clips the selected text.
    const heightPx = (() => {
      const h = styles.height;
      if (typeof h === 'number') return h;
      if (typeof h === 'string' && h.endsWith('px')) {
        const n = parseInt(h, 10);
        return Number.isFinite(n) ? n : undefined;
      }
      return undefined;
    })();

    const borderWidthPx = (() => {
      const bw = styles.borderWidth;
      if (typeof bw === 'number') return bw;
      if (typeof bw === 'string' && bw.endsWith('px')) {
        const n = parseInt(bw, 10);
        return Number.isFinite(n) ? n : 1;
      }
      return 1;
    })();

    const fontSizePx = (() => {
      const fs = styles.fontSize;
      if (typeof fs === 'number') return fs;
      if (typeof fs === 'string' && fs.endsWith('px')) {
        const n = parseInt(fs, 10);
        return Number.isFinite(n) ? n : 14;
      }
      return 14;
    })();

    const adjustedForHeight: React.CSSProperties = (() => {
      if (!heightPx) return {};
      const innerH = Math.max(0, heightPx - borderWidthPx * 2);
      // Aim to keep the text vertically centered.
      // Select rendering varies by browser, but lineHeight+paddingTop/Bottom generally improves centering.
      const targetTextH = Math.max(12, Math.floor(fontSizePx * 1.2));
      const padY = Math.max(0, Math.floor((innerH - targetTextH) / 2));
      const lineHeight = Math.max(0, innerH - padY * 2);
      return {
        paddingTop: `${padY}px`,
        paddingBottom: `${padY}px`,
        lineHeight: `${lineHeight}px`,
      };
    })();

    const selectStyle: React.CSSProperties = {
      ...styles,
      display: 'block', // prevents baseline/line-box extra height in wrappers (keeps overlays aligned to the control)
      backgroundColor: disabled ? '#F3F4F6' : styles.backgroundColor,
      color: disabled ? '#6B7280' : styles.color,
      cursor: disabled ? 'not-allowed' : 'pointer',
      borderColor,
      boxShadow,
      ...adjustedForHeight,
      outline: isFocused && primaryColor ? `2px solid ${primaryColor}` : 'none', // Fallback for browsers that don't support boxShadow
      outlineOffset: '2px', // Prevents outline from overlapping border
      transition: 'border-color 0.2s ease, box-shadow 0.2s ease', // Smooth transitions
    };
    
    const handleFocus = (e: React.FocusEvent<HTMLSelectElement>) => {
      setIsFocused(true);
      onFocus?.(e);
    };
    
    const handleBlur = (e: React.FocusEvent<HTMLSelectElement>) => {
      setIsFocused(false);
      onBlur?.(e);
    };
    
    return (
      <select
        ref={ref}
        {...selectProps}
        id={selectId}
        disabled={disabled}
        style={selectStyle}
        onFocus={handleFocus}
        onBlur={handleBlur}
        aria-invalid={!!error}
        aria-describedby={errorId}
        aria-required={selectProps.required}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {/* Render optgroups when group is provided (visual grouping only). */}
        {(() => {
          const hasGroups = options.some(o => o.group && String(o.group).trim().length > 0);
          if (!hasGroups) {
            return options.map((opt) => (
              <option key={String(opt.value)} value={String(opt.value)} disabled={Boolean(opt.disabled)}>
                {String(opt.label)}
              </option>
            ));
          }

          // Preserve original option order; group null/empty into "ungrouped"
          const groupsInOrder: Array<{ key: string; label?: string }> = [];
          const seen = new Set<string>();
          for (const opt of options) {
            const g = (opt.group && String(opt.group).trim().length > 0) ? String(opt.group).trim() : '';
            if (!seen.has(g)) {
              seen.add(g);
              groupsInOrder.push({ key: g, label: g || undefined });
            }
          }

          return groupsInOrder.map(g => {
            const groupOptions = options.filter(o => {
              const og = (o.group && String(o.group).trim().length > 0) ? String(o.group).trim() : '';
              return og === g.key;
            });

            // Ungrouped options render directly (no optgroup label)
            if (!g.label) {
              return groupOptions.map(opt => (
                <option key={String(opt.value)} value={String(opt.value)} disabled={Boolean(opt.disabled)}>
                  {String(opt.label)}
                </option>
              ));
            }

            return (
              <optgroup key={`group-${g.key}`} label={g.label}>
                {groupOptions.map(opt => (
                  <option key={String(opt.value)} value={String(opt.value)} disabled={Boolean(opt.disabled)}>
                    {String(opt.label)}
                  </option>
                ))}
              </optgroup>
            );
          });
        })()}
      </select>
    );
  }
);

StyledSelect.displayName = 'StyledSelect';
