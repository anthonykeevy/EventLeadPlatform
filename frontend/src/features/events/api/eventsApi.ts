/**
 * Events API Client for Epic 2 Story 2.4
 * Handles event management API calls
 */

import { AxiosError } from 'axios'
import {
  Event,
  EventType,
  EventStatus,
  PublicReviewStatus,
  IndustrySummary,
  CompanySummary,
  EventCreateRequest,
  EventUpdateRequest,
  EventListResponse,
  CreateEventResponse,
  UpdateEventResponse,
  DeleteEventResponse,
  EventFilters
} from '../types/events.types'
import { apiClient, formatError } from '../../../lib/apiClient'

// =====================================================================
// Transformers: Backend snake_case to Frontend camelCase
// =====================================================================

/**
 * Backend event response format (snake_case)
 */
interface BackendEvent {
  event_id: number
  name: string
  description: string | null
  short_description: string | null
  
  company_id: number
  created_by: number
  
  start_datetime: string
  end_datetime: string | null
  timezone_identifier: string | null
  
  venue_name: string | null
  venue_address: string | null
  city: string | null
  state: string | null
  country_id: number | null
  latitude: number | null
  longitude: number | null
  
  event_type_id: number
  event_type: BackendEventType | null
  industry_id: number | null
  tags: string | null
  
  is_public: boolean
  event_status_id: number
  event_status: BackendEventStatus | null
  is_recurring: boolean
  
  organizer_company_id: number | null
  organizer_contact_email: string | null
  organizer_website: string | null
  
  expected_attendees: number | null
  actual_attendees: number | null
  forms_created: number
  total_submissions: number
  
  created_date: string
  updated_date: string | null
  updated_by: number | null
}

interface BackendEventType {
  event_type_id: number
  type_code: string
  type_name: string
  type_description: string | null
  is_active: boolean
  sort_order: number
}

interface BackendEventStatus {
  event_status_id: number
  status_code: string
  status_name: string
  status_description: string | null
  status_color: string | null
  status_icon: string | null
  is_active: boolean
  sort_order: number
}

/**
 * Transform backend event response to frontend format
 * Handles both snake_case (from Pydantic field names) and PascalCase (from aliases)
 */
