# Story 6.3 — Benchmark prompts & outcomes (review sheet)

**Purpose:** One place to read the **canonical UAT prompt** for each benchmark, what **outcome** means in **mocked CI** vs **live Builder**, and how to wire **agency** access for `user2@test.com`.

---

## Important: what was / was not created in the database

| Question | Answer |
|----------|--------|
| Single **Event** with **10 Forms** attached for review? | **No.** Story 6.3 automation added **pytest** only (`test_story_63_benchmark_harness.py`). Nothing inserted into `dbo.Event` / `dbo.Form` for the benchmarks. |
| Where is the “outcome” for CI? | Valid `DefinitionJSON` built in code as `_bm01()` … `_bm10()` in that test file, passed through `generate_form_definition` with **`_request_chatgpt_completion` mocked**. Outcomes are also summarized in `STORY-6.3-BENCHMARK-BASELINE.md`. |
| How do I review **real** layouts in the product? | For each benchmark: open **Form Builder** on a draft → **AI** panel → paste the prompt below → **Generate** → inspect **canvas** (see `STORY-6.3-UAT-TEST-GUIDE.md` §5). Or create ten draft forms under one event manually / via a future seed script. |

If you want a **one-click seed** (one event + ten draft forms + definition JSON from the harness fixtures), that is **new work** (script + your DB); it was not part of the Story 6.3 AC set.

---

## AI panel: is the prompt still visible after Generate?

**Yes.** The prompt `textarea` is controlled by React state and is **not** cleared on success or failure—`handleGenerate` never calls `setPrompt("")`. After a successful run you still see the text you pasted; status and trace appear below it.

---

## All 10 benchmarks — prompt (canonical) + CI outcome

