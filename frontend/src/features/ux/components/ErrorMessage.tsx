import React from 'react';
import { AlertCircle, X, RefreshCw } from 'lucide-react';

export interface ErrorMessageProps {
  title?: string;
  message: string;
  type?: 'error' | 'warning' | 'info';
  dismissible?: boolean;
  onDismiss?: () => void;
  onRetry?: () => void;
  retryLabel?: string;
  className?: string;
  'aria-live'?: 'polite' | 'assertive' | 'off';
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  title = 'Error',
  message,
  type = 'error',
  dismissible = false,
  onDismiss,
  onRetry,
  retryLabel = 'Try Again',
  className = '',
  'aria-live': ariaLive = 'assertive',
}) => {
  const getTypeStyles = () => {
    switch (type) {
      case 'warning':
        return {
          container: 'bg-yellow-50 border-yellow-200',
          icon: 'text-yellow-600',
          title: 'text-yellow-800',
          message: 'text-yellow-700',
        };
      case 'info':
        return {
          container: 'bg-blue-50 border-blue-200',
          icon: 'text-blue-600',
          title: 'text-blue-800',
          message: 'text-blue-700',
        };
      default:
        return {
          container: 'bg-red-50 border-red-200',
          icon: 'text-red-600',
          title: 'text-red-800',
          message: 'text-red-700',
        };
    }
  };

  const styles = getTypeStyles();

  return (
    <div
      className={`border rounded-md p-4 ${styles.container} ${className}`}
      role="alert"
      aria-live={ariaLive}
      aria-atomic="true"
    >
      <div className="flex">
        <div className="flex-shrink-0">
          <AlertCircle className={`h-5 w-5 ${styles.icon}`} aria-hidden="true" />
        </div>
        
        <div className="ml-3 flex-1">
          <h3 className={`text-sm font-medium ${styles.title}`}>
            {title}
          </h3>
          
          <div className={`mt-2 text-sm ${styles.message}`}>
            <p>{message}</p>
          </div>

          {(onRetry || (dismissible && onDismiss)) && (
            <div className="mt-4 flex space-x-3">
              {onRetry && (
                <button
                  type="button"
                  onClick={onRetry}
                  className={`inline-flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                    type === 'error'
                      ? 'text-red-700 bg-red-100 hover:bg-red-200 focus:ring-red-500'
                      : type === 'warning'
                      ? 'text-yellow-700 bg-yellow-100 hover:bg-yellow-200 focus:ring-yellow-500'
                      : 'text-blue-700 bg-blue-100 hover:bg-blue-200 focus:ring-blue-500'
                  }`}
                  aria-label={retryLabel}
                >
                  <RefreshCw className="h-4 w-4 mr-1" />
                  {retryLabel}
                </button>
              )}
              
              {dismissible && onDismiss && (
                <button
                  type="button"
                  onClick={onDismiss}
                  className={`inline-flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                    type === 'error'
                      ? 'text-red-700 bg-red-100 hover:bg-red-200 focus:ring-red-500'
                      : type === 'warning'
                      ? 'text-yellow-700 bg-yellow-100 hover:bg-yellow-200 focus:ring-yellow-500'
                      : 'text-blue-700 bg-blue-100 hover:bg-blue-200 focus:ring-blue-500'
                  }`}
                  aria-label="Dismiss error"
                >
                  <X className="h-4 w-4 mr-1" />
                  Dismiss
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;

