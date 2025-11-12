/**
 * Events Types for Epic 2 Story 2.4
 * Type definitions for event management
 */

// Reference Data Types
export interface EventType {
  eventTypeId: number
  typeCode: string
  typeName: string
  typeDescription: string | null
  isActive: boolean
  sortOrder: number
}

export interface EventStatus {
  eventStatusId: number
  statusCode: string
  statusName: string
  statusDescription: string | null
  statusColor: string | null
  statusIcon: string | null
  isActive: boolean
  sortOrder: number
}

export interface PublicReviewStatus {
  publicReviewStatusId: number
  statusCode: string
  statusName: string
  statusDescription: string | null
  statusColor: string | null
  statusIcon: string | null
  isActive: boolean
  sortOrder: number
}

export interface IndustrySummary {
  industryId: number
  industryCode: string
  industryName: string
  description: string | null
  isActive: boolean
  sortOrder: number
}

export interface CompanySummary {
  companyId: number
  companyName: string
  legalEntityName: string | null
  abn: string | null
  acn: string | null
  website: string | null
  countryId: number | null
}

// Main Event Type
export interface Event {
  eventId: number
  name: string
  description: string | null
  shortDescription: string | null
  
  companyId: number
  createdBy: number
  
  startDateTime: string
  endDateTime: string | null
  timezoneIdentifier: string | null
  
  venueName: string | null
  venueAddress: string | null
  city: string | null
  state: string | null
  countryId: number | null
  latitude: number | null
  longitude: number | null
  
  eventTypeId: number
  eventType: EventType | null
  industryId: number | null
  industry?: IndustrySummary | null
  tags: string | null
  
  isPublic: boolean
  isSharedWithPlatform?: boolean
  isPublicReviewRequired?: boolean
  publicReviewStatusId?: number | null
  publicReviewStatus?: PublicReviewStatus | null
  publicReviewDate?: string | null
  publicReviewBy?: number | null
  publicReviewComments?: string | null
  publicVisibilityDate?: string | null
  eventStatusId: number
  eventStatus: EventStatus | null
  isRecurring: boolean
  
  organizerCompanyId: number | null
  organizerContactEmail: string | null
  organizerWebsite: string | null
  organizerCompany?: CompanySummary | null
  ownerCompany?: CompanySummary | null
  
  expectedAttendees: number | null
  actualAttendees: number | null
  formsCreated: number
  totalSubmissions: number
  
  createdDate: string
  updatedDate: string | null
  updatedBy: number | null
  
  // User role for this event (current user's company role)
  userRole?: {
    role_code: string | null
    role_name: string | null
    has_edit_event: boolean
    has_delete_event: boolean
    has_manage_participants: boolean
    has_view_event: boolean
    is_legacy: boolean
  } | null
}

// Request Types
export interface EventCreateRequest {
  name: string
  description?: string | null
  shortDescription?: string | null
  
  startDatetime: string
  endDatetime?: string | null
  timezoneIdentifier?: string | null
  
  venueName?: string | null
  venueAddress?: string | null
  city?: string | null
  state?: string | null
  countryId?: number | null
  latitude?: number | null
  longitude?: number | null
  
  eventTypeId: number
  industryId?: number | null
  tags?: string | null
  
  isPublic?: boolean
  isSharedWithPlatform?: boolean
  eventStatusId?: number
  isRecurring?: boolean
  
  organizerCompanyId?: number | null
  organizerContactEmail?: string | null
  organizerWebsite?: string | null
  
  expectedAttendees?: number | null
}

export interface EventUpdateRequest {
  name?: string
  description?: string | null
  shortDescription?: string | null
  
  startDatetime?: string
  endDatetime?: string | null
  timezoneIdentifier?: string | null
  
  venueName?: string | null
  venueAddress?: string | null
  city?: string | null
  state?: string | null
  countryId?: number | null
  latitude?: number | null
  longitude?: number | null
  
  eventTypeId?: number
  industryId?: number | null
  tags?: string | null
  
  isPublic?: boolean
  isSharedWithPlatform?: boolean
  eventStatusId?: number
  isRecurring?: boolean
  
  organizerCompanyId?: number | null
  organizerContactEmail?: string | null
  organizerWebsite?: string | null
  
  expectedAttendees?: number | null
}

// Response Types
export interface EventListResponse {
  events: Event[]
  total: number
  page: number
  pageSize: number
}

export interface CreateEventResponse {
  success: boolean
  message: string
  eventId: number
  event: Event
}

export interface UpdateEventResponse {
  success: boolean
  message: string
  eventId: number
  event: Event
}

export interface DeleteEventResponse {
  success: boolean
  message: string
  eventId: number
}

// Filter Types
export interface EventFilters {
  eventTypeId?: number
  statusId?: number
  industryId?: number
  dateFrom?: string
  dateTo?: string
  search?: string
}


