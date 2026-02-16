# Story 5.4: Resolution Rules — Defaults & Assets

**Story:** 5.4 - Shared Resolver Parity  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Created:** 2026-02-16  

---

## 1. Merge order (defaults resolution)

Resolution follows: **Global → Company → Form**.

| Layer | Source | Notes |
|-------|--------|-------|
| Global | `GlobalFormDefaults.DefaultsJSON` | Platform-wide defaults |
| Company | `CompanyFormDefaults.DefaultsJSON` | Company overrides, deep-merged over Global |
| Form | `form_definition.theme`, `.globalStyles`, `.canvasSettings` | Form-level overrides, deep-merged over merged defaults |

Each layer deep-merges over the previous. Nested objects are merged recursively; arrays and scalars are replaced.

---

## 2. Merge algorithm

**Backend:** `backend/modules/form_defaults/service.py`  
- `deep_merge(base, override)` — recursive dict merge  
- `resolve_merged_defaults(db, company_id)` — Global + Company  
- `resolve_definition_for_render(db, company_id, form_definition)` — merged defaults + form overrides  

**Frontend:** `frontend/src/features/builder/utils/definitionResolver.ts`  
- `deepMerge(base, override)` — recursive object merge  
- `resolveDefinitionForRender(defaults, formDefinition)` — defaults (from Init API) + form overrides  

**Parity:** Both implementations produce identical `theme`, `globalStyles`, and `canvasSettings` for the same inputs. Parity tests in `backend/tests/test_resolver_parity.py` enforce this.

### Behavior rules

- If form has a dict for theme/globalStyles/canvasSettings: merge over defaults.
- If form has null/undefined or missing key: use merged defaults for that section.
- If defaults is null (frontend): return form definition as-is.

---

## 3. Asset resolution

**Resolver:** `frontend/src/features/builder/utils/backgroundAssetResolver.ts`  
- `getBackgroundImageSource(background)` — returns content URL for assets, external URL for non-data URLs, null otherwise  
- `resolveAssetContentUrl(assetId)` — `{base}/api/assets/{assetId}/content`  

**Hook:** `frontend/src/features/builder/hooks/useBackgroundImageUrl.ts`  
- Fetches asset via `assetsApi.fetchAssetContentBlobUrl(assetId)` (auth-aware)  
- For external URLs: returns value as-is  
- For asset refs: returns blob URL after fetch; no fallback to content URL on failure (img src cannot send Authorization)

### Usage (shared path)

| Surface | Component | Hook/Resolver |
|---------|-----------|----------------|
| Builder preview | `FormBuilderCanvas` | `useBackgroundImageUrl(page?.background)` |
| Public renderer | `PublicFormArtboard` | `useBackgroundImageUrl(page?.background)` |

Both use the same path; no divergent logic.

---

## 4. Future Review and Publish (Story 5.6)

The future "Review and Publish" admin UI (Story 5.6) must use the same resolver contract:

- **Option A:** Use backend `resolve_definition_for_render` (e.g. via preview token endpoint)  
- **Option B:** Use verified frontend parity — `resolveDefinitionForRender` with initDefaults from a backend endpoint  

No new resolver logic; reuse existing backend or frontend implementation to ensure preview and production render identically.

---

## References

- Story 5.2: Form Builder Init API, resolver implementation
- Story 5.1: Asset upload, `backgroundAssetResolver`, `useBackgroundImageUrl`
- Parity tests: `backend/tests/test_resolver_parity.py`
- Fixtures: `backend/tests/fixtures/parity_fixtures.json`
