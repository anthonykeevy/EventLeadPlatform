"""
JWT Configuration Module
Loads JWT settings from environment variables (.env) and database (ConfigurationService)

Configuration Distribution (Story 1.13):
- .env: Infrastructure & secrets (SECRET_KEY, ALGORITHM)
- Database: Business rules (token expiry times)
"""
import os
from typing import Optional
from sqlalchemy.orm import Session


class JWTConfig:
    """JWT configuration settings"""
    
    def __init__(self) -> None:
        # Load JWT secret (CRITICAL: Must be set in production)
        # Infrastructure config: stays in .env
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
        
        # JWT algorithm: stays in .env (infrastructure)
        self.ALGORITHM: str = os.getenv("JWT_ALGORITHM") or "HS256"
    
    def get_access_token_expire_minutes(self, db: Session) -> int:
        """
        Get JWT access token expiry from database (ConfigurationService).
        Falls back to code default if database unavailable.
        
        Args:
            db: Database session
            
        Returns:
            Access token expiry in minutes (default: 15)
        """
        try:
            from common.config_service import ConfigurationService
            config = ConfigurationService(db)
            return config.get_jwt_access_expiry_minutes()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error loading JWT access expiry from database: {e}, using default")
            from common.constants import DEFAULT_JWT_ACCESS_EXPIRY_MINUTES
            return DEFAULT_JWT_ACCESS_EXPIRY_MINUTES
    
    def get_refresh_token_expire_days(self, db: Session) -> int:
        """
        Get JWT refresh token expiry from database (ConfigurationService).
        Falls back to code default if database unavailable.
        
        Args:
            db: Database session
            
        Returns:
            Refresh token expiry in days (default: 7)
        """
        try:
            from common.config_service import ConfigurationService
            config = ConfigurationService(db)
            return config.get_jwt_refresh_expiry_days()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error loading JWT refresh expiry from database: {e}, using default")
            from common.constants import DEFAULT_JWT_REFRESH_EXPIRY_DAYS
            return DEFAULT_JWT_REFRESH_EXPIRY_DAYS
    
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
    """Get JWT secret key from environment (.env)"""
    return get_jwt_config().SECRET_KEY


def get_algorithm() -> str:
    """Get JWT algorithm from environment (.env)"""
    return get_jwt_config().ALGORITHM


def get_access_token_expire_minutes(db: Session) -> int:
    """
    Get JWT access token expiry from database (ConfigurationService).
    
    Args:
        db: Database session
        
    Returns:
        Access token expiry in minutes (default: 15)
    """
    return get_jwt_config().get_access_token_expire_minutes(db)


def get_refresh_token_expire_days(db: Session) -> int:
    """
    Get JWT refresh token expiry from database (ConfigurationService).
    
    Args:
        db: Database session
        
    Returns:
        Refresh token expiry in days (default: 7)
    """
    return get_jwt_config().get_refresh_token_expire_days(db)

