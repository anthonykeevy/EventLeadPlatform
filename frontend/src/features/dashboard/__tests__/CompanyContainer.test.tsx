/**
 * Company Container Tests - Story 1.18
 * AC-1.18.3: Recursive company container component
 */

import { describe, it, expect, vi } from 'vitest'
import '@testing-library/jest-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { CompanyContainer } from '../components/CompanyContainer'
import type { Company } from '../types/dashboard.types'

const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

vi.mock('../../auth/context/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 1, email: 'test@example.com', first_name: 'Test', last_name: 'User' },
    isAuthenticated: true,
    isLoading: false,
    login: vi.fn(),
    logout: vi.fn(),
    checkAuth: vi.fn()
  }),
  AuthProvider: ({ children }: { children: React.ReactNode }) => children
}))

vi.mock('../../ux/components/ToastProvider', () => ({
  useToastNotifications: () => ({
    showToast: vi.fn(),
    showSuccess: vi.fn(),
    showError: vi.fn(),
    showInfo: vi.fn(),
    showWarning: vi.fn()
  })
}))

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
      <BrowserRouter>
        <CompanyContainer
          company={mockCompany}
          isActive={false}
          isExpanded={false}
          onSelect={mockOnSelect}
          onToggleExpand={mockOnToggleExpand}
          onOpenTeamPanel={mockOnOpenTeamPanel}
        />
      </BrowserRouter>
    )

    expect(screen.getByText('Test Company')).toBeInTheDocument()
    expect(screen.getByText('Head Office')).toBeInTheDocument()
    expect(screen.getByText('Company Admin')).toBeInTheDocument()
  })

  it('should call onSelect when container clicked - AC-1.18.4', () => {
    render(
      <BrowserRouter>
        <CompanyContainer
          company={mockCompany}
          isActive={false}
          isExpanded={false}
          onSelect={mockOnSelect}
          onToggleExpand={mockOnToggleExpand}
          onOpenTeamPanel={mockOnOpenTeamPanel}
        />
      </BrowserRouter>
    )

    const container = screen.getByText('Test Company').closest('div')?.parentElement
    fireEvent.click(container!)

    expect(mockOnSelect).toHaveBeenCalledWith(1)
  })

  it('should show user icon and settings icon for admin - AC-1.18.7', () => {
    render(
      <BrowserRouter>
        <CompanyContainer
          company={mockCompany}
          isActive={false}
          isExpanded={false}
          onSelect={mockOnSelect}
          onToggleExpand={mockOnToggleExpand}
          onOpenTeamPanel={mockOnOpenTeamPanel}
        />
      </BrowserRouter>
    )

    const teamButton = screen.getByLabelText('Team Management')
    const settingsButton = screen.getByLabelText('Company Settings')

    expect(teamButton).toBeInTheDocument()
    expect(settingsButton).toBeInTheDocument()
  })

  it('should not show settings icon for non-admin', () => {
    const nonAdminCompany = { ...mockCompany, userRole: 'Company User' as const }
    
    render(
      <BrowserRouter>
        <CompanyContainer
          company={nonAdminCompany}
          isActive={false}
          isExpanded={false}
          onSelect={mockOnSelect}
          onToggleExpand={mockOnToggleExpand}
          onOpenTeamPanel={mockOnOpenTeamPanel}
        />
      </BrowserRouter>
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
      <BrowserRouter>
        <CompanyContainer
          company={parentWithChild}
          isActive={false}
          isExpanded={true}
          onSelect={mockOnSelect}
          onToggleExpand={mockOnToggleExpand}
          onOpenTeamPanel={mockOnOpenTeamPanel}
        />
      </BrowserRouter>
    )

    expect(screen.getByText('Test Company')).toBeInTheDocument()
    expect(screen.getByText('Child Company')).toBeInTheDocument()
  })
})




