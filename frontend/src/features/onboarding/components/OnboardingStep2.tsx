/**
 * Onboarding Step 2 - Company Setup
 * AC-1.14.3, AC-1.14.4, AC-1.14.5: Company details with ABR search integration
 */

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Loader2, ArrowLeft, Building2 } from 'lucide-react'
import type { OnboardingStep2Data } from '../types/onboarding.types'
import { getAccessToken, storeTokens } from '../../auth/utils/tokenStorage'
import { PostalCodeInput, CountrySelector, useCountries } from '../../validation'
import { getCountryConfig, getStateOptions } from '../../validation/utils/countryConfig'

interface OnboardingStep2Props {
  initialData: OnboardingStep2Data | null
  onComplete: (data: OnboardingStep2Data) => void
  onBack: () => void
  initialCountryId?: number  // From Step 1 country selection
}

export function OnboardingStep2({ initialData, onComplete, onBack, initialCountryId }: OnboardingStep2Props) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [companyCountry, setCompanyCountry] = useState<number>(initialCountryId || 1)  // From Step 1 or default
  
  // Get country-specific labels and configuration
  const countryConfig = getCountryConfig(companyCountry)

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isValid }
  } = useForm<OnboardingStep2Data>({
    mode: 'onChange',
    defaultValues: initialData || {
      companyName: '',
      abn: '',
      gstRegistered: false,
      billingAddress: '',
      billingSuburb: '',
      billingState: '',
      billingPostcode: '',
      billingCountry: 'Australia'
    }
  })

  const postcodeValue = watch('billingPostcode')
  const abnValue = watch('abn')

  const onSubmit = async (data: OnboardingStep2Data) => {
    setIsSubmitting(true)
    setApiError(null)

    try {
      // Call backend API to create company
      const token = getAccessToken()
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.')
      }

      // Remove spaces from ABN for submission
      const cleanedABN = data.abn.replace(/\s/g, '')

      const response = await fetch('http://localhost:8000/api/companies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          company_name: data.companyName,
          abn: cleanedABN,
          acn: null,
          phone: null,
          email: null,
          website: null,
          country_id: companyCountry,  // Story 1.20: User-selected country
          industry_id: null
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create company')
      }

      const result = await response.json()
      
      // Update tokens with new JWT that includes company context
      if (result.access_token && result.refresh_token) {
        storeTokens(result.access_token, result.refresh_token, 3600)
      }

      // Complete onboarding
      onComplete(data)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to create company')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div>
      <h3 className="text-2xl font-semibold text-gray-900 mb-2">
        Set up your company
      </h3>
      <p className="text-gray-600 mb-6">
        Tell us about your company to get started
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        {/* API Error Display */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-800">
            {apiError}
          </div>
        )}

        {/* Country Selection - Story 1.20 */}
        <div>
          <CountrySelector
            value={companyCountry}
            onChange={setCompanyCountry}
            autoDetect={false}
          />
          <p className="mt-1 text-xs text-gray-500">
            Company country (from Step 1). Change if your company is registered in a different country.
          </p>
        </div>

        {/* Company Search Note - Conditional based on country */}
        {countryConfig.hasCompanySearch && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <Building2 className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-blue-800">
                <p className="font-medium mb-1">{countryConfig.companySearchLabel}</p>
                <p className="text-blue-700">
                  Company search integration coming in Story 1.19. For now, please enter details manually.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Company Name */}
        <div>
          <label htmlFor="companyName" className="block text-sm font-medium text-gray-700 mb-1">
            Company Name <span className="text-red-500">*</span>
          </label>
          <input
            id="companyName"
            type="text"
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
              errors.companyName ? 'border-red-500' : 'border-gray-300'
            }`}
            {...register('companyName', {
              required: 'Company name is required',
              minLength: { value: 2, message: 'Company name must be at least 2 characters' }
            })}
          />
          {errors.companyName && (
            <p className="mt-1 text-sm text-red-600">{errors.companyName.message}</p>
          )}
        </div>

        {/* Tax ID (ABN/EIN/NZBN/VAT/BN) - Dynamic based on country */}
        <div>
          <label htmlFor="abn" className="block text-sm font-medium text-gray-700 mb-1">
            {countryConfig.taxIdLabel} {countryConfig.taxIdRequired && <span className="text-red-500">*</span>}
            {!countryConfig.taxIdRequired && <span className="text-gray-400">(optional)</span>}
          </label>
          <input
            id="abn"
            type="text"
            placeholder={countryConfig.taxIdExample}
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
              errors.abn ? 'border-red-500' : 'border-gray-300'
            }`}
            {...register('abn', {
              required: countryConfig.taxIdRequired ? `${countryConfig.taxIdLabel} is required` : false
            })}
          />
          {errors.abn && (
            <p className="mt-1 text-sm text-red-600">{errors.abn.message}</p>
          )}
          <p className="mt-1 text-xs text-gray-500">
            Example: {countryConfig.taxIdExample}
          </p>
        </div>

        {/* Tax Registration - Dynamic based on country */}
        <div>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
              {...register('gstRegistered')}
            />
            <span className="text-sm text-gray-700">{countryConfig.taxLabel} Registered</span>
          </label>
          <p className="ml-6 mt-1 text-xs text-gray-500">
            {countryConfig.taxRate ? `${(countryConfig.taxRate * 100).toFixed(0)}% ${countryConfig.taxLabel}` : 'Tax rate varies by location'}
          </p>
        </div>

        {/* Billing Address */}
        <div>
          <label htmlFor="billingAddress" className="block text-sm font-medium text-gray-700 mb-1">
            Billing Address <span className="text-red-500">*</span>
          </label>
          <input
            id="billingAddress"
            type="text"
            placeholder="Street address"
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
              errors.billingAddress ? 'border-red-500' : 'border-gray-300'
            }`}
            {...register('billingAddress', {
              required: 'Billing address is required'
            })}
          />
          {errors.billingAddress && (
            <p className="mt-1 text-sm text-red-600">{errors.billingAddress.message}</p>
          )}
        </div>

        {/* Address Details Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Suburb */}
          <div>
            <label htmlFor="billingSuburb" className="block text-sm font-medium text-gray-700 mb-1">
              Suburb <span className="text-red-500">*</span>
            </label>
            <input
              id="billingSuburb"
              type="text"
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
                errors.billingSuburb ? 'border-red-500' : 'border-gray-300'
              }`}
              {...register('billingSuburb', {
                required: 'Suburb is required'
              })}
            />
            {errors.billingSuburb && (
              <p className="mt-1 text-sm text-red-600">{errors.billingSuburb.message}</p>
            )}
          </div>

          {/* State/Province/County - Dynamic based on country */}
          <div>
            <label htmlFor="billingState" className="block text-sm font-medium text-gray-700 mb-1">
              {countryConfig.stateLabel} <span className="text-red-500">*</span>
            </label>
            <select
              id="billingState"
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent ${
                errors.billingState ? 'border-red-500' : 'border-gray-300'
              }`}
              {...register('billingState', {
                required: `${countryConfig.stateLabel} is required`
              })}
            >
              <option value="">Select {countryConfig.stateLabel}...</option>
              {getStateOptions(companyCountry).map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {errors.billingState && (
              <p className="mt-1 text-sm text-red-600">{errors.billingState.message}</p>
            )}
          </div>

          {/* Postcode/ZIP Code - Story 1.20 Integration */}
          <PostalCodeInput
            id="billingPostcode"
            name="billingPostcode"
            value={postcodeValue || ''}
            onChange={(value) => setValue('billingPostcode', value)}
            countryId={companyCountry}
            label={countryConfig.postcodeLabel}
            required={true}
          />
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between pt-6">
          <button
            type="button"
            onClick={onBack}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors flex items-center gap-2"
          >
            <ArrowLeft className="w-5 h-5" />
            Back
          </button>

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
                Creating Company...
              </>
            ) : (
              'Complete Onboarding'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}



