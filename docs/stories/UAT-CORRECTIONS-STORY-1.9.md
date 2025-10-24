# UAT Documentation Corrections - Story 1.9

**Date:** 2025-01-19  
**Issue:** Critical discrepancies found between UAT documentation and actual environment

---

## 🚨 Issues Found

### 1. Frontend Port (CRITICAL)
- **Documentation Said:** `http://localhost:5173`
- **Actual:** `http://localhost:3000`
- **Source:** `vite.config.ts` line 14 explicitly sets `port: 3000`
- **Impact:** UAT would fail immediately - testers can't access the application

### 2. Database Name (CRITICAL)
- **Documentation Said:** `EventLeadDB`
- **Actual:** `EventLeadPlatform`
- **Source:** `backend/common/database.py`, `backend/alembic.ini`, `backend/env.example`
- **Impact:** All SQL queries would fail with "database does not exist" error

### 3. UserRefreshToken Table (HIGH)
- **Documentation Said:** `dbo.UserRefreshToken` table exists
- **Actual:** Unknown - need to verify table creation status
- **Model Exists:** YES - `backend/models/user_refresh_token.py` defines the model
- **Impact:** Database verification queries would fail if table not created

---

## ✅ Confirmed Correct Information

From code inspection:

1. **Frontend Port:** `3000` (confirmed in `vite.config.ts`)
2. **Backend Port:** `8000` (confirmed in `authApi.ts`)
3. **Database Name:** `EventLeadPlatform` (confirmed in multiple files)
4. **MailHog Port:** `8025` (standard MailHog port)
5. **Table Schema:** `dbo` (confirmed in models)
6. **Model Name:** `UserRefreshToken` (snake_case in Python, PascalCase table name)

---

## 🔍 Investigation Needed

### UserRefreshToken Table Status

**The model exists**, but we need to check if:
1. **Migration created?** Check `backend/migrations/versions/` for migration file
2. **Migration run?** Check if table exists in database via SSMS

**To verify in SSMS:**
```sql
USE EventLeadPlatform;
GO

-- Check if table exists
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'UserRefreshToken';

-- If exists, check structure
EXEC sp_columns 'UserRefreshToken', 'dbo';
```

**If table doesn't exist**, you need to:
```powershell
# Create migration (if not exists)
cd backend
alembic revision --autogenerate -m "add_user_refresh_token_table"

# Run migration
alembic upgrade head
```

---

## 📝 Required Documentation Updates

All documents need these global replacements:

### Replace ALL Instances:

| Find | Replace |
|------|---------|
| `http://localhost:5173` | `http://localhost:3000` |
| `localhost:5173` | `localhost:3000` |
| `EventLeadDB` | `EventLeadPlatform` |
| `USE EventLeadDB` | `USE EventLeadPlatform` |

### Documents to Update:

1. ✅ `UAT-QUICK-START-STORY-1.9.md`
2. ✅ `UAT-TEST-ACCOUNTS-STORY-1.9.md`
3. ✅ `UAT-RESULTS-FORM-STORY-1.9.html`
4. ✅ `UAT-GUIDE-STORY-1.9.md`
5. ✅ `story-1.9.md` (if it mentions URLs)

---

## 🎯 Immediate Action Plan

### Phase 1: Verify Database State (5 minutes)

**Run this in SSMS:**
```sql
-- 1. Verify database exists
SELECT name FROM sys.databases WHERE name = 'EventLeadPlatform';
-- Expected: Should return 'EventLeadPlatform'

-- 2. Check User table exists
USE EventLeadPlatform;
GO
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'User';
-- Expected: Should return 'User'

-- 3. Check UserEmailVerificationToken table
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'UserEmailVerificationToken';
-- Expected: Should return 'UserEmailVerificationToken'

-- 4. Check UserRefreshToken table
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'UserRefreshToken';
-- Expected: Should return 'UserRefreshToken' (if migration run)
-- If empty result, table doesn't exist - need to run migration

-- 5. Check log tables
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'log' 
ORDER BY TABLE_NAME;
-- Expected: ApiRequest, ApplicationError, etc.

-- 6. List ALL dbo tables
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'dbo' 
ORDER BY TABLE_NAME;
-- This will show you all tables that exist
```

