"""
UserRefreshToken Model (dbo.UserRefreshToken)
Tokens for JWT refresh token workflow
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class UserRefreshToken(Base):
    """
    Refresh token model for JWT authentication.
    
    Workflow:
    1. User logs in successfully
    2. Refresh token generated and stored
    3. Access token expires after 1 hour
    4. Client uses refresh token to get new access token
    5. Refresh token marked as used (optional: one-time use policy)
    
    Attributes:
        UserRefreshTokenID: Primary key
        UserID: Foreign key to dbo.User
        Token: JWT refresh token string
        ExpiresAt: Timestamp when token expires (typically 7 days)
        IsUsed: Whether token has been used (for one-time use policy)
        UsedAt: Timestamp when token was used
        CreatedDate: Timestamp when token was created
        RevokedAt: Timestamp when token was manually revoked
        IsRevoked: Whether token has been manually revoked
    """
    
    __tablename__ = "UserRefreshToken"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    UserRefreshTokenID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    
    # Token
    Token = Column(String(500), nullable=False, unique=True, index=True)
    
    # Expiration
    ExpiresAt = Column(DateTime, nullable=False, index=True)
    
    # Usage Tracking
    IsUsed = Column(Boolean, nullable=False, default=False)
    UsedAt = Column(DateTime, nullable=True)
    
    # Revocation (for security - can manually revoke tokens)
    IsRevoked = Column(Boolean, nullable=False, default=False)
    RevokedAt = Column(DateTime, nullable=True)
    
    # Audit
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self) -> str:
        return f"<UserRefreshToken(UserID={self.UserID}, IsUsed={self.IsUsed}, IsRevoked={self.IsRevoked}, ExpiresAt='{self.ExpiresAt}')>"


