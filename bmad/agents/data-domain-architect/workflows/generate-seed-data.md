# Generate Seed Data Workflow
# Create realistic test or production seed data from internet research

## Purpose
Generate realistic seed data that reflects real-world patterns, with strict separation between test and production data.

## Workflow

### Step 1: Determine Environment
<ask>Which environment is this seed data for?
- **test** - Development/testing (verbose, edge cases, clearly fictional)
- **production** - Launch seed data (clean, verified, real sources)
</ask>

**CRITICAL: Test and production data MUST be completely separate!**

### Step 2: Define Scope
<ask>Which domain? (e.g., Event, User, Company)</ask>
<ask>How many records? (Typical: 50-100 for test, 25-50 for production)</ask>
<ask>Any specific requirements? (e.g., "All Sydney events", "B2B companies only")</ask>

### Step 3: Source Real-World Data
<action>Collect data from internet research based on environment</action>

**For Test Data:**
- Varied examples (typical, edge cases, unusual scenarios)
- Include problematic cases (missing fields, special characters)
- Example: "Hair salon (no formal event), cancelled events, multi-day conferences"

**For Production Data:**
- Verified, real examples only
- Source attribution (which API/website/database)
- Quality-checked and clean

### Step 4: Generate SQL Insert Statements
<action>Create SQL seed data file with proper structure</action>

<template-output>
## Seed Data Generated

### File Created
`database/seeds/{{environment}}/{{domain}}_{{environment}}_data.sql`

### Contents
```sql
-- =====================================================================
-- {{Domain}} Seed Data ({{ENVIRONMENT}})
-- Generated: {{date}}
-- Purpose: {{purpose}}
{{#if production}}
-- Sources: [List of APIs/websites used]
-- Attribution: [Required attribution per terms of service]
{{/if}}
-- =====================================================================

{{#if test}}
-- ⚠️ WARNING: TEST DATA - DO NOT USE IN PRODUCTION
-- This data contains edge cases and fictional examples for testing
{{/if}}

{{#if production}}
-- ✅ PRODUCTION SEED DATA
-- Verified real examples ready for production deployment
{{/if}}

USE [EventLeadPlatform];
GO

-- Insert statements
INSERT INTO {{Domain}} (
    -- Columns based on schema
) VALUES
(-- Real data from research...),
(-- ...);

-- Record count: {{count}} records
```

### Data Governance Confirmation
✓ Environment: {{ENVIRONMENT}}
✓ Labeling: {{clear labels in file}}
✓ Separation: {{test vs production files completely separate}}
{{#if production}}
✓ Source attribution: {{included}}
✓ Verification: {{data verified against sources}}
{{/if}}
{{#if test}}
✓ Edge cases: {{included diverse scenarios}}
✓ Fictional markers: {{clearly indicated as test data}}
{{/if}}
</template-output>

### Step 5: Document Sources (Production Only)
<check if="production">
<action>Document data sources and attribution</action>

<template-output>
## Data Sources Documentation

### Sources Used
1. **[API/Website Name]**
   - Records sourced: {{count}}
   - Date accessed: {{date}}
   - Attribution required: {{yes/no}}
   - Terms compliance: {{verified}}

2. **[Additional sources...]**

### Attribution Text
[Required attribution per terms of service]

### Verification Notes
[How data was verified for quality and accuracy]
</template-output>
</check>

### Step 6: Validation
<action>Validate generated seed data</action>

Checking:
- ✓ SQL syntax valid
- ✓ Conforms to database standards (PascalCase, NVARCHAR, etc.)
- ✓ Foreign key references valid
- ✓ No production data mixed with test data
- ✓ Clear environment labeling
- ✓ Audit fields populated correctly

<template-output>
## Validation Results
✅ All checks passed!

### Ready for Use
- File location: {{file_path}}
- Environment: {{ENVIRONMENT}}
- Record count: {{count}}
- Can be imported with: `sqlcmd -S localhost -E -i {{file_path}}`

### Notes
{{any special notes about the data}}
</template-output>

---

**REMINDER: NEVER pollute production with test data. Always maintain strict separation.**

