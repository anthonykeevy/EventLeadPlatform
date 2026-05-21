# Epic 6 Carry-Forward Backlog

**Purpose:** Central registry of items deferred from Epic 6 stories that have not yet found a home. Each row has an ID, severity, source story, and a suggested home. Items are removed when they are either (a) resolved, or (b) explicitly absorbed into a new story's scope.

**Owner:** SM. Updated at every story closeout — Dev appends new items via `STORY-6.x-CLOSEOUT-REPORT.md` §5; SM merges them here at the housekeeping commit before the merge gate.

**Convention:** Severity = P1 (must reach pre-prod or pre-revenue checklist), P2 (should land in next 1–2 stories), P3 (nice-to-have, can wait), P4 (informational only).

---

## Active items

| ID | Description | Severity | Source story | Suggested home | Notes |
|----|-------------|----------|--------------|----------------|-------|
| `g-64-http2-prod` | **Production infra requirement: HTTP/2 (or AI subdomain).** Under HTTP/1.1 the browser allows ~6 concurrent connections per origin. The AI generation request (up to 20 min) occupies one slot; if the dashboard or other pages make 5+ simultaneous requests they queue behind it, causing partial renders. **Two acceptable resolutions:** (a) confirm the production host (nginx / Azure APIM / etc.) terminates HTTP/2 — multiplexing means one long request never blocks others; or (b) expose `/api/form-ai/*` on a separate subdomain (e.g. `api-ai.`) so it draws from its own connection pool. Cancel button + AbortController (shipped in 6.4) handle explicit-cancel and explicit-navigate-away cases, but do not fire when the form builder component is kept alive in memory during a soft route change. That gap is benign once HTTP/2 is in place. | **P1 infra** | 6.4 (UAT-surfaced) | **Pre-production infrastructure checklist** (must be confirmed before first paid customer). Owner: Tonyk + ops. | Discovered during 6.4 UAT Round 3 §4.1.4. Symptom is queueing, not failure — easy to forget until prod traffic exposes it. |
| `g-frontend-submit-parity` | Submit-button validation parity (design pill ↔ preview summary). When a form has validation issues, the design-time pill and the preview-mode summary should describe them identically. They currently drift in edge cases. | **P2 polish** | 6.3.1 (carry-forward), confirmed not promoted in 6.4 | Story 6.5 frontend pass *(or 6.4.1 micro-story if 6.5 lead doesn't naturally touch the validation surface)* | Originally tagged as a candidate for an optional 6.4.1 micro-story. Did not surface naturally during 6.4 polish work, so still parked. |
| `g-64-pref-cache` | `GET /api/me/preferences` hits the DB on every call. Consider a short-lived per-request cache or ETag if the endpoint is called frequently from multiple panels (it is currently called by `AIAgentPanel` mount and `NotificationsSettingsPopup` mount; will grow as preferences proliferate). | **P3 performance** | 6.4 | Backend infrastructure pass *(no urgency until perf data justifies)* | Cache invalidation has to consider the multi-worker AppSetting cache pattern from 6.4 (each worker caches independently). |
| `g-64-theme-pref-keys` | `ref.UserPreferenceCategory` rows for "Theme" and "Account" are seeded but have no `ref.UserPreferenceKey` rows yet. Keys should follow when the related preference UI is designed (e.g. compact-mode toggle, default-canvas-zoom, email-receipt opt-out). | **P3 backlog** | 6.4 | Story X (theme/account preference screens — TBD) | The architecture is in place; this is purely a content/seed exercise gated on UX decisions about which prefs to expose. |
| `g-6441-company-brand-settings-ui` | Company-level `BrandPosture` and `BrandHeritageOrigin` columns are backend-only. Add Company Settings UI and validation copy before exposing self-service brand posture overrides. | **P2 product** | 6.4.4.1 | Company settings UX story | API/runtime fallback works without UI; default remains AppSetting-driven. |
| `g-6441-native-speaker-review` | Locale block seeds for DE/JP/FR cultural dimensions are present as native-review stubs; production prompt wording for these markets needs native-speaker review before exposure. | **P2 content** | 6.4.4.1 | Locale expansion story | MVP runtime exposes AU/NZ/UK/US/CA/IE/INTL/EU; DE cultural dimensions are seeded for future extension. |
| `g-6441-per-form-locale-dropdown` | Builder currently passes nullable locale/posture fields and relies on backend resolution. Add per-form locale and brand posture override UX later. | **P3 UX** | 6.4.4.1 | Builder settings story | No UI redesign in 6.4.4.1 by constraint. |
| `g-65-catalog-drift` | Seed missing `FormBuilderComponent` rows (`rating`, `url`, `file-upload`, `paragraph`, `address`) + AU `address-lookup-au`; formal add-component checklist; alignment automation. | **P1 catalog** | 6.5c closeout §3 | **Story 6.5d** (Track A) | Absorbed into 6.5d scope 2026-05-21; remove row when 6.5d merges. |

---

## Recently resolved (kept for one cycle for traceability)

| ID | Description | Resolved by | Date |
|----|-------------|-------------|------|
| `g4b-second-pass-rows` | Carry-forward from 6.3.1 about second-pass row layout. | Absorbed into deterministic compiler architecture — no longer applicable | 2026-04-15 |
| `g-doc` | Carry-forward from 6.3.1 about documentation gaps. | Folded into PR #65 workflow guide updates | 2026-04-23 |
| `g-backlog-dropdown-font` | Carry-forward from 6.3.1 about dropdown font sizing. | No regressions observed during 6.4 UAT Round 3; demoted to P4 watchlist; remove if still clean after 6.5 | 2026-04-24 |

---

## How items get added here

1. Dev's closeout report (`STORY-6.x-CLOSEOUT-REPORT.md`) has a §5 **Carry-forward backlog** table listing any new items with ID, description, severity, suggested home.
2. At the SM closeout audit (before the human merges the story PR), SM merges those rows into this file's **Active items** table.
3. SM also reviews **Active items** to flag any new "suggested homes" if a future story now seems like a natural fit.
4. P1 items must additionally be cross-posted to whichever external checklist matches their domain (e.g. pre-production infra checklist, pre-revenue legal checklist) — a row here alone is not sufficient for P1.

---

*Created 2026-04-24 by SM during Story 6.4 closeout audit, fulfilling the PM's recommendation in PR #65.*
