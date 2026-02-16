/**
 * RequestPublishModal - Story 5.6
 * Modal for Company User to request that a Company Admin publish the form.
 * Only shown when RequirePublishApproval is enabled and user is Company User.
 */
import { useState } from 'react'
import { X, Send } from 'lucide-react'
import { createPublishRequest } from '../api/formsApi'

interface RequestPublishModalProps {
  formId: number
  formName: string
  onClose: () => void
  onSuccess: () => void
}

export function RequestPublishModal({ formId, formName, onClose, onSuccess }: RequestPublishModalProps) {
  const [message, setMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setError(null)
    try {
      await createPublishRequest(formId, message.trim() || undefined)
      onSuccess()
      onClose()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit publish request')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Request Publish</h3>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-gray-100 text-gray-500"
            aria-label="Close"
          >
            <X size={20} />
          </button>
        </div>
        <div className="p-4 space-y-4">
          <p className="text-sm text-gray-600">
            Only Company Admins can publish forms. Your request will be added to the admin review queue.
          </p>
          <p className="text-sm font-medium text-gray-700">Form: {formName}</p>
          <div>
            <label htmlFor="request-message" className="block text-sm font-medium text-gray-700 mb-1">
              Message (optional)
            </label>
            <textarea
              id="request-message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Add a note for the admin..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              rows={3}
              maxLength={1000}
              disabled={isSubmitting}
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
        </div>
        <div className="flex justify-end gap-2 p-4 border-t border-gray-200">
          <button
            type="button"
            onClick={onClose}
            className="btn-secondary"
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            className="btn-primary flex items-center gap-2"
            disabled={isSubmitting}
          >
            <Send size={16} />
            {isSubmitting ? 'Submitting...' : 'Submit Request'}
          </button>
        </div>
      </div>
    </div>
  )
}
