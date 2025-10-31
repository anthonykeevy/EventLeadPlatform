/**
 * Theme Context for Epic 2 Story 2.2
 * Provides theme state management using React Context + useReducer
 */

import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react'
import { ReferenceOption } from '../../profile/types/profile.types'
import { getEnhancedProfile } from '../../profile/api/usersApi'
import { useAuth } from '../../auth'

// Theme state interface
export interface ThemeState {
  theme: ReferenceOption | null
  layoutDensity: ReferenceOption | null
  fontSize: ReferenceOption | null
  systemTheme: 'light' | 'dark' | null
  isLoading: boolean
  error: string | null
}

// Theme actions
export type ThemeAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_THEME'; payload: ReferenceOption | null }
  | { type: 'SET_LAYOUT_DENSITY'; payload: ReferenceOption | null }
  | { type: 'SET_FONT_SIZE'; payload: ReferenceOption | null }
  | { type: 'SET_SYSTEM_THEME'; payload: 'light' | 'dark' | null }
  | { type: 'INITIALIZE_THEME'; payload: Partial<ThemeState> }

// Theme context interface
export interface ThemeContextType {
  state: ThemeState
  dispatch: React.Dispatch<ThemeAction>
  // Helper functions
  applyTheme: (theme: ReferenceOption) => void
  applyLayoutDensity: (density: ReferenceOption) => void
  applyFontSize: (fontSize: ReferenceOption) => void
  detectSystemTheme: () => 'light' | 'dark'
  saveToLocalStorage: () => void
  loadFromLocalStorage: () => void
  resetTheme: () => void // Reset to browser defaults
}

// Initial state
const initialState: ThemeState = {
  theme: null,
  layoutDensity: null,
  fontSize: null,
  systemTheme: null,
  isLoading: true,
  error: null
}

// Theme reducer
function themeReducer(state: ThemeState, action: ThemeAction): ThemeState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false }
    
    case 'SET_THEME':
      return { ...state, theme: action.payload, error: null }
    
    case 'SET_LAYOUT_DENSITY':
      return { ...state, layoutDensity: action.payload, error: null }
    
    case 'SET_FONT_SIZE':
      return { ...state, fontSize: action.payload, error: null }
    
    case 'SET_SYSTEM_THEME':
      return { ...state, systemTheme: action.payload }
    
    case 'INITIALIZE_THEME':
      return { ...state, ...action.payload, isLoading: false, error: null }
    
    default:
      return state
  }
}

// Create context
const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

// Theme provider component
export interface ThemeProviderProps {
  children: ReactNode
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [state, dispatch] = useReducer(themeReducer, initialState)
  const { user, isAuthenticated } = useAuth()

  // Detect system theme preference
  const detectSystemTheme = (): 'light' | 'dark' => {
    if (typeof window === 'undefined') return 'light'
    
    try {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      return mediaQuery.matches ? 'dark' : 'light'
    } catch (error) {
      console.warn('Failed to detect system theme:', error)
      return 'light'
    }
  }

  // Apply theme to document
  const applyTheme = (theme: ReferenceOption) => {
    if (typeof document === 'undefined') return
    
    try {
      // Remove existing theme classes and dark class
      document.documentElement.className = document.documentElement.className
        .replace(/theme-\w+/g, '')
        .replace(/\bdark\b/g, '')
        .replace(/\s+/g, ' ')
        .trim()
      
      // Handle system theme - apply actual theme based on system preference
      if (theme.code === 'system') {
        const systemTheme = detectSystemTheme()
        if (systemTheme === 'dark') {
          document.documentElement.classList.add('theme-dark', 'dark')
        } else {
          document.documentElement.classList.add('theme-light')
        }
        document.documentElement.classList.add('theme-system')
        document.documentElement.style.setProperty('--theme-mode', 'system')
      } else {
        // Add theme class
        if (theme.css_class) {
          document.documentElement.classList.add(theme.css_class)
        }
        
        // Add 'dark' class for Tailwind compatibility if dark theme (but not high-contrast)
        if ((theme.code === 'dark' || theme.css_class === 'theme-dark') && theme.code !== 'high-contrast') {
          document.documentElement.classList.add('dark')
        }
        
        // Set CSS custom properties
        document.documentElement.style.setProperty('--theme-mode', theme.code)
      }
      
      console.log(`Theme applied: ${theme.name} (${theme.code})`)
    } catch (error) {
      console.error('Failed to apply theme:', error)
      dispatch({ type: 'SET_ERROR', payload: 'Failed to apply theme' })
    }
  }

