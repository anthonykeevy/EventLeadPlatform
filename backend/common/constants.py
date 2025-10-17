"""
Application Constants
Default fallback values when database configuration unavailable

Configuration Distribution:
- .env: Infrastructure & secrets (DATABASE_URL, JWT_SECRET_KEY, EMAIL_API_KEY)
- Database (AppSetting): Business rules (JWT expiry, password length, token expiry)
- Code (this file): Static logic & default fallbacks

When to use code defaults:
- Database unavailable (connection failure, startup)
- Configuration service error
- Missing database setting (fail-safe)
"""

# ============================================================================
# AUTHENTICATION DEFAULTS (Story 1.13)
# ============================================================================

# JWT Token Configuration
DEFAULT_JWT_ACCESS_EXPIRY_MINUTES = 15
DEFAULT_JWT_REFRESH_EXPIRY_DAYS = 7

# Password Policy
DEFAULT_PASSWORD_MIN_LENGTH = 8
DEFAULT_PASSWORD_REQUIRE_UPPERCASE = False
DEFAULT_PASSWORD_REQUIRE_NUMBER = True
DEFAULT_PASSWORD_EXPIRY_DAYS = 90  # 0 = never expires

# Security
DEFAULT_MAX_FAILED_LOGIN_ATTEMPTS = 5
DEFAULT_ACCOUNT_LOCKOUT_MINUTES = 15
DEFAULT_SESSION_TIMEOUT_MINUTES = 30

# Email Verification & Password Reset
DEFAULT_EMAIL_VERIFICATION_EXPIRY_HOURS = 24
DEFAULT_PASSWORD_RESET_EXPIRY_HOURS = 1

# Team Invitations
DEFAULT_INVITATION_EXPIRY_DAYS = 7

# Token Generation
DEFAULT_TOKEN_LENGTH_BYTES = 32


# ============================================================================
# USER STATUS ENUMS (ref.UserStatus)
# ============================================================================

class UserStatus:
    """User account status codes (from ref.UserStatus)"""
    PENDING = "pending"  # Email not verified
    ACTIVE = "active"  # Active and in good standing
    SUSPENDED = "suspended"  # Temporarily disabled by admin
    LOCKED = "locked"  # Locked due to failed login attempts


# ============================================================================
# USER INVITATION STATUS ENUMS (ref.UserInvitationStatus)
# ============================================================================

class InvitationStatus:
    """Team invitation status codes (from ref.UserInvitationStatus)"""
    PENDING = "pending"  # Awaiting response
    ACCEPTED = "accepted"  # User joined team
    DECLINED = "declined"  # User declined
    EXPIRED = "expired"  # Invitation expired (7-day TTL)
    CANCELLED = "cancelled"  # Admin cancelled


# ============================================================================
# USER ROLE ENUMS (ref.UserRole - System-level)
# ============================================================================

class UserRole:
    """System-level role codes (from ref.UserRole)"""
    SYSTEM_ADMIN = "system_admin"  # Platform administrator
    COMPANY_USER = "company_user"  # Standard company user (no system permissions)


# ============================================================================
# USER COMPANY ROLE ENUMS (ref.UserCompanyRole - Company-level)
# ============================================================================

class UserCompanyRole:
    """Company-level role codes (from ref.UserCompanyRole)"""
    COMPANY_ADMIN = "company_admin"  # Full company access
    COMPANY_USER = "company_user"  # Standard team member
    COMPANY_VIEWER = "company_viewer"  # Read-only access


# ============================================================================
# USER COMPANY STATUS ENUMS (ref.UserCompanyStatus)
# ============================================================================

class UserCompanyStatus:
    """User-company relationship status codes (from ref.UserCompanyStatus)"""
    ACTIVE = "active"  # Active team member
    SUSPENDED = "suspended"  # Temporarily suspended
    REMOVED = "removed"  # Removed from company


# ============================================================================
# JOINED VIA ENUMS (ref.JoinedVia)
# ============================================================================

