# Custom BMAD Agents for EventLeadPlatform

**Created:** 2025-10-12  
**Purpose:** Custom agents to prevent Anthony's v4 pain points  
**Total Agents:** 2

---

## Agent #1: Solomon - SQL Standards Sage 📜

**Purpose:** Validate Alembic database migrations against Anthony's enterprise naming standards

**Persona:** Patient database mentor with decades of SQL Server wisdom

**Prevents:** Database naming violations (v4 pain point: agents not respecting PascalCase)

**Commands:**

```
@bmad/agents/database-migration-validator

*validate-migration          - Validate a single migration file
*validate-all-migrations     - Validate all migrations in project
*generate-template           - Generate compliant migration template
*check-standards             - Display database standards reference
*teach                       - Explain specific database rule (educational)
```

**When to Use:**
- After creating any Alembic migration (before applying)
- Before committing migration to Git
- When unsure if migration follows standards
- To generate properly formatted migration templates

**Example Usage:**
```
@bmad/agents/database-migration-validator
Command: *validate-migration
File: database/migrations/versions/003_create_event_table.py

→ Solomon validates migration
→ Reports violations with teaching explanations
→ Celebrates compliant code
→ Provides fixes for any issues
```

**Location:** `bmad/agents/database-migration-validator/`

**Validation Rules:**
- ✅ NVARCHAR for all text (Unicode support)
- ✅ Primary keys: [TableName]ID format
- ✅ Foreign keys: [ReferencedTableName]ID format
- ✅ Boolean fields: Is/Has prefix
- ✅ PascalCase for all names
- ✅ UTC timestamps with DATETIME2
- ✅ Audit columns on all tables
- ✅ Constraint naming conventions

---

## Agent #2: Sentinel - Epic Boundary Guardian 🛡️

**Purpose:** Prevent cross-epic code modifications (protect completed epic code)

**Persona:** Firm guardian protecting completed work, educational about boundaries

**Prevents:** Epic boundary violations (v4 pain point: Epic 2 modifying Epic 1 code)

**Commands:**

```
@bmad/agents/epic-boundary-guardian

*validate-changes            - Check current changes don't cross boundaries
*check-file                  - Check if specific file can be modified
*mark-epic-complete          - Mark epic complete (creates forbidden zone)
*show-boundaries             - Display current boundaries and protected files
*generate-story-context      - Generate story-context.xml with forbidden zones
```

**When to Use:**
- Before starting any new story (check boundaries)
- After completing an epic (mark as complete and protect)
- Before committing code (validate no boundary violations)
- When generating story-context XML (includes forbidden zones)

**Example Usage:**
```
@bmad/agents/epic-boundary-guardian
Command: *validate-changes
Current Epic: Epic 3 (Events Management)
Files: backend/modules/events/routes.py, backend/modules/auth/middleware.py

→ Sentinel checks if files allowed for Epic 3
→ Detects: backend/modules/auth/ is Epic 1 (if complete, FORBIDDEN)
→ Explains violation and suggests alternatives
→ Offers READ-ONLY usage pattern instead
```

**Location:** `bmad/agents/epic-boundary-guardian/`

**Epic Status Tracked In:** `docs/epic-status.md`

**Boundary Rules:**
- ✅ Completed epic code is READ-ONLY
- ✅ Can import/use completed epic code
- ✅ Cannot modify completed epic files
- ✅ Shared modules require extra review
- ✅ Database migrations are APPEND-ONLY

---

## How These Agents Work Together

**Development Workflow with Guardian Agents:**

```
Step 1: Start new story (Epic 3, Story 3.2)
  ↓
Step 2: Check boundaries
  → @bmad/agents/epic-boundary-guardian
  → Command: *show-boundaries
  → See which files are protected (Epic 1, 2 complete)
  ↓
Step 3: Implement story
  → Create: backend/modules/events/routes.py
  → Use (READ-ONLY): from backend.modules.auth.dependencies import get_current_user
  ↓
Step 4: Create database migration
  → alembic revision --autogenerate -m "Create Event table"
  ↓
Step 5: Validate migration
  → @bmad/agents/database-migration-validator
  → Command: *validate-migration
  → File: database/migrations/versions/005_create_event_table.py
  → Solomon reports: PASS ✅ (all standards followed)
  ↓
Step 6: Before commit, validate boundaries
  → @bmad/agents/epic-boundary-guardian
  → Command: *validate-changes
  → Sentinel reports: PASS ✅ (no boundary violations)
  ↓
Step 7: Commit code
  → git add .
  → git commit -m "Epic 3, Story 3.2: Create Event CRUD endpoints"
  ✅ Clean, standards-compliant, boundary-safe code
```

---

## Installation

**These agents are YAML source files** (compiled to .md by BMAD installer).

**To activate:**

**Option A: If you have BMAD build tools:**
```bash
# Run BMAD installer
# Select: "Compile Agents (Quick rebuild)"
# Agents will be available as @bmad/agents/{{agent-name}}
```

**Option B: Manual activation (no build tools):**
```
The agents are ready to use as-is. Reference them:
@bmad/agents/database-migration-validator
@bmad/agents/epic-boundary-guardian
```

---

## Agent File Structure

```
bmad/agents/
├── database-migration-validator/
│   ├── database-migration-validator.agent.yaml    # Agent definition
│   └── workflows/
│       ├── validate-migration.md                  # Main validation workflow
│       ├── validate-all.md                        # Batch validation
│       ├── generate-template.md                   # Template generator
│       ├── check-standards.md                     # Standards reference
│       └── teach-standard.md                      # Educational mode
│
└── epic-boundary-guardian/
    ├── epic-boundary-guardian.agent.yaml          # Agent definition
    └── workflows/
        ├── validate-changes.md                    # Main validation workflow
        ├── check-file.md                          # Single file check
        ├── mark-complete.md                       # Mark epic complete
        ├── show-boundaries.md                     # Display boundaries
        └── generate-context.md                    # Story-context generator
```

---

## Benefits

**These agents address your v4 pain points:**

✅ **Database naming violations prevented**
- Solomon validates EVERY migration before it's applied
- Catches PascalCase violations, VARCHAR usage, missing audit columns
- Educational feedback (teaches WHY, not just WHAT)

✅ **Epic boundary violations prevented**
- Sentinel blocks modifications to completed epic code
- Forces READ-ONLY usage of dependencies
- Tracks epic status and protected files

✅ **Proactive quality management**
- Validate before committing (not after bugs appear)
- Clear feedback loops (pass/fail, not ambiguous)
- Educational (learn standards over time)

---

## Next Steps

**Before Epic 1 Implementation:**

1. **Familiarize with agents:**
   - Read agent YAML files (see persona, commands)
   - Try `*check-standards` (Solomon shows database rules)
   - Try `*show-boundaries` (Sentinel shows current status)

2. **During Epic 1:**
   - Create migration → Validate with Solomon
   - Before commit → Validate with Sentinel
   - After Epic 1 complete → Mark complete with Sentinel

3. **Epic 1 Complete:**
   - Run: `*mark-epic-complete` (Sentinel locks Epic 1 files)
   - Epic 2 development → Sentinel prevents modifying Epic 1

---

**Created by:** BMad Builder workflow  
**Date:** 2025-10-12  
**Status:** ✅ Ready for use

