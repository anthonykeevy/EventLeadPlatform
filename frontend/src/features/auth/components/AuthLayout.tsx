/**
 * Auth Layout Component - Story 1.9
 * Shared layout for authentication pages (signup, login)
 * 
 * Features:
 * - Centered card layout
 * - Responsive design (mobile, tablet, desktop)
 * - Consistent branding
 */

import React from 'react'

interface AuthLayoutProps {
  children: React.ReactNode
  title: string
  subtitle?: string
}

export function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50 flex items-center justify-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-md">
        {/* Logo/Branding */}
        <div className="text-center mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold text-teal-600 mb-2">
            EventLead
          </h1>
          <p className="text-gray-600 text-sm sm:text-base">
            Multi-Tenant Event Lead Collection Platform
          </p>
        </div>
        
        {/* Auth Card */}
        <div className="bg-white rounded-lg shadow-xl p-6 sm:p-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {title}
            </h2>
            {subtitle && (
              <p className="text-gray-600 text-sm">
                {subtitle}
              </p>
            )}
          </div>
          
          {children}
        </div>
        
        {/* Footer */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            © 2025 EventLead. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  )
}




