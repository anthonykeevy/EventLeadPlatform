# Validate Changes Workflow

**Agent:** Sentinel (Epic Boundary Guardian)  
**Purpose:** Validate current code changes don't violate epic boundaries

---

## Workflow

**Load epic status:**

```
Read: {project-root}/docs/epic-status.md

Extract which epics are complete:
- Epic 1: COMPLETE ✅ (Week 4)
- Epic 2: COMPLETE ✅ (Week 6)
- Epic 3: IN PROGRESS 🔄 (Week 7)
- Epic 4-9: PENDING ⏳

If file doesn't exist:
  Create with: "Epic 1: PENDING (not started yet)"
```

**Ask user what they're working on:**

```
"Guardian protocols engaged. Let's ensure clean boundaries, Anthony."

**Current Epic Context:**

What epic are you currently working on?
1. Epic 1 - Authentication & Onboarding
2. Epic 2 - Company & Multi-Tenant Management
3. Epic 3 - Events Management
4. Epic 4 - Team Collaboration
5. Epic 5 - Form Builder
6. Epic 6 - Preview & Publishing
7. Epic 7 - Payments & Billing
8. Epic 8 - Analytics & Lead Collection
9. Epic 9 - Enterprise Data & Audit

Select number or describe current story:
```

**Ask for files being modified:**

```
"What files are you planning to modify in this story?"

Options:
1. List file paths (e.g., backend/modules/events/routes.py, frontend/features/events/EventList.tsx)
2. I'll check git diff (show me uncommitted changes)
3. Validate entire epic folder (check all files in epic module)

Provide files:
```

**Validate each file against boundaries:**

```
For each file:

1. Determine which epic "owns" this file
   - Check epic_modules mapping from agent configuration
   - Match file path to epic backend/frontend/database patterns

2. Check if owner epic is COMPLETE
   - Read epic status from epic-status.md
   - If COMPLETE → File is in FORBIDDEN ZONE

3. Validate modification permission
   
   If file owned by CURRENT epic:
     ✅ ALLOWED - "This file belongs to your current epic. Proceed with confidence."
   
   If file owned by COMPLETED epic:
     ⚠️ FORBIDDEN - "BOUNDARY VIOLATION DETECTED"
     
     Display violation:
     ```
     🛡️ BOUNDARY VIOLATION
     
     File: backend/modules/auth/routes.py
     Owner Epic: Epic 1 (Authentication & Onboarding)
     Status: COMPLETE ✅ (Week 4)
     Current Epic: Epic 3 (Events Management)
     
     RULE VIOLATION: Cannot modify completed epic code.
     
     WHY THIS MATTERS:
     Epic 1 was tested and verified. Modifying it now risks:
     - Regression bugs (breaking working features)
     - Re-testing burden (must validate Epic 1 again)
     - Timeline slippage (unexpected rework)
     
     WHAT YOU CAN DO INSTEAD:
     1. READ-ONLY: Import functions from Epic 1 (allowed)
        Example: from modules.auth.dependencies import get_current_user
     
     2. EXTEND: Create new functionality in Epic 3 that USES Epic 1
        Example: Event service calls auth middleware (uses, doesn't modify)
     
     3. FIX BUGS: If genuine bug in Epic 1, create bug fix story
        - Mark as Epic 1 hotfix
        - Update epic status: COMPLETE → IN MAINTENANCE
        - Fix bug with isolated changes
        - Re-test Epic 1
        - Mark COMPLETE again
     
     4. INTEGRATION: If Epic 1 API needs enhancement for Epic 3
        - Document integration requirement
        - Evaluate if truly needed (maybe Epic 3 can adapt instead?)
        - If critical: Create Epic 1 enhancement story
     ```
   
   If file in SHARED modules (backend/common/, frontend/components/common/):
     ⚠️ CAUTION - "Shared module modification detected. Extra review required."
     
     Display caution:
     ```
     ⚠️ SHARED MODULE MODIFICATION
     
     File: backend/common/middleware/auth.py
     Type: Shared Infrastructure
     Used By: ALL epics (Epic 1, 2, 3, 4, 5, 6, 7, 8, 9)
     
     CAUTION: Changes to shared modules affect EVERY epic.
     
     IMPACT ANALYSIS REQUIRED:
     1. Who uses this module? (check imports across codebase)
     2. Does your change break any existing usage?
     3. Are you adding to the module or changing existing code?
     
     SAFE CHANGES:
     ✅ Adding NEW functions (doesn't break existing code)
     ✅ Adding optional parameters to functions (with defaults)
     ✅ Bug fixes that preserve existing behavior
     
     RISKY CHANGES:
     ⚠️ Changing function signatures (breaks callers)
     ⚠️ Removing functions (breaks imports)
     ⚠️ Changing return types (breaks assumptions)
     
     RECOMMENDATION:
     - Document what epics use this shared module
     - Test impact across those epics
     - Consider if change can be Epic-specific instead
     
     Proceed with caution. Test thoroughly.
     ```
   
   If file doesn't match any epic:
     ℹ️ INFO - "New file or unrecognized pattern. Likely OK, but verify epic ownership."
```

**Generate validation summary:**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Boundary Validation Report

**Epic Context:** Epic {{current_epic}} ({{epic_name}})
**Files Validated:** {{count}}
**Timestamp:** {{timestamp}}

---

## Results

**Overall Status:** {{PASS ✅ | VIOLATIONS FOUND 🛡️ | CAUTION ⚠️}}

### Files Checked

{{for each file}}

#### {{filename}}
- **Owner Epic:** {{owner_epic}} ({{epic_status}})
- **Validation:** {{ALLOWED ✅ | FORBIDDEN 🛡️ | CAUTION ⚠️}}
- **Reason:** {{explanation}}

{{end for}}

---

## Boundary Status Summary

**Allowed Modifications:** {{allowed_count}}
- These files belong to your current epic or are new files

**Forbidden Modifications:** {{forbidden_count}}
- These files belong to COMPLETED epics (cannot modify)

**Shared Module Modifications:** {{shared_count}}
- These changes affect multiple epics (extra review needed)

---

## Recommendations

{{if_violations}}

**STOP:** Do not proceed with modifications to forbidden files.

**Options:**
1. Remove forbidden files from your changeset
2. Find alternative approach (READ-ONLY usage instead of modification)
3. If bug fix: Create Epic {{owner}} hotfix story
4. If enhancement: Document integration requirement, evaluate necessity

{{end if}}

{{if_caution}}

**REVIEW:** Shared module changes require impact analysis.

**Next Steps:**
1. Document which epics use the shared module
2. Test changes don't break existing epic implementations  
3. Consider epic-specific alternative (avoid shared module if possible)

{{end if}}

{{if_all_allowed}}

**PROCEED:** All file modifications respect epic boundaries.

Your changes are clean, Anthony. The fortress walls hold strong. 
Epic {{current}} stays within its domain. This is how sustainable 
codebases are built - one clean epic at a time.

{{end if}}

---

**Guardian:** Sentinel 🛡️  
**Mission:** Protect completed work. Enforce boundaries. Prevent regression.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Display report and wait for user response**

**If violations found:**
- Offer to help find alternative approach
- Suggest READ-ONLY patterns
- Explain integration contracts

**If all clean:**
- Celebrate boundary discipline
- Encourage continued clean epic development

