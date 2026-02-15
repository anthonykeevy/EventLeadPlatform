# T05 UAT: Builder — Inherit Defaults + Override UX + Init API Integration

**Task:** T05 - Builder: Inherit Defaults + Override UX + Init API Integration  
**Story:** 5.2 - Company Form Defaults (Brand System)  

---

## Prerequisites

- T02, T03, T04 complete
- Backend + frontend running
- Company Admin user; Company with Form Branding Defaults set
- Form context (companyId, eventId) available

---

## UAT Steps

### AC1: Init API consumed on new form

| Step | Status | Notes |
|------|--------|-------|
| Start new form in Builder | | |
| Verify Init API called (Network tab) | | POST /api/form-builder/init with companyId, eventId |
| Defaults from API, not hardcoded | | theme, globalStyles, canvasSettings |
| Toolbox from API components | | Components from Init response |

### AC2: Inherited vs overridden visible

| Step | Status | Notes |
|------|--------|-------|
| Global Properties Panel shows inherited values | | Read-only, source indicated |
| "Override" action available | | Allows form-level override |
| Clear indication: company vs form | | Source label/badge |

### AC3: Save to Company Defaults works

| Step | Status | Notes |
|------|--------|-------|
| Button visible to Company Admin | | Hidden for non-admin |
| Click saves form overrides to company defaults | | PUT /api/companies/{id}/form-defaults |
| Version history updated | | CompanyFormDefaultsVersion |

### AC4: Edit company defaults link

| Step | Status | Notes |
|------|--------|-------|
| Link present in Global Properties | | "Edit company defaults" |
| Opens Company Settings → Form Branding Defaults | | Or navigates to Dashboard |

### AC5: DefinitionJSON persisted on save

| Step | Status | Notes |
|------|--------|-------|
| Save form in Builder | | |
| Full DefinitionJSON written to FormVersion | | Verify DB or API response |

---

*Record results in T05-builder-inherit-override-init-api.uat-results.md*
