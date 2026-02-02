/**
 * Core Auth API - Base authentication functions
 * Separated to avoid circular dependencies with the global apiClient
 */

import axios, { AxiosInstance, AxiosError } from 'axios'
import { LoginCredentials, SignupData, TokenResponse } from '../types/auth.types'
import { getAccessToken, getRefreshToken, clearTokens } from '../utils/tokenStorage'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// Create axios instance for core auth requests (no auto-refresh interceptor)
const coreAuthClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add request interceptor to attach access token (needed for logout or other auth-required endpoints)
coreAuthClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/**
 * Format API errors into user-friendly messages
 */
export function formatAuthError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail: string }>
    const status = axiosError.response?.status
    const detail = axiosError.response?.data?.detail
    
    // Map backend error codes to user-friendly messages
    if (detail) {
      if (detail.includes('already registered') || detail.includes('already exists')) {
        return new Error('This email is already registered. Try logging in.')
      }
      if (detail.includes('Invalid credentials') || detail.includes('Incorrect')) {
        return new Error('Email or password is incorrect.')
      }
      if (detail.includes('not verified') || detail.includes('verify your email')) {
        return new Error('Please verify your email before logging in.')
      }
      if (detail.includes('Password does not meet security requirements')) {
        return new Error(detail)
      }
    }
    
    switch (status) {
      case 401:
        if (detail && (detail.includes('refresh token') || detail.includes('token') || detail.includes('Invalid or expired'))) {
          return new Error(detail || 'Token refresh failed. Please log in again.')
        }
        return new Error('Email or password is incorrect.')
      case 403:
        return new Error('Please verify your email before logging in.')
      case 409:
        return new Error('This email is already registered. Try logging in.')
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

export async function signupUser(data: SignupData): Promise<{ user_id: number; email: string; message: string }> {
  try {
    const response = await coreAuthClient.post('/api/auth/signup', data)
    return response.data
  } catch (error) {
    throw formatAuthError(error)
  }
}

export async function loginUser(credentials: LoginCredentials): Promise<TokenResponse> {
  try {
    const response = await coreAuthClient.post<TokenResponse>('/api/auth/login', credentials)
    return response.data
  } catch (error) {
    throw formatAuthError(error)
  }
}

export async function refreshAccessToken(): Promise<TokenResponse> {
  const attemptRefresh = async (token: string): Promise<TokenResponse> => {
    const response = await coreAuthClient.post<{
      success: boolean
      message: string
      data: {
        access_token: string
        token_type: string
        expires_in: number
      }
    }>('/api/auth/refresh', {
      refresh_token: token,
    })
    
    return {
      access_token: response.data.data.access_token,
      refresh_token: token,
      token_type: response.data.data.token_type,
      expires_in: response.data.data.expires_in,
    }
  }

  const initialRefreshToken = getRefreshToken()
  
  if (!initialRefreshToken) {
    throw new Error('No refresh token available')
  }
  
  try {
    return await attemptRefresh(initialRefreshToken)
  } catch (error) {
    const latestRefreshToken = getRefreshToken()
    const shouldRetry = axios.isAxiosError(error) && error.response?.status === 401
      && latestRefreshToken
      && latestRefreshToken !== initialRefreshToken

    if (shouldRetry) {
      try {
        return await attemptRefresh(latestRefreshToken)
      } catch (retryError) {
        throw formatAuthError(retryError)
      }
    }

    throw formatAuthError(error)
  }
}

export async function logoutUser(): Promise<void> {
  try {
    // await coreAuthClient.post('/api/auth/logout')
    clearTokens()
  } catch (error) {
    clearTokens()
    throw formatAuthError(error)
  }
}

