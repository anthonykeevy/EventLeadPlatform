# Lessons Learned: Story 3.11 - Dynamic Submission (Outbox)

**Story:** 3.11  
**Epic:** Epic 3 - Form Builder & Logic Engine  
**Created:** 2026-02-03  

---

## 📝 Lessons Log

_Append lessons as tasks are completed. Format:_

```markdown
### {date} - {lesson_type} Lesson

**Task:** {task_id}
**Context:** {brief context}
**Issue:** {what went wrong or could be improved}
**Lesson:** {actionable insight}
**Prevention:** {how to avoid in future}
```

---

## Lessons

### 2026-02-03 - Process Lesson

**Task:** T01  
**Context:** Task verification requires `cd frontend; npm run build`.  
**Issue:** Frontend build currently fails due to numerous pre-existing TypeScript errors across unrelated features, blocking “TS builds” verification for otherwise-scoped work.  
**Lesson:** Treat “frontend build is green” as a prerequisite for task verification when ACs require `npm run build`.  
**Prevention:** Create/maintain a dedicated build-stabilization task/branch to restore `npm run build` to green before contract-only tasks that depend on it.

### 2026-02-03 - Tooling Lesson

**Task:** T01  
**Context:** Backend import smoke checks.  
**Issue:** Running `python -c "from backend.main import app"` from repo root fails because backend modules use top-level imports (e.g., `common`, `middleware`) that expect `backend/` as the import root.  
**Lesson:** Run import checks from the `backend/` directory (e.g., `cd backend; python -c "from main import app"`).  
**Prevention:** Document the backend cwd/PYTHONPATH expectation; consider standardizing to package-relative imports in a future refactor.

### 2026-02-04 - Process Lesson

**Task:** T04  
**Context:** Verification required lint/build but baseline tooling was incomplete.  
**Issue:** ESLint config was missing and repo-wide TS errors blocked automated verification.  
**Lesson:** Validate tooling baseline (ESLint config + dependency alignment) before running required test commands.  
**Prevention:** Add a pre-verification checklist step for tooling baseline on frontend tasks.

### 2026-02-04 - Testing Lesson

**Task:** T04  
**Context:** Outbox behavior required manual UAT steps.  
**Issue:** Backoff + auth-free headers rely on manual checks.  
**Lesson:** Add unit/integration tests for outbox retry/backoff and request headers.  
**Prevention:** Include outbox tests in CI with mocked `fetch` and IndexedDB.

### 2026-02-04 - Process Lesson

**Task:** T04  
**Context:** UAT evidence captured via DevTools console scripts.  
**Issue:** Evidence capture steps are ad-hoc.  
**Lesson:** Provide standardized DevTools scripts for persistence and header validation.  
**Prevention:** Add scripts to UAT checklist templates for storage + network inspection.

