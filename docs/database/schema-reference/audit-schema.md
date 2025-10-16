# `audit` Schema - Compliance Audit Trail

**Schema Purpose:** Immutable audit trail for compliance (who did what when)  
**Table Count:** 4  
**Retention:** 7 years (regulatory compliance requirement)  
**Backup Priority:** CRITICAL (legal/compliance requirement, cannot lose)  
**Write Volume:** Medium (business actions only, not every API call)

---

## Schema Overview

The `audit` schema provides a complete, immutable audit trail of all business-critical actions. These tables support compliance requirements (GDPR, Australian Privacy Principles), security investigations, and customer support.

**Key Characteristics:**
- **Append-only:** NEVER update or delete audit records
- **Immutable:** Audit records are permanent evidence
- **Comprehensive:** All user actions logged (login, create, update, delete, role changes)
- **Long retention:** 7 years (compliance requirement)
- **Legal hold capable:** Can freeze deletion for legal investigations

---

## Table Overview

| # | Table | Purpose | Write Volume | Queried By |
|---|-------|---------|--------------|------------|
| 1 | `ActivityLog` | Business actions (login, create, update, delete) | Medium (every user action) | Security team, support |
| 2 | `User` | User record snapshots (before/after changes) | Low (user updates only) | Compliance, support |
| 3 | `Company` | Company record snapshots (before/after changes) | Low (company updates only) | Compliance, support |
| 4 | `Role` | Role assignment changes | Low (role changes only) | Security team, compliance |

---

## 1. `audit.ActivityLog` - Business Action Audit

**Purpose:** Log all business-critical user actions (not technical logs like API requests)

**What Gets Logged:**
- Authentication events (login, logout, password reset)
- Entity creation (user, company, form, event)
- Entity updates (profile changes, company settings)
- Entity deletion (soft delete actions)
- Permission changes (role assignments, team member removal)
- Security events (account lockout, suspicious activity)

**Primary Key:** `ActivityLogID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID` (who performed the action)
- `CompanyID` → `dbo.Company.CompanyID` (tenant context, NULL for system actions)

**Key Columns:**
- `Action` (NVARCHAR(100)) - Action type (e.g., 'user.login', 'form.publish', 'team.invite')
- `EntityType` (NVARCHAR(50)) - Entity affected (e.g., 'User', 'Company', 'Form')
- `EntityID` (BIGINT) - ID of affected entity
- `OldValue` (NVARCHAR(MAX)) - Previous value (JSON snapshot)
- `NewValue` (NVARCHAR(MAX)) - New value (JSON snapshot)
- `IPAddress` (NVARCHAR(50)) - Hashed IP address (privacy-compliant)
- `UserAgent` (NVARCHAR(500)) - Browser/device info
- `RequestID` (NVARCHAR(100)) - Correlation ID (link to log.ApiRequest)
- `CreatedDate` (DATETIME2) - When action occurred (UTC)

**Action Naming Convention:**
- Format: `{domain}.{entity}.{action}`
- Examples:
  - `auth.login.success` / `auth.login.failed`
  - `user.profile.updated`
  - `company.created`
  - `team.user.invited`
  - `form.published`
  - `role.changed`

**Indexes:**
- `IX_ActivityLog_UserID` (find all actions by user)
- `IX_ActivityLog_CompanyID` (find all actions for company)
- `IX_ActivityLog_Action` (filter by action type)
- `IX_ActivityLog_CreatedDate` (time-based queries, archiving)

**Query Patterns:**
```sql
-- User's recent activity (support)
SELECT TOP 100 * 
FROM audit.ActivityLog 
WHERE UserID = @user_id 
ORDER BY CreatedDate DESC;

-- Company audit trail (compliance)
SELECT * 
FROM audit.ActivityLog 
WHERE CompanyID = @company_id 
  AND CreatedDate >= DATEADD(DAY, -30, GETUTCDATE())
ORDER BY CreatedDate DESC;

-- Failed login attempts (security investigation)
SELECT * 
FROM audit.ActivityLog 
WHERE Action = 'auth.login.failed' 
  AND CreatedDate >= DATEADD(HOUR, -1, GETUTCDATE());
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: audit.ActivityLog)

---

## 2. `audit.User` - User Record Snapshots

**Purpose:** Capture before/after snapshots when user records change

**When Records Are Created:**
- User profile updated (name, email, phone)
- User status changed (active → suspended)
- User role changed (company_user → system_admin)
- Security events (account locked, password changed)

**Primary Key:** `AuditUserID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID` (user being audited)
- `ChangedBy` → `dbo.User.UserID` (who made the change, NULL for system changes)

**Key Columns:**
- `UserID` - User being audited
- `FieldName` (NVARCHAR(100)) - Which field changed (e.g., 'Email', 'StatusID')
- `OldValue` (NVARCHAR(MAX)) - Previous value
- `NewValue` (NVARCHAR(MAX)) - New value
- `ChangeType` (NVARCHAR(50)) - Type of change ('update', 'status_change', 'role_change')
- `ChangeReason` (NVARCHAR(500)) - Optional reason (e.g., "Customer requested suspension")
- `ChangedBy` - Who made the change
- `ChangedByEmail` (NVARCHAR(255)) - Email of person who made change (denormalized for reporting)
- `IPAddress`, `UserAgent` - Security context
- `CreatedDate` - When change occurred

**Indexes:**
- `IX_AuditUser_UserID` (find all changes for user)
- `IX_AuditUser_CreatedDate` (time-based queries)
- `IX_AuditUser_FieldName` (filter by field)

**Query Patterns:**
```sql
-- User's change history (compliance, support)
SELECT * 
FROM audit.User 
WHERE UserID = @user_id 
ORDER BY CreatedDate DESC;

