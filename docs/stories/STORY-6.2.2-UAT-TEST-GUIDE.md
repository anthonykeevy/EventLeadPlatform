# Story 6.2.2 — UAT Test Guide

**Story:** 6.2.2 — File Upload Component (Full Stack)  
**Worktree:** `C:\wt\elp\story-epic6-6.2.2-file-upload-full-stack`  
**Branch:** `story/epic6-6.2.2-file-upload-full-stack`

---

## 0) Preconditions

| Step | Action |
|------|--------|
| 0.1 | `git pull` story branch; DB migrated per Dev closeout (Anthony ran Alembic upgrade). |
| 0.2 | Backend + frontend running per usual dev docs. |
| 0.3 | A **published** form with public link token (prod or preview per test case). |

Record environment (URLs, form id, token suffix) in `STORY-6.2.2-UAT-RESULTS.md`.

---

## 1) Builder — toolbox & canvas

| ID | Steps | Expected |
|----|-------|----------|
| 1.1 | Open builder → toolbox | **File upload** appears under Input (or agreed category). |
| 1.2 | Drag onto canvas | Component renders with label + upload affordance + validation region. |
| 1.3 | Properties: set accept to `.pdf`, max size small (e.g. 1MB), single file | Values persist after save/reload. |
| 1.4 | Save definition; run `POST /api/form-validate` (Swagger/Postman) with `file-upload` | **200** / valid. |

---

## 2) Runtime — upload & submit (happy path)

| ID | Steps | Expected |
|----|-------|----------|
| 2.1 | Open public URL with token | Form renders; file control works. |
| 2.2 | Choose valid file (within type/size) | Upload completes; UI shows file name; DevTools shows attachment id response. |
| 2.3 | Submit form | **ACCEPTED**; submission id returned. |
| 2.4 | DB or admin UI (if available) | `FormSubmission` row exists; attachment row(s) have **same** `FormSubmissionID` (not null). |

---

## 3) Negative & abuse (sampling)

| ID | Steps | Expected |
|----|-------|----------|
| 3.1 | Upload file over max size | Clear error; no orphan or orphaned row documented. |
| 3.2 | Upload disallowed type | Rejected. |
| 3.3 | Craft submit payload referencing **foreign** attachment id (from another session or fake uuid) | **Rejected** or validation error (per AC-3). |

---

## 4) Company download

| ID | Steps | Expected |
|----|-------|----------|
| 4.1 | Login as company user with access | Download attachment via documented API → correct bytes + filename. |
| 4.2 | Login as user **without** access | 403/404. |

---

## 5) Regression sniff

| ID | Steps | Expected |
|----|-------|----------|
| 5.1 | Form with **only** text + submit | Still submits. |
| 5.2 | Existing url/rating/paragraph fields |unchanged behaviour. |

---

## 6) Evidence

- Append results + screenshots/log snippets to `docs/stories/STORY-6.2.2-UAT-RESULTS.md`.  
- Link `STORY-6.2.2-GATE-EVIDENCE.md` for automated gates.