function transformEvent(backendEvent: Record<string, unknown>): Event {
  // Handle both snake_case (from Pydantic field names) and PascalCase (from aliases)
  // Backend may serialize using aliases (PascalCase) or field names (snake_case)
  return {
    eventId: backendEvent.event_id ?? backendEvent.EventID ?? 0,
    name: backendEvent.name ?? backendEvent.Name ?? '',
    description: backendEvent.description ?? backendEvent.Description ?? null,
    shortDescription: backendEvent.short_description ?? backendEvent.ShortDescription ?? null,
    
    companyId: backendEvent.company_id ?? backendEvent.CompanyID ?? 0,
    createdBy: backendEvent.created_by ?? backendEvent.CreatedBy ?? 0,
    
    startDateTime: backendEvent.start_datetime ?? backendEvent.StartDateTime ?? '',
    endDateTime: backendEvent.end_datetime ?? backendEvent.EndDateTime ?? null,
    timezoneIdentifier: backendEvent.timezone_identifier ?? backendEvent.TimezoneIdentifier ?? null,
    
    venueName: backendEvent.venue_name ?? backendEvent.VenueName ?? null,
    venueAddress: backendEvent.venue_address ?? backendEvent.VenueAddress ?? null,
    city: backendEvent.city ?? backendEvent.City ?? null,
    state: backendEvent.state ?? backendEvent.State ?? null,
    countryId: backendEvent.country_id ?? backendEvent.CountryID ?? null,
    latitude: backendEvent.latitude ?? backendEvent.Latitude ?? null,
    longitude: backendEvent.longitude ?? backendEvent.Longitude ?? null,
    
    eventTypeId: backendEvent.event_type_id ?? backendEvent.EventTypeID ?? 0,
    eventType: (backendEvent.event_type ?? backendEvent.EventType) ? transformEventType(backendEvent.event_type ?? backendEvent.EventType) : null,
    industryId: backendEvent.industry_id ?? backendEvent.IndustryID ?? null,
    industry: (backendEvent.industry ?? backendEvent.Industry) ? transformIndustry(backendEvent.industry ?? backendEvent.Industry) : null,
    tags: backendEvent.tags ?? backendEvent.Tags ?? null,
    
    isPublic: backendEvent.is_public ?? backendEvent.IsPublic ?? false,
    isSharedWithPlatform: backendEvent.is_shared_with_platform ?? backendEvent.IsSharedWithPlatform ?? false,
    isPublicReviewRequired: backendEvent.is_public_review_required ?? backendEvent.IsPublicReviewRequired ?? false,
    publicReviewStatusId: backendEvent.public_review_status_id ?? backendEvent.PublicReviewStatusID ?? null,
    publicReviewStatus: (backendEvent.public_review_status ?? backendEvent.PublicReviewStatus) ? transformPublicReviewStatus(backendEvent.public_review_status ?? backendEvent.PublicReviewStatus) : null,
    publicReviewDate: backendEvent.public_review_date ?? backendEvent.PublicReviewDate ?? null,
    publicReviewBy: backendEvent.public_review_by ?? backendEvent.PublicReviewBy ?? null,
    publicReviewComments: backendEvent.public_review_comments ?? backendEvent.PublicReviewComments ?? null,
    publicVisibilityDate: backendEvent.public_visibility_date ?? backendEvent.PublicVisibilityDate ?? null,
    eventStatusId: backendEvent.event_status_id ?? backendEvent.EventStatusID ?? 1,
    eventStatus: (backendEvent.event_status ?? backendEvent.EventStatus) ? transformEventStatus(backendEvent.event_status ?? backendEvent.EventStatus) : null,
    isRecurring: backendEvent.is_recurring ?? backendEvent.IsRecurring ?? false,
    
    organizerCompanyId: backendEvent.organizer_company_id ?? backendEvent.OrganizerCompanyID ?? null,
    organizerContactEmail: backendEvent.organizer_contact_email ?? backendEvent.OrganizerContactEmail ?? null,
    organizerWebsite: backendEvent.organizer_website ?? backendEvent.OrganizerWebsite ?? null,
    organizerCompany: (backendEvent.organizer_company ?? backendEvent.OrganizerCompany) ? transformCompanySummary(backendEvent.organizer_company ?? backendEvent.OrganizerCompany) : null,
    ownerCompany: (backendEvent.owner_company ?? backendEvent.OwnerCompany) ? transformCompanySummary(backendEvent.owner_company ?? backendEvent.OwnerCompany) : null,
    
    expectedAttendees: backendEvent.expected_attendees ?? backendEvent.ExpectedAttendees ?? null,
    actualAttendees: backendEvent.actual_attendees ?? backendEvent.ActualAttendees ?? null,
    formsCreated: backendEvent.forms_created ?? backendEvent.FormsCreated ?? 0,
    totalSubmissions: backendEvent.total_submissions ?? backendEvent.TotalSubmissions ?? 0,
    
    createdDate: backendEvent.created_date ?? backendEvent.CreatedDate ?? '',
    updatedDate: backendEvent.updated_date ?? backendEvent.UpdatedDate ?? null,
    updatedBy: backendEvent.updated_by ?? backendEvent.UpdatedBy ?? null,
    
    // User role for this event
    userRole: backendEvent.user_role ? {
      role_code: backendEvent.user_role.role_code ?? null,
      role_name: backendEvent.user_role.role_name ?? null,
      has_edit_event: backendEvent.user_role.has_edit_event ?? false,
      has_delete_event: backendEvent.user_role.has_delete_event ?? false,
      has_manage_participants: backendEvent.user_role.has_manage_participants ?? false,
      has_view_event: backendEvent.user_role.has_view_event ?? true,
      is_legacy: backendEvent.user_role.is_legacy ?? false
    } : null
  }
}

function transformEventType(backendType: Record<string, unknown>): EventType {
  // Handle both snake_case (from Pydantic field names) and PascalCase (from aliases)
  // Pydantic serializes using field names by default, not aliases
  return {
    eventTypeId: backendType.event_type_id ?? backendType.EventTypeID ?? 0,
    typeCode: backendType.type_code ?? backendType.TypeCode ?? '',
    typeName: backendType.type_name ?? backendType.TypeName ?? '',
    typeDescription: backendType.type_description ?? backendType.TypeDescription ?? null,
    isActive: backendType.is_active ?? backendType.IsActive ?? false,
    sortOrder: backendType.sort_order ?? backendType.SortOrder ?? 0
  }
}