-- Who changed their email address recently? (security)
SELECT * 
FROM audit.User 
WHERE FieldName = 'Email' 
  AND CreatedDate >= DATEADD(DAY, -7, GETUTCDATE());
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: audit.User)

---

## 3. `audit.Company` - Company Record Snapshots

**Purpose:** Capture before/after snapshots when company records change

**When Records Are Created:**
- Company profile updated (name, ABN, address)
- Subscription tier changed (free → professional)
- Company status changed (active → suspended)

**Primary Key:** `AuditCompanyID` (BIGINT IDENTITY)

**Foreign Keys:**
- `CompanyID` → `dbo.Company.CompanyID` (company being audited)
- `ChangedBy` → `dbo.User.UserID` (who made the change)

**Key Columns:**
- `CompanyID` - Company being audited
- `FieldName` (NVARCHAR(100)) - Which field changed (e.g., 'CompanyName', 'ABN')
- `OldValue` (NVARCHAR(MAX)) - Previous value
- `NewValue` (NVARCHAR(MAX)) - New value
- `ChangeType` (NVARCHAR(50)) - Type of change ('update', 'subscription_change')
- `ChangeReason` (NVARCHAR(500)) - Optional reason
- `ChangedBy`, `ChangedByEmail`, `IPAddress`, `UserAgent`
- `CreatedDate`

**Indexes:**
- `IX_AuditCompany_CompanyID` (find all changes for company)
- `IX_AuditCompany_CreatedDate` (time-based queries)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: audit.Company)

---

## 4. `audit.Role` - Role Assignment Changes

**Purpose:** Track all role assignment changes (security-critical audit)

**When Records Are Created:**
- User assigned system role (company_user → system_admin)
- User assigned company role (company_user → company_admin)
- User removed from company (role revoked)
- User's company role changed

**Primary Key:** `AuditRoleID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID` (user whose role changed)
- `UserCompanyID` → `dbo.UserCompany.UserCompanyID` (NULL for system roles)
- `CompanyID` → `dbo.Company.CompanyID` (NULL for system roles)
- `ChangedBy` → `dbo.User.UserID` (who made the change)

**Key Columns:**
- `TableName` (NVARCHAR(50)) - Which table changed ('User' for system roles, 'UserCompany' for company roles)
- `RecordID` (BIGINT) - Primary key of changed record
- `ColumnName` (NVARCHAR(50)) - Which column changed ('UserRoleID' or 'UserCompanyRoleID')
- `RoleType` (NVARCHAR(50)) - 'system' or 'company'
- `OldRoleID` (BIGINT) - Previous role ID
- `NewRoleID` (BIGINT) - New role ID
- `OldRoleName` (NVARCHAR(100)) - Previous role name (denormalized)
- `NewRoleName` (NVARCHAR(100)) - New role name (denormalized)
- `ChangeReason` (NVARCHAR(500)) - Why role changed
- `ChangedBy`, `ChangedByEmail`, `IPAddress`, `UserAgent`
- `CreatedDate`

**Indexes:**
- `IX_AuditRole_UserID` (find all role changes for user)
- `IX_AuditRole_CompanyID` (find all role changes in company)
- `IX_AuditRole_CreatedDate` (time-based queries)

**Query Patterns:**
```sql
-- User's role change history (security audit)
SELECT * 
FROM audit.Role 
WHERE UserID = @user_id 
ORDER BY CreatedDate DESC;

-- Who was promoted to system admin? (security review)
SELECT * 
FROM audit.Role 
WHERE RoleType = 'system' 
  AND NewRoleName = 'System Administrator'
ORDER BY CreatedDate DESC;

-- Company admin changes (company audit)
SELECT * 
FROM audit.Role 
WHERE CompanyID = @company_id 
  AND RoleType = 'company'
ORDER BY CreatedDate DESC;
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: audit.Role)

---

## Implementation Patterns

### **Automatic Audit Logging (Trigger Pattern)**

**Option A: Database Triggers** (for critical fields only)
```sql
CREATE TRIGGER trg_User_StatusChange
ON dbo.User
AFTER UPDATE
AS
BEGIN
    IF UPDATE(StatusID)
    BEGIN
        INSERT INTO audit.User (UserID, FieldName, OldValue, NewValue, ChangedBy, CreatedDate)
        SELECT 
            d.UserID,
            'StatusID',
            d.StatusID,  -- OLD value
            i.StatusID,  -- NEW value
            i.UpdatedBy,
            GETUTCDATE()
        FROM deleted d
        INNER JOIN inserted i ON d.UserID = i.UserID
        WHERE d.StatusID != i.StatusID;
    END
