/**
 * Team Management API Client - Story 1.16
 * Handles team invitations and user management
 */

import axios from 'axios'
import { getAccessToken } from '../../auth/utils/tokenStorage'
import type {
  InviteUserRequest,
  InviteUserResponse,
  InvitationListResponse,
  ResendInvitationResponse,
  CancelInvitationResponse,
  EditUserRoleRequest,
  EditUserRoleResponse
} from '../types/team.types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance with auth interceptor
const teamClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add request interceptor to attach access token
teamClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/**
 * Send team invitation
 * AC-1.16.2: Invite User Modal
 */
export async function inviteUser(
  companyId: number,
  data: InviteUserRequest
): Promise<InviteUserResponse> {
  // Transform camelCase to snake_case for backend
  const backendData = {
    email: data.email,
    first_name: data.firstName,
    last_name: data.lastName,
    role: data.role
  }
  
  const response = await teamClient.post(
    `/api/companies/${companyId}/invite`,
    backendData
  )
  return response.data
}

/**
 * List company invitations
 * AC-1.16.3: Invitation List with Actions
 */
export async function listInvitations(
  companyId: number,
  statusFilter?: string,
  page: number = 1,
  pageSize: number = 20
): Promise<InvitationListResponse> {
  const params = new URLSearchParams()
  if (statusFilter) params.append('status_filter', statusFilter)
  params.append('page', page.toString())
  params.append('page_size', pageSize.toString())
  
  const response = await teamClient.get(
    `/api/companies/${companyId}/invitations?${params.toString()}`
  )
  
  // Transform snake_case from backend to camelCase for frontend
  const transformed = {
    invitations: response.data.invitations.map((inv: any) => ({
      invitationId: inv.invitation_id,
      companyId: inv.company_id,
      email: inv.email,
      firstName: inv.first_name,
      lastName: inv.last_name,
      role: inv.role,
      status: inv.status,
      invitedBy: inv.invited_by,
      invitedAt: inv.invited_at,
      expiresAt: inv.expires_at,
      acceptedAt: inv.accepted_at,
      cancelledAt: inv.cancelled_at,
      declinedAt: inv.declined_at,
      resendCount: inv.resend_count,
      lastResentAt: inv.last_resent_at
    })),
    total: response.data.total,
    page: response.data.page,
    pageSize: response.data.page_size
  }
  
  return transformed
}

/**
 * Resend invitation
 * AC-1.16.3: Invitation List with Actions
 */
export async function resendInvitation(
  companyId: number,
  invitationId: number
): Promise<ResendInvitationResponse> {
  const response = await teamClient.post(
    `/api/companies/${companyId}/invitations/${invitationId}/resend`
  )
  
  return {
    success: response.data.success,
    message: response.data.message,
    invitationId: response.data.invitation_id,
    newExpiresAt: response.data.new_expires_at,
    resendCount: response.data.resend_count
  }
}

/**
 * Cancel invitation
 * AC-1.16.3: Invitation List with Actions
 */
export async function cancelInvitation(
  companyId: number,
  invitationId: number
): Promise<CancelInvitationResponse> {
  const response = await teamClient.delete(
    `/api/companies/${companyId}/invitations/${invitationId}`
  )
  
  return {
    success: response.data.success,
    message: response.data.message,
    invitationId: response.data.invitation_id
  }
}

/**
 * Edit user role
 * AC-1.16.6: Role editing modal
 */
export async function editUserRole(
  companyId: number,
  userId: number,
  data: EditUserRoleRequest
): Promise<EditUserRoleResponse> {
  // Transform camelCase to snake_case for backend
  const backendData = {
    role_code: data.roleCode
  }
  
  const response = await teamClient.patch(
    `/api/companies/${companyId}/users/${userId}/role`,
    backendData
  )
  return response.data
}

