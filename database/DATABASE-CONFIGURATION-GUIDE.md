# Database Configuration Guide: Local vs Azure SQL Database

**Project:** EventLeadPlatform  
**Date:** October 2025  
**Purpose:** Comprehensive guide for database configuration decisions

---

## 📋 **Executive Summary**

**Recommendation: Use DIFFERENT configurations for Local Development vs Azure Production**

| Configuration | Local Development | Azure Production |
|---------------|-------------------|------------------|
| **Recovery Model** | SIMPLE (easy management) | Automatic (Azure managed) |
| **File Paths** | Default SQL Server paths | N/A (Azure manages storage) |
| **Collation** | Latin1_General_100_CI_AS_SC_UTF8 | Same (set at creation) |
| **READ_COMMITTED_SNAPSHOT** | ON (manually set) | ON (Azure default) |
| **Query Store** | ON (performance monitoring) | ON (critical for Azure) |
| **TDE** | OFF (not needed locally) | ON (compliance requirement) |
| **Auto-Tuning** | N/A (not supported) | ON (Azure AI optimization) |
| **Backups** | Manual (or none for dev) | Automatic (7-35 days retention) |

---

## 🌍 **1. International Support: COLLATION (CRITICAL)**

### **Your Requirements:**
- Platform must support **any country or language**
- Customers globally (Australia, UK, US, Asia, Europe, etc.)
- User input in multiple languages (names, addresses, event descriptions)
- Emojis and special characters (modern users expect this)

### **Recommended Collation:**

```sql
Latin1_General_100_CI_AS_SC_UTF8
```

**Breakdown:**
- `Latin1_General_100` = Modern Unicode sorting (SQL Server 2008+ algorithm)
- `CI` = **Case Insensitive** ("John" = "john") ← Better UX for searches
- `AS` = **Accent Sensitive** ("José" ≠ "Jose") ← Maintains data integrity
- `SC` = **Supplementary Characters** (emojis, Asian characters, mathematical symbols)
- `UTF8` = **Native UTF-8 storage** (more efficient than NVARCHAR)

### **Why UTF-8?**

| Without UTF-8 (NVARCHAR) | With UTF-8 (VARCHAR + UTF8 collation) |
|--------------------------|----------------------------------------|
| English "Hello" = 12 bytes | English "Hello" = 5 bytes |
| Chinese "你好" = 4 bytes | Chinese "你好" = 6 bytes |
| Mixed text wastes space | Mixed text optimal storage |

**Savings:** 40-50% storage reduction for English text (most of your data)  
**Trade-off:** Slight overhead for Asian languages (still acceptable)

### **Alternative (if SQL Server < 2019):**

```sql
Latin1_General_100_CI_AS_SC
```
Same benefits except UTF-8 storage. Still excellent international support.

### **What You Had (Issue):**

```sql
-- Your previous script didn't specify collation
-- Likely defaulted to: SQL_Latin1_General_CP1_CI_AS
-- Problems:
--   ❌ Old sorting algorithm (SQL Server 2000 era)
--   ❌ No supplementary character support (no emojis)
--   ❌ Poor Unicode support
--   ❌ No UTF-8 storage optimization
```

---

## ⚙️ **2. ANSI Settings: SQLAlchemy Compatibility**

### **Your Previous Script Had These OFF (MAJOR ISSUE):**

```sql
ALTER DATABASE SET ANSI_NULLS OFF          -- ❌ WRONG
ALTER DATABASE SET ANSI_WARNINGS OFF       -- ❌ WRONG
ALTER DATABASE SET QUOTED_IDENTIFIER OFF   -- ❌ WRONG (breaks SQLAlchemy)
```

### **Why This Breaks SQLAlchemy:**

```python
# SQLAlchemy generates queries like this:
SELECT "User"."Email" FROM "User" WHERE "User"."CompanyID" = 1

# QUOTED_IDENTIFIER = OFF breaks this!
# SQL Server won't recognize "User" as a table name

# Also breaks:
user = User.query.filter(User.email == None).first()
# ANSI_NULLS = OFF makes NULL comparisons non-standard
```

### **Correct Settings (ALL must be ON):**

```sql
ALTER DATABASE SET ANSI_NULLS ON
ALTER DATABASE SET ANSI_WARNINGS ON
ALTER DATABASE SET ANSI_PADDING ON
ALTER DATABASE SET QUOTED_IDENTIFIER ON
ALTER DATABASE SET ARITHABORT ON
ALTER DATABASE SET CONCAT_NULL_YIELDS_NULL ON
```

**Impact:** **CRITICAL** - Without these, SQLAlchemy will malfunction.

---

