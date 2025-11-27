"""
Form Management Router
Endpoints for form CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from models.form import Form
from .schemas import (
    FormCreateSchema,
    FormUpdateSchema,
    FormResponse,
    FormListResponse,
    CreateFormResponse,
    UpdateFormResponse,
    DeleteFormResponse,
    FormStatusResponse,
    FormApprovalStatusResponse,
    TransferFormOwnershipRequest,
    TransferFormOwnershipResponse,
    RejectFormRequest,
    ExternalApprovalRequest,
    ExternalApprovalResponse
)
from .service import (
    create_form,
    get_forms,
    get_form_by_id,
    update_form,
    delete_form,
    get_forms_by_event,
    get_form_statuses,
    get_form_approval_statuses,
    transfer_form_ownership
)
from .approval_service import ApprovalService
from common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/forms", tags=["forms"])


# =====================================================================
# Reference Data Endpoints
# =====================================================================

@router.get(
    "/statuses",
    response_model=List[FormStatusResponse],
    summary="Get form statuses",
    description="Get all active form statuses for dropdown selections"
)
async def get_reference_form_statuses(db: Session = Depends(get_db)) -> List[FormStatusResponse]:
    """Get all active form statuses for selection."""
    try:
        form_statuses = await get_form_statuses(db)
        return [
            FormStatusResponse(
                form_status_id=int(fs.FormStatusID),
                status_code=str(fs.StatusCode),
                status_name=str(fs.StatusName),
                status_description=str(fs.StatusDescription) if fs.StatusDescription else None,
                status_color=str(fs.StatusColor) if fs.StatusColor else None,
                status_icon=str(fs.StatusIcon) if fs.StatusIcon else None,
                is_active=bool(fs.IsActive),
                sort_order=int(fs.SortOrder)
            )
            for fs in form_statuses
        ]
    except Exception as e:
        logger.error(f"Error fetching form statuses: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch form statuses"
        )


@router.get(
    "/approval-statuses",
    response_model=List[FormApprovalStatusResponse],
    summary="Get form approval statuses",
    description="Get all active form approval statuses for dropdown selections"
)
async def get_reference_form_approval_statuses(db: Session = Depends(get_db)) -> List[FormApprovalStatusResponse]:
    """Get all active form approval statuses for selection."""
    try:
        form_approval_statuses = await get_form_approval_statuses(db)
        return [
            FormApprovalStatusResponse(
                form_approval_status_id=int(fas.FormApprovalStatusID),
                approval_status_code=str(fas.ApprovalStatusCode),
                approval_status_name=str(fas.ApprovalStatusName),
                approval_status_description=str(fas.ApprovalStatusDescription) if fas.ApprovalStatusDescription else None,
                is_requires_approval=bool(fas.IsRequiresApproval),
                is_active=bool(fas.IsActive),
                sort_order=int(fas.SortOrder)
            )
            for fas in form_approval_statuses
        ]
    except Exception as e:
        logger.error(f"Error fetching form approval statuses: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch form approval statuses"
        )


# =====================================================================
# CRUD Endpoints
# =====================================================================

@router.post(
    "",
    response_model=CreateFormResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create form",
    description="Create a new form header for the company"
)
async def create_new_form(
    request: FormCreateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CreateFormResponse:
    """
    Create a new form header for the company (AC-2.8.1, AC-2.8.2, AC-2.8.3, AC-2.8.4).
    
    Requires authentication and company context.
    Validates required fields and reference data.
    """
    try:
        # Convert Pydantic model to dict for service layer
        # Pydantic with populate_by_name=True already converts camelCase to snake_case
        form_data = request.dict(exclude_none=True)
        
        # Create form
        form = await create_form(
            db=db,
            user_id=current_user.user_id,
            company_id=current_user.company_id,
            form_data=form_data
        )
        
        db.commit()
        db.refresh(form)
        
        # Convert to response model
        form_response = _form_to_response(form)
        
        logger.info(f"Form created successfully: FormID={form.FormID}")
        
        return CreateFormResponse(
            success=True,
            message="Form created successfully",
            formId=form.FormID,
            form=form_response
        )
        
    except ValueError as e:
        logger.warning(f"Invalid form creation request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_detail = str(e)
        logger.error(f"Error creating form: {error_detail}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create form: {error_detail}"
        )


@router.get(
    "",
    response_model=FormListResponse,
    summary="List company forms",
    description="Get all forms for the company with optional filters"
)
async def list_company_forms(
    form_status_id: Optional[int] = Query(None, description="Filter by form status"),
    event_id: Optional[int] = Query(None, description="Filter by event"),
    search: Optional[str] = Query(None, description="Search by name/description"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FormListResponse:
    """
    List all forms for the company with optional filters (AC-2.8.5, AC-2.8.6, AC-2.8.12).
    
    Requires authentication and company context.
    Automatically filters by CompanyID for multi-tenant isolation.
    
    System Admins: Returns ALL forms in the platform (bypasses company filtering)
    """
    try:
        # Build filters dict
        filters = {}
        if form_status_id:
            filters['form_status_id'] = form_status_id
        if event_id:
            filters['event_id'] = event_id
        if search:
            filters['search'] = search
        
        # System Admins see ALL forms, not just company forms
        if current_user.role == "system_admin":
            from models.form import Form
            from sqlalchemy import select
            from sqlalchemy.orm import joinedload
            
            # Get all forms (bypass company filtering)
            query = db.query(Form).options(
                joinedload(Form.form_status),
                joinedload(Form.form_approval_status),
                joinedload(Form.company),
                joinedload(Form.event)
            ).filter(Form.IsDeleted == False)
            
            # Apply filters
            if filters.get('form_status_id'):
                query = query.filter(Form.FormStatusID == filters['form_status_id'])
            if filters.get('event_id'):
                query = query.filter(Form.EventID == filters['event_id'])
            if filters.get('search'):
                from sqlalchemy import or_
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        Form.FormName.like(search_term),
                        Form.FormDescription.like(search_term)
                    )
                )
            
            forms = query.order_by(Form.CreatedDate.desc()).all()
            
            logger.info(f"System Admin {current_user.user_id} viewing all {len(forms)} forms")
        else:
            # Regular users: Get forms (with access filtering)
            forms = await get_forms(
                db=db,
                company_id=current_user.company_id,
                user_id=current_user.user_id,
                filters=filters
            )
        
        # Convert to response models
        form_responses = [_form_to_response(f) for f in forms]
        
        logger.info(f"Retrieved {len(form_responses)} forms for CompanyID={current_user.company_id}")
        
        return FormListResponse(
            forms=form_responses,
            total=len(form_responses),
            page=page,
            pageSize=page_size
        )
        
    except Exception as e:
        logger.error(f"Error listing forms: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list forms"
        )


@router.get(
    "/{form_id}",
    response_model=FormResponse,
    summary="Get form details",
    description="Get a single form by ID"
)
async def get_form_details(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FormResponse:
    """
    Get a single form by ID (AC-2.8.13).
    
    Requires authentication and company context.
    Verifies form belongs to company.
    """
    try:
        form = await get_form_by_id(
            db=db,
            form_id=form_id,
            company_id=current_user.company_id,
            user_id=current_user.user_id
        )
        
        if not form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Form not found: {form_id}"
            )
        
        form_response = _form_to_response(form)
        
        logger.info(f"Retrieved form: FormID={form_id}")
        
        return form_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching form: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch form"
        )


@router.put(
    "/{form_id}",
    response_model=UpdateFormResponse,
    summary="Update form",
    description="Update an existing form header"
)
async def update_existing_form(
    form_id: int,
    request: FormUpdateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UpdateFormResponse:
    """
    Update an existing form (AC-2.8.5).
    
    Requires authentication and company context.
    Verifies form belongs to company.
    """
    try:
        # Convert Pydantic model to dict for service layer
        # Pydantic with populate_by_name=True already converts camelCase to snake_case
        form_data = request.dict(exclude_none=True)
        
        # Update form
        form = await update_form(
            db=db,
            form_id=form_id,
            company_id=current_user.company_id,
            user_id=current_user.user_id,
            form_data=form_data
        )
        
        db.commit()
        db.refresh(form)
        
        form_response = _form_to_response(form)
        
        logger.info(f"Form updated successfully: FormID={form_id}")
        
        return UpdateFormResponse(
            success=True,
            message="Form updated successfully",
            formId=form_id,
            form=form_response
        )
        
    except ValueError as e:
        logger.warning(f"Invalid form update request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating form: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update form"
        )


@router.delete(
    "/{form_id}",
    response_model=DeleteFormResponse,
    summary="Delete form",
    description="Soft delete a form (sets IsDeleted flag)"
)
async def delete_existing_form(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> DeleteFormResponse:
    """
    Soft delete a form (AC-2.8.14).
    
    Requires authentication and company context.
    Verifies form belongs to company.
    """
    try:
        await delete_form(
            db=db,
            form_id=form_id,
            company_id=current_user.company_id,
            user_id=current_user.user_id
        )
        
        db.commit()
        
        logger.info(f"Form deleted successfully: FormID={form_id}")
        
        return DeleteFormResponse(
            success=True,
            message="Form deleted successfully",
            formId=form_id
        )
        
    except ValueError as e:
        logger.warning(f"Invalid form deletion request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting form: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete form"
        )


@router.post(
    "/ownership/transfer",
    response_model=TransferFormOwnershipResponse,
    summary="Transfer form ownership",
    description="Transfer all forms from one user to another (Bulk Ownership Transfer)"
)
async def transfer_ownership(
    request: TransferFormOwnershipRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TransferFormOwnershipResponse:
    """
    Transfer all forms from one user to another (AC-2.10.4).
    
    Requires 'company_admin' role.
    Both users must belong to the same company.
    """
    try:
        # Verify permission (Company Admin only)
        if current_user.role != 'company_admin' and current_user.role != 'system_admin':
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Company Administrators can transfer form ownership"
            )
            
        # Verify company context matches request
        if current_user.role != 'system_admin' and request.company_id != current_user.company_id:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only transfer ownership within your own company"
            )

        # Perform transfer
        result = await transfer_form_ownership(
            db=db,
            from_user_id=request.from_user_id,
            to_user_id=request.to_user_id,
            company_id=request.company_id,
            admin_user_id=current_user.user_id,
            reason=request.reason
        )
        
        db.commit()
        
        logger.info(f"Form ownership transfer complete: {result['forms_transferred']} forms transferred from {request.from_user_id} to {request.to_user_id}")
        
        return TransferFormOwnershipResponse(
            success=True,
            message="Ownership transferred successfully",
            forms_transferred=result['forms_transferred'],
            access_controls_transferred=result['access_controls_transferred'],
            status="completed"
        )
        
    except ValueError as e:
        logger.warning(f"Invalid transfer request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error transferring ownership: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to transfer ownership"
        )


@router.get(
    "/event/{event_id}",
    response_model=FormListResponse,
    summary="Get forms by event",
    description="Get all forms associated with a specific event"
)
async def get_forms_for_event(
    event_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FormListResponse:
    """
    Get all forms for a specific event (AC-2.8.8).
    
    Requires authentication and company context.
    Only returns forms for events belonging to the company.
    """
    try:
        forms = await get_forms_by_event(
            db=db,
            event_id=event_id,
            company_id=current_user.company_id
        )
        
        form_responses = [_form_to_response(f) for f in forms]
        
        logger.info(f"Retrieved {len(form_responses)} forms for EventID={event_id}")
        
        return FormListResponse(
            forms=form_responses,
            total=len(form_responses),
            page=1,
            pageSize=len(form_responses)
        )
        
    except Exception as e:
        logger.error(f"Error fetching forms for event: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch forms for event"
        )


@router.post(
    "/{form_id}/submit",
    response_model=UpdateFormResponse,
    summary="Submit form for approval",
    description="Submit a form for approval (triggers PENDING status if cost > threshold)"
)
async def submit_form_for_approval(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UpdateFormResponse:
    """
    Submit form for approval (AC-2.11.2).
    """
    try:
        service = ApprovalService(db)
        form = await service.submit_for_approval(
            form_id=form_id,
            user_id=current_user.user_id,
            company_id=current_user.company_id
        )
        
        db.commit()
        
        # Convert to response model
        form_response = _form_to_response(form)
        
        return UpdateFormResponse(
            success=True,
            message="Form submitted for approval",
            formId=form.FormID,
            form=form_response
        )
        
    except ValueError as e:
        logger.warning(f"Invalid submit request: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting form: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to submit form")


@router.post(
    "/{form_id}/approve",
    response_model=UpdateFormResponse,
    summary="Approve form",
    description="Approve a pending form (Admin only)"
)
async def approve_form_request(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UpdateFormResponse:
    """
    Approve a pending form (AC-2.11.3).
    """
    try:
        service = ApprovalService(db)
        form = await service.approve_form(
            form_id=form_id,
            admin_user_id=current_user.user_id,
            company_id=current_user.company_id
        )
        
        db.commit()
        
        form_response = _form_to_response(form)
        
        return UpdateFormResponse(
            success=True,
            message="Form approved",
            formId=form.FormID,
            form=form_response
        )
        
    except ValueError as e:
        logger.warning(f"Invalid approve request: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error approving form: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to approve form")


@router.post(
    "/{form_id}/reject",
    response_model=UpdateFormResponse,
    summary="Reject form",
    description="Reject a pending form (Admin only)"
)
async def reject_form_request(
    form_id: int,
    request: RejectFormRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UpdateFormResponse:
    """
    Reject a pending form (AC-2.11.4).
    """
    try:
        service = ApprovalService(db)
        form = await service.reject_form(
            form_id=form_id,
            admin_user_id=current_user.user_id,
            company_id=current_user.company_id,
            reason=request.reason
        )
        
        db.commit()
        
        form_response = _form_to_response(form)
        
        return UpdateFormResponse(
            success=True,
            message="Form rejected",
            formId=form.FormID,
            form=form_response
        )
        
    except ValueError as e:
        logger.warning(f"Invalid reject request: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error rejecting form: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to reject form")


@router.post(
    "/{form_id}/request-external-approval",
    response_model=ExternalApprovalResponse,
    summary="Request external approval",
    description="Request approval from an external stakeholder (Story 2.12)"
)
async def request_external_approval_endpoint(
    form_id: int,
    request: ExternalApprovalRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ExternalApprovalResponse:
    """
    Request approval from an external stakeholder.
    """
    try:
        service = ApprovalService(db)
        result = await service.request_external_approval(
            form_id=form_id,
            requestor_id=current_user.user_id,
            company_id=current_user.company_id,
            external_email=request.email
        )
        
        db.commit()
        
        return ExternalApprovalResponse(
            success=True,
            message=result["message"],
            token=result["token"],
            email=result["email"]
        )
        
    except ValueError as e:
        logger.warning(f"Invalid external approval request: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error requesting external approval: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to request external approval")


# =====================================================================
# Helper Functions
# =====================================================================

def _form_to_response(form: Form) -> FormResponse:
    """Convert Form model to FormResponse schema with relationship data."""
    # Get relationship data
    form_status_response = None
    if form.form_status:
        form_status_response = FormStatusResponse(
            form_status_id=form.form_status.FormStatusID,
            status_code=form.form_status.StatusCode,
            status_name=form.form_status.StatusName,
            status_description=form.form_status.StatusDescription,
            status_color=form.form_status.StatusColor,
            status_icon=form.form_status.StatusIcon,
            is_active=form.form_status.IsActive,
            sort_order=form.form_status.SortOrder
        )
    
    form_approval_status_response = None
    if form.form_approval_status:
        form_approval_status_response = FormApprovalStatusResponse(
            form_approval_status_id=form.form_approval_status.FormApprovalStatusID,
            approval_status_code=form.form_approval_status.ApprovalStatusCode,
            approval_status_name=form.form_approval_status.ApprovalStatusName,
            approval_status_description=form.form_approval_status.ApprovalStatusDescription,
            is_requires_approval=form.form_approval_status.IsRequiresApproval,
            is_active=form.form_approval_status.IsActive,
            sort_order=form.form_approval_status.SortOrder
        )
    
    return FormResponse(
        formId=form.FormID,
        formName=form.FormName,
        formDescription=form.FormDescription,
        companyId=form.CompanyID,
        eventId=form.EventID,
        formStatusId=form.FormStatusID,
        formStatus=form_status_response,
        formApprovalStatusId=form.FormApprovalStatusID,
        formApprovalStatus=form_approval_status_response,
        isPublic=form.IsPublic,
        deploymentCost=form.DeploymentCost,
        totalSubmissions=form.TotalSubmissions,
        demoLeadsCollected=form.DemoLeadsCollected,
        productionLeadsCollected=form.ProductionLeadsCollected,
        lastSubmissionDate=form.LastSubmissionDate,
        lastActivityDate=form.LastActivityDate,
        formThumbnailUrl=form.FormThumbnailURL,
        formPreviewUrl=form.FormPreviewURL,
        createdDate=form.CreatedDate,
        createdBy=form.CreatedBy,
        updatedDate=form.UpdatedDate,
        updatedBy=form.UpdatedBy
    )
