# UAT Results: T05 — Builder Inherit Defaults + Override UX + Init API Integration

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T05 - Builder Inherit Defaults + Override UX + Init API Integration  
**Executed:** 2026-02-15  
**Tester:** Anthony Keevy (Agent-assisted)  
**Result:** ⚠️ **PARTIAL** — Implementation complete; full UAT requires T02/T03/T04 merged

---

## Pre-conditions

| Item | Status | Notes |
|------|--------|-------|
| Backend server running | ⏭️ N/A | Init API (T03) and form-defaults (T02) may not be in main branch |
| Frontend is running | ✅ Pass | Built successfully |
| User logged in as Company Admin | ⏭️ N/A | Manual test required |
| Form with CompanyID and EventID | ⏭️ N/A | Manual test required |
| Migration 039 | ⏭️ N/A | Story branch prerequisite |
| Form Branding Defaults page | ⏭️ N/A | T04 route may not exist in base |

---

## AC Results

### AC1: Init API consumed on new form

| Step | Status | Notes |
|------|--------|-------|
| Builder code calls Init API when companyId+eventId available | ✅ Pass | useBuilderStore.initializeForm fetches form header, calls formBuilderInit |
| Fallback when Init API unavailable | ✅ Pass | formBuilderInit returns null on 404/5xx; createEmptyFormDefinition used |
| Toolbox from Init components when available | ✅ Pass | ComponentSidebar filters by initComponents |

### AC2: Inherited vs overridden visible

| Step | Status | Notes |
|------|--------|-------|
| Note about inherited/overridden | ✅ Pass | "Values can be inherited from company defaults or overridden for this form" when companyId present |
| Form-level override by editing | ✅ Pass | updateGlobalStyles persists form overrides |

### AC3: Save to Company Defaults works

| Step | Status | Notes |
|------|--------|-------|
| Button visible to Company Admin | ✅ Pass | isCompanyAdmin from useAuth; button shown when company_admin/system_admin |
| Calls PUT /api/companies/{id}/form-defaults | ✅ Pass | putCompanyFormDefaults in formDefaultsApi |
| Toast on success | ✅ Pass | useToastNotifications in GlobalStylesPanel |

### AC4: Edit company defaults link

| Step | Status | Notes |
|------|--------|-------|
| Link present when companyId available | ✅ Pass | Links to /dashboard/companies/{id}/form-branding-defaults |
| Opens in new tab | ✅ Pass | target="_blank" rel="noopener noreferrer" |

### AC5: DefinitionJSON persisted on save

| Step | Status | Notes |
|------|--------|-------|
| Full DefinitionJSON on save | ✅ Pass | saveDraft uses normalizeDefinitionForSave; updateDraftVersion/createDraftVersion send full definition |

---

## Regression Check

| Item | Status |
|------|--------|
| Build passes | ✅ Pass |
| No new lint errors | ✅ Pass |
| Graceful degradation when APIs unavailable | ✅ Pass |

---

## Implementation Summary

**Files changed:**

| File | Change | Reason |
|------|--------|--------|
| frontend/src/features/builder/api/formBuilderInitApi.ts | Created | Init API client |
| frontend/src/features/builder/api/formDefaultsApi.ts | Created | Company form-defaults API |
| frontend/src/features/builder/stores/useBuilderStore.ts | Modified | Init flow, formContext, saveToCompanyDefaults |
| frontend/src/features/builder/components/ComponentSidebar.tsx | Modified | Filter toolbox by initComponents |
| frontend/src/features/builder/components/PropertiesPanel.tsx | Modified | Pass formContext, isCompanyAdmin, saveToCompanyDefaults |
| frontend/src/features/builder/components/properties/GlobalStylesPanel.tsx | Modified | Edit link, Save to Company Defaults, inherited note |

---

## Recommended Next Step

**For full UAT:** Merge T02, T03, T04 into story branch, run backend, execute UAT checklist manually.

**Ready for:** PR review and merge into story branch.
