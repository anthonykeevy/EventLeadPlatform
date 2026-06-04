import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { getAccessToken, storeTokens } from '../features/auth/utils/tokenStorage'
import { refreshAccessToken } from '../features/auth/api/coreAuth'
import { getApiBaseUrl } from './apiBaseUrl'

// Create shared axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Add request interceptor to attach access token and fix FormData Content-Type
if (apiClient && apiClient.interceptors && apiClient.interceptors.request) {
  apiClient.interceptors.request.use(
    (config) => {
      const token = getAccessToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      // For FormData, do NOT set Content-Type — browser must set multipart/form-data with boundary
      if (config.data instanceof FormData) {
        delete config.headers['Content-Type']
      }
      return config
    },
    (error) => Promise.reject(error)
  )
}

// Add response interceptor to handle token refresh and session expiry
if (apiClient && apiClient.interceptors && apiClient.interceptors.response) {
  apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

      // Suppress 404 errors for specific endpoints if needed (copied from eventsApi)
      if (error.response?.status === 404 && originalRequest.url?.includes('/timezones/') && originalRequest.url?.includes('/country')) {
        return Promise.reject(error)
      }

      // Check if offline
      if (!navigator.onLine) {
        return Promise.reject(error)
      }

      // Handle 401 Unauthorized
      if (error.response?.status === 401 && !originalRequest._retry) {
        // Avoid infinite loops for auth endpoints
        if (originalRequest.url?.includes('/auth/login') || 
            originalRequest.url?.includes('/auth/refresh') || 
            originalRequest.url?.includes('/auth/signup')) {
          return Promise.reject(error)
        }

        if (originalRequest.url?.includes('/api/public/')) {
          return Promise.reject(error)
        }

        originalRequest._retry = true

        try {
          // Attempt to refresh token
          const tokenResponse = await refreshAccessToken()
          
          // Store new tokens
          const expiresIn = tokenResponse.expires_in || 3600
          storeTokens(tokenResponse.access_token, tokenResponse.refresh_token, expiresIn)
          
          // Update header and retry original request
          originalRequest.headers.Authorization = `Bearer ${tokenResponse.access_token}`
          return apiClient(originalRequest)
        } catch (refreshError) {
          const refreshStatus = (refreshError as AxiosError | undefined)?.response?.status
          if (refreshStatus === 401) {
            window.dispatchEvent(new CustomEvent('eventlead:session-expired'))
          }
          return Promise.reject(refreshError)
        }
      }

      return Promise.reject(error)
    }
  )
}

/**
 * Format error for display (shared utility)
 */
export function formatError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError
    if (axiosError.response) {
      return new Error(
        (axiosError.response.data as { detail?: string })?.detail || 
        axiosError.response.statusText || 
        'An error occurred'
      )
    }
  }
  return new Error(error instanceof Error ? error.message : 'An unknown error occurred')
}

