# Story 5.5: Preview/Production Governance Foundations

**Epic:** Epic 5 - Form Builder Readiness + Review & Publishing  
**Domain:** Form Builder, Public Runtime, Submissions  
**Status:** Implementation Complete — Migration + Manual UAT Pending 
**Priority:** High (foundation for publish flow)  
**Created:** 2026-02-16  
**Owner:** Developer Agent  

---

## 📖 User Story

**As a** Company User or Company Admin,  
**I want** clear separation between preview and production form submissions, with a configurable test threshold and readiness visibility,  
**So that** I can test forms safely before publishing, know when I'm ready to publish, and avoid polluting production data with preview tests.

**Context & entry point:**  
- Stories 5.1–5.4 are complete: assets, company defaults, schema validation, shared resolver parity.  
- Today: public forms can be opened with a token; submissions may not clearly distinguish preview vs production.  
- Epic Phase B requires: preview/production toggle, test threshold gating (optional per company), readiness badges.

---

## 🧭 Scope Boundary

### In scope (Story 5.5)

- **Preview vs Production mode**
  - Clear separation in UI and in stored submissions (flags/metadata).
  - Submissions store `is_preview` (or equivalent) so they can be filtered/separated.
  - Ability to filter and (optionally) delete preview submissions for hygiene.
- **Test threshold gating**
  - Optional per company (enabled/disabled).
  - Threshold is adjustable (platform default + company override in `config.AppSetting` or company settings).
  - Block publish **only when enabled** and threshold is not met (with clear UI messaging).
  - Define what counts as a "test": preview submission **or** explicit "Record test run" action (supports static/no-input forms).
  - Audit trail of test runs (who, when, form version).
- **Readiness badges**
  - Builder or dashboard surface shows readiness status (e.g. "Ready to publish" when threshold met, "X more test runs needed" when not).
- **Form status model**
  - Support draft / pending review / published / unpublished states where needed for this story (minimal; full model may extend into 5.6/5.7).

### Out of scope (Story 5.5)

- Publish request + review flow (Story 5.6).
- Admin Review and Publish UI (Story 5.6+).
- Public URL + activation windows (Story 5.7).
- Full publish/unpublish workflow (partial in 5.5; complete in 5.6/5.7).

---

## 🎯 Done Criteria

- [ ] **DC1:** Submissions store preview vs production flag; backend and API support filtering by mode.
- [ ] **DC2:** Test threshold configurable per company (enabled/disabled, threshold value); stored in DB or `config.AppSetting`.
- [ ] **DC3:** Test runs (preview submissions + "Record test run") are counted and audited (who, when).
- [ ] **DC4:** Publish is blocked when threshold enabled and not met; UI shows clear message (e.g. "X more test runs needed").
- [ ] **DC5:** Readiness badge or equivalent visible in Builder or Dashboard.
- [ ] **DC6:** UAT guide executed and marked PASSED.
- [ ] **DC7:** Story PR merged to `master`.

---

## 📐 References

- Epic scope: `docs/stories/EPIC-5-STATUS.md` (Phase B: Review/Test/Publish Governance)
- PRD: `docs/prd.md` (Preview/Testing, Publish flow)
- Story 5.4 resolution rules: `docs/stories/STORY-5.4-RESOLUTION-RULES.md`
- Git workflow: `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

---

*Story 5.5 - Preview/Production Governance Foundations*  
*Last Updated: 2026-02-16*
