/**
 * Event Management Tab Component
 * Story 2.6: Admin Public Event Review Workflow
 */
import React, { useState, useMemo, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ColumnDef, type Row } from '@tanstack/react-table'
import { DataTable, ColumnFilterConfig } from '../../../components/common/DataTable'
import { adminDashboardApi, AdminEvent } from '../api/adminDashboardApi'
import { adminReviewApi, type AdminEventUpdateRequest } from '../api/adminReviewApi'
import { EventReviewModal } from './EventReviewModal'
import { CheckCircle, XCircle, Clock, Eye, Edit2, Check, X } from 'lucide-react'
import { useToastNotifications } from '../../../features/ux'
import { getEventTypes, getEventStatuses } from '../../events/api/eventsApi'
import { getIndustries } from '../../profile/api/usersApi'
import { useCountries } from '../../validation/hooks/useCountries'
import type { EventType, EventStatus } from '../../events/types/events.types'
import type { IndustryOption } from '../../profile/api/usersApi'

interface EventManagementTabProps {
  dateFilter?: 'all' | 'past' | 'current' | 'future'
  onDateFilterChange?: (filter: 'all' | 'past' | 'current' | 'future') => void
}

export const EventManagementTab: React.FC<EventManagementTabProps> = ({
  dateFilter = 'all',
  onDateFilterChange,
}) => {
  const [selectedEvent, setSelectedEvent] = useState<AdminEvent | null>(null)
  const [showReviewModal, setShowReviewModal] = useState(false)
  const [editingCell, setEditingCell] = useState<{ rowId: string; columnId: string } | null>(null)
  const [editingValue, setEditingValue] = useState<string | number | null>(null)
  const [filters, setFilters] = useState<{
    event_status_id?: number
    event_type_id?: number
    public_review_status?: string
  }>({})
  const [pagination, setPagination] = useState<{ page: number; pageSize: number }>({
    page: 1,
    pageSize: 10,
  })

  const queryClient = useQueryClient()
  const toast = useToastNotifications()

  // Fetch reference data for dropdowns
  const { data: eventTypes = [] } = useQuery<EventType[]>({
    queryKey: ['eventTypes'],
    queryFn: getEventTypes,
  })

  const { data: eventStatuses = [] } = useQuery<EventStatus[]>({
    queryKey: ['eventStatuses'],
    queryFn: getEventStatuses,
  })

  // Column filter configs for table headers (must be after eventTypes and eventStatuses are defined)
  const columnFilterConfigs = useMemo<ColumnFilterConfig[]>(() => {
    return [
      {
        columnId: 'event_type_id',
        type: 'select',
        options: eventTypes.map((type) => ({ value: type.eventTypeId, label: type.typeName })),
        value: filters.event_type_id || null,
      },
      {
        columnId: 'event_status_id',
        type: 'select',
        options: eventStatuses.map((status) => ({ value: status.eventStatusId, label: status.statusName })),
        value: filters.event_status_id || null,
      },
      {
        columnId: 'public_review_status',
        type: 'select',
        options: [
          { value: 'PENDING', label: 'Pending' },
          { value: 'APPROVED', label: 'Approved' },
          { value: 'REJECTED', label: 'Rejected' },
        ],
        value: filters.public_review_status || null,
      },
    ]
  }, [eventTypes, eventStatuses, filters])

  const { data: industries = [] } = useQuery<IndustryOption[]>({
    queryKey: ['industries'],
    queryFn: getIndustries,
  })

  const { data: companies = [] } = useQuery({
    queryKey: ['admin', 'companies'],
    queryFn: adminDashboardApi.getCompanies,
  })

  // Fetch countries for country dropdown
  const { countries } = useCountries()

  // Fetch events with filters
  const { data: eventsData, isLoading } = useQuery({
    queryKey: ['admin', 'events', filters, dateFilter, pagination.page, pagination.pageSize],
    queryFn: () =>
      adminDashboardApi.getEvents({
        ...filters,
        date_filter: dateFilter,
        page: pagination.page,
        page_size: pagination.pageSize,
      }),
  })

  // Mutations for approve/reject
  const approveMutation = useMutation({
    mutationFn: ({ eventId, comment }: { eventId: number; comment?: string }) =>
      adminReviewApi.approveEvent(eventId, { comment }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'events'] })
      queryClient.invalidateQueries({ queryKey: ['admin', 'kpis'] })
      setShowReviewModal(false)
      setSelectedEvent(null)
      toast.success('Event approved successfully')
    },
    onError: (error: unknown) => {
      toast.error(error instanceof Error ? error.message : 'Failed to approve event')
    },
  })

  const rejectMutation = useMutation({
    mutationFn: ({ eventId, comment }: { eventId: number; comment: string }) =>
      adminReviewApi.rejectEvent(eventId, { comment }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'events'] })
      queryClient.invalidateQueries({ queryKey: ['admin', 'kpis'] })
      setShowReviewModal(false)
      setSelectedEvent(null)
      toast.success('Event rejected successfully')
    },
    onError: (error: unknown) => {
      toast.error(error instanceof Error ? error.message : 'Failed to reject event')
    },
  })

  // Mutation for updating events (inline editing) - uses admin endpoint
  const updateEventMutation = useMutation({
    mutationFn: ({ eventId, updates }: { eventId: number; updates: Partial<AdminEventUpdateRequest> }) => {
      // Transform camelCase to snake_case for admin API (if needed)
      const u = updates as Record<string, unknown>
      const adminRequest: Record<string, unknown> = { ...updates }

      // Convert camelCase fields to snake_case if present
      if (u.eventTypeId !== undefined) {
        adminRequest.event_type_id = u.eventTypeId
        delete adminRequest.eventTypeId
      }
      if (u.eventStatusId !== undefined) {
        adminRequest.event_status_id = u.eventStatusId
        delete adminRequest.eventStatusId
      }
      if (u.industryId !== undefined) {
        adminRequest.industry_id = u.industryId
        delete adminRequest.industryId
      }
      if (u.organizerCompanyId !== undefined) {
        adminRequest.organizer_company_id = u.organizerCompanyId
        delete adminRequest.organizerCompanyId
      }
      if (u.startDatetime !== undefined) {
        adminRequest.start_datetime = u.startDatetime
        delete adminRequest.startDatetime
      }
      if (u.endDatetime !== undefined) {
        adminRequest.end_datetime = u.endDatetime
        delete adminRequest.endDatetime
      }

      return adminReviewApi.updateEvent(eventId, adminRequest as AdminEventUpdateRequest)
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'events'] })
      setEditingCell(null)
      setEditingValue(null)
      // Clear expanded row data for the updated event
      setExpandedRowData((prev) => {
        const newData = { ...prev }
        delete newData[`row-${variables.eventId}`]
        return newData
      })
      toast.success('Event updated successfully')
    },
    onError: (error: unknown) => {
      toast.error(error instanceof Error ? error.message : 'Failed to update event')
      setEditingCell(null)
      setEditingValue(null)
    },
  })

  // Helper function to handle cell edit
  const handleCellEdit = useCallback(
    (rowId: string, columnId: string, currentValue: string | number) => {
      setEditingCell({ rowId, columnId })
      setEditingValue(currentValue)
    },
    []
  )

  // Helper function to save cell edit
  const handleCellSave = useCallback(
    (event: AdminEvent, columnId: string, newValue: string | number | null) => {
      if (newValue === null || newValue === '') {
        setEditingCell(null)
        setEditingValue(null)
        return
      }

      const updates: Partial<AdminEventUpdateRequest> = {}

      switch (columnId) {
        case 'event_type_id':
          updates.eventTypeId = Number(newValue)
          break
        case 'event_status_id':
          updates.eventStatusId = Number(newValue)
          break
        case 'industry_id':
          updates.industryId = newValue ? Number(newValue) : null
          break
        case 'company_id':
          updates.organizerCompanyId = Number(newValue)
          break
        default:
          setEditingCell(null)
          setEditingValue(null)
          return
      }

      updateEventMutation.mutate({ eventId: event.event_id, updates })
    },
    [updateEventMutation]
  )

  // Helper function to cancel cell edit
  const handleCellCancel = useCallback(() => {
    setEditingCell(null)
    setEditingValue(null)
  }, [])

  // Helper function to calculate priority based on time since submission
  const getPriorityInfo = useCallback((event: AdminEvent) => {
    if (event.public_review_status !== 'PENDING') {
      return null // Only show priority for pending events
    }

    // Database stores dates in UTC, so we need to parse and compare in UTC
    // Parse the date string - FastAPI/Pydantic typically sends ISO 8601 format
    // Ensure we treat the database UTC time correctly regardless of format
    const createdDateStr = event.created_date
    let submissionDate: Date
    
    // Check if date string has timezone info
    if (createdDateStr.includes('Z') || createdDateStr.match(/[+-]\d{2}:\d{2}$/)) {
      // Date string has timezone info (UTC 'Z' or offset like '+11:00'), parse as-is
      submissionDate = new Date(createdDateStr)
    } else {
      // Date string has no timezone info - assume it's UTC from database
      // Add 'Z' to explicitly mark it as UTC
      submissionDate = new Date(createdDateStr + 'Z')
    }
    
    // Get current time and submission time both as UTC timestamps (milliseconds since epoch)
    // Date.now() and getTime() both return UTC milliseconds, so this comparison is timezone-independent
    const now = Date.now() // Current UTC time in milliseconds
    const submissionTime = submissionDate.getTime() // Event creation UTC time in milliseconds
    
    // Calculate difference in milliseconds, then convert to hours
    // Both are UTC timestamps, so this gives us the actual elapsed time regardless of user's timezone
    const hoursSinceSubmission = (now - submissionTime) / (1000 * 60 * 60)

    let priority: 'low' | 'medium' | 'high' | 'urgent'
    let color: string
    let label: string

    if (hoursSinceSubmission < 24) {
      priority = 'low'
      color = 'bg-green-100 text-green-800'
      label = 'New'
    } else if (hoursSinceSubmission < 48) {
      priority = 'medium'
      color = 'bg-yellow-100 text-yellow-800'
      label = '24h+'
    } else if (hoursSinceSubmission < 72) {
      priority = 'high'
      color = 'bg-orange-100 text-orange-800'
      label = '48h+'
    } else {
      priority = 'urgent'
      color = 'bg-red-100 text-red-800'
      label = '72h+'
    }

    // Format time display with "ago" suffix
    const days = Math.floor(hoursSinceSubmission / 24)
    const hours = Math.floor(hoursSinceSubmission % 24)
    const minutes = Math.floor((hoursSinceSubmission % 1) * 60)
    let timeDisplay = ''
    
    if (days > 0) {
      timeDisplay = `${days}d ${hours}h ago`
    } else if (hours > 0) {
      timeDisplay = `${hours}h ${minutes}m ago`
    } else if (minutes > 0) {
      timeDisplay = `${minutes}m ago`
    } else {
      timeDisplay = 'just now'
    }

    return {
      priority,
      color,
      label,
      hoursSinceSubmission,
      timeDisplay,
    }
  }, [])

  // Editable Dropdown Cell Component
  const EditableDropdownCell: React.FC<{
    row: Row<AdminEvent>
    columnId: string
    currentValue: string | number
    currentDisplay: string
    options: Array<{ id: number; name: string }>
    isEditing: boolean
    editingValue: string | number | null
    onEdit: () => void
    onSave: (value: number | null) => void
    onCancel: () => void
    onValueChange: (value: number | null) => void
    isLoading?: boolean
  }> = ({
    row: _row,
    columnId: _columnId,
    currentValue: _currentValue,
    currentDisplay,
    options,
    isEditing,
    editingValue,
    onEdit,
    onSave,
    onCancel,
    onValueChange,
    isLoading = false,
  }) => {
    if (isEditing) {
      return (
        <div className="flex items-center gap-1">
          <select
            value={editingValue as number}
            onChange={(e) => onValueChange(e.target.value ? Number(e.target.value) : null)}
            className="text-sm border border-teal-500 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-teal-500"
            autoFocus
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                onSave(editingValue as number | null)
              } else if (e.key === 'Escape') {
                onCancel()
              }
            }}
          >
            <option value="">-- Select --</option>
            {options.map((option) => (
              <option key={option.id} value={option.id}>
                {option.name}
              </option>
            ))}
          </select>
          <button
            onClick={() => onSave(editingValue as number | null)}
            disabled={isLoading}
            className="p-1 text-green-600 hover:text-green-700 disabled:opacity-50"
            title="Save"
          >
            <Check className="w-4 h-4" />
          </button>
          <button
            onClick={onCancel}
            disabled={isLoading}
            className="p-1 text-red-600 hover:text-red-700 disabled:opacity-50"
            title="Cancel"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )
    }

    return (
      <div
        className="flex items-center gap-1 group cursor-pointer hover:bg-gray-50 rounded px-1 py-0.5 -mx-1 -my-0.5"
        onClick={onEdit}
        title="Click to edit"
      >
        <span className="text-sm text-gray-600">{currentDisplay}</span>
        <Edit2 className="w-3 h-3 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
    )
  }

  // Table columns
  const columns = useMemo<ColumnDef<AdminEvent>[]>(
    () => [
      {
        accessorKey: 'name',
        header: 'Event Name',
        cell: ({ row }) => {
          const event = row.original
          const priorityInfo = getPriorityInfo(event)
          const isHighPriority = priorityInfo && (priorityInfo.priority === 'high' || priorityInfo.priority === 'urgent')

          return (
            <div className="flex items-center gap-2">
              {isHighPriority && (
                <span
                  className={`inline-flex items-center px-1.5 py-0.5 rounded text-xs font-semibold ${priorityInfo?.color}`}
                  title={`High priority: ${priorityInfo?.timeDisplay} pending`}
                >
                  !
                </span>
              )}
              <div className={`font-medium ${isHighPriority ? 'text-red-900' : 'text-gray-900'}`}>
                {event.name}
              </div>
            </div>
          )
        },
      },
      {
        accessorKey: 'company_id',
        header: 'Company',
        cell: ({ row }) => {
          const event = row.original
          const isEditing = editingCell?.rowId === row.id && editingCell?.columnId === 'company_id'
          
          return (
            <EditableDropdownCell
              row={row}
              columnId="company_id"
              currentValue={event.company_id}
              currentDisplay={event.company_name}
              options={companies.map((c) => ({ id: c.company_id, name: c.company_name }))}
              isEditing={isEditing}
              editingValue={editingValue}
              onEdit={() => handleCellEdit(row.id, 'company_id', event.company_id)}
              onSave={(value) => handleCellSave(event, 'company_id', value)}
              onCancel={handleCellCancel}
              onValueChange={(value) => setEditingValue(value)}
              isLoading={updateEventMutation.isPending}
            />
          )
        },
      },
      {
        accessorKey: 'event_type_id',
        header: 'Type',
        cell: ({ row }) => {
          const event = row.original
          const isEditing = editingCell?.rowId === row.id && editingCell?.columnId === 'event_type_id'
          
          return (
            <EditableDropdownCell
              row={row}
              columnId="event_type_id"
              currentValue={event.event_type_id}
              currentDisplay={event.event_type_name}
              options={eventTypes.map((t) => ({ id: t.eventTypeId, name: t.typeName }))}
              isEditing={isEditing}
              editingValue={editingValue}
              onEdit={() => handleCellEdit(row.id, 'event_type_id', event.event_type_id)}
              onSave={(value) => handleCellSave(event, 'event_type_id', value)}
              onCancel={handleCellCancel}
              onValueChange={(value) => setEditingValue(value)}
              isLoading={updateEventMutation.isPending}
            />
          )
        },
      },
      {
        accessorKey: 'event_status_id',
        header: 'Status',
        cell: ({ row }) => {
          const event = row.original
          const isEditing = editingCell?.rowId === row.id && editingCell?.columnId === 'event_status_id'
          
          return (
            <EditableDropdownCell
              row={row}
              columnId="event_status_id"
              currentValue={event.event_status_id}
              currentDisplay={event.event_status_name}
              options={eventStatuses.map((s) => ({ id: s.eventStatusId, name: s.statusName }))}
              isEditing={isEditing}
              editingValue={editingValue}
              onEdit={() => handleCellEdit(row.id, 'event_status_id', event.event_status_id)}
              onSave={(value) => handleCellSave(event, 'event_status_id', value)}
              onCancel={handleCellCancel}
              onValueChange={(value) => setEditingValue(value)}
              isLoading={updateEventMutation.isPending}
            />
          )
        },
      },
      {
        accessorKey: 'industry_id',
        header: 'Industry',
        cell: ({ row }) => {
          const event = row.original
          const isEditing = editingCell?.rowId === row.id && editingCell?.columnId === 'industry_id'
          
          return (
            <EditableDropdownCell
              row={row}
              columnId="industry_id"
              currentValue={event.industry_id ?? 0}
              currentDisplay={event.industry_name || '—'}
              options={industries.map((i) => ({ id: i.id, name: i.name }))}
              isEditing={isEditing}
              editingValue={editingValue}
              onEdit={() => handleCellEdit(row.id, 'industry_id', event.industry_id ?? 0)}
              onSave={(value) => handleCellSave(event, 'industry_id', value)}
              onCancel={handleCellCancel}
              onValueChange={(value) => setEditingValue(value)}
              isLoading={updateEventMutation.isPending}
            />
          )
        },
      },
      {
        accessorKey: 'public_review_status',
        header: 'Review Status',
        cell: ({ row }) => {
          const event = row.original
          const status = event.public_review_status
          const priorityInfo = getPriorityInfo(event)

          if (!status) {
            return <span className="text-sm text-gray-400">—</span>
          }
          if (status === 'APPROVED') {
            return (
              <span className="inline-flex items-center gap-1 text-sm text-green-700">
                <CheckCircle className="w-4 h-4" />
                Approved
              </span>
            )
          }
          if (status === 'REJECTED') {
            return (
              <span className="inline-flex items-center gap-1 text-sm text-red-700">
                <XCircle className="w-4 h-4" />
                Rejected
              </span>
            )
          }
          if (status === 'PENDING') {
            return (
              <div className="flex flex-col gap-1">
                <span className="inline-flex items-center gap-1 text-sm text-yellow-700">
                  <Clock className="w-4 h-4" />
                  Pending
                </span>
                {priorityInfo && (
                  <div className="flex items-center gap-2">
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${priorityInfo.color}`}
                      title={`Submitted ${priorityInfo.timeDisplay} ago`}
                    >
                      {priorityInfo.label}
                    </span>
                    <span className="text-xs text-gray-500" title={`${priorityInfo.timeDisplay} ago`}>
                      {priorityInfo.timeDisplay}
                    </span>
                  </div>
                )}
              </div>
            )
          }
          return <span className="text-sm text-gray-600">{status}</span>
        },
      },
      {
        accessorKey: 'start_date_time',
        header: 'Start Date',
        cell: ({ row }) => (
          <div className="text-sm text-gray-600">
            {new Date(row.original.start_date_time).toLocaleDateString('en-AU')}
          </div>
        ),
      },
      {
        id: 'actions',
        header: 'Actions',
        cell: ({ row }) => {
          const event = row.original
          const canReview = event.public_review_status === 'PENDING'

          return (
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  setSelectedEvent(event)
                  setShowReviewModal(true)
                }}
                className="inline-flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-teal-700 bg-teal-50 rounded-md hover:bg-teal-100 transition-colors"
              >
                <Eye className="w-4 h-4" />
                {canReview ? 'Review' : 'View'}
              </button>
            </div>
          )
        },
      },
    ],
    [
      eventTypes,
      eventStatuses,
      industries,
      companies,
      editingCell,
      editingValue,
      handleCellEdit,
      handleCellSave,
      handleCellCancel,
      updateEventMutation.isPending,
      getPriorityInfo,
    ]
  )

  const handleApprove = (eventId: number, comment?: string) => {
    approveMutation.mutate({ eventId, comment })
  }

  const handleReject = (eventId: number, comment: string) => {
    rejectMutation.mutate({ eventId, comment })
  }

  const handlePageChange = useCallback((page: number) => {
    setPagination((prev) => ({
      ...prev,
      page,
    }))
  }, [])

  const handlePageSizeChange = useCallback((pageSize: number) => {
    setPagination({
      page: 1,
      pageSize,
    })
  }, [])

  // Expandable row form state
  const [expandedRowData, setExpandedRowData] = useState<Record<string, Partial<AdminEvent>>>({})

  // Handle expandable row form changes
  const handleExpandedRowChange = useCallback((rowId: string, field: string, value: unknown) => {
    setExpandedRowData((prev) => ({
      ...prev,
      [rowId]: {
        ...prev[rowId],
        [field]: value,
      },
    }))
  }, [])

  // Handle expandable row form save
  const handleExpandedRowSave = useCallback(
    (event: AdminEvent) => {
      const rowData = expandedRowData[`row-${event.event_id}`] || {}
      const updates: Partial<AdminEventUpdateRequest> = {}

      // Map form fields to update request (snake_case for admin API)
      if (rowData.name !== undefined && rowData.name !== event.name) {
        updates.name = rowData.name
      }
      if (rowData.description !== undefined && rowData.description !== event.description) {
        updates.description = rowData.description
      }
      if (
        rowData.event_type_id !== undefined &&
        rowData.event_type_id !== event.event_type_id
      ) {
        updates.event_type_id = rowData.event_type_id
      }
      if (
        rowData.event_status_id !== undefined &&
        rowData.event_status_id !== event.event_status_id
      ) {
        updates.event_status_id = rowData.event_status_id
      }
      if (rowData.industry_id !== undefined && rowData.industry_id !== event.industry_id) {
        updates.industry_id = rowData.industry_id || null
      }
      if (rowData.company_id !== undefined && rowData.company_id !== event.company_id) {
        updates.organizer_company_id = rowData.company_id
      }
      if (rowData.start_date_time !== undefined) {
        // Compare dates properly
        const originalDate = event.start_date_time
          ? new Date(event.start_date_time).toISOString()
          : null
        const newDate = rowData.start_date_time
          ? new Date(rowData.start_date_time as string).toISOString()
          : null
        if (originalDate !== newDate) {
          updates.start_datetime = newDate
        }
      }
      if (rowData.end_date_time !== undefined) {
        // Compare dates properly
        const originalDate = event.end_date_time
          ? new Date(event.end_date_time).toISOString()
          : null
        const newDate = rowData.end_date_time
          ? new Date(rowData.end_date_time as string).toISOString()
          : null
        if (originalDate !== newDate) {
          updates.end_datetime = newDate
        }
      }
      if (rowData.short_description !== undefined && rowData.short_description !== event.short_description) {
        updates.short_description = rowData.short_description
      }
      if (rowData.timezone_identifier !== undefined && rowData.timezone_identifier !== event.timezone_identifier) {
        updates.timezone_identifier = rowData.timezone_identifier || null
      }
      if (rowData.venue_name !== undefined && rowData.venue_name !== event.venue_name) {
        updates.venue_name = rowData.venue_name || null
      }
      if (rowData.venue_address !== undefined && rowData.venue_address !== event.venue_address) {
        updates.venue_address = rowData.venue_address || null
      }
      if (rowData.city !== undefined && rowData.city !== event.city) {
        updates.city = rowData.city || null
      }
      if (rowData.state !== undefined && rowData.state !== event.state) {
        updates.state = rowData.state || null
      }
      if (rowData.country_id !== undefined && rowData.country_id !== event.country_id) {
        updates.country_id = rowData.country_id || null
      }
      if (rowData.latitude !== undefined && rowData.latitude !== event.latitude) {
        updates.latitude = rowData.latitude || null
      }
      if (rowData.longitude !== undefined && rowData.longitude !== event.longitude) {
        updates.longitude = rowData.longitude || null
      }
      if (rowData.tags !== undefined && rowData.tags !== event.tags) {
        updates.tags = rowData.tags || null
      }
      if (rowData.is_public !== undefined && rowData.is_public !== event.is_public) {
        updates.is_public = rowData.is_public
      }
      if (rowData.is_shared_with_platform !== undefined && rowData.is_shared_with_platform !== event.is_shared_with_platform) {
        updates.is_shared_with_platform = rowData.is_shared_with_platform
      }
      if (rowData.is_recurring !== undefined && rowData.is_recurring !== event.is_recurring) {
        updates.is_recurring = rowData.is_recurring
      }
      if (rowData.organizer_company_id !== undefined && rowData.organizer_company_id !== event.organizer_company_id) {
        updates.organizer_company_id = rowData.organizer_company_id || null
      }
      if (rowData.organizer_contact_email !== undefined && rowData.organizer_contact_email !== event.organizer_contact_email) {
        updates.organizer_contact_email = rowData.organizer_contact_email || null
      }
      if (rowData.organizer_website !== undefined && rowData.organizer_website !== event.organizer_website) {
        updates.organizer_website = rowData.organizer_website || null
      }
      if (rowData.expected_attendees !== undefined && rowData.expected_attendees !== event.expected_attendees) {
        updates.expected_attendees = rowData.expected_attendees || null
      }

      if (Object.keys(updates).length === 0) {
        toast.info('No changes to save')
        return
      }

      // Use admin API directly with snake_case data
      updateEventMutation.mutate({ eventId: event.event_id, updates })
    },
    [expandedRowData, updateEventMutation, toast]
  )

  // Render expandable row form
  const renderExpandedRow = useCallback(
    (row: Row<AdminEvent>) => {
      const event = row.original as AdminEvent
      const rowId = `row-${event.event_id}`
      // Merge event data with form changes to ensure all fields are available
      const formData = { ...event, ...(expandedRowData[rowId] || {}) }

      return (
        <div className="p-6 bg-gray-50 border-t border-gray-200">
          <div className="w-full">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Edit Event: {event.name}</h3>
            {/* Wide grid layout: 4 columns on large screens, 3 on medium, 2 on small, 1 on mobile */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {/* Event Name - Full width */}
              <div className="sm:col-span-2 lg:col-span-3 xl:col-span-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Event Name *
                </label>
                <input
                  type="text"
                  value={formData.name || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'name', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Enter event name"
                />
              </div>

              {/* Short Description - Full width */}
              <div className="sm:col-span-2 lg:col-span-3 xl:col-span-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Short Description
                </label>
                <input
                  type="text"
                  value={formData.short_description || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'short_description', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Brief summary for list views"
                />
              </div>

              {/* Description - Full width */}
              <div className="sm:col-span-2 lg:col-span-3 xl:col-span-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={formData.description || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'description', e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Enter event description"
                />
              </div>

              {/* Event Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Event Type *
                </label>
                <select
                  value={formData.event_type_id || ''}
                  onChange={(e) =>
                    handleExpandedRowChange(rowId, 'event_type_id', Number(e.target.value))
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
                  <option value="">Select event type...</option>
                  {eventTypes.map((type) => (
                    <option key={type.eventTypeId} value={type.eventTypeId}>
                      {type.typeName}
                    </option>
                  ))}
                </select>
              </div>

              {/* Event Status */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Event Status *
                </label>
                <select
                  value={formData.event_status_id || ''}
                  onChange={(e) =>
                    handleExpandedRowChange(rowId, 'event_status_id', Number(e.target.value))
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
                  <option value="">Select status...</option>
                  {eventStatuses.map((status) => (
                    <option key={status.eventStatusId} value={status.eventStatusId}>
                      {status.statusName}
                    </option>
                  ))}
                </select>
              </div>

              {/* Industry */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Industry
                </label>
                <select
                  value={formData.industry_id || ''}
                  onChange={(e) =>
                    handleExpandedRowChange(
                      rowId,
                      'industry_id',
                      e.target.value ? Number(e.target.value) : null
                    )
                  }
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

              {/* Company */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Company *
                </label>
                <select
                  value={formData.company_id || ''}
                  onChange={(e) =>
                    handleExpandedRowChange(rowId, 'company_id', Number(e.target.value))
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
                  <option value="">Select company...</option>
                  {companies.map((company) => (
                    <option key={company.company_id} value={company.company_id}>
                      {company.company_name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Start Date */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Start Date & Time *
                </label>
                <input
                  type="datetime-local"
                  value={
                    formData.start_date_time
                      ? (() => {
                          try {
                            const date = new Date(formData.start_date_time as string)
                            const year = date.getFullYear()
                            const month = String(date.getMonth() + 1).padStart(2, '0')
                            const day = String(date.getDate()).padStart(2, '0')
                            const hours = String(date.getHours()).padStart(2, '0')
                            const minutes = String(date.getMinutes()).padStart(2, '0')
                            return `${year}-${month}-${day}T${hours}:${minutes}`
                          } catch {
                            return ''
                          }
                        })()
                      : ''
                  }
                  onChange={(e) => {
                    const dateValue = e.target.value
                      ? new Date(e.target.value).toISOString()
                      : null
                    handleExpandedRowChange(rowId, 'start_date_time', dateValue)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                />
              </div>

              {/* End Date */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  End Date & Time
                </label>
                <input
                  type="datetime-local"
                  value={
                    formData.end_date_time
                      ? (() => {
                          try {
                            const date = new Date(formData.end_date_time as string)
                            const year = date.getFullYear()
                            const month = String(date.getMonth() + 1).padStart(2, '0')
                            const day = String(date.getDate()).padStart(2, '0')
                            const hours = String(date.getHours()).padStart(2, '0')
                            const minutes = String(date.getMinutes()).padStart(2, '0')
                            return `${year}-${month}-${day}T${hours}:${minutes}`
                          } catch {
                            return ''
                          }
                        })()
                      : ''
                  }
                  onChange={(e) => {
                    const dateValue = e.target.value
                      ? new Date(e.target.value).toISOString()
                      : null
                    handleExpandedRowChange(rowId, 'end_date_time', dateValue)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                />
              </div>

              {/* Timezone */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Timezone
                </label>
                <input
                  type="text"
                  value={formData.timezone_identifier || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'timezone_identifier', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="e.g., Australia/Sydney"
                />
              </div>

              {/* Venue Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Venue Name
                </label>
                <input
                  type="text"
                  value={formData.venue_name || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'venue_name', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Enter venue name"
                />
              </div>

              {/* Venue Address */}
              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Venue Address
                </label>
                <input
                  type="text"
                  value={formData.venue_address || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'venue_address', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Enter full venue address"
                />
              </div>

              {/* City */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  City
                </label>
                <input
                  type="text"
                  value={formData.city || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'city', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Enter city"
                />
              </div>

              {/* State */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  State/Province
                </label>
                <input
                  type="text"
                  value={formData.state || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'state', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Enter state/province"
                />
              </div>

              {/* Country */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Country
                </label>
                <select
                  value={formData.country_id || ''}
                  onChange={(e) =>
                    handleExpandedRowChange(
                      rowId,
                      'country_id',
                      e.target.value ? Number(e.target.value) : null
                    )
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
                  <option value="">Select country...</option>
                  {countries.map((country) => (
                    <option key={country.id} value={country.id}>
                      {country.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Latitude */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Latitude
                </label>
                <input
                  type="number"
                  step="any"
                  value={formData.latitude || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'latitude', e.target.value ? parseFloat(e.target.value) : null)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="e.g., -33.8688"
                />
              </div>

              {/* Longitude */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Longitude
                </label>
                <input
                  type="number"
                  step="any"
                  value={formData.longitude || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'longitude', e.target.value ? parseFloat(e.target.value) : null)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="e.g., 151.2093"
                />
              </div>

              {/* Tags */}
              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tags
                </label>
                <input
                  type="text"
                  value={formData.tags || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'tags', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="Comma-separated tags"
                />
              </div>

              {/* Is Public */}
              <div>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.is_public || false}
                    onChange={(e) => handleExpandedRowChange(rowId, 'is_public', e.target.checked)}
                    className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Is Public</span>
                </label>
              </div>

              {/* Is Shared With Platform */}
              <div>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.is_shared_with_platform || false}
                    onChange={(e) => handleExpandedRowChange(rowId, 'is_shared_with_platform', e.target.checked)}
                    className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Shared With Platform</span>
                </label>
              </div>

              {/* Is Recurring */}
              <div>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.is_recurring || false}
                    onChange={(e) => handleExpandedRowChange(rowId, 'is_recurring', e.target.checked)}
                    className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
                  />
                  <span className="text-sm font-medium text-gray-700">Is Recurring</span>
                </label>
              </div>

              {/* Organizer Company */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Organizer Company
                </label>
                <select
                  value={formData.organizer_company_id || ''}
                  onChange={(e) =>
                    handleExpandedRowChange(
                      rowId,
                      'organizer_company_id',
                      e.target.value ? Number(e.target.value) : null
                    )
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
                  <option value="">Select organizer company...</option>
                  {companies.map((company) => (
                    <option key={company.company_id} value={company.company_id}>
                      {company.company_name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Organizer Contact Email */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Organizer Contact Email
                </label>
                <input
                  type="email"
                  value={formData.organizer_contact_email || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'organizer_contact_email', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="organizer@example.com"
                />
              </div>

              {/* Organizer Website */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Organizer Website
                </label>
                <input
                  type="url"
                  value={formData.organizer_website || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'organizer_website', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="https://example.com"
                />
              </div>

              {/* Expected Attendees */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Expected Attendees
                </label>
                <input
                  type="number"
                  value={formData.expected_attendees || ''}
                  onChange={(e) => handleExpandedRowChange(rowId, 'expected_attendees', e.target.value ? parseInt(e.target.value) : null)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  placeholder="0"
                />
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-4 flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
              <button
                onClick={() => {
                  // Reset form data for this row
                  setExpandedRowData((prev) => {
                    const newData = { ...prev }
                    delete newData[rowId]
                    return newData
                  })
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
              >
                Cancel
              </button>
              <button
                onClick={() => handleExpandedRowSave(event)}
                disabled={updateEventMutation.isPending}
                className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {updateEventMutation.isPending ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </div>
        </div>
      )
    },
    [
      expandedRowData,
      eventTypes,
      eventStatuses,
      industries,
      companies,
      countries,
      handleExpandedRowChange,
      handleExpandedRowSave,
      updateEventMutation.isPending,
    ]
  )

  return (
    <div className="space-y-4">
      {/* Date Filter Indicator */}
      {dateFilter !== 'all' && (
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between p-3 bg-teal-50 border border-teal-200 rounded-md">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-teal-700">
                Filtered by:{' '}
                {dateFilter === 'past' && 'Past Events'}
                {dateFilter === 'current' && 'Current Events'}
                {dateFilter === 'future' && 'Future Events'}
              </span>
            </div>
            {onDateFilterChange && (
              <button
                onClick={() => onDateFilterChange('all')}
                className="text-sm text-teal-600 hover:text-teal-700 underline"
              >
                Clear filter
              </button>
            )}
          </div>
        </div>
      )}

      {/* Priority Summary */}
      {eventsData?.events && eventsData.events.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Pending Events Priority Summary</h3>
          <div className="flex flex-wrap gap-4">
            {(() => {
              const pendingEvents = eventsData.events.filter(
                (e) => e.public_review_status === 'PENDING'
              )
              const priorityCounts = {
                urgent: 0,
                high: 0,
                medium: 0,
                low: 0,
              }

              pendingEvents.forEach((event) => {
                const priorityInfo = getPriorityInfo(event)
                if (priorityInfo) {
                  priorityCounts[priorityInfo.priority]++
                }
              })

              return (
                <>
                  {priorityCounts.urgent > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center px-2.5 py-1 rounded text-xs font-medium bg-red-100 text-red-800">
                        Urgent (72h+)
                      </span>
                      <span className="text-sm font-semibold text-gray-900">
                        {priorityCounts.urgent}
                      </span>
                    </div>
                  )}
                  {priorityCounts.high > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center px-2.5 py-1 rounded text-xs font-medium bg-orange-100 text-orange-800">
                        High (48h+)
                      </span>
                      <span className="text-sm font-semibold text-gray-900">
                        {priorityCounts.high}
                      </span>
                    </div>
                  )}
                  {priorityCounts.medium > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center px-2.5 py-1 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                        Medium (24h+)
                      </span>
                      <span className="text-sm font-semibold text-gray-900">
                        {priorityCounts.medium}
                      </span>
                    </div>
                  )}
                  {priorityCounts.low > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center px-2.5 py-1 rounded text-xs font-medium bg-green-100 text-green-800">
                        New (&lt;24h)
                      </span>
                      <span className="text-sm font-semibold text-gray-900">
                        {priorityCounts.low}
                      </span>
                    </div>
                  )}
                  {pendingEvents.length === 0 && (
                    <span className="text-sm text-gray-500">No pending events</span>
                  )}
                </>
              )
            })()}
          </div>
        </div>
      )}

      {/* Events Table */}
      <div className="bg-white rounded-lg shadow w-full">
        <DataTable
          columns={columns}
          data={eventsData?.events || []}
          isLoading={isLoading}
          enableSorting={true}
          enableFiltering={true}
          enablePagination={true}
          enableColumnFilters={true}
          columnFilterConfigs={columnFilterConfigs}
          onColumnFilterChange={(columnId, value) => {
            if (columnId === 'event_type_id') {
              setFilters((prev) => ({
                ...prev,
                event_type_id: value ? Number(value) : undefined,
              }))
            } else if (columnId === 'event_status_id') {
              setFilters((prev) => ({
                ...prev,
                event_status_id: value ? Number(value) : undefined,
              }))
            } else if (columnId === 'public_review_status') {
              setFilters((prev) => ({
                ...prev,
                public_review_status: value ? String(value) : undefined,
              }))
            }
            // Reset to first page when filter changes
            setPagination((prev) => ({ ...prev, page: 1 }))
          }}
          enableExpandableRows={true}
          renderExpandedRow={renderExpandedRow}
          pageSize={pagination.pageSize}
          currentPage={pagination.page}
          totalItems={eventsData?.total ?? 0}
          pageSizeOptions={[10, 20, 50]}
          onPageChange={handlePageChange}
          onPageSizeChange={handlePageSizeChange}
          searchPlaceholder="Search events by name..."
          emptyMessage="No events found"
        />
      </div>

      {/* Review Modal */}
      {showReviewModal && selectedEvent && (
        <EventReviewModal
          eventId={selectedEvent.event_id}
          eventName={selectedEvent.name}
          isOpen={showReviewModal}
          onClose={() => {
            setShowReviewModal(false)
            setSelectedEvent(null)
          }}
          onApprove={handleApprove}
          onReject={handleReject}
          isLoading={approveMutation.isPending || rejectMutation.isPending}
        />
      )}
    </div>
  )
}
