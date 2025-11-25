/**
 * Edit Form Modal - Story 2.8
 * Form edit form with all fields
 */

import React, { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { updateForm, getForm, getFormStatuses, getFormApprovalStatuses, submitFormForApproval, approveForm } from '../api/formsApi'
// Note: Form Status and Approval Status are kept for edit as they can change through approval workflow
import { Form, FormUpdateRequest, FormStatus, FormApprovalStatus } from '../types/form.types'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'
import { EnhancedFormInput } from '../../ux/components/EnhancedFormInput'
import { useAuth } from '../../auth/context/AuthContext'

interface EditFormModalProps {
  isOpen: boolean
  form: Form | null
  onClose: () => void
  onSuccess: () => void
}

export function EditFormModal({ isOpen, form, onClose, onSuccess }: EditFormModalProps) {
  const { user } = useAuth()
  const [formData, setFormData] = useState<FormUpdateRequest>({})
  const [formStatuses, setFormStatuses] = useState<FormStatus[]>([])
  const [formApprovalStatuses, setFormApprovalStatuses] = useState<FormApprovalStatus[]>([])
  const [isLoadingRefData, setIsLoadingRefData] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const toast = useToastNotifications()

  // Determine if user is admin
  const isCompanyAdmin = user?.role === 'company_admin' || user?.role === 'system_admin'

  // Helper to check if publish is blocked
  const isPublishBlocked = (cost: number | null, approvalStatusId: number | undefined) => {
    const threshold = 100 // This should ideally come from config, but hardcoded for UI logic matches backend default
    const currentCost = cost || 0
    
    // Find the status object to check code
    const statusObj = formApprovalStatuses.find(s => s.formApprovalStatusId === approvalStatusId)
    // Block if cost > threshold AND NOT Approved
    // Note: If statusObj is undefined (loading), we assume blocked if high cost just in case, 
    // but typically we wait for loading.
    const isApproved = statusObj?.approvalStatusCode === 'APPROVED'
    
    return currentCost > threshold && !isApproved
  }

  // Load form data and reference data
  useEffect(() => {
    if (!isOpen || !form) {
      // Reset form data when modal closes
      setFormData({})
      setFormStatuses([])
      setFormApprovalStatuses([])
      return
    }

    const loadData = async () => {
      setIsLoadingRefData(true)
      setErrors({})
      try {
        // Fetch fresh form data from API to ensure we have the latest data
        const [freshForm, statuses, approvalStatuses] = await Promise.all([
          getForm(form.formId),
          getFormStatuses(),
          getFormApprovalStatuses()
        ])
        setFormStatuses(statuses)
        setFormApprovalStatuses(approvalStatuses)
        
          // Initialize form data with editable fields only
        // Non-editable fields (isPublic, formThumbnailUrl, formPreviewUrl) are auto-managed
        // deploymentCost is now editable for Approval Workflow testing (Story 2.11)
        setFormData({
          formName: freshForm.formName ?? '',
          formDescription: freshForm.formDescription ?? null,
          eventId: freshForm.eventId ?? null,
          formStatusId: freshForm.formStatusId !== undefined && freshForm.formStatusId !== null ? freshForm.formStatusId : undefined,
          formApprovalStatusId: freshForm.formApprovalStatusId !== undefined && freshForm.formApprovalStatusId !== null ? freshForm.formApprovalStatusId : undefined,
          deploymentCost: freshForm.deploymentCost,
        })
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load form data'
        toast.error(errorMessage, 'Failed to load form')
        setErrors({ submit: errorMessage })
      } finally {
        setIsLoadingRefData(false)
      }
    }

    loadData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, form?.formId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form) return

    setErrors({})

    // Validation
    const newErrors: Record<string, string> = {}
    if (formData.formName !== undefined && !formData.formName.trim()) {
      newErrors.formName = 'Form name is required'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    // Check Smart Publish / Interception Logic
    const currentCost = formData.deploymentCost !== undefined ? formData.deploymentCost : form.deploymentCost
    const currentStatusId = formData.formStatusId !== undefined ? formData.formStatusId : form.formStatusId
    const currentApprovalStatusId = formData.formApprovalStatusId !== undefined ? formData.formApprovalStatusId : form.formApprovalStatusId

    // Find if user is trying to set to PUBLISHED
    // ID 3 = PUBLISHED (based on seed data)
    // OR better, find the status code from formStatuses
    const targetStatus = formStatuses.find(s => s.formStatusId === currentStatusId)
    const isTargetingPublished = targetStatus?.statusCode === 'PUBLISHED'
    
    // Check if blocked
    const blocked = isTargetingPublished && isPublishBlocked(currentCost, currentApprovalStatusId)

    if (blocked) {
        // Admin Bypass Logic
        if (isCompanyAdmin) {
             if (!confirm(`Warning: This form exceeds the deployment cost threshold ($${currentCost}).\n\nAs an Administrator, you can publish this immediately without approval.\n\nProceed to Publish?`)) {
                return
             }
             
             setIsSubmitting(true)
             try {
                 // 1. Pre-approve (sets status to APPROVED)
                 await approveForm(form.formId)
                 
                 // 2. Update Form (including status=Published)
                 // Filter out undefined values
                 const updateData: FormUpdateRequest = Object.fromEntries(
                    Object.entries(formData).filter(([_, value]) => value !== undefined)
                 ) as FormUpdateRequest
                 
                 await updateForm(form.formId, updateData)
                 toast.success('Form Published Successfully', 'Success')
                 onSuccess()
                 onClose()
             } catch (err) {
                  const errorMessage = err instanceof Error ? err.message : 'Failed to publish form'
                  toast.error(errorMessage, 'Error')
                  setErrors({ submit: errorMessage })
             } finally {
                 setIsSubmitting(false)
             }
             return
        }

        // Standard User Logic: Show confirmation and submit request
        if (!confirm(`Form requires approval based on your company's policy and will be sent to Company Admins for approval.\n\nSend Request?`)) {
            return
        }

        setIsSubmitting(true)
        try {
          // 1. Save changes first (EXCEPT status change to Published)
          const updateData: FormUpdateRequest = Object.fromEntries(
            Object.entries(formData).filter(([key, value]) => value !== undefined && key !== 'formStatusId')
          ) as FormUpdateRequest
          
          // If user changed status to Published, we need to revert it to original (or keep as is)
          // If user didn't change status, it wouldn't be in formData (undefined)
          // If user changed it, we excluded it above.
          // But wait, if the form WAS Draft, and they changed to Published, we update everything else.
          
          if (Object.keys(updateData).length > 0) {
             await updateForm(form.formId, updateData)
          }
          
          // 2. Trigger submission (sets status to Pending)
          await submitFormForApproval(form.formId)
          
          toast.success('Request sent to Company Admins', 'Success')
          onSuccess()
          onClose()
        } catch (err) {
          const errorMessage = err instanceof Error ? err.message : 'Failed to submit request'
          toast.error(errorMessage, 'Error')
          setErrors({ submit: errorMessage })
        } finally {
          setIsSubmitting(false)
        }
        return
    }

    setIsSubmitting(true)
    try {
      // Filter out undefined values to avoid type issues
      const updateData: FormUpdateRequest = Object.fromEntries(
        Object.entries(formData).filter(([_, value]) => value !== undefined)
      ) as FormUpdateRequest
      
      await updateForm(form.formId, updateData)
      toast.success('Form updated successfully', 'Success')
      onSuccess()
      onClose() // Close modal after successful update
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update form'
      toast.error(errorMessage, 'Error updating form')
      setErrors({ submit: errorMessage })
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen || !form) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4 flex items-center justify-between">
          <h2 className="text-2xl font-bold">Edit Form</h2>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 p-1 rounded transition-colors"
            aria-label="Close modal"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <form onSubmit={handleSubmit} className="overflow-y-auto max-h-[calc(90vh-180px)] p-6">
          {isLoadingRefData ? (
            <div className="flex justify-center py-8">
              <LoadingSpinner size="md" />
            </div>
          ) : (
            <div className="space-y-4">
              {/* Form Name */}
              <EnhancedFormInput
                name="formName"
                label="Form Name"
                value={formData.formName || form.formName}
                onChange={(value) => setFormData(prev => ({ ...prev, formName: value }))}
                error={errors.formName}
                required
                maxLength={200}
              />

              {/* Form Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={formData.formDescription !== undefined ? (formData.formDescription || '') : (form.formDescription || '')}
                  onChange={(e) => setFormData(prev => ({ ...prev, formDescription: e.target.value || null }))}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                />
              </div>

              {/* Deployment Cost */}
              <div className="grid grid-cols-2 gap-4">
                <EnhancedFormInput
                  name="deploymentCost"
                  label="Deployment Cost ($)"
                  type="text" // EnhancedFormInput expects text/password/etc, using text for number with casting
                  value={formData.deploymentCost !== undefined && formData.deploymentCost !== null ? String(formData.deploymentCost) : ''}
                  onChange={(value) => setFormData(prev => ({ ...prev, deploymentCost: value === '' ? null : Number(value) }))}
                  error={errors.deploymentCost}
                  // min/step props need to be handled via other props or custom validation if EnhancedFormInput doesn't support them directly
                  // Assuming EnhancedFormInput passes unknown props down to input
                  {...({ min: 0, step: 0.01, placeholder: "0.00" })}
                  disabled={!isCompanyAdmin} // Read-only for non-admins per Scenario 6.3
                />
                <div />
              </div>

              {/* Form Status */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Form Status
                </label>
                <select
                  value={formData.formStatusId !== undefined ? formData.formStatusId : (form.formStatusId ?? 0)}
                  onChange={(e) => setFormData(prev => ({ ...prev, formStatusId: Number(e.target.value) }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
                  {formStatuses.length === 0 ? (
                    <option value={0}>Loading statuses...</option>
                  ) : (
                    formStatuses
                      .filter(status => status.statusCode !== 'DELETED' && status.statusCode !== 'ARCHIVED')
                      .map((status) => {
                        // Smart Publish: Enable PUBLISHED even if blocked, but interception logic handles it
                        const isPublishedOption = status.statusCode === 'PUBLISHED'
                        const blocked = isPublishedOption && isPublishBlocked(
                          formData.deploymentCost !== undefined ? formData.deploymentCost : form.deploymentCost,
                          formData.formApprovalStatusId !== undefined ? formData.formApprovalStatusId : form.formApprovalStatusId
                        )
                        
                        let suffix = ''
                        if (blocked) {
                             suffix = isCompanyAdmin ? ' (High Cost - Admin Bypass)' : ' (Request Approval)'
                        }

                        return (
                          <option key={status.formStatusId} value={status.formStatusId}>
                            {status.statusName}{suffix}
                          </option>
                        )
                      })
                  )}
                </select>
                {/* Helper Text for Blocked Publish */}
                {isPublishBlocked(
                  formData.deploymentCost !== undefined ? formData.deploymentCost : form.deploymentCost,
                  formData.formApprovalStatusId !== undefined ? formData.formApprovalStatusId : form.formApprovalStatusId
                ) && (
                  <p className="text-xs text-blue-600 mt-1">
                    Selecting Published will trigger an approval request.
                  </p>
                )}
              </div>

              {/* Approval Status - Only visible to Admins */}
              {isCompanyAdmin && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Approval Status
                  </label>
                  <select
                    value={formData.formApprovalStatusId !== undefined ? formData.formApprovalStatusId : (form.formApprovalStatusId ?? 0)}
                    onChange={(e) => setFormData(prev => ({ ...prev, formApprovalStatusId: Number(e.target.value) }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  >
                    {formApprovalStatuses.length === 0 ? (
                      <option value={0}>Loading approval statuses...</option>
                    ) : (
                      formApprovalStatuses.map((status) => (
                        <option key={status.formApprovalStatusId} value={status.formApprovalStatusId}>
                          {status.approvalStatusName}
                        </option>
                      ))
                    )}
                  </select>
                  <p className="text-xs text-gray-500 mt-1">Admin Override: You can manually set approval status here.</p>
                </div>
              )}

              {errors.submit && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{errors.submit}</p>
                </div>
              )}
            </div>
          )}
        </form>

        {/* Footer */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting || isLoadingRefData}
            className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Updating...' : 'Update Form'}
          </button>
        </div>
      </div>
    </div>
  )
}

