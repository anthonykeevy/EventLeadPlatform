# Story 6.3 — Single-Session Dev Prompt

**Story:** 6.3 — AI Context Uplift & Benchmark Baseline  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** _Run `./scripts/git/new-story.ps1` — example:_ `C:\wt\elp\story-epic6-6.3-ai-context-benchmark-baseline`  
**Branch:** `story/epic6-6.3-ai-context-benchmark-baseline` (expected)  
**PR:** Draft PR → merge to `master` via GitHub  

---

## Execution contract

You are the Dev agent. Implement **`docs/stories/story-6.3.md`** using **`docs/stories/story-context-6.3.xml`** as the implementation map. Obey **Green CI/CD** in `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`. Do **not** claim complete without **`STORY-6.3-GATE-EVIDENCE.md`** and green commands recorded.

---

## Step 0 — Preflight

After Human creates the worktree, run (adjust paths if script echoes different folder):

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.3-ai-context-benchmark-baseline" `
  -ExpectedBranch "story/epic6-6.3-ai-context-benchmark-baseline" `
  -ReportFile "docs/stories/STORY-6.3-PREFLIGHT.md"
```

If paths differ, use the actual paths from `git worktree list`.

---

## Step 1 — Read sources

1. `docs/stories/story-6.3.md`  
2. `docs/stories/story-context-6.3.xml`  
3. `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` (current v1.1 → will become v2)  
4. `docs/stories/STORY-6.2-BENCHMARK-FORMS.md`  
5. `backend/modules/form_ai/service.py`  
6. `backend/tests/test_story_6_2_ai_generation_loop.py`  

---

## Step 2 — Context Pack v2

- Edit **`STORY-6.2-AI-CONTEXT-PACK.md`**: bump **Context Pack Version** to **2.0**, add **Changes from v1.1**, align component catalog and examples with **`docs/COMPONENT-FRAMEWORK-GUIDE.md`** and post-6.2.2 **`file-upload`** semantics (public attachment IDs only).  
- Keep JSON-only contract and validator-correction mapping sections accurate.

---

## Step 3 — Pipeline hardening

- Optional: **`FORM_AI_CONTEXT_PACK_PATH`** (confirm naming with `env.example`) — default behavior unchanged when unset.  
- Ensure API errors for missing pack remain actionable (no raw stack to clients).  
- Add tests for override path if env is implemented.

---

## Step 4 — Benchmark harness

- Add **`backend/tests/test_story_63_benchmark_harness.py`**.  
- Cover **all 10** benchmarks from `STORY-6.2-BENCHMARK-FORMS.md` using **mocked** `_request_chatgpt_completion` + fixtures.  
- Assertions: validator acceptance, expected types/counts per benchmark intent, single-page rule.

---

## Step 5 — Baseline doc

- Create **`docs/stories/STORY-6.3-BENCHMARK-BASELINE.md`** with table + SHA + date + `mocked-ci` (or live model if run).  

---

## Step 6 — Gates

```powershell
cd backend; python -m pytest --tb=short
cd ..\frontend; npm run lint; npm run test:unit -- --watch=false
```

Record output in **`docs/stories/STORY-6.3-GATE-EVIDENCE.md`**.

---

## Step 7 — Closeout

- Update `story-6.3.md`: Status Complete, PR #, dates, Dev Agent Record.  
- **`EPIC-6-STATUS.md`** + **`EPIC-6-WORKFLOW-GUIDE.md`** per story closeout checklist.  
- Open/merge PR via GitHub.

---

## Out of scope reminder

- No Story **6.4** conversational edit loop.  
- No new DB migrations unless an unforeseen blocker requires it (unlikely — document in story if so).
