# Decision: External Data Feed Components (Network-Dependent)



**Status:** **Approved** (Dimitri sign-off 2026-05-21; Tony approval pending UAT only)  

**Date:** 2026-05-21 (v2: unified proxy cache, multi-field delivery; §9 resolved)  

**Drivers:** Story 6.5d — `address-lookup-au` + `company-lookup-abr` in one design pass  

**Reviewers:** Dimitri (data domain) ✅ + Winston (component framework) — Tony approves



---



## 1. Problem



We are adding the first builder components that **call third-party APIs at runtime** (GeoScape/PSMA, ABR). Customers may require forms to **run offline** (event lead capture). Today:



- `COMPONENT-FRAMEWORK-REFERENCE.md` / `COMPONENT-FRAMEWORK-GUIDE.md` describe **rendering** only.

- Story 6.5c made **`dbo.FormBuilderComponent` + `resolve_allowed_components()`** authoritative for toolbox, AI, and validator.

- Story 6.2.x added renderers (`rating`, `url`, etc.) **without** catalog seeds → ghost types until 6.5d.



We need one **repeatable pattern** for current and future feed components (payments, SMS verify, etc.).



**Unlike most components** (single value → one export field), EDF components return **multiple structured fields** after resolve. Customers need a **delivery mode**: one concatenated field vs separate mapped fields.



---



## 2. Decision summary



| Layer | Pattern |

|-------|---------|

| **Taxonomy** | New component class: **External Data Feed** (EDF) — subtype of input components with live lookup |

| **Catalog metadata** | `ref.ComponentType.RequiresNetwork` (BIT, default 0) + `FallbackComponentCode` (NVARCHAR(50), nullable) |

| **Form policy** | `Form.RequiresOfflineCapable` (BIT, default 0) — when 1, resolver excludes all `RequiresNetwork = 1` codes |

| **Unified proxy** | One **External Feed Proxy** layer: routes → provider client → **shared cache service** (same pattern as ABR) |

| **Caching** | Extend `cache` schema: existing `cache.ABRSearch`; add **`cache.AddressSearch`** for GeoScape search + resolve payloads — **cost control same as ABR** |

| **Init payload** | `requiresNetwork`, `fallbackComponentCode`, EDF field catalog for properties panel |

| **UI indication** | Toolbox + properties: “Online lookup” when `requiresNetwork` |

| **AI / validator** | Same filter as init — four-consumer alignment (6.5c contract) |

| **Submission** | Structured multi-field payload + optional concatenated export per **delivery mode** (§5) |



---



## 3. Unified External Feed Proxy (Tony requirement)



**Principle:** Browser never calls GeoScape or ABR directly. All EDF traffic goes through platform routes that use the **same architectural pattern** as onboarding ABR:



```

Frontend (builder/runtime)

    → External Feed Proxy routes (form-builder or /api/external-feed/*)

        → Provider client (abr_client | geoscape_client)

        → ExternalFeedCacheService (shared helpers + per-provider adapters)

        → cache.ABRSearch | cache.AddressSearch

        → external API (on cache miss only)

```



### 3.1 Reuse ABR cache pattern for address



| Concern | ABR (existing) | Address (6.5d — new) |

|---------|----------------|----------------------|

| Service | `backend/modules/companies/cache_service.py` | `AddressCacheService` in `backend/modules/external_feed/` sharing **`cache_base.py` helpers** |

| Table | `cache.ABRSearch` | **`cache.AddressSearch`** |

| Cache key | `SearchType` + normalized `SearchValue` | `OperationType` (`Search` \| `Resolve`) + normalized key (query string or `psmaAddressId`) |

| TTL | `ABR_CACHE_TTL_DAYS` (default 30) | `GEOSCAPE_CACHE_TTL_SEARCH_DAYS` (default **1**) + `GEOSCAPE_CACHE_TTL_RESOLVE_DAYS` (default **30**) — see §9.4 |

| Hit tracking | `HitCount`, `LastHitAt` | Same — supports cost analytics |



