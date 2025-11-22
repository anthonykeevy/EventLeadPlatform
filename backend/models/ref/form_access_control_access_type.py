"""
FormAccessControlAccessType Model (ref.FormAccessControlAccessType)
Reference table for form access control access types (View, Edit, Manage, Submit, Analyze)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class FormAccessControlAccessType(Base):
    """
    FormAccessControlAccessType reference model.
    
    Attributes:
        FormAccessControlAccessTypeID: Primary key
        AccessTypeCode: Access type code (VIEW, EDIT, MANAGE, SUBMIT, ANALYZE)
        AccessTypeName: Human-readable name (View, Edit, Manage, Submit, Analyze)
        AccessTypeDescription: Description of access type
        IsActive: Whether the type is active
        SortOrder: Display order
    """
    
    __tablename__ = "FormAccessControlAccessType"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    FormAccessControlAccessTypeID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Access Type Identity
    AccessTypeCode = Column(String(20), nullable=False, unique=True)
    AccessTypeName = Column(String(50), nullable=False)
    AccessTypeDescription = Column(String(200), nullable=True)
    
    # Configuration
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
    form_access_controls = relationship("FormAccessControl", back_populates="access_type")
    
    def __repr__(self) -> str:
        return f"<FormAccessControlAccessType(ID={self.FormAccessControlAccessTypeID}, Code='{self.AccessTypeCode}', Name='{self.AccessTypeName}')>"

