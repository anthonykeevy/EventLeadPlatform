/**
 * Signup Form Component - Story 1.9 (AC-1.9.1, AC-1.9.4)
 * 
 * Features:
 * - Real-time validation with visual feedback
 * - Password strength indicator
 * - Email format validation
 * - Form submission with loading states
 * - User-friendly error messages
 * - Accessibility (ARIA labels, keyboard navigation)
 * - Mobile responsive design
 */

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import { Eye, EyeOff, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useAuthPageRedirect } from '../hooks/useAuthRedirect'
import { AuthLayout } from '../components/AuthLayout'
import { PasswordStrength } from '../components/PasswordStrength'
import type { SignupData } from '../types/auth.types'

interface SignupFormData {
  email: string
  password: string
  first_name: string
  last_name: string
}

export function SignupForm() {
  const { signup, isLoading } = useAuth()
  const [showPassword, setShowPassword] = useState(false)
  const [signupSuccess, setSignupSuccess] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  
  // Redirect if already authenticated
  useAuthPageRedirect()
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isValid, touchedFields },
  } = useForm<SignupFormData>({
    mode: 'onChange', // Real-time validation
    defaultValues: {
      email: '',
      password: '',
      first_name: '',
      last_name: '',
    },
  })
  
  const password = watch('password')
  const email = watch('email')
  
  const onSubmit = async (data: SignupFormData) => {
    setApiError(null)
    
    try {
      await signup(data)
      setSignupSuccess(true)
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Signup failed. Please try again.'
      setApiError(errorMessage)
    }
  }
  
  // AC-1.9.1: Success - Display "Check your email" message
  if (signupSuccess) {
    return (
      <AuthLayout
        title="Check Your Email"
        subtitle="We've sent you a verification link"
      >
        <div className="text-center py-6">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Account Created Successfully!
          </h3>
          <p className="text-gray-600 mb-4">
            We've sent a verification email to <strong>{email}</strong>
          </p>
          <p className="text-sm text-gray-500 mb-6">
            Please click the link in the email to verify your account before logging in.
          </p>
          <Link
            to="/login"
            className="text-teal-600 hover:text-teal-700 font-medium"
          >
            Go to Login →
          </Link>
        </div>
      </AuthLayout>
    )
  }
  
  return (
    <AuthLayout
      title="Create Account"
      subtitle="Sign up to get started with EventLead"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        {/* API Error Display - AC-1.9.5 */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start gap-2">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-800">{apiError}</p>
          </div>
        )}
        
        {/* First Name Field */}
        <div>
          <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
            First Name <span className="text-red-500">*</span>
          </label>
          <input
            id="first_name"
            type="text"
            aria-label="First Name"
            aria-required="true"
            aria-invalid={!!errors.first_name}
            aria-describedby={errors.first_name ? 'first_name-error' : undefined}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
              errors.first_name ? 'border-red-500' :
              touchedFields.first_name ? 'border-green-500' :
              'border-gray-300'
            }`}
            {...register('first_name', {
              required: 'First name is required',
              minLength: {
                value: 2,
                message: 'First name must be at least 2 characters',
              },
              maxLength: {
                value: 50,
                message: 'First name must be less than 50 characters',
              },
            })}
          />
          {errors.first_name && (
            <p id="first_name-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.first_name.message}
            </p>
          )}
        </div>
        
        {/* Last Name Field */}
        <div>
          <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
            Last Name <span className="text-red-500">*</span>
          </label>
          <input
            id="last_name"
            type="text"
            aria-label="Last Name"
            aria-required="true"
            aria-invalid={!!errors.last_name}
            aria-describedby={errors.last_name ? 'last_name-error' : undefined}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
              errors.last_name ? 'border-red-500' :
              touchedFields.last_name ? 'border-green-500' :
              'border-gray-300'
            }`}
            {...register('last_name', {
              required: 'Last name is required',
              minLength: {
                value: 2,
                message: 'Last name must be at least 2 characters',
              },
              maxLength: {
                value: 50,
                message: 'Last name must be less than 50 characters',
              },
            })}
          />
          {errors.last_name && (
            <p id="last_name-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.last_name.message}
            </p>
          )}
        </div>
        
        {/* Email Field - AC-1.9.1: Email format validation */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address <span className="text-red-500">*</span>
          </label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            inputMode="email"
            aria-label="Email Address"
            aria-required="true"
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? 'email-error' : undefined}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
              errors.email ? 'border-red-500' :
              touchedFields.email && !errors.email ? 'border-green-500' :
              'border-gray-300'
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
        
        {/* Password Field - AC-1.9.1: Password strength indicator */}
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Password <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              aria-label="Password"
              aria-required="true"
              aria-invalid={!!errors.password}
              aria-describedby={errors.password ? 'password-error' : 'password-strength'}
              className={`w-full px-4 py-2 pr-12 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
                errors.password ? 'border-red-500' :
                'border-gray-300'
              }`}
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 8,
                  message: 'Password must be at least 8 characters',
                },
                validate: {
                  hasUppercase: (value) => /[A-Z]/.test(value) || 'Must contain uppercase letter',
                  hasLowercase: (value) => /[a-z]/.test(value) || 'Must contain lowercase letter',
                  hasNumber: (value) => /[0-9]/.test(value) || 'Must contain number',
                  hasSpecial: (value) => /[^a-zA-Z0-9]/.test(value) || 'Must contain special character',
                },
              })}
            />
            {/* Password Visibility Toggle - AC-1.9.8 */}
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
          {errors.password && (
            <p id="password-error" className="mt-1 text-sm text-red-600" role="alert">
              {errors.password.message}
            </p>
          )}
          
          {/* Password Strength Indicator - AC-1.9.1 */}
          <PasswordStrength password={password} />
        </div>
        
        {/* Submit Button - AC-1.9.6: Loading states */}
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
              Creating Account...
            </>
          ) : (
            'Sign Up'
          )}
        </button>
        
        {/* Login Link */}
        <div className="text-center text-sm">
          <span className="text-gray-600">Already have an account? </span>
          <Link to="/login" className="text-teal-600 hover:text-teal-700 font-medium">
            Log In
          </Link>
        </div>
      </form>
    </AuthLayout>
  )
}



