# Task T10: Frontend Build Stabilization (lint + build clean)

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T10  
**Status:** ✅ Done  
**Dependencies:** T09  
**Estimated Time:** 2-4 hours  

---

## Brief Scope

- Make frontend baseline green:
  - `npm run lint`
  - `npm run build`
- Resolve **all** current TypeScript + ESLint errors (even if unrelated to Story 3.11).
- Keep changes scoped to correctness + lint fixes (no feature changes).

## Out of Scope

- New features or UI changes beyond what is required to pass lint/build.
- Backend changes (unless a frontend fix requires a small shared type adjustment).

## Acceptance Criteria

- [x] `npm run lint` passes.
- [x] `npm run build` passes.
- [x] Any remaining warnings are documented (if non-blocking).
- [x] Fixes are committed on a task branch with a PR to the story branch.

## Verification Steps

```bash
cd frontend
npm run lint
npm run build
```

## Git / PR (Mandatory)

- Branch: `task/3.11/T10-frontend-build-stabilization`
- PR: task → `story/epic3-3.11-dynamic-submission`

---
