"""
Company Management Schemas
Pydantic models for company requests/responses
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
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
    invitation_id: int = Field(..., description="Created invitation ID")
    expires_at: datetime = Field(..., description="When invitation expires")
    
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

