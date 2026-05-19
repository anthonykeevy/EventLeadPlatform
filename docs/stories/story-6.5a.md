# Story 6.5a - Clarification Questions: Situational Awareness Dropdowns + Locale Override in AI Agent Panel

**Epic:** 6 - AI Generation & Monetization Engine  
**Story ID:** 6.5a  
**Title:** Clarification Questions: Situational Awareness Dropdowns + Locale Override in AI Agent Panel  
**Status:** Draft / Ready for Dev  
**Branch:** `story/epic6-6.5a-clarification-questions`  
**PR:** [#87](https://github.com/anthonykeevy/EventLeadPlatform/pull/87) - Draft PR to `master`  
**Created:** 2026-05-07  
**Depends On:** Story 6.4.8 (AU production prompt context) merged.  
**Unblocks:** Improved AI Agent panel for multi-locale form design and better clarification UX.

---

## 1) Goal

Extend the AI Agent panel (introduced and polished in Story 6.4) with **situational awareness clarification questions** presented as dropdowns. 

The panel must:
- Pre-populate the audience locale based on the current context (user/company/event).
- Allow the user to explicitly override the locale when they are designing a form for a customer or event in a **different locale** from their own.

This provides the AI with better situational context for generating accurate, locale-appropriate forms while giving users explicit control.

---

## 2) In Scope

### 2.1 Research Summary (included for Dev context)

**Existing Countries with Locale Data (from Story 6.4.4.1 seeds + PromptTemplateLocaleBlock):**
- AU, NZ, UK, US, CA, IE, DE, INTL_ONLINE, APAC, EU, NEUTRAL

**Identified Gaps for Current Countries (to be filled in this story):**
- Many countries have only basic `format`/`policy`/`tone` blocks; missing richer situational guidance (e.g., common event types, industry-specific consent wording, typical respondent expectations).
- No dedicated reference data yet for **Form Purpose** or **Respondent Type** — these will be new DB-driven dropdowns.
- Limited help text / examples per locale for the new dropdowns.
- No API surface yet to serve these clarification options filtered by locale.

**New Reference Data to Introduce (scoped only to existing countries above):**
- `ref.FormPurpose` (or equivalent lookup) with locale-aware display names and prompt hints.
- `ref.RespondentType` with locale-aware labels.
- Optional locale-specific overrides or additional context for the above.

All new reference data will be seeded only for the 11 existing audience locales listed above. No expansion to new countries.

### 2.2 AI Agent Panel Enhancements

- Add a new section of dropdown controls in the AI Agent panel for **situational awareness / clarification questions**.
- **Three** clarification dropdowns (all populated from database via API; labels use `DisplayName`, persistence uses `Code` per architecture doc §12 / §16):
  1. **Audience Locale** — pre-populated, user can override.
  2. **Form Purpose / Use Case** — DB-driven options.
  3. **Target Respondent Type** — DB-driven options.
- A fourth dropdown (e.g. Industry) is **parked until after MVP** (architecture doc §16).

### 2.3 Data Flow Requirement (Mandatory)

Every selected dropdown value must:
- Be retrieved from the database via a new or extended API endpoint.
- Be included in the `FormAiGenerateRequest` (or runtime context).
- Be injected into the LLM system prompt (similar to how `locale_block` and `brand_posture_block` are currently injected in `_build_initial_messages`).
- Appear in `GenerationRun` trace metadata for auditability.

### 2.2 Locale Handling

- Locale dropdown is **pre-populated** from the existing audience locale resolution logic (Event → Company → User → AppSetting → fallback AU).
- The dropdown must allow the user to **change/override** the locale at generation time.
- When overridden, the selected locale becomes the authoritative `audienceLocale` for that generation request (passed through to `generate_form_definition`).
- The override is **per-generation** (not persisted as a permanent company preference unless explicitly designed that way in a later story).

### 2.3 Integration with Existing Flow

- The new dropdowns feed into the existing `FormAiGenerateRequest` (or a small extension of it).
- The selected values are included in the runtime context or as explicit parameters to the prompt assembly.
- No breaking changes to the current generation path.

### 2.4 Schema / Data Model

- Minor schema additions if needed to support the new clarification fields in the request or trace metadata.
- Ensure the values are captured in `GenerationRun` / trace for auditability.

### 2.5 UX / Accessibility

- Dropdowns follow existing AI Agent panel styling and patterns.
- Clear labels and help text explaining why the information helps the AI (e.g., "Helps generate the right date formats, phone patterns, and legal wording").
- Mobile-friendly.

---

## 3) Out of Scope (for this story)

| Item | Reason / Future Home |
|------|----------------------|
| Persisting locale override as Company default | Separate settings story |
| Full multi-locale prompt sweep or new countries | Still AU-first; only existing 11 locales in scope |
| Image-to-form or style intent | 6.5b series |
| PII detection or clarification | 6.5c |
| New component types | Out of scope |
| Running Alembic (if migration required) | Tony executes |
| Hardcoded dropdown options in frontend | All options must come from DB via API |
| Fourth dropdown (Industry, etc.) | Post-MVP (§16) |
| Full `PromptAssemblyProfile` for blocks A–I | Registry MVP story (companion architecture doc); 6.5a delivers Block E + `ref.AudienceLocale` |

---

## 4) Acceptance Criteria

**Architecture:** All prompt blocks A–I are database-driven (decision doc §4.1). This story delivers the **clarification tranche** (Block E, three `ref.*` tables, APIs, locale enum removal). Remaining blocks migrate via Prompt Assembly Registry MVP.

1. **AC-1** All **three** clarification dropdowns (Locale, Form Purpose, Respondent Type) are populated from the database via API (no hardcoded lists); UI shows `displayName`, requests persist `code`.
2. **AC-2** Dropdown options are scoped only to the existing 11 audience locales already seeded in the database.
3. **AC-3** Obvious gaps in reference data for the current countries are identified and filled during implementation (documented in the story closeout).
4. **AC-4** Selected values from every dropdown are included in the generation request and injected into the LLM system prompt.
5. **AC-5** Locale override works correctly and is reflected in the generated form content.
6. **AC-6** Focused backend tests cover the new API endpoints, request schema, and prompt injection.
7. **AC-7** UAT includes the 10 provided test prompts (see Section 7) executed in the frontend; dropdown selections visibly affect output.
8. **AC-8** No regressions when dropdowns are left at default values.
9. **AC-9** Help text explains the purpose of each dropdown and how it influences the AI.

---

## 5) Definition of Done

- Story branch pushed to Draft PR #87.
- All ACs met and verified.
- **Prerequisite:** `docs/architecture/decision-6.5a-clarification-options-data-model.md` produced by Dimitri, reviewed and approved by Tony.
- Research & Gap Analysis section completed and included in story documentation (countries, missing reference data, decisions made).
- New DB-driven API endpoints + reference data seeded for existing countries only.
- UAT executed with the 10 provided test prompts; results recorded.
- Story closeout report created with UAT results and gap-filling summary.
- EPIC-6-STATUS.md and EPIC-6-WORKFLOW-GUIDE.md updated.
- No Alembic commands run by agent (if a migration is needed).

---

## 6) Evidence & References

- AI Agent panel from Story 6.4
- Locale resolution logic in `backend/modules/form_ai/service.py` (`_resolve_audience_locale`)
- `FormAiGenerateRequest` schema
- Story 6.4.8 production prompt context (migration 072)
- Existing `PromptTemplateLocaleBlock` seeds for the 11 supported locales
- **Prerequisite Design Task:** `docs/architecture/decision-6.5a-clarification-options-data-model.md` (Dimitri to produce before Dev implementation)

---

## 7) UAT Test Prompts (Frontend Verification)

The following 10 prompts should be used during UAT. For each prompt, the tester changes one or more dropdowns and verifies that the generated form reflects the selected values (especially locale-specific formatting, legal wording, field labels, and tone).

1. "Create a registration form for a tech conference in Sydney"  
   (Test: AU locale + Event Registration purpose + Attendee respondent type)

2. "Build a feedback form for our annual member survey"  
   (Test: NZ locale + Feedback purpose + Member respondent type)

3. "I need a waiver form for a school sports day in Auckland"  
   (Test: NZ locale + Waiver purpose + Parent/Guardian respondent type)

4. "Create a lead capture form for a trade show in London"  
   (Test: UK locale + Lead Capture purpose + Visitor respondent type)

5. "Make a contact form for a US-based charity event"  
   (Test: US locale + Contact/Lead purpose + Donor respondent type)

6. "Registration form for a corporate training session in Toronto"  
   (Test: CA locale + Training/Professional Development purpose + Employee respondent type)

7. "Feedback form for a music festival in Dublin"  
   (Test: IE locale + Event Feedback purpose + Attendee respondent type)

8. "Create a consent form for a research study in Berlin"  
   (Test: DE locale + Research/Consent purpose + Participant respondent type)

9. "Lead generation form for an international online webinar"  
   (Test: INTL_ONLINE locale + Webinar/Online Event purpose + Global Attendee respondent type)

10. "Build a simple event registration form for a community group in Melbourne, but the audience is actually in Singapore"  
    (Test: Explicit locale override to a non-AU value while user context is AU)

**Expected UAT Evidence:** For each of the 10 prompts, capture before/after screenshots or generation traces showing that changing the dropdown values altered locale-specific elements (date format, phone pattern, legal references, tone, field labels) in the output.

---

**Next:** Dev implements in the worktree at `C:\wt\elp\story-epic6-6.5a-clarification-questions`.