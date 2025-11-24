/**
 * Company Container Component - Story 1.18
 * AC-1.18.3: Recursive company container
 * AC-1.18.4: Company selection and switching
 * Story 2.4: Event display when expanded
 */

import React, { useState, useEffect } from 'react'
import { Building2, Users as UsersIcon, Settings, ChevronDown, ChevronRight, Calendar, MapPin, Tag, Globe, Clock, FileText, Edit2, Trash2, Eye, CheckCircle, XCircle, Clock as ClockIcon, AlertCircle, Ban, Star, Share2, LogOut } from 'lucide-react'
import type { Company } from '../types/dashboard.types'
import { getEvents } from '../../events/api/eventsApi'
import type { Event } from '../../events/types/events.types'
import { getFormsByEvent } from '../../forms/api/formsApi'
import type { Form } from '../../forms/types/form.types'
import { checkFormAccess } from '../../forms/api/formAccessApi'
import { useAuth } from '../../auth/context/AuthContext'
import { ShareEventModal } from '../../events/components/ShareEventModal'

interface CompanyContainerProps {
  company: Company
  isActive: boolean
  isExpanded: boolean
  onSelect: (companyId: number) => void
  onToggleExpand: (companyId: number) => void
  onOpenTeamPanel: (companyId: number) => void
  onSetDefaultCompany?: (companyId: number) => void
  onCreateEvent?: (companyId: number) => void
  onEditEvent?: (event: Event) => void
  onDeleteEvent?: (event: Event) => void
  onCreateForm?: (eventId: number) => void
  onEditForm?: (form: Form) => void
  onDeleteForm?: (form: Form) => void
  onViewForm?: (form: Form) => void
  depth?: number
  maxDepth?: number
}

