/**
 * Assets — Documents Page - Story 5.7
 * Company Settings → Assets → Documents (infrastructure placeholder)
 */

import { FileText } from 'lucide-react'

export function AssetsDocumentsPage() {
  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Assets — Documents</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          General document assets. Infrastructure in place for future implementation.
        </p>
      </div>
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <FileText className="w-16 h-16 text-gray-400 mb-4" />
        <p className="text-gray-500 dark:text-gray-400 max-w-md">
          Document asset management coming soon.
        </p>
      </div>
    </div>
  )
}
