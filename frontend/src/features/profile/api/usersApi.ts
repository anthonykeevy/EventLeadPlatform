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
 * Backend response format (snake_case)
 */
interface BackendEnhancedUserProfile {
  user_id: number
  email: string
  first_name: string
  last_name: string
  phone: string | null
  bio: string | null
  role_title: string | null
  is_email_verified: boolean
  theme_preference: {
    id: number
    code: string
    name: string
    description: string
    css_class: string
    base_font_size?: string | null
  } | null
  layout_density: {
    id: number
    code: string
    name: string
    description: string
    css_class: string
    base_font_size?: string | null
  } | null
  font_size: {
    id: number
    code: string
    name: string
    description: string
    css_class: string
    base_font_size?: string | null
  } | null
  industries: Array<{
    user_industry_id: number
    industry_id: number
    industry_name: string
    industry_code: string
    is_primary: boolean
    sort_order: number
  }>
}

/**
 * Transform backend response (snake_case) to frontend format (camelCase)
 */
function transformEnhancedProfile(backendProfile: BackendEnhancedUserProfile): EnhancedUserProfile {
  return {
    userId: backendProfile.user_id,
    email: backendProfile.email,
    firstName: backendProfile.first_name,
    lastName: backendProfile.last_name,
    phone: backendProfile.phone,
    bio: backendProfile.bio,
    roleTitle: backendProfile.role_title,
    isEmailVerified: backendProfile.is_email_verified,
    themePreference: backendProfile.theme_preference ? {
      id: backendProfile.theme_preference.id,
      code: backendProfile.theme_preference.code,
      name: backendProfile.theme_preference.name,
      description: backendProfile.theme_preference.description,
      css_class: backendProfile.theme_preference.css_class,
      base_font_size: backendProfile.theme_preference.base_font_size || null
    } : null,
    layoutDensity: backendProfile.layout_density ? {
      id: backendProfile.layout_density.id,
      code: backendProfile.layout_density.code,
      name: backendProfile.layout_density.name,
      description: backendProfile.layout_density.description,
      css_class: backendProfile.layout_density.css_class,
      base_font_size: backendProfile.layout_density.base_font_size || null
    } : null,
    fontSize: backendProfile.font_size ? {
      id: backendProfile.font_size.id,
      code: backendProfile.font_size.code,
      name: backendProfile.font_size.name,
      description: backendProfile.font_size.description,
      css_class: backendProfile.font_size.css_class,
      base_font_size: backendProfile.font_size.base_font_size || null
    } : null,
    industries: backendProfile.industries.map(industry => ({
      userIndustryId: industry.user_industry_id,
      industryId: industry.industry_id,
      industryName: industry.industry_name,
      industryCode: industry.industry_code,
      isPrimary: industry.is_primary,
      sortOrder: industry.sort_order
    }))
  }
}

/**
 * Get enhanced user profile with Epic 2 fields
 */
export async function getEnhancedProfile(): Promise<EnhancedUserProfile> {
  try {
    const response = await usersClient.get<BackendEnhancedUserProfile>('/api/users/me/profile/enhanced')
    // Transform snake_case response to camelCase
    return transformEnhancedProfile(response.data)
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

