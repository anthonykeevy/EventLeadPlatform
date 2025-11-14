/**
 * Review History Component
 * Story 2.6: Admin Public Event Review Workflow
 */
import React, { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { adminReviewApi, ReviewHistoryEntry } from '../api/adminReviewApi'
import { CheckCircle, XCircle, Filter, X } from 'lucide-react'

interface ReviewHistoryProps {
  eventId?: number
}

export const ReviewHistory: React.FC<ReviewHistoryProps> = ({ eventId }) => {
  const [statusFilter, setStatusFilter] = useState<'all' | 'APPROVED' | 'REJECTED'>('all')
  const [dateFilter, setDateFilter] = useState<'all' | 'today' | 'week' | 'month'>('all')

  const { data: history, isLoading } = useQuery<ReviewHistoryEntry[]>({
    queryKey: ['admin', 'review-history', eventId],
    queryFn: () => adminReviewApi.getReviewHistory(eventId),
    enabled: !!eventId, // Only fetch when eventId is provided
  })

  // Filter history based on status and date
  const filteredHistory = useMemo(() => {
    if (!history) return []

    let filtered = [...history]

    // Filter by status
    if (statusFilter !== 'all') {
      filtered = filtered.filter((entry) => entry.decision === statusFilter)
    }

    // Filter by date
    if (dateFilter !== 'all') {
      const now = new Date()
      const filterDate = new Date()

      switch (dateFilter) {
        case 'today':
          filterDate.setHours(0, 0, 0, 0)
          break
        case 'week':
          filterDate.setDate(now.getDate() - 7)
          break
        case 'month':
          filterDate.setMonth(now.getMonth() - 1)
          break
      }

      filtered = filtered.filter((entry) => {
        const reviewDate = new Date(entry.review_date)
        return reviewDate >= filterDate
      })
    }

    // Sort by review date (newest first)
    return filtered.sort((a, b) => {
      const dateA = new Date(a.review_date).getTime()
      const dateB = new Date(b.review_date).getTime()
      return dateB - dateA
    })
  }, [history, statusFilter, dateFilter])

  // Count entries by status
  const statusCounts = useMemo(() => {
    if (!history) return { approved: 0, rejected: 0, total: 0 }

    return {
      approved: history.filter((e) => e.decision === 'APPROVED').length,
      rejected: history.filter((e) => e.decision === 'REJECTED').length,
      total: history.length,
    }
  }, [history])

  const hasActiveFilters = statusFilter !== 'all' || dateFilter !== 'all'

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-6">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-teal-600"></div>
        <span className="ml-2 text-sm text-gray-600">Loading review history...</span>
      </div>
    )
  }

  return (
    <div>
      <div className="py-4 border-b border-gray-200">
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Review History</h3>
              {statusCounts.total > 0 && (
                <p className="text-sm text-gray-500 mt-1">
                  {statusCounts.total} total • {statusCounts.approved} approved •{' '}
                  {statusCounts.rejected} rejected
                </p>
              )}
            </div>
          </div>

          {/* Filter Controls */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-700">Filters:</span>
            </div>

            {/* Status Filter */}
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Status:</label>
              <select
                value={statusFilter}
                onChange={(e) =>
                  setStatusFilter(e.target.value as 'all' | 'APPROVED' | 'REJECTED')
                }
                className="px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
              >
                <option value="all">All Decisions</option>
                <option value="APPROVED">Approved Only</option>
                <option value="REJECTED">Rejected Only</option>
              </select>
            </div>

            {/* Date Filter */}
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Date:</label>
              <select
                value={dateFilter}
                onChange={(e) =>
                  setDateFilter(e.target.value as 'all' | 'today' | 'week' | 'month')
                }
                className="px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
              >
                <option value="all">All Time</option>
                <option value="today">Today</option>
                <option value="week">Last 7 Days</option>
                <option value="month">Last 30 Days</option>
              </select>
            </div>

            {/* Clear Filters Button */}
            {hasActiveFilters && (
              <button
                onClick={() => {
                  setStatusFilter('all')
                  setDateFilter('all')
                }}
                className="inline-flex items-center gap-1 px-3 py-1.5 text-sm text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
                title="Clear all filters"
              >
                <X className="w-3 h-3" />
                Clear Filters
              </button>
            )}

            {/* Results Count */}
            {hasActiveFilters && (
              <span className="text-sm text-gray-500">
                Showing {filteredHistory.length} of {statusCounts.total} entries
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="divide-y divide-gray-200">
        {filteredHistory && filteredHistory.length > 0 ? (
          filteredHistory.map((entry) => (
            <div key={entry.review_id} className="py-4 hover:bg-gray-50">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-sm font-medium text-gray-900">{entry.event_name}</h3>
                    {entry.decision === 'APPROVED' ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        <CheckCircle className="w-3 h-3" />
                        Approved
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        <XCircle className="w-3 h-3" />
                        Rejected
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-gray-600 space-y-1">
                    <p>
                      <span className="font-medium">Reviewed by:</span> {entry.reviewer_email}
                    </p>
                    <p>
                      <span className="font-medium">Review date:</span>{' '}
                      {new Date(entry.review_date).toLocaleString('en-AU', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </p>
                    {entry.comments && (
                      <div className="mt-2">
                        <p className="font-medium text-gray-700 mb-1">Comments:</p>
                        <p className="text-gray-600 whitespace-pre-wrap bg-gray-50 p-3 rounded-md">
                          {entry.comments}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="py-6 text-center">
            {hasActiveFilters ? (
              <div className="space-y-2">
                <p className="text-sm text-gray-500">No review history matches the current filters</p>
                <button
                  onClick={() => {
                    setStatusFilter('all')
                    setDateFilter('all')
                  }}
                  className="text-sm text-teal-600 hover:text-teal-700 underline"
                >
                  Clear filters to see all reviews
                </button>
              </div>
            ) : (
              <p className="text-sm text-gray-500">No review history found</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
