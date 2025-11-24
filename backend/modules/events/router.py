"""
Event Management Router
Endpoints for event CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, text
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from models.event import Event
from models.form import Form
from models.ref.event_type import EventType
from models.ref.event_status import EventStatus
from models.ref.industry import Industry
from .schemas import (
    EventCreateSchema,
    EventUpdateSchema,
    EventResponse,
    EventListResponse,
    CreateEventResponse,
    UpdateEventResponse,
    DeleteEventResponse,
    EventTypeResponse,
    EventStatusResponse,
    IndustryResponse,
    CompanySummaryResponse,
    ShareEventRequest,
    ShareEventResponse,
    ShareEventByEmailRequest
)
from .service import (
    create_event,
    get_events,
    get_event_by_id,
    update_event,
    delete_event,
    search_events,
    get_event_types,
    get_event_statuses,
    search_company_network_events
)
from .event_company_service import (
    create_event_company_relationship,
    get_event_companies,
    get_company_events,
    disassociate_company_from_event,
    get_event_company_role_by_code
)
from .inference_service import (
    get_country_from_timezone,
    get_user_profile_with_location,
    get_company_profile_with_billing,
    get_recent_event_cities
)
from common.logger import get_logger
from services.email_service import get_email_service
from fastapi import BackgroundTasks

logger = get_logger(__name__)

router = APIRouter(prefix="/api/events", tags=["events"])


# =====================================================================
# Reference Data Endpoints
# =====================================================================

@router.get(
    "/reference/types",
    response_model=List[EventTypeResponse],
    summary="Get event types",
    description="Get all active event types for dropdown selections"
)
async def get_reference_event_types(db: Session = Depends(get_db)) -> List[EventTypeResponse]:
    """Get all active event types for selection."""
    try:
        event_types = await get_event_types(db)
        return [
            EventTypeResponse(
                EventTypeID=int(et.EventTypeID),
                TypeCode=str(et.TypeCode),
                TypeName=str(et.TypeName),
                TypeDescription=str(et.TypeDescription) if et.TypeDescription else None,
                IsActive=bool(et.IsActive),
                SortOrder=int(et.SortOrder)
            )
            for et in event_types
        ]
    except Exception as e:
        logger.error(f"Error fetching event types: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch event types"
        )


@router.get(
    "/public/search",
    response_model=EventListResponse,
    summary="Search public events",
    description="Search public events across all companies (for registration)"
)
async def search_public_events(
    q: Optional[str] = Query(None, description="Search term (optional)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    db: Session = Depends(get_db)
) -> EventListResponse:
    """
    Search public events across all companies (AC-2.4.x).
    
    Returns only approved public events that users can register for.
    Does not require authentication (public endpoint).
    """
    try:
        from modules.events.service import search_public_events as search_public_events_service
        
        events = await search_public_events_service(
            db=db,
            search_term=q,
            limit=limit
        )
        
        event_responses = [_event_to_response(e) for e in events]
        
        logger.info(f"Public event search: {len(event_responses)} events found for term='{q}'")
        
        return EventListResponse(
            events=event_responses,
            total=len(event_responses),
            page=1,
            page_size=limit
        )
        
    except Exception as e:
        logger.error(f"Error searching public events: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search public events"
        )


@router.get(
    "/company-network/search",
    response_model=EventListResponse,
    summary="Search company network visible events",
    description="Search events visible to the company and its linked network (includes platform-approved events)"
)
async def search_company_network_visible_events(
    q: Optional[str] = Query(None, description="Search term (optional)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EventListResponse:
    """
    Search events visible to the authenticated company's network (company-owned, linked companies, or platform-approved).
    """
    try:
        events, total = await search_company_network_events(
            db=db,
            company_id=current_user.company_id,
            search_term=q,
            limit=limit
        )

        event_responses = [_event_to_response(e, company_id=current_user.company_id, db=db) for e in events]

        logger.info(
            f"Company network event search: {len(event_responses)} events found for company={current_user.company_id}, term='{q}'"
        )

        return EventListResponse(
            events=event_responses,
            total=total,
            page=1,
            page_size=limit
        )

    except Exception as e:
        logger.error(f"Error searching company network events: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search company network events"
        )


@router.get(
    "/reference/statuses",
    response_model=List[EventStatusResponse],
    summary="Get event statuses",
    description="Get all active event statuses for dropdown selections"
)
async def get_reference_event_statuses(db: Session = Depends(get_db)) -> List[EventStatusResponse]:
    """Get all active event statuses for selection."""
    try:
        event_statuses = await get_event_statuses(db)
        return [
            EventStatusResponse(
                EventStatusID=int(es.EventStatusID),
                StatusCode=str(es.StatusCode),
                StatusName=str(es.StatusName),
                StatusDescription=str(es.StatusDescription) if es.StatusDescription else None,
                StatusColor=str(es.StatusColor) if es.StatusColor else None,
                StatusIcon=str(es.StatusIcon) if es.StatusIcon else None,
                IsActive=bool(es.IsActive),
                SortOrder=int(es.SortOrder)
            )
            for es in event_statuses
        ]
    except Exception as e:
        logger.error(f"Error fetching event statuses: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch event statuses"
        )


# =====================================================================
# CRUD Endpoints
# =====================================================================

@router.post(
    "",
    response_model=CreateEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create event",
    description="Create a new event for the company"
)
async def create_new_event(
    request: EventCreateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CreateEventResponse:
    """
    Create a new event for the company (AC-2.4.2).
    
    Requires authentication and company context.
    Validates required fields and reference data.
    """
    try:
        # Convert Pydantic model to dict for service layer
        event_data = request.dict(exclude_none=True)
        
        # Create event
        event = await create_event(
            db=db,
            user_id=current_user.user_id,
            company_id=current_user.company_id,
            event_data=event_data
        )
        
        db.commit()
        db.refresh(event)
        
        # Convert to response model
        event_response = _event_to_response(event, company_id=current_user.company_id, db=db)
        
        logger.info(f"Event created successfully: EventID={event.EventID}")
        
        return CreateEventResponse(
            success=True,
            message="Event created successfully",
            event_id=event.EventID,
            event=event_response
        )
        
    except ValueError as e:
        logger.warning(f"Invalid event creation request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_detail = str(e)
        logger.error(f"Error creating event: {error_detail}", exc_info=True)
        db.rollback()
        # Include the actual error message in the response for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {error_detail}"
        )


@router.get(
    "",
    response_model=EventListResponse,
    summary="List company events",
    description="Get all events for the company with optional filters"
)
async def list_company_events(
    event_type_id: Optional[int] = Query(None, description="Filter by event type"),
    status_id: Optional[int] = Query(None, description="Filter by status"),
    industry_id: Optional[int] = Query(None, description="Filter by industry"),
    date_from: Optional[datetime] = Query(None, description="Filter by start date from"),
    date_to: Optional[datetime] = Query(None, description="Filter by start date to"),
    search: Optional[str] = Query(None, description="Search by name/description"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EventListResponse:
    """
    List all events for the company with optional filters (AC-2.4.1, AC-2.4.11, AC-2.4.12).
    
    Requires authentication and company context.
    Automatically filters by CompanyID for multi-tenant isolation.
    
    System Admins: Returns ALL events in the platform (bypasses company filtering)
    """
    try:
        # Build filters dict
        filters = {}
        if event_type_id:
            filters['event_type_id'] = event_type_id
        if status_id:
            filters['status_id'] = status_id
        if industry_id:
            filters['industry_id'] = industry_id
        if date_from:
            filters['date_from'] = date_from
        if date_to:
            filters['date_to'] = date_to
        if search:
            filters['search'] = search
        
        # Ensure company context exists (required for all roles now)
        if not current_user.company_id:
             if current_user.role == "system_admin":
                 logger.warning("System Admin listing events without company context - returning empty list")
                 return EventListResponse(events=[], total=0, page=page, page_size=page_size)
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company context required")

        # System Admins previously saw ALL events here (bypassing company). 
        # We now force them to use the standard flow below (company-scoped), 
        # but the "system_admin" role will bypass form access checks in get_company_events.
        if False and current_user.role == "system_admin":
             pass # Code removed/disabled
        
        # Regular users AND System Admins (in company context): Get events from BOTH sources:
        # 1. Events from EventCompany relationships (includes participant events)
        # 2. Events directly owned by company (for legacy events without EventCompany records)
        # Filter by user form access: only show events where user has access to at least one form
        # (Skipped for Company Admins and Company Users - they see all company events)
        events_from_relationships = await get_company_events(
            db=db,
            company_id=current_user.company_id,
            active_only=True,
            include_participant=True,
            user_id=current_user.user_id,
            user_role=current_user.role
        )
        
        # Get events directly owned by company (for legacy events without EventCompany records)
        events_directly_owned = await get_events(
            db=db,
            company_id=current_user.company_id,
            filters=None  # Don't apply filters here - we'll apply them after merging
        )
        
        # Merge both lists and remove duplicates (by EventID)
        event_ids_seen = set()
        events = []
        for event in events_from_relationships:
            if event.EventID not in event_ids_seen:
                events.append(event)
                event_ids_seen.add(event.EventID)
        
        # Add directly owned events that aren't already in the list
        for event in events_directly_owned:
            if event.EventID not in event_ids_seen:
                events.append(event)
                event_ids_seen.add(event.EventID)
        
        # Filter events by user form access (apply to merged list)
        # Only include events where user has access to at least one form
        # Skip filtering for Company Admins and Company Users - they should see all company events
        if events and current_user.role not in ["company_admin", "company_user", "system_admin"]:
            accessible_event_ids = set()
            
            for event in events:
                # Get all forms for this event
                forms = db.execute(
                    select(Form).where(
                        Form.EventID == event.EventID,
                        Form.IsDeleted == False
                    )
                ).scalars().all()
                
                # For Company Viewers: Only include events where user has access to at least one form
                # Events with no forms are NOT accessible to Company Viewers
                # (Company Admins and Company Users would see all events, but they're filtered out above)
                if not forms:
                    # Event has no forms - Company Viewer cannot have access
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
                            {"user_id": current_user.user_id, "form_id": form.FormID}
                        ).fetchone()
                        
                        if result and bool(result.CanView):
                            # User has access to at least one form in this event
                            accessible_event_ids.add(event.EventID)
                            break  # No need to check other forms for this event
                    except Exception as e:
                        # If function doesn't exist or error occurs, log and skip this form
                        error_msg = str(e)
                        if "fn_GetUserFormAccess" in error_msg or "Invalid object name" in error_msg:
                            logger.error(f"Database function fn_GetUserFormAccess not found. This indicates migrations haven't been run. Event filtering may not work correctly for EventID={event.EventID}")
                            # If the function doesn't exist, we can't filter properly, so skip this event
                            # This ensures that events are only shown if we can verify access
                            break  # Skip to next event
                        else:
                            logger.warning(f"Error checking form access for FormID={form.FormID}, EventID={event.EventID}: {error_msg}")
                        # Continue checking other forms
            
            # Filter events to only include those where user has access to at least one form
            events = [e for e in events if e.EventID in accessible_event_ids]
        
        logger.info(f"Filtered merged events to {len(events)} events where UserID={current_user.user_id} (role={current_user.role}) has form access")
        
        # Apply additional filters if provided
        if filters:
            if filters.get('event_type_id'):
                events = [e for e in events if e.EventTypeID == filters['event_type_id']]
            
            if filters.get('status_id'):
                events = [e for e in events if e.EventStatusID == filters['status_id']]
            
            if filters.get('industry_id'):
                events = [e for e in events if e.IndustryID == filters.get('industry_id')]
            
            if filters.get('date_from'):
                events = [e for e in events if e.StartDateTime and e.StartDateTime >= filters['date_from']]
            
            if filters.get('date_to'):
                events = [e for e in events if e.StartDateTime and e.StartDateTime <= filters['date_to']]
            
            if filters.get('search'):
                search_term = filters['search'].lower()
                events = [
                    e for e in events
                    if (e.Name and search_term in e.Name.lower())
                    or (e.Description and search_term in e.Description.lower())
                    or (e.ShortDescription and search_term in e.ShortDescription.lower())
                ]
        
        # Sort by start date descending (most recent first)
        events.sort(key=lambda e: e.StartDateTime if e.StartDateTime else datetime.min, reverse=True)
        
        # Convert to response models with user role
        event_responses = [_event_to_response(e, company_id=current_user.company_id, db=db) for e in events]
        
        logger.info(f"Retrieved {len(event_responses)} events for CompanyID={current_user.company_id}")
        
        return EventListResponse(
            events=event_responses,
            total=len(event_responses),
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Error listing events: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list events"
        )


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get event details",
    description="Get a single event by ID"
)
async def get_event_details(
    event_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EventResponse:
    """
    Get a single event by ID (AC-2.4.4).
    
    Requires authentication and company context.
    Verifies event belongs to company.
    """
    try:
        # First try to get event owned by company
        event = await get_event_by_id(
            db=db,
            event_id=event_id,
            company_id=current_user.company_id
        )
        
        # If not found, check if event exists and company is a participant
        if not event:
            # Check if event exists (public event or participant relationship)
            # Filter by user form access: only show events where user has access to at least one form
            # (Skipped for Company Admins and Company Users - they see all company events)
            from modules.events.event_company_service import get_company_events
            company_events = await get_company_events(
                db=db,
                company_id=current_user.company_id,
                active_only=True,
                include_participant=True,
                user_id=current_user.user_id,
                user_role=current_user.role
            )
            
            event = next((e for e in company_events if e.EventID == event_id), None)
            
            if not event:
                # Check if event exists at all (for public events)
                event = (
                    db.query(Event)
                    .options(
                        joinedload(Event.event_type),
                        joinedload(Event.event_status),
                        joinedload(Event.public_review_status),
                        joinedload(Event.industry),
                        joinedload(Event.organizer_company),
                        joinedload(Event.company)
                    )
                    .filter(
                        Event.EventID == event_id,
                        Event.IsDeleted == False
                    )
                    .first()
                )
                
                if not event:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Event not found: {event_id}"
                    )
        
        event_response = _event_to_response(event, company_id=current_user.company_id, db=db)
        
        logger.info(f"Retrieved event: EventID={event_id}")
        
        return event_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching event: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch event"
        )


@router.put(
    "/{event_id}",
    response_model=UpdateEventResponse,
    summary="Update event",
    description="Update an existing event"
)
async def update_existing_event(
    event_id: int,
    request: EventUpdateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UpdateEventResponse:
    """
    Update an existing event (AC-2.4.3).
    
    Requires authentication and company context.
    Verifies event belongs to company.
    """
    try:
        # Convert Pydantic model to dict for service layer
        event_data = request.dict(exclude_none=True)
        
        # Normalize placeholder values from frontend ("-1" means "don't update this field")
        # If field has "-1", remove it from event_data so service layer won't update it
        if 'organizer_contact_email' in event_data and event_data['organizer_contact_email'] == "-1":
            del event_data['organizer_contact_email']
            logger.debug(f"Removed organizer_contact_email from update (placeholder value)")
        if 'organizer_website' in event_data and event_data['organizer_website'] == "-1":
            del event_data['organizer_website']
            logger.debug(f"Removed organizer_website from update (placeholder value)")
        
        logger.debug(f"Update event data for EventID={event_id}: {list(event_data.keys())}")
        
        # Update event
        event = await update_event(
            db=db,
            event_id=event_id,
            company_id=current_user.company_id,
            user_id=current_user.user_id,
            event_data=event_data
        )
        
        db.commit()
        db.refresh(event)
        
        event_response = _event_to_response(event, company_id=current_user.company_id, db=db)
        
        logger.info(f"Event updated successfully: EventID={event_id}")
        
        return UpdateEventResponse(
            success=True,
            message="Event updated successfully",
            event_id=event_id,
            event=event_response
        )
        
    except ValueError as e:
        logger.warning(f"Invalid event update request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating event: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update event"
        )


@router.delete(
    "/{event_id}",
    response_model=DeleteEventResponse,
    summary="Delete event",
    description="Archive an event (sets status to Archived)"
)
async def delete_existing_event(
    event_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> DeleteEventResponse:
    """
    Archive an event (AC-2.4.5).
    
    Requires authentication and company context.
    Verifies event belongs to company.
    Archives the event by setting status to Archived (EventStatusID=7).
    Archived events are hidden from customer-facing lists.
    """
    try:
        await delete_event(
            db=db,
            event_id=event_id,
            company_id=current_user.company_id,
            user_id=current_user.user_id
        )
        
        db.commit()
        
        logger.info(f"Event deleted successfully: EventID={event_id}")
        
        return DeleteEventResponse(
            success=True,
            message="Event deleted successfully",
            event_id=event_id
        )
        
    except ValueError as e:
        logger.warning(f"Invalid event deletion request: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting event: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete event"
        )


@router.get(
    "/search",
    response_model=EventListResponse,
    summary="Search events",
    description="Search events by name, description, or short description"
)
async def search_company_events(
    q: str = Query(..., min_length=1, description="Search term"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EventListResponse:
    """
    Search events by name/description (AC-2.4.12).
    
    Requires authentication and company context.
    Only searches within company's events.
    """
    try:
        events = await search_events(
            db=db,
            company_id=current_user.company_id,
            search_term=q
        )
        
        event_responses = [_event_to_response(e, company_id=current_user.company_id, db=db) for e in events]
        
        logger.info(f"Search results: {len(event_responses)} events found for term='{q}'")
        
        return EventListResponse(
            events=event_responses,
            total=len(event_responses),
            page=1,
            page_size=20
        )
        
    except Exception as e:
        logger.error(f"Error searching events: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search events"
        )


# =====================================================================
# Helper Functions
# =====================================================================

def _event_to_response(event: Event, company_id: Optional[int] = None, db: Optional[Session] = None) -> EventResponse:
    """Convert Event model to EventResponse schema with relationship data."""
    # Get relationship data
    event_type_response = None
    if event.event_type:
        event_type_response = EventTypeResponse(
            EventTypeID=event.event_type.EventTypeID,
            TypeCode=event.event_type.TypeCode,
            TypeName=event.event_type.TypeName,
            TypeDescription=event.event_type.TypeDescription,
            IsActive=event.event_type.IsActive,
            SortOrder=event.event_type.SortOrder
        )
    
    event_status_response = None
    if event.event_status:
        event_status_response = EventStatusResponse(
            EventStatusID=event.event_status.EventStatusID,
            StatusCode=event.event_status.StatusCode,
            StatusName=event.event_status.StatusName,
            StatusDescription=event.event_status.StatusDescription,
            StatusColor=event.event_status.StatusColor,
            StatusIcon=event.event_status.StatusIcon,
            IsActive=event.event_status.IsActive,
            SortOrder=event.event_status.SortOrder
        )
    
    industry_response = None
    if event.industry:
        industry_response = IndustryResponse(
            IndustryID=event.industry.IndustryID,
            IndustryCode=event.industry.IndustryCode,
            IndustryName=event.industry.IndustryName,
            Description=event.industry.Description,
            IsActive=event.industry.IsActive,
            SortOrder=event.industry.SortOrder
        )
    
    organizer_company_response = None
    if event.organizer_company:
        organizer_company_response = CompanySummaryResponse(
            CompanyID=event.organizer_company.CompanyID,
            CompanyName=event.organizer_company.CompanyName,
            LegalEntityName=event.organizer_company.LegalEntityName,
            ABN=event.organizer_company.ABN,
            ACN=event.organizer_company.ACN,
            Website=event.organizer_company.Website,
            CountryID=event.organizer_company.CountryID
        )
    
    owner_company_response = None
    if event.company:
        owner_company_response = CompanySummaryResponse(
            CompanyID=event.company.CompanyID,
            CompanyName=event.company.CompanyName,
            LegalEntityName=event.company.LegalEntityName,
            ABN=event.company.ABN,
            ACN=event.company.ACN,
            Website=event.company.Website,
            CountryID=event.company.CountryID
        )
    
    # Get user role for this event if company_id is provided
    user_role_response = None
    if company_id and db:
        try:
            from modules.events.event_company_service import get_event_companies
            from modules.events.schemas import EventUserRole
            
            # Get all companies for this event (sync call since we're in a sync function)
            # Note: get_event_companies is async, but we'll make it work synchronously
            # For now, we'll query directly in the sync function
            from models.event_company import EventCompany
            from models.ref.event_company_role import EventCompanyRole
            from sqlalchemy import select
            from sqlalchemy.orm import joinedload
            
            # Query EventCompany relationships for this event
            event_companies_query = db.query(EventCompany).options(
                joinedload(EventCompany.role)
            ).filter(
                EventCompany.EventID == event.EventID,
                EventCompany.CompanyID == company_id,
                EventCompany.IsActive == True,
                EventCompany.IsDeleted == False
            )
            
            user_relationship = event_companies_query.first()
            
            if user_relationship:
                # Get role details
                role = user_relationship.role
                if role:
                    user_role_response = EventUserRole(
                        role_code=role.RoleCode,
                        role_name=role.RoleName,
                        has_edit_event=role.HasEditEvent,
                        has_delete_event=role.HasDeleteEvent,
                        has_manage_participants=role.HasManageParticipants,
                        has_view_event=role.HasViewEvent,
                        is_legacy=False
                    )
            else:
                # Check if event is owned directly by company (legacy)
                if event.CompanyID == company_id:
                    user_role_response = EventUserRole(
                        role_code="event_owner",
                        role_name="Owner",
                        has_edit_event=True,
                        has_delete_event=True,
                        has_manage_participants=True,
                        has_view_event=True,
                        is_legacy=True
                    )
        except Exception as e:
            # If role lookup fails, just continue without role (don't fail the response)
            logger.debug(f"Error getting user role for event {event.EventID}: {str(e)}")
    
    # Get public review status response if available
    from .schemas import PublicReviewStatusResponse
    public_review_status_response = None
    if event.public_review_status:
        public_review_status_response = PublicReviewStatusResponse(
            PublicReviewStatusID=event.public_review_status.PublicReviewStatusID,
            StatusCode=event.public_review_status.StatusCode,
            StatusName=event.public_review_status.StatusName,
            StatusDescription=event.public_review_status.StatusDescription,
            StatusColor=event.public_review_status.StatusColor,
            StatusIcon=event.public_review_status.StatusIcon,
            IsActive=event.public_review_status.IsActive,
            SortOrder=event.public_review_status.SortOrder
        )
    
    return EventResponse(
        EventID=event.EventID,
        Name=event.Name,
        Description=event.Description,
        ShortDescription=event.ShortDescription,
        CompanyID=event.CompanyID,
        CreatedBy=event.CreatedBy,
        StartDateTime=event.StartDateTime,
        EndDateTime=event.EndDateTime,
        TimezoneIdentifier=event.TimezoneIdentifier,
        VenueName=event.VenueName,
        VenueAddress=event.VenueAddress,
        City=event.City,
        State=event.State,
        CountryID=event.CountryID,
        Latitude=event.Latitude,
        Longitude=event.Longitude,
        EventTypeID=event.EventTypeID,
        event_type=event_type_response,
        IndustryID=event.IndustryID,
        Industry=industry_response,
        Tags=event.Tags,
        IsPublic=event.IsPublic,
        IsSharedWithPlatform=event.IsSharedWithPlatform if hasattr(event, 'IsSharedWithPlatform') else False,
        IsPublicReviewRequired=event.IsPublicReviewRequired if hasattr(event, 'IsPublicReviewRequired') else False,
        PublicReviewStatusID=event.PublicReviewStatusID,
        public_review_status=public_review_status_response,
        PublicReviewDate=event.PublicReviewDate,
        PublicReviewBy=event.PublicReviewBy,
        PublicReviewComments=event.PublicReviewComments,
        PublicVisibilityDate=event.PublicVisibilityDate,
        EventStatusID=event.EventStatusID,
        event_status=event_status_response,
        IsRecurring=event.IsRecurring,
        OrganizerCompanyID=event.OrganizerCompanyID,
        OrganizerContactEmail=event.OrganizerContactEmail,
        OrganizerWebsite=event.OrganizerWebsite,
        OrganizerCompany=organizer_company_response,
        OwnerCompany=owner_company_response,
        ExpectedAttendees=event.ExpectedAttendees,
        ActualAttendees=event.ActualAttendees,
        FormsCreated=event.FormsCreated,
        TotalSubmissions=event.TotalSubmissions,
        CreatedDate=event.CreatedDate,
        UpdatedDate=event.UpdatedDate,
        UpdatedBy=event.UpdatedBy,
        user_role=user_role_response
    )


# =====================================================================
# EventCompany Relationship Endpoints
# =====================================================================

@router.post(
    "/{event_id}/participate",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Create participant relationship",
    description="Create EventCompany relationship with event_participant role when user selects existing public event (AC-2.4.2, AC-2.4.11)."
)
async def create_participant_relationship(
    event_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Create participant relationship when user selects existing public event.
    
    Creates EventCompany relationship with event_participant role.
    User's company becomes a participant in the event.
    """
    try:
        # Verify event exists and is public
        event = await get_event_by_id(db, event_id, current_user.company_id)
        if not event:
            # Check if event exists but is public (not owned by user's company)
            event = (
                db.query(Event)
                .options(
                    joinedload(Event.event_type),
                    joinedload(Event.event_status),
                    joinedload(Event.public_review_status),
                    joinedload(Event.industry),
                    joinedload(Event.organizer_company),
                    joinedload(Event.company)
                )
                .filter(
                    Event.EventID == event_id,
                    Event.IsPublic == True,
                    Event.IsDeleted == False
                )
                .first()
            )
            
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Event {event_id} not found"
                )
        
        # Check if relationship already exists (idempotent)
        from modules.events.event_company_service import get_event_companies
        existing_companies = await get_event_companies(db, event_id, active_only=True)
        existing_relationship = next(
            (ec for ec in existing_companies if ec.CompanyID == current_user.company_id),
            None
        )
        
        if existing_relationship:
            # Relationship already exists - return success (idempotent)
            logger.info(
                f"Participant relationship already exists: EventID={event_id}, "
                f"CompanyID={current_user.company_id}, EventCompanyID={existing_relationship.EventCompanyID}"
            )
            return {
                "success": True,
                "message": "You're already using this public event",
                "event_company_id": existing_relationship.EventCompanyID,
                "event_id": event_id,
                "company_id": current_user.company_id,
                "role": "event_participant",
                "already_exists": True
            }
        
        # Create participant relationship
        event_company = await create_event_company_relationship(
            db=db,
            event_id=event_id,
            company_id=current_user.company_id,
            role_code='event_participant',
            user_id=current_user.user_id
        )
        
        logger.info(
            f"Created participant relationship: EventID={event_id}, "
            f"CompanyID={current_user.company_id}, UserID={current_user.user_id}"
        )
        
        return {
            "success": True,
            "message": "You're now using this public event",
            "event_company_id": event_company.EventCompanyID,
            "event_id": event_id,
            "company_id": current_user.company_id,
            "role": "event_participant",
            "already_exists": False
        }
        
    except ValueError as e:
        logger.error(f"Error creating participant relationship: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating participant relationship: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create participant relationship"
        )


