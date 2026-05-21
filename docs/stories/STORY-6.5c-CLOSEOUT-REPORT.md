# Story 6.5c — Closeout Report



**Story:** 6.5c — Capability Catalog Cutover  

**Date:** 2026-05-20  

**Status:** LocalDB UAT **Pass** (§1–§6); Azure Test §7 pending post-merge. Implementation on branch; commit/push pending.  

**PR:** [#106](https://github.com/anthonykeevy/EventLeadPlatform/pull/106) — Draft → `develop`



---



## 1. Story outcome



Story 6.5c makes **`resolve_allowed_components(db, company_id, country_id)`** the single source of truth for which component types exist, wired into four consumers:



1. Form Builder init / toolbox (`POST /api/form-builder/init`)

2. Form AI Block F (registry `COMPONENT_CAPABILITY` / `DynamicComponentCatalog`)

3. Form AI Blocks A / I (allowed `componentType` fragments)

4. Semantic validator (same resolved set)



Additionally: **`ref.BrandPosture`** + `Company.BrandPostureID` FK; Block C variant selection via registry resolver; frontend toolbox init-only.



**Key achievement:** Toolbox, init API, AI ALLOWED types, and validator all agree for the same company + country context. Country scope proven in UAT (divider AU-only probe). Brand posture proven via API (runs 168/169).



---



## 2. Evidence summary



| Artefact | Path | Result |

|----------|------|--------|

| Preflight | `STORY-6.5c-PREFLIGHT.md` | PASS |

| Migrations | `084`–`086` | Tony applied LocalDB (see gate evidence) |

| Focused pytest | 6.5c + 6.5b regression | **35/35 PASS** |

| AC-15 alignment | `test_story_6_5c_catalog_alignment.py` | PASS |

| Gate evidence | `STORY-6.5c-GATE-EVIDENCE.md` | Complete |

| UAT | `STORY-6.5c-UAT-TEST-GUIDE.md` | §1–§6 **Pass**; §7 pending |



---



## 3. Catalog drift — snapshot vs `FormBuilderComponent` (follow-up)



Story 6.5c correctly retires **`ComponentCapabilitySnapshot`** as the runtime allowed-type source. The authoritative catalog is **`dbo.FormBuilderComponent`** (migration 039 seeds **14 global MVP rows**).



**Gap:** Several types referenced in historical **`config.ComponentCapabilitySnapshot`** JSON and Block G context-pack prose (e.g. `rating`, `address`, `url`, `file-upload`, `paragraph`, `last-name`) were **never seeded** into `FormBuilderComponent`. They therefore:



- Do **not** appear in the Form Builder toolbox (init `components[]`)

- Are **not** in the AI ALLOWED list or semantic validator set after 6.5c cutover

- May still exist in the frontend **renderer** (canvas can display them if manually placed) but are unreachable from the palette



This is **not a 6.5c regression** — it exposes pre-existing misalignment between snapshot/context-pack vocabulary and the builder catalog table. UAT attempted to use `rating` for country-scope testing; UPDATE affected 0 rows because no `rating` row exists.



**Recommendation (post-6.5c / tech debt):** Either seed missing types into `FormBuilderComponent` (with appropriate `ref.ComponentType` rows) or formally deprecate them from snapshot/context-pack docs. Until then, country-scope UAT must use an **existing** catalog code (e.g. `divider`).



---



## 4. Implementation decisions



- **`ComponentCapabilitySnapshotID` on new runs:** Still populated when an active snapshot row exists (audit backward-compat); generation/validator use resolver JSON + `resolvedComponentCatalogHash` in governance payload.

- **`PromptAssemblyRegistry*` vs `PromptAssemblyProfile*` naming:** Deferred; document-only reconciliation (same as 6.5b closeout).

- **Frontend brand posture picker:** Still hardcoded enum in `aiFormGenerationApi.ts`; backend resolves via `ref.BrandPosture` — API path validated in UAT §5.

- **Block F assembly order:** Content from registry section F; insertion point in `_build_initial_messages` unchanged (between I and G) for byte-equivalence with 6.5b.



---



## 5. Tony / UAT record



| Section | Result | Notes |

|---------|--------|-------|

| §1 Migrations | Pass | 084–086; `ref.BrandPosture` four codes |

| §2 Toolbox ↔ init | Pass | Init-only palette |

| §3 AI ↔ toolbox | Pass | Forms 504/813 |

| §4 Country scope | Pass | Divider Country/AU; reverted |

| §5 Brand posture | Pass | API runs 168/169 |

| §6 Automated gates | Pass | 35/35 focused pytest |

| §7 Azure Test | Pending | After merge + deploy |



---



## 6. Risks & mitigations



| Risk | Mitigation |

|------|------------|

| Missing catalog rows (`rating`, etc.) | Documented §3; follow-up seed story |

| Full pytest integration drift (`BrandPostureID`) | Pre-existing; 6.5c logic covered by focused suite |

| Azure Test not yet run | §7 pending; repeat §2–§3 after deploy |



---



## 7. Definition of done status



- [x] Resolver + four-consumer cutover implemented

- [x] Migrations 084–086 authored; Tony applied LocalDB

- [x] Focused tests + AC-15 alignment green

- [x] LocalDB UAT §1–§6 pass

- [x] Gate evidence + UAT guide updated

- [x] Closeout report (this document)

- [ ] Implementation committed/pushed to PR #106

- [ ] Azure Test §7 sign-off

- [ ] PR marked Ready + merge



---



**Agent closeout note:** LocalDB validation complete. Remaining: commit/push branch work, Azure Test §7 after deploy, final PR sign-off.

