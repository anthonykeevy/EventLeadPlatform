"""
UserCompanyRole Reference Model (ref.UserCompanyRole)
Company-level roles for team members
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class UserCompanyRole(Base):
    """
    User company role reference table for company-level permissions.
    
    Company roles: owner, admin, manager, member, viewer
    
    Attributes:
        UserCompanyRoleID: Primary key
        RoleCode: Unique role code (e.g., 'owner', 'admin', 'member')
        RoleName: Display name (e.g., 'Owner', 'Administrator', 'Member')
        Description: Full description of role permissions
        RoleLevel: Numeric hierarchy level (higher = more permissions)
        CanManageCompany: Can edit company settings
        CanManageUsers: Can invite/remove team members
        CanManageEvents: Can create and edit events
        CanManageForms: Can create and edit forms
        CanExportData: Can export lead data
        CanViewReports: Can view analytics and reports
        IsActive: Whether this role is available for assignment
        SortOrder: Display order
    """
    
    __tablename__ = "UserCompanyRole"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    UserCompanyRoleID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    RoleCode = Column(String(50), nullable=False, unique=True, index=True)
    RoleName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=False)
    RoleLevel = Column(Integer, nullable=False)
    
    # Permissions
    CanManageCompany = Column(Boolean, nullable=False, default=False)
    CanManageUsers = Column(Boolean, nullable=False, default=False)
    CanManageEvents = Column(Boolean, nullable=False, default=False)
    CanManageForms = Column(Boolean, nullable=False, default=False)
    CanExportData = Column(Boolean, nullable=False, default=False)
    CanViewReports = Column(Boolean, nullable=False, default=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    user_companies = relationship("UserCompany", back_populates="role", foreign_keys="[UserCompany.UserCompanyRoleID]")
    invitations = relationship("UserInvitation", back_populates="role", foreign_keys="[UserInvitation.UserCompanyRoleID]")
    
    def __repr__(self) -> str:
        return f"<UserCompanyRole(UserCompanyRoleID={self.UserCompanyRoleID}, RoleCode='{self.RoleCode}', RoleName='{self.RoleName}')>"