@router.post(
    "/{event_id}/share",
    response_model=ShareEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Share event with another company",
    description="Grant another company access to this event with a specific role (e.g., Agency)."
)
async def share_event_with_company(
    event_id: int,
    request: ShareEventRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ShareEventResponse:
    """
    Share an event with another company (e.g., Host Company shares with Agency).
    
    Requires 'manage_participants' permission on the event.
    """
    try:
        # Verify event exists and user has access
        # We need to check if the user has 'manage_participants' permission
        from modules.events.event_company_service import get_event_companies
        
        # Get all companies for this event to check user's role
        event_companies = await get_event_companies(
            db=db,
            event_id=event_id,
            active_only=True
        )
        
        # Find current user's company role
        user_relationship = next(
            (ec for ec in event_companies if ec.CompanyID == current_user.company_id),
            None
        )
        
        has_manage_permission = False
        
        if user_relationship and user_relationship.role and user_relationship.role.HasManageParticipants:
            has_manage_permission = True
        else:
            # Check if user is from the owner company (legacy or explicit)
            event = await get_event_by_id(db, event_id, current_user.company_id)
            if event and event.CompanyID == current_user.company_id:
                has_manage_permission = True
        
        if not has_manage_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to share this event"
            )
            
        # Check if relationship already exists
        existing_relationship = next(
            (ec for ec in event_companies if ec.CompanyID == request.company_id),
            None
        )
        
        if existing_relationship:
            return ShareEventResponse(
                success=True,
                message=f"Company is already linked to this event with role: {existing_relationship.role.RoleName if existing_relationship.role else 'Unknown'}",
                event_company_id=existing_relationship.EventCompanyID,
                event_id=event_id,
                company_id=request.company_id,
                role=existing_relationship.role.RoleCode if existing_relationship.role else 'unknown',
                already_exists=True
            )
            
        # Create relationship
        event_company = await create_event_company_relationship(
            db=db,
            event_id=event_id,
            company_id=request.company_id,
            role_code=request.role_code,
            user_id=current_user.user_id
        )
        
        logger.info(
            f"Shared event {event_id} with company {request.company_id} (Role: {request.role_code}) by user {current_user.user_id}"
        )
        
        return ShareEventResponse(
            success=True,
            message="Event shared successfully",
            event_company_id=event_company.EventCompanyID,
            event_id=event_id,
            company_id=request.company_id,
            role=request.role_code,
            already_exists=False
        )
        
    except ValueError as e:
        logger.warning(f"Invalid share request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sharing event: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share event"
        )



