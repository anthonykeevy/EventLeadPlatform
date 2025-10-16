"""
Company Management Schemas
Pydantic models for company requests/responses
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


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

