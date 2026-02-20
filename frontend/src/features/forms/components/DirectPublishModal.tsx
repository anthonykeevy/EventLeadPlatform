/**
 * DirectPublishModal - Story 5.8
 * Modal for direct publish when RequirePublishApproval=false or Admin publishing from builder.
 */
import { useState } from 'react'
import { X, Upload } from 'lucide-react'
import { publishForm } from '../api/formsApi'

type UnpublishMode = 'MANUAL' | 'EVENT_END' | 'SCHEDULED'

interface DirectPublishModalProps {
  formId: number
  formName: string
  hasEvent: boolean
  onClose: () => void
  onSuccess: () => void
}

export function DirectPublishModal({
  formId,
  formName,
  hasEvent,
  onClose,
  onSuccess,
}: DirectPublishModalProps) {
  const [unpublishMode, setUnpublishMode] = useState<UnpublishMode>('MANUAL')
  const [scheduledDate, setScheduledDate] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setError(null)
    try {
      const opts: { unpublishMode: UnpublishMode; scheduledUnpublishDate?: string } = { unpublishMode }
      if (unpublishMode === 'SCHEDULED' && scheduledDate) {
        opts.scheduledUnpublishDate = scheduledDate + 'T23:59:59Z'
      }
      await publishForm(formId, opts)
      onSuccess()
      onClose()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to publish')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Publish Form</h3>
          <button onClick={onClose} className="p-1 rounded hover:bg-gray-100 text-gray-500" aria-label="Close">
            <X size={20} />
          </button>
        </div>
        <div className="p-4 space-y-4">
          <p className="text-sm font-medium text-gray-700">Form: {formName}</p>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">When to unpublish</label>
            <div className="space-y-2">
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="unpublishMode"
                  checked={unpublishMode === 'MANUAL'}
                  onChange={() => setUnpublishMode('MANUAL')}
                  className="rounded"
                />
                <span className="text-sm">Manual</span>
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="unpublishMode"
                  checked={unpublishMode === 'EVENT_END'}
                  onChange={() => setUnpublishMode('EVENT_END')}
                  disabled={!hasEvent}
                  className="rounded"
                />
                <span className="text-sm">Event end date</span>
                {!hasEvent && <span className="text-xs text-gray-500">(link form to event)</span>}
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="unpublishMode"
                  checked={unpublishMode === 'SCHEDULED'}
                  onChange={() => setUnpublishMode('SCHEDULED')}
                  className="rounded"
                />
                <span className="text-sm">Schedule</span>
              </label>
            </div>
            {unpublishMode === 'SCHEDULED' && (
              <input
                type="date"
                value={scheduledDate}
                onChange={(e) => setScheduledDate(e.target.value)}
                className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
              />
            )}
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
        </div>
        <div className="flex justify-end gap-2 p-4 border-t border-gray-200">
          <button type="button" onClick={onClose} className="btn-secondary" disabled={isSubmitting}>
            Cancel
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            className="btn-primary flex items-center gap-2"
            disabled={isSubmitting}
          >
            <Upload size={16} />
            {isSubmitting ? 'Publishing...' : 'Publish'}
          </button>
        </div>
      </div>
    </div>
  )
}
