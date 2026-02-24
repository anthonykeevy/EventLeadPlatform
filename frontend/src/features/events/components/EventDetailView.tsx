/**
 * Event Detail View - Story 2.4 Task 15
 * Displays complete event information in a detailed view
 */

import { useState, useEffect } from 'react'
import { Calendar, MapPin, Tag, Globe, Building2, Edit2, Trash2, ArrowLeft, X, FileText, Plus, Share2, LogOut, Layout } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Event as IEvent } from '../types/events.types'
import { StatusBadge } from './StatusBadge'
import { getFormsByEvent } from '../../forms/api/formsApi'
import { Form } from '../../forms/types/form.types'
import { useToastNotifications } from '../../ux'
import { ShareEventModal } from './ShareEventModal'
import { useAuth } from '../../auth'

interface EventDetailViewProps {
  event: IEvent | null
  onClose: () => void
  onEdit: (event: IEvent) => void
  onDelete: (event: IEvent) => void
  onAddForm?: (eventId: number) => void
  onEditForm?: (form: Form) => void
  onDeleteForm?: (form: Form) => void
}

export function EventDetailView({ 
  event, 
  onClose, 
  onEdit, 
  onDelete,
  onAddForm,
  onEditForm,
  onDeleteForm
}: EventDetailViewProps) {
  const [forms, setForms] = useState<Form[]>([])
  const [isLoadingForms, setIsLoadingForms] = useState(false)
  const [showShareModal, setShowShareModal] = useState(false)
  const toast = useToastNotifications()
  const { user } = useAuth()

  const isShared = event?.companyId !== user?.company_id
  const canEdit = event?.userRole?.has_edit_event ?? !isShared
  const canShare = event?.userRole?.has_manage_participants ?? !isShared

  // Listen for form updates
  useEffect(() => {
    if (!event) return
    const handleFormUpdate = (e: Event) => {
      const customEvent = e as CustomEvent
      if (customEvent.detail.eventId === event.eventId) {
        loadForms()
      }
    }

    window.addEventListener('formCreated', handleFormUpdate)
    window.addEventListener('formUpdated', handleFormUpdate)

    return () => {
      window.removeEventListener('formCreated', handleFormUpdate)
      window.removeEventListener('formUpdated', handleFormUpdate)
    }
  }, [event?.eventId])

  useEffect(() => {
    if (!event) return
    loadForms()
  }, [event?.eventId])

  const loadForms = async () => {
    if (!event) return
    setIsLoadingForms(true)
    try {
      const response = await getFormsByEvent(event.eventId)
      setForms(response.forms)
    } catch (error) {
      console.error('Failed to load forms:', error)
      toast.error('Failed to load forms for this event', 'Error')
    } finally {
      setIsLoadingForms(false)
    }
  }

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

  if (!event) return null

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
            <div className="flex items-center gap-2">
              {/* Share button - Story 2.10 */}
              {canShare && (
                <button
                  onClick={() => setShowShareModal(true)}
                  className="text-white hover:text-gray-200 p-1 rounded transition-colors"
                  title="Share Event"
                >
                  <Share2 className="w-5 h-5" />
                </button>
              )}
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 p-1 rounded transition-colors"
                aria-label="Close modal"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
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
              {/* Forms Section - Story 2.10 */}
              <section>
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <FileText className="w-5 h-5 text-teal-600" />
                    Linked Forms
                  </h4>
                  {onAddForm && (
                    <button
                      onClick={() => onAddForm(event.eventId)}
                      className="text-sm text-teal-600 hover:text-teal-700 font-medium flex items-center gap-1"
                    >
                      <Plus className="w-4 h-4" />
                      Add Form
                    </button>
                  )}
                </div>
                
                {isLoadingForms ? (
                  <div className="text-sm text-gray-500">Loading forms...</div>
                ) : forms.length === 0 ? (
                  <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded-md border border-gray-100">
                    No forms linked to this event yet.
                  </div>
                ) : (
                  <div className="space-y-2">
                    {forms.map(form => (
                      <div 
                        key={form.formId}
                        className="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-md hover:shadow-sm transition-shadow"
                      >
                        <div>
                          <div className="font-medium text-sm text-gray-900">{form.formName}</div>
                          <div className="text-xs text-gray-500 mt-0.5 flex items-center gap-2">
                            <span 
                              className="px-1.5 py-0.5 rounded-full"
                              style={{ 
                                backgroundColor: `${form.formStatus?.statusColor}20`,
                                color: form.formStatus?.statusColor || '#666'
                              }}
                            >
                              {form.formStatus?.statusName}
                            </span>
                            <span>{form.totalSubmissions} submissions</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-1">
                          <Link
                             to={`/forms/${form.formId}/builder`}
                             className="p-1 text-gray-400 hover:text-indigo-600 rounded transition-colors"
                             aria-label="Design form"
                             title="Design form"
                          >
                            <Layout className="w-4 h-4" />
                          </Link>
                          {onEditForm && (
                            <button
                              onClick={() => onEditForm(form)}
                              className="p-1 text-gray-400 hover:text-teal-600 rounded transition-colors"
                              aria-label="Edit form"
                            >
                              <Edit2 className="w-4 h-4" />
                            </button>
                          )}
                          {onDeleteForm && (
                            <button
                              onClick={() => onDeleteForm(form)}
                              className="p-1 text-gray-400 hover:text-red-600 rounded transition-colors"
                              aria-label="Unlink form"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </section>

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
          {canEdit && (
            <button
              type="button"
              onClick={() => onEdit(event)}
              className="px-4 py-2 bg-teal-600 text-white rounded-md text-sm font-medium hover:bg-teal-700 transition-colors flex items-center gap-2"
            >
              <Edit2 className="w-4 h-4" />
              Edit Event
            </button>
          )}
          <button
            type="button"
            onClick={() => onDelete(event)}
            className={`px-4 py-2 ${isShared ? 'bg-orange-500 hover:bg-orange-600' : 'bg-red-600 hover:bg-red-700'} text-white rounded-md text-sm font-medium transition-colors flex items-center gap-2`}
          >
            {isShared ? <LogOut className="w-4 h-4" /> : <Trash2 className="w-4 h-4" />}
            {isShared ? "Leave Event" : "Delete Event"}
          </button>
        </div>
      </div>

      {/* Share Modal - Story 2.10 */}
      {showShareModal && (
        <ShareEventModal
          isOpen={showShareModal}
          eventId={event.eventId}
          eventName={event.name}
          onClose={() => setShowShareModal(false)}
        />
      )}
    </div>
  )
}
