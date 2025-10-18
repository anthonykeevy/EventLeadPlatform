"""
Company Management Schemas
Pydantic models for company requests/responses
"""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Any, Dict, Union
from datetime import datetime


class CreateCompanySchema(BaseModel):
    """
    Request schema for creating a company.
    Used during first-time onboarding.
    """
    company_name: str = Field(..., min_length=1, max_length=200, description="Company name")
    abn: Optional[str] = Field(None, max_length=11, description="Australian Business Number (11 digits)")
    acn: Optional[str] = Field(None, max_length=9, description="Australian Company Number (9 digits)")
    phone: Optional[str] = Field(None, max_length=20, description="Company phone number")
    email: Optional[EmailStr] = Field(None, description="Company email")
    website: Optional[str] = Field(None, max_length=500, description="Company website URL")
    country_id: int = Field(..., description="Country ID from ref.Country")
    industry_id: Optional[int] = Field(None, description="Industry ID from ref.Industry")
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Acme Events Pty Ltd",
                "abn": "51824753556",
                "acn": "123456782",
                "phone": "+61298765432",
                "email": "info@acmeevents.com.au",
                "website": "https://acmeevents.com.au",
                "country_id": 1,
                "industry_id": 5
            }
        }


class CreateCompanyResponse(BaseModel):
    """Response schema for company creation"""
    success: bool = Field(..., description="Whether creation was successful")
    message: str = Field(..., description="Human-readable message")
    company_id: int = Field(..., description="Created company ID")
    user_company_id: int = Field(..., description="Created UserCompany relationship ID")
    access_token: str = Field(..., description="New JWT access token with role and company_id")
    refresh_token: str = Field(..., description="New JWT refresh token")
    role: str = Field(..., description="Assigned role (company_admin)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Company created successfully",
                "company_id": 456,
                "user_company_id": 789,
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "role": "company_admin"
            }
        }


class CompanyDetailsResponse(BaseModel):
    """Response schema for company details"""
    company_id: int
    company_name: str
    abn: Optional[str]
    acn: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    country_id: int
    industry_id: Optional[int]
    is_active: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": 456,
                "company_name": "Acme Events Pty Ltd",
                "abn": "51824753556",
                "acn": "123456782",
                "phone": "+61298765432",
                "email": "info@acmeevents.com.au",
                "website": "https://acmeevents.com.au",
                "country_id": 1,
                "industry_id": 5,
                "is_active": True
            }
        }


# ============================================================================
# Team Invitation Schemas (Story 1.6)
# ============================================================================

class SendInvitationSchema(BaseModel):
    """Request schema for sending team invitation"""
    email: EmailStr = Field(..., description="Email address of invitee")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name of invitee")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name of invitee")
    role: str = Field(..., description="Role to assign (company_admin or company_user)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "jane.smith@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "company_user"
            }
        }


class SendInvitationResponse(BaseModel):
    """Response schema for sending invitation"""
    success: bool = Field(..., description="Whether invitation was sent")
    message: str = Field(..., description="Human-readable message")
    invitation_id: Optional[int] = Field(None, description="Created invitation ID (None for existing users)")
    expires_at: Optional[datetime] = Field(None, description="When invitation expires (None for existing users)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Invitation sent successfully",
                "invitation_id": 123,
                "expires_at": "2025-10-23T10:30:00Z"
            }
        }


class InvitationDetails(BaseModel):
    """Response schema for invitation details"""
    invitation_id: int
    company_id: int
    email: str
    first_name: str
    last_name: str
    role: str
    status: str
    invited_by: str
    invited_at: datetime
    expires_at: datetime
    accepted_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    declined_at: Optional[datetime]
    resend_count: int
    last_resent_at: Optional[datetime]
    
    class Config:
        json_schema_extra = {
            "example": {
                "invitation_id": 123,
                "company_id": 456,
                "email": "jane.smith@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "company_user",
                "status": "pending",
                "invited_by": "John Doe",
                "invited_at": "2025-10-16T10:30:00Z",
                "expires_at": "2025-10-23T10:30:00Z",
                "accepted_at": None,
                "cancelled_at": None,
                "declined_at": None,
                "resend_count": 0,
                "last_resent_at": None
            }
        }


