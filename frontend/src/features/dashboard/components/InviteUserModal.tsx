/**
 * Invite User Modal - Story 1.16
 * AC-1.16.2: Invite User Modal
 * AC-1.16.5: Form validation
 */

import React, { useState, useCallback } from 'react'
import { X, Mail, User, UserPlus, AlertCircle } from 'lucide-react'
import { inviteUser } from '../api/teamApi'
import type { InviteUserRequest } from '../types/team.types'

interface InviteUserModalProps {
  companyId: number
  companyName: string
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export function InviteUserModal({
  companyId,
  companyName,
  isOpen,
  onClose,
  onSuccess
}: InviteUserModalProps) {
  const [formData, setFormData] = useState<InviteUserRequest>({
    email: '',
    firstName: '',
    lastName: '',
    role: 'company_user'
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const validateForm = useCallback(() => {
    const newErrors: Record<string, string> = {}

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email address'
    }

    // First name validation
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required'
    } else if (formData.firstName.trim().length < 2) {
      newErrors.firstName = 'First name must be at least 2 characters'
    }

    // Last name validation
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required'
    } else if (formData.lastName.trim().length < 2) {
      newErrors.lastName = 'Last name must be at least 2 characters'
    }

    // Role validation
    if (!formData.role) {
      newErrors.role = 'Role is required'
    } else if (!['company_admin', 'company_user'].includes(formData.role)) {
      newErrors.role = 'Invalid role selected'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }, [formData])

  const handleChange = useCallback((field: keyof InviteUserRequest, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error for this field when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
    // Clear submit error when user changes any field
    if (submitError) {
      setSubmitError(null)
    }
  }, [errors, submitError])

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitError(null)

    // Validate form
    if (!validateForm()) {
      return
    }

    setIsSubmitting(true)

    try {
      const response = await inviteUser(companyId, formData)
      
      if (response.success) {
        // Success! Reset form and close modal
        setFormData({
          email: '',
          firstName: '',
          lastName: '',
          role: 'company_user'
        })
        setErrors({})
        onSuccess()
        onClose()
      }
    } catch (error: any) {
      console.error('Failed to invite user:', error)
      
      // Handle specific error messages from backend
      if (error.response?.data?.detail) {
        // Handle both string and object detail formats
        const detail = error.response.data.detail
        if (typeof detail === 'string') {
          setSubmitError(detail)
        } else if (Array.isArray(detail)) {
          // Pydantic validation errors are arrays
          const errorMessages = detail.map((err: any) => err.msg).join(', ')
          setSubmitError(`Validation error: ${errorMessages}`)
        } else if (typeof detail === 'object') {
          setSubmitError(JSON.stringify(detail))
        } else {
          setSubmitError('Validation error occurred')
        }
      } else if (error.response?.status === 400) {
        setSubmitError('This email may already be in the company or have a pending invitation')
      } else if (error.response?.status === 403) {
        setSubmitError('You do not have permission to invite users')
      } else if (error.response?.status === 422) {
        setSubmitError('Invalid form data. Please check all fields.')
      } else {
        setSubmitError('Failed to send invitation. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }, [companyId, formData, validateForm, onSuccess, onClose])

  const handleClose = useCallback(() => {
    // Reset form when closing
    setFormData({
      email: '',
      firstName: '',
      lastName: '',
      role: 'company_user'
    })
    setErrors({})
    setSubmitError(null)
    onClose()
  }, [onClose])

  if (!isOpen) return null

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
        onClick={handleClose}
      >
        {/* Modal - AC-1.16.2: Invite User Modal */}
        <div
          className="bg-white rounded-lg shadow-2xl w-full max-w-md transform transition-all"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="bg-teal-600 text-white px-6 py-4 rounded-t-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <UserPlus className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Invite User</h2>
              </div>
              <button
                onClick={handleClose}
                className="text-white hover:text-gray-200 p-1 rounded"
                aria-label="Close"
                disabled={isSubmitting}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <p className="text-teal-100 text-sm mt-1">{companyName}</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            {/* Submit Error */}
            {submitError && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded flex items-start gap-2">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <span className="text-sm">{submitError}</span>
              </div>
            )}

            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email Address *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="email"
                  id="email"
                  value={formData.email}
                  onChange={(e) => handleChange('email', e.target.value)}
                  className={`block w-full pl-10 pr-3 py-2 border ${
                    errors.email ? 'border-red-300' : 'border-gray-300'
                  } rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500`}
                  placeholder="user@example.com"
                  disabled={isSubmitting}
                />
              </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            {/* First Name Field */}
            <div>
              <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                First Name *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  id="firstName"
                  value={formData.firstName}
                  onChange={(e) => handleChange('firstName', e.target.value)}
                  className={`block w-full pl-10 pr-3 py-2 border ${
                    errors.firstName ? 'border-red-300' : 'border-gray-300'
                  } rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500`}
                  placeholder="John"
                  disabled={isSubmitting}
                />
              </div>
              {errors.firstName && (
                <p className="mt-1 text-sm text-red-600">{errors.firstName}</p>
              )}
            </div>

            {/* Last Name Field */}
            <div>
              <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                Last Name *
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  id="lastName"
                  value={formData.lastName}
                  onChange={(e) => handleChange('lastName', e.target.value)}
                  className={`block w-full pl-10 pr-3 py-2 border ${
                    errors.lastName ? 'border-red-300' : 'border-gray-300'
                  } rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500`}
                  placeholder="Smith"
                  disabled={isSubmitting}
                />
              </div>
              {errors.lastName && (
                <p className="mt-1 text-sm text-red-600">{errors.lastName}</p>
              )}
            </div>

            {/* Role Dropdown */}
            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-1">
                Role *
              </label>
              <select
                id="role"
                value={formData.role}
                onChange={(e) => handleChange('role', e.target.value as 'company_admin' | 'company_user')}
                className={`block w-full px-3 py-2 border ${
                  errors.role ? 'border-red-300' : 'border-gray-300'
                } rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500`}
                disabled={isSubmitting}
              >
                <option value="company_user">Company User</option>
                <option value="company_admin">Company Admin</option>
              </select>
              {errors.role && (
                <p className="mt-1 text-sm text-red-600">{errors.role}</p>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Company Admins can invite and manage team members
              </p>
            </div>

            {/* Footer Buttons */}
            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={handleClose}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-colors"
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Sending...
                  </>
                ) : (
                  <>
                    <Mail className="w-4 h-4" />
                    Send Invitation
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  )
}

