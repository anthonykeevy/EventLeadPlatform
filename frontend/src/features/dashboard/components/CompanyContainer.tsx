/**
 * Company Container Component - Story 1.18
 * AC-1.18.3: Recursive company container
 * AC-1.18.4: Company selection and switching
 */

import React from 'react'
import { Building2, Users as UsersIcon, Settings, ChevronDown, ChevronRight } from 'lucide-react'
import type { Company } from '../types/dashboard.types'

interface CompanyContainerProps {
  company: Company
  isActive: boolean
  isExpanded: boolean
  onSelect: (companyId: number) => void
  onToggleExpand: (companyId: number) => void
  onOpenTeamPanel: (companyId: number) => void
  depth?: number
  maxDepth?: number
}

export function CompanyContainer({
  company,
  isActive,
  isExpanded,
  onSelect,
  onToggleExpand,
  onOpenTeamPanel,
  depth = 0,
  maxDepth = 5
}: CompanyContainerProps) {
  const hasChildren = company.childCompanies && company.childCompanies.length > 0
  const isAdmin = company.userRole === 'Company Admin'
  
  // Indentation based on hierarchy level
  const indentClass = depth > 0 ? `ml-${Math.min(depth * 4, 12)}` : ''
  
  // Active state styling
  const containerClass = isActive
    ? 'border-2 border-teal-500 bg-teal-50'
    : 'border border-gray-200 bg-white hover:border-gray-300'

  return (
    <div className={`mb-2 ${indentClass}`}>
      {/* Company Header - AC-1.18.4: Clickable for selection */}
      <div
        className={`${containerClass} rounded-lg transition-all duration-200 cursor-pointer`}
        onClick={() => onSelect(company.companyId)}
      >
        <div className="p-4 flex items-center justify-between">
          {/* Left: Expand toggle + Company info */}
          <div className="flex items-center gap-3 flex-1">
            {/* Expand/Collapse Toggle - AC-1.18.10 */}
            {hasChildren && (
              <button
                onClick={(e) => {
                  e.stopPropagation() // Don't trigger container selection
                  onToggleExpand(company.companyId)
                }}
                className="text-gray-500 hover:text-gray-700 p-1 rounded hover:bg-gray-100"
                aria-label={isExpanded ? 'Collapse' : 'Expand'}
              >
                {isExpanded ? (
                  <ChevronDown className="w-5 h-5" />
                ) : (
                  <ChevronRight className="w-5 h-5" />
                )}
              </button>
            )}
            
            {/* Company Icon and Name */}
            <div className="flex items-center gap-2 flex-1">
              <Building2 className={`w-5 h-5 ${isActive ? 'text-teal-600' : 'text-gray-400'}`} />
              <div>
                <h3 className={`font-semibold ${isActive ? 'text-teal-900' : 'text-gray-900'}`}>
                  {company.companyName}
                </h3>
                <div className="flex items-center gap-2 mt-1">
                  {/* Relationship Badge */}
                  <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">
                    {company.relationshipType}
                  </span>
                  {/* Role Badge */}
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    isAdmin ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                  }`}>
                    {company.userRole}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Right: Action Icons - AC-1.18.7: Team panel trigger */}
          <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
            {/* User Management Icon - AC-1.18.7 */}
            <button
              onClick={() => onOpenTeamPanel(company.companyId)}
              className="p-2 rounded hover:bg-gray-100 text-gray-600 hover:text-gray-900 transition-colors"
              aria-label="Team Management"
              title="Team Management"
            >
              <UsersIcon className="w-5 h-5" />
            </button>

            {/* Settings Icon - Only for admins */}
            {isAdmin && (
              <button
                onClick={() => {/* TODO: Story 1.16 - Company settings */}}
                className="p-2 rounded hover:bg-gray-100 text-gray-600 hover:text-gray-900 transition-colors"
                aria-label="Company Settings"
                title="Company Settings"
              >
                <Settings className="w-5 h-5" />
              </button>
            )}
            
            {/* Event/Form Count Badge */}
            {company.eventCount > 0 && (
              <span className="text-xs bg-teal-100 text-teal-700 px-2 py-1 rounded-full">
                {company.eventCount} event{company.eventCount !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Child Companies - AC-1.18.3: Recursive rendering */}
      {isExpanded && hasChildren && depth < maxDepth && (
        <div className="mt-2">
          {company.childCompanies.map(child => (
            <CompanyContainer
              key={child.companyId}
              company={child}
              isActive={false} // Only top-level selection for MVP
              isExpanded={false} // Children collapsed by default
              onSelect={onSelect}
              onToggleExpand={onToggleExpand}
              onOpenTeamPanel={onOpenTeamPanel}
              depth={depth + 1}
              maxDepth={maxDepth}
            />
          ))}
        </div>
      )}

      {/* Empty State for company with no events - AC-1.18.9 */}
      {isExpanded && !hasChildren && company.eventCount === 0 && (
        <div className="ml-4 mt-2 p-4 border-l-2 border-gray-200 text-sm text-gray-500">
          📭 No events yet. Create your first event!
        </div>
      )}
    </div>
  )
}




