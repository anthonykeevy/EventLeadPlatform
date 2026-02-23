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
      <div className="bg-card rounded-lg shadow-xl max-w-md w-full mx-4 border border-[rgb(var(--color-border))]">
        <div className="flex items-center justify-between p-4 border-b border-[rgb(var(--color-border))]">
          <h3 className="text-lg font-semibold text-[rgb(var(--color-card-foreground))]">Publish Form</h3>
          <button onClick={onClose} className="p-1 rounded hover:bg-[rgb(var(--color-hover))] text-[rgb(var(--color-muted-foreground))]" aria-label="Close">
            <X size={20} />
          </button>
        </div>
        <div className="p-4 space-y-4">
          <p className="text-sm font-medium text-[rgb(var(--color-card-foreground))]">Form: {formName}</p>
          <div>
            <label className="block text-sm font-medium text-[rgb(var(--color-card-foreground))] mb-2">When to unpublish</label>
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-[rgb(var(--color-card-foreground))] cursor-pointer">
                <input
                  type="radio"
                  name="unpublishMode"
                  checked={unpublishMode === 'MANUAL'}
                  onChange={() => setUnpublishMode('MANUAL')}
                  className="rounded"
                />
                <span className="text-sm">Manual</span>
              </label>
              <label className={`flex items-center gap-2 cursor-pointer ${!hasEvent ? 'opacity-60' : ''}`}>
                <input
                  type="radio"
                  name="unpublishMode"
                  checked={unpublishMode === 'EVENT_END'}
                  onChange={() => setUnpublishMode('EVENT_END')}
                  disabled={!hasEvent}
                  className="rounded"
                />
                <span className="text-sm text-[rgb(var(--color-card-foreground))]">Event end date</span>
                {!hasEvent && <span className="text-xs text-[rgb(var(--color-muted-foreground))]">(link form to event)</span>}
              </label>
              <label className="flex items-center gap-2 text-[rgb(var(--color-card-foreground))] cursor-pointer">
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
                className="mt-2 w-full px-3 py-2 border border-[rgb(var(--color-input))] rounded-lg text-sm bg-[rgb(var(--color-background))] text-[rgb(var(--color-foreground))]"
              />
            )}
          </div>
          {error && <p className="text-sm text-[rgb(var(--color-error-text))]">{error}</p>}
        </div>
        <div className="flex justify-end gap-2 p-4 border-t border-[rgb(var(--color-border))]">
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