function transformEventStatus(backendStatus: Record<string, unknown>): EventStatus {
  // Handle both snake_case (from Pydantic field names) and PascalCase (from aliases)
  // Pydantic serializes using field names by default, not aliases
  return {
    eventStatusId: backendStatus.event_status_id ?? backendStatus.EventStatusID ?? 0,
    statusCode: backendStatus.status_code ?? backendStatus.StatusCode ?? '',
    statusName: backendStatus.status_name ?? backendStatus.StatusName ?? '',
    statusDescription: backendStatus.status_description ?? backendStatus.StatusDescription ?? null,
    statusColor: backendStatus.status_color ?? backendStatus.StatusColor ?? null,
    statusIcon: backendStatus.status_icon ?? backendStatus.StatusIcon ?? null,
    isActive: backendStatus.is_active ?? backendStatus.IsActive ?? false,
    sortOrder: backendStatus.sort_order ?? backendStatus.SortOrder ?? 0
  }
}

function transformPublicReviewStatus(backendStatus: Record<string, unknown>): PublicReviewStatus {
  // Handle both snake_case (from Pydantic field names) and PascalCase (from aliases)
  return {
    publicReviewStatusId: backendStatus.public_review_status_id ?? backendStatus.PublicReviewStatusID ?? 0,
    statusCode: backendStatus.status_code ?? backendStatus.StatusCode ?? '',
    statusName: backendStatus.status_name ?? backendStatus.StatusName ?? '',
    statusDescription: backendStatus.status_description ?? backendStatus.StatusDescription ?? null,
    statusColor: backendStatus.status_color ?? backendStatus.StatusColor ?? null,
    statusIcon: backendStatus.status_icon ?? backendStatus.StatusIcon ?? null,
    isActive: backendStatus.is_active ?? backendStatus.IsActive ?? false,
    sortOrder: backendStatus.sort_order ?? backendStatus.SortOrder ?? 0
  }
}

function transformIndustry(backendIndustry: Record<string, unknown>): IndustrySummary {
  return {
    industryId: backendIndustry.industry_id ?? backendIndustry.IndustryID ?? 0,
    industryCode: backendIndustry.industry_code ?? backendIndustry.IndustryCode ?? '',
    industryName: backendIndustry.industry_name ?? backendIndustry.IndustryName ?? '',
    description: backendIndustry.description ?? backendIndustry.Description ?? null,
    isActive: backendIndustry.is_active ?? backendIndustry.IsActive ?? false,
    sortOrder: backendIndustry.sort_order ?? backendIndustry.SortOrder ?? 0
  }
}

function transformCompanySummary(backendCompany: Record<string, unknown>): CompanySummary {
  return {
    companyId: backendCompany.company_id ?? backendCompany.CompanyID ?? 0,
    companyName: backendCompany.company_name ?? backendCompany.CompanyName ?? '',
    legalEntityName: backendCompany.legal_entity_name ?? backendCompany.LegalEntityName ?? null,
    abn: backendCompany.abn ?? backendCompany.ABN ?? null,
    acn: backendCompany.acn ?? backendCompany.ACN ?? null,
    website: backendCompany.website ?? backendCompany.Website ?? null,
    countryId: backendCompany.country_id ?? backendCompany.CountryID ?? null
  }
}

// =====================================================================
// Reference Data API Calls
// =====================================================================

/**
 * Get all active event types for dropdown selections
 */
export async function getEventTypes(): Promise<EventType[]> {
  try {
    console.log('getEventTypes - Calling API endpoint: /api/events/reference/types')
    const response = await apiClient.get<BackendEventType[]>('/api/events/reference/types')
    console.log('getEventTypes - API response:', response.data)
    const transformed = response.data.map(transformEventType)
    console.log('getEventTypes - Transformed data:', transformed)
    return transformed
  } catch (error) {
    console.error('getEventTypes - Error:', error)
    throw formatError(error)
  }
}

/**
 * Get all active event statuses for dropdown selections
 */
