"""
Events Module Schemas
Pydantic models for event requests/responses
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


# =====================================================================
# Reference Data Schemas
# =====================================================================

class EventTypeResponse(BaseModel):
    """Event type reference data"""
    event_type_id: int = Field(..., alias="EventTypeID")
    type_code: str = Field(..., alias="TypeCode")
    type_name: str = Field(..., alias="TypeName")
    type_description: Optional[str] = Field(None, alias="TypeDescription")
    is_active: bool = Field(..., alias="IsActive")
    sort_order: int = Field(..., alias="SortOrder")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "event_type_id": 1,
                "type_code": "TRADE_SHOW",
                "type_name": "Trade Show",
                "type_description": "Industry trade shows and exhibitions",
                "is_active": True,
                "sort_order": 1
            }
        }


class EventStatusResponse(BaseModel):
    """Event status reference data"""
    event_status_id: int = Field(..., alias="EventStatusID")
    status_code: str = Field(..., alias="StatusCode")
    status_name: str = Field(..., alias="StatusName")
    status_description: Optional[str] = Field(None, alias="StatusDescription")
    status_color: Optional[str] = Field(None, alias="StatusColor")
    status_icon: Optional[str] = Field(None, alias="StatusIcon")
    is_active: bool = Field(..., alias="IsActive")
    sort_order: int = Field(..., alias="SortOrder")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "event_status_id": 1,
                "status_code": "DRAFT",
                "status_name": "Draft",
                "status_description": "Event is being created and edited",
                "status_color": "#FFA500",
                "status_icon": "draft-icon",
                "is_active": True,
                "sort_order": 1
            }
        }


class PublicReviewStatusResponse(BaseModel):
    """Public review status reference data"""
    public_review_status_id: int = Field(..., alias="PublicReviewStatusID")
    status_code: str = Field(..., alias="StatusCode")
    status_name: str = Field(..., alias="StatusName")
    status_description: Optional[str] = Field(None, alias="StatusDescription")
    status_color: Optional[str] = Field(None, alias="StatusColor")
    status_icon: Optional[str] = Field(None, alias="StatusIcon")
    is_active: bool = Field(..., alias="IsActive")
    sort_order: int = Field(..., alias="SortOrder")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "public_review_status_id": 1,
                "status_code": "PENDING",
                "status_name": "Pending Review",
                "status_description": "Event is awaiting admin review for platform-wide visibility",
                "status_color": "#FFC107",
                "status_icon": "clock-icon",
                "is_active": True,
                "sort_order": 1
            }
        }


class IndustryResponse(BaseModel):
    """Industry reference data (lightweight)"""
    industry_id: int = Field(..., alias="IndustryID")
    industry_code: str = Field(..., alias="IndustryCode")
    industry_name: str = Field(..., alias="IndustryName")
    description: Optional[str] = Field(None, alias="Description")
    is_active: bool = Field(..., alias="IsActive")
    sort_order: int = Field(..., alias="SortOrder")

    class Config:
        populate_by_name = True


class CompanySummaryResponse(BaseModel):
    """Lightweight company summary for event relationships"""
    company_id: int = Field(..., alias="CompanyID")
    company_name: str = Field(..., alias="CompanyName")
    legal_entity_name: Optional[str] = Field(None, alias="LegalEntityName")
    abn: Optional[str] = Field(None, alias="ABN")
    acn: Optional[str] = Field(None, alias="ACN")
    website: Optional[str] = Field(None, alias="Website")
    country_id: Optional[int] = Field(None, alias="CountryID")

    class Config:
        populate_by_name = True


# =====================================================================
# Event Creation Schema
# =====================================================================

class EventCreateSchema(BaseModel):
    """Request schema for creating an event"""
    name: str = Field(..., min_length=1, max_length=200, description="Event name/title")
    description: Optional[str] = Field(None, description="Detailed event description")
    short_description: Optional[str] = Field(None, max_length=500, description="Brief summary for list views")
    
    # Date/Time
    start_datetime: datetime = Field(..., description="Event start date/time (UTC)")
    end_datetime: Optional[datetime] = Field(None, description="Event end date/time (UTC, nullable)")
    timezone_identifier: Optional[str] = Field(None, max_length=50, description="IANA timezone (e.g., 'Australia/Sydney')")
    
    # Location
    venue_name: Optional[str] = Field(None, max_length=200, description="Venue name")
    venue_address: Optional[str] = Field(None, max_length=500, description="Full venue address")
    city: Optional[str] = Field(None, max_length=100, description="City name")
    state: Optional[str] = Field(None, max_length=100, description="State/Province")
    country_id: Optional[int] = Field(None, description="Country ID from ref.Country")
    latitude: Optional[Decimal] = Field(None, description="GPS latitude (-90 to 90)")
    longitude: Optional[Decimal] = Field(None, description="GPS longitude (-180 to 180)")
    
    # Classification
    event_type_id: int = Field(..., description="Event type ID from ref.EventType")
    industry_id: Optional[int] = Field(None, description="Industry ID from ref.Industry")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    
    # Configuration
    is_public: bool = Field(False, description="Public visibility flag")
    is_shared_with_platform: bool = Field(False, description="User's choice to share event with platform-wide search (requires admin review if True)")
    event_status_id: int = Field(1, description="Event status ID (1=Draft)")
    is_recurring: bool = Field(False, description="Recurring event flag")
    
    # Organizer
    organizer_company_id: Optional[int] = Field(None, description="Organizer company ID")
    organizer_contact_email: Optional[str] = Field(None, max_length=100, description="Organizer contact email")
    organizer_website: Optional[str] = Field(None, max_length=200, description="Organizer website")
    
    # Metrics
    expected_attendees: Optional[int] = Field(None, ge=0, description="Expected attendance")
    
    @validator('end_datetime')
    def validate_end_after_start(cls, v, values):
        if v and 'start_datetime' in values and v < values['start_datetime']:
            raise ValueError('End date must be after start date')
        return v
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if v is not None and (v < Decimal('-90') or v > Decimal('90')):
            raise ValueError('Latitude must be between -90 and 90')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if v is not None and (v < Decimal('-180') or v > Decimal('180')):
            raise ValueError('Longitude must be between -180 and 180')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Consumer Electronics Show 2025",
                "description": "World's largest consumer electronics trade show",
                "short_description": "CES 2025 - Las Vegas",
                "start_datetime": "2025-01-07T09:00:00Z",
                "end_datetime": "2025-01-10T17:00:00Z",
                "timezone_identifier": "America/Los_Angeles",
                "venue_name": "Las Vegas Convention Center",
                "venue_address": "3150 Paradise Rd, Las Vegas, NV 89109, USA",
                "city": "Las Vegas",
                "state": "Nevada",
                "country_id": 1,
                "latitude": "36.1147",
                "longitude": "-115.1728",
                "event_type_id": 1,
                "industry_id": 3,
                "tags": "Technology,Innovation,Electronics",
                "is_public": True,
                "event_status_id": 1,
                "expected_attendees": 150000
            }
        }


# =====================================================================
# Event Update Schema
# =====================================================================

class EventUpdateSchema(BaseModel):
    """Request schema for updating an event"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Event name/title")
    description: Optional[str] = Field(None, description="Detailed event description")
    short_description: Optional[str] = Field(None, max_length=500, description="Brief summary")
    
    # Date/Time
    start_datetime: Optional[datetime] = Field(None, description="Event start date/time (UTC)")
    end_datetime: Optional[datetime] = Field(None, description="Event end date/time (UTC)")
    timezone_identifier: Optional[str] = Field(None, max_length=50, description="IANA timezone")
    
    # Location
    venue_name: Optional[str] = Field(None, max_length=200)
    venue_address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country_id: Optional[int] = Field(None, description="Country ID")
    latitude: Optional[Decimal] = Field(None, description="GPS latitude")
    longitude: Optional[Decimal] = Field(None, description="GPS longitude")
    
    # Classification
    event_type_id: Optional[int] = Field(None, description="Event type ID")
    industry_id: Optional[int] = Field(None, description="Industry ID")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    
    # Configuration
    is_public: Optional[bool] = Field(None, description="Public visibility")
    is_shared_with_platform: Optional[bool] = Field(None, description="User's choice to share event with platform-wide search (requires admin review if True)")
    event_status_id: Optional[int] = Field(None, description="Event status ID")
    is_recurring: Optional[bool] = Field(None, description="Recurring flag")
    
    # Organizer
    organizer_company_id: Optional[int] = Field(None)
    organizer_contact_email: Optional[str] = Field(None, max_length=100)
    organizer_website: Optional[str] = Field(None, max_length=200)
    
    # Metrics
    expected_attendees: Optional[int] = Field(None, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "CES 2025 Updated",
                "event_status_id": 2,
                "expected_attendees": 160000
            }
        }


