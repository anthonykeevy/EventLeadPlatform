# Agent Logging Guide (Component Framework + Builder UI)

**Purpose:** Help agents (and UAT testers) quickly capture and interpret **what the user did** and **what the UI rendered** for Component Framework issues across **Toolbox / Canvas / Properties** (including **Grid Layout** + **resize**).

**For Form AI / API failures:** Treat this guide as the **canonical way to get the truth**. Do **not** infer root cause from the generic UI copy alone. Use `log.ApiRequest` (inbound + outbound chain) and `backend/enhanced_diagnostic_logs.py` as described below — same database the product already writes.

**Primary reference:** `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

---

## UAT test credentials (local dev)

For Builder/UAT sessions, use this seeded test account:

| Email | Password | Role | Notes |
|-------|----------|------|-------|
| user2@test.com | `JChMom7KYLfL88&!` | Company Admin | Use for builder UAT and admin flows |

**⚠️ Local/dev only** — Do not use in production. Rotate if exposed.

**If no seed users:** Sign up a new user via the app, verify email (MailHog at http://localhost:8025), then login.

---

## Quick Start (most common workflow)

### 1) Enable frontend dev logs

Create/update `frontend/.env.local` (or `frontend/.env`) with:

```bash
VITE_ENABLE_DEV_LOGS=true
# Optional: mirrors debug/info logs to console (resize + SmartBorder are noisy)
VITE_LOG_VERBOSE_RESIZE=false
# Optional: persist logs in localStorage for same-tab recovery after reload
VITE_LOG_PERSIST_TO_STORAGE=true
# Optional: send log batches to backend log.FrontendEvent
VITE_LOG_SEND_TO_BACKEND=true
```

Restart the Vite dev server after editing env vars.

### 2) Reproduce the bug and capture logs

In the Builder UI header you should see **“Dev Logs”** (download button). After reproducing the issue, click it and attach the JSON file to the bug report.

If `VITE_LOG_SEND_TO_BACKEND=true` is enabled, recent entries are also sent to `POST /api/v1/logs/frontend` and stored in `log.FrontendEvent`.

### 3) If the bug might involve backend/API

Use the backend diagnostic tool to collect recent API/auth/error context:

```bash
python backend/enhanced_diagnostic_logs.py --limit 50
```

**Form AI / generate failures:** narrow to the route, then correlate by `RequestID`:

```bash
python backend/enhanced_diagnostic_logs.py --path-filter form-ai --limit 20
python backend/enhanced_diagnostic_logs.py --request-id "<inbound-uuid>" --correlation-only
```

For frontend builder events stored in `log.FrontendEvent`, use:

```bash
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "resize" --limit 50
```

---
## Backend diagnostic tool coverage (what it can capture)

`backend/enhanced_diagnostic_logs.py` can pull and print the following log categories:
- **Auth events**: `log.AuthEvent` (event type, user/email, IP, user agent, session, reason JSON)
- **Application errors**: `log.ApplicationError` (error type/message, stack trace, exception type, request ID)
- **API requests**: `log.ApiRequest` (path, status, duration, request/response payloads, headers, query params)
- **Profile/theme enhancement calls**: filtered `log.ApiRequest` entries for theme/layout/font endpoints
- **Email deliveries**: `log.EmailDelivery` (status, provider response, error message, retry count)
- **Epic 2 audit trail**: `audit.ApprovalAuditTrail` (if table exists; otherwise safely skipped)
- **Correlation analysis**: joins `ApplicationError`, `ApiRequest`, `AuthEvent` by `RequestID`
- **Performance summary**: request counts, avg/max duration, error counts for a time window
- **Frontend events**: `log.FrontendEvent` (event type, level, component/session/request context, payload)

### Useful CLI options (focused modes)
- `--limit / -l`: rows per table (default 5)
- `--request-id / -r`: correlation analysis for a specific **inbound** request (the correlation UUID from `log.ApiRequest.RequestID` on the browser/API row — **not** the `:outbound:` suffix rows; see below)
- `--correlation-only`: with `--request-id`, print **only** the correlation block + the full **ApiRequest chain** (parent + all synthetic outbound rows). Use this for Form AI / OpenAI traces without dumping every recent table.
- `--performance-hours / -p`: time window for performance metrics
- `--path-filter`: only show API requests matching a path pattern
- `--no-theme-requests`: hide profile/theme enhancement request section
- `--frontend-only`: query only `log.FrontendEvent`
- `--frontend-filter`: filter frontend event names (e.g., `resize.width`, `fieldshell.resize.commit`)
- `--frontend-component-id`: filter by `ComponentID`
- `--frontend-session-id`: filter by `SessionID`
- `--frontend-level`: filter by log level (`debug|info|warn|error`)

---

## `log.ApiRequest`: inbound vs outbound (Form AI, OpenAI)

Agents often confuse **one user action** with **multiple rows** in `log.ApiRequest`. This section matches the implementation in `backend/middleware/outbound_request_logger.py` and `backend/middleware/request_logger.py`.

### Inbound rows (real HTTP)

- **What:** The API route the browser or integration called (e.g. `POST /api/form-ai/generate`).
- **RequestID:** A single correlation UUID (e.g. `1d5a1cb1-820a-4ee6-9956-dce5820a6a5d`).
- **Path:** Starts with `/api/...` (or your app prefix).

### Outbound rows (synthetic path, tied to the same user request)

- **What:** Each backend HTTP call to an external provider (e.g. OpenAI) is logged as its own `log.ApiRequest` row so duration and payloads appear in the same diagnostics stream.
- **Path:** **Synthetic** — built as `/outbound/{provider}{upstream_path}`, e.g. `/outbound/openai/v1/responses`. This is **not** a route clients call; it is only how the logger stores the outbound call.
- **RequestID:** `{inbound_correlation_uuid}:outbound:{new_uuid}` (parent id **plus** `:outbound:` **plus** another GUID).
- **Headers column:** JSON often includes `"direction": "outbound"`, `"provider": "openai"`, and `"url": "https://api.openai.com/..."`.

So for **one** click on “Generate Form Draft” you typically see **one** inbound row plus **N** outbound rows (N = number of LLM round-trips in that request, often up to **four**: initial generation plus up to three validator correction attempts).

### HTTP 200 ≠ “success” for Form AI

`POST /api/form-ai/generate` usually returns **HTTP 200** even when the JSON body says the draft failed, e.g. `"status": "failed"`, `"trace": { "terminalReason": "retry-cap-exhausted", ... }`. Always read **`ResponsePayload`** on the **inbound** `/api/form-ai/generate` row for the real outcome (`trace.attempts[]`, validation counts, `userMessage`).

OpenAI outbound rows also show **200** when the provider returned a normal response; they do **not** by themselves mean the form validated.

### Form AI: map UI / `trace.terminalReason` → where the truth lives

| UI or `trace.terminalReason` | What actually failed | Where to read the truth |
|------------------------------|----------------------|-------------------------|
| **`retry-cap-exhausted`** | Validator / collisions / boundaries after one or more **successful** model round-trips | Inbound `POST /api/form-ai/generate` → **`ResponsePayload`**: `trace.attempts[]` (counts per attempt). Optionally pull **last** `"Your previous JSON failed..."` block from outbound **`RequestPayload`** (the correction prompt sent to the model). |
| **`provider-error`** | Exception **before** validation (OpenAI HTTP error, missing key, empty response, JSON parse, etc.) | 1) Inbound **`ResponsePayload`**: `trace.attempts` is often **empty**; `attemptCount` may be **1**. 2) **First** row in the chain with `Path LIKE '/outbound/openai%'`: **`StatusCode`** and **`ResponsePayload`**. If **`StatusCode` ≥ 400**, body usually has OpenAI `error` JSON. If **200** but inbound still `provider-error`, failure was after HTTP (parse/post-process) — use **backend stdout**: search for `form-ai generate failed before validation` (full exception is logged). |
| **`context-pack-load-failed`** | Could not read context pack file | Startup path; fix `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` / `FORM_AI_CONTEXT_PACK_PATH`; not an OpenAI row. |

**Getting `RequestID`:** From SQL (latest `Path = '/api/form-ai/generate'`), from **`enhanced_diagnostic_logs.py --path-filter form-ai`**, or from your browser’s Network tab correlation if exposed. Then run `--correlation-only` with that **inbound** UUID.

### How to pull a full trace (recommended)

From the **repository root** (same as Quick Start; `.env` in `backend/` and `DATABASE_URL` / `common.database` must work):

```bash
python backend/enhanced_diagnostic_logs.py --request-id "1d5a1cb1-820a-4ee6-9956-dce5820a6a5d" --correlation-only
```

(Alternatively: `cd backend` then `python enhanced_diagnostic_logs.py ...`.)

This prints:

1. Correlation analysis (join with `ApplicationError` / `ApiRequest` / `AuthEvent` when present — **exact** `RequestID` match only on the inbound id).
2. **CORRELATED log.ApiRequest CHAIN**: every row where `RequestID = '<guid>'` **OR** `RequestID LIKE '<guid>:outbound:%'`, ordered by `ApiRequestID`.

Previously, `--request-id` only surfaced **one** `ApiRequest` row (exact match), so **outbound** OpenAI calls were easy to miss unless you queried SQL manually. The chain section fixes that.

### SQL equivalent (SSMS / diagnostics)

```sql
DECLARE @id NVARCHAR(100) = N'1d5a1cb1-820a-4ee6-9956-dce5820a6a5d';

