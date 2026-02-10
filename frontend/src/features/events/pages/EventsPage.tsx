/**
 * Events Page - Story 2.4 Task 6
 * Main event management page with list, search, and filters
 */

import { useState, useEffect, useCallback } from 'react'
import { Plus, Search, Filter, X } from 'lucide-react'
import { getEvents, getEventTypes, getEventStatuses } from '../api/eventsApi'
import { Event, EventType, EventStatus, EventFilters } from '../types/events.types'
import { EventCard } from '../components/EventCard'
import { CreateEventModal } from '../components/CreateEventModal'
import { EditEventModal } from '../components/EditEventModal'
import { DeleteEventConfirmModal } from '../components/DeleteEventConfirmModal'
import { EventDetailView } from '../components/EventDetailView'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'
import { ErrorMessage } from '../../ux/components/ErrorMessage'
import { CreateFormModal, EditFormModal, DeleteFormConfirmModal } from '../../forms'
import { Form } from '../../forms/types/form.types'
import { useAuth } from '../../auth'

export function EventsPage() {
  const { user } = useAuth()
  // State
  const [events, setEvents] = useState<Event[]>([])

  const [eventTypes, setEventTypes] = useState<EventType[]>([])
  const [eventStatuses, setEventStatuses] = useState<EventStatus[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [, setIsLoadingEvents] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const pageSize = 20

  // Filter state
  const [searchQuery, setSearchQuery] = useState('')
  const [_filters, setFilters] = useState<EventFilters>({})
  const [showFilters, setShowFilters] = useState(false)
  const [selectedEventTypeId, setSelectedEventTypeId] = useState<number | undefined>(undefined)
  const [selectedStatusId, setSelectedStatusId] = useState<number | undefined>(undefined)
  const [dateFrom, setDateFrom] = useState<string>('')
  const [dateTo, setDateTo] = useState<string>('')

  // Modal state
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingEvent, setEditingEvent] = useState<Event | null>(null)
  const [deletingEvent, setDeletingEvent] = useState<Event | null>(null)
  const [viewingEvent, setViewingEvent] = useState<Event | null>(null)

  // Form modals state
  const [showCreateFormModal, setShowCreateFormModal] = useState(false)
  const [showEditFormModal, setShowEditFormModal] = useState(false)
  const [showDeleteFormModal, setShowDeleteFormModal] = useState(false)
  const [formEventId, setFormEventId] = useState<number | null>(null)
  const [selectedForm, setSelectedForm] = useState<Form | null>(null)

  const toast = useToastNotifications()


  // Load reference data on mount
  useEffect(() => {
    const loadReferenceData = async () => {
      try {
        const [types, statuses] = await Promise.all([
          getEventTypes(),
          getEventStatuses()
        ])
        setEventTypes(types)
        setEventStatuses(statuses)
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load reference data'
        setError(errorMessage)
        toast.error(errorMessage, 'Failed to load event types and statuses')
      }
    }

    loadReferenceData()
  }, [toast])

  // Load events
  const loadEvents = useCallback(async () => {
    setIsLoadingEvents(true)
    setError(null)

    try {
      const filtersToUse: EventFilters = {}
      
      if (selectedEventTypeId) filtersToUse.eventTypeId = selectedEventTypeId
      if (selectedStatusId) filtersToUse.statusId = selectedStatusId
      if (dateFrom) filtersToUse.dateFrom = dateFrom
      if (dateTo) filtersToUse.dateTo = dateTo
      if (searchQuery.trim()) filtersToUse.search = searchQuery.trim()

      const response = await getEvents(page, pageSize, filtersToUse)
      setEvents(response.events)
      setTotal(response.total)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load events'
      setError(errorMessage)
      toast.error(errorMessage, 'Failed to load events')
    } finally {
      setIsLoadingEvents(false)
      setIsLoading(false)
    }
  }, [page, searchQuery, selectedEventTypeId, selectedStatusId, dateFrom, dateTo, toast])

  // Load events when filters or page changes
  useEffect(() => {
    loadEvents()
  }, [loadEvents])

  // Handle create event
  const handleCreateSuccess = () => {
    setShowCreateModal(false)
    toast.success('The event has been created successfully', 'Event created')
    loadEvents()
  }

  // Handle edit event
  const handleEdit = (event: Event) => {
    setEditingEvent(event)
  }

  const handleEditSuccess = () => {
    setEditingEvent(null)
    toast.success('The event has been updated successfully', 'Event updated')
    loadEvents()
  }

  // Handle delete event
  const handleDelete = (event: Event) => {
    setDeletingEvent(event)
  }

  const handleDeleteSuccess = () => {
    setDeletingEvent(null)
    toast.success('The event has been deleted successfully', 'Event deleted')
    loadEvents()
  }

  // Handle create form
  const handleCreateForm = (eventId: number) => {
    setFormEventId(eventId)
    setShowCreateFormModal(true)
  }

  const handleFormCreated = () => {
    setShowCreateFormModal(false)
    const eventId = formEventId
    setFormEventId(null)
    // Dispatch custom event to refresh forms for this event
    if (eventId) {
      window.dispatchEvent(new CustomEvent('formCreated', { detail: { eventId } }))
    }
  }

  // Handle edit form
  const handleEditForm = (form: Form) => {
    setSelectedForm(form)
    setShowEditFormModal(true)
  }

  const handleFormUpdated = () => {
    setShowEditFormModal(false)
    const eventId = selectedForm?.eventId
    setSelectedForm(null)
    if (eventId) {
      window.dispatchEvent(new CustomEvent('formUpdated', { detail: { eventId } }))
    }
  }

  // Handle delete form
  const handleDeleteForm = (form: Form) => {
    setSelectedForm(form)
    setShowDeleteFormModal(true)
  }

  const handleFormDeleted = () => {
    setShowDeleteFormModal(false)
    const eventId = selectedForm?.eventId
    setSelectedForm(null)
    if (eventId) {
      window.dispatchEvent(new CustomEvent('formUpdated', { detail: { eventId } }))
    }
  }

  // Clear filters
  const handleClearFilters = () => {
    setSearchQuery('')
    setSelectedEventTypeId(undefined)
    setSelectedStatusId(undefined)
    setDateFrom('')
    setDateTo('')
    setPage(1)
  }

  const hasActiveFilters = searchQuery || selectedEventTypeId || selectedStatusId || dateFrom || dateTo

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Events</h1>
              <p className="text-gray-600 mt-1">Manage your company's events</p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn-primary flex items-center gap-2"
              aria-label="Create new event"
            >
              <Plus className="w-5 h-5" />
              Create Event
            </button>
          </div>

          {/* Search and Filters */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            {/* Search Bar */}
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value)
                  setPage(1)
                }}
                placeholder="Search events by name or description..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
              />
            </div>

            {/* Filter Toggle */}
            <div className="flex items-center justify-between">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-teal-600 transition-colors"
              >
                <Filter className="w-4 h-4" />
                Filters
                {hasActiveFilters && (
                  <span className="bg-teal-600 text-white text-xs px-2 py-0.5 rounded-full">
                    Active
                  </span>
                )}
              </button>
              {hasActiveFilters && (
                <button
                  onClick={handleClearFilters}
                  className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900"
                >
                  <X className="w-4 h-4" />
                  Clear filters
                </button>
              )}
            </div>

            {/* Filter Panel */}
            {showFilters && (
              <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Event Type Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Event Type
                  </label>
                  <select
                    value={selectedEventTypeId || ''}
                    onChange={(e) => {
                      setSelectedEventTypeId(e.target.value ? Number(e.target.value) : undefined)
                      setPage(1)
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  >
                    <option value="">All Types</option>
                    {eventTypes.map((type) => (
                      <option key={type.eventTypeId} value={type.eventTypeId}>
                        {type.typeName}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Status Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status
                  </label>
                  <select
                    value={selectedStatusId || ''}
                    onChange={(e) => {
                      setSelectedStatusId(e.target.value ? Number(e.target.value) : undefined)
                      setPage(1)
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  >
                    <option value="">All Statuses</option>
                    {eventStatuses.map((status) => (
                      <option key={status.eventStatusId} value={status.eventStatusId}>
                        {status.statusName}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Date From Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Start Date From
                  </label>
                  <input
                    type="date"
                    value={dateFrom}
                    onChange={(e) => {
                      setDateFrom(e.target.value)
                      setPage(1)
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  />
                </div>

                {/* Date To Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    End Date To
                  </label>
                  <input
                    type="date"
                    value={dateTo}
                    onChange={(e) => {
                      setDateTo(e.target.value)
                      setPage(1)
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        )}

        {/* Error State */}
        {error && !isLoading && (
          <ErrorMessage
            title="Failed to load events"
            message={error}
            onRetry={loadEvents}
          />
        )}

        {/* Events List */}
        {!isLoading && !error && (
          <>
            {/* Results Count */}
            <div className="mb-4 text-sm text-gray-600">
              Showing {events.length} of {total} event{total !== 1 ? 's' : ''}
            </div>

            {/* Events Grid */}
            {events.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <p className="text-gray-500 text-lg mb-2">No events found</p>
                <p className="text-gray-400 mb-4">
                  {hasActiveFilters
                    ? 'Try adjusting your filters'
                    : 'Create your first event to get started'}
                </p>
                {!hasActiveFilters && (
                  <button
                    onClick={() => setShowCreateModal(true)}
                    className="btn-primary inline-flex items-center gap-2"
                  >
                    <Plus className="w-5 h-5" />
                    Create Event
                  </button>
                )}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {events.map((event) => (
                  <EventCard
                    key={event.eventId}
                    event={event}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                    onView={setViewingEvent}
                  />
                ))}
              </div>
            )}

            {/* Pagination */}
            {total > pageSize && (
              <div className="mt-6 flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  Page {page} of {Math.ceil(total / pageSize)}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setPage(page - 1)}
                    disabled={page === 1}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  <button
                    onClick={() => setPage(page + 1)}
                    disabled={page >= Math.ceil(total / pageSize)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Modals */}
      {showCreateModal && (
        <CreateEventModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleCreateSuccess}
        />
      )}

      {editingEvent && (
        <EditEventModal
          isOpen={!!editingEvent}
          event={editingEvent}
          onClose={() => setEditingEvent(null)}
          onSuccess={handleEditSuccess}
        />
      )}

      {deletingEvent && (
        <DeleteEventConfirmModal
          isOpen={!!deletingEvent}
          event={deletingEvent}
          onClose={() => setDeletingEvent(null)}
          onConfirm={handleDeleteSuccess}
          mode={deletingEvent.companyId !== user?.company_id ? 'leave' : 'delete'}
          companyId={user?.company_id}
        />
      )}

      {viewingEvent && (
        <EventDetailView
          event={viewingEvent}
          onClose={() => setViewingEvent(null)}
          onEdit={(event) => {
            setViewingEvent(null)
            setEditingEvent(event)
          }}
          onDelete={(event) => {
            setViewingEvent(null)
            setDeletingEvent(event)
          }}
          onAddForm={handleCreateForm}
          onEditForm={handleEditForm}
          onDeleteForm={handleDeleteForm}
        />
      )}

      {/* Form Modals */}
      {showCreateFormModal && formEventId && (
        <CreateFormModal
          isOpen={showCreateFormModal}
          eventId={formEventId}
          onClose={() => {
            setShowCreateFormModal(false)
            setFormEventId(null)
          }}
          onSuccess={handleFormCreated}
        />
      )}

      {selectedForm && (
        <EditFormModal
          isOpen={showEditFormModal}
          form={selectedForm}
          onClose={() => {
            setShowEditFormModal(false)
            setSelectedForm(null)
          }}
          onSuccess={handleFormUpdated}
        />
      )}

      {selectedForm && (
        <DeleteFormConfirmModal
          isOpen={showDeleteFormModal}
          form={selectedForm}
          onClose={() => {
            setShowDeleteFormModal(false)
            setSelectedForm(null)
          }}
          onConfirm={handleFormDeleted}
        />
      )}
    </div>
  )
}
