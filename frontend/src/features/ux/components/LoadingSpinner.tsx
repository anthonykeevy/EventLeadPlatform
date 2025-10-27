import React from 'react';
import { Loader2 } from 'lucide-react';

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'primary' | 'secondary' | 'white' | 'gray';
  className?: string;
  'aria-label'?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  color = 'primary',
  className = '',
  'aria-label': ariaLabel = 'Loading',
}) => {
  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return 'h-4 w-4';
      case 'lg':
        return 'h-8 w-8';
      case 'xl':
        return 'h-12 w-12';
      default:
        return 'h-6 w-6';
    }
  };

  const getColorClasses = () => {
    switch (color) {
      case 'secondary':
        return 'text-gray-600';
      case 'white':
        return 'text-white';
      case 'gray':
        return 'text-gray-400';
      default:
        return 'text-blue-600';
    }
  };

  return (
    <div
      className={`inline-flex items-center justify-center ${getSizeClasses()} ${getColorClasses()} ${className}`}
      role="status"
      aria-label={ariaLabel}
    >
      <Loader2
        className="animate-spin"
        aria-hidden="true"
      />
      <span className="sr-only">{ariaLabel}</span>
    </div>
  );
};

// Button loading spinner variant
export const ButtonLoadingSpinner: React.FC<{
  className?: string;
}> = ({ className = '' }) => {
  return (
    <LoadingSpinner
      size="sm"
      color="white"
      className={`mr-2 ${className}`}
      aria-label="Loading"
    />
  );
};

// Page loading spinner
export const PageLoadingSpinner: React.FC<{
  message?: string;
  className?: string;
}> = ({ message = 'Loading...', className = '' }) => {
  return (
    <div className={`flex flex-col items-center justify-center py-12 ${className}`}>
      <LoadingSpinner size="xl" />
      <p className="mt-4 text-gray-600">{message}</p>
    </div>
  );
};

export default LoadingSpinner;