class ListInvitationsResponse(BaseModel):
    """Response schema for listing invitations"""
    invitations: List[InvitationDetails]
    total: int
    page: int
    page_size: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "invitations": [],
                "total": 5,
                "page": 1,
                "page_size": 20
            }
        }


class ResendInvitationResponse(BaseModel):
    """Response schema for resending invitation"""
    success: bool
    message: str
    invitation_id: int
    new_expires_at: datetime
    resend_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Invitation resent successfully",
                "invitation_id": 123,
                "new_expires_at": "2025-10-30T10:30:00Z",
                "resend_count": 1
            }
        }


class CancelInvitationResponse(BaseModel):
    """Response schema for cancelling invitation"""
    success: bool
    message: str
    invitation_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Invitation cancelled successfully",
                "invitation_id": 123
            }
        }


# ============================================================================
# ABR Smart Search Schemas (Story 1.10)
# ============================================================================

class SmartSearchRequest(BaseModel):
    """
    Request schema for smart company search
    
    Story 1.10: Enhanced ABR Search Implementation
    AC-1.10.1: Smart Search Auto-Detection
    """
    query: str = Field(
        ..., 
        min_length=2, 
        max_length=255,
        description="Search query (ABN, ACN, or company name)"
    )
    max_results: Optional[int] = Field(
        10,
        ge=1,
        le=200,
        description="Maximum number of results (1-200, default: 10)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Atlassian",
                "max_results": 10
            }
        }


class CompanySearchResult(BaseModel):
    """
    Individual company search result
    
    Story 1.10: AC-1.10.6: Rich Search Results Display
    """
    company_name: str = Field(..., description="Company legal name")
    abn: Optional[str] = Field(None, description="Australian Business Number (11 digits)")
    abn_formatted: Optional[str] = Field(None, description="ABN with spaces (12 345 678 901)")
    gst_registered: Optional[bool] = Field(None, description="GST registration status")
    entity_type: Optional[str] = Field(None, description="Entity type (e.g., 'Australian Private Company')")
    business_address: Optional[str] = Field(None, description="Primary business address")
    status: Optional[str] = Field(None, description="Entity status (Active, Cancelled, etc.)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Atlassian Pty Ltd",
                "abn": "53102443916",
                "abn_formatted": "53 102 443 916",
                "gst_registered": True,
                "entity_type": "Australian Private Company",
                "business_address": "341 George Street, Sydney NSW 2000",
                "status": "Active"
            }
        }


class SmartSearchResponse(BaseModel):
    """
    Response schema for smart company search
    
    Story 1.10: AC-1.10.4: Company Name Search Implementation
    """
    search_type: str = Field(..., description="Detected search type (ABN, ACN, Name)")
    query: str = Field(..., description="Original search query")
    results: List[CompanySearchResult] = Field(..., description="Search results")
    result_count: int = Field(..., description="Number of results returned")
    cached: bool = Field(..., description="Whether results were served from cache")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "search_type": "Name",
                "query": "Atlassian",
                "results": [
                    {
                        "company_name": "Atlassian Pty Ltd",
                        "abn": "53102443916",
                        "abn_formatted": "53 102 443 916",
                        "gst_registered": True,
                        "entity_type": "Australian Private Company",
                        "business_address": "341 George Street, Sydney NSW 2000",
                        "status": "Active"
                    }
                ],
                "result_count": 1,
                "cached": False,
                "response_time_ms": 1250
            }
        }


class SearchErrorResponse(BaseModel):
    """Error response schema for search failures"""
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="User-friendly error message")
    fallback_url: Optional[str] = Field(None, description="Manual entry fallback URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ABR_API_TIMEOUT",
                "message": "Search is taking longer than expected. Try again or enter details manually.",
                "fallback_url": "/companies/manual-entry"
            }
        }


