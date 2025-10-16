# ADR-001: Database Schema Organization Strategy

**Status:** Accepted  
**Date:** 2025-10-16  
**Deciders:** Anthony Keevy (Product Owner), Winston (Architect)  
**Context:** Epic 1 - Authentication & Onboarding

---

## Context and Problem Statement

EventLeadPlatform requires a scalable, maintainable database architecture to support multi-tenant SaaS operations with strict data isolation, comprehensive audit trails, and high-performance querying. 

**Key Questions:**
- Should we organize tables using SQL Server schemas, or use a flat structure in `dbo`?
- How should we logically separate different types of data (business vs logging vs reference)?
- How can we improve backup/archiving strategies and security boundaries?

**Constraints:**
- Must support multi-tenant data isolation
- Must maintain clear separation between business data, logs, and reference data
- Must support different retention policies (logs = 90 days, audit = 7 years, business data = permanent)
- Must enable efficient backups and disaster recovery

---

## Decision Drivers

1. **Clarity:** Developers should instantly understand a table's purpose from its schema
2. **Security:** Need granular permissions (e.g., read-only access to logs, restricted access to audit data)
3. **Performance:** Different data types have different indexing and query patterns
4. **Lifecycle Management:** Different retention policies require different backup/archiving strategies
5. **Compliance:** Audit data requires special handling for regulatory requirements (7-year retention)
6. **Scalability:** Logging tables generate high write volume and need different optimization strategies

---

## Considered Options

### **Option A: Flat Structure (All Tables in `dbo` Schema)**

```sql
dbo.User
dbo.Company
dbo.Form
dbo.ApiRequest          -- Log table
dbo.ActivityLog         -- Audit table
dbo.Country             -- Reference table
dbo.ABRSearch           -- Cache table
```

**Pros:**
- ✅ Simplest approach (default SQL Server behavior)
- ✅ No schema-qualified queries needed (shorter SQL)
- ✅ Familiar to developers not experienced with schemas

**Cons:**
- ❌ No logical organization (100+ tables all in one namespace)
- ❌ Cannot apply schema-level permissions (must grant table-by-table)
- ❌ Cannot apply different backup strategies per data type
- ❌ Queries don't reveal data type (`SELECT * FROM ApiRequest` - is this business data or logging?)
- ❌ Cannot separate by lifecycle (logs vs permanent business data)

---

### **Option B: Two-Schema Approach (`dbo` + `logging`)**

```sql
dbo.User                -- Business data
dbo.Company
dbo.Form
logging.ApiRequest      -- Logs
logging.ActivityLog
```

**Pros:**
- ✅ Separates business data from logs
- ✅ Can apply different backup strategies
- ✅ Simple two-category mental model

**Cons:**
- ⚠️ Still mixes reference data with business data
- ⚠️ No distinction between compliance audit (7-year retention) and operational logs (90-day retention)
- ⚠️ Cache data mixed with business data
- ⚠️ No separation for configuration data

---

### **Option C: Six-Schema Approach (Full Logical Separation)** ⭐ **CHOSEN**

```sql
dbo.User                    -- Core business entities
dbo.Company
dbo.Form

ref.Country                 -- Reference/lookup data
ref.Language
ref.UserRole

config.AppSetting           -- Runtime configuration
config.ValidationRule

log.ApiRequest              -- Technical logging
log.AuthEvent
log.ApplicationError

audit.ActivityLog           -- Compliance audit trail
audit.User                  // User record changes
audit.Company

cache.ABRSearch             -- External API cache
```

**Pros:**
- ✅ **Self-documenting:** Query reveals data type (`SELECT * FROM log.ApiRequest` - clearly logging)
- ✅ **Security boundaries:** Grant permissions at schema level (read-only on `log`, restricted on `audit`)
- ✅ **Lifecycle management:** Different retention policies per schema
- ✅ **Backup strategies:** Critical backups (hourly) for `dbo`/`audit`, less frequent for `log`
- ✅ **Performance optimization:** Different indexing strategies per schema (write-heavy logs vs read-heavy references)
- ✅ **Compliance:** Clear separation of audit data (cannot be accidentally truncated)
- ✅ **Scalability:** Can move schemas to different filegroups/disks for I/O optimization

**Cons:**
- ⚠️ Schema-qualified queries required (`SELECT * FROM ref.Country` not `SELECT * FROM Country`)
- ⚠️ Slightly more complex for developers unfamiliar with schemas
- ⚠️ Cross-schema foreign keys (but this is a non-issue in SQL Server)

---

## Decision Outcome

