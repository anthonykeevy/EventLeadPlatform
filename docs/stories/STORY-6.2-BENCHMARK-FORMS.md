# Story 6.2 — Benchmark Forms for AI Form Builder Evaluation

**Purpose:** 10 benchmark forms based on real third-party form builder templates (JotForm, Tally,
Cognito Forms, SurveyMonkey). Each card defines a prompt, expected fields, layout expectations,
and scoring criteria. The AI form builder must produce valid `DefinitionJSON` for each; output
is scored against the [Scoring Rubric](#scoring-rubric).

**Created:** 2026-03-20  
**Last Updated:** 2026-03-20  
**Source:** Real templates from third-party embeddable form builders

---

## Scoring Rubric

Each benchmark is scored 0–10 across five dimensions (max 50 per form, max 500 total).

| Dimension | What it measures |
|-----------|-----------------|
| **Field Completeness** | All expected fields present with correct types and labels |
| **Layout Quality** | Logical grouping, no overlaps, readable flow, good use of canvas space |
| **Schema Validity** | Passes `POST /api/form-validate` on first attempt (10) or after retries (partial credit) |
| **Prompt Fidelity** | Output matches what the user asked for — no missing intent, no hallucinated extras |
| **Visual Polish** | Reasonable sizing, spacing, alignment; looks intentional rather than random placement |

---

## Benchmark 1: Party RSVP Form

**Source:** JotForm — Party RSVP template  
**Category:** RSVP / Event Response  
**Complexity:** Low (7 fields)

### Prompt to AI
> "Create an RSVP form for a party. I need the guest's full name, phone number, email,
> whether they will attend (Yes/No radio buttons), how many people they're bringing
> (number field), and a submit button."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | Full Name | text | Yes | |
| 2 | Phone Number | phone | No | |
| 3 | Email | email | Yes | |
| 4 | Will you be attending? | radio | Yes | Options: Yes, No |
| 5 | How many guests? | number | No | |
| 6 | Submit | submit-button | — | |

### Layout Expectations
- Single column, vertical flow
- Radio buttons before number field (logical flow: "attending?" → "how many?")
- Simple, clean form — tests that AI doesn't over-engineer

---

## Benchmark 2: Contact Form with Address

**Source:** Cognito Forms — Basic Contact Form template  
**Category:** Contact / Enquiry  
**Complexity:** Medium (8 fields)

### Prompt to AI
> "Create a contact form with the person's name (first and last name as separate fields),
> their address, phone number, email (required), company name, and a comments text area.
> Add a submit button."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | First Name | text | Yes | |
| 2 | Last Name | text | Yes | |
| 3 | Address | address | No | |
| 4 | Phone | phone | No | |
| 5 | Email | email | Yes | |
| 6 | Company | text | No | |
| 7 | Comments or Questions | textarea | No | |
| 8 | Submit | submit-button | — | |

### Layout Expectations
- Two text fields for first/last name could be side by side or stacked
- Address field before contact fields
- Textarea at the bottom, larger than text inputs
- Tests: address component + mix of required/optional

---

## Benchmark 3: Event Registration Form

**Source:** Tally — Registration Form template  
**Category:** Event Registration  
**Complexity:** Medium (9 fields)

### Prompt to AI
> "Build a registration form for a tech conference. Include first name, last name,
> email address, phone number, company name, job title, and a country dropdown with
> these options: Australia, United States, United Kingdom, Canada, New Zealand, Other.
> Add a submit button labeled 'Register'."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | First Name | text | Yes | |
| 2 | Last Name | text | Yes | |
| 3 | Email Address | email | Yes | |
| 4 | Phone Number | phone | Yes | |
| 5 | Company | text | Yes | |
| 6 | Job Title | text | Yes | |
| 7 | Country | dropdown | Yes | 6 options specified |
| 8 | Register | submit-button | — | buttonText: "Register" |

### Layout Expectations
- First/last name logically paired
- Contact info (email, phone) grouped
- Professional info (company, job title) grouped
- Dropdown near bottom before submit
- Tests: dropdown with specific option list + custom button text

---

## Benchmark 4: Job Application Form

**Source:** Tally — Job Application Form template  
**Category:** Recruitment / HR  
**Complexity:** High (12 fields)

### Prompt to AI
> "Create a job application form. I need first name, last name, email, phone, location
> (text field), LinkedIn profile URL, a 'Why are you interested?' text area, a file upload
> for resume, a 'How did you hear about us?' dropdown (Company Website, LinkedIn, Facebook,
> Referral, Other), and a checkbox for 'I agree to the privacy policy'. Add a submit
> button labeled 'Apply Now'."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | First Name | text | Yes | |
| 2 | Last Name | text | Yes | |
| 3 | Email | email | Yes | |
| 4 | Phone | phone | No | |
| 5 | Location | text | No | |
| 6 | LinkedIn Profile | url | No | URL component |
| 7 | Why are you interested? | textarea | Yes | |
| 8 | Upload Resume | file-upload | Yes | acceptedFileTypes: ".pdf,.doc,.docx" |
| 9 | How did you hear about us? | dropdown | No | 5 options |
| 10 | Privacy Policy | terms | Yes | |
| 11 | Apply Now | submit-button | — | buttonText: "Apply Now" |

### Layout Expectations
- Dense form — 11 components tests spacing and layout decisions
- File upload should have clear visual distinction from text inputs
- URL field for LinkedIn
- Terms before submit button
- Tests: file-upload, url, terms, dropdown, textarea in one form

---

## Benchmark 5: Customer Feedback Survey

**Source:** SurveyMonkey — Customer Satisfaction Survey template (634K+ uses)  
**Category:** Feedback / Survey  
**Complexity:** Medium (8 fields)

### Prompt to AI
> "Build a customer feedback form. Start with a heading 'Customer Feedback'.
> Add a rating component for 'How would you rate your overall experience?' (1-5 stars).
> Then a 'How likely are you to recommend us?' rating (0-10 scale with labels
> 'Not likely' to 'Very likely'). Add a 'What did you like most?' text area and
> 'What could we improve?' text area. Include a 'How did you find us?' dropdown
> (Search Engine, Social Media, Friend, Advertisement, Other). Finish with a Submit button."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | Customer Feedback | header | — | |
| 2 | Overall Experience | rating | Yes | ratingMax: 5, ratingStyle: "stars" |
| 3 | Recommend Us | rating | Yes | ratingMax: 10, ratingStyle: "numbers", labels |
| 4 | What did you like most? | textarea | No | |
| 5 | What could we improve? | textarea | No | |
| 6 | How did you find us? | dropdown | No | 5 options |
| 7 | Submit | submit-button | — | |

### Layout Expectations
- Heading at top
- Two rating components (different scales — 5 stars vs 10 numbers)
- Two text areas should be similar size
- Tests: rating component (both star and numeric), heading, multiple textareas

---

## Benchmark 6: Merchandise Order Form

**Source:** JotForm — Merchandise Order Form template  
**Category:** E-commerce / Order  
**Complexity:** High (11 fields)

### Prompt to AI
> "Create an order form for merchandise. Include customer name (first and last as separate
> fields), email, phone number, a shipping address field, and a 'How did you hear about us?'
> checkbox group with options: Facebook, Instagram, Twitter, YouTube, Television, Internet Search,
> Referral, Other. Add a 'Special Instructions' text area and a submit button labeled
> 'Place Order'."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | First Name | text | Yes | |
| 2 | Last Name | text | Yes | |
| 3 | Email | email | Yes | |
| 4 | Phone Number | phone | No | |
| 5 | Shipping Address | address | Yes | |
| 6 | How did you hear about us? | checkbox | No | 8 options, multi-select |
| 7 | Special Instructions | textarea | No | |
| 8 | Place Order | submit-button | — | buttonText: "Place Order" |

