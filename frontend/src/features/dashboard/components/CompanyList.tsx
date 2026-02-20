/**
 * Company List Component - Story 1.18
 * AC-1.18.1: Display all user's companies with hierarchy
 */

import { Building2 } from 'lucide-react'
import { CompanyContainer } from './CompanyContainer'
import type { Company } from '../types/dashboard.types'
import type { Event } from '../../events/types/events.types'
import type { Form } from '../../forms/types/form.types'

interface CompanyListProps {
  companies: Company[]
  activeCompanyId: number | null
  expandedCompanyIds: number[]
  onSelectCompany: (companyId: number) => void
  onToggleExpand: (companyId: number) => void
  onOpenTeamPanel: (companyId: number) => void
  onSetDefaultCompany?: (companyId: number) => void
  onCreateEvent?: (companyId: number) => void
  onEditEvent?: (event: Event) => void
  onDeleteEvent?: (event: Event) => void
  onCreateForm?: (eventId: number) => void
  onEditForm?: (form: Form) => void
  onDeleteForm?: (form: Form) => void
  onViewForm?: (form: Form) => void
  onUnpublishForm?: (form: Form) => void
  isLoading?: boolean
}

export function CompanyList({
  companies,
  activeCompanyId,
  expandedCompanyIds,
  onSelectCompany,
  onToggleExpand,
  onOpenTeamPanel,
  onSetDefaultCompany,
  onCreateEvent,
  onEditEvent,
  onDeleteEvent,
  onCreateForm,
  onEditForm,
  onDeleteForm,
  onViewForm,
  onUnpublishForm,
  isLoading = false
}: CompanyListProps) {
  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map(i => (
          <div key={i} className="bg-white rounded-lg shadow p-4">
            <div className="animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (companies.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <div className="text-gray-400 mb-4">
          <Building2 className="w-16 h-16 mx-auto" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          No Companies Yet
        </h3>
        <p className="text-gray-600 mb-4">
          Complete onboarding to set up your company profile.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">My Companies</h2>
      
      {companies.map(company => (
        <CompanyContainer
          key={company.companyId}
          company={company}
          isActive={company.companyId === activeCompanyId}
          isExpanded={expandedCompanyIds.includes(company.companyId)}
          onSelect={onSelectCompany}
          onToggleExpand={onToggleExpand}
          onOpenTeamPanel={onOpenTeamPanel}
          onSetDefaultCompany={onSetDefaultCompany}
          onCreateEvent={onCreateEvent}
          onEditEvent={onEditEvent}
          onDeleteEvent={onDeleteEvent}
          onCreateForm={onCreateForm}
          onEditForm={onEditForm}
          onDeleteForm={onDeleteForm}
          onViewForm={onViewForm}
          onUnpublishForm={onUnpublishForm}
          depth={0}
        />
      ))}
    </div>
  )
}

