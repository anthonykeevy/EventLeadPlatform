# Code Review: EventLead Platform (Epics 1–3 Complete)

**Scope:** Development codebase after completing Epic 3 (Form Builder).  
**Date:** 2026-02-06  
**Environment:** Development (not production-hardened).

---

## Executive Summary

- **Strengths:** Clear module boundaries, consistent auth usage, protected-zone discipline, global exception handling, and a solid form builder/renderer/submission foundation (Epic 3).
- **Risks to address before production:** CORS (`allow_origins` includes `"*"`), hardcoded health-check URL, and frontend typecheck/lint debt.
- **Recommendation:** Safe to continue into Epic 5 (Review & Publishing) with the fixes below applied in dev and a pre-production security pass.

---

## 1. Architecture & Structure

### Backend
- **Module layout** is coherent: `auth`, `users`, `invitations` (Epic 1); `companies`, `events`, `admin`, `audit`, `forms` (Epic 2); form versioning, public resolve, public links (Epic 3).
- **Router registration** in `main.py` is explicit and documented (Story references in comments). Public form router is mounted at `/api/public`; form CRUD and versioning stay under `/api/forms`.
- **Protected zones** in `docs/epic-status.md` are well defined (Epic 1/2/3 boundaries). Epic 3 is allowed to add new files under `backend/modules/forms/` without editing protected Epic 2 files.

### Frontend
- **Feature-based structure** under `src/features/` (auth, dashboard, events, forms, builder, renderer, ux, validation, etc.) matches backend domains and supports lazy loading in `App.tsx`.
- **Shared utilities** (`offlineQueue`, `unsavedWorkTracker`, `formAutoSave`) are in `src/utils/` and exposed for debugging where needed.
- **API layer** is centralized (`apiClient` with auth interceptors; feature-specific APIs in `features/*/api/`).

**Verdict:** Structure is in good shape for the next epics.

---

## 2. Security

### Positive
- **Public form resolve** (`GET /api/public/forms/{token}`) does not use `get_current_user`; access is token + link validity + expiration only. Appropriate for unauthenticated respondents.
- **Authenticated form operations** (versions, public links, CRUD) consistently use `Depends(get_current_user)`.
- **Global exception handler** logs to `log.ApplicationError` and avoids leaking stack traces to the client; stack traces are sanitized per `sanitize_stack_trace`.
- **Environment/secrets:** `.env` is gitignored; `.cursorignore` excludes `.env` from indexing.

### Fix Before Production
- **CORS** in `main.py`: `allow_origins` includes `"*"` in addition to localhost. For production, remove `"*"` and list only the frontend origin(s) (e.g. `https://app.eventlead.com`). In dev, keeping only `http://localhost:5173` and `http://127.0.0.1:5173` (and 3000 if still used) is sufficient.
- **Health check** in `App.tsx`: URL is hardcoded `http://127.0.0.1:8000/api/health`. Prefer `apiClient.get('/api/health')` (or `import.meta.env.VITE_API_BASE_URL` + `/api/health`) so it respects the same base URL as the rest of the app and works in staging/production.

---

## 3. Backend Patterns

### Error handling
- Global handler for `Exception` and `HTTPException` ensures all failures are logged and returned in a consistent JSON shape. Good.
- Individual routes raise `HTTPException` with appropriate status codes (e.g. 404 for invalid/expired token in public form resolve).

### Database
- `get_db` dependency and session usage are consistent. Public form resolve uses read-only patterns and defensive `first()` where uniqueness is expected.
- **FormSubmission** (migration 035): Idempotency is enforced at the DB level via `UQ_FormSubmission_FormPublicLinkID_IdempotencyKey`. Good for Story 3.11.

### Logging
- `get_logger(__name__)` used in routers; `LastAccessedAt` update failure is logged as warning and does not fail the request. Appropriate.

### Minor
- `datetime.utcnow()` is used; Python 3.12+ prefers `datetime.now(timezone.utc)` for clarity. Non-blocking; can be done in a cleanup pass.
- `link.LastAccessedAt = datetime.utcnow()` uses a type-ignore; consider a small helper or typed attribute to avoid ignores.

---

## 4. Frontend Patterns

### Positive
- **Lazy loading** of main pages reduces initial bundle size.
- **TanStack Query** with sensible defaults (retry 1, staleTime 5 min).
- **Offline queue** (IndexedDB, `lead_submission` type, retry/backoff) supports offline-first submission; queue is keyed by `userId` to avoid cross-user data.
- **PublicFormArtboard** supports `onSubmissionDeferred`, embed mode, and action query params; validation and rule evaluation are integrated.
- **apiClient** handles Bearer token attachment and 401 refresh flow; auth endpoints are excluded from retry to avoid loops.

### Tech debt (known from T10)
- **TypeScript:** `npm run build` no longer runs `tsc`. Re-enable typecheck (e.g. in CI or as a separate script) and fix existing errors in a dedicated task.
- **ESLint:** 198 warnings (e.g. unused vars, react-hooks deps). Treat as baseline; reduce when touching files (per T10 retro).
- **PostCSS** “missing `from` option” and **offlineQueue** dynamic/static import chunking warning: documented; acceptable for dev; fix in a frontend-hygiene task if desired.

### Configuration
- API base URL from `VITE_API_BASE_URL` with fallback to `http://127.0.0.1:8000` is correct. Health check should use the same base (see Security above).

---

## 5. API Contract & Consistency

- Public form **resolve** response uses camelCase aliases (`linkType`, `definition`) in Pydantic, matching frontend expectations.
- Backend form schemas use Field aliases (e.g. `totalSubmissions`) for JSON; frontend normalizes with fallbacks (`backend.total_submissions ?? backend.totalSubmissions ?? backend.TotalSubmissions`) where needed. Consider standardizing one convention (e.g. camelCase in API JSON) to reduce fallbacks over time.
- Public form router comment says it’s mounted by `public_router`; in `main.py` it’s mounted directly with `prefix="/api/public"`. Comment is slightly misleading; worth a one-line fix in the router docstring.

---

## 6. Testing & Verification

- Backend has structured tests under `backend/tests/` (auth, RBAC, multi-tenancy, forms, etc.).
- Story 3.11 UAT is documented in `STORY-3.11-UAT-TEST-GUIDE.md` with scenarios marked PASS.
- Frontend: some feature-level tests (e.g. validation, UX, dashboard). No full E2E observed; acceptable for current stage. Consider adding a single E2E for “open public form → submit → verify success” before production.

---

## 7. Recommendations (Prioritized)

| Priority | Action | Owner |
|----------|--------|-------|
| **P0 (before prod)** | Remove CORS `"*"` and restrict to frontend origin(s). | Backend |
| **P0 (before prod)** | Use apiClient or env for health check URL in `App.tsx`. | Frontend |
| **P1** | Re-enable TypeScript typecheck in CI or `npm run build` and fix errors. | Frontend |
| **P1** | Add a follow-up task to gradually reduce ESLint warnings when touching files. | Process |
| **P2** | Standardize API JSON to camelCase and reduce frontend fallbacks. | Full-stack |
| **P2** | Fix public_form_router docstring (mount point). | Backend |
| **P3** | Replace `datetime.utcnow()` with `datetime.now(timezone.utc)` where appropriate. | Backend |

---

## 8. Conclusion

The codebase is in good shape for development and for moving into Epic 5. Protected zones and module boundaries are clear; auth and public token behavior are consistent; logging and error handling are solid. Address the two P0 items and the known frontend debt (typecheck + lint) before production, and keep the rest as incremental improvements.

---

*Code review performed against current branch (Epic 3 complete, dev environment).*
