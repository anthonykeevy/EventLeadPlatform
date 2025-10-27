import React from 'react';
import { WifiOff, RefreshCw, AlertTriangle } from 'lucide-react';
import { ErrorMessage } from './ErrorMessage';

export interface NetworkErrorProps {
  onRetry?: () => void;
  onGoOffline?: () => void;
  className?: string;
  showOfflineOption?: boolean;
}

export const NetworkError: React.FC<NetworkErrorProps> = ({
  onRetry,
  onGoOffline,
  className = '',
  showOfflineOption = false,
}) => {
  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    } else {
      // Default retry behavior - reload the page
      window.location.reload();
    }
  };

  const handleGoOffline = () => {
    if (onGoOffline) {
      onGoOffline();
    }
  };

  return (
    <div className={`text-center py-12 px-4 ${className}`}>
      <div className="max-w-md mx-auto">
        <div className="flex justify-center mb-4">
          <WifiOff className="h-16 w-16 text-gray-400" />
        </div>
        
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          Connection Lost
        </h2>
        
        <p className="text-gray-600 mb-6">
          It looks like you're not connected to the internet. Please check your connection and try again.
        </p>

        <div className="space-y-3">
          <button
            onClick={handleRetry}
            className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            aria-label="Retry connection"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Try Again
          </button>

          {showOfflineOption && onGoOffline && (
            <button
              onClick={handleGoOffline}
              className="w-full flex items-center justify-center px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
              aria-label="Continue offline"
            >
              <AlertTriangle className="h-4 w-4 mr-2" />
              Continue Offline
            </button>
          )}
        </div>

        <div className="mt-6 text-sm text-gray-500">
          <p>
            If the problem persists, please check:
          </p>
          <ul className="mt-2 space-y-1 text-left">
            <li>• Your internet connection</li>
            <li>• Your firewall settings</li>
            <li>• Whether the service is temporarily unavailable</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

// Specialized network error message component
export const NetworkErrorMessage: React.FC<{
  onRetry?: () => void;
  className?: string;
}> = ({ onRetry, className }) => {
  return (
    <ErrorMessage
      title="Network Error"
      message="Unable to connect to the server. Please check your internet connection and try again."
      type="error"
      onRetry={onRetry}
      retryLabel="Retry Connection"
      className={className}
    />
  );
};

export default NetworkError;