**Chosen Option:** Option C - Six-Schema Approach

**Rationale:**
- EventLeadPlatform is an enterprise SaaS platform that will grow to 100+ tables across multiple epics
- Clear organization NOW prevents confusion and refactoring later
- Multi-tenant isolation requires strict security boundaries (schema-level permissions)
- Compliance requirements (7-year audit retention) demand clear separation
- Logging volume will be high (every API request logged) - needs separate optimization

---

## Schema Definitions

### **1. `dbo` Schema - Core Business Entities**
**Purpose:** Primary business data customers pay for  
**Retention:** Permanent (soft delete only, never hard delete)  
**Backup Priority:** CRITICAL (hourly backups, point-in-time recovery)  
**Write Volume:** Medium  

**Tables:** User, Company, UserCompany, Event, Form, Submission, Payment, Invoice, Image

---

### **2. `ref` Schema - Reference/Lookup Data**
**Purpose:** Static or slowly-changing reference data  
**Retention:** Permanent  
**Backup Priority:** MEDIUM (changes rarely, can be restored from seed scripts)  
**Write Volume:** VERY LOW (admin changes only)  

**Tables:** Country, Language, Industry, UserRole, UserStatus, CustomerTier

**Characteristics:**
- Very low write volume (almost read-only)
- High read volume (used in every query for dropdowns/lookups)
- Excellent candidate for in-memory caching
- Small tables (10-1000 rows max)

---

### **3. `config` Schema - Runtime Configuration**
**Purpose:** Application configuration parameters (business rules, feature flags)  
**Retention:** Permanent with change history  
**Backup Priority:** HIGH (critical for application behavior)  
**Write Volume:** VERY LOW (admin changes only)  

**Tables:** AppSetting, ValidationRule, FeatureFlag (future)

**Characteristics:**
- Critical for application behavior (controls password policies, token expiry, validation rules)
- Changes require careful audit trail
- Cached aggressively in application layer
- Admin-only modifications

---

### **4. `log` Schema - Technical Logging**
**Purpose:** Application logging for debugging, monitoring, diagnostics  
**Retention:** 90 days, then archive or delete  
**Backup Priority:** MEDIUM (can be rebuilt from application logs if needed)  
**Write Volume:** VERY HIGH (every API request logged)  

**Tables:** ApiRequest, AuthEvent, ApplicationError, Performance

**Characteristics:**
- Highest write volume (every request generates log entry)
- Rarely queried (only for debugging/monitoring)
- Can be on separate filegroup (different disk for I/O optimization)
- Simple indexes optimized for writes
- Aggressive archiving strategy (move to cold storage after 90 days)

---

### **5. `audit` Schema - Compliance Audit Trail**
**Purpose:** Immutable audit trail for compliance (who did what when)  
**Retention:** 7 years (regulatory compliance requirement)  
**Backup Priority:** CRITICAL (legal/compliance requirement, cannot lose)  
**Write Volume:** Medium (business actions only, not every API call)  

**Tables:** ActivityLog, User (snapshots), Company (snapshots), Role (changes)

**Characteristics:**
- Append-only (NEVER update or delete audit records)
- Queried for compliance reports and investigations
- May require legal hold capability (suspend archiving on demand)
- Different from logging (compliance vs debugging)
- Must survive disaster recovery scenarios

---

### **6. `cache` Schema - External API Cache**
**Purpose:** Cache for external API results (safe to delete/rebuild)  
**Retention:** 30-90 days, then delete  
**Backup Priority:** LOW (can be rebuilt from source APIs)  
**Write Volume:** Medium  

**Tables:** ABRSearch, Geocoding (future), EmailValidation (future)

**Characteristics:**
- Can be truncated without data loss (performance optimization, not source of truth)
- Improves performance and reduces external API costs
- TTL-based expiration (rows auto-delete after 30 days)
- May not need full audit columns

---

## Implementation Details

### **SQLAlchemy Configuration**

```python
# backend/models/user.py
class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}  # Specify schema explicitly
    
    user_id = Column('UserID', BigInteger, primary_key=True)
    # ... columns

# backend/models/country.py
class Country(Base):
    __tablename__ = 'Country'
    __table_args__ = {'schema': 'ref'}  # Reference schema
    
    country_id = Column('CountryID', BigInteger, primary_key=True)
    # ... columns
```

### **Alembic Migration**

