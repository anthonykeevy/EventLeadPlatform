import React from 'react'

interface EventTypeSelectorProps {
  selectedType: 'private' | 'public' | null
  onSelect: (type: 'private' | 'public') => void
  onCancel: () => void
}

/**
 * Step 1: Initial event type selection screen
 * 
 * Purpose: Gather user intent without making them feel judged
 * - Uses neutral wording: "Is this event open to the public?"
 * - No visibility statements below options (remove friction)
 * - Simple labels: "No, this is a private event" and "Yes, this event is open to the public"
 */
export const EventTypeSelector: React.FC<EventTypeSelectorProps> = ({
  selectedType,
  onSelect,
  onCancel,
}) => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Is this event open to the public?
        </h3>
        <p className="text-sm text-gray-600">
          Choose how this event will be shared. You can change this later.
        </p>
      </div>

      <div className="space-y-4">
        {/* Private Option */}
        <label
          className={`flex items-start gap-4 p-4 border-2 rounded-lg cursor-pointer transition-all ${
            selectedType === 'private'
              ? 'border-teal-600 bg-teal-50'
              : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
          }`}
        >
          <input
            type="radio"
            name="eventType"
            value="private"
            checked={selectedType === 'private'}
            onChange={() => onSelect('private')}
            className="mt-1 w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500"
            aria-label="No, this is a private event"
          />
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              No, this is a private event
            </div>
            <div className="text-sm text-gray-600 mt-1">
              This event will only be visible to your company and connected companies.
            </div>
          </div>
        </label>

        {/* Public Option */}
        <label
          className={`flex items-start gap-4 p-4 border-2 rounded-lg cursor-pointer transition-all ${
            selectedType === 'public'
              ? 'border-teal-600 bg-teal-50'
              : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
          }`}
        >
          <input
            type="radio"
            name="eventType"
            value="public"
            checked={selectedType === 'public'}
            onChange={() => onSelect('public')}
            className="mt-1 w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500"
            aria-label="Yes, this event is open to the public"
          />
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              Yes, this event is open to the public
            </div>
            <div className="text-sm text-gray-600 mt-1">
              This event can be visible to others. You'll choose sharing options next.
            </div>
          </div>
        </label>
      </div>

      <div className="flex items-center justify-end gap-3 pt-4 border-t">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
        >
          Cancel
        </button>
        {selectedType && (
          <button
            type="button"
            onClick={() => onSelect(selectedType)}
            className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 transition-colors"
          >
            Continue
          </button>
        )}
      </div>
    </div>
  )
}

