# ABR Company Lookup — Form Builder Handoff

**Requested by:** Tony (2026-05-21)  
**Status:** **Mandatory in Story 6.5d Track A** — implement with `address-lookup-au` under `decision-external-data-feed-components.md`  
**Provider:** Already live for **onboarding** (`ref.Country.CompanyValidationProvider = 'ABR'`)

---

## Existing EventLeadPlatform implementation (reuse — do not re-research ABR XML)

| Area | Path |
|------|------|
| **HTTP client** | `backend/modules/companies/abr_client.py` |
| **API routes** | `backend/modules/companies/router.py` — ABR smart search endpoints (Story 1.10 / 1.19) |
| **Schemas** | `backend/modules/companies/schemas.py` — `CompanySearchRequest`, `CompanySearchResult`, etc. |
| **Cache** | `cache.ABRSearch` model |
| **Frontend (onboarding)** | `frontend/src/features/onboarding/components/OnboardingStep2.tsx` — ABR search UX pattern |

**Env:** `ABR_API_KEY`, `ABR_API_TIMEOUT` (see `abr_client.py` docstring).

---

## Builder component target

| Property | Suggested value |
|----------|-----------------|
| `ComponentCode` | `company-lookup-abr` (or `abr-company-search` — pick one, document in closeout) |
| Scope | **Country** — AU (`CompanyValidationProvider = 'ABR'`) |
| Behaviour | Autocomplete by ABN / ACN / name → populate structured company fields on the form (legal name, ABN, entity type, GST flag per onboarding parity) |
| Offline | Same rule as `address-lookup-au`: **exclude** when form requires offline-capable publish |

---

## Implementation checklist (when scheduled)

1. `FormBuilderComponent` seed + `ref.ComponentType`
2. Backend route may **delegate** to existing company ABR search service (avoid duplicate XML parsing)
3. `ComponentRegistry` runtime + preview
4. Four-consumer alignment + `verify_component_catalog_alignment.py`
5. Block G prose — only mention if catalog includes the code for AU non-offline forms

---

*Handoff doc — Story 6.5d SM pack, 2026-05-21.*
