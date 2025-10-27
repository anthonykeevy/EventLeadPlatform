// Mobile optimization utilities for touch-friendly interfaces

export interface TouchTargetOptions {
  minSize?: number;
  padding?: number;
  margin?: number;
}

// Minimum touch target size (44px as per iOS/Android guidelines)
export const MIN_TOUCH_TARGET_SIZE = 44;

// Check if device is mobile
export const isMobileDevice = (): boolean => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

// Check if device supports touch
export const isTouchDevice = (): boolean => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
};

// Check if device is iOS
export const isIOS = (): boolean => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent);
};

// Check if device is Android
export const isAndroid = (): boolean => {
  return /Android/.test(navigator.userAgent);
};

// Get viewport dimensions
export const getViewportDimensions = () => {
  return {
    width: window.innerWidth,
    height: window.innerHeight,
  };
};

// Check if viewport is mobile size
export const isMobileViewport = (): boolean => {
  const { width } = getViewportDimensions();
  return width < 768; // Tailwind's md breakpoint
};

// Check if viewport is tablet size
export const isTabletViewport = (): boolean => {
  const { width } = getViewportDimensions();
  return width >= 768 && width < 1024; // Tailwind's md to lg breakpoint
};

// Check if viewport is desktop size
export const isDesktopViewport = (): boolean => {
  const { width } = getViewportDimensions();
  return width >= 1024; // Tailwind's lg breakpoint
};

// Touch target utilities
export const ensureTouchTarget = (
  element: HTMLElement,
  options: TouchTargetOptions = {}
): void => {
  const {
    minSize = MIN_TOUCH_TARGET_SIZE,
    padding = 8,
    margin = 4,
  } = options;

  const computedStyle = window.getComputedStyle(element);
  const currentWidth = parseInt(computedStyle.width) || 0;
  const currentHeight = parseInt(computedStyle.height) || 0;

  // Ensure minimum size
  if (currentWidth < minSize) {
    element.style.minWidth = `${minSize}px`;
  }
  if (currentHeight < minSize) {
    element.style.minHeight = `${minSize}px`;
  }

  // Add padding for better touch experience
  const currentPadding = computedStyle.padding;
  if (!currentPadding || currentPadding === '0px') {
    element.style.padding = `${padding}px`;
  }

  // Add margin for spacing
  const currentMargin = computedStyle.margin;
  if (!currentMargin || currentMargin === '0px') {
    element.style.margin = `${margin}px`;
  }
};

// Touch event handlers
export const addTouchHandlers = (
  element: HTMLElement,
  handlers: {
    onTouchStart?: (e: TouchEvent) => void;
    onTouchMove?: (e: TouchEvent) => void;
    onTouchEnd?: (e: TouchEvent) => void;
    onTouchCancel?: (e: TouchEvent) => void;
  }
): (() => void) => {
  const { onTouchStart, onTouchMove, onTouchEnd, onTouchCancel } = handlers;

  if (onTouchStart) {
    element.addEventListener('touchstart', onTouchStart, { passive: false });
  }
  if (onTouchMove) {
    element.addEventListener('touchmove', onTouchMove, { passive: false });
  }
  if (onTouchEnd) {
    element.addEventListener('touchend', onTouchEnd, { passive: false });
  }
  if (onTouchCancel) {
    element.addEventListener('touchcancel', onTouchCancel, { passive: false });
  }

  // Return cleanup function
  return () => {
    if (onTouchStart) {
      element.removeEventListener('touchstart', onTouchStart);
    }
    if (onTouchMove) {
      element.removeEventListener('touchmove', onTouchMove);
    }
    if (onTouchEnd) {
      element.removeEventListener('touchend', onTouchEnd);
    }
    if (onTouchCancel) {
      element.removeEventListener('touchcancel', onTouchCancel);
    }
  };
};

// Swipe gesture detection
export interface SwipeOptions {
  threshold?: number;
  velocity?: number;
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  onSwipeUp?: () => void;
  onSwipeDown?: () => void;
}

