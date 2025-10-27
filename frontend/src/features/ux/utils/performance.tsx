// Performance optimization utilities for better UX
import React from 'react';

export interface PerformanceOptions {
  enableLazyLoading?: boolean;
  enableCodeSplitting?: boolean;
  enableImageOptimization?: boolean;
  enableCaching?: boolean;
  enableDebouncing?: boolean;
  enableThrottling?: boolean;
}

// Debounce utility
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number,
  immediate = false
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout | null = null;

  return (...args: Parameters<T>) => {
    const later = () => {
      timeout = null;
      if (!immediate) func(...args);
    };

    const callNow = immediate && !timeout;
    
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    
    if (callNow) func(...args);
  };
};

// Throttle utility
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};

// Lazy loading utility
export const createLazyLoader = (options: {
  root?: Element | null;
  rootMargin?: string;
  threshold?: number | number[];
} = {}) => {
  const {
    root = null,
    rootMargin = '50px',
    threshold = 0.1,
  } = options;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const element = entry.target as HTMLElement;
          const src = element.getAttribute('data-src');
          const srcset = element.getAttribute('data-srcset');
          
          if (src) {
            if (element.tagName === 'IMG') {
              (element as HTMLImageElement).src = src;
            } else {
              element.style.backgroundImage = `url(${src})`;
            }
          }
          
          if (srcset && element.tagName === 'IMG') {
            (element as HTMLImageElement).srcset = srcset;
          }
          
          element.classList.add('loaded');
          observer.unobserve(element);
        }
      });
    },
    { root, rootMargin, threshold }
  );

  return {
    observe: (element: HTMLElement) => observer.observe(element),
    unobserve: (element: HTMLElement) => observer.unobserve(element),
    disconnect: () => observer.disconnect(),
  };
};

// Image optimization utility
export const optimizeImage = (
  src: string,
  options: {
    width?: number;
    height?: number;
    quality?: number;
    format?: 'webp' | 'jpeg' | 'png' | 'avif';
  } = {}
): string => {
  const {
    width,
    height,
    quality = 80,
    format = 'webp',
  } = options;

  // For now, return the original src
  // In a real app, you'd integrate with an image optimization service
  // like Cloudinary, ImageKit, or Next.js Image Optimization
  return src;
};

// Code splitting utility
export const createLazyComponent = <T extends React.ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>,
  fallback?: React.ComponentType<any>
) => {
  const LazyComponent = React.lazy(importFunc);

  return (props: React.ComponentProps<T>) => {
    const FallbackComponent = fallback;
    return (
      <React.Suspense fallback={FallbackComponent ? <FallbackComponent /> : <div>Loading...</div>}>
        <LazyComponent {...props} />
      </React.Suspense>
    );
  };
};

// Memory management utility
export class MemoryManager {
  private static instance: MemoryManager;
  private cleanupFunctions: Set<() => void> = new Set();
  private timers: Set<NodeJS.Timeout> = new Set();
  private intervals: Set<NodeJS.Timeout> = new Set();

  static getInstance(): MemoryManager {
    if (!MemoryManager.instance) {
      MemoryManager.instance = new MemoryManager();
    }
    return MemoryManager.instance;
  }

  addCleanupFunction(cleanup: () => void): void {
    this.cleanupFunctions.add(cleanup);
  }

  addTimer(timer: NodeJS.Timeout): void {
    this.timers.add(timer);
  }

  addInterval(interval: NodeJS.Timeout): void {
    this.intervals.add(interval);
  }

  cleanup(): void {
    // Run all cleanup functions
    this.cleanupFunctions.forEach(cleanup => cleanup());
    this.cleanupFunctions.clear();

    // Clear all timers
    this.timers.forEach(timer => clearTimeout(timer));
    this.timers.clear();

    // Clear all intervals
    this.intervals.forEach(interval => clearInterval(interval));
    this.intervals.clear();
  }
}

