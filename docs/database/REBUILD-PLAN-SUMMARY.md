# Database Rebuild Plan - Epic 1 (Executive Summary)

**Date:** October 16, 2025  
**Architect:** Winston 🏗️ + Solomon 📜  
**Status:** ✅ APPROVED - Ready for execution  
**Version:** 2.0 (Rationalized)

---

## 🎯 Executive Summary

**Objective:** Drop existing database and rebuild from scratch with 45 tables across 6 schemas for Epic 1 (Authentication & Onboarding).

**Why Rebuild?**
- Fix standards violations in existing database (wrong primary keys, naming issues)
- Implement 6-schema organization (`dbo`, `ref`, `config`, `log`, `audit`, `cache`)
- Establish proper reference tables for enum-like fields (14 new reference tables)
- Integrate Dimitri's comprehensive ABR and User domain designs
- Start Epic 1 development with clean, standards-compliant foundation

**Approach:**
- Single Alembic migration (clean history)
- All tables created with proper schemas, constraints, indexes
- Seed data for all reference tables and initial configuration
- Zero production data loss (development database only)

---

## 📊 Database Statistics

| Metric | Count | Details |
|--------|-------|---------|
| **Total Tables** | 45 | Across 6 schemas |
| **Core Business Tables** | 13 | `dbo` schema |
| **Reference Tables** | 14 | `ref` schema (lookup/enum data) |
| **Configuration Tables** | 2 | `config` schema (AppSetting, ValidationRule) |
| **Logging Tables** | 4 | `log` schema (technical logs) |
| **Audit Tables** | 4 | `audit` schema (compliance audit trail) |
| **Cache Tables** | 1 | `cache` schema (ABR search results) |
| **Foreign Keys** | ~60 | Referential integrity enforced |
| **Unique Constraints** | ~25 | Data uniqueness enforced |
| **Indexes** | ~40 | Performance optimization |
| **Seed Records** | ~150 | Initial data for reference tables |

---

## 🗂️ Schema Organization

### **1. `dbo` Schema - Core Business Entities**
**Purpose:** Primary business data (user accounts, companies, invitations)  
**Tables:** 13  
**Retention:** Permanent (soft delete only)  
**Priority:** CRITICAL (hourly backups)

| Table | Purpose | Key Fields |
|-------|---------|----------|
| `User` | User accounts | UserID, Email, StatusID |
| `Company` | Company profiles | CompanyID, CompanyName, ABN |
| `UserCompany` | User-company relationships | UserCompanyID, UserID, CompanyID |
| `CompanyCustomerDetails` | Customer subscription data | CompanyID, CustomerTierID |
| `CompanyBillingDetails` | Billing information | CompanyID, BillingEmail |
| `CompanyOrganizerDetails` | Event organizer data | CompanyID, Website |
| `UserInvitation` | Team invitations | UserInvitationID, InvitedEmail, StatusID |
| `UserEmailVerificationToken` | Email verification | UserEmailVerificationTokenID, Token, ExpiresAt |
| `UserPasswordResetToken` | Password reset | UserPasswordResetTokenID, Token, ExpiresAt |

**See:** `docs/database/schema-reference/dbo-schema.md` for full definitions

---

### **2. `ref` Schema - Reference/Lookup Data**
**Purpose:** Static or slowly-changing lookup data  
**Tables:** 14  
**Retention:** Permanent  
**Priority:** MEDIUM (daily backups, can restore from seed)

**Reference Tables:**
1. `Country` - Country lookup (with currency, tax, integration config)
2. `Language` - Language lookup
3. `Industry` - Industry lookup
4. `UserStatus` - User status (active, pending, suspended, locked)
5. `UserInvitationStatus` - Invitation status (pending, accepted, declined, expired, cancelled)
6. `UserRole` - System-level roles (system_admin, company_user)
7. `UserCompanyRole` - Company-level roles (company_admin, company_user, company_viewer)
8. `UserCompanyStatus` - User-company status (active, suspended, removed)
9. `SettingCategory` - AppSetting categories (authentication, validation, email)
10. `SettingType` - AppSetting data types (integer, boolean, string, json)
11. `RuleType` - ValidationRule types (phone, postal_code, tax_id)
12. `CustomerTier` - Subscription tiers (free, starter, professional, enterprise)
13. `JoinedVia` - How user joined company (signup, invitation, transfer)

