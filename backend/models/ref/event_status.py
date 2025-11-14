"""
EventStatus Reference Model (ref.EventStatus)
Event status classifications with dashboard visual elements
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class EventStatus(Base):
    """
    EventStatus reference table for event status management.
    
    Attributes:
        EventStatusID: Primary key
        StatusCode: Unique status code (e.g., 'DRAFT', 'PUBLISHED')
        StatusName: Display name (e.g., 'Draft', 'Published')
        StatusDescription: Full description of the status
        StatusColor: Hex color code for dashboard display
        StatusIcon: Icon name for dashboard display
        IsActive: Whether status is available for selection
        SortOrder: Display order for status selection
    """
    
    __tablename__ = "EventStatus"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    EventStatusID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Core Fields
    StatusCode = Column(String(20), nullable=False, unique=True)
    StatusName = Column(String(50), nullable=False)
    StatusDescription = Column(String(200), nullable=True)
    
    # Dashboard Visual Elements
    StatusColor = Column(String(7), nullable=True)  # Hex color code
    StatusIcon = Column(String(50), nullable=True)  # Icon name
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    events = relationship("Event", back_populates="event_status", foreign_keys="[Event.EventStatusID]")
    
    def __repr__(self) -> str:
        return f"<EventStatus(EventStatusID={self.EventStatusID}, StatusCode='{self.StatusCode}', StatusName='{self.StatusName}')>"


