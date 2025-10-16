# Database Schema Organization Strategy
**Date:** October 16, 2025  
**Author:** Solomon 📜 with Anthony  
**Purpose:** Define SQL Server schema organization for EventLeadPlatform

---

## 🎯 EXECUTIVE SUMMARY

**Question:** Should we use SQL Server schemas (not table schemas) to organize tables logically?

**Answer:** **YES** - Using schemas is best practice for enterprise databases and provides significant benefits for logging, security, maintenance, and organization.

---

## SQL SERVER SCHEMAS EXPLAINED

**What is a Schema?** (Not to be confused with "table schema")
- A **namespace** or **container** for database objects (tables, views, procedures)
- Default schema in SQL Server: `dbo` (database owner)
- Every table has a schema: `[SchemaName].[TableName]`
- Example: `log.ApiRequest` vs `dbo.User`

**NOT the same as:**
- "Table schema" (columns, data types) - different meaning
- "Database schema" (entire database structure) - different meaning

---

## ✅ BENEFITS OF USING SCHEMAS

### 1. **Logical Organization (Clarity)**
```sql
-- WITHOUT schemas (all in dbo)
dbo.User
dbo.Company
dbo.ApiRequestLog
dbo.AuthEventLog
dbo.ActivityLog
dbo.Country
dbo.Language
dbo.AppSetting

-- WITH schemas (organized)
dbo.User                    -- Core business entity
dbo.Company                 -- Core business entity
log.ApiRequest              -- Logging data
log.AuthEvent               -- Logging data
audit.ActivityLog           -- Audit trail
ref.Country                 -- Reference data
ref.Language                -- Reference data
config.AppSetting           -- Configuration
```

**Benefit:** Instantly know the purpose of a table from its schema name.

---

### 2. **Security (Permission Management)**
```sql
-- Grant read-only access to all logging tables at once
GRANT SELECT ON SCHEMA::log TO [AnalyticsTeam];

-- Grant read/write to reference data maintainers
GRANT SELECT, INSERT, UPDATE ON SCHEMA::ref TO [DataStewardTeam];

-- Deny access to audit tables (except admins)
DENY SELECT ON SCHEMA::audit TO [StandardUsers];
```

**Benefit:** Manage permissions at schema level instead of table-by-table.

---

### 3. **Maintenance & Operations**
```sql
-- Backup only logging data (separate schedule)
BACKUP DATABASE EventLeadPlatform 
    FILEGROUP = [LogFileGroup]  -- log schema on separate filegroup

-- Archive old logging data
SELECT * INTO archive.ApiRequest_2024 
FROM log.ApiRequest 
WHERE CreatedDate < '2024-01-01';

-- Truncate all logging tables for testing
-- Easy to identify which tables are logs
TRUNCATE TABLE log.ApiRequest;
TRUNCATE TABLE log.AuthEvent;
```

**Benefit:** Easier to identify, backup, archive, and maintain related tables.

---

### 4. **Query Clarity (Self-Documenting)**
```sql
-- Query is self-documenting
SELECT u.UserID, u.Email, ar.RequestPath, ar.StatusCode
FROM dbo.User u
INNER JOIN log.ApiRequest ar ON ar.UserID = u.UserID
WHERE ar.CreatedDate > GETUTCDATE() - 1;

-- Immediately clear:
-- - dbo.User = core business entity
-- - log.ApiRequest = logging data
```

**Benefit:** Queries are more readable, intent is clearer.

---

### 5. **Data Lifecycle Management**
```sql
-- Logging data: Retain 90 days, then archive
-- Schema: log.*

-- Audit data: Retain 7 years (compliance), NEVER delete
-- Schema: audit.*

-- Reference data: Rarely changes, no archiving needed
-- Schema: ref.*

-- Cache data: Ephemeral, safe to truncate/rebuild
-- Schema: cache.*
```

**Benefit:** Clear data retention policies per schema.

---

## 🏗️ RECOMMENDED SCHEMA ORGANIZATION

### For EventLeadPlatform (Medium Complexity)

