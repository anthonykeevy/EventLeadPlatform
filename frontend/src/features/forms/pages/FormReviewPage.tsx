/**
 * FormReviewPage - Story 5.6
 * Admin review entry point: test form in preview, then Approve or Reject with optional comment.
 */
import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { Eye, CheckCircle, XCircle, ArrowLeft } from 'lucide-react'
import { getForm } from '../api/formsApi'
import { createPreviewLink, approvePublishRequest, rejectPublishRequest } from '../api/formsApi'
import { useToastNotifications } from '../../ux'

export function FormReviewPage() {
  const { formId } = useParams<{ formId: string }>()
  const navigate = useNavigate()
  const toast = useToastNotifications()
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)
  const [form, setForm] = useState<{ formId: number; formName: string } | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [comment, setComment] = useState('')
  const [rejectReason, setRejectReason] = useState('')

  const id = formId ? parseInt(formId, 10) : NaN

  useEffect(() => {
    if (!id || isNaN(id)) {
      setError('Invalid form ID')
      setLoading(false)
      return
    }
    getForm(id)
      .then((f) => setForm({ formId: f.formId, formName: f.formName }))
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Failed to load form')
      })
      .finally(() => setLoading(false))
  }, [id])

  const handleOpenPreview = async () => {
    if (!id) return
    try {
      setProcessing(true)
      const url = await createPreviewLink(id)
      window.open(url, '_blank', 'noopener,noreferrer')
      toast.success('Preview opened in new tab. Test the form, then return here to Approve or Reject.', 'Info')
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to open preview', 'Error')
    } finally {
      setProcessing(false)
    }
  }

  const handleApprove = async () => {
    if (!id) return
    try {
      setProcessing(true)
      await approvePublishRequest(id, comment || undefined)
      toast.success('Form approved and published.', 'Success')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Failed to approve', 'Error')
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
        {/* Header */}
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
          {/* Step 1: Open in Preview */}
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
              <Eye className="w-4 h-4" />
              Open in preview
            </button>
          </section>

          {/* Step 2: Decide */}
          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">2. Approve or Reject</h2>
            <p className="text-gray-600 text-sm mb-4">
              After testing, approve to publish the form or reject to return it to Draft.
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

            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={handleApprove}
                disabled={processing}
                className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
              >
                <CheckCircle className="w-4 h-4" />
                Approve &amp; Publish
              </button>
              <button
                type="button"
                onClick={handleReject}
                disabled={processing}
                className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
              >
                <XCircle className="w-4 h-4" />
                Reject
              </button>
            </div>

            <div className="mt-4 space-y-3">
              <label htmlFor="reject-reason" className="block text-sm font-medium text-gray-700">
                Rejection reason (optional — provide feedback when rejecting)
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
        </div>
      </div>
    </div>
  )
}
