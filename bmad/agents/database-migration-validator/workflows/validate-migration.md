# Validate Migration Workflow

**Agent:** Solomon (SQL Standards Sage)  
**Purpose:** Validate a single Alembic migration file against Anthony's database standards

---

## Workflow

**Ask user for migration file:**

```
"Greetings, seeker of data perfection! Which migration file shall we examine?"

Please provide:
1. Path to migration file (e.g., database/migrations/versions/001_create_user_table.py)
2. OR paste the migration SQL/Python code directly
```

**Load database standards:**
```
Read: {project-root}/docs/solution-architecture.md
Extract: Database Standards section (authoritative rules)
```

**Parse migration file:**
```
If Python file (.py):
  - Extract CREATE TABLE statements
  - Extract ALTER TABLE statements
  - Extract column definitions
  - Extract constraint definitions

If SQL file (.sql):
  - Parse SQL statements directly
```

**Run validation checks:**

### Check 1: Unicode Support (NVARCHAR vs VARCHAR)
```
Search for: VARCHAR (without N prefix)

If found:
  Violation: "Ah, I see VARCHAR where NVARCHAR should dwell..."
  Teaching: "Unicode support allows international characters. VARCHAR limits us to ASCII only."
  Severity: CRITICAL
  Fix: "Change all VARCHAR to NVARCHAR"
```

### Check 2: Primary Key Naming
```
Search for: PRIMARY KEY with column name

Pattern: Should be [TableName]ID

Example:
  ✅ GOOD: UserID BIGINT IDENTITY(1,1) PRIMARY KEY
  ❌ BAD: id INT PRIMARY KEY
  ❌ BAD: user_id INT PRIMARY KEY (snake_case)

If violation found:
  Teaching: "Primary keys reveal their table: UserID = from User table. Generic 'id' requires context."
```

### Check 3: Foreign Key Naming
```
Search for: FOREIGN KEY constraints

Pattern: FK column MUST be [ReferencedTableName]ID

Example:
  ✅ GOOD: CompanyID BIGINT FOREIGN KEY REFERENCES Company(CompanyID)
  ❌ BAD: company_fk BIGINT FOREIGN KEY...
  ❌ BAD: company_id (snake_case)

If violation:
  Teaching: "Foreign keys are self-documenting: CompanyID immediately tells us it references Company table."
```

### Check 4: Boolean Prefix
```
Search for: BIT columns without Is/Has prefix

Example:
  ✅ GOOD: IsActive BIT
  ✅ GOOD: HasAccess BIT
  ❌ BAD: Active BIT
  ❌ BAD: Deleted BIT (should be IsDeleted)

If violation:
  Teaching: "Boolean fields read like questions: 'IsActive?' Yes or no. 'Active?' is ambiguous - active what?"
```

### Check 5: PascalCase
```
Search for: snake_case or lowercase table/column names

Example:
  ✅ GOOD: User, EventName, CreatedDate
  ❌ BAD: user, event_name, created_date
  ❌ BAD: USER, EVENT_NAME (all caps)

If violation:
  Teaching: "PascalCase is your chosen standard. Consistency creates clarity. Every name tells its purpose."
```

### Check 6: UTC Timestamps
```
Search for: DATETIME (without 2) or GETDATE()

Example:
  ✅ GOOD: CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
  ❌ BAD: CreatedDate DATETIME DEFAULT GETDATE()

If violation:
  Teaching: "DATETIME2 is more precise. GETUTCDATE() stores in UTC (no timezone confusion). Convert to local on display."
```

### Check 7: Audit Columns
```
Check for required audit columns:
  - CreatedDate DATETIME2
  - CreatedBy BIGINT
  - (For mutable tables) LastUpdated DATETIME2, UpdatedBy BIGINT
  - (For soft delete) IsDeleted BIT, DeletedDate, DeletedBy

If missing:
  Teaching: "Audit columns answer 'who created this, when, and who modified it?' Essential for enterprise data management."
```

### Check 8: Constraint Naming
```
Check constraint names follow convention:
  - PK_[TableName]
  - FK_[TableName]_[ReferencedTable]_[FKColumn]
  - UQ_[TableName]_[Column]
  - IX_[TableName]_[Column]
  - CK_[TableName]_[RuleName]

Example:
  ✅ GOOD: CONSTRAINT FK_Form_Event_EventID
  ❌ BAD: CONSTRAINT fk_form_event

If violation:
  Teaching: "Named constraints tell their story. FK_Form_Event_EventID says 'Form table, references Event via EventID.'"
```

---

**Generate validation report:**

```markdown
# Migration Validation Report

**Migration File:** {{filename}}
**Validated:** {{timestamp}}
**Validator:** Solomon (SQL Standards Sage)

---

## Validation Results

**Overall Status:** {{PASS ✅ | VIOLATIONS FOUND ⚠️}}

**Standards Compliance Score:** {{percentage}}%

---

## Detailed Findings

### Critical Violations (Must Fix Before Migration)

{{if_critical_violations_found}}

1. **VARCHAR Usage Detected**
   - Location: Line 45, column `CompanyName VARCHAR(255)`
   - Violation: Rule #1 (Unicode Support)
   - Teaching: Unicode support allows international characters...
   - Fix: Change to `CompanyName NVARCHAR(255)`

{{end_critical}}

### High Priority Violations (Strongly Recommended)

{{if_high_violations}}

### Medium Priority Violations (Best Practice)

{{if_medium_violations}}

---

## What Went Well ✅

{{celebrate_correct_patterns}}

- ✅ All primary keys follow [TableName]ID pattern
- ✅ All boolean fields have Is/Has prefix
- ✅ UTC timestamps used correctly

---

## Summary

{{if_perfect}}
"Ah, a perfect migration! Your database craftsmanship brings joy to this old sage's heart. 
Every table named with care, every column typed with wisdom. This migration honors the data 
it will hold. Well done, Anthony!"

{{if_violations}}
"A worthy attempt, young architect, but a few standards need attention. Fix the {{count}} 
violations above, and this migration will be worthy of your enterprise database. Remember: 
standards are not obstacles - they are the foundation of maintainable systems."

{{if_minor_only}}
"Nearly perfect! Only minor refinements needed. The core structure is sound. Address the 
medium-priority items when time permits, but this migration is acceptable for development."

---

**Next Steps:**

{{if_violations}}
1. Fix violations listed above
2. Run *validate-migration again
3. Once PASS achieved, apply migration with confidence

{{if_pass}}
1. Apply migration: `alembic upgrade head`
2. Verify in database: Check table/column names match expectations
3. Commit to Git: Migration validated ✅
```

**Display report and wait for user acknowledgment**

