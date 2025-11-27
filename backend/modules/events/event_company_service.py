"""
EventCompany Service Module
Business logic for EventCompany relationship management
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, text
from typing import Optional, List
from datetime import datetime

from models.event_company import EventCompany
from models.ref.event_company_role import EventCompanyRole
from models.event import Event
from models.form import Form
from models.form_access_control import FormAccessControl
from models.user_company import UserCompany
from models.ref.user_company_status import UserCompanyStatus
from common.logger import get_logger

logger = get_logger(__name__)


async def create_event_company_relationship(
    db: Session,
    event_id: int,
    company_id: int,
    role_code: str,
    user_id: int
) -> EventCompany:
    """
    Create an EventCompany relationship (owner, organizer, or participant).
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID
        role_code: Role code ('event_owner', 'event_organizer', 'event_participant')
        user_id: User ID creating the relationship
        
    Returns:
        Created EventCompany object
        
    Raises:
        ValueError: If role code is invalid or relationship already exists
    """
    # Get role ID from role code
    role = db.execute(
        select(EventCompanyRole).where(EventCompanyRole.RoleCode == role_code)
    ).scalar_one_or_none()
    
    if not role:
        raise ValueError(f"Invalid role code: {role_code}")
    
    if not role.IsActive:
        raise ValueError(f"Role '{role_code}' is not active")
    
    # Check if relationship already exists (active)
    existing = db.execute(
        select(EventCompany).where(
            EventCompany.EventID == event_id,
            EventCompany.CompanyID == company_id,
            EventCompany.IsActive== True,  # type: ignore[arg-type]
            EventCompany.IsDeleted== False  # type: ignore[arg-type]
        )
    ).scalar_one_or_none()
    
    if existing:
        raise ValueError(
            f"Active EventCompany relationship already exists for EventID={event_id}, CompanyID={company_id}"
        )
    
    # Create relationship
    event_company = EventCompany(
        EventID=event_id,
        CompanyID=company_id,
        EventCompanyRoleID=role.EventCompanyRoleID,
        IsActive=True,
        CreatedBy=user_id,
        FirstUsedDate=datetime.utcnow() if role_code == 'event_participant' else None
    )
    
    db.add(event_company)
    db.commit()
    db.refresh(event_company)
    
    logger.info(
        f"Created EventCompany relationship: EventID={event_id}, CompanyID={company_id}, "
        f"RoleCode={role_code}, EventCompanyID={event_company.EventCompanyID}"
    )
    
    return event_company


async def get_event_companies(
    db: Session,
    event_id: int,
    active_only: bool = True
) -> List[EventCompany]:
    """
    Get all companies for an event.
    
    Args:
        db: Database session
        event_id: Event ID
        active_only: If True, only return active relationships
        
    Returns:
        List of EventCompany objects
    """
    query = db.query(EventCompany).options(
        joinedload(EventCompany.company),
        joinedload(EventCompany.role)
    ).filter(
        EventCompany.EventID == event_id,
        EventCompany.IsDeleted== False  # type: ignore[arg-type]
    )
    
    if active_only:
        query = query.filter(EventCompany.IsActive== True)  # type: ignore[arg-type]
    
    companies = query.all()
    
    logger.info(f"Retrieved {len(companies)} companies for EventID={event_id}")
    
    return companies


async def get_company_events(
    db: Session,
    company_id: int,
    active_only: bool = True,
    include_participant: bool = True,
    user_id: Optional[int] = None,
    user_role: Optional[str] = None
) -> List[Event]:
    """
    Get all events for a company, including events where company is a participant.
    Optionally filters events to only include those where the user has access to at least one form.
    
    Note: Filtering by form access is skipped for Company Admins and Company Users,
    who should see all events for their company regardless of form access.
    
    Args:
        db: Database session
        company_id: Company ID
        active_only: If True, only return active relationships
        include_participant: If True, include events where company is a participant
        user_id: Optional user ID to filter events based on form access. If provided, only returns
                 events where the user has access to at least one form (VIEW access or higher)
        user_role: Optional user role. If "company_admin" or "company_user", form access filtering
                   is skipped (they see all company events)
        
    Returns:
        List of Event objects
    """
    # Get EventCompany relationships
    query = db.query(EventCompany).options(
        joinedload(EventCompany.event).joinedload(Event.event_type),
        joinedload(EventCompany.event).joinedload(Event.event_status),
        joinedload(EventCompany.event).joinedload(Event.public_review_status),
        joinedload(EventCompany.event).joinedload(Event.industry),
        joinedload(EventCompany.event).joinedload(Event.organizer_company),
        joinedload(EventCompany.event).joinedload(Event.company)
    ).filter(
        EventCompany.CompanyID == company_id,
        EventCompany.IsDeleted== False  # type: ignore[arg-type]
    )
    
    if active_only:
        query = query.filter(EventCompany.IsActive== True)  # type: ignore[arg-type]
    
    if include_participant:
        # Include all roles (owner, organizer, participant)
        pass
    else:
        # Only include owner and organizer roles
        owner_role = db.execute(
            select(EventCompanyRole).where(EventCompanyRole.RoleCode == 'event_owner')
        ).scalar_one_or_none()
        organizer_role = db.execute(
            select(EventCompanyRole).where(EventCompanyRole.RoleCode == 'event_organizer')
        ).scalar_one_or_none()
        
        if owner_role and organizer_role:
            query = query.filter(
                or_(
                    EventCompany.EventCompanyRoleID == owner_role.EventCompanyRoleID,
                    EventCompany.EventCompanyRoleID == organizer_role.EventCompanyRoleID
                )
            )
    
    event_companies = query.all()
    events = [ec.event for ec in event_companies if ec.event and not ec.event.IsDeleted]
    
    # Exclude archived events from customer-facing lists
    from models.ref.event_status import EventStatus
    archived_status = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
    ).scalar_one_or_none()
    
    if archived_status:
        events = [e for e in events if e.EventStatusID != archived_status.EventStatusID]
    
    # Filter events based on user form access if user_id is provided
    # Skip filtering for Company Admins and Company Users - they should see all company events
    if user_id is not None and user_role not in ["company_admin", "company_user", "system_admin"]:
        accessible_event_ids = set()
        
        # Get all forms for the events and check user access
        for event in events:
            # Get all forms for this event
            # Note: We do NOT filter by CompanyID here because we want to find forms
            # that might be owned by other companies (e.g., for Agency access)
            forms = db.execute(
                select(Form).where(
                    Form.EventID == event.EventID,
                    Form.IsDeleted== False  # type: ignore[arg-type]
                )
            ).scalars().all()
            
            # For Company Viewers: Only include events where user has access to at least one form
            # Events with no forms are NOT accessible to Company Viewers
            # (Company Admins and Company Users would see all events, but they're filtered out above)
            if not forms:
                # Event has no forms owned by this company - Company Viewer cannot have access
                continue
            
            # Check if user has access to at least one form in this event
            for form in forms:
                try:
                    # Use the database function to check access
                    result = db.execute(
                        text("""
                            SELECT CanView
                            FROM [dbo].[fn_GetUserFormAccess](:user_id, :form_id)
                        """),
                        {"user_id": user_id, "form_id": form.FormID}
                    ).fetchone()
                    
                    if result and bool(result.CanView):
                        # User has access to at least one form in this event
                        accessible_event_ids.add(event.EventID)
                        break  # No need to check other forms for this event
                except Exception as e:
                    # If function doesn't exist or error occurs, fail-closed: deny access
                    error_msg = str(e)
                    if "fn_GetUserFormAccess" in error_msg or "Invalid object name" in error_msg:
                        logger.error(f"SECURITY: Database function fn_GetUserFormAccess not found. Fail-closed: Denying access for EventID={event.EventID}. Database migrations may not be complete.")
                        # Do NOT add event to accessible_event_ids - fail-closed security model
                        # Continue checking other forms, but this form check failed
                    else:
                        logger.warning(f"Error checking form access for FormID={form.FormID}, EventID={event.EventID}: {error_msg}")
                    # Continue checking other forms
        
        # CRITICAL: Also include events where the company has forms (even if not linked via EventCompany)
        # This handles the case where a company owns forms for an event but the event is not linked via EventCompany
        # For Company Viewers, we need to include events where they have form access, regardless of EventCompany linkage
        # We do NOT filter by CompanyID to allow Agency/Cross-company access detection
        # Fix: Use CROSS APPLY instead of EXISTS with column parameter to support SQL Server TVF
        try:
            additional_events_query = db.execute(
                text("""
                    SELECT DISTINCT f.EventID
                    FROM [dbo].[Form] f
                    CROSS APPLY [dbo].[fn_GetUserFormAccess](:user_id, f.FormID) a
                    WHERE f.EventID IS NOT NULL
                      AND f.IsDeleted = 0
                      AND a.CanView = 1
                """),
                {"user_id": user_id}
            ).fetchall()
        except Exception as e:
            # Handle missing database function (e.g. migrations not run)
            error_msg = str(e)
            if "fn_GetUserFormAccess" in error_msg or "Invalid object name" in error_msg:
                logger.error("SECURITY: Database function fn_GetUserFormAccess not found during bulk query. Fail-closed: Denying access. Database migrations may not be complete.")
                # Fail-closed: Return empty result set - no events accessible
                # This prevents unauthorized access when access control cannot be verified
                additional_events_query = []
            else:
                raise e
        
        for row in additional_events_query:
            accessible_event_ids.add(row.EventID)
        
        # Now get the Event objects for all accessible events (both from EventCompany and from forms)
        if accessible_event_ids:
            # Get events from EventCompany (already have these)
            accessible_events = [e for e in events if e.EventID in accessible_event_ids]
            
            # Get additional events that aren't in EventCompany but have accessible forms
            event_ids_from_ec = {e.EventID for e in events}
            missing_event_ids = accessible_event_ids - event_ids_from_ec
            
            if missing_event_ids:
                # Fetch these events directly
                missing_events = db.execute(
                    select(Event)
                    .where(Event.EventID.in_(list(missing_event_ids)))
                    .where(Event.IsDeleted== False)  # type: ignore[arg-type]
                ).scalars().all()
                
                # Exclude archived events
                if archived_status:
                    missing_events = [e for e in missing_events if e.EventStatusID != archived_status.EventStatusID]
                
                accessible_events.extend(missing_events)
            
            events = accessible_events
        else:
            events = []
        
        logger.info(f"Filtered to {len(events)} events for CompanyID={company_id} where UserID={user_id} (role={user_role}) has form access")
    elif user_id is not None:
        logger.info(f"Skipping form access filter for UserID={user_id} with role={user_role} - showing all company events")
    
    # Order by start date descending (most recent first)
    events.sort(key=lambda e: e.StartDateTime if e.StartDateTime else datetime.min, reverse=True)
    
    logger.info(f"Retrieved {len(events)} events for CompanyID={company_id} (including participant relationships)")
    
    return events


async def disassociate_company_from_event(
    db: Session,
    event_id: int,
    company_id: int,
    user_id: int
) -> bool:
    """
    Disassociate a company from an event.
    
    1. Soft delete EventCompany relationship if it exists.
    2. Revoke all form access for users of that company for that event.
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID
        user_id: User ID performing disassociation
        
    Returns:
        True if disassociation successful, False otherwise
        
    Raises:
        ValueError: If relationship cannot be disassociated (e.g. Owner)
    """
    # 1. Find and deactivate active EventCompany relationship
    event_company = db.execute(
        select(EventCompany).where(
            EventCompany.EventID == event_id,
            EventCompany.CompanyID == company_id,
            EventCompany.IsActive== True,  # type: ignore[arg-type]
            EventCompany.IsDeleted== False  # type: ignore[arg-type]
        )
    ).scalar_one_or_none()
    
    if event_company:
        # Get role to check if it's a restricted role (Owner/Organizer cannot leave easily?)
        role = db.execute(
            select(EventCompanyRole).where(
                EventCompanyRole.EventCompanyRoleID == event_company.EventCompanyRoleID
            )
        ).scalar_one_or_none()
        
        # Prevent disassociation for Owners and Organizers
        if role and role.RoleCode in ['event_owner', 'event_organizer']:
            raise ValueError(
                f"Cannot disassociate company with role '{role.RoleCode}'. Event Owners and Organizers cannot leave the event."
            )
        
        # Soft delete relationship
        event_company.IsActive = False  # type: ignore[assignment]
        event_company.DisassociatedDate = datetime.utcnow()  # type: ignore[assignment]
        event_company.DisassociatedBy = user_id  # type: ignore[assignment]
        event_company.UpdatedDate = datetime.utcnow()  # type: ignore[assignment]
        event_company.UpdatedBy = user_id  # type: ignore[assignment]
        
        logger.info(
            f"Disassociated company from event (EventCompany): EventID={event_id}, CompanyID={company_id}, "
            f"EventCompanyID={event_company.EventCompanyID}"
        )
    else:
        logger.info(
            f"No active EventCompany relationship found for EventID={event_id}, CompanyID={company_id}. "
            f"Proceeding to cleanup form access."
        )

    # 2. Revoke Form Access for all users of this company for this event
    # Find users of the company
    company_users = db.execute(
        select(UserCompany.UserID)
        .join(UserCompanyStatus)
        .where(
            UserCompany.CompanyID == company_id,
            UserCompany.IsDeleted== False,  # type: ignore[arg-type]
            UserCompanyStatus.StatusCode == 'active'
        )
    ).scalars().all()
    
    if company_users:
        # Find forms for this event
        event_forms = db.execute(
            select(Form.FormID).where(
                Form.EventID == event_id,
                Form.IsDeleted== False  # type: ignore[arg-type]
            )
        ).scalars().all()
        
        if event_forms:
            # Soft delete FormAccessControl records
            # We update IsDeleted=True
            access_controls = db.execute(
                select(FormAccessControl).where(
                    FormAccessControl.FormID.in_(event_forms),
                    FormAccessControl.UserID.in_(company_users),
                    FormAccessControl.IsDeleted== False  # type: ignore[arg-type]
                )
            ).scalars().all()
            
            for ac in access_controls:
                ac.IsDeleted = True  # type: ignore[assignment]
                ac.UpdatedDate = datetime.utcnow()  # type: ignore[assignment]
                ac.UpdatedBy = user_id  # type: ignore[assignment]
                
            logger.info(
                f"Revoked form access for {len(access_controls)} records for CompanyID={company_id} on EventID={event_id}"
            )

    db.commit()
    
    return True


async def get_event_company_role_by_code(
    db: Session,
    role_code: str
) -> Optional[EventCompanyRole]:
    """
    Get EventCompanyRole by role code.
    
    Args:
        db: Database session
        role_code: Role code ('event_owner', 'event_organizer', 'event_participant')
        
    Returns:
        EventCompanyRole object if found, None otherwise
    """
    role = db.execute(
        select(EventCompanyRole).where(
            EventCompanyRole.RoleCode == role_code,
            EventCompanyRole.IsActive== True  # type: ignore[arg-type]
        )
    ).scalar_one_or_none()
    
    return role

