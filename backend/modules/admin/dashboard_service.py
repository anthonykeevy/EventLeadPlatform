"""
Admin Dashboard Service
Story 2.6: Admin Public Event Review Workflow
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, select
from sqlalchemy.sql import func as sql_func
from typing import List, Optional
from datetime import datetime, timedelta

from models import Event, Company, UserCompany, User
from models.ref.public_review_status import PublicReviewStatus
from models.ref.event_status import EventStatus
from modules.admin.dashboard_schemas import (
    AdminCompanyResponse,
    AdminKPIsResponse,
    AdminEventResponse,
)


class AdminDashboardService:
    """Service for admin dashboard operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_companies(self) -> List[AdminCompanyResponse]:
        """Get all companies on the platform"""
        companies = self.db.query(Company).filter(
            Company.IsDeleted == False
        ).all()
        
        result = []
        for company in companies:
            # Get total users for this company
            total_users = self.db.query(func.count(UserCompany.UserID)).filter(
                and_(
                    UserCompany.CompanyID == company.CompanyID,
                    UserCompany.IsDeleted == False
                )
            ).scalar() or 0
            
            # Get total events for this company
            total_events = self.db.query(func.count(Event.EventID)).filter(
                and_(
                    Event.CompanyID == company.CompanyID,
                    Event.IsDeleted == False
                )
            ).scalar() or 0
            
            result.append(AdminCompanyResponse(
                company_id=company.CompanyID,
                company_name=company.CompanyName,
                created_date=company.CreatedDate,
                total_users=total_users,
                total_events=total_events,
            ))
        
        return result
    
    def get_platform_kpis(self) -> AdminKPIsResponse:
        """Get platform-wide KPIs with breakdowns"""
        # Get archived status for filtering
        archived_status = self.db.execute(
            select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
        ).scalar_one_or_none()
        
        # Total companies
        total_companies = self.db.query(func.count(Company.CompanyID)).filter(
            Company.IsDeleted == False
        ).scalar() or 0
        
        # Total users
        total_users = self.db.query(func.count(User.UserID)).filter(
            User.IsDeleted == False
        ).scalar() or 0
        
        # Total events (excluding archived)
        event_query = self.db.query(func.count(Event.EventID)).filter(
            Event.IsDeleted == False
        )
        if archived_status:
            event_query = event_query.filter(Event.EventStatusID != archived_status.EventStatusID)
        total_events = event_query.scalar() or 0
        
        # Event breakdowns: Past, Current, Future
        # Definitions:
        # - Past: Events that have an End date before today
        # - Current: Events that have not expired AND have a start date within the next 2 months
        # - Future: Events with a start date more than 2 months in the future
        now = datetime.utcnow()
        two_months_from_now = now + timedelta(days=60)
        
        # Base filter for all event queries (excluding archived and deleted)
        base_filter = [Event.IsDeleted == False]
        if archived_status:
            base_filter.append(Event.EventStatusID != archived_status.EventStatusID)
        
        # Past events: EndDate < today OR started more than 2 months ago
        # This includes:
        # - Events that have ended (EndDate < now)
        # - Old events that started more than 2 months ago (even if not ended, they're effectively "past")
        two_months_ago = now - timedelta(days=60)
        past_query = self.db.query(func.count(Event.EventID)).filter(
            *base_filter,
            or_(
                and_(
                    Event.EndDateTime.isnot(None),
                    Event.EndDateTime < now
                ),
                Event.StartDateTime < two_months_ago
            )
        )
        events_past = past_query.scalar() or 0
        
        # Current events: not expired AND StartDate within next 2 months
        # Not expired: EndDate is null OR EndDate >= now
        # StartDate within next 2 months: StartDate >= 2 months ago AND StartDate <= 2 months from now
        # This includes:
        # - Ongoing events (StartDate >= 2 months ago and < now but not expired)
        # - Upcoming events (StartDate >= now and <= 2 months from now)
        current_query = self.db.query(func.count(Event.EventID)).filter(
            *base_filter,
            or_(
                Event.EndDateTime.is_(None),
                Event.EndDateTime >= now
            ),
            Event.StartDateTime >= two_months_ago,
            Event.StartDateTime <= two_months_from_now
        )
        events_current = current_query.scalar() or 0
        
        # Future events: StartDate > 2 months from now
        future_query = self.db.query(func.count(Event.EventID)).filter(
            *base_filter,
            Event.StartDateTime > two_months_from_now
        )
        events_future = future_query.scalar() or 0
        
        # User breakdowns: Inactive, Seldom, Active
        three_months_ago = now - timedelta(days=90)
        twelve_months_ago = now - timedelta(days=365)
        
        # Inactive: created account but never logged in again OR not logged in for 12 months
        inactive_users = self.db.query(func.count(User.UserID)).filter(
            User.IsDeleted == False,
            or_(
                and_(User.LastLoginDate.is_(None), User.CreatedDate < twelve_months_ago),
                and_(User.LastLoginDate.isnot(None), User.LastLoginDate < twelve_months_ago)
            )
        ).scalar() or 0
        
        # Seldom: logged in multiple times (>1) AND last login 3-12 months ago
        seldom_users = self.db.query(func.count(User.UserID)).filter(
            User.IsDeleted == False,
            User.LastLoginDate.isnot(None),
            User.LastLoginDate >= twelve_months_ago,
            User.LastLoginDate < three_months_ago
        ).scalar() or 0
        
        # Active: logged in multiple times (>1) AND last login within 3 months
        active_users = self.db.query(func.count(User.UserID)).filter(
            User.IsDeleted == False,
            User.LastLoginDate.isnot(None),
            User.LastLoginDate >= three_months_ago
        ).scalar() or 0
        
        # Company breakdowns: Inactive, Seldom, Active
        # Get company IDs with events in different time periods
        companies_with_recent_events_ids = [
            row[0] for row in self.db.query(Event.CompanyID).filter(
                Event.IsDeleted == False,
                Event.StartDateTime >= three_months_ago
            ).distinct().all()
        ]
        
        companies_with_old_events_ids = [
            row[0] for row in self.db.query(Event.CompanyID).filter(
                Event.IsDeleted == False,
                Event.StartDateTime >= twelve_months_ago,
                Event.StartDateTime < three_months_ago
            ).distinct().all()
        ]
        
        companies_with_any_events_ids = [
            row[0] for row in self.db.query(Event.CompanyID).filter(
                Event.IsDeleted == False,
                Event.StartDateTime >= twelve_months_ago
            ).distinct().all()
        ]
        
        # Inactive: no active events in last 12 months
        inactive_companies = self.db.query(func.count(Company.CompanyID)).filter(
            Company.IsDeleted == False,
            ~Company.CompanyID.in_(companies_with_any_events_ids) if companies_with_any_events_ids else True
        ).scalar() or 0
        
        # Seldom: had events in last 12 months but not in last 3 months
        seldom_company_ids = [
            cid for cid in companies_with_any_events_ids 
            if cid not in companies_with_recent_events_ids
        ]
        seldom_companies = self.db.query(func.count(Company.CompanyID)).filter(
            Company.IsDeleted == False,
            Company.CompanyID.in_(seldom_company_ids) if seldom_company_ids else False
        ).scalar() or 0
        
        # Active: active events in last 3 months OR current active events
        active_companies = self.db.query(func.count(Company.CompanyID)).filter(
            Company.IsDeleted == False,
            Company.CompanyID.in_(companies_with_recent_events_ids) if companies_with_recent_events_ids else False
        ).scalar() or 0
        
        # Pending review events
        status_counts = (
            self.db.query(
                PublicReviewStatus.StatusCode,
                func.count(Event.EventID)
            )
            .join(
                PublicReviewStatus,
                Event.PublicReviewStatusID == PublicReviewStatus.PublicReviewStatusID
            )
            .filter(Event.IsDeleted == False)
            .group_by(PublicReviewStatus.StatusCode)
            .all()
        )

        status_map = {code: count for code, count in status_counts}

        pending_review = status_map.get('PENDING', 0)
        approved = status_map.get('APPROVED', 0)
        rejected = status_map.get('REJECTED', 0)
        
        return AdminKPIsResponse(
            total_companies=total_companies,
            total_users=total_users,
            total_events=total_events,
            pending_review_events=pending_review,
            approved_events=approved,
            rejected_events=rejected,
            # Event breakdowns
            events_past=events_past,
            events_current=events_current,
            events_future=events_future,
            # User breakdowns
            users_inactive=inactive_users,
            users_seldom=seldom_users,
            users_active=active_users,
            # Company breakdowns
            companies_inactive=inactive_companies,
            companies_seldom=seldom_companies,
            companies_active=active_companies,
        )
    
    def get_all_events(
        self,
        skip: int = 0,
        limit: int = 100,
        event_status_id: Optional[int] = None,
        event_type_id: Optional[int] = None,
        public_review_status: Optional[str] = None,
        date_filter: Optional[str] = None,  # 'past', 'current', 'future'
    ) -> tuple[List[AdminEventResponse], int]:
        """Get all events on the platform (admin-only, no company filter)"""
        # Get archived status for filtering
        archived_status = self.db.execute(
            select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
        ).scalar_one_or_none()
        
        base_query = (
            self.db.query(Event)
            .outerjoin(
                PublicReviewStatus,
                Event.PublicReviewStatusID == PublicReviewStatus.PublicReviewStatusID
            )
            .filter(Event.IsDeleted == False)
        )
        
        # Exclude archived events (same as total_events count)
        if archived_status:
            base_query = base_query.filter(Event.EventStatusID != archived_status.EventStatusID)
        
        # Date filtering: Past, Current, Future
        if date_filter:
            now = datetime.utcnow()
            two_months_from_now = now + timedelta(days=60)
            two_months_ago = now - timedelta(days=60)
            
            if date_filter == 'past':
                # Past: EndDate < today OR started more than 2 months ago
                base_query = base_query.filter(
                    or_(
                        and_(
                            Event.EndDateTime.isnot(None),
                            Event.EndDateTime < now
                        ),
                        Event.StartDateTime < two_months_ago
                    )
                )
            elif date_filter == 'current':
                # Current: not expired AND StartDate within next 2 months (from 2 months ago to 2 months from now)
                base_query = base_query.filter(
                    or_(
                        Event.EndDateTime.is_(None),
                        Event.EndDateTime >= now
                    ),
                    Event.StartDateTime >= two_months_ago,
                    Event.StartDateTime <= two_months_from_now
                )
            elif date_filter == 'future':
                # Future: StartDate > 2 months from now
                base_query = base_query.filter(
                    Event.StartDateTime > two_months_from_now
                )
        
        if event_status_id:
            base_query = base_query.filter(Event.EventStatusID == event_status_id)
        
        if event_type_id:
            base_query = base_query.filter(Event.EventTypeID == event_type_id)
        
        if public_review_status:
            base_query = base_query.filter(PublicReviewStatus.StatusCode == public_review_status)
        
        total = (
            base_query
            .with_entities(func.count(Event.EventID))
            .scalar()
        ) or 0

        events = (
            base_query
            .options(
                joinedload(Event.company),
                joinedload(Event.event_type),
                joinedload(Event.event_status),
                joinedload(Event.industry),
                joinedload(Event.country),
                joinedload(Event.organizer_company),
                joinedload(Event.public_review_status)
            )
            .order_by(Event.CreatedDate.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        result = []
        for event in events:
            result.append(AdminEventResponse(
                event_id=event.EventID,
                name=event.Name,
                description=event.Description,
                short_description=event.ShortDescription,
                company_id=event.CompanyID,
                company_name=event.company.CompanyName if event.company else "Unknown",
                event_type_id=event.EventTypeID,
                event_type_name=event.event_type.TypeName if event.event_type else "Unknown",
                event_status_id=event.EventStatusID,
                event_status_name=event.event_status.StatusName if event.event_status else "Unknown",
                industry_id=event.IndustryID,
                industry_name=event.industry.IndustryName if event.industry else None,
                country_id=event.CountryID,
                country_name=event.country.CountryName if event.country else None,
                start_date_time=event.StartDateTime,
                end_date_time=event.EndDateTime,
                timezone_identifier=event.TimezoneIdentifier,
                venue_name=event.VenueName,
                venue_address=event.VenueAddress,
                city=event.City,
                state=event.State,
                latitude=float(event.Latitude) if event.Latitude else None,
                longitude=float(event.Longitude) if event.Longitude else None,
                tags=event.Tags,
                is_public=event.IsPublic,
                is_shared_with_platform=event.IsSharedWithPlatform,
                is_recurring=event.IsRecurring,
                organizer_company_id=event.OrganizerCompanyID,
                organizer_company_name=event.organizer_company.CompanyName if event.organizer_company else None,
                organizer_contact_email=event.OrganizerContactEmail,
                organizer_website=event.OrganizerWebsite,
                expected_attendees=event.ExpectedAttendees,
                public_review_status=event.public_review_status.StatusCode if event.public_review_status else None,
                created_date=event.CreatedDate,
            ))
        
        return result, total
