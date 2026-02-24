/**
 * Form Access Control API Client for Epic 2 Story 2.9
 * Handles form access control API calls
 */

import {
  FormAccessControlAccessType,
  CompanyRelationshipType,
  GrantAccessRequest,
  AccessListResponse,
  AccessCheckResponse,
  GrantAccessResponse,
  RevokeAccessResponse,
  AccessControlResponse,
  UserResponse,
  CompanyResponse
} from '../types/form-access.types'
import { apiClient, formatError } from '../../../lib/apiClient'

// =====================================================================
// Transformers: Backend to Frontend
// =====================================================================

function transformAccessType(backend: Record<string, unknown>): FormAccessControlAccessType {
  return {
    formAccessControlAccessTypeId: backend.formAccessControlAccessTypeId ?? backend.form_access_control_access_type_id ?? backend.FormAccessControlAccessTypeID ?? 0,
    accessTypeCode: backend.accessTypeCode ?? backend.access_type_code ?? backend.AccessTypeCode ?? '',
    accessTypeName: backend.accessTypeName ?? backend.access_type_name ?? backend.AccessTypeName ?? '',
    accessTypeDescription: backend.accessTypeDescription ?? backend.access_type_description ?? backend.AccessTypeDescription ?? null,
    isActive: backend.isActive ?? backend.is_active ?? backend.IsActive ?? true,
    sortOrder: backend.sortOrder ?? backend.sort_order ?? backend.SortOrder ?? 0,
  }
}

function transformRelationshipType(backend: Record<string, unknown>): CompanyRelationshipType {
  return {
    companyRelationshipTypeId: backend.companyRelationshipTypeId ?? backend.company_relationship_type_id ?? backend.CompanyRelationshipTypeID ?? 0,
    typeName: backend.typeName ?? backend.type_name ?? backend.TypeName ?? '',
    typeDescription: backend.typeDescription ?? backend.type_description ?? backend.TypeDescription ?? null,
    isActive: backend.isActive ?? backend.is_active ?? backend.IsActive ?? true,
  }
}

function transformUserResponse(backend: Record<string, unknown> | null | undefined): UserResponse | null {
  if (!backend) return null
  return {
    userId: backend.userId ?? backend.user_id ?? backend.UserID ?? 0,
    email: backend.email ?? backend.Email ?? '',
    firstName: backend.firstName ?? backend.first_name ?? backend.FirstName ?? null,
    lastName: backend.lastName ?? backend.last_name ?? backend.LastName ?? null,
  }
}

function transformCompanyResponse(backend: Record<string, unknown> | null | undefined): CompanyResponse | null {
  if (!backend) return null
  return {
    companyId: backend.companyId ?? backend.company_id ?? backend.CompanyID ?? 0,
    companyName: backend.companyName ?? backend.company_name ?? backend.CompanyName ?? '',
  }
}

function transformAccessControl(backend: Record<string, unknown>): AccessControlResponse {
  return {
    formAccessControlId: backend.formAccessControlId ?? backend.form_access_control_id ?? backend.FormAccessControlID ?? 0,
    formId: backend.formId ?? backend.form_id ?? backend.FormID ?? 0,
    userId: backend.userId ?? backend.user_id ?? backend.UserID ?? null,
    companyId: backend.companyId ?? backend.company_id ?? backend.CompanyID ?? null,
    formAccessControlAccessTypeId: backend.formAccessControlAccessTypeId ?? backend.form_access_control_access_type_id ?? backend.FormAccessControlAccessTypeID ?? 0,
    companyRelationshipTypeId: backend.companyRelationshipTypeId ?? backend.company_relationship_type_id ?? backend.CompanyRelationshipTypeID ?? null,
    accessType: (backend.accessType ?? backend.access_type) ? transformAccessType((backend.accessType ?? backend.access_type) as Record<string, unknown>) : null,
    relationshipType: (backend.relationshipType ?? backend.relationship_type) ? transformRelationshipType((backend.relationshipType ?? backend.relationship_type) as Record<string, unknown>) : null,
    user: backend.user ? transformUserResponse(backend.user as Record<string, unknown>) : null,
    company: backend.company ? transformCompanyResponse(backend.company as Record<string, unknown>) : null,
    grantedBy: (backend.grantedBy ?? backend.granted_by) ? transformUserResponse((backend.grantedBy ?? backend.granted_by) as Record<string, unknown>) : null,
    grantedDate: backend.grantedDate ?? backend.granted_date ?? backend.GrantedDate ?? '',
    expiryDate: backend.expiryDate ?? backend.expiry_date ?? backend.ExpiryDate ?? null,
    isExpired: backend.isExpired ?? backend.is_expired ?? backend.IsExpired ?? false,
    createdDate: backend.createdDate ?? backend.created_date ?? backend.CreatedDate ?? '',
    updatedDate: backend.updatedDate ?? backend.updated_date ?? backend.UpdatedDate ?? null,
  }
}

