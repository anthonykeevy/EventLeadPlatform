"""
JWT Service Module
Handles JWT token creation, validation, and decoding

Updated for Story 1.13: Token expiry times now read from database (ConfigurationService)
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError  # type: ignore
from sqlalchemy.orm import Session

from config.jwt import (
    get_secret_key,
    get_algorithm,
    get_access_token_expire_minutes,
    get_refresh_token_expire_days
)


def create_access_token(
    db: Session,
    user_id: int,
    email: str,
    role: Optional[str] = None,
    company_id: Optional[int] = None
) -> str:
    """
    Create JWT access token with configurable expiry (default: 15 minutes).
    
    Story 1.13: Expiry time read from database (config.AppSetting: ACCESS_TOKEN_EXPIRY_MINUTES)
    
    Args:
        db: Database session (for ConfigurationService)
        user_id: User ID (becomes 'sub' claim)
        email: User email address
        role: User role from UserCompany (optional)
        company_id: Company ID from UserCompany (optional)
        
    Returns:
        Encoded JWT access token string
        
    Token Payload Structure:
        {
            "sub": <user_id>,
            "email": "<email>",
            "role": "<role>",  # Optional
            "company_id": <company_id>,  # Optional
            "type": "access",
            "exp": <expiration_timestamp>,
            "iat": <issued_at_timestamp>
        }
    """
    now = datetime.utcnow()
    expire = now + timedelta(minutes=get_access_token_expire_minutes(db))
    
    payload: Dict[str, Any] = {
        "sub": user_id,
        "email": email,
        "type": "access",
        "exp": expire,
        "iat": now
    }
    
    # Add optional claims
    if role:
        payload["role"] = role
    if company_id:
        payload["company_id"] = company_id
    
    return jwt.encode(payload, get_secret_key(), algorithm=get_algorithm())


def create_refresh_token(db: Session, user_id: int) -> str:
    """
    Create JWT refresh token with configurable expiry (default: 7 days).
    
    Story 1.13: Expiry time read from database (config.AppSetting: REFRESH_TOKEN_EXPIRY_DAYS)
    
    Args:
        db: Database session (for ConfigurationService)
        user_id: User ID (becomes 'sub' claim)
        
    Returns:
        Encoded JWT refresh token string
        
    Token Payload Structure:
        {
            "sub": <user_id>,
            "type": "refresh",
            "exp": <expiration_timestamp>,
            "iat": <issued_at_timestamp>
        }
    """
    now = datetime.utcnow()
    expire = now + timedelta(days=get_refresh_token_expire_days(db))
    
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire,
        "iat": now
    }
    
    return jwt.encode(payload, get_secret_key(), algorithm=get_algorithm())


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify JWT token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Decoded token payload dictionary
        
    Raises:
        JWTError: If token is invalid, expired, or has invalid signature
        
    Example:
        >>> token = create_access_token(123, "user@example.com")
        >>> payload = decode_token(token)
        >>> print(payload["sub"])  # 123
    """
    try:
        payload = jwt.decode(
            token,
            get_secret_key(),
            algorithms=[get_algorithm()]
        )
        return payload
    except JWTError as e:
        # Re-raise JWT errors for handling by caller
        raise e


def verify_token_type(payload: Dict[str, Any], expected_type: str) -> bool:
    """
    Verify token has the expected type claim.
    
    Args:
        payload: Decoded JWT payload
        expected_type: Expected token type ("access" or "refresh")
        
    Returns:
        True if token type matches, False otherwise
    """
    return payload.get("type") == expected_type


def extract_user_id(payload: Dict[str, Any]) -> int:
    """
    Extract user ID from token payload.
    
    Args:
        payload: Decoded JWT payload
        
    Returns:
        User ID from 'sub' claim
        
    Raises:
        KeyError: If 'sub' claim is missing
    """
    return int(payload["sub"])


def is_token_expired(payload: Dict[str, Any]) -> bool:
    """
    Check if token is expired based on 'exp' claim.
    
    Args:
        payload: Decoded JWT payload
        
    Returns:
        True if token is expired, False otherwise
        
    Note:
        jwt.decode() already validates expiry, but this function
        can be used for manual checking if needed.
    """
    exp = payload.get("exp")
    if not exp:
        return True
    
    return datetime.utcnow().timestamp() > exp

