"""
UserAudit Model (audit.User)
Field-level audit trail for User table changes
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class UserAudit(Base):
    """
    User audit model for field-level change tracking.
    
    Captures detailed changes to User records for compliance.
    
    Attributes:
        AuditUserID: Primary key
        UserID: Foreign key to dbo.User
        FieldName: Name of field that changed (e.g., 'Email', 'StatusID')
        OldValue: Previous value (JSON-encoded)
        NewValue: New value (JSON-encoded)
        ChangeType: Type of change (INSERT, UPDATE, DELETE, STATUS_CHANGE, etc.)
        ChangeReason: Optional reason for change
        ChangedBy: Foreign key to dbo.User who made the change
        ChangedByEmail: Email of user who made change (denormalized)
        IPAddress: IP address of change
        UserAgent: Browser user agent
        CreatedDate: Timestamp when change occurred
        IsDeleted: Soft delete flag
    """
    
    __tablename__ = "User"
    __table_args__ = {"schema": "audit"}
    
    # Primary Key
    AuditUserID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Reference
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    
    # Field Change Details
    FieldName = Column(String(100), nullable=False, index=True)
    OldValue = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    NewValue = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    ChangeType = Column(String(50), nullable=False)  # INSERT, UPDATE, DELETE, STATUS_CHANGE, etc.
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
    user = relationship("User", foreign_keys=[UserID])
    changed_by_user = relationship("User", foreign_keys=[ChangedBy])
    
    def __repr__(self) -> str:
        return f"<UserAudit(AuditUserID={self.AuditUserID}, UserID={self.UserID}, FieldName='{self.FieldName}', ChangeType='{self.ChangeType}')>"