// Performance monitoring utility
export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private metrics: Map<string, number> = new Map();
  private observers: PerformanceObserver[] = [];

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  startTiming(name: string): void {
    performance.mark(`${name}-start`);
  }

  endTiming(name: string): number {
    performance.mark(`${name}-end`);
    performance.measure(name, `${name}-start`, `${name}-end`);
    
    const measure = performance.getEntriesByName(name)[0];
    const duration = measure.duration;
    
    this.metrics.set(name, duration);
    return duration;
  }

  getTiming(name: string): number | undefined {
    return this.metrics.get(name);
  }

  getAllTimings(): Record<string, number> {
    return Object.fromEntries(this.metrics);
  }

  measureWebVitals(): void {
    // First Contentful Paint
    const fcpObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        if (entry.name === 'first-contentful-paint') {
          this.metrics.set('FCP', entry.startTime);
        }
      });
    });
    fcpObserver.observe({ entryTypes: ['paint'] });
    this.observers.push(fcpObserver);

    // Largest Contentful Paint
    const lcpObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.metrics.set('LCP', lastEntry.startTime);
    });
    lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
    this.observers.push(lcpObserver);

    // First Input Delay
    const fidObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        if (entry.processingStart && entry.startTime) {
          this.metrics.set('FID', entry.processingStart - entry.startTime);
        }
      });
    });
    fidObserver.observe({ entryTypes: ['first-input'] });
    this.observers.push(fidObserver);

    // Cumulative Layout Shift
    let clsValue = 0;
    const clsObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        if (!(entry as any).hadRecentInput) {
          clsValue += (entry as any).value;
          this.metrics.set('CLS', clsValue);
        }
      });
    });
    clsObserver.observe({ entryTypes: ['layout-shift'] });
    this.observers.push(clsObserver);
  }

  getWebVitals(): {
    FCP?: number;
    LCP?: number;
    FID?: number;
    CLS?: number;
  } {
    return {
      FCP: this.metrics.get('FCP'),
      LCP: this.metrics.get('LCP'),
      FID: this.metrics.get('FID'),
      CLS: this.metrics.get('CLS'),
    };
  }

  cleanup(): void {
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
  }
}

// Bundle size analyzer utility
export const analyzeBundleSize = (): void => {
  if (process.env.NODE_ENV === 'development') {
    // This would integrate with webpack-bundle-analyzer or similar
    console.log('Bundle size analysis would be available in development mode');
  }
};

// Preloading utility
export const preloadResource = (href: string, as: string): void => {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.href = href;
  link.as = as;
  document.head.appendChild(link);
};

export const preloadImage = (src: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve();
    img.onerror = reject;
    img.src = src;
  });
};

export const preloadFont = (href: string, type: string = 'font/woff2'): void => {
  preloadResource(href, 'font');
  
  // Add font-display: swap for better performance
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = href;
  link.media = 'print';
  link.onload = () => {
    link.media = 'all';
  };
  document.head.appendChild(link);
};

// Caching utility
export class CacheManager {
  private static instance: CacheManager;
  private cache: Map<string, { data: any; timestamp: number; ttl: number }> = new Map();

  static getInstance(): CacheManager {
    if (!CacheManager.instance) {
      CacheManager.instance = new CacheManager();
    }
    return CacheManager.instance;
  }

  set(key: string, data: any, ttl: number = 300000): void { // 5 minutes default
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  get(key: string): any | null {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  has(key: string): boolean {
    const item = this.cache.get(key);
    if (!item) return false;

    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return false;
    }

    return true;
  }

  delete(key: string): boolean {
    return this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }

  size(): number {
    return this.cache.size;
  }
}

// Virtual scrolling utility
export interface VirtualScrollOptions {
  itemHeight: number;
  containerHeight: number;
  totalItems: number;
  overscan?: number;
}

export const createVirtualScroll = (options: VirtualScrollOptions) => {
  const {
    itemHeight,
    containerHeight,
    totalItems,
    overscan = 5,
  } = options;

  return {
    getVisibleRange: (scrollTop: number) => {
      const startIndex = Math.floor(scrollTop / itemHeight);
      const endIndex = Math.min(
        startIndex + Math.ceil(containerHeight / itemHeight) + overscan,
        totalItems - 1
      );

      return {
        startIndex: Math.max(0, startIndex - overscan),
        endIndex,
        totalHeight: totalItems * itemHeight,
        offsetY: startIndex * itemHeight,
      };
    },
  };
};

// Performance optimization hook
export const usePerformanceOptimization = (options: PerformanceOptions = {}) => {
  const {
    enableLazyLoading = true,
    enableCodeSplitting = true,
    enableImageOptimization = true,
    enableCaching = true,
    enableDebouncing = true,
    enableThrottling = true,
  } = options;

  React.useEffect(() => {
    const memoryManager = MemoryManager.getInstance();
    const performanceMonitor = PerformanceMonitor.getInstance();

    // Start performance monitoring
    performanceMonitor.measureWebVitals();

    // Cleanup on unmount
    return () => {
      memoryManager.cleanup();
      performanceMonitor.cleanup();
    };
  }, []);

  return {
    debounce: enableDebouncing ? debounce : (fn: any) => fn,
    throttle: enableThrottling ? throttle : (fn: any) => fn,
    createLazyLoader: enableLazyLoading ? createLazyLoader : () => ({ observe: () => {}, unobserve: () => {}, disconnect: () => {} }),
    optimizeImage: enableImageOptimization ? optimizeImage : (src: string) => src,
    createLazyComponent: enableCodeSplitting ? createLazyComponent : (component: any) => component,
    cache: enableCaching ? CacheManager.getInstance() : null,
  };
};

export default {
  debounce,
  throttle,
  createLazyLoader,
  optimizeImage,
  createLazyComponent,
  MemoryManager,
  PerformanceMonitor,
  analyzeBundleSize,
  preloadResource,
  preloadImage,
  preloadFont,
  CacheManager,
  createVirtualScroll,
  usePerformanceOptimization,
};
