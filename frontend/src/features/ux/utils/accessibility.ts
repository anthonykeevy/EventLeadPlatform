// Accessibility utilities for WCAG 2.1 AA compliance

export interface AccessibilityOptions {
  announceChanges?: boolean;
  liveRegion?: 'polite' | 'assertive' | 'off';
  focusManagement?: boolean;
}

// Screen reader announcements
export const announceToScreenReader = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;

  document.body.appendChild(announcement);

  // Remove after announcement
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
};

// Focus management utilities
export const focusElement = (element: HTMLElement | null) => {
  if (element) {
    element.focus();
    // Ensure focus is visible
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
};

export const focusFirstFocusable = (container: HTMLElement) => {
  const focusableElements = getFocusableElements(container);
  if (focusableElements.length > 0) {
    focusElement(focusableElements[0]);
  }
};

export const focusLastFocusable = (container: HTMLElement) => {
  const focusableElements = getFocusableElements(container);
  if (focusableElements.length > 0) {
    focusElement(focusableElements[focusableElements.length - 1]);
  }
};

// Get all focusable elements within a container
export const getFocusableElements = (container: HTMLElement): HTMLElement[] => {
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

  return Array.from(container.querySelectorAll(focusableSelectors)) as HTMLElement[];
};

// Keyboard navigation helpers
export const handleKeyNavigation = (
  event: KeyboardEvent,
  options: {
    onEnter?: () => void;
    onEscape?: () => void;
    onArrowUp?: () => void;
    onArrowDown?: () => void;
    onArrowLeft?: () => void;
    onArrowRight?: () => void;
    onTab?: (direction: 'forward' | 'backward') => void;
    onSpace?: () => void;
    preventDefault?: boolean;
  }
) => {
  const {
    onEnter,
    onEscape,
    onArrowUp,
    onArrowDown,
    onArrowLeft,
    onArrowRight,
    onTab,
    onSpace,
    preventDefault = true,
  } = options;

  switch (event.key) {
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
        onTab(event.shiftKey ? 'backward' : 'forward');
      }
      break;

    case ' ':
      if (onSpace) {
        if (preventDefault) event.preventDefault();
        onSpace();
      }
      break;
  }
};

// ARIA helpers
export const setAriaExpanded = (element: HTMLElement, expanded: boolean) => {
  element.setAttribute('aria-expanded', expanded.toString());
};

export const setAriaSelected = (element: HTMLElement, selected: boolean) => {
  element.setAttribute('aria-selected', selected.toString());
};

export const setAriaChecked = (element: HTMLElement, checked: boolean) => {
  element.setAttribute('aria-checked', checked.toString());
};

export const setAriaPressed = (element: HTMLElement, pressed: boolean) => {
  element.setAttribute('aria-pressed', pressed.toString());
};

export const setAriaHidden = (element: HTMLElement, hidden: boolean) => {
  element.setAttribute('aria-hidden', hidden.toString());
};

export const setAriaLabel = (element: HTMLElement, label: string) => {
  element.setAttribute('aria-label', label);
};

export const setAriaDescribedBy = (element: HTMLElement, describedBy: string) => {
  element.setAttribute('aria-describedby', describedBy);
};

export const setAriaControls = (element: HTMLElement, controls: string) => {
  element.setAttribute('aria-controls', controls);
};

export const setAriaOwns = (element: HTMLElement, owns: string) => {
  element.setAttribute('aria-owns', owns);
};

// Role helpers
export const setRole = (element: HTMLElement, role: string) => {
  element.setAttribute('role', role);
};

export const setTabIndex = (element: HTMLElement, tabIndex: number | 'auto') => {
  if (tabIndex === 'auto') {
    element.removeAttribute('tabindex');
  } else {
    element.setAttribute('tabindex', tabIndex.toString());
  }
};

