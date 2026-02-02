"""
FrontendEvent Model (log.FrontendEvent)
Frontend logging integration for builder operations
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from common.database import Base


class FrontendEvent(Base):
    """
    Frontend event log model.
    
    Captures frontend events from the builder (SmartBorder, drag, resize, etc.)
    for unified debugging through enhanced_diagnostic_logs.py
    
    Attributes:
        FrontendEventID: Primary key
        EventType: Event category (e.g., 'smartborder.drag.state', 'fieldshell.resize.commit')
        Level: Log level (debug, info, warn, error)
        ComponentId: The component ID this event relates to
        ComponentType: The component type (first-name, text, submit-button, etc.)
        Payload: JSON-encoded event payload
        MetricsJson: JSON-encoded component metrics snapshot
        LayoutType: Derived layout type (grid/object)
        ObjectCount: Count of objects in snapshot
        ContainerWidth: Container width (px)
        ContainerHeight: Container height (px)
        GridColumns: Grid column count (for grid layout)
        GridRows: Grid row count (for grid layout)
        HasValidationObject: Whether validation object is present
        SessionId: Browser session identifier
        UserID: Foreign key to dbo.User (nullable - may not be authenticated)
        RequestID: Correlation ID (nullable)
        BrowserInfo: Browser/user agent information
        PageUrl: The page URL where event occurred
        CreatedDate: Timestamp when event occurred
    """
    
    __tablename__ = "FrontendEvent"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    FrontendEventID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Event Details
    EventType = Column(String(200), nullable=False, index=True)
    Level = Column(String(20), nullable=False, index=True)  # debug, info, warn, error
    
    # Component Context
    ComponentID = Column(String(100), nullable=True, index=True)
    ComponentType = Column(String(100), nullable=True, index=True)
    
    # Payload
    Payload = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    MetricsJson = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON metrics snapshot

    # Metrics Summary (denormalized for fast querying)
    LayoutType = Column(String(50), nullable=True)
    ObjectCount = Column(Integer, nullable=True)
    ContainerWidth = Column(Integer, nullable=True)
    ContainerHeight = Column(Integer, nullable=True)
    GridColumns = Column(Integer, nullable=True)
    GridRows = Column(Integer, nullable=True)
    HasValidationObject = Column(Boolean, nullable=False, server_default="0")
    
    # Session Context
    SessionID = Column(String(100), nullable=True, index=True)
    
    # User Context
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Request Correlation
    RequestID = Column(String(100), nullable=True)
    
    # Browser Context
    BrowserInfo = Column(String(500), nullable=True)
    PageURL = Column(String(1000), nullable=True)
    
    # Timestamp (from frontend)
    ClientTimestamp = Column(BigInteger, nullable=True)  # Unix timestamp from frontend
    
    # Server Timestamp
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="frontend_events")
    
    def __repr__(self) -> str:
        return f"<FrontendEvent(FrontendEventID={self.FrontendEventID}, EventType='{self.EventType}', Level='{self.Level}')>"











