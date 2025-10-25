/**
 * Token Storage Utilities - Story 1.9 (AC-1.9.3)
 * Secure localStorage wrapper for JWT token management
 * 
 * Security Notes:
 * - MVP: Uses localStorage (httpOnly cookies planned for Phase 2)
 * - Tokens are stored with prefixed keys to avoid collisions
 * - All storage operations are wrapped in try-catch for robustness
 * - Token expiration is tracked separately for auto-refresh logic
 */

const ACCESS_TOKEN_KEY = 'eventlead_access_token'
const REFRESH_TOKEN_KEY = 'eventlead_refresh_token'
const TOKEN_EXPIRY_KEY = 'eventlead_token_expiry'

export interface StoredTokens {
  accessToken: string
  refreshToken: string
  expiresAt: number // Unix timestamp in seconds
}

/**
 * Store JWT tokens securely in localStorage
 * AC-1.9.3: Persist tokens in localStorage/sessionStorage with security considerations
 */
export function storeTokens(accessToken: string, refreshToken: string, expiresIn: number = 3600): void {
  try {
    const expiresAt = Math.floor(Date.now() / 1000) + expiresIn
    
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
    localStorage.setItem(TOKEN_EXPIRY_KEY, expiresAt.toString())
  } catch (error) {
    console.error('Failed to store tokens:', error)
    throw new Error('Unable to persist authentication. Please check browser storage settings.')
  }
}

/**
 * Retrieve stored JWT tokens
 * Returns null if tokens don't exist or are corrupted
 */
export function getStoredTokens(): StoredTokens | null {
  try {
    const accessToken = localStorage.getItem(ACCESS_TOKEN_KEY)
    const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)
    const expiresAt = localStorage.getItem(TOKEN_EXPIRY_KEY)
    
    if (!accessToken || !refreshToken || !expiresAt) {
      return null
    }
    
    return {
      accessToken,
      refreshToken,
      expiresAt: parseInt(expiresAt, 10),
    }
  } catch (error) {
    console.error('Failed to retrieve tokens:', error)
    return null
  }
}

/**
 * Get access token only (for API requests)
 */
export function getAccessToken(): string | null {
  try {
    return localStorage.getItem(ACCESS_TOKEN_KEY)
  } catch (error) {
    console.error('Failed to retrieve access token:', error)
    return null
  }
}

/**
 * Get refresh token only (for token refresh flow)
 */
export function getRefreshToken(): string | null {
  try {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  } catch (error) {
    console.error('Failed to retrieve refresh token:', error)
    return null
  }
}

/**
 * Clear all stored tokens (for logout)
 * AC-1.9.3: Logout functionality (clear tokens, redirect to login)
 */
export function clearTokens(): void {
  try {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(TOKEN_EXPIRY_KEY)
  } catch (error) {
    console.error('Failed to clear tokens:', error)
  }
}

/**
 * Check if access token is expired or will expire soon
 * AC-1.9.3: Token expiry handling with automatic refresh
 * @param bufferSeconds - Refresh token this many seconds before actual expiry (default: 5 minutes)
 */
export function isTokenExpiringSoon(bufferSeconds: number = 300): boolean {
  try {
    const expiresAt = localStorage.getItem(TOKEN_EXPIRY_KEY)
    if (!expiresAt) return true
    
    const expiryTime = parseInt(expiresAt, 10)
    const currentTime = Math.floor(Date.now() / 1000)
    const timeUntilExpiry = expiryTime - currentTime
    
    return timeUntilExpiry <= bufferSeconds
  } catch (error) {
    console.error('Failed to check token expiry:', error)
    return true // Assume expired on error
  }
}

/**
 * Check if token is completely expired
 */
export function isTokenExpired(): boolean {
  try {
    const expiresAt = localStorage.getItem(TOKEN_EXPIRY_KEY)
    if (!expiresAt) return true
    
    const expiryTime = parseInt(expiresAt, 10)
    const currentTime = Math.floor(Date.now() / 1000)
    
    return currentTime >= expiryTime
  } catch (error) {
    console.error('Failed to check token expiry:', error)
    return true
  }
}

/**
 * Decode JWT payload (without verification - only for reading user info)
 * Returns null if token is invalid or malformed
 */
export function decodeJWT(token: string): any | null {
  try {
    const payload = token.split('.')[1]
    if (!payload) return null
    
    const decoded = atob(payload)
    return JSON.parse(decoded)
  } catch (error) {
    console.error('Failed to decode JWT:', error)
    return null
  }
}




