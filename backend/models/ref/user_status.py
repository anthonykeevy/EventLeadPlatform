"""
UserStatus Reference Model (ref.UserStatus)
Status codes for user accounts
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from backend.common.database import Base


class UserStatus(Base):
    """
    User status reference table.
    
    Status codes: Active, Pending, Locked, Inactive
    
    Attributes:
        UserStatusID: Primary key
        StatusCode: Unique status code (e.g., 'active', 'pending', 'locked')
        StatusName: Display name (e.g., 'Active', 'Pending Verification')
        Description: Full description of the status
        AllowLogin: Whether users with this status can log in
        IsActive: Whether this status is available for use
        SortOrder: Display order
    """
    
    __tablename__ = "UserStatus"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    UserStatusID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    StatusCode = Column(String(20), nullable=False, unique=True)
    StatusName = Column(String(50), nullable=False)
    Description = Column(String(500), nullable=False)
    AllowLogin = Column(Boolean, nullable=False, default=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="status", foreign_keys="[User.StatusID]")
    
    def __repr__(self) -> str:
        return f"<UserStatus(UserStatusID={self.UserStatusID}, StatusCode='{self.StatusCode}', StatusName='{self.StatusName}')>"

