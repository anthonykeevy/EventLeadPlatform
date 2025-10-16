"""
Token Service Module
Handles generation and validation of authentication tokens (email verification, password reset, refresh tokens, etc.)
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from models.user_email_verification_token import UserEmailVerificationToken
from models.user_refresh_token import UserRefreshToken
from models.user_password_reset_token import UserPasswordResetToken


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


# ============================================================================
# Password Reset Token Functions
# ============================================================================

def generate_password_reset_token(db: Session, user_id: int, expiry_hours: int = 1) -> str:
    """
    Generate and store password reset token.
    
    Args:
        db: Database session
        user_id: ID of user to generate token for
        expiry_hours: Token expiry time in hours (default 1)
        
    Returns:
        Cryptographically secure token string
        
    Security Notes:
        - Uses secrets.token_urlsafe() for cryptographic randomness
        - 32 bytes = 43 base64 characters
        - Tokens are single-use and expire after 1 hour
        - Invalidates any existing unused password reset tokens
    """
    # Invalidate any existing unused password reset tokens for this user
    invalidate_user_password_reset_tokens(db, user_id)
    
    # Generate cryptographically secure token (32 bytes = 43 URL-safe chars)
    token_value = secrets.token_urlsafe(32)
    
    # Calculate expiry time (1 hour for security)
    expires_at = datetime.utcnow() + timedelta(hours=expiry_hours)
    
    # Create token record
    token = UserPasswordResetToken(
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


def validate_password_reset_token(
    db: Session, 
    token_value: str
) -> Optional[UserPasswordResetToken]:
    """
    Validate password reset token and return token record if valid.
    
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
    token = db.query(UserPasswordResetToken).filter(
        UserPasswordResetToken.Token == token_value
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


def mark_password_reset_token_used(db: Session, token: UserPasswordResetToken) -> None:
    """
    Mark password reset token as used to prevent reuse.
    
    Args:
        db: Database session
        token: Token record to mark as used
    """
    token.IsUsed = True
    token.UsedAt = datetime.utcnow()
    db.commit()


def invalidate_user_password_reset_tokens(
    db: Session, 
    user_id: int
) -> int:
    """
    Invalidate all password reset tokens for a user.
    
    This is called when:
    - A new password reset token is generated (invalidate old ones)
    - Password is successfully reset (invalidate remaining tokens)
    
    Args:
        db: Database session
        user_id: User ID to invalidate tokens for
        
    Returns:
        Number of tokens invalidated
    """
    tokens = db.query(UserPasswordResetToken).filter(
        UserPasswordResetToken.UserID == user_id,
        UserPasswordResetToken.IsUsed == False,
        UserPasswordResetToken.ExpiresAt > datetime.utcnow()
    ).all()
    
    for token in tokens:
        token.IsUsed = True
        token.UsedAt = datetime.utcnow()
    
    db.commit()
    
    return len(tokens)


# ============================================================================
# Refresh Token Functions
# ============================================================================

def store_refresh_token(
    db: Session,
    user_id: int,
    token_value: str,
    expiry_days: int = 7
) -> UserRefreshToken:
    """
    Store JWT refresh token in database.
    
    Args:
        db: Database session
        user_id: ID of user the token belongs to
        token_value: JWT refresh token string
        expiry_days: Token expiry time in days (default 7)
        
    Returns:
        Created UserRefreshToken record
    """
    expires_at = datetime.utcnow() + timedelta(days=expiry_days)
    
    token = UserRefreshToken(
        UserID=user_id,
        Token=token_value,
        ExpiresAt=expires_at,
        IsUsed=False,
        IsRevoked=False,
        CreatedDate=datetime.utcnow()
    )
    
    db.add(token)
    db.commit()
    db.refresh(token)
    
    return token


def validate_refresh_token(
    db: Session,
    token_value: str
) -> Optional[UserRefreshToken]:
    """
    Validate refresh token and return token record if valid.
    
    Args:
        db: Database session
        token_value: JWT refresh token string to validate
        
    Returns:
        Token record if valid, None otherwise
        
    Validation Rules:
        - Token must exist in database
        - Token must not be expired (ExpiresAt > now)
        - Token must not be used (IsUsed = false)
        - Token must not be revoked (IsRevoked = false)
    """
    token = db.query(UserRefreshToken).filter(
        UserRefreshToken.Token == token_value
    ).first()
    
    if not token:
        return None
    
    # Check expiry
    if token.ExpiresAt < datetime.utcnow():
        return None
    
    # Check if already used
    if token.IsUsed:
        return None
    
    # Check if revoked
    if token.IsRevoked:
        return None
    
    return token


def mark_refresh_token_used(
    db: Session,
    token: UserRefreshToken
) -> None:
    """
    Mark refresh token as used (for one-time use policy).
    
    Args:
        db: Database session
        token: Token record to mark as used
    """
    token.IsUsed = True
    token.UsedAt = datetime.utcnow()
    db.commit()


def revoke_refresh_token(
    db: Session,
    token: UserRefreshToken
) -> None:
    """
    Manually revoke a refresh token (for security - e.g., logout).
    
    Args:
        db: Database session
        token: Token record to revoke
    """
    token.IsRevoked = True
    token.RevokedAt = datetime.utcnow()
    db.commit()


def revoke_all_user_refresh_tokens(
    db: Session,
    user_id: int
) -> int:
    """
    Revoke all active refresh tokens for a user.
    Useful for "logout from all devices" functionality.
    
    Args:
        db: Database session
        user_id: User ID to revoke tokens for
        
    Returns:
        Number of tokens revoked
    """
    tokens = db.query(UserRefreshToken).filter(
        UserRefreshToken.UserID == user_id,
        UserRefreshToken.IsRevoked == False,
        UserRefreshToken.ExpiresAt > datetime.utcnow()
    ).all()
    
    now = datetime.utcnow()
    for token in tokens:
        token.IsRevoked = True
        token.RevokedAt = now
    
    db.commit()
    
    return len(tokens)

