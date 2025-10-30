/**
 * Profile Types for Epic 2 Story 2.1
 * Type definitions for user profile enhancements
 */

export interface ReferenceOption {
  id: number
  code: string
  name: string
  description: string
  cssClass: string
  baseFontSize?: string | null
}

export interface IndustryAssociation {
  userIndustryId: number
  industryId: number
  industryName: string
  industryCode: string
  isPrimary: boolean
  sortOrder: number
}

export interface EnhancedUserProfile {
  userId: number
  email: string
  firstName: string
  lastName: string
  phone: string | null
  bio: string | null
  roleTitle: string | null
  isEmailVerified: boolean
  themePreference: ReferenceOption | null
  layoutDensity: ReferenceOption | null
  fontSize: ReferenceOption | null
  industries: IndustryAssociation[]
}

export interface ProfileUpdateRequest {
  bio?: string | null
  themePreferenceId?: number | null
  layoutDensityId?: number | null
  fontSizeId?: number | null
}

export interface IndustryAssociationRequest {
  industryId: number
  isPrimary: boolean
  sortOrder?: number | null
}

export interface ProfileUpdateResponse {
  success: boolean
  message: string
  userId: number
}

