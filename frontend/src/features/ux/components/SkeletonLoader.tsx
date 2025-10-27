import React from 'react';

export interface SkeletonLoaderProps {
  className?: string;
  children?: React.ReactNode;
  animate?: boolean;
}

export const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  className = '',
  children,
  animate = true,
}) => {
  const baseClasses = 'bg-gray-200 rounded';
  const animateClasses = animate ? 'animate-pulse' : '';
  
  return (
    <div
      className={`${baseClasses} ${animateClasses} ${className}`}
      aria-hidden="true"
    >
      {children}
    </div>
  );
};

// Common skeleton patterns
export const SkeletonText: React.FC<{
  lines?: number;
  className?: string;
}> = ({ lines = 1, className = '' }) => {
  return (
    <div className={`space-y-2 ${className}`}>
      {Array.from({ length: lines }).map((_, index) => (
        <SkeletonLoader
          key={index}
          className={`h-4 ${index === lines - 1 ? 'w-3/4' : 'w-full'}`}
        />
      ))}
    </div>
  );
};

export const SkeletonCard: React.FC<{
  className?: string;
}> = ({ className = '' }) => {
  return (
    <div className={`p-4 border rounded-lg ${className}`}>
      <div className="flex items-center space-x-3 mb-3">
        <SkeletonLoader className="h-10 w-10 rounded-full" />
        <div className="flex-1">
          <SkeletonText lines={2} />
        </div>
      </div>
      <SkeletonText lines={3} />
    </div>
  );
};

export const SkeletonTable: React.FC<{
  rows?: number;
  columns?: number;
  className?: string;
}> = ({ rows = 5, columns = 4, className = '' }) => {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={rowIndex} className="flex space-x-4">
          {Array.from({ length: columns }).map((_, colIndex) => (
            <SkeletonLoader
              key={colIndex}
              className={`h-4 flex-1 ${colIndex === columns - 1 ? 'w-1/2' : ''}`}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export const SkeletonList: React.FC<{
  items?: number;
  className?: string;
}> = ({ items = 5, className = '' }) => {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: items }).map((_, index) => (
        <div key={index} className="flex items-center space-x-3">
          <SkeletonLoader className="h-8 w-8 rounded" />
          <div className="flex-1">
            <SkeletonText lines={1} />
          </div>
        </div>
      ))}
    </div>
  );
};

// Dashboard-specific skeletons
export const SkeletonKPICard: React.FC<{
  className?: string;
}> = ({ className = '' }) => {
  return (
    <div className={`p-6 bg-white rounded-lg shadow ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <SkeletonLoader className="h-4 w-24" />
        <SkeletonLoader className="h-6 w-6 rounded" />
      </div>
      <SkeletonLoader className="h-8 w-16 mb-2" />
      <SkeletonLoader className="h-3 w-20" />
    </div>
  );
};

export const SkeletonCompanyCard: React.FC<{
  className?: string;
}> = ({ className = '' }) => {
  return (
    <div className={`p-4 border rounded-lg ${className}`}>
      <div className="flex items-start space-x-3">
        <SkeletonLoader className="h-12 w-12 rounded" />
        <div className="flex-1">
          <SkeletonLoader className="h-5 w-32 mb-2" />
          <SkeletonLoader className="h-4 w-48 mb-2" />
          <SkeletonLoader className="h-3 w-24" />
        </div>
        <SkeletonLoader className="h-8 w-8 rounded" />
      </div>
    </div>
  );
};

export default SkeletonLoader;

