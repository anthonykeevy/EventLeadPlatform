"""
CompanyAudit Model (audit.Company)
Field-level audit trail for Company table changes
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class CompanyAudit(Base):
    """
    Company audit model for field-level change tracking.
    
    Captures detailed changes to Company records for compliance.
    
    Attributes:
        AuditCompanyID: Primary key
        CompanyID: Foreign key to dbo.Company
        FieldName: Name of field that changed (e.g., 'CompanyName', 'ABN')
        OldValue: Previous value (JSON-encoded)
        NewValue: New value (JSON-encoded)
        ChangeType: Type of change (INSERT, UPDATE, DELETE, ABR_SYNC, etc.)
        ChangeReason: Optional reason for change
        ChangedBy: Foreign key to dbo.User who made the change
        ChangedByEmail: Email of user who made change (denormalized)
        IPAddress: IP address of change
        UserAgent: Browser user agent
        CreatedDate: Timestamp when change occurred
        IsDeleted: Soft delete flag
    """
    
    __tablename__ = "Company"
    __table_args__ = {"schema": "audit"}
    
    # Primary Key
    AuditCompanyID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Reference
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    
    # Field Change Details
    FieldName = Column(String(100), nullable=False)
    OldValue = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    NewValue = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    ChangeType = Column(String(50), nullable=False)  # INSERT, UPDATE, DELETE, ABR_SYNC, etc.
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
    company = relationship("Company", foreign_keys=[CompanyID])
    changed_by_user = relationship("User", foreign_keys=[ChangedBy])
    
    def __repr__(self) -> str:
        return f"<CompanyAudit(AuditCompanyID={self.AuditCompanyID}, CompanyID={self.CompanyID}, FieldName='{self.FieldName}', ChangeType='{self.ChangeType}')>"

