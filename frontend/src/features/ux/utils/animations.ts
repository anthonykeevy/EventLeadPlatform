// Animation utilities for micro-interactions and transitions

export interface AnimationOptions {
  duration?: number;
  easing?: string;
  delay?: number;
  fillMode?: 'none' | 'forwards' | 'backwards' | 'both';
  iterationCount?: number | 'infinite';
  direction?: 'normal' | 'reverse' | 'alternate' | 'alternate-reverse';
}

export interface SpringOptions {
  tension?: number;
  friction?: number;
  mass?: number;
  damping?: number;
}

// CSS transition utilities
export const createTransition = (
  properties: string | string[],
  options: AnimationOptions = {}
): string => {
  const {
    duration = 200,
    easing = 'ease-in-out',
    delay = 0,
  } = options;

  const props = Array.isArray(properties) ? properties.join(', ') : properties;
  return `${props} ${duration}ms ${easing} ${delay}ms`;
};

// Common transition presets
export const transitions = {
  // Button interactions
  buttonHover: createTransition(['transform', 'background-color', 'box-shadow'], {
    duration: 150,
    easing: 'ease-out',
  }),
  
  buttonActive: createTransition(['transform', 'background-color'], {
    duration: 100,
    easing: 'ease-in',
  }),

  // Form interactions
  inputFocus: createTransition(['border-color', 'box-shadow'], {
    duration: 200,
    easing: 'ease-out',
  }),

  inputError: createTransition(['border-color', 'box-shadow'], {
    duration: 300,
    easing: 'ease-out',
  }),

  // Modal and overlay animations
  modalEnter: createTransition(['opacity', 'transform'], {
    duration: 300,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  }),

  modalExit: createTransition(['opacity', 'transform'], {
    duration: 200,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  }),

  // Toast notifications
  toastEnter: createTransition(['opacity', 'transform'], {
    duration: 300,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  }),

  toastExit: createTransition(['opacity', 'transform'], {
    duration: 200,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  }),

  // Page transitions
  pageEnter: createTransition(['opacity', 'transform'], {
    duration: 400,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  }),

  // Loading states
  loadingPulse: createTransition(['opacity'], {
    duration: 1000,
    easing: 'ease-in-out',
    iterationCount: 'infinite',
    direction: 'alternate',
  }),

  // Skeleton loading
  skeletonShimmer: createTransition(['background-position'], {
    duration: 1500,
    easing: 'linear',
    iterationCount: 'infinite',
  }),
};

// Animation keyframes
export const keyframes = {
  // Fade animations
  fadeIn: {
    '0%': { opacity: '0' },
    '100%': { opacity: '1' },
  },

  fadeOut: {
    '0%': { opacity: '1' },
    '100%': { opacity: '0' },
  },

  // Slide animations
  slideInRight: {
    '0%': { transform: 'translateX(100%)', opacity: '0' },
    '100%': { transform: 'translateX(0)', opacity: '1' },
  },

  slideInLeft: {
    '0%': { transform: 'translateX(-100%)', opacity: '0' },
    '100%': { transform: 'translateX(0)', opacity: '1' },
  },

  slideInUp: {
    '0%': { transform: 'translateY(100%)', opacity: '0' },
    '100%': { transform: 'translateY(0)', opacity: '1' },
  },

  slideInDown: {
    '0%': { transform: 'translateY(-100%)', opacity: '0' },
    '100%': { transform: 'translateY(0)', opacity: '1' },
  },

  slideOutRight: {
    '0%': { transform: 'translateX(0)', opacity: '1' },
    '100%': { transform: 'translateX(100%)', opacity: '0' },
  },

  slideOutLeft: {
    '0%': { transform: 'translateX(0)', opacity: '1' },
    '100%': { transform: 'translateX(-100%)', opacity: '0' },
  },

  // Scale animations
  scaleIn: {
    '0%': { transform: 'scale(0.9)', opacity: '0' },
    '100%': { transform: 'scale(1)', opacity: '1' },
  },

  scaleOut: {
    '0%': { transform: 'scale(1)', opacity: '1' },
    '100%': { transform: 'scale(0.9)', opacity: '0' },
  },

  // Bounce animations
  bounceIn: {
    '0%': { transform: 'scale(0.3)', opacity: '0' },
    '50%': { transform: 'scale(1.05)', opacity: '1' },
    '70%': { transform: 'scale(0.9)' },
    '100%': { transform: 'scale(1)' },
  },

  // Shake animation
  shake: {
    '0%, 100%': { transform: 'translateX(0)' },
    '10%, 30%, 50%, 70%, 90%': { transform: 'translateX(-2px)' },
    '20%, 40%, 60%, 80%': { transform: 'translateX(2px)' },
  },

  // Pulse animation
  pulse: {
    '0%, 100%': { opacity: '1' },
    '50%': { opacity: '0.5' },
  },

  // Spin animation
  spin: {
    '0%': { transform: 'rotate(0deg)' },
    '100%': { transform: 'rotate(360deg)' },
  },

  // Skeleton shimmer
  shimmer: {
    '0%': { backgroundPosition: '-200% 0' },
    '100%': { backgroundPosition: '200% 0' },
  },

  // Success checkmark
  checkmark: {
    '0%': { transform: 'scale(0) rotate(45deg)', opacity: '0' },
    '50%': { transform: 'scale(1.2) rotate(45deg)', opacity: '1' },
    '100%': { transform: 'scale(1) rotate(45deg)', opacity: '1' },
  },
};

