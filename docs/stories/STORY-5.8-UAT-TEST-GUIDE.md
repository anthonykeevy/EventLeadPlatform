# Story 5.8 UAT Test Guide — Admin Review & Publish + Activation

**Story:** 5.8  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Updated:** 2026-02-20  
**UAT Status:** PASSED (Phases 0–5)  
**PM Decisions:** `docs/stories/STORY-5.8-PM-DECISIONS.md`  

---

## Overview

This guide walks through a **single consolidated test run** in sequence. Each phase uses a **new form** because publishing changes form state and a published form can't be reused for draft/pending tests. By creating a **Private Event** first with known dates, we control activation windows and unpublish behaviour.

**Test users needed:** Company Admin, Company User (different accounts)

**Flow at a glance:**

| Phase | Form(s) | What you validate |
|-------|---------|-------------------|
| 0 | — | Event + Form Approval Workflow setup |
| 1 | Form 1 | Approve only → Publish; stable URL |
| 2 | Form 2 | Approve & Publish; EVENT_END unpublish |
| 3 | Form 3 | Manual unpublish; unpublished page |
| 4 | Form 1 | Activation window (event dates) |
| 5 | Forms 4, 5 | Direct publish when approval off |

---

## Phase 0: Setup (One-Time)

### 0.1 Create a Private Event

Create an event we will use for all test forms.

| Step | Action | Expected |
|------|--------|----------|
| 0.1a | Log in as **Company Admin** | — |
| 0.1b | Go to **Dashboard** → select your company | Events list shown |
| 0.1c | Click **+ Create Event** | Event creation form opens |
| 0.1d | Create event: **Name:** "UAT 5.8 Test Event" | — |
| 0.1e | Set **Start date:** tomorrow at 12:00 am | — |
| 0.1f | Set **End date:** 2 weeks from tomorrow at 11:59 pm | — |
| 0.1g | Set **Visibility:** Private | — |
| 0.1h | Set **Status:** Published *(aligns with customer messaging: "Event must be published for forms to be active")* | — |
| 0.1i | Save the event | Event appears on Dashboard |

**Why:** Event dates drive activation windows and EVENT_END unpublish (Story 5.8). With known dates we can verify "event ended" and "form active" correctly. Setting Status to Published aligns with customer-facing messaging. *Note: Form activation currently uses StartDate/EndDate only; Event Status parity is a backlog item (Event–Form Workflow Consistency).*

---

### 0.2 Configure Form Approval Workflow

| Step | Action | Expected |
|------|--------|----------|
| 0.2a | Stay as **Company Admin** | — |
| 0.2b | On Dashboard, select your company, click **Settings** (gear icon) | Company Settings opens |
| 0.2c | In the sidebar, click **Form Approval Workflow** | Form Approval Workflow page |
| 0.2d | Enable **Enforce demo test requirement** | — |
| 0.2e | Set **Required demo runs:** 3 | — |
| 0.2f | Enable **Require publish approval** | — |
| 0.2g | Set **Form cost threshold ($):** 100 (or leave empty to disable cost gate) | — |
| 0.2h | Save | Settings saved |

**Result:** Company Users must complete 3 test runs and request publish; Company Admins approve.

---

## Phase 1: Approve Only Then Publish (DC1, DC2)

Uses **Form 1**. Outcome: Approve-only flow and stable public URL.

### 1.1 Create Form 1 as Company User

| Step | Action | Expected |
|------|--------|----------|
| 1.1a | Log out, log in as **Company User** | — |
| 1.1b | On Dashboard, expand **UAT 5.8 Test Event** | Forms section visible |
| 1.1c | Click **+ Form** | Create form dialog |
| 1.1d | Create form: **Name:** "Form 1 – Approve Only Test" | — |
| 1.1e | Link form to **UAT 5.8 Test Event** | — |
| 1.1f | Add at least one component (e.g. text field), save | Form in Draft |
| 1.1g | Open form in Builder, submit 3 demo runs (use preview + record test run or equivalent) | Readiness: "Ready to publish" |
| 1.1h | Click **Request Publish** (Builder, Edit Form, or Form Detail) | Publish request submitted |

**Expected:** Form status → **Pending Admin Review**. Pending Publish Requests card (Admin view) shows the form.

---

### 1.2 Admin: Approve Only

