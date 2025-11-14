/**
 * Auth Type Definitions - Story 1.9
 * TypeScript interfaces for authentication state and API responses
 */

export interface User {
  id: number
  user_id: number  // Alias for id for backward compatibility
  email: string
  first_name: string
  last_name: string
  email_verified: boolean
  is_active: boolean
  onboarding_complete: boolean
  created_at: string
  role?: string  // System role (e.g., 'system_admin') or company role (e.g., 'company_admin', 'company_user')
  company_id?: number  // Primary company ID (optional for system admins)
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupData {
  email: string
  password: string
  first_name: string
  last_name: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in?: number  // Token expiry time in seconds (optional for backward compatibility)
  user?: User  // Optional - refresh endpoint may not include user
}

export interface AuthError {
  message: string
  code?: string
  status?: number
}




