/**
 * Dashboard Types - Story 1.18
 * Type definitions for dashboard framework and container system
 */

export interface Company {
  companyId: number
  companyName: string
  relationshipType: 'Head Office' | 'Branch' | 'Freelancer' | 'Partner'
  userRole: 'Company Admin' | 'Company User'
  parentCompanyId: number | null
  childCompanies: Company[]
  eventCount: number
  formCount: number
  hierarchyLevel: number
  isPrimaryCompany: boolean
}

export interface KPIData {
  totalForms: number
  totalLeads: number
  activeEvents: number
  companyIds: number[]
}

export interface DashboardState {
  companies: Company[]
  activeCompanyId: number | null
  expandedCompanyIds: number[]
  selectedCompanyIds: number[]
  kpiData: KPIData | null
  isLoadingKPIs: boolean
  // Sliding window state (5-level display)
  visibleCompanyIds: number[]
  fullHierarchyPath: Company[]
}

export interface TeamMember {
  userId: number
  email: string
  firstName: string
  lastName: string
  role: string
  status: 'Active' | 'Pending' | 'Inactive'
}

export interface CompanyUsers {
  companyId: number
  companyName: string
  users: TeamMember[]
}




