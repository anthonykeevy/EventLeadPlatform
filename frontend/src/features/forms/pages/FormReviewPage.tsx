/**
 * FormReviewPage - Story 5.6, 5.8
 * Admin review: Approve only, Approve & Publish, Reject.
 * When published: production URL + copy, Unpublish.
 * Unpublish modes: Manual, Event end, Schedule.
 */
import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { Eye, CheckCircle, XCircle, ArrowLeft, Copy, ExternalLink, Ban } from 'lucide-react'
import {
  getForm,
  getFormReviewContext,
  createPreviewLink,
  approvePublishRequest,
  rejectPublishRequest,
  publishForm,
  unpublishForm,
} from '../api/formsApi'
import { useToastNotifications } from '../../ux'

type UnpublishMode = 'MANUAL' | 'EVENT_END' | 'SCHEDULED'

export function FormReviewPage() {
  const { formId } = useParams<{ formId: string }>()
  const navigate = useNavigate()
  const toast = useToastNotifications()
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)
  const [form, setForm] = useState<{ formId: number; formName: string } | null>(null)
  const [context, setContext] = useState<{
    formStatus: string
    hasPendingRequest: boolean
    hasApprovedRequest: boolean
    productionUrl: string | null
    unpublishMode: string
    scheduledUnpublishDate: string | null
    eventEndDate: string | null
  } | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [comment, setComment] = useState('')
  const [rejectReason, setRejectReason] = useState('')
  const [unpublishMode, setUnpublishMode] = useState<UnpublishMode>('MANUAL')
  const [scheduledDate, setScheduledDate] = useState('')

  const id = formId ? parseInt(formId, 10) : NaN

  useEffect(() => {
    if (!id || isNaN(id)) {
      setError('Invalid form ID')
      setLoading(false)
      return
    }
    Promise.all([getForm(id), getFormReviewContext(id)])
      .then(([f, ctx]) => {
        setForm({ formId: f.formId, formName: f.formName })
        setContext(ctx)
        setUnpublishMode((ctx.unpublishMode as UnpublishMode) || 'MANUAL')
        setScheduledDate(ctx.scheduledUnpublishDate?.slice(0, 10) ?? '')
      })
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load'))
      .finally(() => setLoading(false))
  }, [id])

  const handleOpenPreview = async () => {
    if (!id) return
    try {
      setProcessing(true)
      const url = await createPreviewLink(id)
      window.open(url, '_blank', 'noopener,noreferrer')
      toast.success('Preview opened. Test the form, then return here.', 'Info')
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to open preview', 'Error')
    } finally {
      setProcessing(false)
    }
  }

  const handleApproveOnly = async () => {
    if (!id) return
    try {
      setProcessing(true)
      await approvePublishRequest(id, { publish: false, comment: comment || undefined })
      toast.success('Request approved. Form is ready to publish. You can publish it from the Dashboard when ready.', 'Success')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to approve', 'Error')
    } finally {
      setProcessing(false)
    }
  }

  const handleApproveAndPublish = async () => {
    if (!id) return
    try {
      setProcessing(true)
      const opts: { publish: true; comment?: string; unpublishMode: UnpublishMode; scheduledUnpublishDate?: string } = {
        publish: true,
        comment: comment || undefined,
        unpublishMode,
      }
      if (unpublishMode === 'SCHEDULED' && scheduledDate) {
        opts.scheduledUnpublishDate = scheduledDate + 'T23:59:59Z'
      }
      await approvePublishRequest(id, opts)
      toast.success('Form approved and published.', 'Success')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to approve and publish', 'Error')
    } finally {
      setProcessing(false)
    }
  }

  const handlePublish = async () => {
    if (!id) return
    try {
      setProcessing(true)
      const opts: { unpublishMode: UnpublishMode; scheduledUnpublishDate?: string } = { unpublishMode }
      if (unpublishMode === 'SCHEDULED' && scheduledDate) {
        opts.scheduledUnpublishDate = scheduledDate + 'T23:59:59Z'
      }
      await publishForm(id, opts)
      toast.success('Form published.', 'Success')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to publish', 'Error')
    } finally {
      setProcessing(false)
    }
  }

  const handleReject = async () => {
    if (!id) return
    try {
      setProcessing(true)
      await rejectPublishRequest(id, rejectReason || undefined)
      toast.success('Publish request rejected. Form returned to Draft.', 'Success')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to reject', 'Error')
    } finally {
      setProcessing(false)
    }
  }

  const handleUnpublish = async () => {
    if (!id) return
    try {
      setProcessing(true)
      await unpublishForm(id)
      toast.success('Form unpublished.', 'Success')
      const ctx = await getFormReviewContext(id)
      setContext(ctx)
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to unpublish', 'Error')
    } finally {
      setProcessing(false)
    }
  }

  const handleCopyUrl = () => {
    if (context?.productionUrl) {
      navigator.clipboard.writeText(context.productionUrl)
      toast.success('URL copied to clipboard.', 'Success')
    }
  }

  const isPendingReview = context?.formStatus === 'PENDING_REVIEW'
  const isApprovedForPublish = context?.formStatus === 'APPROVED_FOR_PUBLISH'
  const isPublished = context?.formStatus === 'PUBLISHED'
  const isReadyToPublish = (isPendingReview || isApprovedForPublish) && context?.hasApprovedRequest && !context?.hasPendingRequest
  const hasEvent = !!context?.eventEndDate
  const unpublishDate = context?.scheduledUnpublishDate
    ? new Date(context.scheduledUnpublishDate).toLocaleDateString()
    : context?.eventEndDate
      ? new Date(context.eventEndDate).toLocaleDateString()
      : null

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  if (error || !form) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow p-6">
          <p className="text-red-600">{error ?? 'Form not found'}</p>
          <Link to="/dashboard" className="mt-4 inline-block text-teal-600 hover:underline">
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow overflow-hidden">
        <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4">
          <div className="flex items-center gap-3">
            <Link
              to="/dashboard"
              className="text-white hover:text-gray-200 p-1 rounded transition-colors"
              aria-label="Back to dashboard"
            >
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <h1 className="text-xl font-bold">Review and Publish</h1>
          </div>
          <p className="mt-2 text-teal-100 text-sm">{form.formName}</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Published form: URL + Unpublish */}
          {isPublished && (
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-2">Published form</h2>
              {context?.productionUrl && (
                <div className="flex items-center gap-2 mb-3">
                  <input
                    type="text"
                    readOnly
                    value={context.productionUrl}
                    className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm bg-gray-50"
                  />
                  <button
                    type="button"
                    onClick={handleCopyUrl}
                    className="inline-flex items-center gap-2 px-3 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 text-sm"
                  >
                    <Copy size={16} /> Copy
                  </button>
                  <a
                    href={context.productionUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-3 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 text-sm"
                  >
                    <ExternalLink size={16} /> Open
                  </a>
                </div>
              )}
              {unpublishDate && (
                <p className="text-sm text-amber-700 mb-3">
                  Will unpublish on {unpublishDate}
                </p>
              )}
              <button
                type="button"
                onClick={handleUnpublish}
                disabled={processing}
                className="inline-flex items-center gap-2 px-4 py-2 bg-amber-600 text-white rounded-md hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
              >
                <Ban size={16} /> Unpublish
              </button>
            </section>
          )}

          {/* Ready to publish (approved but not yet published) */}
          {isReadyToPublish && (
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-2">Ready to publish</h2>
              <p className="text-gray-600 text-sm mb-4">
                The publish request was approved. Publish the form now with one click.
              </p>
              <UnpublishModeFields
                unpublishMode={unpublishMode}
                setUnpublishMode={setUnpublishMode}
                scheduledDate={scheduledDate}
                setScheduledDate={setScheduledDate}
                hasEvent={hasEvent}
              />
              <button
                type="button"
                onClick={handlePublish}
                disabled={processing}
                className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium mt-3"
              >
                <CheckCircle size={16} /> Publish
              </button>
            </section>
          )}

          {/* Pending review: Approve only, Approve & Publish, Reject */}
          {isPendingReview && context?.hasPendingRequest && (
            <>
              <section>
                <h2 className="text-lg font-semibold text-gray-900 mb-2">1. Test the form</h2>
                <p className="text-gray-600 text-sm mb-3">
                  Open the form in preview mode to test it before approving or rejecting.
                </p>
                <button
                  type="button"
                  onClick={handleOpenPreview}
                  disabled={processing}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
                >
                  <Eye size={16} /> Open in preview
                </button>
              </section>

              <section>
                <h2 className="text-lg font-semibold text-gray-900 mb-2">2. Approve or Reject</h2>
                <p className="text-gray-600 text-sm mb-4">
                  Approve only to signal ready (publish later), or approve and publish now.
                </p>

                <div className="space-y-3 mb-4">
                  <label htmlFor="comment" className="block text-sm font-medium text-gray-700">
                    Comment (optional)
                  </label>
                  <textarea
                    id="comment"
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    placeholder="Add a note for the requester..."
                    rows={2}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-teal-500 focus:border-teal-500"
                  />
                </div>

                <UnpublishModeFields
                  unpublishMode={unpublishMode}
                  setUnpublishMode={setUnpublishMode}
                  scheduledDate={scheduledDate}
                  setScheduledDate={setScheduledDate}
                  hasEvent={hasEvent}
                />

                <div className="flex flex-wrap gap-3 mt-4">
                  <button
                    type="button"
                    onClick={handleApproveOnly}
                    disabled={processing}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
                  >
                    <CheckCircle size={16} /> Approve only
                  </button>
                  <button
                    type="button"
                    onClick={handleApproveAndPublish}
                    disabled={processing}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
                  >
                    <CheckCircle size={16} /> Approve &amp; Publish
                  </button>
                  <button
                    type="button"
                    onClick={handleReject}
                    disabled={processing}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
                  >
                    <XCircle size={16} /> Reject
                  </button>
                </div>

                <div className="mt-4 space-y-3">
                  <label htmlFor="reject-reason" className="block text-sm font-medium text-gray-700">
                    Rejection reason (optional)
                  </label>
                  <textarea
                    id="reject-reason"
                    value={rejectReason}
                    onChange={(e) => setRejectReason(e.target.value)}
                    placeholder="E.g. Please fix the validation on field X..."
                    rows={2}
                    className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-teal-500 focus:border-teal-500"
                  />
                </div>
              </section>
            </>
          )}

          {!isPendingReview && !isPublished && !isReadyToPublish && (
            <p className="text-gray-600">No pending publish request for this form.</p>
          )}
        </div>
      </div>
    </div>
  )
}

