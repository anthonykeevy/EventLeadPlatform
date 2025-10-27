/**
 * Auth Change Banner - Story 1.16 Enhanced
 * 
 * Non-blocking warning banner when auth changes occur in other tabs.
 * Allows users to save their work before syncing auth state.
 */

import { AlertTriangle, X, Save, LogOut, RefreshCw } from 'lucide-react'
import { useState } from 'react'

export interface AuthChangeBannerProps {
  type: 'logout' | 'login' | 'switch'
  message: string
  description?: string
  onSave?: () => Promise<void>
  onDismiss?: () => void
  onProceed?: () => void
  allowContinue?: boolean
  unsavedCount?: number
}

export function AuthChangeBanner({
  type,
  message,
  description,
  onSave,
  onDismiss,
  onProceed,
  allowContinue = true,
  unsavedCount = 0
}: AuthChangeBannerProps) {
  const [isSaving, setIsSaving] = useState(false)
  const [isProceeding, setIsProceeding] = useState(false)

  const handleSave = async () => {
    if (!onSave) return

    setIsSaving(true)
    try {
      await onSave()
      
      // After saving, proceed with auth change
      if (onProceed) {
        setIsProceeding(true)
        await onProceed()
      }
    } catch (error) {
      console.error('Failed to save:', error)
      alert('Failed to save your work. Please try again.')
    } finally {
      setIsSaving(false)
      setIsProceeding(false)
    }
  }

  const handleProceedWithoutSaving = async () => {
    if (!onProceed) return

    const confirmed = confirm(
      unsavedCount > 0
        ? `You have ${unsavedCount} unsaved item(s). Proceed without saving?`
        : 'Proceed without saving?'
    )

    if (confirmed) {
      setIsProceeding(true)
      try {
        await onProceed()
      } catch (error) {
        console.error('Failed to proceed:', error)
      } finally {
        setIsProceeding(false)
      }
    }
  }

  // Color scheme based on type
  const colors = {
    logout: 'bg-red-50 border-red-400 text-red-900',
    login: 'bg-blue-50 border-blue-400 text-blue-900',
    switch: 'bg-yellow-50 border-yellow-400 text-yellow-900'
  }

  const iconColors = {
    logout: 'text-red-600',
    login: 'text-blue-600',
    switch: 'text-yellow-600'
  }

  return (
    <div className={`fixed top-0 left-0 right-0 z-50 ${colors[type]} border-b-2 p-4 shadow-lg`}>
      <div className="max-w-7xl mx-auto flex items-start justify-between gap-4">
        {/* Icon + Message */}
        <div className="flex items-start gap-3 flex-1">
          <AlertTriangle className={`w-6 h-6 flex-shrink-0 mt-0.5 ${iconColors[type]}`} />
          
          <div className="flex-1">
            <p className="font-semibold text-sm sm:text-base">
              {message}
            </p>
            
            {description && (
              <p className="text-xs sm:text-sm opacity-90 mt-1">
                {description}
              </p>
            )}
            
            {unsavedCount > 0 && (
              <p className="text-xs sm:text-sm font-medium mt-2 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                {unsavedCount} unsaved {unsavedCount === 1 ? 'item' : 'items'}
              </p>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2 flex-shrink-0">
          {/* Save & Continue Button */}
          {onSave && (
            <button
              onClick={handleSave}
              disabled={isSaving || isProceeding}
              className="px-3 sm:px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isSaving ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span className="hidden sm:inline">Saving...</span>
                </>
              ) : isProceeding ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span className="hidden sm:inline">Updating...</span>
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  <span className="hidden sm:inline">Save & Continue</span>
                  <span className="sm:hidden">Save</span>
                </>
              )}
            </button>
          )}

          {/* Proceed Without Saving */}
          {onProceed && !onSave && (
            <button
              onClick={handleProceedWithoutSaving}
              disabled={isProceeding}
              className="px-3 sm:px-4 py-2 border-2 border-current hover:bg-black hover:bg-opacity-5 text-sm font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isProceeding ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span className="hidden sm:inline">Updating...</span>
                </>
              ) : (
                <>
                  {type === 'logout' && <LogOut className="w-4 h-4" />}
                  {type === 'login' && <RefreshCw className="w-4 h-4" />}
                  {type === 'switch' && <RefreshCw className="w-4 h-4" />}
                  <span className="hidden sm:inline">Continue</span>
                </>
              )}
            </button>
          )}

          {/* Dismiss (Keep Working) */}
          {allowContinue && onDismiss && (
            <button
              onClick={onDismiss}
              disabled={isSaving || isProceeding}
              className="p-2 hover:bg-black hover:bg-opacity-5 rounded-lg transition-colors disabled:opacity-50"
              aria-label="Dismiss"
              title="Keep working in this tab"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}


