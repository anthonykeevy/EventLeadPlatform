/**
 * Country Selector Component - Story 1.20
 * 
 * Features:
 * - Dropdown showing country code/flag
 * - Auto-detects user's country from browser
 * - User can manually change if wrong
 * - Used with PhoneInput for international phone formatting
 */

import React, { useEffect } from 'react'
import { useCountries } from '../hooks/useCountries'
import type { Country } from '../hooks/useCountries'

export type { Country }

interface CountrySelectorProps {
  value: number  // CountryID
  onChange: (countryId: number) => void
  autoDetect?: boolean
  className?: string
}

export function CountrySelector({
  value,
  onChange,
  autoDetect = true,
  className = ''
}: CountrySelectorProps) {
  const { countries, isLoading, getCountryByCode } = useCountries()
  
  // Auto-detect country from browser timezone
  useEffect(() => {
    if (autoDetect && !value && countries.length > 0) {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
      
      // Map timezone to country code
      let detectedCode = 'AU'  // Default: Australia
      if (timezone.includes('Pacific/Auckland') || timezone.includes('New_Zealand')) {
        detectedCode = 'NZ'
      } else if (timezone.includes('America/') && !timezone.includes('America/Vancouver') && !timezone.includes('America/Toronto')) {
        detectedCode = 'US'
      } else if (timezone.includes('Europe/London')) {
        detectedCode = 'GB'
      } else if (timezone.includes('America/Toronto') || timezone.includes('America/Vancouver')) {
        detectedCode = 'CA'
      } else if (timezone.includes('Australia/')) {
        detectedCode = 'AU'
      }
      
      // Get actual CountryID from fetched data
      const detected = getCountryByCode(detectedCode)
      if (detected) {
        onChange(detected.id)
      }
    }
  }, [autoDetect, value, onChange, countries, getCountryByCode])
  
  if (isLoading) {
    return (
      <div className={className}>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Country <span className="text-red-500">*</span>
        </label>
        <div className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-500">
          Loading countries...
        </div>
      </div>
    )
  }
  
  return (
    <div className={className}>
      <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-1">
        Country <span className="text-red-500">*</span>
      </label>
      <select
        id="country"
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
      >
        {countries.map(country => (
          <option 
            key={country.id}
            value={country.id}
          >
            {country.phone_prefix} {country.name}
          </option>
        ))}
      </select>
      <p className="mt-1 text-xs text-gray-500">
        Auto-detected based on your location. Change if incorrect.
      </p>
    </div>
  )
}

