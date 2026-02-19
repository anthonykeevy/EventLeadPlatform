/**
 * PublishWorkflowStatus - Story 5.6
 * Clear "Next steps" callout for Company Users so they know where they stand
 * and what to do to get their form approved and published.
 */
import { AlertCircle, CheckCircle, Clock } from 'lucide-react'
import type { FormReadiness } from '../api/formsApi'

interface PublishWorkflowStatusProps {
  /** Current user is Company User (not admin) */
  isCompanyUser: boolean
  /** Company has RequirePublishApproval enabled */
  requirePublishApproval: boolean
  /** Form status code */
  formStatusCode: string | null
  /** Readiness from API */
  readiness: FormReadiness | null
  /** Readiness loading */
  loading?: boolean
}

export function PublishWorkflowStatus({
  isCompanyUser,
  requirePublishApproval,
  formStatusCode,
  readiness,
  loading,
}: PublishWorkflowStatusProps) {
  if (!isCompanyUser) return null

  if (loading || !readiness) {
    return (
      <div className="mt-4 p-4 rounded-lg bg-gray-50 border border-gray-200">
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <span className="animate-pulse">Checking publish status…</span>
        </div>
      </div>
    )
  }

  const isPendingReview = formStatusCode === 'PENDING_REVIEW'
  const isPublished = formStatusCode === 'PUBLISHED'
  const _canRequest = readiness.canPublish
  const needsTests = readiness.testRunsNeeded > 0

  // Company User + approval required: show Story 5.6 workflow
  if (requirePublishApproval) {
    if (isPublished) return null

    if (isPendingReview) {
      return (
        <div className="mt-4 p-4 rounded-lg bg-amber-50 border border-amber-200">
          <div className="flex items-start gap-3">
            <Clock className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-semibold text-amber-900">Pending Admin Review</h4>
              <p className="text-sm text-amber-800 mt-1">
                Your publish request has been sent to Company Admins. They will review and publish the form when ready.
              </p>
            </div>
          </div>
        </div>
      )
    }

    if (needsTests) {
      return (
        <div className="mt-4 p-4 rounded-lg bg-amber-50 border border-amber-200">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-semibold text-amber-900">Next step: Complete test runs</h4>
              <p className="text-sm text-amber-800 mt-1">
                {readiness.message} After that, click <strong>Request Publish</strong> to send the form to a Company Admin for approval.
              </p>
            </div>
          </div>
        </div>
      )
    }

    return (
      <div className="mt-4 p-4 rounded-lg bg-green-50 border border-green-200">
        <div className="flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-semibold text-green-900">Ready to request publish</h4>
            <p className="text-sm text-green-800 mt-1">
              Click <strong>Request Publish</strong> to send this form to a Company Admin. They will review and publish it.
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Company User + no approval required: they can publish directly
  if (needsTests) {
    return (
      <div className="mt-4 p-4 rounded-lg bg-amber-50 border border-amber-200">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-semibold text-amber-900">Next step: Complete test runs</h4>
            <p className="text-sm text-amber-800 mt-1">
              {readiness.message} After that, you can publish this form directly.
            </p>
          </div>
        </div>
      </div>
    )
  }

  if (isPublished) return null

  return (
    <div className="mt-4 p-4 rounded-lg bg-green-50 border border-green-200">
      <div className="flex items-start gap-3">
        <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-semibold text-green-900">Ready to publish</h4>
          <p className="text-sm text-green-800 mt-1">
            You can publish this form directly from the Edit form or via the Publish action.
          </p>
        </div>
      </div>
    </div>
  )
}
