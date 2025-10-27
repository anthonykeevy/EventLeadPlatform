import React, { createContext, useContext, useCallback, useState, ReactNode } from 'react';
import { ToastContainer, ToastProps, ToastType } from './Toast';

export interface ToastOptions {
  type: ToastType;
  title?: string;
  message: string;
  duration?: number;
  dismissible?: boolean;
}

interface ToastContextType {
  toasts: ToastProps[];
  showToast: (options: ToastOptions) => string;
  dismissToast: (id: string) => void;
  dismissAllToasts: () => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

interface ToastProviderProps {
  children: ReactNode;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  maxToasts?: number;
}

export const ToastProvider: React.FC<ToastProviderProps> = ({
  children,
  position = 'top-right',
  maxToasts = 5,
}) => {
  const [toasts, setToasts] = useState<ToastProps[]>([]);

  const showToast = useCallback((options: ToastOptions): string => {
    const id = Math.random().toString(36).substr(2, 9);
    
    const newToast: ToastProps = {
      id,
      ...options,
      onDismiss: dismissToast,
    };

    setToasts(prevToasts => {
      const updatedToasts = [...prevToasts, newToast];
      // Limit the number of toasts
      return updatedToasts.slice(-maxToasts);
    });

    return id;
  }, [maxToasts]);

  const dismissToast = useCallback((id: string) => {
    setToasts(prevToasts => prevToasts.filter(toast => toast.id !== id));
  }, []);

  const dismissAllToasts = useCallback(() => {
    setToasts([]);
  }, []);

  const contextValue: ToastContextType = {
    toasts,
    showToast,
    dismissToast,
    dismissAllToasts,
  };

  return (
    <ToastContext.Provider value={contextValue}>
      {children}
      <ToastContainer
        toasts={toasts}
        onDismiss={dismissToast}
        position={position}
      />
    </ToastContext.Provider>
  );
};

// Convenience hooks for different toast types
export const useToastNotifications = () => {
  const { showToast } = useToast();

  return {
    success: (message: string, title?: string, duration?: number) =>
      showToast({ type: 'success', message, title, duration }),
    
    error: (message: string, title?: string, duration?: number) =>
      showToast({ type: 'error', message, title, duration }),
    
    warning: (message: string, title?: string, duration?: number) =>
      showToast({ type: 'warning', message, title, duration }),
    
    info: (message: string, title?: string, duration?: number) =>
      showToast({ type: 'info', message, title, duration }),
  };
};

export default ToastProvider;

