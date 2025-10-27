/**
 * Invitation Types - Story 1.7 (Frontend)
 */

export interface InvitationDetails {
  invitationId: number
  companyName: string
  roleName: string
  inviterName: string
  invitedEmail: string
  invitedFirstName?: string
  invitedLastName?: string
  expiresAt: string
  isExpired: boolean
  status: string
}

export interface AcceptInvitationResponse {
  success: boolean
  message: string
  companyId: number
  role: string
  accessToken: string
  refreshToken: string
}

export interface SignupWithInvitationRequest {
  invitationToken: string
  password: string
}

