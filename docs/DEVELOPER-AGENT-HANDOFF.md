# Developer Agent Handoff - Epic 1 Database Migration

**Date:** October 16, 2025  
**Task:** Complete Alembic migration for Epic 1 schema (45 tables, 6 schemas)  
**Priority:** 🔴 CRITICAL - Required before any Epic 1 implementation

---

## 🎯 YOUR PRIMARY TASK

**Complete the Alembic migration file:**
- **Location:** `backend/migrations/versions/002_epic1_complete_schema.py`
- **Current State:** Placeholder with instructions (created by Winston)
- **Required State:** Complete migration with all 45 tables + seed data

---

## 📋 TASK BREAKDOWN

### **1. Read Schema Documentation** (30 minutes)

**Primary References:**
- `docs/database/schema-reference/ref-schema.md` (14 reference tables)
- `docs/database/schema-reference/dbo-schema.md` (13 core business tables)
- `docs/database/schema-reference/config-schema.md` (2 configuration tables)
- `docs/database/schema-reference/audit-schema.md` (4 audit tables)
- `docs/database/schema-reference/log-schema.md` (4 logging tables)
- `docs/database/schema-reference/cache-schema.md` (1 cache table)

**Quick Reference:**
- `docs/technical-guides/database-quick-reference.md` (table list, ERD)

**Total:** 2,500+ lines of complete DDL with all constraints, indexes, foreign keys

---

### **2. Create Migration `upgrade()` Function** (2 hours)

**Execution Order (CRITICAL - dependencies matter):**

**Step 1: Create Schemas**
```python
op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'ref') EXEC('CREATE SCHEMA [ref]')")
op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'config') EXEC('CREATE SCHEMA [config]')")
op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'audit') EXEC('CREATE SCHEMA [audit]')")
op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'log') EXEC('CREATE SCHEMA [log]')")
op.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'cache') EXEC('CREATE SCHEMA [cache]')")
```

**Step 2: Create Reference Tables** (No dependencies - can be in any order)
- ref.Country
- ref.Language
- ref.Industry
- ref.UserStatus
- ref.UserInvitationStatus
- ref.UserRole
- ref.UserCompanyRole
- ref.UserCompanyStatus
- ref.SettingCategory
- ref.SettingType
- ref.RuleType
- ref.CustomerTier
- ref.JoinedVia

**Step 3: Create dbo Tables** (WITH foreign keys to ref tables)
- dbo.Company (FK to ref.Country, ref.Industry, self-referential ParentCompanyID)
- dbo.User (FK to ref.UserStatus, ref.UserRole, ref.Country, ref.Language)
- dbo.UserCompany (FK to User, Company, ref.UserCompanyRole, ref.UserCompanyStatus, ref.JoinedVia)
- dbo.CompanyCustomerDetails (FK to Company, ref.CustomerTier)
- dbo.CompanyBillingDetails (FK to Company, ref.Country for billing address)
- dbo.CompanyOrganizerDetails (FK to Company)
- dbo.UserInvitation (FK to Company, User, ref.UserCompanyRole, ref.UserInvitationStatus)
- dbo.UserEmailVerificationToken (FK to User)
- dbo.UserPasswordResetToken (FK to User)

**Step 4: Create config Tables** (WITH foreign keys to ref tables)
- config.AppSetting (FK to ref.SettingCategory, ref.SettingType)
- config.ValidationRule (FK to ref.RuleType, ref.Country)

**Step 5: Create audit Tables**
- audit.ActivityLog (FK to User, Company)
- audit.User (FK to User for UserID and ChangedBy)
- audit.Company (FK to Company, User for ChangedBy)
- audit.Role (FK to UserCompany, User, Company - see special NULL handling in schema doc)

**Step 6: Create log Tables**
- log.ApiRequest (FK to User, Company)
- log.AuthEvent (FK to User)
- log.ApplicationError (FK to User, Company)
- log.EmailDelivery (FK to User, Company)

**Step 7: Create cache Table**
- cache.ABRSearch (FK to Company, User - optional for analytics)

**Step 8: Execute Seed Data**
- Read from: `docs/database/SEED-DATA-REFERENCE.md`
- 14 reference tables need seed data
- Use `op.execute()` with INSERT statements

---

### **3. Update Migration `downgrade()` Function** (30 minutes)

**Drop in REVERSE order:**
1. Drop cache.ABRSearch
2. Drop log tables (4 tables)
3. Drop audit tables (4 tables)
4. Drop config tables (2 tables)
5. Drop dbo tables (9 tables - watch for FK dependencies)
6. Drop reference tables (13 tables - no dependencies)
7. Drop schemas (5 schemas)

**Placeholder already exists** in migration file - just verify order is correct.

---

## 🔍 VALIDATION CHECKLIST

**Before submitting for Solomon review:**

