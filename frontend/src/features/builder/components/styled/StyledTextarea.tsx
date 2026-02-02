/**
 * StyledTextarea Component
 * 
 * Generic textarea component that automatically applies resolved styles.
 * Handles focus/blur styling with primary color.
 */

import React, { useLayoutEffect, useMemo, useRef, useState, forwardRef } from 'react';

export interface StyledTextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
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
  /** Enable auto-grow height behavior */
  autoGrow?: boolean;
  /** Optional max height cap for auto-grow (px) */
  autoGrowMaxHeight?: number;
  /** Resize mode (overrides default vertical) */
  resizeMode?: 'none' | 'vertical' | 'horizontal' | 'both' | 'auto-grow';
}

/**
 * StyledTextarea - Generic textarea with automatic style application
 */
export const StyledTextarea = forwardRef<HTMLTextAreaElement, StyledTextareaProps>(
  ({
    styles,
    primaryColor,
    disabled,
    error,
    componentId,
    autoGrow,
    autoGrowMaxHeight,
    resizeMode,
    onFocus,
    onBlur,
    onInput,
    id,
    ...textareaProps
  }, ref) => {
    const [isFocused, setIsFocused] = useState(false);
    const internalRef = useRef<HTMLTextAreaElement | null>(null);
    
    const defaultBorderColor = styles.borderColor as string;
    const textareaId = id || (componentId ? `${componentId}-input` : undefined);
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
    
    const resolvedResize = useMemo(() => {
      if (resizeMode === 'auto-grow') return 'none';
      if (resizeMode === 'none') return 'none';
      if (resizeMode === 'horizontal') return 'horizontal';
      if (resizeMode === 'both') return 'both';
      return 'vertical';
    }, [resizeMode]);

    const textareaStyle: React.CSSProperties = {
      ...styles,
      display: 'block', // prevents baseline/line-box extra height in wrappers (keeps overlays aligned to the control)
      backgroundColor: disabled ? '#F3F4F6' : styles.backgroundColor,
      color: disabled ? '#6B7280' : styles.color,
      cursor: disabled ? 'not-allowed' : 'text',
      borderColor,
      boxShadow,
      outline: isFocused && primaryColor ? `2px solid ${primaryColor}` : 'none', // Fallback for browsers that don't support boxShadow
      outlineOffset: '2px', // Prevents outline from overlapping border
      transition: 'border-color 0.2s ease, box-shadow 0.2s ease', // Smooth transitions
      resize: resolvedResize,
      overflowY: autoGrow ? 'hidden' : styles.overflowY,
    };
    
    const computeAutoGrowMaxHeight = React.useCallback(() => {
      if (!autoGrow) return undefined;
      if (autoGrowMaxHeight) return autoGrowMaxHeight;
      if (!componentId) return undefined;

      const componentEl = document.querySelector(`[data-component-id="${componentId}"]`) as HTMLElement | null;
      if (!componentEl) return undefined;

      const textareaEl = internalRef.current;
      const componentRect = componentEl.getBoundingClientRect();
      const textareaRect = textareaEl?.getBoundingClientRect();
      const anchorTop = textareaRect?.top ?? componentRect.top;

      const canvasEl = document.getElementById('canvas-stage');
      const canvasRect = canvasEl?.getBoundingClientRect();
      let maxBottom = canvasRect?.bottom ?? Number.POSITIVE_INFINITY;

      if (!canvasRect) {
        // In Public Preview, there is no canvas-stage. Fall back to the nearest
        // scroll container (fixed-height artboard) or the viewport.
        let node: HTMLElement | null = componentEl.parentElement;
        let nearestBoundary = Number.POSITIVE_INFINITY;
        while (node) {
          const style = window.getComputedStyle(node);
          const overflowY = style.overflowY;
          const height = style.height;
          const hasBoundary =
            overflowY === 'auto' ||
            overflowY === 'scroll' ||
            overflowY === 'hidden' ||
            height !== 'auto';
          if (hasBoundary) {
            const rect = node.getBoundingClientRect();
            const isLargerThanComponent = rect.height > componentRect.height + 20;
            if (rect.height > 0 && isLargerThanComponent && rect.bottom > anchorTop + 1) {
              nearestBoundary = Math.min(nearestBoundary, rect.bottom);
            }
          }
          node = node.parentElement;
        }

        if (Number.isFinite(nearestBoundary)) {
          maxBottom = nearestBoundary;
        }

        if (!Number.isFinite(maxBottom)) {
          maxBottom = window.innerHeight;
        }
      }

      const nodes = Array.from(document.querySelectorAll('[data-component-id]')) as HTMLElement[];
      let nearestTop = Infinity;
      for (const node of nodes) {
        if (node === componentEl) continue;
        const rect = node.getBoundingClientRect();
        const overlapsX = rect.left < componentRect.right && rect.right > componentRect.left;
        if (!overlapsX) continue;
        if (rect.top > anchorTop + 1) {
          nearestTop = Math.min(nearestTop, rect.top);
        }
      }

      if (nearestTop !== Infinity) {
        maxBottom = Math.min(maxBottom, nearestTop);
      }

      return Math.max(0, maxBottom - anchorTop - 8);
    }, [autoGrow, autoGrowMaxHeight, componentId]);

    const adjustHeight = React.useCallback(() => {
      if (!autoGrow || !internalRef.current) return;
      const el = internalRef.current;
      el.style.height = 'auto';
      const maxHeight = computeAutoGrowMaxHeight();
      const nextHeight = maxHeight ? Math.min(el.scrollHeight, maxHeight) : el.scrollHeight;
      el.style.height = `${nextHeight}px`;
    }, [autoGrow, computeAutoGrowMaxHeight]);

    useLayoutEffect(() => {
      adjustHeight();
    }, [adjustHeight, textareaProps.value]);

    const handleFocus = (e: React.FocusEvent<HTMLTextAreaElement>) => {
      setIsFocused(true);
      onFocus?.(e);
    };
    
    const handleBlur = (e: React.FocusEvent<HTMLTextAreaElement>) => {
      setIsFocused(false);
      onBlur?.(e);
    };
    
    const handleInput = (e: React.FormEvent<HTMLTextAreaElement>) => {
      if (autoGrow) {
        // Ensure DOM-driven growth even before state updates.
        adjustHeight();
      }
      onInput?.(e);
    };
    
    const setRefs = (node: HTMLTextAreaElement | null) => {
      internalRef.current = node;
      if (typeof ref === 'function') {
        ref(node);
      } else if (ref) {
        ref.current = node;
      }
    };

    return (
      <textarea
        ref={setRefs}
        {...textareaProps}
        id={textareaId}
        disabled={disabled}
        style={textareaStyle}
        onFocus={handleFocus}
        onBlur={handleBlur}
        onInput={handleInput}
        aria-invalid={!!error}
        aria-describedby={errorId}
        aria-required={textareaProps.required}
      />
    );
  }
);

StyledTextarea.displayName = 'StyledTextarea';
