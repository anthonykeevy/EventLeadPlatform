/**
 * Company Container Tests - Story 1.18
 * AC-1.18.3: Recursive company container component
 */

import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { CompanyContainer } from '../components/CompanyContainer'
import type { Company } from '../types/dashboard.types'

const mockCompany: Company = {
  companyId: 1,
  companyName: 'Test Company',
  relationshipType: 'Head Office',
  userRole: 'Company Admin',
  parentCompanyId: null,
  childCompanies: [],
  eventCount: 5,
  formCount: 10,
  hierarchyLevel: 0,
  isPrimaryCompany: true
}

describe('CompanyContainer', () => {
  const mockOnSelect = vi.fn()
  const mockOnToggleExpand = vi.fn()
  const mockOnOpenTeamPanel = vi.fn()

  it('should render company name and badges', () => {
    render(
      <CompanyContainer
        company={mockCompany}
        isActive={false}
        isExpanded={false}
        onSelect={mockOnSelect}
        onToggleExpand={mockOnToggleExpand}
        onOpenTeamPanel={mockOnOpenTeamPanel}
      />
    )

    expect(screen.getByText('Test Company')).toBeInTheDocument()
    expect(screen.getByText('Head Office')).toBeInTheDocument()
    expect(screen.getByText('Company Admin')).toBeInTheDocument()
  })

  it('should call onSelect when container clicked - AC-1.18.4', () => {
    render(
      <CompanyContainer
        company={mockCompany}
        isActive={false}
        isExpanded={false}
        onSelect={mockOnSelect}
        onToggleExpand={mockOnToggleExpand}
        onOpenTeamPanel={mockOnOpenTeamPanel}
      />
    )

    const container = screen.getByText('Test Company').closest('div')?.parentElement
    fireEvent.click(container!)

    expect(mockOnSelect).toHaveBeenCalledWith(1)
  })

  it('should show user icon and settings icon for admin - AC-1.18.7', () => {
    render(
      <CompanyContainer
        company={mockCompany}
        isActive={false}
        isExpanded={false}
        onSelect={mockOnSelect}
        onToggleExpand={mockOnToggleExpand}
        onOpenTeamPanel={mockOnOpenTeamPanel}
      />
    )

    const teamButton = screen.getByLabelText('Team Management')
    const settingsButton = screen.getByLabelText('Company Settings')

    expect(teamButton).toBeInTheDocument()
    expect(settingsButton).toBeInTheDocument()
  })

  it('should not show settings icon for non-admin', () => {
    const nonAdminCompany = { ...mockCompany, userRole: 'Company User' as const }
    
    render(
      <CompanyContainer
        company={nonAdminCompany}
        isActive={false}
        isExpanded={false}
        onSelect={mockOnSelect}
        onToggleExpand={mockOnToggleExpand}
        onOpenTeamPanel={mockOnOpenTeamPanel}
      />
    )

    expect(screen.queryByLabelText('Company Settings')).not.toBeInTheDocument()
  })

  it('should render children recursively - AC-1.18.3', () => {
    const parentWithChild: Company = {
      ...mockCompany,
      childCompanies: [{
        companyId: 2,
        companyName: 'Child Company',
        relationshipType: 'Branch',
        userRole: 'Company User',
        parentCompanyId: 1,
        childCompanies: [],
        eventCount: 0,
        formCount: 0,
        hierarchyLevel: 1,
        isPrimaryCompany: false
      }]
    }

    render(
      <CompanyContainer
        company={parentWithChild}
        isActive={false}
        isExpanded={true}
        onSelect={mockOnSelect}
        onToggleExpand={mockOnToggleExpand}
        onOpenTeamPanel={mockOnOpenTeamPanel}
      />
    )

    expect(screen.getByText('Test Company')).toBeInTheDocument()
    expect(screen.getByText('Child Company')).toBeInTheDocument()
  })
})



