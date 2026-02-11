/**
 * Create Form Modal - Story 2.8
 * Simplified form creation - only Form Name and Description
 * Form Status defaults to Draft, Approval Status based on user role
 */

import React, { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { createForm } from '../api/formsApi'
import { FormCreateRequest } from '../types/form.types'
import { useToastNotifications } from '../../ux'
import { EnhancedFormInput } from '../../ux/components/EnhancedFormInput'

interface CreateFormModalProps {
  isOpen: boolean
  eventId: number | null // Story 2.8: Form must be created in context of an Event
  userRole?: 'Company Admin' | 'Company User' | 'Company Viewer' // User role to determine approval status
  onClose: () => void
  onSuccess: () => void
}

export function CreateFormModal({ isOpen, eventId, userRole = 'Company User', onClose, onSuccess }: CreateFormModalProps) {
  const [formData, setFormData] = useState<FormCreateRequest>({
    formName: '',
    formDescription: null,
    eventId: eventId || null,
    // Defaults set automatically:
    // Form Status: Always Draft (ID 1)
    // Approval Status: Always No Approval Required (ID 1) - Logic handles transition to Pending later if needed
    formStatusId: 1, // Draft
    formApprovalStatusId: 1, // No Approval Required
  })
  
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const toast = useToastNotifications()

  // Update eventId and approval status when props change
  useEffect(() => {
    if (eventId !== null) {
      setFormData(prev => ({ 
        ...prev, 
        eventId,
        formApprovalStatusId: 1
      }))
    }
  }, [eventId, userRole])

  // Reset form when modal closes
  useEffect(() => {
    if (!isOpen) {
      setFormData({
        formName: '',
        formDescription: null,
        eventId: eventId || null,
        formStatusId: 1, // Draft
        formApprovalStatusId: 1, // No Approval Required
      })
      setErrors({})
    }
  }, [isOpen, eventId, userRole])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    // Validation
    const newErrors: Record<string, string> = {}
    if (!formData.formName.trim()) {
      newErrors.formName = 'Form name is required'
    }
    if (!formData.eventId || formData.eventId === 0) {
      newErrors.eventId = 'Event is required. Forms must be created in the context of an event.'
    }
    if (formData.deploymentCost !== undefined && formData.deploymentCost !== null && formData.deploymentCost < 0) {
        newErrors.deploymentCost = 'Cost cannot be negative'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsSubmitting(true)
    try {
      await createForm(formData)
      toast.success('Form created successfully', 'Success')
      onSuccess()
      onClose() // Close modal after successful creation
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create form'
      toast.error(errorMessage, 'Error creating form')
      setErrors({ submit: errorMessage })
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4 flex items-center justify-between">
          <h2 className="text-2xl font-bold">Create Form</h2>
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
          <div className="space-y-4">
            {/* Form Name */}
            <EnhancedFormInput
              name="formName"
              label="Form Name"
              value={formData.formName}
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
                value={formData.formDescription || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, formDescription: e.target.value || null }))}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                placeholder="Optional description for this form"
              />
            </div>

            {/* Deployment Cost */}
            <div className="grid grid-cols-2 gap-4">
              <EnhancedFormInput
                name="deploymentCost"
                label="Deployment Cost ($)"
                type="text"
                value={formData.deploymentCost !== undefined && formData.deploymentCost !== null ? String(formData.deploymentCost) : ''}
                onChange={(value) => setFormData(prev => ({ ...prev, deploymentCost: value === '' ? null : Number(value) }))}
                error={errors.deploymentCost}
                placeholder="0.00"
              />
              
              {/* Placeholder for other fields if needed */}
              <div />
            </div>

            {errors.submit && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600">{errors.submit}</p>
              </div>
            )}
          </div>
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
            disabled={isSubmitting}
            className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Creating...' : 'Create Form'}
          </button>
        </div>
      </div>
    </div>
  )
}

