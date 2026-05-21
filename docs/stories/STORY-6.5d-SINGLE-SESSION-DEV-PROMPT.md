# Story 6.5d — Single-Session Dev Prompt

You are implementing **Story 6.5d — Clarification Data Plane + Component Catalog Completion**.

**Worktree:** `C:\wt\elp\story-epic6-6.5d-clarification-component-platform`  
**Branch:** `story/epic6-6.5d-clarification-component-platform`  
**PR:** [#109](https://github.com/anthonykeevy/EventLeadPlatform/pull/109) — Draft → `develop`  
**Base:** `develop` at or after merge commit `7b908e2` (includes 6.5c + #108 status sync)

---

## Mission (two tracks — same PR)

### Track A — Component platform

1. Seed **missing** `FormBuilderComponent` rows: `rating`, `url`, `file-upload`, `paragraph`, `address` (global).
2. Add **AU** Country-scoped online address component (`address-lookup-au` — **GeoScape/PSMA**; read `docs/architecture/au-address-lookup-geoscape-handoff.md`).
3. **Offline-capable forms:** exclude network-dependent components from resolver/init/AI/validator; fallback = manual `address`.
4. *(Stretch)* ABR company lookup component — `docs/architecture/abr-company-lookup-builder-handoff.md` / `g-65d-abr-builder-component`.
5. Implement `backend/scripts/verify_component_catalog_alignment.py` + tests; register in `EPIC-6-SM-TOOLS-REGISTRY.md`.
6. Follow **`docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md`** for every new type (incl. §0 connectivity).
7. Trim Block G / prompt prose so LLM is not told to emit ghost types.

### Track B — Clarification data plane

1. `ref.AudienceLocale`, `ref.FormPurpose`, `ref.RespondentType` + §11 seeds.
2. Three `GET /api/ref/...` endpoints (list + resolved default).
3. Block **E** in registry; renderer injects E1/E2/E3 prose from resolved refs.
4. `Company` / `Form` / `GenerationRun` columns for defaults + audit.
5. AI Agent panel: three API-driven dropdowns; **remove** `AudienceLocale` enum from generation path (backend + frontend).

---

## Read First

1. `docs/stories/story-6.5d.md`
2. `docs/stories/story-context-6.5d.xml`
3. `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md`
4. `docs/architecture/decision-6.5a-clarification-options-data-model.md`
5. `docs/architecture/prompt-assembly-registry-architecture.md` — §2.7
6. `docs/stories/STORY-6.5c-CLOSEOUT-REPORT.md` — §3
7. `docs/architecture/au-address-lookup-geoscape-handoff.md`
8. `docs/architecture/abr-company-lookup-builder-handoff.md` *(if stretch)*
9. `docs/AGENT-LOGGING-GUIDE.md` + `docs/stories/EPIC-6-SM-TOOLS-REGISTRY.md`
10. `backend/modules/form_builder/component_catalog.py`
8. `backend/migrations/versions/039_form_defaults_component_catalog.py`

---

## Step 0 — Preflight

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.5d-clarification-component-platform" `
  -ExpectedBranch "story/epic6-6.5d-clarification-component-platform" `
  -ReportFile "docs/stories/STORY-6.5d-PREFLIGHT.md"
```

Verify PR #109, alembic head **086**, worktree path correct.

---

## Step 1 — Plan (chat, 8–12 bullets)

Cover: migration list (`087+`), component seeds vs AU address scope, alignment script design, Block E section codes, API shapes, frontend panel files, enum removal list, AC matrix.

---

## Step 2 — Track A (catalog)

- Migrations seed global backlog + AU `address-lookup-au`.
- Wire renderer if new codes need preview/runtime tweaks.
- `verify_component_catalog_alignment.py` — exit 1 on set mismatch; print diff.
- `backend/tests/test_story_6_5d_catalog_alignment.py`
- Update `EPIC-6-SM-TOOLS-REGISTRY.md` in same PR.

**Tony runs Alembic — you do not.**

---

## Step 3 — Track B (clarification)

- Ref tables + seeds per architecture §11.
- Read APIs + resolution helper (Company → Form → request).
- Registry Block E migrations + resolver/renderer.
- Schema migrations for Company/Form/GenerationRun.
- Frontend: dropdowns load from APIs only; pass codes on generate.

---

## Step 4 — Tests

```powershell
python -m pytest backend/tests/test_story_6_5d_*.py --tb=short
python -m pytest backend/tests/test_story_6_5c_*.py backend/tests/test_form_ai_prompt_assembly.py --tb=short
python backend/scripts/verify_component_catalog_alignment.py
python -m pytest --tb=short
```

---

## Step 5 — Closeout artifacts

| File | Required |
|------|----------|
| `STORY-6.5d-GATE-EVIDENCE.md` | Yes |
| `STORY-6.5d-CLOSEOUT-REPORT.md` | Yes (API + migrations) |
| `STORY-6.5d-IMPLEMENTATION-FRICTION-LOG.md` | **Yes — fill friction table** |
| Closeout checklist rows in `story-6.5d.md`, `EPIC-6-STATUS.md`, `EPIC-6-WORKFLOW-GUIDE.md` | Yes |

Mark PR Ready for UAT when green gate passes. Do not merge.

---

## Friction log (mandatory)

What took more than one attempt? Record in `STORY-6.5d-IMPLEMENTATION-FRICTION-LOG.md`. SM uses this in closeout to improve workflow and register automation in `EPIC-6-SM-TOOLS-REGISTRY.md`.

---

*Story 6.5d SM pack — 2026-05-21.*