**Decision:** Do **not** build a one-off GeoScape path without cache. First address search/resolve implementation **must** write through the same proxy+cache discipline as ABR.



**Refactor scope (6.5d):** Extract shared helpers (`normalize_key`, `calculate_expiry`, hit-count update, soft-delete cleanup) into `backend/modules/external_feed/cache_base.py`. New `AddressCacheService` uses them. Existing ABR `CacheService` **unchanged** in 6.5d (follow-up PR may inherit base — avoids onboarding regression).



### 3.2 Route namespace



Prefer **extending proven paths** over duplicating logic:



| Feed | Search | Resolve |

|------|--------|---------|

| ABR | Existing `companies/router` search (already cached) | Same + enrich for builder field map |

| Address AU | `GET /api/external-feed/address-au/search?q=&limit=` | `POST /api/external-feed/address-au/resolve` `{ "psmaAddressId": "..." }` |



Builder components call these routes; onboarding ABR continues using company routes (may share cache service internally).



**Auth:** Builder/runtime routes require authenticated session or public-form token consistent with existing form-builder security; never expose provider API keys to the browser.



---



## 4. Component instances (Story 6.5d)



| ComponentCode | Provider | Scope | Fallback | Cache table |

|---------------|----------|-------|----------|-------------|

| `address-lookup-au` | GeoScape/PSMA | AU Country | `address` | `cache.AddressSearch` |

| `company-lookup-abr` | ABR | AU Country | manual / `text` | `cache.ABRSearch` (existing) |



Both **must** ship in 6.5d Track A so EDF pattern is proven twice (proxy + cache + multi-field delivery).



**Handoffs:** `au-address-lookup-geoscape-handoff.md`, `abr-company-lookup-builder-handoff.md`



---



## 5. Multi-field output & customer delivery modes (Tony requirement)



EDF resolve returns a **field bundle**, not a single string.



### 5.1 Canonical resolved shapes (server)



**Address (`address-lookup-au`)** — example fields:



| Field key | Example |

|-----------|---------|

| `line1`, `line2`, `suburb`, `state`, `postcode` | Structured lines |

| `formattedAddress` | Single display line |

| `psmaAddressId` | Provider ref (when `storeProviderRef`) |



**Company (`company-lookup-abr`)** — align with onboarding / `CompanySearchResult`:



| Field key | Example |

|-----------|---------|

| `legalEntityName`, `abn`, `acn`, `entityType`, `abnStatus`, `gstRegistered` | |



Stored in component props / submission as **`resolvedFields`** object, not one opaque string.



### 5.2 Builder property: `deliveryMode`



| Mode | Behaviour | Export / integration |

|------|-----------|----------------------|

| **`decomposed`** (default) | Customer selects which output fields to expose; each maps to an **export name** (like existing `addressExportMapping`) | Multiple submission/export columns |

| **`concatenated`** | Customer configures a **template** (e.g. `{{line1}}, {{suburb}} {{state}} {{postcode}}`) | Single export column (`exportName` on component) |

| **`both`** | Store full `resolvedFields` internally; export emits **decomposed columns (per `enabledOutputFields` / field map) plus one concatenated column** | Multi-column + `{exportName}_formatted` (or customer alias) |



**`both` contract (locked):**



- **Submission JSON (always):** `{ resolvedFields, concatenatedValue, deliveryMode, psmaAddressId? | abn? }` — full fidelity for replay/audit.

- **CSV/export schema (`both`):** One row per lead with **N decomposed columns** (from `outputFieldExportMap`) **and** one additional concatenated column. No duplicate decomposed columns.

- **Default concatenated export alias:** `{baseExportName}_formatted` where `baseExportName` is the component’s primary `exportName`.

- Aligns with existing `ExportMode` (`multi-column` / `single-value`): `decomposed` → `multi-column`; `concatenated` → `single-value`; `both` → `multi-column` + extra single-value column.



**Properties panel (6.5d minimum):**



- `deliveryMode`: `decomposed` \| `concatenated` \| `both`

- `concatenationTemplate`: string (when concatenated or both)

