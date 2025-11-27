"""
Audit Schemas
Pydantic models for audit API responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AuditEntryResponse(BaseModel):
    """Single audit entry"""
    timestamp: Optional[str]
    action: str
    action_display: str
    user_id: Optional[int]
    user_email: Optional[str]
    user_name: Optional[str]
    is_external: bool
    details: Optional[str]
    old_value: Optional[str] = None  # Structured old values for table display
    new_value: Optional[str] = None  # Structured new values for table display
    token_id: Optional[int] = None
    # Additional context fields for Activity Log table
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    form_name: Optional[str] = None
    event_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class ApprovalChainEntryResponse(BaseModel):
    """Approval chain entry"""
    approver_id: Optional[int]
    approver_email: str
    approver_name: Optional[str]
    is_external: bool
    decision: str
    decided_at: Optional[str]
    token_id: Optional[int]
    reason: Optional[str]
    
    class Config:
        from_attributes = True


class AccessEntryResponse(BaseModel):
    """Access entry"""
    user_id: int
    user_email: str
    user_name: str
    access_type: str
    access_type_display: str
    granted_by_id: int
    granted_by_name: str
    granted_at: Optional[str]
    expires_at: Optional[str]
    
    class Config:
        from_attributes = True


class FormMetadataResponse(BaseModel):
    """Form metadata"""
    form_id: int
    form_name: str
    form_description: Optional[str]
    created_by_id: int
    created_by_email: str
    created_by_name: str
    created_at: Optional[str]
    current_status: str
    current_approval_status: str
    deployment_cost: Optional[float]
    company_id: int
    company_name: str
    event_id: Optional[int]
    event_name: Optional[str]
    
    class Config:
        from_attributes = True


class FormAuditReportResponse(BaseModel):
    """Form audit report response"""
    report_generated_at: str
    form_metadata: FormMetadataResponse
    approval_chain: List[ApprovalChainEntryResponse]
    current_access_list: List[AccessEntryResponse]
    activity_timeline: List[AuditEntryResponse]
    
    class Config:
        from_attributes = True


class EventAuditReportResponse(BaseModel):
    """Event audit report response"""
    report_generated_at: str
    event_id: int
    event_name: str
    company_id: int
    company_name: str
    created_by_id: int
    created_by_name: str
    created_at: Optional[str]
    current_status: str
    forms_count: int
    activity_timeline: List[AuditEntryResponse]
    
    class Config:
        from_attributes = True


class PaginatedActivityLogResponse(BaseModel):
    """Paginated activity log response"""
    items: List[AuditEntryResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    
    class Config:
        from_attributes = True

