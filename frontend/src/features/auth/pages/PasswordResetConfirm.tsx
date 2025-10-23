/**
 * Password Reset Confirmation Page - Story 1.15 (AC-1.15.2, AC-1.15.3)
 * 
 * Features:
 * - Token validation from URL parameter
 * - New password form with confirmation
 * - Password strength indicator
 * - Real-time validation
 * - Calls POST /api/auth/password-reset/confirm
 * - Redirects to login on success
 * - Handles expired/invalid tokens
 * - Mobile responsive design
 */

import React, { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { Eye, EyeOff, Loader2, AlertCircle, CheckCircle } from 'lucide-react'
import { AuthLayout } from '../components/AuthLayout'
import { PasswordStrength } from '../components/PasswordStrength'
import { confirmPasswordReset, validatePasswordResetToken } from '../api/passwordResetApi'

interface ResetConfirmFormData {
  newPassword: string
  confirmPassword: string
}

export function PasswordResetConfirm() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [showNewPassword, setShowNewPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isValidatingToken, setIsValidatingToken] = useState(true)
  const [apiError, setApiError] = useState<string | null>(null)
  const [resetSuccess, setResetSuccess] = useState(false)
  const [tokenValid, setTokenValid] = useState(false)

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isValid },
  } = useForm<ResetConfirmFormData>({
    mode: 'onChange',
    defaultValues: {
      newPassword: '',
      confirmPassword: '',
    },
  })

  const newPassword = watch('newPassword')

  // AC-1.15.2: Validate token on page load
  useEffect(() => {
    const validateToken = async () => {
      if (!token) {
        setApiError('Invalid reset link. Please request a new password reset.')
        setTokenValid(false)
        setIsValidatingToken(false)
        return
      }

      // Validate token with backend before showing form
      setIsValidatingToken(true)
      
      try {
        const isValid = await validatePasswordResetToken(token)
        
        if (isValid) {
          setTokenValid(true)
          setApiError(null)
        } else {
          setTokenValid(false)
          setApiError('This password reset link is invalid or has expired. Please request a new one.')
        }
      } catch (error) {
        setTokenValid(false)
        setApiError('This password reset link is invalid or has expired. Please request a new one.')
      } finally {
        setIsValidatingToken(false)
      }
    }

    validateToken()
  }, [token])

  const onSubmit = async (data: ResetConfirmFormData) => {
    if (!token) {
      setApiError('Invalid reset link. Please request a new password reset.')
      return
    }

    setApiError(null)
    setIsLoading(true)

    try {
      // AC-1.15.2: Call password reset confirmation endpoint
      await confirmPasswordReset(token, data.newPassword)
      
      // AC-1.15.2: Show success and redirect to login
      setResetSuccess(true)
      
      // Redirect after 3 seconds
      setTimeout(() => {
        navigate('/login', { 
          state: { message: 'Password reset successful. You can now log in with your new password.' } 
        })
      }, 3000)
    } catch (error) {
      // AC-1.15.4: Display user-friendly error messages
      const errorMessage = error instanceof Error ? error.message : 'Failed to reset password. Please try again.'
      setApiError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  // AC-1.15.2: Success state
  if (resetSuccess) {
    return (
      <AuthLayout
        title="Password Reset Successful"
        subtitle="You can now log in with your new password"
      >
        <div className="text-center py-6">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Your Password Has Been Reset
          </h3>
          <p className="text-gray-600 mb-4">
            You can now log in with your new password.
          </p>
          <p className="text-sm text-gray-500 mb-6">
            Redirecting to login page...
          </p>
          <Link
            to="/login"
            className="inline-block py-3 px-6 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors"
          >
            Go to Login Now
          </Link>
        </div>
      </AuthLayout>
    )
  }

  // Show loading state while validating token
  if (isValidatingToken) {
    return (
      <AuthLayout
        title="Validating Reset Link"
        subtitle="Please wait..."
      >
        <div className="text-center py-12">
          <Loader2 className="w-12 h-12 text-teal-600 mx-auto mb-4 animate-spin" />
          <p className="text-gray-600">Validating your password reset link...</p>
        </div>
      </AuthLayout>
    )
  }

  // AC-1.15.2: If token invalid, show error with "Request new reset link" button
  if (!token || !tokenValid || apiError) {
    return (
      <AuthLayout
        title="Invalid Reset Link"
        subtitle="This password reset link is invalid or expired"
      >
        <div className="text-center py-6">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Invalid or Expired Reset Link
          </h3>
          <p className="text-gray-600 mb-6">
            This password reset link is invalid or has expired. Password reset links are only valid for 1 hour.
          </p>
          <Link
            to="/reset-password"
            className="inline-block w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors mb-3"
          >
            Request New Reset Link
          </Link>
          <Link
            to="/login"
            className="inline-block text-sm text-gray-600 hover:text-gray-900"
          >
            Back to Login
          </Link>
        </div>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout
      title="Set New Password"
      subtitle="Create a strong password for your account"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        {/* API Error Display - AC-1.15.4 */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start gap-2">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-800">{apiError}</p>
          </div>
        )}

        {/* New Password Field - AC-1.15.2, AC-1.15.3 */}
        <div>
          <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
            New Password <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <input
              id="newPassword"
              type={showNewPassword ? 'text' : 'password'}
              autoComplete="new-password"
              autoFocus
              aria-label="New Password"
              aria-required="true"
              aria-invalid={!!errors.newPassword}
              aria-describedby={errors.newPassword ? 'newPassword-error' : 'password-strength'}
              className={`w-full px-4 py-2 pr-12 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
                errors.newPassword ? 'border-red-500' : 'border-gray-300'
              }`}
              {...register('newPassword', {
                required: 'Password is required',
                minLength: {
                  value: 8,
                  message: 'Password must be at least 8 characters',
                },
              })}
            />
            <button
              type="button"
              onClick={() => setShowNewPassword(!showNewPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
              aria-label={showNewPassword ? 'Hide password' : 'Show password'}
            >
              {showNewPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
          {errors.newPassword && (
            <p id="newPassword-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.newPassword.message}
            </p>
          )}
          
          {/* AC-1.15.3: Password Strength Indicator */}
          <PasswordStrength password={newPassword} />
        </div>

        {/* Confirm Password Field - AC-1.15.2 */}
        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
            Confirm New Password <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <input
              id="confirmPassword"
              type={showConfirmPassword ? 'text' : 'password'}
              autoComplete="new-password"
              aria-label="Confirm New Password"
              aria-required="true"
              aria-invalid={!!errors.confirmPassword}
              aria-describedby={errors.confirmPassword ? 'confirmPassword-error' : undefined}
              className={`w-full px-4 py-2 pr-12 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
                errors.confirmPassword ? 'border-red-500' : 'border-gray-300'
              }`}
              {...register('confirmPassword', {
                required: 'Please confirm your password',
                validate: (value) => value === newPassword || 'Passwords do not match',
              })}
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
              aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
            >
              {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
          {errors.confirmPassword && (
            <p id="confirmPassword-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.confirmPassword.message}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!isValid || isLoading}
          className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-colors flex items-center justify-center gap-2 ${
            !isValid || isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-teal-600 hover:bg-teal-700'
          }`}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Resetting Password...
            </>
          ) : (
            'Reset Password'
          )}
        </button>

        {/* Back to Login Link */}
        <div className="text-center text-sm">
          <span className="text-gray-600">Remember your password? </span>
          <Link to="/login" className="text-teal-600 hover:text-teal-700 font-medium">
            Log In
          </Link>
        </div>
      </form>
    </AuthLayout>
  )
}

