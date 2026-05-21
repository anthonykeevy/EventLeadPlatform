# Decision: External Data Feed Components (Network-Dependent)

**Status:** Draft v2 — **architect sign-off required before 6.5d Track A implementation**  
**Date:** 2026-05-21 (v2: unified proxy cache, multi-field delivery)  
**Drivers:** Story 6.5d — `address-lookup-au` + `company-lookup-abr` in one design pass  
**Reviewers:** Dimitri (data domain) + Winston (component framework) — Tony approves

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
| **Catalog metadata** | `ref.ComponentType.RequiresNetwork` (BIT, default 0) + optional `FallbackComponentCode` |
| **Form policy** | `Form.RequiresOfflineCapable` (BIT, default 0) — when 1, resolver excludes all `RequiresNetwork = 1` codes |
| **Unified proxy** | One **External Feed Proxy** layer: routes → provider client → **shared cache service** (same pattern as ABR) |
| **Caching** | Extend `cache` schema: existing `cache.ABRSearch`; add **`cache.AddressSearch`** (or `PSMAAddressSearch`) for GeoScape search + resolve payloads — **cost control same as ABR** |
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
        → ExternalFeedCacheService (generic or per-provider adapters)
        → cache.ABRSearch | cache.AddressSearch
        → external API (on cache miss only)
```

### 3.1 Reuse ABR cache pattern for address

| Concern | ABR (existing) | Address (6.5d — new) |
|---------|----------------|----------------------|
| Service | `backend/modules/companies/cache_service.py` | **Refactor or generalize** to `ExternalFeedCacheService` with provider=`abr` \| `geoscape` |
| Table | `cache.ABRSearch` | **`cache.AddressSearch`** (name TBD — Dimitri to confirm) |
| Cache key | `SearchType` + normalized `SearchValue` | e.g. `Search` (predictive query) + `Resolve` (PSMA address id) |
| TTL | `ABR_CACHE_TTL_DAYS` (default 30) | `GEOSCAPE_CACHE_TTL_DAYS` (default 30; confirm PSMA licence terms) |
| Hit tracking | `HitCount`, `LastHitAt` | Same — supports cost analytics |

**Decision:** Do **not** build a one-off GeoScape path without cache. First address search/resolve implementation **must** write through the same proxy+cache discipline as ABR.

**Optional refactor (6.5d):** Extract shared interface from `CacheService` so ABR and address share normalization, expiry, and hit-count logic; keep separate tables (different column shapes) unless Dimitri prefers a polymorphic `cache.ExternalFeed` JSON table.

### 3.2 Route namespace (revised draft)

Prefer **extending proven paths** over duplicating logic:

| Feed | Search | Resolve |
|------|--------|---------|
| ABR | Existing `companies/router` search (already cached) | Same + enrich for builder field map |
| Address AU | `GET /api/external-feed/address-au/search` | `POST /api/external-feed/address-au/resolve` |

Builder components call these routes; onboarding ABR continues using company routes (may share cache service internally).

---

## 4. Component instances (Story 6.5d)

| ComponentCode | Provider | Scope | Fallback | Cache table |
|---------------|----------|-------|----------|-------------|
| `address-lookup-au` | GeoScape/PSMA | AU Country | `address` | `cache.AddressSearch` (new) |
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
| **`decomposed`** (default) | Customer selects which output fields to expose; each maps to an **export name** (like existing export mapping) | Multiple submission columns |
| **`concatenated`** | Customer configures a **template** (e.g. `{{line1}}, {{suburb}} {{state}} {{postcode}}`) | Single export field |
| **`both`** | Store decomposed internally; export concatenated only (or vice versa — Dimitri to confirm CRM expectations) | Per form builder export settings |

**Properties panel (6.5d minimum):**

- `deliveryMode`: `decomposed` \| `concatenated` \| `both`
- `concatenationTemplate`: string (when concatenated or both)
- `enabledOutputFields`: string[] — subset of provider field catalog (when decomposed or both)

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

Provider-specific props remain in per-type schema.

---

## 7. Non-goals (6.5d)

- US/international address providers — future EDF instances.
- Public-form runtime without network — offline forms use **fallback** components only.
- Full CRM connector field mapping — export names only (same as today).

---

## 8. Documentation & agent gates

| Doc | Update |
|-----|--------|
| This file | **Approved** before Track A code |
| `COMPONENT-FRAMEWORK-GUIDE.md` / `REFERENCE.md` | EDF + delivery modes |
| `ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` | §0a EDF + cache + delivery |
| `cache-schema.md` | Document new address cache table |

---

## 9. Open questions (architect to close)

1. **RequiresNetwork column** on `ref.ComponentType` vs catalog JSON only?
2. **Offline flag** on `Form` vs publish/event setting?
3. **Cache table design:** dedicated `cache.AddressSearch` vs generic `cache.ExternalFeed` JSON blob?
4. **GeoScape TTL / licence** — max cache duration allowed by PSMA terms?
5. **`both` delivery mode** — export behaviour: one column or many + concatenated duplicate?
6. **Shared `ExternalFeedCacheService` refactor** — in 6.5d scope or follow-up housekeeping if timeboxed?

---

## 10. Acceptance (architecture phase done when)

- [ ] Tony + Dimitri + architect resolve §9.
- [ ] Framework + checklist updated (SM pack).
- [ ] Dev prompt: architecture gate **before** migrations.
- [ ] Tony confirms **chat/workflow** for 6.5d (see Epic 6 workflow — architecture chat separate from Dev implementation chat recommended).

---

*Draft v2 — Story 6.5d SM.*
