# Customer Discovery — Program Status

**Owner:** Anthony Keevy  
**Last updated:** 2026-05-23 (EOD — CRM + agent outreach validated)  
**Purpose:** One page — where you are, what's working, what's blocked, what to do next. Hub PA tracks milestones in `SignalPlatformsPtyLtd/docs/business/pa/work-items.md` (WI-001).

---

## Executive summary

You have **two parallel tracks** that must stay in order:

| Track | Status | Gate |
|-------|--------|------|
| **A — Customer discovery** | 🔄 Active — CRM live, agent outreach validated; awaiting replies + A1-v2 batch | **Primary** until 6+ Persona A interviews |
| **B — Product build** | 🔄 Customer-facing Test landing page promoted to next story; Form Builder vision work paused | Ship landing page for discovery + beta account creation; **only G2 fixes** that discovery can't wait on |
| **C — Billing engine** | ⏸️ **Deferred** (Epic 6.6–6.10) | Start **after** discovery informs packaging + pricing + must-have features |

**Founder call (2026-05-23):** Outreach before billing is correct. Billing scorecard questions and pricing-discovery framework will **inform** Epic 6 design — not the other way around.

---

## What you've built (discovery layer)

### Documentation ↔ code alignment

The `docs/customer-discovery/` folder is your **truth layer** — compare what you *claim* in interviews vs what *ships*:

| Doc | Role |
|-----|------|
| [tenancy-sharing-and-dashboards.md](tenancy-sharing-and-dashboards.md) | Shipped / partial / planned — platform lens |
| [mvp-scope-fix-candidates.md](mvp-scope-fix-candidates.md) | **Code gaps** → product backlog feeder |
| [feature-resonance-scorecard.md](feature-resonance-scorecard.md) | Honest feature states for post-call survey |
| [kill-criteria.md](kill-criteria.md) | Persevere / pivot / kill thresholds + interview trackers |

**Implementation honesty rule:** Scorecard and tenancy doc already mark partial features (kiosk UI, approval backend enforcement, share-to-new-email, company-wide access). Don't claim shipped in calls unless the doc says SHIPPED.

### Live ops

