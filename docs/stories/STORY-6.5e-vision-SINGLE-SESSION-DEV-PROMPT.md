# Story 6.5e-vision — Single-Session Dev Prompt

You are implementing **Story 6.5e-vision — Component Platform Hardening + Image-to-Form Vision Path**.

**Worktree:** `C:\wt\elp\story-epic6-6.5e-vision-image-to-form`  
**Branch:** `story/epic6-6.5e-vision-image-to-form`  
**PR:** [#116](https://github.com/anthonykeevy/EventLeadPlatform/pull/116) — Draft → `develop`  
**Base:** `develop` at head **095** (Alembic); `master` reconciled 2026-05-28 (PR #115)

---

## Mission (two tracks — same PR; Track 0 first)

### Track 0 — Component platform hardening *(mandatory before Track 1)*

1. Finalize **`docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` v1.3** — §0c global-component submit smoke (may already be drafted; verify and complete).
2. Implement **`backend/scripts/verify_edf_props_wired.py`** — for each EDF `ComponentCode` (`address-lookup-au`, `company-lookup-abr`), compare keys in `PropertiesSchemaJSON` (from DB seed or fixture JSON) against runtime reads in `frontend/src/features/builder/components/edf/*Runtime.tsx`. Exit non-zero with diff.
3. Add **`backend/tests/test_story_6_5e_edf_props_wired.py`** (and static test listing script if needed).
4. Ship **`docs/stories/STORY-6.5e-COMPONENT-CHECKLIST-AUDIT-TEMPLATE.md`**; reference from closeout checklist row 6.
5. Register tools in **`docs/stories/EPIC-6-SM-TOOLS-REGISTRY.md`**.
6. Document alignment-script post-migration gate in **`STORY-6.5e-vision-GATE-EVIDENCE.md`** (Tony runs Alembic; Dev does not).
7. **Stretch (P3):** address manual-entry UI (`g-65d-address-manual-fallback`), `editableLegalNameAfterResolve` (`g-65d-editable-legal-name`).
8. **Stretch (P2):** AI panel hint/chips for AU EDF types (`g-65e-ai-edf-prompt-ux`) — e.g. quick-insert prompt fragment for address/ABR lookup.

**Track 0 exit:** props script green; catalog alignment still PASS; checklist v1.3 referenced in workflow guide.

### Track 1 — Image-to-Form vision path

1. **Read** `docs/stories/STORY-6.5-FEASIBILITY-NOTES.md` — endpoint shape, GPT-5 mini vision, canvas preservation, PII deferral to 6.5g.
2. **Backend:** Multimodal generate path — extend `POST /api/form-ai/generate` *or* add dedicated route per your plan (document in closeout). Accept image (multipart or base64) + existing clarification fields.
3. **Model:** Default **GPT-5 mini** with vision content blocks; optional env flag for image-only model fallback.
4. **Prompt:** New registry section(s) for vision extraction + **layout tier map** (visual structure → `widthIntent` hints per `sectionedPromptArchitecture.ts`). Migration **096+** seeds variants — Tony runs Alembic.
5. **`GenerationRun`:** Persist `generation_source` = `text` | `image` (column or audit JSON — follow existing 6.5b audit column patterns).
6. **Low confidence:** When vision extraction is weak, surface 6.5d clarification dropdowns / user message — do not silently emit empty plans.
7. **Frontend:** AI Agent panel — user-facing image upload (PNG/JPG/WebP, ≤5MB, resize client-side optional). Distinct from dev-only "Load DefinitionJSON" button.
8. **Canvas:** Implement `STORY-6.5b-CANVAS-PRESERVATION-CONTRACT.md` rules C1–C5.
9. **Tests:** `backend/tests/test_story_6_5e_image_to_form.py` — mock vision response → valid `FormSemanticPlan` → validator pass (pattern from 6.3.1 tests).
10. **PII:** Full detector deferred to **6.5g-PII**. MVP minimum: optional `isMockData` checkbox on upload UI + pass-through to API (no persistence requirement unless trivial).

**Out of scope:** 6.5f-style, 6.5g-PII full module, 6.5h-fonts, multi-image stitch, Claude vendor.

---

## Read First (order)

1. `docs/stories/story-6.5e-vision.md`
2. `docs/stories/story-context-6.5e-vision.xml`
3. `docs/stories/STORY-6.5-FEASIBILITY-NOTES.md`
4. `docs/stories/STORY-6.5b-CANVAS-PRESERVATION-CONTRACT.md`
5. `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md`
6. `docs/stories/STORY-6.5d-CLOSEOUT-REPORT.md` §4–§6 (EDF lessons)
7. `backend/modules/form_ai/service.py` — `generate_form_definition`
8. `backend/modules/form_ai/prompt_assembly/` — resolver/renderer
9. `frontend/src/features/builder/components/ai/AIAgentPanel.tsx`
10. `docs/stories/EPIC-6-SM-TOOLS-REGISTRY.md` + `docs/AGENT-LOGGING-GUIDE.md`

---

## Step 0 — Preflight

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.5e-vision-image-to-form" `
  -ExpectedBranch "story/epic6-6.5e-vision-image-to-form" `
  -ReportFile "docs/stories/STORY-6.5e-vision-PREFLIGHT.md"
```

Confirm Alembic head **095**, PR draft exists, worktree path correct.

---

## Step 1 — Plan (chat, 10–15 bullets)

Cover: Track 0 script design; Track 1 API shape; migration list; registry section codes; frontend upload UX; test matrix; AC mapping; stretch items if descoping.

---

## Step 2 — Implement Track 0

Then run:

```powershell
cd backend
python scripts/verify_edf_props_wired.py
python scripts/verify_component_catalog_alignment.py
python -m pytest tests/test_story_6_5e_edf_props_wired.py tests/test_story_6_5d_catalog_alignment.py --tb=short -q
```

---

## Step 3 — Implement Track 1

Follow feasibility endpoint guidance. Reuse compiler/validator/remeasure from 6.3.1 — **do not fork** geometry logic.

---

## Step 4 — Tests (full gate)

```powershell
cd backend
python -m pytest tests/test_story_6_5e_*.py tests/test_story_6_5d_*.py tests/test_story_6_5c_*.py tests/test_form_ai_prompt_assembly.py --tb=short -q
python scripts/verify_component_catalog_alignment.py
python scripts/verify_edf_props_wired.py
```

Frontend: `npm test` for touched files if applicable.

---

## Step 5 — Closeout artifacts

| File | Required |
|------|----------|
| `STORY-6.5e-vision-GATE-EVIDENCE.md` | Yes |
| `STORY-6.5e-vision-CLOSEOUT-REPORT.md` | Yes (API + migrations) |
| `STORY-6.5e-vision-IMPLEMENTATION-FRICTION-LOG.md` | **Yes** |
| Component checklist audit table | Yes if any catalog change |
| `story-6.5e-vision.md`, `EPIC-6-STATUS.md`, `EPIC-6-WORKFLOW-GUIDE.md` | Dev updates at closeout |

Mark PR **Ready for review** when local UAT guide steps pass.

---

## Tony-only

```powershell
cd backend
alembic upgrade head
```

---

*SM pack — 2026-05-28*
