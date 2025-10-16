"""
Authentication Schemas
Pydantic models for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any


# ============================================================================
# Signup Schemas
# ============================================================================

class SignupRequest(BaseModel):
    """Request schema for user signup"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "MySecureP@ss123",
                "first_name": "John",
                "last_name": "Doe"
            }
        }


class SignupResponse(BaseModel):
    """Response schema for successful signup"""
    success: bool = Field(..., description="Whether signup was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Signup successful. Please check your email to verify your account.",
                "data": {
                    "user_id": 123,
                    "email": "john.doe@example.com"
                }
            }
        }


# ============================================================================
# Email Verification Schemas
# ============================================================================

class VerifyEmailRequest(BaseModel):
    """Request schema for email verification"""
    token: str = Field(..., min_length=32, description="Email verification token from email link")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "abc123xyz789..."
            }
        }


class VerifyEmailResponse(BaseModel):
    """Response schema for email verification"""
    success: bool = Field(..., description="Whether verification was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Email verified successfully. You can now log in.",
                "data": {
                    "user_id": 123
                }
            }
        }


# ============================================================================
# Error Response Schema
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response schema"""
    success: bool = Field(False, description="Always false for errors")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    errors: Optional[Dict[str, Any]] = Field(None, description="Field-specific errors")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Validation failed",
                "detail": "Password does not meet security requirements",
                "errors": {
                    "password": ["Password must contain at least one uppercase letter"]
                }
            }
        }