- `enabledOutputFields`: string[] — subset of provider field catalog (when decomposed or both)

- `outputFieldExportMap`: `Record<fieldKey, exportName>` — per-field export aliases (decomposed / both)



**Runtime:** After user selects a suggestion, UI shows resolved preview; submission uses chosen delivery shape.



**AI / compiler:** Semantic plan may reference EDF components only when catalog includes them; AI should prefer decomposed field list in prompt when `deliveryMode` is decomposed (Block G update in 6.5d).



### 5.3 Contrast with simple components



| Simple (`text`, `email`) | EDF (`address-lookup-au`, `company-lookup-abr`) |

|--------------------------|--------------------------------------------------|

| `value: string` | `resolvedFields: Record<string, unknown>` + optional `displayValue` / `concatenatedValue` |

| One export name | One or many export names per `deliveryMode` |



---



## 6. PropertiesSchemaJSON (builder + runtime)



Shared EDF props:



| Prop | Type | Purpose |

|------|------|---------|

| `feedProvider` | string | `geoscape` \| `abr` |

| `debounceMs` | number | Default 300 |

| `minQueryLength` | number | Default 3 |

| `storeProviderRef` | boolean | Default true |

| **`deliveryMode`** | enum | `decomposed` \| `concatenated` \| `both` |

| **`concatenationTemplate`** | string | Required when mode includes concatenated |

| **`enabledOutputFields`** | string[] | Subset of provider field catalog |

| **`outputFieldExportMap`** | object | Field key → export column name |



Provider-specific props remain in per-type schema. **Edge-case UX toggles** (manual fallback, delivery instructions, trading-as, etc.) are defined per component in **§11** — form designers control enforcement via the Properties Panel; Dev must wire each toggle to runtime + validation.

---

## 7. Non-goals (6.5d)



- US/international address providers — future EDF instances.

- Public-form runtime without network — offline forms use **fallback** components only.

- Full CRM connector field mapping — export names only (same as today).

- Event-level offline override — deferred; form design flag is authoritative for 6.5d.



---



## 8. Documentation & agent gates



| Doc | Update |

|-----|--------|

| This file | ✅ Approved — Track A code may proceed |

| `COMPONENT-FRAMEWORK-GUIDE.md` / `REFERENCE.md` | EDF + delivery modes (already drafted) |

| `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` | §0a EDF + cache + delivery |

| `cache-schema.md` | Document `cache.AddressSearch` |

| Handoffs | Route paths + flag names aligned; **§11 edge-case toggles** |

---

## 9. Resolved open questions (2026-05-21 — Dimitri)

|---|----------|----------|-----------|

| **9.1** | `RequiresNetwork` on `ref.ComponentType` vs catalog JSON only? | **`ref.ComponentType` columns:** `RequiresNetwork BIT NOT NULL DEFAULT 0`, `FallbackComponentCode NVARCHAR(50) NULL`. Init payload derives from JOIN (not duplicated in `PropertiesSchemaJSON`). | Resolver already JOINs `ref.ComponentType`; SQL filter keeps four-consumer alignment without parsing JSON per row. Type-level flag is stable across Global/Country/Company catalog rows sharing the same type. |

| **9.2** | Offline flag: `Form.RequiresOfflineCapable` vs publish/event-level? | **`dbo.Form.RequiresOfflineCapable BIT NOT NULL DEFAULT 0`.** Event/publish settings do **not** drive EDF exclusion in 6.5d. | Offline is a **form design constraint** (which components belong in toolbox/AI/validator). Event deployment may vary, but the form definition must be buildable without network-dependent types when this flag is set. Extend `resolve_allowed_components(..., requires_offline_capable: bool)` and init API to pass form context. |

| **9.3** | Dedicated `cache.AddressSearch` vs generic `cache.ExternalFeed` JSON? | **Dedicated `cache.AddressSearch`** mirroring `cache.ABRSearch` shape. | Typed columns + `FullResponse` JSON matches proven ABR pattern, supports hit analytics and indexed lookups. Generic blob table loses provider-specific indexes and forces JSON parsing on every read. |

