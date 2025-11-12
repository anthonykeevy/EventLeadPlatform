/**
 * Event Detail View - Story 2.4 Task 15
 * Displays complete event information in a detailed view
 */

import React from 'react'
import { Calendar, MapPin, Tag, Globe, Building2, Edit2, Trash2, ArrowLeft, X } from 'lucide-react'
import { Event } from '../types/events.types'
import { StatusBadge } from './StatusBadge'

interface EventDetailViewProps {
  event: Event | null
  onClose: () => void
  onEdit: (event: Event) => void
  onDelete: (event: Event) => void
}

export function EventDetailView({ event, onClose, onEdit, onDelete }: EventDetailViewProps) {
  if (!event) return null

  const defaultTimeZone = (() => {
    try {
      return Intl.DateTimeFormat().resolvedOptions().timeZone || 'Australia/Sydney'
    } catch {
      return 'Australia/Sydney'
    }
  })()

  const eventTimeZone = event.timezoneIdentifier || defaultTimeZone

  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'Not set'
    try {
      return new Intl.DateTimeFormat('en-AU', {
        timeZone: eventTimeZone,
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
      }).format(new Date(dateString))
    } catch {
      return new Date(dateString).toLocaleString('en-AU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
      })
    }
  }

  const formatDateTime = (dateString: string | null): string => {
    if (!dateString) return 'Not set'
    try {
      return new Intl.DateTimeFormat('en-AU', {
        timeZone: eventTimeZone,
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
      }).format(new Date(dateString))
    } catch {
      return new Date(dateString).toLocaleString('en-AU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
      })
    }
  }

  const getLocationDisplay = (): string => {
    const parts: string[] = []
    if (event.venueName) parts.push(event.venueName)
    if (event.venueAddress) parts.push(event.venueAddress)
    if (event.city) parts.push(event.city)
    if (event.state) parts.push(event.state)
    return parts.length > 0 ? parts.join(', ') : 'Location not set'
  }

  const getCoordinatesDisplay = (): string => {
    if (event.latitude !== null && event.longitude !== null) {
      return `${event.latitude.toFixed(6)}, ${event.longitude.toFixed(6)}`
    }
    return 'Not set'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div
        className="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden transform transition-all"
        role="dialog"
        aria-modal="true"
        aria-labelledby="event-detail-title"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 p-1 rounded transition-colors"
                aria-label="Close detail view"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <h2 id="event-detail-title" className="text-2xl font-bold">
                Event Details
              </h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 p-1 rounded transition-colors"
              aria-label="Close modal"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-180px)] p-6">
          {/* Event Name and Status */}
          <div className="mb-6 pb-6 border-b border-gray-200">
            <div className="flex items-start justify-between gap-4 mb-3">
              <h3 className="text-3xl font-bold text-gray-900 flex-1">
                {event.name}
              </h3>
              <StatusBadge status={event.eventStatus} />
            </div>
            {event.shortDescription && (
              <p className="text-lg text-gray-600 mt-2">
                {event.shortDescription}
              </p>
            )}
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Left Column */}
            <div className="space-y-6">
              {/* Date and Time */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-teal-600" />
                  Date & Time
                </h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Start:</span>{' '}
                    <span className="text-gray-600">{formatDateTime(event.startDateTime)}</span>
                  </div>
                  {event.endDateTime && (
                    <div>
                      <span className="font-medium text-gray-700">End:</span>{' '}
                      <span className="text-gray-600">{formatDateTime(event.endDateTime)}</span>
                    </div>
                  )}
                  {event.timezoneIdentifier && (
                    <div>
                      <span className="font-medium text-gray-700">Timezone:</span>{' '}
                      <span className="text-gray-600">{event.timezoneIdentifier}</span>
                    </div>
                  )}
                  {event.isRecurring && (
                    <div className="mt-2">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-teal-100 text-teal-800">
                        Recurring Event
                      </span>
                    </div>
                  )}
                </div>
              </section>

              {/* Location */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-teal-600" />
                  Location
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="text-gray-600">{getLocationDisplay()}</div>
                  {event.latitude !== null && event.longitude !== null && (
                    <div>
                      <span className="font-medium text-gray-700">Coordinates:</span>{' '}
                      <span className="text-gray-600">{getCoordinatesDisplay()}</span>
                    </div>
                  )}
                </div>
              </section>

              {/* Event Type and Industry */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Tag className="w-5 h-5 text-teal-600" />
                  Classification
                </h4>
                <div className="space-y-2 text-sm">
                  {event.eventType && (
                    <div>
                      <span className="font-medium text-gray-700">Event Type:</span>{' '}
                      <span className="text-gray-600">{event.eventType.typeName}</span>
                    </div>
                  )}
                  {event.tags && (
                    <div>
                      <span className="font-medium text-gray-700">Tags:</span>{' '}
                      <span className="text-gray-600">{event.tags}</span>
                    </div>
                  )}
                </div>
              </section>
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              {/* Description */}
              {event.description && (
                <section>
                  <h4 className="text-lg font-semibold text-gray-900 mb-3">
                    Description
                  </h4>
                  <p className="text-sm text-gray-600 whitespace-pre-wrap">
                    {event.description}
                  </p>
                </section>
              )}

              {/* Organizer Information */}
              {(event.organizerCompanyId || event.organizerContactEmail || event.organizerWebsite) && (
                <section>
                  <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <Building2 className="w-5 h-5 text-teal-600" />
                    Organizer
                  </h4>
                  <div className="space-y-2 text-sm">
                    {event.organizerContactEmail && (
                      <div>
                        <span className="font-medium text-gray-700">Email:</span>{' '}
                        <a
                          href={`mailto:${event.organizerContactEmail}`}
                          className="text-teal-600 hover:text-teal-700 underline"
                        >
                          {event.organizerContactEmail}
                        </a>
                      </div>
                    )}
                    {event.organizerWebsite && (
                      <div>
                        <span className="font-medium text-gray-700">Website:</span>{' '}
                        <a
                          href={event.organizerWebsite}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-teal-600 hover:text-teal-700 underline"
                        >
                          {event.organizerWebsite}
                        </a>
                      </div>
                    )}
                  </div>
                </section>
              )}

              {/* Visibility and Metrics */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Globe className="w-5 h-5 text-teal-600" />
                  Visibility & Metrics
                </h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Visibility:</span>{' '}
                    <span className="text-gray-600">
                      {event.isPublic ? (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          Public
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          Private
                        </span>
                      )}
                    </span>
                  </div>
                  {event.expectedAttendees !== null && (
                    <div>
                      <span className="font-medium text-gray-700">Expected Attendees:</span>{' '}
                      <span className="text-gray-600">{event.expectedAttendees.toLocaleString()}</span>
                    </div>
                  )}
                  {event.actualAttendees !== null && (
                    <div>
                      <span className="font-medium text-gray-700">Actual Attendees:</span>{' '}
                      <span className="text-gray-600">{event.actualAttendees.toLocaleString()}</span>
                    </div>
                  )}
                  <div>
                    <span className="font-medium text-gray-700">Forms Created:</span>{' '}
                    <span className="text-gray-600">{event.formsCreated}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Total Submissions:</span>{' '}
                    <span className="text-gray-600">{event.totalSubmissions}</span>
                  </div>
                </div>
              </section>

              {/* Metadata */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3">
                  Metadata
                </h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Created:</span>{' '}
                    <span className="text-gray-600">{formatDate(event.createdDate)}</span>
                  </div>
                  {event.updatedDate && (
                    <div>
                      <span className="font-medium text-gray-700">Last Updated:</span>{' '}
                      <span className="text-gray-600">{formatDate(event.updatedDate)}</span>
                    </div>
                  )}
                </div>
              </section>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 bg-gray-50 px-6 py-4 flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Close
          </button>
          <button
            type="button"
            onClick={() => onEdit(event)}
            className="px-4 py-2 bg-teal-600 text-white rounded-md text-sm font-medium hover:bg-teal-700 transition-colors flex items-center gap-2"
          >
            <Edit2 className="w-4 h-4" />
            Edit Event
          </button>
          <button
            type="button"
            onClick={() => onDelete(event)}
            className="px-4 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700 transition-colors flex items-center gap-2"
          >
            <Trash2 className="w-4 h-4" />
            Delete Event
          </button>
        </div>
      </div>
    </div>
  )
}

