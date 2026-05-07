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

### 2.1 AI Agent Panel Enhancements

- Add a new section or set of dropdown controls in the AI Agent panel for **situational awareness / clarification questions**.
- Minimum initial set of dropdowns (exact list to be confirmed in implementation):
  - Audience Locale (pre-populated, editable override)
  - Form Purpose / Use Case (e.g., Event Registration, Lead Capture, Feedback, Waiver, etc.)
  - Target Respondent Type (e.g., Attendee, Member, Customer, Staff, Public)
  - Any additional high-value clarification fields identified during implementation.

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
| Full multi-locale prompt sweep | Still AU-first until verification complete |
| Image-to-form or style intent | 6.5b series |
| PII detection or clarification | 6.5c |
| New component types | Out of scope |
| Running Alembic (if migration required) | Tony executes |

---

## 4) Acceptance Criteria

1. **AC-1** Situational awareness dropdowns appear in the AI Agent panel.
2. **AC-2** Locale dropdown is pre-populated from existing resolution logic.
3. **AC-3** User can change the locale in the dropdown; the override is respected in the generated form.
4. **AC-4** The selected locale and other clarification values are passed correctly to the generation backend.
5. **AC-5** No regressions in existing generation behaviour when dropdowns are left at defaults.
6. **AC-6** Focused tests cover the new request parameters and locale override path.
7. **AC-7** UAT confirms the UX is intuitive and the help text is clear.
8. **AC-8** Evidence (screenshots or trace) shows correct locale being used in the system prompt when overridden.

---

## 5) Definition of Done

- Story branch pushed to Draft PR #87.
- All ACs met and verified.
- Story closeout report created with UAT results.
- EPIC-6-STATUS.md and EPIC-6-WORKFLOW-GUIDE.md updated.
- No Alembic commands run by agent (if a migration is needed).

---

## 6) Evidence & References

- AI Agent panel from Story 6.4
- Locale resolution logic in `backend/modules/form_ai/service.py` (`_resolve_audience_locale`)
- `FormAiGenerateRequest` schema
- Story 6.4.8 production prompt context (migration 072)

---

**Next:** Dev implements in the worktree at `C:\wt\elp\story-epic6-6.5a-clarification-questions`.