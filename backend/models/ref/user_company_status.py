"""
UserCompanyStatus Reference Model (ref.UserCompanyStatus)
Status codes for user-company relationships
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class UserCompanyStatus(Base):
    """
    User company status reference table.
    
    Status codes: Active, Inactive, Suspended, Removed
    
    Attributes:
        UserCompanyStatusID: Primary key
        StatusCode: Unique status code (e.g., 'active', 'inactive', 'suspended')
        StatusName: Display name (e.g., 'Active', 'Inactive')
        Description: Full description of the status
        IsActive: Whether this status is available for use
        SortOrder: Display order
    """
    
    __tablename__ = "UserCompanyStatus"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    UserCompanyStatusID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    StatusCode = Column(String(20), nullable=False, unique=True)
    StatusName = Column(String(50), nullable=False)
    Description = Column(String(500), nullable=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    user_companies = relationship("UserCompany", back_populates="status", foreign_keys="[UserCompany.StatusID]")
    
    def __repr__(self) -> str:
        return f"<UserCompanyStatus(UserCompanyStatusID={self.UserCompanyStatusID}, StatusCode='{self.StatusCode}')>"

