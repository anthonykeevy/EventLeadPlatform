# Agent Logging Guide (Component Framework + Builder UI)

**Purpose:** Help agents (and UAT testers) quickly capture and interpret **what the user did** and **what the UI rendered** for Component Framework issues across **Toolbox / Canvas / Properties** (including **Grid Layout** + **resize**).

**Primary reference:** `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

---

## Quick Start (most common workflow)

### 1) Enable frontend dev logs

Create/update `frontend/.env.local` (or `frontend/.env`) with:

```bash
VITE_ENABLE_DEV_LOGS=true
# Optional: mirrors debug/info logs to console (resize + SmartBorder are noisy)
VITE_LOG_VERBOSE_RESIZE=false
```

Restart the Vite dev server after editing env vars.

### 2) Reproduce the bug and download the log bundle

In the Builder UI header you should see **“Dev Logs”** (download button). After reproducing the issue, click it and attach the JSON file to the bug report.

**Optional local persistence:** if you also set `VITE_LOG_PERSIST_TO_STORAGE=true`, logs are persisted to **browser localStorage** for the current browser tab session. This helps if the page reloads mid-debug.

### 3) If the bug might involve backend/API

Use the backend diagnostic tool to collect recent API/auth/error context:

```bash
python backend/enhanced_diagnostic_logs.py --limit 50
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

### Useful CLI options (focused modes)
- `--limit / -l`: rows per table (default 5)
- `--request-id / -r`: correlation analysis for a specific request
- `--performance-hours / -p`: time window for performance metrics
- `--path-filter`: only show API requests matching a path pattern
- `--no-theme-requests`: hide profile/theme enhancement request section

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

---

## Known limitations (important so agents don’t get stuck)

### No backend syncing (by design for now)

This logging is currently **local-only** (browser storage + JSON download). Backend syncing/DB storage is intentionally deferred to a future epic.

### Surface attribution is not consistently explicit in payloads

Some events are named `canvas.*` but may be emitted from toolbox preview render paths too. Future improvement: add `surface: 'toolbox' | 'canvas' | 'runtime'` consistently to payloads.

---

## Bug report “minimum evidence” checklist (for Component Framework UAT)

- **What surface?** toolbox vs canvas vs runtime preview
- **Component identifiers**: component type + componentId (from Properties debug section if needed)
- **What action?** add/drop, drag, resize handle used (E/W/N/S/NE/etc), grid/object layout edits
- **Attach logs**: downloaded `dev-logs-*.json`
- **If API involved**: include `backend/enhanced_diagnostic_logs.py --limit 10` output

---

## See also

- `docs/COMPONENT-FRAMEWORK-REFERENCE.md` (framework contract + parity rules)
- `docs/UNIVERSAL-FIELDSHELL-LOGGING-GUIDE.md` (deeper event taxonomy + snapshot examples)
