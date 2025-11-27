/**
 * Admin Dashboard Page
 * Story 2.6: Admin Public Event Review Workflow
 * Story 2.13: Audit Trail & Compliance
 */
import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { adminDashboardApi, AdminKPIs } from '../api/adminDashboardApi'
import { AdminCompanyList } from '../components/AdminCompanyList'
import { EventManagementTab } from '../components/EventManagementTab'
import { useRequireAdmin } from '../hooks/useRequireAdmin'
import { LoadingSpinner } from '../../ux'
import { KPIModal } from '../components/KPIModal'
import { AuditTable } from '../../audit'

export const AdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'events' | 'activity'>('overview')
  const [usersKpiModalOpen, setUsersKpiModalOpen] = useState(false)
  const [companiesKpiModalOpen, setCompaniesKpiModalOpen] = useState(false)
  const [eventDateFilter, setEventDateFilter] = useState<'all' | 'past' | 'current' | 'future'>('all')
  const { isAdmin, isLoading: authLoading } = useRequireAdmin()

  // Ensure tab is set to events when date filter is applied
  React.useEffect(() => {
    if (eventDateFilter !== 'all' && activeTab !== 'events') {
      setActiveTab('events')
    }
  }, [eventDateFilter, activeTab])

  // Fetch platform KPIs
  const { data: kpis, isLoading: kpisLoading } = useQuery<AdminKPIs>({
    queryKey: ['admin', 'kpis'],
    queryFn: () => adminDashboardApi.getKPIs(),
    enabled: isAdmin,
  })

  // Modal handlers
  const handleCloseUsersModal = () => {
    setUsersKpiModalOpen(false)
  }

  const handleCloseCompaniesModal = () => {
    setCompaniesKpiModalOpen(false)
  }

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner message="Loading admin dashboard..." />
      </div>
    )
  }

  if (!isAdmin) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h2>
          <p className="text-gray-600">You do not have permission to access this page.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="w-full max-w-[98%] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="mt-2 text-gray-600">Platform-wide management and event review</p>
          </div>
          <Link
            to="/dashboard"
            className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 transition-colors"
          >
            Return to User Dashboard
          </Link>
        </div>

        {/* KPI Cards */}
        {!kpisLoading && kpis && (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
            <button
              onClick={() => setCompaniesKpiModalOpen(true)}
              className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow text-left"
            >
              <h3 className="text-sm font-medium text-gray-500">Total Companies</h3>
              <p className="text-2xl font-bold text-gray-900 mt-2">{kpis.total_companies}</p>
            </button>
            <button
              onClick={() => setUsersKpiModalOpen(true)}
              className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow text-left"
            >
              <h3 className="text-sm font-medium text-gray-500">Total Users</h3>
              <p className="text-2xl font-bold text-gray-900 mt-2">{kpis.total_users}</p>
            </button>
            {/* Events KPI - Inline breakdown */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium text-gray-500">Total Events:</span>
                <button
                  onClick={() => {
                    setEventDateFilter('all')
                    setActiveTab('events')
                  }}
                  className="text-2xl font-bold text-teal-600 hover:text-teal-700 cursor-pointer transition-colors"
                >
                  {kpis.total_events}
                </button>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-xs font-medium text-gray-500 mb-1">Past</div>
                <button
                  onClick={() => {
                    setActiveTab('events')
                    setEventDateFilter('past')
                  }}
                  className="text-xl font-bold text-gray-600 hover:opacity-80 cursor-pointer transition-opacity"
                >
                  {kpis.events_past}
                </button>
              </div>
              <div className="text-center">
                <div className="text-xs font-medium text-gray-500 mb-1">Current</div>
                <button
                  onClick={() => {
                    setActiveTab('events')
                    setEventDateFilter('current')
                  }}
                  className="text-xl font-bold text-teal-600 hover:opacity-80 cursor-pointer transition-opacity"
                >
                  {kpis.events_current}
                </button>
              </div>
              <div className="text-center">
                <div className="text-xs font-medium text-gray-500 mb-1">Future</div>
                <button
                  onClick={() => {
                    setActiveTab('events')
                    setEventDateFilter('future')
                  }}
                  className="text-xl font-bold text-blue-600 hover:opacity-80 cursor-pointer transition-opacity"
                >
                  {kpis.events_future}
                </button>
              </div>
            </div>
            </div>
            <div className="bg-yellow-50 rounded-lg shadow p-6 border border-yellow-200">
              <h3 className="text-sm font-medium text-yellow-700">Pending Review</h3>
              <p className="text-2xl font-bold text-yellow-900 mt-2">{kpis.pending_review_events}</p>
            </div>
            <div className="bg-green-50 rounded-lg shadow p-6 border border-green-200">
              <h3 className="text-sm font-medium text-green-700">Approved</h3>
              <p className="text-2xl font-bold text-green-900 mt-2">{kpis.approved_events}</p>
            </div>
            <div className="bg-red-50 rounded-lg shadow p-6 border border-red-200">
              <h3 className="text-sm font-medium text-red-700">Rejected</h3>
              <p className="text-2xl font-bold text-red-900 mt-2">{kpis.rejected_events}</p>
            </div>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('overview')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'overview'
                  ? 'border-teal-500 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('events')}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
                activeTab === 'events'
                  ? 'border-teal-500 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Event Management
              {kpis && kpis.pending_review_events > 0 && (
                <span className="bg-yellow-500 text-white text-xs font-bold rounded-full px-2 py-1">
                  {kpis.pending_review_events}
                </span>
              )}
            </button>
            <button
              onClick={() => setActiveTab('activity')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'activity'
                  ? 'border-teal-500 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Activity Log
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && <AdminCompanyList />}
        {activeTab === 'events' && (
          <EventManagementTab
            dateFilter={eventDateFilter}
            onDateFilterChange={setEventDateFilter}
          />
        )}
        {activeTab === 'activity' && (
          <div className="bg-white rounded-lg shadow">
            <AuditTable 
              title="Company Activity Log"
              showFilters={true}
              enablePagination={true}
              pageSize={25}
            />
          </div>
        )}
      </div>

      {/* Users KPI Modal */}
      {!kpisLoading && kpis && usersKpiModalOpen && (
        <KPIModal
          isOpen={usersKpiModalOpen}
          onClose={handleCloseUsersModal}
          title="Users Breakdown"
          totalLabel="Total Users"
          totalValue={kpis.total_users}
          onTotalClick={() => {
            setActiveTab('overview')
            setUsersKpiModalOpen(false)
          }}
          breakdowns={[
            {
              label: 'Inactive',
              value: kpis.users_inactive,
              color: 'text-gray-600',
              onClick: () => {
                setActiveTab('overview')
                setUsersKpiModalOpen(false)
              },
            },
            {
              label: 'Seldom',
              value: kpis.users_seldom,
              color: 'text-yellow-600',
              onClick: () => {
                setActiveTab('overview')
                setUsersKpiModalOpen(false)
              },
            },
            {
              label: 'Active',
              value: kpis.users_active,
              color: 'text-green-600',
              onClick: () => {
                setActiveTab('overview')
                setUsersKpiModalOpen(false)
              },
            },
          ]}
        />
      )}

      {/* Companies KPI Modal */}
      {!kpisLoading && kpis && companiesKpiModalOpen && (
        <KPIModal
          isOpen={companiesKpiModalOpen}
          onClose={handleCloseCompaniesModal}
          title="Companies Breakdown"
          totalLabel="Total Companies"
          totalValue={kpis.total_companies}
          onTotalClick={() => {
            setActiveTab('overview')
            setCompaniesKpiModalOpen(false)
          }}
          breakdowns={[
            {
              label: 'Inactive',
              value: kpis.companies_inactive,
              color: 'text-gray-600',
              onClick: () => {
                setActiveTab('overview')
                setCompaniesKpiModalOpen(false)
              },
            },
            {
              label: 'Seldom',
              value: kpis.companies_seldom,
              color: 'text-yellow-600',
              onClick: () => {
                setActiveTab('overview')
                setCompaniesKpiModalOpen(false)
              },
            },
            {
              label: 'Active',
              value: kpis.companies_active,
              color: 'text-green-600',
              onClick: () => {
                setActiveTab('overview')
                setCompaniesKpiModalOpen(false)
              },
            },
          ]}
        />
      )}
    </div>
  )
}