  // Apply layout density to document
  const applyLayoutDensity = (density: ReferenceOption) => {
    if (typeof document === 'undefined') return
    
    try {
      // Remove existing density classes
      document.documentElement.className = document.documentElement.className
        .replace(/layout-\w+/g, '')
        .replace(/\s+/g, ' ')
        .trim()
      
      // Add new density class
      if (density.css_class) {
        document.documentElement.classList.add(density.css_class)
      }
      
      // Set CSS custom properties
      document.documentElement.style.setProperty('--layout-density', density.code)
      
      console.log(`Layout density applied: ${density.name} (${density.code})`)
    } catch (error) {
      console.error('Failed to apply layout density:', error)
      dispatch({ type: 'SET_ERROR', payload: 'Failed to apply layout density' })
    }
  }

  // Apply font size to document
  const applyFontSize = (fontSize: ReferenceOption) => {
    if (typeof document === 'undefined') return
    
    try {
      // Remove existing font size classes
      document.documentElement.className = document.documentElement.className
        .replace(/font-\w+/g, '')
        .replace(/\s+/g, ' ')
        .trim()
      
      // Add new font size class
      if (fontSize.css_class) {
        document.documentElement.classList.add(fontSize.css_class)
      }
      
      // Set CSS custom properties
      if (fontSize.base_font_size) {
        document.documentElement.style.setProperty('--base-font-size', fontSize.base_font_size)
        // Also apply to body element for global font size change
        document.body.style.fontSize = fontSize.base_font_size
      }
      document.documentElement.style.setProperty('--font-size', fontSize.code)
      
      console.log(`Font size applied: ${fontSize.name} (${fontSize.code})`)
    } catch (error) {
      console.error('Failed to apply font size:', error)
      dispatch({ type: 'SET_ERROR', payload: 'Failed to apply font size' })
    }
  }

  // Save theme preferences to localStorage
  const saveToLocalStorage = () => {
    if (typeof window === 'undefined') return
    
    try {
      const themeData = {
        theme: state.theme,
        layoutDensity: state.layoutDensity,
        fontSize: state.fontSize,
        systemTheme: state.systemTheme,
        timestamp: Date.now()
      }
      
      localStorage.setItem('eventlead-theme-preferences', JSON.stringify(themeData))
      console.log('Theme preferences saved to localStorage')
    } catch (error) {
      console.error('Failed to save theme preferences:', error)
    }
  }

  // Load theme preferences from localStorage
  const loadFromLocalStorage = () => {
    if (typeof window === 'undefined') return null
    
    try {
      const stored = localStorage.getItem('eventlead-theme-preferences')
      if (!stored) return null
      
      const themeData = JSON.parse(stored)
      
      // Check if data is not too old (7 days)
      const maxAge = 7 * 24 * 60 * 60 * 1000 // 7 days in milliseconds
      if (Date.now() - themeData.timestamp > maxAge) {
        localStorage.removeItem('eventlead-theme-preferences')
        return null
      }
      
      return themeData
    } catch (error) {
      console.error('Failed to load theme preferences:', error)
      localStorage.removeItem('eventlead-theme-preferences')
      return null
    }
  }

