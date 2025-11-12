import React from 'react'
import { Info, Search } from 'lucide-react'

interface EventVisibilitySelectorProps {
  isPublic: boolean
  isSharedWithPlatform: boolean
  onPublicChange: (isPublic: boolean) => void
  onPlatformSharingChange: (isShared: boolean) => void
  onSearchClick?: () => void
  showSearchButton?: boolean
  disabled?: boolean
}

/**
 * Event Visibility Selector Component
 * 
 * Used in full form view (Step 4)
 * - Platform sharing options (Company Network Only vs Share with Platform)
 * - Shown when IsPublic = True
 * - Compact "Search Event" button next to Public radio (shown when user skipped search)
 * - Progressive disclosure based on selection
 * - Help text and tooltips for each option
 */
export const EventVisibilitySelector: React.FC<EventVisibilitySelectorProps> = ({
  isPublic,
  isSharedWithPlatform,
  onPublicChange,
  onPlatformSharingChange,
  onSearchClick,
  showSearchButton = false,
  disabled = false,
}) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium text-gray-700">
          Event Visibility <span className="text-red-500">*</span>
        </label>
        {showSearchButton && onSearchClick && (
          <button
            type="button"
            onClick={onSearchClick}
            className="ml-2 px-2 py-1 text-xs font-medium text-teal-600 hover:text-teal-700 border border-teal-300 rounded hover:bg-teal-50 transition-colors flex items-center gap-1"
            disabled={disabled}
          >
            <Search className="w-3 h-3" />
            Search Events
          </button>
        )}
      </div>

      {/* Public/Private Selection */}
      <div className="flex gap-4">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="isPublic"
            value="private"
            checked={!isPublic}
            onChange={() => onPublicChange(false)}
            disabled={disabled}
            className="w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <span className="text-sm font-medium text-gray-900">Private</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="isPublic"
            value="public"
            checked={isPublic}
            onChange={() => onPublicChange(true)}
            disabled={disabled}
            className="w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <span className="text-sm font-medium text-gray-900">Public</span>
        </label>
      </div>

      {/* Platform Sharing Options - Only shown when Public */}
      {isPublic && (
        <div className="ml-6 mt-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Platform Sharing
          </label>
          <div className="space-y-3">
            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="radio"
                name="platformSharing"
                value="company-network"
                checked={!isSharedWithPlatform}
                onChange={() => onPlatformSharingChange(false)}
                disabled={disabled}
                className="mt-1 w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900">
                  Company Network Only
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  Visible to your company and connected companies. No review required.
                </div>
              </div>
            </label>

            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="radio"
                name="platformSharing"
                value="platform"
                checked={isSharedWithPlatform}
                onChange={() => onPlatformSharingChange(true)}
                disabled={disabled}
                className="mt-1 w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900">
                  Share with Platform
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  Make this event searchable on the platform. Requires admin review (24-48 hours).
                </div>
              </div>
            </label>
          </div>

          {/* Help Text */}
          <div className="mt-4 pt-3 border-t border-gray-200">
            <div className="flex gap-2 text-xs text-gray-600">
              <Info className="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium mb-1">Platform sharing benefits:</p>
                <ul className="list-disc list-inside space-y-0.5">
                  <li>Helps other companies discover your event</li>
                  <li>Allows linking to your event when creating forms</li>
                  <li>Requires admin review for quality assurance</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

