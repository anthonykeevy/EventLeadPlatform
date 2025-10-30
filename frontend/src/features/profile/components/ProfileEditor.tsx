/**
 * Profile Editor Component for Epic 2 Story 2.1
 * Allows users to update bio, theme preferences, layout density, and font size
 */

import React, { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Loader2, Save, X } from 'lucide-react'
import type { EnhancedUserProfile, ProfileUpdateRequest, ReferenceOption } from '../types/profile.types'
import {
  getEnhancedProfile,
  updateProfile,
  getThemes,
  getLayoutDensities,
  getFontSizes
} from '../api/usersApi'
import { useToastNotifications } from '../../ux'

interface ProfileEditorProps {
  onClose?: () => void
}

export function ProfileEditor({ onClose }: ProfileEditorProps) {
  const [profile, setProfile] = useState<EnhancedUserProfile | null>(null)
  const [themes, setThemes] = useState<ReferenceOption[]>([])
  const [densities, setDensities] = useState<ReferenceOption[]>([])
  const [fontSizes, setFontSizes] = useState<ReferenceOption[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const { showSuccessToast, showErrorToast } = useToastNotifications()

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isDirty }
  } = useForm<ProfileUpdateRequest>({
    mode: 'onChange',
    defaultValues: {
      bio: '',
      themePreferenceId: null,
      layoutDensityId: null,
      fontSizeId: null
    }
  })

  const bioValue = watch('bio')
  const themeId = watch('themePreferenceId')
  const densityId = watch('layoutDensityId')
  const fontSizeId = watch('fontSizeId')

  // Load profile and reference data
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true)
      setApiError(null)
      
      try {
        const [profileData, themesData, densitiesData, fontSizesData] = await Promise.all([
          getEnhancedProfile(),
          getThemes(),
          getLayoutDensities(),
          getFontSizes()
        ])
        
        setProfile(profileData)
        setThemes(themesData)
        setDensities(densitiesData)
        setFontSizes(fontSizesData)
        
        // Set form values
        setValue('bio', profileData.bio || '')
        setValue('themePreferenceId', profileData.themePreference?.id || null)
        setValue('layoutDensityId', profileData.layoutDensity?.id || null)
        setValue('fontSizeId', profileData.fontSize?.id || null)
      } catch (error) {
        setApiError(error instanceof Error ? error.message : 'Failed to load profile')
        showErrorToast('Failed to load profile data')
      } finally {
        setIsLoading(false)
      }
    }
    
    loadData()
  }, [setValue, showErrorToast])

  const onSubmit = async (data: ProfileUpdateRequest) => {
    setIsSaving(true)
    setApiError(null)
    
    try {
      await updateProfile(data)
      setProfile(await getEnhancedProfile())
      showSuccessToast('Profile updated successfully')
      
      if (onClose) {
        onClose()
      }
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to update profile')
      showErrorToast('Failed to update profile')
    } finally {
      setIsSaving(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-8 h-8 animate-spin text-teal-600" />
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Edit Profile</h2>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close"
          >
            <X className="w-6 h-6" />
          </button>
        )}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* API Error Display */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-800">
            {apiError}
          </div>
        )}

        {/* Bio Field */}
        <div>
          <label htmlFor="bio" className="block text-sm font-medium text-gray-700 mb-2">
            Professional Bio
          </label>
          <textarea
            id="bio"
            rows={4}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
              errors.bio ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Tell us about yourself..."
            {...register('bio', {
              maxLength: {
                value: 500,
                message: 'Bio must be 500 characters or less'
              }
            })}
          />
          <div className="flex items-center justify-between mt-1">
            {errors.bio && (
              <p className="text-sm text-red-600">{errors.bio.message}</p>
            )}
            <span className={`text-sm ml-auto ${
              (bioValue?.length || 0) > 500 ? 'text-red-600' : 'text-gray-500'
            }`}>
              {bioValue?.length || 0} / 500
            </span>
          </div>
        </div>

        {/* Theme Preference */}
        <div>
          <label htmlFor="theme" className="block text-sm font-medium text-gray-700 mb-2">
            Theme Preference
          </label>
          <select
            id="theme"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            {...register('themePreferenceId', {
              setValueAs: (value) => value === '' ? null : parseInt(value)
            })}
          >
            <option value="">Select theme...</option>
            {themes.map((theme) => (
              <option key={theme.id} value={theme.id}>
                {theme.name} - {theme.description}
              </option>
            ))}
          </select>
          {themeId && (
            <p className="mt-1 text-sm text-gray-500">
              {themes.find(t => t.id === themeId)?.description}
            </p>
          )}
        </div>

        {/* Layout Density */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Layout Density
          </label>
          <div className="space-y-2">
            {densities.map((density) => (
              <label
                key={density.id}
                className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  densityId === density.id
                    ? 'border-teal-500 bg-teal-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  value={density.id}
                  {...register('layoutDensityId', {
                    setValueAs: (value) => value === '' ? null : parseInt(value)
                  })}
                  className="w-5 h-5 text-teal-600 focus:ring-teal-500"
                />
                <div className="ml-3">
                  <div className="font-medium text-gray-900">{density.name}</div>
                  <div className="text-sm text-gray-500">{density.description}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Font Size */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Font Size
          </label>
          <div className="space-y-2">
            {fontSizes.map((fontSize) => (
              <label
                key={fontSize.id}
                className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  fontSizeId === fontSize.id
                    ? 'border-teal-500 bg-teal-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  value={fontSize.id}
                  {...register('fontSizeId', {
                    setValueAs: (value) => value === '' ? null : parseInt(value)
                  })}
                  className="w-5 h-5 text-teal-600 focus:ring-teal-500"
                />
                <div className="ml-3 flex-1">
                  <div className="font-medium text-gray-900 flex items-center justify-between">
                    <span>{fontSize.name}</span>
                    <span className="text-xs text-gray-500">{fontSize.baseFontSize}</span>
                  </div>
                  <div className="text-sm text-gray-500">{fontSize.description}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end gap-4 pt-4 border-t">
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
          )}
          <button
            type="submit"
            disabled={isSaving || !isDirty}
            className={`px-6 py-2 text-white rounded-lg transition-colors flex items-center gap-2 ${
              isSaving || !isDirty
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-teal-600 hover:bg-teal-700'
            }`}
          >
            {isSaving ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="w-5 h-5" />
                Save Changes
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

