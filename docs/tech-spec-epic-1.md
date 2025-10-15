# Technical Specification: Authentication & Onboarding

Date: 2025-10-13
Author: Anthony Keevy
Epic ID: Epic 1
Status: Ready for Review

---

## Overview

Epic 1 establishes the authentication and user onboarding system for the EventLeadPlatform, a multi-tenant SaaS application. This epic implements secure email-based authentication with verification, role-based access control (RBAC) for three user roles, and a comprehensive multi-step onboarding flow that collects user details and company information. The system supports two primary user journeys: first-time users who create new companies (becoming Company Admins), and invited users who join existing companies with assigned roles.

This epic is foundational to the entire platform as it governs access control, multi-tenancy boundaries, and team collaboration capabilities.

## Objectives and Scope

**In Scope:**
- Email-based signup/login with email verification workflow
- Password reset functionality with secure token-based flow
- JWT-based session management with token refresh capabilities
- Three-role RBAC system: System Admin (backend only for MVP), Company Admin (full access), Company User (limited permissions)
- Multi-step onboarding flow for first-time users (user details + company setup)
- Simplified onboarding flow for invited users (user details only)
- Team invitation system with secure tokens and 7-day expiration
- User profile management (name, phone, role/title)
- Company profile creation during onboarding (name, ABN, billing address)
- RBAC middleware for authorization checks across all endpoints
- Activity logging for authentication and user management events

**Out of Scope (Future Epics):**
- Social authentication (Google, Microsoft, LinkedIn)
- Multi-factor authentication (MFA)
- Advanced team permissions (fine-grained permissions beyond Admin/User)
- Seat-based pricing or user limits
- System Admin UI (role exists, admin dashboard in future epic)
- Audit trail UI (data collection only, UI in Epic 9)
- Password policies (complexity requirements deferred to Phase 2)

## System Architecture Alignment

This epic implements components across all three architecture tiers as defined in the solution architecture:

**Backend Tier:**
- `backend/modules/auth/` - Core authentication module containing signup, login, email verification, password reset endpoints and JWT generation
- `backend/modules/auth/middleware.py` - RBAC middleware for role-based authorization
- `backend/modules/companies/` - Company management (minimal CRUD for onboarding)
- `backend/modules/team/` - Invitation management
- `backend/common/security.py` - Password hashing utilities (bcrypt)
- `backend/common/email.py` - Email service abstraction (SendGrid/Azure Communications)

**Database Tier:**
- MS SQL Server tables: `users`, `companies`, `invitations`, `email_verification_tokens`, `password_reset_tokens`, `activity_log`
- Multi-tenant architecture with `company_id` foreign keys
- Row-level security patterns for data isolation

**Frontend Tier:**
- `frontend/features/auth/` - Authentication UI components
- Public pages: Signup, Login, Email Verification Confirmation, Password Reset
- Authenticated onboarding flow: User Details Step, Company Setup Step
- Invitation acceptance page
- JWT token storage and refresh logic in React context

**Cross-Cutting Concerns:**
- Email service integration (SendGrid or Azure Communication Services)
- Token generation and validation (secure cryptographic tokens)
- Audit logging (all auth events tracked in `activity_log` table)

## Detailed Design

### Services and Modules

| Module | Responsibilities | Inputs | Outputs | Owner |
|--------|------------------|---------|---------|-------|
| `backend/modules/auth/router.py` | Authentication REST endpoints (signup, login, verify-email, reset-password, refresh-token) | Email, password, tokens | JWT tokens, success/error responses | Auth Module |
| `backend/modules/auth/service.py` | Business logic for authentication flows, token generation/validation, password hashing | User credentials, tokens | User objects, JWT tokens, validation results | Auth Module |
| `backend/modules/auth/middleware.py` | RBAC authorization checks, JWT validation, role enforcement | JWT token, required role | Decorated endpoint with user context | Auth Module |
| `backend/modules/companies/router.py` | Company CRUD, enhanced ABR search endpoints | Company data, search queries | Company object, search results | Company Module |
| `backend/modules/companies/service.py` | Company business logic, enhanced ABR search, multi-tenant setup | Company data, search queries | Company record, search results | Company Module |
| `backend/modules/companies/abr_client.py` | Enhanced ABR API client (ABN, ACN, Name search) | Search queries | ABR API responses | Company Module |
| `backend/modules/companies/cache_service.py` | Enterprise-grade ABR search caching | Search queries, results | Cached results, analytics | Company Module |
| `backend/modules/companies/relationship_service.py` | Company relationship management (branch, subsidiary) | Company IDs, relationship type | Company relationships, switch requests | Company Module |
| `backend/modules/companies/switch_service.py` | Company switching and access validation | User ID, target company ID | Access validation, switch approval | Company Module |
| `backend/modules/countries/validation_engine.py` | Country-specific validation rules engine | Country ID, field type, value | Validation results, error messages | Countries Module |
| `backend/modules/countries/expansion_service.py` | International expansion setup and management | Country data, validation rules | New country setup, rule configuration | Countries Module |
| `backend/modules/config/specification_service.py` | Application specification parameter resolution and caching | Category, parameter name, country ID | Resolved parameter values | Configuration Module |
| `backend/modules/config/config_api.py` | Configuration API endpoints for frontend consumption | Configuration requests | Parameter values, configuration objects | Configuration Module |
| `backend/modules/team/router.py` | Invitation management (send, accept, cancel, resend) | Invitation data, tokens | Invitation object, success/error | Team Module |
| `backend/modules/team/service.py` | Invitation business logic, token generation, expiry checks | Invitation data | Invitation records, email triggers | Team Module |
| `backend/common/security.py` | Password hashing (bcrypt), token generation (secrets), JWT utilities | Plain text passwords, secrets | Hashed passwords, secure tokens | Common Utilities |
| `backend/common/email.py` | Email service abstraction (SendGrid/Azure), template rendering | Recipient, subject, template, data | Email sent confirmation | Common Utilities |
| `frontend/features/auth/AuthContext.tsx` | React context for auth state, JWT storage, token refresh | User actions (login, logout) | Auth state, user object | Frontend Auth |
| `frontend/features/auth/components/SignupForm.tsx` | Signup form with email/password validation | User input | API call to `/api/auth/signup` | Frontend Auth |
| `frontend/features/auth/components/LoginForm.tsx` | Login form with credential validation | User input | JWT token, navigate to onboarding/dashboard | Frontend Auth |
| `frontend/features/auth/components/OnboardingFlow.tsx` | Multi-step onboarding wizard (user details + company setup) | User/company data | Completed onboarding, navigate to dashboard | Frontend Auth |
| `frontend/features/auth/components/InvitationAcceptance.tsx` | Invitation acceptance page (set password, pre-filled names) | Invitation token, password | User account created, navigate to onboarding | Frontend Auth |
| `frontend/features/companies/components/SmartCompanySearch.tsx` | Enhanced company search with auto-detection (ABN/ACN/Name) | Search query | Company search results, auto-selection | Frontend Companies |
| `frontend/features/companies/components/CompanySearchResults.tsx` | Rich search results display with company details | Search results | Selected company data | Frontend Companies |
| `frontend/features/companies/components/CompanySwitcher.tsx` | Company switching dropdown with relationship context | Current company, user companies | Company switch, access request | Frontend Companies |
| `frontend/features/companies/components/CompanyAccessRequest.tsx` | Request access to company modal | Target company ID | Access request submission | Frontend Companies |
| `frontend/features/countries/components/CountryValidation.tsx` | Country-specific validation hook and utilities | Country ID, field type | Validation rules, error messages | Frontend Countries |
| `frontend/features/countries/components/PhoneInput.tsx` | Dynamic phone input with country-specific validation | Country ID, phone value | Validated phone, error display | Frontend Countries |
| `frontend/features/config/useApplicationConfig.tsx` | React hook for application configuration consumption | Country ID, configuration category | Configuration values, loading state | Frontend Config |
| `frontend/features/config/ConfigProvider.tsx` | React context provider for application configuration | Configuration data | Global configuration state | Frontend Config |
| `frontend/features/ux/components/EnhancedFormInput.tsx` | Enhanced input component with floating labels, validation, masking | Field props, validation rules | Formatted input, validation state | Frontend UX |
| `frontend/features/ux/components/LoadingStates.tsx` | Loading state components (spinners, skeletons, progress) | Loading type, progress data | Loading UI components | Frontend UX |
| `frontend/features/ux/components/ErrorBoundary.tsx` | Error boundary with recovery options | Error state, recovery actions | Error UI, recovery flow | Frontend UX |
| `frontend/features/ux/components/ProgressIndicator.tsx` | Multi-step progress indicator with animations | Step data, current step | Progress UI component | Frontend UX |
| `frontend/features/ux/hooks/useFormValidation.tsx` | Real-time form validation hook | Form data, validation rules | Validation state, errors | Frontend UX |
| `frontend/features/ux/hooks/useAutoSave.tsx` | Auto-save functionality with visual feedback | Form data, save interval | Auto-save state, last saved | Frontend UX |
| `frontend/features/ux/hooks/useKeyboardNavigation.tsx` | Keyboard navigation and accessibility hooks | Navigation targets | Keyboard event handlers | Frontend UX |

### Permission Service Architecture (Future-Proof Design)

To enable future migration to granular permission-based access control (PBAC) without major refactoring, the platform implements a permission abstraction layer starting in Story 1.8. This design allows evolution from role-based access control (RBAC) to PBAC with minimal code changes.

#### Backend Permission Service (Python)

**Module:** `backend/modules/permissions/service.py`

**Purpose:** Centralized permission checking that abstracts the underlying implementation (role flags today, Permission table in future)

**Public API (Stable - Never Changes):**
```python
class PermissionService:
    def has_permission(
        self, 
        user_id: int, 
        permission: Permission, 
        company_id: Optional[int] = None
    ) -> bool:
        """
        Check if user has permission (with optional company scope).
        
        TODAY: Maps permission to role flags (e.g., Permission.EVENTS_CREATE → role.can_manage_events)
        FUTURE: Queries Permission database table
        
        This signature is stable and will not change during PBAC migration.
        """
        
    def get_user_permissions(
        self, 
        user_id: int, 
        company_id: Optional[int] = None
    ) -> List[Permission]:
        """
        Get all permissions for a user (with optional company scope).
        
        TODAY: Derives permissions from role flags
        FUTURE: Queries Permission table directly
        
        Returns: List of Permission enum values
        """
```

**Permission Enum (Comprehensive):**
```python
class Permission(str, Enum):
    # Company Management
    COMPANY_SETTINGS_VIEW = "company:settings:view"
    COMPANY_SETTINGS_EDIT = "company:settings:edit"
    COMPANY_BILLING_VIEW = "company:billing:view"
    COMPANY_BILLING_EDIT = "company:billing:edit"
    
    # User Management
    USERS_VIEW = "users:view"
    USERS_INVITE = "users:invite"
    USERS_EDIT = "users:edit"
    USERS_DELETE = "users:delete"
    USERS_ASSIGN_ROLES = "users:assign_roles"
    
    # Event Management
    EVENTS_VIEW = "events:view"
    EVENTS_CREATE = "events:create"
    EVENTS_EDIT = "events:edit"
    EVENTS_DELETE = "events:delete"
    EVENTS_PUBLISH = "events:publish"
    
    # Form Management
    FORMS_VIEW = "forms:view"
    FORMS_CREATE = "forms:create"
    FORMS_EDIT = "forms:edit"
    FORMS_DELETE = "forms:delete"
    
    # Data & Reports
    DATA_EXPORT = "data:export"
    REPORTS_VIEW = "reports:view"
    REPORTS_CREATE = "reports:create"
    ANALYTICS_VIEW = "analytics:view"
```

**Implementation (Phase 1 - Role Flags):**
```python
# Story 1.8 implementation maps permissions to role flags
def has_permission(self, user_id, permission, company_id):
    role = self._get_company_role(user_id, company_id)
    
    permission_map = {
        Permission.EVENTS_CREATE: role.can_manage_events,
        Permission.EVENTS_EDIT: role.can_manage_events,
        Permission.DATA_EXPORT: role.can_export_data,
        Permission.USERS_INVITE: role.can_manage_users,
        # ... complete mapping
    }
    
    return permission_map.get(permission, False)
```

**Implementation (Phase 2 - Year 2-3, Permission Table):**
```python
# Future migration: Only this implementation changes, public API stays same
def has_permission(self, user_id, permission, company_id):
    return db.query(Permission).join(
        RolePermission
    ).filter(
        UserCompany.user_id == user_id,
        UserCompany.company_id == company_id,
        Permission.code == permission
    ).first() is not None
```

#### Frontend Permission Hook (TypeScript/React)

**Module:** `frontend/src/hooks/usePermissions.ts`

**Purpose:** React hook that provides permission checking for UI components

**Public API (Stable - Never Changes):**
```typescript
export type Permission = 
  | 'company:settings:view'
  | 'company:settings:edit'
  | 'users:invite'
  | 'events:create'
  | 'data:export'
  // ... complete list matching backend

interface PermissionContext {
  hasPermission: (permission: Permission) => boolean;
  hasAnyPermission: (permissions: Permission[]) => boolean;
  hasAllPermissions: (permissions: Permission[]) => boolean;
  permissions: Permission[]; // Full list for debugging
}

export function usePermissions(companyId?: number): PermissionContext {
  // TODAY: Derives permissions from user.company_role flags
  // FUTURE: Uses user.permissions array from API
  
  // Public API never changes, only internal implementation
}
```

**Usage in Components (Never Changes):**
```typescript
function EventDashboard() {
  const { hasPermission } = usePermissions();
  
  return (
    <div>
      {hasPermission('events:create') && <CreateEventButton />}
      
      <PermissionGate permission="data:export">
        <ExportButton />
      </PermissionGate>
    </div>
  );
}
```

#### Migration Path (Year 2-3)

When the platform needs granular permissions (enterprise clients, custom roles), the migration is localized:

**Database Changes:**
```sql
-- Add Permission table
CREATE TABLE [Permission] (
    PermissionID BIGINT PRIMARY KEY,
    PermissionCode NVARCHAR(50), -- 'events:create'
    PermissionName NVARCHAR(100),
    Category NVARCHAR(50),
    ...
);

-- Add RolePermission junction table
CREATE TABLE [RolePermission] (
    UserCompanyRoleID BIGINT,
    PermissionID BIGINT,
    ...
);
```

**Backend Changes (2 files):**
1. `backend/modules/permissions/service.py` - Update private methods only
2. `backend/routes/auth.py` - Change API response to include permissions list

**Frontend Changes (1 file):**
1. `frontend/src/hooks/usePermissions.ts` - Update implementation (10 lines)

**Application Code Changes:**
- **Zero component changes** (all use `hasPermission()` abstraction)
- **Zero service changes** (all use `PermissionService` abstraction)
- **Zero test changes** (test against stable API)

**Estimated Migration Effort:** 2-3 weeks (vs. 8-12 weeks without abstraction)

#### Design Principles

