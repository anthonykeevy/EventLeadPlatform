/**
 * Review History Component
 * Story 2.6: Admin Public Event Review Workflow
 */
import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { adminReviewApi, ReviewHistoryEntry } from '../api/adminReviewApi'
import { CheckCircle, XCircle } from 'lucide-react'

interface ReviewHistoryProps {
  eventId?: number
}

export const ReviewHistory: React.FC<ReviewHistoryProps> = ({ eventId }) => {
  const [statusFilter, setStatusFilter] = useState<'all' | 'APPROVED' | 'REJECTED'>('all')

  const { data: history, isLoading } = useQuery<ReviewHistoryEntry[]>({
    queryKey: ['admin', 'review-history', eventId, statusFilter],
    queryFn: () => adminReviewApi.getReviewHistory(eventId),
    enabled: true,
  })

  const filteredHistory = history?.filter((entry) => {
    if (statusFilter === 'all') return true
    return entry.decision === statusFilter
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
        <span className="ml-3 text-gray-600">Loading review history...</span>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">Review History</h2>
          <select
            value={statusFilter}
            onChange={(e) =>
              setStatusFilter(e.target.value as 'all' | 'APPROVED' | 'REJECTED')
            }
            className="px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:ring-teal-500 focus:border-teal-500"
          >
            <option value="all">All Decisions</option>
            <option value="APPROVED">Approved Only</option>
            <option value="REJECTED">Rejected Only</option>
          </select>
        </div>
      </div>

      <div className="divide-y divide-gray-200">
        {filteredHistory && filteredHistory.length > 0 ? (
          filteredHistory.map((entry) => (
            <div key={entry.review_id} className="px-6 py-4 hover:bg-gray-50">
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
                      {new Date(entry.review_date).toLocaleString()}
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
          <div className="px-6 py-12 text-center text-gray-500">
            No review history found
          </div>
        )}
      </div>
    </div>
  )
}
