import React, { useState } from 'react'
import { Info, X, ExternalLink } from 'lucide-react'

interface ReviewProcessInfoBannerProps {
  onDismiss?: () => void
  guidelinesUrl?: string
}

/**
 * Review Process Info Banner Component
 * 
 * Explains review process (24-48 hour review time)
 * - Link to Public Event Guidelines policy
 * - Dismissible banner
 */
export const ReviewProcessInfoBanner: React.FC<ReviewProcessInfoBannerProps> = ({
  onDismiss,
  guidelinesUrl,
}) => {
  const [isDismissed, setIsDismissed] = useState(false)

  const handleDismiss = () => {
    setIsDismissed(true)
    if (onDismiss) {
      onDismiss()
    }
  }

  if (isDismissed) {
    return null
  }

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 relative">
      <button
        type="button"
        onClick={handleDismiss}
        className="absolute top-2 right-2 text-blue-600 hover:text-blue-800"
        aria-label="Dismiss banner"
      >
        <X className="w-4 h-4" />
      </button>

      <div className="flex gap-3 pr-6">
        <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
        <div className="flex-1">
          <h4 className="font-medium text-blue-900 mb-1">Review Process</h4>
          <p className="text-sm text-blue-800">
            Events submitted for platform sharing require admin review to ensure quality and consistency.
            Review typically takes <strong>24-48 hours</strong>. You'll be notified once your event is reviewed.
          </p>
          {guidelinesUrl && (
            <a
              href={guidelinesUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 mt-2 text-sm text-blue-600 hover:text-blue-800 underline"
              onClick={(e) => {
                // If it's a relative path, prevent default and show message
                if (guidelinesUrl.startsWith('/')) {
                  e.preventDefault()
                  alert('Public Event Guidelines:\n\nEvents submitted for platform sharing require admin review (24-48 hours). We check for content quality, completeness, and compliance with our guidelines.\n\nRequired fields for platform-sharing events:\n- Event Name\n- Full Description\n- Start Date/Time\n- Event Type\n- City\n- Country\n- Organizer Company')
                }
              }}
            >
              View Public Event Guidelines
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

