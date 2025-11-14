/**
 * Event Review Modal Component
 * Story 2.6: Admin Public Event Review Workflow
 */
import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { X, CheckCircle, XCircle, Loader2 } from 'lucide-react'
import { adminReviewApi, EventReviewDetails } from '../api/adminReviewApi'
import { ReviewHistory } from './ReviewHistory'

interface EventReviewModalProps {
  eventId: number
  eventName: string
  isOpen: boolean
  onClose: () => void
  onApprove: (eventId: number, comment?: string) => void
  onReject: (eventId: number, comment: string) => void
  isLoading?: boolean
}

export const EventReviewModal: React.FC<EventReviewModalProps> = ({
  eventId,
  eventName,
  isOpen,
  onClose,
  onApprove,
  onReject,
  isLoading = false,
}) => {
  const [action, setAction] = useState<'approve' | 'reject' | null>(null)
  const [comment, setComment] = useState('')
  const [showConfirm, setShowConfirm] = useState(false)

  // Fetch event details
  const { data: eventDetails, isLoading: loadingDetails } = useQuery<EventReviewDetails>({
    queryKey: ['admin', 'event-review', eventId],
    queryFn: () => adminReviewApi.getEventReviewDetails(eventId),
    enabled: isOpen,
  })

  if (!isOpen) return null

  const isPendingReview = eventDetails?.public_review_status === 'PENDING'

  const handleApproveClick = () => {
    if (!isPendingReview || isLoading) {
      return
    }
    setAction('approve')
    setShowConfirm(true)
  }

  const handleRejectClick = () => {
    if (!isPendingReview || isLoading) {
      return
    }
    setAction('reject')
    setShowConfirm(true)
  }

  const handleConfirm = () => {
    if (action === 'approve') {
      onApprove(eventId, comment || undefined)
    } else if (action === 'reject') {
      if (!comment.trim()) {
        alert('Comment is required for rejection')
        return
      }
      onReject(eventId, comment)
    }
    setShowConfirm(false)
    setAction(null)
    setComment('')
  }

  const handleCancel = () => {
    setShowConfirm(false)
    setAction(null)
    setComment('')
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div
          className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          onClick={onClose}
        />

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          {/* Header */}
          <div className="bg-white px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">
              Review Event: {eventName}
            </h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="bg-white px-6 py-4 max-h-[80vh] overflow-y-auto">
            {loadingDetails ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-teal-600" />
                <span className="ml-3 text-gray-600">Loading event details...</span>
              </div>
            ) : eventDetails ? (
              <div className="space-y-6">
                {/* Event Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Event Name</label>
                    <p className="mt-1 text-sm text-gray-900">{eventDetails.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Company</label>
                    <p className="mt-1 text-sm text-gray-900">{eventDetails.company_name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Creator</label>
                    <p className="mt-1 text-sm text-gray-900">{eventDetails.creator_email}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Event Type</label>
                    <p className="mt-1 text-sm text-gray-900">{eventDetails.event_type_name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Start Date</label>
                    <p className="mt-1 text-sm text-gray-900">
                      {new Date(eventDetails.start_date_time).toLocaleString()}
                    </p>
                  </div>
                  {eventDetails.end_date_time && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">End Date</label>
                      <p className="mt-1 text-sm text-gray-900">
                        {new Date(eventDetails.end_date_time).toLocaleString()}
                      </p>
                    </div>
                  )}
                  {eventDetails.venue_name && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Venue</label>
                      <p className="mt-1 text-sm text-gray-900">{eventDetails.venue_name}</p>
                    </div>
                  )}
                  {eventDetails.country_name && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Country</label>
                      <p className="mt-1 text-sm text-gray-900">{eventDetails.country_name}</p>
                    </div>
                  )}
                </div>

                {eventDetails.description && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Description</label>
                    <p className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">
                      {eventDetails.description}
                    </p>
                  </div>
                )}

                {/* Review History Section */}
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <div className="space-y-4">
                    <ReviewHistory eventId={eventId} />
                  </div>
                </div>

                {/* Review Comment */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Review Comment {action === 'reject' && <span className="text-red-600">*</span>}
                  </label>
                  <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-teal-500 focus:border-teal-500"
                    placeholder={
                      action === 'reject'
                        ? 'Required: Please provide feedback for rejection...'
                        : 'Optional: Add a comment about your decision...'
                    }
                  />
                  {action === 'reject' && !comment.trim() && (
                    <p className="mt-1 text-sm text-red-600">
                      Comment is required for rejection
                    </p>
                  )}
                  {!isPendingReview && (
                    <p className="mt-2 text-sm text-gray-500">
                      Review actions are only available while the event is in the <strong>PENDING</strong> review state.
                    </p>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                Failed to load event details
              </div>
            )}
          </div>

          {/* Footer Actions */}
          <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex items-center justify-end gap-3">
            {!showConfirm ? (
              <>
                <button
                  onClick={onClose}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleRejectClick}
                  className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-red-300"
                  disabled={isLoading || !isPendingReview}
                >
                  <XCircle className="w-4 h-4" />
                  Reject
                </button>
                <button
                  onClick={handleApproveClick}
                  className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-green-300"
                  disabled={isLoading || !isPendingReview}
                >
                  <CheckCircle className="w-4 h-4" />
                  Approve
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={handleCancel}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <button
                  onClick={handleConfirm}
                  className={`px-4 py-2 text-sm font-medium text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 flex items-center gap-2 ${
                    action === 'approve'
                      ? 'bg-green-600 hover:bg-green-700 focus:ring-green-500'
                      : 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
                  }`}
                  disabled={isLoading || (action === 'reject' && !comment.trim())}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      {action === 'approve' ? (
                        <>
                          <CheckCircle className="w-4 h-4" />
                          Confirm Approval
                        </>
                      ) : (
                        <>
                          <XCircle className="w-4 h-4" />
                          Confirm Rejection
                        </>
                      )}
                    </>
                  )}
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
