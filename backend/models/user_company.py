"""
UserCompany Model (dbo.UserCompany)
Junction table linking users to companies with roles and status
"""
from sqlalchemy import Column, BigInteger, Boolean, DateTime, String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.common.database import Base


class UserCompany(Base):
    """
    UserCompany junction table for many-to-many user-company relationships.
    
    Tracks:
    - User membership in companies
    - Company-specific roles (owner, admin, manager, member, viewer)
    - Membership status (active, inactive, suspended, removed)
    - How user joined (signup, invitation, import, admin, API)
    - Primary company designation
    - Invitation and removal tracking
    
    Attributes:
        UserCompanyID: Primary key
        UserID: Foreign key to dbo.User
        CompanyID: Foreign key to dbo.Company
        UserCompanyRoleID: Foreign key to ref.UserCompanyRole
        StatusID: Foreign key to ref.UserCompanyStatus
        IsPrimaryCompany: Whether this is user's primary/default company
        JoinedDate: Timestamp when user joined company
        JoinedViaID: Foreign key to ref.JoinedVia (how user joined)
        InvitedBy: Foreign key to dbo.User who sent invitation
        InvitedDate: Timestamp when invitation was sent
        RemovedDate: Timestamp when user was removed from company
        RemovedBy: Foreign key to dbo.User who removed member
        RemovalReason: Reason for removal
    """
    
    __tablename__ = "UserCompany"
    __table_args__ = (
        UniqueConstraint('UserID', 'CompanyID', name='UQ_UserCompany_User_Company'),
        {"schema": "dbo"}
    )
    
    # Primary Key
    UserCompanyID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    UserCompanyRoleID = Column(BigInteger, ForeignKey('ref.UserCompanyRole.UserCompanyRoleID'), nullable=False, index=True)
    StatusID = Column(BigInteger, ForeignKey('ref.UserCompanyStatus.UserCompanyStatusID'), nullable=False, index=True)
    
    # Membership Details
    IsPrimaryCompany = Column(Boolean, nullable=False, default=False, index=True)
    JoinedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    JoinedViaID = Column(BigInteger, ForeignKey('ref.JoinedVia.JoinedViaID'), nullable=False, index=True)
    
    # Invitation Tracking
    InvitedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    InvitedDate = Column(DateTime, nullable=True)
    
    # Removal Tracking
    RemovedDate = Column(DateTime, nullable=True)
    RemovedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    RemovalReason = Column(String(500), nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="companies", foreign_keys=[UserID])
    company = relationship("Company", back_populates="users")
    role = relationship("UserCompanyRole", back_populates="user_companies", foreign_keys=[UserCompanyRoleID])
    status = relationship("UserCompanyStatus", back_populates="user_companies", foreign_keys=[StatusID])
    joined_via = relationship("JoinedVia", back_populates="user_companies", foreign_keys=[JoinedViaID])
    
    inviter = relationship("User", foreign_keys=[InvitedBy])
    remover = relationship("User", foreign_keys=[RemovedBy])
    
    def __repr__(self) -> str:
        return f"<UserCompany(UserCompanyID={self.UserCompanyID}, UserID={self.UserID}, CompanyID={self.CompanyID})>"

