/**
 * Assets — Terms Page - Story 5.7
 * Company Settings → Assets → Terms
 * PDF + URL; URL validation; production simulation
 */

import { FileText } from 'lucide-react'

export function AssetsTermsPage() {
  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Assets — Terms of Agreement</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Upload PDF or add URL for Terms of Service. When defined, forms with Terms component will use these automatically.
        </p>
      </div>
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <FileText className="w-16 h-16 text-gray-400 mb-4" />
        <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
          Terms of Agreement
        </h3>
        <p className="text-gray-500 dark:text-gray-400 max-w-md">
          PDF upload and URL support, validation, production simulation, and Terms component auto-mapping will be implemented here.
        </p>
      </div>
    </div>
  )
}
