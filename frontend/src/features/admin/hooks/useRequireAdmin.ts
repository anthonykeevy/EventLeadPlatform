/**
 * useRequireAdmin Hook
 * Story 2.6: Admin Public Event Review Workflow
 * 
 * Protects routes by checking for system_admin role
 */
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../auth'

export function useRequireAdmin() {
  const { user, isAuthenticated, isLoading, refreshUser } = useAuth()
  const navigate = useNavigate()
  const [hasRefreshed, setHasRefreshed] = useState(false)

  useEffect(() => {
    if (isLoading) return

    if (!isAuthenticated) {
      navigate('/login?redirect=/admin/dashboard', { replace: true })
      return
    }

    // If user is authenticated but role is missing, try refreshing user data once
    // This handles cases where role was assigned after login (JWT token doesn't have updated role)
    if (user && !user.role && !hasRefreshed) {
      setHasRefreshed(true)
      refreshUser().catch((error) => {
        console.error('Failed to refresh user data:', error)
      })
      return
    }

    if (user && user.role !== 'system_admin') {
      navigate('/dashboard', { replace: true })
      return
    }
  }, [user, isAuthenticated, isLoading, navigate, refreshUser, hasRefreshed])

  return {
    isAdmin: user?.role === 'system_admin',
    isLoading: isLoading || (user && !user.role && !hasRefreshed), // Show loading while refreshing
  }
}
