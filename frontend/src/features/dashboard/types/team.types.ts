/**
 * Team Management Types - Story 1.16
 * Type definitions for team invitations and management
 */

export interface Invitation {
  invitationId: number
  companyId: number
  email: string
  firstName: string
  lastName: string
  role: string
  status: 'pending' | 'accepted' | 'expired' | 'cancelled'
  invitedBy: string
  invitedAt: string
  expiresAt: string
  acceptedAt?: string | null
  cancelledAt?: string | null
  declinedAt?: string | null
  resendCount: number
  lastResentAt?: string | null
}

export interface InviteUserRequest {
  email: string
  firstName: string
  lastName: string
  role: 'company_admin' | 'company_user'
}

export interface InviteUserResponse {
  success: boolean
  message: string
  invitationId?: number
  expiresAt?: string
}

export interface InvitationListResponse {
  invitations: Invitation[]
  total: number
  page: number
  pageSize: number
}

export interface ResendInvitationResponse {
  success: boolean
  message: string
  invitationId: number
  newExpiresAt: string
  resendCount: number
}

export interface CancelInvitationResponse {
  success: boolean
  message: string
  invitationId: number
}

export interface EditUserRoleRequest {
  roleCode: 'company_admin' | 'company_user'
}

export interface EditUserRoleResponse {
  success: boolean
  message: string
}