Prompts below are copied from `STORY-6.2-BENCHMARK-FORMS.md` (“### Prompt to AI”).  
**CI outcome:** `status == "completed"`, **single page**, component **types** match the Expected Fields table (see `test_story_63_benchmark_harness.py` for exact type sets). The test uses **slightly paraphrased** prompts in code for heading / post-processing guardrails; for **human UAT**, prefer the **canonical** blockquotes here.

### 1 — Party RSVP

**Prompt**

> "Create an RSVP form for a party. I need the guest's full name, phone number, email, whether they will attend (Yes/No radio buttons), how many people they're bringing (number field), and a submit button."

**CI outcome (mocked):** Types: `text`, `phone`, `email`, `radio`, `number`, `submit-button`. Fixture: `_bm01()`.

---

### 2 — Contact + address

**Prompt**

> "Create a contact form with the person's name (first and last name as separate fields), their address, phone number, email (required), company name, and a comments text area. Add a submit button."

**CI outcome (mocked):** Types: `text`, `address`, `phone`, `email`, `textarea`, `submit-button` (two `text` name fields). Fixture: `_bm02()`.

---

### 3 — Event registration

**Prompt**

> "Build a registration form for a tech conference. Include first name, last name, email address, phone number, company name, job title, and a country dropdown with these options: Australia, United States, United Kingdom, Canada, New Zealand, Other. Add a submit button labeled 'Register'."

**CI outcome (mocked):** Types: `text`, `email`, `phone`, `dropdown`, `submit-button`. Fixture: `_bm03()`.

#### Live iteration log (Form 403, AI panel)

| Timestamp (local) | RequestID | Retry cap | Profile | Terminal reason | Attempts | Validation summary | Outcome | Next focus |
|---|---|---:|---|---|---:|---|---|---|
| 2026-04-04 21:47 | `8b79892e-ebc8-4162-9993-4889b3582ed4` | 1 | `v1.0.0` | `validated-success` | 2 | `schema=0, bnd=0, coll=0` | Completed after one correction | Keep first-shot mode for cleaner section evaluation |
| 2026-04-04 22:08 | `14b64f84-8efe-4874-b81c-5c24215c6d8e` | 0 | `v1.0.0` | `retry-cap-exhausted` | 1 | `schema=8, bnd=0, coll=1` | Failed first-shot (draft returned) | Remove schema-invalid top-level component keys and tighten dropdown width semantics |
| 2026-04-04 22:25 | `a459699c-f516-4d74-a780-c46a686b8fef` | 0 | `v1.0.1` | `retry-cap-exhausted` | 1 | `schema=0, bnd=0, coll=1` | Schema lever succeeded (8→0), still one layout collision | Target dropdown vs submit spacing (or closed-control collision modeling parity) |
| 2026-04-05 06:02 | `305346b0-18f4-4b25-943e-587e9347e2e5` | 0 | `v1.0.1` | `retry-cap-exhausted` | 1 | `schema=0, bnd=0, coll=6` | Selection-height fix removed `country<->submit`, but generated layout introduced multiple true overlaps | Add one layout lever: enforce non-overlap row packing for paired columns + reserve exclusive x-ranges per row |

Frontend section events recorded for the 22:08 run (`SessionID: sess_d5fa9a7b-bb67-4894-9c49-3e2c53de3be5`):
- `ai.sections.run.start` (`maxSystemCorrectionAttempts=0`, `sectionCount=6`)
- `ai.sections.run.result` (`status=failed`, `terminalReason=retry-cap-exhausted`)

Validator breakdown for RequestID `14b64f84-8efe-4874-b81c-5c24215c6d8e`:
- Schema errors (8): extra top-level `tabOrder` keys at `pages.0.components.[2..9].tabOrder` (`extra_forbidden`).
- Collision (1): `para-event <-> firstName` on `page-1`, overlap area `7840.0`.

Validator breakdown for RequestID `305346b0-18f4-4b25-943e-587e9347e2e5`:
- Schema errors (0), boundary violations (0), collisions (6).
- Collision pairs:
  - `company <-> jobTitle` (`26624.0`)
  - `email <-> phone` (`26624.0`)
  - `event-header <-> lastName` (`30720.0`)
  - `event-header <-> phone` (`4080.0`)
  - `event-paragraph <-> phone` (`23040.0`)
  - `firstName <-> lastName` (`26624.0`)

---

### 4 — Job application

**Prompt**

> "Create a job application form. I need first name, last name, email, phone, location (text field), LinkedIn profile URL, a 'Why are you interested?' text area, a file upload for resume, a 'How did you hear about us?' dropdown (Company Website, LinkedIn, Facebook, Referral, Other), and a checkbox for 'I agree to the privacy policy'. Add a submit button labeled 'Apply Now'."

**CI outcome (mocked):** Includes `file-upload`, `url`, `terms`, `dropdown`, `textarea`, etc. Fixture: `_bm04()`.

---

### 5 — Customer feedback

**Prompt**

> "Build a customer feedback form. Start with a heading 'Customer Feedback'. Add a rating component for 'How would you rate your overall experience?' (1-5 stars). Then a 'How likely are you to recommend us?' rating (0-10 scale with labels 'Not likely' to 'Very likely'). Add a 'What did you like most?' text area and 'What could we improve?' text area. Include a 'How did you find us?' dropdown (Search Engine, Social Media, Friend, Advertisement, Other). Finish with a Submit button."

**CI outcome (mocked):** `header`, two `rating`, `textarea`, `dropdown`, `submit-button`. Fixture: `_bm05()`.

---

### 6 — Merchandise order

**Prompt**

> "Create an order form for merchandise. Include customer name (first and last as separate fields), email, phone number, a shipping address field, and a 'How did you hear about us?' checkbox group with options: Facebook, Instagram, Twitter, YouTube, Television, Internet Search, Referral, Other. Add a 'Special Instructions' text area and a submit button labeled 'Place Order'."

**CI outcome (mocked):** Includes large `checkbox` option set. Fixture: `_bm06()`.

---

### 7 — Newsletter minimal

**Prompt**

> "Create a minimal newsletter signup. Add a heading 'Stay in the loop', a paragraph that says 'Get the latest updates delivered to your inbox.', an email address field, and a subscribe button."

**CI outcome (mocked):** `header`, `paragraph`, `email`, `submit-button`. Fixture: `_bm07()`.

---

### 8 — Pre-order date/time

**Prompt**

> "Create a pre-order form. Include full name (first, last, and middle name as 3 separate text fields), phone number (required), email (required), delivery address, a preferred delivery date picker, a preferred delivery time picker, a 'Special delivery notes' text area, and a submit button labeled 'Place Pre-Order'."

**CI outcome (mocked):** Three `text` name fields, two `date` (`dateType` date + time), etc. Fixture: `_bm08()`.

---

### 9 — Support ticket

**Prompt**

> "Create a support ticket form with a heading 'Submit a Support Request'. Include name, email address, order or reference number (optional), issue category dropdown (Billing, Technical, Account, Shipping, Other), priority dropdown (Low, Medium, High, Urgent), a subject line text field, a 'Describe your issue' text area, and a file upload for attachments (accept images and PDFs). Add a submit button labeled 'Submit Request'."

**CI outcome (mocked):** `header`, `text`, `email`, two `dropdown`, `textarea`, `file-upload`, `submit-button`. Fixture: `_bm09()`.

---

### 10 — Sales lead

**Prompt**

> "Build a sales lead form. Include a heading 'Talk to Sales', first name, last name, work email, phone number, company name, company size dropdown (1-10, 11-50, 51-200, 201-500, 500+), a 'How interested are you?' rating (1-5 stars), a message text area, a terms checkbox 'I consent to receiving marketing communications', and a submit button labeled 'Get in Touch'."

**CI outcome (mocked):** `header`, `text`, `email`, `phone`, `dropdown`, `rating`, `textarea`, `terms`, `submit-button`. Fixture: `_bm10()`.

---

## Give `user2@test.com` agency access to an event

Access is **company-scoped**: the user’s **`CompanyID`** (via `dbo.UserCompany`) must have an **`dbo.EventCompany`** row on the target **`EventID`** with role **`agency_form_builder`** (`ref.EventCompanyRole`).

### 1) Resolve the user’s company

Run against your database (adjust schema if your install differs):

```sql
SELECT u.UserID,
       u.Email,
       uc.CompanyID,
       c.CompanyName,
       ucr.RoleCode AS UserCompanyRole
FROM dbo.[User] u
INNER JOIN dbo.UserCompany uc ON u.UserID = uc.UserID AND uc.IsDeleted = 0
INNER JOIN dbo.Company c ON uc.CompanyID = c.CompanyID AND c.IsDeleted = 0
LEFT JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
WHERE u.Email = N'user2@test.com'
  AND u.IsDeleted = 0;
```

If the user belongs to **multiple** companies, pick the **agency** company that should build forms for the host’s event.

### 2) Link agency company to the event

Use `scripts/link_agency_company_to_event.sql` in this repo:

- Set `@EventID` to the host event.
- Set `@AgencyCompanyID` to `user2@test.com`’s **agency** `CompanyID` from step 1.
- Set `@HostCompanyID` to the **event owner** company (`dbo.Event.CompanyID`).
- Set `@CreatedByUserID` to a host admin user (often the event owner company’s admin).

That script upserts `dbo.EventCompany` with **`agency_form_builder`**.

### 3) Forms under one event

After the link exists, `user2@test.com` (acting as that agency company) can create or open forms **for that `EventID`** per the usual **agency_form_builder** rules in `modules/forms/service.py`. Creating **ten** named drafts is still manual or requires a separate seed—there is no merged automation for that today.

---

## References

- `docs/stories/STORY-6.2-BENCHMARK-FORMS.md` — full expected-field tables and rubric  
- `backend/tests/test_story_63_benchmark_harness.py` — CI fixtures `_bm01`–`_bm10`  
- `docs/stories/STORY-6.3-BENCHMARK-BASELINE.md` — pass table + run metadata  
- `scripts/link_agency_company_to_event.sql` — agency link template  
- **Form AI first-shot tuning (BMAD):** `_bmad/bmm/workflows/form-ai-first-shot-tuning/` — experiment review template, 5-run blocks, checkpoint between blocks; agent `_bmad/bmm/agents/form-builder-master.md`; EventLead CLI `backend/scripts/form_ai_first_shot_tune.py`  
