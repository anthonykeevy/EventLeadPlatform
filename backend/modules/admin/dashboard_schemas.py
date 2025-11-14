"""
Admin Dashboard Schemas
Story 2.6: Admin Public Event Review Workflow
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AdminCompanyResponse(BaseModel):
    """Company response for admin dashboard"""
    company_id: int
    company_name: str
    created_date: datetime
    total_users: int
    total_events: int


class AdminKPIsResponse(BaseModel):
    """Platform-wide KPIs for admin dashboard"""
    total_companies: int
    total_users: int
    total_events: int
    pending_review_events: int
    approved_events: int
    rejected_events: int
    # Event breakdowns
    events_past: int = 0
    events_current: int = 0
    events_future: int = 0
    # User breakdowns
    users_inactive: int = 0
    users_seldom: int = 0
    users_active: int = 0
    # Company breakdowns
    companies_inactive: int = 0
    companies_seldom: int = 0
    companies_active: int = 0


class AdminEventResponse(BaseModel):
    """Event response for admin dashboard - includes all fields for comprehensive review"""
    event_id: int
    name: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    company_id: int
    company_name: str
    event_type_id: int
    event_type_name: str
    event_status_id: int
    event_status_name: str
    industry_id: Optional[int] = None
    industry_name: Optional[str] = None
    country_id: Optional[int] = None
    country_name: Optional[str] = None
    start_date_time: datetime
    end_date_time: Optional[datetime] = None
    timezone_identifier: Optional[str] = None
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tags: Optional[str] = None
    is_public: bool
    is_shared_with_platform: bool
    is_recurring: bool
    organizer_company_id: Optional[int] = None
    organizer_company_name: Optional[str] = None
    organizer_contact_email: Optional[str] = None
    organizer_website: Optional[str] = None
    expected_attendees: Optional[int] = None
    public_review_status: Optional[str] = None
    created_date: datetime


class AdminEventsListResponse(BaseModel):
    """Paginated events list response"""
    events: List[AdminEventResponse]
    total: int
    page: int
    page_size: int
