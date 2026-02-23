/**
 * Form Detail View - Story 2.8
 * Displays complete form information in a detailed view
 * Story 2.13: Added audit report link for admins
 */

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { FileText, Calendar, Edit2, Trash2, ArrowLeft, X, DollarSign, BarChart3, Shield, Send, CheckCircle, XCircle, ClipboardList, ExternalLink } from 'lucide-react'
import { Form } from '../types/form.types'
import { FormStatusBadge } from './FormStatusBadge'
import { ReadinessBadge } from './ReadinessBadge'
import { FormAccessControlModal } from './FormAccessControlModal'
import { ApprovalRequestModal } from './ApprovalRequestModal'
import { checkFormAccess } from '../api/formAccessApi'
import { approveForm, rejectForm, updateForm, getForm, getFormReadiness, recordTestRun, createPreviewLink, getCompanyTestConfig } from '../api/formsApi'
import type { FormReadiness } from '../api/formsApi'
import { RequestPublishModal } from './RequestPublishModal'
import { DirectPublishModal } from './DirectPublishModal'
import { PublishWorkflowStatus } from './PublishWorkflowStatus'
import { AccessCheckResponse } from '../types/form-access.types'
import { useAuth } from '../../auth/context/AuthContext'
import { useToastNotifications } from '../../ux'
import { FormAuditReport } from '../../audit'

interface FormDetailViewProps {
  form: Form | null
  onClose: () => void
  onEdit: (form: Form) => void
  onDelete: (form: Form) => void
}

