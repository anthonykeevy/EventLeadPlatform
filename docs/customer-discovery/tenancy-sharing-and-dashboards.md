# Platform Tenancy, Sharing, and Dashboards

**Purpose:** This is the **platform-lens** reference. Where the persona guides cover operational pain (build a form, distribute it, capture leads), this doc covers what enterprise buyers care about — **visibility, governance, and how the platform replaces a multi-tool process.**

It serves three jobs:
1. Anchors the language used in interviews when the conversation moves from "your last form" to "how your team operates at scale."
2. Tracks which parts of the tenancy / sharing / dashboard model are **shipped** vs. **partial** vs. **planned** — so we don't claim things in interviews we can't deliver.
3. Captures the open design questions that discovery is supposed to resolve.

**Important:** Feature states below are verified against code as of **2026-05-03**. They're more conservative than founder recall in places — that's deliberate. We promise only what's shipped.

---

## The two lenses (read first)

- **Platform lens (what this doc covers):** visibility across forms × events × companies × spend × leads × approvals; replacement of the **SDLC for customer-engagement forms** — design → build → validate → rework → approve → publish → distribute → support; senior-level governance and rollups across the program. Persona B already runs an SDLC for software; we're pointing out they're running an *informal* one for customer-engagement forms with no system of record.
- **Operational lens (covered in persona guides):** day-to-day form building, branding, AI assistance, AU address validation, kiosk, offline capture, embed delivery.

The operational lens makes someone like the tool. The platform lens makes their head of marketing buy it.

The exact SDLC stages will vary per company. The shape (many people, manual handoffs, no consolidated visibility) is universal. Discovery probes the shape, not the specific stages.

---

## The data model in plain English

The platform is built on four primitives, in this hierarchy:

```
User
  └── belongs to → Company  (multi-tenant container)
                    └── creates → Event  (cost stream / engagement container)
                                  └── creates → Form  (the customer-facing artefact)
```

Plus three sharing / federation primitives layered on top:

1. **Cross-company event sharing** — share a whole event with another company; their team sees it in their event list.
2. **Cross-company form access control** — finer-grained access to a single form (View / Edit / Manage / Analyze / Submit) with relationship type and optional expiry.
3. **Company hierarchy** — one company can be parent to others (head office → subsidiaries / branches), with navigation between them.

Each is described below with **shipped / partial / planned** state.

---

## Primitive 1 — User → Company

**State: SHIPPED**

A user always belongs to (at least) one company. Their company is created during onboarding:

- New email signs up → onboarding flow → user sets up their company → first user becomes Company Admin.
- If their company *already exists* on the platform (by domain match or explicit lookup), self-signup currently routes to "request to join" → email to existing Company Admin(s) for approval. *(Verify: this is the design intent; verify exact flow during discovery prep.)*
- Email-share invites that auto-onboard new emails are **planned** (see Primitive 2).

The Company is the multi-tenant boundary — the unit of:
- Billing (whoever owns the share is whoever pays — when billing is built)
- Brand defaults (fonts, colours, spacing inherited by every form)
- Approval workflows
- Audit trail
- Team roles (Company Admin, Company User, Company Viewer)

---

## Primitive 2 — Cross-company event sharing

**State: PARTIAL**

The mechanism exists. The "share an event with someone outside your company" flow:

- Owner of an event can invite another company's user by **email**.
- If that email is **already on the platform**, the email's company is added to the event with a chosen role (event_owner / organizer / participant / agency_form_builder).
- The invited company sees the event in their dashboard with a **"Shared by: [user name]"** tag (currently hardcoded prefix + dynamic user name; not configurable).
- The forms inside the event become visible/accessible to the invited company according to roles.

**What's shipped:**
- Email-share endpoint and modal for events (`ShareEventModal.tsx`)
- "Shared by" tag rendering on events (`CompanyContainer.tsx`)
- Permission gating — only users with `manage_participants` on the event can share

