/**
 * Dashboard API Client - Story 1.18
 * Handles dashboard data fetching and company operations
 */

import axios from 'axios'
import { getAccessToken } from '../../auth/utils/tokenStorage'
import type { Company, KPIData, CompanyUsers } from '../types/dashboard.types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance with auth interceptor
const dashboardClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add request interceptor to attach access token
dashboardClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/**
 * Get all companies user belongs to (hierarchical structure)
 * AC-1.18.1: Dashboard displays all user's companies
 */
export async function getUserCompanies(): Promise<{ companies: Company[] }> {
  const response = await dashboardClient.get('/api/users/me/companies')
  
  // Transform snake_case from backend to camelCase for frontend
  const companies = response.data.map((item: any) => ({
    companyId: item.company_id,
    companyName: item.company_name,
    relationshipType: item.relationship?.relationship_type || 'Head Office',
    userRole: item.role === 'company_admin' ? 'Company Admin' : 'Company User',
    parentCompanyId: item.relationship?.parent_company_id || null,
    childCompanies: [],
    eventCount: 0, // TODO: Epic 2
    formCount: 0,  // TODO: Epic 2
    hierarchyLevel: 0,
    isPrimaryCompany: item.is_primary
  }))
  
  return { companies }
}

/**
 * Get KPI data for specified companies
 * AC-1.18.8: KPI components update based on selected company
 */
export async function getKPIData(companyIds: number[]): Promise<KPIData> {
  const params = companyIds.map(id => `companyIds[]=${id}`).join('&')
  const response = await dashboardClient.get(`/api/dashboard/kpis?${params}`)
  return response.data
}

/**
 * Get users for a specific company (team management panel)
 * AC-1.18.7: User icon opens team panel
 */
export async function getCompanyUsers(companyId: number): Promise<CompanyUsers> {
  const response = await dashboardClient.get(`/api/companies/${companyId}/users`)
  
  // Transform snake_case from backend to camelCase for frontend
  const transformed = {
    companyId: response.data.companyId,
    companyName: response.data.companyName,
    users: response.data.users.map((user: any) => ({
      userId: user.userId,
      email: user.email,
      firstName: user.firstName,
      lastName: user.lastName,
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
export async function switchCompany(companyId: number): Promise<{ success: boolean; activeCompanyId: number }> {
  const response = await dashboardClient.post('/api/users/me/switch-company', { companyId })
  return response.data
}

/**
 * Get events for a company (lazy load when container expands)
 * AC-1.18.12: Lazy load events/forms on expand
 */
export async function getCompanyEvents(companyId: number): Promise<any[]> {
  const response = await dashboardClient.get(`/api/companies/${companyId}/events`)
  return response.data
}



