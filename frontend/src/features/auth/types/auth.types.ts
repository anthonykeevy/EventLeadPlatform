/**
 * Auth Type Definitions - Story 1.9
 * TypeScript interfaces for authentication state and API responses
 */

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  email_verified: boolean
  is_active: boolean
  onboarding_complete: boolean
  created_at: string
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
  user: User
}

export interface AuthError {
  message: string
  code?: string
  status?: number
}




