/**
 * Dashboard API Client - Story 1.18
 * Handles dashboard data fetching and company operations
 */

import { apiClient } from '../../../lib/apiClient'
import type { Company, KPIData, CompanyUsers } from '../types/dashboard.types'

/**
 * Get all companies user belongs to (hierarchical structure)
 * AC-1.18.1: Dashboard displays all user's companies
 */
export async function getUserCompanies(): Promise<{ companies: Company[] }> {
  const response = await apiClient.get('/api/users/me/companies')
  
  // Transform snake_case from backend to camelCase for frontend
  const companies = (response.data as Record<string, unknown>[]).map((item: Record<string, unknown>) => {
    const rel = item.relationship as Record<string, unknown> | undefined
    return {
    companyId: item.company_id,
    companyName: item.company_name,
    relationshipType: rel?.relationship_type || 'Head Office',
    userRole: item.role === 'company_admin' ? 'Company Admin' : item.role === 'company_viewer' ? 'Company Viewer' : 'Company User',
    parentCompanyId: rel?.parent_company_id || null,
    childCompanies: [],
    eventCount: item.event_count ?? 0,
    formCount: 0,  // TODO: Epic 2
    hierarchyLevel: 0,
    isPrimaryCompany: item.is_primary,
    joinedVia: item.joined_via || null
  }
  })
  
  return { companies }
}

/**
 * Get KPI data for specified companies
 * AC-1.18.8: KPI components update based on selected company
 */
export async function getKPIData(companyIds: number[]): Promise<KPIData> {
  const params = companyIds.map(id => `companyIds[]=${id}`).join('&')
  const response = await apiClient.get(`/api/dashboard/kpis?${params}`)
  return response.data
}

/**
 * Get users for a specific company (team management panel)
 * AC-1.18.7: User icon opens team panel
 */
export async function getCompanyUsers(companyId: number): Promise<CompanyUsers> {
  const response = await apiClient.get(`/api/companies/${companyId}/users`)
  
  // Transform snake_case from backend to camelCase for frontend
  const data = response.data as Record<string, unknown>
  const transformed = {
    companyId: data.companyId ?? data.company_id,
    companyName: data.companyName ?? data.company_name,
    users: (data.users as Record<string, unknown>[]).map((user: Record<string, unknown>) => ({
      userId: user.userId ?? user.user_id,
      email: user.email,
      firstName: user.firstName ?? user.first_name,
      lastName: user.lastName ?? user.last_name,
      role: user.role,
      status: user.status
    }))
  }
  
  return transformed
}

/**
 * Switch active company context
 * AC-1.18.4: Company switching by clicking containers
 */
export async function switchCompany(companyId: number): Promise<{ 
  access_token?: string
  refresh_token?: string
  company?: {
    company_id: number
    company_name: string
    role: string
  }
}> {
  const response = await apiClient.post('/api/users/me/switch-company', { companyId })
  return response.data
}

/**
 * Set a company as default (primary) without switching context
 */
export async function setDefaultCompany(companyId: number): Promise<{
  company: {
    company_id: number
    company_name: string
    role: string
  }
}> {
  const response = await apiClient.post('/api/users/me/set-default-company', { companyId })
  return response.data
}

/**
 * Get events for a company (lazy load when container expands)
 * AC-1.18.12: Lazy load events/forms on expand
 */
export async function getCompanyEvents(companyId: number): Promise<unknown[]> {
  const response = await apiClient.get(`/api/companies/${companyId}/events`)
  return response.data
}
