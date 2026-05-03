# Industry Pain Research — Marketing & Developer War Stories (AU-weighted)

**Compiled:** 2026-05-02
**Purpose:** Reference material for customer-discovery interviews. Use as pattern recognition and "unlock prompts" of last resort, NOT as a checklist. See `README.md` for ground rules.

---

## How to use this doc

Pattern catalogue, not an interview script. Let interviewees volunteer pain in their own words first — that's the Mom Test signal. Only when someone is genuinely vague after open prompts should you reach for an unlock: *"I've heard from others that [specific X] sometimes happens — does that ring true for you?"* Then shut up. A polite nod is not a signal; you're listening for whether they latch on with a real story. Reading this list at someone is leading the witness — don't.

Source-quality note: this leans on G2/Capterra and event-industry trade press. Reddit-specific threads were thin (`site:reddit.com` queries mostly returned no indexed hits). Where AU signal is genuinely thin, I've said so rather than padding.

---

## Pain category 1: At-the-event failures

**Pattern:** Connectivity drops, dead tablets, and app glitches during the actual event window — when there's no time to debug. Backup plans rarely exist.

**Documented examples:**
- *"A dead tablet battery, spotty Wi-Fi, or an app glitch could bring your lead capture efforts to a halt. Having a backup plan is essential."* — Limelight Platform
- Vendors now sell offline-mode as a headline feature because venue Wi-Fi failure is treated as expected — ExpoPlatform
- Cvent LeadCapture users on Trustpilot/PissedConsumer report having to *"screenshot each lead from the app and type them in manually"* after download issues post-event

**Suggested unlock prompt:** *"I've heard from others that venue Wi-Fi at trade shows regularly drops out — and that the offline fallback in their tool either didn't sync properly or wasn't there at all. Has anything like that ever bitten you?"*

---

## Pain category 2: Data quality

**Pattern:** Paper handwriting can't be read; tire-kickers fake their email; no validation at the point of capture means the cleanup happens days later by someone who wasn't at the booth.

**Documented examples:**
- *"Illegible handwriting and incorrect email addresses rendered some forms unusable… both methods required hours of manually entering data into a spreadsheet, delaying follow-up."* — Integrate/Promega case study
- *"At busy trade show booths, qualified prospects walk away while tire-kickers fill out forms with fake information."* — Gushwork
- Salesforce Web-to-Lead junk leads are a perennial admin complaint; standard fix is CAPTCHA + honeypot + validation rules flagging keywords — Salesforce Ben

**Suggested unlock prompt:** *"When you go through last quarter's event leads, what proportion of them turn out to be unusable — illegible, fake email, junk? Some teams I've spoken to put it as high as 30%."*

---

## Pain category 3: Lead handoff & follow-up delay

**Pattern:** Leads sit in spreadsheets/scanner exports for days before reaching the CRM. By the time sales calls, the prospect has forgotten the conversation or talked to a competitor. Sales then blame marketing for "low quality."

