/**
 * Phone Input Component with Country-Specific Validation - Story 1.20 (AC-1.20.2, AC-1.20.4, AC-1.20.5)
 * 
 * Features:
 * - Real-time validation using Story 1.12 backend API
 * - Country-specific phone formats (Australia: +61)
 * - Clear error messages with example values
 * - Mobile responsive
 * - Accessible (ARIA labels)
 */

import React, { useState, useEffect } from 'react'
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import { useValidation } from '../hooks/useValidation'

interface PhoneInputProps {
  id?: string
  name?: string
  value: string
  onChange: (value: string) => void
  onBlur?: () => void
  countryId?: number
  onCountryDetected?: (countryId: number) => void  // Auto-detect country from prefix
  required?: boolean
  disabled?: boolean
  className?: string
}

export function PhoneInput({
  id = 'phone',
  name = 'phone',
  value,
  onChange,
  onBlur,
  countryId = 1, // Default: Australia
  onCountryDetected,
  required = false,
  disabled = false,
  className = ''
}: PhoneInputProps) {
  const { validate, isValidating } = useValidation(countryId)
  const [validationError, setValidationError] = useState<string | null>(null)
  const [exampleValue, setExampleValue] = useState<string | null>(null)
  const [isValid, setIsValid] = useState<boolean | null>(null)
  const [touched, setTouched] = useState(false)
  const [lastValidatedValue, setLastValidatedValue] = useState<string>('')  // Track what we validated

  // Auto-detect country when user types international prefix
  const handleChange = (newValue: string) => {
    onChange(newValue)
    
    // Detect country from international prefix
    if (newValue.startsWith('+') && onCountryDetected) {
      if (newValue.startsWith('+61')) onCountryDetected(1)  // Australia
      else if (newValue.startsWith('+64')) onCountryDetected(14)  // New Zealand
      else if (newValue.startsWith('+1')) onCountryDetected(15)  // USA (or Canada=17 - user can switch)
      else if (newValue.startsWith('+44')) onCountryDetected(16)  // UK
    }
  }

  const handleBlur = async () => {
    setTouched(true)
    onBlur?.()

    if (!value || value.trim() === '') {
      setValidationError(null)
      setIsValid(null)
      return
    }

    // AC-1.20.2: Validate using backend API
    const result = await validate('phone', value)

    // Story 1.20: Update to local format FIRST (before setting validation state)
    let finalValue = value
    if (result.isValid && result.displayValue && result.displayValue !== value) {
      finalValue = result.displayValue
      onChange(result.displayValue)  // Update to local format (e.g., +61... → 04...)
    }
    
    // Set validation state AFTER value update
    setIsValid(result.isValid)
    setValidationError(result.isValid ? null : result.errorMessage || 'Invalid phone number')
    setExampleValue(result.exampleValue || null)
    setLastValidatedValue(finalValue)  // Remember what we just validated
  }

  // Reset validation only when value ACTUALLY changes (not when we update to displayValue)
  useEffect(() => {
    if (touched && value && value !== lastValidatedValue) {
      // User typed something new - clear old validation
      setIsValid(null)
      setValidationError(null)
      setExampleValue(null)
    }
  }, [value, touched, lastValidatedValue])
  
  // Reset validation when country changes
  useEffect(() => {
    if (touched) {
      setIsValid(null)
      setValidationError(null)
      setExampleValue(null)
      setLastValidatedValue('')
    }
  }, [countryId, touched])

  return (
    <div className={className}>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        Phone Number {required && <span className="text-red-500">*</span>}
      </label>
      
      <div className="relative">
        <input
          id={id}
          name={name}
          type="tel"
          inputMode="tel"
          value={value}
          onChange={(e) => handleChange(e.target.value)}
          onBlur={handleBlur}
          disabled={disabled}
          placeholder="0412345678"
          aria-label="Phone Number"
          aria-required={required}
          aria-invalid={touched && !isValid}
          aria-describedby={validationError ? `${id}-error` : undefined}
          className={`w-full px-4 py-3 pr-12 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
            disabled ? 'bg-gray-100 cursor-not-allowed' :
            touched && isValid === true ? 'border-green-500' :
            touched && isValid === false ? 'border-red-500' :
            'border-gray-300'
          }`}
        />
        
        {/* Validation Status Icon - AC-1.20.5 */}
        <div className="absolute right-3 top-1/2 -translate-y-1/2">
          {isValidating && (
            <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
          )}
          {!isValidating && touched && isValid === true && (
            <CheckCircle className="w-5 h-5 text-green-600" />
          )}
          {!isValidating && touched && isValid === false && (
            <AlertCircle className="w-5 h-5 text-red-600" />
          )}
        </div>
      </div>

      {/* Error Message with Example - AC-1.20.4 */}
      {touched && validationError && (
        <div id={`${id}-error`} className="mt-2 text-sm text-red-600" role="alert">
          <p>{validationError}</p>
          {exampleValue && (
            <p className="mt-1 text-gray-600">
              Example: <span className="font-mono text-gray-900">{exampleValue}</span>
            </p>
          )}
        </div>
      )}

      {/* Success Message */}
      {touched && isValid === true && !validationError && (
        <p className="mt-2 text-sm text-green-600">
          ✓ Valid phone number
        </p>
      )}
    </div>
  )
}

