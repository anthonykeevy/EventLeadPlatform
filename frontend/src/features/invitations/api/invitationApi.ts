/**
 * Invitation API Client - Story 1.7 (Frontend)
 * Handles invitation viewing and acceptance
 */

import axios from 'axios'
import { getAccessToken } from '../../auth/utils/tokenStorage'
import type { InvitationDetails, AcceptInvitationResponse } from '../types/invitation.types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance
const invitationClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add request interceptor to attach access token (if available)
invitationClient.interceptors.request.use(
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
 * View invitation details (public endpoint)
 * AC-1.7.1: Public endpoint to view invitation details
 */
export async function viewInvitation(token: string): Promise<InvitationDetails> {
  const response = await invitationClient.get(`/api/invitations/${token}`)
  
  // Transform snake_case from backend to camelCase for frontend
  return {
    invitationId: response.data.invitation_id,
    companyName: response.data.company_name,
    roleName: response.data.role_name,
    inviterName: response.data.inviter_name,
    invitedEmail: response.data.invited_email,
    invitedFirstName: response.data.invited_first_name,
    invitedLastName: response.data.invited_last_name,
    expiresAt: response.data.expires_at,
    isExpired: response.data.is_expired,
    status: response.data.status
  }
}

/**
 * Accept invitation (requires authentication)
 * AC-1.7.3: Protected endpoint to accept invitation
 */
export async function acceptInvitation(token: string): Promise<AcceptInvitationResponse> {
  const response = await invitationClient.post(`/api/invitations/${token}/accept`)
  
  return {
    success: response.data.success,
    message: response.data.message,
    companyId: response.data.company_id,
    role: response.data.role,
    accessToken: response.data.access_token,
    refreshToken: response.data.refresh_token
  }
}

/**
 * Sign up with invitation (new user)
 * AC-1.7.5, AC-1.7.6: New user signup with auto-accept
 */
export async function signupWithInvitation(
  email: string,
  firstName: string,
  lastName: string,
  password: string,
  token: string
): Promise<AcceptInvitationResponse> {
  const response = await invitationClient.post('/api/auth/signup', {
    email: email,
    password: password,
    first_name: firstName,
    last_name: lastName,
    invitation_token: token
  })
  
  return {
    success: true,
    message: response.data.message || 'Account created successfully',
    companyId: response.data.data?.company_id || 0,
    role: response.data.data?.role || '',
    accessToken: response.data.data?.access_token || '',
    refreshToken: response.data.data?.refresh_token || ''
  }
}

