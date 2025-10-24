/**
 * Onboarding Step 1 - User Details
 * AC-1.14.2, AC-1.14.3: Collect user profile information
 */

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Loader2 } from 'lucide-react'
import type { OnboardingStep1Data } from '../types/onboarding.types'
import { getAccessToken } from '../../auth/utils/tokenStorage'
import { PhoneInput, CountrySelector } from '../../validation'

interface OnboardingStep1Props {
  initialData: OnboardingStep1Data | null
  onComplete: (data: OnboardingStep1Data) => void
  user: any
}

export function OnboardingStep1({ initialData, onComplete, user }: OnboardingStep1Props) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [selectedCountry, setSelectedCountry] = useState<number>(1)  // Default: Australia

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isValid }
  } = useForm<OnboardingStep1Data>({
    mode: 'onChange',
    defaultValues: initialData || {
      firstName: user?.first_name || '',
      lastName: user?.last_name || '',
      phone: '',
      roleTitle: ''
    }
  })

  const phoneValue = watch('phone')

  const onSubmit = async (data: OnboardingStep1Data) => {
    setIsSubmitting(true)
    setApiError(null)

    try {
      // Call backend API to update user details
      const token = getAccessToken()
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.')
      }

      const response = await fetch('http://localhost:8000/api/users/me/details', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          phone: data.phone || null,
          timezone_identifier: 'Australia/Sydney', // Default timezone for Epic 1
          role_title: data.roleTitle || null
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to save user details')
      }

      // Proceed to Step 2 - include country selection
      onComplete({
        ...data,
        countryId: selectedCountry
      })
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to save details')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div>
      <h3 className="text-2xl font-semibold text-gray-900 mb-2">
        Tell us about yourself
      </h3>
      <p className="text-gray-600 mb-6">
        We'll use this information to personalize your experience
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        {/* API Error Display */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-800">
            {apiError}
          </div>
        )}

        {/* First Name */}
        <div>
          <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
            First Name <span className="text-red-500">*</span>
          </label>
          <input
            id="firstName"
            type="text"
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
              errors.firstName ? 'border-red-500' : 'border-gray-300'
            }`}
            {...register('firstName', {
              required: 'First name is required',
              minLength: { value: 2, message: 'First name must be at least 2 characters' }
            })}
          />
          {errors.firstName && (
            <p className="mt-1 text-sm text-red-600">{errors.firstName.message}</p>
          )}
        </div>

        {/* Last Name */}
        <div>
          <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
            Last Name <span className="text-red-500">*</span>
          </label>
          <input
            id="lastName"
            type="text"
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
              errors.lastName ? 'border-red-500' : 'border-gray-300'
            }`}
            {...register('lastName', {
              required: 'Last name is required',
              minLength: { value: 2, message: 'Last name must be at least 2 characters' }
            })}
          />
          {errors.lastName && (
            <p className="mt-1 text-sm text-red-600">{errors.lastName.message}</p>
          )}
        </div>

        {/* Country Selection - Story 1.20 */}
        <CountrySelector
          value={selectedCountry}
          onChange={setSelectedCountry}
          autoDetect={true}
        />
        
        {/* Phone Number - Story 1.20 Integration */}
        <PhoneInput
          id="phone"
          name="phone"
          value={phoneValue || ''}
          onChange={(value) => setValue('phone', value)}
          countryId={selectedCountry}
          onCountryDetected={setSelectedCountry}
          required={false}
        />

        {/* Role/Title */}
        <div>
          <label htmlFor="roleTitle" className="block text-sm font-medium text-gray-700 mb-1">
            Role/Title <span className="text-gray-400">(optional)</span>
          </label>
          <input
            id="roleTitle"
            type="text"
            placeholder="e.g., Marketing Manager, Event Coordinator"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            {...register('roleTitle')}
          />
        </div>

        {/* Next Button */}
        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={!isValid || isSubmitting}
            className={`px-8 py-3 rounded-lg font-medium text-white transition-colors flex items-center gap-2 ${
              !isValid || isSubmitting
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-teal-600 hover:bg-teal-700'
            }`}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Saving...
              </>
            ) : (
              'Next: Company Setup'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}



