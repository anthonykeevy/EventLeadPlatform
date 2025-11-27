"""
Public Approval Router
Handles public-facing approval endpoints (no auth required, token-protected)
Story 2.12
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from typing import Dict, Any

from common.database import get_db
from common.logger import get_logger
from models.form import Form
from modules.forms.approval_service import ApprovalService
from models.ref.form_approval_status import FormApprovalStatus

router = APIRouter(prefix="/api/public/approval", tags=["Public Approval"])
logger = get_logger(__name__)

@router.get("/{token}")
async def get_approval_context(
    token: str = Path(..., description="Approval Token"),
    db: Session = Depends(get_db)
):
    """
    Get context for an external approval request.
    Returns form details (Name, Cost, Description) for the approver to review.
    """
    service = ApprovalService(db)
    
    try:
        # Validate token and get record
        approval_token = await service.validate_approval_token(token)
        
        # Get form details
        # Use options(joinedload) to avoid lazy loading issues with Event and User
        from sqlalchemy.orm import joinedload
        from sqlalchemy import select
        
        query = select(Form).options(
            joinedload(Form.event),
            joinedload(Form.created_by_user)
        ).where(Form.FormID == approval_token.FormID)
        
        form = db.execute(query).scalar_one_or_none()
        
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
            
        # Check if still pending
        status = db.get(FormApprovalStatus, form.FormApprovalStatusID)
        if status.ApprovalStatusCode != 'PENDING':
            return {
                "valid": False,
                "message": f"This request has already been processed (Status: {status.StatusName}).",
                "status": status.ApprovalStatusCode
            }
            
        return {
            "valid": True,
            "formName": form.FormName,
            "description": form.FormDescription, # Fixed attribute name
            "deploymentCost": float(form.DeploymentCost) if form.DeploymentCost else 0.0, # Ensure float for JSON
            "eventStartDate": form.event.StartDateTime if form.event else None, # Fixed attribute access
            "requestor": f"{approval_token.creator.FirstName} {approval_token.creator.LastName}" if approval_token.creator else "Unknown",
            "status": status.ApprovalStatusCode
        }
        
    except ValueError as e:
        logger.warning(f"Invalid token access attempt: {token} - {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving approval context: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{token}/decide")
async def submit_decision(
    token: str = Path(..., description="Approval Token"),
    decision_data: Dict[str, Any] = Body(..., description="Decision data (decision, reason)"),
    db: Session = Depends(get_db)
):
    """
    Submit an approval decision via token.
    """
    service = ApprovalService(db)
    
    decision = decision_data.get("decision")
    reason = decision_data.get("reason")
    
    if not decision:
        raise HTTPException(status_code=400, detail="Decision is required")
        
    try:
        await service.decide_via_token(token, decision, reason)
        db.commit()
        
        action_verb = "approved" if decision.lower() == "approve" else "rejected"
        return {"success": True, "message": f"Request {action_verb} successfully."}
        
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting decision: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

