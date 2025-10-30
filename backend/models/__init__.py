"""
SQLAlchemy Models
All database models for the EventLead Platform

This module exports all models and ensures they are registered with SQLAlchemy Base.
Import from this module to ensure proper model discovery and relationship resolution.

Usage:
    from models import User, Company, UserCompany
    
Organization:
    - ref: Reference/lookup tables (16 models - Epic 2: +3)
    - dbo: Core business entities (10 models - Epic 2: +1)
    - config: Configuration tables (2 models)
    - audit: Audit trail tables (4 models)
    - log: Technical logging tables (4 models)
    - cache: API cache tables (1 model)
    
Total: 37 models across 6 schemas (Epic 2: +4 models)
"""

# Core business models (dbo schema)
from .user import User
from .company import Company
from .user_company import UserCompany
from .user_industry import UserIndustry
from .company_customer_details import CompanyCustomerDetails
from .company_billing_details import CompanyBillingDetails
from .company_organizer_details import CompanyOrganizerDetails
from .user_invitation import UserInvitation
from .user_email_verification_token import UserEmailVerificationToken
from .user_password_reset_token import UserPasswordResetToken
from .user_refresh_token import UserRefreshToken

# Reference tables (ref schema)
from .ref import (
    Country,
    Language,
    Industry,
    UserStatus,
    UserInvitationStatus,
    UserRole,
    UserCompanyRole,
    UserCompanyStatus,
    SettingCategory,
    SettingType,
    RuleType,
    CustomerTier,
    JoinedVia,
    ThemePreference,
    LayoutDensity,
    FontSize,
)

# Configuration tables (config schema)
from .config import (
    AppSetting,
    ValidationRule,
)

# Audit tables (audit schema)
from .audit import (
    ActivityLog,
    UserAudit,
    CompanyAudit,
    RoleAudit,
)

# Log tables (log schema)
from .log import (
    ApiRequest,
    AuthEvent,
    ApplicationError,
    EmailDelivery,
)

# Cache tables (cache schema)
from .cache import (
    ABRSearch,
)


# Export all models
__all__ = [
    # Core business models (dbo)
    "User",
    "Company",
    "UserCompany",
    "UserIndustry",
    "CompanyCustomerDetails",
    "CompanyBillingDetails",
    "CompanyOrganizerDetails",
    "UserInvitation",
    "UserEmailVerificationToken",
    "UserPasswordResetToken",
    "UserRefreshToken",
    
    # Reference tables (ref)
    "Country",
    "Language",
    "Industry",
    "UserStatus",
    "UserInvitationStatus",
    "UserRole",
    "UserCompanyRole",
    "UserCompanyStatus",
    "SettingCategory",
    "SettingType",
    "RuleType",
    "CustomerTier",
    "JoinedVia",
    "ThemePreference",
    "LayoutDensity",
    "FontSize",
    
    # Configuration tables (config)
    "AppSetting",
    "ValidationRule",
    
    # Audit tables (audit)
    "ActivityLog",
    "UserAudit",
    "CompanyAudit",
    "RoleAudit",
    
    # Log tables (log)
    "ApiRequest",
    "AuthEvent",
    "ApplicationError",
    "EmailDelivery",
    
    # Cache tables (cache)
    "ABRSearch",
]


# Model count validation
def get_model_count() -> int:
    """Get total number of registered models."""
    return len(__all__)


def validate_models() -> None:
    """
    Validate that all models are properly registered with SQLAlchemy Base.
    
    Raises:
        RuntimeError: If models are not properly registered
    """
    from common.database import Base
    
    expected_count = 37  # Updated for Epic 2: 33 base + 4 new models
    actual_count = len(__all__)
    
    if actual_count != expected_count:
        raise RuntimeError(
            f"Model count mismatch: expected {expected_count}, got {actual_count}"
        )
    
    # Verify all models are registered with Base
    registered_tables = set(Base.metadata.tables.keys())
    
    print(f"✓ Loaded {actual_count} models")
    print(f"✓ Registered {len(registered_tables)} tables with SQLAlchemy")
    print(f"✓ Schemas: ref, dbo, config, audit, log, cache")
