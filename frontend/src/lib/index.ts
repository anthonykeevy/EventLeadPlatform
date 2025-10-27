/**
 * Library exports
 */
export { 
  signup, 
  verifyEmail, 
  resendVerification, 
  login, 
  calculatePasswordStrength, 
  isValidEmail,
  type SignupRequest,
  type SignupResponse,
  type VerifyEmailResponse,
  type LoginRequest,
  type TokenResponse,
  type ApiError
} from './auth'
export * from './config'

