"""
FormAccessControl Model (dbo.FormAccessControl)
Access control for forms - grants access to users/companies with different permission levels
"""
from sqlalchemy import Column, BigInteger, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from common.database import Base


class FormAccessControl(Base):
    """
    FormAccessControl model for managing form access grants.
    
    Features:
    - Granular access control (View, Edit, Manage, Submit, Analyze)
    - User and company-based access grants
    - Access expiry support (optional ExpiryDate)
    - Relationship type tracking (Partner, Vendor, Client, Affiliate)
    - Audit trail with full change tracking
    - Soft deletes for data retention
    
    Attributes:
        FormAccessControlID: Primary key
        FormID: Form being accessed (FK to Form)
        UserID: User with access (FK to User)
        CompanyID: Company granting access (FK to Company)
        FormAccessControlAccessTypeID: Access type (FK to FormAccessControlAccessType)
        CompanyRelationshipTypeID: Relationship type (FK to CompanyRelationshipType)
        GrantedBy: User who granted access (FK to User)
        GrantedDate: When access was granted (UTC)
        ExpiryDate: When access expires (NULL = permanent access)
    """
    
    __tablename__ = "FormAccessControl"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    FormAccessControlID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Form and User References
    FormID = Column(BigInteger, ForeignKey('dbo.Form.FormID'), nullable=False, index=True)
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    
    # Access Control Details (Reference Tables)
    FormAccessControlAccessTypeID = Column(Integer, ForeignKey('ref.FormAccessControlAccessType.FormAccessControlAccessTypeID'), nullable=False, index=True)
    CompanyRelationshipTypeID = Column(Integer, ForeignKey('ref.CompanyRelationshipType.CompanyRelationshipTypeID'), nullable=False)
    
    # Access Management
    GrantedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    GrantedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    ExpiryDate = Column(DateTime, nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    
    # Relationships
    form = relationship("Form", foreign_keys=[FormID])
    user = relationship("User", foreign_keys=[UserID])
    company = relationship("Company", foreign_keys=[CompanyID])
    access_type = relationship("FormAccessControlAccessType", foreign_keys=[FormAccessControlAccessTypeID])
    relationship_type = relationship("CompanyRelationshipType", foreign_keys=[CompanyRelationshipTypeID])
    granted_by_user = relationship("User", foreign_keys=[GrantedBy])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    
    def __repr__(self) -> str:
        return f"<FormAccessControl(FormAccessControlID={self.FormAccessControlID}, FormID={self.FormID}, UserID={self.UserID})>"

