/**
 * Create Event Modal - Story 2.4 Task 8
 * Event creation form with all required and optional fields
 */

import React, { useState, useEffect, useMemo } from 'react'
import { X, Calendar, MapPin, Globe, Building2, Briefcase, Users } from 'lucide-react'
import { 
  createEvent, 
  getEventTypes, 
  getEventStatuses, 
  searchPublicEvents, 
  participateInEvent,
  getCountryFromTimezone,
  getUserProfileForInference,
  getRecentEventCities,
  getEventById
} from '../api/eventsApi'
import { EventCreateRequest, EventType, EventStatus, Event } from '../types/events.types'
import { getIndustries, IndustryOption } from '../../profile/api/usersApi'
import { useCountries } from '../../validation/hooks/useCountries'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'
import { EnhancedFormInput } from '../../ux/components/EnhancedFormInput'
import { getUserCompanies } from '../../dashboard/api/dashboardApi'
import { EventTypeSelector } from './EventTypeSelector'
import { EventSearchStep } from './EventSearchStep'
import { PlatformSearchabilityQuestion } from './PlatformSearchabilityQuestion'
import { EventVisibilitySelector } from './EventVisibilitySelector'
import { ReviewProcessInfoBanner } from './ReviewProcessInfoBanner'
import { ReviewStatusBadge } from './ReviewStatusBadge'
import { useAuth } from '../../auth'
import { formAutoSave } from '../../../utils/formAutoSave'
import { offlineQueue } from '../../../utils/offlineQueue'

const createInitialFormData = (): EventCreateRequest => ({
    name: '',
    description: null,
    shortDescription: null,
    startDatetime: '',
    endDatetime: null,
    timezoneIdentifier: Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC',
    venueName: null,
    venueAddress: null,
    city: null,
    state: null,
    countryId: null,
    latitude: null,
    longitude: null,
    eventTypeId: 0,
    industryId: null,
    tags: null,
  isPublic: undefined,
  isSharedWithPlatform: false,
  eventStatusId: 1,
    isRecurring: false,
    organizerCompanyId: null,
    organizerContactEmail: null,
    organizerWebsite: null,
    expectedAttendees: null
  })

interface CreateEventModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export function CreateEventModal({ isOpen, onClose, onSuccess }: CreateEventModalProps) {
  const { user } = useAuth()
  const userId = user?.id || user?.user_id || 0

  // Form state
  const [formData, setFormData] = useState<EventCreateRequest>(() => createInitialFormData())
  const [hasRestoredDraft, setHasRestoredDraft] = useState(false)

  // Reference data
  const [eventTypes, setEventTypes] = useState<EventType[]>([])
  const [eventStatuses, setEventStatuses] = useState<EventStatus[]>([])
  const [industries, setIndustries] = useState<IndustryOption[]>([])
  const [userCompanies, setUserCompanies] = useState<Array<{ companyId: number; companyName: string }>>([])
  const [isLoadingRefData, setIsLoadingRefData] = useState(true)

  // Multi-step progressive disclosure state
  type Step = 'type-selection' | 'search-skip' | 'platform-question' | 'form'
  const [currentStep, setCurrentStep] = useState<Step>('type-selection')
  const [selectedEventType, setSelectedEventType] = useState<'private' | 'public' | null>(null)
  const [skippedSearch, setSkippedSearch] = useState(false)
  const [selectedPlatformOption, setSelectedPlatformOption] = useState<'company-network' | 'platform' | null>(null)
  const [usedExistingEvent, setUsedExistingEvent] = useState(false)
  const [selectedExistingEvent, setSelectedExistingEvent] = useState<Event | null>(null)
  const [isLoadingExistingEvent, setIsLoadingExistingEvent] = useState(false)

  // Form state
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [activeTab, setActiveTab] = useState<'essentials' | 'enhanced' | 'advanced'>('essentials')
  const [hasSelectedVisibility, setHasSelectedVisibility] = useState(false) // Progressive disclosure: show tabs only after Private/Public selected

  // Public event search state
  const [publicEventSearchTerm, setPublicEventSearchTerm] = useState('')
  const [publicEventResults, setPublicEventResults] = useState<Event[]>([])
  const [isSearchingPublicEvents, setIsSearchingPublicEvents] = useState(false)

  // Get browser locale for date formatting
  const browserLocale = useMemo(() => {
    return navigator.language || navigator.languages?.[0] || 'en-AU'
  }, [])

  // Detect if locale uses 12-hour or 24-hour format
  const uses12HourFormat = useMemo(() => {
    const testDate = new Date('2023-01-01T14:00:00')
    const timeStr = testDate.toLocaleTimeString(browserLocale, { hour: 'numeric' })
    return !timeStr.includes('14') && (timeStr.includes('PM') || timeStr.includes('AM'))
  }, [browserLocale])

  const toast = useToastNotifications()
  const { countries, getCountryById } = useCountries()
  const isJoinExistingEvent = selectedExistingEvent !== null
  
  // Smart field inference state
  const [fieldInferenceSource, setFieldInferenceSource] = useState<Record<string, string>>({}) // Track where each field value came from

