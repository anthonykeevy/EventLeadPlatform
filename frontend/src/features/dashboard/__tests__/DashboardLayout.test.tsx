/**
 * Dashboard Layout Tests - Story 1.18
 * AC-1.18.1, AC-1.18.4, AC-1.18.12: Dashboard loading and performance
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { DashboardLayout } from '../components/DashboardLayout'
import * as dashboardApi from '../api/dashboardApi'
import * as authHooks from '../../auth'

vi.mock('../../ux/components/ToastProvider', () => ({
  useToastNotifications: () => ({
    showToast: vi.fn(),
    showSuccess: vi.fn(),
    showError: vi.fn(),
    showInfo: vi.fn(),
    showWarning: vi.fn()
  })
}))

vi.mock('../../theme/context/ThemeContext', () => ({
  useTheme: () => ({
    currentTheme: {
      id: 'default',
      name: 'Default',
      colors: { primary: '#0f766e', secondary: '#0369a1', accent: '#f59e0b' }
    },
    setTheme: vi.fn(),
    customThemes: [],
    saveCustomTheme: vi.fn(),
    deleteCustomTheme: vi.fn(),
    previewTheme: vi.fn(),
    isPreviewing: false,
    state: {
      theme: 'light',
      layoutDensity: 'comfortable',
      animationSpeed: 'normal',
      primaryColor: '#0f766e'
    },
    setGlobalState: vi.fn()
  })
}))

vi.mock('../../auth/context/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 1, email: 'test@example.com', first_name: 'Test', last_name: 'User', company_id: 1 },
    isAuthenticated: true,
    isLoading: false,
    login: vi.fn(),
    logout: vi.fn(),
    checkAuth: vi.fn()
  }),
  AuthProvider: ({ children }: { children: React.ReactNode }) => children
}))

// Mock API calls
vi.mock('../api/dashboardApi')
vi.mock('../../auth')

const mockUser = {
  user_id: 1,
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  onboarding_complete: true,
  role: 'Company Admin',
  company_id: 1
}

const mockCompanies = {
  companies: [
    {
      companyId: 1,
      companyName: 'Test Company',
      relationshipType: 'Head Office' as const,
      userRole: 'Company Admin' as const,
      parentCompanyId: null,
      childCompanies: [],
      eventCount: 5,
      formCount: 10,
      hierarchyLevel: 0,
      isPrimaryCompany: true
    }
  ]
}

const mockKPIData = {
  totalForms: 10,
  totalLeads: 50,
  activeEvents: 5,
  companyIds: [1]
}

describe('DashboardLayout', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(authHooks.useAuth).mockReturnValue({
      user: mockUser,
      isAuthenticated: true,
      isLoading: false,
      error: null,
      login: vi.fn(),
      signup: vi.fn(),
      logout: vi.fn(),
      refreshToken: vi.fn(),
      refreshUser: vi.fn()
    })
    vi.mocked(dashboardApi.getUserCompanies).mockResolvedValue(mockCompanies)
    vi.mocked(dashboardApi.getKPIData).mockResolvedValue(mockKPIData)
    vi.mocked(dashboardApi.switchCompany).mockResolvedValue({})
    vi.mocked(dashboardApi.setDefaultCompany).mockResolvedValue(undefined)
  })

  it('should render dashboard layout - AC-1.18.1', async () => {
    render(
      <BrowserRouter>
        <DashboardLayout />
      </BrowserRouter>
    )

    await waitFor(
      () => {
        expect(screen.getByText(/EventLead/i)).toBeInTheDocument()
        expect(screen.getAllByText(/Dashboard/i).length).toBeGreaterThan(0)
      },
      { timeout: 3000 }
    )
  })

  it('should load companies on mount - AC-1.18.1', async () => {
    render(
      <BrowserRouter>
        <DashboardLayout />
      </BrowserRouter>
    )

    await waitFor(
      () => {
        expect(dashboardApi.getUserCompanies).toHaveBeenCalled()
        expect(screen.getAllByText(/Test Company/i).length).toBeGreaterThan(0)
      },
      { timeout: 3000 }
    )
  })

  it('should load KPI data for active company - AC-1.18.8', async () => {
    render(
      <BrowserRouter>
        <DashboardLayout />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(dashboardApi.getKPIData).toHaveBeenCalledWith([1])
      expect(screen.getByText('Total Forms')).toBeInTheDocument()
      expect(screen.getByText('10')).toBeInTheDocument()
    })
  })

  it('should show empty state when no companies - AC-1.18.9', async () => {
    vi.mocked(dashboardApi.getUserCompanies).mockResolvedValue({ companies: [] })

    render(
      <BrowserRouter>
        <DashboardLayout />
      </BrowserRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/No Companies Yet/i)).toBeInTheDocument()
    })
  })
})