## 🚀 **3. Concurrency: READ_COMMITTED_SNAPSHOT**

### **What Is This?**

Traditional SQL Server (your script):
```
User A: SELECT * FROM Users WHERE Email = 'test@example.com'
  |
  |---BLOCKED---> (waits for User B's transaction to finish)
  |
User B: UPDATE Users SET Email = 'new@example.com' WHERE UserID = 123
```

With READ_COMMITTED_SNAPSHOT:
```
User A: SELECT * FROM Users WHERE Email = 'test@example.com'  ← Returns immediately
  |
  |---NO BLOCKING---> (reads snapshot, doesn't wait)
  |
User B: UPDATE Users SET Email = 'new@example.com' WHERE UserID = 123
```

### **Why This Matters for Web Apps:**

**Scenario: User viewing dashboard while admin updates company settings**

| Without RCS (Your Script) | With RCS (Recommended) |
|---------------------------|------------------------|
| Dashboard query **BLOCKS** until update finishes | Dashboard query returns **immediately** |
| User sees loading spinner (5-10 seconds) | User sees data instantly (<1 second) |
| Poor user experience | Excellent user experience |

**Recommendation:** **ALWAYS ON for web applications**

### **Local vs Azure:**

| Environment | Setting | How to Enable |
|-------------|---------|---------------|
| **Local SQL Server** | OFF by default | `ALTER DATABASE SET READ_COMMITTED_SNAPSHOT ON` |
| **Azure SQL Database** | **ON by default** | Already enabled (no action needed) |

---

## 💾 **4. Recovery Model: SIMPLE vs FULL**

### **Your Previous Script:**

```sql
ALTER DATABASE SET RECOVERY FULL
-- This requires transaction log backups every 15-30 minutes
-- If you don't back up the log, it grows INFINITELY
-- Development databases can fill your disk!
```

### **Recommended Approach:**

| Environment | Recovery Model | Reason |
|-------------|----------------|--------|
| **Local Development** | **SIMPLE** | No log management needed, automatic cleanup |
| **Azure Production** | **Automatic** | Azure manages backups, no choice needed |

### **SIMPLE Recovery Benefits (Development):**

```sql
-- With SIMPLE:
Transaction log automatically truncates after checkpoint (every 60 seconds)
  ↓
Log file stays small (~256MB)
  ↓
No manual backup management
  ↓
Focus on coding, not DBA tasks
```

### **Azure SQL Database (Production):**

Azure **automatically** handles backups:
- **Full backup:** Weekly (Sunday night)
- **Differential backup:** Every 12-24 hours
- **Transaction log backup:** Every 5-10 minutes
- **Point-in-time restore:** Any time in last 7-35 days
- **Long-term retention:** Up to 10 years (optional, extra cost)

**You don't configure recovery model in Azure - it's managed for you.**

---

## 📊 **5. Query Store: Performance Monitoring**

### **What Is Query Store?**

Built-in "flight recorder" for SQL Server that captures:
- Which queries are running
- How long they take
- What resources they use (CPU, memory, I/O)
- Query execution plans

### **Why Enable It?**

**Scenario: After deploying Epic 5, users report "Forms are slow to load"**

Without Query Store:
```
❌ You: "Which queries are slow?"
❌ Users: "I don't know, just slow"
❌ You: Guessing game, no data
❌ Result: Days to find the issue
```

With Query Store:
```
✅ Open Query Store in Azure Portal or SSMS
✅ See: "FormElement load query takes 8 seconds (was 200ms last week)"
✅ Root cause: Missing index on FormElementOrder column
✅ Fix: Add index, instant improvement
✅ Result: Issue fixed in 30 minutes
```

### **Recommendation:** **ALWAYS ON (both Local and Azure)**

**Storage Cost:** ~1GB (negligible)  
**Performance Impact:** <1% (unnoticeable)  
**Troubleshooting Value:** **INVALUABLE**

---

## 🗄️ **6. File Paths & Storage**

### **Your Previous Script (Local-Specific):**

```sql
FILENAME = N'C:\Data\SQL\Data\EventTrackerDB_Dev.mdf'
FILENAME = N'D:\Data\SQL\Log\EventTrackerDB_Dev_log.ldf'
```

**Problem:** These paths won't exist on other developers' machines.

### **Recommended Approach (Local Development):**

```sql
-- Use default SQL Server paths (portable)
FILENAME = N'EventLeadPlatform.mdf'
-- SQL Server uses its configured default directory
-- Usually: C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\
```

**Benefit:** Script works on ANY developer's machine, no path changes needed.

### **Azure SQL Database:**

```
N/A - Azure manages storage
You only specify service tier (Basic, S0, S3, GP_Gen5_2, etc.)
Storage is abstracted away
```