export function FormDetailView({ form, onClose, onEdit, onDelete }: FormDetailViewProps) {
  const { user } = useAuth()
  const toast = useToastNotifications()
  const [userAccess, setUserAccess] = useState<AccessCheckResponse | null>(null)
  const [, setIsLoadingAccess] = useState(false)
  const [showAccessControl, setShowAccessControl] = useState(false)
  const [showApprovalRequest, setShowApprovalRequest] = useState(false)
  const [showAuditReport, setShowAuditReport] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [readiness, setReadiness] = useState<FormReadiness | null>(null)
  const [readinessLoading, setReadinessLoading] = useState(false)
  const [requirePublishApproval, setRequirePublishApproval] = useState(false)
  const [formCostThreshold, setFormCostThreshold] = useState<number | null>(null)
  const [showRequestPublishModal, setShowRequestPublishModal] = useState(false)
  const [showDirectPublishModal, setShowDirectPublishModal] = useState(false)
  const [displayForm, setDisplayForm] = useState<Form | null>(null)

  useEffect(() => {
    if (form) {
      getForm(form.formId).then(setDisplayForm).catch(() => setDisplayForm(form))
      loadUserAccess()
      loadReadiness()
      getCompanyTestConfig().then((c) => {
        setRequirePublishApproval(c.requirePublishApproval)
        setFormCostThreshold(c.formCostThreshold)
      }).catch(() => {})

      // Refresh readiness when user returns from preview tab (Phase 1.1g)
      const onVisibilityChange = () => {
        if (document.visibilityState === 'visible') {
          loadReadiness()
          getForm(form.formId).then(setDisplayForm).catch(() => {})
        }
      }
      document.addEventListener('visibilitychange', onVisibilityChange)
      return () => document.removeEventListener('visibilitychange', onVisibilityChange)
    } else {
      setDisplayForm(null)
    }
  }, [form])

  const loadUserAccess = async () => {
    if (!form) return
    try {
      setIsLoadingAccess(true)
      const access = await checkFormAccess(form.formId)
      setUserAccess(access)
    } catch (err) {
      console.error('Failed to check form access:', err)
    } finally {
      setIsLoadingAccess(false)
    }
  }

  const loadReadiness = async () => {
    if (!form) return
    try {
      setReadinessLoading(true)
      const r = await getFormReadiness(form.formId)
      setReadiness(r)
    } catch (err) {
      console.error('Failed to load readiness:', err)
      setReadiness(null)
    } finally {
      setReadinessLoading(false)
    }
  }

  const handleRecordTestRun = async () => {
    if (!form) return
    try {
      setIsProcessing(true)
      await recordTestRun(form.formId)
      toast.success('Test run recorded', 'Success')
      loadReadiness()
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to record test run'
      toast.error(msg, 'Error')
    } finally {
      setIsProcessing(false)
    }
  }

  /** Open form in preview so user can complete a real test submission (fills + submits). */
  const handleOpenPreview = async () => {
    if (!form) return
    try {
      setIsProcessing(true)
      const previewUrl = await createPreviewLink(form.formId)
      window.open(previewUrl, '_blank', 'noopener,noreferrer')
      toast.success('Preview opened in new tab. Complete and submit the form to count as a test run.', 'Info')
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to open preview'
      toast.error(msg, 'Error')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleSubmitForApproval = async () => {
    if (!form) return

    // Smart Publish / Interception Logic (cost gate from company config)
    const threshold = formCostThreshold ?? 100
    const currentCost = form.deploymentCost ?? 0

    if (threshold != null && currentCost > threshold) {
        // Admin Bypass Logic
        if (isCompanyAdmin) {
             if (!confirm(`Warning: This form's deployment cost ($${currentCost}) exceeds the company threshold ($${threshold}).\n\nAs an Administrator, you can publish this immediately without approval.\n\nProceed to Publish?`)) {
                return
             }
             
             try {
                setIsProcessing(true)
                // 1. Pre-approve (sets status to APPROVED)
                await approveForm(form.formId)
                // 2. Publish (sets status to PUBLISHED)
                // Note: updateForm will pass the guard because approval status is now APPROVED
                await updateForm(form.formId, { formStatusId: 3 }) 
                alert('Form Published Successfully')
                onClose()
                window.location.reload()
             } catch (err: unknown) {
                 console.error(err)
                 alert(err instanceof Error ? err.message : 'Failed to publish form')
             } finally {
                 setIsProcessing(false)
             }
             return
        }

        // Standard User Logic
        setShowApprovalRequest(true)
    } else {
        // Low cost form - Auto-publish
        if (!confirm('Publish this form?')) return
        
        try {
          setIsProcessing(true)
          // ID 3 = PUBLISHED (based on seed data)
          await updateForm(form.formId, { formStatusId: 3 })
          alert('Form published')
          onClose()
          window.location.reload()
        } catch (err: unknown) {
           console.error('Failed to publish:', err)
           alert(err instanceof Error ? err.message : 'Failed to publish form')
        } finally {
           setIsProcessing(false)
        }
    }
  }

  const handleApprove = async () => {
    if (!form) return
    if (!confirm('Approve this form?')) return

    try {
      setIsProcessing(true)
      await approveForm(form.formId)
      alert('Form approved')
      // Force a reload of the dashboard/list if possible, or assume onClose will trigger refetch in parent
      // Since we can't control parent refetch easily without context, ensure parent handles onClose by refetching.
      onClose()
      // Optional: reload page if simple
      window.location.reload() 
    } catch (err) {
      console.error('Failed to approve:', err)
      alert('Failed to approve form')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReject = async () => {
    if (!form) return
    const reason = prompt('Enter rejection reason:')
    if (!reason) return

    try {
      setIsProcessing(true)
      await rejectForm(form.formId, reason)
      alert('Form rejected')
      onClose()
    } catch (err) {
      console.error('Failed to reject:', err)
      alert('Failed to reject form')
    } finally {
      setIsProcessing(false)
    }
  }

  if (!form) return null

  const effectiveForm = displayForm ?? form

  // Determine if user is Admin (Company Admin or System Admin)
  const isCompanyAdmin = user?.role === 'company_admin' || user?.role === 'system_admin'

  const canManage = userAccess?.accessLevel === 'MANAGE'
  const canEdit = canManage || userAccess?.accessLevel === 'EDIT'

  // Story 5.6/5.8: Pending Review and Approved for Publish status
  const isPendingReview = effectiveForm.formStatus?.statusCode === 'PENDING_REVIEW'
  const isApprovedForPublish = effectiveForm.formStatus?.statusCode === 'APPROVED_FOR_PUBLISH'

  // Approval Logic
  const cost = effectiveForm.deploymentCost || 0
  const isPending = effectiveForm.formApprovalStatus?.approvalStatusCode === 'PENDING'
  const isNoApproval = effectiveForm.formApprovalStatus?.approvalStatusCode === 'NO_APPROVAL' || !effectiveForm.formApprovalStatus
  const isRejected = effectiveForm.formApprovalStatus?.approvalStatusCode === 'REJECTED'
  
  // Show Submit if: Can Edit AND (No Approval OR Rejected) AND Cost > 100
  // Note: Now mostly handled by auto-trigger on Publish attempt, but keeping explicit submit 
  // for manual workflow if draft status persists or retry needed.
  // Updated requirement: Button should be "Publish" which triggers check, but Detail view 
  // often shows "Submit" as specific action for Drafts.
  // Let's align with Smart Publish: Detail View shouldn't show "Submit" separately if we want 
  // user to click "Publish" to trigger it. 
  // However, we agreed to replace "Submit" with "Publish" logic or keep Submit if blocked.
  // In DetailView, we usually just show actions. 
  // Let's HIDE explicit "Submit for Approval" button and rely on "Publish" action (if we added one here)
  // OR keep "Submit for Approval" as the fallback manual way if auto-trigger failed or for re-submission.
  // Actually, Scenario 2.4 says: "Publish button is disabled/hidden" -> "Submit" is shown?
  // No, Scenario 2.2 says User clicks "Publish". 
  // If DetailView doesn't have a "Publish" button (it has Edit/Delete), then where do they Publish?
  // Usually Publish is an Edit action (changing status).
  // BUT, high cost forms MIGHT need a dedicated "Submit" button if they can't change status in Edit.
  
  // Let's stick to the "Smart Publish" flow where changing status triggers it.
  // BUT we need a way to trigger it from Detail View if Edit is blocked.
  // Let's show a "Publish" button here for Owners that triggers the check.
  
  // Unified approval: needsApproval = RequirePublishApproval OR (FormCostThreshold set AND cost > threshold)
  const needsApproval =
    requirePublishApproval ||
    (formCostThreshold != null && (cost ?? 0) > formCostThreshold)
  // Show "Publish" (Request Approval) if: Draft/Rejected, Cost > threshold (when threshold set), Can Edit
  const showSmartPublish =
    canEdit &&
    (isNoApproval || isRejected) &&
    formCostThreshold != null &&
    cost > formCostThreshold

  // Story 5.6 + Unified: Request Publish when Company User + needsApproval + not already pending
  const showRequestPublish =
    !isCompanyAdmin &&
    needsApproval &&
    canEdit &&
    (isNoApproval || isRejected) &&
    effectiveForm.formStatus?.statusCode !== 'PUBLISHED' &&
    !isPendingReview &&
    !isApprovedForPublish

  const requestPublishDisabled = !(readiness?.canPublish ?? false)
  const requestPublishTooltip = requestPublishDisabled && readiness?.message
    ? readiness.message
    : undefined

  // Story 5.8 + Unified: Direct Publish when Admin or !needsApproval
  const showDirectPublish =
    (isCompanyAdmin || !needsApproval) &&
    canEdit &&
    (isNoApproval || isRejected) &&
    effectiveForm.formStatus?.statusCode !== 'PUBLISHED' &&
    !isPendingReview &&
    !isApprovedForPublish
  const directPublishDisabled = !(readiness?.canPublish ?? false)
  const directPublishTooltip = directPublishDisabled && readiness?.message ? readiness.message : undefined
  
  // Show Approve/Reject ONLY if: User is Admin AND Form is Pending
  // PRE-APPROVAL: Also show if Draft (No Approval) AND Cost > 100 (Scenario 4)
  // HIDE if current user is the owner (Self-approval handled via Publish)
  const isOwner = user?.id === effectiveForm.createdBy
  const showDecision =
    isCompanyAdmin &&
    !isOwner &&
    (isPending || (isNoApproval && formCostThreshold != null && cost > formCostThreshold))

  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'Never'
    try {
      return new Intl.DateTimeFormat('en-AU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(new Date(dateString))
    } catch {
      return new Date(dateString).toLocaleString('en-AU')
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div
        className="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden transform transition-all"
        role="dialog"
        aria-modal="true"
        aria-labelledby="form-detail-title"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={onClose}
                className="text-white hover:text-gray-200 p-1 rounded transition-colors"
                aria-label="Close detail view"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <h2 id="form-detail-title" className="text-2xl font-bold">
                Form Details
              </h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 p-1 rounded transition-colors"
              aria-label="Close modal"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-180px)] p-6">
          {/* Form Name and Status */}
          <div className="mb-6 pb-6 border-b border-gray-200">
            <div className="flex items-start justify-between gap-4 mb-3">
              <h3 className="text-3xl font-bold text-gray-900 flex-1">
                {effectiveForm.formName}
              </h3>
              <FormStatusBadge status={effectiveForm.formStatus} approvalStatus={effectiveForm.formApprovalStatus} />
            </div>
            {form.formDescription && (
              <p className="text-lg text-gray-600 mt-2">
                {form.formDescription}
              </p>
            )}
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Left Column */}
            <div className="space-y-6">
              {/* Status Information */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <FileText className="w-5 h-5 text-teal-600" />
                  Status
                </h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Form Status:</span>{' '}
                    <span className="text-gray-600">{effectiveForm.formStatus?.statusName || 'Unknown'}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Approval:</span>{' '}
                    <span className="text-gray-600">
                      {needsApproval
                        ? 'Required (publish approval or cost gate)'
                        : form.formApprovalStatus?.approvalStatusName || 'Not required'}
                    </span>
                    {formCostThreshold != null && (
                      <span className="text-xs text-gray-500 ml-1">
                        (cost &gt; ${formCostThreshold} triggers approval)
                      </span>
                    )}
                  </div>
                  {needsApproval && !isCompanyAdmin && (
                    <div>
                      <span className="font-medium text-gray-700">Publish approval:</span>{' '}
                      <span className="text-amber-700 font-medium">Required</span>
                      <span className="text-xs text-gray-500 ml-1">(Company Admin must approve)</span>
                    </div>
                  )}
                  <div>
                    <span className="font-medium text-gray-700">Public Access:</span>{' '}
                    <span className="text-gray-600">{form.isPublic ? 'Yes' : 'No'}</span>
                  </div>
                  {/* Story 5.5: Readiness badge */}
                  <div className="pt-2">
                    <ReadinessBadge
                      readiness={readiness ?? { canPublish: true, testRunCount: 0, testThresholdRequired: 0, testRunsNeeded: 0, message: 'Ready to publish' }}
                      onOpenPreview={canManage ? handleOpenPreview : undefined}
                      onRecordTestRun={canEdit && !canManage ? handleRecordTestRun : undefined}
                      loading={readinessLoading}
                    />
                  </div>
                  {/* Story 5.6 + Unified: Next steps for Company Users */}
                  <PublishWorkflowStatus
                    isCompanyUser={!isCompanyAdmin}
                    requirePublishApproval={needsApproval}
                    formStatusCode={effectiveForm.formStatus?.statusCode ?? null}
                    readiness={readiness}
                    loading={readinessLoading}
                  />
                </div>
              </section>

              {/* Activity Metrics */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-teal-600" />
                  Activity Metrics
                </h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Total Submissions:</span>{' '}
                    <span className="text-gray-600">{effectiveForm.totalSubmissions}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Demo Leads:</span>{' '}
                    <span className="text-gray-600">{form.demoLeadsCollected}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Production Leads:</span>{' '}
                    <span className="text-gray-600">{effectiveForm.productionLeadsCollected}</span>
                  </div>
                  {form.lastSubmissionDate && (
                    <div>
                      <span className="font-medium text-gray-700">Last Submission:</span>{' '}
                      <span className="text-gray-600">{formatDate(form.lastSubmissionDate)}</span>
                    </div>
                  )}
                  {form.lastActivityDate && (
                    <div>
                      <span className="font-medium text-gray-700">Last Activity:</span>{' '}
                      <span className="text-gray-600">{formatDate(form.lastActivityDate)}</span>
                    </div>
                  )}
                </div>
              </section>
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              {/* Deployment Information */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-teal-600" />
                  Deployment
                </h4>
                <div className="space-y-2 text-sm">
                  {form.deploymentCost != null && !Number.isNaN(Number(form.deploymentCost)) && (
                    <div>
                      <span className="font-medium text-gray-700">Deployment Cost:</span>{' '}
                      <span className="text-gray-600">${(Number(form.deploymentCost) || 0).toFixed(2)}</span>
                    </div>
                  )}
                  {form.formThumbnailUrl && (
                    <div>
                      <span className="font-medium text-gray-700">Thumbnail URL:</span>{' '}
                      <a href={form.formThumbnailUrl} target="_blank" rel="noopener noreferrer" className="text-teal-600 hover:underline">
                        View
                      </a>
                    </div>
                  )}
                  {form.formPreviewUrl && (
                    <div>
                      <span className="font-medium text-gray-700">Preview URL:</span>{' '}
                      <a href={form.formPreviewUrl} target="_blank" rel="noopener noreferrer" className="text-teal-600 hover:underline">
                        View
                      </a>
                    </div>
                  )}
                </div>
              </section>

              {/* Audit Trail */}
              <section>
                <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-teal-600" />
                  Audit Trail
                </h4>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Created:</span>{' '}
                    <span className="text-gray-600">{formatDate(form.createdDate)}</span>
                  </div>
                  {form.updatedDate && (
                    <div>
                      <span className="font-medium text-gray-700">Last Updated:</span>{' '}
                      <span className="text-gray-600">{formatDate(form.updatedDate)}</span>
                    </div>
                  )}
                  {/* Full Compliance Report - Only for Admins (Story 2.13) */}
                  {isCompanyAdmin && (
                    <button
                      onClick={() => setShowAuditReport(true)}
                      className="mt-3 px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors flex items-center gap-2"
                    >
                      <ClipboardList className="w-4 h-4" />
                      View Compliance Report
                    </button>
                  )}
                </div>
              </section>

              {/* Access Control Section */}
              {userAccess && (
                <section>
                  <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <Shield className="w-5 h-5 text-teal-600" />
                    Access Control
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">Your Access Level:</span>{' '}
                      <span className="text-gray-600 font-semibold">
                        {userAccess.accessLevel || 'No Access'}
                      </span>
                    </div>
                    {canManage && (
                      <button
                        onClick={() => setShowAccessControl(true)}
                        className="mt-2 px-3 py-1.5 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 transition-colors flex items-center gap-2"
                      >
                        <Shield className="w-4 h-4" />
                        Manage Access
                      </button>
                    )}
                  </div>
                </section>
              )}
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            Close
          </button>

          {/* Story 5.6: Pending Admin Review indicator (Company User) */}
          {isPendingReview && !isCompanyAdmin && (
            <span className="px-4 py-2 text-sm font-medium text-amber-700 bg-amber-100 rounded-md">
              Pending Admin Review
            </span>
          )}

          {/* Story 5.8: Approved for Publish indicator (Company User) */}
          {isApprovedForPublish && !isCompanyAdmin && (
            <span className="px-4 py-2 text-sm font-medium text-teal-700 bg-teal-100 rounded-md">
              Approved — Ready to Publish
            </span>
          )}

          {/* Story 5.6/5.8: Link to FormReviewPage when Admin viewing form in Pending Admin Review or Approved for Publish */}
          {(isPendingReview || isApprovedForPublish) && isCompanyAdmin && form && (
            <Link
              to={`/forms/${form.formId}/review`}
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                isApprovedForPublish
                  ? 'text-teal-800 bg-teal-100 border border-teal-300 hover:bg-teal-200'
                  : 'text-amber-800 bg-amber-100 border border-amber-300 hover:bg-amber-200'
              }`}
            >
              <ExternalLink size={16} />
              Review & Publish
            </Link>
          )}

          {/* Story 5.6: Request Publish (Company User + approval required) */}
          {showRequestPublish && (
            <button
              onClick={() => !requestPublishDisabled && !isProcessing && setShowRequestPublishModal(true)}
              disabled={isProcessing || requestPublishDisabled}
              title={requestPublishTooltip}
              className={`px-4 py-2 text-sm font-medium rounded-md transition-colors flex items-center gap-2 ${
                requestPublishDisabled
                  ? 'text-gray-400 bg-gray-300 cursor-not-allowed'
                  : 'text-white bg-indigo-600 hover:bg-indigo-700'
              }`}
            >
              <Send className="w-4 h-4" />
              Request Publish
            </button>
          )}

          {/* Story 5.8: Direct Publish (when RequirePublishApproval=false or Admin) */}
          {showDirectPublish && (
            <button
              onClick={() => !directPublishDisabled && !isProcessing && setShowDirectPublishModal(true)}
              disabled={isProcessing || directPublishDisabled}
              title={directPublishTooltip}
              className={`px-4 py-2 text-sm font-medium rounded-md transition-colors flex items-center gap-2 ${
                directPublishDisabled
                  ? 'text-gray-400 bg-gray-300 cursor-not-allowed'
                  : 'text-white bg-teal-600 hover:bg-teal-700'
              }`}
            >
              <Send className="w-4 h-4" />
              Publish
            </button>
          )}
          
          {/* Smart Publish Button (when NOT using Request Publish or Direct Publish flow) */}
          {showSmartPublish && !showRequestPublish && !showDirectPublish && (
             <button
               onClick={handleSubmitForApproval}
               disabled={isProcessing}
               className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors flex items-center gap-2"
             >
               <Send className="w-4 h-4" />
               {isCompanyAdmin ? 'Publish' : 'Publish (Request Approval)'}
             </button>
          )}
          
          {/* Admin Decisions */}
          {showDecision && (
            <>
              {/* Only show Reject if it's actually pending or previously approved? No, only pending. */}
              {isPending && (
                  <button
                    onClick={handleReject}
                    disabled={isProcessing}
                    className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors flex items-center gap-2"
                  >
                    <XCircle className="w-4 h-4" />
                    Reject
                  </button>
              )}
              
              <button
                onClick={handleApprove}
                disabled={isProcessing}
                className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 transition-colors flex items-center gap-2"
              >
                <CheckCircle className="w-4 h-4" />
                {isPending ? 'Approve & Publish' : 'Pre-Approve'}
              </button>
            </>
          )}

          {canEdit && (
            <button
              onClick={() => onEdit(effectiveForm)}
              className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 transition-colors flex items-center gap-2"
            >
              <Edit2 className="w-4 h-4" />
              Edit
            </button>
          )}
          {canManage && (
            <button
              onClick={() => onDelete(effectiveForm)}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" />
              Delete
            </button>
          )}
        </div>
      </div>

      {/* Story 5.6: Request Publish Modal */}
      {showRequestPublishModal && form && (
        <RequestPublishModal
          formId={form.formId}
          formName={effectiveForm.formName}
          onClose={() => setShowRequestPublishModal(false)}
          onSuccess={() => {
            onClose()
            window.location.reload()
          }}
        />
      )}

      {/* Story 5.8: Direct Publish Modal */}
      {showDirectPublishModal && form && (
        <DirectPublishModal
          formId={form.formId}
          formName={effectiveForm.formName}
          hasEvent={!!form.eventId}
          onClose={() => setShowDirectPublishModal(false)}
          onSuccess={() => {
            onClose()
            window.location.reload()
          }}
        />
      )}

      {/* Access Control Modal */}
      {showAccessControl && (
        <FormAccessControlModal
          isOpen={showAccessControl}
          formId={form.formId}
          onClose={() => setShowAccessControl(false)}
        />
      )}

      {/* Approval Request Modal */}
      {showApprovalRequest && (
        <ApprovalRequestModal
          isOpen={showApprovalRequest}
          formId={form.formId}
          formName={effectiveForm.formName}
          deploymentCost={form.deploymentCost || 0}
          onClose={() => setShowApprovalRequest(false)}
          onSuccess={() => {
            alert('Approval request sent successfully')
            onClose() // Close detail view
          }}
        />
      )}

      {/* Audit Report Modal (Story 2.13) */}
      {showAuditReport && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-[60] flex items-center justify-center p-4">
          <FormAuditReport 
            formId={form.formId}
            onClose={() => setShowAuditReport(false)}
          />
        </div>
      )}
    </div>
  )
}