**1. `dbo` Schema (Core Business Entities)**
- **Purpose:** Primary business entities (customers pay for this data)
- **Retention:** Permanent (soft delete only)
- **Backup Priority:** CRITICAL - Most frequent backups
- **Tables:**
  - `User` - Core user entity
  - `Company` - Core company entity
  - `Event` - Core event entity
  - `Form` - Core form builder
  - `Submission` - Core lead capture
  - `Image` - Core image storage
  - `Payment` - Core payment transactions
  - `Invoice` - Core billing
  - `Invitation` - Core team invitations

---

**2. `log` Schema (Application Logging)**
- **Purpose:** Technical logging for debugging, monitoring, diagnostics
- **Retention:** 90 days, then archive or delete
- **Backup Priority:** MEDIUM - Can rebuild from app logs if needed
- **Tables:**
  - `ApiRequest` - HTTP request/response logging
  - `AuthEvent` - Authentication events (login, logout, token refresh)
  - `ErrorLog` - Application errors and exceptions
  - `PerformanceLog` - Slow query tracking, operation timing
  - `EmailLog` - Email delivery tracking
  - `WebSocketLog` - WebSocket connection/disconnection events

**Characteristics:**
- High write volume (every API request logged)
- Rarely queried (only for debugging)
- Can be on separate filegroup (different disk for I/O)
- Can use simpler indexes (fewer, lighter)

---

**3. `audit` Schema (Compliance & Audit Trail)**
- **Purpose:** Immutable audit trail for compliance (who did what when)
- **Retention:** 7 years (regulatory compliance)
- **Backup Priority:** CRITICAL - Legal/compliance requirement
- **Tables:**
  - `ActivityLog` - All user actions (CRUD operations)
  - `AuditUser` - User record changes (before/after)
  - `AuditCompany` - Company record changes
  - `AuditForm` - Form changes (design history)
  - `AuditRole` - Role changes (RBAC audit)

**Characteristics:**
- Append-only (NEVER update or delete)
- Medium write volume (business actions only)
- Queried for compliance reports
- May need legal hold capability

---

**4. `ref` Schema (Reference/Lookup Data)**
- **Purpose:** Static or slowly-changing reference data
- **Retention:** Permanent (reference data)
- **Backup Priority:** MEDIUM - Changes rarely
- **Tables:**
  - `Country` - Country lookup
  - `Language` - Language lookup
  - `Industry` - Industry lookup
  - `UserRole` - User role definitions (if table-based, not enum)
  - `InvitationStatus` - Invitation status lookup (if table-based)
  - `UserStatus` - User status lookup (if table-based)

**Characteristics:**
- Very low write volume (admin changes only)
- High read volume (every form, every query)
- Excellent candidate for caching
- Small tables (100-1000 rows max)

---

**5. `config` Schema (Configuration Management)**
- **Purpose:** Runtime application configuration
- **Retention:** Permanent with change history
- **Backup Priority:** HIGH - Critical for app behavior
- **Tables:**
  - `AppSetting` - Runtime business rules
  - `ValidationRule` - Country-specific validation
  - `FeatureFlag` - Feature toggles (future)
  - `PricingTier` - Subscription pricing (future)

**Characteristics:**
- Very low write volume (admin changes only)
- Medium read volume (cached in app)
- Changes require careful audit trail

---

**6. `cache` Schema (Ephemeral Cache Data)**
- **Purpose:** Cache for external API results (safe to delete/rebuild)
- **Retention:** 30-90 days, then delete
- **Backup Priority:** LOW - Can be rebuilt from source
- **Tables:**
  - `ABRSearchCache` - ABR API lookup cache
  - `GeocodingCache` - Address geocoding cache (future)
  - `EmailValidationCache` - Email validation cache (future)

**Characteristics:**
- Can be truncated without data loss
- Improves performance but not critical
- May not need audit columns (CreatedBy, UpdatedBy)

---

## 📊 SCHEMA ORGANIZATION TABLE

