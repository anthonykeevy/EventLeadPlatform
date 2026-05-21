# AU Address Lookup (GeoScape / PSMA) — Dev Handoff

**Story:** 6.5d Track A (`address-lookup-au`)  
**Status:** Reference — routes and flags per [decision-external-data-feed-components.md](./decision-external-data-feed-components.md) (Approved)  
**Provider:** GeoScape / PSMA (`ref.Country.AddressValidationProvider = 'Geoscape'` in seed data)

---

## Source project (Tony's working implementation)

| Resource | Path (JobTrackerDB) |
|----------|-------------------|
| **Domain doc (start here)** | `project-knowledge/domains/geoscape/domain-doc.md` |
| **Service layer** | `project-core/backend/app/services/geoscape/geoscape_service.py` |
| **HTTP client** | `project-core/backend/app/services/geoscape/geoscape_client.py` |
| **REST routes** | `project-core/backend/app/api/address.py` — `GET /api/address/search`, `POST /api/address/validate` |
| **Legacy integration notes** | `project-knowledge/legacy-docs/geoscape-api-integration.md` |
| **Improvements summary** | `project-core/backend/GEOSCAPE_IMPROVEMENTS_SUMMARY.md` |

**Do not copy JobTrackerDB DB tables** (PSMA* tables) into EventLeadPlatform unless Dimitri/architecture explicitly requires them. For the builder component, prefer **proxy APIs** on EventLeadPlatform backend + store selected address lines in `DefinitionJSON` / submission payload (same pattern as generic `address` component).

---

## API facts (verified in JobTrackerDB)

| Item | Value |
|------|--------|
| **Base URL** | `https://api.psma.com.au` (not `api.geoscape.com.au`) |
| **Auth** | `Authorization: {GEOSCAPE_API_KEY}` — simple key, **no** `Bearer` prefix |
| **Search** | `GET /v1/predictive/address?query=...&limit=...` |
| **Details** | `GET /v1/addresses/{psmaId}` |
| **Env var (suggested)** | `GEOSCAPE_API_KEY` (align with Tony's JobTrackerDB `.env`) |

**Non-existent endpoints (do not implement):** `/v1/predictive/address/validate`, `/v1/health`, `/v2/addresses/*`.

**Rate limits (free tier reference):** ~2 req/s, 20k credits/month — design debounced autocomplete in builder.

---

## EventLeadPlatform wiring (6.5d scope)

1. **Backend module** — `backend/modules/external_feed/` (or sibling) with thin routes per [decision-external-data-feed-components.md](./decision-external-data-feed-components.md) §3.2:
   - `GET /api/external-feed/address-au/search?q=&limit=`
   - `POST /api/external-feed/address-au/resolve` `{ "psmaAddressId": "..." }`
2. **Reuse patterns** from `backend/modules/companies/abr_client.py` (httpx, timeout, structured errors) + **`cache.AddressSearch`** via `AddressCacheService` (mandatory — not optional).
3. **Frontend** — extend `ComponentRegistry` for `address-lookup-au`: debounced search, pick suggestion, map PSMA id → structured lines.
4. **Catalog** — Country-scoped `FormBuilderComponent` row (AU only); see `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md`.
5. **Properties Panel toggles** — implement all `address-lookup-au` switches in decision doc **§11.2** (manual fallback, delivery instructions, unit line, strict validation).

**Reference UX:** Mirror `SmartCompanySearch` no-results / error panels; reuse onboarding manual-entry copy where possible.

---

## Offline / online-required forms (first API-dependent component)

`address-lookup-au` is the **first builder component that requires live third-party API access**. When a customer explicitly requires the published form to **run offline** (event lead capture without connectivity):

- **Exclude** `address-lookup-au` from `resolve_allowed_components()` for that form/company context.
- Offer **`address`** (manual entry) as the offline-safe alternative in toolbox + AI ALLOWED list.

**Design tasks for Dev:**

| Task | Notes |
|------|--------|
| Model flag | **`Form.RequiresOfflineCapable`** (BIT, default 0) — approved in EDF decision §9.2. |
| Resolver filter | When `RequiresOfflineCapable = 1`, omit codes where `ref.ComponentType.RequiresNetwork = 1`. |
| AI / validator | Same filter as init toolbox (four-consumer alignment). |
| UAT | Form marked offline-capable → AU lookup absent; manual `address` present. |
| Edge-case UAT | §11.2 toggles: manual fallback, delivery instructions, strict validation |

Document chosen flag name in `STORY-6.5d-CLOSEOUT-REPORT.md`.

---

## Credentials

Tony has a working GeoScape account in JobTrackerDB. For EventLeadPlatform local/Test:

- Add `GEOSCAPE_API_KEY` to backend `.env` (never commit).
- Azure Test: Key Vault / App Setting per 6.11 patterns when available.

---

## Related platform data

- `ref.Country.IntegrationConfig` JSON mentions `geoscapeApiUrl` — **update at implementation** if still pointing at deprecated host; runtime must use `api.psma.com.au`.
- Generic `address` component (global) remains offline-safe fallback.

---

*Handoff doc — Story 6.5d SM pack, 2026-05-21.*