**What's partial / not shipped:**
- **Email-share onboarding for non-tenant emails.** Today, if the email isn't on the platform the API returns "User not found." The full design is: send an email anyway → invitee onboards → if their company matches the inviter's, auto-add to that company; if their company is different and exists, request-to-join the existing company; if their company doesn't exist, they create it and become its admin; in all cases the original event share is honoured once they're on the platform. This is **planned** — see [mvp-scope-fix-candidates.md](mvp-scope-fix-candidates.md).
- **Configurable / suppressible "shared by" tag** — important for white-label scenarios.
- **External-share guardrails** — confirmation modal, domain allow/blocklist, distinct audit-action codes for external vs. internal shares.

---

## Primitive 3 — Cross-company form access control

**State: PARTIAL**

A finer-grained primitive than event sharing. Granted *inside* a form (or to a target outside the company that owns it):

- 5 access types: **View / Edit / Manage / Analyze / Submit**
- **Relationship type** captured per grant (branch / subsidiary / partner / etc.) — currently *metadata only*, doesn't enforce different permissions
- **Optional expiry date** on every grant
- Targets: a specific **User** ✅ or a target **Company** ❌ (API rejects with "not yet implemented")

**What's shipped:**
- `FormAccessControl` table with relationship-type FK, expiry, access-type FK
- `GrantAccessForm.tsx` modal with all UI fields working for user-target grants
- Backend grant/revoke endpoints for user-target grants
- Existing-access display with revoke action

**What's partial / not shipped:**
- **Granting access to a whole company in one action** — UI offers the "Company" radio button; API rejects. Either build it or hide the option (see [mvp-scope-fix-candidates.md](mvp-scope-fix-candidates.md)).
- **Email flow for company-wide form grants** — if/when company-wide is built, the same auto-onboarding flow as Primitive 2 applies.
- **Relationship-type enforcement** — open design question: should branch/subsidiary/partner gate different default permissions, or stay metadata?

---

## Primitive 4 — Company hierarchy (federation)

**State: PARTIAL — primitive shipped, group rollup planned**

For organisations where head office handles overall marketing and subsidiary BUs run their own engagements:

- `Company.ParentCompanyID` self-referential FK + `CompanyRelationship` table (parent ↔ child, relationship type, status)
- 5-level hierarchy navigation in the dashboard (`hierarchyUtils.ts`) — switch between any company you have access to
- Each company's data loads **separately** when you switch into it

**What's shipped:**
- Hierarchy data model
- Navigation / company switcher

**What's not shipped:**
- **Group admin role** with implicit visibility into all subsidiaries
- **Consolidated dashboard** that aggregates KPIs (forms active, leads, spend, pending approvals) across parent + all children at once
- **Aggregation endpoints** — no backend code today does `SELECT … WHERE company_id IN (SELECT id FROM companies WHERE parent_company_id = X)`

This is the single biggest gap for the **enterprise-platform-value sale.** A federated marketing org's head of marketing wants one screen — "what is happening across all my BUs right now" — and that screen doesn't exist yet. Discovery should validate appetite (out of scope for current MVP, but on the roadmap if signal is strong).

---

## How each persona uses the model

### Persona A — SMB user

Single company. No federation. Few or no shares. The interesting questions are about the *form*, not the tenancy. Tenancy is invisible plumbing.

- One company, 2–10 users, mix of roles
- Events as cost-stream containers (per trade show, campaign, launch, survey, etc.)
- Forms within events
- Occasional external share — invite a contractor to design a form for one event
- Dashboard need: my company's forms / leads / pending approvals; nothing more

### Persona B — Enterprise

Where the tenancy model earns its keep.