| Step | Action | Expected |
|------|--------|----------|
| 1.2a | Log out, log in as **Company Admin** | — |
| 1.2b | On Dashboard, see **Pending Publish Requests** with Form 1 | Card visible |
| 1.2c | Click **Review & Publish** (or open `/forms/{formId}/review`) | FormReviewPage opens |
| 1.2d | Verify two options: **Approve only** and **Approve & Publish** | Both visible (DC1) |
| 1.2e | Click **Approve only** | Success message; form stays ready to publish |
| 1.2f | Verify form is NOT yet published (no public URL in Dashboard) | FormPublicLink not created (DC1.3) |

---

### 1.3 Admin: Publish Form 1

| Step | Action | Expected |
|------|--------|----------|
| 1.3a | On FormReviewPage (or form detail), click **Publish** | Publish modal opens |
| 1.3b | Select unpublish mode **Manual** | — |
| 1.3c | Confirm publish | Form → **Published** |
| 1.3d | Open production URL in new tab | Form loads (DC2) |
| 1.3e | Submit a response via public URL | Submission recorded (DC2.4) |

**Form 1 is now published.** Keep the URL for later. Do not unpublish yet if you will reuse for Phase 4 (activation window).

---

## Phase 2: Approve & Publish (DC1.5, DC2)

Uses **Form 2**. Outcome: Single-step approve-and-publish.

### 2.1 Create Form 2 and Request Publish

| Step | Action | Expected |
|------|--------|----------|
| 2.1a | Log in as **Company User** | — |
| 2.1b | Create **Form 2 – Approve and Publish Test** under UAT 5.8 Test Event | — |
| 2.1c | Add component, save; complete 3 demo runs | Ready to publish |
| 2.1d | Click **Request Publish** | Form → Pending Admin Review |

---

### 2.2 Admin: Approve & Publish

| Step | Action | Expected |
|------|--------|----------|
| 2.2a | Log in as **Company Admin** | — |
| 2.2b | Open FormReviewPage for Form 2 | — |
| 2.2c | Select unpublish mode **Event end date** (event already linked) | Event end date shown |
| 2.2d | Click **Approve & Publish** | Form published immediately (DC1.5) |
| 2.2e | Verify production URL created; copy and open in new tab | Form loads (DC2) |
| 2.2f | On Dashboard, verify "Will unpublish on [event end date]" badge | Visible (DC5) |

**Form 2 is now published** with EVENT_END unpublish mode.

---

## Phase 3: Unpublish Modes and Manual Unpublish (DC3, DC4, DC5, DC6)

Uses **Form 3**. Outcome: Unpublish modes, manual unpublish, unpublished page.

### 3.1 Create and Publish Form 3

| Step | Action | Expected |
|------|--------|----------|
| 3.1a | As **Company User**, create **Form 3 – Unpublish Test** under UAT 5.8 Test Event | — |
| 3.1b | Complete 3 runs, Request Publish | — |
| 3.1c | As **Company Admin**, open FormReviewPage for Form 3 | — |
| 3.1d | Select unpublish mode **Schedule**; set unpublish date to tomorrow | — |
| 3.1e | Click **Approve & Publish** | Form published |
| 3.1f | Note production URL; verify "Will unpublish on [date]" on Dashboard | (DC3, DC5) |

---

### 3.2 Manual Unpublish and Unpublished Page

| Step | Action | Expected |
|------|--------|----------|
| 3.2a | As **Company Admin**, open FormReviewPage for Form 3 | Production URL + copy visible (DC6) |
| 3.2b | Click **Unpublish** | Form → Unpublished (DC4) |
| 3.2c | Open same production URL (as visitor or incognito) | "Form unpublished" page (no 404) (DC4.3) |
| 3.2d | Verify "Request admin to publish again" CTA | Visible (DC4.4) |
| 3.2e | (Optional) Click CTA | In-app notification to Admins (DC4.5) |
| 3.2f | On Dashboard, verify form shows Unpublished; production URL no longer active | — |

---

## Phase 4: Activation Window (DC9)

Uses **Form 1** (or Form 2) — already published and linked to Event. Outcome: Form served when event active; "event ended" when outside window.

### 4.1 Event Within Window

| Step | Action | Expected |
|------|--------|----------|
| 4.1a | Ensure UAT 5.8 Test Event has **End date in the future** | — |
| 4.1b | Open Form 1 (or 2) production URL | Form loads (DC9.1) |

---

### 4.2 Event Ended

| Step | Action | Expected |
|------|--------|----------|
| 4.2a | As **Company Admin**, edit **UAT 5.8 Test Event** | — |
| 4.2b | Set **End date** to yesterday | Event in the past |
| 4.2c | Save event | — |
| 4.2d | Open Form 1 production URL | "Event ended" or similar (no form) (DC9.2) |

