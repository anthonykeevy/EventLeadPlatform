import React, { useState, useCallback } from 'react'
import { Lock, LogIn, LogOut, AlertTriangle } from 'lucide-react'
import { LoginCredentials } from '../types/auth.types'

interface SessionExpiredModalProps {
  isOpen: boolean
  email?: string
  onLogin: (credentials: LoginCredentials) => Promise<void>
  onLogout: () => void
}

export function SessionExpiredModal({
  isOpen,
  email,
  onLogin,
  onLogout
}: SessionExpiredModalProps) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email) return
    
    setError(null)
    setIsSubmitting(true)

    try {
      await onLogin({ email, password })
      // Password cleared on success by parent closing modal, 
      // but good practice to reset if we stay mounted
      setPassword('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setIsSubmitting(false)
    }
  }, [email, password, onLogin])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 z-[9999] flex items-center justify-center p-4 backdrop-blur-sm">
      <div 
        className="bg-white rounded-lg shadow-2xl w-full max-w-md overflow-hidden transform transition-all scale-100"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-amber-500 text-white px-6 py-4 flex items-center gap-3">
          <AlertTriangle className="w-6 h-6" />
          <h2 className="text-xl font-semibold">Session Expired</h2>
        </div>

        <div className="p-6">
          <p className="text-gray-600 mb-6">
            Your session has expired due to inactivity or security updates. 
            Please re-enter your password to continue right where you left off.
          </p>

          {email && (
            <div className="mb-4 p-3 bg-gray-50 rounded-lg border border-gray-200 flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center font-semibold text-sm">
                {email.charAt(0).toUpperCase()}
              </div>
              <span className="text-gray-700 font-medium">{email}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="reauth-password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="password"
                  id="reauth-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-colors"
                  placeholder="Enter your password"
                  autoFocus
                  disabled={isSubmitting}
                />
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={onLogout}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-colors flex items-center justify-center gap-2"
                disabled={isSubmitting}
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg font-medium transition-colors shadow-sm flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
                disabled={isSubmitting || !password}
              >
                {isSubmitting ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <LogIn className="w-4 h-4" />
                )}
                Resume Session
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

