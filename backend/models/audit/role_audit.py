"""
RoleAudit Model (audit.Role)
Audit trail for role changes (system and company roles)
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class RoleAudit(Base):
    """
    Role audit model for role assignment/change tracking.
    
    Tracks both system-level (UserRole) and company-level (UserCompanyRole) role changes.
    
    Attributes:
        AuditRoleID: Primary key
        TableName: Table where change occurred ('UserRole' or 'UserCompanyRole')
        RecordID: ID of record that changed
        ColumnName: Column that changed (typically 'RoleID')
        RoleType: Type of role ('system' or 'company')
        UserCompanyID: Foreign key to dbo.UserCompany (for company roles)
        UserID: Foreign key to dbo.User
        CompanyID: Foreign key to dbo.Company (for company roles)
        OldRoleID: Previous role ID
        NewRoleID: New role ID
        OldRoleName: Previous role name (denormalized)
        NewRoleName: New role name (denormalized)
        ChangeReason: Reason for role change
        ChangedBy: Foreign key to dbo.User who made the change
        ChangedByEmail: Email of user who made change (denormalized)
        IPAddress: IP address of change
        UserAgent: Browser user agent
        CreatedDate: Timestamp when change occurred
        IsDeleted: Soft delete flag
    """
    
    __tablename__ = "Role"
    __table_args__ = {"schema": "audit"}
    
    # Primary Key
    AuditRoleID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Change Metadata
    TableName = Column(String(50), nullable=False)
    RecordID = Column(BigInteger, nullable=False)
    ColumnName = Column(String(50), nullable=False)
    RoleType = Column(String(50), nullable=False, index=True)  # 'system' or 'company'
    
    # References
    UserCompanyID = Column(BigInteger, ForeignKey('dbo.UserCompany.UserCompanyID'), nullable=True, index=True)
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True, index=True)
    
    # Role Change Details
    OldRoleID = Column(BigInteger, nullable=True)
    NewRoleID = Column(BigInteger, nullable=True)
    OldRoleName = Column(String(100), nullable=True)
    NewRoleName = Column(String(100), nullable=True)
    ChangeReason = Column(String(500), nullable=True)
    
    # Change Context
    ChangedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    ChangedByEmail = Column(String(255), nullable=True)
    IPAddress = Column(String(50), nullable=True)
    UserAgent = Column(String(500), nullable=True)
    
    # Timestamp
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    
    # Relationships
    user_company = relationship("UserCompany", foreign_keys=[UserCompanyID])
    user = relationship("User", foreign_keys=[UserID])
    company = relationship("Company", foreign_keys=[CompanyID])
    changed_by_user = relationship("User", foreign_keys=[ChangedBy])
    
    def __repr__(self) -> str:
        return f"<RoleAudit(AuditRoleID={self.AuditRoleID}, UserID={self.UserID}, RoleType='{self.RoleType}', OldRoleName='{self.OldRoleName}', NewRoleName='{self.NewRoleName}')>"

