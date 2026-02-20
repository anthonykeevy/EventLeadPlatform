"""
Public Form Resolve Schemas (Story 3.8, 5.8)
Public endpoint: GET /api/public/forms/{token}
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class PublicFormResolveResponse(BaseModel):
    link_type: str = Field(..., alias="linkType")  # PREVIEW | PRODUCTION | UNPUBLISHED | EVENT_ENDED
    definition: Optional[Dict[str, Any]] = Field(None, alias="definition")
    message: Optional[str] = Field(None, alias="message")

    class Config:
        populate_by_name = True