@router.post(
    "/{event_id}/share-by-email",
    response_model=ShareEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Share event via email",
    description="Share an event with a user by email. If the user exists, links their company."
)
async def share_event_by_email(
    event_id: int,
    request: ShareEventByEmailRequest,
    background_tasks: BackgroundTasks,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ShareEventResponse:
    """
    Share an event with a user by email.
    
    1. Finds user by email.
    2. If found, finds their active company.
    3. Creates EventCompany relationship.
    4. Requires 'manage_participants' permission.
    5. Sends email notification to the user.
    """
    try:
        # Verify event exists and user has access (same permission check as standard share)
        from modules.events.event_company_service import get_event_companies
        
        event_companies = await get_event_companies(
            db=db,
            event_id=event_id,
            active_only=True
        )
        
        # Find current user's company role
        user_relationship = next(
            (ec for ec in event_companies if ec.CompanyID == current_user.company_id),
            None
        )
        
        has_manage_permission = False
        
        if user_relationship and user_relationship.role and user_relationship.role.HasManageParticipants:
            has_manage_permission = True
        else:
            # Check if user is from the owner company (legacy or explicit)
            event = await get_event_by_id(db, event_id, current_user.company_id)
            if event and event.CompanyID == current_user.company_id:
                has_manage_permission = True
        
        if not has_manage_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to share this event"
            )

        # Find user by email
        from models.user import User
        target_user = db.query(User).filter(User.Email == request.email).first()
        
        if not target_user:
            # TODO: In future stories, this could trigger an invitation flow
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please ask them to sign up first."
            )
            
        # Find user's active company
        # We prioritize 'active' status and maybe 'owner' or 'admin' roles if multiple
        from models.user_company import UserCompany
        from models.ref.user_company_status import UserCompanyStatus
        from models.company import Company
        
        target_user_companies = db.query(UserCompany).join(UserCompanyStatus).filter(
            UserCompany.UserID == target_user.UserID,
            UserCompany.IsDeleted == False,
            UserCompanyStatus.StatusCode == 'active'
        ).all()
        
        if not target_user_companies:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User exists but is not associated with any active company."
            )
            
        # Logic to pick the "primary" company if multiple:
        # For now, just pick the first one. In future, could prompt or pick based on role.
        target_company_id = target_user_companies[0].CompanyID
        target_company = db.get(Company, target_company_id)

        if not target_company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target company not found"
            )
        
        # Check if relationship already exists
        existing_relationship = next(
            (ec for ec in event_companies if ec.CompanyID == target_company_id),
            None
        )
        
        # Fetch inviter details for email
        inviter = db.get(User, current_user.user_id)
        inviter_company = db.get(Company, current_user.company_id)
        
        # If relationship already exists, we still might want to notify them?
        # Or just return as before. For now, keep existing behavior but maybe warn.
        if existing_relationship:
            return ShareEventResponse(
                success=True,
                message=f"User's company ({target_company.CompanyName}) is already linked to this event.",
                event_company_id=existing_relationship.EventCompanyID,
                event_id=event_id,
                company_id=target_company_id,
                role=existing_relationship.role.RoleCode if existing_relationship.role else 'unknown',
                already_exists=True
            )

        # Create relationship
        event_company = await create_event_company_relationship(
            db=db,
            event_id=event_id,
            company_id=target_company_id,
            role_code=request.role_code,
            user_id=current_user.user_id
        )
        
        # Send email notification
        try:
            # Get event details for email
            event_details = await get_event_by_id(db, event_id, current_user.company_id)
            if not event_details:
                 # Fallback if not directly owned
                 event_details = db.get(Event, event_id)

            if event_details:
                email_service = get_email_service()
                # Use FRONTEND_URL from env, defaulting to localhost:3000 if not set
                import os
                frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
                event_url = f"{frontend_url}/dashboard/events" # Direct deep link if supported, else list
                
                background_tasks.add_task(
                    email_service.send_email,
                    to=str(target_user.Email),
                    subject=f"Access Granted: {event_details.Name} - EventLead Platform",
                    template_name="event_shared",
                    template_vars={
                        "recipient_name": target_user.FirstName,
                        "inviter_name": f"{inviter.FirstName} {inviter.LastName}" if inviter else "An administrator",
                        "inviter_company_name": inviter_company.CompanyName if inviter_company else "Host Company",
                        "event_name": event_details.Name,
                        "role_name": "Agency Form Builder" if request.role_code == "agency_form_builder" else request.role_code,
                        "event_url": event_url
                    }
                )
                logger.info(f"Queued share notification email to {target_user.Email}")
        except Exception as email_err:
            logger.error(f"Failed to queue share notification email: {str(email_err)}")
            # Don't fail the request if email fails, but log it
        
        logger.info(
            f"Shared event {event_id} with user {request.email} (Company: {target_company.CompanyName}) by user {current_user.user_id}"
        )
        
        return ShareEventResponse(
            success=True,
            message=f"Event shared with {target_company.CompanyName}",
            event_company_id=event_company.EventCompanyID,
            event_id=event_id,
            company_id=target_company_id,
            role=request.role_code,
            already_exists=False
        )

    except ValueError as e:
        logger.warning(f"Invalid share request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sharing event by email: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share event"
        )


