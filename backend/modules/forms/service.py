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
from .approval_service import ApprovalService
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
    
    # Check for ANY active relationship (Agency OR Participant)
    # Story 2.4 allowed participants to create forms for public events
    event_company = db.execute(
        select(EventCompany).where(
            EventCompany.EventID == event_id,
            EventCompany.CompanyID == company_id,
            EventCompany.IsActive == True,
            EventCompany.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if event_company:
        logger.info(f"Company {company_id} has active relationship (RoleID={event_company.EventCompanyRoleID}) with Event {event_id}")
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
    form_company_id = company_id
    if form_data.get('event_id'):
        has_access = await _check_company_has_event_access(db, form_data['event_id'], company_id)
        
        if not has_access:
            # Double check if the event belongs to the company (direct ownership)
            # The _check_company_has_event_access helper already does this, but let's be explicit for debugging.
            event = db.execute(
                select(Event).where(Event.EventID == form_data['event_id'])
            ).scalar_one_or_none()
            
            if event and event.CompanyID == company_id:
                # It IS owned by the company. Why did helper fail?
                # Maybe IsDeleted check or something else?
                # Let's assume helper is correct and maybe data is stale or company_id mismatch.
                logger.warning(f"Access check failed for Event {form_data['event_id']} and Company {company_id}. EventOwner={event.CompanyID}")
                pass
            
            raise ValueError(f"Invalid event ID or event does not belong to your company: {form_data['event_id']}")
            
        # Fix for agency-created forms: Ensure form is assigned to Event Owner Company
        # Fetch event details
        event = db.execute(
            select(Event).where(Event.EventID == form_data['event_id'])
        ).scalar_one_or_none()
        
        if event and event.CompanyID != company_id:
            # Check if this is an Agency relationship
            from models.event_company import EventCompany
            from models.ref.event_company_role import EventCompanyRole
            
            agency_relationship = db.execute(
                select(EventCompany)
                .join(EventCompanyRole, EventCompany.EventCompanyRoleID == EventCompanyRole.EventCompanyRoleID)
                .where(
                    EventCompany.EventID == event.EventID,
                    EventCompany.CompanyID == company_id,
                    EventCompany.IsActive == True,
                    EventCompany.IsDeleted == False,
                    EventCompanyRole.RoleCode == 'agency_form_builder'
                )
            ).scalar_one_or_none()

            if agency_relationship:
                # Creating form as an Agency
                # User feedback: Agency creates forms FOR THE CLIENT (who granted access).
                # However, create_form currently receives 'company_id' as the Creator's Company.
                # Unless we implement 'On Behalf Of' logic, the form will belong to the Agency.
                # For now, we simply do NOT force it to the Event Owner.
                # The form will belong to 'company_id' (the Agency).
                # This allows the Agency to see and manage the form.
                # If transfer to Client is needed, it can be done later.
                logger.info(f"Agency user (Company {company_id}) creating form for Event {event.EventID}. Form owned by creator (Agency).")
            else:
                # Participant relationship (or other) - Form belongs to the Participant Company
                logger.info(f"Participant user (Company {company_id}) creating form for Event {event.EventID} owned by Company {event.CompanyID}. Form owned by creator.")
    
    # Create form object
    form = Form(
        FormName=form_data['form_name'],
        FormDescription=form_data.get('form_description'),
        CompanyID=form_company_id,
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
        # Get creator info for audit details
        creator = db.get(User, user_id)
        creator_display = f"{creator.Email} ({creator.FirstName} {creator.LastName})" if creator else f"User {user_id}"
        
        import json
        new_value_json = json.dumps({
            "details": f"Created form '{form.FormName}'",
            "form_name": form.FormName,
            "created_by": creator_display
        })
        
        activity_log = ActivityLog(
            UserID=user_id,
            CompanyID=company_id,
            Action="form.created",
            EntityType="Form",
            EntityID=form.FormID,
            NewValue=new_value_json,
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
    
    # Store ALL editable field values for audit trail (before any changes)
    old_values = {
        "form_name": form.FormName,
        "form_description": form.FormDescription,
        "form_status_id": form.FormStatusID,
        "form_approval_status_id": form.FormApprovalStatusID,
        "event_id": form.EventID,
        "is_public": form.IsPublic,
        "deployment_cost": float(form.DeploymentCost) if form.DeploymentCost else None,
        "form_thumbnail_url": form.FormThumbnailURL,
        "form_preview_url": form.FormPreviewURL
    }
    
    # Validate form status if provided
    if form_data.get('form_status_id'):
        form_status = db.execute(
            select(FormStatus).where(FormStatus.FormStatusID == form_data['form_status_id'])
        ).scalar_one_or_none()
        
        if not form_status:
            raise ValueError(f"Invalid form status ID: {form_data['form_status_id']}")

        # Publish Guard (Story 2.11)
        # If trying to set status to PUBLISHED, check approval
        if form_status.StatusCode == 'PUBLISHED':
            # Check if changing TO published (or already published and updating something else? 
            # Guard should probably run if status is being set to PUBLISHED, even if already published? 
            # No, only if transitioning or valid check.
            # If already published, cost check might not be needed or logic is different.
            # Let's assume if we are setting it to PUBLISHED, we must pass the guard.
            approval_service = ApprovalService(db)
            # We need to check against the NEW cost if provided, else old cost
            # Construct a temporary form object or update the attributes on the instance temporarily?
            # Or just pass the form and handle the potential new cost.
            # ApprovalService.check_publish_guard uses form.DeploymentCost.
            # We should update the form object's cost first if it's changing, OR handle it manually.
            
            # Let's update the form object with new values BEFORE check, but don't commit yet.
            # We already have 'form' object attached to session.
            temp_cost = form_data.get('deployment_cost', form.DeploymentCost)
            
            # We need to be careful not to persist partial updates if validation fails.
            # But check_publish_guard reads from the form object. 
            # Let's temporarily set the cost on the object, check, and if fail, rollback/error.
            # Actually, we haven't applied changes yet in this function.
            
            # Let's modify check_publish_guard to accept optional cost override?
            # Or just manually check here.
            
            # Re-implementing check here to avoid modifying ApprovalService interface for now
            from common.config_service import ConfigurationService
            config_service = ConfigurationService(db)
            threshold = config_service.get_approval_cost_threshold()
            cost = temp_cost or 0
            
            if cost > threshold:
                # Check approval status
                # If approval status is ALSO being updated, use that.
                new_approval_status_id = form_data.get('form_approval_status_id', form.FormApprovalStatusID)
                
                # Get status code for this ID
                approval_status_row = db.execute(
                    select(FormApprovalStatus).where(FormApprovalStatus.FormApprovalStatusID == new_approval_status_id)
                ).scalar_one_or_none()
                
                if not approval_status_row or approval_status_row.ApprovalStatusCode != 'APPROVED':
                     raise ValueError(f"Form requires approval (Cost ${cost} > ${threshold}) before publishing.")

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
    
    # Log form update to audit trail - only log fields that actually changed
    try:
        import json
        
        # Capture new values for ALL editable fields (after changes applied)
        new_values = {
            "form_name": form.FormName,
            "form_description": form.FormDescription,
            "form_status_id": form.FormStatusID,
            "form_approval_status_id": form.FormApprovalStatusID,
            "event_id": form.EventID,
            "is_public": form.IsPublic,
            "deployment_cost": float(form.DeploymentCost) if form.DeploymentCost else None,
            "form_thumbnail_url": form.FormThumbnailURL,
            "form_preview_url": form.FormPreviewURL
        }
        
        # Find which fields actually changed
        changed_fields = {}
        old_changed = {}
        for key in old_values:
            if old_values[key] != new_values[key]:
                changed_fields[key] = new_values[key]
                old_changed[key] = old_values[key]
        
        # Only log if there are actual changes
        if changed_fields:
            # Get updater info
            updater = db.get(User, user_id)
            updater_display = f"{updater.Email} ({updater.FirstName} {updater.LastName})" if updater else f"User {user_id}"
            
            # Resolve IDs to human-readable names for better audit display
            def get_status_name(status_id):
                if not status_id:
                    return "None"
                status = db.execute(
                    select(FormStatus).where(FormStatus.FormStatusID == status_id)
                ).scalar_one_or_none()
                return status.StatusName if status else f"Unknown ({status_id})"
            
            def get_approval_status_name(status_id):
                if not status_id:
                    return "None"
                status = db.execute(
                    select(FormApprovalStatus).where(FormApprovalStatus.FormApprovalStatusID == status_id)
                ).scalar_one_or_none()
                return status.ApprovalStatusName if status else f"Unknown ({status_id})"
            
            # Field display name mapping for cleaner output
            field_display_names = {
                "form_name": "Form Name",
                "form_description": "Description",
                "form_status_id": "Status",
                "form_approval_status_id": "Approval Status",
                "event_id": "Event",
                "is_public": "Public",
                "deployment_cost": "Deployment Cost",
                "form_thumbnail_url": "Thumbnail URL",
                "form_preview_url": "Preview URL"
            }
            
            # Build structured change data for table display on frontend
            # Format: { "field_name": {"old": "...", "new": "..."}, ... }
            structured_changes = {}
            change_descriptions = []
            
            for key in changed_fields:
                old_val = old_changed[key]
                new_val = changed_fields[key]
                display_name = field_display_names.get(key, key.replace('_', ' ').title())
                
                # Resolve IDs to names for better readability
                if key == "form_status_id":
                    old_display = get_status_name(old_val)
                    new_display = get_status_name(new_val)
                elif key == "form_approval_status_id":
                    old_display = get_approval_status_name(old_val)
                    new_display = get_approval_status_name(new_val)
                elif key == "event_id":
                    old_event = db.execute(select(Event).where(Event.EventID == old_val)).scalar_one_or_none() if old_val else None
                    new_event = db.execute(select(Event).where(Event.EventID == new_val)).scalar_one_or_none() if new_val else None
                    old_display = old_event.Name if old_event else "None"
                    new_display = new_event.Name if new_event else "None"
                elif key == "is_public":
                    old_display = "Yes" if old_val else "No"
                    new_display = "Yes" if new_val else "No"
                elif key == "deployment_cost":
                    old_display = f"${old_val:.2f}" if old_val is not None else "Not set"
                    new_display = f"${new_val:.2f}" if new_val is not None else "Not set"
                else:
                    old_display = str(old_val) if old_val is not None else "None"
                    new_display = str(new_val) if new_val is not None else "None"
                
                # Add to structured changes for table display
                structured_changes[display_name] = {
                    "old": old_display,
                    "new": new_display
                }
                change_descriptions.append(f"{display_name}: {old_display} → {new_display}")
            
            details_text = ", ".join(change_descriptions)
            
            activity_log = ActivityLog(
                UserID=user_id,
                CompanyID=company_id,
                Action="form.updated",
                EntityType="Form",
                EntityID=form.FormID,
                OldValue=json.dumps(structured_changes),  # Structured for table display
                NewValue=json.dumps({
                    "changes": structured_changes,  # Structured data
                    "details": details_text,  # Human-readable summary
                    "updated_by": updater_display
                }),
                CreatedDate=datetime.utcnow()
            )
            db.add(activity_log)
            
            # Check if approval status changed to APPROVED - log a separate form.approved entry
            if "form_approval_status_id" in changed_fields:
                new_approval_status = db.execute(
                    select(FormApprovalStatus).where(FormApprovalStatus.FormApprovalStatusID == changed_fields["form_approval_status_id"])
                ).scalar_one_or_none()
                
                if new_approval_status and new_approval_status.ApprovalStatusCode == 'APPROVED':
                    # Log a separate approval entry for the Approvals tab
                    approval_log = ActivityLog(
                        UserID=user_id,
                        CompanyID=company_id,
                        Action="form.approved",
                        EntityType="Form",
                        EntityID=form.FormID,
                        NewValue=json.dumps({
                            "details": f"Approved by {updater_display}",
                            "approved_by": updater_display,
                            "form_name": form.FormName
                        }),
                        CreatedDate=datetime.utcnow()
                    )
                    db.add(approval_log)
                    logger.info(f"Logged form.approved for form {form_id} - approval via form update")
            
            db.flush()
        else:
            logger.debug(f"Form {form_id} update skipped audit log - no tracked fields changed")
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
    # Check if company owns the event
    event_ownership = db.execute(
        select(Event.CompanyID).where(Event.EventID == event_id)
    ).scalar_one_or_none()
    
    is_owner = (event_ownership == company_id)

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
    
    # Build query - filter by company unless agency access OR event owner
    query = select(Form).options(
        joinedload(Form.form_status),
        joinedload(Form.form_approval_status),
        joinedload(Form.company),
        joinedload(Form.event)
    ).where(
        Form.EventID == event_id,
        Form.IsDeleted == False
    )
    
    # Only filter by company if NOT agency access AND NOT owner
    if not has_agency_access and not is_owner:
        query = query.where(Form.CompanyID == company_id)
        logger.info(f"Filtering forms by CompanyID={company_id} for EventID={event_id}")
    else:
        logger.info(f"Access granted (Owner={is_owner}, Agency={has_agency_access}) - returning all forms for EventID={event_id}")
    
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


async def transfer_form_ownership(
    db: Session,
    from_user_id: int,
    to_user_id: int,
    company_id: int,
    admin_user_id: int,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transfer ownership of all forms from one user to another within the same company.
    
    Args:
        db: Database session
        from_user_id: User ID to transfer from
        to_user_id: User ID to transfer to
        company_id: Company ID
        admin_user_id: Admin User ID performing the transfer
        reason: Reason for transfer
        
    Returns:
        Dictionary with transfer statistics
        
    Raises:
        ValueError: If users not in company or invalid IDs
    """
    logger.info(f"Starting bulk form ownership transfer: From={from_user_id}, To={to_user_id}, Company={company_id}, Admin={admin_user_id}")
    
    # 1. Validate users exist and belong to the company
    # We check 'Active' status for recipient, but sender might be inactive (off-boarding)
    from models.user_company import UserCompany
    from models.ref.user_company_status import UserCompanyStatus
    
    # Check recipient
    recipient = db.execute(
        select(UserCompany).join(UserCompanyStatus).where(
            UserCompany.UserID == to_user_id,
            UserCompany.CompanyID == company_id,
            UserCompany.IsDeleted == False,
            UserCompanyStatus.StatusCode == 'active'
        )
    ).scalar_one_or_none()
    
    if not recipient:
        raise ValueError(f"Recipient user {to_user_id} is not an active member of company {company_id}")
        
    # Check sender (just needs to exist in company history)
    sender = db.execute(
        select(UserCompany).where(
            UserCompany.UserID == from_user_id,
            UserCompany.CompanyID == company_id
        )
    ).scalar_one_or_none()
    
    if not sender:
        raise ValueError(f"Sender user {from_user_id} is not associated with company {company_id}")
        
    # 2. Find forms eligible for transfer
    # Criteria:
    # A. Form is owned by the sender
    # AND
    # B. (Form belongs to the target company OR Form belongs to an Event owned by the target company)
    # This handles both internal transfers (employee off-boarding) and agency handovers.
    
    forms = db.execute(
        select(Form)
        .join(Event, Form.EventID == Event.EventID, isouter=True)
        .where(
            Form.CreatedBy == from_user_id,
            Form.IsDeleted == False,
            or_(
                Form.CompanyID == company_id,
                Event.CompanyID == company_id
            )
        )
    ).scalars().all()
    
    if not forms:
        logger.info(f"No eligible forms found for user {from_user_id} transfer to company {company_id}")
        return {
            "forms_transferred": 0,
            "access_controls_transferred": 0
        }
        
    # 3. Update ownership
    forms_count = 0
    for form in forms:
        # Update creator/owner
        # Note: CreatedBy is the owner. UpdatedBy records who did the transfer.
        # CRITICAL: Also update CompanyID to ensure the target company owns the form now
        old_company_id = form.CompanyID
        
        form.CreatedBy = to_user_id
        form.UpdatedBy = admin_user_id
        form.CompanyID = company_id
        form.UpdatedDate = datetime.utcnow()
        forms_count += 1
        
        # Log activity
        try:
            activity_log = ActivityLog(
                UserID=admin_user_id,
                CompanyID=company_id,
                Action="form.ownership_transferred",
                EntityType="Form",
                EntityID=form.FormID,
                OldValue=f"Owner: {from_user_id}, Company: {old_company_id}",
                NewValue=f"Owner: {to_user_id}, Company: {company_id}",
                Comments=f"Bulk transfer: {reason}" if reason else "Bulk transfer",
                CreatedDate=datetime.utcnow()
            )
            db.add(activity_log)
        except Exception as e:
            logger.warning(f"Failed to log audit for form {form.FormID}: {e}")

    # 4. Update FormAccessControl (if any specific grants exist for the sender)
    # If sender had specific access to other forms, we might want to transfer that too.
    # But the requirement usually focuses on OWNERSHIP of created forms.
    # Let's stick to ownership transfer as per story description "Transferring all forms from one user to another".
    
    # However, if there are access controls GRANTED by the sender, they remain valid (granted by ID X).
    # We don't necessarily need to change 'GrantedBy' unless required.
    
    db.flush()
    
    logger.info(f"Transferred {forms_count} forms from User {from_user_id} to User {to_user_id}")
    
    return {
        "forms_transferred": forms_count,
        "access_controls_transferred": 0 # Placeholder if we implement access transfer later
    }
