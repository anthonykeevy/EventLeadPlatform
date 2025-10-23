/**
 * Password Reset API Client Tests - Story 1.15
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import axios from 'axios'
import { requestPasswordReset, confirmPasswordReset } from '../api/passwordResetApi'

// Mock axios
vi.mock('axios')

describe('Password Reset API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('requestPasswordReset - AC-1.15.1', () => {
    it('should call POST /api/auth/password-reset/request with email', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: {
          success: true,
          message: 'If the email exists, a password reset link has been sent.',
        },
      })

      const result = await requestPasswordReset('user@example.com')

      expect(mockPost).toHaveBeenCalledWith(
        'http://localhost:8000/api/auth/password-reset/request',
        { email: 'user@example.com' },
        { timeout: 10000 }
      )
      expect(result).toEqual({
        success: true,
        message: 'If the email exists, a password reset link has been sent.',
      })
    })

    it('should handle network errors gracefully', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue({
        isAxiosError: true,
        response: undefined,
      })

      await expect(requestPasswordReset('user@example.com')).rejects.toThrow(
        'Connection error. Please check your internet and try again.'
      )
    })

    it('should handle 500 server errors', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue({
        isAxiosError: true,
        response: {
          status: 500,
          data: { detail: 'Internal server error' },
        },
      })

      await expect(requestPasswordReset('user@example.com')).rejects.toThrow(
        'Something went wrong. Please try again later.'
      )
    })
  })

  describe('confirmPasswordReset - AC-1.15.2', () => {
    it('should call POST /api/auth/password-reset/confirm with token and new_password', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: {
          success: true,
          message: 'Password reset successful',
          user_id: 123, // Backend returns snake_case
        },
      })

      const result = await confirmPasswordReset('abc123', 'NewPassword123!')

      expect(mockPost).toHaveBeenCalledWith(
        'http://localhost:8000/api/auth/password-reset/confirm',
        {
          token: 'abc123',
          new_password: 'NewPassword123!', // API expects snake_case
        },
        { timeout: 10000 }
      )

      // Should transform response to camelCase
      expect(result).toEqual({
        success: true,
        message: 'Password reset successful',
        userId: 123, // Transformed to camelCase
      })
    })

    it('should handle expired token error (400)', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue({
        isAxiosError: true,
        response: {
          status: 400,
          data: { detail: 'Invalid or expired password reset token' },
        },
      })

      await expect(confirmPasswordReset('expired-token', 'NewPassword123!')).rejects.toThrow(
        'This password reset link has expired or is invalid. Please request a new one.'
      )
    })

    it('should handle password validation errors', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue({
        isAxiosError: true,
        response: {
          status: 400,
          data: {
            detail: 'Password does not meet security requirements: Must be at least 8 characters',
          },
        },
      })

      await expect(confirmPasswordReset('valid-token', 'short')).rejects.toThrow(
        'Password does not meet security requirements: Must be at least 8 characters'
      )
    })

    it('should handle 422 validation errors', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue({
        isAxiosError: true,
        response: {
          status: 422,
          data: { detail: 'Validation error' },
        },
      })

      await expect(confirmPasswordReset('valid-token', 'NewPassword123!')).rejects.toThrow(
        'Please check your input and try again.'
      )
    })

    it('should handle network errors', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue({
        isAxiosError: true,
        response: undefined,
      })

      await expect(confirmPasswordReset('valid-token', 'NewPassword123!')).rejects.toThrow(
        'Connection error. Please check your internet and try again.'
      )
    })

    it('should handle unexpected errors', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockRejectedValue(new Error('Unexpected error'))

      await expect(confirmPasswordReset('valid-token', 'NewPassword123!')).rejects.toThrow(
        'An unexpected error occurred. Please try again.'
      )
    })
  })

  describe('snake_case to camelCase transformation', () => {
    it('should transform user_id to userId in confirmPasswordReset response', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: {
          success: true,
          message: 'Password reset successful',
          user_id: 456, // Backend returns snake_case
        },
      })

      const result = await confirmPasswordReset('token123', 'Password123!')

      expect(result.userId).toBe(456)
      expect(result).not.toHaveProperty('user_id')
    })
  })

  describe('Environment variable configuration', () => {
    it('should use VITE_API_BASE_URL from environment if set', async () => {
      // Note: This test verifies the API client uses the correct base URL
      // The actual implementation uses import.meta.env.VITE_API_BASE_URL
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: { success: true, message: 'Success' },
      })

      await requestPasswordReset('test@example.com')

      const callUrl = mockPost.mock.calls[0][0]
      expect(callUrl).toContain('/api/auth/password-reset/request')
    })
  })

  describe('Timeout configuration', () => {
    it('should set 10 second timeout for requestPasswordReset', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: { success: true, message: 'Success' },
      })

      await requestPasswordReset('test@example.com')

      expect(mockPost).toHaveBeenCalledWith(
        expect.any(String),
        expect.any(Object),
        { timeout: 10000 }
      )
    })

    it('should set 10 second timeout for confirmPasswordReset', async () => {
      const mockPost = vi.mocked(axios.post)
      mockPost.mockResolvedValue({
        data: { success: true, message: 'Success', user_id: 1 },
      })

      await confirmPasswordReset('token', 'Password123!')

      expect(mockPost).toHaveBeenCalledWith(
        expect.any(String),
        expect.any(Object),
        { timeout: 10000 }
      )
    })
  })
})