export function CompanyContainer({
  company,
  isActive,
  isExpanded,
  onSelect,
  onToggleExpand,
  onOpenTeamPanel,
  onSetDefaultCompany,
  onCreateEvent,
  onEditEvent,
  onDeleteEvent,
  onCreateForm,
  onEditForm,
  onDeleteForm,
  onViewForm,
  depth = 0,
  maxDepth = 5
}: CompanyContainerProps) {
  const { user } = useAuth()
  const hasChildren = company.childCompanies && company.childCompanies.length > 0
  const isAdmin = company.userRole === 'Company Admin'
  
  // Event state management - Story 2.4
  const [events, setEvents] = useState<Event[]>([])
  const [isLoadingEvents, setIsLoadingEvents] = useState(false)
  const [eventsError, setEventsError] = useState<string | null>(null)
  
  // Event expansion state - Story 2.8: Forms nested under Events
  const [expandedEventIds, setExpandedEventIds] = useState<number[]>([])
  
  // Forms state management - Story 2.8
  const [eventForms, setEventForms] = useState<Record<number, Form[]>>({})
  const [isLoadingForms, setIsLoadingForms] = useState<Record<number, boolean>>({})
  
  // Form access levels - Story 2.9: Store access level for each form
  const [formAccessLevels, setFormAccessLevels] = useState<Record<number, string | null>>({})
  
  // Share Event state - Story 2.10
  const [showShareModal, setShowShareModal] = useState(false)
  const [eventToShare, setEventToShare] = useState<Event | null>(null)

  // Fetch events when expanded and company has events - Story 2.4
  // Only load events if this company matches the active company context from auth
  // Reload events when company changes, becomes active/expanded, or when auth context company changes
  useEffect(() => {
    // Only load events if:
    // 1. Company is expanded
    // 2. Company has no children (children have their own containers)
    // 3. Company has events
    // 4. This company matches the active company
    // 
    // IMPORTANT: Use `isActive` prop as PRIMARY check because it's updated optimistically
    // in DashboardLayout when handleSelectCompany is called, before async operations complete.
    // The `user?.company_id` might lag behind during company switches due to async state updates.
    // We check BOTH to ensure we have the most accurate state, but prioritize the prop.
    const isActiveFromContext = user?.company_id === company.companyId
    const isActiveFromProp = isActive // Passed from DashboardLayout based on activeCompanyId
    // Company is active if prop says so (fast, optimistic) OR context confirms (slower, authoritative)
    const isActiveCompany = isActiveFromProp || isActiveFromContext
    
    console.log(`[CompanyContainer ${company.companyId}] Event load check:`, {
      isExpanded,
      hasChildren,
      eventCount: company.eventCount,
      isActiveCompany,
      isActiveFromProp,
      isActiveFromContext,
      userCompanyId: user?.company_id,
      companyId: company.companyId,
      isActive
    })
    
    // CRITICAL: Clear events if company is NOT active
    // Only clear if we're certain it's not active (both prop and context agree)
    // This prevents premature clearing during the transition period
    if (!isActiveFromProp && !isActiveFromContext && user?.company_id !== undefined) {
      // Both prop and context confirm this company is not active - clear events immediately
      console.log(`[CompanyContainer ${company.companyId}] Clearing events - not active company (prop: ${isActiveFromProp}, context: ${isActiveFromContext}, userCompanyId: ${user?.company_id})`)
      setEvents([])
      setEventsError(null)
      setExpandedEventIds([])
      setEventForms({})
      return // Don't try to load events for inactive company
    }
    
    if (isExpanded && !hasChildren) {
      // Load events if company is active (from prop OR context) and has events
      // NOTE: We use isActiveCompany which checks both prop and context, so it works even
      // during the transition period when prop says active but context hasn't updated yet
      if (isActiveCompany && company.eventCount > 0) {
        console.log(`[CompanyContainer ${company.companyId}] Loading events (active company, ${company.eventCount} events, prop: ${isActiveFromProp}, context: ${isActiveFromContext})...`)
        // Pass isActiveCompany flag to loadEvents so it can bypass the user.company_id check
        // during the transition period
        loadEvents(isActiveCompany)
      } else if (isActiveCompany && company.eventCount === 0) {
        // Active company but no events - clear any existing events
        console.log(`[CompanyContainer ${company.companyId}] Active company but no events (count: 0) - clearing`)
        setEvents([])
        setEventsError(null)
        setExpandedEventIds([])
        setEventForms({})
      }
    } else {
      // Clear events when collapsed or has children
      if (!isExpanded || hasChildren) {
        console.log(`[CompanyContainer ${company.companyId}] Clearing events - collapsed or has children`)
        setEvents([])
        setEventsError(null)
        setExpandedEventIds([])
        setEventForms({})
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isExpanded, company.companyId, company.eventCount, company.childCompanies?.length, isActive, user?.company_id])

  // Listen for offline queue processing completion and refresh events
  useEffect(() => {
    const handleQueueProcessed = () => {
      // Only refresh if this company is expanded and active
      if (isExpanded && isActive && !hasChildren) {
        console.log('🔄 Offline queue processed - refreshing events')
        loadEvents(true) // Pass isActive=true since we already checked it above
      }
    }

    window.addEventListener('offlineQueueProcessed', handleQueueProcessed)
    return () => {
      window.removeEventListener('offlineQueueProcessed', handleQueueProcessed)
    }
  }, [isExpanded, isActive, hasChildren]) // eslint-disable-next-line react-hooks/exhaustive-deps

  // Listen for form creation/update and refresh forms for that event - Story 2.8
  useEffect(() => {
    const handleFormCreated = (event: CustomEvent<{ eventId: number }>) => {
      const { eventId } = event.detail
      // If this event is expanded, refresh its forms
      if (expandedEventIds.includes(eventId)) {
        console.log(`🔄 Form created - refreshing forms for event ${eventId}`)
        loadFormsForEvent(eventId)
      }
    }

    const handleFormUpdated = (event: CustomEvent<{ eventId: number }>) => {
      const { eventId } = event.detail
      // If this event is expanded, refresh its forms
      if (expandedEventIds.includes(eventId)) {
        console.log(`🔄 Form updated - refreshing forms for event ${eventId}`)
        loadFormsForEvent(eventId)
      }
    }

    window.addEventListener('formCreated', handleFormCreated as EventListener)
    window.addEventListener('formUpdated', handleFormUpdated as EventListener)
    return () => {
      window.removeEventListener('formCreated', handleFormCreated as EventListener)
      window.removeEventListener('formUpdated', handleFormUpdated as EventListener)
    }
  }, [expandedEventIds]) // eslint-disable-line react-hooks/exhaustive-deps
  
  const loadEvents = async (isActiveOverride?: boolean) => {
    // Use isActiveOverride (from prop) if provided, otherwise check user context
    // This allows loading events during company switch when prop is true but context hasn't updated yet
    const isCurrentlyActive = isActiveOverride !== undefined 
      ? isActiveOverride 
      : (user?.company_id === company.companyId)
    
    if (!isCurrentlyActive) {
      console.log(`[CompanyContainer ${company.companyId}] Skipping event load - not active company (override: ${isActiveOverride}, userCompanyId: ${user?.company_id})`)
      return
    }
    
    // Store the expected company ID to verify after async operation
    const expectedCompanyId = company.companyId
    const wasActiveFromProp = isActiveOverride === true
    
    console.log(`[CompanyContainer ${company.companyId}] Starting to load events... (wasActiveFromProp: ${wasActiveFromProp})`)
    setIsLoadingEvents(true)
    setEventsError(null)
    
    // Clear events immediately when starting to load (prevents stale data showing)
    setEvents([])
    
    try {
      const response = await getEvents(1, 50) // Load up to 50 events
      
      // CRITICAL: Verify the company is still active before setting events
      // This prevents events from the previous company showing up after a switch
      // Check both prop (isActive) and context (user.company_id) to handle transition period
      const isStillActive = wasActiveFromProp || (user?.company_id === expectedCompanyId)
      
      if (!isStillActive) {
        console.log(`[CompanyContainer ${expectedCompanyId}] Event load completed but company switched - discarding results (userCompanyId: ${user?.company_id}, wasActiveFromProp: ${wasActiveFromProp})`)
        setEvents([])
        return
      }
      
      console.log(`[CompanyContainer ${company.companyId}] Loaded ${response.events.length} events`)
      setEvents(response.events)
    } catch (error) {
      // Only set error if company is still active
      const isStillActive = wasActiveFromProp || (user?.company_id === expectedCompanyId)
      if (isStillActive) {
        console.error(`[CompanyContainer ${company.companyId}] Failed to load events:`, error)
        setEventsError('Failed to load events')
        setEvents([])
      } else {
        console.log(`[CompanyContainer ${expectedCompanyId}] Event load failed but company switched - discarding error`)
      }
    } finally {
      // Only update loading state if company is still active
      const isStillActive = wasActiveFromProp || (user?.company_id === expectedCompanyId)
      if (isStillActive) {
        setIsLoadingEvents(false)
      }
    }
  }
  
  // Load forms for an event - Story 2.8
  // Always load forms so we can show count even when collapsed
  // Story 2.9: Also check access level for each form
  const loadFormsForEvent = async (eventId: number) => {
    setIsLoadingForms(prev => ({ ...prev, [eventId]: true }))
    try {
      const response = await getFormsByEvent(eventId)
      setEventForms(prev => ({ ...prev, [eventId]: response.forms }))
      
      // Check access level for each form - Story 2.9
      const accessLevels: Record<number, string | null> = {}
      await Promise.all(
        response.forms.map(async (form) => {
          try {
            const accessCheck = await checkFormAccess(form.formId)
            accessLevels[form.formId] = accessCheck.accessLevel || accessCheck.accessType?.accessTypeCode || null
          } catch (error) {
            console.error(`Failed to check access for form ${form.formId}:`, error)
            accessLevels[form.formId] = null
          }
        })
      )
      setFormAccessLevels(prev => ({ ...prev, ...accessLevels }))
    } catch (error) {
      console.error(`Failed to load forms for event ${eventId}:`, error)
      setEventForms(prev => ({ ...prev, [eventId]: [] }))
    } finally {
      setIsLoadingForms(prev => ({ ...prev, [eventId]: false }))
    }
  }
  
  // Load forms for all events when events are loaded - Story 2.8
  // Also set all events to expanded by default
  useEffect(() => {
    if (events.length > 0) {
      // Expand all events by default
      const allEventIds = events.map(event => event.eventId)
      setExpandedEventIds(allEventIds)
      
      // Load forms for all events
      events.forEach(event => {
        if (!eventForms[event.eventId] && !isLoadingForms[event.eventId]) {
          loadFormsForEvent(event.eventId)
        }
      })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [events])
  
  // Toggle event expansion - Story 2.8
  const handleToggleEventExpand = (eventId: number) => {
    setExpandedEventIds(prev => {
      const isExpanded = prev.includes(eventId)
      if (isExpanded) {
        // Collapsing - remove from expanded list
        return prev.filter(id => id !== eventId)
      } else {
        // Expanding - add to list (forms already loaded)
        return [...prev, eventId]
      }
    })
  }

  // Helper function to get form status icon
  const getFormStatusIcon = (statusCode: string) => {
    switch (statusCode.toUpperCase()) {
      case 'DRAFT':
        return <FileText className="w-3 h-3" />
      case 'REVIEW':
        return <ClockIcon className="w-3 h-3" />
      case 'PUBLISHED':
        return <CheckCircle className="w-3 h-3" />
      case 'PAUSED':
        return <AlertCircle className="w-3 h-3" />
      default:
        return <FileText className="w-3 h-3" />
    }
  }

  // Helper function to get approval status icon
  const getApprovalStatusIcon = (approvalStatusCode: string) => {
    switch (approvalStatusCode.toUpperCase()) {
      case 'NO_APPROVAL':
        return <CheckCircle className="w-3 h-3" />
      case 'PENDING':
        return <ClockIcon className="w-3 h-3" />
      case 'APPROVED':
        return <CheckCircle className="w-3 h-3" />
      case 'REJECTED':
        return <XCircle className="w-3 h-3" />
      case 'CANCELLED':
        return <Ban className="w-3 h-3" />
      case 'EXPIRED':
        return <ClockIcon className="w-3 h-3" />
      default:
        return <FileText className="w-3 h-3" />
    }
  }
  
  // Indentation based on hierarchy level
  const indentClass = depth > 0 ? `ml-${Math.min(depth * 4, 12)}` : ''
  
  // Active state styling
  const containerClass = isActive
    ? 'border-2 border-teal-500 bg-teal-50'
    : 'border border-gray-200 bg-white hover:border-gray-300'

  return (
    <div className={`mb-2 ${indentClass}`}>
      {/* Company Header - AC-1.18.4: Clickable for selection */}
      <div
        className={`${containerClass} rounded-lg transition-all duration-200 cursor-pointer`}
        onClick={() => onSelect(company.companyId)}
      >
        <div className="p-4 flex items-center justify-between">
          {/* Left: Expand toggle + Company info */}
          <div className="flex items-center gap-3 flex-1">
            {/* Expand/Collapse Toggle - Always visible to allow collapsing/expanding events */}
            <button
              onClick={(e) => {
                e.stopPropagation() // Don't trigger container selection
                onToggleExpand(company.companyId)
              }}
              className="text-gray-500 hover:text-gray-700 p-1 rounded hover:bg-gray-100 flex-shrink-0"
              aria-label={isExpanded ? 'Collapse' : 'Expand'}
              title={isExpanded ? 'Collapse' : 'Expand'}
            >
              {isExpanded ? (
                <ChevronDown className="w-5 h-5" />
              ) : (
                <ChevronRight className="w-5 h-5" />
              )}
            </button>
            
            {/* Company Icon and Name */}
            <div className="flex items-center gap-2 flex-1">
              <Building2 className={`w-5 h-5 ${isActive ? 'text-teal-600' : 'text-gray-400'}`} />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className={`font-semibold ${isActive ? 'text-teal-900' : 'text-gray-900'}`}>
                    {company.companyName}
                  </h3>
                  {/* Default Company Indicator - Clickable to set as default */}
                  {(company.isPrimaryCompany || company.joinedVia === 'signup') && onSetDefaultCompany && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation() // Don't trigger container selection
                        if (!company.isPrimaryCompany) {
                          onSetDefaultCompany(company.companyId)
                        }
                      }}
                      className={`p-1 rounded hover:bg-gray-100 transition-colors ${
                        company.isPrimaryCompany ? 'cursor-default' : 'cursor-pointer'
                      }`}
                      title={company.isPrimaryCompany ? 'Default Company' : company.joinedVia === 'signup' ? 'Your Company - Click to set as default' : 'Click to set as default'}
                      disabled={company.isPrimaryCompany}
                    >
                      <Star 
                        className={`w-4 h-4 ${company.isPrimaryCompany ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300 hover:text-yellow-400'}`} 
                      />
                    </button>
                  )}
                </div>
                <div className="flex items-center gap-2 mt-1">
                  {/* Relationship Badge */}
                  <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">
                    {company.relationshipType}
                  </span>
                  {/* Role Badge */}
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    isAdmin ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                  }`}>
                    {company.userRole}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Right: Action Icons - AC-1.18.7: Team panel trigger */}
          <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
            {/* User Management Icon - AC-1.18.7 */}
            {/* Team Management button - only show for Company Admin and Company User (not Company Viewer) */}
            {(company.userRole === 'Company Admin' || company.userRole === 'Company User') && (
              <button
                onClick={() => onOpenTeamPanel(company.companyId)}
                className="p-2 rounded hover:bg-gray-100 text-gray-600 hover:text-gray-900 transition-colors"
                aria-label="Team Management"
                title="Team Management"
              >
                <UsersIcon className="w-5 h-5" />
              </button>
            )}

            {/* Settings Icon - Only for admins */}
            {isAdmin && (
              <button
                onClick={() => {/* TODO: Story 1.16 - Company settings */}}
                className="p-2 rounded hover:bg-gray-100 text-gray-600 hover:text-gray-900 transition-colors"
                aria-label="Company Settings"
                title="Company Settings"
              >
                <Settings className="w-5 h-5" />
              </button>
            )}
            
            {/* Event/Form Count Badge */}
            {company.eventCount > 0 && (
              <span className="text-xs bg-teal-100 text-teal-700 px-2 py-1 rounded-full">
                {company.eventCount} event{company.eventCount !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Child Companies - AC-1.18.3: Recursive rendering */}
      {isExpanded && hasChildren && depth < maxDepth && (
        <div className="mt-2">
          {company.childCompanies.map(child => (
            <CompanyContainer
              key={child.companyId}
              company={child}
              isActive={false} // Only top-level selection for MVP
              isExpanded={false} // Children collapsed by default
              onSelect={onSelect}
              onToggleExpand={onToggleExpand}
              onOpenTeamPanel={onOpenTeamPanel}
              onSetDefaultCompany={onSetDefaultCompany}
              onCreateEvent={onCreateEvent}
              onEditEvent={onEditEvent}
              onDeleteEvent={onDeleteEvent}
              onCreateForm={onCreateForm}
              onEditForm={onEditForm}
              onDeleteForm={onDeleteForm}
              onViewForm={onViewForm}
              depth={depth + 1}
              maxDepth={maxDepth}
            />
          ))}
        </div>
      )}

      {/* Events Display - Story 2.4: Show events when expanded */}
      {isExpanded && !hasChildren && company.eventCount > 0 && (
        <div className="ml-4 mt-2 p-4 border-l-2 border-gray-200 space-y-3">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-teal-600" />
              <h4 className="text-sm font-semibold text-gray-700">
                Events ({company.eventCount})
              </h4>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation()
                onCreateEvent?.(company.companyId)
              }}
              disabled={!navigator.onLine}
              title={!navigator.onLine ? 'Event creation requires internet connection (reference data unavailable offline)' : 'Create a new event'}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors flex items-center gap-1 ${
                !navigator.onLine
                  ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                  : 'text-white bg-teal-600 hover:bg-teal-700'
              }`}
            >
              <span>+</span>
              Create Event
            </button>
          </div>
          
          {isLoadingEvents ? (
            <div className="text-sm text-gray-500 py-4">Loading events...</div>
          ) : eventsError ? (
            <div className="text-sm text-red-600 py-4">{eventsError}</div>
          ) : events.length === 0 ? (
            <div className="text-sm text-gray-500 py-4">No events found</div>
          ) : (
            <div className="space-y-2">
              {events.map((event) => {
                const isEventExpanded = expandedEventIds.includes(event.eventId)
                const forms = eventForms[event.eventId] || []
                const isLoadingEventForms = isLoadingForms[event.eventId] || false
                
                // Check if event is shared (owned by another company)
                // We use userRole to determine specific permissions, but for high-level UI adjustments:
                const isShared = event.companyId !== company.companyId
                const ownerName = event.ownerCompany?.companyName
                
                // Permissions
                const canEdit = event.userRole?.has_edit_event ?? !isShared
                const canShare = event.userRole?.has_manage_participants ?? !isShared
                
                return (
                  <div key={event.eventId} className="bg-white rounded-lg border border-gray-200 hover:border-teal-300 hover:shadow-md transition-all">
                    {/* Split Layout: Event Details (Left) | Forms List (Right) */}
                    <div className="flex">
                      {/* Left Side: Event Details */}
                      <div className="flex-1 p-3 border-r border-gray-200">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center gap-2 flex-1">
                            <button
                              onClick={(e) => {
                                e.stopPropagation()
                                handleToggleEventExpand(event.eventId)
                              }}
                              className="text-gray-400 hover:text-gray-600 p-0.5 rounded"
                              aria-label={isEventExpanded ? 'Collapse forms' : 'Expand forms'}
                            >
                              {isEventExpanded ? (
                                <ChevronDown className="w-4 h-4" />
                              ) : (
                                <ChevronRight className="w-4 h-4" />
                              )}
                            </button>
                            <div>
                                <h5 className="text-sm font-semibold text-gray-900 line-clamp-2">
                                  {event.name}
                                </h5>
                                {isShared && ownerName && (
                                    <span className="text-xs text-gray-500 font-normal block">
                                        (Shared by: {ownerName})
                                    </span>
                                )}
                            </div>
                            {event.eventStatus && (
                              <span
                                className="text-xs px-2 py-1 rounded-full flex-shrink-0"
                                style={{
                                  backgroundColor: event.eventStatus.statusColor 
                                    ? `${event.eventStatus.statusColor}20` 
                                    : '#f3f4f620',
                                  color: event.eventStatus.statusColor || '#6b7280'
                                }}
                              >
                                {event.eventStatus.statusName}
                              </span>
                            )}
                            {/* Form Count Badge - Show when collapsed */}
                            {!isEventExpanded && (
                              <span className="text-xs bg-teal-100 text-teal-700 px-2 py-1 rounded-full flex-shrink-0">
                                {forms.length} {forms.length === 1 ? 'form' : 'forms'}
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-1 flex-shrink-0">
                            {/* Action Icons - Edit, Share, Delete */}
                            {canEdit && (
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation()
                                    onEditEvent?.(event)
                                  }}
                                  className="p-1 text-teal-600 hover:text-teal-700 hover:bg-teal-50 rounded transition-colors"
                                  title="Edit event"
                                >
                                  <Edit2 className="w-3.5 h-3.5" />
                                </button>
                            )}
                            {/* Share Button - Story 2.10: Only for admins or event owners */}
                            {canShare && (
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation()
                                    setEventToShare(event)
                                    setShowShareModal(true)
                                  }}
                                  className="p-1 text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded transition-colors"
                                  title="Share event with agency"
                                >
                                  <Share2 className="w-3.5 h-3.5" />
                                </button>
                            )}
                            <button
                              onClick={(e) => {
                                e.stopPropagation()
                                onDeleteEvent?.(event)
                              }}
                              className={`p-1 ${isShared ? 'text-orange-600 hover:text-orange-700 hover:bg-orange-50' : 'text-red-600 hover:text-red-700 hover:bg-red-50'} rounded transition-colors`}
                              title={isShared ? "Leave Event" : "Delete event"}
                            >
                              {isShared ? <LogOut className="w-3.5 h-3.5" /> : <Trash2 className="w-3.5 h-3.5" />}
                            </button>
                          </div>
                        </div>
                      
                        {/* Event Type */}
                        {event.eventType && (
                          <div className="flex items-center gap-1 text-xs text-gray-600 mb-1">
                            <Tag className="w-3 h-3 text-teal-600" />
                            <span>{event.eventType.typeName}</span>
                          </div>
                        )}
                        
                        {/* Date/Time */}
                        {event.startDateTime && (
                          <div className="flex items-center gap-1 text-xs text-gray-600 mb-1">
                            <Calendar className="w-3 h-3 text-teal-600" />
                            <div>
                              <span className="font-medium">
                                {new Date(event.startDateTime).toLocaleDateString('en-AU', {
                                  month: 'short',
                                  day: 'numeric',
                                  year: 'numeric'
                                })}
                              </span>
                              <span className="ml-1">
                                {new Date(event.startDateTime).toLocaleTimeString('en-AU', {
                                  hour: '2-digit',
                                  minute: '2-digit'
                                })}
                              </span>
                              {event.endDateTime && (
                                <span className="text-gray-500 ml-1">
                                  - {new Date(event.endDateTime).toLocaleDateString('en-AU', {
                                    month: 'short',
                                    day: 'numeric',
                                    year: new Date(event.endDateTime).getFullYear() !== new Date(event.startDateTime).getFullYear() ? 'numeric' : undefined
                                  })}
                                  {new Date(event.endDateTime).toLocaleTimeString('en-AU', {
                                    hour: '2-digit',
                                    minute: '2-digit'
                                  })}
                                </span>
                              )}
                            </div>
                          </div>
                        )}
                        
                        {/* Location */}
                        {(event.venueName || event.city || event.state) && (
                          <div className="flex items-start gap-1 text-xs text-gray-600 mb-1">
                            <MapPin className="w-3 h-3 text-teal-600 mt-0.5 flex-shrink-0" />
                            <div className="line-clamp-2">
                              {[event.venueName, event.city, event.state].filter(Boolean).join(', ')}
                            </div>
                          </div>
                        )}
                        
                        {/* Public/Private Indicator */}
                        <div className="flex items-center gap-2 mb-1">
                          {event.isPublic !== undefined && (
                            <div className="flex items-center gap-1 text-xs">
                              <Globe className={`w-3 h-3 ${event.isPublic ? 'text-blue-600' : 'text-gray-400'}`} />
                              <span className={event.isPublic ? 'text-blue-600 font-medium' : 'text-gray-500'}>
                                {event.isPublic ? 'Public' : 'Private'}
                              </span>
                            </div>
                          )}
                          {event.isRecurring && (
                            <div className="flex items-center gap-1 text-xs text-gray-600">
                              <Clock className="w-3 h-3" />
                              <span>Recurring</span>
                            </div>
                          )}
                        </div>
                        
                        {/* Tags */}
                        {event.tags && (
                          <div className="flex items-center gap-1 text-xs text-gray-500 mb-1">
                            <Tag className="w-3 h-3" />
                            <span className="line-clamp-1">{event.tags}</span>
                          </div>
                        )}
                        
                        {/* Expected Attendees */}
                        {event.expectedAttendees && (
                          <div className="text-xs text-gray-600 mb-1">
                            Expected: {event.expectedAttendees.toLocaleString()} attendees
                          </div>
                        )}
                        
                        {/* Short Description */}
                        {event.shortDescription && (
                          <p className="text-xs text-gray-600 mt-2 line-clamp-2">
                            {event.shortDescription}
                          </p>
                        )}
                        
                      </div>

                      {/* Right Side: Forms List - Only show when expanded */}
                      {isEventExpanded && (
                        <div className="flex-1 p-3 bg-gray-50 max-h-[400px] overflow-y-auto">
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center gap-2">
                              <FileText className="w-3 h-3 text-teal-600" />
                              <h6 className="text-xs font-semibold text-gray-700">
                                Forms ({forms.length})
                              </h6>
                            </div>
                            <button
                              onClick={(e) => {
                                e.stopPropagation()
                                onCreateForm?.(event.eventId)
                              }}
                              className="px-2 py-1 text-xs font-medium text-white bg-teal-600 hover:bg-teal-700 rounded transition-colors flex items-center gap-1"
                              title="Create form for this event"
                            >
                              <span>+</span>
                              Form
                            </button>
                          </div>
                          
                          {isLoadingEventForms ? (
                            <div className="text-xs text-gray-500 py-4 text-center">Loading forms...</div>
                          ) : forms.length === 0 ? (
                            <div className="text-xs text-gray-500 py-4 text-center">
                              No forms yet. Create your first form for this event.
                            </div>
                          ) : (
                            <div className="space-y-2">
                              {forms.map((form) => (
                                <div
                                  key={form.formId}
                                  className="bg-white rounded border border-gray-200 p-2 hover:border-teal-300 hover:shadow-sm transition-all"
                                >
                                  <div className="flex items-start gap-2">
                                    {/* Thumbnail */}
                                    <div className="flex-shrink-0 w-16 h-16 bg-gray-100 rounded border border-gray-200 overflow-hidden">
                                      {form.formThumbnailUrl ? (
                                        <img 
                                          src={form.formThumbnailUrl} 
                                          alt={form.formName}
                                          className="w-full h-full object-cover"
                                          onError={(e) => {
                                            (e.target as HTMLImageElement).style.display = 'none'
                                          }}
                                        />
                                      ) : (
                                        <div className="w-full h-full flex items-center justify-center">
                                          <FileText className="w-6 h-6 text-gray-400" />
                                        </div>
                                      )}
                                    </div>
                                    
                                    {/* Form Details */}
                                    <div className="flex-1 min-w-0">
                                      <div className="flex items-start justify-between gap-2 mb-1">
                                        <div className="flex-1 min-w-0">
                                          <h6 className="text-xs font-semibold text-gray-900 line-clamp-1">
                                            {form.formName}
                                          </h6>
                                          {form.formDescription && (
                                            <p className="text-xs text-gray-600 line-clamp-1 mt-0.5">
                                              {form.formDescription}
                                            </p>
                                          )}
                                        </div>
                                        
                                        {/* Action Icons - Story 2.9: Conditionally show based on access level */}
                                        <div className="flex items-center gap-1 flex-shrink-0">
                                          {(() => {
                                            const accessLevel = formAccessLevels[form.formId]?.toUpperCase()
                                            const hasView = accessLevel && ['VIEW', 'SUBMIT', 'ANALYZE', 'EDIT', 'MANAGE'].includes(accessLevel)
                                            const hasEdit = accessLevel && ['EDIT', 'MANAGE'].includes(accessLevel)
                                            const hasManage = accessLevel === 'MANAGE'
                                            
                                            return (
                                              <>
                                                {/* View button - shown for VIEW, SUBMIT, ANALYZE, EDIT, or MANAGE access */}
                                                {hasView && (
                                                  <button
                                                    onClick={(e) => {
                                                      e.stopPropagation()
                                                      onViewForm?.(form)
                                                    }}
                                                    className="p-1 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded transition-colors"
                                                    title="View form"
                                                  >
                                                    <Eye className="w-3.5 h-3.5" />
                                                  </button>
                                                )}
                                                
                                                {/* Edit button - shown for EDIT or MANAGE access */}
                                                {hasEdit && (
                                                  <button
                                                    onClick={(e) => {
                                                      e.stopPropagation()
                                                      onEditForm?.(form)
                                                    }}
                                                    className="p-1 text-teal-600 hover:text-teal-700 hover:bg-teal-50 rounded transition-colors"
                                                    title="Edit form"
                                                  >
                                                    <Edit2 className="w-3.5 h-3.5" />
                                                  </button>
                                                )}
                                                
                                                {/* Delete button - only shown for MANAGE access */}
                                                {hasManage && (
                                                  <button
                                                    onClick={(e) => {
                                                      e.stopPropagation()
                                                      onDeleteForm?.(form)
                                                    }}
                                                    className="p-1 text-red-600 hover:text-red-700 hover:bg-red-50 rounded transition-colors"
                                                    title="Delete form"
                                                  >
                                                    <Trash2 className="w-3.5 h-3.5" />
                                                  </button>
                                                )}
                                              </>
                                            )
                                          })()}
                                        </div>
                                      </div>
                                      
                                      {/* Status Icons */}
                                      <div className="flex items-center gap-2 mt-1.5">
                                        {/* Form Status */}
                                        {form.formStatus && (
                                          <div 
                                            className="flex items-center gap-1 text-xs px-1.5 py-0.5 rounded"
                                            style={{
                                              backgroundColor: form.formStatus.statusColor 
                                                ? `${form.formStatus.statusColor}20` 
                                                : '#f3f4f620',
                                              color: form.formStatus.statusColor || '#6b7280'
                                            }}
                                            title={form.formStatus.statusDescription || form.formStatus.statusName}
                                          >
                                            {getFormStatusIcon(form.formStatus.statusCode)}
                                            <span className="font-medium">{form.formStatus.statusName}</span>
                                          </div>
                                        )}
                                        
                                        {/* Approval Status */}
                                        {form.formApprovalStatus && form.formApprovalStatus.approvalStatusCode !== 'NO_APPROVAL' && (
                                          <div 
                                            className="flex items-center gap-1 text-xs px-1.5 py-0.5 rounded"
                                            style={{
                                              backgroundColor: form.formApprovalStatus.approvalStatusCode === 'PENDING' 
                                                ? '#fef3c720'
                                                : form.formApprovalStatus.approvalStatusCode === 'APPROVED'
                                                ? '#d1fae520'
                                                : form.formApprovalStatus.approvalStatusCode === 'REJECTED'
                                                ? '#fee2e220'
                                                : '#f3f4f620',
                                              color: form.formApprovalStatus.approvalStatusCode === 'PENDING' 
                                                ? '#d97706'
                                                : form.formApprovalStatus.approvalStatusCode === 'APPROVED'
                                                ? '#059669'
                                                : form.formApprovalStatus.approvalStatusCode === 'REJECTED'
                                                ? '#dc2626'
                                                : '#6b7280'
                                            }}
                                            title={form.formApprovalStatus.approvalStatusDescription || form.formApprovalStatus.approvalStatusName}
                                          >
                                            {getApprovalStatusIcon(form.formApprovalStatus.approvalStatusCode)}
                                            <span className="font-medium">{form.formApprovalStatus.approvalStatusName}</span>
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}

      {/* Empty State for company with no events - AC-1.18.9 */}
      {isExpanded && !hasChildren && company.eventCount === 0 && (
        <div className="ml-4 mt-2 p-4 border-l-2 border-gray-200">
          <button
            onClick={(e) => {
              e.stopPropagation()
              onCreateEvent?.(company.companyId)
            }}
            disabled={!navigator.onLine}
            title={!navigator.onLine ? 'Event creation requires internet connection (reference data unavailable offline)' : 'Create your first event'}
            className={`text-sm font-medium transition-colors flex items-center gap-1 ${
              !navigator.onLine
                ? 'text-gray-400 cursor-not-allowed'
                : 'text-teal-600 hover:text-teal-700 hover:underline cursor-pointer'
            }`}
          >
            <span>📭 No events yet. Create your first event!</span>
          </button>
        </div>
      )}

      {/* Share Event Modal - Story 2.10 */}
      {eventToShare && (
        <ShareEventModal
          isOpen={showShareModal}
          eventId={eventToShare.eventId}
          eventName={eventToShare.name}
          onClose={() => {
            setShowShareModal(false)
            setEventToShare(null)
          }}
        />
      )}
    </div>
  )
}