**See:** `docs/database/schema-reference/ref-schema.md` for full definitions

---

### **3. `config` Schema - Runtime Configuration**
**Purpose:** Application configuration parameters  
**Tables:** 2  
**Retention:** Permanent with change history  
**Priority:** HIGH (critical for application behavior)

| Table | Purpose | Records |
|-------|---------|---------|
| `AppSetting` | Business rules (password policy, token expiry) | ~15 |
| `ValidationRule` | Country-specific validation patterns | ~20 |

**Key Configuration:**
- Password policy: Min length 8, expiry 90 days
- Token expiry: Access 15 min, refresh 7 days, verification 24 hrs
- Country-specific validation patterns (phone, postal, tax ID formats)

**See:** `docs/database/schema-reference/config-schema.md` for full definitions

---

### **4. `log` Schema - Technical Logging**
**Purpose:** Application logging for debugging/monitoring  
**Tables:** 4  
**Retention:** 90 days, then archive  
**Priority:** MEDIUM (high write volume, rarely queried)

| Table | Purpose | Write Volume |
|-------|---------|--------------|
| `ApiRequest` | HTTP request/response logging | VERY HIGH (every request) |
| `AuthEvent` | Authentication events | MEDIUM (login/logout) |
| `ApplicationError` | Application errors | LOW (errors only) |
| `EmailDelivery` | Email delivery tracking | MEDIUM (verification, reset, invitations) |

**See:** `docs/database/schema-reference/log-schema.md` for full definitions

---

### **5. `audit` Schema - Compliance Audit Trail**
**Purpose:** Immutable audit trail for compliance  
**Tables:** 4  
**Retention:** 7 years (regulatory requirement)  
**Priority:** CRITICAL (legal/compliance)

| Table | Purpose | Audit Scope |
|-------|---------|-------------|
| `ActivityLog` | Business actions | All user actions (login, create, update, delete) |
| `User` | User snapshots | User record changes (before/after) |
| `Company` | Company snapshots | Company record changes |
| `Role` | Role changes | User role assignments/changes |

**See:** `docs/database/schema-reference/audit-schema.md` for full definitions

---

### **6. `cache` Schema - External API Cache**
**Purpose:** Cache for external API results  
**Tables:** 1  
**Retention:** 30-90 days  
**Priority:** LOW (can be rebuilt from source)

| Table | Purpose | TTL |
|-------|---------|-----|
| `ABRSearch` | ABR API results | 90 days |

**See:** `docs/database/schema-reference/cache-schema.md` for full definitions

---

## 🔑 Key Architectural Decisions

### **1. Schema Organization (ADR-001)**
**Decision:** Use 6 SQL Server schemas for logical separation  
**Rationale:** Security boundaries, lifecycle management, backup strategies  
**Impact:** Self-documenting queries, schema-level permissions

### **2. Backend Abstraction Layer (ADR-002)**
**Decision:** 3-layer abstraction (SQLAlchemy, Pydantic, Service)  
**Rationale:** Isolate database naming from frontend  
**Impact:** Database refactoring doesn't break frontend

### **3. Naming Conventions (ADR-003)**
**Decision:** PascalCase (DB) → snake_case (Python) → camelCase (API)  
**Rationale:** Each layer uses native convention  
**Impact:** Idiomatic code in every layer

### **4. Database Normalization (ADR-004)**
**Decision:** Reference tables for all enum-like fields  
**Rationale:** Data integrity, extensibility, UI metadata  
**Impact:** 14 reference tables, ~60 foreign keys

**See:** `docs/architecture/decisions/` for full ADR documents

---

## 🌐 International Readiness

### **Country Table Enhancements:**
- **Currency:** CurrencyCode (ISO 4217), CurrencySymbol, CurrencyName
- **Tax:** TaxRate, TaxName, TaxInclusive, TaxNumberLabel
- **Integrations:** CompanyValidationProvider, AddressValidationProvider, IntegrationConfig (JSON)

