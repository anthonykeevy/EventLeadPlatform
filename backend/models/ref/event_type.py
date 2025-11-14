"""
EventType Reference Model (ref.EventType)
Event type classifications for events
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class EventType(Base):
    """
    EventType reference table for event classification.
    
    Attributes:
        EventTypeID: Primary key
        TypeCode: Unique event type code (e.g., 'TRADE_SHOW', 'CONFERENCE')
        TypeName: Display name (e.g., 'Trade Show', 'Conference')
        TypeDescription: Full description of the event type
        IsActive: Whether event type is available for selection
        SortOrder: Display order for event type selection
    """
    
    __tablename__ = "EventType"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    EventTypeID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Core Fields
    TypeCode = Column(String(20), nullable=False, unique=True)
    TypeName = Column(String(50), nullable=False)
    TypeDescription = Column(String(200), nullable=True)
    
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
    events = relationship("Event", back_populates="event_type", foreign_keys="[Event.EventTypeID]")
    
    def __repr__(self) -> str:
        return f"<EventType(EventTypeID={self.EventTypeID}, TypeCode='{self.TypeCode}', TypeName='{self.TypeName}')>"