| Schema | Purpose | Retention | Backup Priority | Write Volume | Examples |
|--------|---------|-----------|-----------------|--------------|----------|
| **dbo** | Core business | Permanent (soft delete) | CRITICAL | Medium | User, Company, Form, Submission |
| **log** | Technical logging | 90 days | MEDIUM | **Very High** | ApiRequest, AuthEvent, ErrorLog |
| **audit** | Compliance trail | 7 years | CRITICAL | Medium | ActivityLog, AuditUser, AuditForm |
| **ref** | Reference data | Permanent | MEDIUM | Very Low | Country, Language, Industry |
| **config** | Runtime config | Permanent | HIGH | Very Low | AppSetting, ValidationRule |
| **cache** | External API cache | 30-90 days | LOW | Medium | ABRSearchCache, GeocodingCache |

---

## 🎯 RECOMMENDED APPROACH FOR EVENTLEADPLATFORM

### Phase 1: Start Simple (Epic 1-3)
**Use 3 schemas only:**
1. **`dbo`** - All core business tables
2. **`log`** - All logging tables (ApiRequest, AuthEvent, etc.)
3. **`ref`** - All reference data (Country, Language, Industry)

**Why?**
- Simple to implement
- Biggest immediate benefit (separate logging from business data)
- BMAD agents can handle 3 schemas easily
- Alembic migrations straightforward

**Example Migration:**
```python
# Create log schema
op.execute("CREATE SCHEMA log;")

# Create table in log schema
op.create_table(
    'ApiRequest',
    sa.Column('ApiRequestID', sa.BIGINT(), nullable=False),
    sa.Column('RequestPath', sa.NVARCHAR(500), nullable=False),
    # ... columns
    schema='log'  # Specify schema here
)
```

---

### Phase 2: Add Complexity (Epic 4-6)
**Add more schemas:**
4. **`audit`** - Split audit trail from logging
5. **`config`** - Configuration management
6. **`cache`** - External API caching

**Why?**
- As system grows, benefits become clearer
- Team grows, security permissions become important
- Data lifecycle management becomes critical

---

## ⚠️ CONSIDERATIONS & TRADE-OFFS

### Complexity Considerations

**PROS:**
- ✅ Clear logical organization
- ✅ Better security (permission management)
- ✅ Easier maintenance (backups, archiving)
- ✅ Self-documenting queries
- ✅ Data lifecycle management

**CONS:**
- ❌ More complex migrations (must specify schema)
- ❌ SQLAlchemy requires schema configuration
- ❌ BMAD agents must be aware of schemas
- ❌ Cross-schema foreign keys (minor overhead)
- ❌ More moving parts for solo developer

---

### Migration Complexity

**Without Schemas:**
```python
# Simple
op.create_table('ApiRequest', ...)
```

**With Schemas:**
```python
# More explicit (but clearer)
op.execute("CREATE SCHEMA log;")
op.create_table('ApiRequest', ..., schema='log')
```

---

### SQLAlchemy Configuration

**Without Schemas:**
```python
class User(Base):
    __tablename__ = 'User'
```

**With Schemas:**
```python
class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}  # Explicit schema

class ApiRequest(Base):
    __tablename__ = 'ApiRequest'
    __table_args__ = {'schema': 'log'}  # Different schema
```

---

## 🏆 BEST PRACTICES

### 1. Schema Naming Conventions
- ✅ Use lowercase: `log`, `audit`, `ref`, `config`, `cache`
- ✅ Single word, descriptive
- ✅ Consistent across environments
- ❌ Avoid: `tbl_`, `schema_`, version numbers

### 2. Foreign Key Relationships
- ✅ Can reference across schemas: `dbo.User` ← `log.ApiRequest.UserID`
- ✅ Core business entities should be in `dbo`
- ✅ Logging/audit tables reference `dbo` entities

