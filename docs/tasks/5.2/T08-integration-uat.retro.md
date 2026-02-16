# Retro: T08 — Integration + UAT

**Task:** T08 - Integration + UAT  
**Date:** 2026-02-16  

---

## What went well

- **UAT automation:** Chrome DevTools MCP enabled full login → Dashboard → Form Branding Defaults → Builder flow with snapshot/click/fill.
- **Defect detection:** "Save to Company Defaults" 422 surfaced immediately; network + schema inspection pinpointed payload mismatch.
- **Targeted fix:** Single-file change in `formDefaultsApi.ts`; no backend changes required.

---

## What could improve

- **API contract alignment:** Builder and Dashboard use different `formDefaultsApi` modules; Builder API did not match backend `UpdateFormDefaultsRequest`. Unify or document contract.
- **Frontend source of truth:** UAT ran against frontend that may have been from a different worktree; fixes in T08 worktree require explicit restart from correct path.

---

## Lessons for future

- **Payload schema:** When multiple clients (Dashboard, Builder) call same PUT endpoint, share request schema/types or add integration test.
- **Agent UAT:** Ensure services run from the task worktree so code changes apply immediately.

---

*Ralf-Dev retro 2026-02-16*
