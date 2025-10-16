"""
Authentication Models
Pydantic models for authentication and current user context
"""
from pydantic import BaseModel
from typing import Optional


class CurrentUser(BaseModel):
    """
    Current authenticated user extracted from JWT.
    
    This model represents the authenticated user's identity and context
    throughout the request lifecycle. Injected by JWTAuthMiddleware.
    
    Attributes:
        user_id: Unique user identifier
        email: User email address
        role: User role (company_admin, company_user, platform_admin, etc.)
        company_id: Active company ID for multi-tenant context
    """
    user_id: int
    email: str
    role: Optional[str] = None
    company_id: Optional[int] = None
    
    class Config:
        frozen = True  # Immutable after creation
        schema_extra = {
            "example": {
                "user_id": 123,
                "email": "john.doe@example.com",
                "role": "company_admin",
                "company_id": 456
            }
        }

