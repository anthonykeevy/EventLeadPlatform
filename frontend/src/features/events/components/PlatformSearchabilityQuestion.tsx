import React from 'react'
import { Info } from 'lucide-react'

interface PlatformSearchabilityQuestionProps {
  selectedOption: 'company-network' | 'platform' | null
  onSelect: (option: 'company-network' | 'platform') => void
  onBack: () => void
}

/**
 * Step 3B: Platform searchability question
 * 
 * Only shown if user skipped search in Step 2B
 * 
 * Options:
 * - "No, keep it within my company network" → IsPublic = True, IsSharedWithPlatform = False
 * - "Yes, make it searchable on the platform" → IsPublic = True, IsSharedWithPlatform = True, PublicReviewStatusID = PENDING
 */
export const PlatformSearchabilityQuestion: React.FC<PlatformSearchabilityQuestionProps> = ({
  selectedOption,
  onSelect,
  onBack,
}) => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Would you like to make this event searchable on the platform?
        </h3>
        <p className="text-sm text-gray-600">
          This helps other companies discover and link to your event when creating forms.
        </p>
      </div>

      {/* Info Banner */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex gap-3">
          <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-blue-800">
            <p className="font-medium mb-1">Making your event searchable:</p>
            <ul className="list-disc list-inside space-y-1 text-blue-700">
              <li>Helps other companies discover and link to your event</li>
              <li>Requires admin review for quality assurance (24-48 hours)</li>
              <li>Allows platform-wide visibility once approved</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Options */}
      <div className="space-y-4">
        {/* Company Network Only Option */}
        <label
          className={`flex items-start gap-4 p-4 border-2 rounded-lg cursor-pointer transition-all ${
            selectedOption === 'company-network'
              ? 'border-teal-600 bg-teal-50'
              : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
          }`}
        >
          <input
            type="radio"
            name="platformSearchability"
            value="company-network"
            checked={selectedOption === 'company-network'}
            onChange={() => onSelect('company-network')}
            className="mt-1 w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500"
            aria-label="No, keep it within my company network"
          />
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              No, keep it within my company network
            </div>
            <div className="text-sm text-gray-600 mt-1">
              Visible to your company and connected companies only. No review required.
            </div>
          </div>
        </label>

        {/* Platform Searchable Option */}
        <label
          className={`flex items-start gap-4 p-4 border-2 rounded-lg cursor-pointer transition-all ${
            selectedOption === 'platform'
              ? 'border-teal-600 bg-teal-50'
              : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
          }`}
        >
          <input
            type="radio"
            name="platformSearchability"
            value="platform"
            checked={selectedOption === 'platform'}
            onChange={() => onSelect('platform')}
            className="mt-1 w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500"
            aria-label="Yes, make it searchable on the platform"
          />
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              Yes, make it searchable on the platform
            </div>
            <div className="text-sm text-gray-600 mt-1">
              Others can discover and link to this event. Requires admin review (24-48 hours).
            </div>
          </div>
        </label>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center justify-between gap-3 pt-4 border-t">
        <button
          type="button"
          onClick={onBack}
          className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors flex items-center gap-2"
        >
          ← Back
        </button>
        {selectedOption && (
          <button
            type="button"
            onClick={() => onSelect(selectedOption)}
            className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 transition-colors"
          >
            Continue
          </button>
        )}
      </div>
    </div>
  )
}

