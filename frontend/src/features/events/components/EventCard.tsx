/**
 * Event Card Component - Story 2.4 Task 7
 * Displays event information in a card format
 */

import React from 'react'
import { Calendar, MapPin, Tag, Edit2, Trash2 } from 'lucide-react'
import { Event } from '../types/events.types'
import { StatusBadge } from './StatusBadge'

interface EventCardProps {
  event: Event
  onEdit: (event: Event) => void
  onDelete: (event: Event) => void
  onView?: (event: Event) => void
}

export function EventCard({ event, onEdit, onDelete, onView }: EventCardProps) {
  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'No date set'
    const timeZone = event.timezoneIdentifier || (() => {
      try {
        return Intl.DateTimeFormat().resolvedOptions().timeZone || 'Australia/Sydney'
      } catch {
        return 'Australia/Sydney'
      }
    })()

    try {
      return new Intl.DateTimeFormat('en-AU', {
        timeZone,
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(new Date(dateString))
    } catch {
      return new Date(dateString).toLocaleString('en-AU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }

  const getLocationDisplay = (): string => {
    const parts: string[] = []
    if (event.venueName) parts.push(event.venueName)
    if (event.city) parts.push(event.city)
    if (event.state) parts.push(event.state)
    return parts.length > 0 ? parts.join(', ') : 'Location not set'
  }

  return (
    <div
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 border border-gray-200 overflow-hidden cursor-pointer"
      onClick={() => onView?.(event)}
    >
      {/* Header with Status Badge */}
      <div className="p-4 pb-3 border-b border-gray-100">
        <div className="flex items-start justify-between mb-2">
          <div className="flex flex-col flex-1 pr-2">
            <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
              {event.name}
            </h3>
            {event.userRole && !event.userRole.is_legacy && (
              <span className="inline-flex items-center mt-1 px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800 w-fit">
                {event.userRole.role_name || 'Agency Access'}
              </span>
            )}
          </div>
          <StatusBadge status={event.eventStatus} />
        </div>
      </div>

      {/* Event Details */}
      <div className="p-4 space-y-3">
        {/* Date/Time */}
        <div className="flex items-start text-sm text-gray-600">
          <Calendar className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-teal-600" />
          <div>
            <div className="font-medium">Start: {formatDate(event.startDateTime)}</div>
            {event.endDateTime && (
              <div className="text-gray-500">End: {formatDate(event.endDateTime)}</div>
            )}
          </div>
        </div>

        {/* Location */}
        <div className="flex items-start text-sm text-gray-600">
          <MapPin className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-teal-600" />
          <span className="line-clamp-2">{getLocationDisplay()}</span>
        </div>

        {/* Event Type */}
        {event.eventType && (
          <div className="flex items-center text-sm text-gray-600">
            <Tag className="w-4 h-4 mr-2 flex-shrink-0 text-teal-600" />
            <span>{event.eventType.typeName}</span>
          </div>
        )}

        {/* Short Description */}
        {event.shortDescription && (
          <p className="text-sm text-gray-600 line-clamp-2 mt-2">
            {event.shortDescription}
          </p>
        )}
      </div>

      {/* Actions Footer */}
      <div className="px-4 py-3 bg-gray-50 border-t border-gray-100 flex items-center justify-end gap-2">
        <button
          onClick={(e) => {
            e.stopPropagation()
            onEdit(event)
          }}
          className="px-3 py-1.5 text-sm font-medium text-teal-600 hover:text-teal-700 hover:bg-teal-50 rounded-md transition-colors flex items-center gap-1"
          aria-label={`Edit ${event.name}`}
        >
          <Edit2 className="w-4 h-4" />
          Edit
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation()
            onDelete(event)
          }}
          className="px-3 py-1.5 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition-colors flex items-center gap-1"
          aria-label={`Delete ${event.name}`}
        >
          <Trash2 className="w-4 h-4" />
          Delete
        </button>
      </div>
    </div>
  )
}
