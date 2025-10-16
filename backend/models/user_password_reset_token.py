"""
UserPasswordResetToken Model (dbo.UserPasswordResetToken)
Tokens for password reset workflow
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class UserPasswordResetToken(Base):
    """
    Password reset token model.
    
    Workflow:
    1. User requests password reset
    2. Reset token generated and sent via email
    3. User clicks reset link with token
    4. Token validated (not expired, not used)
    5. User sets new password
    6. Token marked as used
    7. User's PasswordHash updated
    
    Security:
    - Tokens expire after short period (15-60 minutes)
    - One-time use only
    - IP address and user agent tracked
    - Failed attempts logged
    
    Attributes:
        UserPasswordResetTokenID: Primary key
        UserID: Foreign key to dbo.User
        Token: Secure reset token (URL-safe, cryptographically secure)
        ExpiresAt: Timestamp when token expires (typically 15-60 minutes)
        IsUsed: Whether token has been used
        UsedAt: Timestamp when token was used
        IPAddress: IP address of requester (security tracking)
        UserAgent: User agent of requester (security tracking)
        CreatedDate: Timestamp when token was created
    """
    
    __tablename__ = "UserPasswordResetToken"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    UserPasswordResetTokenID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    
    # Token
    Token = Column(String(500), nullable=False, unique=True, index=True)
    
    # Expiration
    ExpiresAt = Column(DateTime, nullable=False, index=True)
    
    # Usage Tracking
    IsUsed = Column(Boolean, nullable=False, default=False)
    UsedAt = Column(DateTime, nullable=True)
    
    # Security Tracking
    IPAddress = Column(String(50), nullable=True)
    UserAgent = Column(String(500), nullable=True)
    
    # Audit
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Relationships
    user = relationship("User", back_populates="password_reset_tokens")
    
    def __repr__(self) -> str:
        return f"<UserPasswordResetToken(UserID={self.UserID}, IsUsed={self.IsUsed}, ExpiresAt='{self.ExpiresAt}')>"

