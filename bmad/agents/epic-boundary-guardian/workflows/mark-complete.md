# Mark Epic Complete Workflow

**Agent:** Sentinel (Epic Boundary Guardian)  
**Purpose:** Mark an epic as complete and create forbidden zones to protect completed work

---

## Workflow

**Load epic status:**
```
Read: {project-root}/docs/epic-status.md
```

**Update epic status:**
```
Mark Epic 1 as COMPLETE
Set completion date: 2025-10-26
Set status: COMPLETE
```

**Create forbidden zones:**
```
Epic 1 Files (READ-ONLY):
- backend/modules/auth/
- backend/modules/companies/
- backend/modules/invitations/
- frontend/features/auth/
- frontend/features/dashboard/
- frontend/features/invitations/
- frontend/features/ux/
- database/migrations/001_*.py
- database/migrations/002_*.py
- database/migrations/003_*.py
- database/migrations/004_*.py
- database/migrations/005_*.py
- database/migrations/006_*.py
```

**Update epic status file:**
```
Write to: {project-root}/docs/epic-status.md
Content: Epic 1 marked as COMPLETE with forbidden zones
```

**Display confirmation:**
```
🛡️ EPIC 1 PROTECTED - Forbidden Zones Created

Epic 1: EventLead Platform Foundation - COMPLETE ✅
Completion Date: 2025-10-26
Status: PROTECTED (READ-ONLY)

Forbidden Zones Created:
- Authentication & Onboarding modules
- Company & Multi-Tenant modules  
- Team Collaboration modules
- Frontend Auth, Dashboard, Invitations, UX modules
- Database migrations 001-006

Allowed Interactions:
- ✅ Import functions/classes (read-only usage)
- ✅ Call API endpoints (integration usage)
- ✅ Reference database tables in queries (FK relationships)

Forbidden Actions:
- ❌ Modify any files in protected paths
- ❌ Change API contracts or function signatures
- ❌ Edit database migrations
- ❌ Refactor code (even if "improving")

Epic 2 can now begin with protected Epic 1 foundation!
```

**Save epic status:**
```
Write to: {project-root}/docs/epic-status.md
```

**Display to user:**
