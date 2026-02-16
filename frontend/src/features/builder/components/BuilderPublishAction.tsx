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
  const [readiness, setReadiness] = useState<{ canPublish: boolean } | null>(null)
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
  const showRequestPublish =
    !isCompanyAdmin &&
    requireApproval &&
    (readiness?.canPublish ?? false) &&
    !isPendingReview

  if (isPendingReview && !isCompanyAdmin) {
    return (
      <span className="px-3 py-1.5 text-sm font-medium text-amber-700 bg-amber-100 rounded-md">
        Pending Admin Review
      </span>
    )
  }

  if (showRequestPublish) {
    return (
      <>
        <button
          type="button"
          onClick={() => setShowModal(true)}
          className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2"
        >
          <Send size={16} /> Request Publish
        </button>
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
