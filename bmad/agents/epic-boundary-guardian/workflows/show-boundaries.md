# Show Epic Boundaries Workflow

**Agent:** Sentinel (Epic Boundary Guardian)  
**Purpose:** Display current epic boundaries and forbidden zones

---

## Workflow

**Load epic status:**
```
Read: {project-root}/docs/epic-status.md
```

**Generate boundary visualization:**

```markdown
🛡️ **Epic Boundary Status - EventLeadPlatform**

**Updated:** {{timestamp}}

---

## Current Forbidden Zones (Completed Epics)

{{for each complete epic}}

### Epic {{number}}: {{name}} ✅ COMPLETE ({{completion_date}})

**PROTECTED FILES (READ-ONLY):**
```
{{epic_backend_modules}}
{{epic_frontend_modules}}
{{epic_database_files}}
{{epic_models}}
```

**ALLOWED INTERACTIONS:**
- ✅ Import functions/classes (read-only usage)
- ✅ Call API endpoints (integration usage)
- ✅ Reference database tables in queries (FK relationships)

**FORBIDDEN ACTIONS:**
- ❌ Modify any files in protected paths
- ❌ Change API contracts or function signatures
- ❌ Edit database migrations
- ❌ Refactor code (even if "improving")

**WHY PROTECTED:**
Epic {{number}} was completed in Week {{week}}, tested, and verified. 
Changes now would require re-testing and risk regression bugs.

---

{{end for}}

{{if_no_complete_epics}}

**No epics complete yet.** All code is modifiable.

Once Epic 1 completes, its files will become protected forbidden zones.

{{end if}}

---

## Current Epic In Progress

**Epic {{current}}:** {{name}} 🔄 IN PROGRESS

**YOUR WORKSPACE (Unrestricted):**
```
{{current_epic_modules}}
```

You can modify these files freely - they're your epic's domain.

---

## Shared Infrastructure (Modify with Caution)

**These modules are used by MULTIPLE epics:**
```
backend/common/          - Middleware, utilities, providers
frontend/components/common/  - Shared UI components
frontend/lib/            - Shared hooks, utilities
database/migrations/     - APPEND-ONLY (add new, don't edit old)
```

**Rule:** Shared modules CAN be modified, but:
1. Changes must be ADDITIVE (add features, don't break existing)
2. Test impact across ALL epics using the module
3. Document changes in epic retrospective

---

## Epic Dependency Graph

```
Auth (Epic 1) ← No dependencies (foundation)
  ↓ (provides current_user)
Companies (Epic 2) ← Depends on: Epic 1
  ↓ (provides current_company, multi-tenant context)
Events (Epic 3) ← Depends on: Epic 1, 2
Team (Epic 4) ← Depends on: Epic 1, 2
Forms (Epic 5) ← Depends on: Epic 1, 2, 3
Payments (Epic 7) ← Depends on: Epic 1, 2, 5
Analytics (Epic 8) ← Depends on: Epic 1, 2, 5
```

**READ-ONLY Dependencies:**
- Later epics can USE earlier epic code (import, call APIs)
- Later epics CANNOT MODIFY earlier epic code

---

## Boundary Discipline Benefits

**Why we enforce boundaries:**

1. **Prevents Regression** - Completed code stays stable
2. **Preserves Testing** - No need to re-test Epic 1 when building Epic 3
3. **Clear Ownership** - Each epic owns its domain
4. **Sustainable Development** - Build forward, don't circle back
5. **Addresses v4 Pain** - No more "Epic 2 broke Epic 1" surprises

**Your v4 experience taught us:** Boundaries aren't restrictions - they're protection.

---

🛡️ **Guardian active. Boundaries monitored. Your completed work is safe.**
```

**Display to user**

