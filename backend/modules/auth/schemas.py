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
# Login Schemas
# ============================================================================

class LoginRequest(BaseModel):
    """Request schema for user login"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "MySecureP@ss123"
            }
        }


class LoginResponse(BaseModel):
    """Response schema for successful login"""
    success: bool = Field(..., description="Whether login was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Login data including tokens")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "data": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 3600
                }
            }
        }


# ============================================================================
# Token Refresh Schemas
# ============================================================================

class RefreshRequest(BaseModel):
    """Request schema for token refresh"""
    refresh_token: str = Field(..., min_length=10, description="JWT refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshResponse(BaseModel):
    """Response schema for token refresh"""
    success: bool = Field(..., description="Whether refresh was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="New access token data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Token refreshed successfully",
                "data": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 3600
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


# ============================================================================
# Password Reset Schemas
# ============================================================================

class PasswordResetRequestSchema(BaseModel):
    """Request schema for password reset initiation"""
    email: EmailStr = Field(..., description="User's email address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com"
            }
        }


class PasswordResetRequestResponse(BaseModel):
    """Response schema for password reset request"""
    success: bool = Field(..., description="Whether request was processed")
    message: str = Field(..., description="Human-readable message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "If the email exists, a password reset link has been sent."
            }
        }


class PasswordResetConfirmSchema(BaseModel):
    """Request schema for password reset confirmation"""
    token: str = Field(..., description="Password reset token from email")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "abc123def456",
                "new_password": "MyNewSecureP@ss123"
            }
        }


class PasswordResetConfirmResponse(BaseModel):
    """Response schema for password reset confirmation"""
    success: bool = Field(..., description="Whether password was reset")
    message: str = Field(..., description="Human-readable message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Password reset successfully. You can now log in with your new password."
            }
        }
