"""
PublicReviewStatus Reference Model (ref.PublicReviewStatus)
Public review status classifications for event review workflow
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class PublicReviewStatus(Base):
    """
    PublicReviewStatus reference table for event public review workflow.
    
    Status Codes:
        PENDING: Event is in admin review queue
        APPROVED: Admin approved - event can go public when user publishes it
        REJECTED: Admin rejected - event cannot be made public
    
    Attributes:
        PublicReviewStatusID: Primary key
        StatusCode: Unique status code (e.g., 'PENDING', 'APPROVED', 'REJECTED')
        StatusName: Display name (e.g., 'Pending Review', 'Approved', 'Rejected')
        StatusDescription: Full description of the status
        StatusColor: Hex color code for dashboard display
        StatusIcon: Icon name for dashboard display
        IsActive: Whether status is available for selection
        SortOrder: Display order for status selection
    """
    
    __tablename__ = "PublicReviewStatus"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    PublicReviewStatusID = Column(BigInteger, primary_key=True, autoincrement=True)
    
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
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)  # Nullable for system-created records
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    events = relationship("Event", back_populates="public_review_status", foreign_keys="[Event.PublicReviewStatusID]")
    
    def __repr__(self) -> str:
        return f"<PublicReviewStatus(PublicReviewStatusID={self.PublicReviewStatusID}, StatusCode='{self.StatusCode}', StatusName='{self.StatusName}')>"