export async function getEventStatuses(): Promise<EventStatus[]> {
  try {
    console.log('getEventStatuses - Calling API endpoint: /api/events/reference/statuses')
    const response = await apiClient.get<Record<string, unknown>[]>('/api/events/reference/statuses')
    console.log('getEventStatuses - API response:', response.data)
    const transformed = response.data.map(transformEventStatus)
    console.log('getEventStatuses - Transformed data:', transformed)
    return transformed
  } catch (error) {
    console.error('getEventStatuses - Error:', error)
    throw formatError(error)
  }
}

/**
 * Search events visible to the user's company network (includes platform-approved events)
 */
export async function searchPublicEvents(searchTerm?: string, limit: number = 20): Promise<EventListResponse> {
  try {
    const params = new URLSearchParams()
    if (searchTerm) params.append('q', searchTerm)
    params.append('limit', limit.toString())
    
    // Authenticated endpoint - includes company network visibility plus platform-approved events
    const response = await apiClient.get<{
      events: Record<string, unknown>[]  // Handle both PascalCase and snake_case from backend
      total: number
      page: number
      page_size: number
    }>(`/api/events/company-network/search?${params.toString()}`)
    
    console.log('searchPublicEvents - Raw response:', response.data)
    console.log('searchPublicEvents - Events array:', response.data.events)
    
    const transformed = response.data.events.map(event => {
      console.log('Transforming event:', event)
      const transformedEvent = transformEvent(event)
      console.log('Transformed event:', transformedEvent)
      return transformedEvent
    })
    
    return {
      events: transformed,
      total: response.data.total,
      page: response.data.page,
      pageSize: response.data.page_size
    }
  } catch (error) {
    console.error('Error in searchPublicEvents:', error)
    throw formatError(error)
  }
}

/**
 * Create participant relationship when user selects existing public event
 * Creates EventCompany relationship with event_participant role
 */
export async function participateInEvent(eventId: number): Promise<{ success: boolean; message: string; event_company_id: number; alreadyExists: boolean }> {
  try {
    const response = await apiClient.post<{
      success: boolean
      message: string
      event_company_id: number
      event_id: number
      company_id: number
      role: string
      already_exists?: boolean
    }>(`/api/events/${eventId}/participate`)
    
    return {
      success: response.data.success,
      message: response.data.message,
      event_company_id: response.data.event_company_id,
      alreadyExists: response.data.already_exists ?? false
    }
  } catch (error) {
    console.error('Error creating participant relationship:', error)
    throw formatError(error)
  }
}

/**
 * Share an event with another company (e.g., Agency)
 */
export async function shareEvent(eventId: number, companyId: number, roleCode: string = 'agency_form_builder'): Promise<{ success: boolean; message: string }> {
  try {
    const response = await apiClient.post<{
      success: boolean
      message: string
      event_company_id: number
      event_id: number
      company_id: number
      role: string
      already_exists?: boolean
    }>(`/api/events/${eventId}/share`, {
      company_id: companyId,
      role_code: roleCode
    })
    
    return {
      success: response.data.success,
      message: response.data.message
    }
  } catch (error) {
    console.error('Error sharing event:', error)
    throw formatError(error)
  }
}

/**
 * Share an event with a user via email
 */
export async function shareEventByEmail(eventId: number, email: string, roleCode: string = 'agency_form_builder'): Promise<{ success: boolean; message: string; alreadyExists?: boolean }> {
  try {
    const response = await apiClient.post<{
      success: boolean
      message: string
      event_company_id: number
      event_id: number
      company_id: number
      role: string
      already_exists?: boolean
    }>(`/api/events/${eventId}/share-by-email`, {
      email: email,
      role_code: roleCode
    })
    
    return {
      success: response.data.success,
      message: response.data.message,
      alreadyExists: response.data.already_exists
    }
  } catch (error) {
    console.error('Error sharing event by email:', error)
    throw formatError(error)
  }
}


/**
 * Get all companies for an event
 */
export async function getEventCompanies(eventId: number): Promise<{
  success: boolean
  companies: Array<{
    event_company_id: number
    company_id: number
    company_name: string
    role_code: string
    role_name: string
    is_active: boolean
    forms_created: number
    first_used_date: string | null
    last_used_date: string | null
  }>
  total: number
}> {
  try {
    const response = await apiClient.get<{
      success: boolean
      event_id: number
      companies: Array<{
        event_company_id: number
        company_id: number
        company_name: string
        role_code: string
        role_name: string
        is_active: boolean
        forms_created: number
        first_used_date: string | null
        last_used_date: string | null
      }>
      total: number
    }>(`/api/events/${eventId}/companies`)
    
    return response.data
  } catch (error) {
    console.error('Error getting event companies:', error)
    throw formatError(error)
  }
}

