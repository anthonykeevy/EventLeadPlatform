/**
 * Admin Dashboard API
 * Story 2.6: Admin Public Event Review Workflow
 */
import axios, { AxiosInstance } from 'axios'
import { getAccessToken } from '../../auth/utils/tokenStorage'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// Create axios instance with auth interceptor
const adminClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add request interceptor to attach access token
adminClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export interface AdminCompany {
  company_id: number
  company_name: string
  created_date: string
  total_users: number
  total_events: number
}

export interface AdminKPIs {
  total_companies: number
  total_users: number
  total_events: number
  pending_review_events: number
  approved_events: number
  rejected_events: number
}

export interface AdminEvent {
  event_id: number
  name: string
  description?: string
  company_name: string
  event_type_name: string
  event_status_name: string
  industry_name?: string
  country_name?: string
  start_date_time: string
  end_date_time?: string
  public_review_status?: string
  is_public: boolean
  created_date: string
}

export interface AdminEventsListResponse {
  events: AdminEvent[]
  total: number
  page: number
  page_size: number
}

export const adminDashboardApi = {
  /**
   * Get all companies
   */
  async getCompanies(): Promise<AdminCompany[]> {
    const response = await adminClient.get('/api/admin/dashboard/companies')
    return response.data
  },

  /**
   * Get platform KPIs
   */
  async getKPIs(): Promise<AdminKPIs> {
    const response = await adminClient.get('/api/admin/dashboard/kpis')
    return response.data
  },

  /**
   * Get all events
   */
  async getEvents(params?: {
    event_status_id?: number
    event_type_id?: number
    public_review_status?: string
    page?: number
    page_size?: number
  }): Promise<AdminEventsListResponse> {
    const response = await adminClient.get('/api/admin/dashboard/events', { params })
    return response.data
  },
}
