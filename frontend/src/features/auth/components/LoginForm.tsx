/**
 * Login Form Component - Story 1.9 (AC-1.9.2, AC-1.9.4)
 * 
 * Features:
 * - Email and password authentication
 * - Real-time validation with visual feedback
 * - "Remember me" checkbox (optional)
 * - "Forgot password?" link
 * - Form submission with JWT storage
 * - Automatic navigation (onboarding vs dashboard)
 * - User-friendly error messages
 * - Accessibility (ARIA labels, keyboard navigation)
 * - Mobile responsive design
 */

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import { Eye, EyeOff, Loader2, AlertCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useAuthPageRedirect } from '../hooks/useAuthRedirect'
import { AuthLayout } from '../components/AuthLayout'
import type { LoginCredentials } from '../types/auth.types'

interface LoginFormData extends LoginCredentials {
  rememberMe?: boolean
}

export function LoginForm() {
  const { login, isLoading } = useAuth()
  const [showPassword, setShowPassword] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  
  // Redirect if already authenticated
  useAuthPageRedirect()
  
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<LoginFormData>({
    mode: 'onChange', // Real-time validation
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false,
    },
  })
  
  const onSubmit = async (data: LoginFormData) => {
    setApiError(null)
    
    try {
      // AC-1.9.2: Success - Store JWT tokens and navigate to dashboard/onboarding
      await login({ email: data.email, password: data.password })
      // Navigation is handled inside the login function in AuthContext
    } catch (error) {
      // AC-1.9.5: Display user-friendly error messages
      const errorMessage = error instanceof Error ? error.message : 'Login failed. Please try again.'
      setApiError(errorMessage)
    }
  }
  
  return (
    <AuthLayout
      title="Welcome Back"
      subtitle="Log in to your EventLead account"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        {/* API Error Display - AC-1.9.5 */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start gap-2">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-800">{apiError}</p>
          </div>
        )}
        
        {/* Email Field - AC-1.9.2 */}
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
        
        {/* Password Field - AC-1.9.2 */}
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Password <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              aria-label="Password"
              aria-required="true"
              aria-invalid={!!errors.password}
              aria-describedby={errors.password ? 'password-error' : undefined}
              className={`w-full px-4 py-2 pr-12 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors ${
                errors.password ? 'border-red-500' : 'border-gray-300'
              }`}
              {...register('password', {
                required: 'Password is required',
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
        </div>
        
        {/* Remember Me & Forgot Password - AC-1.9.2 */}
        <div className="flex items-center justify-between">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              id="rememberMe"
              type="checkbox"
              className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
              {...register('rememberMe')}
            />
            <span className="text-sm text-gray-700">Remember me</span>
          </label>
          
          <Link
            to="/reset-password"
            className="text-sm text-teal-600 hover:text-teal-700 font-medium"
          >
            Forgot password?
          </Link>
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
              Logging In...
            </>
          ) : (
            'Log In'
          )}
        </button>
        
        {/* Signup Link */}
        <div className="text-center text-sm">
          <span className="text-gray-600">Don't have an account? </span>
          <Link to="/signup" className="text-teal-600 hover:text-teal-700 font-medium">
            Sign Up
          </Link>
        </div>
      </form>
    </AuthLayout>
  )
}



