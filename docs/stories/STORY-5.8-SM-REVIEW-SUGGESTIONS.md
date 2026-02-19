# Story 5.8 — SM Review Suggestions

**From:** Bob (Scrum Master)  
**Date:** 2026-02-18  
**Status:** Suggestions for PM/dev to incorporate before or during implementation  

---

## Story (story-5.8.md)

- **"Ready to publish" state:** Clarify what state the form is in after "Approve only" (new `FormStatus`, `PENDING_REVIEW` with an approved flag, or something else).
- **DC2:** Make "public URL works" concrete (e.g. "form loads in public view and submissions are recorded").
- **DC4:** ~~Decide whether the public URL returns 404 or a "form unavailable" message~~ **Resolved:** PM decision — dedicated page (no 404) with "Request admin to publish again" CTA; CTA → in-app notification to all Company Admins.
- **DC3 & DC9:** Add behaviour when Form has no linked Event (disable EVENT_END, block activation window, or define fallback).
- **Default unpublish mode:** Specify the default when publishing (e.g. MANUAL) and whether the user must choose.
- **Auto-unpublish:** Explicitly include or exclude a background job/cron for SCHEDULED and EVENT_END; if in scope, add a DC.
- **"Form detail":** Replace with specific page/route, or drop it and keep FormReviewPage + Dashboard.
- **Test threshold:** Clarify what it is and where it is defined (e.g. CompanyFormTestConfig).
- **Prerequisite:** Story says 5.6; UAT says 5.6 and 5.7. Align or explain.

---

## Context (story-context-5.8.xml)

- **Form without Event:** Add how to handle EVENT_END and activation window when no Event.
- **Auto-unpublish execution:** If a job runs SCHEDULED/EVENT_END, add it to in-scope and references.
- **References:** Add `Event` model path and dashboard form-card component path.
- **Out-of-scope:** Add "Custom expiry on production links" to align with story.
- **"Form detail":** Add ref if that unpublish location stays in scope.

---

## UAT Guide (STORY-5.8-UAT-TEST-GUIDE.md)

- **DC1 Step 1.4:** Add the exact place Admin publishes after "Approve only" (FormReviewPage, Dashboard, or both).
- **DC3:** Add step for Form with no Event (e.g. EVENT_END disabled or error).
- **DC9:** Add step for Event with null or missing EndDate.
- **DC3:** Add validation for SCHEDULED unpublish date in the past.
- **EVENT_END:** Add step for changing Event.EndDate after publish (does unpublish date update?).
- **Pre-conditions:** Add or reference test threshold setup for Company User publish tests.
- **Prerequisite:** Align with story (5.6 only vs 5.6 + 5.7).
- **DC11/DC12:** Add explicit UAT steps (e.g. "All DC1–DC10 passed" and "Story PR merged") or state they are process, not manual-test steps.

---

## Consistency & Other

- **PM Decisions vs Story status:** PM Decisions is "Proposed — PM to approve." Story is "Ready." Either update Story to "Blocked: PM approval pending" or mark PM Decisions as approved.
- **Unpublish locations:** Story lists FormReviewPage, Event Dashboard, "and/or form detail"; DC4 and UAT only mention FormReviewPage and Dashboard. Add "form detail" to DC4/UAT or remove it from the story scope.
- **DC8 "queue if available":** UAT 8.2 says "or note N/A." Add a brief definition of "available" (e.g. "in-app queue implemented and accessible").

---

*Incorporate these into story, context, and UAT before creating STORY-5.8-SINGLE-SESSION-DEV-PROMPT.md*
