import React from 'react';
import { AlertCircle, Loader2 } from 'lucide-react';

interface ManualFallbackAction {
  label: string;
  onActivate: () => void;
}

interface EdfLookupResultsPanelProps {
  isLoading: boolean;
  error: string | null;
  emptyMessage?: string;
  showEmpty: boolean;
  children?: React.ReactNode;
  /** Optional one-line header above results (e.g. "6 companies found"). */
  resultCountLabel?: string;
  /** Shown on no-results / API error panels when manual entry is enabled. */
  manualFallback?: ManualFallbackAction;
}

function ManualFallbackLink({ manualFallback }: { manualFallback: ManualFallbackAction }) {
  return (
    <button
      type="button"
      onClick={manualFallback.onActivate}
      className="mt-2 text-sm font-medium underline hover:opacity-80 text-left"
    >
      {manualFallback.label}
    </button>
  );
}

export const EdfLookupResultsPanel: React.FC<EdfLookupResultsPanelProps> = ({
  isLoading,
  error,
  emptyMessage = 'No matches found.',
  showEmpty,
  children,
  resultCountLabel,
  manualFallback,
}) => {
  if (isLoading) {
    return (
      <div className="mt-2 flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 py-2">
        <Loader2 className="w-4 h-4 animate-spin shrink-0" />
        <span>Searching…</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-2 rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/20 dark:border-red-800 p-3 text-sm text-red-700 dark:text-red-300">
        <div className="flex items-start gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <div className="flex-1 min-w-0">
            <span>{error}</span>
            {manualFallback ? <ManualFallbackLink manualFallback={manualFallback} /> : null}
          </div>
        </div>
      </div>
    );
  }

  if (showEmpty) {
    return (
      <div className="mt-2 rounded-lg border border-yellow-200 bg-yellow-50 dark:bg-yellow-900/20 dark:border-yellow-800 p-3 text-sm text-yellow-800 dark:text-yellow-200">
        <p>{emptyMessage}</p>
        {manualFallback ? <ManualFallbackLink manualFallback={manualFallback} /> : null}
      </div>
    );
  }

  if (!children) return null;

  return (
    <div className="max-h-48 overflow-y-auto rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-900 shadow-lg ring-1 ring-black/5">
      {resultCountLabel ? (
        <div className="px-3 py-1.5 text-xs text-gray-500 dark:text-gray-400 border-b border-gray-100 dark:border-gray-800 sticky top-0 bg-white dark:bg-gray-900">
          {resultCountLabel}
        </div>
      ) : null}
      {children}
    </div>
  );
};
