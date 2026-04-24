# Story 6.4 — UAT Results

**Story:** 6.4 — AI Agent Panel Production Polish + User Preferences Architecture Foundation  
**UAT Owner:** Anthony  
**Date:** 2026-04-24  
**Final verdict:** ✅ PASS

---

## Round 1 — Foundation (§2) · PASS

| Section | Result | Notes |
|---------|--------|-------|
| §2.1 Schema | PASS | Tables created; seed rows present |
| §2.2 Read API | PASS | GET returns categories + entries; default fallback confirmed |
| §2.3 Write API | PASS | PATCH with valid key writes; invalid key / type mismatch returns 4xx; no partial writes |
| §2.4 Reset API | PASS | DELETE soft-deletes; GET returns default |
| §2.5 Notifications UI | PASS | Notifications section renders; toggles work; optimistic update visible |
| §2.6 Extensibility (AC-15) | PASS | Second demo preference (`show_compile_summary`) auto-rendered with no frontend code change |
| §2.7 Architecture doc (AC-16) | PASS | `docs/USER-PREFERENCES-ARCHITECTURE.md` exists and reviewed |

---

## Round 2 — AI Agent Panel Polish (§3) · PASS

| Section | Result | Notes |
|---------|--------|-------|
| §3.1 Last prompt persistence (AC-1) | PASS | Prompt restored after exiting form and returning |
| §3.2 Replace-form warning (AC-2/3/4) | PASS | Modal appeared on non-empty canvas; "don't show again" suppressed future modals; Notifications toggle restored warning; empty canvas skipped modal |
| §3.3 Transport selector hidden (AC-5) | PASS | `<select>` not rendered; resolved transport still shown in trace |
| §3.4 Retry input hidden (AC-6) | PASS | Input not rendered; `maxSystemCorrectionAttempts` absent from network payload |
| §3.5 Silent autoload (AC-7/8) | PASS | Soft-validation draft applied automatically; hard failure showed error message |

---

## Round 3 — Regression + Hygiene (§4) · PASS

| Section | Result | Notes |
|---------|--------|-------|
| §4.1.1 Backend pytest | PASS | 41 new tests pass; baseline preserved |
| §4.1.2 Frontend test:unit | PASS | 283 tests pass (28 files); baseline preserved |
| §4.1.3 Story 6.3.1 smoke | PASS | Generation + deterministic compiler + canvas output working |
| §4.1.4 Existing surfaces smoke | PASS | Theme/Account settings, login/logout functional |
| §4.2.1 Architecture doc | PASS | Exists and reviewed |
| §4.2.2 Migration count | PASS | 4 files: 058 DDL + 059 categories + 060 keys + 061 AppSetting seed |
| §4.2.3 Closeout report | PASS | `STORY-6.4-CLOSEOUT-REPORT.md` complete |
| §4.2.4 Gate evidence | PASS | `STORY-6.4-GATE-EVIDENCE.md` complete |

---

## Observations / Carry-forward

**Transient collision on first run (not a bug):**  
On the first generation during UAT, two collisions were observed on a form containing Radio and Option components. DevTools showed the `/api/form-ai/remeasure` call was not visible at the time. On re-run, remeasure completed and the form had no collisions. Root cause: under the HTTP/1.1 local dev server the AI generation request occupies one of ~6 browser connection slots; remeasure (which fires after generate returns) was queued briefly. This is benign — tracked as `g-64-http2-prod` (P1 infra carry-forward). The Cancel button aborts correctly on explicit click. Navigate-away during generation (soft route change) does not fire the unmount signal — also documented in the carry-forward.

---

**Sign-off**

```
Round 1 (foundation): PASS  Date: 2026-04-24
Round 2 (polish):     PASS  Date: 2026-04-24
Round 3 (regression): PASS  Date: 2026-04-24
Final UAT PASS:       PASS  Date: 2026-04-24
```
