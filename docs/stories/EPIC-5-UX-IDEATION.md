# Epic 5 UX Ideation - Form Builder Readiness + Review & Publishing (Preview/Test/Publish)

**Epic:** 5  
**Status:** 📝 Draft (ideation artifact; evolves during Epic 5)  
**Created:** 2026-02-06  
**Owner:** UX + PM + Dev (shared)  

---

## Why this exists

Epic 5 spans **two primary surfaces**:

- **Dashboard** (management + visibility + approvals)
- **Builder** (creation + testing actions)

This document captures the **minimum viable user journeys + screen map** so Epic 5 delivers clear customer value without a long UAT thrash cycle.

Primary references:
- PRD publish request flow: `docs/prd.md` (“Create Form & Request Publish”)
- Epic scope: `docs/stories/EPIC-5-STATUS.md`
- Optional UX concept: `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`

---

## Personas (Epic 5)

### Company User (builder/marketer)
- Builds forms for an event
- Runs preview tests to confirm the form behaves correctly
- Cannot publish directly → requests publish from an admin
- Needs clear feedback loop when admin requests changes

### Company Admin (manager/ops)
- Wants visibility from the dashboard: “Which forms are ready / blocked / live?”
- Reviews publish requests
- Validates the form quickly (review mode) and publishes/unpublishes
- Owns operational settings (activation windows; company-level test threshold overrides)

---

## UX principle: “Dashboard-first management”

Management-level staff should be able to complete most of their Epic 5 work **without opening the builder**:
- See readiness and publish state at a glance
- Review requests and publish/unpublish
- Copy production link and confirm activation status

The builder remains the place to **edit** and **run tests**.

---

## Builder Readiness UX (Phase A — Foundation)

Epic 5 starts with “Form Builder Readiness” (assets + defaults + schema parity). UX implications we must design up front:

### Background assets (no embedded base64)
- Backgrounds should be selected from a **company asset library** (or uploaded into it).
- Builder should clearly communicate:
  - The image is stored as an **asset** (reusable) and referenced by the form (not embedded into JSON).
  - Replace/remove actions are safe and reversible.
- Recommended interaction:
  - “Choose background…” opens an **Asset Picker** (Upload new / Select existing / Search).
- Placement behaviors (production expectations):
  - Background placement supports **cropping** (negative offsets allowed; canvas clips the image).
  - Enforce an **intersection rule**:
    - If the image is fully off-canvas → it is **auto-removed from the canvas**.
    - The asset remains available in the library, so the user can re-add it (and ideally an Undo also restores it).

### Company-level brand defaults (set once, inherit everywhere)
- Defaults should be managed in **Dashboard** (Company Settings → “Form Branding Defaults”).
- Builder should surface “inherited vs overridden”:
  - Show inherited values (read-only) with an “Override” action
  - Provide a link: “Edit company defaults” (opens dashboard settings)

---

## Screen map (minimum viable)

### Dashboard
1. **Company Dashboard** (events list)
2. **Event Dashboard** (forms list per event)
   - Form card/table shows:
     - Status badge (Draft / Pending Review / Published / Unpublished)
     - Readiness indicator (Preview tests \(X/Y\), last tested)
     - Primary actions (open builder, request publish / review, copy link if published)
3. **Admin Review Queue** (can be embedded in Event Dashboard or separate page)
   - List of pending publish requests
   - Deep link into “Review and Publish”
4. **Company Settings: Form Branding Defaults** (Phase A)
   - Set fonts/colors/typography/spacing defaults once
   - Explains inheritance rules (company → form → component)
5. **Form Management / Detail (optional)**
   - Activation window summary
   - Production URL/token display (copy)
   - Preview vs Production submission filters (minimal hygiene)

### Builder
6. **Builder (Draft editing)**
   - Header includes Preview/Production toggle + test counter + publish CTA
   - Background panel uses **Asset Picker** (Phase A)
7. **Review Mode (Admin)**
   - Uses the preview runtime (read-only)
   - Actions: Request changes / Decline / Publish / Unpublish

### Notifications (entry points)
8. **In-app notifications/queue** (minimum viable)
9. **Email notification** (optional; can be added later)

---

## Builder header: key interactions (Epic 5)

### Preview vs Production mode
- Always visible “mode chip” (e.g., **Preview** / **Production**).
- Switching modes changes:
  - What URL is shown for sharing/testing
  - How submissions are tagged (preview vs production)

