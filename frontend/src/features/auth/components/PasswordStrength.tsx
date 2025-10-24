/**
 * Password Strength Indicator - Story 1.9 (AC-1.9.1)
 * Visual feedback for password strength with requirements display
 */

import React from 'react'
import { Check, X } from 'lucide-react'

interface PasswordRequirement {
  label: string
  met: boolean
}

interface PasswordStrengthProps {
  password: string
  className?: string
}

export function PasswordStrength({ password, className = '' }: PasswordStrengthProps) {
  // Check individual requirements
  const requirements: PasswordRequirement[] = [
    { label: 'At least 8 characters', met: password.length >= 8 },
    { label: 'Contains uppercase letter', met: /[A-Z]/.test(password) },
    { label: 'Contains lowercase letter', met: /[a-z]/.test(password) },
    { label: 'Contains number', met: /[0-9]/.test(password) },
    { label: 'Contains special character', met: /[^a-zA-Z0-9]/.test(password) },
  ]
  
  // Calculate strength score
  const metCount = requirements.filter(r => r.met).length
  let strength: 'weak' | 'fair' | 'strong' | 'very-strong' = 'weak'
  let strengthColor = 'bg-red-500'
  let strengthLabel = 'Weak'
  
  if (metCount >= 5) {
    strength = 'very-strong'
    strengthColor = 'bg-green-600'
    strengthLabel = 'Very Strong'
  } else if (metCount >= 4) {
    strength = 'strong'
    strengthColor = 'bg-green-500'
    strengthLabel = 'Strong'
  } else if (metCount >= 3) {
    strength = 'fair'
    strengthColor = 'bg-yellow-500'
    strengthLabel = 'Fair'
  }
  
  // Don't show indicator if no password entered
  if (password.length === 0) {
    return null
  }
  
  return (
    <div className={`mt-2 ${className}`}>
      {/* Strength bar */}
      <div className="flex items-center gap-2 mb-2">
        <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all duration-300 ${strengthColor}`}
            style={{ width: `${(metCount / requirements.length) * 100}%` }}
          />
        </div>
        <span className={`text-sm font-medium ${
          strength === 'very-strong' || strength === 'strong' ? 'text-green-600' :
          strength === 'fair' ? 'text-yellow-600' :
          'text-red-600'
        }`}>
          {strengthLabel}
        </span>
      </div>
      
      {/* Requirements checklist */}
      <div className="space-y-1">
        {requirements.map((req, index) => (
          <div
            key={index}
            className={`flex items-center gap-2 text-sm ${
              req.met ? 'text-green-600' : 'text-gray-500'
            }`}
          >
            {req.met ? (
              <Check className="w-4 h-4 flex-shrink-0" />
            ) : (
              <X className="w-4 h-4 flex-shrink-0 opacity-50" />
            )}
            <span>{req.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}