```python
def upgrade():
    # Create schemas (only once in initial migration)
    op.execute("CREATE SCHEMA log;")
    op.execute("CREATE SCHEMA ref;")
    op.execute("CREATE SCHEMA config;")
    op.execute("CREATE SCHEMA audit;")
    op.execute("CREATE SCHEMA cache;")
    
    # Create tables in appropriate schemas
    op.create_table(
        'Country',
        sa.Column('CountryID', sa.BigInteger(), nullable=False),
        sa.Column('CountryName', sa.NVARCHAR(100), nullable=False),
        schema='ref'  # Specify schema
    )
```

### **Cross-Schema Foreign Keys**

```sql
-- User table (dbo schema) references Country (ref schema)
CREATE TABLE [dbo].[User] (
    UserID BIGINT PRIMARY KEY,
    CountryID BIGINT NULL,
    CONSTRAINT FK_User_Country FOREIGN KEY (CountryID) 
        REFERENCES [ref].[Country](CountryID)  -- Cross-schema FK
);
```

**Note:** SQL Server fully supports cross-schema foreign keys with no performance penalty.

---

## Consequences

### **Positive:**

1. **Self-Documenting Queries:**
   ```sql
   -- Instantly clear this is logging data
   SELECT * FROM log.ApiRequest WHERE StatusCode = 500;
   
   -- Instantly clear this is reference data
   SELECT * FROM ref.Country WHERE CountryCode = 'AU';
   ```

2. **Schema-Level Permissions:**
   ```sql
   -- Grant read-only access to logs for support team
   GRANT SELECT ON SCHEMA::log TO SupportTeam;
   
   -- Restrict audit data to compliance officers only
   GRANT SELECT ON SCHEMA::audit TO ComplianceOfficers;
   REVOKE ALL ON SCHEMA::audit TO Developers;
   ```

3. **Lifecycle Management:**
   ```sql
   -- Archive logs older than 90 days
   DELETE FROM log.ApiRequest WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
   
   -- NEVER delete audit data (7-year retention)
   -- Automated job prevents deletion from audit schema
   ```

4. **Backup Strategies:**
   ```
   dbo schema:   Hourly full backup + point-in-time recovery
   audit schema: Hourly full backup + immutable backups
   ref schema:   Daily backup (changes rarely)
   config schema: Hourly backup (critical for app behavior)
   log schema:   Daily backup (can lose some logs if disaster)
   cache schema: No backup (can be rebuilt from APIs)
   ```

5. **Performance Optimization:**
   ```sql
   -- Move log schema to separate filegroup on faster disk
   ALTER DATABASE EventLeadPlatform ADD FILEGROUP LogFileGroup;
   ALTER DATABASE EventLeadPlatform ADD FILE (NAME='LogData', FILENAME='E:\Logs\log.ndf') TO FILEGROUP LogFileGroup;
   CREATE TABLE log.ApiRequest (...) ON LogFileGroup;
   ```

### **Negative:**

1. **Schema-Qualified Queries Required:**
   - Developers must write `SELECT * FROM ref.Country` not `SELECT * FROM Country`
   - **Mitigation:** SQLAlchemy abstracts this (model configuration handles schema)

2. **Learning Curve:**
   - Developers unfamiliar with schemas need brief training
   - **Mitigation:** This ADR documents the approach, plus quick-reference guides

3. **Cross-Schema Foreign Keys:**
   - Slightly more verbose constraint definitions
   - **Mitigation:** Non-issue in SQL Server (full support, no performance penalty)

---

## Compliance with Standards

**BMAD v6 Alignment:**
- ✅ Architecture Decision Record created (documents rationale)
- ✅ Aligns with BMAD principle: "Architecture drives implementation"
- ✅ Forward-looking (prepares for 100+ tables across 8 epics)

**Anthony's Database Standards:**
- ✅ Maintains PascalCase naming for all tables/columns
- ✅ Preserves audit column requirements
- ✅ Supports multi-tenant isolation patterns
- ✅ Enhances security and compliance capabilities

**Industry Best Practices:**
- ✅ Follows SQL Server schema best practices (logical organization)
- ✅ Aligns with microservices patterns (clear boundaries)
- ✅ Supports compliance requirements (GDPR, Australian Privacy Principles)

---

## References

- Solution Architecture: `docs/solution-architecture.md` (Database Architecture section)
- Database Rebuild Plan: `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md`
- SQL Server Schemas Documentation: https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema
- OWASP Security Best Practices: Row-Level Security and multi-tenant patterns

---

## Approval

**Approved by:** Anthony Keevy  
**Date:** 2025-10-16  
**Status:** Accepted - Implemented in Epic 1 database rebuild

---

**Winston** 🏗️  
*"Architecture is about organization. Schemas are our filing system."*

