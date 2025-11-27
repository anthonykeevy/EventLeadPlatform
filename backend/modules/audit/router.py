"""
Audit Router
API endpoints for compliance reports and audit logs (Story 2.13)
Secured with RBAC - Only Company Admins and System Admins can access
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from .compliance_service import ComplianceService
from .schemas import (
    FormAuditReportResponse,
    EventAuditReportResponse,
    PaginatedActivityLogResponse
)
from common.logger import get_logger
from sqlalchemy import select, text

logger = get_logger(__name__)

router = APIRouter(prefix="/audit", tags=["Audit & Compliance"])


async def require_admin_or_compliance_officer(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dependency to enforce RBAC for audit endpoints.
    Only allows:
    - System Admins (global access)
    - Company Admins (access to their company's data)
    
    Returns the validated user with their company_id.
    """
    user_id = current_user.user_id
    company_id = current_user.company_id
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
        
    # Check System Admin
    is_system_admin = db.execute(
        text("""
            SELECT 1
            FROM [dbo].[User] u
            INNER JOIN ref.UserRole ur ON u.UserRoleID = ur.UserRoleID
            WHERE u.UserID = :user_id
              AND u.IsDeleted = 0
              AND ur.RoleCode = 'system_admin'
        """),
        {"user_id": user_id}
    ).fetchone()
    
    if is_system_admin:
        return {"user_id": user_id, "company_id": company_id, "is_system_admin": True}
        
    # Check Company Admin
    if not company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Company Admins and System Admins can access audit reports"
        )
        
    is_company_admin = db.execute(
        text("""
            SELECT 1
            FROM dbo.UserCompany uc
            INNER JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
            INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
            WHERE uc.UserID = :user_id
              AND uc.CompanyID = :company_id
              AND uc.IsDeleted = 0
              AND ucs.StatusCode = 'active'
              AND ucr.RoleCode = 'company_admin'
        """),
        {"user_id": user_id, "company_id": company_id}
    ).fetchone()
    
    if not is_company_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Company Admins and System Admins can access audit reports"
        )
        
    return {"user_id": user_id, "company_id": company_id, "is_system_admin": False}


@router.get(
    "/form/{form_id}",
    response_model=FormAuditReportResponse,
    summary="Get Form Compliance Report",
    description="Generate a comprehensive compliance report for a specific form. "
                "Includes metadata, approval chain, access list, and activity timeline."
)
async def get_form_audit_report(
    form_id: int,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin_or_compliance_officer)
):
    """
    Get compliance report for a form.
    
    Security: Only Company Admins (for their company) and System Admins can access.
    
    Response includes:
    - Form metadata (creator, dates, status)
    - Approval chain (who approved, including external emails and token IDs)
    - Current access list
    - Complete activity timeline
    """
    # Validate form belongs to user's company (if not system admin)
    if not admin_user["is_system_admin"]:
        from models.form import Form
        form = db.execute(
            select(Form).where(Form.FormID == form_id)
        ).scalar_one_or_none()
        
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form not found: {form_id}"
            )
            
        if form.CompanyID != admin_user["company_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Form does not belong to your company"
            )
    
    try:
        service = ComplianceService(db)
        report = await service.generate_form_audit_report(form_id)
        return report.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating form audit report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating audit report"
        )


@router.get(
    "/event/{event_id}",
    response_model=EventAuditReportResponse,
    summary="Get Event Compliance Report",
    description="Generate a comprehensive compliance report for a specific event. "
                "Includes all associated forms and their activity."
)
async def get_event_audit_report(
    event_id: int,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin_or_compliance_officer)
):
    """
    Get compliance report for an event.
    
    Security: Only Company Admins (for their company) and System Admins can access.
    
    Response includes:
    - Event metadata
    - Form count
    - Combined activity timeline (event + all forms)
    """
    # Validate event belongs to user's company (if not system admin)
    if not admin_user["is_system_admin"]:
        from models.event import Event
        event = db.execute(
            select(Event).where(Event.EventID == event_id)
        ).scalar_one_or_none()
        
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event not found: {event_id}"
            )
            
        if event.CompanyID != admin_user["company_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Event does not belong to your company"
            )
    
    try:
        service = ComplianceService(db)
        report = await service.generate_event_audit_report(event_id)
        return report.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating event audit report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating audit report"
        )


@router.get(
    "/company/activity",
    response_model=PaginatedActivityLogResponse,
    summary="Get Company Activity Log",
    description="Get paginated activity log for the company. "
                "Supports filtering by entity type, action, user, form, and event. "
                "System Admins can optionally specify company_id to filter, or see all activity."
)
async def get_company_activity_log(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(50, ge=10, le=100, description="Items per page"),
    entity_type: str = Query(None, description="Filter by entity type (Form, Event, etc.)"),
    action_filter: str = Query(None, description="Filter by action code"),
    company_id_filter: int = Query(None, description="Filter by company ID (System Admin only)"),
    user_id_filter: int = Query(None, description="Filter by user ID"),
    form_id_filter: int = Query(None, description="Filter by form ID"),
    event_id_filter: int = Query(None, description="Filter by event ID"),
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin_or_compliance_officer)
):
    """
    Get paginated activity log for the company.
    
    Security: Only Company Admins (for their company) and System Admins can access.
    
    Query Parameters:
    - page: Page number (1-based)
    - page_size: Items per page (10-100)
    - entity_type: Filter by entity type (Form, Event, User, etc.)
    - action_filter: Filter by action code (e.g., 'approved', 'created')
    - company_id_filter: (System Admin only) Filter by specific company ID
    - user_id_filter: Filter by user ID
    - form_id_filter: Filter by form ID
    - event_id_filter: Filter by event ID (includes all forms for that event)
    
    For System Admins:
    - If company_id_filter is provided: Returns activity for that company
    - If no filter provided: Returns ALL activity across all companies
    
    For Company Admins:
    - Returns activity only for their company
    """
    is_system_admin = admin_user.get("is_system_admin", False)
    company_id = admin_user.get("company_id")
    
    # Determine which company to query
    if is_system_admin:
        # System admin can filter by company or see all
        target_company_id = company_id_filter  # None means all companies
    else:
        # Company admin must use their own company
        if not company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company ID required for activity log"
            )
        target_company_id = company_id
    
    try:
        service = ComplianceService(db)
        result = await service.get_company_activity_log(
            company_id=target_company_id,  # None for system admin = all companies
            page=page,
            page_size=page_size,
            entity_type=entity_type,
            action_filter=action_filter,
            user_id_filter=user_id_filter,
            form_id_filter=form_id_filter,
            event_id_filter=event_id_filter
        )
        return result
    except Exception as e:
        logger.error(f"Error getting company activity log: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving activity log"
        )

