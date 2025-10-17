"""
Configuration Service
Centralized configuration management with database-backed settings and code fallbacks

Story: 1.13 - Configuration Service Implementation
Design: Simplified (AppSetting table) vs Tech Spec (3-table hierarchy)
"""
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
import json
import logging

from backend.models.config.app_setting import AppSetting
from backend.models.ref import SettingCategory, SettingType
from backend.common.constants import (
    DEFAULT_JWT_ACCESS_EXPIRY_MINUTES,
    DEFAULT_JWT_REFRESH_EXPIRY_DAYS,
    DEFAULT_PASSWORD_MIN_LENGTH,
    DEFAULT_PASSWORD_REQUIRE_UPPERCASE,
    DEFAULT_PASSWORD_REQUIRE_NUMBER,
    DEFAULT_PASSWORD_EXPIRY_DAYS,
    DEFAULT_MAX_FAILED_LOGIN_ATTEMPTS,
    DEFAULT_ACCOUNT_LOCKOUT_MINUTES,
    DEFAULT_SESSION_TIMEOUT_MINUTES,
    DEFAULT_EMAIL_VERIFICATION_EXPIRY_HOURS,
    DEFAULT_PASSWORD_RESET_EXPIRY_HOURS,
    DEFAULT_INVITATION_EXPIRY_DAYS,
)

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of a configuration value validation"""
    
    def __init__(self, is_valid: bool, error_message: Optional[str] = None):
        self.is_valid = is_valid
        self.error_message = error_message


class ConfigurationService:
    """
    Centralized configuration service for Epic 1.
    
    Features:
    - Retrieves settings from database (config.AppSetting)
    - Falls back to code defaults if setting missing or DB unavailable
    - In-memory caching with 5-minute TTL
    - Type conversion based on SettingType
    - Convenience methods for Epic 1 settings
    
    Usage:
        config = ConfigurationService(db)
        jwt_expiry = config.get_jwt_access_expiry_minutes()
        
    Configuration Distribution:
    - .env: Infrastructure & secrets (DATABASE_URL, JWT_SECRET, EMAIL_API_KEY)
    - Database (AppSetting): Business rules (JWT expiry, password length, token expiry)
    - Code (constants.py): Static logic & default fallbacks
    """
    
    def __init__(self, db: Session):
        """
        Initialize configuration service.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self._cache: Dict[str, Any] = {}
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl_seconds = 300  # 5 minutes
        
    
    def get_setting(
        self, 
        setting_key: str, 
        default: Any = None,
        category_code: Optional[str] = None
    ) -> Any:
        """
        Get application setting value with type conversion.
        
        Resolution order:
        1. Check in-memory cache (if valid)
        2. Query database (config.AppSetting)
        3. Fall back to provided default
        4. Fall back to None
        
        Args:
            setting_key: Setting key (e.g., 'ACCESS_TOKEN_EXPIRY_MINUTES')
            default: Fallback value if setting not found
            category_code: Optional category filter for faster lookup
            
        Returns:
            Setting value (type-converted) or default
            
        Example:
            >>> config = ConfigurationService(db)
            >>> expiry = config.get_setting('ACCESS_TOKEN_EXPIRY_MINUTES', 15)
            >>> # Returns: 15 (from database or default)
        """
        # Check cache first (with TTL validation)
        if self._is_cache_valid() and setting_key in self._cache:
            logger.debug(f"Cache hit: {setting_key}")
            return self._cache[setting_key]
        
        try:
            # Query database for setting
            query = self.db.query(AppSetting).filter(
                and_(
                    AppSetting.SettingKey == setting_key,
                    AppSetting.IsActive == True,
                    AppSetting.IsDeleted == False
                )
            )
            
            # Optional category filter (optimization)
            if category_code:
                query = query.join(SettingCategory).filter(
                    SettingCategory.CategoryCode == category_code
                )
            
            setting = query.first()
            
            if setting:
                # Type conversion based on SettingType
                value = self._convert_value(setting.SettingValue, setting.setting_type.TypeCode)
                
                # Cache the converted value
                self._cache[setting_key] = value
                self._update_cache_timestamp()
                
                logger.debug(f"Database hit: {setting_key} = {value}")
                return value
            else:
                # Setting not found - fall back to default
                logger.warning(f"Setting not found: {setting_key}, using default: {default}")
                return default
                
        except Exception as e:
            # Database error - fall back to default
            logger.error(f"Error retrieving setting {setting_key}: {e}, using default: {default}")
            return default
    
    
    def _convert_value(self, value: str, setting_type_code: str) -> Any:
        """
        Convert string value to appropriate type based on SettingType.
        
        Args:
            value: String value from database
            setting_type_code: Type code ('integer', 'boolean', 'string', 'json', 'decimal')
            
        Returns:
            Type-converted value or None on error
        """
        try:
            if setting_type_code == 'integer':
                return int(value)
            elif setting_type_code == 'boolean':
                return value.lower() in ('true', '1', 'yes')
            elif setting_type_code == 'decimal':
                return float(value)
            elif setting_type_code == 'json':
                return json.loads(value)
            else:  # 'string'
                return value
        except Exception as e:
            logger.error(f"Error converting value '{value}' to type '{setting_type_code}': {e}")
            return None
    
    
    def _is_cache_valid(self) -> bool:
        """
        Check if cache is still valid (within TTL).
        
        Returns:
            True if cache is valid, False otherwise
        """
        if self._cache_timestamp is None:
            return False
        
        elapsed = (datetime.utcnow() - self._cache_timestamp).total_seconds()
        return elapsed < self._cache_ttl_seconds
    
    
    def _update_cache_timestamp(self):
        """Update cache timestamp to current time."""
        self._cache_timestamp = datetime.utcnow()
    
    
    def invalidate_cache(self):
        """
        Invalidate in-memory cache (force refresh on next get_setting call).
        
        Use when settings are updated via admin endpoints.
        """
        self._cache.clear()
        self._cache_timestamp = None
        logger.info("Configuration cache invalidated")
    
    
    # ========================================================================
    # CONVENIENCE METHODS FOR EPIC 1 SETTINGS
    # ========================================================================
    
    def get_jwt_access_expiry_minutes(self) -> int:
        """
        Get JWT access token expiry in minutes.
        
        Returns:
            Access token lifetime in minutes (default: 15)
        """
        return self.get_setting(
            'ACCESS_TOKEN_EXPIRY_MINUTES',
            DEFAULT_JWT_ACCESS_EXPIRY_MINUTES,
            'authentication'
        )
    
    
    def get_jwt_refresh_expiry_days(self) -> int:
        """
        Get JWT refresh token expiry in days.
        
        Returns:
            Refresh token lifetime in days (default: 7)
        """
        return self.get_setting(
            'REFRESH_TOKEN_EXPIRY_DAYS',
            DEFAULT_JWT_REFRESH_EXPIRY_DAYS,
            'authentication'
        )
    
    
    def get_password_min_length(self) -> int:
        """
        Get minimum password length.
        
        Returns:
            Minimum password length in characters (default: 8)
        """
        return self.get_setting(
            'PASSWORD_MIN_LENGTH',
            DEFAULT_PASSWORD_MIN_LENGTH,
            'authentication'
        )
    
    
    def get_password_require_uppercase(self) -> bool:
        """
        Get whether password requires uppercase letter.
        
        Returns:
            True if uppercase required, False otherwise (default: False)
        """
        return self.get_setting(
            'PASSWORD_REQUIRE_UPPERCASE',
            DEFAULT_PASSWORD_REQUIRE_UPPERCASE,
            'authentication'
        )
    
    
    def get_password_require_number(self) -> bool:
        """
        Get whether password requires number.
        
        Returns:
            True if number required, False otherwise (default: True)
        """
        return self.get_setting(
            'PASSWORD_REQUIRE_NUMBER',
            DEFAULT_PASSWORD_REQUIRE_NUMBER,
            'authentication'
        )
    
    
    def get_password_expiry_days(self) -> int:
        """
        Get password expiry in days (0 = never expires).
        
        Returns:
            Password expiry in days (default: 90)
        """
        return self.get_setting(
            'PASSWORD_EXPIRY_DAYS',
            DEFAULT_PASSWORD_EXPIRY_DAYS,
            'authentication'
        )
    
    
    def get_max_failed_login_attempts(self) -> int:
        """
        Get maximum failed login attempts before account lockout.
        
        Returns:
            Maximum failed login attempts (default: 5)
        """
        return self.get_setting(
            'MAX_LOGIN_ATTEMPTS',
            DEFAULT_MAX_FAILED_LOGIN_ATTEMPTS,
            'security'
        )
    
    
    def get_account_lockout_minutes(self) -> int:
        """
        Get account lockout duration in minutes.
        
        Returns:
            Lockout duration in minutes (default: 15)
        """
        return self.get_setting(
            'ACCOUNT_LOCKOUT_MINUTES',
            DEFAULT_ACCOUNT_LOCKOUT_MINUTES,
            'security'
        )
    
    
    def get_session_timeout_minutes(self) -> int:
        """
        Get session timeout in minutes.
        
        Returns:
            Session timeout in minutes (default: 30)
        """
        return self.get_setting(
            'SESSION_TIMEOUT_MINUTES',
            DEFAULT_SESSION_TIMEOUT_MINUTES,
            'security'
        )
    
    
    def get_email_verification_expiry_hours(self) -> int:
        """
        Get email verification token expiry in hours.
        
        Returns:
            Email verification token lifetime in hours (default: 24)
        """
        return self.get_setting(
            'EMAIL_VERIFICATION_EXPIRY_HOURS',
            DEFAULT_EMAIL_VERIFICATION_EXPIRY_HOURS,
            'authentication'
        )
    
    
    def get_password_reset_expiry_hours(self) -> int:
        """
        Get password reset token expiry in hours.
        
        Returns:
            Password reset token lifetime in hours (default: 1)
        """
        return self.get_setting(
            'PASSWORD_RESET_EXPIRY_HOURS',
            DEFAULT_PASSWORD_RESET_EXPIRY_HOURS,
            'authentication'
        )
    
    
    def get_invitation_expiry_days(self) -> int:
        """
        Get team invitation expiry in days.
        
        Returns:
            Team invitation lifetime in days (default: 7)
        """
        return self.get_setting(
            'INVITATION_EXPIRY_DAYS',
            DEFAULT_INVITATION_EXPIRY_DAYS,
            'authentication'
        )
    
    
    # ========================================================================
    # ADMIN METHODS (Story 1.13 Task 9)
    # ========================================================================
    
    def update_setting(
        self, 
        setting_key: str, 
        new_value: str,
        updated_by: Optional[int] = None
    ) -> bool:
        """
        Update application setting value (admin only).
        
        Args:
            setting_key: Setting key to update
            new_value: New value (as string, will be type-converted)
            updated_by: User ID making the change
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            setting = self.db.query(AppSetting).filter(
                and_(
                    AppSetting.SettingKey == setting_key,
                    AppSetting.IsDeleted == False
                )
            ).first()
            
            if not setting:
                logger.error(f"Setting not found: {setting_key}")
                return False
            
            # Validate new value against SettingType
            validation = self._validate_setting_value(new_value, setting.setting_type.TypeCode)
            if not validation.is_valid:
                logger.error(f"Invalid value for {setting_key}: {validation.error_message}")
                return False
            
            # Update setting
            setting.SettingValue = new_value
            setting.UpdatedDate = datetime.utcnow()
            setting.UpdatedBy = updated_by
            
            self.db.commit()
            
            # Invalidate cache
            self.invalidate_cache()
            
            logger.info(f"Setting updated: {setting_key} = {new_value} by user {updated_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating setting {setting_key}: {e}")
            self.db.rollback()
            return False
    
    
    def _validate_setting_value(self, value: str, setting_type_code: str) -> ValidationResult:
        """
        Validate setting value against its type.
        
        Args:
            value: Value to validate (as string)
            setting_type_code: Expected type code
            
        Returns:
            ValidationResult with is_valid and error_message
        """
        try:
            if setting_type_code == 'integer':
                int(value)
            elif setting_type_code == 'decimal':
                float(value)
            elif setting_type_code == 'boolean':
                if value.lower() not in ('true', 'false', '0', '1', 'yes', 'no'):
                    return ValidationResult(False, "Boolean must be 'true', 'false', '0', or '1'")
            elif setting_type_code == 'json':
                json.loads(value)
            # 'string' requires no validation
            
            return ValidationResult(True)
            
        except ValueError as e:
            return ValidationResult(False, f"Invalid {setting_type_code}: {str(e)}")
        except json.JSONDecodeError as e:
            return ValidationResult(False, f"Invalid JSON: {str(e)}")
    
    
    def get_all_settings(self, category_code: Optional[str] = None) -> list[dict]:
        """
        Get all application settings (admin only).
        
        Args:
            category_code: Optional category filter
            
        Returns:
            List of setting dictionaries
        """
        try:
            query = self.db.query(AppSetting).filter(
                AppSetting.IsDeleted == False
            )
            
            if category_code:
                query = query.join(SettingCategory).filter(
                    SettingCategory.CategoryCode == category_code
                )
            
            settings = query.order_by(AppSetting.SortOrder, AppSetting.SettingKey).all()
            
            return [
                {
                    'setting_key': s.SettingKey,
                    'setting_value': s.SettingValue,
                    'category': s.category.CategoryCode,
                    'type': s.setting_type.TypeCode,
                    'description': s.Description,
                    'default_value': s.DefaultValue,
                    'is_editable': s.IsEditable,
                    'is_active': s.IsActive,
                }
                for s in settings
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving all settings: {e}")
            return []

