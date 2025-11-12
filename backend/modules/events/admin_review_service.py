"""
Admin Review Service Module
Business logic for admin event review operations
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from common.logger import get_logger
from models.event import Event
from models.ref.event_status import EventStatus
from models.ref.public_review_status import PublicReviewStatus
from models.user import User

logger = get_logger(__name__)


class AdminReviewService:
    """
    Service layer that encapsulates the public review workflow operations
    used by Story 2.6 / Story 2.7 admin endpoints.
    """
    
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------ #
    # Helper lookups
    # ------------------------------------------------------------------ #
    def _get_public_review_status(self, status_code: str) -> Optional[PublicReviewStatus]:
        return self.db.execute(
            select(PublicReviewStatus).where(
                PublicReviewStatus.StatusCode == status_code,
                PublicReviewStatus.IsDeleted == False,  # noqa: E712
            )
        ).scalar_one_or_none()

    def _get_event_status(self, status_code: str) -> Optional[EventStatus]:
        return self.db.execute(
            select(EventStatus).where(
                EventStatus.StatusCode == status_code,
                EventStatus.IsDeleted == False,  # noqa: E712
            )
        ).scalar_one_or_none()

    def _validate_admin_user(self, admin_user_id: int) -> User:
        admin_user = self.db.execute(
            select(User).where(
                User.UserID == admin_user_id,
                User.IsDeleted == False,  # noqa: E712
            )
        ).scalar_one_or_none()

        if not admin_user:
            raise ValueError(f"Admin user not found: {admin_user_id}")
        return admin_user

    def _get_event(self, event_id: int) -> Event:
        event = (
            self.db.query(Event)
            .options(
                joinedload(Event.company),
                joinedload(Event.created_by_user),
                joinedload(Event.event_type),
                joinedload(Event.event_status),
                joinedload(Event.industry),
                joinedload(Event.country),
                joinedload(Event.public_review_status),
                joinedload(Event.public_review_by_user),
            )
            .filter(
                Event.EventID == event_id,
                Event.IsDeleted == False,  # noqa: E712
            )
            .first()
        )
        
        if not event:
            raise ValueError(f"Event not found: {event_id}")
        return event

    # ------------------------------------------------------------------ #
    # Mutating operations
    # ------------------------------------------------------------------ #
    def approve_event(
        self,
        event_id: int,
        admin_user_id: int,
        comment: Optional[str] = None,
        public_visibility_date: Optional[datetime] = None,
    ) -> Event:
        """
        Approve an event for platform-wide visibility.
        """
        self._validate_admin_user(admin_user_id)
        event = self._get_event(event_id)

        if not event.IsSharedWithPlatform:
            raise ValueError("Can only approve events that are shared with the platform")

        pending_status = self._get_public_review_status("PENDING")
        approved_status = self._get_public_review_status("APPROVED")
        
        if not pending_status or not approved_status:
            raise ValueError("Public review statuses not found in database")
        
        if event.PublicReviewStatusID != pending_status.PublicReviewStatusID:
            raise ValueError("Can only approve events that are currently Pending")
        
        event.PublicReviewStatusID = approved_status.PublicReviewStatusID
        event.PublicReviewDate = datetime.utcnow()
        event.PublicReviewBy = admin_user_id
        event.PublicReviewComments = comment
        event.PublicVisibilityDate = public_visibility_date or datetime.utcnow()
        event.UpdatedDate = datetime.utcnow()
        event.UpdatedBy = admin_user_id

        self.db.flush()
        self.db.commit()
        self.db.refresh(event)

        logger.info(
            "Event approved",
            extra={
                "event_id": event.EventID,
                "admin_user_id": admin_user_id,
                "public_review_status_id": approved_status.PublicReviewStatusID,
            },
                        )
        return event
    
    def reject_event(
        self,
        event_id: int,
        admin_user_id: int,
        comment: str,
    ) -> Event:
        """
        Reject an event for platform-wide visibility.
        """
        self._validate_admin_user(admin_user_id)

        if not comment or not comment.strip():
            raise ValueError("Comment is required when rejecting an event")
        
        event = self._get_event(event_id)

        if not event.IsSharedWithPlatform:
            raise ValueError("Can only reject events that are shared with the platform")

        pending_status = self._get_public_review_status("PENDING")
        rejected_status = self._get_public_review_status("REJECTED")
        
        if not pending_status or not rejected_status:
            raise ValueError("Public review statuses not found in database")
        
        if event.PublicReviewStatusID != pending_status.PublicReviewStatusID:
            raise ValueError("Can only reject events that are currently Pending")
        
        event.PublicReviewStatusID = rejected_status.PublicReviewStatusID
        event.PublicReviewDate = datetime.utcnow()
        event.PublicReviewBy = admin_user_id
        event.PublicReviewComments = comment
        event.IsSharedWithPlatform = False
        event.UpdatedDate = datetime.utcnow()
        event.UpdatedBy = admin_user_id

        self.db.flush()
        self.db.commit()
        self.db.refresh(event)

        logger.info(
            "Event rejected",
            extra={
                "event_id": event.EventID,
                "admin_user_id": admin_user_id,
                "public_review_status_id": rejected_status.PublicReviewStatusID,
            },
        )
        return event

    # ------------------------------------------------------------------ #
    # Query operations
    # ------------------------------------------------------------------ #
    def get_pending_review_events(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return pending events prepared for the PendingReviewEventResponse schema.
        """
        pending_status = self._get_public_review_status("PENDING")
        if not pending_status:
            return []

        archived_status = self._get_event_status("ARCHIVED")

        query = (
            self.db.query(Event)
            .options(
                joinedload(Event.company),
                joinedload(Event.created_by_user),
            )
            .filter(
                Event.IsPublic == True,  # noqa: E712
                Event.IsSharedWithPlatform == True,  # noqa: E712
                Event.PublicReviewStatusID == pending_status.PublicReviewStatusID,
                Event.IsDeleted == False,  # noqa: E712
            )
            )

        if archived_status:
            query = query.filter(Event.EventStatusID != archived_status.EventStatusID)
        
        if filters:
            if filters.get("event_type_id"):
                query = query.filter(Event.EventTypeID == filters["event_type_id"])
            if filters.get("company_id"):
                query = query.filter(Event.CompanyID == filters["company_id"])
            if filters.get("date_from"):
                query = query.filter(Event.CreatedDate >= filters["date_from"])
            if filters.get("date_to"):
                query = query.filter(Event.CreatedDate <= filters["date_to"])

        events = (
            query.order_by(Event.CreatedDate.asc()).offset(skip).limit(limit).all()
        )

        responses: List[Dict[str, Any]] = []
        now = datetime.utcnow()

        for event in events:
            created_date = event.CreatedDate or now
            days_pending = max((now - created_date).days, 0)
            responses.append(
                {
                    "event_id": event.EventID,
                    "name": event.Name,
                    "description": event.Description,
                    "company_name": event.company.CompanyName if event.company else "",
                    "creator_email": (
                        event.created_by_user.Email if event.created_by_user else None
                    ),
                    "created_date": created_date,
                    "days_pending": days_pending,
                }
            )
        
        return responses
    
    def get_event_review_details(self, event_id: int) -> Optional[Dict[str, Any]]:
        """
        Return full event details for admin review.
        """
        try:
            event = self._get_event(event_id)
        except ValueError:
            return None
        
        return {
            "event_id": event.EventID,
            "name": event.Name,
            "description": event.Description,
            "company_name": event.company.CompanyName if event.company else "",
            "creator_email": (
                event.created_by_user.Email if event.created_by_user else None
            ),
            "start_date_time": event.StartDateTime,
            "end_date_time": event.EndDateTime,
            "venue_name": event.VenueName,
            "venue_address": event.VenueAddress,
            "city": event.City,
            "state": event.State,
            "country_name": event.country.CountryName if event.country else None,
            "event_type_name": (
                event.event_type.TypeName if event.event_type else "Unknown"
            ),
            "event_status_name": (
                event.event_status.StatusName if event.event_status else "Unknown"
            ),
            "industry_name": event.industry.IndustryName if event.industry else None,
            "is_public": bool(event.IsPublic),
            "public_review_status": (
                event.public_review_status.StatusCode
                if event.public_review_status
                else None
            ),
            "created_date": event.CreatedDate,
        }

    def get_review_history(self, event_id: int) -> List[Dict[str, Any]]:
        """
        Build a lightweight review history from the event record itself.
        (Future enhancement: move to dedicated audit table.)
        """
        try:
            event = self._get_event(event_id)
        except ValueError:
            return []

        if not event.PublicReviewDate:
            return []

        reviewer = event.public_review_by_user.Email if event.public_review_by_user else None
        decision = (
            event.public_review_status.StatusCode
            if event.public_review_status
            else None
        )

        return [
            {
                "review_id": event.EventID,
                "event_id": event.EventID,
                "event_name": event.Name,
                "reviewer_email": reviewer,
                "review_date": event.PublicReviewDate,
                "decision": decision,
                "comments": event.PublicReviewComments,
            }
        ]

    def get_event_review_status(self, event_id: int) -> Optional[Dict[str, Any]]:
        """
        Return review status information for event creators.
        """
        try:
            event = self._get_event(event_id)
        except ValueError:
            return None

        reviewer_email = (
            event.public_review_by_user.Email if event.public_review_by_user else None
        )

        return {
            "review_status": (
                event.public_review_status.StatusCode
                if event.public_review_status
                else None
            ),
            "review_date": event.PublicReviewDate,
            "reviewer_email": reviewer_email,
            "review_comments": event.PublicReviewComments,
            "public_visibility_date": event.PublicVisibilityDate,
        }
