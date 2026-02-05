# UAT Results: T09

**Story:** 3.11  
**Task:** Integration + UAT Polish (Scenarios 1–10)  
**Date:** 2026-02-05  
**Tester:** Automation (Cursor MCP)

---

## Scenario Results

| Scenario | Result | Notes |
|----------|--------|-------|
| 1 — Online submit uploads immediately | ✅ PASS | Success banner shown; fields cleared. |
| 2 — Offline submit queued | ✅ PASS | Offline banner shown; outbox pending count increased. |
| 3 — Queue survives reload | ✅ PASS | Manual offline reload confirmed queued item persisted. |
| 4 — Reconnect triggers auto-sync | ✅ PASS | Pending item processed after online event; outbox pending count returned to 0. |
| 5 — Backend down while online | ✅ PASS | Simulated upload failure queued; restore synced to success. |
| 6 — Idempotency (no duplicates) | ✅ PASS | Replay returned `status: "DUPLICATE"` for same idempotency key. |
| 7 — Invalid/expired token | ✅ PASS | UI shows “Unable to open form / Invalid form link.” |
| 8 — Shared-device safety (clear fields) | ✅ PASS | Fields cleared after online and offline captures. |
| 9 — Validation telemetry | ✅ PASS | Validation errors shown; telemetry POST observed; no outbox item created. |
| 10 — Kiosk session rotation | ✅ PASS | Same device ID, different session IDs across two kiosk submissions. |

---

## Evidence Highlights

- **Idempotency:** `POST /api/public/forms/{token}/submissions` returned `{ status: "DUPLICATE" }`.
- **Validation telemetry:** Network request observed to `/api/public/forms/{token}/telemetry/validation`.
- **Kiosk rotation:** Outbox items show same `clientDeviceId` with different `clientSessionId`.

---

## Blocking Issue

- None.
