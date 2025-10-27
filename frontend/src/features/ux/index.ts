// UX Enhancement & Polish Feature
// Story 1.17: Comprehensive UX improvements for Epic 1

// Components
export { ErrorBoundary } from './components/ErrorBoundary';
export { ErrorMessage } from './components/ErrorMessage';
export { NetworkError, NetworkErrorMessage } from './components/NetworkError';
export { LoadingSpinner, ButtonLoadingSpinner, PageLoadingSpinner } from './components/LoadingSpinner';
export { 
  SkeletonLoader, 
  SkeletonText, 
  SkeletonCard, 
  SkeletonTable, 
  SkeletonList,
  SkeletonKPICard,
  SkeletonCompanyCard 
} from './components/SkeletonLoader';
export { 
  ProgressBar, 
  StepProgress, 
  CircularProgress 
} from './components/ProgressBar';
export { 
  Toast, 
  ToastContainer 
} from './components/Toast';
export { 
  ToastProvider, 
  useToast, 
  useToastNotifications 
} from './components/ToastProvider';
export { EnhancedFormInput } from './components/EnhancedFormInput';
export { UXProvider } from './components/UXProvider';

// Hooks
export { 
  useFormValidation, 
  useFieldValidation 
} from './hooks/useFormValidation';
export { 
  useAutoSave, 
  useFormAutoSave 
} from './hooks/useAutoSave';
export { 
  useKeyboardNavigation, 
  useFocusTrap, 
  useArrowNavigation 
} from './hooks/useKeyboardNavigation';

// Utils
export * from './utils/accessibility';
export * from './utils/animations';
export * from './utils/mobile';
export * from './utils/performance';

// Types
export type { ToastType } from './components/Toast';
export type { ToastOptions } from './components/ToastProvider';
export type { ToastProps } from './components/Toast';
export type { ToastContainerProps } from './components/Toast';
export type { EnhancedFormInputProps } from './components/EnhancedFormInput';
export type { ValidationRule, ValidationRules, ValidationErrors } from './hooks/useFormValidation';
export type { UseFormValidationOptions, UseFormValidationReturn } from './hooks/useFormValidation';
export type { UseAutoSaveOptions, UseAutoSaveReturn } from './hooks/useAutoSave';
export type { KeyboardNavigationOptions, UseKeyboardNavigationReturn } from './hooks/useKeyboardNavigation';
export type { UseFocusTrapOptions } from './hooks/useKeyboardNavigation';
export type { UseArrowNavigationOptions } from './hooks/useKeyboardNavigation';
export type { AccessibilityOptions } from './utils/accessibility';