**Documented examples:**
- *"Leads are manually compiled into a spreadsheet, 'cleaned up' days later, and finally uploaded to the CRM a week after the event. By then, any urgency is gone."* — Default.com
- *"Nearly 80% of trade show leads are never followed up on."* — widely-circulated industry claim (folklore-grade rather than rigorous, but it's the number marketers cite to each other)
- *"Teams leave the booth with just a spreadsheet of names and zero context, causing leads to go cold by Monday."* — Cvent LeadCapture critique, Blinq competitor comparison via Momencio

**Suggested unlock prompt:** *"I've heard the gap between capturing a lead at an event and it reaching a salesperson can be a week or more — long enough that the prospect's forgotten the conversation. What does that timeline actually look like for you?"*

---

## Pain category 4: Form-builder friction

**Pattern:** Generic templates that need rebuilding every event, branding limits unless you pay enterprise pricing, response caps that don't match event traffic spikes, and admin/seat limits that bottleneck the team that needs to make a quick change on the day.

**Documented examples:**
- Jotform: *"Not being able to have multiple people access Jotform admin is a significant drawback. It… creates a bottleneck in team flow, as only one person has the ability to edit and revise forms."* — Capterra
- Typeform: *"The Basic plan at $29/month only gets you 100 responses, and those limits are shared across ALL your forms."* + *"The complete lack of offline capability is a significant limitation."* — Capterra
- HubSpot Forms: *"Forms and surveys are severely limited in functionality and appearance for certain use-cases outside of traditional lead-generation."* — G2
- Jotform: *"Costs increase too fast once you outgrow the free plan… The Enterprise level… priced out of range for most teams."* — Capterra

**Suggested unlock prompt:** *"For one-off events, paying for a full enterprise SaaS subscription year-round can feel disproportionate. How does the budgeting on these tools sit with you?"*

---

## Pain category 5: Consent & compliance (AU-weighted)

**Pattern:** Spam Act 2003 requires demonstrable consent; the new Privacy Act tranche (assented Dec 2024) is tightening the definition. Audit trails proving who consented to what at which timestamp are commonly missing or fragmented across systems. Marketing teams running events in AU plus EU (or for AU companies marketing into EU) carry both obligations simultaneously.

**Documented examples:**
- Spam Act fines: *"up to $220,000 for a single breach, and as much as $2.1 million for subsequent breaches."* — ACMA / DLA Piper / Norton Rose Fulbright
- ACMA: consent buried in fine print or *"lengthy privacy policies or that require multiple click-throughs to find is not sufficient."* — Addisons summary
- 2024 Privacy Act reform: consent must now be *"voluntary, informed, current, specific and unambiguous."* The reform *"will put the practice of 'consent bundling' on shakier legal ground"* (one tickbox covering collection + marketing + third-party share). — Norton Rose Fulbright; ADMA
- OAIC has named marketing practices in its 2025–26 regulatory priorities — ADMA Privacy Series
- DSAR record-keeping pain: *"Teams relying on manual coordination, ad-hoc searches across disconnected systems, and email-based tracking create bottlenecks."* — DataGrail/Osano

**Suggested unlock prompt:** *"If somebody emailed you tomorrow and said 'prove I consented to your marketing on [date] at [event]' — how long would it take you to put your hands on that record?"*

---

## Pain category 6: Integration nightmares

**Pattern:** CSV re-key between event tool and CRM/MAP, field-mapping mistakes that surface weeks later, picklist-vs-free-text type mismatches, sync delays. Field-mapping errors are well-documented even in the most-used integration in the industry (HubSpot ↔ Salesforce).

**Documented examples:**
- *"A dropdown field in Salesforce won't sync neatly with a free-text field in HubSpot… you end up with errors, failed syncs, or values that make no sense to users on either side."* — NewBreed Revenue
- Multiple "Lead Source" / "Lead Source Detail" / "Original Source" variants cause routing confusion — NewBreed Revenue
- HubSpot has one record for leads+contacts; Salesforce separates them — this is the structural trap that makes event leads land in the wrong object — RevPartners
- HubSpot community recurrently features people whose Salesforce field *"isn't available"* in the integration mapper

**Suggested unlock prompt:** *"How do leads from your last event actually get into your CRM — manual import, integration, or somewhere in between?"*

---

## Pain category 7: Multi-stakeholder messes

**Pattern:** Agency builds the form, brand team rejects the look. Marketing ops can't extract data without IT. Approvals take longer than the lead time before the event. Nobody has admin access on the day a field needs changing.

**Documented examples:**
- Jotform admin-bottleneck quote (above) is a direct manifestation of this pattern at the tool level.
- HubSpot G2 users: *"Marketing contacts that unsubscribed could not be resubscribed by them filling out a new form — the only way to resubscribe them was through the 'manage preferences' link in an email they received in the past."* — G2 (an example of marketing-ops pain that ends up being an *external* user-experience problem)

**Honest gap:** I couldn't find strong documented examples of "agency built it, brand rejected it" or "approval delays before publish" in public reviews — these likely live in private Slacks, agency post-mortems, and LinkedIn rants that don't surface in search. Treat this as a category to *probe in interviews* rather than one with strong public corroboration.

**Suggested unlock prompt:** *"On a typical event form, how many people need to touch it before it goes live — and what's the bottleneck?"*

---

## Pain category 8: Kiosk / unattended capture

**Pattern:** Tablet left on a stand for self-serve capture; previous person's data still on screen; no auto-reset; embarrassing exposure or APP-breach territory.

**Documented examples:**
- Jotform's own kiosk-mode docs implicitly acknowledge the problem: *"The kiosk will reset automatically after the inactivity period you set… The form automatically returns to the start page after each submission, and each session remains separate to keep respondent data secure."* — Jotform docs (the fact that this needs to be configured, and is off by default in many tools, is the pain)
- Android tablet kiosk-mode guides note the failure modes when not configured: *"Users can browse YouTube, dig into Settings, or download apps."* — Esper / Scalefusion / 42Gears

**Honest gap:** Specific complaint threads about "previous attendee's data still visible" are sparse in public sources — this likely happens but doesn't get tweeted about because it's embarrassing. Worth probing in interviews; weak public corroboration.

**Suggested unlock prompt:** *"When you've used a tablet on the booth as a self-serve form, how confident are you that the next person didn't see the previous person's details?"*

---

## Pain category 9: Agency-specific pain

**Pattern:** Client lost access after project ended; multi-tenant data leakage risk; "Powered by [vendor]" footer embarrassing on premium client work; reseller billing complexity.

**Documented examples:**
- Jotform white-label page is upfront that white-label is an Enterprise feature: *"removing Jotform branding"* is gated to the top tier — Jotform Enterprise white-label page (the gating itself is the agency pain)
- SPP.co positions explicitly around agency form workflows (order/intake/onboarding/contact) suggesting agencies don't get those flows from generic builders — SPP.co

**Honest gap:** Agency-specific reseller complaints (multi-client data leaks, lost-access-after-project) didn't surface in indexed reviews. This is a category where the founder's interview pool will be the primary source rather than secondary research. **Don't lean on this section as evidence; lean on it as a list of things to *ask about*.**

**Suggested unlock prompt:** *"When a project wraps with a client, what happens to the form and the data — who keeps the keys?"*

---

## Pain category 10: Developer-pain-from-marketing-handoff (IMPORTANT)

**Pattern:** Marketing has a requirement that the off-the-shelf form tool can't handle (AU address validation, embedded payment, conditional logic, audit trail, custom CRM object). Engineering ends up building bespoke. Multiple weekends disappear. The thing then becomes load-bearing and unmaintained.

**Documented examples:**

**AU address validation (Geoscape / G-NAF):**
- Geoscape themselves describe G-NAF as *"a complex and large dataset (~5GB unpacked), consisting of multiple tables that will need to be joined prior to use… primarily designed for application developers and large-scale spatial integration."* They shipped a simplified product (G-NAF Core) specifically to *"[reduce] the need to select fields and build data relationships"* — i.e. the vendor confirmed the integration pain by building a workaround for it. — Geoscape docs
- A whole cottage industry exists because rolling your own is hard: Addressr (open source), Addressify, SmartAddress, Addresser, AddressFinder. Each is a "we ate the G-NAF integration pain so you don't have to" business. The Elastic blog post on "real-time address search with G-NAF and Elasticsearch" exists as an artefact of this being a real engineering project.
- Address-validation APIs assume connectivity, which collides head-on with the at-the-event failure pattern (category 1).

**Stripe / embedded payment:** WPForms, Gravity Forms, Formidable, Everest Forms all gate Stripe + conditional payments behind Pro tiers — the signal: builders add the feature when they notice customers leaving to build it custom.

**Conditional logic:** Typeform Capterra — *"Complex conditional inputs are limited."*

**Consent capture with audit trail:** see category 5. The combination of "specific, unambiguous, timestamped, durable, tied to the consent-text version that was live at submission time" is what generic form builders typically don't ship.

**CRM custom-object mapping:** where category 6 pain bites hardest — see HubSpot Community "field unavailable in mapper" threads.

**File upload + virus scanning, phone validation across countries:** not strongly documented in this scan — honest gaps. Probe in interviews if relevant.

**Multi-step / save-progress:** SurveyMonkey/Typeform free-tier caps and feature-gating make this an upgrade trigger; friction not war story. — Capterra

**Suggested unlock prompt:** *"Have you ever had a marketing team come to you with a form requirement that should have been easy in [Typeform/Jotform/HubSpot Forms] but ended up being a custom build? What was the requirement?"*

---

## Competitor review patterns (G2 / Capterra summary)

| Competitor | Most common complaints (paraphrased from reviews) |
|---|---|
| **Jotform** | Single-admin bottleneck; pricing scales aggressively past free tier; ticket support quality poor; mobile-app lag on complex forms; cluttered UI for new users |
| **Typeform** | Free plan severely capped (10 responses/mo); response limits shared across all forms; no offline capability; conditional logic limited; HIPAA gated to Enterprise; design customisation restricted |
| **HubSpot Forms** | Cost scaling with contact growth; functionality limited outside classic lead-gen use cases; can't resubscribe via new form; reporting customisation gated to higher tiers |
| **Cvent LeadCapture** | Captures names from badges but no conversation context; download/export failures forcing manual screenshot transcription; aggressive auto-renewal/contract enforcement; steep learning curve; lowest-rated of the competitive set in one March 2026 comparison |
| **SurveyMonkey** | Free plan caps responses (~25 visible) and questions (10); advanced features paywalled; design/branding limited; expensive for low-volume users (~$500/yr cited); priority support gated |
| **Microsoft Forms** | Easier setup than SurveyMonkey but customisation thinner; data-export better than design — but limited as a marketing/lead-capture tool rather than internal-survey tool |
| **Captello** | Method-switching friction (badge vs QR vs business card); occasional scanner inaccuracy; data import/export cumbersome (overall sentiment positive though) |
| **iCapture** | Generally positive in reviews; support strongly rated; complaints thin in this scan |
| **Eventleaf** | Check-in app gated to higher tiers; registration-to-contact-list sync unreliable for some users; limited branding customisation; recurring-event cancellation awkward; documentation thin |
| **Momencio** | Setup clunky; no event cloning; steep learning curve; iOS app bugs; business-card OCR misses fields; multi-step workflows require many taps |

---

## AU-specific signals

- **Privacy Act reform is live.** Royal Assent 10 Dec 2024 on tranche one. New consent definition (voluntary, informed, current, specific, unambiguous) is enforceable. OAIC has named marketing practices a 2025–26 priority. "Consent bundling" forms are explicitly in the crosshairs.
- **Spam Act fines remain meaningful** ($220k single / $2.1m repeat). ACMA has said fine-print/click-through-buried consent is non-compliant.
- **G-NAF integration pain is acknowledged by Geoscape themselves** (via the G-NAF Core simplification) and by the cottage industry of paid AU address-validation services. Strongest documented AU dev-pain signal in this scan.
- **EEAA/ABEA and Mumbrella/AdNews signals are thin** for specific tool-pain commentary. EEAA merged into ABEA on 1 Jul 2023 — no published ABEA exhibitor pain report surfaced. Ask interviewees directly what they've seen at Mumbrella360 / ABEA / B2B Summit; don't rely on these as secondary sources.

---

## What surprised me

1. **Cvent LeadCapture rates worst of the major event-tech competitors in recent comparisons.** The "names off badges, no conversation context" critique is specific and repeated. If interviewees use Cvent, that's the wedge.
2. **G-NAF integration pain has its own cottage industry.** Multiple paid AU address-validation services exist purely because rolling your own is hard — that's a stronger market signal than any single quote. Most concrete documented AU dev-pain on the list.
3. **Privacy Act tranche one (Dec 2024) is a timing tailwind** most form builders haven't visibly responded to. "Consent bundling" — exactly what most generic form tickboxes do today — is now on shakier legal ground. Test in interviews whether marketing teams know this is changing; many won't, which is itself a signal.
4. **The single-admin bottleneck on Jotform was more specific than expected** — multi-stakeholder access is a real pain even in widely-used tools, not just an enterprise edge case.
5. **Reddit was thinner than expected.** `site:reddit.com` queries returned almost no indexed hits. Conversations likely live in private Slacks, LinkedIn comments, agency Discords. Worth lurking r/eventprofs and r/marketingops manually during interview prep — manual browse will likely surface more than search.

---

## Sources

**G2 / Capterra reviews:**
- Capterra — Jotform reviews: https://www.capterra.com/p/158456/JotForm-4-0/reviews/
- Capterra — Typeform reviews: https://www.capterra.com/p/137289/Typeform/reviews/
- G2 — HubSpot Marketing Hub reviews: https://www.g2.com/products/hubspot-marketing-hub/reviews
- G2 — SurveyMonkey reviews: https://www.g2.com/products/surveymonkey/reviews
- G2 — Microsoft Forms vs SurveyMonkey: https://www.g2.com/compare/microsoft-forms-vs-surveymonkey
- G2 — Cvent products: https://www.g2.com/sellers/cvent
- Trustpilot — Cvent: https://www.trustpilot.com/review/www.cvent.com
- PissedConsumer — Cvent: https://cvent.pissedconsumer.com/review.html
- Capterra — Eventleaf reviews: https://www.capterra.com/p/102609/Eventleaf/reviews/
- Capterra — Momencio reviews: https://www.capterra.com/p/168197/momencio/reviews/
- G2 — Captello vs iCapture comparison: https://www.g2.com/compare/captello-lead-capture-software-vs-icapture
- Surva.ai — Typeform Capterra summary: https://www.surva.ai/blog/typeform-capterra-d03f1

**Australian regulatory / industry sources:**
- DLA Piper Privacy Matters — Australia's e-marketing expectations: https://privacymatters.dlapiper.com/2024/08/australias-e-marketing-expectations-when-customers-dont-give-a-spam/
- Norton Rose Fulbright — Spam Act compliance: https://www.nortonrosefulbright.com/en/knowledge/publications/5615dd36/dont-filter-this-out-are-you-spam-act-compliant
- Norton Rose Fulbright — Privacy Act reform: https://www.nortonrosefulbright.com/en/knowledge/publications/be98b0ff/australian-privacy-alert-parliament-passes-major-and-meaningful-privacy-law-reform
- ACMA — Avoid sending spam: https://www.acma.gov.au/avoid-sending-spam
- Addisons — ACMA consent expectations: https://addisons.com/article/the-acma-has-issued-a-statement-about-its-expectations-for-using-consent-to-conduct-e-marketing-and-telemarketing/
- ADMA — OAIC 2025-26 marketing priorities: https://adma.com.au/resources/privacy-series-oaic-targets-marketing-practices-2025-26-regulatory-priorities
- ADMA — Understanding Consent: https://adma.com.au/resources/privacy-series-understanding-consent
- OAIC APP 7 Direct Marketing: https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-7-app-7-direct-marketing

**Geoscape / AU address validation:**
- Geoscape G-NAF product page: https://geoscape.com.au/products/g-naf/
- Geoscape G-NAF Data Product Description: https://docs.geoscape.com.au/_/downloads/gnaf_desc/en/stable/pdf/
- Geoscape National Address Verification: https://geoscape.com.au/products/national-address-verification/
- data.gov.au G-NAF dataset: https://data.gov.au/data/dataset/geocoded-national-address-file-g-naf
- Mountain Pass `addressr` (open source): https://github.com/mountain-pass/addressr
- Elastic blog — real-time AU address search with G-NAF: https://www.elastic.co/blog/realtime-address-search-with-australian-gnaf

**Trade show / event lead capture commentary:**
- Limelight Platform — pros/cons of trade show lead capture apps: https://www.limelightplatform.com/blog/pros-and-cons-of-using-a-trade-show-lead-capture-app
- ExpoPlatform — trade show lead capture: https://expoplatform.com/blog/lead-retrieval/trade-show-lead-capture/
- Integrate — Promega case study (paper to digital): https://www.integrate.com/case-studies/promega
- Integrate — Event Marketer's Guide to Lead Capture Forms: https://www.integrate.com/blog/guide-lead-capture-forms
- Default.com — trade show follow-up: https://www.default.com/post/following-up-on-trade-show-leads
- MarkEmpa — why trade show follow-up fails: https://www.markempa.com/trade-show-follow-up-tips/

**CRM integration / Salesforce:**
- NewBreed Revenue — HubSpot-Salesforce integration problems: https://www.newbreedrevenue.com/blog/hubspot-salesforce-integration-problems
- RevPartners — HubSpot Salesforce integration guide: https://blog.revpartners.io/en/revops-articles/an-expert-guide-to-a-hubspot-salesforce-integration
- Salesforce Ben — Web-to-Lead admin playbook: https://www.salesforceben.com/the-admins-playbook-for-web-to-lead-in-salesforce-security-routing-and-data/
- HubSpot community — Salesforce field mapping threads: https://community.hubspot.com/t5/Sales-Integrations/Field-unavailable-in-Salesforce-Integration-mapping/m-p/564571

**Consent / DSAR / GDPR record-keeping:**
- Reform.app — preparing consent records for GDPR audits: https://www.reform.app/blog/5-steps-to-prepare-consent-records-for-gdpr-audits
- DataGrail — DSAR glossary: https://www.datagrail.io/glossary/data-subject-access-request-dsar/
- Osano — DSAR guide: https://www.osano.com/articles/data-subject-access-requests-guide
- DPN — GDPR consent records: https://dpnetwork.org.uk/gdpr-consent-evidence/

**Kiosk mode:**
- Jotform — kiosk mode docs: https://www.jotform.com/help/571-how-to-use-kiosk-mode-in-jotform-mobile-forms/
- Esper — Android kiosk mode: https://www.esper.io/blog/android-kiosk-mode-vs-kiosk-software

**AU industry bodies (limited signal in this scan):**
- ABEA: https://www.abea.org.au/
- EEAA / Exhibitions & Events Australia: https://eea.net.au/
- Mumbrella: https://mumbrella.com.au/

**Categories where Reddit search returned no usable indexed results in this scan** (worth manual browse by the founder): r/eventprofs, r/marketingops, r/B2BMarketing, r/AusBusiness, r/webdev developer war stories.
