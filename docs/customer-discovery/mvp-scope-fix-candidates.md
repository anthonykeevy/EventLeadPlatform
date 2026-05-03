# MVP Scope — Fix Candidates Surfaced During Discovery Prep

**Purpose:** Capture the gaps between *design intent* and *shipped code* that surfaced during discovery preparation, so they don't get lost. These should be triaged into the project plan as build / fix / defer decisions before MVP launch.

**This doc isn't the project plan** — it's a feeder doc. Its job is to surface candidates with enough context for triage.

**Last verified against code:** 2026-05-03

---

## How to use this doc

For each candidate:
- **Status** — proposed disposition (Build pre-MVP / Defer / Replace / Decide after discovery)
- **Why it surfaced** — what made this visible
- **Risk if shipped as-is** — what the customer-visible failure looks like if we don't address it
- **Effort hint** — rough size; not a substitute for actual estimation

**The ask:** triage these into your project plan within the next sprint. Several block honest interview claims, which means launching with them unaddressed risks immediate trust damage.

---

## Pre-launch fix candidates (UI/API alignment)

### 1. Email-share onboarding for non-tenant emails

**Status proposal: Build pre-MVP**
**Why it surfaced:** Code today returns "User not found" if the share-target email isn't on the platform. Founder's design intent is the full onboarding flow:
> Email is sent regardless of whether the recipient is on the platform. If they don't have an account, they sign up. During signup, they create their company. If their company matches the inviter's, auto-add them. If different & the company exists on the platform, request-to-join is sent to existing Company Admin(s). If different & company doesn't exist, they become Company Admin of their newly-created company. The original event share is honoured once they're on the platform.

**Risk if shipped as-is:** The most common share scenario (sharing with someone outside your tenant) silently fails. Customers will report "we sent the share, they never got it" — corroded trust on day one.

**Effort hint:** Medium. Touches `share_event_by_email`, signup flow, invitation token model, MailHog/SendGrid email templates, post-signup auto-grant logic.

**Discovery dependency:** Light — current intent is well-defined; discovery validates whether enterprise IT teams will *accept* user-initiated request-to-join, or require IT-provisioned access (Q9 in tenancy doc).

---

### 2. Backend enforcement of cost-gated approval — OR pivot to alternative governance

**Status proposal: Decide after discovery (lean toward Replace)**
**Why it surfaced:** UI gates correctly route over-threshold forms to approval workflow, but `ApprovalService.submit_for_approval()` reads the threshold and `pass`-es. A user with publish permission could direct-API publish a high-cost form bypassing approval entirely.

**Founder's own reflection:** "I half-implemented it because Form builder is only a small percentage of their overall event cost so there is normally one person that will manage the platform and create forms... budget enforcement is hard because of variable lead volume costs (100 vs 1000 leads)."

This is a strong signal that the *current shape* of cost-gating may be the wrong governance mechanism.

**Risk if shipped as-is:**
- (a) Claiming "approval workflow with cost gating" in interviews when the backend doesn't enforce is misleading.
- (b) If a customer does rely on it, a determined or careless user can bypass.

**Options to triage post-discovery:**
- (i) Wire backend enforcement of the existing per-form cost gate (preserves current design)
- (ii) Replace with annual/quarterly company budget that depletes
- (iii) Replace with soft notification only (no blocker)
- (iv) Replace with pre-approved per-event/campaign sub-budgets
- (v) Remove cost-gating entirely and rely on team discipline + dashboard visibility
- (vi) Hybrid — soft notification by default, hard cap optional per company

**Effort hint:** Small if (v) or (iii); medium if (i) or (iv); larger if (ii). Discovery scorecard Q4 is designed to gather evidence here before committing.

**Discovery dependency:** Strong. Don't build until Persona B and C interviews surface what governance shape customers actually want.

---

### 3. Company-wide form access — UI / API alignment

**Status proposal: Build pre-MVP OR hide UI**
**Why it surfaced:** `GrantAccessForm.tsx` modal offers "Grant access to: User / Company" radio buttons. Selecting "Company" calls the API which returns "Company-wide access not yet implemented."

**Risk if shipped as-is:** Customer clicks the option, sees error, files a bug. Worst-of-both-worlds — UI promises a feature that backend rejects.

**Decision options:**
- **Hide the UI (cheap):** ship with only User-target supported; reintroduce Company target when implemented.
- **Build the feature (more work but better):** decide implementation shape — grant to all current members? all current + future? a "company has access" flag distinct from per-user grants? (Open design Q8 in tenancy doc.)

**Effort hint:** Hide UI = trivial. Implement feature = medium.

**Discovery dependency:** Light if hiding UI. Light-to-medium if implementing — discovery should validate which shape is needed.

---

### 4. Kiosk auto-reset — form-builder UI surface

**Status proposal: Defer unless discovery shows switching-signal**
**Why it surfaced:** Renderer fully implements `kiosk=1` + `autoResetSeconds` query parameters. There is **no** form-builder UI, **no** publish-modal toggle, **no** form-schema field for kiosk mode. Today a customer can't enable kiosk mode without manually crafting a URL.

**Risk if shipped as-is:** Listed as a feature in interviews / marketing → customer can't find how to enable it → trust damage. Mitigation today: don't claim kiosk as shipped (scorecard already reflects this honestly).

