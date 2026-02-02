import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { getAccessToken, storeTokens, clearTokens } from '../features/auth/utils/tokenStorage'
import { refreshAccessToken } from '../features/auth/api/coreAuth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// Create shared axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Add request interceptor to attach access token
apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Add response interceptor to handle token refresh and session expiry
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
        // Refresh failed - keep session state but notify for retry
        window.dispatchEvent(new CustomEvent('eventlead:refresh-failed', {
          detail: {
            status: (refreshError as AxiosError | undefined)?.response?.status || 0
          }
        }))
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

/**
 * Format error for display (shared utility)
 */
export function formatError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError
    if (axiosError.response) {
      return new Error(
        (axiosError.response.data as any)?.detail || 
        axiosError.response.statusText || 
        'An error occurred'
      )
    }
  }
  return new Error(error instanceof Error ? error.message : 'An unknown error occurred')
}