export const addSwipeHandlers = (
  element: HTMLElement,
  options: SwipeOptions = {}
): (() => void) => {
  const {
    threshold = 50,
    velocity = 0.3,
    onSwipeLeft,
    onSwipeRight,
    onSwipeUp,
    onSwipeDown,
  } = options;

  let startX = 0;
  let startY = 0;
  let startTime = 0;

  const handleTouchStart = (e: TouchEvent) => {
    const touch = e.touches[0];
    startX = touch.clientX;
    startY = touch.clientY;
    startTime = Date.now();
  };

  const handleTouchEnd = (e: TouchEvent) => {
    const touch = e.changedTouches[0];
    const endX = touch.clientX;
    const endY = touch.clientY;
    const endTime = Date.now();

    const deltaX = endX - startX;
    const deltaY = endY - startY;
    const deltaTime = endTime - startTime;
    const velocityX = Math.abs(deltaX) / deltaTime;
    const velocityY = Math.abs(deltaY) / deltaTime;

    // Check if swipe meets threshold and velocity requirements
    if (Math.abs(deltaX) > threshold && velocityX > velocity) {
      if (deltaX > 0 && onSwipeRight) {
        onSwipeRight();
      } else if (deltaX < 0 && onSwipeLeft) {
        onSwipeLeft();
      }
    }

    if (Math.abs(deltaY) > threshold && velocityY > velocity) {
      if (deltaY > 0 && onSwipeDown) {
        onSwipeDown();
      } else if (deltaY < 0 && onSwipeUp) {
        onSwipeUp();
      }
    }
  };

  return addTouchHandlers(element, {
    onTouchStart: handleTouchStart,
    onTouchEnd: handleTouchEnd,
  });
};

// Pull-to-refresh implementation
export interface PullToRefreshOptions {
  threshold?: number;
  onRefresh: () => void;
  refreshText?: string;
  pullingText?: string;
  refreshingText?: string;
}

export const addPullToRefresh = (
  element: HTMLElement,
  options: PullToRefreshOptions
): (() => void) => {
  const {
    threshold = 80,
    onRefresh,
    refreshText = 'Pull to refresh',
    pullingText = 'Release to refresh',
    refreshingText = 'Refreshing...',
  } = options;

  let startY = 0;
  let currentY = 0;
  let isPulling = false;
  let isRefreshing = false;

  // Create refresh indicator
  const indicator = document.createElement('div');
  indicator.className = 'pull-to-refresh-indicator';
  indicator.textContent = refreshText;
  indicator.style.cssText = `
    position: absolute;
    top: -50px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 20px;
    font-size: 14px;
    color: #666;
    transition: all 0.3s ease;
    z-index: 1000;
  `;

  element.style.position = 'relative';
  element.appendChild(indicator);

  const handleTouchStart = (e: TouchEvent) => {
    if (isRefreshing) return;
    
    startY = e.touches[0].clientY;
    isPulling = false;
  };

  const handleTouchMove = (e: TouchEvent) => {
    if (isRefreshing) return;

    currentY = e.touches[0].clientY;
    const deltaY = currentY - startY;

    // Only allow pull when at top of scroll
    if (element.scrollTop === 0 && deltaY > 0) {
      e.preventDefault();
      isPulling = true;

      const progress = Math.min(deltaY / threshold, 1);
      const translateY = Math.min(deltaY * 0.5, threshold * 0.5);

      element.style.transform = `translateY(${translateY}px)`;
      indicator.style.top = `${-50 + translateY}px`;
      indicator.style.opacity = progress.toString();

      if (deltaY >= threshold) {
        indicator.textContent = pullingText;
        indicator.style.background = 'rgba(59, 130, 246, 0.1)';
        indicator.style.color = '#3b82f6';
      } else {
        indicator.textContent = refreshText;
        indicator.style.background = 'rgba(0, 0, 0, 0.1)';
        indicator.style.color = '#666';
      }
    }
  };

  const handleTouchEnd = (e: TouchEvent) => {
    if (isRefreshing || !isPulling) return;

    const deltaY = currentY - startY;

    if (deltaY >= threshold) {
      isRefreshing = true;
      indicator.textContent = refreshingText;
      indicator.style.background = 'rgba(59, 130, 246, 0.2)';
      indicator.style.color = '#3b82f6';

      // Reset position
      element.style.transform = 'translateY(0)';
      indicator.style.top = '-50px';
      indicator.style.opacity = '0';

      // Trigger refresh
      onRefresh();

      // Reset after refresh
      setTimeout(() => {
        isRefreshing = false;
        indicator.textContent = refreshText;
        indicator.style.background = 'rgba(0, 0, 0, 0.1)';
        indicator.style.color = '#666';
      }, 1000);
    } else {
      // Reset position
      element.style.transform = 'translateY(0)';
      indicator.style.top = '-50px';
      indicator.style.opacity = '0';
    }

    isPulling = false;
  };

  const cleanup = addTouchHandlers(element, {
    onTouchStart: handleTouchStart,
    onTouchMove: handleTouchMove,
    onTouchEnd: handleTouchEnd,
  });

  return () => {
    cleanup();
    if (indicator.parentNode) {
      indicator.parentNode.removeChild(indicator);
    }
  };
};

