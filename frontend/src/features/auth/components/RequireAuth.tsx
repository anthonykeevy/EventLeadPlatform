import React, { useEffect } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { PageLoadingSpinner } from '../../../features/ux'

interface RequireAuthProps {
  children: JSX.Element
  redirectTo?: string
}

/**
 * Wrapper for protected routes
 * Redirects to login if user is not authenticated
 */
export function RequireAuth({ children, redirectTo = '/login' }: RequireAuthProps) {
  const { user, isAuthenticated, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return <PageLoadingSpinner message="Verifying session..." />
  }

  if (!isAuthenticated || !user) {
    // Redirect to login page, saving the current location for redirect back
    return <Navigate to={redirectTo} state={{ from: location }} replace />
  }

  return children
}

