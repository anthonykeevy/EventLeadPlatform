/**
 * Account Settings Popup Component
 * Shows user profile details and allows editing preferences
 */

import React, { useState, useEffect, useRef } from 'react'
import { X, User, Mail, FileText, Briefcase } from 'lucide-react'
import { useAuth } from '../../auth'
import { 
  getEnhancedProfile, 
  updateProfile,
  updateUserDetails,
  getUserProfile,
  type UpdateUserDetailsRequest
} from '../../profile/api/usersApi'
import type { 
  EnhancedUserProfile
} from '../../profile/types/profile.types'
import { useToastNotifications } from '../../ux'
import { IndustryManager } from './IndustryManager'

// Note: IndustryManager is imported from preferences/components, not profile/components

interface AccountSettingsPopupProps {
  isOpen: boolean
  onClose: () => void
}

export function AccountSettingsPopup({ isOpen, onClose }: AccountSettingsPopupProps) {
  const { refreshUser, user: authUser } = useAuth()
  const toast = useToastNotifications()
  
  const [profile, setProfile] = useState<EnhancedUserProfile | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [roleTitle, setRoleTitle] = useState('')
  const [bio, setBio] = useState('')
  const [timezone, setTimezone] = useState('Australia/Sydney') // Default timezone, will be updated when profile loads
  const [hasChanges, setHasChanges] = useState(false)
  
  // Track if data has been loaded to prevent multiple calls
  const dataLoadedRef = useRef(false)
  const isLoadingRef = useRef(false)

  // Load profile data - only once when popup opens
  useEffect(() => {
    // Only load if popup is open, data hasn't been loaded, and not currently loading
    if (isOpen && !dataLoadedRef.current && !isLoadingRef.current) {
      isLoadingRef.current = true
      
      const loadData = async () => {
        try {
          setIsLoading(true)
          // Load both enhanced profile and basic profile (for timezone)
          const [profileData, userProfile] = await Promise.all([
            getEnhancedProfile(),
            getUserProfile()
          ])
          
          setProfile(profileData)
          setFirstName(profileData.firstName || '')
          setLastName(profileData.lastName || '')
          setRoleTitle(profileData.roleTitle || '')
          setBio(profileData.bio || '')
          setTimezone(userProfile.timezone_identifier || 'Australia/Sydney')
          dataLoadedRef.current = true
        } catch (error) {
          console.error('Failed to load profile data:', error)
          toast.error('Failed to load profile data')
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
  }, [isOpen, toast])

  // Track changes
  useEffect(() => {
    if (profile) {
      const firstNameChanged = firstName !== (profile.firstName || '')
      const lastNameChanged = lastName !== (profile.lastName || '')
      const roleTitleChanged = roleTitle !== (profile.roleTitle || '')
      const bioChanged = bio !== (profile.bio || '')
      setHasChanges(firstNameChanged || lastNameChanged || roleTitleChanged || bioChanged)
    }
  }, [firstName, lastName, roleTitle, bio, profile])

  // Handle ESC key to close
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        if (hasChanges) {
          if (confirm('You have unsaved changes. Are you sure you want to close?')) {
            onClose()
          }
        } else {
          onClose()
        }
      }
    }
    
    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [isOpen, hasChanges, onClose])

  // Handle save
  const handleSave = async () => {
    if (!profile) return
    
    setIsSaving(true)
    
    try {
      // Update user details (firstName, lastName, position title) via /me/details endpoint
      // This endpoint requires timezone_identifier, which we get from user profile
      const detailsRequest: UpdateUserDetailsRequest = {
        first_name: firstName || undefined,
        last_name: lastName || undefined,
        role_title: roleTitle || null,
        timezone_identifier: timezone, // Get from user profile (loaded on mount)
        phone: profile.phone || null
      }
      
      console.log('[AccountSettingsPopup] Updating user details:', detailsRequest)
      await updateUserDetails(detailsRequest)
      
      // Update bio via profile enhancements endpoint
      await updateProfile({
        bio: bio || null
      })
      
      // Refresh user data
      await refreshUser()
      
      // Reload profile to get updated data
      const updatedProfile = await getEnhancedProfile()
      setProfile(updatedProfile)
      setFirstName(updatedProfile.firstName || '')
      setLastName(updatedProfile.lastName || '')
      setRoleTitle(updatedProfile.roleTitle || '')
      setBio(updatedProfile.bio || '')
      setHasChanges(false)
      
      toast.success('Profile updated successfully')
    } catch (error) {
      console.error('Failed to save profile:', error)
      toast.error('Failed to save profile changes')
    } finally {
      setIsSaving(false)
    }
  }

  // Handle industries updated (callback from IndustryManager)
  const handleIndustriesUpdated = async () => {
    // Refresh profile to get updated industry data
    try {
      const updatedProfile = await getEnhancedProfile()
      setProfile(updatedProfile)
    } catch (error) {
      console.error('Failed to reload profile:', error)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <User className="w-5 h-5 text-teal-600 dark:text-teal-400" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Account Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            aria-label="Close account settings"
          >
            <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
              <span className="ml-3 text-gray-600 dark:text-gray-400">Loading profile data...</span>
            </div>
          ) : profile ? (
            <div className="space-y-6">
              {/* User Information */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <User className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">Personal Information</h3>
                </div>
                
                <div className="space-y-4">
                  {/* First Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      First Name
                    </label>
                    <input
                      type="text"
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                      placeholder="First name"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:text-white"
                      maxLength={100}
                    />
                  </div>

                  {/* Last Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Last Name
                    </label>
                    <input
                      type="text"
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                      placeholder="Last name"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:text-white"
                      maxLength={100}
                    />
                  </div>

                  {/* Email */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      <Mail className="w-4 h-4 inline mr-1" />
                      Email
                    </label>
                    <div className="text-gray-900 dark:text-gray-100">
                      {profile.email}
                      {profile.isEmailVerified && (
                        <span className="ml-2 text-xs text-green-600 dark:text-green-400">✓ Verified</span>
                      )}
                    </div>
                  </div>

                  {/* Position Title */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      <Briefcase className="w-4 h-4 inline mr-1" />
                      Position Title
                    </label>
                    <input
                      type="text"
                      value={roleTitle}
                      onChange={(e) => setRoleTitle(e.target.value)}
                      placeholder="e.g., Marketing Manager, Event Coordinator"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:text-white"
                      maxLength={100}
                    />
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Your job position or title
                    </p>
                  </div>

                  {/* Bio */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      <FileText className="w-4 h-4 inline mr-1" />
                      Bio
                    </label>
                    <textarea
                      value={bio}
                      onChange={(e) => {
                        if (e.target.value.length <= 500) {
                          setBio(e.target.value)
                        }
                      }}
                      placeholder="Tell us about yourself..."
                      rows={4}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:text-white resize-none"
                      maxLength={500}
                    />
                    <div className="flex items-center justify-between mt-1">
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Professional bio or summary (optional)
                      </p>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {bio.length}/500
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Industry Associations */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Briefcase className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">Industry Associations</h3>
                </div>
                <IndustryManager onUpdate={handleIndustriesUpdated} />
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-600 dark:text-gray-400">Failed to load profile data</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {hasChanges ? 'You have unsaved changes' : 'All changes are saved'}
            </p>
            <div className="flex items-center gap-3">
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              >
                {hasChanges ? 'Cancel' : 'Close'}
              </button>
              <button
                onClick={handleSave}
                disabled={!hasChanges || isSaving}
                className="px-4 py-2 bg-teal-600 dark:bg-teal-500 text-white rounded-lg hover:bg-teal-700 dark:hover:bg-teal-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSaving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

