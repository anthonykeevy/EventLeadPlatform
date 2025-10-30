/**
 * User Profile API Client for Epic 2 Story 2.1
 * Handles user profile API calls
 */

import axios, { AxiosInstance, AxiosError } from 'axios'
import {
  EnhancedUserProfile,
  ProfileUpdateRequest,
  ProfileUpdateResponse,
  IndustryAssociation,
  IndustryAssociationRequest,
  ReferenceOption
} from '../types/profile.types'
import { getAccessToken } from '../../auth/utils/tokenStorage'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance for user requests
const usersClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add request interceptor to attach access token
usersClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Format error for display
function formatError(error: unknown): Error {
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

/**
 * Get enhanced user profile with Epic 2 fields
 */
export async function getEnhancedProfile(): Promise<EnhancedUserProfile> {
  try {
    const response = await usersClient.get<EnhancedUserProfile>('/api/users/me/profile/enhanced')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Update user profile enhancements
 */
export async function updateProfile(request: ProfileUpdateRequest): Promise<ProfileUpdateResponse> {
  try {
    const response = await usersClient.put<ProfileUpdateResponse>('/api/users/me/profile/enhancements', request)
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get user's industry associations
 */
export async function getUserIndustries(): Promise<IndustryAssociation[]> {
  try {
    const response = await usersClient.get<IndustryAssociation[]>('/api/users/me/industries')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Add industry association
 */
export async function addIndustry(request: IndustryAssociationRequest): Promise<IndustryAssociation> {
  try {
    const response = await usersClient.post<IndustryAssociation>('/api/users/me/industries', request)
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Update industry association
 */
export async function updateIndustry(
  userIndustryId: number,
  request: IndustryAssociationRequest
): Promise<IndustryAssociation> {
  try {
    const response = await usersClient.put<IndustryAssociation>(
      `/api/users/me/industries/${userIndustryId}`,
      request
    )
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Remove industry association
 */
export async function removeIndustry(userIndustryId: number): Promise<void> {
  try {
    await usersClient.delete(`/api/users/me/industries/${userIndustryId}`)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get theme preferences (public endpoint)
 */
export async function getThemes(): Promise<ReferenceOption[]> {
  try {
    const response = await usersClient.get<ReferenceOption[]>('/api/users/reference/themes')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get layout densities (public endpoint)
 */
export async function getLayoutDensities(): Promise<ReferenceOption[]> {
  try {
    const response = await usersClient.get<ReferenceOption[]>('/api/users/reference/layout-densities')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get font sizes (public endpoint)
 */
export async function getFontSizes(): Promise<ReferenceOption[]> {
  try {
    const response = await usersClient.get<ReferenceOption[]>('/api/users/reference/font-sizes')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

