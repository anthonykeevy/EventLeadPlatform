/**
 * Theme Settings Popup Component
 * Compact theme customization interface for the user menu
 */

import React, { useState, useEffect, useRef } from 'react'
import { X, Palette, Layout, Type } from 'lucide-react'
import { useTheme } from '../../theme'
import { ReferenceOption } from '../../profile/types/profile.types'
import { getThemes, getLayoutDensities, getFontSizes, updateProfile } from '../../profile/api/usersApi'
import { useToastNotifications } from '../../ux'

interface ThemeSettingsPopupProps {
  isOpen: boolean
  onClose: () => void
}

export function ThemeSettingsPopup({ isOpen, onClose }: ThemeSettingsPopupProps) {
  const { state, dispatch, applyTheme, applyLayoutDensity, applyFontSize } = useTheme()
  const toast = useToastNotifications()
  
  const [themes, setThemes] = useState<ReferenceOption[]>([])
  const [densities, setDensities] = useState<ReferenceOption[]>([])
  const [fontSizes, setFontSizes] = useState<ReferenceOption[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  
  // Preview mode state (Story 2.3: Preview before save)
  const [previewTheme, setPreviewTheme] = useState<ReferenceOption | null>(null)
  const [previewDensity, setPreviewDensity] = useState<ReferenceOption | null>(null)
  const [previewFontSize, setPreviewFontSize] = useState<ReferenceOption | null>(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  
  // Track if data has been loaded to prevent multiple calls
  const dataLoadedRef = useRef(false)
  const isLoadingRef = useRef(false)

  // Load theme reference data - only once when popup opens
  useEffect(() => {
    // Only load if popup is open, data hasn't been loaded, and not currently loading
    if (isOpen && !dataLoadedRef.current && !isLoadingRef.current) {
      isLoadingRef.current = true
      
      const loadData = async () => {
        try {
          setIsLoading(true)
          const [themesData, densitiesData, fontSizesData] = await Promise.all([
            getThemes(),
            getLayoutDensities(),
            getFontSizes()
          ])
          
          setThemes(themesData)
          setDensities(densitiesData)
          setFontSizes(fontSizesData)
          dataLoadedRef.current = true
        } catch (error) {
          console.error('Failed to load theme data:', error)
          toast.error('Failed to load theme options')
          // Reset refs on error so user can retry
          dataLoadedRef.current = false
        } finally {
          setIsLoading(false)
          isLoadingRef.current = false
        }
      }

      loadData()
    }
    
    // Don't reset data loaded flag when popup closes - cache data for better performance
    // Only reset on error so user can retry
  }, [isOpen]) // Only depend on isOpen

  // Reset preview state when popup closes (Story 2.3)
  useEffect(() => {
    if (!isOpen && hasUnsavedChanges) {
      // Revert to saved state
      if (state.theme) applyTheme(state.theme)
      if (state.layoutDensity) applyLayoutDensity(state.layoutDensity)
      if (state.fontSize) applyFontSize(state.fontSize)
      
      // Reset preview state
      setPreviewTheme(null)
      setPreviewDensity(null)
      setPreviewFontSize(null)
      setHasUnsavedChanges(false)
    }
  }, [isOpen, hasUnsavedChanges, state.theme, state.layoutDensity, state.fontSize, applyTheme, applyLayoutDensity, applyFontSize])

  // Handle theme selection - Preview mode (Story 2.3)
  const handleThemeChange = (theme: ReferenceOption) => {
    // Apply preview immediately for visual feedback
    setPreviewTheme(theme)
    applyTheme(theme)
    setHasUnsavedChanges(true)
  }

  // Handle density selection - Preview mode (Story 2.3)
  const handleDensityChange = (density: ReferenceOption) => {
    // Apply preview immediately for visual feedback
    setPreviewDensity(density)
    applyLayoutDensity(density)
    setHasUnsavedChanges(true)
  }

  // Handle font size selection - Preview mode (Story 2.3)
  const handleFontSizeChange = (fontSize: ReferenceOption) => {
    // Apply preview immediately for visual feedback
    setPreviewFontSize(fontSize)
    applyFontSize(fontSize)
    setHasUnsavedChanges(true)
  }

  // Apply preview changes (Story 2.3)
  const handleApplyChanges = async () => {
    try {
      setIsSaving(true)
      
      const updates: any = {}
      
      if (previewTheme) {
        applyTheme(previewTheme)
        dispatch({ type: 'SET_THEME', payload: previewTheme })
        updates.themePreferenceId = previewTheme.id
      }
      
      if (previewDensity) {
        applyLayoutDensity(previewDensity)
        dispatch({ type: 'SET_LAYOUT_DENSITY', payload: previewDensity })
        updates.layoutDensityId = previewDensity.id
      }
      
      if (previewFontSize) {
        applyFontSize(previewFontSize)
        dispatch({ type: 'SET_FONT_SIZE', payload: previewFontSize })
        updates.fontSizeId = previewFontSize.id
      }
      
      // Save all changes to backend
      if (Object.keys(updates).length > 0) {
        const result = await updateProfile(updates)
        
        if (!result || !result.success) {
          throw new Error(`API returned unsuccessful response: ${result?.message || 'Unknown error'}`)
        }
        
        const changes = []
        if (previewTheme) changes.push(`theme to ${previewTheme.name}`)
        if (previewDensity) changes.push(`density to ${previewDensity.name}`)
        if (previewFontSize) changes.push(`font size to ${previewFontSize.name}`)
        
        toast.success(`Updated ${changes.join(', ')}`)
      }
      
      // Reset preview state
      setPreviewTheme(null)
      setPreviewDensity(null)
      setPreviewFontSize(null)
      setHasUnsavedChanges(false)
      
    } catch (error) {
      console.error('Failed to save preferences:', error)
      toast.error('Failed to save preferences')
      
      // Revert preview changes on error
      handleCancelChanges()
    } finally {
      setIsSaving(false)
    }
  }

  // Cancel preview changes (Story 2.3)
  const handleCancelChanges = () => {
    // Revert to saved state
    if (state.theme) applyTheme(state.theme)
    if (state.layoutDensity) applyLayoutDensity(state.layoutDensity)
    if (state.fontSize) applyFontSize(state.fontSize)
    
    // Reset preview state
    setPreviewTheme(null)
    setPreviewDensity(null)
    setPreviewFontSize(null)
    setHasUnsavedChanges(false)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <Palette className="w-5 h-5 text-teal-600 dark:text-teal-400" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Theme Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            aria-label="Close theme settings"
          >
            <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
              <span className="ml-3 text-gray-600">Loading theme options...</span>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Theme Selection */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Palette className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">Theme</h3>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {themes.map((theme) => (
                    <button
                      key={theme.id}
                      onClick={() => handleThemeChange(theme)}
                      disabled={isSaving}
                      className={`p-3 rounded-lg border-2 transition-all duration-200 text-left ${
                        (previewTheme?.id === theme.id || (!previewTheme && state.theme?.id === theme.id))
                          ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                          : 'border-gray-200 hover:border-gray-300 dark:border-gray-700'
                      } ${isSaving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                    >
                      <div className={`font-medium text-sm ${state.theme?.id === theme.id ? 'text-gray-900 dark:text-teal-100' : 'text-gray-900 dark:text-gray-100'}`}>
                        {theme.name}
                      </div>
                      <div className={`text-xs mt-1 ${state.theme?.id === theme.id ? 'text-gray-500 dark:text-teal-200' : 'text-gray-500 dark:text-gray-400'}`}>
                        {theme.description}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Layout Density */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Layout className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">Layout Density</h3>
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {densities.map((density) => (
                    <button
                      key={density.id}
                      onClick={() => handleDensityChange(density)}
                      disabled={isSaving}
                      className={`p-3 rounded-lg border-2 transition-all duration-200 text-center ${
                        (previewDensity?.id === density.id || (!previewDensity && state.layoutDensity?.id === density.id))
                          ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                          : 'border-gray-200 hover:border-gray-300 dark:border-gray-700'
                      } ${isSaving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                    >
                      <div className={`font-medium text-sm ${state.layoutDensity?.id === density.id ? 'text-gray-900 dark:text-teal-100' : 'text-gray-900 dark:text-gray-100'}`}>
                        {density.name}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Font Size */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Type className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">Font Size</h3>
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {fontSizes.map((fontSize) => (
                    <button
                      key={fontSize.id}
                      onClick={() => handleFontSizeChange(fontSize)}
                      disabled={isSaving}
                      className={`p-3 rounded-lg border-2 transition-all duration-200 text-center ${
                        (previewFontSize?.id === fontSize.id || (!previewFontSize && state.fontSize?.id === fontSize.id))
                          ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                          : 'border-gray-200 hover:border-gray-300 dark:border-gray-700'
                      } ${isSaving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                    >
                      <div className={`font-medium text-sm ${state.fontSize?.id === fontSize.id ? 'text-gray-900 dark:text-teal-100' : 'text-gray-900 dark:text-gray-100'}`}>
                        {fontSize.name}
                      </div>
                      {fontSize.base_font_size && (
                        <div className={`text-xs mt-1 ${state.fontSize?.id === fontSize.id ? 'text-gray-500 dark:text-teal-200' : 'text-gray-500 dark:text-gray-400'}`}>
                          {fontSize.base_font_size}
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* System Theme Info */}
              {state.theme?.code === 'system' && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <span className="text-sm text-blue-800">
                      Following system preference: {state.systemTheme || 'detecting...'}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800">
          {hasUnsavedChanges ? (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <p className="text-sm text-yellow-800 dark:text-yellow-200">
                  You have unsaved changes
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleCancelChanges}
                  disabled={isSaving}
                  className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleApplyChanges}
                  disabled={isSaving}
                  className="px-4 py-2 text-sm font-medium text-white bg-teal-600 dark:bg-teal-500 rounded-lg hover:bg-teal-700 dark:hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isSaving ? 'Saving...' : 'Apply'}
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Select a preference to preview, then click Apply to save
              </p>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-teal-600 dark:bg-teal-500 text-white rounded-lg hover:bg-teal-700 dark:hover:bg-teal-600 transition-colors"
              >
                Done
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
