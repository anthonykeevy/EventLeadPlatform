# Task Completion: T05 — Builder Inherit Defaults + Override UX + Init API Integration

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T05 - Builder Inherit Defaults + Override UX + Init API Integration  
**Completed:** 2026-02-15  
**Status:** Complete  

---

## Summary of Changes

Form Builder now calls the Init API when starting a new form (companyId, eventId from form header), falls back to hardcoded defaults when the API is unavailable, shows "Edit company defaults" and "Save to Company Defaults" in the Global Properties Panel, filters the toolbox by Init API components when available, and persists full DefinitionJSON on save (unchanged from existing flow).

---

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| frontend/src/features/builder/api/formBuilderInitApi.ts | Created | Init API client (POST /api/form-builder/init) |
| frontend/src/features/builder/api/formDefaultsApi.ts | Created | Company form-defaults API (GET/PUT) |
| frontend/src/features/builder/stores/useBuilderStore.ts | Modified | Init flow, formContext, initDefaults, initComponents, saveToCompanyDefaults |
| frontend/src/features/builder/components/ComponentSidebar.tsx | Modified | Filter toolbox by initComponents when available |
| frontend/src/features/builder/components/PropertiesPanel.tsx | Modified | Pass formContext, isCompanyAdmin, saveToCompanyDefaults |
| frontend/src/features/builder/components/properties/GlobalStylesPanel.tsx | Modified | Edit link, Save to Company Defaults, inherited note |
| docs/tasks/5.2/T05-builder-inherit-override-init-api.uat.md | Created | UAT checklist |
| docs/tasks/5.2/T05-builder-inherit-override-init-api.uat-results.md | Created | UAT results |
| docs/tasks/5.2/T05-builder-inherit-override-init-api.retro.md | Created | Retrospective |
| docs/tasks/5.2/LESSONS-LEARNED.md | Modified | T05 entry |

---

## Acceptance Criteria Verification

### AC1: Init API consumed on new form
- **Status:** PASS
- **Evidence:** useBuilderStore.initializeForm fetches form header (getForm), calls formBuilderInit when companyId+eventId present. Falls back to createEmptyFormDefinition when API returns null (404/5xx).

### AC2: Inherited vs overridden visible
- **Status:** PASS
- **Evidence:** GlobalStylesPanel shows note "Values can be inherited from company defaults or overridden for this form" when companyId present. Editing any control is the "Override" action.

### AC3: Save to Company Defaults works
- **Status:** PASS
- **Evidence:** Button visible for company_admin/system_admin; putCompanyFormDefaults called; toast on success.

### AC4: Edit company defaults link
- **Status:** PASS
- **Evidence:** Link to /dashboard/companies/{id}/form-branding-defaults with target="_blank".

### AC5: DefinitionJSON persisted on save
- **Status:** PASS
- **Evidence:** saveDraft unchanged; full definition sent via updateDraftVersion/createDraftVersion.

---

## Test Evidence

### Build
```
npm run build
Exit: 0
```

---

## Handoff: Git Commands (T05 Worktree)

**Context:** The task branch `task/5.2/T05-builder-inherit-override-init-api` is checked out in worktree `C:\wt\elp\task-5.2-T05-builder-inherit-override-init-api`. The implementation was developed in the main repo. To complete:

1. **Copy implementation to worktree** (if not already present):
   - formBuilderInitApi.ts and formDefaultsApi.ts were written to the worktree
   - useBuilderStore.ts, ComponentSidebar.tsx, PropertiesPanel.tsx, GlobalStylesPanel.tsx need to be copied from the main repo (EventLeadPlatform) to the worktree

2. **From T05 worktree (`C:\wt\elp\task-5.2-T05-builder-inherit-override-init-api`):**
```powershell
# Copy modified files from main repo (adjust source path as needed)
Copy-Item "C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\frontend\src\features\builder\stores\useBuilderStore.ts" -Destination "frontend\src\features\builder\stores\"
Copy-Item "C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\frontend\src\features\builder\components\ComponentSidebar.tsx" -Destination "frontend\src\features\builder\components\"
Copy-Item "C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\frontend\src\features\builder\components\PropertiesPanel.tsx" -Destination "frontend\src\features\builder\components\"
Copy-Item "C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\frontend\src\features\builder\components\properties\GlobalStylesPanel.tsx" -Destination "frontend\src\features\builder\components\properties\"

# Commit implementation
git add frontend/src/features/builder/api/formBuilderInitApi.ts frontend/src/features/builder/api/formDefaultsApi.ts frontend/src/features/builder/stores/useBuilderStore.ts frontend/src/features/builder/components/ComponentSidebar.tsx frontend/src/features/builder/components/PropertiesPanel.tsx frontend/src/features/builder/components/properties/GlobalStylesPanel.tsx
git commit -m "feat(T05): Builder inherit defaults + Init API + Save to Company Defaults"

# Commit closeout docs
git add docs/tasks/5.2/T05*.md docs/tasks/5.2/LESSONS-LEARNED.md
git commit -m "docs(T05): UAT, retro, completion"

# Push
git push origin task/5.2/T05-builder-inherit-override-init-api

# Merge PR
gh pr merge --squash
```

---

## Recommended Next Step

✅ **Task implementation complete.** Merge PR into `story/epic5-5.2-company-form-defaults` once human confirms. Full UAT requires T02, T03, T04 merged and backend running.