### Layout Expectations
- Name fields logically paired
- Contact info before shipping address
- Checkbox group with many options takes more vertical space
- Tests: checkbox group with 8 options + address + custom button text

---

## Benchmark 7: Newsletter Signup (Minimal)

**Source:** Indie Hackers — Footer newsletter signup  
**Category:** Newsletter / Email Capture  
**Complexity:** Very Low (4 fields)

### Prompt to AI
> "Create a minimal newsletter signup. Add a heading 'Stay in the loop', a paragraph
> that says 'Get the latest updates delivered to your inbox.', an email address field,
> and a subscribe button."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | Stay in the loop | header | — | |
| 2 | Get the latest updates... | paragraph | — | |
| 3 | Email Address | email | Yes | |
| 4 | Subscribe | submit-button | — | buttonText: "Subscribe" |

### Layout Expectations
- Compact, centered layout — should NOT spread across full canvas
- Minimal vertical height
- Tests: AI restraint — should not add unnecessary fields or over-engineer
- Tests: paragraph component usage

---

## Benchmark 8: Pre-Order Form with Date/Time

**Source:** JotForm — Pre-Order Form template  
**Category:** Booking / Pre-order  
**Complexity:** High (11 fields)

### Prompt to AI
> "Create a pre-order form. Include full name (first, last, and middle name as 3 separate
> text fields), phone number (required), email (required), delivery address, a preferred
> delivery date picker, a preferred delivery time picker, a 'Special delivery notes' text area,
> and a submit button labeled 'Place Pre-Order'."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | First Name | text | Yes | |
| 2 | Middle Name | text | No | |
| 3 | Last Name | text | Yes | |
| 4 | Phone Number | phone | Yes | |
| 5 | Email | email | Yes | |
| 6 | Delivery Address | address | Yes | |
| 7 | Preferred Date | date | Yes | dateType: "date" |
| 8 | Preferred Time | date | No | dateType: "time" |
| 9 | Special Delivery Notes | textarea | No | |
| 10 | Place Pre-Order | submit-button | — | buttonText: "Place Pre-Order" |

