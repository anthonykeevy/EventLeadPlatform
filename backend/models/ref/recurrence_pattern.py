"""
RecurrencePattern Reference Model (ref.RecurrencePattern)
Recurrence pattern classifications for recurring events
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class RecurrencePattern(Base):
    """
    RecurrencePattern reference table for event recurrence management.
    
    Attributes:
        RecurrencePatternID: Primary key
        PatternCode: Unique pattern code (e.g., 'DAILY', 'WEEKLY')
        PatternName: Display name (e.g., 'Daily', 'Weekly')
        PatternDescription: Full description of the pattern
        PatternFormula: Formula for calculating next occurrence
        IsActive: Whether pattern is available for selection
        SortOrder: Display order for pattern selection
    """
    
    __tablename__ = "RecurrencePattern"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    RecurrencePatternID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Core Fields
    PatternCode = Column(String(20), nullable=False, unique=True)
    PatternName = Column(String(50), nullable=False)
    PatternDescription = Column(String(200), nullable=True)
    PatternFormula = Column(String(100), nullable=True)  # Formula for calculating next occurrence
    
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
    events = relationship("Event", back_populates="recurrence_pattern", foreign_keys="[Event.RecurrencePatternID]")
    
    def __repr__(self) -> str:
        return f"<RecurrencePattern(RecurrencePatternID={self.RecurrencePatternID}, PatternCode='{self.PatternCode}', PatternName='{self.PatternName}')>"


