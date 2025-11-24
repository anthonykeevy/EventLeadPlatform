/**
 * Form Ownership API Client
 * Handles bulk ownership transfer operations
 */

import { apiClient, formatError } from '../../../lib/apiClient'

// Types
export interface TransferOwnershipRequest {
  from_user_id: number
  to_user_id: number
  company_id: number
  reason?: string
}

export interface TransferOwnershipResponse {
  forms_transferred: number
  access_controls_transferred: number
  status: string
  message: string
  success: boolean
}

// API Functions

/**
 * Transfer all forms from one user to another
 */
export async function transferFormOwnership(request: TransferOwnershipRequest): Promise<TransferOwnershipResponse> {
  try {
    const response = await apiClient.post<TransferOwnershipResponse>('/api/forms/ownership/transfer', request)
    return response.data
  } catch (error) {
    throw formatError(error)
  }
}
