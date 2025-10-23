/**
 * Password Reset Request Page - Story 1.15 (AC-1.15.1)
 * 
 * Features:
 * - Email input with validation
 * - Calls POST /api/auth/password-reset/request
 * - Always shows success message (security)
 * - Loading state during submission
 * - User-friendly error handling
 * - Mobile responsive design
 */

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import { Loader2, AlertCircle, CheckCircle, ArrowLeft } from 'lucide-react'
import { AuthLayout } from '../components/AuthLayout'
import { requestPasswordReset } from '../api/passwordResetApi'

interface ResetRequestFormData {
  email: string
}

export function PasswordResetRequest() {
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [requestSent, setRequestSent] = useState(false)
  const [submittedEmail, setSubmittedEmail] = useState<string>('')

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<ResetRequestFormData>({
    mode: 'onChange',
    defaultValues: {
      email: '',
    },
  })

  const onSubmit = async (data: ResetRequestFormData) => {
    setApiError(null)
    setIsLoading(true)

    try {
      // AC-1.15.1: Call password reset request endpoint
      await requestPasswordReset(data.email)
      
      // AC-1.15.1: Always show success message (security)
      setSubmittedEmail(data.email)
      setRequestSent(true)
    } catch (error) {
      // AC-1.15.4: Display user-friendly error messages
      const errorMessage = error instanceof Error ? error.message : 'Failed to send reset email. Please try again.'
      setApiError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  // AC-1.15.1: Success state - "If an account exists with this email, you'll receive password reset instructions."
  if (requestSent) {
    return (
      <AuthLayout
        title="Check Your Email"
        subtitle="Password reset instructions sent"
      >
        <div className="text-center py-6">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Password Reset Email Sent
          </h3>
          <p className="text-gray-600 mb-4">
            If an account exists with <strong>{submittedEmail}</strong>, you'll receive password reset instructions.
          </p>
          <p className="text-sm text-gray-500 mb-6">
            Please check your inbox and click the reset link. The link expires in 1 hour.
          </p>
          <Link
            to="/login"
            className="block w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors"
          >
            Return to Login
          </Link>
          
          <p className="text-sm text-gray-500 mt-6">
            Didn't receive the email? Check your spam folder or{' '}
            <button
              onClick={() => {
                setRequestSent(false)
                setSubmittedEmail('')
              }}
              className="text-teal-600 hover:text-teal-700 font-medium underline"
            >
              try again
            </button>
            .
          </p>
        </div>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout
      title="Reset Password"
      subtitle="Enter your email to receive a password reset link"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        {/* API Error Display - AC-1.15.4 */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start gap-2">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-800">{apiError}</p>
          </div>
        )}

        {/* Email Field - AC-1.15.1 */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address <span className="text-red-500">*</span>
          </label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            inputMode="email"
            autoFocus
            aria-label="Email Address"
            aria-required="true"
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? 'email-error' : undefined}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
              errors.email ? 'border-red-500' : 'border-gray-300'
            }`}
            {...register('email', {
              required: 'Email is required',
              pattern: {
                value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
                message: 'Please enter a valid email address',
              },
            })}
          />
          {errors.email && (
            <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.email.message}
            </p>
          )}
        </div>

        {/* Submit Button - AC-1.15.1 */}
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
              Sending Reset Link...
            </>
          ) : (
            'Send Reset Link'
          )}
        </button>

        {/* Back to Login Link */}
        <div className="text-center pt-4">
          <Link
            to="/login"
            className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Login
          </Link>
        </div>
      </form>
    </AuthLayout>
  )
}

