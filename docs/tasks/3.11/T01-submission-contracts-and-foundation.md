# Task T01: Submission Contracts + Foundations

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T01  
**Status:** ⏳ Ready  
**Dependencies:** None  
**Estimated Time:** 2-3 hours  

---

## 📋 Task Overview

**Objective:** Establish the foundation for Story 3.11 by locking down:
- The **public submission API contract** (frontend + backend schemas)
- The **outbox item contract** (what we store in IndexedDB and how we retry)
- The **telemetry event contract** for validation failures (privacy-safe)
- The **client identity rules** (`clientDeviceId`, rotating `clientSessionId`, `submitAttemptId`)

This task must be runnable in isolation and must not require DB migrations to be executed.

---

## ✅ Scope (In)

- [ ] Define **public submission payload** types on frontend (TypeScript)
- [ ] Define matching **Pydantic schemas** on backend for:
  - submission request/response
  - validation telemetry event payload (contract only)
- [ ] Define **outbox item** TypeScript type (the record we store in IndexedDB)
- [ ] Define **client identity helpers** contract:
  - Stable `clientDeviceId` (random UUID, persisted)
  - Rotating `clientSessionId` per respondent (rotates on page load and kiosk reset)
  - `submitAttemptId` per submit click
- [ ] Implement a **value diagnostics** helper for telemetry (no raw values) that yields:
  - value type, length/trimmed length, and basic shape flags
- [ ] Document the canonical API endpoints (paths + minimal responses) in code comments so FE/BE stay aligned

---

## 🚫 Scope (Out)

- ❌ No DB migrations (those are T02; human runs migrations)
- ❌ No backend route wiring (`POST /api/public/forms/{token}/submissions`) (T03)
- ❌ No IndexedDB implementation (T04)
- ❌ No changes to renderer submit behavior (T05+)
- ❌ No new UI features in the Builder / dashboard (future stories)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `backend/migrations/` | Migration work is isolated to T02 |
| `frontend/src/features/builder/` | Builder is complete; submission work is renderer-focused |
| `frontend/src/features/auth/` | Public renderer/submission must remain auth-free |

---

## ✅ Acceptance Criteria

### AC1: Submission contract is defined (FE + BE)
- **Criterion:** A single, explicit payload shape exists in TypeScript and Pydantic that match field-for-field.
- **Verification:** TS builds; backend imports load; a reader can compare the two files and see the same required fields.

### AC2: Outbox item contract is defined
- **Criterion:** There is a TypeScript type/interface for the IndexedDB outbox record including idempotency + status + retry fields.
- **Verification:** TS builds; type is referenced in docs/comments for T04.

### AC3: Client identity contract is defined
- **Criterion:** `clientDeviceId` is stable; `clientSessionId` rotates per respondent; `submitAttemptId` is per submit.
- **Verification:** Helper signatures exist and are documented; no fingerprinting is introduced.

### AC4: Value diagnostics exist (no raw values)
- **Criterion:** A helper returns a diagnostics object for a value without including the raw value.
- **Verification:** Unit test or manual invocation shows output contains type/length/flags only.

---

## 🔧 Implementation Details (Concrete)

### Frontend (TypeScript)

Create:
- `frontend/src/features/renderer/types/publicSubmission.types.ts`
- `frontend/src/features/renderer/types/telemetry.types.ts`
- `frontend/src/features/renderer/utils/clientIdentity.ts`
- `frontend/src/features/renderer/utils/valueDiagnostics.ts`

Suggested types:

```ts
// publicSubmission.types.ts
export type PublicSubmissionLinkType = 'PREVIEW' | 'PRODUCTION'

export type PublicAnswersByComponentId = Record<string, unknown>

export type PublicSubmissionContext = {
  clientDeviceId: string
  clientSessionId: string
  submitAttemptId: string
  clientTimezone?: string
  clientLocale?: string
  clientUserAgent?: string
  clientScreen?: { width: number; height: number; dpr?: number }
  clientViewport?: { width: number; height: number }
  renderCanvasWidth?: number
  renderCanvasHeight?: number
  renderScaleAtSubmit?: number
  appVersion?: string
  buildSha?: string
}

export type PublicFormSubmissionRequest = {
  idempotencyKey: string
  submittedAtClient: string // ISO
  answersByComponentId: PublicAnswersByComponentId
  context: PublicSubmissionContext
}

export type PublicFormSubmissionResponse = {
  submissionId: number | string
  status: 'ACCEPTED' | 'DUPLICATE'
}
```

