"""
EventCompany Service Module
Business logic for EventCompany relationship management
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_, or_, text
from typing import Optional, List, Dict, Any
from datetime import datetime

from models.event_company import EventCompany
from models.ref.event_company_role import EventCompanyRole
from models.ref.event_status import EventStatus
from models.event import Event
from models.company import Company
from models.form import Form
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
            EventCompany.IsActive == True,
            EventCompany.IsDeleted == False
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
        EventCompany.IsDeleted == False
    )
    
    if active_only:
        query = query.filter(EventCompany.IsActive == True)
    
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
        EventCompany.IsDeleted == False
    )
    
    if active_only:
        query = query.filter(EventCompany.IsActive == True)
    
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
            # Get all forms for this event that belong to the company
            forms = db.execute(
                select(Form).where(
                    Form.EventID == event.EventID,
                    Form.CompanyID == company_id,  # Only check forms owned by this company
                    Form.IsDeleted == False
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
                    # If function doesn't exist or error occurs, log and skip this form
                    error_msg = str(e)
                    if "fn_GetUserFormAccess" in error_msg or "Invalid object name" in error_msg:
                        logger.warning(f"Database function fn_GetUserFormAccess not found. Skipping form access check for EventID={event.EventID}")
                    else:
                        logger.warning(f"Error checking form access for FormID={form.FormID}, EventID={event.EventID}: {error_msg}")
                    # Continue checking other forms
        
        # CRITICAL: Also include events where the company has forms (even if not linked via EventCompany)
        # This handles the case where a company owns forms for an event but the event is not linked via EventCompany
        # For Company Viewers, we need to include events where they have form access, regardless of EventCompany linkage
        additional_events_query = db.execute(
            text("""
                SELECT DISTINCT f.EventID
                FROM [dbo].[Form] f
                WHERE f.CompanyID = :company_id
                  AND f.EventID IS NOT NULL
                  AND f.IsDeleted = 0
                  AND EXISTS (
                      SELECT 1
                      FROM [dbo].[fn_GetUserFormAccess](:user_id, f.FormID) a
                      WHERE a.CanView = 1
                  )
            """),
            {"company_id": company_id, "user_id": user_id}
        ).fetchall()
        
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
                    .where(Event.IsDeleted == False)
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
    Disassociate a company from an event (soft delete participant relationship).
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID
        user_id: User ID performing disassociation
        
    Returns:
        True if disassociation successful, False otherwise
        
    Raises:
        ValueError: If relationship not found or cannot be disassociated
    """
    # Find active relationship
    event_company = db.execute(
        select(EventCompany).where(
            EventCompany.EventID == event_id,
            EventCompany.CompanyID == company_id,
            EventCompany.IsActive == True,
            EventCompany.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if not event_company:
        raise ValueError(
            f"Active EventCompany relationship not found for EventID={event_id}, CompanyID={company_id}"
        )
    
    # Get role to check if it's a participant (only participants can be disassociated)
    role = db.execute(
        select(EventCompanyRole).where(
            EventCompanyRole.EventCompanyRoleID == event_company.EventCompanyRoleID
        )
    ).scalar_one_or_none()
    
    if role and role.RoleCode != 'event_participant':
        raise ValueError(
            f"Cannot disassociate company with role '{role.RoleCode}'. Only participants can be disassociated."
        )
    
    # Soft delete relationship
    event_company.IsActive = False
    event_company.DisassociatedDate = datetime.utcnow()
    event_company.DisassociatedBy = user_id
    event_company.UpdatedDate = datetime.utcnow()
    event_company.UpdatedBy = user_id
    
    db.commit()
    
    logger.info(
        f"Disassociated company from event: EventID={event_id}, CompanyID={company_id}, "
        f"EventCompanyID={event_company.EventCompanyID}"
    )
    
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
            EventCompanyRole.IsActive == True
        )
    ).scalar_one_or_none()
    
    return role

