"""
Logging Schemas
Request/Response models for frontend logging integration
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class FrontendLogEntry(BaseModel):
    """Single frontend log entry"""
    ts: int = Field(..., description="Unix timestamp from frontend")
    level: str = Field(..., description="Log level: debug, info, warn, error")
    event: str = Field(..., description="Event type (e.g., 'smartborder.drag.state')")
    payload: Optional[Dict[str, Any]] = Field(None, description="Event payload")
    
    class Config:
        extra = "allow"


class FrontendLogBatch(BaseModel):
    """Batch of frontend log entries"""
    entries: List[FrontendLogEntry] = Field(..., description="Array of log entries")
    sessionId: str = Field(..., description="Browser session identifier")
    pageUrl: Optional[str] = Field(None, description="Current page URL")
    browserInfo: Optional[str] = Field(None, description="Browser/user agent info")


class FrontendLogResponse(BaseModel):
    """Response after logging entries"""
    received: int = Field(..., description="Number of entries received")
    stored: int = Field(..., description="Number of entries stored")
    message: str = Field("OK", description="Status message")