| Asset | Status |
|-------|--------|
| [Scorecard Google Form](https://docs.google.com/forms/d/e/1FAIpQLSdElnXesGMZ_GkBLs4SGWMSHtsxqf1FPcQ3ODHWLmmbIgLLuA/viewform) | ✅ Live |
| [Evidence spreadsheet](https://docs.google.com/spreadsheets/d/1byCo9I52tHVwrKO8RJEunFe2KLZ6Lt-sPLLqtlv466c/edit) | ✅ Live (interview scorecards) |
| **SignalPlatformsCRM** (hub) | ✅ Live — 97 candidates, 5 May-6 outreach, agent enrichment + drafts |
| [Apps Script](https://script.google.com/home/projects/1XVSx-0NoKzV1xx4nNfREytPzFS9JDDXt-Z8oTZBS4tqTbaKqQPgHpKtx/edit) | ✅ Form automation |

### Outreach

- **~97 procured leads** — imported to **SignalPlatformsCRM** (S1 ✅)
- **5 LinkedIn messages** sent **2026-05-06** (A1-v1) — in CRM as Pending; monitor for replies
- **v2 templates** — new sends via S3 only (`A1-v2`); agent skill `@crm-linkedin-outreach`
- **Agent session 2026-05-23:** S2.5 enrichment + S3 draft workflow validated end-to-end
- **Next:** replies → S4 Contact; next batch from `outreach_queue` (never-contacted)

---

## Product build status (what discovery feeds)

### Next — Customer-facing beta landing page (Epic 6 Phase A sequencing change)

| Item | Status | Link |
|------|--------|------|
| Story **6.5e-landing** Customer-facing Beta Landing Page | ⏳ Next — PM/SM story pack needed | `docs/stories/story-6.5e-landing-page.md` |
| Story **6.5e-vision** Image-to-Form / Form Builder vision path | ⏸️ Deferred pending customer feedback | `docs/stories/story-6.5e-vision.md` |
| AR/AI components through 6.5d | ✅ Complete | Epic 6 Phase A foundation is strong enough to pause speculative builder work |

**Your focus:** Use the Test system as a credible customer-facing beta URL during discovery. Do not continue Form Builder vision work until interviews and scorecards show which capabilities are true switching signals.

### Deferred — Billing engine (Epic 6 Phase B)

| Story | Title | Status |
|-------|-------|--------|
| 6.6 | Platform Billing Infrastructure (Stripe Direct) | ⏸️ Deferred post-discovery |
| 6.7 | Unified Publish & Payment Gate | ⏸️ |
| 6.8 | GST Invoicing | ⏸️ |
| 6.9–6.10 | Connect / form payments | ⏸️ |

**Why defer:** [pricing-discovery-framework.md](pricing-discovery-framework.md) + scorecard pricing sections need **customer anchors** before locking $99/form, subscription vs PAYG, agency billing model.

**Manual pilot option:** G3 paid pilot can use invoice/manual charge while discovery runs — see hub `launch-tracker.md`.

### G2 fixes (only if discovery converts to pilot)

From [mvp-scope-fix-candidates.md](mvp-scope-fix-candidates.md) — triage order:

1. Email-share onboarding (#1) — if agency/collab comes up in interviews
2. Hide company-wide access UI (#3) — quick trust fix
3. Prod transactional email (#6) — before stranger beta
4. Cost-gated approval (#2) — **decide after discovery**, not before
5. Kiosk UI (#4) — **decide after discovery** switching-signal data

---

## End-to-end process (nine steps)

See **[process/MASTER-PIPELINE.md](process/MASTER-PIPELINE.md)** — S1 lead intake → S9 billing decision → future sales pipeline.

```
S1 Candidates (webset CSV) → S2 Qualify → S3 LinkedIn → S4 Response → S5 Book
→ S6 Interview → S7 Transcript → S8 Scorecard → S9 Billing synthesis → WI-004
```

---

## What's working

- **Doc-vs-code discipline** — scorecard and tenancy doc prevent over-claiming; discovery prep surfaced real gaps into mvp-scope backlog
- **Mom Test program design** — personas, kill criteria, no early demo rule
- **Ops partially live** — form + evidence sheet; outreach process defined
- **Sequencing instinct** — outreach before billing matches goals and reduces rework on Stripe model

## What's not working yet

- **Outreach ops** — no Outreach tab = no funnel visibility; v1 sends not backfilled
- **Interview volume** — 0 completed interviews; learning loop not spinning
- **Transcript → synthesis** — no standard folder/prompt yet for agent-assisted write-ups
- **Hub ↔ product sync** — billing still listed as pre-pilot goal without "post-discovery" gate in goals.md (PA fixing)
- **Implementation comfort** — partial features create anxiety; mitigated by honest scorecard + deferring billing until discovery clarifies priorities

---

## Next actions (PA recommendation — max 3 at a time)

### This week — discovery first

1. **S1 + backfill** — Import webset CSV to **Candidates** tab; paste 5 May-6 rows into **Outreach** ([improvement-backlog.md](process/improvement-backlog.md) P1–P2)
2. **S2 + S3** — Qualify next 10; send 5× **A1-v2** to Qualified + hands-on Y
3. **S6–S8** — First interview through full pipeline when a reply books

### Parallel — product (limited)

4. **Prepare Story 6.5e-landing** — PM/SM story pack + Draft PR for the Test system landing page; no billing stories and no Form Builder vision work until customer signal improves

### Explicitly not now

- Epic 6.6+ billing implementation
- Story 6.5e-vision / image-to-form implementation
- Production deploy (Story 6.11) until billing **or** manual pilot path chosen
- Large G2 fixes unless a booked pilot requires them

---

## Decisions pending your input

Reply with preferences so PA can lock routing:

| # | Question | Options |
|---|----------|---------|
| 1 | **First interview target persona** | A only for 6 calls? or mix A+C early? |
| 2 | **G2 fix before interviews?** | Hide company-access UI only (1 hr)? or ship nothing until first interview feedback? |
| 3 | **Transcript storage** | Google Drive folder per interview? or paste into Evidence sheet Notes tab? |
| 4 | **Billing pilot** | Manual invoice for first payer vs wait for Stripe 6.6 after discovery? |
| 5 | **Weekly review day** | Monday kill-criteria (as README says) — confirm? |

---

## Related hub links

- WI-001 — G2 + discovery outreach (`SignalPlatformsPtyLtd/docs/business/pa/work-items.md`)
- Launch gates — `SignalPlatformsPtyLtd/docs/business/pa/launch-tracker.md`
- Billing research — `SignalPlatformsPtyLtd/projects/eventlead-billing-model/` *(when triaged)*
