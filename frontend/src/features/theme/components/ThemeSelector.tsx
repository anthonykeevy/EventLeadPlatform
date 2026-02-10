/**
 * Theme Selector Component for Epic 2 Story 2.2
 * Allows users to select theme, layout density, and font size preferences
 */

import { useState, useEffect } from 'react'
import { useTheme } from '../context/ThemeContext'
import { ReferenceOption } from '../../profile/types/profile.types'
import { updateProfile } from '../../profile/api/usersApi'
import { useToastNotifications } from '../../ux'

interface ThemeSelectorProps {
  className?: string
  showLabels?: boolean
  compact?: boolean
  themes?: ReferenceOption[]
  densities?: ReferenceOption[]
  fontSizes?: ReferenceOption[]
  previewMode?: boolean // Story 2.3: Enable preview mode (preview before save)
}

export function ThemeSelector({ 
  className = '', 
  showLabels = true, 
  compact: _compact = false,
  themes = [],
  densities = [],
  fontSizes = [],
  previewMode = false // Default to Story 2.2 behavior (immediate save)
}: ThemeSelectorProps) {
  const { state, dispatch, applyTheme, applyLayoutDensity, applyFontSize } = useTheme()
  const toast = useToastNotifications()
  
  const [isSaving, setIsSaving] = useState(false)
  // Preview mode state (Story 2.3)
  const [previewTheme, setPreviewTheme] = useState<ReferenceOption | null>(null)
  const [previewDensity, setPreviewDensity] = useState<ReferenceOption | null>(null)
  const [previewFontSize, setPreviewFontSize] = useState<ReferenceOption | null>(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)

  // Set default selections if not already set
  useEffect(() => {
    if (!state.theme && themes.length > 0) {
      const defaultTheme = themes.find(t => t.code === 'system') || themes[0]
      dispatch({ type: 'SET_THEME', payload: defaultTheme })
    }
    
    if (!state.layoutDensity && densities.length > 0) {
      const defaultDensity = densities.find(d => d.code === 'comfortable') || densities[0]
      dispatch({ type: 'SET_LAYOUT_DENSITY', payload: defaultDensity })
    }
    
    if (!state.fontSize && fontSizes.length > 0) {
      const defaultFontSize = fontSizes.find(f => f.code === 'medium') || fontSizes[0]
      dispatch({ type: 'SET_FONT_SIZE', payload: defaultFontSize })
    }
  }, [themes, densities, fontSizes, state.theme, state.layoutDensity, state.fontSize, dispatch])

  // Handle theme selection
  const handleThemeChange = async (theme: ReferenceOption) => {
    if (previewMode) {
      // Story 2.3: Preview mode - apply temporarily without saving
      setPreviewTheme(theme)
      applyTheme(theme) // Apply preview immediately for visual feedback
      setHasUnsavedChanges(true)
    } else {
      // Story 2.2: Immediate save behavior
      try {
        setIsSaving(true)
        
        // Apply theme immediately for visual feedback
        applyTheme(theme)
        dispatch({ type: 'SET_THEME', payload: theme })
        
        // Save to backend
        await updateProfile({ themePreferenceId: theme.id })
        
        toast.success(`Theme changed to ${theme.name}`)
      } catch (error) {
        console.error('Failed to update theme:', error)
        toast.error('Failed to save theme preference')
        
        // Revert on error
        if (state.theme) {
          applyTheme(state.theme)
        }
      } finally {
        setIsSaving(false)
      }
    }
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
        await updateProfile(updates)
        
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

  // Handle layout density selection
  const handleDensityChange = async (density: ReferenceOption) => {
    if (previewMode) {
      // Story 2.3: Preview mode - apply temporarily without saving
      setPreviewDensity(density)
      applyLayoutDensity(density) // Apply preview immediately for visual feedback
      setHasUnsavedChanges(true)
    } else {
      // Story 2.2: Immediate save behavior
      try {
        setIsSaving(true)
        
        // Apply density immediately for visual feedback
        applyLayoutDensity(density)
        dispatch({ type: 'SET_LAYOUT_DENSITY', payload: density })
        
        // Save to backend
        await updateProfile({ layoutDensityId: density.id })
        
        toast.success(`Layout density changed to ${density.name}`)
      } catch (error) {
        console.error('Failed to update layout density:', error)
        toast.error('Failed to save layout density preference')
        
        // Revert on error
        if (state.layoutDensity) {
          applyLayoutDensity(state.layoutDensity)
        }
      } finally {
        setIsSaving(false)
      }
    }
  }

  // Handle font size selection
  const handleFontSizeChange = async (fontSize: ReferenceOption) => {
    if (previewMode) {
      // Story 2.3: Preview mode - apply temporarily without saving
      setPreviewFontSize(fontSize)
      applyFontSize(fontSize) // Apply preview immediately for visual feedback
      setHasUnsavedChanges(true)
    } else {
      // Story 2.2: Immediate save behavior
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
  }

  if (themes.length === 0 || densities.length === 0 || fontSizes.length === 0) {
    return (
      <div className={`theme-selector ${className}`}>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="space-y-2">
            <div className="h-8 bg-gray-200 rounded"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  if (state.error) {
    return (
      <div className={`theme-selector ${className}`}>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800 text-sm">{state.error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`theme-selector ${className}`}>
      <div className="space-y-6">
        {/* Theme Selection */}
        <div className="space-y-3">
          {showLabels && (
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Theme
            </label>
          )}
          <div className="grid grid-cols-2 gap-2">
            {themes.map((theme) => (
              <button
                key={theme.id}
                onClick={() => handleThemeChange(theme)}
                disabled={isSaving}
                className={`
                  relative p-3 rounded-lg border-2 transition-all duration-200
                  ${state.theme?.id === theme.id
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 hover:border-gray-300 dark:border-gray-700 dark:hover:border-gray-600'
                  }
                  ${isSaving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-md'}
                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                `}
                aria-pressed={state.theme?.id === theme.id}
                aria-label={`Select ${theme.name} theme`}
              >
                <div className="text-center">
                  <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {theme.name}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {theme.description}
                  </div>
                </div>
                {state.theme?.id === theme.id && (
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

        {/* Layout Density Selection */}
        <div className="space-y-3">
          {showLabels && (
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Layout Density
            </label>
          )}
          <div className="grid grid-cols-3 gap-2">
            {densities.map((density) => (
              <button
                key={density.id}
                onClick={() => handleDensityChange(density)}
                disabled={isSaving}
                className={`
                  relative p-3 rounded-lg border-2 transition-all duration-200
                  ${state.layoutDensity?.id === density.id
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 hover:border-gray-300 dark:border-gray-700 dark:hover:border-gray-600'
                  }
                  ${isSaving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-md'}
                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                `}
                aria-pressed={state.layoutDensity?.id === density.id}
                aria-label={`Select ${density.name} layout density`}
              >
                <div className="text-center">
                  <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {density.name}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {density.description}
                  </div>
                </div>
                {state.layoutDensity?.id === density.id && (
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

        {/* Font Size Selection */}
        <div className="space-y-3">
          {showLabels && (
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Font Size
            </label>
          )}
          <div className="grid grid-cols-3 gap-2">
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
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {fontSize.base_font_size}
                  </div>
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

        {/* System Theme Info */}
        {state.theme?.code === 'system' && (
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
            <div className="flex items-center">
              <svg className="w-4 h-4 text-blue-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <span className="text-sm text-blue-800 dark:text-blue-200">
                Following system preference: {state.systemTheme || 'detecting...'}
              </span>
            </div>
          </div>
        )}

        {/* Preview Mode Controls (Story 2.3) */}
        {previewMode && hasUnsavedChanges && (
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mt-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-yellow-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <span className="text-sm text-yellow-800 dark:text-yellow-200">
                  You have unsaved preference changes. Click Apply to save or Cancel to revert.
                </span>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={handleCancelChanges}
                  disabled={isSaving}
                  className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Cancel
                </button>
                <button
                  onClick={handleApplyChanges}
                  disabled={isSaving}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 dark:bg-blue-500 rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSaving ? 'Saving...' : 'Apply'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ThemeSelector
