/**
 * Edit Event Modal - Story 2.4 Task 9
 * Event edit form reusing CreateEventModal components
 */

import React, { useState, useEffect } from 'react'
import { X, Calendar, MapPin, Tag, Globe, Building2 } from 'lucide-react'
import { updateEvent, getEventTypes, getEventStatuses } from '../api/eventsApi'
import { Event, EventUpdateRequest, EventType, EventStatus } from '../types/events.types'
import { getIndustries, IndustryOption } from '../../profile/api/usersApi'
import { useCountries } from '../../validation/hooks/useCountries'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'
import { EnhancedFormInput } from '../../ux/components/EnhancedFormInput'
import { EventVisibilitySelector } from './EventVisibilitySelector'
import { ReviewStatusBadge } from './ReviewStatusBadge'
import { ReviewFeedbackPanel } from './ReviewFeedbackPanel'
import { offlineQueue } from '../../../utils/offlineQueue'

interface EditEventModalProps {
  isOpen: boolean
  event: Event | null
  onClose: () => void
  onSuccess: () => void
}

export function EditEventModal({ isOpen, event, onClose, onSuccess }: EditEventModalProps) {
  // Form state
  const [formData, setFormData] = useState<EventUpdateRequest>({})

  // Reference data
  const [eventTypes, setEventTypes] = useState<EventType[]>([])
  const [eventStatuses, setEventStatuses] = useState<EventStatus[]>([])
  const [industries, setIndustries] = useState<IndustryOption[]>([])
  const [isLoadingRefData, setIsLoadingRefData] = useState(true)

  // Form state
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [activeSection, setActiveSection] = useState<'basic' | 'location' | 'details'>('basic')
  
  // User permissions for this event (from event object)
  const userRole = event?.userRole ? {
    role_code: event.userRole.role_code || 'event_participant',
    role_name: event.userRole.role_name || 'Participant',
    has_edit_event: event.userRole.has_edit_event,
    has_delete_event: event.userRole.has_delete_event,
    has_manage_participants: event.userRole.has_manage_participants,
    has_view_event: event.userRole.has_view_event
  } : null

  const toast = useToastNotifications()
  const { countries } = useCountries()

  // Load reference data and populate form
  useEffect(() => {
    if (!isOpen || !event) return

    let isMounted = true

    const loadReferenceData = async () => {
      setIsLoadingRefData(true)
      
      // Check if offline - reference data requires network connection
      if (!navigator.onLine) {
        if (isMounted) {
          setIsLoadingRefData(false)
          // Don't show error - offline editing is allowed with limitations
          // Reference data will be unavailable, but text fields can still be edited
        }
        return
      }
      
      try {
        const [types, statuses, industryOptions] = await Promise.all([
          getEventTypes(),
          getEventStatuses(),
          getIndustries()
        ])
        
        // Only update state if component is still mounted
        if (!isMounted) return
        
        setEventTypes(types)
        setEventStatuses(statuses)
        setIndustries(industryOptions)
      } catch (error) {
        if (!isMounted) return
        // Don't show error when offline - offline editing is allowed with limitations
        if (navigator.onLine) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to load reference data'
          toast.error(errorMessage, 'Load error')
        }
      } finally {
        if (isMounted) {
          setIsLoadingRefData(false)
        }
      }
    }

    loadReferenceData()
    
    // Listen for online event to retry loading reference data
    const handleOnline = () => {
      if (isMounted && isOpen && event && (eventTypes.length === 0 || eventStatuses.length === 0)) {
        console.log('🌐 Connection restored - retrying reference data load')
        loadReferenceData()
      }
    }
    
    window.addEventListener('online', handleOnline)
    
    return () => {
      isMounted = false
      window.removeEventListener('online', handleOnline)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, event?.eventId]) // Only depend on eventId, not the whole event object

  // Reset form on close
  useEffect(() => {
    if (!isOpen) {
      setFormData({})
      setErrors({})
      setActiveSection('basic')
    }
  }, [isOpen])

  // Populate form with existing event data when modal opens (always, even when offline)
  // This ensures form is populated immediately, regardless of reference data loading
  useEffect(() => {
    if (!isOpen || !event) return

    setFormData({
      name: event.name,
      description: event.description,
      shortDescription: event.shortDescription,
      startDatetime: event.startDateTime ? new Date(event.startDateTime).toISOString().slice(0, 16) : '',
      endDatetime: event.endDateTime ? new Date(event.endDateTime).toISOString().slice(0, 16) : null,
      timezoneIdentifier: event.timezoneIdentifier || Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC',
      venueName: event.venueName,
      venueAddress: event.venueAddress,
      city: event.city,
      state: event.state,
      countryId: event.countryId,
      latitude: event.latitude,
      longitude: event.longitude,
      eventTypeId: event.eventTypeId,
      industryId: event.industryId,
      tags: event.tags,
      isPublic: event.isPublic,
      eventStatusId: event.eventStatusId,
      isRecurring: event.isRecurring,
      organizerCompanyId: event.organizerCompanyId,
      organizerContactEmail: event.organizerContactEmail,
      organizerWebsite: event.organizerWebsite,
      expectedAttendees: event.expectedAttendees
    })
  }, [isOpen, event?.eventId]) // Only depend on eventId to avoid unnecessary re-renders

  // Helper function to normalize URL (add https:// if missing protocol)
  const normalizeUrl = (url: string | null | undefined): string | null => {
    if (!url || !url.trim()) return null
    const trimmed = url.trim()
    // If URL doesn't start with http:// or https://, add https://
    if (trimmed && !trimmed.match(/^https?:\/\//i)) {
      return `https://${trimmed}`
    }
    return trimmed
  }

  // Validation
  const validate = (): boolean => {
    if (!event) {
      return false
    }

    const newErrors: Record<string, string> = {}

    const currentName = formData.name !== undefined ? formData.name : event.name
    if (!currentName || !currentName.trim()) {
      newErrors.name = 'Event name is required'
    } else if (currentName.length > 200) {
      newErrors.name = 'Event name must be 200 characters or less'
    }

    const originalStart = event.startDateTime ? new Date(event.startDateTime).toISOString().slice(0, 16) : ''
    const currentStart = formData.startDatetime !== undefined ? (formData.startDatetime ?? '') : originalStart
    if (!currentStart) {
      newErrors.startDatetime = 'Start date/time is required'
    } else {
      const startDate = new Date(currentStart)
      if (isNaN(startDate.getTime())) {
        newErrors.startDatetime = 'Invalid start date/time'
      }
    }

    const currentEnd = formData.endDatetime !== undefined
      ? formData.endDatetime
      : event.endDateTime
        ? new Date(event.endDateTime).toISOString().slice(0, 16)
        : null
    if (currentEnd && currentStart) {
      const startDate = new Date(currentStart)
      const endDate = new Date(currentEnd)
      if (endDate <= startDate) {
        newErrors.endDatetime = 'End date/time must be after start date/time'
      }
    }

    if (formData.latitude !== undefined && formData.latitude !== null && (formData.latitude < -90 || formData.latitude > 90)) {
      newErrors.latitude = 'Latitude must be between -90 and 90'
    }

    if (formData.longitude !== undefined && formData.longitude !== null && (formData.longitude < -180 || formData.longitude > 180)) {
      newErrors.longitude = 'Longitude must be between -180 and 180'
    }

    if (formData.organizerContactEmail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.organizerContactEmail)) {
      newErrors.organizerContactEmail = 'Invalid email address'
    }

    // URL validation - check if it's a valid URL format (with or without protocol)
    if (formData.organizerWebsite && formData.organizerWebsite.trim()) {
      const normalizedUrl = normalizeUrl(formData.organizerWebsite)
      if (normalizedUrl) {
        try {
          // Try to create a URL object with the normalized URL
          new URL(normalizedUrl)
        } catch {
          newErrors.organizerWebsite = 'Please enter a valid URL'
        }
      }
    }

    const currentEventTypeId = formData.eventTypeId !== undefined ? formData.eventTypeId : event.eventTypeId
    if (!currentEventTypeId) {
      newErrors.eventTypeId = 'Event type is required'
    }

    const effectiveIsPublic = formData.isPublic !== undefined ? formData.isPublic : event.isPublic ?? false
    const effectiveIsShared = formData.isSharedWithPlatform !== undefined ? formData.isSharedWithPlatform : event.isSharedWithPlatform ?? false

    const currentCity = formData.city !== undefined ? formData.city : event.city ?? ''
    const currentCountryId = formData.countryId !== undefined ? formData.countryId : event.countryId ?? null
    const currentShortDescription = formData.shortDescription !== undefined ? formData.shortDescription : event.shortDescription ?? null
    const currentDescription = formData.description !== undefined ? formData.description : event.description ?? null

    if (effectiveIsPublic) {
      if (!currentCity || !currentCity.trim()) {
        newErrors.city = 'City is required for public events'
      }

      if (!currentCountryId) {
        newErrors.countryId = 'Country is required for public events'
      }

      const shortDescLength = currentShortDescription ? currentShortDescription.trim().length : 0
      if (shortDescLength < 50 || shortDescLength > 500) {
        newErrors.shortDescription = 'Short description must be 50-500 characters'
      }
    }

    if (effectiveIsShared) {
      const descriptionLength = currentDescription ? currentDescription.trim().length : 0
      if (descriptionLength === 0) {
        newErrors.description = 'Full description is required for platform-sharing events'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Handle submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!event) return

    // Check permissions
    if (!userRole || !userRole.has_edit_event) {
      toast.error('You do not have permission to edit this event', 'Permission denied')
      return
    }

    if (!validate()) {
      toast.error('Please fix the form errors', 'Validation failed')
      return
    }

    // Normalize URL before submitting (add https:// if missing)
    const submitData = { ...formData }
    if (submitData.organizerWebsite) {
      submitData.organizerWebsite = normalizeUrl(submitData.organizerWebsite)
    }

    // Check if offline - queue the update instead
    if (!navigator.onLine) {
      setIsSubmitting(true)
      try {
        await offlineQueue.enqueue('event_update', {
          eventId: event.eventId,
          eventData: submitData
        })
        toast.success(
          'Edit queued',
          'Your changes will be saved when connection is restored'
        )
        onClose() // Close modal since edit is queued
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to queue edit'
        toast.error(errorMessage, 'Queue failed')
        setIsSubmitting(false)
      }
      return
    }

    setIsSubmitting(true)
    try {
      await updateEvent(event.eventId, submitData)
      toast.success('Event updated successfully', 'Success')
      onSuccess()
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update event'
      toast.error(errorMessage, 'Update failed')
    } finally {
      setIsSubmitting(false)
    }
  }
  
  const canEditEvent = !!(userRole && userRole.has_edit_event)

  // Helper to check if field requires reference data (unavailable offline)
  const requiresReferenceData = (fieldName: string): boolean => {
    const referenceDataFields = ['eventTypeId', 'eventStatusId', 'industryId', 'countryId', 'organizerCompanyId']
    return referenceDataFields.includes(fieldName)
  }

  // Helper to check if field should be disabled
  const isFieldDisabled = (fieldName?: string): boolean => {
    if (!canEditEvent) return true
    
    // If offline and field requires reference data, disable it
    if (fieldName && !navigator.onLine && requiresReferenceData(fieldName)) {
      return true
    }
    
    return false
  }

  // Handle field changes
  const handleChange = (field: keyof EventUpdateRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[field]
        return newErrors
      })
    }
  }

  if (!isOpen || !event) return null

  const originalStart = event.startDateTime ? new Date(event.startDateTime).toISOString().slice(0, 16) : ''
  const currentStart = formData.startDatetime !== undefined ? (formData.startDatetime ?? '') : originalStart
  const currentName = formData.name !== undefined ? formData.name : event.name
  const currentEventTypeId = formData.eventTypeId !== undefined ? formData.eventTypeId : event.eventTypeId
  const currentShortDescription = formData.shortDescription !== undefined ? formData.shortDescription : event.shortDescription ?? null
  const currentCity = formData.city !== undefined ? formData.city : event.city ?? ''
  const currentCountryId = formData.countryId !== undefined ? formData.countryId : event.countryId ?? null
  const currentDescription = formData.description !== undefined ? formData.description : event.description ?? null
  const effectiveIsPublic = formData.isPublic !== undefined ? formData.isPublic : event.isPublic ?? false
  const effectiveIsShared = formData.isSharedWithPlatform !== undefined ? formData.isSharedWithPlatform : event.isSharedWithPlatform ?? false

  const isPublicRequired = canEditEvent && effectiveIsPublic
  const isPlatformSharedRequired = canEditEvent && effectiveIsShared

  const incompleteRequiredFields: string[] = []
  if (canEditEvent) {
    if (!currentName || !currentName.trim()) {
      incompleteRequiredFields.push('Event Name')
    }
    if (!currentStart) {
      incompleteRequiredFields.push('Start Date/Time')
    }
    if (!currentEventTypeId) {
      incompleteRequiredFields.push('Event Type')
    }
    if (isPublicRequired) {
      if (!currentCity || !currentCity.trim()) {
        incompleteRequiredFields.push('City')
      }
      if (!currentCountryId) {
        incompleteRequiredFields.push('Country')
      }
      const shortDescLength = currentShortDescription ? currentShortDescription.trim().length : 0
      if (shortDescLength < 50 || shortDescLength > 500) {
        incompleteRequiredFields.push('Short Description (50-500 characters)')
      }
    }
    if (isPlatformSharedRequired) {
      const descriptionLength = currentDescription ? currentDescription.trim().length : 0
      if (descriptionLength === 0) {
        incompleteRequiredFields.push('Full Description (required for platform sharing)')
      }
    }
  }

  const isUpdateDisabled = isSubmitting || isLoadingRefData || !canEditEvent || incompleteRequiredFields.length > 0
  const shouldShowTooltip = canEditEvent && incompleteRequiredFields.length > 0
  const submitAriaDescribedBy = shouldShowTooltip ? 'edit-event-tooltip' : undefined

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        {/* Modal */}
        <div
          className="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden transform transition-all"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Edit Event</h2>
                <p className="text-teal-100 text-sm mt-1">{event.name}</p>
              </div>
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 p-1 rounded transition-colors"
                aria-label="Close"
                disabled={isSubmitting}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="overflow-y-auto max-h-[calc(90vh-180px)]">
            {/* Section Tabs */}
            <div className="border-b border-gray-200 bg-gray-50 px-6 py-2 flex gap-4">
              <button
                type="button"
                onClick={() => setActiveSection('basic')}
                className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                  activeSection === 'basic'
                    ? 'bg-teal-600 text-white'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Basic Info
              </button>
              <button
                type="button"
                onClick={() => setActiveSection('location')}
                className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                  activeSection === 'location'
                    ? 'bg-teal-600 text-white'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Location
              </button>
              <button
                type="button"
                onClick={() => setActiveSection('details')}
                className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                  activeSection === 'details'
                    ? 'bg-teal-600 text-white'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Additional Details
              </button>
            </div>

            <div className="p-6 space-y-6">
              {isLoadingRefData ? (
                <div className="flex justify-center py-8">
                  <LoadingSpinner size="medium" />
                </div>
              ) : (
                <>
                      {/* Basic Info Section */}
                  {activeSection === 'basic' && (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                          <Calendar className="w-5 h-5 text-teal-600" />
                          Basic Information
                        </h3>
                        {userRole && (
                          <div className="text-sm text-gray-600">
                            <span className="font-medium">Your role:</span> {userRole.role_name}
                            {!userRole.has_edit_event && (
                              <span className="ml-2 text-orange-600 font-medium">(View Only)</span>
                            )}
                          </div>
                        )}
                      </div>

                      {/* Offline Editing Banner */}
                      {!navigator.onLine && canEditEvent && (
                        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-md" role="alert">
                          <div className="flex items-start">
                            <div className="flex-shrink-0">
                              <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                              </svg>
                            </div>
                            <div className="ml-3 flex-1">
                              <h4 className="text-sm font-medium text-yellow-800">Editing Offline</h4>
                              <div className="mt-2 text-sm text-yellow-700">
                                <p className="mb-1">You're currently offline. You can edit text fields, dates, and other basic information.</p>
                                <p className="mb-1"><strong>Fields unavailable offline:</strong> Event Type, Status, Industry, Country, Organizer Company (require reference data)</p>
                                <p>Your changes will be saved locally and uploaded automatically when your connection is restored.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Event Name */}
                      <div>
                        <EnhancedFormInput
                          type="text"
                          label="Event Name"
                          name="name"
                          value={formData.name ?? ''}
                          onChange={(value) => handleChange('name', value)}
                          placeholder="Enter event name"
                          required
                          error={errors.name}
                          maxLength={200}
                          disabled={isFieldDisabled()}
                        />
                      </div>

                      {/* Short Description */}
                      <div>
                        <EnhancedFormInput
                          type="textarea"
                          label="Short Description"
                          name="shortDescription"
                          value={formData.shortDescription ?? ''}
                          onChange={(value) => handleChange('shortDescription', value || null)}
                          placeholder="Brief summary for list views (max 500 characters)"
                          maxLength={500}
                          showCharacterCount
                          required={isPublicRequired}
                          error={errors.shortDescription}
                          disabled={isFieldDisabled()}
                        />
                      </div>

                      {/* Description */}
                      <div>
                        <EnhancedFormInput
                          type="textarea"
                          label="Full Description"
                          name="description"
                          value={formData.description ?? ''}
                          onChange={(value) => handleChange('description', value || null)}
                          placeholder="Detailed event description"
                          required={isPlatformSharedRequired}
                          error={errors.description}
                          disabled={isFieldDisabled()}
                        />
                      </div>

                      {/* Start DateTime */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Start Date & Time
                          {canEditEvent && (
                            <span className="text-red-500 ml-1">*</span>
                          )}
                        </label>
                        <input
                          type="datetime-local"
                          value={formData.startDatetime ?? originalStart}
                          onChange={(e) => handleChange('startDatetime', e.target.value)}
                          disabled={isFieldDisabled()}
                          required={canEditEvent}
                          className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                            errors.startDatetime ? 'border-red-500' : 'border-gray-300'
                          } ${isFieldDisabled() ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''}`}
                        />
                        {errors.startDatetime && (
                          <p className="mt-1 text-sm text-red-600">{errors.startDatetime}</p>
                        )}
                      </div>

                      {/* End DateTime */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          End Date & Time
                        </label>
                        <input
                          type="datetime-local"
                          value={formData.endDatetime ?? ''}
                          onChange={(e) => handleChange('endDatetime', e.target.value || null)}
                          disabled={isFieldDisabled()}
                          className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                            errors.endDatetime ? 'border-red-500' : 'border-gray-300'
                          } ${isFieldDisabled() ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''}`}
                        />
                        {errors.endDatetime && (
                          <p className="mt-1 text-sm text-red-600">{errors.endDatetime}</p>
                        )}
                      </div>

                      {/* Timezone */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Timezone
                        </label>
                        <input
                          type="text"
                          value={formData.timezoneIdentifier ?? ''}
                          onChange={(e) => handleChange('timezoneIdentifier', e.target.value)}
                          placeholder="e.g., America/New_York, Europe/London"
                          disabled={isFieldDisabled()}
                          className={`w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                            isFieldDisabled() ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''
                          }`}
                        />
                        <p className="mt-1 text-xs text-gray-500">
                          IANA timezone identifier (e.g., America/New_York)
                        </p>
                      </div>

                      {/* Event Type */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Event Type
                          {canEditEvent && (
                            <span className="text-red-500 ml-1">*</span>
                          )}
                          {!navigator.onLine && canEditEvent && (
                            <span className="ml-2 text-xs text-yellow-600 font-normal">(Unavailable offline)</span>
                          )}
                        </label>
                        {!navigator.onLine && eventTypes.length === 0 ? (
                          <div className="w-full px-3 py-2 border border-yellow-400 bg-yellow-50 rounded-md">
                            <p className="text-sm text-yellow-800">
                              <strong>Offline:</strong> Event type selection requires internet connection. Current value: <strong>{event.eventType?.typeName || 'Unknown'}</strong>
                            </p>
                          </div>
                        ) : (
                          <select
                            value={formData.eventTypeId ?? event.eventTypeId}
                            onChange={(e) => handleChange('eventTypeId', Number(e.target.value))}
                            disabled={isFieldDisabled('eventTypeId')}
                            required={canEditEvent}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.eventTypeId ? 'border-red-500' : 'border-gray-300'
                            } ${isFieldDisabled('eventTypeId') ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''}`}
                          >
                            {eventTypes.length > 0 ? (
                              eventTypes.map((type) => (
                                <option key={type.eventTypeId} value={type.eventTypeId}>
                                  {type.typeName}
                                </option>
                              ))
                            ) : (
                              <option value={event.eventTypeId}>{event.eventType?.typeName || 'Loading...'}</option>
                            )}
                          </select>
                        )}
                        {errors.eventTypeId && (
                          <p className="mt-1 text-sm text-red-600">{errors.eventTypeId}</p>
                        )}
                      </div>

                      {/* Event Status */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Status
                          {!navigator.onLine && canEditEvent && (
                            <span className="ml-2 text-xs text-yellow-600 font-normal">(Unavailable offline)</span>
                          )}
                        </label>
                        {!navigator.onLine && eventStatuses.length === 0 ? (
                          <div className="w-full px-3 py-2 border border-yellow-400 bg-yellow-50 rounded-md">
                            <p className="text-sm text-yellow-800">
                              <strong>Offline:</strong> Status selection requires internet connection. Current value: <strong>{event.eventStatus?.statusName || 'Unknown'}</strong>
                            </p>
                          </div>
                        ) : (
                          <select
                            value={formData.eventStatusId ?? event.eventStatusId}
                            onChange={(e) => handleChange('eventStatusId', Number(e.target.value))}
                            disabled={isFieldDisabled('eventStatusId')}
                            className={`w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              isFieldDisabled('eventStatusId') ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''
                            }`}
                          >
                            {eventStatuses.length > 0 ? (
                              eventStatuses.map((status) => (
                                <option key={status.eventStatusId} value={status.eventStatusId}>
                                  {status.statusColor ? '● ' : ''}{status.statusName}{status.statusDescription ? ` - ${status.statusDescription}` : ''}
                                </option>
                              ))
                            ) : (
                              <option value={event.eventStatusId}>
                                {event.eventStatus?.statusName || 'Loading...'}
                              </option>
                            )}
                          </select>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Location Section */}
                  {activeSection === 'location' && (
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                        <MapPin className="w-5 h-5 text-teal-600" />
                        Location Information
                      </h3>

                      {/* Venue Name */}
                      <div>
                        <EnhancedFormInput
                          type="text"
                          label="Venue Name"
                          name="venueName"
                          value={formData.venueName ?? ''}
                          onChange={(value) => handleChange('venueName', value || null)}
                          placeholder="Enter venue name"
                          maxLength={200}
                          disabled={isFieldDisabled()}
                        />
                      </div>

                      {/* Venue Address */}
                      <div>
                        <EnhancedFormInput
                          type="textarea"
                          label="Venue Address"
                          name="venueAddress"
                          value={formData.venueAddress ?? ''}
                          onChange={(value) => handleChange('venueAddress', value || null)}
                          placeholder="Full venue address"
                          maxLength={500}
                          disabled={isFieldDisabled()}
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        {/* City */}
                        <div>
                          <EnhancedFormInput
                            type="text"
                            label="City"
                            name="city"
                            value={formData.city ?? ''}
                          onChange={(value) => handleChange('city', value || null)}
                            placeholder="City"
                            maxLength={100}
                          required={isPublicRequired}
                            error={errors.city}
                            disabled={isFieldDisabled()}
                          />
                        </div>

                        {/* State */}
                        <div>
                          <EnhancedFormInput
                            type="text"
                            label="State/Province"
                            name="state"
                            value={formData.state ?? ''}
                            onChange={(value) => handleChange('state', value || null)}
                            placeholder="State or Province"
                            maxLength={100}
                            disabled={isFieldDisabled()}
                          />
                        </div>
                      </div>

                      {/* Country */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Country
                          {isPublicRequired && (
                            <span className="text-red-500 ml-1">*</span>
                          )}
                          {!navigator.onLine && canEditEvent && (
                            <span className="ml-2 text-xs text-yellow-600 font-normal">(Unavailable offline)</span>
                          )}
                        </label>
                        {!navigator.onLine ? (
                          <div className="w-full px-3 py-2 border border-yellow-400 bg-yellow-50 rounded-md">
                            <p className="text-sm text-yellow-800">
                              <strong>Offline:</strong> Country selection requires internet connection. Current value: <strong>{event.countryId ? (countries.find(c => c.id === event.countryId)?.name || `Country ID: ${event.countryId}`) : 'Not set'}</strong>
                            </p>
                          </div>
                        ) : (
                          <select
                            value={formData.countryId ?? event.countryId ?? ''}
                            onChange={(e) => handleChange('countryId', e.target.value ? Number(e.target.value) : null)}
                            disabled={isFieldDisabled('countryId')}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.countryId ? 'border-red-500' : 'border-gray-300'
                            } ${isFieldDisabled('countryId') ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''}`}
                            required={isPublicRequired}
                          >
                            <option value="">Select country...</option>
                            {countries.length > 0 ? (
                              countries.map((country) => (
                                <option key={country.id} value={country.id}>
                                  {country.name}
                                </option>
                              ))
                            ) : (
                              event.countryId && (
                                <option value={event.countryId}>Country ID: {event.countryId}</option>
                              )
                            )}
                          </select>
                        )}
                        {errors.countryId && (
                          <p className="mt-1 text-sm text-red-600">{errors.countryId}</p>
                        )}
                      </div>

                      {/* Coordinates */}
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Latitude
                          </label>
                          <input
                            type="number"
                            step="any"
                            min="-90"
                            max="90"
                            value={formData.latitude ?? ''}
                            onChange={(e) => handleChange('latitude', e.target.value ? parseFloat(e.target.value) : null)}
                            disabled={isFieldDisabled()}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.latitude ? 'border-red-500' : 'border-gray-300'
                            } ${isFieldDisabled() ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''}`}
                            placeholder="-90 to 90"
                          />
                          {errors.latitude && (
                            <p className="mt-1 text-sm text-red-600">{errors.latitude}</p>
                          )}
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Longitude
                          </label>
                          <input
                            type="number"
                            step="any"
                            min="-180"
                            max="180"
                            value={formData.longitude ?? ''}
                            onChange={(e) => handleChange('longitude', e.target.value ? parseFloat(e.target.value) : null)}
                            disabled={isFieldDisabled()}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.longitude ? 'border-red-500' : 'border-gray-300'
                            } ${isFieldDisabled() ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''}`}
                            placeholder="-180 to 180"
                          />
                          {errors.longitude && (
                            <p className="mt-1 text-sm text-red-600">{errors.longitude}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Additional Details Section */}
                  {activeSection === 'details' && (
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                        <Building2 className="w-5 h-5 text-teal-600" />
                        Additional Details
                      </h3>

                      {/* Industry */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Industry
                          {!navigator.onLine && canEditEvent && (
                            <span className="ml-2 text-xs text-yellow-600 font-normal">(Unavailable offline)</span>
                          )}
                        </label>
                        {!navigator.onLine && industries.length === 0 ? (
                          <div className="w-full px-3 py-2 border border-yellow-400 bg-yellow-50 rounded-md">
                            <p className="text-sm text-yellow-800">
                              <strong>Offline:</strong> Industry selection requires internet connection. Current value: <strong>{event.industry?.name || event.industryId ? `Industry ID: ${event.industryId}` : 'Not set'}</strong>
                            </p>
                          </div>
                        ) : (
                          <select
                            value={formData.industryId ?? event.industryId ?? ''}
                            onChange={(e) => handleChange('industryId', e.target.value ? Number(e.target.value) : null)}
                            disabled={isFieldDisabled('industryId')}
                            className={`w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              isFieldDisabled('industryId') ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''
                            }`}
                          >
                            <option value="">Select industry...</option>
                            {industries.length > 0 ? (
                              industries.map((industry) => (
                                <option key={industry.id} value={industry.id}>
                                  {industry.name}
                                </option>
                              ))
                            ) : (
                              event.industryId && (
                                <option value={event.industryId}>
                                  {event.industry?.name || `Industry ID: ${event.industryId}`}
                                </option>
                              )
                            )}
                          </select>
                        )}
                      </div>

                      {/* Tags */}
                      <div>
                        <EnhancedFormInput
                          type="text"
                          label="Tags"
                          name="tags"
                          value={formData.tags ?? ''}
                          onChange={(value) => handleChange('tags', value || null)}
                          placeholder="Comma-separated tags"
                          disabled={isFieldDisabled()}
                        />
                      </div>

                      {/* Expected Attendees */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Expected Attendees
                        </label>
                        <input
                          type="number"
                          min="0"
                          value={formData.expectedAttendees ?? ''}
                          onChange={(e) => handleChange('expectedAttendees', e.target.value ? parseInt(e.target.value) : null)}
                          disabled={isFieldDisabled()}
                          className={`w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                            isFieldDisabled() ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''
                          }`}
                          placeholder="Expected number of attendees"
                        />
                      </div>

                      {/* Organizer Contact Email */}
                      <div>
                        <EnhancedFormInput
                          type="email"
                          label="Organizer Contact Email"
                          name="organizerContactEmail"
                          value={formData.organizerContactEmail ?? ''}
                          onChange={(value) => handleChange('organizerContactEmail', value || null)}
                          placeholder="contact@example.com"
                          error={errors.organizerContactEmail}
                          disabled={isFieldDisabled()}
                        />
                      </div>

                      {/* Organizer Website */}
                      <div>
                        <EnhancedFormInput
                          type="text"
                          label="Organizer Website"
                          name="organizerWebsite"
                          value={formData.organizerWebsite ?? ''}
                          onChange={(value) => handleChange('organizerWebsite', value || null)}
                          placeholder="www.example.com or https://www.example.com"
                          disabled={isFieldDisabled()}
                          error={errors.organizerWebsite}
                        />
                      </div>

                      {/* Event Visibility Selector */}
                      {canEditEvent && (
                        <div className="space-y-4">
                          <EventVisibilitySelector
                            isPublic={formData.isPublic ?? event.isPublic ?? false}
                            isSharedWithPlatform={formData.isSharedWithPlatform ?? event.isSharedWithPlatform ?? false}
                            onPublicChange={(isPublic) => handleChange('isPublic', isPublic)}
                            onPlatformSharingChange={(isShared) => handleChange('isSharedWithPlatform', isShared)}
                            disabled={isFieldDisabled()}
                          />
                        </div>
                      )}

                      {/* Review Status Badge - Show if event is shared with platform */}
                      {(event.isSharedWithPlatform || formData.isSharedWithPlatform) && event.publicReviewStatus && (
                        <div className="mt-4">
                          <ReviewStatusBadge
                            status={event.publicReviewStatus.statusCode as 'PENDING' | 'APPROVED' | 'REJECTED'}
                            statusName={event.publicReviewStatus.statusName || undefined}
                          />
                        </div>
                      )}

                      {/* Review Feedback Panel - Show if rejected */}
                      {event.publicReviewStatus?.statusCode === 'REJECTED' && event.publicReviewComments && (
                        <div className="mt-4">
                          <ReviewFeedbackPanel
                            reviewComments={event.publicReviewComments}
                            reviewDate={event.publicReviewDate || undefined}
                            onResubmit={() => {
                              // Enable platform sharing again to resubmit
                              handleChange('isSharedWithPlatform', true)
                            }}
                          />
                        </div>
                      )}

                      {/* Recurring Event Checkbox */}
                      <div className="mt-4">
                        <label className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            checked={formData.isRecurring ?? event.isRecurring}
                            onChange={(e) => handleChange('isRecurring', e.target.checked)}
                            disabled={isFieldDisabled()}
                            className={`w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500 ${
                              isFieldDisabled() ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                          />
                          <span className="text-sm text-gray-700">Recurring Event</span>
                        </label>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>

            {/* Footer */}
            <div className="border-t border-gray-200 bg-gray-50 px-6 py-4 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={onClose}
                disabled={isSubmitting}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Cancel
              </button>
              <div className="relative group">
                <button
                  type="submit"
                  disabled={isUpdateDisabled}
                  aria-disabled={isUpdateDisabled}
                  aria-describedby={submitAriaDescribedBy}
                  className="btn-primary flex items-center gap-2 px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-gray-400"
                  title={!canEditEvent ? `You do not have permission to edit this event. Your role: ${userRole?.role_name || 'Unknown'}` : undefined}
                >
                  {isSubmitting ? (
                    <>
                      <LoadingSpinner size="small" />
                      Updating...
                    </>
                  ) : (
                    'Update Event'
                  )}
                </button>
                {shouldShowTooltip && (
                  <div
                    id="edit-event-tooltip"
                    role="tooltip"
                    className="absolute bottom-full right-0 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md shadow-lg z-50 min-w-[250px] max-w-[400px] opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 pointer-events-none transition-opacity duration-200"
                  >
                    <div className="font-semibold mb-1">Please complete the following required fields:</div>
                    <ul className="list-disc list-inside space-y-1">
                      {incompleteRequiredFields.map((field, index) => (
                        <li key={index}>{field}</li>
                      ))}
                    </ul>
                    <div className="absolute bottom-0 right-4 transform translate-y-full border-4 border-transparent border-t-gray-900"></div>
                  </div>
                )}
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  )
}
