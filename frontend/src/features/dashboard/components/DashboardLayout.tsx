/**
 * Dashboard Layout - Story 1.18
 * AC-1.18.1: Top-level dashboard container
 * AC-1.18.12: Performance - loads within 3 seconds
 */

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../auth'
import { OnboardingModal } from '../../onboarding'
import { CreateEventModal, EditEventModal, DeleteEventConfirmModal } from '../../events'
import type { Event } from '../../events/types/events.types'
import { CreateFormModal, EditFormModal, DeleteFormConfirmModal, FormDetailView } from '../../forms'
import type { Form } from '../../forms/types/form.types'
import { UserMenu } from './UserMenu'
import { KPISection } from './KPISection'
import { CompanyList } from './CompanyList'
import { TeamManagementPanel } from './TeamManagementPanel'
import { Breadcrumbs } from './Breadcrumbs'
import { EmptyState } from './EmptyState'
import { getUserCompanies, getKPIData, switchCompany, setDefaultCompany } from '../api/dashboardApi'
import { buildCompanyTree, getPathToCompany, findCompanyById } from '../utils/hierarchyUtils'
import type { Company, KPIData } from '../types/dashboard.types'
import { useToastNotifications } from '../../ux'

export function DashboardLayout() {
  const { user, logout, refreshUser, isLoading: isAuthLoading } = useAuth()
  const navigate = useNavigate()
  const toast = useToastNotifications()
  
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

  // Event creation modal state - Story 2.4
  const [showCreateEventModal, setShowCreateEventModal] = useState(false)
  const [showEditEventModal, setShowEditEventModal] = useState(false)
  const [showDeleteEventModal, setShowDeleteEventModal] = useState(false)
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  
  // Form creation modal state - Story 2.8
  const [showCreateFormModal, setShowCreateFormModal] = useState(false)
  const [showEditFormModal, setShowEditFormModal] = useState(false)
  const [showDeleteFormModal, setShowDeleteFormModal] = useState(false)
  const [showFormDetailView, setShowFormDetailView] = useState(false)
  const [selectedForm, setSelectedForm] = useState<Form | null>(null)
  const [formEventId, setFormEventId] = useState<number | null>(null)

  // Load companies on mount (but only if onboarding complete)
  // On initial load, switch to default company automatically
  useEffect(() => {
    // If auth is still loading, wait
    if (isAuthLoading) return

    // Don't try to load companies if user hasn't completed onboarding
    if (user && user.onboarding_complete) {
      // On initial mount, switch to default company (shouldSwitchToDefault = true)
      // This ensures the JWT token matches the default company
      const isInitialLoad = activeCompanyId === null && companies.length === 0
      loadCompanies(isInitialLoad)
    } else if (user && !user.onboarding_complete) {
      // User needs to complete onboarding first - companies will load after
      setIsLoadingCompanies(false)
    } else if (!user) {
      // User is not authenticated - stop loading and show empty/guest state
      setIsLoadingCompanies(false)
    }
  }, [user?.onboarding_complete, isAuthLoading, user]) // Reload when auth state changes
  
  // Load KPIs when active company changes
  useEffect(() => {
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
  }, [activeCompanyId])

  // Listen for offline queue processing completion and refresh KPIs
  useEffect(() => {
    const handleQueueProcessed = () => {
      // Refresh KPIs when queue processes (new events may have been created)
      if (activeCompanyId) {
        console.log('🔄 Offline queue processed - refreshing KPIs')
        loadKPIs([activeCompanyId])
        // Also reload companies to update event counts
        loadCompanies()
      }
    }

    window.addEventListener('offlineQueueProcessed', handleQueueProcessed)
    return () => {
      window.removeEventListener('offlineQueueProcessed', handleQueueProcessed)
    }
  }, [activeCompanyId]) // eslint-disable-line react-hooks/exhaustive-deps

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
      await loadCompanies(false, null) // Don't switch, no company to preserve
  }

  const loadCompanies = async (shouldSwitchToDefault = false, preserveCompanyId: number | null = null) => {
    if (!user) return // Don't load if no user

    setIsLoadingCompanies(true)
    try {
      const data = await getUserCompanies()
      const hierarchicalCompanies = buildCompanyTree(data.companies)
      setCompanies(hierarchicalCompanies)
      setAllCompaniesFlat(data.companies)
      
      if (data.companies.length > 0) {
        let selectedCompany = null
        
        // If we should switch to the default company (e.g., on initial load or after login)
        if (shouldSwitchToDefault) {
          // Auto-select company with priority:
          // 1. User's "own company" (joined via signup)
          // 2. Primary company (explicitly set by user)
          // 3. First company as fallback
          selectedCompany = data.companies.find(c => c.joinedVia === 'signup')
          if (!selectedCompany) {
            selectedCompany = data.companies.find(c => c.isPrimaryCompany)
          }
          if (!selectedCompany) {
            selectedCompany = data.companies[0]
          }
          
          // If default company doesn't match the current active company, switch to it
          if (selectedCompany.companyId !== activeCompanyId) {
            // Switch to the default company (this will update JWT tokens)
            try {
              const response = await switchCompany(selectedCompany.companyId)
              
              // Store new tokens if provided
              if (response.access_token && response.refresh_token) {
                const { storeTokens } = await import('../../auth/utils/tokenStorage')
                const expiresIn = 24 * 60 * 60 // 24 hours in seconds
                storeTokens(response.access_token, response.refresh_token, expiresIn)
              }
              
              // Refresh user data to get updated company_id in auth context
              await refreshUser()
            } catch (error) {
              console.error('Failed to switch to default company:', error)
              // Continue anyway - we'll still select it in the UI
            }
          }
          
          setActiveCompanyId(selectedCompany.companyId)
          
          // Auto-expand selected company
          setExpandedCompanyIds([selectedCompany.companyId])
          
          // Set breadcrumb path
          const path = getPathToCompany(selectedCompany, data.companies)
          setBreadcrumbPath(path)
        } else {
          // NOT switching to default - preserve specified company or current active company if it still exists
          // This is important when reloading after a manual company switch
          // Priority: preserveCompanyId (explicit) > activeCompanyId (from state)
          // CRITICAL: If preserveCompanyId is provided, use it regardless of activeCompanyId value
          // (React state updates are async, so activeCompanyId might still be the old value)
          const companyToPreserve = preserveCompanyId !== null && preserveCompanyId !== undefined
            ? preserveCompanyId  // Explicitly provided - always use it
            : (activeCompanyId ?? null)  // Fall back to state value
          
          console.log(`[DashboardLayout] loadCompanies preservation check: preserveCompanyId=${preserveCompanyId}, activeCompanyId=${activeCompanyId}, companyToPreserve=${companyToPreserve}`)
          
          if (companyToPreserve) {
            const companyToPreserveExists = data.companies.find(c => c.companyId === companyToPreserve)
            
            if (companyToPreserveExists) {
              // Preserve the specified/active company - keep it active and ensure it's expanded
              console.log(`[DashboardLayout] Preserving active company ${companyToPreserve} after reload`)
              setActiveCompanyId(companyToPreserve)
              setExpandedCompanyIds([companyToPreserve])
              
              // Update breadcrumb path
              const path = getPathToCompany(companyToPreserveExists, data.companies)
              setBreadcrumbPath(path)
            } else {
              // Preserved company no longer exists or wasn't specified - fall back to default
              selectedCompany = data.companies.find(c => c.joinedVia === 'signup')
              if (!selectedCompany) {
                selectedCompany = data.companies.find(c => c.isPrimaryCompany)
              }
              if (!selectedCompany) {
                selectedCompany = data.companies[0]
              }
              
              setActiveCompanyId(selectedCompany.companyId)
              setExpandedCompanyIds([selectedCompany.companyId])
              
              // Set breadcrumb path
              const path = getPathToCompany(selectedCompany, data.companies)
              setBreadcrumbPath(path)
            }
          }
        }
      }
    } catch (error) {
      console.error('Failed to load companies:', error)
    } finally {
      setIsLoadingCompanies(false)
    }
  }

  const loadKPIs = async (companyIds: number[]) => {
    if (!user) return

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
    
    console.log(`[DashboardLayout] Switching to company ${companyId}...`)
    
    // Call backend to switch company context FIRST (before updating UI state)
    try {
      const response = await switchCompany(companyId)
      
      // Store new tokens if provided
      if (response.access_token && response.refresh_token) {
        const { storeTokens } = await import('../../auth/utils/tokenStorage')
        // Calculate expiry (default 24 hours)
        const expiresIn = 24 * 60 * 60 // 24 hours in seconds
        storeTokens(response.access_token, response.refresh_token, expiresIn)
      }
      
      // Update UI state immediately (optimistic update)
      // This ensures the UI reflects the switch immediately
      setActiveCompanyId(companyId)
      setExpandedCompanyIds([companyId])
      
      // Refresh user data to get updated company_id in auth context
      // This MUST complete before events can load (events depend on user.company_id)
      await refreshUser()
      console.log(`[DashboardLayout] User refreshed, company_id should now be ${companyId}`)
      
      // Update breadcrumb path - AC-1.18.5
      const company = findCompanyById(companies, companyId)
      if (company) {
        const path = getPathToCompany(company, allCompaniesFlat)
        setBreadcrumbPath(path)
      }
      
      // Reload companies to get updated data (including event counts for the new company context)
      // This is important because event counts are filtered by user access based on company role
      // CRITICAL: Pass companyId explicitly as preserveCompanyId, because React state updates are async
      // and activeCompanyId might still be the old value when loadCompanies executes
      console.log(`[DashboardLayout] Reloading companies, preserving companyId=${companyId} (activeCompanyId=${activeCompanyId})`)
      await loadCompanies(false, companyId) // Don't switch again, preserve the company we just switched to
      
      // Ensure the company is still expanded after reload
      // This MUST be set AFTER loadCompanies to ensure the expanded state persists
      setExpandedCompanyIds([companyId])
      console.log(`[DashboardLayout] Company ${companyId} should now be expanded with updated event counts`)
    } catch (error) {
      console.error('Failed to switch company:', error)
      toast.error('Failed to switch company', 'Error')
    }
  }

  // Handle setting default company (without switching)
  const handleSetDefaultCompany = async (companyId: number) => {
    try {
      await setDefaultCompany(companyId)
      toast.success('Default company updated', 'Success')
      
      // Reload companies to get updated isPrimaryCompany status
      await loadCompanies()
    } catch (error) {
      console.error('Failed to set default company:', error)
      toast.error('Failed to set default company', 'Error')
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
  const handleToggleExpand = async (companyId: number) => {
    const isCurrentlyExpanded = expandedCompanyIds.includes(companyId)
    
    if (!isCurrentlyExpanded) {
      // Expanding - if this company is not the active company, switch to it first
      // This ensures events load correctly when expanding a company (JWT context must match)
      if (companyId !== activeCompanyId) {
        // Switch to this company (this will update JWT context and expand it)
        // handleSelectCompany sets expandedCompanyIds to [companyId], so we're done
        await handleSelectCompany(companyId)
        return
      }
      // Company is active but not expanded - just expand it
      setExpandedCompanyIds(prev => [...prev, companyId])
    } else {
      // Collapsing - just remove from expanded list
      setExpandedCompanyIds(prev => prev.filter(id => id !== companyId))
    }
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

  // Handle event creation from dashboard - Story 2.4
  const handleCreateEvent = (companyId: number) => {
    // Prevent event creation when offline (required fields unavailable)
    if (!navigator.onLine) {
      toast.warning(
        'Event creation unavailable offline',
        'Event creation requires reference data (event types, statuses) that is only available when connected to the internet. Please connect to create events.'
      )
      return
    }
    
    // Switch to the company context if not already active
    if (companyId !== activeCompanyId) {
      handleSelectCompany(companyId)
    }
    setShowCreateEventModal(true)
  }

  const handleEventCreated = () => {
    setShowCreateEventModal(false)
    // Reload companies to update event counts
    loadCompanies()
    // Reload KPIs to update event counts
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
  }

  // Handle event edit from dashboard - Story 2.4
  const handleEditEvent = (event: Event) => {
    setSelectedEvent(event)
    setShowEditEventModal(true)
  }

  const handleEventUpdated = () => {
    setShowEditEventModal(false)
    setSelectedEvent(null)
    // Reload companies to update event counts
    loadCompanies()
    // Reload KPIs to update event counts
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
  }

  // Handle event delete from dashboard - Story 2.4
  const handleDeleteEvent = (event: Event) => {
    setSelectedEvent(event)
    setShowDeleteEventModal(true)
  }

  const handleEventDeleted = () => {
    setShowDeleteEventModal(false)
    setSelectedEvent(null)
    // Reload companies to update event counts
    loadCompanies()
    // Reload KPIs to update event counts
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
  }

  // Handle form creation from dashboard - Story 2.8
  const handleCreateForm = (eventId: number) => {
    if (!navigator.onLine) {
      toast.warning(
        'Form creation unavailable offline',
        'Form creation requires reference data that is only available when connected to the internet.'
      )
      return
    }
    setFormEventId(eventId)
    setShowCreateFormModal(true)
  }

  const handleFormCreated = () => {
    setShowCreateFormModal(false)
    const eventId = formEventId
    setFormEventId(null)
    // Reload companies to refresh form counts
    loadCompanies()
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
    // Dispatch custom event to refresh forms for this event
    if (eventId) {
      window.dispatchEvent(new CustomEvent('formCreated', { detail: { eventId } }))
    }
  }

  // Handle form edit from dashboard - Story 2.8
  const handleEditForm = (form: Form) => {
    setSelectedForm(form)
    setShowEditFormModal(true)
  }

  const handleFormUpdated = () => {
    setShowEditFormModal(false)
    const eventId = selectedForm?.eventId
    setSelectedForm(null)
    // Reload companies to refresh form data
    loadCompanies()
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
    // Dispatch custom event to refresh forms for this event
    if (eventId) {
      window.dispatchEvent(new CustomEvent('formUpdated', { detail: { eventId } }))
    }
  }

  // Handle form delete from dashboard - Story 2.8
  const handleDeleteForm = (form: Form) => {
    setSelectedForm(form)
    setShowDeleteFormModal(true)
  }

  // Handle form view from dashboard - Story 2.9
  const handleViewForm = (form: Form) => {
    setSelectedForm(form)
    setShowFormDetailView(true)
  }

  const handleFormDetailViewClose = () => {
    setShowFormDetailView(false)
    setSelectedForm(null)
  }

  const handleFormDeleted = () => {
    setShowDeleteFormModal(false)
    setSelectedForm(null)
    // Reload companies to update form counts
    loadCompanies()
    if (activeCompanyId) {
      loadKPIs([activeCompanyId])
    }
  }

  // Remove handleLogout since it's now handled in UserMenu

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header - AC-1.18.10: Navigation integration */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo and Navigation */}
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-3">
                <h1 className="text-2xl font-bold text-teal-600 cursor-pointer" onClick={() => navigate('/dashboard')}>
                  EventLead
                </h1>
                <span className="text-sm text-gray-500">Dashboard</span>
              </div>
              
              {/* Navigation Links */}
              <nav className="flex items-center gap-4 ml-4">
                <button
                  onClick={() => navigate('/dashboard')}
                  className="text-sm font-medium text-gray-700 hover:text-teal-600 transition-colors"
                >
                  Dashboard
                </button>
              </nav>
            </div>

            {/* User Menu */}
            {user && (
              <UserMenu user={user} />
            )}
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

        {/* Empty State: Guest Access (Unauthenticated) */}
        {!isLoadingCompanies && !user && (
          <EmptyState type="guest-access" />
        )}

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
              onSetDefaultCompany={handleSetDefaultCompany}
              onCreateEvent={handleCreateEvent}
              onEditEvent={handleEditEvent}
              onDeleteEvent={handleDeleteEvent}
              onCreateForm={handleCreateForm}
              onEditForm={handleEditForm}
              onDeleteForm={handleDeleteForm}
              onViewForm={handleViewForm}
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

      {/* Create Event Modal - Story 2.4 */}
      <CreateEventModal
        isOpen={showCreateEventModal}
        onClose={() => setShowCreateEventModal(false)}
        onSuccess={handleEventCreated}
      />

      {/* Edit Event Modal - Story 2.4 */}
      {selectedEvent && (
        <EditEventModal
          isOpen={showEditEventModal}
          onClose={() => {
            setShowEditEventModal(false)
            setSelectedEvent(null)
          }}
          onSuccess={handleEventUpdated}
          event={selectedEvent}
        />
      )}

      {/* Delete Event Modal - Story 2.4 */}
      {selectedEvent && (
        <DeleteEventConfirmModal
          isOpen={showDeleteEventModal}
          onClose={() => {
            setShowDeleteEventModal(false)
            setSelectedEvent(null)
          }}
          onConfirm={handleEventDeleted}
          event={selectedEvent}
          mode={selectedEvent.companyId !== activeCompanyId ? 'leave' : 'delete'}
          companyId={activeCompanyId || undefined}
        />
      )}

      {/* Create Form Modal - Story 2.8 */}
      {formEventId !== null && (
        <CreateFormModal
          isOpen={showCreateFormModal}
          eventId={formEventId}
          userRole={activeCompanyId ? findCompanyById(companies, activeCompanyId)?.userRole : 'Company User'}
          onClose={() => {
            setShowCreateFormModal(false)
            setFormEventId(null)
          }}
          onSuccess={handleFormCreated}
        />
      )}

      {/* Edit Form Modal - Story 2.8 */}
      {selectedForm && (
        <EditFormModal
          isOpen={showEditFormModal}
          form={selectedForm}
          onClose={() => {
            setShowEditFormModal(false)
            setSelectedForm(null)
          }}
          onSuccess={handleFormUpdated}
        />
      )}

      {/* Delete Form Modal - Story 2.8 */}
      {selectedForm && (
        <DeleteFormConfirmModal
          isOpen={showDeleteFormModal}
          form={selectedForm}
          onClose={() => {
            setShowDeleteFormModal(false)
            setSelectedForm(null)
          }}
          onConfirm={handleFormDeleted}
        />
      )}

      {/* Form Detail View Modal - Story 2.9 */}
      {showFormDetailView && selectedForm && (
        <FormDetailView
          form={selectedForm}
          onClose={handleFormDetailViewClose}
          onEdit={(form) => {
            handleFormDetailViewClose()
            handleEditForm(form)
          }}
          onDelete={(form) => {
            handleFormDetailViewClose()
            handleDeleteForm(form)
          }}
        />
      )}
    </div>
  )
}
