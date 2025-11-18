/**
 * Edit Form Modal - Story 2.8
 * Form edit form with all fields
 */

import React, { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { updateForm, getForm, getFormStatuses, getFormApprovalStatuses } from '../api/formsApi'
// Note: Form Status and Approval Status are kept for edit as they can change through approval workflow
import { Form, FormUpdateRequest, FormStatus, FormApprovalStatus } from '../types/form.types'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'
import { EnhancedFormInput } from '../../ux/components/EnhancedFormInput'

interface EditFormModalProps {
  isOpen: boolean
  form: Form | null
  onClose: () => void
  onSuccess: () => void
}

export function EditFormModal({ isOpen, form, onClose, onSuccess }: EditFormModalProps) {
  const [formData, setFormData] = useState<FormUpdateRequest>({})
  const [formStatuses, setFormStatuses] = useState<FormStatus[]>([])
  const [formApprovalStatuses, setFormApprovalStatuses] = useState<FormApprovalStatus[]>([])
  const [isLoadingRefData, setIsLoadingRefData] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const toast = useToastNotifications()

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
        // Non-editable fields (isPublic, deploymentCost, formThumbnailUrl, formPreviewUrl) are auto-managed
        setFormData({
          formName: freshForm.formName ?? '',
          formDescription: freshForm.formDescription ?? null,
          eventId: freshForm.eventId ?? null,
          formStatusId: freshForm.formStatusId !== undefined && freshForm.formStatusId !== null ? freshForm.formStatusId : undefined,
          formApprovalStatusId: freshForm.formApprovalStatusId !== undefined && freshForm.formApprovalStatusId !== null ? freshForm.formApprovalStatusId : undefined,
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
              <LoadingSpinner size="medium" />
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
                      .map((status) => (
                        <option key={status.formStatusId} value={status.formStatusId}>
                          {status.statusName}
                        </option>
                      ))
                  )}
                </select>
              </div>

              {/* Form Approval Status */}
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
              </div>

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

