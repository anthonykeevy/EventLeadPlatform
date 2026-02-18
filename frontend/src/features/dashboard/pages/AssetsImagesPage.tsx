/**
 * Assets — Images Page - Story 5.7
 * Company Settings → Assets → Images
 * Grid/list toggle; DnD + file picker; delete confirmation; display name; audit; forms usage; image swap
 */

import { Image, Grid3X3, List } from 'lucide-react'

export function AssetsImagesPage() {
  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Assets — Images</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Upload and manage company images. Use grid or list view. Images can be used as form backgrounds and in components.
        </p>
      </div>
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <Image className="w-16 h-16 text-gray-400 mb-4" />
        <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
          Image Assets
        </h3>
        <p className="text-gray-500 dark:text-gray-400 max-w-md">
          Grid/list view, drag-and-drop upload, display name, forms-using-image, and image swap will be implemented here.
          Infrastructure from Story 5.1 (backgrounds) will be extended.
        </p>
        <div className="mt-4 flex gap-2">
          <button className="p-2 rounded border border-gray-300 dark:border-gray-600" title="Grid view">
            <Grid3X3 className="w-5 h-5" />
          </button>
          <button className="p-2 rounded border border-gray-300 dark:border-gray-600" title="List view">
            <List className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
