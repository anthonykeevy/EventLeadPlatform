import { useEffect, useCallback, useRef, useState } from 'react';

export interface KeyboardNavigationOptions {
  onEnter?: () => void;
  onEscape?: () => void;
  onArrowUp?: () => void;
  onArrowDown?: () => void;
  onArrowLeft?: () => void;
  onArrowRight?: () => void;
  onTab?: (direction: 'forward' | 'backward') => void;
  onSpace?: () => void;
  onDelete?: () => void;
  onBackspace?: () => void;
  enabled?: boolean;
  preventDefault?: boolean;
}

export interface UseKeyboardNavigationReturn {
  setFocusableRef: (ref: HTMLElement | null) => void;
  focus: () => void;
  blur: () => void;
  isFocused: boolean;
}

export const useKeyboardNavigation = (
  options: KeyboardNavigationOptions = {}
): UseKeyboardNavigationReturn => {
  const {
    onEnter,
    onEscape,
    onArrowUp,
    onArrowDown,
    onArrowLeft,
    onArrowRight,
    onTab,
    onSpace,
    onDelete,
    onBackspace,
    enabled = true,
    preventDefault = true,
  } = options;

  const elementRef = useRef<HTMLElement | null>(null);
  const isFocusedRef = useRef(false);

  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    if (!enabled || !elementRef.current) return;

    const { key, shiftKey } = event;

    switch (key) {
      case 'Enter':
        if (onEnter) {
          if (preventDefault) event.preventDefault();
          onEnter();
        }
        break;

      case 'Escape':
        if (onEscape) {
          if (preventDefault) event.preventDefault();
          onEscape();
        }
        break;

      case 'ArrowUp':
        if (onArrowUp) {
          if (preventDefault) event.preventDefault();
          onArrowUp();
        }
        break;

      case 'ArrowDown':
        if (onArrowDown) {
          if (preventDefault) event.preventDefault();
          onArrowDown();
        }
        break;

      case 'ArrowLeft':
        if (onArrowLeft) {
          if (preventDefault) event.preventDefault();
          onArrowLeft();
        }
        break;

      case 'ArrowRight':
        if (onArrowRight) {
          if (preventDefault) event.preventDefault();
          onArrowRight();
        }
        break;

      case 'Tab':
        if (onTab) {
          if (preventDefault) event.preventDefault();
          onTab(shiftKey ? 'backward' : 'forward');
        }
        break;

      case ' ':
        if (onSpace) {
          if (preventDefault) event.preventDefault();
          onSpace();
        }
        break;

      case 'Delete':
        if (onDelete) {
          if (preventDefault) event.preventDefault();
          onDelete();
        }
        break;

      case 'Backspace':
        if (onBackspace) {
          if (preventDefault) event.preventDefault();
          onBackspace();
        }
        break;
    }
  }, [
    enabled,
    onEnter,
    onEscape,
    onArrowUp,
    onArrowDown,
    onArrowLeft,
    onArrowRight,
    onTab,
    onSpace,
    onDelete,
    onBackspace,
    preventDefault,
  ]);

  const handleFocus = useCallback(() => {
    isFocusedRef.current = true;
  }, []);

  const handleBlur = useCallback(() => {
    isFocusedRef.current = false;
  }, []);

  useEffect(() => {
    const element = elementRef.current;
    if (!element || !enabled) return;

    element.addEventListener('keydown', handleKeyDown);
    element.addEventListener('focus', handleFocus);
    element.addEventListener('blur', handleBlur);

    return () => {
      element.removeEventListener('keydown', handleKeyDown);
      element.removeEventListener('focus', handleFocus);
      element.removeEventListener('blur', handleBlur);
    };
  }, [handleKeyDown, handleFocus, handleBlur, enabled]);

  const setFocusableRef = useCallback((ref: HTMLElement | null) => {
    elementRef.current = ref;
  }, []);

  const focus = useCallback(() => {
    if (elementRef.current) {
      elementRef.current.focus();
    }
  }, []);

  const blur = useCallback(() => {
    if (elementRef.current) {
      elementRef.current.blur();
    }
  }, []);

  return {
    setFocusableRef,
    focus,
    blur,
    isFocused: isFocusedRef.current,
  };
};

