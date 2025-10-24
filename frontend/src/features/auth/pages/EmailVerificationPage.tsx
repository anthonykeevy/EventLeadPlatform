/**
 * Email Verification Page - Story 1.1 Frontend Component
 * Handles email verification via token from URL query parameter
 */

import React, { useEffect, useState } from 'react'
import { useSearchParams, Link, useNavigate } from 'react-router-dom'
import { CheckCircle, XCircle, Loader2, AlertCircle } from 'lucide-react'
import { AuthLayout } from '../components/AuthLayout'
import * as authApi from '../api/authApi'

type VerificationState = 'verifying' | 'success' | 'error' | 'invalid'

export function EmailVerificationPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [state, setState] = useState<VerificationState>('verifying')
  const [errorMessage, setErrorMessage] = useState<string>('')
  const [email, setEmail] = useState<string>('')
  
  useEffect(() => {
    const token = searchParams.get('token')
    
    if (!token) {
      setState('invalid')
      setErrorMessage('No verification token provided')
      return
    }
    
    // Call backend verification endpoint
    verifyEmail(token)
  }, [searchParams])
  
  const verifyEmail = async (token: string) => {
    try {
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      const response = await fetch(`${API_BASE_URL}/api/auth/verify-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        setState('success')
        setEmail(data.email || '')
        // Auto-redirect to login after 3 seconds
        setTimeout(() => {
          navigate('/login')
        }, 3000)
      } else {
        setState('error')
        setErrorMessage(data.detail || 'Verification failed')
      }
    } catch (error) {
      setState('error')
      setErrorMessage('Connection error. Please try again.')
    }
  }
  
  // Verifying state
  if (state === 'verifying') {
    return (
      <AuthLayout
        title="Verifying Email"
        subtitle="Please wait while we verify your email address"
      >
        <div className="text-center py-8">
          <Loader2 className="w-16 h-16 text-teal-600 mx-auto mb-4 animate-spin" />
          <p className="text-gray-600">Verifying your email address...</p>
        </div>
      </AuthLayout>
    )
  }
  
  // Success state
  if (state === 'success') {
    return (
      <AuthLayout
        title="Email Verified!"
        subtitle="Your account has been activated"
      >
        <div className="text-center py-6">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Email Successfully Verified!
          </h3>
          <p className="text-gray-600 mb-4">
            Your account is now active. You can log in to access the EventLead platform.
          </p>
          {email && (
            <p className="text-sm text-gray-500 mb-6">
              Verified email: <strong>{email}</strong>
            </p>
          )}
          <div className="space-y-3">
            <Link
              to="/login"
              className="block w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors"
            >
              Continue to Login
            </Link>
            <p className="text-sm text-gray-500">
              You will be redirected automatically in 3 seconds...
            </p>
          </div>
        </div>
      </AuthLayout>
    )
  }
  
  // Error state
  if (state === 'error' || state === 'invalid') {
    return (
      <AuthLayout
        title="Verification Failed"
        subtitle="We couldn't verify your email address"
      >
        <div className="text-center py-6">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Verification Failed
          </h3>
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-2">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-800">
                {errorMessage}
              </p>
            </div>
          </div>
          <div className="space-y-3 text-sm text-gray-600">
            <p>This verification link may have:</p>
            <ul className="list-disc list-inside text-left space-y-1">
              <li>Expired (links are valid for 24 hours)</li>
              <li>Already been used</li>
              <li>Been entered incorrectly</li>
            </ul>
          </div>
          <div className="mt-6 space-y-3">
            <Link
              to="/signup"
              className="block w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors"
            >
              Sign Up Again
            </Link>
            <Link
              to="/login"
              className="block w-full py-3 px-4 border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-lg font-medium transition-colors"
            >
              Back to Login
            </Link>
          </div>
        </div>
      </AuthLayout>
    )
  }
  
  return null
}

