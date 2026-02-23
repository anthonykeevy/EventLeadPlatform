/**
 * BuilderPublishAction - Story 5.6, 5.8
 * Request Publish / Publish / Pending Review CTA for Builder header.
 * When RequirePublishApproval=false or Admin: show direct Publish.
 * When Company User + approval required: show Request Publish.
 */
import { useState, useEffect } from 'react'
import { Send, Upload } from 'lucide-react'
import { useAuth } from '../../auth/context/AuthContext'
import { getForm, getFormReadiness, getCompanyTestConfig } from '../../forms/api/formsApi'
import { RequestPublishModal } from '../../forms/components/RequestPublishModal'
import { DirectPublishModal } from '../../forms/components/DirectPublishModal'

interface BuilderPublishActionProps {
  formId: string
  formName?: string
}

export function BuilderPublishAction({ formId, formName: fallbackFormName }: BuilderPublishActionProps) {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [showRequestModal, setShowRequestModal] = useState(false)
  const [showPublishModal, setShowPublishModal] = useState(false)
  const [formStatus, setFormStatus] = useState<string | null>(null)
  const [readiness, setReadiness] = useState<{ canPublish: boolean; message?: string } | null>(null)
  const [requireApproval, setRequireApproval] = useState(false)
  const [formCostThreshold, setFormCostThreshold] = useState<number | null>(null)
  const [deploymentCost, setDeploymentCost] = useState<number>(0)
  const [formName, setFormName] = useState(fallbackFormName ?? '')
  const [hasEvent, setHasEvent] = useState(false)

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
        setFormCostThreshold(config.formCostThreshold ?? null)
        setDeploymentCost(form.deploymentCost ?? 0)
        setHasEvent(!!form.eventId)
      })
      .catch(() => {})
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    // Refresh readiness when user returns from preview tab (Phase 1.1g)
    const onVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        getFormReadiness(formIdNum).then((r) => {
          if (!cancelled) setReadiness(r)
        })
      }
    }
    document.addEventListener('visibilitychange', onVisibilityChange)
    return () => {
      cancelled = true
      document.removeEventListener('visibilitychange', onVisibilityChange)
    }
  }, [formId, formIdNum, fallbackFormName])

  if (loading || !formStatus) return null
  if (formStatus === 'PUBLISHED') return null

  const isPendingReview = formStatus === 'PENDING_REVIEW'
  const isApprovedForPublish = formStatus === 'APPROVED_FOR_PUBLISH'
  const needsApproval =
    requireApproval ||
    (formCostThreshold != null && deploymentCost > formCostThreshold)
  const canRequestPublish = !isCompanyAdmin && needsApproval && !isPendingReview && !isApprovedForPublish
  const canDirectPublish = (isCompanyAdmin || !needsApproval) && !isPendingReview
  const isReadyToPublish = readiness?.canPublish ?? false

  if (isPendingReview && !isCompanyAdmin) {
    return (
      <span className="px-3 py-1.5 text-sm font-medium text-amber-700 bg-amber-100 rounded-md">
        Pending Admin Review
      </span>
    )
  }

  if (isApprovedForPublish && !isCompanyAdmin) {
    return (
      <span className="px-3 py-1.5 text-sm font-medium text-teal-700 bg-teal-100 rounded-md">
        Approved — Ready to Publish
      </span>
    )
  }

  if (canRequestPublish) {
    const notReadyMessage = !isReadyToPublish && readiness?.message
      ? readiness.message
      : 'Complete required test runs to request publish'
    return (
      <>
        <div className="relative group">
          <button
            type="button"
            onClick={() => isReadyToPublish && setShowRequestModal(true)}
            disabled={!isReadyToPublish}
            className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
            title={!isReadyToPublish ? notReadyMessage : 'Request that a Company Admin publish this form'}
          >
            <Send size={16} /> Request Publish
          </button>
          {!isReadyToPublish && (
            <div className="absolute bottom-full left-0 mb-1 px-2 py-1.5 text-xs text-white bg-gray-800 rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 max-w-xs">
              {notReadyMessage}
            </div>
          )}
        </div>
        {showRequestModal && (
          <RequestPublishModal
            formId={formIdNum}
            formName={formName || 'Form'}
            onClose={() => setShowRequestModal(false)}
            onSuccess={() => window.location.reload()}
          />
        )}
      </>
    )
  }

  if (canDirectPublish) {
    const notReadyMessage = !isReadyToPublish && readiness?.message
      ? readiness.message
      : 'Complete required test runs to publish'
    return (
      <>
        <div className="relative group">
          <button
            type="button"
            onClick={() => isReadyToPublish && setShowPublishModal(true)}
            disabled={!isReadyToPublish}
            className="btn-primary text-sm py-1.5 px-3 flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
            title={!isReadyToPublish ? notReadyMessage : 'Publish this form'}
          >
            <Upload size={16} /> Publish
          </button>
          {!isReadyToPublish && (
            <div className="absolute bottom-full left-0 mb-1 px-2 py-1.5 text-xs text-white bg-gray-800 rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 max-w-xs">
              {notReadyMessage}
            </div>
          )}
        </div>
        {showPublishModal && (
          <DirectPublishModal
            formId={formIdNum}
            formName={formName || 'Form'}
            hasEvent={hasEvent}
            onClose={() => setShowPublishModal(false)}
            onSuccess={() => window.location.reload()}
          />
        )}
      </>
    )
  }

  return null
}