- **Federation is the headline feature.** Head office (Company P) is parent to regional / BU subsidiaries (Companies C1, C2, C3). Marketing leadership at HO wants visibility across all of them.
- **Cross-company event sharing** is used for global campaigns — HO designs a campaign event, shares to all regions; each region creates region-specific forms inside the shared event.
- **Form access control with relationship type** captures the actual relationship — "this form is shared with our APAC subsidiary as a branch, not a partner" — even if the permissions are the same today.
- **Approval workflow** carries cost-aware UI today; backend enforcement and budget-based governance are open design questions.
- **Dashboard need (planned, not shipped):** group admin sees consolidated KPIs across parent + subsidiaries; company admin sees their own slice; company user sees their own work.

### Persona C — Agency / service provider

The tenancy model bends toward agency reality, with three sub-model variations:

- **Project agency:** Agency lives in their own company, builds a form there, then shares the event/form with the client company at handoff. "Shared by [Agency]" tag tells the client where it came from. Once handed over, agency can step away or maintain access.
- **Managed-service agency:** Agency holds the event/form in their tenancy and shares **read-only** access (View / Analyze) back to the client. Agency runs operations; client sees results without disrupting them. The "Shared by" tag actually reinforces who's running it.
- **MarTech consultancy:** Less likely to use the sharing model. They get invited *into* the client's tenancy as a user during implementation.

The agency-specific scorecard items (AG1–AG10) probe which of these models customers expect us to support best.

---

## Dashboard lenses by persona

The current dashboard is **generic and flat** — every user in a company sees the same layout, scoped to that company. There are no role-based lenses, no aggregations, no senior-level KPI views. **This is a real platform-lens gap** and one of the most-likely-to-be-asked items in enterprise discovery.

The lenses below describe what each persona / role *probably needs* — to be validated by discovery, not built ahead of it.

### Persona A — SMB Company Admin

- Forms active right now / in last 30 days
- Leads captured this period (across forms)
- Pending approvals (forms my team has submitted)
- Upcoming events with form-ready status
- Spend this period (when billing is wired)
- Recent activity log highlights

### Persona A — SMB Company User

- My forms (built / submitted for approval / published)
- Leads on my forms
- Approval requests I'm waiting on

### Persona B — Group Admin (planned, not shipped)

The headline enterprise value:

- Consolidated forms-active and leads-captured **across all companies in the group**, with drill-down per subsidiary
- Top-performing forms across the group
- Pending approvals across the group, with severity / cost flag
- Spend YTD across the group, with per-subsidiary breakdown
- Recent shared-event activity
- Anomalies: subsidiaries that haven't published in N weeks, approval queues stalled, forms with no submissions

### Persona B — Company Admin (subsidiary)

- My company's slice of the above
- Plus: events / forms shared *into* my company by HO or other subsidiaries

### Persona B — Company User

- Same as Persona A user view, but with shared-in events visible

### Persona C — Agency Principal (project)

- Active client engagements (events shared out)
- Forms shared and their status
- Payment / billing status per engagement *(when billing is wired)*

### Persona C — Agency Principal (managed-service)

- Per-client lead volumes (for reporting back)
- Active forms per client
- Billing status per client
- Pending approvals across all clients I'm running

### Persona C — Agency Account Manager

- My specific client portfolio only — not all agency clients

---

## Open design questions for discovery

These are the things this doc *can't* answer alone — discovery is meant to. Each is also a probe in one or more persona guides.

### 1. Email-share to non-tenant emails — how do we onboard?

When Company A shares an event with `someone@external.com` and `someone@external.com` isn't on the platform yet, what should happen?

- **Founder's intent:** email is sent regardless; recipient onboards; if their company matches inviter's, auto-add to that company; if different & exists, request-to-join existing company admin; if different & new, they become admin of their newly-created company; original event share honoured once they're on the platform.
- **Code today:** "User not found" error. Half the design is missing.
- **Discovery validates:** is this the right flow? Are there scenarios where auto-onboarding is *unwanted* (e.g., enterprise procurement requires explicit vendor onboarding before any platform access)?

### 2. White-label / configurable "shared by" tag

