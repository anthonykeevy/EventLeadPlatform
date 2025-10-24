/**
 * Dashboard Layout - Story 1.18
 * AC-1.18.1: Top-level dashboard container
 * AC-1.18.12: Performance - loads within 3 seconds
 */

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { LogOut, User as UserIcon } from 'lucide-react'
import { useAuth } from '../../auth'
import { OnboardingModal } from '../../onboarding'
import { KPISection } from './KPISection'
import { CompanyList } from './CompanyList'
import { TeamManagementPanel } from './TeamManagementPanel'
import { Breadcrumbs } from './Breadcrumbs'
import { EmptyState } from './EmptyState'
import { getUserCompanies, getKPIData, switchCompany } from '../api/dashboardApi'
import { buildCompanyTree, getPathToCompany, findCompanyById } from '../utils/hierarchyUtils'
import type { Company, KPIData } from '../types/dashboard.types'

export function DashboardLayout() {
  const { user, logout, refreshUser } = useAuth()
  const navigate = useNavigate()
  
  // Dashboard state
  const [companies, setCompanies] = useState<Company[]>([])
  const [allCompaniesFlat, setAllCompaniesFlat] = useState<Company[]>([])
  const [activeCompanyId, setActiveCompanyId] = useState<number | null>(null)
  const [expandedCompanyIds, setExpandedCompanyIds] = useState<number[]>([])
  const [kpiData, setKpiData] = useState<KPIData | null>(null)
  const [isLoadingCompanies, setIsLoadingCompanies] = useState(true)
  const [isLoadingKPIs, setIsLoadingKPIs] = useState(false)
  const [breadcrumbPath, setBreadcrumbPath] = useState<Company[]>([])
  
  // Team panel state
  const [teamPanelCompanyId, setTeamPanelCompanyId] = useState<number | null>(null)
  const [teamPanelCompanyName, setTeamPanelCompanyName] = useState<string>('')
  const [teamPanelUserRole, setTeamPanelUserRole] = useState<'Company Admin' | 'Company User'>('Company User')
  
  // Onboarding modal state - AC-1.14.1
  const [showOnboardingModal, setShowOnboardingModal] = useState(false)

  // Load companies on mount (but only if onboarding complete)
  useEffect(() => {
    // Don't try to load companies if user hasn't completed onboarding
    if (user && user.onboarding_complete) {
      loadCompanies()
    } else if (user && !user.onboarding_complete) {
      // User needs to complete onboarding first - companies will load after
      setIsLoadingCompanies(false)
    }
  }, [user])

  // Load KPIs when active company changes
  useEffect(() => {
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
  }, [activeCompanyId])

  // Show onboarding modal if user hasn't completed onboarding - AC-1.14.1
  useEffect(() => {
    if (user && !user.onboarding_complete) {
      setShowOnboardingModal(true)
    }
  }, [user])
  
  // Handle onboarding completion - AC-1.14.8
  const handleOnboardingComplete = async () => {
    setShowOnboardingModal(false)
    
    // Refresh user object from the new JWT (contains onboarding_complete=true)
    await refreshUser()
    
    // Reload companies to show newly created company
    await loadCompanies()
  }

  const loadCompanies = async () => {
    setIsLoadingCompanies(true)
    try {
      const data = await getUserCompanies()
      const hierarchicalCompanies = buildCompanyTree(data.companies)
      setCompanies(hierarchicalCompanies)
      setAllCompaniesFlat(data.companies)
      
      // Auto-select first company (or primary company)
      if (data.companies.length > 0) {
        const primaryCompany = data.companies.find(c => c.isPrimaryCompany) || data.companies[0]
        setActiveCompanyId(primaryCompany.companyId)
        
        // Auto-expand first level
        setExpandedCompanyIds([primaryCompany.companyId])
        
        // Set breadcrumb path
        const path = getPathToCompany(primaryCompany, data.companies)
        setBreadcrumbPath(path)
      }
    } catch (error) {
      console.error('Failed to load companies:', error)
    } finally {
      setIsLoadingCompanies(false)
    }
  }

  const loadKPIs = async (companyIds: number[]) => {
    setIsLoadingKPIs(true)
    try {
      const data = await getKPIData(companyIds)
      setKpiData(data)
    } catch (error) {
      console.error('Failed to load KPIs:', error)
      // Set empty KPIs on error
      setKpiData({
        totalForms: 0,
        totalLeads: 0,
        activeEvents: 0,
        companyIds
      })
    } finally {
      setIsLoadingKPIs(false)
    }
  }

  // AC-1.18.4: Company selection and switching
  const handleSelectCompany = async (companyId: number) => {
    if (companyId === activeCompanyId) return
    
    setActiveCompanyId(companyId)
    
    // Update breadcrumb path - AC-1.18.5
    const company = findCompanyById(companies, companyId)
    if (company) {
      const path = getPathToCompany(company, allCompaniesFlat)
      setBreadcrumbPath(path)
    }
    
    // Call backend to switch company context
    try {
      await switchCompany(companyId)
    } catch (error) {
      console.error('Failed to switch company:', error)
    }
  }
  
  // Breadcrumb navigation handler - AC-1.18.5
  const handleBreadcrumbNavigate = (companyId: number | null) => {
    if (companyId === null) {
      // Navigate to dashboard home (clear selection)
      setActiveCompanyId(null)
      setBreadcrumbPath([])
    } else {
      handleSelectCompany(companyId)
    }
  }

  // AC-1.18.10: Expand/collapse containers
  const handleToggleExpand = (companyId: number) => {
    setExpandedCompanyIds(prev =>
      prev.includes(companyId)
        ? prev.filter(id => id !== companyId)
        : [...prev, companyId]
    )
  }

  // AC-1.18.7: Open team management panel
  const handleOpenTeamPanel = (companyId: number) => {
    const company = findCompanyById(companies, companyId)
    if (company) {
      setTeamPanelCompanyId(companyId)
      setTeamPanelCompanyName(company.companyName)
      setTeamPanelUserRole(company.userRole)
    }
  }

  const handleCloseTeamPanel = () => {
    setTeamPanelCompanyId(null)
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header - AC-1.18.10: Navigation integration */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-teal-600 cursor-pointer" onClick={() => navigate('/dashboard')}>
                EventLead
              </h1>
              <span className="text-sm text-gray-500">Dashboard</span>
            </div>

            {/* User Menu */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm">
                <UserIcon className="w-4 h-4 text-gray-500" />
                <span className="text-gray-700">
                  {user?.first_name} {user?.last_name}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded transition-colors"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumbs - AC-1.18.5 */}
        {breadcrumbPath.length > 0 && (
          <Breadcrumbs path={breadcrumbPath} onNavigate={handleBreadcrumbNavigate} />
        )}

        {/* KPI Section - AC-1.18.8 */}
        <KPISection kpiData={kpiData} isLoading={isLoadingKPIs} />

        {/* Empty State - AC-1.18.9: Check if onboarding required */}
        {!isLoadingCompanies && companies.length === 0 && user && !user.onboarding_complete && (
          <EmptyState type="onboarding-required" />
        )}

        {/* Empty State - AC-1.18.9: No companies (but onboarding complete) */}
        {!isLoadingCompanies && companies.length === 0 && user && user.onboarding_complete && (
          <EmptyState type="no-companies" />
        )}

        {/* Company List - AC-1.18.1 */}
        {companies.length > 0 && (
          <CompanyList
            companies={companies}
            activeCompanyId={activeCompanyId}
            expandedCompanyIds={expandedCompanyIds}
            onSelectCompany={handleSelectCompany}
            onToggleExpand={handleToggleExpand}
            onOpenTeamPanel={handleOpenTeamPanel}
            isLoading={isLoadingCompanies}
          />
        )}
      </main>

      {/* Team Management Panel - AC-1.18.7 */}
      {teamPanelCompanyId && (
        <TeamManagementPanel
          companyId={teamPanelCompanyId}
          companyName={teamPanelCompanyName}
          userRole={teamPanelUserRole}
          isOpen={teamPanelCompanyId !== null}
          onClose={handleCloseTeamPanel}
        />
      )}
      
      {/* Onboarding Modal - AC-1.14.1: Story 1.14 */}
      <OnboardingModal
        isOpen={showOnboardingModal}
        onComplete={handleOnboardingComplete}
      />
    </div>
  )
}