### Layout Expectations
- Three name fields in logical order
- Date and time pickers could be paired visually
- Address before date/time
- Tests: date component in both date and time modes, 3 text fields for name parts

---

## Benchmark 9: Support Ticket Form

**Source:** Composite from Zendesk/Freshdesk support patterns  
**Category:** Customer Support  
**Complexity:** Medium (10 fields)

### Prompt to AI
> "Create a support ticket form with a heading 'Submit a Support Request'. Include name,
> email address, order or reference number (optional), issue category dropdown (Billing,
> Technical, Account, Shipping, Other), priority dropdown (Low, Medium, High, Urgent),
> a subject line text field, a 'Describe your issue' text area, and a file upload for
> attachments (accept images and PDFs). Add a submit button labeled 'Submit Request'."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | Submit a Support Request | header | — | |
| 2 | Your Name | text | Yes | |
| 3 | Email Address | email | Yes | |
| 4 | Order / Reference Number | text | No | |
| 5 | Issue Category | dropdown | Yes | 5 options |
| 6 | Priority | dropdown | Yes | 4 options |
| 7 | Subject | text | Yes | |
| 8 | Describe Your Issue | textarea | Yes | |
| 9 | Attachments | file-upload | No | acceptedFileTypes: ".pdf,.jpg,.png" |
| 10 | Submit Request | submit-button | — | buttonText: "Submit Request" |

### Layout Expectations
- Heading at top
- Two dropdowns (category + priority) logically grouped
- Textarea for description should be the largest field
- File upload after description
- Tests: heading, two dropdowns with specific options, file-upload, textarea sizing

---

## Benchmark 10: Sales Lead with Rating

**Source:** Composite from Monday.com lead form + NPS patterns  
**Category:** Lead Generation / Sales  
**Complexity:** High (12 fields)

### Prompt to AI
> "Build a sales lead form. Include a heading 'Talk to Sales', first name, last name,
> work email, phone number, company name, company size dropdown (1-10, 11-50, 51-200,
> 201-500, 500+), a 'How interested are you?' rating (1-5 stars), a message text area,
> a terms checkbox 'I consent to receiving marketing communications', and a submit button
> labeled 'Get in Touch'."

### Expected Fields
| # | Label | Component Type | Required | Notes |
|---|-------|---------------|----------|-------|
| 1 | Talk to Sales | header | — | |
| 2 | First Name | text | Yes | |
| 3 | Last Name | text | Yes | |
| 4 | Work Email | email | Yes | |
| 5 | Phone Number | phone | No | |
| 6 | Company Name | text | Yes | |
| 7 | Company Size | dropdown | Yes | 5 options |
| 8 | How interested are you? | rating | No | ratingMax: 5, stars |
| 9 | Message | textarea | No | |
| 10 | Marketing consent | terms | Yes | |
| 11 | Get in Touch | submit-button | — | buttonText: "Get in Touch" |

### Layout Expectations
- Heading at top
- Name fields paired
- Contact info grouped (email, phone)
- Company info grouped (name, size dropdown)
- Rating component between groups
- Terms before submit
- Tests: heading, dropdown, rating, terms, custom button text — many component types in one form

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total benchmarks | 10 |
| Component types tested | text, email, phone, url, number, date, dropdown, checkbox, radio, textarea, address, file-upload, rating, terms, submit-button, header, paragraph, divider |
| **New components tested** | url (BM4), file-upload (BM4, BM9), rating (BM5, BM10), paragraph (BM7) |
| Field count range | 4 (minimal) — 12 (complex) |
| Average fields per form | 8.5 |
| Forms with headings | 5 / 10 |
| Forms with dropdowns | 6 / 10 |
| Forms with textareas | 8 / 10 |
| Forms with file-upload | 2 / 10 |
| Forms with rating | 2 / 10 |
| Forms with terms | 2 / 10 |
| Forms with paragraph | 1 / 10 |
| Forms with url | 1 / 10 |

## Source Summary

| Benchmark | Source Builder | Template Name |
|-----------|--------------|---------------|
| 1 | JotForm | Party RSVP Form |
| 2 | Cognito Forms | Basic Contact Form |
| 3 | Tally | Registration Form |
| 4 | Tally | Job Application Form |
| 5 | SurveyMonkey | Customer Satisfaction Survey |
| 6 | JotForm | Merchandise Order Form |
| 7 | Indie Hackers | Newsletter Signup |
| 8 | JotForm | Pre-Order Form |
| 9 | Zendesk/Freshdesk | Support Ticket (composite) |
| 10 | Monday.com + NPS | Sales Lead (composite) |

---

## How to Use This Document

1. **Test Harness** — Feed each benchmark prompt through the AI generation pipeline.
2. **Score** — Evaluate output against expected fields, layout, and the 5 scoring dimensions.
3. **Track** — Record scores in a results matrix (to be created in the test harness).
4. **Iterate** — After context pack changes, re-run all 10 to detect regressions or improvements.
5. **Baseline** — First full run establishes the baseline; subsequent runs measure delta.
