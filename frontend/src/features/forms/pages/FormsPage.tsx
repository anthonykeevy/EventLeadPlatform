/**
 * Forms Page - Story 2.8
 * Main form management page with list, search, and filters
 */

import React, { useState, useEffect, useCallback } from 'react'
import { Plus, Search, Filter, X } from 'lucide-react'
import { getForms, getFormStatuses, getFormApprovalStatuses, FormFilters } from '../api/formsApi'
import { Form, FormStatus, FormApprovalStatus } from '../types/form.types'
import { FormCard } from '../components/FormCard'
import { CreateFormModal } from '../components/CreateFormModal'
import { EditFormModal } from '../components/EditFormModal'
import { DeleteFormConfirmModal } from '../components/DeleteFormConfirmModal'
import { FormDetailView } from '../components/FormDetailView'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'
import { ErrorMessage } from '../../ux/components/ErrorMessage'

export function FormsPage() {
  // State
  const [forms, setForms] = useState<Form[]>([])
  const [formStatuses, setFormStatuses] = useState<FormStatus[]>([])
  const [formApprovalStatuses, setFormApprovalStatuses] = useState<FormApprovalStatus[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isLoadingForms, setIsLoadingForms] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const pageSize = 20

  // Filter state
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState<FormFilters>({})
  const [showFilters, setShowFilters] = useState(false)
  const [selectedStatusId, setSelectedStatusId] = useState<number | undefined>(undefined)
  const [selectedEventId, setSelectedEventId] = useState<number | undefined>(undefined)

  // Modal state
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingForm, setEditingForm] = useState<Form | null>(null)
  const [deletingForm, setDeletingForm] = useState<Form | null>(null)
  const [viewingForm, setViewingForm] = useState<Form | null>(null)

  const { showToast } = useToastNotifications()

  // Load reference data on mount
  useEffect(() => {
    const loadReferenceData = async () => {
      try {
        const [statuses, approvalStatuses] = await Promise.all([
          getFormStatuses(),
          getFormApprovalStatuses()
        ])
        setFormStatuses(statuses)
        setFormApprovalStatuses(approvalStatuses)
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load reference data'
        setError(errorMessage)
        showToast.error(errorMessage, 'Failed to load form statuses')
      }
    }

    loadReferenceData()
  }, [showToast])

  // Load forms
  const loadForms = useCallback(async () => {
    setIsLoadingForms(true)
    setError(null)

    try {
      const filtersToUse: FormFilters = {}
      
      if (selectedStatusId) filtersToUse.formStatusId = selectedStatusId
      if (selectedEventId) filtersToUse.eventId = selectedEventId
      if (searchQuery.trim()) filtersToUse.search = searchQuery.trim()

      const response = await getForms(filtersToUse, page, pageSize)
      setForms(response.forms)
      setTotal(response.total)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load forms'
      setError(errorMessage)
      showToast.error(errorMessage, 'Failed to load forms')
    } finally {
      setIsLoadingForms(false)
      setIsLoading(false)
    }
  }, [page, searchQuery, selectedStatusId, selectedEventId, showToast])

  // Load forms when filters or page changes
  useEffect(() => {
    loadForms()
  }, [loadForms])

  // Handle create form
  const handleCreateSuccess = () => {
    setShowCreateModal(false)
    showToast.success('The form has been created successfully', 'Form created')
    loadForms()
  }

  // Handle edit form
  const handleEdit = (form: Form) => {
    setEditingForm(form)
  }

  const handleEditSuccess = () => {
    setEditingForm(null)
    showToast.success('The form has been updated successfully', 'Form updated')
    loadForms()
  }

  // Handle delete form
  const handleDelete = (form: Form) => {
    setDeletingForm(form)
  }

  const handleDeleteSuccess = () => {
    setDeletingForm(null)
    showToast.success('The form has been deleted successfully', 'Form deleted')
    loadForms()
  }

  // Clear filters
  const handleClearFilters = () => {
    setSearchQuery('')
    setSelectedStatusId(undefined)
    setSelectedEventId(undefined)
    setPage(1)
  }

  const hasActiveFilters = searchQuery || selectedStatusId || selectedEventId

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Forms</h1>
              <p className="text-gray-600 mt-1">Manage your company's forms</p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn-primary flex items-center gap-2"
              aria-label="Create new form"
            >
              <Plus className="w-5 h-5" />
              Create Form
            </button>
          </div>

          {/* Search and Filters */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            {/* Search Bar */}
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value)
                  setPage(1)
                }}
                placeholder="Search forms by name or description..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
              />
            </div>

            {/* Filter Toggle */}
            <div className="flex items-center justify-between">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-teal-600 transition-colors"
              >
                <Filter className="w-4 h-4" />
                Filters
                {hasActiveFilters && (
                  <span className="bg-teal-600 text-white text-xs px-2 py-0.5 rounded-full">
                    Active
                  </span>
                )}
              </button>
              {hasActiveFilters && (
                <button
                  onClick={handleClearFilters}
                  className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900"
                >
                  <X className="w-4 h-4" />
                  Clear filters
                </button>
              )}
            </div>

            {/* Filter Panel */}
            {showFilters && (
              <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Status Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status
                  </label>
                  <select
                    value={selectedStatusId || ''}
                    onChange={(e) => {
                      setSelectedStatusId(e.target.value ? Number(e.target.value) : undefined)
                      setPage(1)
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                  >
                    <option value="">All Statuses</option>
                    {formStatuses.map((status) => (
                      <option key={status.formStatusId} value={status.formStatusId}>
                        {status.statusName}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <LoadingSpinner size="large" />
          </div>
        )}

        {/* Error State */}
        {error && !isLoading && (
          <ErrorMessage
            title="Failed to load forms"
            message={error}
            onRetry={loadForms}
          />
        )}

        {/* Forms List */}
        {!isLoading && !error && (
          <>
            {/* Results Count */}
            <div className="mb-4 text-sm text-gray-600">
              Showing {forms.length} of {total} form{total !== 1 ? 's' : ''}
            </div>

            {/* Forms Grid */}
            {forms.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <p className="text-gray-500 text-lg mb-2">No forms found</p>
                <p className="text-gray-400 mb-4">
                  {hasActiveFilters
                    ? 'Try adjusting your filters'
                    : 'Create your first form to get started'}
                </p>
                {!hasActiveFilters && (
                  <button
                    onClick={() => setShowCreateModal(true)}
                    className="btn-primary inline-flex items-center gap-2"
                  >
                    <Plus className="w-5 h-5" />
                    Create Form
                  </button>
                )}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {forms.map((form) => (
                  <FormCard
                    key={form.formId}
                    form={form}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                    onView={setViewingForm}
                  />
                ))}
              </div>
            )}

            {/* Pagination */}
            {total > pageSize && (
              <div className="mt-6 flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  Page {page} of {Math.ceil(total / pageSize)}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setPage(page - 1)}
                    disabled={page === 1}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  <button
                    onClick={() => setPage(page + 1)}
                    disabled={page >= Math.ceil(total / pageSize)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Modals */}
      {showCreateModal && (
        <CreateFormModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleCreateSuccess}
        />
      )}

      {editingForm && (
        <EditFormModal
          isOpen={!!editingForm}
          form={editingForm}
          onClose={() => setEditingForm(null)}
          onSuccess={handleEditSuccess}
        />
      )}

      {deletingForm && (
        <DeleteFormConfirmModal
          isOpen={!!deletingForm}
          form={deletingForm}
          onClose={() => setDeletingForm(null)}
          onConfirm={handleDeleteSuccess}
        />
      )}

      {viewingForm && (
        <FormDetailView
          form={viewingForm}
          onClose={() => setViewingForm(null)}
          onEdit={(form) => {
            setViewingForm(null)
            setEditingForm(form)
          }}
          onDelete={(form) => {
            setViewingForm(null)
            setDeletingForm(form)
          }}
        />
      )}
    </div>
  )
}