| **9.4** | GeoScape TTL vs licence terms | **Split TTL by operation:** `GEOSCAPE_CACHE_TTL_SEARCH_DAYS=1` (predictive), `GEOSCAPE_CACHE_TTL_RESOLVE_DAYS=30` (stable `psmaAddressId` → lines). **Client/browser must never cache** API responses (GeoScape Developer Terms §9). Server-side cache is internal cost-control only — Tony to confirm against subscription/API-specific terms before production scale. | Predictive search is high-churn and licence-sensitive; resolve-by-id is stable like ABR entity lookup. ABR remains 30 days (`ABR_CACHE_TTL_DAYS`). |

| **9.5** | `deliveryMode = both` — export shape | **Submission:** full `resolvedFields` + `concatenatedValue`. **Export:** decomposed columns per `outputFieldExportMap` **plus** one concatenated column (`{exportName}_formatted` default). | Matches CRM expectations (structured fields for mapping + one human-readable line for reps). Avoids duplicating every decomposed field twice. |

| **9.6** | `ExternalFeedCacheService` refactor in 6.5d vs follow-up | **6.5d:** shared `cache_base.py` helpers + new `AddressCacheService`. **Follow-up:** migrate ABR `CacheService` to inherit same base. | Delivers address cache without risking onboarding ABR regression. Pattern is established for future EDF providers. |



### 9.7 Schema deltas (migration preview)



**`ref.ComponentType`** (alter):



```sql

RequiresNetwork BIT NOT NULL CONSTRAINT DF_ComponentType_RequiresNetwork DEFAULT 0,

FallbackComponentCode NVARCHAR(50) NULL

-- Seed: address-lookup-au → RequiresNetwork=1, FallbackComponentCode='address'

-- Seed: company-lookup-abr → RequiresNetwork=1, FallbackComponentCode='text'

```



**`dbo.Form`** (alter):



```sql

RequiresOfflineCapable BIT NOT NULL CONSTRAINT DF_Form_RequiresOfflineCapable DEFAULT 0

```



**`cache.AddressSearch`** (new — mirror ABR analytics columns):



| Column | Type | Notes |

|--------|------|-------|

| `OperationType` | NVARCHAR(20) PK | `Search` \| `Resolve` |

| `CacheKey` | NVARCHAR(255) PK | Normalized query or `psmaAddressId` |

| `ResultIndex` | INT PK | Default 0 (multi-match search) |

| `Line1`, `Line2`, `Suburb`, `State`, `Postcode` | NVARCHAR | Extracted resolve fields |

| `FormattedAddress` | NVARCHAR(500) | Display line |

| `PsmaAddressId` | NVARCHAR(100) | Provider ref |

| `FullResponse` | NVARCHAR(MAX) | Complete API JSON |

| `SearchDate`, `ExpiresAt` | DATETIME2 | UTC |

| `HitCount`, `LastHitAt` | INT / DATETIME2 | Analytics |

| `IsDeleted` | BIT | Soft delete |

| Audit / context | BIGINT nullable | `CreatedBy`, `UserID`, `CompanyID` optional |



**Resolver filter (pseudo):**



```sql

-- When @RequiresOfflineCapable = 1:

AND ct.RequiresNetwork = 0

```

---

## 11. Edge-case UX & Properties Panel toggles (Dev contract)

**Principle:** The **form designer** controls lookup strictness and optional fields via **Properties Panel switches** on each EDF component instance. Props live in `DefinitionJSON` / `PropertiesSchemaJSON`; runtime and submit validation **must honour them**. Do not hardcode enforcement — read props from the component instance.

**Reuse:** Onboarding implements ABR no-results / API-error → manual entry (`SmartCompanySearch.tsx`, `OnboardingStep2.tsx`). Port into `company-lookup-abr`; mirror the same escape-hatch pattern for `address-lookup-au`.

### 11.1 Properties Panel layout (both EDF types)

