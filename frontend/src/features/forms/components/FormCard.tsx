/**
 * Form Card Component - Story 2.8
 * Displays form information in a card format
 */

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Calendar, Edit2, Trash2, Eye, Shield, Layout } from 'lucide-react'
import { Form } from '../types/form.types'
import { FormStatusBadge } from './FormStatusBadge'
import { checkFormAccess } from '../api/formAccessApi'
import { AccessCheckResponse } from '../types/form-access.types'

interface FormCardProps {
  form: Form
  onEdit: (form: Form) => void
  onDelete: (form: Form) => void
  onView?: (form: Form) => void
  onDesign?: (form: Form) => void
}

export function FormCard({ form, onEdit, onDelete, onView }: FormCardProps) {
  const [userAccess, setUserAccess] = useState<AccessCheckResponse | null>(null)

  useEffect(() => {
    loadUserAccess()
  }, [form.formId])

  const loadUserAccess = async () => {
    try {
      const access = await checkFormAccess(form.formId)
      setUserAccess(access)
    } catch (err) {
      console.error('Failed to check form access:', err)
    }
  }

  const canManage = userAccess?.accessLevel === 'MANAGE'
  const canEdit = canManage || userAccess?.accessLevel === 'EDIT'
  const isShared = userAccess?.hasAccess && userAccess?.accessLevel !== 'MANAGE' // Not owner

  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'Never'
    try {
      return new Intl.DateTimeFormat('en-AU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(new Date(dateString))
    } catch {
      return new Date(dateString).toLocaleString('en-AU')
    }
  }

  return (
    <div
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 border border-gray-200 overflow-hidden cursor-pointer"
      onClick={() => onView?.(form)}
    >
      {/* Header with Status Badge */}
      <div className="p-4 pb-3 border-b border-gray-100">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1 pr-2">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                {form.formName}
              </h3>
              {isShared && (
                <span className="flex items-center gap-1 text-xs text-teal-600" title="Shared form">
                  <Shield className="w-3 h-3" />
                </span>
              )}
            </div>
            {userAccess?.accessLevel && userAccess.accessLevel !== 'MANAGE' && (
              <span className="text-xs text-gray-500">
                Access: {userAccess.accessLevel}
              </span>
            )}
          </div>
          <FormStatusBadge status={form.formStatus} approvalStatus={form.formApprovalStatus} />
        </div>
      </div>

      {/* Form Details */}
      <div className="p-4 space-y-3">
        {/* Description */}
        {form.formDescription && (
          <p className="text-sm text-gray-600 line-clamp-2">
            {form.formDescription}
          </p>
        )}

        {/* Activity Metrics */}
        <div className="grid grid-cols-2 gap-3 pt-2 border-t border-gray-100">
          <div className="text-sm">
            <div className="text-gray-500">Total Submissions</div>
            <div className="font-semibold text-gray-900">{form.totalSubmissions}</div>
          </div>
          <div className="text-sm">
            <div className="text-gray-500">Leads Collected</div>
            <div className="font-semibold text-gray-900">
              {form.productionLeadsCollected + form.demoLeadsCollected}
            </div>
          </div>
        </div>

        {/* Last Activity */}
        {form.lastActivityDate && (
          <div className="flex items-center text-xs text-gray-500">
            <Calendar className="w-3 h-3 mr-1.5 flex-shrink-0" />
            <span>Last activity: {formatDate(form.lastActivityDate)}</span>
          </div>
        )}
      </div>

      {/* Actions Footer */}
      <div className="px-4 py-3 bg-gray-50 border-t border-gray-100 flex items-center justify-end gap-2">
        {onView && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              onView(form)
            }}
            className="px-3 py-1.5 text-sm font-medium text-gray-600 hover:text-gray-700 hover:bg-gray-100 rounded-md transition-colors flex items-center gap-1"
            aria-label={`View ${form.formName}`}
          >
            <Eye className="w-4 h-4" />
            View
          </button>
        )}
        {canEdit && (
          <Link
            to={`/forms/${form.formId}/builder`}
            className="px-3 py-1.5 text-sm font-medium text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded-md transition-colors flex items-center gap-1"
            aria-label={`Design ${form.formName}`}
            onClick={(e) => e.stopPropagation()}
          >
            <Layout className="w-4 h-4" />
            Design
          </Link>
        )}
        {canEdit && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              onEdit(form)
            }}
            className="px-3 py-1.5 text-sm font-medium text-teal-600 hover:text-teal-700 hover:bg-teal-50 rounded-md transition-colors flex items-center gap-1"
            aria-label={`Edit ${form.formName}`}
          >
            <Edit2 className="w-4 h-4" />
            Edit
          </button>
        )}
        {canManage && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              onDelete(form)
            }}
            className="px-3 py-1.5 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition-colors flex items-center gap-1"
            aria-label={`Delete ${form.formName}`}
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        )}
      </div>
    </div>
  )
}

