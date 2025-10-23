/**
 * Auth Features - Story 1.9
 * Frontend Authentication - Signup & Login Pages
 */

// Components
export { SignupForm } from './components/SignupForm'
export { LoginForm } from './components/LoginForm'
export { AuthLayout } from './components/AuthLayout'
export { PasswordStrength } from './components/PasswordStrength'

// Context & Hooks
export { AuthProvider, useAuth } from './context/AuthContext'
export { useAuthPageRedirect, useRequireAuth } from './hooks/useAuthRedirect'

// Types
export type { User, AuthState, LoginCredentials, SignupData, TokenResponse, AuthError } from './types/auth.types'

// API
export * as authApi from './api/authApi'

// Utils
export * as tokenStorage from './utils/tokenStorage'

// Email Verification Page (Story 1.1 Frontend Component - Added 2025-10-21)
export { EmailVerificationPage as EmailVerification } from './pages/EmailVerificationPage'

// Password Reset Pages (Story 1.15 - Added 2025-10-22)
export { PasswordResetRequest } from './pages/PasswordResetRequest'
export { PasswordResetConfirm } from './pages/PasswordResetConfirm'