  // Load reference data and smart field inference
  useEffect(() => {
    if (!isOpen) return

    let isMounted = true

    const loadReferenceData = async () => {
      setIsLoadingRefData(true)
      
      // Check if offline - reference data requires network connection
      if (!navigator.onLine) {
        if (isMounted) {
          setIsLoadingRefData(false)
          toast.warning(
            'Reference data unavailable offline',
            'Event types, statuses, and other options require an internet connection. Please connect to the internet to create events.'
          )
        }
        return
      }
      
      try {
        const [types, statuses, industryOptions, userProfile, companiesData] = await Promise.all([
          getEventTypes(),
          getEventStatuses(),
          getIndustries(),
          getUserProfileForInference().catch(() => null), // Don't fail if inference fails
          getUserCompanies().catch(() => ({ companies: [] })) // Don't fail if companies fail
        ])
        
        // Only update state if component is still mounted
        if (!isMounted) return
        
        // Smart field inference: Pre-fill timezone and country from user profile
        if (userProfile) {
          const inferredFields: Partial<EventCreateRequest> = {}
          const sourceTracking: Record<string, string> = {}
          
          // Timezone from user profile
          if (userProfile.timezone_identifier) {
            inferredFields.timezoneIdentifier = userProfile.timezone_identifier
            sourceTracking.timezoneIdentifier = '🔍 From your profile'
          }
          
          // Country from user profile (or infer from timezone if country not set)
          if (userProfile.country_id) {
            inferredFields.countryId = userProfile.country_id
            sourceTracking.countryId = '🔍 From your profile'
          } else if (userProfile.timezone_identifier) {
            // Try to infer country from timezone
            const countryInfo = await getCountryFromTimezone(userProfile.timezone_identifier).catch(() => null)
            if (countryInfo) {
              inferredFields.countryId = countryInfo.country_id
              sourceTracking.countryId = '🔍 Auto-detected from timezone'
            }
          }
          
          // Update form data with inferred values
          if (Object.keys(inferredFields).length > 0) {
            setFormData(prev => ({ ...prev, ...inferredFields }))
            setFieldInferenceSource(prev => ({ ...prev, ...sourceTracking }))
          }
        }
        
        console.log('CreateEventModal - Loaded eventTypes:', types)
        console.log('CreateEventModal - Loaded eventStatuses:', statuses)
        setEventTypes(types)
        setEventStatuses(statuses)
        setIndustries(industryOptions)
        setUserCompanies(companiesData.companies.map(c => ({ companyId: c.companyId, companyName: c.companyName })))

        // Don't auto-select event type - let user choose
      } catch (error) {
        if (!isMounted) return
        const errorMessage = error instanceof Error ? error.message : 'Failed to load reference data'
        toast.error(errorMessage, 'Load error')
      } finally {
        if (isMounted) {
          setIsLoadingRefData(false)
        }
      }
    }

    loadReferenceData()
    
    // Listen for online event to retry loading reference data
    const handleOnline = () => {
      if (isMounted && isOpen && eventTypes.length === 0) {
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
  }, [isOpen])

  // Restore draft on open (only once per modal open)
  useEffect(() => {
    if (!isOpen || !userId || hasRestoredDraft) return

    const restoreDraft = async () => {
      try {
        const draft = await formAutoSave.restore('event_create', undefined, userId)
        if (draft) {
          setFormData(draft)
          setHasRestoredDraft(true)
          toast.info('Draft restored', 'Your previous work has been restored')
        }
      } catch (error) {
        console.error('Failed to restore draft:', error)
      }
    }

    restoreDraft()
  }, [isOpen, userId, hasRestoredDraft, toast])

  // Auto-save form draft every 30 seconds
  useEffect(() => {
    if (!isOpen || !userId || currentStep !== 'form' || isJoinExistingEvent) return

    let firstSaveShown = false

    const cleanup = formAutoSave.startAutoSave(
      'event_create',
      undefined,
      userId,
      () => formData,
      () => {
        // Show notification only on first save
        if (!firstSaveShown) {
          toast.success('Draft saved', 'Your work is being saved automatically')
          firstSaveShown = true
        }
      }
    )

    return cleanup
  }, [isOpen, userId, formData, currentStep, isJoinExistingEvent, toast])

  // Reset form on close
  useEffect(() => {
    if (!isOpen) {
      setFormData(createInitialFormData())
      setFieldInferenceSource({})
      setErrors({})
      setActiveTab('essentials')
      setHasSelectedVisibility(false)
      setHasRestoredDraft(false)
      // Reset step state
      setCurrentStep('type-selection')
      setSelectedEventType(null)
      setSkippedSearch(false)
      setSelectedPlatformOption(null)
      setUsedExistingEvent(false)
      setSelectedExistingEvent(null)
      setIsLoadingExistingEvent(false)
      setPublicEventSearchTerm('')
      setPublicEventResults([])
    }
  }, [isOpen])

  // Validation
  const validate = (): boolean => {
    if (isJoinExistingEvent) {
      return true
    }

    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Event name is required'
    } else if (formData.name.length > 200) {
      newErrors.name = 'Event name must be 200 characters or less'
    }

    if (!formData.startDatetime) {
      newErrors.startDatetime = 'Start date/time is required'
    } else {
      const startDate = new Date(formData.startDatetime)
      if (isNaN(startDate.getTime())) {
        newErrors.startDatetime = 'Invalid start date/time'
      }
    }

    if (formData.endDatetime) {
      const startDate = new Date(formData.startDatetime)
      const endDate = new Date(formData.endDatetime)
      if (endDate <= startDate) {
        newErrors.endDatetime = 'End date/time must be after start date/time'
      }
    }

    if (!formData.eventTypeId || formData.eventTypeId === 0) {
      newErrors.eventTypeId = 'Event type is required'
    }
    if (formData.isPublic === undefined) {
      newErrors.isPublic = 'Please select if this is a public or private event'
    }

    if (formData.latitude != null && (formData.latitude < -90 || formData.latitude > 90)) {
      newErrors.latitude = 'Latitude must be between -90 and 90'
    }

    if (formData.longitude != null && (formData.longitude < -180 || formData.longitude > 180)) {
      newErrors.longitude = 'Longitude must be between -180 and 180'
    }

    if (formData.organizerContactEmail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.organizerContactEmail)) {
      newErrors.organizerContactEmail = 'Invalid email address'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Handle submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (selectedExistingEvent) {
      setIsSubmitting(true)
      try {
        const participation = await participateInEvent(selectedExistingEvent.eventId)
        if (participation.alreadyExists) {
          toast.warning('You are already a participant for this event', 'Nothing to update')
        } else {
          toast.success('You have joined this event as a participant', 'Success')
        }
        onSuccess()
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to join event'
        toast.error(errorMessage, 'Join failed')
      } finally {
        setIsSubmitting(false)
      }
      return
    }

    if (!validate()) {
      toast.error('Please fix the form errors', 'Validation failed')
      return
    }

    // Check if offline - queue the request instead
    if (!navigator.onLine) {
      try {
        await offlineQueue.enqueue('event_create', formData)
        toast.success(
          'Event queued',
          'Your event will be created when connection is restored'
        )
        // Clear draft since it's queued
        await formAutoSave.clear('event_create', undefined, userId)
        onClose()
        return
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to queue event'
        toast.error(errorMessage, 'Queue failed')
        return
      }
    }

    setIsSubmitting(true)
    try {
      await createEvent(formData)
      // Clear draft on successful submission
      await formAutoSave.clear('event_create', undefined, userId)
      toast.success('Event created successfully', 'Success')
      onSuccess()
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to create event'
      toast.error(errorMessage, 'Create failed')
    } finally {
      setIsSubmitting(false)
    }
  }

  // Check required fields and return incomplete fields
  const getIncompleteRequiredFields = (): string[] => {
    if (isJoinExistingEvent) {
      return []
    }

    const incomplete: string[] = []

    if (!formData.name.trim()) {
      incomplete.push('Event Name')
    }

    if (!formData.startDatetime) {
      incomplete.push('Start Date/Time')
    }

    if (!formData.eventTypeId || formData.eventTypeId === 0) {
      if (!navigator.onLine && eventTypes.length === 0) {
        incomplete.push('Event Type (unavailable offline - connect to internet)')
      } else {
        incomplete.push('Event Type')
      }
    }

    if (formData.isPublic === undefined) {
      incomplete.push('Event Visibility (Private/Public)')
    }

    // For public events, additional required fields
    if (formData.isPublic === true) {
      if (!formData.city) {
        incomplete.push('City')
      }
      if (!formData.countryId) {
        incomplete.push('Country')
      }
      if (!formData.shortDescription || formData.shortDescription.length < 50) {
        incomplete.push('Short Description (50-500 characters)')
      }
      if (!formData.organizerCompanyId) {
        incomplete.push('Organizer Company')
      }
    }

    // For platform-sharing events, description is required (backend requirement)
    if (formData.isSharedWithPlatform === true) {
      if (!formData.description || formData.description.trim().length === 0) {
        incomplete.push('Full Description (required for platform sharing)')
      }
    }

    return incomplete
  }

  // Real-time validation on field change
  const validateField = (field: keyof EventCreateRequest, value: any): void => {
    const newErrors: Record<string, string> = { ...errors }

    // Clear existing error for this field
    delete newErrors[field]

    // Validate specific fields
    switch (field) {
      case 'name':
        if (!value.trim()) {
          newErrors.name = 'Event name is required'
        } else if (value.length > 200) {
          newErrors.name = 'Event name must be 200 characters or less'
        } else if (value.length < 3) {
          newErrors.name = 'Event name must be at least 3 characters'
        }
        break

      case 'startDatetime':
        if (!value) {
          newErrors.startDatetime = 'Start date/time is required'
        } else {
          const startDate = new Date(value)
          if (isNaN(startDate.getTime())) {
            newErrors.startDatetime = 'Invalid start date/time'
          }
        }
        break

      case 'endDatetime':
        if (value) {
          const startDate = new Date(formData.startDatetime)
          const endDate = new Date(value)
          if (isNaN(endDate.getTime())) {
            newErrors.endDatetime = 'Invalid end date/time'
          } else if (endDate <= startDate) {
            newErrors.endDatetime = 'End date/time must be after start date/time'
          }
        }
        break

      case 'eventTypeId':
        if (!value || value === 0) {
          newErrors.eventTypeId = 'Event type is required'
        }
        break

      case 'shortDescription':
        if (formData.isPublic === true) {
          if (!value || value.length < 50) {
            newErrors.shortDescription = 'Short description must be at least 50 characters for public events'
          } else if (value.length > 500) {
            newErrors.shortDescription = 'Short description must be 500 characters or less'
          }
        }
        break

      case 'city':
        if (formData.isPublic === true && !value) {
          newErrors.city = 'City is required for public events'
        }
        break

      case 'countryId':
        if (formData.isPublic === true && (!value || value === 0)) {
          newErrors.countryId = 'Country is required for public events'
        }
        break

      case 'latitude':
        if (value !== null && value !== undefined && value !== '') {
          const lat = Number(value)
          if (isNaN(lat) || lat < -90 || lat > 90) {
            newErrors.latitude = 'Latitude must be between -90 and 90'
          }
        }
        break

      case 'longitude':
        if (value !== null && value !== undefined && value !== '') {
          const lon = Number(value)
          if (isNaN(lon) || lon < -180 || lon > 180) {
            newErrors.longitude = 'Longitude must be between -180 and 180'
          }
        }
        break

      case 'organizerContactEmail':
        if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          newErrors.organizerContactEmail = 'Invalid email address'
        }
        break

      case 'description':
        // Description is required for platform-sharing events (backend requirement)
        if (formData.isSharedWithPlatform === true) {
          if (!value || value.trim().length === 0) {
            newErrors.description = 'Full description is required for platform-sharing events'
          }
        }
        break
    }

    setErrors(newErrors)
  }

