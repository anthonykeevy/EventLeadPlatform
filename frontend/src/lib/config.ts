/**
 * Configuration API Service - Story 1.13
 * Handles fetching application configuration from the backend
 */
import axios, { AxiosError } from 'axios'
import { useQuery, UseQueryResult } from '@tanstack/react-query'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// API Response Types
export interface AppConfig {
  password_min_length: number
  password_require_uppercase: boolean
  password_require_number: boolean
  jwt_access_expiry_minutes: number
  email_verification_expiry_hours: number
  invitation_expiry_days: number
  company_name_min_length: number
  company_name_max_length: number
}

export interface ApiError {
  detail: string
}

// Create axios instance with default config
const configApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

/**
 * Fetch application configuration from backend
 * AC-1.13.7: Public configuration endpoint for frontend consumption
 */
export async function fetchAppConfig(): Promise<AppConfig> {
  try {
    const response = await configApi.get<AppConfig>('/api/config')
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<ApiError>
      throw {
        message: axiosError.response?.data?.detail || 'Failed to fetch configuration',
        status: axiosError.response?.status,
        response: axiosError.response,
      }
    }
    throw error
  }
}

/**
 * React Query hook for fetching application configuration
 * AC-1.13.9: Frontend configuration hook with React Query caching
 * 
 * Features:
 * - 5-minute cache (staleTime)
 * - Automatic background refetch
 * - Error handling
 * - Loading states
 * 
 * Usage:
 * ```tsx
 * const { config, isLoading, error } = useAppConfig();
 * 
 * if (isLoading) return <LoadingSpinner />;
 * if (error) return <ErrorMessage error={error} />;
 * 
 * return <input minLength={config?.password_min_length || 8} />;
 * ```
 */
export function useAppConfig(): UseQueryResult<AppConfig, Error> & { config: AppConfig | undefined } {
  const query = useQuery<AppConfig, Error>({
    queryKey: ['app-config'],
    queryFn: fetchAppConfig,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
    gcTime: 10 * 60 * 1000, // Keep in cache for 10 minutes (formerly cacheTime)
    retry: 3, // Retry failed requests up to 3 times
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
  })

  return {
    ...query,
    config: query.data,
  }
}

/**
 * Default configuration fallback values
 * Used when API is unavailable or during initial load
 */
export const DEFAULT_CONFIG: AppConfig = {
  password_min_length: 8,
  password_require_uppercase: false,
  password_require_number: true,
  jwt_access_expiry_minutes: 15,
  email_verification_expiry_hours: 24,
  invitation_expiry_days: 7,
  company_name_min_length: 2,
  company_name_max_length: 200,
}

