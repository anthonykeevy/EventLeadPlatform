# Story 6.5c — UAT Test Guide & Results



**Story:** 6.5c — Capability Catalog Cutover  

**UAT owner:** Tony + SM  

**Environment:** LocalDB first, then Azure Test after merge to `develop`  

**Last updated:** 2026-05-20



---



## Section 1 — Migration & ref.BrandPosture



Pass criteria:



- Migrations `084+` applied (`alembic upgrade head`).

- `ref.BrandPosture` has four active rows (`local`, `heritage`, `neutral`, `transcreate`).

- Company posture resolves through ref table (spot-check in SSMS).



**Section 1 Final:** **Pass**



**Evidence:** Tony confirmed migrations applied and `ref.BrandPosture` rows exist. Alembic output recorded in `STORY-6.5c-GATE-EVIDENCE.md` § Migrations executed.



---



## Section 2 — Toolbox ↔ Init alignment



Pass criteria:



- Open Form Builder for an **AU** company/event.

- Toolbox shows only component types returned by init (no extra static types).

- Note `componentCode` list from browser network tab (`POST /api/form-builder/init`).



**Section 2 Final:** **Pass**



**Evidence:** Toolbox palette matches init `components[]` only (14 global MVP types); no extra static registry types after Story 6.5c `ComponentSidebar` cutover.



---



## Section 3 — AI prompt ↔ toolbox alignment



Pass criteria:



- Same AU context: run **Generate Form Draft** with a prompt that needs address/email/phone.

- AI panel trace shows ALLOWED COMPONENT TYPES matching Section 2 toolbox codes.

- Generation succeeds without `unknown-component-type` for types visible in toolbox.

- No regression: no `context-pack-load-failed` / `prompt-assembly-resolution-failed`.



**Section 3 Final:** **Pass**



**Evidence:** Forms **504** (AU) and **813** (GB, after Event 40 → GB) — GenerationRuns **165** / **167** `validated-success`. ALLOWED types align with init catalog; no assembly-resolution failures.



---



## Section 4 — Country scope change



Pass criteria:



- Switch to a non-AU event (or company) where AU-only components should not apply.

- Re-load builder: AU-only codes **absent** from toolbox on non-AU context; present on AU context.



**Section 4 Final:** **Pass**



**Evidence (2026-05-20):**



1. Scoped `divider` (`FormBuilderComponentID = 14`) to **Country / AU** via SSMS.

2. Form **813** (UK event, GB) — **Divider absent** from toolbox.

3. Form **504** (AU event) — **Divider present** in toolbox.

4. Reverted `divider` to **Global**; both forms show Divider again.



**Note:** Use an existing `FormBuilderComponent` row (e.g. `divider`, `radio`). Types like `rating` exist only in legacy `ComponentCapabilitySnapshot` JSON, not in `dbo.FormBuilderComponent` — see closeout § Catalog drift.



---



## Section 5 — Brand posture



Pass criteria:



- Change brand posture via API (no UI in scope); generation uses correct Block C variant prose.

- `GenerationRun` / snapshot records posture resolution source.



**Section 5 Final:** **Pass**



**Evidence (agent API run, LocalDB, 2026-05-20):**



| Run | Request | `meta.brand` | `GenerationRun` | Block C variant |

|-----|---------|--------------|-----------------|-----------------|

| **168** | `brandPosture: "neutral"`, form **504** | `resolved: neutral`, `source: request.brandPosture` | `BrandPosture=neutral`, `validated-success` | `VariantCode=neutral` — *"Brand posture: neutral. Use market-neutral voice..."* |

| **169** | `brandPosture: "heritage"`, `brandHeritageOrigin: "US"`, form **504** | `resolved: heritage`, `heritageOrigin: US`, `source: request.brandPosture` | `BrandPosture=heritage`, `BrandHeritageOrigin=US`, `validated-success` | `VariantCode=heritage` — *"Brand posture: heritage... {heritageOrigin}..."* |



Endpoint: `POST /api/form-ai/generate` (authenticated). Block C variant confirmed via `GenerationRun.PromptVariantSnapshot` → `variantIds.C` → `config.PromptSectionVariant.VariantCode`.



---



## Section 6 — Automated gates



Review `STORY-6.5c-GATE-EVIDENCE.md` — focused + full pytest summaries.



**Section 6 Final:** **Pass**



**Evidence:** Story 6.5c + 6.5b regression **35/35** targeted pytest. Migrations **083 → 084 → 085 → 086** applied (Tony). Full-suite drift documented (pre-existing integration fixture issues); not blocking 6.5c catalog logic.



---



## Section 7 — Test environment (post-merge)



After merge to `develop` and deploy:



- Repeat Sections 2–3 on `signalplatforms-test`.

- Confirm catalog alignment holds in deployed Test.



**Section 7 Final:** _Pending_ — Tony to confirm after worktree merge and Azure Test deploy.



---



## UAT Result Summary



| Section | Result | Notes |

|---|---|---|

| 1 Migrations / ref.BrandPosture | **Pass** | 084–086 applied; four ref rows confirmed |

| 2 Toolbox ↔ init | **Pass** | Init-only palette; 14 global MVP types |

| 3 AI prompt ↔ toolbox | **Pass** | Forms 504/813; runs 165/167 |

| 4 Country scope | **Pass** | Divider AU-only probe; reverted to Global |

| 5 Brand posture | **Pass** | API runs 168/169; Block C variants neutral + heritage |

| 6 Automated gates | **Pass** | 35/35 focused pytest; gate evidence updated |

| 7 Azure Test | _Pending_ | After merge + deploy to Test |



**Final:** _Pending Azure Test (§7)_ — LocalDB UAT **Pass** for §1–§6.

