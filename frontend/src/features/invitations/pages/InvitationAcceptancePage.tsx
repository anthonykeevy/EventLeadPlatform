/**
 * Invitation Acceptance Page - Story 1.7 (Frontend Complete)
 * AC-1.7.1: Public endpoint to view invitation details
 * AC-1.7.3: Accept invitation (existing user - requires authentication)
 * AC-1.7.5, AC-1.7.6: New user signup with invitation
 */

import { useEffect, useState, useCallback } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Mail, Building, Shield, Calendar, CheckCircle, AlertCircle, Loader, Lock, Eye, EyeOff } from 'lucide-react'
import { useAuth } from '../../auth/context/AuthContext'
import { viewInvitation, acceptInvitation, signupWithInvitation } from '../api/invitationApi'
import type { InvitationDetails } from '../types/invitation.types'

export function InvitationAcceptancePage() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const navigate = useNavigate()
  const { user } = useAuth()

  const [invitation, setInvitation] = useState<InvitationDetails | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  
  // New user password fields
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [passwordErrors, setPasswordErrors] = useState<string[]>([])

  useEffect(() => {
    if (!token) {
      setError('No invitation token provided')
      setIsLoading(false)
      return
    }

    loadInvitation()
  }, [token])

  const loadInvitation = async () => {
    if (!token) return

    setIsLoading(true)
    setError(null)

    try {
      const data = await viewInvitation(token)
      setInvitation(data)
    } catch (err: any) {
      console.error('Failed to load invitation:', err)
      if (err.response?.status === 404) {
        setError('Invitation not found or has expired')
      } else {
        setError('Failed to load invitation details')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const validatePassword = useCallback(() => {
    const errors: string[] = []

    if (!password) {
      errors.push('Password is required')
    } else {
      if (password.length < 8) errors.push('At least 8 characters')
      if (!/[A-Z]/.test(password)) errors.push('At least one uppercase letter')
      if (!/[a-z]/.test(password)) errors.push('At least one lowercase letter')
      if (!/[0-9]/.test(password)) errors.push('At least one number')
      if (!/[^A-Za-z0-9]/.test(password)) errors.push('At least one special character')
    }

    if (password !== confirmPassword) {
      errors.push('Passwords do not match')
    }

    setPasswordErrors(errors)
    return errors.length === 0
  }, [password, confirmPassword])

  const handleNewUserSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!token || !invitation) return

    setError(null)

    if (!validatePassword()) {
      return
    }

    setIsSubmitting(true)

    try {
      const response = await signupWithInvitation(
        invitation.invitedEmail,
        invitation.invitedFirstName || '',
        invitation.invitedLastName || '',
        password,
        token
      )
      
      if (response.accessToken) {
        // Store new tokens
        localStorage.setItem('eventlead_access_token', response.accessToken)
        localStorage.setItem('eventlead_refresh_token', response.refreshToken)
        localStorage.setItem('eventlead_token_expiry', String(Math.floor(Date.now() / 1000) + 3600))
        
        setSuccess(true)
        
        // Redirect to dashboard after 2 seconds
        setTimeout(() => {
          window.location.href = '/dashboard'
        }, 2000)
      }
    } catch (err: any) {
      console.error('Failed to signup with invitation:', err)
      
      if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError('Failed to create account. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleExistingUserAccept = async () => {
    if (!token || !user) return

    setIsSubmitting(true)
    setError(null)

    try {
      const response = await acceptInvitation(token)
      
      if (response.success) {
        // Store new tokens (user now has new role and company)
        localStorage.setItem('eventlead_access_token', response.accessToken)
        localStorage.setItem('eventlead_refresh_token', response.refreshToken)
        
        setSuccess(true)
        
        // Reload page to update auth context, then redirect to dashboard
        setTimeout(() => {
          window.location.href = '/dashboard'
        }, 2000)
      }
    } catch (err: any) {
      console.error('Failed to accept invitation:', err)
      
      if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else if (err.response?.status === 400) {
        setError('This invitation cannot be accepted. It may have already been used or expired.')
      } else if (err.response?.status === 401) {
        setError('You must be logged in to accept this invitation')
      } else {
        setError('Failed to accept invitation. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full text-center">
          <Loader className="w-12 h-12 text-teal-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading invitation details...</p>
        </div>
      </div>
    )
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full text-center">
          <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            {user ? 'Invitation Accepted!' : 'Account Created!'}
          </h1>
          <p className="text-gray-600 mb-6">
            You've successfully joined {invitation?.companyName}
          </p>
          <p className="text-sm text-gray-500">
            Redirecting to dashboard...
          </p>
        </div>
      </div>
    )
  }

  if (error || !invitation) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
          <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-4 text-center">
            Invitation Error
          </h1>
          <p className="text-red-600 mb-6 text-center">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="block w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors text-center"
          >
            Return to Home
          </button>
        </div>
      </div>
    )
  }

  // Check if invitation is expired
  const isExpired = invitation.isExpired || new Date(invitation.expiresAt) < new Date()

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-6">
          <Mail className="w-16 h-16 text-teal-600 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Team Invitation
          </h1>
          <p className="text-gray-600">
            You've been invited to join a team on EventLead
          </p>
        </div>

        {/* Invitation Details */}
        <div className="space-y-3 mb-6">
          <div className="bg-gray-50 rounded-lg p-4 space-y-3">
            <div className="flex items-start gap-3">
              <Building className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-gray-600">Company</p>
                <p className="font-medium text-gray-900">{invitation.companyName}</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Shield className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-gray-600">Role</p>
                <p className="font-medium text-gray-900">{invitation.roleName}</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Mail className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-gray-600">Invited by</p>
                <p className="font-medium text-gray-900">{invitation.inviterName}</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Calendar className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-gray-600">Expires</p>
                <p className="font-medium text-gray-900">
                  {new Date(invitation.expiresAt).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>

          {/* Status Messages */}
          {isExpired && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3">
              <p className="text-sm text-red-700 text-center">
                ⚠️ This invitation has expired
              </p>
            </div>
          )}

          {invitation.status !== 'pending' && !isExpired && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <p className="text-sm text-yellow-700 text-center">
                This invitation has already been {invitation.status}
              </p>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 flex items-start gap-2">
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {/* Action Area */}
        {!isExpired && invitation.status === 'pending' && (
          <div>
            {user ? (
              // EXISTING USER - Show accept button
              <div>
                <p className="text-sm text-gray-600 mb-4 text-center">
                  Logged in as <span className="font-medium">{user.email}</span>
                </p>
                <button
                  onClick={handleExistingUserAccept}
                  disabled={isSubmitting}
                  className="w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isSubmitting ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Accepting...
                    </>
                  ) : (
                    <>
                      <CheckCircle className="w-5 h-5" />
                      Accept Invitation
                    </>
                  )}
                </button>
              </div>
            ) : (
              // NEW USER - Show password setup form
              <form onSubmit={handleNewUserSignup} className="space-y-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                  <p className="text-sm text-blue-900 font-medium">Set up your account</p>
                  <p className="text-xs text-blue-700 mt-1">
                    Create a password to accept this invitation
                  </p>
                </div>

                {/* Email (read-only) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email Address
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Mail className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      type="email"
                      value={invitation.invitedEmail}
                      disabled
                      className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-600"
                    />
                  </div>
                </div>

                {/* Password */}
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                    Create Password *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Lock className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      id="password"
                      value={password}
                      onChange={(e) => {
                        setPassword(e.target.value)
                        setPasswordErrors([])
                      }}
                      className="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                      placeholder="Enter password"
                      disabled={isSubmitting}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    >
                      {showPassword ? (
                        <EyeOff className="h-5 w-5 text-gray-400" />
                      ) : (
                        <Eye className="h-5 w-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Confirm Password */}
                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm Password *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Lock className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      id="confirmPassword"
                      value={confirmPassword}
                      onChange={(e) => {
                        setConfirmPassword(e.target.value)
                        setPasswordErrors([])
                      }}
                      className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                      placeholder="Confirm password"
                      disabled={isSubmitting}
                    />
                  </div>
                </div>

                {/* Password Requirements */}
                {passwordErrors.length > 0 && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <p className="text-sm font-medium text-red-900 mb-2">Password requirements:</p>
                    <ul className="text-xs text-red-700 space-y-1">
                      {passwordErrors.map((err, idx) => (
                        <li key={idx}>• {err}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isSubmitting || !password || !confirmPassword}
                  className="w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isSubmitting ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Creating Account...
                    </>
                  ) : (
                    <>
                      <CheckCircle className="w-5 h-5" />
                      Create Account & Join Team
                    </>
                  )}
                </button>
              </form>
            )}
          </div>
        )}

        <div className="mt-6 text-center">
          <button 
            onClick={() => navigate('/')} 
            className="text-sm text-gray-500 hover:text-gray-700"
          >
            Return to Home
          </button>
        </div>
      </div>
    </div>
  )
}