### Phase 2: Fix Missing Tables (if needed)

**If UserRefreshToken table doesn't exist:**

```powershell
# Option A: Run existing migration
cd backend
alembic upgrade head

# Option B: If no migration exists, create one
alembic revision --autogenerate -m "add_refresh_token_table"
alembic upgrade head

# Verify
alembic current
```

### Phase 3: Update All Documentation (10 minutes)

I will update all 4 UAT documents with correct values.

---

## 💡 Why These Issues Happened

**Frontend Port (5173 vs 3000):**
- Vite default port is 5173
- Your project customized it to 3000 in `vite.config.ts`
- I assumed Vite default without checking config

**Database Name (EventLeadDB vs EventLeadPlatform):**
- Common convention: Add "DB" suffix to database names
- Your project uses the full project name
- I didn't verify actual connection strings

**UserRefreshToken Table:**
- Model exists in code, but may not have been migrated to database
- This is common in development - model created but migration not run yet
- Backend might work without it if refresh token feature not implemented yet

---

## ⚠️ Consequences if Not Fixed

### Frontend Port Issue:
```
Tester opens http://localhost:5173
→ Error: "This site can't be reached"
→ UAT stops immediately, 0% completion
```

### Database Name Issue:
```
Tester runs: USE EventLeadDB;
→ Error: "Database 'EventLeadDB' does not exist"
→ All database verification fails
→ Can't validate data is saved correctly
```

### UserRefreshToken Table Issue:
```
Tester runs: SELECT * FROM dbo.UserRefreshToken...
→ Error: "Invalid object name 'dbo.UserRefreshToken'"
→ Login verification queries fail
→ Can't verify refresh tokens are created
```

**Result:** UAT would appear to fail even if frontend works perfectly.

---

## ✅ Corrected Environment Configuration

### Frontend
```
URL: http://localhost:3000
Server: Vite (dev server)
Port: 3000 (custom, not default 5173)
API Proxy: /api → http://localhost:8000
```

### Backend
```
URL: http://localhost:8000
Server: FastAPI (Uvicorn)
Port: 8000
Database: EventLeadPlatform
Driver: ODBC Driver 18 for SQL Server
```

### MailHog
```
SMTP: localhost:1025
Web UI: http://localhost:8025
```

### Database
```
Server: localhost (or .\SQLEXPRESS)
Database: EventLeadPlatform
Auth: Windows Authentication (Trusted_Connection=Yes)
Schema: dbo (main tables), log (logging tables)
```

---

## 🔄 Next Steps

1. **YOU:** Run Phase 1 queries in SSMS to verify database state
2. **YOU:** Share results (which tables exist, which don't)
3. **ME:** Update all 4 UAT documents with correct values
4. **YOU:** Run any missing migrations if needed
5. **ME:** Create corrected versions of all documents
6. **YOU:** Proceed with UAT using corrected documents

---

## 📊 Verification Checklist

Before starting UAT, verify:

- [ ] Frontend runs on port 3000: `npm run dev` → check output
- [ ] Backend runs on port 8000: `python main.py` → check output  
- [ ] MailHog accessible: open http://localhost:8025
- [ ] Database name is EventLeadPlatform: run query above
- [ ] User table exists: run query above
- [ ] UserEmailVerificationToken table exists: run query above
- [ ] UserRefreshToken table exists: run query above
- [ ] log.ApiRequest table exists: run query above
- [ ] log.ApplicationError table exists: run query above

---

**Status:** Waiting for database verification results before updating documentation.

**ETA to Fix:** 10 minutes after database status confirmed.



