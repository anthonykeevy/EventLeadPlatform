import React, { ReactNode } from 'react';
import { ErrorBoundary } from './ErrorBoundary';
import { ToastProvider } from './ToastProvider';

interface UXProviderProps {
  children: ReactNode;
  enableErrorBoundary?: boolean;
  enableToastNotifications?: boolean;
  toastPosition?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  maxToasts?: number;
}

export const UXProvider: React.FC<UXProviderProps> = ({
  children,
  enableErrorBoundary = true,
  enableToastNotifications = true,
  toastPosition = 'top-right',
  maxToasts = 5,
}) => {
  const content = enableToastNotifications ? (
    <ToastProvider position={toastPosition} maxToasts={maxToasts}>
      {children}
    </ToastProvider>
  ) : (
    children
  );

  return enableErrorBoundary ? (
    <ErrorBoundary>
      {content}
    </ErrorBoundary>
  ) : (
    content
  );
};

export default UXProvider;

