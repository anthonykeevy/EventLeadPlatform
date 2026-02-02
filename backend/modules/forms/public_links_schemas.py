"""
Public Form Link Schemas (Story 3.8)
Token-based public renderer links: /forms/:token
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PublicLinkType:
    PREVIEW = "PREVIEW"
    PRODUCTION = "PRODUCTION"


class CreatePublicLinkRequest(BaseModel):
    link_type: str = Field(..., alias="linkType", description="PREVIEW or PRODUCTION")
    expires_at: Optional[datetime] = Field(None, alias="expiresAt", description="Optional expiration (UTC)")

    class Config:
        populate_by_name = True


class PublicLinkResponse(BaseModel):
    token: str = Field(..., alias="token")
    link_type: str = Field(..., alias="linkType")
    url: str = Field(..., alias="url")
    is_active: bool = Field(..., alias="isActive")
    expires_at: Optional[datetime] = Field(None, alias="expiresAt")
    created_date: datetime = Field(..., alias="createdDate")
    last_accessed_at: Optional[datetime] = Field(None, alias="lastAccessedAt")

    class Config:
        populate_by_name = True


class CreatePublicLinkResponse(BaseModel):
    success: bool = Field(..., alias="success")
    message: str = Field(..., alias="message")
    link: PublicLinkResponse = Field(..., alias="link")

    class Config:
        populate_by_name = True


class ListPublicLinksResponse(BaseModel):
    links: List[PublicLinkResponse] = Field(..., alias="links")
    total: int = Field(..., alias="total")

    class Config:
        populate_by_name = True


class RevokePublicLinkResponse(BaseModel):
    success: bool = Field(..., alias="success")
    message: str = Field(..., alias="message")
    token: str = Field(..., alias="token")

    class Config:
        populate_by_name = True