class JoinedVia:
    """User acquisition method codes (from ref.JoinedVia)"""
    SIGNUP = "signup"  # Self-signup during onboarding
    INVITATION = "invitation"  # Invited by company admin
    TRANSFER = "transfer"  # Transferred from another company (future)


# ============================================================================
# SETTING CATEGORY ENUMS (ref.SettingCategory)
# ============================================================================

class SettingCategory:
    """Application setting category codes (from ref.SettingCategory)"""
    AUTHENTICATION = "authentication"  # Auth and password policy
    VALIDATION = "validation"  # Input validation rules
    EMAIL = "email"  # Email delivery and templates
    SECURITY = "security"  # Security policies and rate limiting


# ============================================================================
# SETTING TYPE ENUMS (ref.SettingType)
# ============================================================================

class SettingType:
    """Application setting type codes (from ref.SettingType)"""
    INTEGER = "integer"  # Whole number
    BOOLEAN = "boolean"  # True/false flag
    STRING = "string"  # Text value
    JSON = "json"  # JSON object
    DECIMAL = "decimal"  # Decimal number


# ============================================================================
# RULE TYPE ENUMS (ref.RuleType)
# ============================================================================

class RuleType:
    """Validation rule type codes (from ref.RuleType)"""
    PHONE = "phone"  # Phone number format
    POSTAL_CODE = "postal_code"  # Postal/zip code format
    TAX_ID = "tax_id"  # Tax identifier (ABN, EIN, VAT)
    EMAIL = "email"  # Email format
    ADDRESS = "address"  # Address format


# ============================================================================
# CUSTOMER TIER ENUMS (ref.CustomerTier)
# ============================================================================

class CustomerTier:
    """Subscription tier codes (from ref.CustomerTier)"""
    FREE = "free"  # Free tier
    STARTER = "starter"  # Starter plan
    PROFESSIONAL = "professional"  # Professional plan
    ENTERPRISE = "enterprise"  # Enterprise plan


# ============================================================================
# COMPANY DISPLAY NAME SOURCE ENUMS (dbo.Company.DisplayNameSource)
# ============================================================================

class CompanyDisplayNameSource:
    """Company display name source options (from dbo.Company)"""
    LEGAL = "Legal"  # Use LegalEntityName
    BUSINESS = "Business"  # Use first BusinessName
    CUSTOM = "Custom"  # Use CustomDisplayName
    USER = "User"  # Use user-entered CompanyName


# ============================================================================
# ABN STATUS ENUMS (dbo.Company.ABNStatus)
# ============================================================================

class ABNStatus:
    """ABN status codes (from dbo.Company and cache.ABRSearch)"""
    ACTIVE = "Active"  # ABN is active
    CANCELLED = "Cancelled"  # ABN cancelled
    HISTORICAL = "Historical"  # Historical ABN record


# ============================================================================
# ABR SEARCH TYPE ENUMS (cache.ABRSearch.SearchType)
# ============================================================================

class ABRSearchType:
    """ABR search type codes (from cache.ABRSearch)"""
    ABN = "ABN"  # Search by ABN (11 digits)
    ACN = "ACN"  # Search by ACN (9 digits)
    NAME = "Name"  # Search by company name


# ============================================================================
# VALIDATION PATTERNS (Regex)
# ============================================================================

# Email validation (basic RFC 5322 pattern)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Australia-specific patterns (country-specific validation in ValidationRule table)
AUSTRALIAN_MOBILE_REGEX = r'^04\d{8}$'
AUSTRALIAN_LANDLINE_REGEX = r'^0[2-8]\d{8}$'
AUSTRALIAN_POSTCODE_REGEX = r'^\d{4}$'
AUSTRALIAN_ABN_REGEX = r'^\d{11}$'
AUSTRALIAN_ACN_REGEX = r'^\d{9}$'


