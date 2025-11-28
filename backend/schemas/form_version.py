"""
Form Version Schemas
Pydantic models for form versioning
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict, List
from datetime import datetime
from enum import Enum

class VersionStatus(str, Enum):
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    ARCHIVED = 'ARCHIVED'

class FormVersionBase(BaseModel):
    definition: Dict[str, Any] = Field(..., description="The complete form schema")
    version_comment: Optional[str] = Field(None, max_length=500, alias="versionComment", description="Optional comment describing changes")

class FormVersionCreate(FormVersionBase):
    """Schema for creating a new form version"""
    pass

class FormVersionUpdate(BaseModel):
    """Schema for updating a draft version"""
    definition: Dict[str, Any] = Field(..., description="The complete form schema")
    version_comment: Optional[str] = Field(None, max_length=500, alias="versionComment")

class FormVersionResponse(FormVersionBase):
    """Response schema for form version"""
    form_version_id: int = Field(..., alias="formVersionId")
    form_id: int = Field(..., alias="formId")
    version_number: int = Field(..., alias="versionNumber")
    status: str = Field(..., description="DRAFT, PUBLISHED, ARCHIVED")
    is_active: bool = Field(..., alias="isActive")
    created_date: datetime = Field(..., alias="createdDate")
    created_by: Optional[int] = Field(None, alias="createdBy")
    published_date: Optional[datetime] = Field(None, alias="publishedDate")
    published_by: Optional[int] = Field(None, alias="publishedBy")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class FormVersionListResponse(BaseModel):
    """List of form versions"""
    versions: List[FormVersionResponse] = Field(..., alias="versions")
    
    model_config = ConfigDict(
        populate_by_name=True
    )

