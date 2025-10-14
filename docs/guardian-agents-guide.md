# Guardian Agents Guide
**EventLeadPlatform - Custom BMAD Agents**

Created: October 2025  
For: Anthony Keevy  
Purpose: Prevent v4 pain points with specialized guardian agents

---

## 🛡️ **Your Guardian Agent Team**

Three specialized agents protect your development process:

### 1. Solomon 📜 - SQL Standards Sage
**Purpose:** Validate database migrations against enterprise standards  
**Pain Point Solved:** "Agents didn't respect database naming conventions (v4 issue)"

### 2. Sentinel 🛡️ - Epic Boundary Guardian
**Purpose:** Prevent cross-epic code modifications  
**Pain Point Solved:** "Epic 2 agents modified completed Epic 1 code (v4 issue)"

### 3. Dimitri 🔍 - Data Domain Architect
**Purpose:** Industry research, schema design, seed data generation  
**Value Added:** Ensure data models match/exceed industry standards

---

## 🚀 **How to Activate Agents in Cursor**

### Method 1: Reference in Chat (Recommended)

```
@bmad/agents/data-domain-architect
Hi Dimitri, analyze the Event domain...
```

```
@bmad/agents/database-migration-validator
Solomon, validate my migration...
```

```
@bmad/agents/epic-boundary-guardian
Sentinel, validate my changes...
```

### Method 2: Direct File Reference

Type `@` in Cursor chat, then select:
- `bmad/agents/data-domain-architect.md`
- `bmad/agents/database-migration-validator.md`
- `bmad/agents/epic-boundary-guardian.md`

---

## 📋 **Agent Quick Reference**

### Solomon 📜 - Database Migration Validator

**When to Use:** Before committing any database migration

**Commands:**
- `*validate-migration` - Check single migration file
- `*validate-all-migrations` - Check all migrations
- `*generate-template` - Create compliant migration template
- `*check-standards` - Display all database standards
- `*teach` - Learn about a specific standard

**Example Usage:**
```
@bmad/agents/database-migration-validator
*validate-migration

Solomon: "Which migration file?"
You: "database/migrations/versions/001_create_user_table.py"

Solomon: 
✓ User table uses PascalCase
✓ UserID follows [TableName]ID pattern
✓ Email is NVARCHAR (Unicode support)
✓ IsActive uses Is prefix
✓ CreatedDate uses DATETIME2 + GETUTCDATE()
✓ All audit columns present

"Perfect migration, Anthony! All standards followed beautifully."
```

**Standards Enforced:**
1. NVARCHAR for ALL text (Unicode)
2. [TableName]ID for primary keys
3. [ReferencedTable]ID for foreign keys
4. Is/Has prefix for booleans
5. PascalCase naming
6. UTC DATETIME2 timestamps
7. Audit columns (CreatedDate, CreatedBy, etc.)
8. Named constraints (PK_, FK_, UQ_, IX_)

---

### Sentinel 🛡️ - Epic Boundary Guardian

**When to Use:** Before committing code, especially when working on Epic 2+

**Commands:**
- `*validate-changes` - Check current changes for violations
- `*check-file` - Verify if specific file can be modified
- `*mark-epic-complete` - Mark epic complete (creates protected zone)
- `*show-boundaries` - Display current forbidden zones
- `*generate-story-context` - Create story context with boundaries

**Example Usage:**
```
@bmad/agents/epic-boundary-guardian
*validate-changes

Sentinel: "Scanning your changes..."

✓ backend/modules/companies/routes.py (OK - Epic 2 territory)
✓ Imports from backend.modules.auth (OK - read-only use)
❌ VIOLATION: Modified backend/modules/auth/routes.py (Epic 1 - COMPLETED)

"Anthony, Epic 1 is complete and protected. You can:
1. Import/use Epic 1 functions (allowed)
2. Create new routes in Epic 2 territory (recommended)
3. Mark Epic 1 incomplete if you truly need changes

This protects your tested code from regressions."
```

**Boundary Rules:**
- ✅ Completed epic code is READ-ONLY
- ✅ Can import/use completed code
- ❌ Cannot modify completed epic files
- ❌ Cannot edit old migrations
- ⚠️ Shared modules need extra review