---

### 4.3 Event Not Yet Started

| Step | Action | Expected |
|------|--------|----------|
| 4.3a | Edit event: set **Start date** to next week, **End date** to 2 weeks after | Event in future |
| 4.3b | Save | — |
| 4.3c | Open Form 1 production URL | "Event ended" or "Not yet active" (DC9.3) |

---

### 4.4 Event Within Window Again

| Step | Action | Expected |
|------|--------|----------|
| 4.4a | Edit event: set **Start date** to yesterday, **End date** to next week | Event currently active |
| 4.4b | Save | — |
| 4.4c | Open Form 1 production URL | Form loads (DC9.4) |

---

## Phase 5: Direct Publish (No Approval) — DC7, DC10

Uses **Form 4** and **Form 5**. Outcome: When approval is off, users publish directly; approval UI is hidden.

### 5.1 Turn Off Approval

| Step | Action | Expected |
|------|--------|----------|
| 5.1a | As **Company Admin**, open **Company Settings** → **Form Approval Workflow** | — |
| 5.1b | Disable **Require publish approval** | — |
| 5.1c | Save | — |

---

### 5.2 Verify Approval UI Hidden (DC10)

| Step | Action | Expected |
|------|--------|----------|
| 5.2a | View Dashboard as **Company Admin** | **Pending Publish Requests** card NOT visible (DC10.2) |
| 5.2b | Log in as **Company User** | — |
| 5.2c | Open a Draft form (or create Form 4) | No "Request Publish" — **Publish** button only (DC10.3) |
| 5.2d | Form Approval Workflow page in Settings | Still visible; setting can be changed (DC10.5) |

---

### 5.3 Direct Publish as Admin (DC7)

| Step | Action | Expected |
|------|--------|----------|
| 5.3a | As **Company Admin**, create **Form 4 – Direct Publish Admin** under event | — |
| 5.3b | Add component, complete 3 runs | Ready |
| 5.3c | Click **Publish** (not Request Publish) | Direct publish flow |
| 5.3d | Publish with Manual unpublish | Form published; FormPublicLink created (DC7.2) |

---

### 5.4 Direct Publish as Company User (DC7)

| Step | Action | Expected |
|------|--------|----------|
| 5.4a | As **Company User**, create **Form 5 – Direct Publish User** | — |
| 5.4b | Add component, complete 3 runs | Ready |
| 5.4c | Click **Publish** directly | Form published (DC7.3) |
| 5.4d | Verify no Request Publish flow | Direct Publish only (DC7.4) |

---

### 5.5 Restore Approval (Optional)

| Step | Action | Expected |
|------|--------|----------|
| 5.5a | As **Company Admin**, re-enable **Require publish approval** | For future testing |

---

## Pass Checklist

Use this to record results:

| Phase | Outcome | Pass? |
|-------|---------|-------|
| **0** | Event created with known dates; Form Approval Workflow configured | ☑ |
| **1** | Approve only → Publish; stable public URL; submission works | ☑ |
| **2** | Approve & Publish; EVENT_END unpublish mode; Dashboard badge | ☑ |
| **3** | SCHEDULED unpublish; manual Unpublish; unpublished page (no 404); CTA | ☑ |
| **4** | Activation: form when in window; "event ended" when outside | ☑ |
| **5** | RequirePublishApproval=false: approval UI hidden; Admin + User direct publish | ☑ |

**DC8** (in-app reminders): Dashboard "Will unpublish on [date]" is checked in Phases 2 and 3. Queue items (7 days/1 day before) — verify if implemented, or note N/A.

**All phases pass** = UAT PASSED ✅ (2026-02-20)

---

## Form Summary

| Form | Purpose |
|------|---------|
| Form 1 | Approve only → Publish; also used for activation window (Phase 4) |
| Form 2 | Approve & Publish with EVENT_END unpublish |
| Form 3 | SCHEDULED unpublish; manual unpublish; unpublished page |
| Form 4 | Direct publish as Admin (RequirePublishApproval=false) |
| Form 5 | Direct publish as Company User (RequirePublishApproval=false) |

---

## References

- Story: `docs/stories/story-5.8.md`
- PM decisions: `docs/stories/STORY-5.8-PM-DECISIONS.md`
- Unified workflow: `docs/UNIFIED-APPROVAL-WORKFLOW-IDEA.md`
- Public resolver: `backend/modules/forms/public_form_router.py`