### Readiness indicator (test threshold)
- Preview testing is **configurable** (company can enable/disable; threshold adjustable).
- If enabled: “Preview tests: \(X/Y\)” is visible.
  - If \(X < Y\): Publish CTA is disabled (admin) or becomes “Request publish” but shows warning
  - Helper text: “Run \(Y - X\) more preview tests to publish.”
- If disabled: show a compact state (e.g., “Testing: Off”) and do not block publish.
- Static/no-input forms:
  - Provide a “Record test run” action so tests are not dependent on having inputs/submission.

### Publish CTA (role aware)
- Company User:
  - If approval workflow is enabled: CTA label **Request Publish**
    - Opens modal: select admin(s) + optional message
    - After sending: show persistent state “Pending Admin Review”
  - If approval workflow is disabled: CTA label **Publish** (subject to test gating if enabled)
- Company Admin:
  - CTA label: **Publish**
  - If blocked by tests: disable with clear reason + quick link to run a preview test
  - If allowed: publish (payment deferred to Epic 6; do not block UX on Stripe here)

---

## Journey 0 (primary): Solo operator (Company Admin) publishes directly

Most small customers will have a **single user** in the company. In that case the user is a **Company Admin** and should be able to build and publish without any “request approval” friction.

1. Admin creates event → opens builder → builds the form.
2. Admin selects background via Asset Picker and relies on inherited company defaults (optional).
3. Admin runs preview tests **if the company has testing enabled** (or records test runs for static forms).
4. Admin clicks **Publish**.

---

## Journey 1: Company User (build → test → request publish)

> This journey is the **separation-of-duties** scenario and should be treated as **optional**. It applies when a company has multiple users and enables publish approval.

1. From **Event Dashboard**, user clicks **Create Form** → opens Builder.
2. User builds the form (auto-saved; status = Draft).
3. User chooses a background via **Asset Picker** (upload/select existing).
4. User relies on **inherited company brand defaults** (or overrides per-form if needed).
5. User switches to **Preview** and runs tests until “Preview tests: \(X/Y\)” meets threshold (or records test runs for static forms).
6. User clicks **Request Publish**.
7. Modal:
   - “Only Company Admins can publish forms.”
   - Select admin(s)
   - Optional message
8. Success:
   - Builder shows “Pending Admin Review”
   - Event Dashboard shows badge “Pending Review” with readiness “\(X/Y\) tests complete”
9. If admin requests changes:
   - User sees “Changes requested” message and a link back to builder

---

## Journey 2: Company Admin (review queue → review → publish/unpublish)

1. Admin opens **Dashboard** and sees:
   - Pending publish requests count
   - Event Dashboard form cards flagged “Pending Review”
2. Admin opens a publish request (Review Queue → “Review and Publish”).
3. Admin lands in **Review Mode**:
   - Read-only runtime preview
   - Shows readiness state (tests \(X/Y\), last tested)
4. Admin chooses:
   - **Request changes** (writes note; request remains pending)
   - **Decline** (writes note; request closed; form remains draft)
   - **Publish** (status becomes Published; production URL displayed in dashboard)
5. Post-publish:
   - Event Dashboard shows Published badge + Copy Link action
   - Activation window status visible (active / scheduled / ended)
6. Admin can **Unpublish** (immediate offline) if needed.

---

## Status badges (customer-facing)

Minimum set:
- **Draft**
- **Pending Admin Review**
- **Published**
- **Unpublished**

Each status must be visible in:
- Event Dashboard (forms list)
- Builder header (for the current form)

---

## Open questions (to resolve during Story 5.1–5.3)

1. **What counts as a “preview test”?**
   - Option A: “preview submission recorded” increments count
   - Option B: explicit “Mark test complete” action in preview mode
2. **Where does the admin review happen?**
   - Standalone review page (preferred) vs entering builder in read-only mode
3. **Where do we configure the threshold override?**
   - Company settings vs per-event override
4. **Notifications**
   - In-app only (MVP) vs email (nice-to-have)
5. **Approval + testing toggles**
   - Company-level switches:
     - Require publish approval (request/review) vs allow direct publish
     - Require preview testing vs testing off
     - Minimum tests required (when enabled)
5. **Asset library UX**
   - Company-wide library vs event-scoped library vs per-form assets
   - Deletion semantics (soft delete; “used by X forms” warning)

---

## Non-goals (explicit)

- Payments/Stripe UX (Epic 6)
- Deep analytics dashboards (Epic 7)
- Real-time co-editing collaboration (Epic 4 advanced)

---

*Epic 5 UX Ideation - Draft*  
*Last Updated: 2026-02-07*

