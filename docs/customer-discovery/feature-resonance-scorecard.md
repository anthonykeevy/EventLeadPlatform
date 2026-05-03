# Feature Resonance Scorecard (async follow-up survey)

**Purpose:** Capture honest, written feedback on each feature *after* the interview, when there's no social pressure to be polite. Goal is to find which built features actually matter as **switching signals**, which are **retention features**, and which are **table stakes** — and which planned ones to prioritise vs. cut.

**Format:** Build this as a Google Form or Typeform. Send within 24 hours of every interview as a thank-you with a personal note. Keep it under 5 minutes — fewer responses if it's longer.

**Branching:** First question: "Which describes you best?"
- A — SMB / mid-market user (you collect data from your own customers)
- B — Enterprise (200+ staff, multi-region or multi-BU)
- C — Agency / service provider (you deliver forms on behalf of clients)

Show conditional sections accordingly.

---

## Survey copy (paste into form builder)

**Title:** Quick reaction — EventLead features
**Intro:** "Thanks for your time earlier. To get the most useful read, I'd like your gut reaction on each feature below — built and planned. Should take 4–5 minutes. Honest 'don't care' answers are more valuable than polite 'sounds great' ones."

**Scoring scale (use for every feature):**
- **1 — Don't care / not relevant to me**
- **2 — Nice to have, wouldn't change my decision**
- **3 — Useful, might tip the scales** *(retention feature)*
- **4 — Important, I'd specifically look for this** *(strong retention or weak switching)*
- **5 — Critical, I'd switch tools to get this** *(switching signal)*

For each feature also offer an optional one-line text: *"Anything you'd add about this?"*

---

## Section 1 — Already built (everyone answers)