SELECT ApiRequestID, RequestID, Method, Path, StatusCode, DurationMs, UserID, CreatedDate
FROM log.ApiRequest
WHERE RequestID = @id OR RequestID LIKE @id + N':outbound:%'
ORDER BY ApiRequestID;

-- Business outcome (often large JSON):
SELECT ResponsePayload
FROM log.ApiRequest
WHERE RequestID = @id AND Path = N'/api/form-ai/generate';
```

### Payload size / truncation

`RequestPayload` / `ResponsePayload` on `log.ApiRequest` may be **truncated** or omitted depending on app settings (`ConfigurationService` logging capture flags and max size in `outbound_request_logger.py` / request logger). If `ResponsePayload` is null, check server stdout logs or temporarily relax logging limits in **non-production** only.

---

## What’s in the frontend log bundle (devLogger)

Frontend logs are emitted via `frontend/src/features/builder/utils/devLogger.ts` and downloaded as a **backend-ready batch**:

```json
{
  "sessionId": "sess_...",
  "pageUrl": "http://localhost:3000/...",
  "browserInfo": "Mozilla/5.0 ...",
  "entries": [
    { "ts": 1700000000000, "level": "info", "event": "fieldshell.drag.drop", "payload": { ... } }
  ]
}
```

### Snapshot payloads (key for “what did the UI actually do?”)

Many high-signal events carry a `ComponentSnapshot` from `frontend/src/features/builder/utils/componentSnapshot.ts`, including:
- **Rendered (DOM)**: `bounds`, `objectMetrics.*.rect`, `gridMetrics.*`
- **Normalized (Canvas px)**: `canvasBounds`, `objectMetrics.*.canvasRect`, `canvasMetrics.screenToCanvasRatio`
- **Intent (Props subset)**: `props.objectLayout`, `props.gridLayout`, `props.*WidthOverride`, spacing overrides, etc.

When debugging “it looks wrong”, trust snapshot **Rendered/Normalized** fields first (they match what the user sees).

---

## Event cheat-sheet (what to filter for)

### Toolbox → Canvas (add / drop / placement)
- **pointer math**: `drag.pointer.*`
- **toolbox drops**: `toolbox.component.dropped`, `component.dropped`
- **boundary clamp**: `collision.boundary.*`

### Canvas drag (move existing component)
- **start/grab/drop**: `fieldshell.drag.start`, `fieldshell.drag.grabbed`, `fieldshell.drag.beforeDrop`, `fieldshell.drag.drop`
- **live constraint enforcement**: `fieldshell.collision.constrained`
- **post-drop overlap detection**: `fieldshell.collision.detected` (warn)

### Canvas resize (E/W/N/S + corners + input-only handle)
- **pointer stream**: `resize.pointer.down`, `resize.pointer.move`, `resize.pointer.up`
- **start/preview/commit**: `fieldshell.resize.start`, `fieldshell.resize.preview`, `fieldshell.resize.beforeDrop`, `fieldshell.resize.commit`
- **high-signal calculations**: `resize.width.chain`, `resize.width.comparison`, `resize.preview.edge.position`, `resize.commit.edge.position`
- **constraints/collisions**: `resize.constraints.*`, `resize.collision.*`
- **preview actually applied**: `resize.preview.applied`
- **preview phase + authority**: `resize.preview.phase`, `resize.preview.predicted_vs_settled`
- **boundary-lock lifecycle**: `resize.preview.boundary.lock.created`, `resize.preview.boundary.lock.used`, `resize.preview.boundary.lock.released`
- **settled-preview corrections**: `resize.preview.settled.constrained`
- **commit authority**: `fieldshell.resize.commit` now includes `commitSource`
- **input-only width**: `resize.input.*`

### SmartBorder (what boundary the user *actually* sees)
- `smartborder.calculate.*`, `smartborder.segments.*`, `smartborder.path.calculated`
- during E/W preview: `smartborder.preview.synthetic-segment`

### Layout editors (Properties Panel)
- **Object Layout**: `objectlayout.*`, plus `fieldshell.properties.layout.changed`
- **Grid Layout**: `gridlayout.*`, plus `panel.layout.changed`

### Surface-only visual guides (Toolbox/Canvas parity)
- **TextLengthIndicator**: `canvas.textlength.*`
- **Dropdown sizing guide**: `canvas.dropdown.width.*`
- **Submit button width math**: `button.width.calculated`, `panel.button.width.*`

### Undo/Redo (helps reconstruct “what changed”)
- `history.push`, `history.undo`, `history.redo`

### Sectioned Form AI runs (AI Agent panel)
- `ai.sections.run.start` (logs section ids/titles/hash/size + retry count + transport)
- `ai.sections.run.result` (logs status/terminal reason/attempts + section metadata)
  - includes `postProcessingSummary` with:
    - `changedComponentCount`
    - `changedComponents[]` (`componentId`, `componentType`, `before{x,y}`, `after{x,y}`)
    - `canvasHeightBefore`, `canvasHeightAfter`, `canvasHeightChanged`
  - includes `attemptPostProcessing[]` per attempt for retry-loop diagnostics
- `ai.sections.run.error` (logs failed run config + error message)

---

## Known limitations (important so agents don’t get stuck)

### Form AI traces need the inbound RequestID + chain semantics

Do not assume a single `log.ApiRequest` row per generate. Read **`log.ApiRequest` inbound vs outbound (Form AI, OpenAI)** above and use `--correlation-only` or the SQL `LIKE ':outbound:%'` pattern.

### Backend syncing is opt-in

Frontend logging defaults to local capture only. To store events in `log.FrontendEvent`, set `VITE_LOG_SEND_TO_BACKEND=true` and ensure backend route `/api/v1/logs/frontend` is reachable.

### Surface attribution is not consistently explicit in payloads

Some events are named `canvas.*` but may be emitted from toolbox preview render paths too. Future improvement: add `surface: 'toolbox' | 'canvas' | 'runtime'` consistently to payloads.

---

## Bug report “minimum evidence” checklist (for Component Framework UAT)

- **What surface?** toolbox vs canvas vs runtime preview
- **Component identifiers**: component type + componentId (from Properties debug section if needed)
- **What action?** add/drop, drag, resize handle used (E/W/N/S/NE/etc), grid/object layout edits
- **Attach logs**: downloaded `dev-logs-*.json`
- **If API involved**: include `backend/enhanced_diagnostic_logs.py --limit 10` output (or **`--request-id … --correlation-only`** for Form AI)

---

## See also

- `docs/COMPONENT-FRAMEWORK-REFERENCE.md` (framework contract + parity rules)
- `docs/UNIVERSAL-FIELDSHELL-LOGGING-GUIDE.md` (deeper event taxonomy + snapshot examples)