  // Reset theme to browser defaults (on logout)
  const resetTheme = React.useCallback(() => {
    if (typeof document === 'undefined') return
    
    try {
      console.log('Resetting theme to browser defaults...')
      
      // Get current classes for debugging
      const currentClasses = document.documentElement.className
      console.log('Current document classes before reset:', currentClasses)
      
      // Remove all theme classes - more aggressive approach
      let classes = document.documentElement.className.split(/\s+/)
      classes = classes.filter(cls => 
        !cls.startsWith('theme-') && 
        !cls.startsWith('layout-') && 
        !cls.startsWith('font-') && 
        cls !== 'dark'
      )
      document.documentElement.className = classes.join(' ').trim()
      
      // Reset CSS custom properties
      document.documentElement.style.removeProperty('--theme-mode')
      document.documentElement.style.removeProperty('--layout-density')
      document.documentElement.style.removeProperty('--font-size')
      document.documentElement.style.removeProperty('--base-font-size')
      
      // Reset body font size
      document.body.style.fontSize = ''
      document.body.style.removeProperty('font-size')
      
      // Reset state
      dispatch({ type: 'INITIALIZE_THEME', payload: initialState })
      
      // Clear localStorage on logout (even if it was already cleared)
      if (typeof window !== 'undefined') {
        try {
          localStorage.removeItem('eventlead-theme-preferences')
        } catch (e) {
          // localStorage might be cleared already, ignore
        }
      }
      
      console.log('Theme reset to browser defaults - classes after reset:', document.documentElement.className)
    } catch (error) {
      console.error('Failed to reset theme:', error)
    }
  }, [dispatch])

  // Initialize theme on mount and when user logs in
  useEffect(() => {
    const initializeTheme = async () => {
      try {
        dispatch({ type: 'SET_LOADING', payload: true })
        
        // Detect system theme
        const systemTheme = detectSystemTheme()
        dispatch({ type: 'SET_SYSTEM_THEME', payload: systemTheme })
        
        // If user is authenticated, load preferences from backend
        if (isAuthenticated && user) {
          try {
            console.log('Loading theme preferences from backend for user:', user.email)
            const profile = await getEnhancedProfile()
            console.log('Loaded profile from backend:', {
              userId: profile.userId,
              email: profile.email,
              themePreference: profile.themePreference ? {
                id: profile.themePreference.id,
                code: profile.themePreference.code,
                name: profile.themePreference.name
              } : null,
              layoutDensity: profile.layoutDensity ? {
                id: profile.layoutDensity.id,
                code: profile.layoutDensity.code,
                name: profile.layoutDensity.name
              } : null,
              fontSize: profile.fontSize ? {
                id: profile.fontSize.id,
                code: profile.fontSize.code,
                name: profile.fontSize.name
              } : null
            })
            
            // Map backend response to theme state
            const themeData: Partial<ThemeState> = {
              theme: profile.themePreference || null,
              layoutDensity: profile.layoutDensity || null,
              fontSize: profile.fontSize || null,
              systemTheme,
              isLoading: false,
              error: null
            }
            
            // Apply preferences
            dispatch({ type: 'INITIALIZE_THEME', payload: themeData })
            
            // Apply themes to document
            if (profile.themePreference) {
              console.log('Applying theme from backend:', profile.themePreference.name)
              applyTheme(profile.themePreference)
            } else {
              console.log('No theme preference found in backend profile')
            }
            if (profile.layoutDensity) {
              console.log('Applying layout density from backend:', profile.layoutDensity.name)
              applyLayoutDensity(profile.layoutDensity)
            }
            if (profile.fontSize) {
              console.log('Applying font size from backend:', profile.fontSize.name)
              applyFontSize(profile.fontSize)
            }
            
            // Save to localStorage for offline access
            if (profile.themePreference || profile.layoutDensity || profile.fontSize) {
              const themeDataForStorage = {
                theme: profile.themePreference,
                layoutDensity: profile.layoutDensity,
                fontSize: profile.fontSize,
                systemTheme,
                timestamp: Date.now()
              }
              localStorage.setItem('eventlead-theme-preferences', JSON.stringify(themeDataForStorage))
            }
          } catch (error) {
            console.error('Failed to load user preferences from backend:', error)
            // Fall back to localStorage
            const storedData = loadFromLocalStorage()
            if (storedData) {
              dispatch({ type: 'INITIALIZE_THEME', payload: storedData })
              if (storedData.theme) applyTheme(storedData.theme)
              if (storedData.layoutDensity) applyLayoutDensity(storedData.layoutDensity)
              if (storedData.fontSize) applyFontSize(storedData.fontSize)
            } else {
              dispatch({ type: 'INITIALIZE_THEME', payload: { systemTheme } })
            }
          }
        } else {
          // Not authenticated - don't load preferences, use system theme
          // Don't reset here - only reset on logout (handled by separate useEffect)
          dispatch({ type: 'INITIALIZE_THEME', payload: { systemTheme } })
        }
        
      } catch (error) {
        console.error('Failed to initialize theme:', error)
        dispatch({ type: 'SET_ERROR', payload: 'Failed to initialize theme system' })
      }
    }

    initializeTheme()
  }, [isAuthenticated, user, resetTheme]) // Only include essential dependencies

