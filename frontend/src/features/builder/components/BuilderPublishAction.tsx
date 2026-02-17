/**
 * BuilderPublishAction - Story 5.6
 * Request Publish / Publish / Pending Review CTA for Builder header.
 * Shown when form is draft and user can request publish or publish.
 */
import { useState, useEffect } from 'react'
import { Send } from 'lucide-react'
import { useAuth } from '../../auth/context/AuthContext'
import { getForm, getFormReadiness, getCompanyTestConfig } from '../../forms/api/formsApi'
import { RequestPublishModal } from '../../forms/components/RequestPublishModal'

interface BuilderPublishActionProps {
  formId: string
  formName?: string
}

export function BuilderPublishAction({ formId, formName: fallbackFormName }: BuilderPublishActionProps) {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formStatus, setFormStatus] = useState<string | null>(null)
  const [readiness, setReadiness] = useState<{ canPublish: boolean; message?: string } | null>(null)
  const [requireApproval, setRequireApproval] = useState(false)
  const [formName, setFormName] = useState(fallbackFormName ?? '')

  const isCompanyAdmin = user?.role === 'company_admin' || user?.role === 'system_admin'
  const formIdNum = Number(formId)

  useEffect(() => {
    if (!formId || !formIdNum) return
    let cancelled = false
    setLoading(true)
    Promise.all([
      getForm(formIdNum),
      getFormReadiness(formIdNum),
      getCompanyTestConfig(),
    ])
      .then(([form, r, config]) => {
        if (cancelled) return
        setFormStatus(form.formStatus?.statusCode ?? null)
        setFormName(form.formName || fallbackFormName || '')
        setReadiness(r)
        setRequireApproval(config.requirePublishApproval)
      })
      .catch(() => {})
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => { cancelled = true }
  }, [formId, formIdNum, fallbackFormName])

  if (loading || !formStatus) return null
  if (formStatus === 'PUBLISHED') return null

  const isPendingReview = formStatus === 'PENDING_REVIEW'
  const canRequestPublish = !isCompanyAdmin && requireApproval && !isPendingReview
  const isReadyToRequest = readiness?.canPublish ?? false
  const showRequestPublish = canRequestPublish && isReadyToRequest

  if (isPendingReview && !isCompanyAdmin) {
    return (
      <span className="px-3 py-1.5 text-sm font-medium text-amber-700 bg-amber-100 rounded-md">
        Pending Admin Review
      </span>
    )
  }

  // Show Request Publish when Company User + approval required; disable with tooltip if not ready
  if (canRequestPublish) {
    const notReadyMessage = !isReadyToRequest && readiness?.message
      ? readiness.message
      : 'Complete required test runs to request publish'
    return (
      <>
        <div className="relative group">
          <button
            type="button"
            onClick={() => isReadyToRequest && setShowModal(true)}
            disabled={!isReadyToRequest}
            className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
            title={!isReadyToRequest ? notReadyMessage : 'Request that a Company Admin publish this form'}
          >
            <Send size={16} /> Request Publish
          </button>
          {!isReadyToRequest && (
            <div className="absolute bottom-full left-0 mb-1 px-2 py-1.5 text-xs text-white bg-gray-800 rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 max-w-xs">
              {notReadyMessage}
            </div>
          )}
        </div>
        {showModal && (
          <RequestPublishModal
            formId={formIdNum}
            formName={formName || 'Form'}
            onClose={() => setShowModal(false)}
            onSuccess={() => window.location.reload()}
          />
        )}
      </>
    )
  }

  return null
}