**Decision options:**
- (a) Build the UI surface (form schema + builder property + publish-modal toggle) — small / medium effort
- (b) Mark kiosk as an explicitly planned feature in interviews; don't claim shipped
- (c) Remove from scope if discovery shows weak interest

**Effort hint:** Small if persisting at form level; medium if also adding event-level kiosk config inheritance.

**Discovery dependency:** Strong. Track scorecard reactions (#7) and unprompted mentions in Persona A & C interviews. If <10% rate it ≥4, defer or remove.

---

## Pre-launch infrastructure work (newly raised)

### 5. Test and Production environment setup

**Status proposal: Build pre-MVP — non-negotiable**
**Why it surfaced:** Currently 100% in development. No test or production environment exists. This is a launch blocker, not a feature gap.

**What's involved (non-exhaustive):**
- Cloud infrastructure provisioning (Azure per architecture choice)
- Environment-specific configuration (database connection, secrets management, email — replace MailHog with production SMTP, e.g. SendGrid / SES)
- CI/CD pipeline (build, test, migrate, deploy)
- Database migration strategy across environments
- Domain + DNS + SSL
- Monitoring / logging / alerting (at minimum: error tracking, uptime, log aggregation)
- Backup + restore strategy
- Data residency decision (matters for AU enterprise sales — see scorecard E5)
- Incident response basics
- Asset storage migration (local dev → Azure Blob, already abstracted at the storage-provider layer per earlier scan)

**Risk if not done:**
- Can't run a real customer pilot
- Can't credibly claim SLA in any enterprise procurement conversation
- Can't honour DPA / data-residency commitments
- Lose first-customer trust if early production has incidents from misconfigured infrastructure

**Effort hint:** Significant — typically 2–4 weeks of focused founder time, more if you're building monitoring / SOC2 prep into the same scope.

**Discovery dependency:** None for the work itself. Discovery may inform region choice (AU vs. multi-region) and certifications worth investing in (SOC 2 Type II, ISO 27001) if they surface as procurement gates.

---

### 6. Email infrastructure for production

**Status proposal: Build pre-MVP, ties to #5**
**Why it surfaced:** Dev currently uses MailHog. Production needs real transactional email — share invites, signup verification, approval notifications, password reset.

**Considerations:**
- SendGrid, AWS SES, Postmark, or Azure Communication Services
- DKIM / SPF / DMARC configuration on a dedicated sending domain
- Bounce / complaint handling
- Template management
- Audit logging of sent emails (for compliance)

**Risk:** Share invites that don't deliver = silent failure (worse than #1 because customer can't even tell something broke).

**Effort hint:** Small to medium, depending on provider choice and existing abstractions.

---

## Feature-shape decisions surfaced during prep

These aren't "fix" candidates — they're decisions where the answer matters before MVP launch but doesn't necessarily mean a build today.

### 7. "Shared by" tag — make configurable / suppressible?

**Why it surfaced:** Today the tag is hardcoded "Shared by: [user name]". Founder noted "It could be more visible" — suggesting both *visibility* and *suppression* are open design questions.

**Discovery validates:** how many agencies want it suppressed for white-label scenarios. If >40% of Persona C interviewees flag this as a switching-signal feature, prioritise. If <10%, leave as-is.

**Effort hint:** Small — admin setting in Company config, conditional render.

---

### 8. Group admin role + consolidated dashboard

**Why it surfaced:** Founder explicitly out of MVP scope but wants to "start collecting information if this is of value." The single biggest gap for the platform-value enterprise sale.

**Discovery validates:** appetite, KPI priorities, dealbreaker-vs-roadmap-acceptable status. Almost certainly a Persona B switching-signal, but unconfirmed without interviews.

**Decision after discovery:** if signal is strong, this becomes the post-MVP investment thesis. If weak, focus elsewhere.

---

### 9. Self-signup → existing company → admin-approval flow

**Why it surfaced:** Part of the email-share onboarding design (#1) but also relevant for organic self-signup.

**Discovery validates:** is this the right security posture for enterprise customers, or do they want IT-provisioned access only? Some companies will reject any platform that allows self-provisioning of their company tenancy.

**Decision after discovery:** may need an "enterprise mode" toggle that disables self-signup for companies that opt-in.

---

## Open design questions (not fix candidates, but pending decisions)

These belong in [tenancy-sharing-and-dashboards.md](tenancy-sharing-and-dashboards.md) as discovery-resolved questions, but are reproduced here so the project plan sees them:

- Billing model on shared events / forms (who pays — sharer, publisher, agency-as-merchant?)
- Relationship-type enforcement (metadata only vs. permission-gating)
- External-share safety (confirmation modal, domain controls, distinct audit codes)

---

## Suggested triage order

If forced to rank, I'd go:

1. **#5 Test/Prod environments** — non-negotiable, blocks everything else
2. **#6 Email infrastructure** — couples to #5; cheap once #5 is in motion
3. **#1 Email-share onboarding flow** — enables most-common share scenario; without it the platform's headline collaboration story is broken
4. **#3 Company-wide form access** — at minimum hide the UI; ideally implement
5. **#2 Cost-gated approval decision** — deliberately wait for discovery before building or replacing
6. **#4 Kiosk UI** — wait for discovery signal
7. **#7 / #8 / #9** — wait for discovery