END;
```

**Option B: Service Layer Logging** (more flexible, recommended)
```python
# Service layer
async def update_user_status(user_id: int, new_status_id: int, changed_by: int, reason: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    old_status_id = user.status_id
    
    # Update user
    user.status_id = new_status_id
    user.updated_by = changed_by
    user.updated_date = datetime.utcnow()
    db.commit()
    
    # Log to audit table
    audit_record = AuditUser(
        user_id=user_id,
        field_name='StatusID',
        old_value=str(old_status_id),
        new_value=str(new_status_id),
        change_type='status_change',
        change_reason=reason,
        changed_by=changed_by,
        created_date=datetime.utcnow()
    )
    db.add(audit_record)
    db.commit()
```

---

### **Middleware for Activity Logging**

```python
# FastAPI middleware
@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    # Get current user from JWT
    current_user = await get_current_user(request)
    
    # Execute request
    response = await call_next(request)
    
    # Log business actions (not GET requests, only state-changing actions)
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and current_user:
        action = f"{request.url.path}.{request.method.lower()}"
        
        await log_activity(
            user_id=current_user.user_id,
            company_id=current_user.company_id,
            action=action,
            ip_address=hash_ip(request.client.host),
            user_agent=request.headers.get('User-Agent'),
            request_id=request.state.request_id
        )
    
    return response
```

---

## Compliance & Retention

### **GDPR Compliance**

**Right to Access:**
```sql
-- Customer requests their audit history
SELECT * FROM audit.ActivityLog WHERE UserID = @user_id;
SELECT * FROM audit.User WHERE UserID = @user_id;
SELECT * FROM audit.Role WHERE UserID = @user_id;
```

**Right to Erasure (Limited):**
- Audit records may be HASHED (not deleted) for privacy
- Legal requirement to retain audit trail (7 years)
- **Compromise:** Hash PII fields (email, name) but keep audit structure

```sql
-- Anonymize audit records (GDPR erasure request)
UPDATE audit.User 
SET ChangedByEmail = 'REDACTED',
    OldValue = CASE WHEN FieldName IN ('Email', 'FirstName', 'LastName') THEN 'REDACTED' ELSE OldValue END,
    NewValue = CASE WHEN FieldName IN ('Email', 'FirstName', 'LastName') THEN 'REDACTED' ELSE NewValue END
WHERE UserID = @user_id;
```

### **Australian Privacy Principles**

- Principle 11: Security of personal information (audit trail proves security measures)
- Principle 12: Access to personal information (customers can request audit history)
- Principle 13: Correction of personal information (audit trail shows correction history)

### **Retention Policy**

```sql
-- Archive audit records older than 7 years
-- (Move to cold storage, DO NOT DELETE)
INSERT INTO audit_archive.ActivityLog 
SELECT * FROM audit.ActivityLog 
WHERE CreatedDate < DATEADD(YEAR, -7, GETUTCDATE());

DELETE FROM audit.ActivityLog 
WHERE CreatedDate < DATEADD(YEAR, -7, GETUTCDATE());
```

---

## Query Performance

**Read Performance:**
- Write volume: MEDIUM (every user action logged)
- Read volume: LOW (security investigations, support tickets)
- Table growth: ~1M records/year (estimate: 100 active users × 100 actions/day)

**Optimization Strategy:**
- Partition tables by year (improves query performance for recent data)
- Index on UserID, CompanyID, CreatedDate (most common filters)
- Archive old records to cold storage (S3, Azure Blob)

**Query Patterns:**
```sql
-- Recent activity (fast - uses index)
SELECT TOP 100 * 
FROM audit.ActivityLog 
WHERE UserID = @user_id 
  AND CreatedDate >= DATEADD(DAY, -30, GETUTCDATE())
ORDER BY CreatedDate DESC;

-- Full history (slower - may need archival search)
SELECT * 
FROM audit.ActivityLog 
WHERE UserID = @user_id 
ORDER BY CreatedDate DESC;
```

---

## Related Documentation

**Architecture:**
- `docs/solution-architecture.md` - Security Architecture section
- `docs/architecture/decisions/ADR-001-database-schema-organization.md`

**Database:**
- `docs/database/REBUILD-PLAN-SUMMARY.md`
- `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` - Full SQL definitions

**Compliance:**
- GDPR: https://gdpr.eu/
- Australian Privacy Principles: https://www.oaic.gov.au/privacy/australian-privacy-principles

---

**Winston** 🏗️  
*"Audit trails are evidence. Treat them like court documents."*

