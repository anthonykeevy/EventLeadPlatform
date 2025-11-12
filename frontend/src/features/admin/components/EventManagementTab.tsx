/**
 * Event Management Tab Component
 * Story 2.6: Admin Public Event Review Workflow
 */
import React, { useState, useMemo, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ColumnDef } from '@tanstack/react-table'
import { DataTable } from '../../../components/common/DataTable'
import { adminDashboardApi, AdminEvent } from '../api/adminDashboardApi'
import { adminReviewApi } from '../api/adminReviewApi'
import { EventReviewModal } from './EventReviewModal'
import { CheckCircle, XCircle, Clock, Eye } from 'lucide-react'
import { useToastNotifications } from '../../../features/ux'

export const EventManagementTab: React.FC = () => {
  const [selectedEvent, setSelectedEvent] = useState<AdminEvent | null>(null)
  const [showReviewModal, setShowReviewModal] = useState(false)
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

  // Fetch events with filters
  const { data: eventsData, isLoading } = useQuery({
    queryKey: ['admin', 'events', filters, pagination.page, pagination.pageSize],
    queryFn: () =>
      adminDashboardApi.getEvents({
        ...filters,
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
    onError: (error: any) => {
      toast.error(error?.message || 'Failed to approve event')
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
    onError: (error: any) => {
      toast.error(error?.message || 'Failed to reject event')
    },
  })

  // Table columns
  const columns = useMemo<ColumnDef<AdminEvent>[]>(
    () => [
      {
        accessorKey: 'name',
        header: 'Event Name',
        cell: ({ row }) => (
          <div className="font-medium text-gray-900">{row.original.name}</div>
        ),
      },
      {
        accessorKey: 'company_name',
        header: 'Company',
        cell: ({ row }) => (
          <div className="text-sm text-gray-600">{row.original.company_name}</div>
        ),
      },
      {
        accessorKey: 'event_type_name',
        header: 'Type',
        cell: ({ row }) => (
          <span className="text-sm text-gray-600">{row.original.event_type_name}</span>
        ),
      },
      {
        accessorKey: 'event_status_name',
        header: 'Status',
        cell: ({ row }) => (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {row.original.event_status_name}
          </span>
        ),
      },
      {
        accessorKey: 'public_review_status',
        header: 'Review Status',
        cell: ({ row }) => {
          const status = row.original.public_review_status
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
              <span className="inline-flex items-center gap-1 text-sm text-yellow-700">
                <Clock className="w-4 h-4" />
                Pending
              </span>
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
    []
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

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Review Status
            </label>
            <select
              value={filters.public_review_status || ''}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  public_review_status: e.target.value || undefined,
                })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500"
            >
              <option value="">All Statuses</option>
              <option value="PENDING">Pending</option>
              <option value="APPROVED">Approved</option>
              <option value="REJECTED">Rejected</option>
            </select>
          </div>
          {/* TODO: Add Event Status and Event Type filters when reference data is available */}
        </div>
      </div>

      {/* Events Table */}
      <div className="bg-white rounded-lg shadow">
        <DataTable
          columns={columns}
          data={eventsData?.events || []}
          isLoading={isLoading}
          enableSorting={true}
          enableFiltering={true}
          enablePagination={true}
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