---

## 🔒 **7. Security & Compliance**

### **Transparent Data Encryption (TDE)**

**Local Development:**
```sql
ALTER DATABASE SET ENCRYPTION OFF
-- Reason: Not needed for local dev, adds performance overhead
```

**Azure Production:**
```sql
ALTER DATABASE SET ENCRYPTION ON
-- Reason: 
--   1. Compliance requirement (GDPR, privacy laws)
--   2. Protects data at rest
--   3. No extra cost in Azure
--   4. Minimal performance impact (<5%)
```

### **Advanced Threat Protection (Azure Only)**

Azure SQL Database includes AI-powered security monitoring:
- SQL injection detection
- Unusual access patterns
- Data exfiltration attempts
- Brute force attacks

**Configure via:** Azure Portal > SQL Database > Security > Advanced Threat Protection

**Cost:** Included in most service tiers (or ~$15/month for Basic tier)

---

## 🎯 **8. Azure-Specific Features**

### **Automatic Tuning (Azure AI)**

Azure SQL Database can **automatically optimize your database:**

```sql
ALTER DATABASE SET AUTOMATIC_TUNING (
    CREATE_INDEX = ON,          -- Auto-create missing indexes
    DROP_INDEX = ON,            -- Auto-drop unused indexes
    FORCE_LAST_GOOD_PLAN = ON   -- Fix query plan regressions
);
```

**Real Example:**
```
Week 5: You deploy Epic 8 (Lead Analytics)
  ↓
Customers run complex dashboard queries
  ↓
Azure detects: "Query on Submissions table is slow (full table scan)"
  ↓
Azure automatically: Creates index on SubmittedDate column
  ↓
Query goes from 5 seconds → 50ms
  ↓
You get email: "Azure created index IX_Submissions_SubmittedDate"
```

**This is AMAZING for solo developers** - AI DBA for free!

### **Accelerated Database Recovery (ADR)**

**Traditional SQL Server:**
```
Database crashes mid-transaction
  ↓
Recovery on restart: 30-60 minutes (replaying transaction log)
  ↓
Downtime: 30-60 minutes
```

**With ADR (Azure default):**
```
Database crashes mid-transaction
  ↓
Recovery on restart: 5-10 seconds (version-based recovery)
  ↓
Downtime: 5-10 seconds
```

**Enabled automatically in Azure, manually in SQL Server 2019+**

---

## 💰 **9. Azure Service Tier Recommendations**

### **Development/Testing:**

| Tier | vCores | Storage | Cost/Month (AUD) | Use Case |
|------|--------|---------|------------------|----------|
| **Basic** | Shared | 2GB | ~$7 | Initial setup, schema design |
| **S0** | Shared | 250GB | ~$20 | Active development, most dev work |

**Recommendation:** Start with **S0** ($20/month), scale up for load testing.

### **Production:**

| Tier | vCores | Storage | DTUs | Cost/Month (AUD) | Use Case |
|------|--------|---------|------|------------------|----------|
| **S3** | Shared | 250GB | 100 | ~$120 | MVP (100-200 users) |
| **GP_Gen5_2** | 2 vCores | 32GB | N/A | ~$450 | Better performance (200-500 users) |
| **GP_Gen5_4** | 4 vCores | 32GB | N/A | ~$900 | Scale (500-1000+ users) |

**Recommendation for Launch:** Start with **S3** ($120/month), monitor usage, scale as needed.

### **How to Choose:**

1. **Start conservatively** (S3)
2. **Monitor metrics** (DTU usage, query performance)
3. **Scale up if:**
   - DTU usage consistently >80%
   - Queries are slow despite Query Store optimizations
   - User complaints about performance
4. **Azure makes scaling easy** (no downtime, click a button)

---

## 📝 **10. Collation Change Impact**

### **CRITICAL: Collation cannot be changed after database creation**

If you create database with wrong collation:
```sql
-- THE ONLY FIX:
1. Export all data (backup)
2. DROP DATABASE
3. CREATE DATABASE with correct collation
4. Import data back
```

**This is PAINFUL in production** - get it right from day 1!

### **Our Approach:**

```sql
-- Local Development
CREATE DATABASE EventLeadPlatform 
    COLLATE Latin1_General_100_CI_AS_SC_UTF8;

-- Azure Production (set during creation via Azure Portal)
Collation: Latin1_General_100_CI_AS_SC_UTF8
```

**Test early:** Create database with production collation from day 1 (even in dev).

---

## ✅ **11. Recommended Configuration Matrix**

### **Local Development:**

