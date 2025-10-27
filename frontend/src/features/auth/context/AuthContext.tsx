/**
 * Auth Context - Story 1.9 (AC-1.9.3) + Story 1.16 Enhanced
 * React context for global authentication state management
 * 
 * Features:
 * - Store and manage JWT access token and refresh token
 * - Provide current user object (from JWT payload)
 * - Auto-refresh access token before expiration
 * - Logout functionality (clear tokens, redirect to login)
 * - Persist tokens in localStorage with security considerations
 * - Token expiry handling with automatic refresh
 * 
 * Story 1.16 Enhanced Features:
 * - Graceful multi-tab synchronization (no forced reloads)
 * - Unsaved work detection and protection
 * - BroadcastChannel API with localStorage fallback
 * - Non-blocking auth change notifications
 * - Offline-ready architecture
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import type { User, AuthState, LoginCredentials, SignupData } from '../types/auth.types'
import * as authApi from '../api/authApi'
import * as tokenStorage from '../utils/tokenStorage'
import { unsavedWorkTracker } from '../../../utils/unsavedWorkTracker'
import { AuthChangeBanner } from '../../../components/AuthChangeBanner'

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
  
  const [authChangeBanner, setAuthChangeBanner] = useState<{
    show: boolean
    type: 'logout' | 'login' | 'switch'
    message: string
    description?: string
    newUser?: User | null
  } | null>(null)
  
  const navigate = useNavigate()
  const location = useLocation()
  const refreshTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const broadcastChannelRef = useRef<BroadcastChannel | null>(null)
  
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
   * Story 1.16 Enhanced: Graceful logout with unsaved work check
   */
  const logout = useCallback(() => {
    // Check for unsaved work
    const hasUnsavedWork = unsavedWorkTracker.hasUnsavedWork()
    
    if (hasUnsavedWork) {
      const unsavedCount = unsavedWorkTracker.getUnsavedCount()
      const summary = unsavedWorkTracker.getSummary()
      
      const confirmed = confirm(
        `You have ${unsavedCount} unsaved item(s):\n\n${summary}\n\nAre you sure you want to logout?`
      )
      
      if (!confirmed) {
        return // User cancelled logout
      }
    }
    
    // Proceed with logout
    performLogout()
  }, [])
  
  /**
   * Perform actual logout (internal)
   */
  const performLogout = useCallback(() => {
    // Clear refresh timeout
    if (refreshTimeoutRef.current) {
      clearTimeout(refreshTimeoutRef.current)
    }
    
    // Broadcast logout to other tabs
    broadcastAuthChange({ type: 'LOGOUT' })
    
    // Clear ALL localStorage (not just tokens)
    tokenStorage.clearAllStorage()
    
    // Clear unsaved work tracker
    unsavedWorkTracker.clear()
    
    // Reset state
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    })
    
    // Navigate to login (NO RELOAD - just navigate)
    navigate('/login')
  }, [navigate])
  
  /**
   * AC-1.9.2: Login - Store tokens and navigate
   * Story 1.16 Enhanced: Force reload on initial login for clean state
   */
  const login = useCallback(async (credentials: LoginCredentials) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }))
    
    try {
      const response = await authApi.loginUser(credentials)
      
      // Store tokens
      tokenStorage.storeTokens(response.access_token, response.refresh_token, 3600)
      
      // Broadcast login to other tabs
      broadcastAuthChange({ 
        type: 'LOGIN',
        user: response.user
      })
      
      // Update state with user
      setState({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      })
      
      // Schedule auto-refresh
      scheduleTokenRefresh()
      
      // FORCE RELOAD on initial login to ensure fresh auth state
      // This is different from cross-tab sync (which is graceful)
      window.location.href = '/dashboard'
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed'
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }))
      throw error
    }
  }, [scheduleTokenRefresh])
  
  /**
   * AC-1.9.1: Signup
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
   * Refresh current user data
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
    }
  }, [])
  
  /**
   * Broadcast auth change to other tabs
   */
  const broadcastAuthChange = useCallback((message: any) => {
    // Try BroadcastChannel first (modern browsers)
    if (broadcastChannelRef.current) {
      try {
        broadcastChannelRef.current.postMessage(message)
      } catch (error) {
        console.error('BroadcastChannel failed:', error)
      }
    }
    
    // Also update localStorage to trigger storage events (fallback for older browsers)
    // This is handled automatically by storeTokens/clearTokens
  }, [])
  
  /**
   * Handle auth change from another tab
   */
  const handleAuthChangeFromOtherTab = useCallback((newUser: User | null, changeType: 'login' | 'logout' | 'switch') => {
    // Check if current tab has unsaved work
    const hasUnsavedWork = unsavedWorkTracker.hasUnsavedWork()
    
    if (hasUnsavedWork) {
      // DON'T sync immediately - show banner instead
      const unsavedCount = unsavedWorkTracker.getUnsavedCount()
      const summary = unsavedWorkTracker.getSummary()
      
      setAuthChangeBanner({
        show: true,
        type: changeType,
        message: changeType === 'logout' 
          ? 'You\'ve been logged out in another tab'
          : newUser
          ? `Logged in as ${newUser.email} in another tab`
          : 'Auth state changed in another tab',
        description: `You have ${unsavedCount} unsaved item(s): ${summary}. Save your work before syncing.`,
        newUser
      })
    } else {
      // No unsaved work - safe to sync immediately
      if (changeType === 'logout') {
        console.log('🔄 Syncing logout from another tab')
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        })
        navigate('/login')
      } else if (newUser) {
        console.log('🔄 Syncing login from another tab')
        setState({
          user: newUser,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
        
        // Only navigate if not already on dashboard
        if (!location.pathname.startsWith('/dashboard')) {
          navigate('/dashboard')
        }
      }
    }
  }, [navigate, location])
  
  /**
   * Handle "Save & Continue" from banner
   */
  const handleSaveAndSync = useCallback(async () => {
    try {
      // Save all unsaved work
      await unsavedWorkTracker.saveAll()
      
      // Now safe to sync auth state
      if (authChangeBanner?.type === 'logout') {
        performLogout()
      } else if (authChangeBanner?.newUser) {
        setState({
          user: authChangeBanner.newUser,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
        navigate('/dashboard')
      }
      
      // Hide banner
      setAuthChangeBanner(null)
    } catch (error) {
      console.error('Failed to save work:', error)
      alert('Failed to save your work. Please try again or cancel the operation.')
    }
  }, [authChangeBanner, navigate])
  
  /**
   * Initialize auth state on mount
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
  
  /**
   * Story 1.16 Enhanced: Multi-tab synchronization
   * Uses BroadcastChannel with localStorage fallback
   */
  useEffect(() => {
    // Try to create BroadcastChannel (modern browsers)
    try {
      broadcastChannelRef.current = new BroadcastChannel('eventlead_auth')
      
      broadcastChannelRef.current.onmessage = (event) => {
        const { type, user } = event.data
        
        switch (type) {
          case 'LOGIN':
            handleAuthChangeFromOtherTab(user, 'login')
            break
          case 'LOGOUT':
            handleAuthChangeFromOtherTab(null, 'logout')
            break
          case 'SWITCH_COMPANY':
            // Company switch doesn't require full auth sync
            // Just refresh user data
            refreshUser()
            break
        }
      }
      
      console.log('✅ BroadcastChannel initialized')
    } catch (error) {
      console.log('⚠️ BroadcastChannel not available, using localStorage fallback')
      broadcastChannelRef.current = null
    }
    
    // Fallback: localStorage events (for older browsers or if BroadcastChannel fails)
    const handleStorageChange = (e: StorageEvent) => {
      // Storage event fires when localStorage changes in OTHER tabs
      if (e.key === 'eventlead_access_token' || e.key === null) {
        if (!e.newValue) {
          // Token was removed (logout in another tab)
          console.log('🔄 Logout detected in another tab (storage event)')
          handleAuthChangeFromOtherTab(null, 'logout')
        } else {
          // Token was added/updated (login in another tab)
          console.log('🔄 Login detected in another tab (storage event)')
          
          // Decode the new token to get user info
          try {
            const payload = tokenStorage.decodeJWT(e.newValue)
            const newUser: User = {
              id: payload.user_id,
              user_id: payload.user_id,
              email: payload.email,
              first_name: payload.first_name || '',
              last_name: payload.last_name || '',
              email_verified: payload.email_verified !== false,
              is_active: payload.is_active !== false,
              onboarding_complete: payload.onboarding_complete !== false,
              created_at: payload.created_at || new Date().toISOString()
            }
            handleAuthChangeFromOtherTab(newUser, 'login')
          } catch (error) {
            console.error('Failed to decode token from storage event:', error)
          }
        }
      }
    }
    
    // Listen for storage changes from other tabs
    window.addEventListener('storage', handleStorageChange)
    
    return () => {
      // Cleanup
      if (broadcastChannelRef.current) {
        broadcastChannelRef.current.close()
      }
      window.removeEventListener('storage', handleStorageChange)
    }
  }, [handleAuthChangeFromOtherTab, refreshUser])
  
  /**
   * Setup beforeunload warning if unsaved work exists
   */
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (unsavedWorkTracker.hasUnsavedWork()) {
        e.preventDefault()
        e.returnValue = 'You have unsaved changes. Are you sure you want to leave?'
        return e.returnValue
      }
    }
    
    window.addEventListener('beforeunload', handleBeforeUnload)
    
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
    }
  }, [])
  
  const value: AuthContextValue = {
    ...state,
    login,
    signup,
    logout,
    refreshToken,
    refreshUser,
  }
  
  return (
    <AuthContext.Provider value={value}>
      {/* Auth Change Banner */}
      {authChangeBanner?.show && (
        <AuthChangeBanner
          type={authChangeBanner.type}
          message={authChangeBanner.message}
          description={authChangeBanner.description}
          unsavedCount={unsavedWorkTracker.getUnsavedCount()}
          onSave={handleSaveAndSync}
          onDismiss={() => setAuthChangeBanner(null)}
          onProceed={async () => {
            // Proceed without saving (already confirmed in banner)
            if (authChangeBanner.type === 'logout') {
              performLogout()
            } else if (authChangeBanner.newUser) {
              setState({
                user: authChangeBanner.newUser,
                isAuthenticated: true,
                isLoading: false,
                error: null,
              })
              navigate('/dashboard')
            }
            setAuthChangeBanner(null)
          }}
          allowContinue={true}
        />
      )}
      
      {children}
    </AuthContext.Provider>
  )
}

/**
 * AC-1.9.3: useAuth() hook for consuming components
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  
  return context
}