| Panel section | Contents |
|---------------|----------|
| **Lookup** | Debounce, min query length, auto-select single result (company only) |
| **Delivery & export** | `deliveryMode`, templates, export maps (§5) |
| **Fallback & validation** | Manual override allow/require, validated-only modes |
| **Extra fields** | Delivery instructions, unit/line2, trading-as |
| **Advanced** | Store provider ref, editable-after-resolve, inactive-ABN rules |

When a toggle is **off**, hide dependent controls (e.g. `requireDeliveryInstructions` only when `allowDeliveryInstructions = true`).

**Designer conflict rules (enforce in Properties Panel UI):**

| If designer sets… | Then… |
|-------------------|--------|
| `requireValidatedAddress = true` | Disable or warn on `allowManualFallback = true` (mutually exclusive strict modes) |
| `blockOnInactiveAbn = true` | Warn if `allowManualFallback = true` (manual bypasses ABN status) |
| `allowDeliveryInstructions = false` | Hide `requireDeliveryInstructions` and label/export overrides |

---

### 11.2 `address-lookup-au` — toggles

| Prop | Type | Default | Properties Panel label | Runtime when **ON** | Runtime when **OFF** | Validation |
|------|------|---------|------------------------|---------------------|----------------------|------------|
| **`allowManualFallback`** | boolean | `true` | Allow manual address entry | Show *“Can’t find your address? Enter manually”*; inline manual fields (`line1`, `line2`, `suburb`, `state`, `postcode`); `validationSource: 'manual'` | Lookup-only; no manual link | If OFF, respondent must pick a PSMA suggestion (or leave empty if field optional) |
| **`requireValidatedAddress`** | boolean | `false` | Require validated address (PSMA) | Submit blocked unless `psmaAddressId` present | Manual entry allowed without `psmaAddressId` when `allowManualFallback` ON | If ON, designer should turn OFF manual fallback (see conflict rules) |
| **`editableAfterResolve`** | boolean | `true` | Allow editing after autocomplete | Resolved lines editable after pick | Read-only after pick | Set `addressModifiedAfterResolve: true` if user edits post-resolve |
| **`showUnitField`** | boolean | `true` | Show unit / address line 2 | Show `line2` after resolve and in manual mode | Hide `line2` field | Unit often absent from authority data — always user-editable when shown |
| **`allowDeliveryInstructions`** | boolean | `false` | Show delivery instructions field | Optional textarea below address (not sent to GeoScape) | Field hidden | Independent of PSMA |
| **`requireDeliveryInstructions`** | boolean | `false` | Require delivery instructions | Required when field visible | N/A | Panel: only when `allowDeliveryInstructions=true` |
| **`deliveryInstructionsLabel`** | string | `"Delivery instructions"` | Delivery instructions label | Runtime + panel label | — | — |
| **`deliveryInstructionsExportName`** | string | `"{exportName}_instructions"` | Export name for instructions | CSV/export column name | — | Default from component `exportName` |
| **`showPoBoxHelperText`** | boolean | `true` | Show PO Box / parcel locker hint | No-results hint for PO Box / locker → use manual | No extra hint | Only when `allowManualFallback=true` |

**No-results / error UX:** Yellow panel (no results) or red panel (API error) + manual link when `allowManualFallback`. Copy pattern from `SmartCompanySearch`.

**Submission metadata (always):**

```json
{
  "validationSource": "geoscape | manual",
  "psmaAddressId": "... | null",
  "addressModifiedAfterResolve": false,
  "resolvedFields": { "line1", "line2", "suburb", "state", "postcode", "formattedAddress" },
  "deliveryInstructions": "... | null"
}
```

---

### 11.3 `company-lookup-abr` — toggles

