/**
 * Theme Settings Page for Epic 2 Story 2.2
 * Complete theme customization interface
 */

import React, { useState, useEffect } from 'react'
import { ThemeSelector } from '../components/ThemeSelector'
import { DensitySelector } from '../components/DensitySelector'
import { FontSizeSelector } from '../components/FontSizeSelector'
import { useTheme } from '../context/ThemeContext'
import { ReferenceOption } from '../../profile/types/profile.types'
import { getThemes, getLayoutDensities, getFontSizes } from '../../profile/api/usersApi'

export function ThemeSettingsPage() {
  const { state } = useTheme()
  const [themes, setThemes] = useState<ReferenceOption[]>([])
  const [densities, setDensities] = useState<ReferenceOption[]>([])
  const [fontSizes, setFontSizes] = useState<ReferenceOption[]>([])
  const [isLoading, setIsLoading] = useState(true)

  // Load all theme reference data once
  useEffect(() => {
    const loadAllData = async () => {
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
      } catch (error) {
        console.error('Failed to load theme reference data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadAllData()
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading theme options...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Theme Settings
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Customize your interface theme, layout density, and font size preferences.
          </p>
        </div>

        {/* Current Settings Summary */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Current Settings
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Theme
              </h3>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {state.theme?.name || 'Not set'}
              </p>
              {state.theme?.code === 'system' && state.systemTheme && (
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  System: {state.systemTheme}
                </p>
              )}
            </div>
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Layout Density
              </h3>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {state.layoutDensity?.name || 'Not set'}
              </p>
            </div>
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                Font Size
              </h3>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {state.fontSize?.name || 'Not set'}
              </p>
              {state.fontSize?.base_font_size && (
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {state.fontSize.base_font_size}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Theme Customization */}
        <div className="space-y-8">
          {/* Theme Selection */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Theme Selection
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Choose your preferred color scheme. The system theme will automatically follow your operating system's preference.
            </p>
            <ThemeSelector showLabels={false} themes={themes} densities={densities} fontSizes={fontSizes} />
          </div>

          {/* Layout Density */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Layout Density
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Adjust the spacing and density of interface elements to match your preference.
            </p>
            <DensitySelector showLabel={false} densities={densities} />
          </div>

          {/* Font Size */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Font Size
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Choose the text size that's most comfortable for reading.
            </p>
            <FontSizeSelector showLabel={false} fontSizes={fontSizes} />
          </div>
        </div>

        {/* Preview Section */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Preview
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            See how your theme settings look with sample content.
          </p>
          
          <div className="space-y-4">
            {/* Sample Card */}
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Sample Card
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                This is a sample card to demonstrate how your theme settings affect the interface.
              </p>
              <div className="flex space-x-2">
                <button className="btn-primary">
                  Primary Button
                </button>
                <button className="btn-secondary">
                  Secondary Button
                </button>
                <button className="btn-outline">
                  Outline Button
                </button>
              </div>
            </div>

            {/* Sample Form */}
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Sample Form
              </h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Sample Input
                  </label>
                  <input
                    type="text"
                    className="input-enhanced w-full"
                    placeholder="Enter some text..."
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Sample Select
                  </label>
                  <select className="input-enhanced w-full">
                    <option>Option 1</option>
                    <option>Option 2</option>
                    <option>Option 3</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Sample Status Messages */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-green-800 dark:text-green-200 font-medium">
                    Success Message
                  </span>
                </div>
                <p className="text-green-700 dark:text-green-300 text-sm mt-1">
                  This is a success message example.
                </p>
              </div>

              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <span className="text-red-800 dark:text-red-200 font-medium">
                    Error Message
                  </span>
                </div>
                <p className="text-red-700 dark:text-red-300 text-sm mt-1">
                  This is an error message example.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>
            Theme preferences are automatically saved and will be restored when you return.
          </p>
        </div>
      </div>
    </div>
  )
}

export default ThemeSettingsPage
