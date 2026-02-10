/**
 * Delete Form Confirm Modal - Story 2.8
 * Confirmation dialog for form deletion
 */

import { useState } from 'react'
import { X, AlertTriangle } from 'lucide-react'
import { deleteForm } from '../api/formsApi'
import { Form } from '../types/form.types'
import { useToastNotifications } from '../../ux'

interface DeleteFormConfirmModalProps {
  isOpen: boolean
  form: Form | null
  onClose: () => void
  onConfirm: () => void
}

export function DeleteFormConfirmModal({ isOpen, form, onClose, onConfirm }: DeleteFormConfirmModalProps) {
  const [isDeleting, setIsDeleting] = useState(false)
  const toast = useToastNotifications()

  const handleDelete = async () => {
    if (!form) return

    setIsDeleting(true)
    try {
      await deleteForm(form.formId)
      toast.success('Form deleted successfully', 'Success')
      onConfirm()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete form'
      toast.error(errorMessage, 'Error deleting form')
    } finally {
      setIsDeleting(false)
    }
  }

  if (!isOpen || !form) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-md">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-6 h-6 text-red-600" />
            <h2 className="text-xl font-bold text-gray-900">Delete Form</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 p-1 rounded transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="px-6 py-4">
          <p className="text-gray-700 mb-4">
            Are you sure you want to delete the form <strong>"{form.formName}"</strong>?
          </p>
          <p className="text-sm text-gray-500">
            This action will soft delete the form. It will no longer appear in your forms list, but the data will be retained for audit purposes.
          </p>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            disabled={isDeleting}
          >
            Cancel
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isDeleting ? 'Deleting...' : 'Delete Form'}
          </button>
        </div>
      </div>
    </div>
  )
}