The tag exists today as a hardcoded "Shared by: [user name]" prefix.

- **Tension:** managed-service agencies and white-label resellers don't want their name showing up on the client's view of the event.
- **Discovery validates:** how many agencies want it suppressed entirely vs. customised vs. left as-is? Is this a switching-signal feature for any persona, or a nice-to-have?

### 3. Billing on shared events / forms

Today there's no billing code at all, so this is purely design.

- **Founder's current intent:** Company A (the inviter / share owner) pays.
- **Alternative:** the company that publishes pays (regardless of who shared).
- **Alternative for agencies:** agency takes payment from end-customer and remits a platform fee (B2B2C variation).
- **Discovery validates:** what model do customers actually expect? Probably different per persona — Persona B may want HO-pays-for-subsidiary; Persona C may want pass-through-to-client.

### 4. Cost-governance — is per-form approval the right mechanism?

The current design (cost-aware UI gating + admin approval over a threshold) is **half-implemented and arguably the wrong shape.** Founder's own observation: usually one person manages forms across all events; per-form cost approval may create blockers without delivering real governance.

Real options to test in discovery:
- (a) Hard cost cap per form — admin must approve anything over $X
- (b) Annual / quarterly budget per company that depletes
- (c) Soft notification only — admin emailed on publish, no blocker
- (d) Pre-approved budget per event/campaign — sub-budgets owned by event leads
- (e) Doesn't matter — one person owns all forms anyway
- (f) Other

This is **scorecard Q4** and a probe in Persona B (procurement section) and Persona C (visibility probes).

### 5. Group admin / consolidated dashboard

Out of MVP scope today, but a likely Persona B switching-signal.

- **Discovery validates:** how often does this come up unprompted? What KPIs do they want at the group level? Is it a hard requirement for adoption or a future-roadmap-acceptable item?

### 6. Relationship-type enforcement

`FormAccessControl.RelationshipTypeID` is captured but doesn't gate different permissions today.

- **Discovery validates:** do customers expect different defaults for branch vs. subsidiary vs. partner? Or is the flat model fine and relationship type is just metadata for reporting?

### 7. External-share safety

Permission checks exist today but no confirmation modal, no domain controls, no internal/external audit distinction.

- **Discovery validates:** which of those would actually be required by procurement / security to adopt the platform?

### 8. Company-wide form access — implementation shape

UI offers it, API rejects. If we build it, should it:
- (a) Grant access to all *current* members of the target company?
- (b) Create a role that grants access to all *future* members too?
- (c) Be implemented as a lightweight "company has access" flag rather than per-user grants?

### 9. Self-signup → existing company → admin-approval flow

Founder's design: if a new email's company already exists on the platform, request-to-join is sent to existing Company Admin(s).

- **Discovery validates:** does this match what enterprise IT and security teams want, or is it a security risk in their view? Some enterprises will require IT-led provisioning, not user-initiated join requests.

---

## Cross-references

- Operational features → [feature-resonance-scorecard.md](feature-resonance-scorecard.md) Sections 1–2
- Enterprise gaps → [feature-resonance-scorecard.md](feature-resonance-scorecard.md) Section 3
- Agency features → [feature-resonance-scorecard.md](feature-resonance-scorecard.md) Section 4
- Cost-governance design question → [feature-resonance-scorecard.md](feature-resonance-scorecard.md) Q4
- Pre-launch fix candidates derived from this doc → [mvp-scope-fix-candidates.md](mvp-scope-fix-candidates.md)
- Pricing-conversation probes that surface security/dashboard intent → [pricing-discovery-framework.md](pricing-discovery-framework.md) ("What pricing answers also reveal" section)
- Persona B platform-lens probes → [persona-b-enterprise-guide.md](persona-b-enterprise-guide.md)
- Persona C off-boarding & visibility probes → [persona-c-agency-guide.md](persona-c-agency-guide.md)
