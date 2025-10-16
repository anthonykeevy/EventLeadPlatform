"""
UserRole Reference Model (ref.UserRole)
System-level roles for platform administration
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class UserRole(Base):
    """
    User role reference table for platform-level permissions.
    
    System roles: superadmin, admin, support, user
    
    Attributes:
        UserRoleID: Primary key
        RoleCode: Unique role code (e.g., 'superadmin', 'admin', 'user')
        RoleName: Display name (e.g., 'Super Administrator', 'User')
        Description: Full description of role permissions
        RoleLevel: Numeric hierarchy level (higher = more permissions)
        CanManagePlatform: Can manage platform-wide settings
        CanManageAllCompanies: Can view and manage all companies
        CanViewAllData: Can view all data across platform
        CanAssignSystemRoles: Can assign system-level roles
        IsActive: Whether this role is available for assignment
        SortOrder: Display order
    """
    
    __tablename__ = "UserRole"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    UserRoleID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    RoleCode = Column(String(50), nullable=False, unique=True, index=True)
    RoleName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=False)
    RoleLevel = Column(Integer, nullable=False)
    
    # Permissions
    CanManagePlatform = Column(Boolean, nullable=False, default=False)
    CanManageAllCompanies = Column(Boolean, nullable=False, default=False)
    CanViewAllData = Column(Boolean, nullable=False, default=False)
    CanAssignSystemRoles = Column(Boolean, nullable=False, default=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="user_role", foreign_keys="[User.UserRoleID]")
    
    def __repr__(self) -> str:
        return f"<UserRole(UserRoleID={self.UserRoleID}, RoleCode='{self.RoleCode}', RoleName='{self.RoleName}')>"

