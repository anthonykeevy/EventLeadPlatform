"""
Configuration API Schemas
Pydantic models for configuration API requests and responses
"""
from typing import Optional
from pydantic import BaseModel, Field


class PublicConfigResponse(BaseModel):
    """
    Public configuration response (frontend consumption)
    
    Only includes settings safe for public exposure (no secrets)
    """
    # Password policy
    password_min_length: int = Field(..., description="Minimum password length")
    password_require_uppercase: bool = Field(..., description="Require uppercase letter")
    password_require_number: bool = Field(..., description="Require number")
    
    # JWT settings (read-only for frontend info)
    jwt_access_expiry_minutes: int = Field(..., description="JWT access token lifetime (minutes)")
    
    # Token expiry times
    email_verification_expiry_hours: int = Field(..., description="Email verification token lifetime (hours)")
    invitation_expiry_days: int = Field(..., description="Team invitation lifetime (days)")
    
    # Company validation
    company_name_min_length: int = Field(default=2, description="Minimum company name length")
    company_name_max_length: int = Field(default=200, description="Maximum company name length")
    
    class Config:
        json_schema_extra = {
            "example": {
                "password_min_length": 8,
                "password_require_uppercase": False,
                "password_require_number": True,
                "jwt_access_expiry_minutes": 15,
                "email_verification_expiry_hours": 24,
                "invitation_expiry_days": 7,
                "company_name_min_length": 2,
                "company_name_max_length": 200
            }
        }


class SettingResponse(BaseModel):
    """Individual setting response (admin only)"""
    setting_key: str
    setting_value: str
    category: str
    type: str
    description: str
    default_value: str
    is_editable: bool
    is_active: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "setting_key": "PASSWORD_MIN_LENGTH",
                "setting_value": "8",
                "category": "authentication",
                "type": "integer",
                "description": "Minimum password length (characters)",
                "default_value": "8",
                "is_editable": True,
                "is_active": True
            }
        }


class UpdateSettingRequest(BaseModel):
    """Request to update a setting value (admin only)"""
    new_value: str = Field(..., description="New setting value (as string)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "new_value": "10"
            }
        }


class UpdateSettingResponse(BaseModel):
    """Response after updating a setting"""
    success: bool
    message: str
    setting_key: str
    new_value: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Setting updated successfully. Cache invalidated.",
                "setting_key": "PASSWORD_MIN_LENGTH",
                "new_value": "10"
            }
        }


class CacheInvalidationResponse(BaseModel):
    """Response after invalidating configuration cache"""
    success: bool
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Configuration cache invalidated successfully"
            }
        }

