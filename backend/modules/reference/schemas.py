"""Reference API schemas (Story 6.5d)."""
from typing import List, Optional

from pydantic import BaseModel, Field


class RefClarificationItem(BaseModel):
    code: str
    displayName: str
    description: Optional[str] = None
    flagEmoji: Optional[str] = None
    promptHint: Optional[str] = None
    clarificationSummary: Optional[str] = None


class RefClarificationListResponse(BaseModel):
    items: List[RefClarificationItem]
    defaultCode: str
    resolvedDefault: RefClarificationItem


class RefListQuery(BaseModel):
    formId: Optional[int] = Field(default=None, ge=1)
    code: Optional[str] = Field(default=None, max_length=50)
