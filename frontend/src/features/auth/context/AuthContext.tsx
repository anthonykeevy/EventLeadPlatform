/**
 * Auth Context - Story 1.9 (AC-1.9.3)
 * React context for global authentication state management
 * 
 * Features:
 * - Store and manage JWT access token and refresh token
 * - Provide current user object (from JWT payload)
 * - Auto-refresh access token before expiration
 * - Logout functionality (clear tokens, redirect to login)
 * - Persist tokens in localStorage with security considerations
 * - Token expiry handling with automatic refresh
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import type { User, AuthState, LoginCredentials, SignupData } from '../types/auth.types'
import * as authApi from '../api/authApi'
import * as tokenStorage from '../utils/tokenStorage'

interface AuthContextValue extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>
  signup: (data: SignupData) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  })
  
  const navigate = useNavigate()
  const refreshTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  
  /**
   * AC-1.9.3: Auto-refresh access token before expiration
   * Refresh token 5 minutes (300 seconds) before expiry
   */
  const scheduleTokenRefresh = useCallback(() => {
    // Clear existing timeout
    if (refreshTimeoutRef.current) {
      clearTimeout(refreshTimeoutRef.current)
    }
    
    const tokens = tokenStorage.getStoredTokens()
    if (!tokens) return
    
    const currentTime = Math.floor(Date.now() / 1000)
    const timeUntilExpiry = tokens.expiresAt - currentTime
    const refreshBuffer = 300 // 5 minutes
    
    // Schedule refresh for 5 minutes before expiry
    const refreshIn = Math.max(0, timeUntilExpiry - refreshBuffer) * 1000
    
    refreshTimeoutRef.current = setTimeout(async () => {
      try {
        await refreshToken()
      } catch (error) {
        console.error('Auto-refresh failed:', error)
        logout()
      }
    }, refreshIn)
  }, [])
  
  /**
   * AC-1.9.2: Success - Store JWT tokens and navigate to dashboard/onboarding
   * If onboarding_complete=false → /onboarding
   * If onboarding_complete=true → /dashboard
   */
  const login = useCallback(async (credentials: LoginCredentials) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }))
    
    try {
      const response = await authApi.loginUser(credentials)
      
      // Store tokens
      tokenStorage.storeTokens(response.access_token, response.refresh_token, 3600)
      
      // Update state with user
      setState({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      })
      
      // Schedule auto-refresh
      scheduleTokenRefresh()
      
      // Always navigate to dashboard (Story 1.14)
      // Onboarding modal will appear automatically if onboarding_complete=false
      navigate('/dashboard')
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed'
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }))
      throw error
    }
  }, [navigate, scheduleTokenRefresh])
  
  /**
   * AC-1.9.1: Form submission calls POST /api/auth/signup endpoint
   * Success: Display "Check your email" message with verification instructions
   */
  const signup = useCallback(async (data: SignupData) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }))
    
    try {
      await authApi.signupUser(data)
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: null,
      }))
      
      // Note: Don't auto-login after signup - user must verify email first
      // Signup success is handled in the component (show success message)
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Signup failed'
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }))
      throw error
    }
  }, [])
  
  /**
   * AC-1.9.3: Logout functionality (clear tokens, redirect to login)
   */
  const logout = useCallback(() => {
    // Clear refresh timeout
    if (refreshTimeoutRef.current) {
      clearTimeout(refreshTimeoutRef.current)
    }
    
    // Clear tokens
    tokenStorage.clearTokens()
    
    // Reset state
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    })
    
    // Redirect to login
    navigate('/login')
  }, [navigate])
  
  /**
   * AC-1.9.3: Refresh access token
   */
  const refreshToken = useCallback(async () => {
    try {
      const response = await authApi.refreshAccessToken()
      
      // Store new tokens
      tokenStorage.storeTokens(response.access_token, response.refresh_token, 3600)
      
      // Update user state if provided
      if (response.user) {
        setState(prev => ({
          ...prev,
          user: response.user,
        }))
      }
      
      // Schedule next refresh
      scheduleTokenRefresh()
    } catch (error) {
      console.error('Token refresh failed:', error)
      logout()
    }
  }, [logout, scheduleTokenRefresh])
  
  /**
   * Refresh current user data (after onboarding, profile updates, etc.)
   */
  const refreshUser = useCallback(async () => {
    try {
      const user = await authApi.getCurrentUser()
      setState(prev => ({
        ...prev,
        user,
      }))
    } catch (error) {
      console.error('Failed to refresh user:', error)
      // Don't logout - just log the error
    }
  }, [])
  
  /**
   * Initialize auth state on mount
   * Check for existing tokens and restore session
   */
  useEffect(() => {
    const initializeAuth = async () => {
      const tokens = tokenStorage.getStoredTokens()
      
      if (!tokens) {
        setState(prev => ({ ...prev, isLoading: false }))
        return
      }
      
      // Check if token is expired
      if (tokenStorage.isTokenExpired()) {
        tokenStorage.clearTokens()
        setState(prev => ({ ...prev, isLoading: false }))
        return
      }
      
      try {
        // Try to get current user with stored token
        const user = await authApi.getCurrentUser()
        
        setState({
          user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
        
        // Schedule token refresh
        scheduleTokenRefresh()
      } catch (error) {
        console.error('Failed to restore session:', error)
        tokenStorage.clearTokens()
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        })
      }
    }
    
    initializeAuth()
    
    // Cleanup on unmount
    return () => {
      if (refreshTimeoutRef.current) {
        clearTimeout(refreshTimeoutRef.current)
      }
    }
  }, [scheduleTokenRefresh])
  
  const value: AuthContextValue = {
    ...state,
    login,
    signup,
    logout,
    refreshToken,
    refreshUser,
  }
  
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

/**
 * AC-1.9.3: useAuth() hook for consuming components
 * Provides: user, loading, login(), logout(), signup() functions
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  
  return context
}