// Hook for focus trap (useful for modals)
export interface UseFocusTrapOptions {
  enabled?: boolean;
  initialFocus?: HTMLElement | null;
  returnFocusOnDeactivate?: boolean;
}

export const useFocusTrap = (options: UseFocusTrapOptions = {}) => {
  const {
    enabled = true,
    initialFocus,
    returnFocusOnDeactivate = true,
  } = options;

  const containerRef = useRef<HTMLElement | null>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);

  const getFocusableElements = useCallback(() => {
    if (!containerRef.current) return [];

    const focusableSelectors = [
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      'a[href]',
      'area[href]',
      'iframe',
      'object',
      'embed',
      '[tabindex]:not([tabindex="-1"])',
      '[contenteditable="true"]',
    ].join(', ');

    return Array.from(
      containerRef.current.querySelectorAll(focusableSelectors)
    ) as HTMLElement[];
  }, []);

  const trapFocus = useCallback((event: KeyboardEvent) => {
    if (!enabled || !containerRef.current) return;

    if (event.key === 'Tab') {
      const focusableElements = getFocusableElements();
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];

      if (event.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstElement) {
          event.preventDefault();
          lastElement?.focus();
        }
      } else {
        // Tab
        if (document.activeElement === lastElement) {
          event.preventDefault();
          firstElement?.focus();
        }
      }
    }
  }, [enabled, getFocusableElements]);

  const activate = useCallback(() => {
    if (!enabled) return;

    // Store the currently focused element
    previousActiveElement.current = document.activeElement as HTMLElement;

    // Focus the initial element or the first focusable element
    if (initialFocus) {
      initialFocus.focus();
    } else {
      const focusableElements = getFocusableElements();
      focusableElements[0]?.focus();
    }

    // Add event listener for focus trapping
    document.addEventListener('keydown', trapFocus);
  }, [enabled, initialFocus, getFocusableElements, trapFocus]);

  const deactivate = useCallback(() => {
    if (!enabled) return;

    // Remove event listener
    document.removeEventListener('keydown', trapFocus);

    // Return focus to the previously focused element
    if (returnFocusOnDeactivate && previousActiveElement.current) {
      previousActiveElement.current.focus();
    }
  }, [enabled, trapFocus, returnFocusOnDeactivate]);

  const setContainerRef = useCallback((ref: HTMLElement | null) => {
    containerRef.current = ref;
  }, []);

  return {
    setContainerRef,
    activate,
    deactivate,
  };
};

// Hook for arrow key navigation in lists
export interface UseArrowNavigationOptions {
  items: any[];
  onSelect?: (item: any, index: number) => void;
  onNavigate?: (index: number) => void;
  enabled?: boolean;
  loop?: boolean;
}

export const useArrowNavigation = ({
  items,
  onSelect,
  onNavigate,
  enabled = true,
  loop = false,
}: UseArrowNavigationOptions) => {
  const [selectedIndex, setSelectedIndex] = useState(-1);

  const navigate = useCallback((direction: 'up' | 'down') => {
    if (!enabled || items.length === 0) return;

    setSelectedIndex(prevIndex => {
      let newIndex = prevIndex;

      if (direction === 'down') {
        newIndex = loop && prevIndex === items.length - 1 ? 0 : Math.min(prevIndex + 1, items.length - 1);
      } else {
        newIndex = loop && prevIndex === 0 ? items.length - 1 : Math.max(prevIndex - 1, 0);
      }

      onNavigate?.(newIndex);
      return newIndex;
    });
  }, [enabled, items.length, loop, onNavigate]);

  const select = useCallback((index: number) => {
    if (index >= 0 && index < items.length) {
      setSelectedIndex(index);
      onSelect?.(items[index], index);
    }
  }, [items, onSelect]);

  const reset = useCallback(() => {
    setSelectedIndex(-1);
  }, []);

  const keyboardNavigation = useKeyboardNavigation({
    onArrowUp: () => navigate('up'),
    onArrowDown: () => navigate('down'),
    onEnter: () => {
      if (selectedIndex >= 0) {
        select(selectedIndex);
      }
    },
    enabled,
  });

  return {
    selectedIndex,
    navigate,
    select,
    reset,
    keyboardNavigation,
  };
};

export default useKeyboardNavigation;
