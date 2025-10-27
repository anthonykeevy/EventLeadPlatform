/**
 * Edit Role Modal - Story 1.16
 * AC-1.16.6: Role editing modal opens from edit button
 * AC-1.16.7: Role restrictions enforced in UI
 */

import React, { useState, useCallback } from 'react'
import { X, Shield, AlertCircle } from 'lucide-react'
import { editUserRole } from '../api/teamApi'
import type { EditUserRoleRequest } from '../types/team.types'

interface EditRoleModalProps {
  companyId: number
  companyName: string
  userId: number
  userName: string
  currentRole: string
  currentUserRole: 'Company Admin' | 'Company User'
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export function EditRoleModal({
  companyId,
  companyName,
  userId,
  userName,
  currentRole,
  currentUserRole,
  isOpen,
  onClose,
  onSuccess
}: EditRoleModalProps) {
  // Map display role to API role code
  const currentRoleCode = currentRole === 'Company Admin' ? 'company_admin' : 'company_user'
  
  const [selectedRole, setSelectedRole] = useState<'company_admin' | 'company_user'>(currentRoleCode)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  // AC-1.16.7: Role restrictions - only show roles equal or lower than current user's role
  const availableRoles = currentUserRole === 'Company Admin' 
    ? [
        { code: 'company_admin' as const, label: 'Company Admin', description: 'Can invite and manage team members' },
        { code: 'company_user' as const, label: 'Company User', description: 'Standard team member access' }
      ]
    : [
        { code: 'company_user' as const, label: 'Company User', description: 'Standard team member access' }
      ]

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitError(null)

    // Check if role actually changed
    if (selectedRole === currentRoleCode) {
      onClose()
      return
    }

    setIsSubmitting(true)

    try {
      const response = await editUserRole(companyId, userId, { roleCode: selectedRole })
      
      if (response.success) {
        onSuccess()
        onClose()
      }
    } catch (error: any) {
      console.error('Failed to edit user role:', error)
      
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
        } else {
          setSubmitError('Validation error occurred')
        }
      } else if (error.response?.status === 403) {
        setSubmitError('You do not have permission to edit this user\'s role')
      } else if (error.response?.status === 404) {
        setSubmitError('User not found')
      } else if (error.response?.status === 422) {
        setSubmitError('Invalid role selection. Please try again.')
      } else {
        setSubmitError('Failed to update role. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }, [companyId, userId, selectedRole, currentRoleCode, onSuccess, onClose])

  const handleClose = useCallback(() => {
    setSelectedRole(currentRoleCode)
    setSubmitError(null)
    onClose()
  }, [currentRoleCode, onClose])

  if (!isOpen) return null

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
        onClick={handleClose}
      >
        {/* Modal - AC-1.16.6: Role editing modal */}
        <div
          className="bg-white rounded-lg shadow-2xl w-full max-w-md transform transition-all"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="bg-teal-600 text-white px-6 py-4 rounded-t-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Shield className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Edit User Role</h2>
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

            {/* User Info */}
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600">Editing role for:</p>
              <p className="font-medium text-gray-900 mt-1">{userName}</p>
              <p className="text-xs text-gray-500 mt-1">Current role: {currentRole}</p>
            </div>

            {/* Role Selection - AC-1.16.7: Only show allowed roles */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Select New Role *
              </label>
              <div className="space-y-2">
                {availableRoles.map((role) => (
                  <label
                    key={role.code}
                    className={`flex items-start p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                      selectedRole === role.code
                        ? 'border-teal-500 bg-teal-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <input
                      type="radio"
                      name="role"
                      value={role.code}
                      checked={selectedRole === role.code}
                      onChange={(e) => setSelectedRole(e.target.value as 'company_admin' | 'company_user')}
                      className="mt-1 mr-3 text-teal-600 focus:ring-teal-500"
                      disabled={isSubmitting}
                    />
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">{role.label}</div>
                      <div className="text-sm text-gray-500 mt-1">{role.description}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Warning if changing to admin */}
            {selectedRole === 'company_admin' && currentRoleCode === 'company_user' && (
              <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded flex items-start gap-2">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <span className="text-sm">
                  This user will be able to invite and manage team members, including other admins.
                </span>
              </div>
            )}

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
                disabled={isSubmitting || selectedRole === currentRoleCode}
              >
                {isSubmitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Updating...
                  </>
                ) : (
                  <>
                    <Shield className="w-4 h-4" />
                    Update Role
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

