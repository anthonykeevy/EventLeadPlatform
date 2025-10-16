# Story 0.1: Database Models & Core Infrastructure

Status: Ready

## Story

As a developer,
I want all SQLAlchemy models and core infrastructure components in place,
so that I can build authentication and business logic features on a solid foundation.

## Acceptance Criteria

1. **AC-0.1.1**: All SQLAlchemy models created for Epic 1 tables (User, Company, UserCompany, tokens, log tables, ref tables)
2. **AC-0.1.2**: Models follow Solomon standards (PascalCase, audit columns, proper relationships)
3. **AC-0.1.3**: Database connection and session management working (`backend/common/database.py`)
4. **AC-0.1.4**: Security utilities implemented (bcrypt password hashing, token generation)
5. **AC-0.1.5**: Base Pydantic schemas created for common patterns
6. **AC-0.1.6**: All models can successfully query existing database tables
7. **AC-0.1.7**: Models include proper indexes and foreign key relationships
8. **AC-0.1.8**: Type hints and docstrings present for all public APIs

## Tasks / Subtasks

- [ ] **Task 1: Database Connection & Session Management** (AC: 0.1.3)
  - [ ] Review existing `backend/common/database.py` (already exists from previous work)
  - [ ] Verify SQLAlchemy engine configuration (connection pooling, timeouts)
  - [ ] Verify SessionLocal factory configuration
  - [ ] Verify `get_db()` dependency function for FastAPI
  - [ ] Test: Connection to EventLeadPlatform database successful
  - [ ] Test: Session creation and cleanup works correctly

- [ ] **Task 2: Security Utilities Foundation** (AC: 0.1.4)
  - [ ] Review/create `backend/common/security.py`
  - [ ] Implement `hash_password(password: str) -> str` using bcrypt (cost factor 12)
  - [ ] Implement `verify_password(plain: str, hashed: str) -> bool`
  - [ ] Implement `generate_secure_token(length: int = 32) -> str` using secrets.token_urlsafe()
  - [ ] Test: Password hashing produces bcrypt format `$2b$12$...`
  - [ ] Test: Password verification works correctly
  - [ ] Test: Tokens are cryptographically secure and unique

- [ ] **Task 3: Reference Table Models (ref schema)** (AC: 0.1.1, 0.1.2)
  - [ ] Create `backend/models/ref/` directory
  - [ ] Create `backend/models/ref/__init__.py`
  - [ ] Create `backend/models/ref/country.py` - Country model
  - [ ] Create `backend/models/ref/language.py` - Language model
  - [ ] Create `backend/models/ref/user_status.py` - UserStatus model
  - [ ] Create `backend/models/ref/user_invitation_status.py` - UserInvitationStatus model
  - [ ] Create `backend/models/ref/user_role.py` - UserRole model
  - [ ] Create `backend/models/ref/user_company_role.py` - UserCompanyRole model
  - [ ] Create `backend/models/ref/user_company_status.py` - UserCompanyStatus model
  - [ ] Create `backend/models/ref/setting_category.py` - SettingCategory model
  - [ ] Create `backend/models/ref/setting_type.py` - SettingType model
  - [ ] Create `backend/models/ref/rule_type.py` - RuleType model
  - [ ] Create `backend/models/ref/customer_tier.py` - CustomerTier model
  - [ ] Create `backend/models/ref/joined_via.py` - JoinedVia model
  - [ ] Create `backend/models/ref/industry.py` - Industry model
  - [ ] Test: All ref models can query existing tables and retrieve seed data

- [ ] **Task 4: Core Business Models (dbo schema)** (AC: 0.1.1, 0.1.2, 0.1.7)
  - [ ] Create `backend/models/` directory structure
  - [ ] Create `backend/models/__init__.py`
  - [ ] Create `backend/models/user.py` with User model
    - Fields: UserID (PK), Email, PasswordHash, FirstName, LastName, Phone, RoleTitle, EmailVerified, EmailVerifiedDate, OnboardingComplete, LastLogin, AccessTokenVersion
    - Audit fields: CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy
    - Relationships: companies (via UserCompany), invitations, verification_tokens, reset_tokens
  - [ ] Create `backend/models/company.py` with Company model
    - Fields: CompanyID (PK), CompanyName, ABN, ACN, TradingName, EntityTypeCode, EntityTypeName, GSTRegistered, IsActive
    - Audit fields: CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy
    - Relationships: users (via UserCompany), customer_details, billing_details, organizer_details
  - [ ] Create `backend/models/user_company.py` with UserCompany model
    - Fields: UserCompanyID (PK), UserID (FK), CompanyID (FK), UserCompanyRoleID (FK), UserCompanyStatusID (FK), IsDefaultCompany, JoinedVia, InvitedBy
    - Audit fields: CreatedDate, UpdatedDate, IsDeleted, DeletedDate
    - Relationships: user, company, role, status
  - [ ] Create `backend/models/company_customer_details.py` - CompanyCustomerDetails model
  - [ ] Create `backend/models/company_billing_details.py` - CompanyBillingDetails model
  - [ ] Create `backend/models/company_organizer_details.py` - CompanyOrganizerDetails model
  - [ ] Create `backend/models/user_invitation.py` - UserInvitation model
  - [ ] Create `backend/models/user_email_verification_token.py` - UserEmailVerificationToken model
  - [ ] Create `backend/models/user_password_reset_token.py` - UserPasswordResetToken model
  - [ ] Test: All dbo models can query existing tables
  - [ ] Test: Foreign key relationships work correctly

