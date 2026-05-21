# Decision: External Data Feed Components (Network-Dependent)

**Status:** Draft — **architect sign-off required before 6.5d Track A implementation**  
**Date:** 2026-05-21  
**Drivers:** Story 6.5d — `address-lookup-au` + `company-lookup-abr` in one design pass  
**Reviewers:** Dimitri (data domain) + Winston (component framework) — Tony approves

---

## 1. Problem

We are adding the first builder components that **call third-party APIs at runtime** (GeoScape/PSMA, ABR). Customers may require forms to **run offline** (event lead capture). Today:

- `COMPONENT-FRAMEWORK-REFERENCE.md` / `COMPONENT-FRAMEWORK-GUIDE.md` describe **rendering** only.
- Story 6.5c made **`dbo.FormBuilderComponent` + `resolve_allowed_components()`** authoritative for toolbox, AI, and validator.
- Story 6.2.x added renderers (`rating`, `url`, etc.) **without** catalog seeds → ghost types until 6.5d.

We need one **repeatable pattern** for current and future feed components (payments, SMS verify, etc.).

---

## 2. Decision summary

| Layer | Pattern |
|-------|---------|
| **Taxonomy** | New component class: **External Data Feed** (EDF) — subtype of input components with live lookup |
| **Catalog metadata** | `ref.ComponentType.RequiresNetwork` (BIT, default 0) + optional `FallbackComponentCode` (e.g. `address-lookup-au` → `address`) |
| **Form policy** | `Form.RequiresOfflineCapable` (BIT, default 0) — when 1, resolver excludes all `RequiresNetwork = 1` codes |
| **Backend proxy** | Platform-owned routes only (no browser → third party). Reuse provider modules (`address_lookup_au`, extend `companies` ABR). |
| **Init payload** | Expose `requiresNetwork: boolean` and `fallbackComponentCode?: string` per component in `POST /api/form-builder/init` |
| **UI indication** | Toolbox + properties: badge/icon “Online lookup” when `requiresNetwork` |
| **AI / validator** | Same filter as init — four-consumer alignment (6.5c contract) |
| **DefinitionJSON** | Store **resolved structured fields** + provider reference ids (PSMA id, ABN), not raw API payloads |

---

## 3. Component instances (Story 6.5d)

| ComponentCode | Provider | Scope | Fallback | Backend reuse |
|---------------|----------|-------|----------|---------------|
| `address-lookup-au` | GeoScape/PSMA | AU Country | `address` | New thin module; see `au-address-lookup-geoscape-handoff.md` |
| `company-lookup-abr` | ABR | AU Country | manual company fields or `text` blocks | `abr_client.py` + `companies/router.py` |

Both **must** ship in 6.5d Track A so the EDF pattern is proven twice.

---

## 4. API shape (platform proxy — draft)

```
GET  /api/external-feed/address-au/search?q=&limit=
POST /api/external-feed/address-au/resolve   { psmaId | selectedSuggestion }
GET  /api/external-feed/company-abr/search?q=&type=abn|acn|name
POST /api/external-feed/company-abr/resolve  { abn | selectedEntity }
```

Exact paths may align with existing `/api/companies/...` ABR routes — architect confirms **one namespace** vs split.

---

## 5. PropertiesSchemaJSON (builder + runtime)

Shared EDF props (in addition to label/validation):

| Prop | Type | Purpose |
|------|------|---------|
| `feedProvider` | string | `geoscape` \| `abr` (telemetry, support) |
| `debounceMs` | number | Autocomplete throttle (default 300) |
| `minQueryLength` | number | Default 3 |
| `storeProviderRef` | boolean | Persist provider id on submit (default true) |

Component-specific props remain in per-type schema (e.g. decompose address lines).

---

## 6. Non-goals (6.5d)

- US/international address providers (SmartyStreets etc.) — future EDF instances.
- Caching policy beyond existing `cache.ABRSearch` pattern — extend similarly if needed.
- Public-form runtime without network — offline forms use **fallback** components only.

---

## 7. Documentation & agent gates (mandatory)

| Doc | Update |
|-----|--------|
| `docs/architecture/decision-external-data-feed-components.md` | This file — **approved** before Dev codes Track A |
| `docs/COMPONENT-FRAMEWORK-GUIDE.md` | § External Data Feed + **read order** |
| `docs/COMPONENT-FRAMEWORK-REFERENCE.md` | § External Data Feed (platform + UI) |
| `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` | § EDF + links |
| `docs/stories/story-6.5d.md` | ACs reference this decision |

---

## 8. Open questions (architect to close)

1. **Column placement:** `RequiresNetwork` on `ref.ComponentType` vs JSON in `FormBuilderComponent.PropertiesSchemaJSON` only?
2. **Offline flag:** `Form.RequiresOfflineCapable` vs publish-setting / event-level flag?
3. **ABR route reuse:** Wrap existing company search endpoints vs new `external-feed` router?
4. **Submission shape:** Standard EDF answer envelope in `DefinitionJSON` / submission API?

---

## 9. Acceptance (architecture phase done when)

- [ ] Tony + architect comment on §8 resolved.
- [ ] Framework GUIDE + REFERENCE sections merged.
- [ ] Checklist § EDF present.
- [ ] Dev prompt lists this file in Read First **before** migrations.

---

*Draft for architect review — Story 6.5d SM.*
