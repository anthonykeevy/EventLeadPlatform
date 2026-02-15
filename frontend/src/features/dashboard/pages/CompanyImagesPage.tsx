/**
 * Company Images Page - Placeholder
 * Company Settings → Company Images (future)
 */

import { Image } from 'lucide-react'

export function CompanyImagesPage() {
  return (
    <div className="h-full flex flex-col items-center justify-center p-8 text-center">
      <Image className="w-16 h-16 text-gray-400 mb-4" />
      <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
        Company Images
      </h2>
      <p className="text-gray-500 dark:text-gray-400 max-w-sm">
        Manage company logos and branding images. This feature is coming soon.
      </p>
    </div>
  )
}