  // Handle field changes with real-time validation
  const handleChange = (field: keyof EventCreateRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Validate field in real-time
    validateField(field, value)
  }

  // Handle keyboard navigation
  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (e: KeyboardEvent) => {
      // Escape key closes modal
      if (e.key === 'Escape' && !isSubmitting) {
        onClose()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, isSubmitting, onClose])

  // Focus management: Move focus to first required field after visibility selection
  useEffect(() => {
    if (hasSelectedVisibility && activeTab === 'essentials') {
      // Small delay to ensure DOM is updated
      setTimeout(() => {
        const firstInput = document.querySelector<HTMLInputElement>(
          'input[name="eventName"], input[type="text"][aria-required="true"]'
        )
        if (firstInput) {
          firstInput.focus()
        }
      }, 100)
    }
  }, [hasSelectedVisibility, activeTab])

  // Handle public event search
  const handlePublicEventSearch = async (searchTerm: string) => {
    if (searchTerm.length < 2) {
      setPublicEventResults([])
      return
    }

    // Check if offline - don't make API call
    if (!navigator.onLine) {
      setPublicEventResults([])
      setIsSearchingPublicEvents(false)
      return
    }

    setIsSearchingPublicEvents(true)
    try {
      const results = await searchPublicEvents(searchTerm, 10)
      console.log('Public event search results:', results)
      setPublicEventResults(results.events || [])
    } catch (error) {
      console.error('Error searching public events:', error)
      setPublicEventResults([])
    } finally {
      setIsSearchingPublicEvents(false)
    }
  }

  // Step transition handlers
  const handleEventTypeSelect = (type: 'private' | 'public') => {
    setSelectedEventType(type)
    if (type === 'private') {
      // Step 2A: Private → Show full form immediately
      handleChange('isPublic', false)
      handleChange('isSharedWithPlatform', false)
      setCurrentStep('form')
      setHasSelectedVisibility(true)
    } else {
      // Step 2B: Public → Show Search/Skip options
      handleChange('isPublic', true)
      setCurrentStep('search-skip')
    }
  }

  const handleSearchSkip = () => {
    setSkippedSearch(true)
    // Step 3B: Show platform searchability question
    setCurrentStep('platform-question')
  }

  const handlePlatformOptionSelect = (option: 'company-network' | 'platform') => {
    setSelectedPlatformOption(option)
    if (option === 'company-network') {
      handleChange('isSharedWithPlatform', false)
    } else {
      handleChange('isSharedWithPlatform', true)
    }
    // Step 4: Show full form
    setCurrentStep('form')
    setHasSelectedVisibility(true)
  }

  const handleUseExistingEvent = async (event: Event) => {
    setIsLoadingExistingEvent(true)
    setUsedExistingEvent(true)
    setFieldInferenceSource({})

    try {
      let eventDetails: Event = event
      try {
        const fullEvent = await getEventById(event.eventId)
        if (fullEvent) {
          eventDetails = fullEvent
        }
      } catch (fetchError) {
        console.warn('Could not load full event details, using search result data', fetchError)
        toast.warning('Using summary data from search results – some fields may be missing', 'Limited details')
      }

      setSelectedExistingEvent(eventDetails)
      setSelectedEventType('public')
      setSelectedPlatformOption(eventDetails.isSharedWithPlatform ? 'platform' : 'company-network')
      setCurrentStep('form')
      setHasSelectedVisibility(true)
      setActiveTab('essentials')
      setErrors({})

      const joinFormData: EventCreateRequest = {
        ...createInitialFormData(),
        name: eventDetails.name || '',
        shortDescription: eventDetails.shortDescription || null,
        description: eventDetails.description || null,
        startDatetime: eventDetails.startDateTime || '',
        endDatetime: eventDetails.endDateTime || null,
        timezoneIdentifier: eventDetails.timezoneIdentifier || Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC',
        venueName: eventDetails.venueName || null,
        venueAddress: eventDetails.venueAddress || null,
        city: eventDetails.city || null,
        state: eventDetails.state || null,
        countryId: eventDetails.countryId || null,
        latitude: eventDetails.latitude ?? null,
        longitude: eventDetails.longitude ?? null,
        eventTypeId: eventDetails.eventTypeId || 0,
        industryId: eventDetails.industryId ?? null,
        tags: eventDetails.tags ?? null,
        isPublic: true,
        isSharedWithPlatform: eventDetails.isSharedWithPlatform ?? true,
        eventStatusId: eventDetails.eventStatusId || 1,
        organizerCompanyId: eventDetails.organizerCompanyId ?? null,
        organizerContactEmail: eventDetails.organizerContactEmail ?? null,
        organizerWebsite: eventDetails.organizerWebsite ?? null,
        expectedAttendees: eventDetails.expectedAttendees ?? null
      }

      setFormData(joinFormData)
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to load selected event'
      toast.error(message, 'Load failed')
      handleResetExistingEventSelection()
    } finally {
      setIsLoadingExistingEvent(false)
    }
  }

  const handleResetExistingEventSelection = () => {
    setSelectedExistingEvent(null)
    setUsedExistingEvent(false)
    setSelectedPlatformOption(null)
    setHasSelectedVisibility(false)
    setActiveTab('essentials')
    setCurrentStep('search-skip')
    setSelectedEventType('public')
    setSkippedSearch(false)
    setErrors({})
    setFieldInferenceSource({})
    setFormData(createInitialFormData())
    setPublicEventSearchTerm('')
    setPublicEventResults([])
  }

