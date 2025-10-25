/**
 * Onboarding Step 2 - Company Setup
 * AC-1.14.3, AC-1.14.4, AC-1.14.5: Company details with ABR search integration
 */

import React, { useState, useCallback } from 'react'
import { useForm } from 'react-hook-form'
import { Loader2, ArrowLeft, Building2, Edit } from 'lucide-react'
import type { OnboardingStep2Data } from '../types/onboarding.types'
import { getAccessToken, storeTokens } from '../../auth/utils/tokenStorage'
import { PostalCodeInput, CountrySelector, useCountries } from '../../validation'
import { getCountryConfig, getStateOptions } from '../../validation/utils/countryConfig'
import { SmartCompanySearch, parseBusinessAddress, enrichCompanyByABN, type CompanySearchResult } from '../../companies'

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
  const [useManualEntry, setUseManualEntry] = useState(false)  // Toggle between ABR search and manual entry
  const [abrData, setAbrData] = useState<CompanySearchResult | null>(null)  // Store ABR data for submission
  const [searchedACN, setSearchedACN] = useState<string | null>(null)  // Store ACN if searched by ACN
  const [isEnriching, setIsEnriching] = useState(false)  // Loading state for ABN enrichment
  
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

  // Handle company selection from ABR search (Story 1.19)
  const handleCompanySelected = useCallback(async (company: CompanySearchResult, searchContext?: {searchType: string, query: string}) => {
    // If searched by Name, enrich with full ABN details (get entity type, GST, etc.)
    let enrichedCompany = company
    if (searchContext?.searchType === 'Name' && company.abn) {
      setIsEnriching(true)
      
      try {
        const fullDetails = await enrichCompanyByABN(company.abn)
        if (fullDetails) {
          enrichedCompany = fullDetails
        }
      } finally {
        setIsEnriching(false)
      }
    }
    
    // Store enriched ABR data for later submission
    setAbrData(enrichedCompany)
    
    // If searched by ACN, store the ACN value
    if (searchContext?.searchType === 'ACN') {
      const cleanACN = searchContext.query.replace(/\s/g, '')
      setSearchedACN(cleanACN)
    }
    
    // Pre-fill company details (use enriched data if available)
    setValue('companyName', enrichedCompany.companyName, { shouldValidate: true })
    if (enrichedCompany.abn) {
      setValue('abn', enrichedCompany.abn, { shouldValidate: true })
    }
    setValue('gstRegistered', enrichedCompany.gstRegistered || false, { shouldValidate: true })

    // Parse and pre-fill billing address (use enriched data if available)
    if (enrichedCompany.businessAddress) {
      const addressParts = parseBusinessAddress(enrichedCompany.businessAddress)
      setValue('billingAddress', addressParts.street, { shouldValidate: true })
      setValue('billingSuburb', addressParts.suburb, { shouldValidate: true })
      setValue('billingState', addressParts.state, { shouldValidate: true })
      setValue('billingPostcode', addressParts.postcode, { shouldValidate: true })
    }

    // Switch to manual entry mode so user can edit
    setUseManualEntry(true)
  }, [setValue])

  // Handle manual entry toggle
  const handleManualEntry = useCallback(() => {
    setUseManualEntry(true)
  }, [])

  // Show ABR search when:
  // - Country is Australia (hasCompanySearch = true, code = 'AU')
  // - User hasn't selected manual entry mode
  const showABRSearch = countryConfig.hasCompanySearch && countryConfig.code === 'AU' && !useManualEntry

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
          acn: abrData?.acn || searchedACN || null,  // Story 1.19: ACN from ABR or search query
          phone: null,
          email: null,
          website: null,
          country_id: companyCountry,  // Story 1.20: User-selected country
          industry_id: null,
          // Story 1.19: Include ABR data if available
          legal_entity_name: abrData?.companyName || null,
          abn_status: abrData?.status || null,
          entity_type: abrData?.entityType || null,
          gst_registered: abrData?.gstRegistered || data.gstRegistered || null
        })
      })

      if (!response.ok) {
        const error = await response.json()
        // Extract the actual error message from the detail
        const errorMessage = typeof error.detail === 'string' 
          ? error.detail 
          : error.detail?.message || error.message || 'Failed to create company'
        throw new Error(errorMessage)
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

        {/* ABR Smart Search - Story 1.19 (Australia only) */}
        {showABRSearch && (
          <div className="bg-teal-50 border border-teal-200 rounded-lg p-5">
            <div className="mb-4">
              <h4 className="text-base font-semibold text-teal-900 mb-1">
                🔍 Search Australian Business Register
              </h4>
              <p className="text-sm text-teal-700">
                Find your company by ABN, ACN, or company name. We'll automatically fill in your details.
              </p>
            </div>
            
            {isEnriching && (
              <div className="mb-4 bg-white border border-teal-300 rounded-lg p-3 flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-teal-600" />
                <span className="text-sm text-teal-800">Loading complete company details from ABR...</span>
              </div>
            )}
            
            <SmartCompanySearch
              onCompanySelected={handleCompanySelected}
              onManualEntry={handleManualEntry}
              autoSelect={true}
            />
          </div>
        )}

        {/* Manual Entry Toggle (when ABR search is showing) */}
        {showABRSearch && (
          <div className="text-center -mt-2">
            <button
              type="button"
              onClick={() => setUseManualEntry(true)}
              className="text-sm text-teal-700 hover:text-teal-800 font-medium underline"
            >
              Skip search and enter details manually
            </button>
          </div>
        )}

        {/* Back to Search Link (when in manual entry mode for AU) */}
        {!showABRSearch && countryConfig.hasCompanySearch && countryConfig.code === 'AU' && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 flex items-center justify-between">
            <p className="text-sm text-gray-700">Entering details manually</p>
            <button
              type="button"
              onClick={() => setUseManualEntry(false)}
              className="text-sm text-teal-700 hover:text-teal-800 font-medium flex items-center gap-1"
            >
              <Building2 className="w-4 h-4" />
              Search ABR instead
            </button>
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



