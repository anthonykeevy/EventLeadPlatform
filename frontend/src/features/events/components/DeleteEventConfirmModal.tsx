/**
 * Delete Event Confirmation Modal - Story 2.4 Task 12
 * Confirms event deletion before soft delete
 */

import React, { useState } from 'react'
import { X, AlertTriangle, Trash2, LogOut } from 'lucide-react'
import { Event } from '../types/events.types'
import { deleteEvent, leaveEvent } from '../api/eventsApi'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'

interface DeleteEventConfirmModalProps {
  isOpen: boolean
  event: Event | null
  onClose: () => void
  onConfirm: () => void
  mode?: 'delete' | 'leave'
  companyId?: number // Required for 'leave' mode
}

export function DeleteEventConfirmModal({
  isOpen,
  event,
  onClose,
  onConfirm,
  mode = 'delete',
  companyId
}: DeleteEventConfirmModalProps) {
  const [isProcessing, setIsProcessing] = useState(false)
  const toast = useToastNotifications()

  const handleConfirm = async () => {
    if (!event) return
    
    if (mode === 'leave' && !companyId) {
      toast.error('Company ID required to leave event', 'Error')
      return
    }

    setIsProcessing(true)
    try {
      if (mode === 'delete') {
        await deleteEvent(event.eventId)
        toast.success('Event deleted successfully', 'Success')
      } else {
        await leaveEvent(event.eventId, companyId!)
        toast.success('Left event successfully', 'Success')
      }
      onConfirm()
      onClose()
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : `Failed to ${mode} event`
      toast.error(errorMessage, `${mode === 'delete' ? 'Delete' : 'Leave'} failed`)
    } finally {
      setIsProcessing(false)
    }
  }

  if (!isOpen || !event) return null

  const isDelete = mode === 'delete'

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
          <div className={`${isDelete ? 'bg-red-600' : 'bg-orange-500'} text-white px-6 py-4 rounded-t-lg`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-6 h-6" />
                <h2 className="text-xl font-semibold">{isDelete ? 'Delete Event' : 'Leave Event'}</h2>
              </div>
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 p-1 rounded"
                aria-label="Close"
                disabled={isProcessing}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            <div className="mb-4">
              <p className="text-gray-700 mb-2">
                {isDelete 
                  ? <>Are you sure you want to delete the event <strong>"{event.name}"</strong>?</>
                  : <>Are you sure you want to remove access to <strong>"{event.name}"</strong> for your company?</>
                }
              </p>
              <p className="text-sm text-gray-500">
                {isDelete
                  ? "This action will soft-delete the event. It will no longer appear in your event list."
                  : "You will no longer see this event or be able to manage its forms. The event owner will still have full access."
                }
              </p>
            </div>

            {/* Event Details */}
            <div className="bg-gray-50 rounded-md p-4 mb-4">
              <div className="text-sm text-gray-600 space-y-1">
                <div>
                  <span className="font-medium">Event:</span> {event.name}
                </div>
                {event.ownerCompany && !isDelete && (
                   <div>
                    <span className="font-medium">Owner:</span> {event.ownerCompany.companyName}
                   </div>
                )}
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
                disabled={isProcessing}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                disabled={isProcessing}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-white disabled:opacity-50 disabled:cursor-not-allowed ${isDelete ? 'bg-red-600 hover:bg-red-700' : 'bg-orange-500 hover:bg-orange-600'}`}
              >
                {isProcessing ? (
                  <>
                    <LoadingSpinner size="sm" />
                    {isDelete ? 'Deleting...' : 'Leaving...'}
                  </>
                ) : (
                  <>
                    {isDelete ? <Trash2 className="w-4 h-4" /> : <LogOut className="w-4 h-4" />}
                    {isDelete ? 'Delete Event' : 'Leave Event'}
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
