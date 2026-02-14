"""
Form Builder Init API Schemas (Story 5.2 T03)
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FormBuilderInitRequest(BaseModel):
    """Body for POST /api/form-builder/init."""
    companyId: int = Field(..., ge=1, description="Company ID")
    eventId: int = Field(..., ge=1, description="Event ID")


class FormBuilderInitContext(BaseModel):
    """Context echoed back (companyId, eventId, countryId)."""
    companyId: int
    eventId: int
    countryId: Optional[int] = None


class FormBuilderComponentItem(BaseModel):
    """Single component in the catalog."""
    componentCode: str
    displayName: str
    category: Optional[str] = None
    sortOrder: int = 0
    propertiesSchema: Optional[Dict[str, Any]] = None
    structure: Optional[Dict[str, Any]] = None
    defaultGridLayoutVertical: Optional[Dict[str, Any]] = None
    defaultGridLayoutHorizontal: Optional[Dict[str, Any]] = None
    validationConfig: Optional[Dict[str, Any]] = None


class FormBuilderDefinitionJSON(BaseModel):
    """Initial DefinitionJSON skeleton."""
    schemaVersion: int = 1
    theme: Optional[Dict[str, Any]] = None
    globalStyles: Optional[Dict[str, Any]] = None
    canvasSettings: Optional[Dict[str, Any]] = None
    pages: List[Dict[str, Any]] = Field(default_factory=lambda: [{"id": "page-1", "components": []}])
    logic: List[Any] = Field(default_factory=list)


class FormBuilderInitResponse(BaseModel):
    """Response for POST /api/form-builder/init."""
    schemaVersion: int
    context: FormBuilderInitContext
    defaults: Dict[str, Any]
    components: List[FormBuilderComponentItem]
    definitionJSON: FormBuilderDefinitionJSON
