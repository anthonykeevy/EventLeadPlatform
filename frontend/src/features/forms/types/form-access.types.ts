/**
 * Form Access Control Types for Epic 2 Story 2.9
 * Type definitions for form access control management
 */

// Reference Data Types
export interface FormAccessControlAccessType {
  formAccessControlAccessTypeId: number
  accessTypeCode: string
  accessTypeName: string
  accessTypeDescription: string | null
  isActive: boolean
  sortOrder: number
}

export interface CompanyRelationshipType {
  companyRelationshipTypeId: number
  typeName: string
  typeDescription: string | null
  isActive: boolean
}

// User and Company Response Types
export interface UserResponse {
  userId: number
  email: string
  firstName: string | null
  lastName: string | null
}

export interface CompanyResponse {
  companyId: number
  companyName: string
}

// Main Access Control Type
export interface FormAccessControl {
  formAccessControlId: number
  formId: number
  userId: number
  companyId: number
  formAccessControlAccessTypeId: number
  companyRelationshipTypeId: number
  accessType: FormAccessControlAccessType | null
  relationshipType: CompanyRelationshipType | null
  grantedBy: UserResponse | null
  grantedDate: string
  expiryDate: string | null
  isExpired: boolean
  createdDate: string
  updatedDate: string | null
}

// Request Types
export interface GrantAccessRequest {
  userId?: number | null
  companyId?: number | null
  formAccessControlAccessTypeId: number
  companyRelationshipTypeId: number
  expiryDate?: string | null
}

// Response Types
export interface AccessControlResponse {
  formAccessControlId: number
  formId: number
  userId: number | null
  companyId: number | null
  formAccessControlAccessTypeId: number
  companyRelationshipTypeId: number | null
  accessType: FormAccessControlAccessType | null
  relationshipType: CompanyRelationshipType | null
  user: UserResponse | null
  company: CompanyResponse | null
  grantedBy: UserResponse | null
  grantedDate: string
  expiryDate: string | null
  isExpired: boolean
  createdDate: string
  updatedDate: string | null
}

export interface AccessListResponse {
  accessEntries: AccessControlResponse[]
  totalCount: number
}

export interface AccessCheckResponse {
  hasAccess: boolean
  accessLevel: string | null
  accessType: FormAccessControlAccessType | null
}

export interface GrantAccessResponse {
  success: boolean
  message: string
  accessControl: AccessControlResponse
}

export interface RevokeAccessResponse {
  success: boolean
  message: string
  accessId: number
}

