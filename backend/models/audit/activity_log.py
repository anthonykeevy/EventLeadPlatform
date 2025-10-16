"""
ActivityLog Model (audit.ActivityLog)
General activity log for audit compliance
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class ActivityLog(Base):
    """
    Activity log model for compliance audit trail.
    
    Captures all significant user actions for compliance and security auditing.
    
    Attributes:
        ActivityLogID: Primary key
        UserID: Foreign key to dbo.User (nullable for system actions)
        UserEmail: Email address of user (denormalized for historical record)
        Action: Action performed (e.g., 'login', 'create_event', 'delete_lead')
        EntityType: Type of entity affected (e.g., 'User', 'Event', 'Lead')
        EntityID: ID of affected entity
        CompanyID: Foreign key to dbo.Company (nullable for system actions)
        OldValue: JSON snapshot of entity before change
        NewValue: JSON snapshot of entity after change
        IPAddress: IP address of user
        UserAgent: Browser user agent string
        RequestID: Unique request ID for correlation
        CreatedDate: Timestamp when action occurred
    """
    
    __tablename__ = "ActivityLog"
    __table_args__ = {"schema": "audit"}
    
    # Primary Key
    ActivityLogID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # User Context
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True, index=True)
    UserEmail = Column(String(255), nullable=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True, index=True)
    
    # Action Details
    Action = Column(String(100), nullable=False, index=True)
    EntityType = Column(String(50), nullable=False)
    EntityID = Column(BigInteger, nullable=True)
    
    # Change Tracking
    OldValue = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    NewValue = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    
    # Security Context
    IPAddress = Column(String(50), nullable=True)
    UserAgent = Column(String(500), nullable=True)
    RequestID = Column(String(100), nullable=True)
    
    # Timestamp
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="activity_logs", foreign_keys=[UserID])
    company = relationship("Company", back_populates="activity_logs")
    
    def __repr__(self) -> str:
        return f"<ActivityLog(ActivityLogID={self.ActivityLogID}, Action='{self.Action}', EntityType='{self.EntityType}', UserID={self.UserID})>"

