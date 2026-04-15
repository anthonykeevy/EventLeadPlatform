# Story 6.3.1 — Single-Session Dev Prompt

**Story:** 6.3.1 — Simplified AI Output + Deterministic Layout Foundation  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** _Created by **`@bmad-agent-bmm-sm`** via `./scripts/git/new-story.ps1`_  
**Branch:** `story/epic6-6.3.1-simplified-ai-deterministic-layout` (expected)  
**PR:** Draft PR -> merge to `master` via GitHub

---

## Execution contract

Implement **`docs/stories/story-6.3.1.md`** using **`docs/stories/story-context-6.3.1.xml`** as the map.  
Use **`docs/analysis/eventlead_form_ai_workflow.md`** as architecture source of truth (grid-only pipeline).  
Use **`docs/COMPONENT-FRAMEWORK-REFERENCE.md`** for capability ingestion coverage and component contract alignment.  
Use **`docs/AGENT-LOGGING-GUIDE.md`** for diagnostics and evidence extraction.

Do not claim complete without:

- `STORY-6.3.1-GATE-EVIDENCE.md`
- green test/lint commands
- correlated RequestID evidence
- at least one one-variable-at-a-time tuning sequence

---

## Step 0 — Preflight

After SM creates the worktree and Human opens it in this Cursor window, run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.3.1-simplified-ai-deterministic-layout" `
  -ExpectedBranch "story/epic6-6.3.1-simplified-ai-deterministic-layout" `
  -ReportFile "docs/stories/STORY-6.3.1-PREFLIGHT.md"
```

If paths differ, use actual values from `git worktree list`.

---

## Step 1 — Read sources

1. `docs/stories/story-6.3.1.md`  
2. `docs/stories/story-context-6.3.1.xml`  
3. `docs/analysis/eventlead_form_ai_workflow.md`  
4. `docs/COMPONENT-FRAMEWORK-REFERENCE.md`  
5. `docs/AGENT-LOGGING-GUIDE.md`  
6. `backend/modules/form_ai/service.py`  
7. `frontend/src/features/builder/components/ai/AIAgentPanel.tsx`

---

## Step 2 — Simplified semantic contract + deterministic compiler

- Implement or finalize simplified Step 1 semantic payload contract.
- Ensure deterministic Step 2 compile path produces valid single-page `DefinitionJSON`.
- Enforce grid-only layout resolution.
- Keep raw semantic output and final compiled output both traceable.

---

## Step 3 — Capability ingestion and validation contracts

- Implement versioned capability snapshot ingestion from framework metadata sources.
- Ensure new components/features become available via snapshot refresh (no ad-hoc manual duplication path).
- Implement structured per-component validation contracts:
  - allowed rules
  - parameter schemas
  - compatibility constraints
  - message policy

---

## Step 4 — Canvas-responsive width classes

- Resolve `compact`, `half`, `full` against current canvas width/grid.
- Apply deterministic class-to-span/px mapping with per-component bounds.
- Document and test fallback/downgrade behavior for constrained canvases.

---

## Step 5 — Logging discipline and one-variable tuning

Follow `docs/AGENT-LOGGING-GUIDE.md` exactly:

- capture inbound `RequestID` for each key run
- capture correlated outbound chain (`:outbound:` rows)
- record terminal reason and validation counts

Tuning rule:

- change one meaningful variable per run (prompt section OR policy flag OR layout rule OR validation mapping)
- record hypothesis -> result -> keep/revert decision in gate evidence

---

## Step 6 — Gates

```powershell
cd backend; python -m pytest --tb=short
cd ..\frontend; npm run lint; npm run test:unit -- --watch=false
```

Record results in `docs/stories/STORY-6.3.1-GATE-EVIDENCE.md`.

---

## Step 7 — Closeout updates

- Update `story-6.3.1.md` Dev record fields.
- Update `EPIC-6-STATUS.md` and `EPIC-6-WORKFLOW-GUIDE.md` per closeout checklist.
- Keep scope boundary: Story 6.4 handles iterative edit UX on top of this foundation.

---

## Out of scope reminder

- No multi-page AI generation
- No non-grid layout execution path
- No Alembic migrations unless explicitly requested by Anthony
