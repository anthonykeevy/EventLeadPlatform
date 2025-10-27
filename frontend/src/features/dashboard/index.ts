/**
 * Dashboard Feature - Story 1.18, Story 1.16
 * Export all dashboard components and utilities
 */

// Components
export { DashboardLayout } from './components/DashboardLayout'
export { KPISection } from './components/KPISection'
export { KPICard } from './components/KPICard'
export { CompanyList } from './components/CompanyList'
export { CompanyContainer } from './components/CompanyContainer'
export { TeamManagementPanel } from './components/TeamManagementPanel'
export { Breadcrumbs } from './components/Breadcrumbs'
export { EmptyState } from './components/EmptyState'
export { InviteUserModal } from './components/InviteUserModal'
export { EditRoleModal } from './components/EditRoleModal'

// Pages
export { DashboardPage } from './pages/DashboardPage'

// API
export * as dashboardApi from './api/dashboardApi'
export * as teamApi from './api/teamApi'

// Types
export type { Company, KPIData, DashboardState, TeamMember, CompanyUsers } from './types/dashboard.types'
export type { Invitation, InviteUserRequest, InviteUserResponse } from './types/team.types'

// Utils
export * as hierarchyUtils from './utils/hierarchyUtils'