**Epic Territories:**
- Epic 1: `backend/modules/auth/`, `frontend/features/auth/`
- Epic 2: `backend/modules/companies/`, `frontend/features/dashboard/`
- Epic 3: `backend/modules/events/`, `frontend/features/events/`
- Epic 4: `backend/modules/team/`, `frontend/features/team/`
- Epic 5: `backend/modules/forms/`, `frontend/features/forms/`
- Epic 6: `backend/modules/forms/services/publish_*.py`
- Epic 7: `backend/modules/payments/`, `frontend/features/payments/`
- Epic 8: `backend/modules/analytics/`, `frontend/features/analytics/`
- Epic 9: `backend/modules/audit/`

---

### Dimitri 🔍 - Data Domain Architect

**When to Use:** Before starting epic development, when designing data models

**Commands:**
- `*analyze-domain` - Complete domain analysis (PRIMARY COMMAND)
- `*research-industry` - Deep competitive research
- `*discover-sources` - Find public data sources (APIs, costs)
- `*generate-seed-data` - Create test/production seed data
- `*propose-schema` - Design normalized schema
- `*validate-model` - Review schema vs industry
- `*recommend-metrics` - Dashboard KPI suggestions
- `*suggest-enhancements` - Product improvement ideas
- `*compare-competitors` - Side-by-side competitive analysis
- `*generate-dictionary` - Create data dictionary
- `*track-trends` - Industry data trends
- `*export-findings` - Generate reports

**Example Usage (Your Event Job):**
```
@bmad/agents/data-domain-architect
*analyze-domain

Dimitri: "Which domain would you like me to analyze?"
You: "Event - for companies with booths collecting leads"

Dimitri: "Tell me the business context..."
You: "We need to handle formal events (conferences, trade shows) 
      AND informal scenarios (hair salon wanting a feedback form)"

Dimitri: [Executes 90-minute analysis]

Phase 1: Industry Research
✓ Researched Eventbrite, Ticket Tailor, Bizzabo
✓ Analyzed 100+ real events (formal and informal)
✓ Documented industry-standard fields

Phase 2: Data Source Intelligence
✓ Discovered Eventbrite API (free tier 1000 calls/day)
✓ Found ICC Sydney event calendar (web scraping)
✓ Identified Tourism NSW database (public, curated)
✓ Cost analysis: $99/mo for unlimited API vs free scraping
✓ Recommendation: "Hybrid - curated database + user additions"

Phase 3: Schema Design
✓ Proposed normalized Event table
✓ Handles formal events (venue, dates, organizer)
✓ Handles informal scenarios (Event relationship is OPTIONAL)
✓ Industry-standard fields: Name, StartDate, EndDate, Venue, etc.
✓ Validated against Solomon's standards ✓

Phase 4: Seed Data
✓ Test data: 50 examples (includes hair salon edge case)
   File: database/seeds/test/event_test_data.sql
   Label: "TEST DATA - DO NOT USE IN PRODUCTION"
   
✓ Production data: 50 verified Australian events
   File: database/seeds/production/event_production_seed.sql
   Sources: Eventbrite API (30), ICC Sydney (15), Tourism NSW (5)
   Attribution: Included per terms of service

Phase 5: Strategic Recommendations
✓ Strategy: "Hybrid curated + user-created (like Bizzabo)"
✓ Dashboard metrics → UX Expert: "% forms at curated vs user-created"
✓ Product enhancement → PM: "Event API integration for auto-population"

Deliverables Created:
- docs/data-domains/event-domain-analysis.md (comprehensive report)
- database/schemas/event-schema-proposal.sql (normalized design)
- database/seeds/test/event_test_data.sql (50 test examples)
- database/seeds/production/event_production_seed.sql (50 verified)
- docs/data-domains/event-data-dictionary.md (field documentation)
```

**Dimitri's Unique Value:**
- ✅ Industry intelligence (what competitors do)
- ✅ Data source discovery (APIs, costs, legal terms)
- ✅ Strategic recommendations (curated vs user-generated)
- ✅ Strict data governance (test vs production separation)
- ✅ Cross-agent collaboration (shares insights with team)

---

## 🔄 **Typical Development Workflow with Guardians**

### Before Starting an Epic