/**
 * Get current user's role for an event
 */
export async function getMyRoleForEvent(eventId: number): Promise<{
  success: boolean
  role_code: string
  role_name: string
  has_edit_event: boolean
  has_delete_event: boolean
  has_manage_participants: boolean
  has_view_event: boolean
  is_legacy: boolean
}> {
  try {
    const response = await apiClient.get<{
      success: boolean
      role_code: string
      role_name: string
      has_edit_event: boolean
      has_delete_event: boolean
      has_manage_participants: boolean
      has_view_event: boolean
      is_legacy: boolean
    }>(`/api/events/${eventId}/my-role`)
    
    return response.data
  } catch (error) {
    console.error('Error getting user role for event:', error)
    throw formatError(error)
  }
}

/**
 * Smart Field Inference APIs
 */

/**
 * Get country from timezone identifier
 */
export async function getCountryFromTimezone(timezoneIdentifier: string): Promise<{ country_id: number; country_code: string; country_name: string } | null> {
  try {
    const response = await apiClient.get<{
      success: boolean
      timezone_identifier: string
      country_id: number
      country_code: string
      country_name: string
      timezone_display_name: string
    }>(`/api/events/timezones/country?timezone_identifier=${encodeURIComponent(timezoneIdentifier)}`)
    
    if (response.data.success) {
      return {
        country_id: response.data.country_id,
        country_code: response.data.country_code,
        country_name: response.data.country_name
      }
    }
    return null
  } catch (error) {
    // 404 is expected when timezone doesn't have country mapping - this is fine
    // Only log as debug, not as error
    if ((error as AxiosError).response?.status === 404) {
      console.debug(`Country not found for timezone: ${timezoneIdentifier} (this is expected if timezone doesn't have a country mapping)`)
      return null
    }
    
    // For other errors, log as debug since this is optional inference
    console.debug('Could not get country from timezone:', timezoneIdentifier, error)
    return null
  }
}

/**
 * Get user profile with location for smart field inference
 */
export async function getUserProfileForInference(): Promise<{ timezone_identifier: string; country_id: number | null; country_code: string | null; country_name: string | null } | null> {
  try {
    const response = await apiClient.get<{
      success: boolean
      user_id: number
      timezone_identifier: string
      country_id: number | null
      country_code: string | null
      country_name: string | null
    }>('/api/events/inference/user-profile')
    
    if (response.data.success) {
      return {
        timezone_identifier: response.data.timezone_identifier,
        country_id: response.data.country_id,
        country_code: response.data.country_code,
        country_name: response.data.country_name
      }
    }
    return null
  } catch (error) {
    console.error('Error getting user profile for inference:', error)
    return null
  }
}

/**
 * Get company profile with billing city for smart field inference
 */
export async function getCompanyProfileForInference(companyId: number): Promise<{ billing_city: string | null; billing_state: string | null; country_id: number | null } | null> {
  try {
    const response = await apiClient.get<{
      success: boolean
      company_id: number
      company_name: string
      country_id: number | null
      billing_city: string | null
      billing_state: string | null
      billing_country_id: number | null
    }>(`/api/events/inference/company-profile/${companyId}`)
    
    if (response.data.success) {
      return {
        billing_city: response.data.billing_city,
        billing_state: response.data.billing_state,
        country_id: response.data.country_id
      }
    }
    return null
  } catch (error) {
    console.error('Error getting company profile for inference:', error)
    return null
  }
}

/**
 * Get recent event cities for smart field inference
 */
export async function getRecentEventCities(limit: number = 5): Promise<string[]> {
  try {
    const response = await apiClient.get<{
      success: boolean
      cities: string[]
      count: number
    }>(`/api/events/inference/recent-cities?limit=${limit}`)
    
    if (response.data.success) {
      return response.data.cities
    }
    return []
  } catch (error) {
    console.error('Error getting recent cities:', error)
    return []
  }
}

// =====================================================================
// CRUD API Calls
// =====================================================================