| Setting | Value | Reason |
|---------|-------|--------|
| **Collation** | Latin1_General_100_CI_AS_SC_UTF8 | International support |
| **ANSI Settings** | ALL ON | SQLAlchemy compatibility |
| **READ_COMMITTED_SNAPSHOT** | ON | Web app concurrency |
| **Recovery Model** | SIMPLE | Easy management |
| **Query Store** | ON | Performance monitoring |
| **TDE** | OFF | Not needed, saves overhead |
| **File Paths** | Default | Portable across machines |

### **Azure Production:**

| Setting | Value | Reason |
|---------|-------|--------|
| **Collation** | Latin1_General_100_CI_AS_SC_UTF8 | International support |
| **ANSI Settings** | ALL ON (default) | Azure default, compatible |
| **READ_COMMITTED_SNAPSHOT** | ON (automatic) | Azure default |
| **Recovery Model** | Automatic | Azure manages backups |
| **Query Store** | ON | Critical for troubleshooting |
| **TDE** | ON | Compliance requirement |
| **Automatic Tuning** | ON | AI performance optimization |
| **Service Tier** | S3 (MVP) | Balance of cost and performance |
| **Geo-Replication** | ON (Production) | Disaster recovery |

---

## 🚦 **12. Implementation Steps**

### **Step 1: Create Local Database (NOW)**

```powershell
# Navigate to project
cd C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform

# Run local database creation script
sqlcmd -S localhost -E -i database/scripts/create-database-local.sql

# Verify
sqlcmd -S localhost -E -Q "USE EventLeadPlatform; SELECT @@VERSION, DATABASEPROPERTYEX('EventLeadPlatform', 'Collation');"
```

### **Step 2: Update Connection String**

Edit `.env.local`:
```bash
DATABASE_URL=mssql+pyodbc://localhost/EventLeadPlatform?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no
```

### **Step 3: Test Connection**

```powershell
# Start backend
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# Open browser
http://localhost:8000/api/test-database

# Should show: SQL Server 2022 version + connection success
```

### **Step 4: Azure Database (Week 20 - Before Production Deploy)**

```bash
# Create Azure SQL Server (one-time)
az sql server create \
  --name eventlead-sql-au \
  --resource-group eventlead-rg \
  --location australiaeast \
  --admin-user sqladmin \
  --admin-password "YourStrongPassword123!"

# Create database with correct collation
az sql db create \
  --name EventLeadPlatform \
  --server eventlead-sql-au \
  --service-objective S3 \
  --collation Latin1_General_100_CI_AS_SC_UTF8

# Configure firewall (allow Azure services)
az sql server firewall-rule create \
  --server eventlead-sql-au \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Run configuration script
sqlcmd -S eventlead-sql-au.database.windows.net -U sqladmin -P "YourStrongPassword123!" \
  -d EventLeadPlatform -i database/scripts/create-database-azure.sql
```

---

## 🎯 **13. Key Takeaways**

### **What to Change from Your Previous Script:**

| Your Script | Recommendation | Impact |
|-------------|----------------|--------|
| No collation specified | **Latin1_General_100_CI_AS_SC_UTF8** | **CRITICAL** - Enables international support |
| ANSI_NULLS OFF | **ANSI_NULLS ON** | **CRITICAL** - Breaks SQLAlchemy if OFF |
| QUOTED_IDENTIFIER OFF | **QUOTED_IDENTIFIER ON** | **CRITICAL** - Breaks SQLAlchemy if OFF |
| READ_COMMITTED_SNAPSHOT OFF | **READ_COMMITTED_SNAPSHOT ON** | **HIGH** - Poor concurrency if OFF |
| RECOVERY FULL (dev) | **RECOVERY SIMPLE** (dev) | **MEDIUM** - Easier management |
| Hardcoded file paths | **Use defaults** | **LOW** - Better portability |

### **What to Keep from Your Previous Script:**

- ✅ Query Store enabled (excellent)
- ✅ PAGE_VERIFY CHECKSUM (data integrity)
- ✅ AUTO_UPDATE_STATISTICS (performance)

---

## 📚 **14. References**

- **SQL Server Collations:** https://learn.microsoft.com/en-us/sql/relational-databases/collations/collation-and-unicode-support
- **Azure SQL Database:** https://learn.microsoft.com/en-us/azure/azure-sql/database/
- **Query Store:** https://learn.microsoft.com/en-us/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store
- **READ_COMMITTED_SNAPSHOT:** https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-set-options#read_committed_snapshot
- **SQLAlchemy SQL Server:** https://docs.sqlalchemy.org/en/20/dialects/mssql.html

---

**Document Created By:** Winston (Architect Agent)  
**For:** Anthony Keevy  
**Date:** October 2025  
**Status:** Ready for implementation

