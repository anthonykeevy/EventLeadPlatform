/**
 * Postal Code Input Component with Country-Specific Validation - Story 1.20 (AC-1.20.3, AC-1.20.4, AC-1.20.5)
 * 
 * Features:
 * - Real-time validation using Story 1.12 backend API
 * - Country-specific postal code formats (Australia: 4 digits)
 * - Clear error messages with example values
 * - Mobile responsive
 * - Accessible (ARIA labels)
 */

import React, { useState, useEffect } from 'react'
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import { useValidation } from '../hooks/useValidation'

interface PostalCodeInputProps {
  id?: string
  name?: string
  value: string
  onChange: (value: string) => void
  onBlur?: () => void
  countryId?: number
  label?: string  // Custom label (e.g., "ZIP Code", "Postcode")
  required?: boolean
  disabled?: boolean
  className?: string
}

export function PostalCodeInput({
  id = 'postalCode',
  name = 'postalCode',
  value,
  onChange,
  onBlur,
  countryId = 1, // Default: Australia
  label = 'Postcode',  // Default label
  required = false,
  disabled = false,
  className = ''
}: PostalCodeInputProps) {
  const { validate, isValidating } = useValidation(countryId)
  const [validationError, setValidationError] = useState<string | null>(null)
  const [exampleValue, setExampleValue] = useState<string | null>(null)
  const [isValid, setIsValid] = useState<boolean | null>(null)
  const [touched, setTouched] = useState(false)
  const [maxLength, setMaxLength] = useState<number | undefined>(undefined)  // Dynamic from backend

  // Fetch validation constraints when country changes
  useEffect(() => {
    const fetchConstraints = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/countries/${countryId}/validation-rules/postal_code`
        )
        if (response.ok) {
          const metadata = await response.json()
          setMaxLength(metadata.max_length || undefined)
        }
      } catch (error) {
        console.error('Failed to fetch validation constraints:', error)
      }
    }
    
    fetchConstraints()
  }, [countryId])

  const handleBlur = async () => {
    setTouched(true)
    onBlur?.()

    if (!value || value.trim() === '') {
      setValidationError(null)
      setIsValid(null)
      return
    }

    // AC-1.20.3: Validate using backend API
    const result = await validate('postal_code', value)

    setIsValid(result.isValid)
    setValidationError(result.isValid ? null : result.errorMessage || 'Invalid postal code')
    setExampleValue(result.exampleValue || null)
  }

  // Reset validation when value changes
  useEffect(() => {
    if (touched && value) {
      setIsValid(null)
      setValidationError(null)
    }
  }, [value, touched])

  return (
    <div className={className}>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      
      <div className="relative">
        <input
          id={id}
          name={name}
          type="text"
          inputMode="numeric"
          maxLength={maxLength}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onBlur={handleBlur}
          disabled={disabled}
          placeholder="2000"
          aria-label="Postcode"
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
          ✓ Valid postcode
        </p>
      )}
    </div>
  )
}

