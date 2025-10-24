"""
Invitation Acceptance Schemas
Pydantic models for invitation viewing and acceptance
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InvitationDetailsResponse(BaseModel):
    """
    Response schema for public invitation details.
    Shows information needed for user to decide whether to accept.
    """
    invitation_id: int = Field(..., description="Invitation ID")
    company_name: str = Field(..., description="Company name")
    role_name: str = Field(..., description="Role being offered")
    inviter_name: str = Field(..., description="Name of person who sent invitation")
    invited_email: str = Field(..., description="Email address invited")
    expires_at: datetime = Field(..., description="When invitation expires")
    is_expired: bool = Field(..., description="Whether invitation has expired")
    status: str = Field(..., description="Invitation status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "invitation_id": 123,
                "company_name": "Acme Events Pty Ltd",
                "role_name": "Team Member",
                "inviter_name": "John Doe",
                "invited_email": "jane@example.com",
                "expires_at": "2025-10-23T10:30:00Z",
                "is_expired": False,
                "status": "pending"
            }
        }


class AcceptInvitationResponse(BaseModel):
    """Response schema for invitation acceptance"""
    success: bool = Field(..., description="Whether acceptance was successful")
    message: str = Field(..., description="Human-readable message")
    company_id: int = Field(..., description="Company ID joined")
    role: str = Field(..., description="Role assigned")
    access_token: str = Field(..., description="New JWT access token with role and company_id")
    refresh_token: str = Field(..., description="New JWT refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Invitation accepted successfully",
                "company_id": 456,
                "role": "company_user",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class SwitchCompanyRequest(BaseModel):
    """Request schema for switching active company"""
    company_id: int = Field(..., description="Company ID to switch to")
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": 789
            }
        }


class SwitchCompanyResponse(BaseModel):
    """Response schema for company switching"""
    success: bool = Field(..., description="Whether switch was successful")
    message: str = Field(..., description="Human-readable message")
    company_id: int = Field(..., description="Active company ID")
    company_name: str = Field(..., description="Company name")
    role: str = Field(..., description="User's role in this company")
    access_token: str = Field(..., description="New JWT access token with updated company_id")
    refresh_token: str = Field(..., description="New JWT refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Switched to Acme Events Pty Ltd",
                "company_id": 789,
                "company_name": "Acme Events Pty Ltd",
                "role": "company_admin",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


