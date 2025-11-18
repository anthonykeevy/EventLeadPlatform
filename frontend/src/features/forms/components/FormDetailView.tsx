/**
 * Form Detail View - Story 2.8
 * Displays complete form information in a detailed view
 */

import React from 'react'
import { FileText, Calendar, Edit2, Trash2, ArrowLeft, X, Globe, DollarSign, BarChart3 } from 'lucide-react'
import { Form } from '../types/form.types'
import { FormStatusBadge } from './FormStatusBadge'

interface FormDetailViewProps {
  form: Form | null
  onClose: () => void
  onEdit: (form: Form) => void
  onDelete: (form: Form) => void
}

export function FormDetailView({ form, onClose, onEdit, onDelete }: FormDetailViewProps) {
  if (!form) return null

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
                      <span className="text-gray-600">${form.deploymentCost.toFixed(2)}</span>
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
                </div>
              </section>
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
          <button
            onClick={() => onEdit(form)}
            className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 transition-colors flex items-center gap-2"
          >
            <Edit2 className="w-4 h-4" />
            Edit
          </button>
          <button
            onClick={() => onDelete(form)}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors flex items-center gap-2"
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}

