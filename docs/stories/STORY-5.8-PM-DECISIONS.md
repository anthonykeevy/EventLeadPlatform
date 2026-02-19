# Story 5.8 — PM Decisions (Approval, Unpublish, Notifications)

**For:** Dev team, Story implementation  
**From:** Product Manager  
**Story:** 5.8 Admin Review & Publish + Activation  
**Created:** 2026-02-18  
**Status:** Approved — use for implementation  

---

## 1. Approval Flow: Approve Only vs Approve & Publish

**Requested:** Give approver two options when reviewing a publish request:
- **Approve only** — approve the request but do not publish yet
- **Approve and publish** — approve and publish immediately (current behaviour)

**Recommendation: Include both options**

| Option | Use case | Result |
|--------|----------|--------|
| **Approve only** | Admin wants to signal "looks good" but will publish later (e.g. after payment, after final check) | FormPublishRequest → approved; Form stays PENDING_REVIEW or returns to a "Ready to publish" state. |
| **Approve and publish** | Admin is ready to go live now | FormPublishRequest → approved; Form → PUBLISHED; FormPublicLink created. |

**Design notes:**
- "Approve only" implies form remains in a state where Admin can publish with one click later (without re-request). May need new state "Approved (not yet published)" or keep PENDING_REVIEW with flag `approved_for_publish`.
- Requester gets different notifications: "Admin approved your request" vs "Your form has been published."

**PM decision:** Approve both options. Add "Approve only" as primary, "Approve & Publish" as secondary CTA (or vice versa based on most common flow).

---

## 2. Unpublish Options: Three Modes

**Requested:** Three ways to control when a form is unpublished:

| Option | Description |
|--------|-------------|
| **Manually unpublish** | Form stays published until Company Admin manually unpublishes. |
| **Event end date** | Form auto-unpublishes when the event ends. Show event end date. |
| **Schedule** | Date picker: Admin sets a specific unpublish date. |

**Recommendation: Include all three**

**Data model:**
- Add `Form.UnpublishMode` or equivalent: `MANUAL` | `EVENT_END` | `SCHEDULED`
- Add `Form.ScheduledUnpublishDate` (nullable; used when SCHEDULED)
- When EVENT_END: derive from `Event.EndDate` (Form → Event relationship)
- When MANUAL: no auto-unpublish; admin triggers manually.

**UI:**
- On publish (or in form/event settings): Radio or dropdown for unpublish mode.
- When EVENT_END selected: Show event end date (read-only or link to edit event).
- When SCHEDULED selected: Show date picker for unpublish date.
- When MANUAL selected: No additional fields.

**PM decision:** Approve all three options. Implement in Story 5.8.

---

## 3. Unpublish Notifications — Research & Recommendation

**Requested:** Send notifications:
- 7 days before unpublish
- 1 day before unpublish
- When unpublished

**Concern:** Avoid being annoying; research how other platforms handle this.

### Research Summary

**Form builders (Jotform, Typeform, etc.):**
- Jotform: Form expiration date exists; no built-in auto-notifications to form owner before expiry. Users can set reminder emails for submission deadlines via autoresponders, but not for form expiration.
- Pattern: Most form platforms do not notify form owners before auto-disable.

**SaaS notification best practices (Courier, Zigpoll, Twilio):**
- **Notification fatigue:** 73% of users unsubscribe due to too many irrelevant or poorly timed messages.
- **Best practice:** Granular preference centers — let users control notification types, frequency, and channels.
- **Recommended approach:** Offer opt-in reminders rather than forced notifications. "Would you like reminders before this form is unpublished? [ ] 7 days [ ] 1 day [ ] When unpublished".

**PRD / Epic scope:**
- PRD mentions email for: publish requested, published, team join. Notifications are feature-specific.
- **Epic 4 (Team Collaboration)** — user referenced this when mentioning "Communication"; team invites, approvals, etc. will align here.
- Epic 5: "Optional email notifications for publish requested / changes requested / published" — in-app queue is MVP.

### Recommendation

| Approach | Pros | Cons |
|----------|------|------|
| **Forced notifications (7d, 1d, on)** | Ensures admins are never surprised | Risk of fatigue; may feel intrusive |
| **Opt-in reminders** | User controls; respects attention | Some may miss unpublish if they opt out |
| **Preference center (company-level)** | Consistent with SaaS best practice; scalable | More dev; needs settings UI |

