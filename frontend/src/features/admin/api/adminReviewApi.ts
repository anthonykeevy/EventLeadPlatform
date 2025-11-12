/**
 * Admin Review API
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

export interface PendingReviewEvent {
  event_id: number
  name: string
  description?: string
  company_name: string
  creator_email: string
  created_date: string
  days_pending: number
}

export interface EventReviewDetails {
  event_id: number
  name: string
  description?: string
  company_name: string
  creator_email: string
  start_date_time: string
  end_date_time?: string
  venue_name?: string
  venue_address?: string
  city?: string
  state?: string
  country_name?: string
  event_type_name: string
  event_status_name: string
  industry_name?: string
  is_public: boolean
  public_review_status?: string
  created_date: string
}

export interface ApproveEventRequest {
  comment?: string
  public_visibility_date?: string
}

export interface RejectEventRequest {
  comment: string
}

export interface ReviewHistoryEntry {
  review_id: number
  event_id: number
  event_name: string
  reviewer_email: string
  review_date: string
  decision: string
  comments?: string
}

export interface EventReviewStatus {
  review_status?: string
  review_date?: string
  reviewer_email?: string
  review_comments?: string
  public_visibility_date?: string
}

export const adminReviewApi = {
  /**
   * Get events pending review
   */
  async getPendingReviewEvents(skip: number = 0, limit: number = 100): Promise<PendingReviewEvent[]> {
    const response = await adminClient.get('/api/admin/events/pending-review', {
      params: { skip, limit },
    })
    return response.data
  },

  /**
   * Get event review details
   */
  async getEventReviewDetails(eventId: number): Promise<EventReviewDetails> {
    const response = await adminClient.get(`/api/admin/events/${eventId}/review`)
    return response.data
  },

  /**
   * Approve event
   */
  async approveEvent(eventId: number, request: ApproveEventRequest): Promise<void> {
    await adminClient.post(`/api/admin/events/${eventId}/approve`, request)
  },

  /**
   * Reject event
   */
  async rejectEvent(eventId: number, request: RejectEventRequest): Promise<void> {
    await adminClient.post(`/api/admin/events/${eventId}/reject`, request)
  },

  /**
   * Get review history
   */
  async getReviewHistory(eventId?: number): Promise<ReviewHistoryEntry[]> {
    const url = eventId
      ? `/api/admin/events/${eventId}/review-history`
      : '/api/admin/events/review-history'
    const response = await adminClient.get(url)
    return response.data
  },

  /**
   * Get review status (for event creators)
   */
  async getEventReviewStatus(eventId: number): Promise<EventReviewStatus> {
    const response = await adminClient.get(`/api/events/${eventId}/review-status`)
    return response.data
  },
}
