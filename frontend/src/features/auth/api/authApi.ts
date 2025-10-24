/**
 * Auth API Client - Story 1.9 (AC-1.9.10)
 * Handles authentication API calls with automatic token refresh
 */

import axios, { AxiosInstance, AxiosError } from 'axios'
import { LoginCredentials, SignupData, TokenResponse, User } from '../types/auth.types'
import { getAccessToken, getRefreshToken, storeTokens, clearTokens } from '../utils/tokenStorage'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance for auth requests
const authClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add request interceptor to attach access token
authClient.interceptors.request.use(
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
 * AC-1.9.1: Form submission calls POST /api/auth/signup endpoint
 * Request: {email, password, first_name, last_name}
 * Response: {success: true, message: "...", data: {user_id, email}}
 */
export async function signupUser(data: SignupData): Promise<{ user_id: number; email: string; message: string }> {
  try {
    const response = await authClient.post('/api/auth/signup', data)
    return response.data
  } catch (error) {
    throw formatAuthError(error)
  }
}

/**
 * AC-1.9.2: Form submission calls POST /api/auth/login endpoint
 * Request: {email, password}
 * Response: {access_token, refresh_token, user: {...}}
 */
export async function loginUser(credentials: LoginCredentials): Promise<TokenResponse> {
  try {
    const response = await authClient.post<TokenResponse>('/api/auth/login', credentials)
    return response.data
  } catch (error) {
    throw formatAuthError(error)
  }
}

/**
 * AC-1.9.3: POST /api/auth/refresh with {refresh_token}
 * Response: {access_token, refresh_token}
 * Auto-refresh logic: Refresh token 5 minutes before expiry
 */
export async function refreshAccessToken(): Promise<TokenResponse> {
  const refreshToken = getRefreshToken()
  
  if (!refreshToken) {
    throw new Error('No refresh token available')
  }
  
  try {
    const response = await authClient.post<TokenResponse>('/api/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  } catch (error) {
    // If refresh fails, clear tokens and force re-login
    clearTokens()
    throw formatAuthError(error)
  }
}

/**
 * Get current user profile
 * Requires valid access token
 */
export async function getCurrentUser(): Promise<User> {
  try {
    const response = await authClient.get<User>('/api/auth/me')
    return response.data
  } catch (error) {
    throw formatAuthError(error)
  }
}

/**
 * Logout (backend may have logout endpoint in future)
 */
export async function logoutUser(): Promise<void> {
  try {
    // Optional: Call backend logout endpoint if exists
    // await authClient.post('/api/auth/logout')
    clearTokens()
  } catch (error) {
    // Still clear tokens even if backend call fails
    clearTokens()
    throw formatAuthError(error)
  }
}

/**
 * Format API errors into user-friendly messages
 * AC-1.9.5: Display API errors in user-friendly language
 */
function formatAuthError(error: unknown): Error {
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
      // Password validation errors: Let backend's specific message through
      if (detail.includes('Password does not meet security requirements')) {
        return new Error(detail) // Use backend's detailed message
      }
    }
    
    // Handle by status code
    switch (status) {
      case 401:
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

