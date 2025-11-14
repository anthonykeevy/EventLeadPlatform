"""
Event Service Module
Business logic for event CRUD operations
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, and_
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

from models.event import Event
from models.ref.event_type import EventType
from models.ref.event_status import EventStatus
from models.ref.industry import Industry
from models.ref.country import Country
from models.ref.public_review_status import PublicReviewStatus
from models.company import Company
from models.user import User
from models.event_company import EventCompany
from models.ref.event_company_role import EventCompanyRole
from models.company_relationship import CompanyRelationship
from common.logger import get_logger
from common.multi_tenant import filter_by_company

logger = get_logger(__name__)


def _normalize_empty_string(value: Any) -> Optional[str]:
    """
    Normalize empty/placeholder values to None.
    
    Frontend often sends "-1", empty strings, or None for empty fields.
    This function converts all of these to None for proper database storage.
    
    Args:
        value: The value to normalize
        
    Returns:
        None if value is empty/placeholder, otherwise the original value as string
    """
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value == "" or value == "-1":
            return None
        return value
    # For non-string values, return as-is (they'll be handled by validation)
    return value


async def create_event(
    db: Session,
    user_id: int,
    company_id: int,
    event_data: Dict[str, Any]
) -> Event:
    """
    Create a new event for the company.
    
    Args:
        db: Database session
        user_id: User ID creating the event
        company_id: Company ID (for multi-tenant filtering)
        event_data: Event creation data from request
        
    Returns:
        Created Event object
        
    Raises:
        ValueError: If validation fails or duplicate event detected
    """
    # Check for duplicate events (same name + start date + company)
    # This prevents accidental duplicates, especially when linking to existing public events
    event_name = event_data.get('name', '').strip()
    start_datetime_input = event_data.get('start_datetime')
    
    if event_name and start_datetime_input:
        try:
            # Pydantic schema already converts string to datetime, so this should be a datetime object
            start_datetime_obj = None
            if isinstance(start_datetime_input, datetime):
                start_datetime_obj = start_datetime_input
            elif isinstance(start_datetime_input, str):
                # Fallback: parse string if somehow it's still a string
                try:
                    # Try ISO format first
                    start_datetime_obj = datetime.fromisoformat(start_datetime_input.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    # Try other common formats
                    try:
                        start_datetime_obj = datetime.strptime(start_datetime_input, '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        start_datetime_obj = None
            
            if start_datetime_obj:
                # Check for existing event with same name and start date (within same company)
                # Use a time window of ±1 day to catch variations in time entry
                from datetime import timedelta
                duplicate_query = db.query(Event).filter(
                    Event.CompanyID == company_id,
                    Event.Name.ilike(event_name),  # Case-insensitive match
                    Event.StartDateTime >= start_datetime_obj - timedelta(days=1),
                    Event.StartDateTime <= start_datetime_obj + timedelta(days=1),
                    ~Event.IsDeleted  # Use ~ instead of == False
                )
                
                # Exclude archived events from duplicate check
                archived_status = db.execute(
                    select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
                ).scalar_one_or_none()
                if archived_status:
                    duplicate_query = duplicate_query.filter(Event.EventStatusID != archived_status.EventStatusID)
                
                existing_duplicate = duplicate_query.first()
                
                if existing_duplicate:
                    logger.warning(
                        f"Duplicate event detected: EventID={existing_duplicate.EventID}, "
                        f"Name='{event_name}', CompanyID={company_id}, StartDateTime={start_datetime_obj}"
                    )
                    raise ValueError(
                        f"An event with the same name '{event_name}' and start date already exists. "
                        f"Please check if this is the same event or use a different name."
                    )
        except Exception as e:
            # If duplicate check fails, log but don't block event creation
            # This ensures duplicate check doesn't break valid event creation
            logger.warning(f"Duplicate check failed (non-blocking): {str(e)}")
            # Continue with event creation
    
    # Validate event type exists
    event_type = db.execute(
        select(EventType).where(EventType.EventTypeID == event_data['event_type_id'])
    ).scalar_one_or_none()
    
    if not event_type:
        raise ValueError(f"Invalid event type ID: {event_data['event_type_id']}")
    
    # =====================================================================
    # GUARD 1: Event Creation Guard - Set review status based on IsPublic and IsSharedWithPlatform
    # =====================================================================
    is_public = event_data.get('is_public', False)
    is_shared_with_platform = event_data.get('is_shared_with_platform', False)
    
    # Get DRAFT status for private events
    draft_status = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == 'DRAFT')
    ).scalar_one_or_none()
    
    if not draft_status:
        raise ValueError("DRAFT event status not found in database")
        
    # Determine event status and review status based on workflow rules
    if is_public:
        # Public events: Use user's event_status_id if provided, otherwise default to DRAFT
        # (User controls EventStatus - we don't force PENDING_REVIEW anymore)
        event_status_id = event_data.get('event_status_id', draft_status.EventStatusID)
        
        if is_shared_with_platform:
            # Public + Platform Sharing → Requires admin review
            # Validate required fields for platform-sharing events
            if not event_data.get('description'):
                raise ValueError("Description is required for platform-sharing events")
            if not event_data.get('start_datetime'):
                raise ValueError("Start date/time is required for platform-sharing events")
            if not event_data.get('event_type_id'):
                raise ValueError("Event type is required for platform-sharing events")
            
            # Get PENDING review status
            pending_review_status = db.execute(
                select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'PENDING')
            ).scalar_one_or_none()
            
            if not pending_review_status:
                raise ValueError("PENDING public review status not found in database")
            
            public_review_status_id = pending_review_status.PublicReviewStatusID
            is_public_review_required = True
        else:
            # Public + Company Network Only → No review needed
            public_review_status_id = None
            is_public_review_required = False
    else:
        # Private events → No review, no platform sharing
        event_status_id = event_data.get('event_status_id', draft_status.EventStatusID)
        public_review_status_id = None
        is_shared_with_platform = False  # Force False for private events
        is_public_review_required = False
    
    # Validate event status exists
    event_status = db.execute(
        select(EventStatus).where(EventStatus.EventStatusID == event_status_id)
    ).scalar_one_or_none()
    
    if not event_status:
        raise ValueError(f"Invalid event status ID: {event_status_id}")
    
    # Validate industry if provided
    if event_data.get('industry_id'):
        industry = db.execute(
            select(Industry).where(Industry.IndustryID == event_data['industry_id'])
        ).scalar_one_or_none()
        
        if not industry:
            raise ValueError(f"Invalid industry ID: {event_data['industry_id']}")
    
    # Validate country if provided
    if event_data.get('country_id'):
        country = db.execute(
            select(Country).where(Country.CountryID == event_data['country_id'])
        ).scalar_one_or_none()
        
        if not country:
            raise ValueError(f"Invalid country ID: {event_data['country_id']}")
    
    # Ensure datetime objects are timezone-naive (SQL Server DateTime expects naive UTC)
    from datetime import timezone as tz
    start_datetime = event_data['start_datetime']
    if isinstance(start_datetime, datetime) and start_datetime.tzinfo is not None:
        # Convert to UTC first, then remove timezone info to get naive UTC
        start_datetime = start_datetime.astimezone(tz.utc).replace(tzinfo=None)
    
    end_datetime = event_data.get('end_datetime')
    if end_datetime and isinstance(end_datetime, datetime) and end_datetime.tzinfo is not None:
        # Convert to UTC first, then remove timezone info to get naive UTC
        end_datetime = end_datetime.astimezone(tz.utc).replace(tzinfo=None)
    
    # Create event object
    event = Event(
        Name=event_data['name'],
        Description=event_data.get('description'),
        ShortDescription=event_data.get('short_description'),
        CompanyID=company_id,
        CreatedBy=user_id,
        StartDateTime=start_datetime,
        EndDateTime=end_datetime,
        TimezoneIdentifier=event_data.get('timezone_identifier'),
        VenueName=event_data.get('venue_name'),
        VenueAddress=event_data.get('venue_address'),
        City=event_data.get('city'),
        State=event_data.get('state'),
        CountryID=event_data.get('country_id'),
        Latitude=event_data.get('latitude'),
        Longitude=event_data.get('longitude'),
        EventTypeID=event_data['event_type_id'],
        IndustryID=event_data.get('industry_id'),
        Tags=event_data.get('tags'),
        IsPublic=is_public,
        IsSharedWithPlatform=is_shared_with_platform,
        IsPublicReviewRequired=is_public_review_required,
        PublicReviewStatusID=public_review_status_id,  # FK to ref.PublicReviewStatus
        EventStatusID=event_status_id,  # User-controlled (defaults to DRAFT)
        IsRecurring=event_data.get('is_recurring', False),
        OrganizerCompanyID=event_data.get('organizer_company_id'),
        OrganizerContactEmail=_normalize_empty_string(event_data.get('organizer_contact_email')),
        OrganizerWebsite=_normalize_empty_string(event_data.get('organizer_website')),
        ExpectedAttendees=event_data.get('expected_attendees'),
        FormsCreated=0,
        TotalSubmissions=0,
        CreatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    
    db.add(event)
    db.flush()
    
    # Create EventCompany relationship with event_owner role
    owner_role = db.execute(
        select(EventCompanyRole).where(EventCompanyRole.RoleCode == 'event_owner')
    ).scalar_one_or_none()
    
    if owner_role:
        event_company_owner = EventCompany(
            EventID=event.EventID,
            CompanyID=company_id,
            EventCompanyRoleID=owner_role.EventCompanyRoleID,
            IsActive=True,
            CreatedBy=user_id
        )
        db.add(event_company_owner)
        logger.info(
            f"Created EventCompany owner relationship: EventID={event.EventID}, "
            f"CompanyID={company_id}, RoleCode=event_owner"
        )
    
    # If OrganizerCompanyID is different from owner, create event_organizer relationship
    organizer_company_id = event_data.get('organizer_company_id')
    if organizer_company_id and organizer_company_id != company_id:
        organizer_role = db.execute(
            select(EventCompanyRole).where(EventCompanyRole.RoleCode == 'event_organizer')
        ).scalar_one_or_none()
        
        if organizer_role:
            event_company_organizer = EventCompany(
                EventID=event.EventID,
                CompanyID=organizer_company_id,
                EventCompanyRoleID=organizer_role.EventCompanyRoleID,
                IsActive=True,
                CreatedBy=user_id
            )
            db.add(event_company_organizer)
            logger.info(
                f"Created EventCompany organizer relationship: EventID={event.EventID}, "
                f"CompanyID={organizer_company_id}, RoleCode=event_organizer"
            )
    
    db.commit()
    db.refresh(event)
    
    logger.info(f"Event created: EventID={event.EventID}, Name='{event.Name}', CompanyID={company_id}")
    
    return event


async def get_events(
    db: Session,
    company_id: int,
    filters: Optional[Dict[str, Any]] = None
) -> List[Event]:
    """
    Get all events for a company with optional filters.
    
    Args:
        db: Database session
        company_id: Company ID (for multi-tenant filtering)
        filters: Optional filters (event_type_id, status_id, date_from, date_to, industry_id, search)
        
    Returns:
        List of Event objects
    """
    # Get Archived status ID to exclude archived events
    archived_status = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
    ).scalar_one_or_none()
    
    # Build query with eager loading of relationships
    query = db.query(Event).options(
        joinedload(Event.event_type),
        joinedload(Event.event_status),
        joinedload(Event.public_review_status),
        joinedload(Event.industry),
        joinedload(Event.organizer_company),
        joinedload(Event.company)
    ).filter(
        Event.CompanyID == company_id,
        Event.IsDeleted == False
    )
    
    # Exclude archived events from customer-facing lists
    if archived_status:
        query = query.filter(Event.EventStatusID != archived_status.EventStatusID)
    
    # Apply filters
    if filters:
        if filters.get('event_type_id'):
            query = query.filter(Event.EventTypeID == filters['event_type_id'])
        
        if filters.get('status_id'):
            query = query.filter(Event.EventStatusID == filters['status_id'])
        
        if filters.get('industry_id'):
            query = query.filter(Event.IndustryID == filters['industry_id'])
        
        if filters.get('date_from'):
            query = query.filter(Event.StartDateTime >= filters['date_from'])
        
        if filters.get('date_to'):
            query = query.filter(Event.StartDateTime <= filters['date_to'])
        
        if filters.get('search'):
            search_term = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    Event.Name.like(search_term),
                    Event.Description.like(search_term),
                    Event.ShortDescription.like(search_term)
                )
            )
    
    # Order by start date descending (most recent first)
    events = query.order_by(Event.StartDateTime.desc()).all()
    
    logger.info(f"Retrieved {len(events)} events for CompanyID={company_id}")
    
    return events


async def get_event_by_id(
    db: Session,
    event_id: int,
    company_id: int
) -> Optional[Event]:
    """
    Get a single event by ID, verifying it belongs to the company.
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID (for multi-tenant filtering)
        
    Returns:
        Event object if found and belongs to company, None otherwise
    """
    event = db.execute(
        select(Event)
        .options(
            joinedload(Event.event_type),
            joinedload(Event.event_status),
            joinedload(Event.public_review_status),
            joinedload(Event.industry),
            joinedload(Event.organizer_company),
            joinedload(Event.company)
        )
        .where(
            Event.EventID == event_id,
            Event.CompanyID == company_id,
            Event.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if event:
        logger.info(f"Retrieved event: EventID={event_id}, CompanyID={company_id}")
    else:
        logger.warning(f"Event not found: EventID={event_id}, CompanyID={company_id}")
    
    return event


async def update_event(
    db: Session,
    event_id: int,
    company_id: int,
    user_id: int,
    event_data: Dict[str, Any],
    skip_company_check: bool = False
) -> Event:
    """
    Update an event, verifying it belongs to the company.
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID (for multi-tenant filtering, ignored if skip_company_check=True)
        user_id: User ID making the update
        event_data: Event update data from request
        skip_company_check: If True, skip company ownership verification (admin only)
        
    Returns:
        Updated Event object
        
    Raises:
        ValueError: If event not found, doesn't belong to company, or validation fails
    """
    # Get event and verify company ownership (or skip check for admin)
    if skip_company_check:
        # Admin update: query event directly without company filter
        event = db.execute(
            select(Event)
            .options(
                joinedload(Event.event_type),
                joinedload(Event.event_status),
                joinedload(Event.public_review_status),
                joinedload(Event.industry),
                joinedload(Event.organizer_company),
                joinedload(Event.company)
            )
            .where(
                Event.EventID == event_id,
                Event.IsDeleted == False
            )
        ).scalar_one_or_none()
        
        if not event:
            raise ValueError(f"Event not found: {event_id}")
        
        # Use event's actual company_id for the rest of the logic
        company_id = event.CompanyID
    else:
        # Regular update: verify company ownership
        event = await get_event_by_id(db, event_id, company_id)
        
        if not event:
            raise ValueError(f"Event not found or does not belong to your company: {event_id}")
    
    # Validate event type if provided
    if event_data.get('event_type_id'):
        event_type = db.execute(
            select(EventType).where(EventType.EventTypeID == event_data['event_type_id'])
        ).scalar_one_or_none()
        
        if not event_type:
            raise ValueError(f"Invalid event type ID: {event_data['event_type_id']}")
    
    # Validate event status if provided
    if event_data.get('event_status_id'):
        event_status = db.execute(
            select(EventStatus).where(EventStatus.EventStatusID == event_data['event_status_id'])
        ).scalar_one_or_none()
        
        if not event_status:
            raise ValueError(f"Invalid event status ID: {event_data['event_status_id']}")
    
    # Validate industry if provided
    if event_data.get('industry_id'):
        industry = db.execute(
            select(Industry).where(Industry.IndustryID == event_data['industry_id'])
        ).scalar_one_or_none()
        
        if not industry:
            raise ValueError(f"Invalid industry ID: {event_data['industry_id']}")
    
    # Validate country if provided
    if event_data.get('country_id'):
        country = db.execute(
            select(Country).where(Country.CountryID == event_data['country_id'])
        ).scalar_one_or_none()
        
        if not country:
            raise ValueError(f"Invalid country ID: {event_data['country_id']}")
    
    # Update event fields
    if 'name' in event_data:
        event.Name = event_data['name']
    if 'description' in event_data:
        event.Description = event_data['description']
    if 'short_description' in event_data:
        event.ShortDescription = event_data['short_description']
    if 'start_datetime' in event_data:
        event.StartDateTime = event_data['start_datetime']
    if 'end_datetime' in event_data:
        event.EndDateTime = event_data['end_datetime']
    if 'timezone_identifier' in event_data:
        event.TimezoneIdentifier = event_data['timezone_identifier']
    if 'venue_name' in event_data:
        event.VenueName = event_data['venue_name']
    if 'venue_address' in event_data:
        event.VenueAddress = event_data['venue_address']
    if 'city' in event_data:
        event.City = event_data['city']
    if 'state' in event_data:
        event.State = event_data['state']
    if 'country_id' in event_data:
        event.CountryID = event_data['country_id']
    if 'latitude' in event_data:
        event.Latitude = event_data['latitude']
    if 'longitude' in event_data:
        event.Longitude = event_data['longitude']
    if 'event_type_id' in event_data:
        event.EventTypeID = event_data['event_type_id']
    if 'industry_id' in event_data:
        event.IndustryID = event_data['industry_id']
    if 'tags' in event_data:
        event.Tags = event_data['tags']
    # =====================================================================
    # GUARD 2: IsPublic Update Guard - Handle IsPublic changes
    # =====================================================================
    if 'is_public' in event_data:
        was_public = event.IsPublic
        new_is_public = event_data['is_public']
        
        if was_public != new_is_public:
            if not was_public and new_is_public:
                # Changing from Private → Public
                # Get current IsSharedWithPlatform value (or use new value if provided)
                new_is_shared_with_platform = event_data.get('is_shared_with_platform', event.IsSharedWithPlatform)
                
                if new_is_shared_with_platform:
                    # Public + Platform Sharing → Requires admin review
                    # Validate required fields for platform-sharing events
                    if not event.Description and not event_data.get('description'):
                        raise ValueError("Description is required for platform-sharing events")
                    if not event.StartDateTime and not event_data.get('start_datetime'):
                        raise ValueError("Start date/time is required for platform-sharing events")
                    if not event.EventTypeID and not event_data.get('event_type_id'):
                        raise ValueError("Event type is required for platform-sharing events")
                    
                    # Get PENDING review status
                    pending_review_status = db.execute(
                        select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'PENDING')
                    ).scalar_one_or_none()
                    
                    if not pending_review_status:
                        raise ValueError("PENDING public review status not found in database")
                    
                    event.PublicReviewStatusID = pending_review_status.PublicReviewStatusID
                    event.IsPublicReviewRequired = True
                    event.IsSharedWithPlatform = True
                else:
                    # Public + Company Network Only → No review needed
                    event.PublicReviewStatusID = None
                    event.IsPublicReviewRequired = False
                    event.IsSharedWithPlatform = False
                
                event.IsPublic = True
            elif was_public and not new_is_public:
                # Changing from Public → Private
                # Clear review status and platform sharing
                event.IsPublic = False
                event.IsSharedWithPlatform = False
                event.PublicReviewStatusID = None
                event.IsPublicReviewRequired = False
                # Note: Keep review history (PublicReviewDate, PublicReviewBy, PublicReviewComments) for audit trail
        else:
            # IsPublic unchanged, just update the value
            event.IsPublic = new_is_public
    
    # =====================================================================
    # GUARD 4A: IsSharedWithPlatform Update Guard - Handle platform sharing changes
    # =====================================================================
    if 'is_shared_with_platform' in event_data:
        was_shared_with_platform = event.IsSharedWithPlatform
        new_is_shared_with_platform = event_data['is_shared_with_platform']
        
        if was_shared_with_platform != new_is_shared_with_platform:
            if not was_shared_with_platform and new_is_shared_with_platform:
                # Enabling platform sharing
                # Ensure event is public
                if not event.IsPublic:
                    event.IsPublic = True
                
                # Validate required fields for platform-sharing events
                if not event.Description and not event_data.get('description'):
                    raise ValueError("Description is required for platform-sharing events")
                if not event.StartDateTime and not event_data.get('start_datetime'):
                    raise ValueError("Start date/time is required for platform-sharing events")
                if not event.EventTypeID and not event_data.get('event_type_id'):
                    raise ValueError("Event type is required for platform-sharing events")
                
                # Get PENDING review status
                pending_review_status = db.execute(
                    select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'PENDING')
                ).scalar_one_or_none()
                
                if not pending_review_status:
                    raise ValueError("PENDING public review status not found in database")
                
                event.PublicReviewStatusID = pending_review_status.PublicReviewStatusID
                event.IsPublicReviewRequired = True
                event.IsSharedWithPlatform = True
            elif was_shared_with_platform and not new_is_shared_with_platform:
                # Disabling platform sharing
                # Get PENDING status to check if we should clear it
                pending_review_status = db.execute(
                    select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'PENDING')
                ).scalar_one_or_none()
                
                if pending_review_status and event.PublicReviewStatusID == pending_review_status.PublicReviewStatusID:
                    # Clear review status if PENDING
                    event.PublicReviewStatusID = None
                
                event.IsSharedWithPlatform = False
                event.IsPublicReviewRequired = False
                # Note: Keep review history if APPROVED/REJECTED (for audit trail)
        else:
            # IsSharedWithPlatform unchanged, just update the value
            event.IsSharedWithPlatform = new_is_shared_with_platform
    # =====================================================================
    # GUARD 4B: EventStatus Update Guard - Handle event lifecycle changes
    # =====================================================================
    if 'event_status_id' in event_data:
        old_event_status_id = event.EventStatusID
        new_event_status_id = event_data['event_status_id']
        
        if old_event_status_id != new_event_status_id:
            # Get the EventStatus objects
            old_event_status = db.execute(
                select(EventStatus).where(EventStatus.EventStatusID == old_event_status_id)
            ).scalar_one_or_none()
            
            new_event_status = db.execute(
                select(EventStatus).where(EventStatus.EventStatusID == new_event_status_id)
            ).scalar_one_or_none()
            
            if new_event_status:
                if new_event_status.StatusCode == 'ARCHIVED':
                    # If archiving event, clear review status if PENDING
                    pending_review_status = db.execute(
                        select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'PENDING')
                    ).scalar_one_or_none()
                    
                    if pending_review_status and event.PublicReviewStatusID == pending_review_status.PublicReviewStatusID:
                        # Clear review status if PENDING
                        event.PublicReviewStatusID = None
                    
                    # Disable platform sharing
                    event.IsSharedWithPlatform = False
                    event.IsPublicReviewRequired = False
                    # Note: Keep review history if APPROVED/REJECTED (for audit trail)
                
                elif new_event_status.StatusCode == 'CANCELLED':
                    # If cancelling event, notify stakeholders if it was approved for platform sharing
                    approved_review_status = db.execute(
                        select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'APPROVED')
                    ).scalar_one_or_none()
                    
                    if approved_review_status and event.PublicReviewStatusID == approved_review_status.PublicReviewStatusID:
                        if event.IsSharedWithPlatform:
                            # Event was approved but cancelled - notify stakeholders
                            # TODO: Implement notification logic (email to event creator, etc.)
                            logger.info(
                                f"Event {event.EventID} was approved for platform sharing but has been cancelled. "
                                f"Stakeholders should be notified."
                            )
                    # Note: Keep review history for audit trail
        
        event.EventStatusID = new_event_status_id
    # Update other fields
    if 'is_recurring' in event_data:
        event.IsRecurring = event_data['is_recurring']
    if 'organizer_company_id' in event_data:
        event.OrganizerCompanyID = event_data['organizer_company_id']
    if 'organizer_contact_email' in event_data:
        # Router should have already removed "-1" placeholder values
        # At this point, if the field is in event_data, it means it should be updated
        email_value = event_data['organizer_contact_email']
        if isinstance(email_value, str) and email_value.strip() != "":
            event.OrganizerContactEmail = email_value.strip()
        else:
            # Empty string or None means clear the field
            event.OrganizerContactEmail = None
    
    if 'organizer_website' in event_data:
        # Router should have already removed "-1" placeholder values
        # At this point, if the field is in event_data, it means it should be updated
        website_value = event_data['organizer_website']
        if isinstance(website_value, str) and website_value.strip() != "":
            event.OrganizerWebsite = website_value.strip()
        else:
            # Empty string or None means clear the field
            event.OrganizerWebsite = None
    if 'expected_attendees' in event_data:
        event.ExpectedAttendees = event_data['expected_attendees']
    
    event.UpdatedDate = datetime.utcnow()
    event.UpdatedBy = user_id
    
    db.flush()
    
    logger.info(f"Event updated: EventID={event_id}, CompanyID={company_id}")
    
    return event


async def delete_event(
    db: Session,
    event_id: int,
    company_id: int,
    user_id: int
) -> None:
    """
    Archive an event (set status to Archived) instead of soft delete.
    Verifies event belongs to the company.
    
    Args:
        db: Database session
        event_id: Event ID
        company_id: Company ID (for multi-tenant filtering)
        user_id: User ID making the deletion
        
    Raises:
        ValueError: If event not found or doesn't belong to company
    """
    # Get event and verify company ownership
    event = await get_event_by_id(db, event_id, company_id)
    
    if not event:
        raise ValueError(f"Event not found or does not belong to your company: {event_id}")
    
    # Verify event was created by this company
    if event.CompanyID != company_id:
        raise ValueError(f"Event does not belong to your company: {event_id}")
    
    # Get Archived status (EventStatusID = 7)
    archived_status = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
    ).scalar_one_or_none()
    
    if not archived_status:
        raise ValueError("Archived status not found in database")
    
    # Archive the event instead of soft delete
    event.EventStatusID = archived_status.EventStatusID
    event.UpdatedDate = datetime.utcnow()
    event.UpdatedBy = user_id

    # When an event is archived it should no longer appear in platform sharing queues.
    # Always mark sharing disabled and review not required.
    event.IsSharedWithPlatform = False
    event.IsPublicReviewRequired = False

    # If the event was still pending review, clear the review linkage entirely.
    pending_review_status = db.execute(
        select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'PENDING')
    ).scalar_one_or_none()

    if pending_review_status and event.PublicReviewStatusID == pending_review_status.PublicReviewStatusID:
        event.PublicReviewStatusID = None
        event.PublicReviewDate = None
        event.PublicReviewBy = None
        event.PublicReviewComments = None

    db.flush()
    
    logger.info(f"Event archived: EventID={event_id}, CompanyID={company_id}, StatusID={archived_status.EventStatusID}")


async def get_platform_wide_visible_events(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    filters: Optional[Dict[str, Any]] = None
) -> tuple[List[Event], int]:
    """
    Get events visible in platform-wide search.
    
    Query filters:
    - IsPublic = True
    - IsSharedWithPlatform = True
    - PublicReviewStatusID = APPROVED
    - EventStatusID = PUBLISHED
    - IsDeleted = False
    
    Args:
        db: Database session
        page: Page number (1-based)
        page_size: Number of items per page
        filters: Optional filters (event_type_id, industry_id, date_from, date_to, search_term)
        
    Returns:
        Tuple of (list of Event objects, total count)
    """
    # Get APPROVED status
    approved_status = db.execute(
        select(PublicReviewStatus).where(PublicReviewStatus.StatusCode == 'APPROVED')
    ).scalar_one_or_none()
    
    if not approved_status:
        return [], 0
    
    # Get PUBLISHED status
    published_status = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == 'PUBLISHED')
    ).scalar_one_or_none()
    
    if not published_status:
        return [], 0
    
    # Build query
    query = (
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
            Event.IsPublic == True,
            Event.IsSharedWithPlatform == True,
            Event.PublicReviewStatusID == approved_status.PublicReviewStatusID,
            Event.EventStatusID == published_status.EventStatusID,
            Event.IsDeleted == False
        )
    )

    current_time = datetime.utcnow()
    query = query.filter(
        or_(
            Event.EndDateTime == None,
            Event.EndDateTime >= current_time
        )
    )
    
    # Apply filters
    if filters:
        if filters.get('event_type_id'):
            query = query.filter(Event.EventTypeID == filters['event_type_id'])
        if filters.get('industry_id'):
            query = query.filter(Event.IndustryID == filters['industry_id'])
        if filters.get('date_from'):
            query = query.filter(Event.StartDateTime >= filters['date_from'])
        if filters.get('date_to'):
            query = query.filter(Event.StartDateTime <= filters['date_to'])
        if filters.get('search_term'):
            search_term = f"%{filters['search_term']}%"
            query = query.filter(
                or_(
                    Event.Name.ilike(search_term),
                    Event.Description.ilike(search_term),
                    Event.ShortDescription.ilike(search_term)
                )
            )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    events = query.order_by(Event.StartDateTime.asc()).offset(offset).limit(page_size).all()
    
    return events, total


async def get_company_network_visible_events(
    db: Session,
    company_id: int,
    page: int = 1,
    page_size: int = 20,
    filters: Optional[Dict[str, Any]] = None
) -> tuple[List[Event], int]:
    """
    Get events visible to company network (company and linked organizations).
    
    Query filters:
    - IsPublic = True
    - IsDeleted = False
    - Additional filters for company network (Event.CompanyID == company_id OR linked via EventCompany)
    
    Args:
        db: Database session
        company_id: Company ID
        page: Page number (1-based)
        page_size: Number of items per page
        filters: Optional filters (event_type_id, industry_id, date_from, date_to, search_term)
        
    Returns:
        Tuple of (list of Event objects, total count)
    """
    # Build query - events visible to company network
    # Include events where:
    # 1. Event.CompanyID == company_id (company's own events)
    # 2. Event is linked via EventCompany (participant/organizer relationships)
    # Determine full company network (company + linked organizations via CompanyRelationship)
    network_company_ids = {company_id}
    processed_company_ids = set()
    pending_company_ids = {company_id}

    while pending_company_ids:
        current_company_id = pending_company_ids.pop()
        if current_company_id in processed_company_ids:
            continue

        processed_company_ids.add(current_company_id)

        relationships = db.execute(
            select(
                CompanyRelationship.ParentCompanyID,
                CompanyRelationship.ChildCompanyID
            ).where(
                or_(
                    CompanyRelationship.ParentCompanyID == current_company_id,
                    CompanyRelationship.ChildCompanyID == current_company_id
                ),
                CompanyRelationship.Status == 'active',
                CompanyRelationship.IsDeleted == False
            )
        ).all()

        for parent_id, child_id in relationships:
            for related_company_id in (parent_id, child_id):
                if related_company_id not in network_company_ids:
                    network_company_ids.add(related_company_id)
                    pending_company_ids.add(related_company_id)

    network_company_ids_list = list(network_company_ids)

    archived_status = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
    ).scalar_one_or_none()

    event_company_subquery = (
        select(EventCompany.EventID)
        .where(
            EventCompany.CompanyID.in_(network_company_ids_list),
            EventCompany.IsDeleted == False,
            EventCompany.IsActive == True
        )
    )

    query = (
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
            Event.IsPublic == True,
            Event.IsDeleted == False,
            or_(
                Event.CompanyID.in_(network_company_ids_list),
                Event.EventID.in_(event_company_subquery)
            )
        )
    )

    if archived_status:
        query = query.filter(Event.EventStatusID != archived_status.EventStatusID)

    current_time = datetime.utcnow()
    query = query.filter(
        or_(
            Event.EndDateTime == None,
            Event.EndDateTime >= current_time
        )
    )
    
    # Apply filters
    if filters:
        if filters.get('event_type_id'):
            query = query.filter(Event.EventTypeID == filters['event_type_id'])
        if filters.get('industry_id'):
            query = query.filter(Event.IndustryID == filters['industry_id'])
        if filters.get('date_from'):
            query = query.filter(Event.StartDateTime >= filters['date_from'])
        if filters.get('date_to'):
            query = query.filter(Event.StartDateTime <= filters['date_to'])
        if filters.get('search_term'):
            search_term = f"%{filters['search_term']}%"
            query = query.filter(
                or_(
                    Event.Name.ilike(search_term),
                    Event.Description.ilike(search_term),
                    Event.ShortDescription.ilike(search_term)
                )
            )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    events = query.order_by(Event.StartDateTime.asc()).offset(offset).limit(page_size).all()
    
    return events, total


async def search_company_network_events(
    db: Session,
    company_id: int,
    search_term: Optional[str] = None,
    limit: int = 20
) -> tuple[List[Event], int]:
    """
    Search events visible to the company network (company-owned, linked companies, or platform-approved).
    Combines company network results with platform-wide approved events and removes duplicates.
    """
    filters: Dict[str, Any] = {}
    if search_term:
        filters['search_term'] = search_term

    network_events, _ = await get_company_network_visible_events(
        db=db,
        company_id=company_id,
        page=1,
        page_size=limit,
        filters=filters
    )

    platform_events, _ = await get_platform_wide_visible_events(
        db=db,
        page=1,
        page_size=limit,
        filters=filters
    )

    combined_events: List[Event] = []
    seen_ids: set[int] = set()

    for event in network_events + platform_events:
        if event.EventID not in seen_ids:
            combined_events.append(event)
            seen_ids.add(event.EventID)

    total = len(combined_events)
    return combined_events[:limit], total


async def search_public_events(
    db: Session,
    search_term: Optional[str] = None,
    limit: int = 20
) -> List[Event]:
    """
    Search public events across all companies (for event registration).
    
    This method searches platform-wide visible events (approved and published).
    
    Args:
        db: Database session
        search_term: Optional search term (searches name, description, short_description)
        limit: Maximum number of results
        
    Returns:
        List of public Event objects that are approved for public visibility
    """
    # Use platform-wide visibility query
    filters = {}
    if search_term:
        filters['search_term'] = search_term
    
    events, _ = await get_platform_wide_visible_events(
        db=db,
        page=1,
        page_size=limit,
        filters=filters
    )
    
    return events


async def search_events(
    db: Session,
    company_id: int,
    search_term: str
) -> List[Event]:
    """
    Search events by name, description, or short description.
    
    Args:
        db: Database session
        company_id: Company ID (for multi-tenant filtering)
        search_term: Search term
        
    Returns:
        List of matching Event objects
    """
    search_pattern = f"%{search_term}%"
    
    events = db.execute(
        select(Event).where(
            Event.CompanyID == company_id,
            Event.IsDeleted == False,
            or_(
                Event.Name.like(search_pattern),
                Event.Description.like(search_pattern),
                Event.ShortDescription.like(search_pattern)
            )
        )
    ).scalars().all()
    
    logger.info(f"Search results: {len(events)} events found for CompanyID={company_id}, term='{search_term}'")
    
    return events


async def get_event_types(db: Session) -> List[EventType]:
    """
    Get all active event types.
    
    Args:
        db: Database session
        
    Returns:
        List of EventType objects
    """
    event_types = db.execute(
        select(EventType).where(
            EventType.IsDeleted == False,
            EventType.IsActive == True
        ).order_by(EventType.SortOrder)
    ).scalars().all()
    
    return event_types


async def get_event_statuses(db: Session) -> List[EventStatus]:
    """
    Get all active event statuses.
    Only returns statuses where IsActive=True (Rejected and Archived are now IsActive=False).
    
    Args:
        db: Database session
        
    Returns:
        List of EventStatus objects with IsActive=True
    """
    event_statuses = db.execute(
        select(EventStatus).where(
            EventStatus.IsDeleted == False,
            EventStatus.IsActive == True
        ).order_by(EventStatus.SortOrder)
    ).scalars().all()
    
    return event_statuses