/**
 * Get all events for the current company
 * With optional filtering and pagination
 */
export async function getEvents(
  page: number = 1,
  pageSize: number = 20,
  filters?: EventFilters
): Promise<EventListResponse> {
  try {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    params.append('page_size', pageSize.toString())
    
    if (filters?.eventTypeId) params.append('event_type_id', filters.eventTypeId.toString())
    if (filters?.statusId) params.append('status_id', filters.statusId.toString())
    if (filters?.industryId) params.append('industry_id', filters.industryId.toString())
    if (filters?.dateFrom) params.append('date_from', filters.dateFrom)
    if (filters?.dateTo) params.append('date_to', filters.dateTo)
    if (filters?.search) params.append('search', filters.search)
    
    const response = await apiClient.get<{
      events: BackendEvent[]
      total: number
      page: number
      page_size: number
    }>(`/api/events?${params.toString()}`)
    
    // Debug: Log raw backend response
    console.log('📥 getEvents - Raw backend response:', response.data)
    if (response.data.events.length > 0) {
      console.log('📥 getEvents - First event from backend:', JSON.stringify(response.data.events[0], null, 2))
    }
    
    const transformed = response.data.events.map(transformEvent)
    
    // Debug: Log transformed event
    if (transformed.length > 0) {
      console.log('✅ getEvents - Transformed event:', transformed[0])
      console.log('✅ getEvents - Event tags:', transformed[0].tags)
      console.log('✅ getEvents - Event expectedAttendees:', transformed[0].expectedAttendees)
      console.log('✅ getEvents - Event latitude:', transformed[0].latitude)
      console.log('✅ getEvents - Event longitude:', transformed[0].longitude)
      console.log('✅ getEvents - Event organizerEmail:', transformed[0].organizerContactEmail)
      console.log('✅ getEvents - Event organizerWebsite:', transformed[0].organizerWebsite)
    }
    
    return {
      events: transformed,
      total: response.data.total,
      page: response.data.page,
      pageSize: response.data.page_size
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get a single event by ID
 */
export async function getEventById(eventId: number): Promise<Event> {
  try {
    const response = await apiClient.get<BackendEvent>(`/api/events/${eventId}`)
    return transformEvent(response.data)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Create a new event
 */
/**
 * Transform EventCreateRequest (camelCase) to backend format (snake_case)
 * Used by both createEvent and offlineQueue
 */
export function transformEventCreateRequest(request: EventCreateRequest): Record<string, unknown> {
  return {
    name: request.name,
    description: request.description ?? null,
    short_description: request.shortDescription ?? null,
    
    start_datetime: request.startDatetime,
    end_datetime: request.endDatetime ?? null,
    timezone_identifier: request.timezoneIdentifier ?? null,
    
    venue_name: request.venueName ?? null,
    venue_address: request.venueAddress ?? null,
    city: request.city ?? null,
    state: request.state ?? null,
    country_id: request.countryId ?? null,
    latitude: request.latitude ?? null,
    longitude: request.longitude ?? null,
    
    event_type_id: request.eventTypeId,
    industry_id: request.industryId ?? null,
    tags: request.tags ?? null,
    
    is_public: request.isPublic ?? false,
    is_shared_with_platform: request.isSharedWithPlatform ?? false,
    event_status_id: request.eventStatusId ?? 1,
    is_recurring: request.isRecurring ?? false,
    
    organizer_company_id: request.organizerCompanyId ?? null,
    organizer_contact_email: request.organizerContactEmail ?? null,
    organizer_website: request.organizerWebsite ?? null,
    
    expected_attendees: request.expectedAttendees ?? null
  }
}

export async function createEvent(request: EventCreateRequest): Promise<CreateEventResponse> {
  try {
    // Transform camelCase to snake_case for backend
    const backendRequest = transformEventCreateRequest(request)
    
    const response = await apiClient.post<{
      success: boolean
      message: string
      event_id: number
      event: BackendEvent
    }>('/api/events', backendRequest)
    
    return {
      success: response.data.success,
      message: response.data.message,
      eventId: response.data.event_id,
      event: transformEvent(response.data.event)
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Update an existing event
 */
export async function updateEvent(
  eventId: number,
  request: EventUpdateRequest
): Promise<UpdateEventResponse> {
  try {
    // Transform camelCase to snake_case for backend
    const backendRequest: Record<string, unknown> = {}
    
    if (request.name !== undefined) backendRequest.name = request.name
    if (request.description !== undefined) backendRequest.description = request.description
    if (request.shortDescription !== undefined) backendRequest.short_description = request.shortDescription
    
    if (request.startDatetime !== undefined) backendRequest.start_datetime = request.startDatetime
    if (request.endDatetime !== undefined) backendRequest.end_datetime = request.endDatetime
    if (request.timezoneIdentifier !== undefined) backendRequest.timezone_identifier = request.timezoneIdentifier
    
    if (request.venueName !== undefined) backendRequest.venue_name = request.venueName
    if (request.venueAddress !== undefined) backendRequest.venue_address = request.venueAddress
    if (request.city !== undefined) backendRequest.city = request.city
    if (request.state !== undefined) backendRequest.state = request.state
    if (request.countryId !== undefined) backendRequest.country_id = request.countryId
    if (request.latitude !== undefined) backendRequest.latitude = request.latitude
    if (request.longitude !== undefined) backendRequest.longitude = request.longitude
    
    if (request.eventTypeId !== undefined) backendRequest.event_type_id = request.eventTypeId
    if (request.industryId !== undefined) backendRequest.industry_id = request.industryId
    if (request.tags !== undefined) backendRequest.tags = request.tags
    
    if (request.isPublic !== undefined) backendRequest.is_public = request.isPublic
    if (request.isSharedWithPlatform !== undefined) backendRequest.is_shared_with_platform = request.isSharedWithPlatform
    if (request.eventStatusId !== undefined) backendRequest.event_status_id = request.eventStatusId
    if (request.isRecurring !== undefined) backendRequest.is_recurring = request.isRecurring
    
    if (request.organizerCompanyId !== undefined) backendRequest.organizer_company_id = request.organizerCompanyId
    if (request.organizerContactEmail !== undefined) backendRequest.organizer_contact_email = request.organizerContactEmail
    if (request.organizerWebsite !== undefined) backendRequest.organizer_website = request.organizerWebsite
    
    if (request.expectedAttendees !== undefined) backendRequest.expected_attendees = request.expectedAttendees
    
    const response = await apiClient.put<{
      success: boolean
      message: string
      event_id: number
      event: BackendEvent
    }>(`/api/events/${eventId}`, backendRequest)
    
    return {
      success: response.data.success,
      message: response.data.message,
      eventId: response.data.event_id,
      event: transformEvent(response.data.event)
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Delete an event (soft delete)
 */
export async function deleteEvent(eventId: number): Promise<DeleteEventResponse> {
  try {
    const response = await apiClient.delete<{
      success: boolean
      message: string
      event_id: number
    }>(`/api/events/${eventId}`)
    
    return {
      success: response.data.success,
      message: response.data.message,
      eventId: response.data.event_id
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Leave an event (disassociate company)
 */
export async function leaveEvent(eventId: number, companyId: number): Promise<{ success: boolean; message: string }> {
  try {
    const response = await apiClient.delete<{
      success: boolean
      message: string
      event_id: number
      company_id: number
    }>(`/api/events/${eventId}/companies/${companyId}`)
    
    return {
      success: response.data.success,
      message: response.data.message
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Search events with filters
 */
export async function searchEvents(
  filters: EventFilters,
  page: number = 1,
  pageSize: number = 20
): Promise<EventListResponse> {
  try {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    params.append('page_size', pageSize.toString())
    
    if (filters.eventTypeId) params.append('event_type_id', filters.eventTypeId.toString())
    if (filters.statusId) params.append('status_id', filters.statusId.toString())
    if (filters.industryId) params.append('industry_id', filters.industryId.toString())
    if (filters.dateFrom) params.append('date_from', filters.dateFrom)
    if (filters.dateTo) params.append('date_to', filters.dateTo)
    if (filters.search) params.append('search', filters.search)
    
    const response = await apiClient.get<{
      events: BackendEvent[]
      total: number
      page: number
      page_size: number
    }>(`/api/events/search?${params.toString()}`)
    
    return {
      events: response.data.events.map(transformEvent),
      total: response.data.total,
      page: response.data.page,
      pageSize: response.data.page_size
    }
  } catch (error) {
    throw formatError(error)
  }
}