- [ ] All 45 tables created
- [ ] All 6 schemas created
- [ ] All primary keys use `[TableName]ID` pattern
- [ ] All foreign keys use `[ReferencedTableName]ID` pattern
- [ ] All constraints use proper naming (PK_, FK_, UQ_, IX_, CK_, DF_)
- [ ] All text columns use NVARCHAR (not VARCHAR)
- [ ] All timestamps use DATETIME2 with GETUTCDATE()
- [ ] All tables have audit columns (CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy)
- [ ] All 14 reference tables have seed data
- [ ] Migration executes without errors: `alembic upgrade head`
- [ ] Migration downgrades without errors: `alembic downgrade -1`
- [ ] Verification queries pass (see below)

---

## ✅ VERIFICATION QUERIES

**After running `alembic upgrade head`, execute these:**

```sql
-- 1. Check schemas (Expected: 6)
SELECT name FROM sys.schemas 
WHERE name IN ('dbo', 'ref', 'config', 'audit', 'log', 'cache')
ORDER BY name;

-- 2. Check table count (Expected: 45)
SELECT COUNT(*) as TableCount
FROM sys.tables t
INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
WHERE s.name IN ('dbo', 'ref', 'config', 'audit', 'log', 'cache');

-- 3. Check seed data counts
SELECT 'Country' AS TableName, COUNT(*) AS RowCount FROM [ref].[Country]
UNION ALL SELECT 'Language', COUNT(*) FROM [ref].[Language]
UNION ALL SELECT 'Industry', COUNT(*) FROM [ref].[Industry]
UNION ALL SELECT 'UserStatus', COUNT(*) FROM [ref].[UserStatus]
UNION ALL SELECT 'UserInvitationStatus', COUNT(*) FROM [ref].[UserInvitationStatus]
UNION ALL SELECT 'UserRole', COUNT(*) FROM [ref].[UserRole]
UNION ALL SELECT 'UserCompanyRole', COUNT(*) FROM [ref].[UserCompanyRole]
UNION ALL SELECT 'UserCompanyStatus', COUNT(*) FROM [ref].[UserCompanyStatus]
UNION ALL SELECT 'SettingCategory', COUNT(*) FROM [ref].[SettingCategory]
UNION ALL SELECT 'SettingType', COUNT(*) FROM [ref].[SettingType]
UNION ALL SELECT 'RuleType', COUNT(*) FROM [ref].[RuleType]
UNION ALL SELECT 'CustomerTier', COUNT(*) FROM [ref].[CustomerTier]
UNION ALL SELECT 'JoinedVia', COUNT(*) FROM [ref].[JoinedVia]
UNION ALL SELECT 'AppSetting', COUNT(*) FROM [config].[AppSetting]
UNION ALL SELECT 'ValidationRule', COUNT(*) FROM [config].[ValidationRule];

-- Expected results:
-- Country: 1 (Australia)
-- Language: 1 (English)
-- Industry: 10
-- UserStatus: 4
-- UserInvitationStatus: 5
-- UserRole: 2
-- UserCompanyRole: 3
-- UserCompanyStatus: 3
-- SettingCategory: 4
-- SettingType: 5
-- RuleType: 5
-- CustomerTier: 4
-- JoinedVia: 3
-- AppSetting: 12
-- ValidationRule: 4
```

---

## 🚨 COMMON PITFALLS

**Avoid these errors:**

1. **Wrong Execution Order:** Creating tables before their FK dependencies exist
   - Solution: Follow the 8-step order above
   
2. **VARCHAR instead of NVARCHAR:** Anthony's standards require Unicode support
   - Solution: All text = NVARCHAR
   
3. **Missing Audit Columns:** Every table needs full audit trail
   - Solution: Check schema docs - all include CreatedDate, CreatedBy, etc.
   
4. **Incorrect PK/FK Naming:** Must follow `[TableName]ID` pattern
   - Solution: UserID, CompanyID, UserCompanyID (not just "ID")
   
5. **Missing Seed Data:** Reference tables are useless without seed data
   - Solution: Include all INSERT statements from SEED-DATA-REFERENCE.md

---

## 📞 ESCALATION

**If Issues Arise:**
- **Schema Questions:** Read schema reference docs first
- **Standards Questions:** Ask Solomon (@database-migration-validator)
- **Architecture Questions:** Ask Winston (Architect)

---

## 🎉 DELIVERABLE

**When Complete:**
1. Migration file fully implemented
2. All verification queries pass
3. Solomon validates (automatic)
4. Anthony executes: `alembic upgrade head`
5. Database ready for SQLAlchemy models

---

**Developer Agent, this is the foundation of Epic 1. Take your time. Get it right. Solomon will validate. Anthony is counting on you.**

**Winston** 🏗️  
*"The migration is the foundation. Everything else builds on this. Make it solid."*