**Example (Australia):**
```json
{
  "countryCode": "AU",
  "currencyCode": "AUD",
  "currencySymbol": "$",
  "taxRate": 0.10,
  "taxName": "GST",
  "taxInclusive": false,
  "taxNumberLabel": "ABN",
  "companyValidationProvider": "ABR",
  "addressValidationProvider": "Geoscape",
  "integrationConfig": {
    "abrApiUrl": "https://abr.business.gov.au/json/",
    "geoscapeApiUrl": "https://api.geoscape.com.au/"
  }
}
```

---

## 🚀 Advanced Features Included

### **1. JWT Session Management (Logout All Devices)**
**Fields Added to User:**
- `SessionToken` (NVARCHAR(255)) - Current session identifier
- `AccessTokenVersion` (INT) - Increment to invalidate all access tokens
- `RefreshTokenVersion` (INT) - Increment to invalidate all refresh tokens

**Use Cases:**
- Password reset → Increment all → All devices logged out
- Security event → Increment AccessTokenVersion → Force re-login

---

### **2. ABR Integration (Australian Business Register)**
**Dimitri's Full Design Integrated:**
- `LegalEntityName` - Official ABR name
- `BusinessNames` (JSON array) - All trading names
- `CustomDisplayName` - User override
- `DisplayNameSource` (legal, custom, business)
- `ABNStatus`, `EntityType`, `GSTRegistered`
- `ParentCompanyID` - Hierarchical company relationships

**ABRSearch Cache:**
- Supports multi-search (ABN, ACN, Name)
- Composite primary key: (SearchType, SearchValue)
- Full JSON response cached for 90 days

---

### **3. User Domain Enhancements**
**Dimitri's Full User Design:**
- **Profile:** RoleTitle, ProfilePictureUrl, TimezoneIdentifier (IANA)
- **Security:** EmailVerifiedAt, LastPasswordChange, FailedLoginAttempts
- **Audit:** Self-referential FKs (CreatedBy, UpdatedBy, DeletedBy → UserID)
- **Status:** IsLocked, LockedUntil, LockedReason

---

### **4. Comprehensive Invitation Lifecycle**
**Fields Added:**
- `CancelledAt`, `CancelledBy`, `CancellationReason`
- `DeclinedAt`, `DeclineReason`
- `ResendCount`, `LastResentAt` (rate limiting)

---

### **5. UserCompany Relationship Tracking**
**Fields Added:**
- `Status` → FK to `ref.UserCompanyStatus` (active, suspended, removed)
- `JoinedVia` → FK to `ref.JoinedVia` (signup, invitation)
- `RemovedDate`, `RemovedBy`, `RemovalReason`

---

## 📦 Seed Data Summary

### **Reference Tables (Initial Population):**

| Table | Records | Examples |
|-------|---------|----------|
| `Country` | 1 (AU) | Australia (expandable to 250+) |
| `Language` | 1 (EN) | English (expandable to 100+) |
| `Industry` | 0 | TBD (future seed) |
| `UserStatus` | 4 | active, pending, suspended, locked |
| `UserInvitationStatus` | 5 | pending, accepted, declined, expired, cancelled |
| `UserRole` | 2 | system_admin, company_user |
| `UserCompanyRole` | 3 | company_admin, company_user, company_viewer |
| `UserCompanyStatus` | 3 | active, suspended, removed |
| `SettingCategory` | 4 | authentication, validation, email, security |
| `SettingType` | 5 | integer, boolean, string, json, decimal |
| `RuleType` | 5 | phone, postal_code, tax_id, email, address |
| `CustomerTier` | 4 | free, starter, professional, enterprise |
| `JoinedVia` | 3 | signup, invitation, transfer |

### **Configuration Tables:**

| Table | Records | Examples |
|-------|---------|----------|
| `AppSetting` | 15 | Password policy, token expiry, rate limits |
| `ValidationRule` | 20 | Phone/postal/tax formats per country |

**See:** `docs/database/seed-data.sql` for full seed data

---

## 🛠️ Implementation Steps

### **Phase 1: Database Reset**
1. Stop all backend services
2. Drop existing database: `DROP DATABASE EventLeadPlatform`
3. Create new database: `CREATE DATABASE EventLeadPlatform`
4. Create 6 schemas: `dbo`, `ref`, `config`, `log`, `audit`, `cache`

### **Phase 2: Reset Alembic**
1. Delete `backend/migrations/versions/*.py` (clear migration history)
2. Reset Alembic: `alembic stamp base`
3. Create initial migration: `alembic revision -m "Epic 1 database structure"`