| Prop | Type | Default | Properties Panel label | Runtime when **ON** | Runtime when **OFF** | Validation |
|------|------|---------|------------------------|---------------------|----------------------|------------|
| **`allowManualFallback`** | boolean | `true` | Allow manual company entry | *“Can’t find your company? Enter manually”*; `companyName` + optional `abn`; `validationSource: 'manual'` | ABR lookup only | Port onboarding UX |
| **`requireAbn`** | boolean | `false` | Require ABN on submission | 11-digit ABN required (ABR or manual) | ABN optional | Manual: format + checksum only; no fake “verified” badge |
| **`requireAbnWhenManual`** | boolean | `false` | Require ABN when entering manually | Manual path requires ABN field | Manual without ABN OK | Panel: only when `allowManualFallback=true` |
| **`autoSelectSingleResult`** | boolean | `true` | Auto-select single search result | One hit → auto-fill | Always show result list | Matches `SmartCompanySearch` |
| **`allowTradingAs`** | boolean | `true` | Show “Trading as” field | Optional text after select/manual; exports as `tradingAs` | Hidden | Captures display ≠ legal entity name |
| **`tradingAsLabel`** | string | `"Trading as (optional)"` | Trading as label | Runtime label | — | — |
| **`tradingAsExportName`** | string | `"{exportName}_tradingAs"` | Export name for trading as | Export column | — | — |
| **`showBusinessNamesInResults`** | boolean | `true` | Show business names in results | Cards show legal + matched business name subtitle | Legal name only | Backend: return `businessNames[]`, `matchedName` when available |
| **`editableLegalNameAfterResolve`** | boolean | `false` | Allow editing legal name after lookup | `legalEntityName` editable post-select | Read-only after ABR select | Set `legalNameModifiedAfterResolve: true` if edited |
| **`warnOnInactiveAbn`** | boolean | `true` | Warn when ABN is not Active | Yellow banner for Cancelled/Inactive | No warning | Submit still allowed unless `blockOnInactiveAbn` |
| **`blockOnInactiveAbn`** | boolean | `false` | Block submission for inactive ABN | Submit blocked when status ≠ Active | Inactive allowed | Warn designer if combined with `allowManualFallback` |

**Submission metadata (always):**

```json
{
  "validationSource": "abr | manual",
  "matchType": "legal | business_name | trading_name | abn | acn | manual",
  "legalEntityName": "...",
  "tradingAs": "... | null",
  "abn": "... | null",
  "legalNameModifiedAfterResolve": false,
  "resolvedFields": { "legalEntityName", "abn", "acn", "entityType", "abnStatus", "gstRegistered" }
}
```

---

### 11.4 Designer default presets (catalog `PropertiesSchemaJSON` defaults)

| Use case | Component | Notable defaults |
|----------|-----------|------------------|
| Event lead capture | `address-lookup-au` | `allowManualFallback=true`, `allowDeliveryInstructions=false`, `editableAfterResolve=true` |
| Mail / sample fulfilment | `address-lookup-au` | `requireValidatedAddress=true`, `allowManualFallback=false`, `allowDeliveryInstructions=true` |
| Company lead (standard) | `company-lookup-abr` | `allowManualFallback=true`, `allowTradingAs=true`, `requireAbn=false` |
| B2B qualified lead | `company-lookup-abr` | `requireAbn=true`, `blockOnInactiveAbn=true`, `allowManualFallback=false` |

Designers override any default per instance in the Properties Panel.

---

### 11.5 Dev checklist (edge cases)

- [ ] All §11.2 / §11.3 props in `PropertiesSchemaJSON` with `default`, `title`, `description`.
- [ ] Panel binds toggles; dependent controls hidden per §11.1 conflict rules.
- [ ] Runtime + submit validator read instance props (not constants).
- [ ] Export schema includes `deliveryInstructions` / `tradingAs` columns only when parent `allow*` is true.
- [ ] Submission includes `validationSource` (+ `matchType` for company).
- [ ] UAT: each critical toggle ON/OFF × no-results / API-error / happy path.

---

## 10. Acceptance (architecture phase)



- [x] Tony + Dimitri + architect resolve §9.

- [x] Framework + checklist reference approved decision (SM pack).

- [x] Dev prompt: architecture gate **before** migrations.
- [x] §11 edge-case Properties Panel toggles documented for Dev.
- [ ] Tony confirms **chat/workflow** for 6.5d implementation (separate Dev chat).



---



*Approved v2 — Story 6.5d SM / Dimitri (Data Domain Architect).*

