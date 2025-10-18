"""
JoinedVia Reference Model (ref.JoinedVia)
Methods by which users join companies
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class JoinedVia(Base):
    """
    Joined via reference table for tracking how users join companies.
    
    Methods: Signup, Invitation, Import, Admin, API
    
    Attributes:
        JoinedViaID: Primary key
        MethodCode: Unique method code (e.g., 'signup', 'invitation', 'import')
        MethodName: Display name (e.g., 'Sign Up', 'Team Invitation')
        Description: Full description of the join method
        IsActive: Whether this method is available for use
        SortOrder: Display order
    """
    
    __tablename__ = "JoinedVia"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    JoinedViaID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    MethodCode = Column(String(20), nullable=False, unique=True)
    MethodName = Column(String(50), nullable=False)
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
    user_companies = relationship("UserCompany", back_populates="joined_via", foreign_keys="[UserCompany.JoinedViaID]")
    
    def __repr__(self) -> str:
        return f"<JoinedVia(JoinedViaID={self.JoinedViaID}, MethodCode='{self.MethodCode}', MethodName='{self.MethodName}')>"