// Mobile-specific CSS classes
export const mobileClasses = {
  // Touch targets
  touchTarget: 'min-h-[44px] min-w-[44px] p-2',
  touchTargetLarge: 'min-h-[48px] min-w-[48px] p-3',
  
  // Mobile spacing
  mobilePadding: 'p-4 sm:p-6',
  mobileMargin: 'm-4 sm:m-6',
  mobileGap: 'gap-4 sm:gap-6',
  
  // Mobile text sizes
  mobileText: 'text-sm sm:text-base',
  mobileHeading: 'text-lg sm:text-xl',
  mobileTitle: 'text-xl sm:text-2xl',
  
  // Mobile layout
  mobileStack: 'flex flex-col space-y-4',
  mobileGrid: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
  mobileFullWidth: 'w-full sm:w-auto',
  
  // Mobile interactions
  mobileTap: 'active:scale-95 transition-transform',
  mobileHover: 'hover:scale-105 sm:hover:scale-105',
  
  // Mobile forms
  mobileInput: 'text-base sm:text-sm', // Prevents zoom on iOS
  mobileButton: 'h-12 sm:h-10',
  
  // Mobile navigation
  mobileNav: 'fixed bottom-0 left-0 right-0 sm:relative sm:bottom-auto',
  mobileNavItem: 'flex-1 sm:flex-none',
};

// Responsive breakpoint utilities
export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

// Media query helpers
export const createMediaQuery = (breakpoint: keyof typeof breakpoints) => {
  return `@media (min-width: ${breakpoints[breakpoint]})`;
};

// Mobile-first responsive design helper
export const responsive = {
  mobile: (styles: string) => styles,
  tablet: (styles: string) => `${createMediaQuery('md')} { ${styles} }`,
  desktop: (styles: string) => `${createMediaQuery('lg')} { ${styles} }`,
  large: (styles: string) => `${createMediaQuery('xl')} { ${styles} }`,
};

// Viewport meta tag helper
export const getViewportMetaTag = (): string => {
  return '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">';
};

// Mobile performance optimizations
export const optimizeForMobile = (): void => {
  // Disable double-tap zoom
  document.addEventListener('touchstart', (e) => {
    if (e.touches.length > 1) {
      e.preventDefault();
    }
  }, { passive: false });

  // Prevent pull-to-refresh on body
  document.body.style.overscrollBehavior = 'contain';

  // Optimize scrolling
  document.documentElement.style.scrollBehavior = 'smooth';
};

// Mobile-specific event listeners
export const addMobileOptimizations = (): (() => void) => {
  const cleanupFunctions: (() => void)[] = [];

  // Prevent zoom on input focus (iOS)
  const preventZoom = (e: Event) => {
    const target = e.target as HTMLElement;
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
      const viewport = document.querySelector('meta[name="viewport"]') as HTMLMetaElement;
      if (viewport) {
        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
      }
    }
  };

  const restoreZoom = (e: Event) => {
    const target = e.target as HTMLElement;
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
      const viewport = document.querySelector('meta[name="viewport"]') as HTMLMetaElement;
      if (viewport) {
        viewport.content = 'width=device-width, initial-scale=1.0';
      }
    }
  };

  document.addEventListener('focusin', preventZoom);
  document.addEventListener('focusout', restoreZoom);

  cleanupFunctions.push(() => {
    document.removeEventListener('focusin', preventZoom);
    document.removeEventListener('focusout', restoreZoom);
  });

  return () => {
    cleanupFunctions.forEach(cleanup => cleanup());
  };
};

export default {
  isMobileDevice,
  isTouchDevice,
  isIOS,
  isAndroid,
  getViewportDimensions,
  isMobileViewport,
  isTabletViewport,
  isDesktopViewport,
  ensureTouchTarget,
  addTouchHandlers,
  addSwipeHandlers,
  addPullToRefresh,
  mobileClasses,
  breakpoints,
  createMediaQuery,
  responsive,
  getViewportMetaTag,
  optimizeForMobile,
  addMobileOptimizations,
};

