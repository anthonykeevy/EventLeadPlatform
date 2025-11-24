/**
 * Auth API Client - Story 1.9 (AC-1.9.10)
 * Handles authentication API calls with automatic token refresh
 */

import { User } from '../types/auth.types'
import { apiClient } from '../../../lib/apiClient'
import { formatAuthError } from './coreAuth'

// Re-export core auth functions (login, signup, refresh, logout)
export * from './coreAuth'

/**
 * Get current user profile
 * Requires valid access token
 * Uses global apiClient which handles auto-refresh on 401 errors
 */
export async function getCurrentUser(): Promise<User> {
  try {
    const response = await apiClient.get<User>('/api/auth/me')
    return response.data
  } catch (error) {
    throw formatAuthError(error)
  }
}