// =====================================================================
// API Functions
// =====================================================================

/**
 * Get all access types (reference data)
 */
export async function getAccessTypes(): Promise<FormAccessControlAccessType[]> {
  try {
    const response = await apiClient.get('/api/forms/access-types')
    return (response.data as Record<string, unknown>[]).map(transformAccessType)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get all relationship types (reference data)
 */
export async function getRelationshipTypes(): Promise<CompanyRelationshipType[]> {
  try {
    const response = await apiClient.get('/api/forms/relationship-types')
    return (response.data as Record<string, unknown>[]).map(transformRelationshipType)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Search for users by name or email
 */
export interface UserSearchResult {
  userId: number
  email: string
  firstName: string | null
  lastName: string | null
}

export async function searchUsers(query: string, limit: number = 10): Promise<UserSearchResult[]> {
  try {
    const response = await apiClient.get('/api/forms/search-users', {
      params: { query, limit }
    })
    return (response.data as Record<string, unknown>[]).map((u: Record<string, unknown>) => ({
      userId: u.userId ?? u.user_id ?? u.UserID ?? 0,
      email: u.email ?? u.Email ?? '',
      firstName: u.firstName ?? u.first_name ?? u.FirstName ?? null,
      lastName: u.lastName ?? u.last_name ?? u.LastName ?? null,
    }))
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Search for companies by name
 */
export interface CompanySearchResult {
  companyId: number
  companyName: string
}

export async function searchCompanies(query: string, limit: number = 10): Promise<CompanySearchResult[]> {
  try {
    const response = await apiClient.get('/api/forms/search-companies', {
      params: { query, limit }
    })
    return (response.data as Record<string, unknown>[]).map((c: Record<string, unknown>) => ({
      companyId: c.companyId ?? c.company_id ?? c.CompanyID ?? 0,
      companyName: c.companyName ?? c.company_name ?? c.CompanyName ?? '',
    }))
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get all company members for a form (for dropdown)
 */
export async function getCompanyMembersForForm(formId: number): Promise<UserSearchResult[]> {
  try {
    const response = await apiClient.get(`/api/forms/${formId}/company-members`)
    return (response.data as Record<string, unknown>[]).map((u: Record<string, unknown>) => ({
      userId: u.userId ?? u.user_id ?? u.UserID ?? 0,
      email: u.email ?? u.Email ?? '',
      firstName: u.firstName ?? u.first_name ?? u.FirstName ?? null,
      lastName: u.lastName ?? u.last_name ?? u.LastName ?? null,
    }))
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get all related companies for a form (for dropdown)
 */
export async function getRelatedCompaniesForForm(formId: number): Promise<CompanySearchResult[]> {
  try {
    const response = await apiClient.get(`/api/forms/${formId}/related-companies`)
    return (response.data as Record<string, unknown>[]).map((c: Record<string, unknown>) => ({
      companyId: c.companyId ?? c.company_id ?? c.CompanyID ?? 0,
      companyName: c.companyName ?? c.company_name ?? c.CompanyName ?? '',
    }))
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Grant access to a form
 */
export async function grantFormAccess(
  formId: number,
  request: GrantAccessRequest
): Promise<GrantAccessResponse> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/access`, request)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Access granted successfully',
      accessControl: transformAccessControl(response.data.accessControl ?? response.data.access_control ?? response.data),
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get access list for a form
 */
export async function getFormAccessList(
  formId: number,
  accessTypeId?: number
): Promise<AccessListResponse> {
  try {
    const params: Record<string, string | number> = {}
    if (accessTypeId) {
      params.access_type_id = accessTypeId
    }
    const response = await apiClient.get(`/api/forms/${formId}/access`, { params })
    return {
      accessEntries: (response.data.accessEntries ?? response.data.access_entries ?? []).map(transformAccessControl),
      totalCount: response.data.totalCount ?? response.data.total_count ?? 0,
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Revoke access to a form
 */
export async function revokeFormAccess(
  formId: number,
  accessId: number
): Promise<RevokeAccessResponse> {
  try {
    const response = await apiClient.delete(`/api/forms/${formId}/access/${accessId}`)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Access revoked successfully',
      accessId: response.data.accessId ?? response.data.access_id ?? accessId,
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Check current user's access level to a form
 */
export async function checkFormAccess(formId: number): Promise<AccessCheckResponse> {
  try {
    const response = await apiClient.get(`/api/forms/${formId}/access/check`)
    return {
      hasAccess: response.data.hasAccess ?? response.data.has_access ?? false,
      accessLevel: response.data.accessLevel ?? response.data.access_level ?? null,
      accessType: (response.data.accessType ?? response.data.access_type) 
        ? transformAccessType(response.data.accessType ?? response.data.access_type) 
        : null,
    }
  } catch (error) {
    throw formatError(error)
  }
}
