"""
Form Defaults API Schemas (Story 5.2)
Pydantic models for request/response
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Request schemas ---

class UpdateFormDefaultsRequest(BaseModel):
    """Body for PUT global or company defaults."""
    defaults: Dict[str, Any] = Field(..., description="DefaultsJSON: theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent")
    changeSummary: Optional[str] = Field(None, max_length=500, description="Optional change summary for audit trail")


# --- Response schemas ---

class FormDefaultsResponse(BaseModel):
    """Merged or single-tier defaults payload."""
    defaults: Dict[str, Any] = Field(..., description="theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent")
    versionNumber: Optional[int] = Field(None, description="Current version number when applicable")

    class Config:
        from_attributes = True


class FormDefaultsVersionEntry(BaseModel):
    """Single entry in version history."""
    versionNumber: int
    defaults: Dict[str, Any]
    changeSummary: Optional[str] = None
    createdDate: str
    createdBy: Optional[int] = None

    class Config:
        from_attributes = True


class FormDefaultsHistoryResponse(BaseModel):
    """Version history list."""
    items: List[FormDefaultsVersionEntry]
    total: int