// Color contrast utilities
export const getContrastRatio = (color1: string, color2: string): number => {
  const getLuminance = (color: string): number => {
    const rgb = hexToRgb(color);
    if (!rgb) return 0;

    const { r, g, b } = rgb;
    const [rs, gs, bs] = [r, g, b].map(c => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });

    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
  };

  const l1 = getLuminance(color1);
  const l2 = getLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);

  return (lighter + 0.05) / (darker + 0.05);
};

export const hexToRgb = (hex: string): { r: number; g: number; b: number } | null => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
};

export const meetsContrastRatio = (color1: string, color2: string, level: 'AA' | 'AAA' = 'AA'): boolean => {
  const ratio = getContrastRatio(color1, color2);
  return level === 'AA' ? ratio >= 4.5 : ratio >= 7;
};

// Focus trap implementation
export const createFocusTrap = (container: HTMLElement) => {
  const focusableElements = getFocusableElements(container);
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Tab') {
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
  };

  const activate = () => {
    document.addEventListener('keydown', handleKeyDown);
    firstElement?.focus();
  };

  const deactivate = () => {
    document.removeEventListener('keydown', handleKeyDown);
  };

  return { activate, deactivate };
};

// Skip links for keyboard navigation
export const createSkipLink = (targetId: string, text: string = 'Skip to main content'): HTMLElement => {
  const skipLink = document.createElement('a');
  skipLink.href = `#${targetId}`;
  skipLink.textContent = text;
  skipLink.className = 'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-md';
  
  skipLink.addEventListener('click', (e) => {
    e.preventDefault();
    const target = document.getElementById(targetId);
    if (target) {
      focusElement(target);
    }
  });

  return skipLink;
};

// High contrast mode detection
export const isHighContrastMode = (): boolean => {
  return window.matchMedia('(prefers-contrast: high)').matches;
};

// Reduced motion detection
export const prefersReducedMotion = (): boolean => {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

// Screen reader detection (basic)
export const isScreenReaderActive = (): boolean => {
  return window.navigator.userAgent.includes('NVDA') || 
         window.navigator.userAgent.includes('JAWS') ||
         window.navigator.userAgent.includes('VoiceOver');
};

// Announce page changes for single-page applications
export const announcePageChange = (pageTitle: string) => {
  // Update the page title
  document.title = pageTitle;
  
  // Announce to screen readers
  announceToScreenReader(`Navigated to ${pageTitle}`, 'assertive');
  
  // Update the main heading if it exists
  const mainHeading = document.querySelector('h1');
  if (mainHeading) {
    mainHeading.textContent = pageTitle;
  }
};

// Utility to ensure proper heading hierarchy
export const validateHeadingHierarchy = (container: HTMLElement = document.body): string[] => {
  const headings = Array.from(container.querySelectorAll('h1, h2, h3, h4, h5, h6'));
  const issues: string[] = [];
  let previousLevel = 0;

  headings.forEach((heading, index) => {
    const level = parseInt(heading.tagName.charAt(1));
    
    if (index === 0 && level !== 1) {
      issues.push(`First heading should be h1, found ${heading.tagName}`);
    }
    
    if (level > previousLevel + 1) {
      issues.push(`Heading level skipped: ${heading.tagName} follows ${previousLevel > 0 ? `h${previousLevel}` : 'nothing'}`);
    }
    
    previousLevel = level;
  });

  return issues;
};

export default {
  announceToScreenReader,
  focusElement,
  focusFirstFocusable,
  focusLastFocusable,
  getFocusableElements,
  handleKeyNavigation,
  setAriaExpanded,
  setAriaSelected,
  setAriaChecked,
  setAriaPressed,
  setAriaHidden,
  setAriaLabel,
  setAriaDescribedBy,
  setAriaControls,
  setAriaOwns,
  setRole,
  setTabIndex,
  getContrastRatio,
  meetsContrastRatio,
  createFocusTrap,
  createSkipLink,
  isHighContrastMode,
  prefersReducedMotion,
  isScreenReaderActive,
  announcePageChange,
  validateHeadingHierarchy,
};

