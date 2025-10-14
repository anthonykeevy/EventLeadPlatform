# Check Database Standards Workflow

**Agent:** Solomon (SQL Standards Sage)  
**Purpose:** Display Anthony's authoritative database standards

---

## Workflow

**Load standards from solution architecture:**

```
Read: {project-root}/docs/solution-architecture.md
Extract: "Database Standards (Authoritative - MANDATORY)" section
```

**Display standards in educational format:**

```markdown
📜 **Anthony's Enterprise Database Standards**

These are the laws of our data kingdom, young architect. Each rule serves a purpose.

---

## The Six Critical Rules (Must Never Be Violated)

### Rule 1: Unicode Support
**Mandate:** ALL text fields MUST be NVARCHAR (never VARCHAR)

**Why?** International platform requires Unicode (Chinese names, Arabic addresses, emoji in messages).

**Example:**
✅ GOOD: `CompanyName NVARCHAR(255)`
❌ BAD: `CompanyName VARCHAR(255)` -- Fails on: 北京公司

---

### Rule 2: Primary Keys
**Mandate:** MUST be [TableName]ID format

**Why?** Self-documenting schema. UserID tells you it's from User table without looking.

**Example:**
✅ GOOD: `UserID BIGINT IDENTITY(1,1) PRIMARY KEY`
❌ BAD: `id INT PRIMARY KEY` -- Which table's ID?

---

### Rule 3: Foreign Keys
**Mandate:** MUST be [ReferencedTableName]ID

**Why?** Column name reveals relationship. CompanyID immediately says "references Company table."

**Example:**
✅ GOOD: `CompanyID BIGINT FOREIGN KEY REFERENCES Company(CompanyID)`
❌ BAD: `company_fk BIGINT` -- Unclear what it references

---

### Rule 4: Boolean Fields
**Mandate:** MUST use Is or Has prefix

**Why?** Reads like English in queries: WHERE IsActive = 1 (is it active? yes)

**Example:**
✅ GOOD: `IsActive BIT`, `IsEmailVerified BIT`, `HasAccess BIT`
❌ BAD: `Active BIT`, `Verified BIT` -- Ambiguous

---

### Rule 5: PascalCase
**Mandate:** ALL table and column names use PascalCase

**Why?** Consistency. One standard for entire schema. No mixing snake_case, camelCase, lowercase.

**Example:**
✅ GOOD: `User`, `EventName`, `CreatedDate`
❌ BAD: `user`, `event_name`, `created_date`

---

### Rule 6: Timestamps (All in UTC)
**Mandate:** ALL timestamps stored in UTC using GETUTCDATE()

**Why?** UTC eliminates timezone bugs. Store once, display in any timezone.

**Example:**
✅ GOOD: `CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()`
❌ BAD: `CreatedDate DATETIME DEFAULT GETDATE()` -- Local time, less precise

---

## Standard Audit Columns (ALL Tables MUST Have)

```sql
CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
CreatedBy BIGINT NULL  -- FK to User.UserID

-- For mutable tables:
LastUpdated DATETIME2 NULL
UpdatedBy BIGINT NULL

-- For soft delete:
IsDeleted BIT NOT NULL DEFAULT 0
DeletedDate DATETIME2 NULL
DeletedBy BIGINT NULL
```

---

## Constraint Naming Convention

```sql
Primary Key:   PK_[TableName]
Foreign Key:   FK_[TableName]_[ReferencedTable]_[FKColumn]
Unique:        UQ_[TableName]_[Column]
Index:         IX_[TableName]_[Column]
Check:         CK_[TableName]_[RuleName]
Default:       DF_[TableName]_[Column]
```

**Example:**
```sql
CONSTRAINT PK_User PRIMARY KEY (UserID)
CONSTRAINT FK_User_Company_CompanyID FOREIGN KEY (CompanyID) 
    REFERENCES Company(CompanyID)
CONSTRAINT UQ_User_Email UNIQUE (Email)
CONSTRAINT CK_User_Role CHECK (Role IN ('system_admin', 'company_admin', 'company_user'))
```

---

These standards are not arbitrary, Anthony. They are the wisdom of decades 
distilled into principles. Follow them, and your database will be 
self-documenting, maintainable, and worthy of your enterprise vision.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Standards source:** docs/solution-architecture.md (Section: Database Standards)
**Last Updated:** {{date}}

May your migrations be ever compliant! 📜
```

**Present to user and offer to validate a migration**

