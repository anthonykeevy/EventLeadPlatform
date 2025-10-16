"""
AuthEvent Model (log.AuthEvent)
Authentication and authorization event logging
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class AuthEvent(Base):
    """
    Authentication event log model.
    
    Captures all authentication-related events for security monitoring.
    Events: login_success, login_failure, logout, password_reset, email_verification, etc.
    
    Attributes:
        AuthEventID: Primary key
        EventType: Type of auth event (login_success, login_failure, logout, etc.)
        UserID: Foreign key to dbo.User (nullable for failed login attempts)
        Email: Email address used in auth attempt (for failed logins)
        Reason: Reason for event (e.g., 'invalid_password', 'account_locked')
        IPAddress: Client IP address
        UserAgent: Browser user agent string
        RequestID: Unique request ID (correlation ID)
        CreatedDate: Timestamp when event occurred
    """
    
    __tablename__ = "AuthEvent"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    AuthEventID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Event Details
    EventType = Column(String(50), nullable=False, index=True)
    Reason = Column(String(255), nullable=True)
    
    # User Context
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True, index=True)
    Email = Column(String(255), nullable=True, index=True)
    
    # Security Context
    IPAddress = Column(String(50), nullable=True)
    UserAgent = Column(String(500), nullable=True)
    RequestID = Column(String(100), nullable=True)
    
    # Timestamp
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="auth_events")
    
    def __repr__(self) -> str:
        return f"<AuthEvent(AuthEventID={self.AuthEventID}, EventType='{self.EventType}', Email='{self.Email}', Reason='{self.Reason}')>"