### 3. Schema Permissions (Future)
```sql
-- Developers: Full access to dbo, log, cache
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO [Developers];
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::log TO [Developers];

-- Analytics Team: Read-only to log, audit
GRANT SELECT ON SCHEMA::log TO [AnalyticsTeam];
GRANT SELECT ON SCHEMA::audit TO [AnalyticsTeam];

-- Support Team: Read-only to dbo, log
GRANT SELECT ON SCHEMA::dbo TO [SupportTeam];
GRANT SELECT ON SCHEMA::log TO [SupportTeam];
```

### 4. Backup Strategy by Schema
```sql
-- Critical schemas: Hourly backups
-- dbo, audit

-- Medium priority: Daily backups
-- ref, config

-- Low priority: Weekly backups
-- log, cache (can be rebuilt)
```

---

## 📋 MIGRATION PLAN

### Option A: Start with Schemas (Recommended if starting fresh)
1. Define schemas in first migration (before any tables)
2. All new tables created in appropriate schema
3. BMAD agents configured with schema awareness

### Option B: Migrate Existing Tables (If you have existing dbo tables)
1. Create new schemas
2. Use `ALTER SCHEMA` to move tables
3. Update all foreign keys and indexes
4. Update SQLAlchemy models
5. Test all migrations

**Example:**
```sql
-- Create schemas
CREATE SCHEMA log;
CREATE SCHEMA ref;

-- Move tables
ALTER SCHEMA log TRANSFER dbo.ApiRequestLog;
ALTER SCHEMA ref TRANSFER dbo.Country;

-- Rename if needed
EXEC sp_rename 'log.ApiRequestLog', 'ApiRequest';
```

---

## 🎯 ANTHONY'S LOGGING TABLES

Based on Solution Architecture, these should be in `log` schema:

| Current Name (dbo) | New Name (log schema) | Purpose |
|--------------------|-----------------------|---------|
| `ApiRequestLog` | `log.ApiRequest` | HTTP request/response logging |
| `AuthEventLog` | `log.AuthEvent` | Authentication events |
| `EmailLog` | `log.EmailDelivery` | Email delivery tracking |
| `ErrorLog` | `log.ApplicationError` | Application errors |

**Audit tables** (consider `audit` schema instead):
| Current Name (dbo) | New Name (audit schema) | Purpose |
|--------------------|-----------------------|---------|
| `ActivityLog` | `audit.ActivityLog` | User action audit trail |
| `AuditLog` | `audit.DataChange` | Generic audit trail |
| `AuditUser` | `audit.User` | User record changes |
| `AuditRole` | `audit.Role` | Role changes |

---

## 🎓 RECOMMENDATION FOR ANTHONY

### **RECOMMENDED: Use Schemas (3 schemas to start)**

**Why this is right for you:**
1. ✅ **Your Background:** Enterprise data management experience - you'll appreciate proper organization
2. ✅ **Your Need:** Extensive logging and audit trail - schemas make this manageable
3. ✅ **Your Scale:** Medium-size database (20-30 tables) - schemas prevent table name explosion
4. ✅ **Future Growth:** Team growth - schemas enable better security and permissions
5. ✅ **Maintenance:** Clear data lifecycle (logs vs business data) - easier backups/archiving

**Start with 3 schemas:**
- `dbo` - Core business entities
- `log` - All logging tables (high volume, short retention)
- `ref` - Reference/lookup data

**Add later (Epic 4+):**
- `audit` - Audit trail (separate from logging)
- `config` - Configuration (AppSetting, ValidationRule)
- `cache` - External API cache

---

## 📄 UPDATE REQUIRED DOCUMENTS

If you decide to use schemas, update:
1. **Solution Architecture** - Add schema organization section
2. **Database Standards** - Add schema naming conventions
3. **Tech Spec Epic 1** - Update table names with schemas
4. **Story Context XML** - Include schema in table definitions

---

## 🚀 NEXT STEPS

**If you approve using schemas:**
1. I'll update Solution Architecture with schema organization
2. I'll update Database Standards with schema rules
3. I'll create migration plan for existing tables
4. I'll configure BMAD agents with schema awareness

**Decision needed:**
- Start with 3 schemas (dbo, log, ref)?
- Or stay with default dbo for now?

---

**END OF DOCUMENT**

