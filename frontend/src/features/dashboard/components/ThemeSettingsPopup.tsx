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
  const { state, dispatch, applyTheme, applyLayoutDensity, applyFontSize, saveToLocalStorage } = useTheme()
  const toast = useToastNotifications()
  
  const [themes, setThemes] = useState<ReferenceOption[]>([])
  const [densities, setDensities] = useState<ReferenceOption[]>([])
  const [fontSizes, setFontSizes] = useState<ReferenceOption[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  
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

  // Handle theme selection
  const handleThemeChange = async (theme: ReferenceOption) => {
    try {
      setIsSaving(true)
      applyTheme(theme)
      dispatch({ type: 'SET_THEME', payload: theme })
      console.log('Calling updateProfile with themePreferenceId:', theme.id)
      const result = await updateProfile({ themePreferenceId: theme.id })
      console.log('Theme update response:', JSON.stringify(result, null, 2))
      
      // Verify response
      if (!result || !result.success) {
        throw new Error(`API returned unsuccessful response: ${result?.message || 'Unknown error'}`)
      }
      
      // Save was successful - the theme is already applied and state is updated
      // Don't reload from backend immediately as it might return cached/stale data
      // The preferences will be loaded correctly on next login/refresh
      console.log('Theme saved successfully to backend. Using current theme:', theme.name)
      
      // State change will trigger useEffect to save to localStorage
      toast.success(`Theme changed to ${theme.name}`)
    } catch (error) {
      console.error('Failed to update theme:', error)
      // Log detailed error information
      if (error instanceof Error) {
        console.error('Error message:', error.message)
        console.error('Error stack:', error.stack)
      }
      // Check if it's an Axios error
      if ((error as any).response) {
        console.error('API Response:', (error as any).response.status, (error as any).response.data)
      }
      toast.error(`Failed to save theme preference: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsSaving(false)
    }
  }

  // Handle density selection
  const handleDensityChange = async (density: ReferenceOption) => {
    try {
      setIsSaving(true)
      applyLayoutDensity(density)
      dispatch({ type: 'SET_LAYOUT_DENSITY', payload: density })
      console.log('Calling updateProfile with layoutDensityId:', density.id)
      const result = await updateProfile({ layoutDensityId: density.id })
      console.log('Density update response:', JSON.stringify(result, null, 2))
      
      // Verify response
      if (!result || !result.success) {
        throw new Error(`API returned unsuccessful response: ${result?.message || 'Unknown error'}`)
      }
      
      // Save was successful - the density is already applied and state is updated
      console.log('Layout density saved successfully to backend. Using current density:', density.name)
      
      // State change will trigger useEffect to save to localStorage
      toast.success(`Layout density changed to ${density.name}`)
    } catch (error) {
      console.error('Failed to update density:', error)
      if (error instanceof Error) {
        console.error('Error message:', error.message)
        console.error('Error stack:', error.stack)
      }
      if ((error as any).response) {
        console.error('API Response:', (error as any).response.status, (error as any).response.data)
      }
      toast.error(`Failed to save density preference: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsSaving(false)
    }
  }

  // Handle font size selection
  const handleFontSizeChange = async (fontSize: ReferenceOption) => {
    try {
      setIsSaving(true)
      applyFontSize(fontSize)
      dispatch({ type: 'SET_FONT_SIZE', payload: fontSize })
      console.log('Calling updateProfile with fontSizeId:', fontSize.id)
      const result = await updateProfile({ fontSizeId: fontSize.id })
      console.log('Font size update response:', JSON.stringify(result, null, 2))
      
      // Verify response
      if (!result || !result.success) {
        throw new Error(`API returned unsuccessful response: ${result?.message || 'Unknown error'}`)
      }
      
      // Save was successful - the font size is already applied and state is updated
      console.log('Font size saved successfully to backend. Using current font size:', fontSize.name)
      
      // State change will trigger useEffect to save to localStorage
      toast.success(`Font size changed to ${fontSize.name}`)
    } catch (error) {
      console.error('Failed to update font size:', error)
      if (error instanceof Error) {
        console.error('Error message:', error.message)
        console.error('Error stack:', error.stack)
      }
      if ((error as any).response) {
        console.error('API Response:', (error as any).response.status, (error as any).response.data)
      }
      toast.error(`Failed to save font size preference: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsSaving(false)
    }
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
                        state.theme?.id === theme.id
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
                        state.layoutDensity?.id === density.id
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
                        state.fontSize?.id === fontSize.id
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
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Changes are saved automatically
            </p>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-teal-600 dark:bg-teal-500 text-white rounded-lg hover:bg-teal-700 dark:hover:bg-teal-600 transition-colors"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
