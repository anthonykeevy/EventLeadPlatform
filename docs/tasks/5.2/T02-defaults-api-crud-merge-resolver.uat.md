# T02 UAT: Defaults API — CRUD + Merge Resolver

**Task:** T02 - Defaults API: CRUD + Merge Resolver  
**Story:** 5.2 - Company Form Defaults (Brand System)  

---

## Prerequisites

- Database: EventLeadPlatform (SQL Server) with migration 039 applied (T01)
- Backend venv activated
- Valid JWT for company_admin (company defaults) or system_admin (global defaults)
- Company and User exist for company-scoped tests

---

## UAT Steps

### AC1: Global defaults API exists

#### GET /api/form-defaults/global
- **Auth:** system_admin JWT
- **Expected:** 200, `{ "defaults": { theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent }, "versionNumber": 1 }`
- **403:** Non-admin user

#### PUT /api/form-defaults/global
- **Auth:** system_admin JWT
- **Body:** `{ "defaults": { "theme": { "primaryColor": "#FF0000" }, ... }, "changeSummary": "UAT test" }`
- **Expected:** 200, updated defaults returned with incremented versionNumber
- **403:** Non-admin user

#### GET /api/form-defaults/global/history
- **Auth:** system_admin JWT
- **Expected:** 200, `{ "items": [ { versionNumber, defaults, changeSummary, createdDate, createdBy } ], "total": N }`

---

### AC2: Company defaults API exists

#### GET /api/companies/{id}/form-defaults
- **Auth:** JWT for user in company
- **Expected:** 200, merged defaults (Global + Company overrides)
- **403:** User not in company

#### PUT /api/companies/{id}/form-defaults
- **Auth:** company_admin JWT for that company
- **Body:** `{ "defaults": { "theme": { "primaryColor": "#00FF00" } }, "changeSummary": "Company branding" }`
- **Expected:** 200, updated merged defaults
- **403:** Non-admin or wrong company

#### GET /api/companies/{id}/form-defaults/history
- **Auth:** company_admin JWT for that company
- **Expected:** 200, `{ "items": [...], "total": N }`

---

### AC3: Merge resolver produces correct structure

1. PUT company defaults with partial override (e.g. only theme.primaryColor)
2. GET merged defaults
3. **Verify:** Global values preserved where not overridden; company override applied
4. **Verify:** Response includes theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent

---

### AC4: Version tables populated on update

1. PUT global or company defaults
2. Query `[dbo].[GlobalFormDefaultsVersion]` or `[dbo].[CompanyFormDefaultsVersion]`
3. **Verify:** New row with CreatedBy, CreatedDate, VersionNumber incremented

---

## Quick Manual Test (curl/Postman)

Replace `{JWT}` and `{COMPANY_ID}`:

```bash
# Global (system_admin)
curl -H "Authorization: Bearer {JWT}" http://localhost:8000/api/form-defaults/global

# Company merged
curl -H "Authorization: Bearer {JWT}" http://localhost:8000/api/companies/{COMPANY_ID}/form-defaults

# Put company
curl -X PUT -H "Authorization: Bearer {JWT}" -H "Content-Type: application/json" \
  -d '{"defaults":{"theme":{"primaryColor":"#00AA00"}},"changeSummary":"UAT"}' \
  http://localhost:8000/api/companies/{COMPANY_ID}/form-defaults
```