  const renderJoinExistingEventSummary = () => {
    if (!selectedExistingEvent) {
      return null
    }

    const formatDateTime = (iso?: string | null) => {
      if (!iso) return 'Not provided'
      const date = new Date(iso)
      if (Number.isNaN(date.getTime())) return iso
      try {
        return new Intl.DateTimeFormat(browserLocale, {
          dateStyle: 'medium',
          timeStyle: 'short'
        }).format(date)
      } catch {
        return date.toLocaleString()
      }
    }

    const startDate = formatDateTime(selectedExistingEvent.startDateTime)
    const endDate = selectedExistingEvent.endDateTime ? formatDateTime(selectedExistingEvent.endDateTime) : null
    const country = selectedExistingEvent.countryId ? getCountryById(selectedExistingEvent.countryId) : undefined
    const locationParts = [
      selectedExistingEvent.venueName,
      selectedExistingEvent.venueAddress,
      selectedExistingEvent.city,
      selectedExistingEvent.state,
      country?.name
    ].filter(Boolean).join(', ') || 'Not provided'

    const reviewStatusCode = selectedExistingEvent.publicReviewStatus?.statusCode
      ? (selectedExistingEvent.publicReviewStatus.statusCode.toUpperCase() as 'PENDING' | 'APPROVED' | 'REJECTED')
      : selectedExistingEvent.isSharedWithPlatform
        ? 'PENDING'
        : null

    const organizerCompanyName = selectedExistingEvent.organizerCompany?.companyName?.trim()
    const organizerAbn = selectedExistingEvent.organizerCompany?.abn
    const organizerInfoParts = [
      organizerCompanyName,
      organizerAbn ? `ABN ${organizerAbn}` : null
    ].filter(Boolean) as string[]
    const organizerInfo = organizerInfoParts.length > 0
      ? organizerInfoParts.join(' • ')
      : selectedExistingEvent.organizerCompanyId
        ? `Company ID ${selectedExistingEvent.organizerCompanyId}`
        : 'Not provided'

    const organizerContactSources = [
      selectedExistingEvent.organizerContactEmail,
      selectedExistingEvent.organizerWebsite,
      selectedExistingEvent.organizerCompany?.website
    ].filter(Boolean) as string[]
    const organizerContact = organizerContactSources.length > 0 ? organizerContactSources.join(' • ') : null

    const ownerCompanyName = selectedExistingEvent.ownerCompany?.companyName?.trim()
    const ownerAbn = selectedExistingEvent.ownerCompany?.abn
    const ownerInfoParts = [
      ownerCompanyName,
      ownerAbn ? `ABN ${ownerAbn}` : null
    ].filter(Boolean) as string[]
    const ownerCompanyInfo = ownerInfoParts.length > 0
      ? ownerInfoParts.join(' • ')
      : selectedExistingEvent.companyId
        ? `Company ID ${selectedExistingEvent.companyId}`
        : 'Original organizer not available'

    const industryOption = selectedExistingEvent.industryId != null
      ? industries.find(option => option.id === selectedExistingEvent.industryId)
      : undefined
    const industryName = selectedExistingEvent.industry?.industryName
      ?? industryOption?.name
      ?? 'Not provided'
    const industryDescription = selectedExistingEvent.industry?.description ?? industryOption?.description ?? null

    const expectedAttendees = selectedExistingEvent.expectedAttendees != null
      ? selectedExistingEvent.expectedAttendees.toLocaleString()
      : 'Not provided'

    const platformVisibilityText = selectedExistingEvent.isSharedWithPlatform
      ? 'Shared on the EventLead platform'
      : 'Visible to company network only'

    const reviewStatusText = selectedExistingEvent.isSharedWithPlatform
      ? (selectedExistingEvent.publicReviewStatus?.statusName || 'Pending Review')
      : 'No review required'

    const eventStatusText = selectedExistingEvent.eventStatus?.statusName || 'Status not available'

    const participantCompanyName = userCompanies.length > 0 ? userCompanies[0].companyName : 'your company'

    return (
      <div className="space-y-6">
        <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
          <div>
            <h3 className="text-xl font-semibold text-gray-900">Join Existing Platform Event</h3>
            <p className="text-sm text-gray-600">
              We will add <span className="font-semibold">{participantCompanyName}</span> as a participant.
              Event details remain managed by the original organizer.
            </p>
            <p className="mt-1 text-xs text-gray-500">
              All fields are read-only. Contact the organizer if you need changes to the shared event.
            </p>
            {reviewStatusCode && (
              <div className="mt-3">
                <ReviewStatusBadge
                  status={reviewStatusCode}
                  statusName={selectedExistingEvent.publicReviewStatus?.statusName}
                />
              </div>
            )}
          </div>
          <button
            type="button"
            onClick={handleResetExistingEventSelection}
            className="text-sm font-medium text-teal-600 hover:text-teal-700 underline transition-colors"
          >
            Choose a different event
          </button>
        </div>

        {isLoadingExistingEvent ? (
          <div className="flex justify-center py-12">
            <LoadingSpinner size="md" />
          </div>
        ) : (
          <div className="rounded-xl border border-teal-100 bg-white shadow-sm">
            <div className="border-b border-gray-100 px-6 py-4">
              <h4 className="text-lg font-semibold text-gray-900">{selectedExistingEvent.name}</h4>
              {selectedExistingEvent.shortDescription && (
                <p className="mt-1 text-sm text-gray-600">{selectedExistingEvent.shortDescription}</p>
              )}
              <div className="mt-3 flex flex-wrap gap-2">
                {selectedExistingEvent.eventType?.typeName && (
                  <span className="inline-flex items-center rounded-full bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-700">
                    {selectedExistingEvent.eventType.typeName}
                  </span>
                )}
                <span className="inline-flex items-center rounded-full bg-gray-100 px-3 py-1 text-xs font-semibold text-gray-700">
                  {eventStatusText}
                </span>
                <span className="inline-flex items-center rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                  Review: {reviewStatusText}
                </span>
              </div>
            </div>

            <div className="grid gap-6 px-6 py-5 md:grid-cols-2">
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <Calendar className="mt-0.5 h-5 w-5 text-teal-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Schedule</p>
                    <p className="text-sm text-gray-600">{startDate}</p>
                    {endDate && <p className="text-sm text-gray-600">Ends: {endDate}</p>}
                    <p className="text-xs text-gray-500">
                      Timezone: {selectedExistingEvent.timezoneIdentifier || 'Not provided'}
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <MapPin className="mt-0.5 h-5 w-5 text-teal-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Location</p>
                    <p className="text-sm text-gray-600">{locationParts}</p>
                    {selectedExistingEvent.latitude != null && selectedExistingEvent.longitude != null && (
                      <p className="text-xs text-gray-500">
                        Coordinates: {selectedExistingEvent.latitude}, {selectedExistingEvent.longitude}
                      </p>
                    )}
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <Building2 className="mt-0.5 h-5 w-5 text-teal-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Organizer</p>
                    <p className="text-sm text-gray-600">{organizerInfo}</p>
                    {organizerContact && <p className="text-xs text-gray-500">{organizerContact}</p>}
                    <p className="text-xs text-gray-500">Original owner: {ownerCompanyInfo}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Briefcase className="mt-0.5 h-5 w-5 text-teal-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Industry</p>
                    <p className="text-sm text-gray-600">{industryName}</p>
                    {industryDescription && (
                      <p className="text-xs text-gray-500">{industryDescription}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Globe className="mt-0.5 h-5 w-5 text-teal-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Platform visibility</p>
                    <p className="text-sm text-gray-600">{platformVisibilityText}</p>
                    <p className="text-xs text-gray-500">Review status: {reviewStatusText}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Users className="mt-0.5 h-5 w-5 text-teal-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Expected attendees</p>
                    <p className="text-sm text-gray-600">{expectedAttendees}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div className="border-t border-gray-200 bg-gray-50 px-6 py-4 -mx-6 -mb-6 flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            disabled={isSubmitting}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitDisabled}
            aria-disabled={isSubmitDisabled}
            className="btn-primary flex items-center gap-2 px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? (
              <>
                <LoadingSpinner size="sm" />
                {submittingLabel}
              </>
            ) : (
              submitButtonLabel
            )}
          </button>
        </div>
      </div>
    )
  }

  // Smart Field Inference: Load company billing city and recent cities
  const loadSmartFieldInference = async () => {
    try {
      // Get recent cities
      const recentCities = await getRecentEventCities(5)
      
      // If we have recent cities and city field is empty, suggest the most recent one
      if (recentCities.length > 0) {
        setFormData(prev => {
          // Only set if city is empty
          if (!prev.city) {
            setFieldInferenceSource(prevSources => ({ ...prevSources, city: '🔍 From your recent events' }))
            return { ...prev, city: recentCities[0] }
          }
          return prev
        })
      }
      
      // Note: Company billing city requires company ID which we'll need to get from auth context
      // This will be implemented when we have access to current company ID
    } catch (error) {
      console.debug('Error loading smart field inference:', error)
      // Don't show error to user - inference is optional
    }
  }

  // Handle timezone change - infer country from timezone
  const handleTimezoneChange = async (timezoneIdentifier: string) => {
    handleChange('timezoneIdentifier', timezoneIdentifier)
    
    // If country not already set, try to infer from timezone
    if (!formData.countryId) {
      try {
        const countryInfo = await getCountryFromTimezone(timezoneIdentifier)
        if (countryInfo) {
          setFormData(prev => ({ ...prev, countryId: countryInfo.country_id }))
          setFieldInferenceSource(prev => ({ ...prev, countryId: '🔍 Auto-detected from timezone' }))
        }
      } catch (error) {
        // Timezone-to-country mapping not available - this is fine, user can manually select country
        console.debug('Could not infer country from timezone:', timezoneIdentifier)
      }
    }
  }

  const incompleteRequiredFields = getIncompleteRequiredFields()
  const submitButtonLabel = isJoinExistingEvent ? 'Join Event' : 'Create Event'
  const submittingLabel = isJoinExistingEvent ? 'Joining...' : 'Creating...'
  const isSubmitDisabled = isJoinExistingEvent
    ? (isSubmitting || isLoadingExistingEvent)
    : (isSubmitting || isLoadingRefData || incompleteRequiredFields.length > 0)
  const submitAriaDescribedBy = !isJoinExistingEvent && incompleteRequiredFields.length > 0
    ? 'create-event-tooltip'
    : undefined

  if (!isOpen) return null

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
        onClick={onClose}
        role="dialog"
        aria-modal="true"
        aria-labelledby="create-event-title"
      >
        {/* Modal */}
        <div
          className="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden transform transition-all"
          onClick={(e) => e.stopPropagation()}
          role="document"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4">
            <div className="flex items-center justify-between">
              <h2 id="create-event-title" className="text-2xl font-bold">Create Event</h2>
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 p-1 rounded transition-colors"
                aria-label="Close modal"
                disabled={isSubmitting}
                aria-disabled={isSubmitting}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="overflow-y-auto max-h-[calc(90vh-180px)]">
            {/* Tab Navigation - Progressive Disclosure: Only show after Private/Public selected */}
            {hasSelectedVisibility && !isJoinExistingEvent && (
              <div className="border-b border-gray-200 bg-gray-50 px-6 py-2 flex gap-4 transition-all duration-300 ease-in-out">
                <button
                  type="button"
                  onClick={() => setActiveTab('essentials')}
                  aria-label="Tab 1: Essentials"
                  aria-selected={activeTab === 'essentials'}
                  aria-controls="essentials-tab-panel"
                  id="essentials-tab"
                  role="tab"
                  className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                    activeTab === 'essentials'
                      ? 'bg-teal-600 text-white shadow-sm'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  Tab 1: Essentials
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('enhanced')}
                  aria-label="Tab 2: Enhanced Details"
                  aria-selected={activeTab === 'enhanced'}
                  aria-controls="enhanced-tab-panel"
                  id="enhanced-tab"
                  role="tab"
                  className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                    activeTab === 'enhanced'
                      ? 'bg-teal-600 text-white shadow-sm'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  Tab 2: Enhanced Details
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('advanced')}
                  aria-label="Tab 3: Advanced"
                  aria-selected={activeTab === 'advanced'}
                  aria-controls="advanced-tab-panel"
                  id="advanced-tab"
                  role="tab"
                  className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                    activeTab === 'advanced'
                      ? 'bg-teal-600 text-white shadow-sm'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  Tab 3: Advanced
                </button>
              </div>
            )}

