"""
Forms Module Schemas
Pydantic models for form requests/responses
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal


# =====================================================================
# Reference Data Schemas
# =====================================================================

class FormStatusResponse(BaseModel):
    """Form status reference data"""
    form_status_id: int = Field(..., alias="formStatusId")
    status_code: str = Field(..., alias="statusCode")
    status_name: str = Field(..., alias="statusName")
    status_description: Optional[str] = Field(None, alias="statusDescription")
    status_color: Optional[str] = Field(None, alias="statusColor")
    status_icon: Optional[str] = Field(None, alias="statusIcon")
    is_active: bool = Field(..., alias="isActive")
    sort_order: int = Field(..., alias="sortOrder")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "form_status_id": 1,
                "status_code": "DRAFT",
                "status_name": "Draft",
                "status_description": "Form is being created and edited",
                "status_color": "#FFA500",
                "status_icon": "draft-icon",
                "is_active": True,
                "sort_order": 1
            }
        }


class FormApprovalStatusResponse(BaseModel):
    """Form approval status reference data"""
    form_approval_status_id: int = Field(..., alias="formApprovalStatusId")
    approval_status_code: str = Field(..., alias="approvalStatusCode")
    approval_status_name: str = Field(..., alias="approvalStatusName")
    approval_status_description: Optional[str] = Field(None, alias="approvalStatusDescription")
    is_requires_approval: bool = Field(..., alias="isRequiresApproval")
    is_active: bool = Field(..., alias="isActive")
    sort_order: int = Field(..., alias="sortOrder")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "form_approval_status_id": 1,
                "approval_status_code": "NO_APPROVAL",
                "approval_status_name": "No Approval Required",
                "approval_status_description": "Form can be deployed without approval",
                "is_requires_approval": False,
                "is_active": True,
                "sort_order": 1
            }
        }


# =====================================================================
# Request Schemas
# =====================================================================

class FormCreateSchema(BaseModel):
    """Schema for creating a new form"""
    form_name: str = Field(..., min_length=1, max_length=200, alias="formName")
    form_description: Optional[str] = Field(None, alias="formDescription")
    event_id: Optional[int] = Field(None, alias="eventId")
    form_status_id: int = Field(..., alias="formStatusId")
    form_approval_status_id: int = Field(..., alias="formApprovalStatusId")
    is_public: bool = Field(False, alias="isPublic")
    deployment_cost: Optional[Decimal] = Field(None, ge=0, alias="deploymentCost")
    form_thumbnail_url: Optional[str] = Field(None, max_length=500, alias="formThumbnailUrl")
    form_preview_url: Optional[str] = Field(None, max_length=500, alias="formPreviewUrl")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "formName": "Customer Feedback Survey",
                "formDescription": "Collect feedback from customers after event attendance",
                "eventId": 1,
                "formStatusId": 1,
                "formApprovalStatusId": 1,
                "isPublic": False,
                "deploymentCost": 0.00,
                "formThumbnailUrl": "https://cdn.eventlead.com/thumbnails/form_123.png",
                "formPreviewUrl": "https://eventlead.com/preview/form/123"
            }
        }


class FormUpdateSchema(BaseModel):
    """Schema for updating an existing form"""
    form_name: Optional[str] = Field(None, min_length=1, max_length=200, alias="formName")
    form_description: Optional[str] = Field(None, alias="formDescription")
    event_id: Optional[int] = Field(None, alias="eventId")
    form_status_id: Optional[int] = Field(None, alias="formStatusId")
    form_approval_status_id: Optional[int] = Field(None, alias="formApprovalStatusId")
    is_public: Optional[bool] = Field(None, alias="isPublic")
    deployment_cost: Optional[Decimal] = Field(None, ge=0, alias="deploymentCost")
    form_thumbnail_url: Optional[str] = Field(None, max_length=500, alias="formThumbnailUrl")
    form_preview_url: Optional[str] = Field(None, max_length=500, alias="formPreviewUrl")
    
    class Config:
        populate_by_name = True


class TransferFormOwnershipRequest(BaseModel):
    """Request schema for bulk transfer of form ownership"""
    from_user_id: int = Field(..., alias="from_user_id")
    to_user_id: int = Field(..., alias="to_user_id")
    company_id: int = Field(..., alias="company_id")
    reason: Optional[str] = Field(None, alias="reason")
    
    class Config:
        populate_by_name = True


class RejectFormRequest(BaseModel):
    """Schema for rejecting a form"""
    reason: str = Field(..., min_length=1, max_length=500, alias="reason")
    
    class Config:
        populate_by_name = True


class ExternalApprovalRequest(BaseModel):
    """Schema for requesting external approval"""
    email: str = Field(..., min_length=5, max_length=255, alias="email")
    
    class Config:
        populate_by_name = True


class TransferFormOwnershipResponse(BaseModel):
    """Response for bulk transfer of form ownership"""
    success: bool = Field(..., alias="success")
    message: str = Field(..., alias="message")
    forms_transferred: int = Field(..., alias="forms_transferred")
    access_controls_transferred: int = Field(..., alias="access_controls_transferred")
    status: str = Field(..., alias="status")
    
    class Config:
        populate_by_name = True


# =====================================================================
# Response Schemas
# =====================================================================

class FormResponse(BaseModel):
    """Form response with all metadata"""
    form_id: int = Field(..., alias="formId")
    form_name: str = Field(..., alias="formName")
    form_description: Optional[str] = Field(None, alias="formDescription")
    company_id: int = Field(..., alias="companyId")
    event_id: Optional[int] = Field(None, alias="eventId")
    form_status_id: int = Field(..., alias="formStatusId")
    form_status: Optional[FormStatusResponse] = Field(None, alias="formStatus")
    form_approval_status_id: int = Field(..., alias="formApprovalStatusId")
    form_approval_status: Optional[FormApprovalStatusResponse] = Field(None, alias="formApprovalStatus")
    is_public: bool = Field(..., alias="isPublic")
    deployment_cost: Optional[Decimal] = Field(None, alias="deploymentCost")
    total_submissions: int = Field(..., alias="totalSubmissions")
    demo_leads_collected: int = Field(..., alias="demoLeadsCollected")
    production_leads_collected: int = Field(..., alias="productionLeadsCollected")
    last_submission_date: Optional[datetime] = Field(None, alias="lastSubmissionDate")
    last_activity_date: Optional[datetime] = Field(None, alias="lastActivityDate")
    form_thumbnail_url: Optional[str] = Field(None, alias="formThumbnailUrl")
    form_preview_url: Optional[str] = Field(None, alias="formPreviewUrl")
    created_date: datetime = Field(..., alias="createdDate")
    created_by: int = Field(..., alias="createdBy")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate")
    updated_by: Optional[int] = Field(None, alias="updatedBy")
    
    class Config:
        populate_by_name = True
        from_attributes = True


class FormListResponse(BaseModel):
    """Paginated list of forms"""
    forms: List[FormResponse] = Field(..., alias="forms")
    total: int = Field(..., alias="total")
    page: int = Field(..., alias="page")
    page_size: int = Field(..., alias="pageSize")
    
    class Config:
        populate_by_name = True


class CreateFormResponse(BaseModel):
    """Response for form creation"""
    success: bool = Field(..., alias="success")
    message: str = Field(..., alias="message")
    form_id: int = Field(..., alias="formId")
    form: FormResponse = Field(..., alias="form")
    
    class Config:
        populate_by_name = True


class UpdateFormResponse(BaseModel):
    """Response for form update"""
    success: bool = Field(..., alias="success")
    message: str = Field(..., alias="message")
    form_id: int = Field(..., alias="formId")
    form: FormResponse = Field(..., alias="form")
    
    class Config:
        populate_by_name = True


class DeleteFormResponse(BaseModel):
    """Response for form deletion"""
    success: bool = Field(..., alias="success")
    message: str = Field(..., alias="message")
    form_id: int = Field(..., alias="formId")
    
    class Config:
        populate_by_name = True


class ExternalApprovalResponse(BaseModel):
    """Response for external approval request"""
    success: bool = Field(..., alias="success")
    message: str = Field(..., alias="message")
    token: str = Field(..., alias="token")
    email: str = Field(..., alias="email")
    
    class Config:
        populate_by_name = True
