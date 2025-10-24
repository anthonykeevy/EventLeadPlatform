/**
 * Empty State Component - Story 1.18
 * AC-1.18.9: Empty states for dashboard and companies
 */

import React from 'react'
import { Building2, FileText, Plus } from 'lucide-react'

interface EmptyStateProps {
  type: 'no-companies' | 'no-events' | 'onboarding-required'
  onAction?: () => void
}

export function EmptyState({ type, onAction }: EmptyStateProps) {
  if (type === 'no-companies') {
    return (
      <div className="bg-white rounded-lg shadow p-12 text-center">
        <Building2 className="w-20 h-20 text-gray-300 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          No Companies Yet
        </h3>
        <p className="text-gray-600 mb-6">
          Complete onboarding to set up your company profile.
        </p>
        {onAction && (
          <button
            onClick={onAction}
            className="px-6 py-3 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors"
          >
            Complete Onboarding
          </button>
        )}
      </div>
    )
  }

  if (type === 'no-events') {
    return (
      <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-3" />
        <h4 className="text-lg font-medium text-gray-700 mb-2">
          No Events Yet
        </h4>
        <p className="text-gray-500 mb-4">
          Create your first event to start collecting leads!
        </p>
        {onAction && (
          <button
            onClick={onAction}
            className="inline-flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors"
          >
            <Plus className="w-5 h-5" />
            Create Event
          </button>
        )}
      </div>
    )
  }

  if (type === 'onboarding-required') {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center">
        <div className="text-6xl mb-4">👋</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Let's Get You Set Up!
        </h3>
        <p className="text-gray-600 mb-6">
          Complete your profile and company setup to start using EventLead.
        </p>
        <p className="text-sm text-gray-500">
          The onboarding modal will appear shortly... (Story 1.14)
        </p>
      </div>
    )
  }

  return null
}



