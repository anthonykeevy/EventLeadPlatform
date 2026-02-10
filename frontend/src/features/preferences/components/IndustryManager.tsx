/**
 * Industry Manager Component for Preferences (Reusable)
 * Allows users to manage their industry associations
 * Can be used in AccountSettingsPopup and PreferencesPage
 */

import { useState, useEffect } from 'react'
import { Loader2, Plus, Trash2, Star, StarOff } from 'lucide-react'
import type { IndustryAssociation, IndustryAssociationRequest } from '../../profile/types/profile.types'
import { 
  getUserIndustries, 
  addIndustry, 
  updateIndustry, 
  removeIndustry,
  getIndustries,
  type IndustryOption 
} from '../../profile/api/usersApi'
import { useToastNotifications } from '../../ux'
import { IndustrySearch } from './IndustrySearch'

interface IndustryManagerProps {
  onUpdate?: () => void
  compact?: boolean
}

export function IndustryManager({ onUpdate, compact = false }: IndustryManagerProps) {
  const [industries, setIndustries] = useState<IndustryAssociation[]>([])
  const [availableIndustries, setAvailableIndustries] = useState<IndustryOption[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isProcessing, setIsProcessing] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const toast = useToastNotifications()

  // Load industries
  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setIsLoading(true)
    setApiError(null)
    
    try {
      const [userIndustries, allIndustries] = await Promise.all([
        getUserIndustries(),
        getIndustries()
      ])
      setIndustries(userIndustries)
      setAvailableIndustries(allIndustries)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to load industries')
      toast.error('Failed to load industries')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddIndustry = async (industryId: number, isPrimary: boolean) => {
    setIsProcessing(true)
    setApiError(null)
    
    try {
      const request: IndustryAssociationRequest = {
        industryId,
        isPrimary
      }
      
      await addIndustry(request)
      await loadData()
      toast.success('Industry added successfully')
      setShowAddModal(false)
      if (onUpdate) onUpdate()
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to add industry')
      toast.error('Failed to add industry')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleSetPrimary = async (userIndustryId: number | undefined) => {
    if (!userIndustryId || isNaN(userIndustryId)) {
      console.error('[IndustryManager] Invalid userIndustryId:', userIndustryId)
      toast.error('Invalid industry selection')
      return
    }
    
    setIsProcessing(true)
    setApiError(null)
    
    try {
      const industry = industries.find(i => i.userIndustryId === userIndustryId)
      if (!industry) {
        console.error('[IndustryManager] Industry not found for userIndustryId:', userIndustryId)
        toast.error('Industry not found')
        return
      }
      
      console.log('[IndustryManager] Setting primary industry:', { userIndustryId, industry })
      
      const request: IndustryAssociationRequest = {
        industryId: industry.industryId,
        isPrimary: true
      }
      
      await updateIndustry(userIndustryId, request)
      await loadData()
      toast.success('Primary industry updated')
      if (onUpdate) onUpdate()
    } catch (error) {
      console.error('[IndustryManager] Error setting primary:', error)
      const errorMessage = error instanceof Error ? error.message : 'Failed to update industry'
      setApiError(errorMessage)
      toast.error(errorMessage)
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
      await loadData()
      toast.success('Industry removed successfully')
      if (onUpdate) onUpdate()
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to remove industry')
      toast.error('Failed to remove industry')
    } finally {
      setIsProcessing(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-4">
        <Loader2 className="w-6 h-6 animate-spin text-teal-600" />
        <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">Loading industries...</span>
      </div>
    )
  }

  const primaryIndustry = industries.find(i => i.isPrimary)
  const secondaryIndustries = industries.filter(i => !i.isPrimary).sort((a, b) => a.sortOrder - b.sortOrder)

  // Filter out already-selected industries from available list
  const selectedIndustryIds = industries.map(i => i.industryId)
  const availableForSelection = availableIndustries.filter(
    industry => !selectedIndustryIds.includes(industry.id)
  )

  return (
    <div className={compact ? '' : 'space-y-4'}>
      {/* API Error Display */}
      {apiError && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3 text-sm text-red-800 dark:text-red-200 mb-4">
          {apiError}
        </div>
      )}

      {/* Primary Industry */}
      {primaryIndustry && (
        <div className="mb-4">
          <div className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2 uppercase tracking-wide">
            Primary Industry
          </div>
          <div className="flex items-center justify-between p-3 bg-teal-50 dark:bg-teal-900/20 border border-teal-200 dark:border-teal-800 rounded-lg">
            <div className="flex items-center gap-2">
              <Star className="w-4 h-4 text-teal-600 dark:text-teal-400 fill-current" />
              <div>
                <div className="font-medium text-gray-900 dark:text-gray-100 text-sm">
                  {primaryIndustry.industryName}
                </div>
                {!compact && (
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    {primaryIndustry.industryCode}
                  </div>
                )}
              </div>
            </div>
            {industries.length > 1 && (
              <button
                onClick={() => handleRemove(primaryIndustry.userIndustryId)}
                disabled={isProcessing}
                className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 disabled:opacity-50 p-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                aria-label="Remove industry"
                title="Remove industry"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      )}

      {/* Secondary Industries */}
      {secondaryIndustries.length > 0 && (
        <div className="mb-4">
          <div className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2 uppercase tracking-wide">
            Additional Industries
          </div>
          <div className="space-y-2">
            {secondaryIndustries.map((industry) => (
              <div
                key={industry.userIndustryId}
                className="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-gray-300 dark:hover:border-gray-600 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <StarOff className="w-4 h-4 text-gray-400" />
                  <div>
                    <div className="font-medium text-gray-900 dark:text-gray-100 text-sm">
                      {industry.industryName}
                    </div>
                    {!compact && (
                      <div className="text-xs text-gray-600 dark:text-gray-400">
                        {industry.industryCode}
                      </div>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleSetPrimary(industry.userIndustryId)}
                    disabled={isProcessing}
                    className="px-2 py-1 text-xs text-teal-600 dark:text-teal-400 hover:text-teal-800 dark:hover:text-teal-300 disabled:opacity-50 transition-colors"
                  >
                    Set Primary
                  </button>
                  <button
                    onClick={() => handleRemove(industry.userIndustryId)}
                    disabled={isProcessing}
                    className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 disabled:opacity-50 p-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                    aria-label="Remove industry"
                    title="Remove industry"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {industries.length === 0 && (
        <div className="text-center py-6 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            You haven't added any industries yet
          </p>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors text-sm flex items-center gap-2 mx-auto"
          >
            <Plus className="w-4 h-4" />
            Add Industry
          </button>
        </div>
      )}

      {/* Add Industry Button */}
      {industries.length > 0 && (
        <button
          onClick={() => setShowAddModal(true)}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm text-gray-700 dark:text-gray-300 flex items-center justify-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Add Industry
        </button>
      )}

      {/* Add Industry Modal with Search */}
      {showAddModal && (
        <IndustrySearch
          availableIndustries={availableForSelection}
          onSelect={(industryId, isPrimary) => {
            handleAddIndustry(industryId, isPrimary)
          }}
          onClose={() => setShowAddModal(false)}
          isProcessing={isProcessing}
          hasPrimaryIndustry={!!primaryIndustry}
        />
      )}
    </div>
  )
}

