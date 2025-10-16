"""
JWT Configuration Module
Loads JWT settings from environment variables
"""
import os
from typing import Optional


class JWTConfig:
    """JWT configuration settings"""
    
    def __init__(self) -> None:
        # Load JWT secret (CRITICAL: Must be set in production)
        self.SECRET_KEY: str = os.getenv(
            "JWT_SECRET_KEY",
            "dev-secret-key-change-in-production-min-32-chars"
        ) or "dev-secret-key-change-in-production-min-32-chars"
        
        # Validate secret key length
        if len(self.SECRET_KEY) < 32:
            raise ValueError(
                "JWT_SECRET_KEY must be at least 32 characters long for security. "
                "Generate a secure key: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        
        # JWT algorithm
        self.ALGORITHM: str = os.getenv("JWT_ALGORITHM") or "HS256"
        
        # Token expiry settings
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("JWT_EXPIRATION_MINUTES") or "60"
        )
        self.REFRESH_TOKEN_EXPIRE_DAYS: int = int(
            os.getenv("REFRESH_TOKEN_EXPIRE_DAYS") or "7"
        )
    
    def validate(self) -> None:
        """Validate JWT configuration"""
        if not self.SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY environment variable is required")
        
        if self.SECRET_KEY == "dev-secret-key-change-in-production-min-32-chars":
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                "⚠️  WARNING: Using default JWT secret key. "
                "This is INSECURE for production! "
                "Set JWT_SECRET_KEY environment variable."
            )


# Global JWT configuration instance
_jwt_config: Optional[JWTConfig] = None


def get_jwt_config() -> JWTConfig:
    """
    Get JWT configuration singleton.
    Initializes on first call.
    """
    global _jwt_config
    if _jwt_config is None:
        _jwt_config = JWTConfig()
        _jwt_config.validate()
    return _jwt_config


# Convenience exports
def get_secret_key() -> str:
    return get_jwt_config().SECRET_KEY


def get_algorithm() -> str:
    return get_jwt_config().ALGORITHM


def get_access_token_expire_minutes() -> int:
    return get_jwt_config().ACCESS_TOKEN_EXPIRE_MINUTES


def get_refresh_token_expire_days() -> int:
    return get_jwt_config().REFRESH_TOKEN_EXPIRE_DAYS