  // Track previous auth state to detect logout
  const prevAuthRef = React.useRef<{ isAuthenticated: boolean; userId: number | null }>({
    isAuthenticated: isAuthenticated || false,
    userId: user?.id || null
  })

  // Listen for logout event and reset theme immediately
  useEffect(() => {
    const handleLogout = () => {
      console.log('Logout event received - resetting theme')
      resetTheme()
    }
    
    if (typeof window !== 'undefined') {
      window.addEventListener('eventlead:logout', handleLogout)
      return () => {
        window.removeEventListener('eventlead:logout', handleLogout)
      }
    }
  }, [resetTheme])

  // Reset theme when user logs out (only if they were previously logged in)
  useEffect(() => {
    const wasAuthenticated = prevAuthRef.current.isAuthenticated
    const wasLoggedIn = prevAuthRef.current.userId !== null
    const isNowLoggedOut = !isAuthenticated && !user
    
    // Only reset if user was previously logged in and now logged out
    if (wasAuthenticated && wasLoggedIn && isNowLoggedOut) {
      console.log('User logged out - resetting theme')
      resetTheme()
    }
    
    // Update ref for next comparison
    prevAuthRef.current = {
      isAuthenticated: isAuthenticated || false,
      userId: user?.id || null
    }
  }, [isAuthenticated, user, resetTheme])
  
  // Ensure theme is reset when not authenticated (for login page)
  useEffect(() => {
    if (!isAuthenticated && !user && state.theme) {
      console.log('User not authenticated - resetting theme')
      resetTheme()
    }
  }, [isAuthenticated, user]) // Only check auth state, not theme state

  // Save to localStorage when state changes
  useEffect(() => {
    if (!state.isLoading && state.theme) {
      saveToLocalStorage()
    }
  }, [state.theme, state.layoutDensity, state.fontSize])

  // Listen for system theme changes
  useEffect(() => {
    if (typeof window === 'undefined') return
    
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    
    const handleSystemThemeChange = (e: MediaQueryListEvent) => {
      const newSystemTheme = e.matches ? 'dark' : 'light'
      dispatch({ type: 'SET_SYSTEM_THEME', payload: newSystemTheme })
      
      // If user has system theme selected, reapply the theme
      if (state.theme?.code === 'system' && state.theme) {
        applyTheme(state.theme)
        console.log('System theme changed to:', newSystemTheme)
      }
    }
    
    mediaQuery.addEventListener('change', handleSystemThemeChange)
    
    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange)
    }
  }, [state.theme])


  const contextValue: ThemeContextType = {
    state,
    dispatch,
    applyTheme,
    applyLayoutDensity,
    applyFontSize,
    detectSystemTheme,
    saveToLocalStorage,
    loadFromLocalStorage,
    resetTheme
  }

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  )
}

// Hook to use theme context
export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

// Hook for theme state only
export function useThemeState(): ThemeState {
  const { state } = useTheme()
  return state
}

// Hook for theme actions only
export function useThemeActions() {
  const { dispatch, applyTheme, applyLayoutDensity, applyFontSize, detectSystemTheme, saveToLocalStorage, loadFromLocalStorage } = useTheme()
  return {
    dispatch,
    applyTheme,
    applyLayoutDensity,
    applyFontSize,
    detectSystemTheme,
    saveToLocalStorage,
    loadFromLocalStorage
  }
}
