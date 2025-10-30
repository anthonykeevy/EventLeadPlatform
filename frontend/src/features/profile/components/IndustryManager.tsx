/**
 * Industry Manager Component for Epic 2 Story 2.1
 * Allows users to manage their industry associations
 */

import React, { useState, useEffect } from 'react'
import { Loader2, Plus, Trash2, Star, StarOff } from 'lucide-react'
import type { IndustryAssociation, IndustryAssociationRequest, ReferenceOption } from '../types/profile.types'
import { useToastNotifications } from '../../ux'
import {
  getUserIndustries,
  addIndustry,
  updateIndustry,
  removeIndustry,
  getThemes
} from '../api/usersApi'

interface IndustryManagerProps {
  onClose?: () => void
}

export function IndustryManager({ onClose }: IndustryManagerProps) {
  const [industries, setIndustries] = useState<IndustryAssociation[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isProcessing, setIsProcessing] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedIndustryId, setSelectedIndustryId] = useState<number | null>(null)
  const { showSuccessToast, showErrorToast } = useToastNotifications()

  // Load industries
  useEffect(() => {
    loadIndustries()
  }, [])

  const loadIndustries = async () => {
    setIsLoading(true)
    setApiError(null)
    
    try {
      const data = await getUserIndustries()
      setIndustries(data)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to load industries')
      showErrorToast('Failed to load industries')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddIndustry = async (isPrimary: boolean) => {
    if (!selectedIndustryId) {
      showErrorToast('Please select an industry')
      return
    }
    
    setIsProcessing(true)
    setApiError(null)
    
    try {
      const request: IndustryAssociationRequest = {
        industryId: selectedIndustryId,
        isPrimary
      }
      
      await addIndustry(request)
      await loadIndustries()
      showSuccessToast('Industry added successfully')
      setShowAddModal(false)
      setSelectedIndustryId(null)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to add industry')
      showErrorToast('Failed to add industry')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleSetPrimary = async (userIndustryId: number) => {
    setIsProcessing(true)
    setApiError(null)
    
    try {
      const industry = industries.find(i => i.userIndustryId === userIndustryId)
      if (!industry) return
      
      const request: IndustryAssociationRequest = {
        industryId: industry.industryId,
        isPrimary: true
      }
      
      await updateIndustry(userIndustryId, request)
      await loadIndustries()
      showSuccessToast('Primary industry updated')
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to update industry')
      showErrorToast('Failed to update industry')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleRemove = async (userIndustryId: number) => {
    if (!confirm('Are you sure you want to remove this industry?')) {
      return
    }
    
    setIsProcessing(true)
    setApiError(null)
    
    try {
      await removeIndustry(userIndustryId)
      await loadIndustries()
      showSuccessToast('Industry removed successfully')
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to remove industry')
      showErrorToast('Failed to remove industry')
    } finally {
      setIsProcessing(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-8 h-8 animate-spin text-teal-600" />
      </div>
    )
  }

  const primaryIndustry = industries.find(i => i.isPrimary)
  const secondaryIndustries = industries.filter(i => !i.isPrimary)

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">My Industries</h2>
          <p className="text-sm text-gray-600 mt-1">Manage your industry associations</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Add Industry
        </button>
      </div>

      {/* API Error Display */}
      {apiError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-800 mb-4">
          {apiError}
        </div>
      )}

      {/* Primary Industry */}
      {primaryIndustry && (
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Primary Industry</h3>
          <div className="flex items-center justify-between p-4 bg-teal-50 border border-teal-200 rounded-lg">
            <div className="flex items-center gap-3">
              <Star className="w-5 h-5 text-teal-600 fill-current" />
              <div>
                <div className="font-medium text-gray-900">{primaryIndustry.industryName}</div>
                <div className="text-sm text-gray-600">{primaryIndustry.industryCode}</div>
              </div>
            </div>
            <button
              onClick={() => handleRemove(primaryIndustry.userIndustryId)}
              disabled={isProcessing}
              className="text-red-600 hover:text-red-800 disabled:opacity-50"
              aria-label="Remove industry"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {/* Secondary Industries */}
      {secondaryIndustries.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Additional Industries</h3>
          <div className="space-y-2">
            {secondaryIndustries.map((industry) => (
              <div
                key={industry.userIndustryId}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <StarOff className="w-5 h-5 text-gray-400" />
                  <div>
                    <div className="font-medium text-gray-900">{industry.industryName}</div>
                    <div className="text-sm text-gray-600">{industry.industryCode}</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleSetPrimary(industry.userIndustryId)}
                    disabled={isProcessing}
                    className="px-3 py-1 text-sm text-teal-600 hover:text-teal-800 disabled:opacity-50 transition-colors"
                  >
                    Set as Primary
                  </button>
                  <button
                    onClick={() => handleRemove(industry.userIndustryId)}
                    disabled={isProcessing}
                    className="text-red-600 hover:text-red-800 disabled:opacity-50"
                    aria-label="Remove industry"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {industries.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">You haven't added any industries yet</p>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors flex items-center gap-2 mx-auto"
          >
            <Plus className="w-5 h-5" />
            Add Your First Industry
          </button>
        </div>
      )}

      {/* Add Industry Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Add Industry</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Industry
              </label>
              <select
                value={selectedIndustryId || ''}
                onChange={(e) => setSelectedIndustryId(e.target.value ? parseInt(e.target.value) : null)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
              >
                <option value="">Choose an industry...</option>
                {/* Note: In real implementation, we'd fetch available industries from the API */}
                <option value="1">Technology</option>
                <option value="2">Healthcare</option>
                <option value="3">Finance</option>
                <option value="4">Retail</option>
                <option value="5">Hospitality</option>
              </select>
            </div>

            {apiError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-800 mb-4">
                {apiError}
              </div>
            )}

            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowAddModal(false)}
                disabled={isProcessing}
                className="flex-1 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={() => handleAddIndustry(true)}
                disabled={isProcessing || !selectedIndustryId}
                className="flex-1 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
              >
                {isProcessing ? <Loader2 className="w-5 h-5 animate-spin" /> : <Plus className="w-5 h-5" />}
                Add as Primary
              </button>
              <button
                onClick={() => handleAddIndustry(false)}
                disabled={isProcessing || !selectedIndustryId}
                className="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
              >
                {isProcessing ? <Loader2 className="w-5 h-5 animate-spin" /> : <Plus className="w-5 h-5" />}
                Add
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

