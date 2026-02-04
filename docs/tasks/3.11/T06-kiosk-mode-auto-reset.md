# Task T06: Kiosk Mode (Optional) - Auto-reset + Countdown + Session Rotation

**Story:** 3.11 - Dynamic Submission (Outbox)  
**Task ID:** T06  
**Status:** ⏳ Ready  
**Dependencies:** T05  
**Estimated Time:** 1-2 hours  

---

## 📋 Task Overview

**Objective:** Add an **optional kiosk mode** for public renderer sessions to improve shared-device safety:

- Auto-reset the form after a configurable timeout
- Show a visible countdown warning before reset
- Rotate `clientSessionId` on reset / new session cycle

This complements T05’s clear-after-capture behavior by handling the “user walks away mid-entry” scenario.

---

## ✅ Preconditions

- T05 is merged (renderer submit + clear-after-capture exists).
- Public renderer loads via `PublicFormRendererPage`.

---

## ✅ Scope (In)

- Add kiosk mode enablement (organiser-controlled; UI wiring deferred):
  - **Initial approach:** query params on the public renderer link, e.g.:
    - `?kiosk=1`
    - `&autoResetSeconds=30`
    - (optional) `&countdownSeconds=10`
- When kiosk mode is enabled:
  - Start an inactivity timer after any meaningful user interaction (field change, focus/typing)
  - When the timer reaches the countdown window:
    - show a visible countdown banner/notice: “Resetting in 10s…”
  - When timer expires:
    - clear all values
    - clear validation UI
    - clear any submit notice
    - rotate `clientSessionId` (new session)
- Ensure manual “Reset” triggers the same kiosk reset behavior when kiosk mode is enabled (including session rotation).

---

## 🚫 Scope (Out)

- UI settings to configure kiosk mode in the dashboard/builder (future story)
- Device fingerprinting (forbidden)
- Advanced session analytics (future)

---

## 🔒 Forbidden Zones

| Path | Reason |
|------|--------|
| `frontend/src/features/builder/**` | Builder is out of scope |
| `frontend/src/features/auth/**` | Public flow must remain auth-free |

---

## ✅ Acceptance Criteria

- **AC1:** When `kiosk=1` and the user is inactive for `autoResetSeconds`, the form clears and validation state resets.
- **AC2:** A visible countdown appears during the final `countdownSeconds` before reset.
- **AC3:** `clientSessionId` changes on kiosk reset (and on manual reset when kiosk mode enabled).
- **AC4:** When kiosk mode is disabled, existing behavior is unchanged.

---

## 🧪 Verification / Evidence (Agent-owned)

Minimum automated checks (frontend):

```powershell
cd frontend
npm run lint
npm run build
```

Manual UAT (suggested):
- Open public link with `?kiosk=1&autoResetSeconds=10&countdownSeconds=5`
- Start entering values, then stop interacting
- Verify countdown appears and form clears after timeout

---

## Git / PR (Mandatory)

- Branch: `task/3.11/T06-kiosk-mode-auto-reset`
- PR: task → `story/epic3-3.11-dynamic-submission`

