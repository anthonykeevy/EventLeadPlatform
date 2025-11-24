import React, { useState, useEffect, useRef } from 'react'
import { Search, Check, X, Calendar } from 'lucide-react'
import { Event } from '../types/events.types'
import { getEvents } from '../api/eventsApi'
import { useToastNotifications } from '../../ux'

interface EventSelectorProps {
  selectedEventId: number | null
  onSelect: (event: Event | null) => void
  label?: string
  placeholder?: string
  disabled?: boolean
  required?: boolean
}

export function EventSelector({
  selectedEventId,
  onSelect,
  label = 'Event',
  placeholder = 'Select an event...',
  disabled = false,
  required = false
}: EventSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [events, setEvents] = useState<Event[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  
  const wrapperRef = useRef<HTMLDivElement>(null)
  const toast = useToastNotifications()

  // Load initial selected event details if ID provided
  useEffect(() => {
    if (selectedEventId && (!selectedEvent || selectedEvent.eventId !== selectedEventId)) {
      // If we have the event in our list, use it
      const eventInList = events.find(e => e.eventId === selectedEventId)
      if (eventInList) {
        setSelectedEvent(eventInList)
      } else {
        // Otherwise fetch it (search by ID isn't directly supported by search endpoint, 
        // but we can load initial page and see or rely on search)
        // For now, we'll rely on the user searching or the list being populated.
        // Ideally we'd have a getEvent(id) here, but let's just load the list.
        loadEvents()
      }
    } else if (!selectedEventId) {
      setSelectedEvent(null)
    }
  }, [selectedEventId, events])

  const loadEvents = async (search: string = '') => {
    setIsLoading(true)
    try {
      // Fetch active events
      const response = await getEvents(1, 20, { search })
      setEvents(response.events)
    } catch (error) {
      console.error('Failed to load events:', error)
      toast.error('Failed to load events', 'Error')
    } finally {
      setIsLoading(false)
    }
  }

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Load events when dropdown opens
  useEffect(() => {
    if (isOpen && events.length === 0) {
      loadEvents()
    }
  }, [isOpen])

  // Handle search debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      if (isOpen) {
        loadEvents(searchTerm)
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [searchTerm, isOpen])

  const handleSelect = (event: Event) => {
    setSelectedEvent(event)
    onSelect(event)
    setIsOpen(false)
    setSearchTerm('')
  }

  const handleClear = (e: React.MouseEvent) => {
    e.stopPropagation()
    setSelectedEvent(null)
    onSelect(null)
  }

  return (
    <div className="relative" ref={wrapperRef}>
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      
      <div
        className={`
          relative w-full cursor-pointer bg-white border rounded-md shadow-sm pl-3 pr-10 py-2 text-left 
          focus:outline-none focus:ring-1 focus:ring-teal-500 focus:border-teal-500 sm:text-sm
          ${disabled ? 'bg-gray-100 cursor-not-allowed border-gray-300' : 'border-gray-300'}
        `}
        onClick={() => !disabled && setIsOpen(!isOpen)}
      >
        <span className={`block truncate ${!selectedEvent ? 'text-gray-500' : 'text-gray-900'}`}>
          {selectedEvent ? selectedEvent.name : placeholder}
        </span>
        
        <div className="absolute inset-y-0 right-0 flex items-center pr-2">
          {selectedEvent && !disabled && (
            <button
              onClick={handleClear}
              className="p-1 hover:bg-gray-100 rounded-full text-gray-400 hover:text-gray-600 mr-1"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          <Search className="h-4 w-4 text-gray-400" />
        </div>
      </div>

      {isOpen && !disabled && (
        <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
          <div className="sticky top-0 bg-white p-2 border-b border-gray-100">
            <input
              type="text"
              className="w-full border-gray-300 rounded-md text-sm focus:ring-teal-500 focus:border-teal-500"
              placeholder="Search events..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onClick={(e) => e.stopPropagation()}
              autoFocus
            />
          </div>

          {isLoading ? (
            <div className="py-4 text-center text-gray-500">Loading...</div>
          ) : events.length === 0 ? (
            <div className="py-4 text-center text-gray-500">No events found</div>
          ) : (
            <ul className="divide-y divide-gray-100">
              {events.map((event) => (
                <li
                  key={event.eventId}
                  className={`
                    cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-teal-50
                    ${selectedEventId === event.eventId ? 'bg-teal-50 text-teal-900' : 'text-gray-900'}
                  `}
                  onClick={() => handleSelect(event)}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium block truncate">
                      {event.name}
                    </span>
                    {event.eventStatus && (
                      <span 
                        className="text-xs px-2 py-0.5 rounded-full ml-2 whitespace-nowrap"
                        style={{ 
                          backgroundColor: `${event.eventStatus.statusColor}20`, 
                          color: event.eventStatus.statusColor || '#666' 
                        }}
                      >
                        {event.eventStatus.statusName}
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-gray-500 flex items-center mt-0.5">
                    <Calendar className="w-3 h-3 mr-1" />
                    {new Date(event.startDateTime).toLocaleDateString()}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}

