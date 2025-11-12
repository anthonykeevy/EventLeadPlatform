/**
 * Company Container Component - Story 1.18
 * AC-1.18.3: Recursive company container
 * AC-1.18.4: Company selection and switching
 * Story 2.4: Event display when expanded
 */

import React, { useState, useEffect } from 'react'
import { Building2, Users as UsersIcon, Settings, ChevronDown, ChevronRight, Calendar, MapPin, Tag, Globe, Clock } from 'lucide-react'
import type { Company } from '../types/dashboard.types'
import { getEvents } from '../../events/api/eventsApi'
import type { Event } from '../../events/types/events.types'

interface CompanyContainerProps {
  company: Company
  isActive: boolean
  isExpanded: boolean
  onSelect: (companyId: number) => void
  onToggleExpand: (companyId: number) => void
  onOpenTeamPanel: (companyId: number) => void
  onCreateEvent?: (companyId: number) => void
  onEditEvent?: (event: Event) => void
  onDeleteEvent?: (event: Event) => void
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
  onCreateEvent,
  onEditEvent,
  onDeleteEvent,
  depth = 0,
  maxDepth = 5
}: CompanyContainerProps) {
  const hasChildren = company.childCompanies && company.childCompanies.length > 0
  const isAdmin = company.userRole === 'Company Admin'
  
  // Event state management - Story 2.4
  const [events, setEvents] = useState<Event[]>([])
  const [isLoadingEvents, setIsLoadingEvents] = useState(false)
  const [eventsError, setEventsError] = useState<string | null>(null)
  
  // Fetch events when expanded and company has events - Story 2.4
  useEffect(() => {
    if (isExpanded && !hasChildren && company.eventCount > 0) {
      loadEvents()
    } else {
      // Clear events when collapsed
      setEvents([])
      setEventsError(null)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isExpanded, company.eventCount, company.childCompanies?.length])

  // Listen for offline queue processing completion and refresh events
  useEffect(() => {
    const handleQueueProcessed = () => {
      // Only refresh if this company is expanded and active
      if (isExpanded && isActive && !hasChildren) {
        console.log('🔄 Offline queue processed - refreshing events')
        loadEvents()
      }
    }

    window.addEventListener('offlineQueueProcessed', handleQueueProcessed)
    return () => {
      window.removeEventListener('offlineQueueProcessed', handleQueueProcessed)
    }
  }, [isExpanded, isActive, hasChildren]) // eslint-disable-line react-hooks/exhaustive-deps
  
  const loadEvents = async () => {
    setIsLoadingEvents(true)
    setEventsError(null)
    try {
      const response = await getEvents(1, 50) // Load up to 50 events
      setEvents(response.events)
    } catch (error) {
      console.error('Failed to load events:', error)
      setEventsError('Failed to load events')
      setEvents([])
    } finally {
      setIsLoadingEvents(false)
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
            {/* Expand/Collapse Toggle - AC-1.18.10 */}
            {hasChildren && (
              <button
                onClick={(e) => {
                  e.stopPropagation() // Don't trigger container selection
                  onToggleExpand(company.companyId)
                }}
                className="text-gray-500 hover:text-gray-700 p-1 rounded hover:bg-gray-100"
                aria-label={isExpanded ? 'Collapse' : 'Expand'}
              >
                {isExpanded ? (
                  <ChevronDown className="w-5 h-5" />
                ) : (
                  <ChevronRight className="w-5 h-5" />
                )}
              </button>
            )}
            
            {/* Company Icon and Name */}
            <div className="flex items-center gap-2 flex-1">
              <Building2 className={`w-5 h-5 ${isActive ? 'text-teal-600' : 'text-gray-400'}`} />
              <div>
                <h3 className={`font-semibold ${isActive ? 'text-teal-900' : 'text-gray-900'}`}>
                  {company.companyName}
                </h3>
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
            <button
              onClick={() => onOpenTeamPanel(company.companyId)}
              className="p-2 rounded hover:bg-gray-100 text-gray-600 hover:text-gray-900 transition-colors"
              aria-label="Team Management"
              title="Team Management"
            >
              <UsersIcon className="w-5 h-5" />
            </button>

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
              onCreateEvent={onCreateEvent}
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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {events.map((event) => (
                <div
                  key={event.eventId}
                  className="bg-white rounded-lg border border-gray-200 p-3 hover:border-teal-300 hover:shadow-md transition-all cursor-pointer"
                  onClick={(e) => {
                    // Only open edit if clicking on the card itself (not buttons)
                    if ((e.target as HTMLElement).closest('button')) return
                    onEditEvent?.(event)
                  }}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h5 className="text-sm font-semibold text-gray-900 flex-1 pr-2 line-clamp-2">
                      {event.name}
                    </h5>
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
                  
                  <div className="flex items-center gap-2 mt-3 pt-2 border-t border-gray-100">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        onEditEvent?.(event)
                      }}
                      className="text-xs text-teal-600 hover:text-teal-700 font-medium"
                    >
                      Edit
                    </button>
                    <span className="text-gray-300">|</span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        onDeleteEvent?.(event)
                      }}
                      className="text-xs text-red-600 hover:text-red-700 font-medium"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
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
    </div>
  )
}