**Suggested decision:**
- **MVP (Story 5.8):** Implement **in-app** reminders only. When a form has SCHEDULED or EVENT_END unpublish:
  - Show in Dashboard: "Form [X] will unpublish on [date]" badge/notice.
  - Optional: In-app notification/queue item 7 days before, 1 day before, and when unpublished (if in-app notification system exists).
- **Email reminders:** Defer to a **Communication / Notification Preferences** story or Epic. Reasons:
  - Requires email infrastructure (SendGrid/Azure) and template design.
  - Best practice is opt-in preference center — separate from publish flow.
  - PRD already lists email as optional for publish flow.
- **Future:** Add **User Preference Centre** to Profile dropdown — platform-wide page for notification and communication preferences. Build incrementally as we add processes. Cross-epic: Epic 4 (Team Collaboration), Epic 5 (publish flow). See backlog in EPIC-5-STATUS.md.

**PM decision:** In-app reminders in Story 5.8 (Dashboard notice + in-app queue if available). Email reminders → backlog / Communication workstream.

---

## 4. Activation Windows

**Requested:** Include event-based activation in Story 5.8 (form active only when event is within start/end dates).

**Decision:** **In scope.** Event-based: form is "active" when event is within Event.StartDate–EndDate. Public resolver returns "event ended" (or similar) when outside window. Use existing Form–Event relationship.

---

## 5. Hide Approval Workflows When Company Does Not Need Them

**Requested:** When company has `RequirePublishApproval` disabled, hide approval-workflow UI so users aren't shown irrelevant options.

**Decision:** **Implement.** When `RequirePublishApproval` (CompanyFormTestConfig) is false:
- **Hide:** PendingPublishRequestsCard, Request Publish flow, links to FormReviewPage/review queue.
- **Show:** Direct Publish for Company Users and Admins (subject to test threshold).
- **Keep:** Form Approval Workflow page in Company Settings — that's where the setting is configured; admins can enable it later if needed.

---

## 6. Unpublished Form — Public URL Experience (DC4)

**Problem:** A 404 when someone visits a link to an unpublished form is poor UX. They may have bookmarked or shared the link; the form may have been advertised.

**PM decision:** Do **not** return 404. Instead, serve a dedicated **"Form unpublished"** page with:

1. **Message:** Clear, friendly copy — e.g. "This form is no longer active. It has been unpublished."
2. **CTA:** "If this form should still be available, you can request the administrator to publish it again."
3. **Action:** When the visitor clicks that CTA, send an **in-app notification** to **all Company Admins** for that form's company: "Someone visited an unpublished form and requested it be published again. [Form name] is still being advertised. Would you like to publish it?"
4. **Admin flow:** Admins can dismiss or act (publish from the notification / FormReviewPage / Dashboard).

**Implementation:** Public resolver detects unpublished (FormPublicLink.IsActive=false or Form.Status=UNPUBLISHED); serves the unpublished page instead of form or 404. CTA triggers API to create a "re-publish request" or equivalent; notification system delivers to Company Admins. Use in-app notifications for MVP; email to admins can be added later if in-app queue exists.

---

## 7. Summary of PM Decisions

| # | Topic | Decision |
|---|-------|----------|
| 1 | Approval options | **Approve only** + **Approve and publish** — both available on FormReviewPage. |
| 2 | Unpublish modes | **Manually**, **Event end date**, **Schedule** (date picker) — all three. |
| 3 | Unpublish notifications | **MVP:** In-app only (Dashboard notice, queue if available). **Defer:** Email reminders to Communication/preference-center workstream. |
| 4 | Activation windows | **In scope.** Event-based (Event.StartDate–EndDate); public resolver shows "event ended" when outside window. |
| 5 | Hide approval workflows | When RequirePublishApproval=false: hide publish-request UI; all users publish directly. Form Approval Workflow Settings page remains. |
| 6 | Unpublished form URL | **Dedicated page** (no 404). Message + "Request admin to publish again" CTA → in-app notification to all Company Admins. |

---

## References

- Story: `docs/stories/story-5.8.md`
- PRD: `docs/prd.md` (User Flow 3.4, Admin Approves Publish)
- Epic 5: `docs/stories/EPIC-5-STATUS.md`
- Research: Jotform form expiration; Courier/Twilio preference-center best practices

---

*PM decisions — approve before updating story-5.8.md and implementation*
