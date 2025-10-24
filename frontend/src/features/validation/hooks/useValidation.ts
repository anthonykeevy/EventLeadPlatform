/**
 * Validation Hook - Story 1.20 (AC-1.20.1)
 * Provides country-specific field validation using Story 1.12 backend API
 */

import { useState, useCallback } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export interface ValidationResult {
  isValid: boolean
  errorMessage?: string
  exampleValue?: string
  formattedValue?: string  // International format for storage
  displayValue?: string  // Local format for display (Story 1.20)
  displayFormat?: string  // Pattern like '04XX XXX XXX'
  spacingPattern?: string  // Spacing pattern
  matchedRule?: {
    ruleName: string
    exampleValue: string
  }
}

export interface UseValidationReturn {
  validate: (ruleType: string, value: string) => Promise<ValidationResult>
  isValidating: boolean
}

/**
 * Hook for country-specific field validation
 * AC-1.20.1: Fetch validation rules from the API
 * 
 * @param countryId - Country ID (default: 1 for Australia)
 * @returns Object with validate function and loading state
 */
export function useValidation(countryId: number = 1): UseValidationReturn {
  const [isValidating, setIsValidating] = useState(false)

  const validate = useCallback(async (ruleType: string, value: string): Promise<ValidationResult> => {
    if (!value || value.trim() === '') {
      return { isValid: true } // Empty values handled by required validation
    }

    setIsValidating(true)

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/countries/${countryId}/validate`,
        {
          rule_type: ruleType,  // Backend expects snake_case
          value: value.trim()
        },
        { timeout: 5000 }
      )

      // Transform response from snake_case to camelCase
      const result = {
        isValid: response.data.is_valid,
        errorMessage: response.data.error_message,
        exampleValue: response.data.example_value,
        formattedValue: response.data.formatted_value,  // International format
        displayValue: response.data.display_value,  // Local format (Story 1.20)
        displayFormat: response.data.display_format,
        spacingPattern: response.data.spacing_pattern,
        matchedRule: response.data.matched_rule ? {
          ruleName: response.data.matched_rule.rule_name,
          exampleValue: response.data.matched_rule.example_value
        } : undefined
      }
      
      setIsValidating(false)
      return result
    } catch (error) {
      setIsValidating(false)
      
      if (axios.isAxiosError(error) && error.response?.data) {
        // Backend returned validation error
        return {
          isValid: false,
          errorMessage: error.response.data.error_message || 'Invalid format',
          exampleValue: error.response.data.example_value
        }
      }

      // Network or unexpected error - fail gracefully
      console.error('Validation error:', error)
      return {
        isValid: true, // Don't block user on validation service failure
        errorMessage: undefined
      }
    }
  }, [countryId])

  return { validate, isValidating }
}