# =====================================================================
# Event Response Schemas
# =====================================================================

class EventUserRole(BaseModel):
    """User's role information for an event"""
    role_code: Optional[str] = Field(None, description="Role code (event_owner, event_organizer, event_participant)")
    role_name: Optional[str] = Field(None, description="Role display name")
    has_edit_event: bool = Field(False, description="Can edit event details")
    has_delete_event: bool = Field(False, description="Can delete event")
    has_manage_participants: bool = Field(False, description="Can manage event participants")
    has_view_event: bool = Field(True, description="Can view event details")
    is_legacy: bool = Field(False, description="True if event has no EventCompany record (legacy)")
    
    class Config:
        populate_by_name = True


class EventResponse(BaseModel):
    """Response schema for a single event"""
    event_id: int = Field(..., alias="EventID")
    name: str = Field(..., alias="Name")
    description: Optional[str] = Field(None, alias="Description")
    short_description: Optional[str] = Field(None, alias="ShortDescription")
    
    company_id: int = Field(..., alias="CompanyID")
    created_by: int = Field(..., alias="CreatedBy")
    
    start_datetime: datetime = Field(..., alias="StartDateTime")
    end_datetime: Optional[datetime] = Field(None, alias="EndDateTime")
    timezone_identifier: Optional[str] = Field(None, alias="TimezoneIdentifier")
    
    venue_name: Optional[str] = Field(None, alias="VenueName")
    venue_address: Optional[str] = Field(None, alias="VenueAddress")
    city: Optional[str] = Field(None, alias="City")
    state: Optional[str] = Field(None, alias="State")
    country_id: Optional[int] = Field(None, alias="CountryID")
    latitude: Optional[Decimal] = Field(None, alias="Latitude")
    longitude: Optional[Decimal] = Field(None, alias="Longitude")
    
    event_type_id: int = Field(..., alias="EventTypeID")
    event_type: Optional[EventTypeResponse] = None
    industry_id: Optional[int] = Field(None, alias="IndustryID")
    industry: Optional[IndustryResponse] = Field(None, alias="Industry")
    tags: Optional[str] = Field(None, alias="Tags")
    
    is_public: bool = Field(..., alias="IsPublic")
    is_shared_with_platform: bool = Field(..., alias="IsSharedWithPlatform")
    is_public_review_required: bool = Field(..., alias="IsPublicReviewRequired")
    public_review_status_id: Optional[int] = Field(None, alias="PublicReviewStatusID")
    public_review_status: Optional[PublicReviewStatusResponse] = None
    public_review_date: Optional[datetime] = Field(None, alias="PublicReviewDate")
    public_review_by: Optional[int] = Field(None, alias="PublicReviewBy")
    public_review_comments: Optional[str] = Field(None, alias="PublicReviewComments")
    public_visibility_date: Optional[datetime] = Field(None, alias="PublicVisibilityDate")
    event_status_id: int = Field(..., alias="EventStatusID")
    event_status: Optional[EventStatusResponse] = None
    is_recurring: bool = Field(..., alias="IsRecurring")
    
    organizer_company_id: Optional[int] = Field(None, alias="OrganizerCompanyID")
    organizer_contact_email: Optional[str] = Field(None, alias="OrganizerContactEmail")
    organizer_website: Optional[str] = Field(None, alias="OrganizerWebsite")
    organizer_company: Optional[CompanySummaryResponse] = Field(None, alias="OrganizerCompany")
    owner_company: Optional[CompanySummaryResponse] = Field(None, alias="OwnerCompany")
    
    expected_attendees: Optional[int] = Field(None, alias="ExpectedAttendees")
    actual_attendees: Optional[int] = Field(None, alias="ActualAttendees")
    forms_created: int = Field(..., alias="FormsCreated")
    total_submissions: int = Field(..., alias="TotalSubmissions")
    
    created_date: datetime = Field(..., alias="CreatedDate")
    updated_date: Optional[datetime] = Field(None, alias="UpdatedDate")
    updated_by: Optional[int] = Field(None, alias="UpdatedBy")
    
    # User role for this event (current user's company role)
    user_role: Optional[EventUserRole] = Field(None, description="Current user's role for this event")
    
    class Config:
        populate_by_name = True
        from_attributes = True


class EventListResponse(BaseModel):
    """Response schema for event list"""
    events: List[EventResponse]
    total: int
    page: int = 1
    page_size: int = 20
    
    class Config:
        json_schema_extra = {
            "example": {
                "events": [],
                "total": 0,
                "page": 1,
                "page_size": 20
            }
        }


class CreateEventResponse(BaseModel):
    """Response schema for event creation"""
    success: bool
    message: str
    event_id: int
    event: EventResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Event created successfully",
                "event_id": 1,
                "event": {}
            }
        }


class UpdateEventResponse(BaseModel):
    """Response schema for event update"""
    success: bool
    message: str
    event_id: int
    event: EventResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Event updated successfully",
                "event_id": 1,
                "event": {}
            }
        }


class DeleteEventResponse(BaseModel):
    """Response schema for event deletion"""
    success: bool
    message: str
    event_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Event deleted successfully",
                "event_id": 1
            }
        }


