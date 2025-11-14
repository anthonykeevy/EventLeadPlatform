"""
Event Model (dbo.Event)
Core event entity with comprehensive metadata and lifecycle management
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from common.database import Base


class Event(Base):
    """
    Event model representing events where users collect leads and forms.
    
    Features:
    - Multi-tenant event access (company-scoped)
    - Complete lifecycle management (Draft → Published → Completed)
    - Location support (Physical, Online, Hybrid)
    - Industry classification
    - Event type categorization
    - Public/private visibility
    - Audit trail with full change tracking
    - Soft deletes for data retention
    
    Attributes:
        EventID: Primary key
        Name: Event name/title
        Description: Detailed event description
        ShortDescription: Brief summary for list views
        CompanyID: Owner company (for multi-tenant filtering)
        CreatedBy: User who created event
        StartDateTime: Event start date/time (UTC)
        EndDateTime: Event end date/time (UTC, nullable)
        TimezoneIdentifier: IANA timezone for display
        VenueName: Venue name
        VenueAddress: Full venue address
        City: City name
        State: State/Province
        CountryID: Country (foreign key)
        Latitude: GPS latitude
        Longitude: GPS longitude
        EventTypeID: Event type (foreign key)
        IndustryID: Industry (foreign key, nullable)
        Tags: Comma-separated tags
        IsPublic: Public visibility flag
        EventStatusID: Event status (foreign key)
        IsRecurring: Recurring event flag
        RecurrencePatternID: Recurrence pattern (foreign key, nullable)
        IsPublicReviewRequired: Public review required flag
        IsSharedWithPlatform: User's choice to share event with platform-wide search
        PublicReviewStatusID: Public review status (foreign key to ref.PublicReviewStatus)
        PublicReviewDate: Public review completion date
        PublicReviewBy: User who completed review
        PublicReviewComments: Review comments
        PublicVisibilityDate: Specific date when event becomes public
        DuplicateEventID: Original event ID if duplicate
        IsDuplicate: Duplicate event flag
        OrganizerCompanyID: Organizer company (foreign key, nullable)
        OrganizerContactEmail: Organizer contact email
        OrganizerWebsite: Organizer website
        ExpectedAttendees: Expected attendance
        ActualAttendees: Actual attendance
        FormsCreated: Number of forms created
        TotalSubmissions: Total form submissions
    """
    
    __tablename__ = "Event"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    EventID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Event Identity
    Name = Column(String(200), nullable=False)
    Description = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    ShortDescription = Column(String(500), nullable=True)
    
    # Ownership and Context
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    
    # Date/Time Information
    StartDateTime = Column(DateTime, nullable=False)
    EndDateTime = Column(DateTime, nullable=True)
    TimezoneIdentifier = Column(String(50), nullable=True)
    
    # Location Information
    VenueName = Column(String(200), nullable=True)
    VenueAddress = Column(String(500), nullable=True)
    City = Column(String(100), nullable=True)
    State = Column(String(100), nullable=True)
    CountryID = Column(BigInteger, ForeignKey('ref.Country.CountryID'), nullable=True)
    Latitude = Column(DECIMAL(10, 8), nullable=True)
    Longitude = Column(DECIMAL(11, 8), nullable=True)
    
    # Classification
    EventTypeID = Column(Integer, ForeignKey('ref.EventType.EventTypeID'), nullable=False, index=True)
    IndustryID = Column(BigInteger, ForeignKey('ref.Industry.IndustryID'), nullable=True)
    Tags = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    
    # Event Configuration
    IsPublic = Column(Boolean, nullable=False, default=False)
    EventStatusID = Column(Integer, ForeignKey('ref.EventStatus.EventStatusID'), nullable=False, index=True)
    IsRecurring = Column(Boolean, nullable=False, default=False)
    RecurrencePatternID = Column(Integer, ForeignKey('ref.RecurrencePattern.RecurrencePatternID'), nullable=True)
    
    # Public Event Review Process
    IsPublicReviewRequired = Column(Boolean, nullable=False, default=False)
    IsSharedWithPlatform = Column(Boolean, nullable=False, default=False)  # User's choice to share with platform-wide search
    PublicReviewStatusID = Column(BigInteger, ForeignKey('ref.PublicReviewStatus.PublicReviewStatusID'), nullable=True)  # FK to ref.PublicReviewStatus
    PublicReviewDate = Column(DateTime, nullable=True)
    PublicReviewBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    PublicReviewComments = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    PublicVisibilityDate = Column(DateTime, nullable=True)
    
    # Duplicate Event Detection
    DuplicateEventID = Column(BigInteger, ForeignKey('dbo.Event.EventID'), nullable=True)
    IsDuplicate = Column(Boolean, nullable=False, default=False)
    
    # Organizer Information
    OrganizerCompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True)
    OrganizerContactEmail = Column(String(100), nullable=True)
    OrganizerWebsite = Column(String(200), nullable=True)
    
    # Event Metrics
    ExpectedAttendees = Column(Integer, nullable=True)
    ActualAttendees = Column(Integer, nullable=True)
    FormsCreated = Column(Integer, nullable=False, default=0)
    TotalSubmissions = Column(Integer, nullable=False, default=0)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    company = relationship("Company", foreign_keys=[CompanyID])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    event_type = relationship("EventType", foreign_keys=[EventTypeID])
    event_status = relationship("EventStatus", foreign_keys=[EventStatusID])
    recurrence_pattern = relationship("RecurrencePattern", foreign_keys=[RecurrencePatternID])
    industry = relationship("Industry", foreign_keys=[IndustryID])
    country = relationship("Country", foreign_keys=[CountryID])
    organizer_company = relationship("Company", foreign_keys=[OrganizerCompanyID])
    original_event = relationship("Event", remote_side=[EventID], foreign_keys=[DuplicateEventID])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])
    public_review_status = relationship("PublicReviewStatus", foreign_keys=[PublicReviewStatusID])
    public_review_by_user = relationship("User", foreign_keys=[PublicReviewBy])
    
    def __repr__(self) -> str:
        return f"<Event(EventID={self.EventID}, Name='{self.Name}', CompanyID={self.CompanyID})>"

