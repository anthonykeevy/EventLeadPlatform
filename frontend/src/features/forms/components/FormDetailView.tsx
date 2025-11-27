/**
 * Form Detail View - Story 2.8
 * Displays complete form information in a detailed view
 * Story 2.13: Added audit report link for admins
 */

import React, { useState, useEffect } from 'react'
import { FileText, Calendar, Edit2, Trash2, ArrowLeft, X, Globe, DollarSign, BarChart3, Shield, Send, CheckCircle, XCircle, ClipboardList } from 'lucide-react'
import { Form } from '../types/form.types'
import { FormStatusBadge } from './FormStatusBadge'
import { FormAccessControlModal } from './FormAccessControlModal'
import { ApprovalRequestModal } from './ApprovalRequestModal'
import { checkFormAccess } from '../api/formAccessApi'
import { submitFormForApproval, approveForm, rejectForm, updateForm } from '../api/formsApi'
import { AccessCheckResponse } from '../types/form-access.types'
import { useAuth } from '../../auth/context/AuthContext'
import { FormAuditReport } from '../../audit'

interface FormDetailViewProps {
  form: Form | null
  onClose: () => void
  onEdit: (form: Form) => void
  onDelete: (form: Form) => void
}

export function FormDetailView({ form, onClose, onEdit, onDelete }: FormDetailViewProps) {
  const { user } = useAuth()
  const [userAccess, setUserAccess] = useState<AccessCheckResponse | null>(null)
  const [isLoadingAccess, setIsLoadingAccess] = useState(false)
  const [showAccessControl, setShowAccessControl] = useState(false)
  const [showApprovalRequest, setShowApprovalRequest] = useState(false)
  const [showAuditReport, setShowAuditReport] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)

  useEffect(() => {
    if (form) {
      loadUserAccess()
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

  const handleSubmitForApproval = async () => {
    if (!form) return
    
    // Smart Publish / Interception Logic
    const threshold = 100
    const currentCost = form.deploymentCost || 0
    
    if (currentCost > threshold) {
        // Admin Bypass Logic
        if (isCompanyAdmin) {
             if (!confirm(`Warning: This form exceeds the deployment cost threshold ($${currentCost}).\n\nAs an Administrator, you can publish this immediately without approval.\n\nProceed to Publish?`)) {
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
             } catch (err) {
                 console.error(err)
                 alert('Failed to publish form')
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
        } catch (err) {
           console.error('Failed to publish:', err)
           alert('Failed to publish form')
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

  // Determine if user is Admin (Company Admin or System Admin)
  const isCompanyAdmin = user?.role === 'company_admin' || user?.role === 'system_admin'

  const canManage = userAccess?.accessLevel === 'MANAGE'
  const canEdit = canManage || userAccess?.accessLevel === 'EDIT'
  const canView = userAccess?.hasAccess || canEdit || canManage

  // Approval Logic
  const cost = form.deploymentCost || 0
  const isPending = form.formApprovalStatus?.approvalStatusCode === 'PENDING'
  const isNoApproval = form.formApprovalStatus?.approvalStatusCode === 'NO_APPROVAL' || !form.formApprovalStatus
  const isRejected = form.formApprovalStatus?.approvalStatusCode === 'REJECTED'
  
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
  
  // Show "Publish" (Request Approval) if: Draft/Rejected, Cost > 100, Can Edit
  const showSmartPublish = canEdit && (isNoApproval || isRejected) && cost > 100
  
  // Show Approve/Reject ONLY if: User is Admin AND Form is Pending
  // PRE-APPROVAL: Also show if Draft (No Approval) AND Cost > 100 (Scenario 4)
  // HIDE if current user is the owner (Self-approval handled via Publish)
  const isOwner = user?.id === form.createdBy
  const showDecision = isCompanyAdmin && !isOwner && (isPending || (isNoApproval && cost > 100))

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
                {form.formName}
              </h3>
              <FormStatusBadge status={form.formStatus} approvalStatus={form.formApprovalStatus} />
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
                    <span className="text-gray-600">{form.formStatus?.statusName || 'Unknown'}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Approval Status:</span>{' '}
                    <span className="text-gray-600">{form.formApprovalStatus?.approvalStatusName || 'Unknown'}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Public Access:</span>{' '}
                    <span className="text-gray-600">{form.isPublic ? 'Yes' : 'No'}</span>
                  </div>
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
                    <span className="text-gray-600">{form.totalSubmissions}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Demo Leads:</span>{' '}
                    <span className="text-gray-600">{form.demoLeadsCollected}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Production Leads:</span>{' '}
                    <span className="text-gray-600">{form.productionLeadsCollected}</span>
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
                  {form.deploymentCost !== null && (
                    <div>
                      <span className="font-medium text-gray-700">Deployment Cost:</span>{' '}
                      <span className="text-gray-600">${Number(form.deploymentCost).toFixed(2)}</span>
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
          
          {/* Smart Publish Button (Replaces manual Submit) */}
          {showSmartPublish && (
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
              onClick={() => onEdit(form)}
              className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 transition-colors flex items-center gap-2"
            >
              <Edit2 className="w-4 h-4" />
              Edit
            </button>
          )}
          {canManage && (
            <button
              onClick={() => onDelete(form)}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" />
              Delete
            </button>
          )}
        </div>
      </div>

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
          formName={form.formName}
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

