/**
 * Admin Dashboard API
 * Story 2.6: Admin Public Event Review Workflow
 */
import { apiClient } from '../../../lib/apiClient'

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
  // Event breakdowns
  events_past: number
  events_current: number
  events_future: number
  // User breakdowns
  users_inactive: number
  users_seldom: number
  users_active: number
  // Company breakdowns
  companies_inactive: number
  companies_seldom: number
  companies_active: number
}

export interface AdminEvent {
  event_id: number
  name: string
  description?: string
  short_description?: string
  company_id: number
  company_name: string
  event_type_id: number
  event_type_name: string
  event_status_id: number
  event_status_name: string
  industry_id?: number
  industry_name?: string
  country_id?: number
  country_name?: string
  start_date_time: string
  end_date_time?: string
  timezone_identifier?: string
  venue_name?: string
  venue_address?: string
  city?: string
  state?: string
  latitude?: number
  longitude?: number
  tags?: string
  is_public: boolean
  is_shared_with_platform: boolean
  is_recurring: boolean
  organizer_company_id?: number
  organizer_company_name?: string
  organizer_contact_email?: string
  organizer_website?: string
  expected_attendees?: number
  public_review_status?: string
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
    const response = await apiClient.get('/api/admin/dashboard/companies')
    return response.data
  },

  /**
   * Get platform KPIs
   */
  async getKPIs(): Promise<AdminKPIs> {
    const response = await apiClient.get('/api/admin/dashboard/kpis')
    return response.data
  },

  /**
   * Get all events
   */
  async getEvents(params?: {
    event_status_id?: number
    event_type_id?: number
    public_review_status?: string
    date_filter?: 'past' | 'current' | 'future' | 'all'
    page?: number
    page_size?: number
  }): Promise<AdminEventsListResponse> {
    // Convert 'all' to undefined for backend
    const apiParams = { ...params }
    if (apiParams.date_filter === 'all') {
      delete apiParams.date_filter
    }
    const response = await apiClient.get('/api/admin/dashboard/events', { params: apiParams })
    return response.data
  },
}
