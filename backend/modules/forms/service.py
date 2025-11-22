"""
Form Service Module
Business logic for form CRUD operations
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, and_
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

from models.form import Form
from models.ref.form_status import FormStatus
from models.ref.form_approval_status import FormApprovalStatus
from models.company import Company
from models.user import User
from models.event import Event
from models.audit.activity_log import ActivityLog
from .access_control_service import get_user_accessible_forms, check_user_access, get_user_access_level
from .access_guard import check_form_access_guard
from common.logger import get_logger

logger = get_logger(__name__)


async def _check_company_has_event_access(
    db: Session,
    event_id: int,
    company_id: int
) -> bool:
    """
    Check if a company has access to an event (either owns it or has agency relationship).
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID
        
    Returns:
        True if company owns the event or has agency relationship, False otherwise
    """
    # Check if company owns the event
    event = db.execute(
        select(Event).where(
            Event.EventID == event_id,
            Event.CompanyID == company_id,
            Event.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if event:
        return True
    
    # Check if company has agency relationship with event (agency_form_builder role)
    from models.event_company import EventCompany
    from models.ref.event_company_role import EventCompanyRole
    
    agency_role = db.execute(
        select(EventCompanyRole).where(EventCompanyRole.RoleCode == 'agency_form_builder')
    ).scalar_one_or_none()
    
    if agency_role:
        event_company = db.execute(
            select(EventCompany).where(
                EventCompany.EventID == event_id,
                EventCompany.CompanyID == company_id,
                EventCompany.EventCompanyRoleID == agency_role.EventCompanyRoleID,
                EventCompany.IsActive == True,
                EventCompany.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if event_company:
            logger.info(f"Company {company_id} has agency_form_builder access to Event {event_id}")
            return True
    
    return False


async def create_form(
    db: Session,
    user_id: int,
    company_id: int,
    form_data: Dict[str, Any]
) -> Form:
    """
    Create a new form for the company.
    
    Args:
        db: Database session
        user_id: User ID creating the form
        company_id: Company ID (for multi-tenant filtering)
        form_data: Form creation data from request
        
    Returns:
        Created Form object
        
    Raises:
        ValueError: If validation fails
    """
    # Validate form status exists
    form_status = db.execute(
        select(FormStatus).where(FormStatus.FormStatusID == form_data['form_status_id'])
    ).scalar_one_or_none()
    
    if not form_status:
        raise ValueError(f"Invalid form status ID: {form_data['form_status_id']}")
    
    # Validate form approval status exists
    form_approval_status = db.execute(
        select(FormApprovalStatus).where(FormApprovalStatus.FormApprovalStatusID == form_data['form_approval_status_id'])
    ).scalar_one_or_none()
    
    if not form_approval_status:
        raise ValueError(f"Invalid form approval status ID: {form_data['form_approval_status_id']}")
    
    # Validate company exists
    company = db.execute(
        select(Company).where(Company.CompanyID == company_id)
    ).scalar_one_or_none()
    
    if not company:
        raise ValueError(f"Invalid company ID: {company_id}")
    
    # Validate event if provided (allow agency relationships)
    if form_data.get('event_id'):
        has_access = await _check_company_has_event_access(db, form_data['event_id'], company_id)
        
        if not has_access:
            raise ValueError(f"Invalid event ID or event does not belong to your company: {form_data['event_id']}")
    
    # Create form object
    form = Form(
        FormName=form_data['form_name'],
        FormDescription=form_data.get('form_description'),
        CompanyID=company_id,
        EventID=form_data.get('event_id'),
        FormStatusID=form_data['form_status_id'],
        FormApprovalStatusID=form_data['form_approval_status_id'],
        IsPublic=form_data.get('is_public', False),
        DeploymentCost=form_data.get('deployment_cost'),
        FormThumbnailURL=form_data.get('form_thumbnail_url'),
        FormPreviewURL=form_data.get('form_preview_url'),
        TotalSubmissions=0,
        DemoLeadsCollected=0,
        ProductionLeadsCollected=0,
        CreatedBy=user_id,
        CreatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    
    db.add(form)
    db.flush()
    
    # Log form creation to audit trail
    try:
        activity_log = ActivityLog(
            UserID=user_id,
            CompanyID=company_id,
            Action="form.created",
            EntityType="Form",
            EntityID=form.FormID,
            NewValue=f'{{"form_name": "{form.FormName}", "form_id": {form.FormID}}}',
            CreatedDate=datetime.utcnow()
        )
        db.add(activity_log)
        db.flush()
    except Exception as e:
        logger.warning(f"Failed to log form creation to audit trail: {str(e)}")
    
    logger.info(f"Form created: FormID={form.FormID}, Name='{form.FormName}', CompanyID={company_id}")
    
    return form


async def get_forms(
    db: Session,
    company_id: int,
    user_id: int,
    filters: Optional[Dict[str, Any]] = None
) -> List[Form]:
    """
    Get all forms user has access to (company ownership OR granted access).
    
    Args:
        db: Database session
        company_id: Company ID (for company-owned forms)
        user_id: User ID (for access filtering)
        filters: Optional filters (form_status_id, event_id, search)
        
    Returns:
        List of Form objects user has access to
    """
    # Get accessible forms (company-owned OR granted access)
    forms = await get_user_accessible_forms(db, user_id, company_id)
    
    # Apply filters
    if filters:
        if filters.get('form_status_id'):
            forms = [f for f in forms if f.FormStatusID == filters['form_status_id']]
        
        if filters.get('event_id'):
            forms = [f for f in forms if f.EventID == filters['event_id']]
        
        if filters.get('search'):
            search_term = filters['search'].lower()
            forms = [
                f for f in forms
                if (f.FormName and search_term in f.FormName.lower()) or
                   (f.FormDescription and search_term in f.FormDescription.lower())
            ]
    
    # Order by created date descending (most recent first)
    forms = sorted(forms, key=lambda f: f.CreatedDate, reverse=True)
    
    logger.info(f"Retrieved {len(forms)} accessible forms for UserID={user_id}, CompanyID={company_id}")
    
    return forms


async def get_form_by_id(
    db: Session,
    form_id: int,
    company_id: int,
    user_id: int
) -> Optional[Form]:
    """
    Get a single form by ID, checking user has View access.
    
    Args:
        db: Database session
        form_id: Form ID
        company_id: Company ID (for validation)
        user_id: User ID (for access check)
        
    Returns:
        Form object if found and user has access, None otherwise
    """
    try:
        # Check access (raises HTTPException if denied)
        form = await check_form_access_guard(db, form_id, user_id, "VIEW")
        
        # Eager load relationships
        form = db.execute(
            select(Form)
            .options(
                joinedload(Form.form_status),
                joinedload(Form.form_approval_status),
                joinedload(Form.company),
                joinedload(Form.event)
            )
            .where(Form.FormID == form_id)
        ).scalar_one_or_none()
        
        if form:
            logger.info(f"Retrieved form: FormID={form_id}, UserID={user_id}")
        else:
            logger.warning(f"Form not found: FormID={form_id}")
        
        return form
    except Exception as e:
        logger.warning(f"Access denied or form not found: FormID={form_id}, UserID={user_id}, Error={str(e)}")
        return None


async def update_form(
    db: Session,
    form_id: int,
    company_id: int,
    user_id: int,
    form_data: Dict[str, Any]
) -> Form:
    """
    Update a form, checking user has Manage access.
    
    Args:
        db: Database session
        form_id: Form ID
        company_id: Company ID (for validation)
        user_id: User ID making the update
        form_data: Form update data from request
        
    Returns:
        Updated Form object
        
    Raises:
        ValueError: If form not found, access denied, or validation fails
    """
    # Check Manage access (raises HTTPException if denied)
    form = await check_form_access_guard(db, form_id, user_id, "MANAGE")
    
    # Store old values for audit trail
    old_values = {
        "form_name": form.FormName,
        "form_status_id": form.FormStatusID,
        "form_approval_status_id": form.FormApprovalStatusID,
        "event_id": form.EventID
    }
    
    # Validate form status if provided
    if form_data.get('form_status_id'):
        form_status = db.execute(
            select(FormStatus).where(FormStatus.FormStatusID == form_data['form_status_id'])
        ).scalar_one_or_none()
        
        if not form_status:
            raise ValueError(f"Invalid form status ID: {form_data['form_status_id']}")
    
    # Validate form approval status if provided
    if form_data.get('form_approval_status_id'):
        form_approval_status = db.execute(
            select(FormApprovalStatus).where(FormApprovalStatus.FormApprovalStatusID == form_data['form_approval_status_id'])
        ).scalar_one_or_none()
        
        if not form_approval_status:
            raise ValueError(f"Invalid form approval status ID: {form_data['form_approval_status_id']}")
    
    # Validate event if provided (allow agency relationships)
    if form_data.get('event_id') is not None:
        if form_data['event_id']:
            has_access = await _check_company_has_event_access(db, form_data['event_id'], company_id)
            
            if not has_access:
                raise ValueError(f"Invalid event ID or event does not belong to your company: {form_data['event_id']}")
    
    # Update form fields
    if 'form_name' in form_data:
        form.FormName = form_data['form_name']
    if 'form_description' in form_data:
        form.FormDescription = form_data['form_description']
    if 'event_id' in form_data:
        form.EventID = form_data['event_id']
    if 'form_status_id' in form_data:
        form.FormStatusID = form_data['form_status_id']
    if 'form_approval_status_id' in form_data:
        form.FormApprovalStatusID = form_data['form_approval_status_id']
    if 'is_public' in form_data:
        form.IsPublic = form_data['is_public']
    if 'deployment_cost' in form_data:
        form.DeploymentCost = form_data['deployment_cost']
    if 'form_thumbnail_url' in form_data:
        form.FormThumbnailURL = form_data['form_thumbnail_url']
    if 'form_preview_url' in form_data:
        form.FormPreviewURL = form_data['form_preview_url']
    
    form.UpdatedDate = datetime.utcnow()
    form.UpdatedBy = user_id
    
    db.flush()
    
    # Log form update to audit trail
    try:
        new_values = {
            "form_name": form.FormName,
            "form_status_id": form.FormStatusID,
            "form_approval_status_id": form.FormApprovalStatusID,
            "event_id": form.EventID
        }
        activity_log = ActivityLog(
            UserID=user_id,
            CompanyID=company_id,
            Action="form.updated",
            EntityType="Form",
            EntityID=form.FormID,
            OldValue=str(old_values),
            NewValue=str(new_values),
            CreatedDate=datetime.utcnow()
        )
        db.add(activity_log)
        db.flush()
    except Exception as e:
        logger.warning(f"Failed to log form update to audit trail: {str(e)}")
    
    logger.info(f"Form updated: FormID={form_id}, CompanyID={company_id}")
    
    return form


async def delete_form(
    db: Session,
    form_id: int,
    company_id: int,
    user_id: int
) -> None:
    """
    Soft delete a form, checking user has Manage access.
    
    Args:
        db: Database session
        form_id: Form ID
        company_id: Company ID (for validation)
        user_id: User ID making the deletion
        
    Raises:
        ValueError: If form not found or access denied
    """
    # Check Manage access (raises HTTPException if denied)
    form = await check_form_access_guard(db, form_id, user_id, "MANAGE")
    
    # Soft delete
    form.IsDeleted = True
    form.DeletedDate = datetime.utcnow()
    form.DeletedBy = user_id
    form.UpdatedDate = datetime.utcnow()
    form.UpdatedBy = user_id
    
    db.flush()
    
    # Log form deletion to audit trail
    try:
        activity_log = ActivityLog(
            UserID=user_id,
            CompanyID=company_id,
            Action="form.deleted",
            EntityType="Form",
            EntityID=form.FormID,
            OldValue=f'{{"form_name": "{form.FormName}", "form_id": {form.FormID}}}',
            CreatedDate=datetime.utcnow()
        )
        db.add(activity_log)
        db.flush()
    except Exception as e:
        logger.warning(f"Failed to log form deletion to audit trail: {str(e)}")
    
    logger.info(f"Form deleted: FormID={form_id}, CompanyID={company_id}")


async def get_forms_by_event(
    db: Session,
    event_id: int,
    company_id: int
) -> List[Form]:
    """
    Get all forms for a specific event.
    
    For agency relationships (agency_form_builder role), returns ALL forms for the event,
    regardless of which company owns them. Otherwise, only returns forms owned by the company.
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID (for multi-tenant filtering)
        
    Returns:
        List of Form objects for the event
    """
    # Check if company has agency relationship with event (agency_form_builder role)
    from models.event_company import EventCompany
    from models.ref.event_company_role import EventCompanyRole
    
    agency_role = db.execute(
        select(EventCompanyRole).where(EventCompanyRole.RoleCode == 'agency_form_builder')
    ).scalar_one_or_none()
    
    has_agency_access = False
    if agency_role:
        event_company = db.execute(
            select(EventCompany).where(
                EventCompany.EventID == event_id,
                EventCompany.CompanyID == company_id,
                EventCompany.EventCompanyRoleID == agency_role.EventCompanyRoleID,
                EventCompany.IsActive == True,
                EventCompany.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if event_company:
            has_agency_access = True
            logger.info(f"Company {company_id} has agency_form_builder access to Event {event_id} - returning all forms")
    
    # Build query - filter by company unless agency access
    query = select(Form).options(
        joinedload(Form.form_status),
        joinedload(Form.form_approval_status),
        joinedload(Form.company),
        joinedload(Form.event)
    ).where(
        Form.EventID == event_id,
        Form.IsDeleted == False
    )
    
    # Only filter by company if NOT agency access
    if not has_agency_access:
        query = query.where(Form.CompanyID == company_id)
        logger.info(f"Filtering forms by CompanyID={company_id} for EventID={event_id}")
    else:
        logger.info(f"Agency access detected - returning all forms for EventID={event_id} (not filtered by company)")
    
    query = query.order_by(Form.CreatedDate.desc())
    
    forms = db.execute(query).scalars().all()
    
    logger.info(f"Retrieved {len(forms)} forms for EventID={event_id}, CompanyID={company_id} (agency_access={has_agency_access})")
    
    return forms


async def get_form_statuses(db: Session) -> List[FormStatus]:
    """
    Get all active form statuses.
    
    Args:
        db: Database session
        
    Returns:
        List of FormStatus objects
    """
    form_statuses = db.execute(
        select(FormStatus).where(
            FormStatus.IsDeleted == False,
            FormStatus.IsActive == True
        ).order_by(FormStatus.SortOrder)
    ).scalars().all()
    
    return form_statuses


async def get_form_approval_statuses(db: Session) -> List[FormApprovalStatus]:
    """
    Get all active form approval statuses.
    
    Args:
        db: Database session
        
    Returns:
        List of FormApprovalStatus objects
    """
    form_approval_statuses = db.execute(
        select(FormApprovalStatus).where(
            FormApprovalStatus.IsDeleted == False,
            FormApprovalStatus.IsActive == True
        ).order_by(FormApprovalStatus.SortOrder)
    ).scalars().all()
    
    return form_approval_statuses