// CSS-in-JS animation helpers
export const createKeyframes = (name: string, keyframe: Record<string, Record<string, string>>): string => {
  const keyframeString = Object.entries(keyframe)
    .map(([percentage, styles]) => {
      const styleString = Object.entries(styles)
        .map(([property, value]) => `${property}: ${value}`)
        .join('; ');
      return `${percentage} { ${styleString} }`;
    })
    .join(' ');

  return `@keyframes ${name} { ${keyframeString} }`;
};

// Animation classes for Tailwind CSS
export const animationClasses = {
  // Fade animations
  'animate-fade-in': 'animate-fade-in',
  'animate-fade-out': 'animate-fade-out',
  
  // Slide animations
  'animate-slide-in-right': 'animate-slide-in-right',
  'animate-slide-in-left': 'animate-slide-in-left',
  'animate-slide-in-up': 'animate-slide-in-up',
  'animate-slide-in-down': 'animate-slide-in-down',
  'animate-slide-out-right': 'animate-slide-out-right',
  'animate-slide-out-left': 'animate-slide-out-left',
  
  // Scale animations
  'animate-scale-in': 'animate-scale-in',
  'animate-scale-out': 'animate-scale-out',
  
  // Bounce animations
  'animate-bounce-in': 'animate-bounce-in',
  
  // Utility animations
  'animate-shake': 'animate-shake',
  'animate-pulse': 'animate-pulse',
  'animate-spin': 'animate-spin',
  'animate-shimmer': 'animate-shimmer',
  'animate-checkmark': 'animate-checkmark',
};

// Hover effects
export const hoverEffects = {
  // Button hover effects
  buttonLift: 'hover:transform hover:scale-105 hover:shadow-lg',
  buttonGlow: 'hover:shadow-lg hover:shadow-blue-500/25',
  buttonSlide: 'hover:translate-x-1',
  
  // Card hover effects
  cardLift: 'hover:transform hover:-translate-y-1 hover:shadow-xl',
  cardGlow: 'hover:shadow-lg hover:shadow-gray-500/25',
  
  // Link hover effects
  linkUnderline: 'hover:underline hover:decoration-2 hover:underline-offset-4',
  linkColor: 'hover:text-blue-600 transition-colors',
  
  // Image hover effects
  imageZoom: 'hover:transform hover:scale-105 transition-transform',
  imageOverlay: 'hover:opacity-90 transition-opacity',
};

// Focus effects
export const focusEffects = {
  // Standard focus ring
  focusRing: 'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
  
  // Custom focus styles
  focusGlow: 'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:shadow-lg',
  focusScale: 'focus:outline-none focus:transform focus:scale-105',
  
  // Form input focus
  inputFocus: 'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
  inputFocusError: 'focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',
};

// Animation utilities for React components
export const useAnimation = (animationName: string, options: AnimationOptions = {}) => {
  const {
    duration = 300,
    easing = 'ease-in-out',
    delay = 0,
    fillMode = 'forwards',
    iterationCount = 1,
    direction = 'normal',
  } = options;

  return {
    animationName,
    animationDuration: `${duration}ms`,
    animationTimingFunction: easing,
    animationDelay: `${delay}ms`,
    animationFillMode: fillMode,
    animationIterationCount: iterationCount,
    animationDirection: direction,
  };
};

// Reduced motion support
export const respectsReducedMotion = (): boolean => {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

// Animation controller for complex sequences
export class AnimationController {
  private animations: Map<string, Animation> = new Map();
  private isReducedMotion: boolean;

  constructor() {
    this.isReducedMotion = respectsReducedMotion();
  }

  addAnimation(name: string, element: HTMLElement, keyframes: Keyframe[], options: KeyframeAnimationOptions) {
    if (this.isReducedMotion) {
      // Apply final state immediately for reduced motion
      const finalKeyframe = keyframes[keyframes.length - 1];
      Object.assign(element.style, finalKeyframe);
      return;
    }

    const animation = element.animate(keyframes, options);
    this.animations.set(name, animation);
    return animation;
  }

  playAnimation(name: string) {
    const animation = this.animations.get(name);
    if (animation) {
      animation.play();
    }
  }

  pauseAnimation(name: string) {
    const animation = this.animations.get(name);
    if (animation) {
      animation.pause();
    }
  }

  stopAnimation(name: string) {
    const animation = this.animations.get(name);
    if (animation) {
      animation.cancel();
      this.animations.delete(name);
    }
  }

  stopAllAnimations() {
    this.animations.forEach(animation => animation.cancel());
    this.animations.clear();
  }
}

// Utility to create staggered animations
export const createStaggeredAnimation = (
  elements: HTMLElement[],
  animationName: string,
  staggerDelay: number = 100
) => {
  elements.forEach((element, index) => {
    const delay = index * staggerDelay;
    element.style.animationDelay = `${delay}ms`;
    element.classList.add(animationName);
  });
};

// Utility to create entrance animations
export const createEntranceAnimation = (
  element: HTMLElement,
  type: 'fade' | 'slide' | 'scale' | 'bounce' = 'fade',
  direction: 'up' | 'down' | 'left' | 'right' = 'up'
) => {
  const animationClass = `animate-${type}-in-${direction}`;
  element.classList.add(animationClass);
};

// Utility to create exit animations
export const createExitAnimation = (
  element: HTMLElement,
  type: 'fade' | 'slide' | 'scale' = 'fade',
  direction: 'up' | 'down' | 'left' | 'right' = 'up'
) => {
  const animationClass = `animate-${type}-out-${direction}`;
  element.classList.add(animationClass);
};

export default {
  createTransition,
  transitions,
  keyframes,
  createKeyframes,
  animationClasses,
  hoverEffects,
  focusEffects,
  useAnimation,
  respectsReducedMotion,
  AnimationController,
  createStaggeredAnimation,
  createEntranceAnimation,
  createExitAnimation,
};