class CacheStatisticsResponse(BaseModel):
    """
    Response schema for cache statistics (admin only)
    
    Story 1.10: AC-1.10.9: Cache Cleanup & Maintenance
    AC-1.10.11: Success Rate Metrics
    """
    total_cached_searches: int = Field(..., description="Total unique searches cached")
    total_cache_entries: int = Field(..., description="Total cache entries (including multiple results)")
    active_cache_entries: int = Field(..., description="Active (non-expired) cache entries")
    expired_entries: int = Field(..., description="Expired cache entries")
    cache_hit_rate_percent: float = Field(..., description="Cache hit rate percentage")
    total_cache_hits: int = Field(..., description="Total cache hits")
    average_hits_per_search: float = Field(..., description="Average hits per search")
    popular_searches: List[Dict[str, Any]] = Field(..., description="Top 10 popular searches")
    search_type_distribution: Dict[str, Dict[str, int]] = Field(..., description="Search type statistics")
    estimated_api_cost_savings_percent: float = Field(..., description="Estimated API cost savings")
    cache_ttl_days: int = Field(..., description="Cache TTL in days")
    generated_at: str = Field(..., description="Statistics generation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_cached_searches": 1500,
                "total_cache_entries": 3200,
                "active_cache_entries": 2800,
                "expired_entries": 400,
                "cache_hit_rate_percent": 42.5,
                "total_cache_hits": 8500,
                "average_hits_per_search": 5.7,
                "popular_searches": [
                    {
                        "search_type": "Name",
                        "search_key": "atlassian",
                        "hit_count": 45,
                        "last_hit": "2025-10-18T10:30:00Z"
                    }
                ],
                "search_type_distribution": {
                    "ABN": {"unique_searches": 500, "total_hits": 2000},
                    "ACN": {"unique_searches": 200, "total_hits": 800},
                    "Name": {"unique_searches": 800, "total_hits": 5700}
                },
                "estimated_api_cost_savings_percent": 40.0,
                "cache_ttl_days": 30,
                "generated_at": "2025-10-18T12:00:00Z"
            }
        }


# ============================================================================
# Schemas for Company Relationships (Story 1.11)
# ============================================================================

class CreateRelationshipRequest(BaseModel):
    related_company_id: int = Field(..., description="The ID of the company to establish a relationship with.")
    relationship_type: str = Field(..., description="The type of relationship (e.g., 'branch', 'subsidiary', 'partner').")
    
    @validator('relationship_type')
    def validate_relationship_type(cls, v):
        allowed_types = {'branch', 'subsidiary', 'partner'}
        if v not in allowed_types:
            raise ValueError(f"relationship_type must be one of {allowed_types}")
        return v

class RelationshipResponse(BaseModel):
    relationship_id: int
    parent_company_id: int
    child_company_id: int
    relationship_type: str
    status: str
    established_at: datetime

    class Config:
        orm_mode = True

class CreateRelationshipResponse(BaseModel):
    success: bool
    message: str
    relationship: RelationshipResponse


# ============================================================================
# Schemas for Access Requests (Story 1.11)
# ============================================================================

class CreateAccessRequestSchema(BaseModel):
    reason: Optional[str] = Field(None, max_length=500, description="Optional reason for the access request.")

class AccessRequestResponse(BaseModel):
    request_id: int = Field(alias="CompanySwitchRequestID")
    user_id: int = Field(alias="UserID")
    to_company_id: int = Field(alias="ToCompanyID")
    status: Union[str, int] = Field(alias="StatusID")  # Can be int (FK) or str (will be populated in router)
    requested_at: datetime = Field(alias="RequestedAt")
    reason: Optional[str] = Field(default=None, alias="Reason")

    model_config = {"from_attributes": True, "populate_by_name": True}

class CreateAccessRequestResponse(BaseModel):
    success: bool
    message: str
    request: AccessRequestResponse

class RejectAccessRequestSchema(BaseModel):
    reason: Optional[str] = Field(None, max_length=500, description="Optional reason for rejecting the request.")


class UpdateRelationshipStatusRequest(BaseModel):
    status: str = Field(..., description="The new status for the relationship ('active', 'suspended', 'terminated').")
    reason: Optional[str] = Field(None, max_length=500, description="Optional reason for the status change, for audit purposes.")

    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = {'active', 'suspended', 'terminated'}
        if v not in allowed_statuses:
            raise ValueError(f"status must be one of {allowed_statuses}")
        return v