- [ ] **Task 5: Configuration Models (config schema)** (AC: 0.1.1, 0.1.2)
  - [ ] Create `backend/models/config/` directory
  - [ ] Create `backend/models/config/__init__.py`
  - [ ] Create `backend/models/config/app_setting.py` - AppSetting model
  - [ ] Create `backend/models/config/validation_rule.py` - ValidationRule model
  - [ ] Test: Config models can query existing tables

- [ ] **Task 6: Audit Models (audit schema)** (AC: 0.1.1, 0.1.2)
  - [ ] Create `backend/models/audit/` directory
  - [ ] Create `backend/models/audit/__init__.py`
  - [ ] Create `backend/models/audit/activity_log.py` - ActivityLog model
  - [ ] Create `backend/models/audit/user_audit.py` - User audit model
  - [ ] Create `backend/models/audit/company_audit.py` - Company audit model
  - [ ] Create `backend/models/audit/role_audit.py` - Role audit model
  - [ ] Test: Audit models can query existing tables

- [ ] **Task 7: Log Models (log schema)** (AC: 0.1.1, 0.1.2)
  - [ ] Create `backend/models/log/` directory
  - [ ] Create `backend/models/log/__init__.py`
  - [ ] Create `backend/models/log/api_request.py` - ApiRequest model
  - [ ] Create `backend/models/log/auth_event.py` - AuthEvent model
  - [ ] Create `backend/models/log/application_error.py` - ApplicationError model
  - [ ] Create `backend/models/log/email_delivery.py` - EmailDelivery model
  - [ ] Test: Log models can query existing tables

- [ ] **Task 8: Cache Models (cache schema)** (AC: 0.1.1, 0.1.2)
  - [ ] Create `backend/models/cache/` directory
  - [ ] Create `backend/models/cache/__init__.py`
  - [ ] Create `backend/models/cache/abr_search.py` - ABRSearch model
  - [ ] Test: Cache model can query existing table

- [ ] **Task 9: Base Pydantic Schemas** (AC: 0.1.5)
  - [ ] Create `backend/schemas/` directory
  - [ ] Create `backend/schemas/__init__.py`
  - [ ] Create `backend/schemas/base.py` with common patterns:
    - BaseResponse (success, message, data)
    - ErrorResponse (error, details)
    - PaginationParams (page, pageSize, sortBy, sortOrder)
    - PaginatedResponse (items, total, page, pageSize)
  - [ ] Create `backend/schemas/common.py` with field validators:
    - EmailStr validator
    - Phone number validator (Australian format)
    - ABN/ACN validators
  - [ ] Test: Schema validation works correctly

- [ ] **Task 10: Model Registration & Imports** (AC: 0.1.6)
  - [ ] Update `backend/models/__init__.py` to export all models
  - [ ] Verify all models registered with SQLAlchemy Base
  - [ ] Create comprehensive test that imports all models
  - [ ] Test: All models can be imported without circular dependency errors
  - [ ] Test: All table names match database (PascalCase)

- [ ] **Task 11: Integration Testing** (AC: 0.1.6, 0.1.7)
  - [ ] Test: Query User table and retrieve records
  - [ ] Test: Query Company table and retrieve records
  - [ ] Test: Query UserCompany with joins (User + Company + Role)
  - [ ] Test: Query all reference tables and verify seed data
  - [ ] Test: Foreign key relationships navigable (user.companies works)
  - [ ] Test: Audit columns have proper defaults (CreatedDate = GETUTCDATE())
  - [ ] Test: All indexes exist as defined in migration
  - [ ] Test: Password hashing and token generation work end-to-end

- [ ] **Task 12: Documentation** (AC: 0.1.8)
  - [ ] Add docstrings to all model classes
  - [ ] Add type hints to all security utility functions
  - [ ] Document model relationships and usage patterns
  - [ ] Create quick reference for common queries

## Dev Notes

### Architecture Patterns and Constraints

**Database Connection Pattern:**
- SQLAlchemy 2.0+ style (using `Session` and `select()`)
- Connection pooling enabled (pool_pre_ping=True, pool_recycle=3600)
- Session per request via FastAPI dependency injection