@router.get(
    "/{event_id}/my-role",
    response_model=dict,
    summary="Get current user's role for event",
    description="Get the current user's company role for an event (owner, organizer, or participant) with permissions."
)
async def get_my_role_for_event(
    event_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get current user's company role for an event.
    
    Returns role information including permissions (can edit, can delete, etc.).
    """
    try:
        # Get all companies for this event
        event_companies = await get_event_companies(
            db=db,
            event_id=event_id,
            active_only=True
        )
        
        # Find current user's company role
        user_relationship = next(
            (ec for ec in event_companies if ec.CompanyID == current_user.company_id),
            None
        )
        
        if not user_relationship:
            # Check if event is owned directly by company (legacy)
            event = (
                db.query(Event)
                .options(
                    joinedload(Event.event_type),
                    joinedload(Event.event_status),
                    joinedload(Event.public_review_status),
                    joinedload(Event.industry),
                    joinedload(Event.organizer_company),
                    joinedload(Event.company)
                )
                .filter(
                    Event.EventID == event_id,
                    Event.CompanyID == current_user.company_id,
                    Event.IsDeleted == False
                )
                .first()
            )
            
            if event:
                # Legacy event - user is owner (no EventCompany record)
                return {
                    "success": True,
                    "role_code": "event_owner",
                    "role_name": "Owner",
                    "has_edit_event": True,
                    "has_delete_event": True,
                    "has_manage_participants": True,
                    "has_view_event": True,
                    "is_legacy": True
                }
            else:
                # No relationship found
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have access to this event"
                )
        
        # Get role details
        role = user_relationship.role
        if not role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Role information not found"
            )
        
        return {
            "success": True,
            "role_code": role.RoleCode,
            "role_name": role.RoleName,
            "has_edit_event": role.HasEditEvent,
            "has_delete_event": role.HasDeleteEvent,
            "has_manage_participants": role.HasManageParticipants,
            "has_view_event": role.HasViewEvent,
            "is_legacy": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user role for event: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user role for event"
        )


@router.get(
    "/{event_id}/companies",
    response_model=dict,
    summary="Get all companies for event",
    description="Get all companies participating in an event with their roles (AC-2.4.11)."
)
async def get_event_companies_endpoint(
    event_id: int,
    active_only: bool = Query(True, description="Only return active relationships"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get all companies for an event.
    
    Returns list of companies with their roles (owner, organizer, participant).
    """
    try:
        # Verify event exists and user has access
        event = await get_event_by_id(db, event_id, current_user.company_id)
        if not event:
            # Check if event is public or user's company is a participant
            event = (
                db.query(Event)
                .options(
                    joinedload(Event.event_type),
                    joinedload(Event.event_status),
                    joinedload(Event.public_review_status),
                    joinedload(Event.industry),
                    joinedload(Event.organizer_company),
                    joinedload(Event.company)
                )
                .filter(
                    Event.EventID == event_id,
                    Event.IsDeleted == False
                )
                .first()
            )
            
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Event {event_id} not found"
                )
        
        event_companies = await get_event_companies(
            db=db,
            event_id=event_id,
            active_only=active_only
        )
        
        companies_data = []
        for ec in event_companies:
            companies_data.append({
                "event_company_id": ec.EventCompanyID,
                "company_id": ec.CompanyID,
                "company_name": ec.company.CompanyName if ec.company else None,
                "role_code": ec.role.RoleCode if ec.role else None,
                "role_name": ec.role.RoleName if ec.role else None,
                "is_active": ec.IsActive,
                "forms_created": ec.FormsCreated,
                "first_used_date": ec.FirstUsedDate.isoformat() if ec.FirstUsedDate else None,
                "last_used_date": ec.LastUsedDate.isoformat() if ec.LastUsedDate else None
            })
        
        logger.info(f"Retrieved {len(companies_data)} companies for EventID={event_id}")
        
        return {
            "success": True,
            "event_id": event_id,
            "companies": companies_data,
            "total": len(companies_data)
        }
        
    except Exception as e:
        logger.error(f"Error getting event companies: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get event companies"
        )


