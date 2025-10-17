"""
Configuration API Router
Endpoints for reading and managing application configuration

Story 1.13: Configuration Service Implementation
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from common.database import get_db
from common.config_service import ConfigurationService
from common.constants import (
    MAX_COMPANY_NAME_LENGTH,
    HTTPStatus,
    ErrorCode,
)
from modules.config.schemas import (
    PublicConfigResponse,
    SettingResponse,
    UpdateSettingRequest,
    UpdateSettingResponse,
    CacheInvalidationResponse,
)
# from modules.auth.dependencies import require_role  # TODO: Uncomment when auth is integrated
# from backend.common.constants import UserRole  # TODO: Uncomment when auth is integrated


router = APIRouter(prefix="/api/config", tags=["Configuration"])


@router.get(
    "/",
    response_model=PublicConfigResponse,
    summary="Get public configuration",
    description="Get configuration settings safe for frontend consumption (no secrets)"
)
def get_public_config(
    db: Session = Depends(get_db)
) -> PublicConfigResponse:
    """
    Get public configuration settings for frontend.
    
    Story 1.13 Task 8: Public configuration endpoint
    
    Returns only settings safe for public exposure:
    - Password policy (min length, requirements)
    - Token expiry times (for UI display)
    - Company validation rules
    
    Does NOT return:
    - JWT secret keys
    - Database credentials
    - Email API keys
    - Other secrets
    
    Example response:
        {
            "password_min_length": 8,
            "password_require_uppercase": False,
            "password_require_number": True,
            "jwt_access_expiry_minutes": 15,
            "email_verification_expiry_hours": 24,
            "invitation_expiry_days": 7
        }
    """
    try:
        config = ConfigurationService(db)
        
        return PublicConfigResponse(
            # Password policy
            password_min_length=config.get_password_min_length(),
            password_require_uppercase=config.get_password_require_uppercase(),
            password_require_number=config.get_password_require_number(),
            
            # JWT settings
            jwt_access_expiry_minutes=config.get_jwt_access_expiry_minutes(),
            
            # Token expiry times
            email_verification_expiry_hours=config.get_email_verification_expiry_hours(),
            invitation_expiry_days=config.get_invitation_expiry_days(),
            
            # Company validation (hardcoded for now, can be moved to database in future)
            company_name_min_length=2,
            company_name_max_length=MAX_COMPANY_NAME_LENGTH,
        )
        
    except Exception as e:
        # Log error but don't expose internal details
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error retrieving public configuration: {e}")
        
        # Return graceful degradation (code defaults)
        from common.constants import (
            DEFAULT_JWT_ACCESS_EXPIRY_MINUTES,
            DEFAULT_PASSWORD_MIN_LENGTH,
            DEFAULT_EMAIL_VERIFICATION_EXPIRY_HOURS,
            DEFAULT_INVITATION_EXPIRY_DAYS,
        )
        
        return PublicConfigResponse(
            password_min_length=DEFAULT_PASSWORD_MIN_LENGTH,
            password_require_uppercase=False,
            password_require_number=True,
            jwt_access_expiry_minutes=DEFAULT_JWT_ACCESS_EXPIRY_MINUTES,
            email_verification_expiry_hours=DEFAULT_EMAIL_VERIFICATION_EXPIRY_HOURS,
            invitation_expiry_days=DEFAULT_INVITATION_EXPIRY_DAYS,
            company_name_min_length=2,
            company_name_max_length=MAX_COMPANY_NAME_LENGTH,
        )


# ============================================================================
# ADMIN ENDPOINTS (Story 1.13 Task 9)
# ============================================================================

admin_router = APIRouter(prefix="/api/admin/settings", tags=["Configuration - Admin"])


@admin_router.get(
    "/",
    response_model=List[SettingResponse],
    summary="Get all settings (Admin)",
    description="Get all application settings with metadata (admin only)"
)
def get_all_settings(
    category: str = None,
    db: Session = Depends(get_db),
    # current_user = Depends(require_role(UserRole.SYSTEM_ADMIN))  # TODO: Uncomment when auth is integrated
) -> List[SettingResponse]:
    """
    Get all application settings (admin only).
    
    Story 1.13 Task 9: Admin configuration management
    
    Args:
        category: Optional category filter (authentication, validation, email, security)
        
    Returns:
        List of all settings with metadata
        
    Requires:
        - system_admin role
    """
    config = ConfigurationService(db)
    settings = config.get_all_settings(category_code=category)
    
    return [SettingResponse(**setting) for setting in settings]


@admin_router.put(
    "/{setting_key}",
    response_model=UpdateSettingResponse,
    summary="Update setting (Admin)",
    description="Update an application setting value (admin only)"
)
def update_setting(
    setting_key: str,
    request: UpdateSettingRequest,
    db: Session = Depends(get_db),
    # current_user = Depends(require_role(UserRole.SYSTEM_ADMIN))  # TODO: Uncomment when auth is integrated
) -> UpdateSettingResponse:
    """
    Update application setting value (admin only).
    
    Story 1.13 Task 9: Admin configuration management
    
    Args:
        setting_key: Setting key to update (e.g., PASSWORD_MIN_LENGTH)
        request: New value (as string)
        
    Returns:
        Success response with updated value
        
    Requires:
        - system_admin role
        
    Example:
        PUT /api/admin/settings/PASSWORD_MIN_LENGTH
        Body: {"new_value": "10"}
    """
    config = ConfigurationService(db)
    
    # TODO: Get current_user.user_id when auth is integrated
    updated_by = None  # Will be current_user.user_id
    
    success = config.update_setting(
        setting_key=setting_key,
        new_value=request.new_value,
        updated_by=updated_by
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": ErrorCode.CONFIGURATION_ERROR,
                "message": f"Failed to update setting: {setting_key}. Setting may not exist or value is invalid."
            }
        )
    
    return UpdateSettingResponse(
        success=True,
        message="Setting updated successfully. Cache invalidated.",
        setting_key=setting_key,
        new_value=request.new_value
    )


@admin_router.post(
    "/reload",
    response_model=CacheInvalidationResponse,
    summary="Invalidate cache (Admin)",
    description="Force reload of configuration cache (admin only)"
)
def invalidate_cache(
    db: Session = Depends(get_db),
    # current_user = Depends(require_role(UserRole.SYSTEM_ADMIN))  # TODO: Uncomment when auth is integrated
) -> CacheInvalidationResponse:
    """
    Invalidate configuration cache (admin only).
    
    Story 1.13 Task 9: Admin configuration management
    
    Forces configuration service to reload settings from database
    on next access. Useful if settings were updated directly in database.
    
    Requires:
        - system_admin role
    """
    config = ConfigurationService(db)
    config.invalidate_cache()
    
    return CacheInvalidationResponse(
        success=True,
        message="Configuration cache invalidated successfully"
    )


# Export both routers
def include_routers(app):
    """Include configuration routers in main app"""
    app.include_router(router, prefix="/api")
    app.include_router(admin_router, prefix="/api")

