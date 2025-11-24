/**
 * User Profile API Client for Epic 2 Story 2.1
 * Handles user profile API calls
 */

import { apiClient, formatError } from '../../../lib/apiClient'
import {
  EnhancedUserProfile,
  ProfileUpdateRequest,
  ProfileUpdateResponse,
  IndustryAssociation,
  IndustryAssociationRequest,
  ReferenceOption
} from '../types/profile.types'

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
    const response = await apiClient.get<BackendEnhancedUserProfile>('/api/users/me/profile/enhanced')
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
    const response = await apiClient.put<ProfileUpdateResponse>('/api/users/me/profile/enhancements', request)
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Update user details (name, phone, timezone, role title)
 * Backend expects snake_case
 */
export interface UpdateUserDetailsRequest {
  first_name?: string
  last_name?: string
  phone?: string | null
  timezone_identifier: string
  role_title?: string | null
}

export interface UpdateUserDetailsResponse {
  success: boolean
  message: string
  user_id: number
}

export async function updateUserDetails(request: UpdateUserDetailsRequest): Promise<UpdateUserDetailsResponse> {
  try {
    console.log('[updateUserDetails] Sending request:', request)
    const response = await apiClient.post<UpdateUserDetailsResponse>('/api/users/me/details', request)
    console.log('[updateUserDetails] Response received:', response.data)
    return response.data
  } catch (error) {
    console.error('[updateUserDetails] Error:', error)
    throw formatError(error)
  }
}

/**
 * Get user's industry associations
 * Transform backend snake_case to frontend camelCase
 */
interface BackendIndustryAssociation {
  user_industry_id: number
  industry_id: number
  industry_name: string
  industry_code: string
  is_primary: boolean
  sort_order: number
}

export async function getUserIndustries(): Promise<IndustryAssociation[]> {
  try {
    const response = await apiClient.get<BackendIndustryAssociation[]>('/api/users/me/industries')
    // Transform snake_case to camelCase
    return response.data.map(industry => ({
      userIndustryId: industry.user_industry_id,
      industryId: industry.industry_id,
      industryName: industry.industry_name,
      industryCode: industry.industry_code,
      isPrimary: industry.is_primary,
      sortOrder: industry.sort_order
    }))
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Add industry association
 * Note: Backend expects snake_case, so we transform camelCase to snake_case
 */
export async function addIndustry(request: IndustryAssociationRequest): Promise<IndustryAssociation> {
  try {
    // Transform camelCase to snake_case for backend
    const backendRequest = {
      industry_id: request.industryId,
      is_primary: request.isPrimary,
      sort_order: request.sortOrder || null
    }
    console.log('[addIndustry] Sending request:', backendRequest)
    const response = await apiClient.post<IndustryAssociation>('/api/users/me/industries', backendRequest)
    console.log('[addIndustry] Response received:', response.data)
    return response.data
  } catch (error) {
    console.error('[addIndustry] Error:', error)
    throw formatError(error)
  }
}

/**
 * Update industry association
 * Note: Backend expects snake_case, so we transform camelCase to snake_case
 */
interface BackendIndustryAssociationResponse {
    user_industry_id: number;
    industry_id: number;
    industry_name: string;
    industry_code: string;
    is_primary: boolean;
    sort_order: number;
}

export async function updateIndustry(
  userIndustryId: number,
  request: IndustryAssociationRequest
): Promise<IndustryAssociation> {
  try {
    // Transform camelCase to snake_case for backend
    const backendRequest = {
      industry_id: request.industryId,
      is_primary: request.isPrimary,
      sort_order: request.sortOrder || null
    }
    console.log('[updateIndustry] Sending request:', { userIndustryId, backendRequest })
    const response = await apiClient.put<BackendIndustryAssociationResponse>(
      `/api/users/me/industries/${userIndustryId}`,
      backendRequest
    )
    console.log('[updateIndustry] Response received:', response.data)
    // Transform snake_case to camelCase
    return {
      userIndustryId: response.data.user_industry_id,
      industryId: response.data.industry_id,
      industryName: response.data.industry_name,
      industryCode: response.data.industry_code,
      isPrimary: response.data.is_primary,
      sortOrder: response.data.sort_order
    }
  } catch (error) {
    console.error('[updateIndustry] Error:', error)
    throw formatError(error)
  }
}

/**
 * Remove industry association
 */
export async function removeIndustry(userIndustryId: number): Promise<void> {
  try {
    await apiClient.delete(`/api/users/me/industries/${userIndustryId}`)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get theme preferences (public endpoint)
 */
export async function getThemes(): Promise<ReferenceOption[]> {
  try {
    const response = await apiClient.get<ReferenceOption[]>('/api/users/reference/themes')
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
    const response = await apiClient.get<ReferenceOption[]>('/api/users/reference/layout-densities')
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
    const response = await apiClient.get<ReferenceOption[]>('/api/users/reference/font-sizes')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Industry option from reference endpoint
 */
export interface IndustryOption {
  id: number
  code: string
  name: string
  description: string
}

/**
 * Get all industries (public endpoint)
 */
export async function getIndustries(): Promise<IndustryOption[]> {
  try {
    const response = await apiClient.get<IndustryOption[]>('/api/users/reference/industries')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get user profile with timezone
 * Used for getting timezone_identifier for updating user details
 */
interface UserProfileResponse {
  user_id: number
  email: string
  first_name: string
  last_name: string
  phone: string | null
  timezone_identifier: string
  role_title: string | null
  is_email_verified: boolean
  onboarding_complete: boolean
  onboarding_step: number
}

export async function getUserProfile(): Promise<UserProfileResponse> {
  try {
    const response = await apiClient.get<UserProfileResponse>('/api/users/me')
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}