| # | Feature | Plain-English description |
|---|---|---|
| 1 | **Branded forms with custom backgrounds** | Drag-and-drop form designer where you can use your own background image and brand colours, not generic templates |
| 2 | **AI form generation from a description** | Type "registration form for our healthcare expo with company name, decision timeframe, and consent" — AI generates the form |
| 3 | **Offline lead capture** | Form keeps working when Wi-Fi drops at the venue; data syncs automatically when connection returns |
| 4 | **Drag-and-drop AU address validation** | Validated, deliverable Australian addresses via Geoscape / G-NAF — no developer integration required |
| 5 | **Embed-anywhere delivery** | Drop a snippet into your website, CRM page, or marketing platform — no separate URL needed |
| 6 | **Public form URL** | Stable, shareable link for the form (also QR-code friendly) |
| 7 | **Kiosk mode with auto-reset** *(renderer supports via URL parameters today; form-builder/publish UI to enable per-form is not yet built)* | Form sits on a tablet (reception, retail, event), auto-resets after a configurable timeout if abandoned |
| 8 | **Multi-tenant company workspace with team roles** | Company admins, users, and viewers, with controls on who can edit, publish, or just see analytics |
| 9 | **Approval workflow before publishing** *(approval flow shipped; cost-aware UI shipped; backend enforcement of cost threshold is not yet wired — fix candidate)* | Junior staff can build forms; admin must approve before they go live |
| 10 | **Cross-company event sharing via email** *(works today for emails already on the platform; auto-onboarding for new emails is the planned full flow — see #22)* | Invite another company (agency, branch, partner) to participate in your event by email |
| 11 | **"Shared by [Company / User]" tag on shared events** *(currently shows hardcoded prefix + sharer's user name; not configurable)* | When you receive a shared event, you see who shared it with you |
| 12 | **Form-level access control with relationship type and expiry** *(user-target works; granting to an entire target company is planned — API currently rejects "company-wide" grants — see #23)* | Grant View / Edit / Manage / Analyze / Submit access to a specific user with optional expiry. Relationship type (branch, subsidiary, partner) is captured as metadata |
| 13 | **Company hierarchy navigation** *(parent/child + 5-level switcher shipped; consolidated group dashboard is planned — see #24)* | Companies can be organised parent → child (head office → subsidiaries); user can switch context between any company they have access to |
| 14 | **Company-level brand defaults** | Set fonts, colours, spacing once at the company level — every new form inherits them |
| 15 | **Full audit trail** | Track who did what (created, edited, published, approved, exported) with timestamps for compliance |
| 16 | **Per-event activation windows** | Forms automatically go live and stop accepting submissions on event start/end dates |
| 17 | **International field validation** | Phone, address, and identifier rules built for AU / NZ / US / UK / CA out of the box |
| 18 | **Form versioning** | Every change creates a version — roll back to a prior version if needed |
| 19 | **CSV export of leads** | Download in formats compatible with Salesforce, Marketing Cloud, Emarsys |
| 20 | **20+ field types including file upload, signatures, ratings** | Beyond simple inputs — collect documents, ratings, terms acceptance |

---

## Section 2 — Planned but not yet built (everyone answers)

The goal here is to find which planned features are worth prioritising vs. cutting. Items renumbered to follow the expanded "built" list above.

| # | Feature | Plain-English description |
|---|---|---|
| 21 | **Pay-per-published-form pricing** | Pay only when a form goes live, no subscription — only pay for what you use |
| 22 | **Auto-onboarding for shared-event email invites** | When you share an event with someone whose email isn't on the platform, the email link onboards them, sets up their company (or joins them to existing one), and grants them access — all in one flow |
| 23 | **Company-wide form access grants** | Grant a target company access to a form in one action, instead of individually adding each of their users |
| 24 | **Group admin consolidated dashboard** | Senior view aggregating KPIs (forms active, leads captured, spend, pending approvals) across a parent company and all its subsidiaries simultaneously |
| 25 | **Senior dashboard lenses by role** | Different at-a-glance dashboards depending on whether you're Company Admin (all forms/leads/spend/pending approvals for your company), Company User (your own work + shared with you), or Group Admin (consolidated across companies) |
| 26 | **Image-to-form (vision AI)** | Upload a screenshot or photo of a form and AI generates a digital version |
| 27 | **Stripe Connect payments on forms** | Add a payment field to your form — collect registration fees, deposits etc. directly into your Stripe account |
| 28 | **PII detection guardrails** | System warns you if a form looks like it's collecting sensitive personal data (SSN, credit card etc.) |
| 29 | **Privacy Act / GDPR consent v2** *(not started — topical given AU Privacy Act tranche-one reforms passed Dec 2024)* | Specific, voluntary, current, unambiguous consent capture per submission with timestamped audit trail and DSAR support |
| 30 | **Configurable / suppressible "shared by" tag** | Choose to hide, customise, or whitelabel the "shared by" attribution shown on shared events — useful for agency white-label scenarios |
| 31 | **External-share guardrails** | Confirmation modal when sharing externally; optional domain allowlist/blocklist; distinct audit-action codes for external vs. internal shares |
| 32 | **Backend enforcement of cost-gated approval** *(or alternative governance model — open design question; see Section 5)* | Backend prevents direct-API publish of high-cost forms unless approval is in `APPROVED` state, regardless of UI path |

---

## Section 3 — Enterprise-only (show only to Persona B)

These are gaps we know we have. We need to know which are real dealbreakers for *your* company.

For each, ask: **Would this be a hard requirement for [company] to adopt the tool?**
- **Yes — hard requirement, can't proceed without it**
- **Yes — but we could pilot without it if there's a committed roadmap**
- **No — would be nice but not blocking**
- **Not relevant for us**

| # | Gap | Description |
|---|---|---|
| E1 | **SSO / SAML / OIDC** | Single sign-on with Okta, Azure AD, Google Workspace, Ping etc. |
| E2 | **Webhooks / native CRM integration** | Real-time push of leads to Salesforce / Marketo / HubSpot / Eloqua, not just CSV export |
| E3 | **Custom domain on public forms** | Forms hosted on yourbrand.com, not eventleadplatform.com |
| E4 | **Self-serve data subject deletion (GDPR / Privacy Act)** | UI to honour right-to-be-forgotten requests without raising a support ticket |
| E5 | **Data residency commitments** | Guaranteed AU / EU / US data hosting region |
| E6 | **SOC 2 Type II / ISO 27001 certification** | Formal security certification |
| E7 | **DPA + sub-processor list** | Standard data processing agreement and named sub-processors |
| E8 | **Audit log streaming to SIEM** | Push audit events to Splunk / Datadog / your SIEM in real time |
| E9 | **IP allowlisting on admin app** | Restrict admin access to corporate-IP-only |
| E10 | **VPAT / accessibility (ACR) report** | Formal accessibility conformance documentation |
| E11 | **Lead deduplication & enrichment** | Match leads against ZoomInfo / Clearbit / 6sense, dedupe against CRM |
| E12 | **Multi-language forms** | Same form rendered in multiple languages based on visitor preference |
| E13 | **Field-level encryption / PII masking** | Some fields encrypted at rest, masked in UI unless user has explicit access |
| E14 | **Bring-your-own-storage** | Lead and asset data stored in your S3 bucket, not ours |
| E15 | **A/B testing of forms** | Run two form variants, compare conversion |
| E16 | **E-signature integration (DocuSign / Adobe Sign)** | Forms requiring legally-binding signature for waivers / contracts |
| E17 | **Consent management & lawful-basis tracking** | Capture and timestamp specific consent (marketing, data sharing, profiling) per submission |
| E18 | **Scheduled exports to data warehouse** | Nightly push of leads to BigQuery / Snowflake / Redshift |

---

## Section 4 — Agency-only (show only to Persona C)

For each: **How important is this for delivering forms on behalf of clients?**
1 (don't care) → 5 (would switch tools to get this)

| # | Feature | Description |
|---|---|---|
| AG1 | **Multi-client workspace with full data isolation** | Each client is its own workspace; no risk of data crossing clients |
| AG2 | **White-label custom domain per client** | Forms appear on the client's domain, not yours or ours; client never sees agency-tooling branding |
| AG3 | **Scoped agency-builder role** | Your team can build/run forms inside a client's workspace without seeing other clients |
| AG4 | **Agency master billing (you pay, you re-bill clients)** | Single invoice to the agency; you handle re-billing to each client at your margin |
| AG5 | **Pass-through billing (each client pays directly)** | Each client billed individually; agency takes a referral commission |
| AG6 | **Rapid client onboarding** | New client workspace stood up in minutes, with brand defaults inherited from a template |
| AG7 | **Clean client offboarding** | At project end, transfer ownership to client with one action; or archive cleanly without data loss |
| AG8 | **Client-facing read-only dashboard** | Client can log in to see results without being able to edit |
| AG9 | **Form template library shareable across clients** | Build once, reuse across client engagements with brand swap |
| AG10 | **Reseller / partner program** | Formal margin, co-selling, marketing assets you can use with clients |

---

## Section 5 — Free text (always show)

1. **What's the single feature on this list that would most affect your decision to use this?** (free text)
2. **What's missing from this list that you'd expect a tool like this to do?** (free text)
3. **If you had to remove three features to keep the price down, which would go?** (free text)
4. **Cost / spend governance — open design question.** When a junior team member builds a form that costs money to publish, how would you most want spend to be controlled in your team? *Multiple choice + comment box:*
   - (a) Hard cost cap per form — admin must approve anything over $X
   - (b) Annual / quarterly budget per company that depletes — when budget runs out, no more publishes
   - (c) Soft notification only — admin gets emailed when something's published, no blocker
   - (d) Pre-approved budget per event/campaign — sub-budgets are owned by event leads
   - (e) Doesn't matter — one person in our team owns all forms anyway
   - (f) Other — describe
5. **(Persona C only)** *Would you see this as a tool you'd use when a client asks, or a platform you'd run your service on top of? Why?* (free text)
6. **Anything else you want me to know that didn't come up on the call?** (free text)

---

## How to analyse responses

After 5+ responses per persona, look at:

- **Mean score per feature** — anything <2.5 is a candidate to deprioritise; **>4 is a switching-signal candidate**, worth highlighting in sales
- **Variance** — high-variance features (some 5s, some 1s) usually indicate segment splits. Investigate.
- **Switching-signal tally** — count of 5s per feature. Anything with ≥40% of respondents giving a 5 is a sales talking point and should be front-and-centre.
- **Enterprise gap "hard requirement" tally (Persona B)** — gaps marked "Yes — hard" by >40% of B respondents are your build-next list.
- **Agency platform-vs-tool answer (Q4)** — count "platform I'd run on" vs. "tool I'd use." This is the single most important Persona C signal.
- **Free-text Q2** ("what's missing") — group into themes. Themes mentioned by 2+ respondents are signal.
- **Free-text Q3** ("what would you cut") — features named by multiple people are scope candidates.

Track all of this in a spreadsheet alongside the interview log so you can correlate written scores against in-call commitment signals. Discrepancies are interesting — high written enthusiasm + low call commitment usually = polite but not buying.
