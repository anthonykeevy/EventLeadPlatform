/**
 * Delete Event Confirmation Modal - Story 2.4 Task 12
 * Confirms event deletion before soft delete
 */

import React, { useState } from 'react'
import { X, AlertTriangle, Trash2 } from 'lucide-react'
import { Event } from '../types/events.types'
import { deleteEvent } from '../api/eventsApi'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'

interface DeleteEventConfirmModalProps {
  isOpen: boolean
  event: Event | null
  onClose: () => void
  onConfirm: () => void
}

export function DeleteEventConfirmModal({
  isOpen,
  event,
  onClose,
  onConfirm
}: DeleteEventConfirmModalProps) {
  const [isDeleting, setIsDeleting] = useState(false)
  const { showToast } = useToastNotifications()

  const handleConfirm = async () => {
    if (!event) return

    setIsDeleting(true)
    try {
      await deleteEvent(event.eventId)
      onConfirm()
      onClose()
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete event'
      showToast.error(errorMessage, 'Delete failed')
    } finally {
      setIsDeleting(false)
    }
  }

  if (!isOpen || !event) return null

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        {/* Modal */}
        <div
          className="bg-white rounded-lg shadow-2xl w-full max-w-md transform transition-all"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="bg-red-600 text-white px-6 py-4 rounded-t-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Delete Event</h2>
              </div>
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 p-1 rounded"
                aria-label="Close"
                disabled={isDeleting}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            <div className="mb-4">
              <p className="text-gray-700 mb-2">
                Are you sure you want to delete the event <strong>"{event.name}"</strong>?
              </p>
              <p className="text-sm text-gray-500">
                This action will soft-delete the event. It will no longer appear in your event list,
                but can be restored from the database if needed.
              </p>
            </div>

            {/* Event Details */}
            <div className="bg-gray-50 rounded-md p-4 mb-4">
              <div className="text-sm text-gray-600 space-y-1">
                <div>
                  <span className="font-medium">Event:</span> {event.name}
                </div>
                {event.eventType && (
                  <div>
                    <span className="font-medium">Type:</span> {event.eventType.typeName}
                  </div>
                )}
                {event.startDateTime && (
                  <div>
                    <span className="font-medium">Start Date:</span>{' '}
                    {new Date(event.startDateTime).toLocaleDateString('en-AU')}
                  </div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end gap-3">
              <button
                onClick={onClose}
                disabled={isDeleting}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                disabled={isDeleting}
                className="btn-danger flex items-center gap-2 px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isDeleting ? (
                  <>
                    <LoadingSpinner size="small" />
                    Deleting...
                  </>
                ) : (
                  <>
                    <Trash2 className="w-4 h-4" />
                    Delete Event
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
