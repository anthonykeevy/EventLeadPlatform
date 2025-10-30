"""
User Management Schemas
Pydantic models for user profile requests/responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

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
        orm_mode = True
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


# ============================================================================
# Schemas for Company Switching (Story 1.11)
# ============================================================================

class SwitchCompanyRequest(BaseModel):
    company_id: int = Field(..., description="The ID of the company to switch to.")

class SwitchedCompanyInfo(BaseModel):
    company_id: int
    company_name: str
    role: str

class SwitchCompanyResponse(BaseModel):
    access_token: str
    refresh_token: str
    company: SwitchedCompanyInfo
    
class RelationshipInfo(BaseModel):
    relationship_id: int
    related_company_id: int
    related_company_name: str
    relationship_type: str
    status: str

class UserCompanyInfo(BaseModel):
    company_id: int
    company_name: str
    role: str
    is_primary: bool
    joined_at: datetime
    relationship: Optional[RelationshipInfo] = None


# ============================================================================
# Epic 2: Enhanced User Profile Schemas
# ============================================================================

class UserProfileUpdateSchema(BaseModel):
    """
    Request schema for updating user profile enhancements (Epic 2).
    All fields are optional for partial updates.
    """
    bio: Optional[str] = Field(None, max_length=500, description="Professional bio/summary")
    theme_preference_id: Optional[int] = Field(None, description="Theme preference ID")
    layout_density_id: Optional[int] = Field(None, description="Layout density ID")
    font_size_id: Optional[int] = Field(None, description="Font size ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "bio": "Marketing professional with 10 years of experience",
                "theme_preference_id": 2,
                "layout_density_id": 1,
                "font_size_id": 2
            }
        }


class ReferenceOptionResponse(BaseModel):
    """Response schema for reference table options"""
    id: int = Field(..., description="Option ID")
    code: str = Field(..., description="Unique code")
    name: str = Field(..., description="Display name")
    description: str = Field(..., description="Full description")
    css_class: str = Field(..., description="CSS class for frontend")
    base_font_size: Optional[str] = Field(None, description="Base font size (for FontSize only)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 2,
                "code": "dark",
                "name": "Dark Theme",
                "description": "Dark interface with dark backgrounds",
                "css_class": "theme-dark",
                "base_font_size": None
            }
        }


class IndustryAssociationSchema(BaseModel):
    """Request schema for adding/updating industry association"""
    industry_id: int = Field(..., description="Industry ID")
    is_primary: bool = Field(default=False, description="Whether this is the primary industry")
    sort_order: Optional[int] = Field(None, description="Display order (for secondary industries)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "industry_id": 5,
                "is_primary": False,
                "sort_order": 1
            }
        }


class IndustryAssociationResponse(BaseModel):
    """Response schema for industry association"""
    user_industry_id: int = Field(..., description="UserIndustry junction table ID")
    industry_id: int = Field(..., description="Industry ID")
    industry_name: str = Field(..., description="Industry name")
    industry_code: str = Field(..., description="Industry code")
    is_primary: bool = Field(..., description="Whether this is the primary industry")
    sort_order: int = Field(..., description="Display order")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_industry_id": 10,
                "industry_id": 5,
                "industry_name": "Technology",
                "industry_code": "tech",
                "is_primary": False,
                "sort_order": 1
            }
        }


class EnhancedUserProfileResponse(BaseModel):
    """Response schema for enhanced user profile (Epic 2)"""
    user_id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    bio: Optional[str]
    role_title: Optional[str]
    is_email_verified: bool
    
    # Epic 2 Enhanced Fields
    theme_preference: Optional[ReferenceOptionResponse] = None
    layout_density: Optional[ReferenceOptionResponse] = None
    font_size: Optional[ReferenceOptionResponse] = None
    industries: List[IndustryAssociationResponse] = Field(default_factory=list, description="User's industry associations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+61412345678",
                "bio": "Marketing professional",
                "role_title": "Marketing Manager",
                "is_email_verified": True,
                "theme_preference": {
                    "id": 2,
                    "code": "dark",
                    "name": "Dark Theme",
                    "description": "Dark interface",
                    "css_class": "theme-dark",
                    "base_font_size": None
                },
                "layout_density": {
                    "id": 1,
                    "code": "compact",
                    "name": "Compact",
                    "description": "Tight spacing",
                    "css_class": "layout-compact",
                    "base_font_size": None
                },
                "font_size": {
                    "id": 2,
                    "code": "medium",
                    "name": "Medium",
                    "description": "Standard text size",
                    "css_class": "font-medium",
                    "base_font_size": "16px"
                },
                "industries": [
                    {
                        "user_industry_id": 10,
                        "industry_id": 5,
                        "industry_name": "Technology",
                        "industry_code": "tech",
                        "is_primary": True,
                        "sort_order": 0
                    }
                ]
            }
        }