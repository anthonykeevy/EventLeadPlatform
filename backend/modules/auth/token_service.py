"""
Token Service Module
Handles generation and validation of authentication tokens (email verification, password reset, etc.)
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from models.user_email_verification_token import UserEmailVerificationToken


def generate_verification_token(db: Session, user_id: int, expiry_hours: int = 24) -> str:
    """
    Generate and store email verification token.
    
    Args:
        db: Database session
        user_id: ID of user to generate token for
        expiry_hours: Token expiry time in hours (default 24)
        
    Returns:
        Cryptographically secure token string
        
    Security Notes:
        - Uses secrets.token_urlsafe() for cryptographic randomness
        - 32 bytes = 43 base64 characters
        - Tokens are single-use and have expiration
    """
    # Generate cryptographically secure token (32 bytes = 43 URL-safe chars)
    token_value = secrets.token_urlsafe(32)
    
    # Calculate expiry time
    expires_at = datetime.utcnow() + timedelta(hours=expiry_hours)
    
    # Create token record
    token = UserEmailVerificationToken(
        UserID=user_id,
        Token=token_value,
        ExpiresAt=expires_at,
        IsUsed=False,
        CreatedDate=datetime.utcnow()
    )
    
    db.add(token)
    db.commit()
    db.refresh(token)
    
    return token_value


def validate_token(
    db: Session, 
    token_value: str
) -> Optional[UserEmailVerificationToken]:
    """
    Validate email verification token and return token record if valid.
    
    Args:
        db: Database session
        token_value: Token string to validate
        
    Returns:
        Token record if valid, None otherwise
        
    Validation Rules:
        - Token must exist in database
        - Token must not be expired (ExpiresAt > now)
        - Token must not be used (IsUsed = false)
    """
    # Find token
    token = db.query(UserEmailVerificationToken).filter(
        UserEmailVerificationToken.Token == token_value
    ).first()
    
    if not token:
        return None
    
    # Check expiry
    if token.ExpiresAt < datetime.utcnow():
        return None
    
    # Check if already used
    if token.IsUsed:
        return None
    
    return token


def mark_token_used(db: Session, token: UserEmailVerificationToken) -> None:
    """
    Mark token as used to prevent reuse.
    
    Args:
        db: Database session
        token: Token record to mark as used
    """
    token.IsUsed = True
    token.UsedAt = datetime.utcnow()
    db.commit()


def invalidate_user_verification_tokens(
    db: Session, 
    user_id: int
) -> int:
    """
    Invalidate all email verification tokens for a user.
    
    Args:
        db: Database session
        user_id: User ID to invalidate tokens for
        
    Returns:
        Number of tokens invalidated
    """
    tokens = db.query(UserEmailVerificationToken).filter(
        UserEmailVerificationToken.UserID == user_id,
        UserEmailVerificationToken.IsUsed == False,
        UserEmailVerificationToken.ExpiresAt > datetime.utcnow()
    ).all()
    
    for token in tokens:
        token.IsUsed = True
        token.UsedAt = datetime.utcnow()
    
    db.commit()
    
    return len(tokens)