### **Phase 3: Create Migration**
1. Copy SQL definitions from schema-reference docs
2. Create all 45 tables in single migration
3. Insert seed data for all reference tables
4. Verify constraints and indexes

### **Phase 4: Execute & Verify**
1. Run migration: `alembic upgrade head`
2. Verify table count: `SELECT COUNT(*) FROM sys.tables` (should be 45)
3. Verify schemas: `SELECT DISTINCT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES`
4. Verify seed data: `SELECT COUNT(*) FROM ref.UserStatus` (should be 4)
5. Test foreign keys: Attempt invalid insert (should fail)

---

## ✅ Success Criteria

- [ ] All 45 tables created across 6 schemas
- [ ] All foreign keys enforced (test invalid inserts fail)
- [ ] All unique constraints enforced (test duplicate inserts fail)
- [ ] All indexes created (query `sys.indexes`)
- [ ] All seed data populated (150+ records across reference tables)
- [ ] Alembic migration history clean (only 1 initial migration)
- [ ] No Solomon violations (run audit after creation)
- [ ] Backend can connect and query tables
- [ ] All table documentation up to date

---

## 📚 Related Documentation

**Architecture:**
- `docs/solution-architecture.md` - Overall system architecture
- `docs/architecture/decisions/ADR-001-database-schema-organization.md`
- `docs/architecture/decisions/ADR-002-backend-abstraction-layer.md`
- `docs/architecture/decisions/ADR-003-naming-convention-strategy.md`
- `docs/architecture/decisions/ADR-004-database-normalization.md`

**Database Details:**
- `docs/database/schema-reference/dbo-schema.md` - Core business tables (13)
- `docs/database/schema-reference/ref-schema.md` - Reference tables (14)
- `docs/database/schema-reference/config-schema.md` - Configuration tables (2)
- `docs/database/schema-reference/audit-schema.md` - Audit tables (4)
- `docs/database/schema-reference/log-schema.md` - Logging tables (4)
- `docs/database/schema-reference/cache-schema.md` - Cache tables (1)
- `docs/database/seed-data.sql` - All seed INSERT statements

**Implementation Guides:**
- `docs/technical-guides/backend-database-abstraction-layer.md` - Backend patterns
- `docs/technical-guides/backend-quick-reference.md` - 1-page cheat sheet
- `docs/technical-guides/database-quick-reference.md` - Table list + ERD

---

## 🔄 Next Steps After Database Rebuild

**Immediate (Day 1):**
1. ✅ Verify database creation successful
2. ✅ Test backend connection
3. ✅ Create SQLAlchemy models for all tables
4. ✅ Create Pydantic schemas for API contracts
5. ✅ Create service layer templates

**Short-term (Week 1):**
1. Implement Story 1.1 (User Signup with validation)
2. Implement Story 1.2 (Email Verification flow)
3. Implement Story 1.3 (Login & JWT authentication)

**Mid-term (Week 2-3):**
1. Implement remaining Epic 1 stories (Company Onboarding, Team Invitations)
2. Add logging middleware (populate `log` tables)
3. Add audit middleware (populate `audit` tables)

---

## ⚠️ Known Limitations & Future Enhancements

**Current Scope (Epic 1 Only):**
- No Event, Form, Submission tables (Epic 2+)
- No Image table (Epic 6)
- No Payment, Invoice tables (Epic 7)
- Basic seed data only (Australia, English)

**Future Enhancements:**
- Add remaining countries (250+)
- Add remaining languages (100+)
- Add industry seed data
- Add timezone reference table (post-MVP)
- Add feature flags to CustomerTier
- Add password history (prevent reuse)
- Add API rate limiting table (track per-user quotas)

---

## 👥 Approvals

**Reviewed by:**
- ✅ Anthony Keevy (Product Owner) - 2025-10-16
- ✅ Winston (Architect) - 2025-10-16
- ✅ Solomon (Database Validator) - 2025-10-16
- ✅ Dimitri (Data Domain Architect) - Designs integrated

**Status:** ✅ APPROVED - Ready for execution

---

**Winston** 🏗️ + **Solomon** 📜  
*"A solid foundation makes all the difference."*

