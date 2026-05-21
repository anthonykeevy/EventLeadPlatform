# Add a Component to the Platform — Checklist

**Owner:** Platform / Epic 6  
**Status:** Adopted with Story 6.5d (2026-05-21)  
**Audience:** Dev agents, Tony (UAT), SM (closeout audit)

After Story 6.5c, **the only authoritative list of buildable component types** is `dbo.FormBuilderComponent`, resolved at runtime by `resolve_allowed_components()` and exposed via `POST /api/form-builder/init`. A renderer in `ComponentRegistry.tsx` without a matching catalog row is a **ghost type** — the canvas may render it, but the toolbox, AI, and validator will not.

Use this checklist for **every** new or restored component type.

---

## 0. Decide scope (Global / Country / Company)

| Scope | When to use | Example |
|-------|-------------|---------|
| **Global** | Available in all markets | `text`, `rating` |
| **Country** | Market-specific capability | `address-lookup-au` (AU only) |
| **Company** | Tenant-specific override | Rare; same pattern as Global |

---

## 1. Reference data (`ref.ComponentType`)

- [ ] Row exists in `ref.ComponentType` with `ComponentTypeCode` = canonical `ComponentCode` (kebab-case, stable).
- [ ] `IsActive = 1`, correct `Category` for toolbox grouping.

---

## 2. Catalog row (`dbo.FormBuilderComponent`)

- [ ] Migration seeds `FormBuilderComponent` with correct `ComponentScopeID` + `CountryID` / `CompanyID` as required.
- [ ] `PropertiesSchemaJSON`, `StructureJSON`, `DefaultGridLayoutVerticalJSON`, `DefaultGridLayoutHorizontalJSON` populated (copy pattern from migration 039 or sibling component).
- [ ] `SortOrder` set; `IsActive = 1`, `IsDeleted = 0`.
- [ ] **Downgrade** documented in migration docstring.

---

## 3. Frontend renderer (`ComponentRegistry.tsx`)

- [ ] `ComponentDefinition` exists for the `ComponentCode` (must match DB code exactly).
- [ ] `previewComponent` + `runtimeComponent` implemented (or explicitly delegated).
- [ ] `ComponentType` union in `builder.types.ts` includes the code (if still used for typing).
- [ ] Toolbox uses **init payload only** (Story 6.5c) — no static palette entry that bypasses init.

---

## 4. Four-consumer alignment (mandatory after 6.5c)

Run (or extend) the catalog alignment check for a fixture `company_id` + `country_id`:

- [ ] `POST /api/form-builder/init` → `components[].componentCode` includes the new code when scope applies.
- [ ] `resolve_allowed_components()` returns the same code.
- [ ] Form AI Block F / A / I ALLOWED list includes the code (generate or unit test).
- [ ] Semantic validator accepts the code; rejects unknown codes.

Story 6.5d delivers `backend/scripts/verify_component_catalog_alignment.py` — register in `docs/stories/EPIC-6-SM-TOOLS-REGISTRY.md`.

---

## 5. Compiler / validation / export (if applicable)

- [ ] `componentCapabilities.ts` / `validationEngine.ts` / `collisionDetection.ts` heights updated if new surface type.
- [ ] `ComponentValidationContract` row if semantic validation rules apply.
- [ ] Export mapping if decomposed fields (e.g. address lines).

---

## 6. Prompt / context prose

- [ ] Block G (`STORY-6.2-AI-CONTEXT-PACK` / registry FEW_SHOT variant) mentions the type **only if** it is in the catalog for the target market.
- [ ] Do not document types in prose that are not seeded — causes AI to emit `unknown-component-type`.

---

## 7. Tests

- [ ] Migration static test lists new revision.
- [ ] Unit test: resolver returns new code for intended scope.
- [ ] Unit test: code **absent** when country scope does not match (for Country-scoped rows).
- [ ] Alignment script passes for AU (and non-AU negative case if Country-scoped).

---

## 8. UAT (Tony)

- [ ] LocalDB: `alembic upgrade head`, reload builder, confirm toolbox shows component.
- [ ] AI generate a form that should use the component; no `unknown-component-type`.
- [ ] Azure Test after merge to `develop`.

---

## 9. SM closeout

- [ ] Closeout report lists new `ComponentCode`(s) and migration IDs.
- [ ] `EPIC-6-SM-TOOLS-REGISTRY.md` updated if new automation added.
- [ ] Carry-forward backlog updated (remove resolved catalog-gap items).

---

## AU online address (`address-lookup-au`) — Story 6.5d reference implementation

This story uses this checklist end-to-end for:

- **Country-scoped** row `address-lookup-au` (AU `CountryID` only).
- Wired autocomplete behaviour per existing `address` renderer + AU provider config (Dev to confirm provider/env vars).
- Proves Country ∪ Global catalog pattern from architecture §2.3.

---

*Process version 1.0 — Story 6.5d.*
