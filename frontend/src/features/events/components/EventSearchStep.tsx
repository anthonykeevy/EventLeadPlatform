import React, { useMemo, useState } from 'react'
import { Search, Calendar, MapPin, Building2, X } from 'lucide-react'
import { Event } from '../types/events.types'

interface EventSearchStepProps {
  onSearch: (searchTerm: string) => void
  onSkip: () => void
  onBack: () => void
  searchTerm: string
  searchResults: Event[]
  isSearching: boolean
  onSelectEvent: (event: Event) => void
  onClearSearch: () => void
}

/**
 * Step 2B: Search/Skip options screen
 * 
 * Shows when user selects "Public" event type
 * - Primary action: "Search for Existing Events"
 * - Secondary action: "Skip & Create New Event"
 * - If user selects existing event: Skip platform searchability question, proceed directly to full form
 */
export const EventSearchStep: React.FC<EventSearchStepProps> = ({
  onSearch,
  onSkip,
  onBack,
  searchTerm,
  searchResults,
  isSearching,
  onSelectEvent,
  onClearSearch,
}) => {
  const [localSearchTerm, setLocalSearchTerm] = useState(searchTerm)
  const defaultTimeZone = useMemo(
    () => {
      try {
        return Intl.DateTimeFormat().resolvedOptions().timeZone || 'Australia/Sydney'
      } catch {
        return 'Australia/Sydney'
      }
    },
    []
  )

  const formatDateRange = (start?: string | null, end?: string | null, timeZone?: string | null) => {
    if (!start) {
      return null
    }

    try {
      const formatter = new Intl.DateTimeFormat('en-AU', {
        timeZone: timeZone ?? defaultTimeZone,
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      })

      const startDate = formatter.format(new Date(start))
      if (!end) {
        return startDate
      }

      const endDate = formatter.format(new Date(end))
      return startDate === endDate ? startDate : `${startDate} - ${endDate}`
    } catch {
      const startDate = new Date(start).toLocaleDateString('en-AU')
      if (!end) {
        return startDate
      }
      const endDate = new Date(end).toLocaleDateString('en-AU')
      return startDate === endDate ? startDate : `${startDate} - ${endDate}`
    }
  }

  const handleSearch = (value: string) => {
    setLocalSearchTerm(value)
    if (value.length >= 2) {
      onSearch(value)
    }
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Search for Existing Events
        </h3>
        <p className="text-sm text-gray-600">
          Find similar events to use as a reference. This helps ensure consistency and can pre-fill your form.
        </p>
      </div>

      {/* Search Input */}
      <div className="space-y-4">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={localSearchTerm}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder="Search by event name..."
            className="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
            aria-label="Search for existing events"
          />
          {localSearchTerm && (
            <button
              type="button"
              onClick={() => {
                setLocalSearchTerm('')
                onClearSearch()
              }}
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
              aria-label="Clear search"
            >
              <X className="h-5 w-5 text-gray-400 hover:text-gray-600" />
            </button>
          )}
        </div>

        {isSearching && (
          <div className="text-sm text-gray-500 text-center py-2">
            Searching...
          </div>
        )}

        {/* Search Results */}
        {searchResults.length > 0 && (
          <div className="border border-gray-200 rounded-lg divide-y divide-gray-200 max-h-96 overflow-y-auto">
            {searchResults.map((event) => (
              <div
                key={event.eventId}
                className="p-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1">
                    <div className="font-medium text-sm text-gray-900 mb-1">
                      {event.name || 'Untitled Event'}
                    </div>
                    {event.shortDescription && (
                      <div className="text-xs text-gray-600 mt-1 line-clamp-2 mb-2">
                        {event.shortDescription}
                      </div>
                    )}
                    <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-500">
                      {event.startDateTime && (
                        <div className="flex items-center gap-1">
                          <Calendar size={12} className="text-gray-400" />
                          <span>
                            {formatDateRange(event.startDateTime, event.endDateTime, event.timezoneIdentifier)}
                          </span>
                        </div>
                      )}
                      {(event.city || event.venueName) && (
                        <div className="flex items-center gap-1">
                          <MapPin size={12} className="text-gray-400" />
                          <span>
                            {event.city || event.venueName}
                            {event.state && `, ${event.state}`}
                          </span>
                        </div>
                      )}
                      {event.organizerCompanyId && (
                        <div className="flex items-center gap-1">
                          <Building2 size={12} className="text-gray-400" />
                          <span>Organizer info available</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => onSelectEvent(event)}
                    className="px-3 py-1.5 text-xs font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 transition-colors whitespace-nowrap"
                  >
                    Use This Event
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {localSearchTerm.length >= 2 && searchResults.length === 0 && !isSearching && (
          <div className="text-sm text-gray-500 text-center py-4">
            {!navigator.onLine ? (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="font-medium text-yellow-800 mb-1">Search unavailable while offline</p>
                <p className="text-yellow-700 text-xs">
                  Please reconnect to search for events. You can still create a new event offline.
                </p>
              </div>
            ) : (
              'No events found. Try a different search term or skip to create a new event.'
            )}
          </div>
        )}
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
        <div className="flex gap-3">
          {localSearchTerm.length >= 2 && (
            <button
              type="button"
              onClick={() => {
                setLocalSearchTerm('')
                onClearSearch()
              }}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
            >
              Clear Search
            </button>
          )}
          <button
            type="button"
            onClick={onSkip}
            className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 transition-colors"
          >
            Skip & Create New Event
          </button>
        </div>
      </div>
    </div>
  )
}

