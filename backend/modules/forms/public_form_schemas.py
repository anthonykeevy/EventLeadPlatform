"""
Public Form Resolve Schemas (Story 3.8)
Public endpoint: GET /api/public/forms/{token}
"""
from pydantic import BaseModel, Field
from typing import Any, Dict


class PublicFormResolveResponse(BaseModel):
    link_type: str = Field(..., alias="linkType")
    definition: Dict[str, Any] = Field(..., alias="definition")

    class Config:
        populate_by_name = True

