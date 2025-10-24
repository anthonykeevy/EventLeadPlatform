/**
 * Breadcrumbs Component - Story 1.18
 * AC-1.18.5: Breadcrumb navigation shows full path (clickable)
 */

import React from 'react'
import { ChevronRight, Home } from 'lucide-react'
import type { Company } from '../types/dashboard.types'

interface BreadcrumbsProps {
  path: Company[]
  onNavigate: (companyId: number | null) => void
}

export function Breadcrumbs({ path, onNavigate }: BreadcrumbsProps) {
  if (path.length === 0) return null

  return (
    <nav className="flex items-center gap-2 text-sm mb-4 overflow-x-auto" aria-label="Breadcrumb">
      {/* Dashboard Home */}
      <button
        onClick={() => onNavigate(null)}
        className="flex items-center gap-1 text-gray-600 hover:text-gray-900 transition-colors"
        aria-label="Dashboard"
      >
        <Home className="w-4 h-4" />
        <span>Dashboard</span>
      </button>

      {/* Path segments */}
      {path.map((company, index) => (
        <React.Fragment key={company.companyId}>
          <ChevronRight className="w-4 h-4 text-gray-400" />
          
          {index === path.length - 1 ? (
            // Last item (current) - not clickable
            <span className="font-medium text-gray-900">
              {company.companyName}
            </span>
          ) : (
            // Intermediate items - clickable
            <button
              onClick={() => onNavigate(company.companyId)}
              className="text-gray-600 hover:text-gray-900 hover:underline transition-colors"
            >
              {company.companyName}
            </button>
          )}
        </React.Fragment>
      ))}
    </nav>
  )
}