1. **Stable Public APIs:** `has_permission()` signature never changes
2. **Implementation Hiding:** Private methods can change freely
3. **Permission Thinking:** Even with roles, think in terms of permissions
4. **Future-Ready:** Design assumes evolution to PBAC
5. **Zero Breaking Changes:** Migration is internal implementation change

This architecture is implemented in Story 1.8 (Role Management) and used by Stories 1.5-1.7 (Team features and RBAC middleware).

### Data Models and Contracts

**Database Schema Design (Dimitri's Domain Analysis)**

The Epic 1 implementation uses three comprehensive domain schemas designed by Dimitri and validated by Solomon:

#### **User Domain Schema (5 Tables)**
```sql
-- Lookup Tables (2)
UserStatus (StatusCode, DisplayName, Description, AllowLogin, ...)
InvitationStatus (StatusCode, DisplayName, CanResend, CanCancel, IsFinalState, ...)

-- Core Tables (3)  
User (UserID, Email, PasswordHash, FirstName, LastName, Status, OnboardingComplete, 
      EmailVerificationToken, PasswordResetToken, SessionToken, AccessTokenVersion, 
      RefreshTokenVersion, FailedLoginCount, LockedUntil, ...)
      
UserCompany (UserCompanyID, UserID, CompanyID, Role, Status, IsDefaultCompany, 
             JoinedDate, JoinedVia, InvitedByUserID, ...)
             
Invitation (InvitationID, CompanyID, InvitedByUserID, InvitedEmail, InvitedFirstName, 
           InvitedLastName, AssignedRole, InvitationToken, Status, ExpiresAt, ...)
```

**Key Features:**
- **Multi-Company Access**: UserCompany many-to-many table enables freelancers/consultants to join multiple companies
- **Status Lookup Tables**: Architectural improvement over CHECK constraints - add statuses without schema migration
- **JWT Session Management**: AccessTokenVersion + RefreshTokenVersion for "logout all devices" functionality
- **Brute Force Protection**: FailedLoginCount + LockedUntil (5 failed attempts = 15 min lockout)
- **Full Audit Trail**: CreatedBy, UpdatedBy, DeletedBy on all tables (Solomon's standards)

#### **Company Domain Schema (4 Tables + Enhanced ABR Cache)**
```sql
-- Core Entity (1)
Company (CompanyID, Name, LegalName, Website, Phone, Industry, ParentCompanyID, ...)

-- Extension Tables (3) - Role-Specific Context
CompanyCustomerDetails (CompanyID, SubscriptionPlan, SubscriptionStatus, BillingCompanyID, 
                       TestThreshold, AnalyticsOptOut, MaxUsers, ...)
                       
CompanyBillingDetails (CompanyID, ABN, GSTRegistered, TaxInvoiceName, BillingEmail, 
                      BillingAddress, FirstInvoiceDate, IsLocked, ABNLastVerified, ...)
                      
CompanyOrganizerDetails (CompanyID, PublicProfileName, Description, LogoUrl, 
                        BrandColorPrimary, ContactEmail, OrganizerSource, IsPublic, ...)

-- Enhanced ABR Search Cache (NEW)
ABRSearchCache (SearchType, SearchKey, ResultIndex, SearchResult, CreatedAt, ExpiresAt, ...)
-- SearchType: 'ABN', 'ACN', 'Name'
-- SearchKey: ABN (11 digits), ACN (9 digits), or normalized company name
-- ResultIndex: For multi-result searches (0 for single results)
-- SearchResult: JSON containing full ABR API response
```

**Key Features:**
- **Multi-Role Support**: Same company can be customer + organizer + billing entity
- **Enhanced ABR Search**: Multi-search capability (ABN, ACN, Company Name) with smart auto-detection
- **Enterprise-Grade Caching**: 300x faster cached results, 40% API cost reduction
- **Australian Tax Compliance**: ABN validation, GST calculation, billing entity locking after first invoice
- **Parent-Subsidiary**: Hierarchical company relationships for enterprise billing
- **Branch Company Scenarios**: Support for cross-branch invitations and company switching
- **Smart Search UX**: ~90% search success rate (up from ~20%) with intuitive multi-search interface

#### **SQLAlchemy Models (Backend Implementation)**
```python
# User Models
class UserStatus(Base):
    __tablename__ = "UserStatus"
    StatusCode = Column(NVARCHAR(20), primary_key=True)
    DisplayName = Column(NVARCHAR(50), nullable=False)
    AllowLogin = Column(Boolean, nullable=False)

class User(Base):
    __tablename__ = "User"
    UserID = Column(BigInteger, primary_key=True, autoincrement=True)
    Email = Column(NVARCHAR(100), unique=True, nullable=False)
    PasswordHash = Column(NVARCHAR(255), nullable=False)
    FirstName = Column(NVARCHAR(100), nullable=False)
    LastName = Column(NVARCHAR(100), nullable=False)
    Status = Column(NVARCHAR(20), ForeignKey("UserStatus.StatusCode"))
    OnboardingComplete = Column(Boolean, default=False)
    EmailVerificationToken = Column(NVARCHAR(255), nullable=True)
    PasswordResetToken = Column(NVARCHAR(255), nullable=True)
    SessionToken = Column(NVARCHAR(255), nullable=True)
    AccessTokenVersion = Column(Integer, default=1)
    RefreshTokenVersion = Column(Integer, default=1)
    FailedLoginCount = Column(Integer, default=0)
    LockedUntil = Column(DATETIME2, nullable=True)
    # ... audit trail fields

class UserCompany(Base):
    __tablename__ = "UserCompany"
    UserCompanyID = Column(BigInteger, primary_key=True, autoincrement=True)
    UserID = Column(BigInteger, ForeignKey("User.UserID"))
    CompanyID = Column(BigInteger, ForeignKey("Company.CompanyID"))
    Role = Column(NVARCHAR(20), default="company_user")
    IsDefaultCompany = Column(Boolean, default=False)
    Status = Column(NVARCHAR(20), default="active")
    JoinedDate = Column(DATETIME2, default=datetime.utcnow)
    JoinedVia = Column(NVARCHAR(20), nullable=False)
```

# Company Models  
class Company(Base):
    __tablename__ = "Company"
    CompanyID = Column(BigInteger, primary_key=True, autoincrement=True)
    Name = Column(NVARCHAR(200), nullable=False)
    LegalName = Column(NVARCHAR(200), nullable=True)
    Website = Column(NVARCHAR(500), nullable=True)
    Phone = Column(NVARCHAR(20), nullable=True)
    Industry = Column(NVARCHAR(100), nullable=True)
    ParentCompanyID = Column(BigInteger, ForeignKey("Company.CompanyID"), nullable=True)
    # ... audit trail fields

class CompanyBillingDetails(Base):
    __tablename__ = "CompanyBillingDetails"
    CompanyID = Column(BigInteger, ForeignKey("Company.CompanyID"), primary_key=True)
    ABN = Column(NVARCHAR(11), unique=True, nullable=False)
    GSTRegistered = Column(Boolean, nullable=False)
    TaxInvoiceName = Column(NVARCHAR(200), nullable=False)
    BillingEmail = Column(NVARCHAR(100), nullable=False)
    BillingAddress = Column(NVARCHAR(500), nullable=False)
    IsLocked = Column(Boolean, default=False)
    FirstInvoiceDate = Column(DATETIME2, nullable=True)
    # ... other fields

# Enhanced ABR Search Cache Model
class ABRSearchCache(Base):
    __tablename__ = "ABRSearchCache"
    SearchType = Column(NVARCHAR(20), primary_key=True)  # 'ABN', 'ACN', 'Name'
    SearchKey = Column(NVARCHAR(200), primary_key=True)  # ABN, ACN, or normalized name
    ResultIndex = Column(Integer, primary_key=True)      # 0 for single results
    SearchResult = Column(JSON, nullable=False)          # Full ABR API response
    CreatedAt = Column(DATETIME2, default=datetime.utcnow, nullable=False)
    ExpiresAt = Column(DATETIME2, nullable=False)        # 30-day TTL
    HitCount = Column(Integer, default=0)                # Cache analytics
    LastHitAt = Column(DATETIME2, nullable=True)
```

#### **Branch Company Scenarios & Company Switching (NEW)**

**Business Use Cases:**

**Scenario 1: Marketing Manager → Branch Event Manager**
```
Marketing Manager (Head Office) invites Event Manager (Branch Office)
- Both users belong to different companies (Head Office vs Branch)
- Branch pays for their own events (separate billing)
- Need to establish relationship between companies
```

**Scenario 2: Branch Event Manager → Head Office Marketing Manager**
```
Branch Event Manager discovers platform and invites Head Office Marketing Manager
- Branch user invites Head Office user
- Head Office user needs to join Branch company or create relationship
- Company switching capability required
```

**Solution Architecture:**

```python
class CompanyRelationship(Base):
    __tablename__ = "CompanyRelationship"
    RelationshipID = Column(BigInteger, primary_key=True, autoincrement=True)
    ParentCompanyID = Column(BigInteger, ForeignKey("Company.CompanyID"))
    ChildCompanyID = Column(BigInteger, ForeignKey("Company.CompanyID"))
    RelationshipType = Column(NVARCHAR(50), nullable=False)  # 'branch', 'subsidiary', 'partner'
    Status = Column(NVARCHAR(20), default="active")  # 'active', 'suspended', 'terminated'
    EstablishedBy = Column(BigInteger, ForeignKey("User.UserID"))  # Who created the relationship
    EstablishedAt = Column(DATETIME2, default=datetime.utcnow)
    # ... audit trail fields

class CompanySwitchRequest(Base):
    __tablename__ = "CompanySwitchRequest"
    RequestID = Column(BigInteger, primary_key=True, autoincrement=True)
    UserID = Column(BigInteger, ForeignKey("User.UserID"))
    FromCompanyID = Column(BigInteger, ForeignKey("Company.CompanyID"))
    ToCompanyID = Column(BigInteger, ForeignKey("Company.CompanyID"))
    RequestType = Column(NVARCHAR(50), nullable=False)  # 'invitation_accepted', 'company_switch', 'relationship_join'
    Status = Column(NVARCHAR(20), default="pending")  # 'pending', 'approved', 'rejected'
    RequestedBy = Column(BigInteger, ForeignKey("User.UserID"))
    RequestedAt = Column(DATETIME2, default=datetime.utcnow)
    # ... audit trail fields
```

**Enhanced Invitation Flow:**
```python
class EnhancedInvitationService:
    async def send_cross_company_invitation(self, inviter_user_id: int, 
                                          invited_email: str, 
                                          target_company_id: int,
                                          relationship_context: str = None):
        """Handle invitations between different companies"""
        
        # Check if companies have existing relationship
        relationship = await self.get_company_relationship(
            inviter_user_id, target_company_id
        )
        
        if not relationship:
            # Create company relationship request
            await self.create_relationship_request(
                from_company_id=inviter_user.company_id,
                to_company_id=target_company_id,
                relationship_type="branch",
                established_by=inviter_user_id
            )
        
        # Send invitation with relationship context
        invitation = await self.create_invitation(
            company_id=target_company_id,
            invited_email=invited_email,
            relationship_context=relationship_context,
            cross_company=True
        )
        
        return invitation
```

**Company Switching UX:**
```typescript
// Frontend: Company Switcher Component
const CompanySwitcher = () => {
  const [companies, setCompanies] = useState([]);
  const [currentCompany, setCurrentCompany] = useState(null);
  
  const switchCompany = async (companyId: number) => {
    // Validate user has access to target company
    const hasAccess = await validateCompanyAccess(companyId);
    
    if (!hasAccess) {
      // Show "Request Access" modal
      showCompanyAccessRequestModal(companyId);
      return;
    }
    
    // Switch company context
    await switchCompanyContext(companyId);
    setCurrentCompany(companyId);
  };
  
  return (
    <Dropdown>
      {companies.map(company => (
        <DropdownItem 
          key={company.id}
          onClick={() => switchCompany(company.id)}
          active={company.id === currentCompany}
        >
          {company.name} {company.relationship_type && `(${company.relationship_type})`}
        </DropdownItem>
      ))}
      <DropdownItem onClick={showJoinCompanyModal}>
        + Join Another Company
      </DropdownItem>
    </Dropdown>
  );
};
```

#### **Application Specification System (NEW)**

**Business Requirement:**
- **Zero Hard-Coding**: All application parameters stored in database
- **Multi-Level Configuration**: Global, Country, and Environment-specific settings
- **Runtime Configuration**: Changes without code deployment
- **Audit Trail**: Track all configuration changes
- **Environment Support**: Dev, Staging, Production configurations

**Option 1: Hierarchical Application Specification (Recommended)**

```sql
-- Global Application Parameters (applies everywhere)
CREATE TABLE [ApplicationSpecification] (
    SpecificationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Category NVARCHAR(100) NOT NULL,              -- 'authentication', 'validation', 'business_rules'
    ParameterName NVARCHAR(200) NOT NULL,         -- 'password_min_length', 'jwt_expiry_minutes'
    ParameterValue NVARCHAR(MAX) NOT NULL,        -- '8', '15', '{"enabled": true, "retries": 3}'
    DataType NVARCHAR(50) NOT NULL,               -- 'string', 'integer', 'boolean', 'json', 'decimal'
    Description NVARCHAR(500) NOT NULL,           -- Human-readable description
    IsActive BIT NOT NULL DEFAULT 1,              -- Enable/disable parameter
    SortOrder INT NOT NULL DEFAULT 999,           -- Display order
    -- ... audit trail fields
    CONSTRAINT UK_ApplicationSpecification_Category_Parameter 
        UNIQUE (Category, ParameterName)
);

-- Country-Specific Parameters (overrides global)
CREATE TABLE [CountryApplicationSpecification] (
    CountrySpecificationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CountryID BIGINT NOT NULL,
    Category NVARCHAR(100) NOT NULL,              -- Same categories as global
    ParameterName NVARCHAR(200) NOT NULL,         -- Same parameter names as global
    ParameterValue NVARCHAR(MAX) NOT NULL,        -- Country-specific value
    DataType NVARCHAR(50) NOT NULL,               -- Same data types as global
    Description NVARCHAR(500) NULL,               -- Country-specific description
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- ... audit trail fields
    CONSTRAINT FK_CountryApplicationSpecification_Country 
        FOREIGN KEY (CountryID) REFERENCES [Country](CountryID),
    CONSTRAINT UK_CountryApplicationSpecification_Country_Category_Parameter 
        UNIQUE (CountryID, Category, ParameterName)
);

-- Environment-Specific Parameters (overrides country and global)
CREATE TABLE [EnvironmentApplicationSpecification] (
    EnvironmentSpecificationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    EnvironmentName NVARCHAR(50) NOT NULL,        -- 'development', 'staging', 'production'
    CountryID BIGINT NULL,                        -- NULL = applies to all countries
    Category NVARCHAR(100) NOT NULL,
    ParameterName NVARCHAR(200) NOT NULL,
    ParameterValue NVARCHAR(MAX) NOT NULL,
    DataType NVARCHAR(50) NOT NULL,
    Description NVARCHAR(500) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- ... audit trail fields
    CONSTRAINT FK_EnvironmentApplicationSpecification_Country 
        FOREIGN KEY (CountryID) REFERENCES [Country](CountryID),
    CONSTRAINT UK_EnvironmentApplicationSpecification_Environment_Country_Category_Parameter 
        UNIQUE (EnvironmentName, ISNULL(CountryID, 0), Category, ParameterName)
);
```

**Resolution Priority (Highest to Lowest):**
1. **Environment + Country** (most specific)
2. **Environment + Global** (environment override)
3. **Country** (country override)
4. **Global** (default fallback)

---

## **Application Specification Service Implementation**

```python
class ApplicationSpecificationService:
    def __init__(self, environment: str = "production"):
        self.environment = environment
        self.cache = {}  # In-memory cache for performance
    
    async def get_parameter(self, category: str, parameter_name: str, 
                          country_id: int = None) -> Any:
        """Get parameter value with proper resolution priority"""
        
        cache_key = f"{self.environment}:{country_id}:{category}:{parameter_name}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Priority 1: Environment + Country specific
        if country_id:
            env_country_value = await self._get_environment_country_parameter(
                category, parameter_name, country_id
            )
            if env_country_value is not None:
                self.cache[cache_key] = env_country_value
                return env_country_value
        
        # Priority 2: Environment + Global
        env_global_value = await self._get_environment_global_parameter(
            category, parameter_name
        )
        if env_global_value is not None:
            self.cache[cache_key] = env_global_value
            return env_global_value
        
        # Priority 3: Country specific
        if country_id:
            country_value = await self._get_country_parameter(
                category, parameter_name, country_id
            )
            if country_value is not None:
                self.cache[cache_key] = country_value
                return country_value
        
        # Priority 4: Global default
        global_value = await self._get_global_parameter(category, parameter_name)
        if global_value is not None:
            self.cache[cache_key] = global_value
            return global_value
        
        raise ValueError(f"Parameter not found: {category}.{parameter_name}")
    
    async def get_authentication_config(self, country_id: int = None) -> Dict:
        """Get all authentication parameters for a country"""
        return {
            'password_min_length': await self.get_parameter('authentication', 'password_min_length', country_id),
            'password_require_special_chars': await self.get_parameter('authentication', 'password_require_special_chars', country_id),
            'jwt_access_token_expiry_minutes': await self.get_parameter('authentication', 'jwt_access_token_expiry_minutes', country_id),
            'jwt_refresh_token_expiry_days': await self.get_parameter('authentication', 'jwt_refresh_token_expiry_days', country_id),
            'max_failed_login_attempts': await self.get_parameter('authentication', 'max_failed_login_attempts', country_id),
            'account_lockout_minutes': await self.get_parameter('authentication', 'account_lockout_minutes', country_id),
        }
    
    async def get_validation_config(self, country_id: int = None) -> Dict:
        """Get all validation parameters for a country"""
        return {
            'email_verification_expiry_hours': await self.get_parameter('validation', 'email_verification_expiry_hours', country_id),
            'password_reset_expiry_hours': await self.get_parameter('validation', 'password_reset_expiry_hours', country_id),
            'invitation_expiry_days': await self.get_parameter('validation', 'invitation_expiry_days', country_id),
            'company_name_min_length': await self.get_parameter('validation', 'company_name_min_length', country_id),
            'company_name_max_length': await self.get_parameter('validation', 'company_name_max_length', country_id),
        }
    
    async def get_business_rules_config(self, country_id: int = None) -> Dict:
        """Get all business rules for a country"""
        return {
            'default_test_threshold': await self.get_parameter('business_rules', 'default_test_threshold', country_id),
            'free_tier_max_events': await self.get_parameter('business_rules', 'free_tier_max_events', country_id),
            'free_tier_max_users': await self.get_parameter('business_rules', 'free_tier_max_users', country_id),
            'abn_cache_ttl_days': await self.get_parameter('business_rules', 'abn_cache_ttl_days', country_id),
            'max_invitations_per_day': await self.get_parameter('business_rules', 'max_invitations_per_day', country_id),
        }
    
    async def invalidate_cache(self, category: str = None, parameter_name: str = None):
        """Invalidate cache when parameters are updated"""
        if category and parameter_name:
            # Invalidate specific parameter
            keys_to_remove = [key for key in self.cache.keys() 
                            if f"{category}:{parameter_name}" in key]
        else:
            # Invalidate all cache
            keys_to_remove = list(self.cache.keys())
        
        for key in keys_to_remove:
            del self.cache[key]
```

---

## **Sample Configuration Data**

```sql
-- Global Default Parameters
INSERT INTO [ApplicationSpecification] (Category, ParameterName, ParameterValue, DataType, Description) VALUES
-- Authentication
('authentication', 'password_min_length', '8', 'integer', 'Minimum password length'),
('authentication', 'password_require_special_chars', 'true', 'boolean', 'Require special characters in password'),
('authentication', 'jwt_access_token_expiry_minutes', '15', 'integer', 'JWT access token expiry in minutes'),
('authentication', 'jwt_refresh_token_expiry_days', '7', 'integer', 'JWT refresh token expiry in days'),
('authentication', 'max_failed_login_attempts', '5', 'integer', 'Max failed login attempts before lockout'),
('authentication', 'account_lockout_minutes', '15', 'integer', 'Account lockout duration in minutes'),

-- Validation
('validation', 'email_verification_expiry_hours', '24', 'integer', 'Email verification token expiry in hours'),
('validation', 'password_reset_expiry_hours', '1', 'integer', 'Password reset token expiry in hours'),
('validation', 'invitation_expiry_days', '7', 'integer', 'Team invitation expiry in days'),
('validation', 'company_name_min_length', '2', 'integer', 'Minimum company name length'),
('validation', 'company_name_max_length', '200', 'integer', 'Maximum company name length'),

-- Business Rules
('business_rules', 'default_test_threshold', '5', 'integer', 'Default preview tests required before publish'),
('business_rules', 'free_tier_max_events', '10', 'integer', 'Maximum events for free tier'),
('business_rules', 'free_tier_max_users', '5', 'integer', 'Maximum users for free tier'),
('business_rules', 'abn_cache_ttl_days', '30', 'integer', 'ABN lookup cache TTL in days'),
('business_rules', 'max_invitations_per_day', '50', 'integer', 'Maximum invitations per company per day');

-- Australia-Specific Overrides
INSERT INTO [CountryApplicationSpecification] (CountryID, Category, ParameterName, ParameterValue, DataType, Description) VALUES
-- Australia uses AU CountryID = 1
(1, 'validation', 'company_name_min_length', '3', 'integer', 'Australia requires longer company names'),
(1, 'business_rules', 'abn_cache_ttl_days', '30', 'integer', 'ABR API allows 30-day caching for Australia');
```

---

## **Usage in Application Code**

```python
# Instead of hard-coded values
# password_min_length = 8  # HARD-CODED ❌

# Use configuration service
config_service = ApplicationSpecificationService(environment="production")

# Authentication validation
auth_config = await config_service.get_authentication_config(country_id=1)
password_min_length = auth_config['password_min_length']  # From database ✅

# JWT token generation
jwt_config = await config_service.get_authentication_config(country_id=1)
access_token_expiry = jwt_config['jwt_access_token_expiry_minutes']

# Business rules
business_config = await config_service.get_business_rules_config(country_id=1)
max_events = business_config['free_tier_max_events']
```

---

## **Frontend Configuration Hook**

```typescript
const useApplicationConfig = (countryId?: number) => {
  const [config, setConfig] = useState({});
  
  useEffect(() => {
    const loadConfig = async () => {
      const response = await fetch(`/api/config?country_id=${countryId || ''}`);
      const configData = await response.json();
      setConfig(configData);
    };
    
    loadConfig();
  }, [countryId]);
  
  const getConfig = (category: string, parameter: string) => {
    return config[category]?.[parameter];
  };
  
  return { config, getConfig };
};

// Usage in components
const SignupForm = ({ countryId }) => {
  const { getConfig } = useApplicationConfig(countryId);
  
  const passwordMinLength = getConfig('authentication', 'password_min_length') || 8;
  const requireSpecialChars = getConfig('authentication', 'password_require_special_chars') || true;
  
  return (
    <input 
      type="password"
      minLength={passwordMinLength}
      pattern={requireSpecialChars ? ".*[!@#$%^&*].*" : ".*"}
      placeholder={`Password (min ${passwordMinLength} chars${requireSpecialChars ? ', special chars required' : ''})`}
    />
  );
};
```

---

## **Recommendation: Option 1 (Hierarchical)**

I recommend **Option 1** because it provides:

1. **Maximum Flexibility**: Global → Country → Environment overrides
2. **Environment Support**: Different configs for Dev/Staging/Production
3. **Future-Proof**: Can add more hierarchy levels if needed
4. **Clear Resolution**: Explicit priority order
5. **Performance**: Caching and efficient lookups

This system will **completely eliminate hard-coding** and provide the flexibility you need for international expansion and business rule changes without code deployments.

#### **International Foundation & Web Properties (NEW)**

**Business Requirements:**
- **Web Properties**: Sort order, colors, active status for flexible UI
- **Country-Specific Validation**: Different phone/postal code rules per country
- **International Expansion**: Quick setup for new markets
- **Validation Rule Engine**: Flexible system for different countries

**Enhanced Schema Design:**

```sql
-- Enhanced Country Web Properties
CREATE TABLE [CountryWebProperties] (
    CountryWebPropertiesID BIGINT IDENTITY(1,1) NOT NULL, -- Primary key
    CountryID BIGINT NOT NULL,                   -- Foreign key to Country
    SortOrder INT NOT NULL DEFAULT 999,          -- Display order in dropdowns
    DisplayColor NVARCHAR(7) NULL,               -- Hex color for UI theming
    IsActive BIT NOT NULL DEFAULT 1,             -- Show/hide in UI
    LaunchPriority INT NULL,                     -- Expansion priority (1=highest)
    MarketingName NVARCHAR(100) NULL,            -- Marketing-friendly name
    SupportEmail NVARCHAR(100) NULL,             -- Country-specific support
    LegalJurisdiction NVARCHAR(100) NULL,        -- Legal entity jurisdiction
    TimezoneOffset NVARCHAR(10) NULL,            -- UTC offset (e.g., "+10:00")
    DateFormat NVARCHAR(20) NOT NULL DEFAULT 'DD/MM/YYYY', -- Local date format
    CurrencySymbol NVARCHAR(5) NOT NULL DEFAULT '$', -- Currency display symbol
    CurrencyPosition NVARCHAR(10) NOT NULL DEFAULT 'before', -- 'before' or 'after'
    
    -- Audit trail fields (Solomon's standards)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT PK_CountryWebProperties PRIMARY KEY (CountryWebPropertiesID),
    CONSTRAINT FK_CountryWebProperties_Country 
        FOREIGN KEY (CountryID) REFERENCES [Country](CountryID),
    CONSTRAINT FK_CountryWebProperties_CreatedBy 
        FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_CountryWebProperties_UpdatedBy 
        FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_CountryWebProperties_DeletedBy 
        FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    CONSTRAINT CK_CountryWebProperties_DisplayColor 
        CHECK (DisplayColor IS NULL OR DisplayColor LIKE '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]'),
    CONSTRAINT CK_CountryWebProperties_LaunchPriority 
        CHECK (LaunchPriority IS NULL OR LaunchPriority > 0),
    CONSTRAINT CK_CountryWebProperties_SortOrder 
        CHECK (SortOrder > 0)
);

-- Flexible Validation Rules Engine
CREATE TABLE [ValidationRule] (
    ValidationRuleID BIGINT IDENTITY(1,1) NOT NULL, -- Primary key
    CountryID BIGINT NOT NULL,
    RuleType NVARCHAR(50) NOT NULL,              -- 'phone', 'postal_code', 'tax_id', 'address'
    RuleName NVARCHAR(100) NOT NULL,             -- Human-readable name
    ValidationPattern NVARCHAR(500) NOT NULL,    -- Regex pattern
    ErrorMessage NVARCHAR(200) NOT NULL,         -- User-friendly error message
    IsActive BIT NOT NULL DEFAULT 1,             -- Enable/disable rule
    SortOrder INT NOT NULL DEFAULT 999,          -- Rule precedence
    MinLength INT NULL,                          -- Minimum length (for phone)
    MaxLength INT NULL,                          -- Maximum length
    ExampleValue NVARCHAR(100) NULL,             -- Example valid value
    
    -- Audit trail fields (Solomon's standards)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT PK_ValidationRule PRIMARY KEY (ValidationRuleID),
    CONSTRAINT FK_ValidationRule_Country 
        FOREIGN KEY (CountryID) REFERENCES [Country](CountryID),
    CONSTRAINT FK_ValidationRule_CreatedBy 
        FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_ValidationRule_UpdatedBy 
        FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_ValidationRule_DeletedBy 
        FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    CONSTRAINT CK_ValidationRule_RuleType 
        CHECK (RuleType IN ('phone', 'postal_code', 'tax_id', 'address', 'email', 'url')),
    CONSTRAINT CK_ValidationRule_SortOrder 
        CHECK (SortOrder > 0),
    CONSTRAINT CK_ValidationRule_MinLength 
        CHECK (MinLength IS NULL OR MinLength > 0),
    CONSTRAINT CK_ValidationRule_MaxLength 
        CHECK (MaxLength IS NULL OR MaxLength > 0),
    CONSTRAINT CK_ValidationRule_LengthRange 
        CHECK (MinLength IS NULL OR MaxLength IS NULL OR MinLength <= MaxLength)
);

-- Enhanced Lookup Tables with Web Properties
CREATE TABLE [LookupTableWebProperties] (
    LookupTableWebPropertiesID BIGINT IDENTITY(1,1) NOT NULL, -- Primary key
    TableName NVARCHAR(100) NOT NULL,            -- Lookup table name (unique)
    DisplayName NVARCHAR(100) NOT NULL,          -- Human-readable table name
    SortOrder INT NOT NULL DEFAULT 999,          -- Display order
    DisplayColor NVARCHAR(7) NULL,               -- UI theme color
    IsActive BIT NOT NULL DEFAULT 1,             -- Show/hide in admin
    IconClass NVARCHAR(50) NULL,                 -- CSS icon class
    Description NVARCHAR(500) NULL,              -- Table description
    
    -- Audit trail fields (Solomon's standards)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT PK_LookupTableWebProperties PRIMARY KEY (LookupTableWebPropertiesID),
    CONSTRAINT UQ_LookupTableWebProperties_TableName UNIQUE (TableName),
    CONSTRAINT FK_LookupTableWebProperties_CreatedBy 
        FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_LookupTableWebProperties_UpdatedBy 
        FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_LookupTableWebProperties_DeletedBy 
        FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    CONSTRAINT CK_LookupTableWebProperties_DisplayColor 
        CHECK (DisplayColor IS NULL OR DisplayColor LIKE '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]'),
    CONSTRAINT CK_LookupTableWebProperties_SortOrder 
        CHECK (SortOrder > 0)
);

-- Enhanced Lookup Values with Web Properties
CREATE TABLE [LookupValueWebProperties] (
    LookupValueWebPropertiesID BIGINT IDENTITY(1,1) NOT NULL, -- Primary key
    TableName NVARCHAR(100) NOT NULL,            -- References lookup table name
    ValueCode NVARCHAR(50) NOT NULL,             -- References lookup value code
    SortOrder INT NOT NULL DEFAULT 999,          -- Display order in dropdowns
    DisplayColor NVARCHAR(7) NULL,               -- UI color coding
    IconClass NVARCHAR(50) NULL,                 -- CSS icon
    TooltipText NVARCHAR(200) NULL,              -- Hover tooltip
    IsDefault BIT NOT NULL DEFAULT 0,            -- Default selection
    IsActive BIT NOT NULL DEFAULT 1,             -- Show/hide in UI
    
    -- Audit trail fields (Solomon's standards)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    CONSTRAINT PK_LookupValueWebProperties PRIMARY KEY (LookupValueWebPropertiesID),
    CONSTRAINT UQ_LookupValueWebProperties_TableName_ValueCode UNIQUE (TableName, ValueCode),
    CONSTRAINT FK_LookupValueWebProperties_Table 
        FOREIGN KEY (TableName) REFERENCES [LookupTableWebProperties](TableName),
    CONSTRAINT FK_LookupValueWebProperties_CreatedBy 
        FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_LookupValueWebProperties_UpdatedBy 
        FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_LookupValueWebProperties_DeletedBy 
        FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    CONSTRAINT CK_LookupValueWebProperties_DisplayColor 
        CHECK (DisplayColor IS NULL OR DisplayColor LIKE '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]'),
    CONSTRAINT CK_LookupValueWebProperties_SortOrder 
        CHECK (SortOrder > 0)
);
```

**Country-Specific Validation Engine:**
```python
class ValidationRuleEngine:
    def __init__(self, country_id: int):
        self.country_id = country_id
        self.rules = self.load_validation_rules()
    
    def validate_phone(self, phone: str) -> ValidationResult:
        """Validate phone number using country-specific rules"""
        phone_rules = self.rules.get('phone', [])
        
        for rule in sorted(phone_rules, key=lambda x: x.sort_order):
            if re.match(rule.validation_pattern, phone):
                return ValidationResult(valid=True, rule=rule)
        
        return ValidationResult(
            valid=False, 
            error_message=phone_rules[0].error_message if phone_rules else "Invalid phone format"
        )
    
    def validate_postal_code(self, postal_code: str) -> ValidationResult:
        """Validate postal code using country-specific rules"""
        postal_rules = self.rules.get('postal_code', [])
        
        for rule in sorted(postal_rules, key=lambda x: x.sort_order):
            if re.match(rule.validation_pattern, postal_code):
                return ValidationResult(valid=True, rule=rule)
        
        return ValidationResult(
            valid=False,
            error_message=postal_rules[0].error_message if postal_rules else "Invalid postal code"
        )
```

**International Expansion Setup:**
```python
class InternationalExpansionService:
    async def setup_new_country(self, country_code: str, 
                               validation_rules: Dict[str, List[Dict]]):
        """Quick setup for new country expansion"""
        
        # 1. Add country with web properties
        country = await self.create_country_with_properties(
            country_code=country_code,
            web_properties={
                'sort_order': 999,
                'display_color': '#0066CC',
                'is_active': True,
                'launch_priority': 5
            }
        )
        
        # 2. Add country-specific validation rules
        for rule_type, rules in validation_rules.items():
            for rule_data in rules:
                await self.create_validation_rule(
                    country_id=country.country_id,
                    rule_type=rule_type,
                    **rule_data
                )
        
        # 3. Activate country in UI
        await self.activate_country_ui(country.country_id)
        
        return country
    
    async def get_country_validation_rules(self, country_id: int) -> Dict[str, List]:
        """Get all validation rules for a country"""
        rules = await self.db.query(ValidationRule).filter(
            ValidationRule.CountryID == country_id,
            ValidationRule.IsActive == True
        ).order_by(ValidationRule.RuleType, ValidationRule.SortOrder).all()
        
        # Group by rule type
        grouped_rules = {}
        for rule in rules:
            if rule.rule_type not in grouped_rules:
                grouped_rules[rule.rule_type] = []
            grouped_rules[rule.rule_type].append(rule)
        
        return grouped_rules
```

**Frontend: Dynamic Validation:**
```typescript
const useCountryValidation = (countryId: number) => {
  const [validationRules, setValidationRules] = useState({});
  
  useEffect(() => {
    // Load country-specific validation rules
    loadValidationRules(countryId).then(setValidationRules);
  }, [countryId]);
  
  const validateField = (fieldType: string, value: string): ValidationResult => {
    const rules = validationRules[fieldType] || [];
    
    for (const rule of rules.sort((a, b) => a.sortOrder - b.sortOrder)) {
      if (new RegExp(rule.validationPattern).test(value)) {
        return { valid: true, rule };
      }
    }
    
    return { 
      valid: false, 
      errorMessage: rules[0]?.errorMessage || "Invalid format" 
    };
  };
  
  return { validateField, validationRules };
};

// Usage in forms
const PhoneInput = ({ countryId, value, onChange }) => {
  const { validateField } = useCountryValidation(countryId);
  const [error, setError] = useState("");
  
  const handleChange = (newValue: string) => {
    const validation = validateField('phone', newValue);
    setError(validation.valid ? "" : validation.errorMessage);
    onChange(newValue);
  };
  
  return (
    <div>
      <input 
        value={value} 
        onChange={(e) => handleChange(e.target.value)}
        placeholder="Enter phone number"
      />
      {error && <span className="error">{error}</span>}
    </div>
  );
};
```

#### **Enhanced ABR Search Services (NEW)**

**Smart Search Detection Logic:**
```python
class ABRSearchService:
    def detect_search_type(self, query: str) -> str:
        """Auto-detect search type based on input format"""
        query = query.strip().replace(" ", "")
        
        if len(query) == 11 and query.isdigit():
            return "abn"  # 11 digits = ABN
        elif len(query) == 9 and query.isdigit():
            return "acn"  # 9 digits = ACN
        else:
            return "name"  # Text = company name search
    
    async def smart_search(self, query: str, search_type: str = "auto") -> SmartCompanySearchResponse:
        """Multi-search capability with smart auto-detection"""
        if search_type == "auto":
            search_type = self.detect_search_type(query)
        
        # Check cache first (300x faster)
        cache_result = await self.cache_service.get_search_result(search_type, query)
        if cache_result:
            return SmartCompanySearchResponse(
                results=cache_result["results"],
                total_results=len(cache_result["results"]),
                search_type=search_type,
                cache_hit=True,
                response_time_ms=5  # Cache hit ~5ms
            )
        
        # API call if not cached (~1500ms)
        api_result = await self.abr_client.search(search_type, query)
        
        # Cache the result (30-day TTL)
        await self.cache_service.set_search_result(search_type, query, api_result)
        
        return SmartCompanySearchResponse(
            results=api_result["results"],
            total_results=len(api_result["results"]),
            search_type=search_type,
            cache_hit=False,
            response_time_ms=1500  # API call ~1500ms
        )
```

**Enterprise-Grade Cache Service:**
```python
class ABRCacheService:
    async def get_search_result(self, search_type: str, search_key: str) -> Optional[Dict]:
        """Get cached search result with TTL validation"""
        # Check if cache entry exists and hasn't expired
        cache_entry = await self.db.query(ABRSearchCache).filter(
            ABRSearchCache.SearchType == search_type,
            ABRSearchCache.SearchKey == search_key,
            ABRSearchCache.ExpiresAt > datetime.utcnow()
        ).first()
        
        if cache_entry:
            # Update hit analytics
            cache_entry.HitCount += 1
            cache_entry.LastHitAt = datetime.utcnow()
            await self.db.commit()
            
            return cache_entry.SearchResult
        
        return None
    
    async def set_search_result(self, search_type: str, search_key: str, result: Dict):
        """Cache search result with 30-day TTL"""
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        # Store each result as separate cache entry for multi-result searches
        for index, search_result in enumerate(result["results"]):
            cache_entry = ABRSearchCache(
                SearchType=search_type,
                SearchKey=search_key,
                ResultIndex=index,
                SearchResult=search_result,
                ExpiresAt=expires_at
            )
            await self.db.add(cache_entry)
        
        await self.db.commit()
```

#### **API Contracts (Request/Response Models)**
```python
# Authentication Endpoints
class SignupRequest(BaseModel):
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserProfile
    company: CompanyProfile
    expires_in: int

# Enhanced Company Search (NEW)
class SmartCompanySearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)
    search_type: Optional[Literal["auto", "abn", "acn", "name"]] = "auto"

class CompanySearchResult(BaseModel):
    abn: str
    acn: Optional[str]
    name: str
    legal_name: Optional[str]
    gst_registered: bool
    entity_type: Optional[str]
    status: str
    business_names: List[str] = []
    address: Optional[Dict[str, str]] = None
    match_type: Literal["exact", "partial", "fuzzy"]

class SmartCompanySearchResponse(BaseModel):
    results: List[CompanySearchResult]
    total_results: int
    search_type: str
    cache_hit: bool
    response_time_ms: int

# Company Onboarding
class CompanyDetailsRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    legal_name: Optional[str] = Field(None, max_length=200)
    abn: str = Field(..., regex=r'^\d{11}$')
    billing_email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    billing_address: str = Field(..., min_length=10, max_length=500)

# Invitation Management
class InviteUserRequest(BaseModel):
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: Literal["company_admin", "company_user"] = "company_user"
```

**Activity Log Model (`backend/models/activity_log.py` - Auth Events Only):**
```python
class ActivityLog(Base):
    __tablename__ = "activity_log"
    
    activity_id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    company_id = Column(UNIQUEIDENTIFIER, ForeignKey("companies.company_id"), nullable=True)
    user_id = Column(UNIQUEIDENTIFIER, ForeignKey("users.user_id"), nullable=True)
    action = Column(Enum(ActivityAction), nullable=False)  # signup, login, email_verified, password_reset, etc.
    entity_type = Column(Enum(EntityType), nullable=False)  # user, company, invitation
    entity_id = Column(UNIQUEIDENTIFIER, nullable=True)
    details_json = Column(NVARCHAR(MAX), nullable=True)  # JSON with additional context
    created_at = Column(DATETIME2, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    company = relationship("Company")
    user = relationship("User")
```

### APIs and Interfaces

**Authentication Endpoints:**

```
POST /api/auth/signup
Request:
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
Response (201):
{
  "message": "Verification email sent. Please check your email.",
  "user_id": "uuid"
}
Error Codes: 400 (invalid email/password), 409 (email already exists)

---

POST /api/auth/verify-email
Request:
{
  "token": "secure-verification-token"
}
Response (200):
{
  "message": "Email verified successfully. Please log in."
}
Error Codes: 400 (invalid token), 410 (token expired)

---

POST /api/auth/login
Request:
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
Response (200):
{
  "access_token": "jwt-token",
  "refresh_token": "jwt-refresh-token",
  "user": {
    "user_id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "company_admin",
    "company_id": "uuid",
    "onboarding_complete": true
  }
}
Error Codes: 401 (invalid credentials), 403 (email not verified)

---

POST /api/auth/refresh
Request:
{
  "refresh_token": "jwt-refresh-token"
}
Response (200):
{
  "access_token": "new-jwt-token"
}
Error Codes: 401 (invalid refresh token)

---

POST /api/auth/reset-password-request
Request:
{
  "email": "user@example.com"
}
Response (200):
{
  "message": "Password reset email sent if account exists."
}
Error Codes: None (always returns 200 for security)

---

POST /api/auth/reset-password
Request:
{
  "token": "secure-reset-token",
  "new_password": "NewSecurePassword123"
}
Response (200):
{
  "message": "Password reset successfully. Please log in."
}
Error Codes: 400 (invalid token), 410 (token expired), 400 (weak password)

---

GET /api/auth/me
Headers: Authorization: Bearer {jwt-token}
Response (200):
{
  "user_id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "company_admin",
  "company_id": "uuid",
  "onboarding_complete": true
}
Error Codes: 401 (unauthorized)

---

POST /api/auth/logout
Headers: Authorization: Bearer {jwt-token}
Response (200):
{
  "message": "Logged out successfully."
}
```

**Onboarding Endpoints:**

```
POST /api/users/onboarding/user-details
Headers: Authorization: Bearer {jwt-token}
Request:
{
  "first_name": "John",
  "last_name": "Doe",
  "role_title": "Marketing Manager",
  "phone_number": "+61412345678"
}
Response (200):
{
  "message": "User details saved.",
  "user": { ...user object... }
}
Error Codes: 400 (validation errors), 401 (unauthorized)

---

POST /api/users/onboarding/company-setup
Headers: Authorization: Bearer {jwt-token}
Request:
{
  "company_name": "Acme Corp",
  "abn": "12345678901",
  "billing_address": {
    "street": "123 Main St",
    "city": "Sydney",
    "state": "NSW",
    "postcode": "2000",
    "country": "Australia"
  },
  "company_phone": "+61298765432",
  "industry": "Technology"
}
Response (200):
{
  "message": "Company created successfully.",
  "company": { ...company object... },
  "user": { ...updated user with company_id and company_admin role... }
}
Error Codes: 400 (validation errors, invalid ABN), 401 (unauthorized)

---

POST /api/users/onboarding/complete
Headers: Authorization: Bearer {jwt-token}
Response (200):
{
  "message": "Onboarding complete. Welcome!",
  "user": { ...user with onboarding_complete=true... }
}
Error Codes: 400 (onboarding not ready), 401 (unauthorized)
```

**Invitation Endpoints:**

```
POST /api/team/invitations
Headers: Authorization: Bearer {jwt-token}
Required Role: company_admin
Request:
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "assigned_role": "company_user"
}
Response (201):
{
  "message": "Invitation sent successfully.",
  "invitation": {
    "invitation_id": "uuid",
    "invited_email": "jane@example.com",
    "status": "pending",
    "expires_at": "2025-10-20T12:00:00Z"
  }
}
Error Codes: 400 (validation), 403 (not company_admin), 409 (user already exists)

---

POST /api/team/invitations/accept
Request:
{
  "invitation_token": "secure-invitation-token",
  "password": "NewUserPassword123"
}
Response (201):
{
  "message": "Invitation accepted. Account created.",
  "access_token": "jwt-token",
  "refresh_token": "jwt-refresh-token",
  "user": { ...user object with company_id and assigned role... }
}
Error Codes: 400 (invalid token), 410 (expired invitation), 409 (email already registered)

---

GET /api/team/invitations
Headers: Authorization: Bearer {jwt-token}
Required Role: company_admin
Response (200):
{
  "invitations": [
    {
      "invitation_id": "uuid",
      "invited_email": "jane@example.com",
      "invited_first_name": "Jane",
      "invited_last_name": "Smith",
      "assigned_role": "company_user",
      "status": "pending",
      "invited_at": "2025-10-13T12:00:00Z",
      "expires_at": "2025-10-20T12:00:00Z"
    }
  ]
}

---

POST /api/team/invitations/{invitation_id}/resend
Headers: Authorization: Bearer {jwt-token}
Required Role: company_admin
Response (200):
{
  "message": "Invitation resent with new expiration.",
  "invitation": { ...updated invitation with new token and expires_at... }
}
Error Codes: 404 (invitation not found), 400 (already accepted)

---

DELETE /api/team/invitations/{invitation_id}
Headers: Authorization: Bearer {jwt-token}
Required Role: company_admin
Response (200):
{
  "message": "Invitation cancelled."
}
```

### Workflows and Sequencing

**Workflow 1: First-Time User Signup & Onboarding (Company Creator)**

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       │ 1. POST /api/auth/signup
       │    {email, password}
       ▼
┌─────────────────────────────────────────┐
│ Auth Service                            │
│ - Validate email format                 │
│ - Check email not already registered    │
│ - Hash password (bcrypt)                │
│ - Create User record (email_verified=false) │
│ - Generate verification token           │
│ - Store token in email_verification_tokens │
└──────┬──────────────────────────────────┘
       │
       │ 2. Trigger email service
       ▼
┌─────────────────────────────────────────┐
│ Email Service                           │
│ - Send verification email               │
│ - Include secure token link             │
│ - Link: /verify-email?token={token}    │
└──────┬──────────────────────────────────┘
       │
       │ 3. User clicks verification link
       ▼
┌─────────────────────────────────────────┐
│ Auth Service                            │
│ - Validate token                        │
│ - Check expiration (24 hours)           │
│ - Mark user.email_verified = true       │
│ - Mark token as used                    │
│ - Log activity                          │
└──────┬──────────────────────────────────┘
       │
       │ 4. Redirect to login page
       │ 5. POST /api/auth/login
       ▼
┌─────────────────────────────────────────┐
│ Auth Service                            │
│ - Validate credentials                  │
│ - Check email_verified = true           │
│ - Generate JWT access token (15 min)    │
│ - Generate JWT refresh token (7 days)   │
│ - Update last_login timestamp           │
│ - Return tokens + user object           │
└──────┬──────────────────────────────────┘
       │
       │ 6. Check onboarding_complete = false
       │ 7. Navigate to onboarding flow
       ▼
┌─────────────────────────────────────────┐
│ Onboarding Step 1: User Details        │
│ - POST /api/users/onboarding/user-details │
│   {first_name, last_name, role_title, phone} │
│ - Update User record                    │
└──────┬──────────────────────────────────┘
       │
       │ 8. Navigate to Step 2
       ▼
┌─────────────────────────────────────────┐
│ Onboarding Step 2: Company Setup       │
│ - POST /api/users/onboarding/company-setup │
│   {company_name, abn, billing_address, ...} │
│ - Create Company record                 │
│ - Assign user.company_id                │
│ - Assign user.role = company_admin      │
└──────┬──────────────────────────────────┘
       │
       │ 9. POST /api/users/onboarding/complete
       ▼
┌─────────────────────────────────────────┐
│ Complete Onboarding                     │
│ - Set user.onboarding_complete = true   │
│ - Log activity                          │
│ - Navigate to dashboard                 │
└─────────────────────────────────────────┘
```

**Workflow 2: Invited User Join Flow**

```
┌─────────────┐
│ Company     │
│ Admin       │
└──────┬──────┘
       │
       │ 1. POST /api/team/invitations
       │    {first_name, last_name, email, assigned_role}
       ▼
┌─────────────────────────────────────────┐
│ Team Service                            │
│ - Validate inviter is company_admin     │
│ - Check email not already registered    │
│ - Generate secure invitation token      │
│ - Calculate expires_at (+7 days)        │
│ - Create Invitation record              │
└──────┬──────────────────────────────────┘
       │
       │ 2. Trigger email service
       ▼
┌─────────────────────────────────────────┐
│ Email Service                           │
│ - Send invitation email to invitee      │
│ - Include company name, assigned role   │
│ - Include invitation link with token    │
│ - Link: /accept-invitation?token={token} │
└──────┬──────────────────────────────────┘
       │
       │ 3. Invitee clicks invitation link
       │ 4. POST /api/team/invitations/accept
       │    {invitation_token, password}
       ▼
┌─────────────────────────────────────────┐
│ Team Service                            │
│ - Validate token                        │
│ - Check expiration (7 days)             │
│ - Check status = pending                │
│ - Create User record:                   │
│   - email from invitation               │
│   - first_name, last_name pre-filled    │
│   - company_id from invitation          │
│   - role from invitation.assigned_role  │
│   - email_verified = true (auto)        │
│ - Hash password                         │
│ - Mark invitation.status = accepted     │
│ - Generate JWT tokens                   │
│ - Log activity                          │
└──────┬──────────────────────────────────┘
       │
       │ 5. Auto-login with JWT tokens
       │ 6. Check onboarding_complete = false
       │ 7. Navigate to simplified onboarding
       ▼
┌─────────────────────────────────────────┐
│ Onboarding: User Details (Simplified)  │
│ - First/last name pre-filled from invite│
│ - POST /api/users/onboarding/user-details │
│   {first_name, last_name, role_title, phone} │
│ - Skip company setup (already has company_id) │
└──────┬──────────────────────────────────┘
       │
       │ 8. POST /api/users/onboarding/complete
       ▼
┌─────────────────────────────────────────┐
│ Complete Onboarding                     │
│ - Set user.onboarding_complete = true   │
│ - Send notification to Company Admin    │
│ - Navigate to dashboard                 │
└─────────────────────────────────────────┘
```

**Workflow 3: Password Reset Flow**

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       │ 1. Click "Forgot Password" on login page
       │ 2. POST /api/auth/reset-password-request
       │    {email}
       ▼
┌─────────────────────────────────────────┐
│ Auth Service                            │
│ - Check if user exists with email       │
│ - Generate secure reset token           │
│ - Calculate expires_at (+1 hour)        │
│ - Store token in password_reset_tokens  │
│ - Always return 200 (security)          │
└──────┬──────────────────────────────────┘
       │
       │ 3. Trigger email service (if user exists)
       ▼
┌─────────────────────────────────────────┐
│ Email Service                           │
│ - Send password reset email             │
│ - Include secure token link             │
│ - Link: /reset-password?token={token}  │
│ - Mention 1-hour expiration             │
└──────┬──────────────────────────────────┘
       │
       │ 4. User clicks reset link
       │ 5. POST /api/auth/reset-password
       │    {token, new_password}
       ▼
┌─────────────────────────────────────────┐
│ Auth Service                            │
│ - Validate token                        │
│ - Check expiration (1 hour)             │
│ - Hash new password (bcrypt)            │
│ - Update user.password_hash             │
│ - Mark token as used                    │
│ - Invalidate all existing JWT tokens    │
│ - Log activity                          │
│ - Redirect to login page                │
└─────────────────────────────────────────┘
```

## UX Design Specifications

### User Journey Mapping

**Journey 1: First-Time User Signup & Company Creation**
```
Signup → Email Verification → Login → User Details → Company Setup → Dashboard
    ↓           ↓              ↓         ↓            ↓           ↓
  30s        2-5 min        10s       45s          2-3 min      Instant
```

**Journey 2: Invited User Acceptance**
```
Invitation Email → Set Password → User Details → Dashboard
       ↓              ↓            ↓           ↓
    5 min          1 min         30s        Instant
```

**Journey 3: Branch Company Cross-Invitation**
```
Marketing Manager → Branch Invitation → Event Manager Acceptance → Company Switching
       ↓                  ↓                    ↓                      ↓
     2 min              30s                  2 min                  15s
```

### Error State Design

**Email Verification Failures:**
- **Expired Token**: "Verification link expired. Request a new one below."
- **Invalid Token**: "Invalid verification link. Please check your email or request a new one."
- **Already Used**: "Email already verified. You can now log in."

**Company Search Failures:**
- **ABR API Down**: "Company search temporarily unavailable. You can continue manually or try again later."
- **Invalid ABN**: "Invalid ABN format. Please enter 11 digits."
- **No Results**: "No companies found. Try a different search or continue manually."

**Invitation Failures:**
- **Email Bounces**: "Email delivery failed. Please verify the email address and try again."
- **User Already Exists**: "This user is already registered. They can be invited through the team management page."

**Network Failures:**
- **Connection Lost**: "Connection lost. Your progress has been saved. Reconnecting..."
- **Timeout**: "Request timed out. Please check your connection and try again."

### Loading States & Micro-Interactions

**Email Verification Sending:**
```typescript
interface EmailSendingState {
  status: 'idle' | 'sending' | 'sent' | 'error';
  progress: number; // 0-100
  message: string;
  animation: 'pulse' | 'spin' | 'fade';
}
```

**Company Search Loading:**
```typescript
interface SearchLoadingState {
  status: 'idle' | 'searching' | 'found' | 'error';
  searchType: 'auto' | 'abn' | 'acn' | 'name';
  skeletonResults: number; // 3-5 skeleton cards
  debounceTimer: number; // 300ms
}
```

**Onboarding Progress:**
```typescript
interface OnboardingProgress {
  currentStep: number;
  totalSteps: number;
  stepNames: string[];
  completionPercentage: number;
  autoSave: {
    status: 'saving' | 'saved' | 'error';
    lastSaved: Date;
  };
}
```

**Company Switching Animation:**
```typescript
interface CompanySwitchAnimation {
  fadeOutCurrent: boolean;
  fadeInNew: boolean;
  contextPreservation: boolean;
  duration: number; // 300ms
}
```

### Mobile/Tablet Optimization

**Responsive Onboarding Flow:**
- **Desktop**: 2-column layout (progress + form)
- **Tablet**: Single column with larger touch targets (44px minimum)
- **Mobile**: Stacked layout with full-width inputs

**Touch-Friendly Controls:**
- Minimum 44px touch targets for all interactive elements
- Increased spacing between form fields (24px minimum)
- Larger dropdown menus for company selection
- Swipe gestures for step navigation (optional)

**Tablet-Optimized Company Search:**
- Larger search input field (48px height)
- Touch-friendly result cards (60px minimum height)
- Optimized for landscape orientation (event booth usage)
- One-handed operation support

**Mobile Invitation Acceptance:**
- Simplified form layout
- Large, clear call-to-action buttons
- Auto-focus on password field
- Keyboard-optimized input types

### Enhanced Form Components

**Input Field Enhancements:**
```typescript
interface EnhancedInputField {
  floatingLabels: boolean;
  inlineValidation: boolean;
  characterCounters: boolean;
  autoComplete: boolean;
  inputMasking: boolean; // ABN: XXX XXX XXX XX, Phone: +61 XXX XXX XXX
  realTimeValidation: boolean;
  errorRecovery: boolean;
}
```

**Button States:**
```typescript
interface ButtonStates {
  loading: {
    spinner: boolean;
    disabled: boolean;
    text: string; // "Sending..." vs "Send Invitation"
  };
  success: {
    icon: string;
    message: string;
    duration: number; // 2 seconds
  };
  error: {
    message: string;
    retryAvailable: boolean;
  };
  hover: {
    elevation: boolean;
    colorShift: boolean;
  };
  focus: {
    outline: boolean;
    ring: boolean;
  };
}
```

**Error Messaging:**
```typescript
interface ErrorMessaging {
  inlineErrors: boolean;
  errorIcons: boolean;
  contextualHelp: boolean;
  errorRecovery: boolean;
  fieldLevelErrors: boolean;
  formLevelErrors: boolean;
}
```

### Enhanced Data Display Components

**Company Cards:**
```typescript
interface CompanyCardDesign {
  layout: 'grid' | 'list' | 'compact';
  informationHierarchy: [
    'name',
    'abn',
    'gst_status',
    'address',
    'entity_type'
  ];
  actionButtons: ['select', 'view_details', 'edit'];
  hoverStates: {
    elevation: boolean;
    borderHighlight: boolean;
    quickActions: boolean;
  };
}
```

**Search Results:**
```typescript
interface SearchResultsDesign {
  resultRanking: boolean;
  highlightMatches: boolean;
  quickActions: boolean;
  infiniteScroll: boolean;
  resultCount: boolean;
  searchTime: boolean;
  cacheIndicator: boolean; // "Cached result" badge
}
```

### UX Metrics & Success Criteria

**User Experience Metrics:**
```typescript
interface UXSuccessCriteria {
  onboardingCompletion: {
    target: '>85%';
    measurement: 'Users who complete full onboarding flow';
    tracking: 'Analytics event: onboarding_completed';
  };
  
  timeToValue: {
    target: '<5 minutes';
    measurement: 'Time from signup to first successful company creation';
    tracking: 'Performance timing API';
  };
  
  errorRecovery: {
    target: '>90%';
    measurement: 'Users who recover from errors without support';
    tracking: 'Error recovery flow completion';
  };
  
  userSatisfaction: {
    target: '>4.5/5';
    measurement: 'Post-onboarding user satisfaction survey';
    tracking: 'In-app survey after onboarding';
  };
  
  searchSuccessRate: {
    target: '>90%';
    measurement: 'Users who find their company via search';
    tracking: 'Company search completion rate';
  };
  
  mobileUsability: {
    target: '>80%';
    measurement: 'Mobile users who complete onboarding';
    tracking: 'Device-specific completion rates';
  };
}
```

### Accessibility Features

**ARIA Implementation:**
- Form labels properly associated with inputs
- Error messages announced to screen readers
- Progress indicators with aria-live regions
- Keyboard navigation for all interactive elements

**Keyboard Navigation:**
- Tab order follows logical flow
- Enter key submits forms
- Escape key closes modals
- Arrow keys navigate dropdown options

**Visual Accessibility:**
- High contrast mode support
- Focus indicators visible (2px outline)
- Text size scaling up to 200%
- Color not the only indicator of state

**Screen Reader Support:**
- Descriptive alt text for icons
- Form validation messages announced
- Progress updates announced
- Page structure with proper headings

### Micro-Interactions & Animations

**Form Validation:**
- Real-time validation with smooth transitions
- Error states fade in/out (200ms)
- Success checkmarks appear after validation
- Field highlighting on focus/blur

**Loading States:**
- Skeleton loading for search results
- Progress bars for multi-step processes
- Spinner animations for async operations
- Success animations for completed actions

**Transitions:**
- Page transitions (300ms ease-in-out)
- Modal open/close (200ms ease-out)
- Step transitions in onboarding (400ms slide)
- Company switching fade (300ms)

**Feedback:**
- Haptic feedback on mobile devices
- Visual feedback for button presses
- Audio cues for critical actions (optional)
- Toast notifications for non-critical updates

### UX Testing Plan

**Usability Testing:**
- 5 users per persona (Marketing Michelle, Event Coordinator Emma)
- Task-based testing for each user journey
- A/B testing for onboarding flow variations
- Mobile vs desktop experience comparison

**Accessibility Testing:**
- Screen reader testing (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation testing
- High contrast mode testing
- Color blindness simulation testing

**Performance Testing:**
- Core Web Vitals measurement
- Mobile performance testing
- Network throttling simulation
- Battery usage optimization

## Non-Functional Requirements

### Performance

**Response Time Targets:**
- Authentication endpoints (login, signup): < 500ms p95
- Token refresh: < 200ms p95
- Email verification: < 300ms p95
- Onboarding endpoints: < 600ms p95 (database writes involved)

**Concurrency:**
- Support 100 concurrent login requests without degradation
- Handle 50 concurrent signups without email delivery delays
- Token validation must not become bottleneck (use efficient JWT libraries)

**Scalability:**
- Authentication system must support 10,000+ registered users (MVP target)
- Email verification tokens must be efficiently indexed for fast lookups
- JWT token validation must use cached public key (no database hit per request)

**Email Delivery:**
- Email verification sent within 5 seconds of signup
- Password reset emails sent within 5 seconds of request
- Invitation emails sent within 5 seconds of creation
- Use async email sending (Celery/background tasks) to avoid blocking HTTP requests

### Security

**Password Security:**
- Use bcrypt for password hashing with cost factor 12
- Minimum password length: 8 characters (no complexity requirements for MVP)
- Passwords NEVER logged or stored in plain text
- Passwords NEVER sent via email

**Token Security:**
- Email verification tokens: 32-byte cryptographically secure random tokens (urlsafe_b64encode)
- Password reset tokens: 32-byte cryptographically secure random tokens
- Invitation tokens: 32-byte cryptographically secure random tokens
- JWT secrets: 256-bit randomly generated secret stored in Azure Key Vault
- JWT access tokens: 15-minute expiration
- JWT refresh tokens: 7-day expiration, rotated on use

**Transport Security:**
- All endpoints HTTPS only (TLS 1.2+)
- Strict-Transport-Security header enforced
- No sensitive data in URL query parameters (use POST body)

**Authentication & Authorization:**
- RBAC middleware validates JWT and role on every protected endpoint
- JWT tokens include: user_id, email, role, company_id, exp, iat
- Middleware injects `current_user` into request context for easy access
- Failed login attempts tracked (rate limiting in Phase 2)

**Multi-Tenant Security:**
- All database queries filtered by `company_id` where applicable
- Users can only access data within their company
- Company Admins validated before invitation/team management operations
- No cross-company data leakage (validated in testing)

**Audit Logging:**
- Log all authentication events: signup, login, email_verified, password_reset
- Log all user management events: invitation_sent, invitation_accepted, user_created
- Logs include: timestamp, user_id, company_id, IP address (hashed), action, result
- Logs stored in `activity_log` table for compliance

### Reliability/Availability

**Uptime Target:**
- 99.5% uptime for authentication endpoints (critical for access)
- Graceful degradation if email service temporarily unavailable (queue emails)

**Error Handling:**
- All endpoints return consistent error format:
  ```json
  {
    "error": "error_code",
    "message": "Human-readable message",
    "details": { ...optional field-level errors... }
  }
  ```
- Database connection failures: Retry 3 times with exponential backoff
- Email service failures: Queue for retry (up to 3 attempts)
- Token validation failures: Clear error messages (expired vs invalid)

**Data Integrity:**
- Atomic transactions for multi-step operations (user creation + company creation)
- Foreign key constraints enforced in database
- Unique constraints on email, tokens
- Rollback on any step failure during onboarding

**Recovery:**
- Users can resend verification email if first one fails/expires
- Users can resend password reset email multiple times
- Company Admins can resend invitations if expired
- No data loss: All critical data persisted to database before HTTP response

### Observability

**Logging:**
- Structured JSON logs for all authentication events
- Log Levels:
  - INFO: Successful logins, signups, verifications
  - WARN: Failed login attempts, expired tokens
  - ERROR: Email delivery failures, database errors, unexpected exceptions
- Logs include correlation ID for tracing user journey across requests

**Metrics:**
- Track signup conversion rate (signups → email verified → onboarding complete)
- Track login success/failure rates
- Track password reset request volume
- Track invitation sent → accepted conversion rates
- Track email delivery success rates

**Tracing:**
- Each request assigned unique `request_id` for correlation
- `request_id` passed to email service, database queries
- Frontend includes `request_id` in error reports

**Health Checks:**
- `/api/health` endpoint returns 200 if database accessible
- `/api/health/email` endpoint checks email service connectivity (admin only)

**Alerts:**
- Alert if login failure rate > 20% (potential attack or system issue)
- Alert if email delivery failure rate > 10%
- Alert if signup-to-verification conversion < 50% (email delivery problems)
- Alert if database connection pool exhausted

## Dependencies and Integrations

**Backend Dependencies (Python 3.13):**

| Package | Version | Purpose | Epic 1 Usage |
|---------|---------|---------|--------------|
| `fastapi` | 0.115.7 | Web framework | Core REST API endpoints for auth |
| `uvicorn[standard]` | 0.34.3 | ASGI server | Run FastAPI application |
| `pydantic` | 2.10.6 | Data validation | Request/response models, validation |
| `sqlalchemy` | 2.0.40 | ORM | Database models (User, Company, Invitation, tokens) |
| `alembic` | 1.14.1 | Database migrations | Create auth-related tables |
| `pyodbc` | 5.2.0 | MS SQL Server driver | Connect to Azure SQL Database |
| `python-jose[cryptography]` | 3.3.0 | JWT library | Generate and validate JWT tokens |
| `passlib[bcrypt]` | 1.7.4 | Password hashing | Hash passwords with bcrypt |
| `bcrypt` | 4.2.1 | Bcrypt algorithm | Password hashing (cost factor 12) |
| `azure-communication-email` | 1.0.1b1 | Email service | Send verification, reset, invitation emails |
| `structlog` | 24.4.0 | Structured logging | JSON logs for auth events |
| `python-decouple` | 3.8 | Environment config | Load secrets from .env file |
| `pytest` | 8.3.5 | Testing framework | Unit and integration tests |
| `pytest-asyncio` | 0.25.3 | Async test support | Test async endpoints |

**Frontend Dependencies (React 18):**

| Package | Version | Purpose | Epic 1 Usage |
|---------|---------|---------|--------------|
| `react` | 18.2.0 | UI library | Build auth components |
| `react-dom` | 18.2.0 | React renderer | Render to DOM |
| `react-router-dom` | 6.20.0 | Routing | Navigate between signup, login, onboarding pages |
| `zustand` | 4.4.6 | State management | Auth context, user state persistence |
| `react-hook-form` | 7.48.2 | Form handling | Signup, login, onboarding forms with validation |
| `@tanstack/react-query` | 5.8.4 | API state management | Cache user data, handle mutations |
| `axios` | 1.6.2 | HTTP client | Call authentication API endpoints |
| `@radix-ui/react-dialog` | 1.0.5 | Modal component | Onboarding modal, error dialogs |
| `lucide-react` | 0.294.0 | Icon library | UI icons for forms |
| `tailwindcss` | 3.3.5 | CSS framework | Style auth screens |
| `typescript` | 5.2.2 | Type safety | Type-safe components and API calls |

**External Service Integrations:**

| Service | Provider | Purpose | Configuration |
|---------|----------|---------|---------------|
| Azure SQL Database | Microsoft Azure | Primary database | Connection string in Azure Key Vault |
| Azure Communication Services | Microsoft Azure | Email delivery | API key in Azure Key Vault, sender domain verified |
| Azure Key Vault | Microsoft Azure | Secrets management | Store JWT secret, database connection string, email API key |
| Azure Application Insights | Microsoft Azure | Logging and monitoring | Instrumentation key for structured logs |

**Integration Points:**

**1. Azure SQL Database:**
- Connection via `pyodbc` driver
- Connection pooling (max 20 connections for auth module)
- Tables: `users`, `companies`, `invitations`, `email_verification_tokens`, `password_reset_tokens`, `activity_log`
- All queries parameterized to prevent SQL injection
- Transactions for multi-step operations (e.g., company creation + user update)

**2. Azure Communication Email Service:**
- Async email sending (background tasks to avoid blocking HTTP responses)
- Email templates stored in `backend/templates/emails/`:
  - `verification_email.html` - Email verification link
  - `password_reset_email.html` - Password reset link
  - `invitation_email.html` - Team invitation link
- Sender email: `noreply@eventlead.com` (verified domain)
- Retry logic: 3 attempts with exponential backoff
- Failure handling: Queue email for manual retry if all attempts fail

**3. Azure Key Vault:**
- Secrets accessed via Azure SDK (`DefaultAzureCredential`)
- Secrets:
  - `JWT_SECRET_KEY` - 256-bit secret for JWT signing
  - `DATABASE_CONNECTION_STRING` - SQL connection string
  - `EMAIL_API_KEY` - Azure Communication Services key
- Secrets cached in memory at application startup
- Rotation: JWT secret rotated every 90 days (Phase 2)

**4. Azure Application Insights:**
- Structured logs sent to Application Insights
- Custom events tracked:
  - `user_signup`, `user_login`, `email_verified`
  - `password_reset_requested`, `password_reset_completed`
  - `invitation_sent`, `invitation_accepted`
- Logs queryable via Kusto Query Language (KQL)
- Real-time monitoring dashboard for auth metrics

**Environment Variables (`.env` file):**
```
# Application
ENVIRONMENT=development
DEBUG=True

# Azure Key Vault
KEY_VAULT_URL=https://eventlead-kv.vault.azure.net/

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_ALGORITHM=HS256

# Email Configuration
EMAIL_FROM_ADDRESS=noreply@eventlead.com
EMAIL_FROM_NAME=EventLead Platform

# Frontend URL (for email links)
FRONTEND_URL=https://app.eventlead.com

# Azure Application Insights
APPINSIGHTS_INSTRUMENTATION_KEY=<from Key Vault>
```

**No Third-Party SaaS Dependencies:**
- No Auth0, Okta, or similar authentication services (built in-house)
- No SendGrid or Mailgun (using Azure Communication Services)
- All core authentication logic owned and controlled

## Acceptance Criteria (Authoritative)

These acceptance criteria are derived from the PRD and define the testable requirements for Epic 1 completion.

**AC-1: User Signup and Email Verification**
- AC-1.1: User can submit signup form with valid email and password
- AC-1.2: System validates email format and password minimum length (8 characters)
- AC-1.3: System prevents duplicate email registration (409 error returned)
- AC-1.4: System sends verification email within 5 seconds of signup
- AC-1.5: Verification email contains secure token link that expires in 24 hours
- AC-1.6: User clicking verification link marks `email_verified = true`
- AC-1.7: System displays success message and redirects to login page
- AC-1.8: User cannot log in until email is verified (403 error returned)

**AC-2: User Login and JWT Token Generation**
- AC-2.1: User can submit login form with email and password
- AC-2.2: System validates credentials and returns JWT access token (15-minute expiration)
- AC-2.3: System returns JWT refresh token (7-day expiration)
- AC-2.4: JWT tokens include: user_id, email, role, company_id, exp, iat
- AC-2.5: System updates `last_login` timestamp on successful login
- AC-2.6: System returns 401 error for invalid credentials
- AC-2.7: System returns 403 error if email not verified

**AC-3: First-Time User Onboarding (Company Creator)**
- AC-3.1: After successful login, system checks `onboarding_complete` flag
- AC-3.2: If false, system navigates user to onboarding flow (cannot skip)
- AC-3.3: **Step 1 - User Details:** User can enter first name, last name, role title (optional), phone (optional)
- AC-3.4: System validates required fields and Australian phone format (+61)
- AC-3.5: System saves user details and navigates to Step 2
- AC-3.6: **Step 2 - Company Setup:** User can enter company name, ABN, billing address
- AC-3.7: System provides enhanced company search with auto-detection (ABN/ACN/Name)
- AC-3.8: System validates search results via ABR API with enterprise-grade caching (300x faster)
- AC-3.9: System achieves ~90% search success rate (up from ~20%) with smart search UX
- AC-3.10: System validates Australian address (state dropdown, 4-digit postcode)
- AC-3.11: System creates Company + CompanyCustomerDetails + CompanyBillingDetails records
- AC-3.12: System creates UserCompany record with Role="company_admin" and IsDefaultCompany=true
- AC-3.13: System sets `user.onboarding_complete = true`
- AC-3.14: System populates billing details with ABN API data (TaxInvoiceName, GSTRegistered)
- AC-3.15: System logs activity: `company_created`, `onboarding_completed`
- AC-3.16: System navigates user to dashboard

**AC-4: Password Reset Flow**
- AC-4.1: User can request password reset from login page
- AC-4.2: System sends password reset email within 5 seconds (always returns 200 for security)
- AC-4.3: Reset email contains secure token link that expires in 1 hour
- AC-4.4: User clicking reset link can enter new password
- AC-4.5: System validates new password meets minimum length (8 characters)
- AC-4.6: System hashes new password with bcrypt and updates user record
- AC-4.7: System marks reset token as used (cannot be reused)
- AC-4.8: System invalidates all existing JWT tokens for that user
- AC-4.9: System redirects user to login page with success message
- AC-4.10: User can log in with new password

**AC-5: Team Invitation Flow (Company Admin Invites User)**
- AC-5.1: Company Admin can access Team Management page
- AC-5.2: Company Admin can submit invitation form with first name, last name, email, assigned role
- AC-5.3: System validates inviter has `role = company_admin`
- AC-5.4: System prevents inviting existing users (409 error)
- AC-5.5: System generates secure invitation token
- AC-5.6: System sends invitation email within 5 seconds
- AC-5.7: Invitation email includes company name, assigned role, and invitation link
- AC-5.8: Invitation expires in 7 days
- AC-5.9: System displays invitation in "Pending Invitations" list with status from InvitationStatus lookup
- AC-5.10: Company Admin can resend expired invitations (generates new token, new 7-day window)
- AC-5.11: Company Admin can cancel pending invitations (updates status via InvitationStatus)
- AC-5.12: System supports multi-company invitations (user can join multiple companies)

**AC-6: Invited User Acceptance Flow**
- AC-6.1: Invited user clicks invitation link and lands on acceptance page
- AC-6.2: Acceptance page displays company name and assigned role
- AC-6.3: First name and last name pre-filled from invitation (editable)
- AC-6.4: Email pre-filled from invitation (read-only)
- AC-6.5: User enters password and confirms password
- AC-6.6: System validates invitation token and expiration
- AC-6.7: System creates User record with invitation details
- AC-6.8: System creates UserCompany record with invitation company and assigned role
- AC-6.9: System sets IsDefaultCompany=true for invitation company (first company)
- AC-6.10: System sets `email_verified = true` (invitation email = verification)
- AC-6.11: System marks invitation status as "accepted" via InvitationStatus lookup
- AC-6.12: System generates JWT tokens and auto-logs in user
- AC-6.13: System navigates user to simplified onboarding (user details only, no company setup)
- AC-6.14: After onboarding, system sends notification to Company Admin

**AC-7: RBAC Middleware and Authorization**
- AC-7.1: All protected endpoints validate JWT token in Authorization header
- AC-7.2: Middleware extracts user_id, current_company_id, role from JWT
- AC-7.3: Middleware queries UserCompany table to validate user's access to current company
- AC-7.4: Middleware injects `current_user` and `current_user_company` objects into request context
- AC-7.5: Endpoints requiring `company_admin` role return 403 if UserCompany.Role="company_user"
- AC-7.6: Endpoints requiring `system_admin` role return 403 if user is not system admin
- AC-7.7: JWT tokens include AccessTokenVersion for "logout all devices" functionality
- AC-7.8: Middleware validates AccessTokenVersion matches User.AccessTokenVersion
- AC-7.9: Expired JWT tokens return 401 error with clear message
- AC-7.10: Invalid/malformed JWT tokens return 401 error

**AC-8: Multi-Tenant Data Isolation**
- AC-8.1: All user queries filtered by UserCompany table where applicable
- AC-8.2: Company User cannot access data from companies they don't belong to
- AC-8.3: Company Admin cannot access data from other companies
- AC-8.4: Invitation endpoints only show/manage invitations for current company
- AC-8.5: Activity log entries scoped to company (no cross-company visibility)
- AC-8.6: User can switch between companies via company switcher dropdown
- AC-8.7: JWT tokens include current_company_id for session context
- AC-8.8: UserCompany.Status="active" required for company access

**AC-9: Token Refresh Flow**
- AC-9.1: User can submit refresh token to `/api/auth/refresh` endpoint
- AC-9.2: System validates refresh token signature and expiration
- AC-9.3: System returns new access token (15-minute expiration)
- AC-9.4: System returns 401 if refresh token expired or invalid
- AC-9.5: Frontend automatically refreshes access token before expiration

**AC-10: Enhanced ABR Search (NEW)**
- AC-10.1: System provides smart company search with auto-detection (ABN/ACN/Name)
- AC-10.2: System detects ABN search when user enters 11 digits
- AC-10.3: System detects ACN search when user enters 9 digits  
- AC-10.4: System performs company name search for text input
- AC-10.5: System provides debounced search with 300ms delay for optimal UX
- AC-10.6: System displays rich search results with company details (name, ABN, GST status)
- AC-10.7: System auto-selects single results for seamless UX
- AC-10.8: System provides enterprise-grade caching with 300x faster cached results
- AC-10.9: System maintains 30-day cache TTL compliance with ABR terms
- AC-10.10: System achieves ~90% search success rate (up from ~20%)
- AC-10.11: System provides comprehensive error handling and fallbacks
- AC-10.12: System includes cache analytics and performance monitoring

**AC-11: Branch Company Scenarios (NEW)**
- AC-11.1: System supports cross-company invitations between related companies
- AC-11.2: System creates company relationships (branch, subsidiary, partner) when needed
- AC-11.3: System handles "Marketing Manager → Branch Event Manager" invitation flow
- AC-11.4: System handles "Branch Event Manager → Head Office Marketing Manager" invitation flow
- AC-11.5: System provides company switching capability for multi-company users
- AC-11.6: System validates user access before allowing company switch
- AC-11.7: System shows relationship context in company switcher dropdown
- AC-11.8: System provides "Request Access" flow for unauthorized company access
- AC-11.9: System maintains separate billing for branch companies
- AC-11.10: System tracks company relationship establishment and changes

**AC-12: International Foundation & Web Properties (NEW)**
- AC-12.1: System provides web properties (sort order, colors, active status) for all lookup tables
- AC-12.2: System supports country-specific validation rules (phone, postal code, tax ID)
- AC-12.3: System enables quick setup for new country expansion
- AC-12.4: System provides flexible validation rule engine with precedence ordering
- AC-12.5: System displays country-specific validation messages to users
- AC-12.6: System supports dynamic phone validation based on selected country
- AC-12.7: System supports dynamic postal code validation based on selected country
- AC-12.8: System provides country-specific date and currency formatting
- AC-12.9: System enables admin configuration of validation rules without code changes
- AC-12.10: System maintains validation rule audit trail and versioning

**AC-13: Application Specification System (NEW)**
- AC-13.1: System provides global application parameters for all configuration values
- AC-13.2: System supports country-specific parameter overrides
- AC-13.3: System supports environment-specific parameter overrides (dev/staging/production)
- AC-13.4: System resolves parameter values with clear priority order (environment+country > environment+global > country > global)
- AC-13.5: System caches parameter values for performance optimization
- AC-13.6: System provides runtime configuration changes without code deployment
- AC-13.7: System maintains audit trail for all parameter changes
- AC-13.8: System supports parameter categorization (authentication, validation, business_rules)
- AC-13.9: System validates parameter data types and constraints
- AC-13.10: System provides configuration service API for frontend and backend consumption

**AC-14: UX Design & User Experience**
- AC-14.1: System provides comprehensive error states with clear recovery paths for all failure scenarios
- AC-14.2: System displays loading states with progress indicators for all async operations
- AC-14.3: System implements responsive design optimized for desktop, tablet, and mobile devices
- AC-14.4: System provides accessibility features including ARIA labels, keyboard navigation, and screen reader support
- AC-14.5: System includes micro-interactions and animations for enhanced user feedback
- AC-14.6: System achieves >85% onboarding completion rate and <5 minute time-to-value
- AC-14.7: System provides real-time form validation with inline error messaging
- AC-14.8: System includes auto-save functionality with visual feedback for multi-step processes
- AC-14.9: System supports touch-friendly controls with minimum 44px touch targets for mobile/tablet
- AC-14.10: System provides comprehensive user journey mapping with clear success metrics

**AC-15: Activity Logging**
- AC-15.1: System logs all signup events with timestamp, user_id
- AC-15.2: System logs all login events with timestamp, user_id, IP (hashed)
- AC-15.3: System logs email verification events
- AC-15.4: System logs password reset events
- AC-15.5: System logs invitation sent/accepted events with company_id
- AC-15.6: System logs company creation events
- AC-15.7: All logs stored in `activity_log` table with structured JSON format

## Enhanced ABR Search Implementation (NEW)

### **Implementation Phases:**

#### **Phase 1: Enhanced Backend (Week 1)**
- [ ] Deploy enhanced ABRSearchCache schema
- [ ] Implement multi-search ABR client (`abr_client.py`)
- [ ] Add smart search backend routes (`POST /companies/smart-search`)
- [ ] Integrate enhanced caching service (`cache_service.py`)
- [ ] Add cache cleanup stored procedures

#### **Phase 2: Enhanced Frontend (Week 2)**
- [ ] Deploy SmartCompanySearch component
- [ ] Implement auto-detection logic (ABN/ACN/Name)
- [ ] Add debounced search functionality (300ms delay)
- [ ] Integrate rich results display
- [ ] Add auto-selection for single results

#### **Phase 3: UX Polish (Week 3)**
- [ ] Mobile optimization and responsive design
- [ ] Accessibility enhancements (ARIA, keyboard navigation)
- [ ] Search analytics integration
- [ ] Performance monitoring setup
- [ ] User testing and validation

### **Success Metrics:**
- **Search Success Rate**: >90% (up from ~20%)
- **Time to Find Company**: <30 seconds
- **Search Error Rate**: <5%
- **Search Completion Rate**: >85%
- **Cache Hit Rate**: 40% average
- **API Cost Reduction**: 40%
- **Response Time Improvement**: 300x for cached results

## Traceability Mapping

This table maps acceptance criteria to implementation components and test strategies.

| AC ID | Spec Section | Backend Component(s) | Frontend Component(s) | Database Table(s) | Test Strategy |
|-------|--------------|----------------------|----------------------|-------------------|---------------|
| AC-1.1 to AC-1.8 | Email Verification | `auth/router.py::signup`, `auth/router.py::verify_email`, `common/email.py` | `SignupForm.tsx`, `EmailVerificationPage.tsx` | `users`, `email_verification_tokens` | Unit: Service logic, Integration: E2E signup flow |
| AC-2.1 to AC-2.7 | JWT Login | `auth/router.py::login`, `auth/service.py::generate_tokens`, `common/security.py` | `LoginForm.tsx`, `AuthContext.tsx` | `users` | Unit: Token generation, Integration: Login flow |
| AC-3.1 to AC-3.14 | First-Time Onboarding | `users/router.py::onboarding_user_details`, `users/router.py::onboarding_company_setup`, `companies/service.py` | `OnboardingFlow.tsx`, `OnboardingStep1.tsx`, `OnboardingStep2.tsx` | `users`, `companies`, `activity_log` | Unit: Company creation, Integration: Full onboarding flow |
| AC-4.1 to AC-4.10 | Password Reset | `auth/router.py::reset_password_request`, `auth/router.py::reset_password`, `common/email.py` | `PasswordResetRequest.tsx`, `PasswordResetForm.tsx` | `users`, `password_reset_tokens` | Unit: Token validation, Integration: Full reset flow |
| AC-5.1 to AC-5.11 | Invitation Management | `team/router.py::create_invitation`, `team/router.py::resend_invitation`, `team/service.py` | `TeamManagement.tsx`, `InvitationList.tsx`, `InviteUserModal.tsx` | `invitations`, `activity_log` | Unit: Invitation logic, Integration: Full invitation flow |
| AC-6.1 to AC-6.13 | Invitation Acceptance | `team/router.py::accept_invitation`, `team/service.py`, `users/router.py::onboarding_user_details` | `InvitationAcceptance.tsx`, `OnboardingFlow.tsx` | `invitations`, `users`, `activity_log` | Unit: Token validation, Integration: Full acceptance + onboarding |
| AC-7.1 to AC-7.7 | RBAC Middleware | `auth/middleware.py::require_auth`, `auth/middleware.py::require_role`, `auth/service.py::validate_jwt` | `AuthContext.tsx`, `ProtectedRoute.tsx` | `users` | Unit: Middleware tests, Integration: Role enforcement tests |
| AC-8.1 to AC-8.5 | Multi-Tenant Isolation | All service layer functions with `company_id` filtering | N/A | All tables with `company_id` FK | Unit: Query filters, Integration: Cross-company access attempts |
| AC-9.1 to AC-9.5 | Token Refresh | `auth/router.py::refresh`, `auth/service.py::generate_access_token` | `AuthContext.tsx::refreshAccessToken` | N/A | Unit: Refresh logic, Integration: Expired token refresh |
| AC-10.1 to AC-10.12 | Enhanced ABR Search | `companies/abr_client.py`, `companies/cache_service.py`, `companies/router.py::smart_search` | `SmartCompanySearch.tsx`, `CompanySearchResults.tsx` | `ABRSearchCache` | Unit: Search logic, Integration: Full search flow, Performance: Cache hit rates |
| AC-11.1 to AC-11.10 | Branch Company Scenarios | `companies/relationship_service.py`, `companies/switch_service.py` | `CompanySwitcher.tsx`, `CompanyAccessRequest.tsx` | `CompanyRelationship`, `CompanySwitchRequest` | Unit: Relationship logic, Integration: Cross-company invitation flow |
| AC-12.1 to AC-12.10 | International Foundation | `countries/validation_engine.py`, `countries/expansion_service.py` | `CountryValidation.tsx`, `PhoneInput.tsx` | `CountryWebProperties`, `ValidationRule`, `LookupValueWebProperties` | Unit: Validation rules, Integration: Country-specific validation |
| AC-13.1 to AC-13.10 | Application Specification | `config/specification_service.py`, `config/config_api.py` | `useApplicationConfig.tsx`, `ConfigProvider.tsx` | `ApplicationSpecification`, `CountryApplicationSpecification`, `EnvironmentApplicationSpecification` | Unit: Parameter resolution, Integration: Configuration loading |
| AC-14.1 to AC-14.10 | UX Design & User Experience | All services with error handling, loading states | `EnhancedFormInput.tsx`, `LoadingStates.tsx`, `ErrorBoundary.tsx`, `ProgressIndicator.tsx`, `useFormValidation.tsx`, `useAutoSave.tsx`, `useKeyboardNavigation.tsx` | N/A | Unit: UX component tests, Integration: User journey testing, Accessibility: Screen reader testing, Performance: UX metrics validation |
| AC-15.1 to AC-15.7 | Activity Logging | `common/logging.py::log_activity`, All auth/team services | N/A | `activity_log` | Unit: Log writes, Integration: Verify logs created for each event |

## Risks, Assumptions, Open Questions

**Risks:**

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Email delivery failures** (verification, reset, invitation emails not delivered) | HIGH | Use Azure Communication Services with verified domain; implement retry logic (3 attempts); queue failed emails for manual review; monitor delivery rates with alerts |
| **JWT secret compromise** | CRITICAL | Store in Azure Key Vault; rotate every 90 days (Phase 2); use 256-bit cryptographically secure secret; never log or expose in errors |
| **Multi-tenant data leakage** (users accessing other companies' data) | CRITICAL | Mandatory `company_id` filtering in all queries; comprehensive integration tests; code review checklist; use database row-level security where possible |
| **Token expiration edge cases** (race conditions, expired tokens causing UX issues) | MEDIUM | Frontend auto-refreshes token before expiration; clear error messages; retry logic for expired tokens |
| **Onboarding abandonment** (users drop off during multi-step onboarding) | MEDIUM | Monitor conversion rates; allow saving progress (Phase 2); simplify flow if conversion < 70% |
| **Invitation spam/abuse** (malicious admins inviting many fake users) | MEDIUM | Rate limit invitations (10 per hour per company - Phase 2); track invitation patterns; flag suspicious activity |
| **Password reset token abuse** (attacker spamming reset requests) | MEDIUM | Rate limit reset requests (5 per hour per IP - Phase 2); short token expiration (1 hour); always return 200 to prevent email enumeration |
| **RBAC bypass** (bugs in middleware allowing unauthorized access) | HIGH | Comprehensive middleware unit tests; integration tests for role enforcement; security audit before launch |

**Assumptions:**

1. **Azure Communication Services email delivery is reliable** (>95% delivery rate)
   - If false: Fall back to SendGrid or implement manual email queue review
   
2. **Users have access to their email** during signup/verification flow
   - If false: Provide "Resend verification email" option

3. **ABN validation format check is sufficient** (11 digits)
   - If false: Integrate with ABR (Australian Business Register) API in Phase 2

4. **JWT tokens with 15-minute expiration are acceptable UX**
   - If false: Increase to 30 minutes or implement seamless auto-refresh

5. **First user creating company should automatically become Company Admin**
   - If false: Add role selection during company setup

6. **Invited users will accept invitations within 7 days**
   - If false: Increase expiration to 14 days or make configurable

7. **Email verification within 24 hours is acceptable**
   - If false: Increase token expiration to 48 hours

8. **Bcrypt cost factor 12 provides sufficient security without UX impact**
   - If false: Adjust cost factor or use Argon2 algorithm

9. **No rate limiting required for MVP** (deferred to Phase 2)
   - If false: Implement basic rate limiting using Redis/in-memory cache

10. **Azure Key Vault latency is acceptable** (<100ms for secret retrieval)
    - If false: Cache secrets in memory at application startup

**Open Questions:**

| Question | Decision Needed By | Assigned To | Status |
|----------|-------------------|-------------|--------|
| Should we implement "Remember Me" functionality (longer refresh token expiration)? | Before Story 1.2 (Login) | Anthony | OPEN |
| Should we send welcome email after onboarding completion? | Before Story 1.3 (Onboarding) | Anthony | OPEN |
| Should Company Admin be notified when invited user completes onboarding? | Before Story 1.5 (Invitations) | Anthony | OPEN |
| Should we log failed login attempts for security monitoring? | Before Story 1.2 (Login) | Anthony | YES - Include in AC-10 |
| Should we implement password complexity requirements (uppercase, numbers, symbols)? | Before Story 1.1 (Signup) | Anthony | NO - Deferred to Phase 2 |
| Should we allow users to change their email address? | Before Story 1.6 (User Profile) | Anthony | NO - Deferred to Phase 2 |
| Should we implement account deletion/deactivation? | Before Epic 2 (Company Management) | Anthony | NO - Deferred to Epic 9 (Audit) |
| Should we implement MFA (Multi-Factor Authentication)? | Before Beta Launch | Anthony | NO - Deferred to Phase 2 |

## UX Implementation Guidelines

### Frontend Architecture for UX

**Component Hierarchy:**
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── SignupForm.tsx (enhanced with UX features)
│   │   │   ├── LoginForm.tsx (enhanced with UX features)
│   │   │   ├── OnboardingFlow.tsx (enhanced with progress, auto-save)
│   │   │   └── InvitationAcceptance.tsx (enhanced with error states)
│   │   └── hooks/
│   │       ├── useFormValidation.tsx
│   │       ├── useAutoSave.tsx
│   │       └── useKeyboardNavigation.tsx
│   ├── companies/
│   │   ├── components/
│   │   │   ├── SmartCompanySearch.tsx (enhanced with loading states)
│   │   │   ├── CompanySearchResults.tsx (enhanced with animations)
│   │   │   ├── CompanySwitcher.tsx (enhanced with transitions)
│   │   │   └── CompanyAccessRequest.tsx (enhanced with error handling)
│   │   └── hooks/
│   │       └── useCompanySearch.tsx
│   └── ux/
│       ├── components/
│       │   ├── EnhancedFormInput.tsx
│       │   ├── LoadingStates.tsx
│       │   ├── ErrorBoundary.tsx
│       │   ├── ProgressIndicator.tsx
│       │   └── ToastNotifications.tsx
│       ├── hooks/
│       │   ├── useFormValidation.tsx
│       │   ├── useAutoSave.tsx
│       │   ├── useKeyboardNavigation.tsx
│       │   └── useAccessibility.tsx
│       └── utils/
│           ├── animations.ts
│           ├── validation.ts
│           └── accessibility.ts
```

### UX Component Specifications

**Enhanced Form Input Component:**
```typescript
interface EnhancedFormInputProps {
  // Core props
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'tel' | 'url';
  value: string;
  onChange: (value: string) => void;
  
  // UX enhancements
  floatingLabel?: boolean;
  inlineValidation?: boolean;
  inputMasking?: boolean;
  autoComplete?: string;
  placeholder?: string;
  
  // Validation
  validation?: {
    required?: boolean;
    pattern?: RegExp;
    minLength?: number;
    maxLength?: number;
    custom?: (value: string) => string | null;
  };
  
  // Error handling
  error?: string;
  showError?: boolean;
  
  // Accessibility
  ariaLabel?: string;
  ariaDescribedBy?: string;
  
  // Styling
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'outlined' | 'filled';
}
```

**Loading States Component:**
```typescript
interface LoadingStatesProps {
  type: 'spinner' | 'skeleton' | 'progress' | 'pulse';
  size?: 'sm' | 'md' | 'lg';
  message?: string;
  progress?: number; // 0-100 for progress type
  skeletonLines?: number; // for skeleton type
  color?: 'primary' | 'secondary' | 'accent';
}
```

**Error Boundary Component:**
```typescript
interface ErrorBoundaryProps {
  fallback?: React.ComponentType<{error: Error, retry: () => void}>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  children: React.ReactNode;
}

interface ErrorFallbackProps {
  error: Error;
  retry: () => void;
  showDetails?: boolean;
  recoveryActions?: Array<{
    label: string;
    action: () => void;
    variant: 'primary' | 'secondary';
  }>;
}
```

### UX Testing Implementation

**Component Testing with UX Focus:**
```typescript
// Example: Enhanced Form Input Test
describe('EnhancedFormInput', () => {
  it('should display floating label when focused', () => {
    render(<EnhancedFormInput name="email" label="Email" floatingLabel />);
    
    const input = screen.getByRole('textbox');
    fireEvent.focus(input);
    
    expect(screen.getByText('Email')).toHaveClass('floating-label');
  });
  
  it('should show inline validation errors', () => {
    render(
      <EnhancedFormInput 
        name="email" 
        label="Email" 
        inlineValidation 
        validation={{ required: true }}
        value=""
      />
    );
    
    const input = screen.getByRole('textbox');
    fireEvent.blur(input);
    
    expect(screen.getByText('This field is required')).toBeInTheDocument();
  });
  
  it('should be accessible via keyboard navigation', () => {
    render(<EnhancedFormInput name="email" label="Email" />);
    
    const input = screen.getByRole('textbox');
    input.focus();
    
    expect(input).toHaveFocus();
    expect(input).toHaveAttribute('tabindex', '0');
  });
});
```

**User Journey Testing:**
```typescript
// Example: Complete Onboarding Journey Test
describe('Onboarding User Journey', () => {
  it('should complete onboarding in under 5 minutes', async () => {
    const startTime = Date.now();
    
    // Step 1: Signup
    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'Password123');
    await user.click(screen.getByRole('button', { name: 'Sign Up' }));
    
    // Step 2: Email verification (mocked)
    await waitFor(() => {
      expect(screen.getByText('Check your email')).toBeInTheDocument();
    });
    
    // Step 3: Login
    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'Password123');
    await user.click(screen.getByRole('button', { name: 'Log In' }));
    
    // Step 4: User details
    await user.type(screen.getByLabelText('First Name'), 'John');
    await user.type(screen.getByLabelText('Last Name'), 'Doe');
    await user.click(screen.getByRole('button', { name: 'Continue' }));
    
    // Step 5: Company setup
    await user.type(screen.getByLabelText('Company Name'), 'Acme Corp');
    await user.type(screen.getByLabelText('ABN'), '12345678901');
    await user.click(screen.getByRole('button', { name: 'Complete Setup' }));
    
    const endTime = Date.now();
    const duration = (endTime - startTime) / 1000; // seconds
    
    expect(duration).toBeLessThan(300); // 5 minutes
    expect(screen.getByText('Welcome to EventLead!')).toBeInTheDocument();
  });
});
```

### Performance Optimization for UX

**Lazy Loading Strategy:**
```typescript
// Lazy load heavy components
const OnboardingFlow = lazy(() => import('./OnboardingFlow'));
const CompanySearch = lazy(() => import('./CompanySearch'));

// Use Suspense with loading fallback
<Suspense fallback={<LoadingStates type="skeleton" skeletonLines={5} />}>
  <OnboardingFlow />
</Suspense>
```

**Optimistic Updates:**
```typescript
// Optimistic UI updates for better perceived performance
const useOptimisticCompanySearch = () => {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const search = async (query: string) => {
    // Optimistically show skeleton loading
    setIsLoading(true);
    setResults([]);
    
    try {
      const data = await searchCompanies(query);
      setResults(data);
    } catch (error) {
      // Show error state with retry option
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };
  
  return { results, isLoading, search };
};
```

**Accessibility Implementation:**
```typescript
// Accessibility utilities
export const useAccessibility = () => {
  const announceToScreenReader = (message: string) => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  };
  
  const trapFocus = (element: HTMLElement) => {
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            lastElement.focus();
            e.preventDefault();
          }
        } else {
          if (document.activeElement === lastElement) {
            firstElement.focus();
            e.preventDefault();
          }
        }
      }
    };
    
    element.addEventListener('keydown', handleTabKey);
    firstElement?.focus();
    
    return () => {
      element.removeEventListener('keydown', handleTabKey);
    };
  };
  
  return { announceToScreenReader, trapFocus };
};
```

## Test Strategy Summary

**Test Levels:**

**1. Unit Tests (pytest)**
- **Target Coverage:** 80%+ for auth, team, company modules
- **Focus Areas:**
  - Password hashing and validation (`common/security.py`)
  - JWT token generation and validation (`auth/service.py`)
  - Token expiration logic (email verification, password reset, invitation)
  - ABN format validation (`companies/service.py`)
  - Email address validation
  - RBAC middleware (`auth/middleware.py`)
  - Multi-tenant query filtering (company_id checks)

- **Test Examples:**
  ```python
  # test_auth_service.py
  def test_hash_password_bcrypt_cost_12():
      password = "SecurePassword123"
      hashed = hash_password(password)
      assert hashed.startswith("$2b$12$")
      
  def test_verify_password_correct():
      password = "SecurePassword123"
      hashed = hash_password(password)
      assert verify_password(password, hashed) == True
      
  def test_generate_jwt_includes_claims():
      user = create_test_user()
      token = generate_jwt(user)
      claims = decode_jwt(token)
      assert claims["user_id"] == str(user.user_id)
      assert claims["role"] == "company_admin"
      assert claims["company_id"] == str(user.company_id)
  ```

**2. Integration Tests (pytest + TestClient)**
- **Focus Areas:**
  - Full signup → verification → login → onboarding flow
  - Password reset end-to-end
  - Invitation creation → acceptance → onboarding
  - Role-based endpoint access (403 enforcement)
  - Multi-tenant data isolation (cross-company access attempts)
  - Email sending (mocked Azure Communication Service)

- **Test Examples:**
  ```python
  # test_auth_flow_integration.py
  def test_full_signup_flow():
      # 1. Signup
      response = client.post("/api/auth/signup", json={"email": "test@example.com", "password": "Password123"})
      assert response.status_code == 201
      
      # 2. Verify email
      token = get_latest_verification_token()
      response = client.post("/api/auth/verify-email", json={"token": token})
      assert response.status_code == 200
      
      # 3. Login
      response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "Password123"})
      assert response.status_code == 200
      assert "access_token" in response.json()
  ```

**3. End-to-End Tests (Playwright + React Testing Library)**
- **Focus Areas:**
  - First-time user journey: Signup → Email verification → Login → Onboarding (2 steps) → Dashboard
  - Invited user journey: Click invite link → Set password → Onboarding → Dashboard
  - Password reset journey: Request reset → Click email link → Set new password → Login
  - Company Admin invite flow: Navigate to Team → Send invitation → Check pending list

- **Test Tools:**
  - Frontend: React Testing Library for component tests
  - E2E: Playwright for full browser automation
  - Email: Mailhog or similar for testing email delivery

**4. UX/UI Tests**
- **Component Testing (React Testing Library + Jest):**
  - Enhanced form input validation and error states
  - Loading states and skeleton components
  - Error boundary recovery flows
  - Progress indicator functionality
  - Accessibility compliance (ARIA labels, keyboard navigation)

- **User Journey Testing (Playwright):**
  - Complete onboarding flow timing (<5 minutes)
  - Error recovery scenarios
  - Mobile/tablet responsive behavior
  - Cross-browser compatibility
  - Performance under load

- **Accessibility Testing:**
  - Screen reader compatibility (NVDA, JAWS, VoiceOver)
  - Keyboard-only navigation
  - High contrast mode support
  - Color blindness simulation
  - WCAG 2.1 AA compliance

**5. Security Tests**
- **Manual Security Audit:**
  - OWASP Top 10 checklist
  - JWT token validation edge cases
  - SQL injection prevention (parameterized queries)
  - XSS prevention (React escapes by default)
  - CSRF prevention (not applicable for JWT-based auth)

- **Automated Security Scans:**
  - Dependency vulnerability scanning (Dependabot)
  - Static analysis (Bandit for Python, ESLint security plugin for React)

**5. Performance Tests**
- **Load Testing (Locust):**
  - 100 concurrent logins (target: < 500ms p95)
  - 50 concurrent signups (target: < 600ms p95)
  - Token refresh under load (target: < 200ms p95)

**Test Data Strategy:**

**Fixtures:**
- Test users with different roles (system_admin, company_admin, company_user)
- Test companies with billing data
- Test invitations (pending, accepted, expired, cancelled)
- Test tokens (valid, expired, used, invalid)

**Database Strategy:**
- Use separate test database
- Reset database before each test suite run
- Use database transactions for test isolation (rollback after each test)

**Test Execution:**
- Unit tests run on every commit (pre-commit hook)
- Integration tests run on every push (CI/CD pipeline)
- E2E tests run nightly or before release
- Performance tests run before launch and after major changes

**Acceptance Criteria Coverage:**

| AC Group | Unit Tests | Integration Tests | E2E Tests |
|----------|-----------|------------------|-----------|
| AC-1 (Signup & Verification) | ✅ Password validation, token generation | ✅ Full signup flow | ✅ Browser signup + email click |
| AC-2 (Login & JWT) | ✅ Token generation, expiration | ✅ Login with valid/invalid creds | ✅ Browser login + redirect |
| AC-3 (Onboarding) | ✅ ABN validation, address validation | ✅ Full onboarding flow | ✅ Browser onboarding (2 steps) |
| AC-4 (Password Reset) | ✅ Token generation, expiration | ✅ Full reset flow | ✅ Browser reset + email click |
| AC-5 (Invitation Management) | ✅ Token generation, role validation | ✅ Create/resend/cancel invitations | ✅ Browser invite flow |
| AC-6 (Invitation Acceptance) | ✅ Token validation | ✅ Accept invitation + onboarding | ✅ Browser acceptance flow |
| AC-7 (RBAC Middleware) | ✅ JWT validation, role checks | ✅ Role enforcement on endpoints | ✅ Browser access denied scenarios |
| AC-8 (Multi-Tenant Isolation) | ✅ Query filters | ✅ Cross-company access attempts | N/A |
| AC-9 (Token Refresh) | ✅ Refresh token validation | ✅ Refresh before/after expiration | ✅ Browser auto-refresh |
| AC-10 (Activity Logging) | ✅ Log writes | ✅ Logs created for all events | N/A |

**Test Environment:**
- Development: Local SQL Server + Azure emulators
- Staging: Azure SQL Database + Azure services (pre-production)
- Production: Full Azure stack

**Definition of Done (Testing):**
- ✅ All unit tests pass (80%+ coverage)
- ✅ All integration tests pass
- ✅ All E2E tests pass for critical paths
- ✅ All UX/UI component tests pass with accessibility compliance
- ✅ User journey tests pass (<5 minute onboarding completion)
- ✅ No critical security vulnerabilities
- ✅ Performance targets met (< 500ms p95 for auth endpoints)
- ✅ UX metrics targets met (>85% onboarding completion, >90% error recovery)
- ✅ Manual testing completed for all acceptance criteria
- ✅ Code review completed with security and UX checklists
- ✅ Accessibility audit passed (WCAG 2.1 AA compliance)
- ✅ Mobile/tablet responsive testing completed

