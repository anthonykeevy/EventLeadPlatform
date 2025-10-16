"""
UserInvitationStatus Reference Model (ref.UserInvitationStatus)
Status codes for user invitations
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class UserInvitationStatus(Base):
    """
    User invitation status reference table.
    
    Status codes: Pending, Accepted, Declined, Expired, Cancelled
    
    Attributes:
        UserInvitationStatusID: Primary key
        StatusCode: Unique status code (e.g., 'pending', 'accepted', 'expired')
        StatusName: Display name (e.g., 'Pending', 'Accepted')
        Description: Full description of the status
        CanResend: Whether invitations in this status can be resent
        CanCancel: Whether invitations in this status can be cancelled
        IsFinalState: Whether this status is terminal (no further changes)
        IsActive: Whether this status is available for use
        SortOrder: Display order
    """
    
    __tablename__ = "UserInvitationStatus"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    UserInvitationStatusID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    StatusCode = Column(String(20), nullable=False, unique=True)
    StatusName = Column(String(50), nullable=False)
    Description = Column(String(500), nullable=False)
    CanResend = Column(Boolean, nullable=False, default=False)
    CanCancel = Column(Boolean, nullable=False, default=False)
    IsFinalState = Column(Boolean, nullable=False, default=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    invitations = relationship("UserInvitation", back_populates="status", foreign_keys="[UserInvitation.StatusID]")
    
    def __repr__(self) -> str:
        return f"<UserInvitationStatus(UserInvitationStatusID={self.UserInvitationStatusID}, StatusCode='{self.StatusCode}')>"

