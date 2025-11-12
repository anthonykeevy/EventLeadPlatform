"""
Admin Review Schemas
Story 2.6: Admin Public Event Review Workflow
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ApproveEventRequest(BaseModel):
    """Request schema for approving an event"""
    comment: Optional[str] = None
    public_visibility_date: Optional[datetime] = None  # If set, event becomes public on this date


class RejectEventRequest(BaseModel):
    """Request schema for rejecting an event"""
    comment: str  # Required for rejection


class PendingReviewEventResponse(BaseModel):
    """Event response for pending review queue"""
    event_id: int
    name: str
    description: Optional[str] = None
    company_name: str
    creator_email: str
    created_date: datetime
    days_pending: int  # Days since submission


class ReviewHistoryResponse(BaseModel):
    """Review history entry"""
    review_id: int  # EventID (since review is stored in Event table)
    event_id: int
    event_name: str
    reviewer_email: str
    review_date: datetime
    decision: str  # 'APPROVED' or 'REJECTED'
    comments: Optional[str] = None


class EventReviewStatusResponse(BaseModel):
    """Review status for event creators"""
    review_status: Optional[str]  # 'PENDING', 'APPROVED', 'REJECTED'
    review_date: Optional[datetime]
    reviewer_email: Optional[str]
    review_comments: Optional[str]
    public_visibility_date: Optional[datetime]


class EventReviewDetailsResponse(BaseModel):
    """Complete event details for review"""
    event_id: int
    name: str
    description: Optional[str]
    company_name: str
    creator_email: str
    start_date_time: datetime
    end_date_time: Optional[datetime]
    venue_name: Optional[str]
    venue_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country_name: Optional[str]
    event_type_name: str
    event_status_name: str
    industry_name: Optional[str]
    is_public: bool
    public_review_status: Optional[str]
    created_date: datetime
