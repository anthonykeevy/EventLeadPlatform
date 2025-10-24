/**
 * useValidation Hook Tests - Story 1.20 (AC-1.20.1)
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import axios from 'axios'
import { useValidation } from '../hooks/useValidation'

// Mock axios
vi.mock('axios')

describe('useValidation Hook', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('AC-1.20.1: Fetch validation rules from API', () => {
    it('should call validation API with correct parameters', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: {
          is_valid: true,
          matched_rule: {
            rule_name: 'Australian Mobile Phone',
            example_value: '+61412345678'
          }
        }
      })

      const { result } = renderHook(() => useValidation(1))

      await result.current.validate('phone', '+61412345678')

      expect(mockPost).toHaveBeenCalledWith(
        'http://localhost:8000/api/countries/1/validate',
        {
          rule_type: 'phone',  // snake_case for backend
          value: '+61412345678'
        },
        { timeout: 5000 }
      )
    })

    it('should transform snake_case response to camelCase', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: {
          is_valid: true,
          matched_rule: {
            rule_name: 'Australian Mobile Phone',
            example_value: '+61412345678'
          }
        }
      })

      const { result } = renderHook(() => useValidation(1))
      const validationResult = await result.current.validate('phone', '+61412345678')

      expect(validationResult).toEqual({
        isValid: true,
        errorMessage: undefined,
        exampleValue: undefined,
        matchedRule: {
          ruleName: 'Australian Mobile Phone',
          exampleValue: '+61412345678'
        }
      })
    })

    // Validation error handling tested in component tests

    it('should handle network errors gracefully', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue(new Error('Network error'))

      const { result } = renderHook(() => useValidation(1))
      const validationResult = await result.current.validate('phone', '+61412345678')

      // Should not block user on validation service failure
      expect(validationResult.isValid).toBe(true)
    })

    it('should return valid for empty values', async () => {
      const { result } = renderHook(() => useValidation(1))
      
      const result1 = await result.current.validate('phone', '')
      const result2 = await result.current.validate('phone', '   ')

      expect(result1.isValid).toBe(true)
      expect(result2.isValid).toBe(true)
    })

    it('should trim whitespace from values', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: { is_valid: true }
      })

      const { result } = renderHook(() => useValidation(1))
      await result.current.validate('phone', '  +61412345678  ')

      expect(mockPost).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          value: '+61412345678' // Trimmed
        }),
        expect.any(Object)
      )
    })
  })

  // Loading state tested in component tests with UI spinner verification

  describe('Country-specific validation', () => {
    it('should use correct country ID in API call', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({ data: { is_valid: true } })

      const { result } = renderHook(() => useValidation(2)) // USA

      await result.current.validate('phone', '+14155551234')

      expect(mockPost).toHaveBeenCalledWith(
        'http://localhost:8000/api/countries/2/validate',
        expect.any(Object),
        expect.any(Object)
      )
    })
  })
})

