"""
User Management Schemas
Pydantic models for user profile requests/responses
"""
from pydantic import BaseModel, Field
from typing import Optional


class UpdateUserDetailsSchema(BaseModel):
    """
    Request schema for updating user profile details.
    Used during onboarding or profile updates.
    """
    phone: Optional[str] = Field(None, min_length=1, max_length=20, description="Phone number")
    timezone_identifier: str = Field(..., min_length=1, max_length=50, description="IANA timezone (e.g., 'Australia/Sydney')")
    role_title: Optional[str] = Field(None, max_length=100, description="Job title/role")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+61412345678",
                "timezone_identifier": "Australia/Sydney",
                "role_title": "Marketing Manager"
            }
        }


class UpdateUserDetailsResponse(BaseModel):
    """Response schema for user details update"""
    success: bool = Field(..., description="Whether update was successful")
    message: str = Field(..., description="Human-readable message")
    user_id: int = Field(..., description="Updated user ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User details updated successfully",
                "user_id": 123
            }
        }


class UserProfileResponse(BaseModel):
    """Response schema for user profile data"""
    user_id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    timezone_identifier: str
    role_title: Optional[str]
    is_email_verified: bool
    onboarding_complete: bool
    onboarding_step: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+61412345678",
                "timezone_identifier": "Australia/Sydney",
                "role_title": "Marketing Manager",
                "is_email_verified": True,
                "onboarding_complete": False,
                "onboarding_step": 2
            }
        }

