"""
UserEmailVerificationToken Model (dbo.UserEmailVerificationToken)
Tokens for email verification workflow
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.common.database import Base


class UserEmailVerificationToken(Base):
    """
    Email verification token model.
    
    Workflow:
    1. User signs up with email
    2. Verification token generated and sent via email
    3. User clicks verification link with token
    4. Token validated and marked as used
    5. User's IsEmailVerified flag set to True
    
    Attributes:
        UserEmailVerificationTokenID: Primary key
        UserID: Foreign key to dbo.User
        Token: Secure verification token (URL-safe, cryptographically secure)
        ExpiresAt: Timestamp when token expires (typically 24-48 hours)
        IsUsed: Whether token has been used
        UsedAt: Timestamp when token was used
        CreatedDate: Timestamp when token was created
    """
    
    __tablename__ = "UserEmailVerificationToken"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    UserEmailVerificationTokenID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    
    # Token
    Token = Column(String(500), nullable=False, unique=True, index=True)
    
    # Expiration
    ExpiresAt = Column(DateTime, nullable=False, index=True)
    
    # Usage Tracking
    IsUsed = Column(Boolean, nullable=False, default=False)
    UsedAt = Column(DateTime, nullable=True)
    
    # Audit
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Relationships
    user = relationship("User", back_populates="verification_tokens")
    
    def __repr__(self) -> str:
        return f"<UserEmailVerificationToken(UserID={self.UserID}, IsUsed={self.IsUsed}, ExpiresAt='{self.ExpiresAt}')>"