**Model Standards (Solomon Requirements):**
- **Table Names:** PascalCase (User, Company, UserCompany)
- **Column Names:** PascalCase (UserID, FirstName, EmailVerified)
- **Primary Keys:** [TableName]ID pattern (UserID, CompanyID)
- **Foreign Keys:** [ReferencedTable]ID pattern (UserID in UserCompany)
- **Indexes:** IX_TableName_ColumnName pattern
- **Constraints:** PK_, FK_, UQ_, CK_, DF_ prefixes
- **Audit Columns:** CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy
- **Timestamps:** DATETIME2 with UTC (GETUTCDATE() default)

**Security Standards:**
- **Password Hashing:** bcrypt with cost factor 12 (balance security/performance)
- **Token Generation:** `secrets.token_urlsafe(32)` for cryptographic security (256 bits)
- **Never log:** Passwords, tokens, sensitive data

**Schema Organization:**
```
backend/models/
├── __init__.py (exports all models)
├── user.py (dbo.User)
├── company.py (dbo.Company)
├── user_company.py (dbo.UserCompany)
├── company_customer_details.py
├── company_billing_details.py
├── company_organizer_details.py
├── user_invitation.py
├── user_email_verification_token.py
├── user_password_reset_token.py
├── ref/
│   ├── __init__.py
│   ├── country.py
│   ├── language.py
│   ├── user_status.py
│   └── ... (13 ref tables)
├── config/
│   ├── __init__.py
│   ├── app_setting.py
│   └── validation_rule.py
├── audit/
│   ├── __init__.py
│   ├── activity_log.py
│   └── ... (4 audit tables)
├── log/
│   ├── __init__.py
│   ├── api_request.py
│   └── ... (4 log tables)
└── cache/
    ├── __init__.py
    └── abr_search.py
```

### Project Structure Notes

**SQLAlchemy Configuration:**
```python
# backend/common/database.py (already exists)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "...")
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Model Example Pattern:**
```python
# backend/models/user.py
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func
from backend.common.database import Base

class User(Base):
    __tablename__ = "User"
    __table_args__ = {"schema": "dbo"}
    
    UserID = Column(BigInteger, primary_key=True, autoincrement=True)
    Email = Column(String(255), unique=True, nullable=False, index=True)
    PasswordHash = Column(String(255), nullable=False)
    FirstName = Column(String(100), nullable=True)
    LastName = Column(String(100), nullable=True)
    EmailVerified = Column(Boolean, nullable=False, default=False)
    OnboardingComplete = Column(Boolean, nullable=False, default=False)
    
    # Audit columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    IsDeleted = Column(Boolean, nullable=False, default=False)
```

### Database Tables Used

**All 34 tables from Epic 1 migration:**

**ref schema (13 tables):**
- Country, Language, Industry, UserStatus, UserInvitationStatus, UserRole, UserCompanyRole, UserCompanyStatus, SettingCategory, SettingType, RuleType, CustomerTier, JoinedVia

**dbo schema (9 tables):**
- User, Company, UserCompany, CompanyCustomerDetails, CompanyBillingDetails, CompanyOrganizerDetails, UserInvitation, UserEmailVerificationToken, UserPasswordResetToken

**config schema (2 tables):**
- AppSetting, ValidationRule

**audit schema (4 tables):**
- ActivityLog, User (audit), Company (audit), Role (audit)

**log schema (4 tables):**
- ApiRequest, AuthEvent, ApplicationError, EmailDelivery

**cache schema (1 table):**
- ABRSearch

### Testing Standards Summary

**Model Testing (`backend/tests/models/`):**
- Test model creation and querying
- Test relationships and joins
- Test foreign key constraints
- Test index usage
- Test audit column defaults

**Security Testing (`backend/tests/test_security.py`):**
- Test password hashing (bcrypt format, cost factor)
- Test password verification (correct/incorrect)
- Test token generation (uniqueness, length, security)

**Database Testing:**
- Use pytest fixtures for database session
- Rollback transactions after each test (no persistent test data)
- Test against actual database (not mocks) for integration confidence

### References

- [Database Quick Reference: Complete table list](docs/technical-guides/database-quick-reference.md)
- [dbo Schema Reference: Core business tables](docs/database/schema-reference/dbo-schema.md)
- [ref Schema Reference: Reference/lookup tables](docs/database/schema-reference/ref-schema.md)
- [log Schema Reference: Technical logging tables](docs/database/schema-reference/log-schema.md)
- [ADR-003: Naming Convention Strategy](docs/architecture/decisions/ADR-003-naming-convention-strategy.md)
- [Backend Quick Reference: Module structure](docs/technical-guides/backend-quick-reference.md)
- [Tech Spec Epic 1: Implementation Standards (lines 3150-3390)](docs/tech-spec-epic-1.md#L3150-L3390)

## Dev Agent Record

### Context Reference

- [Story Context 0.1](../story-context-0.1.xml) - Generated 2025-10-16

### Agent Model Used

<!-- Will be populated by Developer Agent during implementation -->

### Debug Log References

### Completion Notes List

### File List