Outbox record:

```ts
export type PublicOutboxStatus = 'pending' | 'uploading' | 'failed' | 'success'

export type PublicOutboxItem = {
  outboxItemId: string // client UUID
  token: string
  linkType?: PublicSubmissionLinkType
  request: PublicFormSubmissionRequest
  status: PublicOutboxStatus
  retryCount: number
  lastError?: string
  createdAt: number
  lastTriedAt?: number
}
```

Client identity helpers:
- `getOrCreateClientDeviceId(): string`
- `createNewClientSessionId(): string`
- `createSubmitAttemptId(): string`

Value diagnostics:

```ts
export type ValueDiagnostics = {
  type: 'null' | 'string' | 'number' | 'boolean' | 'array' | 'object' | 'unknown'
  length?: number
  trimmedLength?: number
  flags?: {
    hasWhitespace?: boolean
    hasPlus?: boolean
    digitCountBucket?: '0' | '1-3' | '4-7' | '8-12' | '13+'
  }
}

export function getValueDiagnostics(value: unknown): ValueDiagnostics
```

### Backend (Pydantic schemas)

Create:
- `backend/modules/forms/public_submission_schemas.py`

Suggested Pydantic models:
- `PublicFormSubmissionRequest`
- `PublicFormSubmissionResponse`
- `PublicValidationEventRequest` (contract only; storage/ingest later)

Important: backend uses PascalCase DB columns but Pydantic schemas are typically snake_case with aliases. Follow existing schema style in `backend/modules/forms/public_form_schemas.py`.

---

## 🧪 Required Tests / Verification

- **Frontend:** `cd frontend; npm run build` (must compile)
- **Backend:** run whatever lightweight module import smoke check exists (at minimum, no syntax errors when starting backend).
- **Manual checks:**
  - Call `getValueDiagnostics("  test  ")` → returns type string + trimmedLength, no raw value.
  - Confirm `clientSessionId` is documented to rotate on kiosk reset/new submission.

---

## 🧨 Expected Error Cases

| Scenario | Expected behavior (in this task) |
|----------|----------------------------------|
| Telemetry helper passed an object/array | Diagnostics returns type + safe flags only |
| Caller attempts to log raw values | Explicitly forbidden; keep raw values out of diagnostics type |

---

## 🔁 Out-of-Scope Handling

If user asks to:
- Implement DB table/migration → route to **T02**
- Implement public submission endpoint → route to **T03**
- Implement IndexedDB outbox → route to **T04**
- Wire submit button behavior → route to **T05**
- Add kiosk countdown UI → route to **T06**
- Store/aggregate telemetry for dashboard → route to **T07**

---

## 🌿 Git / PR Requirements (Mandatory)

- Create branch: `task/3.11/T01-submission-contracts-and-foundation`
- Open PR: `task/3.11/...` → `story/epic3-3.11-dynamic-submission`

Recommended (PowerShell):

```powershell
scripts/git/new-task.ps1 -StoryBranch "story/epic3-3.11-dynamic-submission" -StoryId 3.11 -TaskId T01 -Slug "submission-contracts-and-foundation" -CreateWorktree
```

---

## 📤 Handoff Requirements

After completion, provide:
1. List of files created/modified
2. Confirmation that FE + BE contract fields match
3. Verification output for TS build
4. Any discovered patterns or pitfalls recorded in `docs/tasks/3.11/LESSONS-LEARNED.md`

---

## 📚 References

- Story: `docs/stories/story-3.11.md`
- Context: `docs/stories/story-context-3.11.xml`
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

*Task spec created by Ralf-SM*  
*Last Updated: 2026-02-03*