function UnpublishModeFields({
  unpublishMode,
  setUnpublishMode,
  scheduledDate,
  setScheduledDate,
  hasEvent,
}: {
  unpublishMode: UnpublishMode
  setUnpublishMode: (m: UnpublishMode) => void
  scheduledDate: string
  setScheduledDate: (s: string) => void
  hasEvent: boolean
}) {
  return (
    <div className="space-y-3 mb-4">
      <label className="block text-sm font-medium text-[rgb(var(--color-foreground))]">When to unpublish</label>
      <div className="flex flex-wrap gap-4">
        <label className="flex items-center gap-2 text-[rgb(var(--color-foreground))] cursor-pointer">
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
          <span className="text-sm text-[rgb(var(--color-foreground))]">Event end date</span>
          {!hasEvent && <span className="text-xs text-[rgb(var(--color-muted-foreground))]">(link form to event)</span>}
        </label>
        <label className="flex items-center gap-2 text-[rgb(var(--color-foreground))] cursor-pointer">
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
        <div>
          <input
            type="date"
            value={scheduledDate}
            onChange={(e) => setScheduledDate(e.target.value)}
            className="rounded-md border border-[rgb(var(--color-input))] px-3 py-2 text-sm bg-[rgb(var(--color-background))] text-[rgb(var(--color-foreground))]"
          />
        </div>
      )}
    </div>
  )
}