```
Step 1: Domain Analysis
@dimitri
*analyze-domain
Domain: [Your domain]
→ Dimitri researches industry, proposes schema, generates seed data

Step 2: Schema Validation
@solomon
*validate-migration
File: [Your migration]
→ Solomon validates against database standards

Step 3: Implement Epic
[Develop epic stories with dev agent...]

Step 4: Mark Complete
@sentinel
*mark-epic-complete
Epic: [Epic number]
→ Sentinel creates protected zone

Step 5: Next Epic
@sentinel
*validate-changes
→ Sentinel ensures no boundary violations
```

### Example: Starting Epic 3 (Events)

```bash
# Week 1: Domain Analysis
@dimitri *analyze-domain
# Dimitri researches event platforms, proposes schema

# Week 2: Schema Implementation
# Developer creates migration
@solomon *validate-migration
# Solomon validates compliance

# Week 3-4: Development
# [Implement Epic 3 stories...]

# Week 5: Epic Complete
@sentinel *mark-epic-complete
Epic: 3
# Sentinel protects Epic 3 from future changes

# Week 6: Start Epic 4
@sentinel *validate-changes
# Sentinel ensures Epic 4 doesn't modify Epic 3
```

---

## 📊 **Agent Collaboration Matrix**

| Agent | Sends To | Receives From | Purpose |
|-------|----------|---------------|---------|
| **Dimitri** | UX Expert | Developer | Dashboard metrics |
| **Dimitri** | Product Manager | Developer | Enhancement suggestions |
| **Dimitri** | Solomon | - | Schema validation |
| **Solomon** | Developer | Dimitri | Migration approval |
| **Sentinel** | Developer | - | Boundary validation |
| **Developer** | Solomon, Sentinel | Dimitri | Code implementation |

---

## 🎯 **Pain Points Solved**

### v4 Pain Point #1: "Agents didn't respect database naming conventions"
**Solution:** Solomon validates EVERY migration
- Catches violations before commit
- Explains WHY each rule exists
- Generates compliant templates

### v4 Pain Point #2: "Epic 2 agents modified Epic 1 completed code"
**Solution:** Sentinel enforces epic boundaries
- Detects cross-epic modifications
- Protects completed work
- Suggests alternatives (import vs modify)

### v6 Value Add: "Data models need industry completeness"
**Solution:** Dimitri researches industry
- Analyzes competitors (Eventbrite, etc.)
- Ensures schema matches market expectations
- Discovers public data sources
- Generates realistic seed data

---

## 📁 **Agent Files Location**

**Cursor-Ready (.md format):**
- `.cursor/rules/bmad/agents/data-domain-architect.md` ✅
- `.cursor/rules/bmad/agents/database-migration-validator.md` ✅
- `.cursor/rules/bmad/agents/epic-boundary-guardian.md` ✅

**Source Files (YAML + Workflows):**
- `bmad/agents/data-domain-architect/` (YAML, workflows, docs)
- `bmad/agents/database-migration-validator/` (YAML, workflows, docs)
- `bmad/agents/epic-boundary-guardian/` (YAML, workflows, docs)

**Index:**
- `.cursor/rules/bmad/index.mdc` (lists all agents)

---

## ✅ **Testing Your Agents**

### Test 1: Activate Dimitri
```
@bmad/agents/data-domain-architect

Expected: Dimitri greets you, shows menu with 12 commands
```

### Test 2: Activate Solomon
```
@bmad/agents/database-migration-validator

Expected: Solomon shows database standards quick reference
```

### Test 3: Activate Sentinel
```
@bmad/agents/epic-boundary-guardian

Expected: Sentinel shows current epic boundaries
```

---

## 📚 **Documentation**

**Comprehensive Guides:**
- `bmad/agents/data-domain-architect/README.md` - Dimitri's full documentation
- `bmad/agents/database-migration-validator/` - Solomon's workflows
- `bmad/agents/epic-boundary-guardian/` - Sentinel's workflows

**Quick Start:**
- This file! (`docs/guardian-agents-guide.md`)

---

## 🎓 **Next Steps**

**Now that agents are ready:**

1. ✅ **Test Dimitri** - Run your Event domain analysis job
2. ✅ **Start Epic 1** - Authentication & Onboarding
3. ✅ **Use Solomon** - Validate first migration
4. ✅ **Use Sentinel** - Protect Epic 1 when complete

---

**Your guardian agents are ready to protect your development process and ensure data excellence!** 🦸

**Created by:** BMad Builder  
**Date:** October 2025  
**Status:** Production Ready ✅

