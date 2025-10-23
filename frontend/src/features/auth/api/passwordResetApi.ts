/**
 * Password Reset API Client - Story 1.15
 * Handles password reset API calls with snake_case/camelCase transformations
 */

import axios, { AxiosError } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export interface PasswordResetRequestResponse {
  success: boolean
  message: string
}

export interface PasswordResetConfirmResponse {
  success: boolean
  message: string
  userId: number
}

export interface TokenValidationResponse {
  valid: boolean
  message: string
}

/**
 * Validate password reset token
 * GET /api/auth/password-reset/validate/{token}
 * Returns 200 if valid, 400 if invalid/expired/used
 */
export async function validatePasswordResetToken(token: string): Promise<boolean> {
  try {
    await axios.get(
      `${API_BASE_URL}/api/auth/password-reset/validate/${token}`,
      { timeout: 10000 }
    )
    return true
  } catch (error) {
    return false
  }
}

/**
 * AC-1.15.1: Request Password Reset
 * POST /api/auth/password-reset/request
 * Always returns success (security: don't reveal if email exists)
 */
export async function requestPasswordReset(email: string): Promise<PasswordResetRequestResponse> {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/password-reset/request`,
      { email },
      { timeout: 10000 }
    )
    return response.data
  } catch (error) {
    throw formatPasswordResetError(error)
  }
}

/**
 * AC-1.15.2: Confirm Password Reset
 * POST /api/auth/password-reset/confirm
 * ⚠️ Backend expects snake_case (new_password)
 */
export async function confirmPasswordReset(
  token: string,
  newPassword: string
): Promise<PasswordResetConfirmResponse> {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/password-reset/confirm`,
      {
        token,
        new_password: newPassword, // ⚠️ Backend expects snake_case
      },
      { timeout: 10000 }
    )

    // Transform response to camelCase
    return {
      success: response.data.success,
      message: response.data.message,
      userId: response.data.user_id, // ⚠️ Transform snake_case to camelCase
    }
  } catch (error) {
    throw formatPasswordResetError(error)
  }
}

/**
 * Format API errors into user-friendly messages
 * AC-1.15.4: Display user-friendly error messages
 */
function formatPasswordResetError(error: unknown): Error {
  // Check if it's an axios error (either via axios.isAxiosError or duck typing)
  const isAxiosErr = axios.isAxiosError(error) || (error && typeof error === 'object' && 'isAxiosError' in error)
  
  if (isAxiosErr) {
    const axiosError = error as AxiosError<{ detail: string }>
    const status = axiosError.response?.status
    const detail = axiosError.response?.data?.detail

    // Map backend error codes to user-friendly messages
    if (detail) {
      if (detail.includes('Invalid or expired')) {
        return new Error('This password reset link has expired or is invalid. Please request a new one.')
      }
      if (detail.includes('Password does not meet security requirements')) {
        return new Error(detail) // Use backend's detailed password validation message
      }
    }

    // Handle by status code
    switch (status) {
      case 400:
        return new Error('This password reset link is invalid or has expired. Please request a new one.')
      case 422:
        return new Error('Please check your input and try again.')
      case 500:
        return new Error('Something went wrong. Please try again later.')
      default:
        if (!axiosError.response) {
          return new Error('Connection error. Please check your internet and try again.')
        }
        return new Error(detail || 'An error occurred. Please try again.')
    }
  }

  return new Error('An unexpected error occurred. Please try again.')
}

