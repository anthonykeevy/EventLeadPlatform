"""
Form Ownership Transfer Router
API endpoints for bulk form ownership transfer operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from .ownership_service import transfer_form_ownership
from common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/forms/ownership", tags=["Form Ownership"])


class TransferOwnershipRequest(BaseModel):
    """Request model for form ownership transfer"""
    from_user_id: int = Field(..., description="User ID to transfer ownership FROM")
    to_user_id: int = Field(..., description="User ID to transfer ownership TO")
    company_id: int = Field(..., description="Company ID (must match company of both users)")
    reason: Optional[str] = Field(None, description="Optional reason for transfer")
    
    class Config:
        json_schema_extra = {
            "example": {
                "from_user_id": 123,
                "to_user_id": 456,
                "company_id": 789,
                "reason": "Bulk ownership transfer on offboarding - user leaving company"
            }
        }


class TransferOwnershipResponse(BaseModel):
    """Response model for form ownership transfer"""
    forms_transferred: int = Field(..., description="Number of forms transferred")
    access_controls_transferred: int = Field(..., description="Number of access control entries transferred")
    status: str = Field(..., description="Transfer status")
    message: str = Field(..., description="Transfer message")
    success: bool = Field(..., description="Whether transfer was successful")
    
    class Config:
        json_schema_extra = {
            "example": {
                "forms_transferred": 15,
                "access_controls_transferred": 8,
                "status": "SUCCESS",
                "message": "Ownership transfer completed successfully",
                "success": True
            }
        }


@router.post("/transfer", response_model=TransferOwnershipResponse, status_code=status.HTTP_200_OK)
async def transfer_ownership(
    request: TransferOwnershipRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transfer form ownership from one user to another within a company.
    
    **Permissions Required:**
    - Company Admin for the specified company, OR
    - System Admin (global override)
    
    **What it does:**
    - Updates `Form.CreatedBy` for all forms owned by `from_user_id` in the company
    - Updates `FormAccessControl.UserID` entries for transferred forms
    - Creates audit trail records in `audit.ActivityLog`
    
    **Use Cases:**
    - Off-boarding: Transfer all forms from a departing user to another team member
    - Role change: Reassign forms when a user changes roles
    - Bulk reassignment: Consolidate form ownership within a company
    
    **Args:**
    - `from_user_id`: User ID to transfer ownership FROM
    - `to_user_id`: User ID to transfer ownership TO
    - `company_id`: Company ID (must match company of both users)
    - `reason`: Optional reason for transfer (e.g., "Bulk ownership transfer on offboarding")
    
    **Returns:**
    - Number of forms transferred
    - Number of access control entries transferred
    - Transfer status and message
    """
    logger.info(
        f"Ownership transfer request: FromUserID={request.from_user_id}, "
        f"ToUserID={request.to_user_id}, CompanyID={request.company_id}, "
        f"PerformedBy={current_user.user_id}"
    )
    
    try:
        result = await transfer_form_ownership(
            db=db,
            from_user_id=request.from_user_id,
            to_user_id=request.to_user_id,
            company_id=request.company_id,
            performed_by=current_user.user_id,
            reason=request.reason
        )
        
        return TransferOwnershipResponse(
            forms_transferred=result["FormsTransferred"],
            access_controls_transferred=result["AccessControlsTransferred"],
            status=result.get("Status", "SUCCESS"),
            message=result.get("Message", "Ownership transfer completed successfully"),
            success=result["Success"]
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (already have proper status codes)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in ownership transfer endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error transferring form ownership: {str(e)}"
        )