# ============================================================================
# PHYSICAL LIMITS (Never change - hard limits)
# ============================================================================

# Field length limits (must match database schema)
MAX_EMAIL_LENGTH = 255
MAX_NAME_LENGTH = 100
MAX_COMPANY_NAME_LENGTH = 200
MAX_PHONE_LENGTH = 20
MAX_URL_LENGTH = 500

# Token lengths
TOKEN_LENGTH_BYTES = 32  # 256-bit tokens (44 characters base64)

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Rate limiting (requests per minute)
DEFAULT_RATE_LIMIT_PER_MINUTE = 60
AUTH_RATE_LIMIT_PER_MINUTE = 10  # Login/signup endpoints


# ============================================================================
# FEATURE FLAGS (Epic 1 MVP)
# ============================================================================

# Epic 1 MVP Features (Always enabled)
FEATURE_MULTI_TENANCY = True
FEATURE_TEAM_INVITATIONS = True
FEATURE_EMAIL_VERIFICATION = True
FEATURE_PASSWORD_RESET = True

# Future Features (Disabled in Epic 1)
FEATURE_MULTI_COMPANY_USER = True  # Story 1.11 (Branch Companies)
FEATURE_ABR_SEARCH_CACHE = True  # Story 1.10 (Enhanced ABR Search)
FEATURE_COUNTRY_VALIDATION = True  # Story 1.12 (International Foundation)
FEATURE_TWO_FACTOR_AUTH = False  # Future epic
FEATURE_SSO = False  # Future epic
FEATURE_API_WEBHOOKS = False  # Future epic


# ============================================================================
# TIMEZONE DEFAULTS
# ============================================================================

DEFAULT_TIMEZONE = "Australia/Sydney"
SUPPORTED_TIMEZONES = [
    "Australia/Sydney",
    "Australia/Melbourne",
    "Australia/Brisbane",
    "Australia/Adelaide",
    "Australia/Perth",
    "Australia/Hobart",
    "Australia/Darwin",
]


# ============================================================================
# CURRENCY DEFAULTS (Epic 1 MVP: Australia only)
# ============================================================================

DEFAULT_CURRENCY_CODE = "AUD"
DEFAULT_CURRENCY_SYMBOL = "$"


# ============================================================================
# AUDIT TRAIL CONSTANTS
# ============================================================================

class ChangeType:
    """Audit trail change types"""
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    STATUS_CHANGE = "status_change"
    ROLE_CHANGE = "role_change"


class EntityType:
    """Entity types for audit logging"""
    USER = "user"
    COMPANY = "company"
    USER_COMPANY = "user_company"
    INVITATION = "invitation"
    SETTING = "setting"
    VALIDATION_RULE = "validation_rule"


# ============================================================================
# HTTP STATUS CODE HELPERS
# ============================================================================

class HTTPStatus:
    """Common HTTP status codes"""
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


# ============================================================================
# ERROR CODES (API Error Responses)
# ============================================================================

class ErrorCode:
    """Application error codes for API responses"""
    # Authentication
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    EMAIL_NOT_VERIFIED = "EMAIL_NOT_VERIFIED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_SUSPENDED = "ACCOUNT_SUSPENDED"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    
    # Authorization
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    COMPANY_ACCESS_DENIED = "COMPANY_ACCESS_DENIED"
    
    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    INVALID_EMAIL_FORMAT = "INVALID_EMAIL_FORMAT"
    PASSWORD_TOO_WEAK = "PASSWORD_TOO_WEAK"
    
    # Business Logic
    USER_NOT_FOUND = "USER_NOT_FOUND"
    COMPANY_NOT_FOUND = "COMPANY_NOT_FOUND"
    INVITATION_NOT_FOUND = "INVITATION_NOT_FOUND"
    INVITATION_EXPIRED = "INVITATION_EXPIRED"
    INVITATION_ALREADY_ACCEPTED = "INVITATION_ALREADY_ACCEPTED"
    
    # System
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