            <div className="p-6 space-y-6">
              {isLoadingRefData ? (
                <div className="flex justify-center py-8">
                  <LoadingSpinner size="md" />
                </div>
              ) : (
                <>
                  {/* Step 1: Event Type Selection */}
                  {currentStep === 'type-selection' && (
                    <EventTypeSelector
                      selectedType={selectedEventType}
                      onSelect={handleEventTypeSelect}
                      onCancel={onClose}
                    />
                  )}

                  {/* Step 2B: Search/Skip Options (only for public events) */}
                  {currentStep === 'search-skip' && (
                    <EventSearchStep
                      onSearch={handlePublicEventSearch}
                      onSkip={handleSearchSkip}
                      onBack={() => setCurrentStep('type-selection')}
                      searchTerm={publicEventSearchTerm}
                      searchResults={publicEventResults}
                      isSearching={isSearchingPublicEvents}
                      onSelectEvent={handleUseExistingEvent}
                      onClearSearch={() => {
                              setPublicEventSearchTerm('')
                              setPublicEventResults([])
                      }}
                    />
                  )}

                  {/* Step 3B: Platform Searchability Question (only if skipped search) */}
                  {currentStep === 'platform-question' && (
                    <PlatformSearchabilityQuestion
                      selectedOption={selectedPlatformOption}
                      onSelect={handlePlatformOptionSelect}
                      onBack={() => setCurrentStep('search-skip')}
                    />
                  )}

                  {/* Step 4: Full Form (also Step 2A for private events) */}
                  {currentStep === 'form' && (
                    isJoinExistingEvent ? (
                      renderJoinExistingEventSummary()
                    ) : (
                      <div className="space-y-6">
                        {/* Show review process info banner if platform sharing is enabled */}
                        {formData.isSharedWithPlatform && (
                          <ReviewProcessInfoBanner 
                            guidelinesUrl="/docs/policies/public-event-guidelines"
                          />
                        )}

                        {/* Event Visibility Selector - Replaces old radio buttons */}
                        <div className="space-y-4 border-b pb-6 mb-6">
                          <EventVisibilitySelector
                            isPublic={formData.isPublic ?? false}
                            isSharedWithPlatform={formData.isSharedWithPlatform ?? false}
                            onPublicChange={(isPublic) => {
                              handleChange('isPublic', isPublic)
                              if (!isPublic) {
                                handleChange('isSharedWithPlatform', false)
                              } else {
                                loadSmartFieldInference()
                              }
                            }}
                            onPlatformSharingChange={(isShared) => {
                              handleChange('isSharedWithPlatform', isShared)
                            }}
                            onSearchClick={() => setCurrentStep('search-skip')}
                            showSearchButton={skippedSearch && !usedExistingEvent}
                          />
                          {errors.isPublic && (
                            <p className="mt-1 text-sm text-red-600">{errors.isPublic}</p>
                          )}
                        </div>

                  {/* Tab 1: Essentials - Progressive Disclosure */}
                      {hasSelectedVisibility && activeTab === 'essentials' && (
                    <div 
                      id="essentials-tab-panel"
                      role="tabpanel"
                      aria-labelledby="essentials-tab"
                      className="space-y-4 animate-fade-in"
                    >
                      <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                        <Calendar className="w-5 h-5 text-teal-600" />
                        Essential Information
                      </h3>

                      {/* Event Name - Required */}
                      <div>
                        <EnhancedFormInput
                          type="text"
                          label="Event Name"
                          name="name"
                          value={formData.name}
                          onChange={(value) => handleChange('name', value)}
                          placeholder="Enter event name"
                          required
                          error={errors.name}
                          maxLength={200}
                          aria-required="true"
                          aria-describedby={errors.name ? 'name-error' : 'name-help'}
                        />
                        {errors.name && (
                          <p id="name-error" className="mt-1 text-sm text-red-600" role="alert">
                            {errors.name}
                          </p>
                        )}
                        <p id="name-help" className="sr-only">
                          Event name is required and must be between 3 and 200 characters
                        </p>
                      </div>

                      {/* Short Description - Required for Public Events */}
                      <div>
                        <EnhancedFormInput
                          type="textarea"
                          label={formData.isPublic === true ? "Short Description *" : "Short Description"}
                          name="shortDescription"
                          value={formData.shortDescription || ''}
                          onChange={(value) => handleChange('shortDescription', value || null)}
                          placeholder="Brief summary for list views (max 500 characters)"
                          maxLength={500}
                          showCharacterCount
                          required={formData.isPublic === true}
                          aria-required={formData.isPublic === true}
                          error={errors.shortDescription}
                        />
                        {errors.shortDescription && (
                          <p className="mt-1 text-sm text-red-600" role="alert">
                            {errors.shortDescription}
                          </p>
                        )}
                        {formData.isPublic === true && (
                          <p className="mt-1 text-xs text-gray-500">
                            Short description is required for public events (50-500 characters)
                          </p>
                        )}
                      </div>

                      {/* Start Date and Time - Required */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Start Date <span className="text-red-500">*</span>
                          </label>
                          <input
                            type="date"
                            value={formData.startDatetime ? formData.startDatetime.split('T')[0] : ''}
                            onChange={(e) => {
                              const dateValue = e.target.value
                              const timeValue = formData.startDatetime ? formData.startDatetime.split('T')[1] : '00:00'
                              handleChange('startDatetime', dateValue ? `${dateValue}T${timeValue}` : '')
                            }}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.startDatetime ? 'border-red-500' : 'border-gray-300'
                            }`}
                            required
                            aria-required="true"
                            aria-describedby={errors.startDatetime ? 'start-date-error' : 'start-date-help'}
                            id="start-date-input"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Start Time <span className="text-red-500">*</span>
                            <span className="text-xs text-gray-500 ml-2">
                              ({uses12HourFormat ? '12-hour' : '24-hour'} format)
                            </span>
                          </label>
                          <input
                            type="time"
                            step="60"
                            value={formData.startDatetime ? formData.startDatetime.split('T')[1]?.slice(0, 5) || '00:00' : '00:00'}
                            onChange={(e) => {
                              const timeValue = e.target.value ? e.target.value + ':00' : '00:00:00'
                              const dateValue = formData.startDatetime ? formData.startDatetime.split('T')[0] : new Date().toISOString().split('T')[0]
                              handleChange('startDatetime', `${dateValue}T${timeValue}`)
                            }}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.startDatetime ? 'border-red-500' : 'border-gray-300'
                            }`}
                            required
                            aria-required="true"
                            aria-describedby={errors.startDatetime ? 'start-time-error' : 'start-time-help'}
                            aria-label={`Start time in ${uses12HourFormat ? '12-hour' : '24-hour'} format`}
                            id="start-time-input"
                          />
                        </div>
                      </div>
                      {errors.startDatetime && (
                        <p id="start-date-error" className="mt-1 text-sm text-red-600" role="alert">
                          {errors.startDatetime}
                        </p>
                      )}
                      <p id="start-date-help" className="sr-only">
                        Start date and time are required. Format: {uses12HourFormat ? '12-hour (AM/PM)' : '24-hour'}
                      </p>
                      <p id="start-time-help" className="sr-only">
                        Start time is required. Format: {uses12HourFormat ? '12-hour (AM/PM)' : '24-hour'}
                      </p>

                      {/* End Date and Time */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            End Date
                          </label>
                          <input
                            type="date"
                            value={formData.endDatetime ? formData.endDatetime.split('T')[0] : ''}
                            onChange={(e) => {
                              const dateValue = e.target.value
                              const timeValue = formData.endDatetime ? formData.endDatetime.split('T')[1] : '00:00'
                              handleChange('endDatetime', dateValue ? `${dateValue}T${timeValue}` : null)
                            }}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.endDatetime ? 'border-red-500' : 'border-gray-300'
                            }`}
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            End Time
                            <span className="text-xs text-gray-500 ml-2">
                              ({uses12HourFormat ? '12-hour' : '24-hour'} format)
                            </span>
                          </label>
                          <input
                            type="time"
                            step="60"
                            value={formData.endDatetime ? formData.endDatetime.split('T')[1]?.slice(0, 5) || '00:00' : ''}
                            onChange={(e) => {
                              const timeValue = e.target.value ? e.target.value + ':00' : '00:00:00'
                              const dateValue = formData.endDatetime ? formData.endDatetime.split('T')[0] : (formData.startDatetime ? formData.startDatetime.split('T')[0] : new Date().toISOString().split('T')[0])
                              handleChange('endDatetime', `${dateValue}T${timeValue}`)
                            }}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.endDatetime ? 'border-red-500' : 'border-gray-300'
                            }`}
                          />
                        </div>
                      </div>
                      {errors.endDatetime && (
                        <p className="mt-1 text-sm text-red-600">{errors.endDatetime}</p>
                      )}

                      {/* Timezone */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Timezone
                          {fieldInferenceSource.timezoneIdentifier && (
                            <span className="ml-2 text-xs text-teal-600 font-normal">
                              {fieldInferenceSource.timezoneIdentifier}
                            </span>
                          )}
                        </label>
                        <input
                          type="text"
                          value={formData.timezoneIdentifier || ''}
                          onChange={(e) => handleTimezoneChange(e.target.value)}
                          placeholder="e.g., America/New_York, Europe/London"
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                        />
                        <p className="mt-1 text-xs text-gray-500">
                          IANA timezone identifier (e.g., America/New_York)
                          {fieldInferenceSource.timezoneIdentifier && (
                            <span className="block mt-1 text-teal-600">
                              {fieldInferenceSource.timezoneIdentifier}
                            </span>
                          )}
                        </p>
                      </div>

                      {/* Location: City and Country - Required for Public Events */}
                      {formData.isPublic === true && (
                        <>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {/* City - Required for Public */}
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">
                                City <span className="text-red-500">*</span>
                                {fieldInferenceSource.city && (
                                  <span className="ml-2 text-xs text-teal-600 font-normal">
                                    {fieldInferenceSource.city}
                                  </span>
                                )}
                              </label>
                              <EnhancedFormInput
                                type="text"
                                label=""
                                name="city"
                                value={formData.city || ''}
                                onChange={(value) => {
                                  handleChange('city', value || null)
                                  // Clear source tracking when user manually changes
                                  if (fieldInferenceSource.city && value) {
                                    setFieldInferenceSource(prev => {
                                      const newSources = { ...prev }
                                      delete newSources.city
                                      return newSources
                                    })
                                  }
                                }}
                                placeholder="City"
                                maxLength={100}
                                required
                                aria-required="true"
                                error={errors.city}
                                aria-describedby={errors.city ? 'city-error' : 'city-help'}
                              />
                              {errors.city && (
                                <p id="city-error" className="mt-1 text-sm text-red-600" role="alert">
                                  {errors.city}
                                </p>
                              )}
                              {fieldInferenceSource.city && !errors.city && (
                                <p className="mt-1 text-xs text-teal-600">
                                  {fieldInferenceSource.city}
                                </p>
                              )}
                              <p id="city-help" className="sr-only">
                                City is required for public events. Enter the city where the event will take place.
                              </p>
                            </div>

                            {/* State - Optional */}
                            <div>
                              <EnhancedFormInput
                                type="text"
                                label="State/Province"
                                name="state"
                                value={formData.state || ''}
                                onChange={(value) => handleChange('state', value || null)}
                                placeholder="State or Province"
                                maxLength={100}
                              />
                            </div>
                          </div>

                          {/* Country - Required for Public */}
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Country <span className="text-red-500">*</span>
                              {fieldInferenceSource.countryId && (
                                <span className="ml-2 text-xs text-teal-600 font-normal">
                                  {fieldInferenceSource.countryId}
                                </span>
                              )}
                            </label>
                            <select
                              value={formData.countryId || ''}
                              onChange={(e) => {
                                handleChange('countryId', e.target.value ? Number(e.target.value) : null)
                                // Clear source tracking when user manually changes
                                if (fieldInferenceSource.countryId) {
                                  setFieldInferenceSource(prev => {
                                    const newSources = { ...prev }
                                    delete newSources.countryId
                                    return newSources
                                  })
                                }
                              }}
                              className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                                errors.countryId ? 'border-red-500' : 'border-gray-300'
                              }`}
                              required
                              aria-required="true"
                              aria-describedby={errors.countryId ? 'country-error' : 'country-help'}
                              id="country-select"
                            >
                              <option value="">Select country...</option>
                              {countries.map((country) => (
                                <option key={country.id} value={country.id}>
                                  {country.name}
                                </option>
                              ))}
                            </select>
                            {errors.countryId && (
                              <p id="country-error" className="mt-1 text-sm text-red-600" role="alert">
                                {errors.countryId}
                              </p>
                            )}
                            {fieldInferenceSource.countryId && (
                              <p className="mt-1 text-xs text-teal-600">
                                {fieldInferenceSource.countryId}
                              </p>
                            )}
                            <p id="country-help" className="sr-only">
                              Country is required for public events. Select from the dropdown.
                            </p>
                          </div>
                        </>
                      )}

                      {/* Event Type - Required */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Event Type <span className="text-red-500">*</span>
                        </label>
                        {!navigator.onLine && eventTypes.length === 0 ? (
                          <div className="w-full px-3 py-2 border border-yellow-400 bg-yellow-50 rounded-md">
                            <p className="text-sm text-yellow-800">
                              <strong>Offline:</strong> Event types are unavailable. Please connect to the internet to select an event type.
                            </p>
                          </div>
                        ) : (
                          <select
                            value={formData.eventTypeId}
                            onChange={(e) => handleChange('eventTypeId', Number(e.target.value))}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.eventTypeId ? 'border-red-500' : 'border-gray-300'
                            } ${!navigator.onLine && eventTypes.length === 0 ? 'bg-gray-100 cursor-not-allowed' : ''}`}
                            required
                            disabled={!navigator.onLine && eventTypes.length === 0}
                            aria-required="true"
                            aria-describedby={errors.eventTypeId ? 'event-type-error' : 'event-type-help'}
                            id="event-type-select"
                          >
                            <option key="select-event-type" value={0}>Select event type...</option>
                            {eventTypes.length > 0 ? (
                              eventTypes.map((type) => (
                                <option key={type.eventTypeId} value={type.eventTypeId}>
                                  {type.typeName}
                                </option>
                              ))
                            ) : (
                              <option value={0} disabled>
                                {!navigator.onLine ? 'Unavailable offline' : 'Loading event types...'}
                              </option>
                            )}
                          </select>
                        )}
                        {errors.eventTypeId && (
                          <p id="event-type-error" className="mt-1 text-sm text-red-600" role="alert">
                            {errors.eventTypeId}
                          </p>
                        )}
                        <p id="event-type-help" className="sr-only">
                          Event type is required. Select from the dropdown.
                        </p>
                      </div>

                      {/* Organizer Company - Required for Public Events */}
                      {formData.isPublic === true && (
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Organizer Company <span className="text-red-500">*</span>
                          </label>
                          <select
                            value={formData.organizerCompanyId || ''}
                            onChange={(e) => handleChange('organizerCompanyId', e.target.value ? Number(e.target.value) : null)}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.organizerCompanyId ? 'border-red-500' : 'border-gray-300'
                            }`}
                            required
                            aria-required="true"
                            aria-describedby={errors.organizerCompanyId ? 'organizer-company-error' : 'organizer-company-help'}
                            id="organizer-company-select"
                          >
                            <option value="">Select organizer company...</option>
                            {userCompanies.map((company) => (
                              <option key={company.companyId} value={company.companyId}>
                                {company.companyName}
                              </option>
                            ))}
                          </select>
                          {errors.organizerCompanyId && (
                            <p id="organizer-company-error" className="mt-1 text-sm text-red-600" role="alert">
                              {errors.organizerCompanyId}
                            </p>
                          )}
                          <p id="organizer-company-help" className="sr-only">
                            Organizer company is required for public events. Select the company organizing this event.
                          </p>
                          <p className="mt-1 text-xs text-gray-500">
                            Select the company organizing this event. This will be visible to other users searching for public events.
                          </p>
                        </div>
                      )}

                      {/* Event Status */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Status
                        </label>
                        <select
                          value={formData.eventStatusId || 1}
                          onChange={(e) => handleChange('eventStatusId', Number(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                        >
                          {eventStatuses.map((status) => (
                            <option key={status.eventStatusId} value={status.eventStatusId}>
                              {status.statusColor ? '● ' : ''}{status.statusName}{status.statusDescription ? ` - ${status.statusDescription}` : ''}
                            </option>
                          ))}
                        </select>
                      </div>

                    </div>
                  )}

                  {/* Tab 2: Enhanced Details - Progressive Disclosure */}
                      {hasSelectedVisibility && activeTab === 'enhanced' && (
                    <div 
                      id="enhanced-tab-panel"
                      role="tabpanel"
                      aria-labelledby="enhanced-tab"
                      className="space-y-4 animate-fade-in"
                    >
                      <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                          <MapPin className="w-5 h-5 text-teal-600" />
                          Location Information
                        </h3>
                        <button
                          type="button"
                          onClick={() => setActiveTab('advanced')}
                          className="text-sm text-teal-600 hover:text-teal-700 underline transition-colors"
                        >
                          Skip to Tab 3: Advanced →
                        </button>
                      </div>

                      {/* Venue Name */}
                      <div>
                        <EnhancedFormInput
                          type="text"
                          label="Venue Name"
                          name="venueName"
                          value={formData.venueName || ''}
                          onChange={(value) => handleChange('venueName', value || null)}
                          placeholder="Enter venue name"
                          maxLength={200}
                        />
                      </div>

                      {/* Venue Address */}
                      <div>
                        <EnhancedFormInput
                          type="textarea"
                          label="Venue Address"
                          name="venueAddress"
                          value={formData.venueAddress || ''}
                          onChange={(value) => handleChange('venueAddress', value || null)}
                          placeholder="Full venue address"
                          maxLength={500}
                        />
                      </div>

                      {/* Full Description - Moved from Tab 1 */}
                      <div>
                        <EnhancedFormInput
                          type="textarea"
                          label={formData.isSharedWithPlatform === true ? "Full Description *" : "Full Description"}
                          name="description"
                          value={formData.description || ''}
                          onChange={(value) => handleChange('description', value || null)}
                          placeholder="Detailed event description"
                          required={formData.isSharedWithPlatform === true}
                          aria-required={formData.isSharedWithPlatform === true}
                          error={errors.description}
                        />
                        {formData.isSharedWithPlatform === true && (
                          <p className="mt-1 text-xs text-gray-500">
                            Full description is required for platform-sharing events (this field is in Tab 2: Enhanced Details)
                          </p>
                        )}
                        {errors.description && (
                          <p className="mt-1 text-sm text-red-600" role="alert">
                            {errors.description}
                          </p>
                        )}
                      </div>

                      {/* Location: City and Country - Only show for Private events (Public events have these in Tab 1) */}
                      {formData.isPublic === false && (
                        <>
                          <div className="grid grid-cols-2 gap-4">
                            {/* City - Optional for Private */}
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">
                                City
                                {fieldInferenceSource.city && (
                                  <span className="ml-2 text-xs text-teal-600 font-normal">
                                    {fieldInferenceSource.city}
                                  </span>
                                )}
                              </label>
                              <EnhancedFormInput
                                type="text"
                                label=""
                                name="city"
                                value={formData.city || ''}
                                onChange={(value) => {
                                  handleChange('city', value || null)
                                  // Clear source tracking when user manually changes
                                  if (fieldInferenceSource.city && value) {
                                    setFieldInferenceSource(prev => {
                                      const newSources = { ...prev }
                                      delete newSources.city
                                      return newSources
                                    })
                                  }
                                }}
                                placeholder="City"
                                maxLength={100}
                              />
                              {fieldInferenceSource.city && (
                                <p className="mt-1 text-xs text-teal-600">
                                  {fieldInferenceSource.city}
                                </p>
                              )}
                            </div>

                            {/* State - Optional */}
                            <div>
                              <EnhancedFormInput
                                type="text"
                                label="State/Province"
                                name="state"
                                value={formData.state || ''}
                                onChange={(value) => handleChange('state', value || null)}
                                placeholder="State or Province"
                                maxLength={100}
                              />
                            </div>
                          </div>

                          {/* Country - Optional for Private */}
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              Country
                              {fieldInferenceSource.countryId && (
                                <span className="ml-2 text-xs text-teal-600 font-normal">
                                  {fieldInferenceSource.countryId}
                                </span>
                              )}
                            </label>
                            <select
                              value={formData.countryId || ''}
                              onChange={(e) => {
                                handleChange('countryId', e.target.value ? Number(e.target.value) : null)
                                // Clear source tracking when user manually changes
                                if (fieldInferenceSource.countryId) {
                                  setFieldInferenceSource(prev => {
                                    const newSources = { ...prev }
                                    delete newSources.countryId
                                    return newSources
                                  })
                                }
                              }}
                              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                            >
                              <option value="">Select country...</option>
                              {countries.map((country) => (
                                <option key={country.id} value={country.id}>
                                  {country.name}
                                </option>
                              ))}
                            </select>
                            {fieldInferenceSource.countryId && (
                              <p className="mt-1 text-xs text-teal-600">
                                {fieldInferenceSource.countryId}
                              </p>
                            )}
                          </div>
                        </>
                      )}

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
                            value={formData.latitude || ''}
                            onChange={(e) => handleChange('latitude', e.target.value ? parseFloat(e.target.value) : null)}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.latitude ? 'border-red-500' : 'border-gray-300'
                            }`}
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
                            value={formData.longitude || ''}
                            onChange={(e) => handleChange('longitude', e.target.value ? parseFloat(e.target.value) : null)}
                            className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
                              errors.longitude ? 'border-red-500' : 'border-gray-300'
                            }`}
                            placeholder="-180 to 180"
                          />
                          {errors.longitude && (
                            <p className="mt-1 text-sm text-red-600">{errors.longitude}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Tab 3: Advanced - Progressive Disclosure */}
                      {hasSelectedVisibility && activeTab === 'advanced' && (
                    <div 
                      id="advanced-tab-panel"
                      role="tabpanel"
                      aria-labelledby="advanced-tab"
                      className="space-y-4 animate-fade-in"
                    >
                      <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                          <Building2 className="w-5 h-5 text-teal-600" />
                          Advanced Features
                        </h3>
                        <button
                          type="button"
                          onClick={() => setActiveTab('essentials')}
                          className="text-sm text-teal-600 hover:text-teal-700 underline transition-colors"
                        >
                          ← Back to Tab 1: Essentials
                        </button>
                      </div>

                      {/* Industry */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Industry
                        </label>
                        <select
                          value={formData.industryId || ''}
                          onChange={(e) => handleChange('industryId', e.target.value ? Number(e.target.value) : null)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                        >
                          <option value="">Select industry...</option>
                          {industries.map((industry) => (
                            <option key={industry.id} value={industry.id}>
                              {industry.name}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* Tags */}
                      <div>
                        <EnhancedFormInput
                          type="text"
                          label="Tags"
                          name="tags"
                          value={formData.tags || ''}
                          onChange={(value) => handleChange('tags', value || null)}
                          placeholder="Comma-separated tags"
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
                          value={formData.expectedAttendees || ''}
                          onChange={(e) => handleChange('expectedAttendees', e.target.value ? parseInt(e.target.value) : null)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                          placeholder="Expected number of attendees"
                        />
                      </div>

                      {/* Organizer Contact Email */}
                      <div>
                        <EnhancedFormInput
                          type="email"
                          label="Organizer Contact Email"
                          name="organizerContactEmail"
                          value={formData.organizerContactEmail || ''}
                          onChange={(value) => handleChange('organizerContactEmail', value || null)}
                          placeholder="contact@example.com"
                          error={errors.organizerContactEmail}
                        />
                      </div>

                      {/* Organizer Website */}
                      <div>
                        <EnhancedFormInput
                          type="url"
                          label="Organizer Website"
                          name="organizerWebsite"
                          value={formData.organizerWebsite || ''}
                          onChange={(value) => handleChange('organizerWebsite', value || null)}
                          placeholder="https://www.example.com"
                        />
                      </div>

                      {/* Recurring Event Checkbox */}
                      <div>
                        <label className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            checked={formData.isRecurring}
                            onChange={(e) => handleChange('isRecurring', e.target.checked)}
                            className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
                          />
                          <span className="text-sm text-gray-700">Recurring Event</span>
                        </label>
                      </div>
                    </div>
                  )}

                      {/* Footer - Only show on form step */}
                      <div className="border-t border-gray-200 bg-gray-50 px-6 py-4 -mx-6 -mb-6 flex items-center justify-end gap-3">
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
                            disabled={isSubmitDisabled}
                            aria-disabled={isSubmitDisabled}
                            aria-describedby={submitAriaDescribedBy}
                            className="btn-primary flex items-center gap-2 px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {isSubmitting ? (
                              <>
                                <LoadingSpinner size="sm" />
                                {submittingLabel}
                              </>
                            ) : (
                              submitButtonLabel
                            )}
                          </button>
                          {!isJoinExistingEvent && incompleteRequiredFields.length > 0 && (
                            <div
                              id="create-event-tooltip"
                              role="tooltip"
                              className="absolute bottom-full right-0 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md shadow-lg z-50 min-w-[250px] max-w-[400px] opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 pointer-events-none transition-opacity duración-200"
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
                    </div>
                  )
                )}
                </>
              )}
            </div>
          </form>
        </div>
      </div>
    </>
  )
}
