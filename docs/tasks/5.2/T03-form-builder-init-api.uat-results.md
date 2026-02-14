# T03 UAT Results

**Task:** T03 - Form Builder Init API (Single Payload)  
**Date:** 2026-02-14  
**Executor:** Ralf-Dev (Agent)  

---

## Automated Verification

| Check | Result | Evidence |
|-------|--------|----------|
| Backend imports | PASS | `python -c "from main import app"` succeeds |
| Form Builder route registered | PASS | `/api/form-builder/init` in app routes |
| Auth enforced | PASS | POST without Authorization returns 401 "Missing authorization header" |
| OpenAPI docs | PASS | GET /docs shows POST /api/form-builder/init |

---

## Manual UAT (Requires User)

Full UAT requires:
- Migration 039 applied (T01)
- T02 Defaults API working (Global + Company seeds)
- Backend venv activated
- Valid JWT; CompanyID and EventID exist in DB

### AC1: Endpoint exists
- **Action:** `POST /api/form-builder/init` with body `{"companyId": 1, "eventId": 1}` and Bearer token
- **Expected:** 200, valid payload
- **400/404:** Invalid companyId or eventId

### AC2: Response contains merged defaults
- `defaults.theme`, `defaults.globalStyles`, `defaults.canvasSettings`
- `defaults.defaultGridLayoutsByComponent` (allowed components only)

### AC3: Response contains component catalog
- `components` array: one per allowed component (Global ∪ Country ∪ Company)
- Each has: componentCode, displayName, propertiesSchema, structure, defaultGridLayoutVertical, defaultGridLayoutHorizontal

### AC4: Response contains DefinitionJSON skeleton
- `definitionJSON` with schemaVersion, empty pages, empty logic

### AC5: Context echoed
- `context.companyId`, `context.eventId`, `context.countryId`

---

## UAT Status

**Agent verification:** PASS (endpoint registered, auth enforced, imports succeed)  
**Full manual UAT:** Pending user execution with DB + JWT + valid Company/Event

---

*Ralf-Dev*