@router.delete(
    "/{event_id}/companies/{company_id}",
    response_model=dict,
    summary="Disassociate company from event",
    description="Disassociate a company from an event (soft delete participant relationship) (AC-2.4.11)."
)
async def disassociate_company_from_event_endpoint(
    event_id: int,
    company_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Disassociate a company from an event.
    
    Only participants can be disassociated. Owner and organizer relationships cannot be removed.
    """
    try:
        # Verify user has permission to disassociate
        # 1. Can disassociate own company (leave event)
        # 2. Can disassociate others if has manage_participants permission (revoke access)
        
        has_permission = False
        
        if company_id == current_user.company_id:
            has_permission = True
        else:
            # Check for manage_participants permission
            from modules.events.event_company_service import get_event_companies
            
            # Get all companies for this event to check user's role
            event_companies = await get_event_companies(
                db=db,
                event_id=event_id,
                active_only=True
            )
            
            # Find current user's company role
            user_relationship = next(
                (ec for ec in event_companies if ec.CompanyID == current_user.company_id),
                None
            )
            
            if user_relationship and user_relationship.role and user_relationship.role.HasManageParticipants:
                has_permission = True
            else:
                # Check if user is from the owner company (legacy or explicit)
                event = await get_event_by_id(db, event_id, current_user.company_id)
                if event and event.CompanyID == current_user.company_id:
                    has_permission = True
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to remove this company from the event"
            )
        
        # Disassociate company
        success = await disassociate_company_from_event(
            db=db,
            event_id=event_id,
            company_id=company_id,
            user_id=current_user.user_id
        )
        
        logger.info(
            f"Disassociated company from event: EventID={event_id}, "
            f"CompanyID={company_id}, UserID={current_user.user_id}"
        )
        
        return {
            "success": True,
            "message": "Company disassociated from event successfully",
            "event_id": event_id,
            "company_id": company_id
        }
        
    except ValueError as e:
        logger.error(f"Error disassociating company from event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disassociating company from event: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to disassociate company from event"
        )


# =====================================================================
# Smart Field Inference Endpoints
# =====================================================================

@router.get(
    "/timezones/country",
    response_model=dict,
    summary="Get country from timezone",
    description="Get country information inferred from timezone identifier (AC-2.4.2)."
)
async def get_country_from_timezone_endpoint(
    timezone_identifier: str = Query(..., description="IANA timezone identifier (e.g., 'Australia/Sydney')"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get country information from timezone identifier.
    
    Used for smart field inference - when user selects a timezone,
    automatically suggest the corresponding country.
    """
    try:
        country_info = await get_country_from_timezone(db, timezone_identifier)
        
        if not country_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country not found for timezone: {timezone_identifier}"
            )
        
        return {
            "success": True,
            "timezone_identifier": timezone_identifier,
            "country_id": country_info["country_id"],
            "country_code": country_info["country_code"],
            "country_name": country_info["country_name"],
            "timezone_display_name": country_info["timezone_display_name"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting country from timezone: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get country from timezone"
        )


@router.get(
    "/inference/user-profile",
    response_model=dict,
    summary="Get user profile with location",
    description="Get user profile with timezone and country for smart field inference (AC-2.4.2)."
)
async def get_user_profile_for_inference(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get user profile with timezone and country information.
    
    Used for smart field inference - pre-fill timezone and country
    based on user's profile settings.
    """
    try:
        profile = await get_user_profile_with_location(db, current_user.user_id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        return {
            "success": True,
            "user_id": profile["user_id"],
            "timezone_identifier": profile["timezone_identifier"],
            "country_id": profile["country_id"],
            "country_code": profile["country_code"],
            "country_name": profile["country_name"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile for inference: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.get(
    "/inference/company-profile/{company_id}",
    response_model=dict,
    summary="Get company profile with billing",
    description="Get company profile with billing city for smart field inference (AC-2.4.2)."
)
async def get_company_profile_for_inference(
    company_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get company profile with billing city information.
    
    Used for smart field inference - pre-fill city based on
    company's billing address.
    """
    try:
        # Verify user has access to this company
        from models.user_company import UserCompany
        from models.ref.user_company_status import UserCompanyStatus
        
        user_company = db.execute(
            select(UserCompany).join(UserCompanyStatus).where(
                UserCompany.UserID == current_user.user_id,
                UserCompany.CompanyID == company_id,
                UserCompany.IsDeleted == False,
                UserCompanyStatus.StatusCode == "active"
            )
        ).scalar_one_or_none()
        
        if not user_company:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this company"
            )
        
        profile = await get_company_profile_with_billing(db, company_id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found"
            )
        
        return {
            "success": True,
            "company_id": profile["company_id"],
            "company_name": profile["company_name"],
            "country_id": profile["country_id"],
            "billing_city": profile["billing_city"],
            "billing_state": profile["billing_state"],
            "billing_country_id": profile["billing_country_id"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting company profile for inference: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get company profile"
        )


@router.get(
    "/inference/recent-cities",
    response_model=dict,
    summary="Get recent event cities",
    description="Get user's recently used cities from their events for smart field inference (AC-2.4.2)."
)
async def get_recent_cities_endpoint(
    limit: int = Query(5, ge=1, le=10, description="Maximum number of cities to return"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get user's recently used cities from their events.
    
    Used for smart field inference - suggest cities the user
    has used in previous events.
    """
    try:
        cities = await get_recent_event_cities(db, current_user.user_id, limit)
        
        return {
            "success": True,
            "cities": cities,
            "count": len(cities)
        }
    except Exception as e:
        logger.error(f"Error getting recent cities: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get recent cities"
        )


