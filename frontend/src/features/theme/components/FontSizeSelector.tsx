/**
 * Font Size Selector Component for Epic 2 Story 2.2
 * Allows users to select font size preference
 */

import React, { useState } from 'react'
import { useTheme } from '../context/ThemeContext'
import { ReferenceOption } from '../../profile/types/profile.types'
import { updateProfile } from '../../profile/api/usersApi'
import { useToastNotifications } from '../../ux'

interface FontSizeSelectorProps {
  className?: string
  showLabel?: boolean
  compact?: boolean
  fontSizes?: ReferenceOption[]
}

export function FontSizeSelector({ 
  className = '', 
  showLabel = true, 
  compact = false,
  fontSizes = []
}: FontSizeSelectorProps) {
  const { state, dispatch, applyFontSize } = useTheme()
  const toast = useToastNotifications()
  
  const [isSaving, setIsSaving] = useState(false)

  // Handle font size selection
  const handleFontSizeChange = async (fontSize: ReferenceOption) => {
    try {
      setIsSaving(true)
      
      // Apply font size immediately for visual feedback
      applyFontSize(fontSize)
      dispatch({ type: 'SET_FONT_SIZE', payload: fontSize })
      
      // Save to backend
      await updateProfile({ fontSizeId: fontSize.id })
      
      toast.success(`Font size changed to ${fontSize.name}`)
    } catch (error) {
      console.error('Failed to update font size:', error)
      toast.error('Failed to save font size preference')
      
      // Revert on error
      if (state.fontSize) {
        applyFontSize(state.fontSize)
      }
    } finally {
      setIsSaving(false)
    }
  }

  if (fontSizes.length === 0) {
    return (
      <div className={`font-size-selector ${className}`}>
        <div className="animate-pulse">
          {showLabel && <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>}
          <div className="flex space-x-2">
            <div className="h-8 bg-gray-200 rounded flex-1"></div>
            <div className="h-8 bg-gray-200 rounded flex-1"></div>
            <div className="h-8 bg-gray-200 rounded flex-1"></div>
          </div>
        </div>
      </div>
    )
  }

  if (state.error) {
    return (
      <div className={`font-size-selector ${className}`}>
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-red-800 text-sm">{state.error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`font-size-selector ${className}`}>
      {showLabel && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Font Size
        </label>
      )}
      
      <div className={`grid gap-2 ${compact ? 'grid-cols-3' : 'grid-cols-1 sm:grid-cols-3'}`}>
        {fontSizes.map((fontSize) => (
          <button
            key={fontSize.id}
            onClick={() => handleFontSizeChange(fontSize)}
            disabled={isSaving}
            className={`
              relative p-3 rounded-lg border-2 transition-all duration-200
              ${state.fontSize?.id === fontSize.id
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-200 hover:border-gray-300 dark:border-gray-700 dark:hover:border-gray-600'
              }
              ${isSaving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-md'}
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
            `}
            aria-pressed={state.fontSize?.id === fontSize.id}
            aria-label={`Select ${fontSize.name} font size`}
          >
            <div className="text-center">
              <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                {fontSize.name}
              </div>
              {!compact && (
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {fontSize.base_font_size}
                </div>
              )}
            </div>
            {state.fontSize?.id === fontSize.id && (
              <div className="absolute top-2 right-2">
                <svg className="w-4 h-4 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
            )}
          </button>
        ))}
      </div>
    </div>
  )
}

export default FontSizeSelector
