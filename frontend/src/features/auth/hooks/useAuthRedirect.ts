/**
 * useAuthRedirect Hook - Story 1.9 (AC-1.9.7)
 * Handles authentication-based redirects
 * 
 * Features:
 * - Redirect authenticated users away from login/signup to dashboard
 * - Query parameter support for redirect after login (?redirect=/events)
 * - Automatic redirect based on onboarding status
 */

import { useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

/**
 * Redirect authenticated users away from auth pages
 * Use on login/signup pages
 */
export function useAuthPageRedirect() {
  const { isAuthenticated, user, isLoading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  
  useEffect(() => {
    if (isLoading) return
    
    if (isAuthenticated && user) {
      // Check for redirect query parameter
      const params = new URLSearchParams(location.search)
      const redirectTo = params.get('redirect')
      
      if (redirectTo) {
        navigate(redirectTo, { replace: true })
      } else {
        // Always navigate to dashboard (onboarding modal shows if incomplete)
        navigate('/dashboard', { replace: true })
      }
    }
  }, [isAuthenticated, user, isLoading, navigate, location])
}

/**
 * Require authentication for protected routes
 * Use on dashboard, profile, settings pages
 */
export function useRequireAuth() {
  const { isAuthenticated, isLoading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  
  useEffect(() => {
    if (isLoading) return
    
    if (!isAuthenticated) {
      // Save intended destination for redirect after login
      const redirectParam = location.pathname !== '/' ? `?redirect=${location.pathname}` : ''
      navigate(`/login${redirectParam}`, { replace: true })
    }
  }, [isAuthenticated, isLoading, navigate, location])
  
  return { isLoading }
}




