# Story 6.4.8 - Promote AU-005 Into Production Prompt Context

**Epic:** 6 - AI Generation & Monetization Engine  
**Story ID:** 6.4.8  
**Title:** Promote AU-005 Into Production Prompt Context  
**Status:** Draft / Ready for Dev  
**Branch:** `story/epic6-6.4.8-au-production-prompt-context`  
**PR:** [#85](https://github.com/anthonykeevy/EventLeadPlatform/pull/85) - Draft PR to `master`  
**Created:** 2026-05-06  
**Depends On:** Story 6.4.7 ([PR #84](https://github.com/anthonykeevy/EventLeadPlatform/pull/84)) merged.  
**Unblocks:** Production AU prompt quality uplift and continuation toward image-to-form / broader AI launch readiness.

---

## 1) Goal

Promote the winning Story 6.4.7 AU prompt behaviour into the production Form AI prompt/context path.

Story 6.4.7 proved that `AU-005` is the strongest behaviour target (`4.471 / 5`, `89.4%`) and that `AU-006` is the best evidence for lint-clean conflict wording. This story converts those findings from eval-only overlays into durable production prompt/context storage so live generation benefits without relying on `system_prompt_addendum`.

Success means the production prompt/context store implements AU-005's strict AU + publish-ready behaviour, keeps AU-006's lint-clean conflict style, and passes targeted eval evidence without materially regressing policy, validation, or copy quality.

---

## 2) In Scope

### 2.1 Production prompt/context-store update

Update the production prompt/context source of truth, not the eval-only overlay.

**All prompt and context changes must be version-controlled.** Prompts are served exclusively from the database via `config.PromptTemplateVersion` (immutable versions) and `config.PromptTemplateLocaleBlock` (locale-specific blocks). The production path in `generate_form_definition` / `_build_initial_messages` resolves the active `PromptAssemblyProfile` and the latest active `PromptTemplateVersion` + locale blocks; no hardcoded prompt text or eval-only `system_prompt_addendum` is permitted for production behaviour.

Expected implementation targets:

- Create a **new** `PromptTemplateVersion` row (or update `PromptTemplateLocaleBlock` seeds for the active template) that encodes the AU-005 behaviour + AU-006 lint-clean wording.
- `backend/migrations/versions/...` seed migration that inserts the new versioned prompt/locale block records (never mutates existing active versions or old migration files).
- `backend/tests/form_ai_eval/au_locale_contract_v1.json` if the production AU contract needs versioned text aligned with the new prompt wording.
- Existing prompt assembly in `backend/modules/form_ai/service.py` only if required to support the production context shape cleanly (changes here must still route through versioned DB records).

The likely minimum implementation is a new migration after current head that:
- Inserts a new `PromptTemplateVersion` (or new `PromptTemplateLocaleBlock` rows) containing the AU production prompt content.
- Does **not** rewrite or edit any prior migration files.
- Leaves the current active `PromptTemplateVersion` and `PromptAssemblyProfile` unchanged until Tony reviews and promotes the new version.

Tony will review the generated migration, then manually update the alembic head and test before any promotion of the new version to active status.

### 2.2 Behaviour to preserve from AU-005

The production context must preserve these AU-005 behaviours:

- `audienceLocale = AU` is authoritative for generated form copy and component configuration.
- Use Australian English and AU conventions for phone, dates, address labels, currency, privacy, marketing-message consent, waivers, terms, and acknowledgements.
- When a user prompt includes foreign-market cues that conflict with AU, generate the Australian equivalent unless the form is explicitly collecting an external destination/source-market value.
- Include every material field group requested by the user.
- Make required/optional intent explicit through `validationIntent`.
- Use the most specific supported component type.
- Preserve requested sections, validation rules, and key options while applying AU localisation.
- Keep publish-ready ordering and copy:
  - identity/contact first,
  - form-specific choices next,
  - operational notes/preferences after that,
  - consent/terms near the end.
- Avoid adding address, organisation, role, or extra context fields unless requested or clearly necessary.
- Prefer checkbox or terms acknowledgement patterns over typed signatures unless a signature is explicitly requested.

### 2.3 Lint-clean wording from AU-006

Use AU-006's lesson for production phrasing:

- Do not paste long lists of forbidden foreign tokens into production prompt text.
- Describe categories of conflicting cues and substitution behaviour positively.
- Keep prompt-context lint at `0` findings.

Do not repeat AU-006's weaknesses:

- Generic privacy/marketing wording.
- Weak validation intent.
- Weaker copy polish.

### 2.4 Targeted p11-style fix

Add a targeted instruction for international event/timezone prompts:

- Avoid generated timezone options or labels that introduce foreign phone-code-like strings or overseas region names unless the form is explicitly collecting an external value.
- Preserve legitimate external destination/source-market collection when explicitly requested.

### 2.5 Verification and evidence

Run fast deterministic/focused tests first, then targeted AU eval evidence.

Required evidence:

- Focused tests for locale assembly/contract and affected prompt/context paths.
- Prompt-context lint remains `0` findings on the production candidate.
- AU deterministic generated-output findings are materially below the Story 6.4.6 baseline (`130`) and preferably close to AU-006's `3`.
- Judge/eval quality remains close to AU-005 and does not repeat AU-006 regressions in:
  - `policy_compliance`,
  - `validation_intent_accuracy`,
  - `copy_quality_score`.
- `p11` leakage is specifically reviewed.

---

## 3) Out of Scope

| Item | Reason / future home |
|---|---|
| New prompt-eval framework features | Story 6.4.6/6.4.7 already provide the needed harness. Raise a Dev-owned fix only if the harness blocks verification. |
| Frontend UI changes | This is production prompt/context storage and backend/eval verification only. |
| Broad six-locale sweep | AU launch quality remains the target. |
| Image-to-form / clarification UX / PII layers | Future Epic 6 stories after production AU prompt context is stabilised. |
| Running Alembic commands | Agents may create migration files but must not run Alembic upgrade/downgrade/revision/history/current. Tony runs migrations. |

---

## 4) Acceptance Criteria

1. **AC-1 Production source updated:** AU-005 behaviour is represented in production prompt/context storage, not as an eval-only `system_prompt_addendum`.
2. **AC-2 Migration prepared:** Any DB seed/context-store change is implemented as a new migration after current head; old migrations are not rewritten.
3. **AC-3 AU conflict wording lint-clean:** Production context uses AU-006-style positive conflict handling and avoids literal forbidden-token prompt-context lint.
4. **AC-4 AU legal/policy specificity preserved:** Production wording explicitly preserves Privacy Act 1988, Spam Act 2003, and AU-appropriate consent/terms/acknowledgement behaviour without becoming generic.
5. **AC-5 Validation and form completeness preserved:** Production wording keeps AU-005's field coverage, validation intent, component specificity, and publish-ready structure guard.
6. **AC-6 p11 risk addressed:** International event/timezone prompts avoid unintended foreign phone-code-like strings or overseas region names unless explicitly collecting external values.
7. **AC-7 Focused tests green:** Relevant locale assembly, locale resolution, migration static, prompt/eval, and judge/diff tests pass with exact summaries recorded.
8. **AC-8 Production candidate eval recorded:** AU production candidate run is recorded with deterministic AU findings and prompt-context lint evidence.
9. **AC-9 Judge/eval comparison recorded:** Candidate is compared against `story-6.4.6-au-baseline-current`, AU-005, and AU-006 expectations; policy/validation/copy regressions are explicitly checked.
10. **AC-10 No frontend touched:** Frontend remains unchanged unless a blocker is explicitly raised and approved.
11. **AC-11 Evidence docs complete:** Gate evidence, UAT guide/results, and closeout report record implementation, verification, migration instructions for Tony, and follow-up recommendations.
12. **AC-12 Version control and DB seed enforced:** All prompt/context changes are delivered exclusively through new immutable `PromptTemplateVersion` records and/or new `PromptTemplateLocaleBlock` seed records in a migration. Existing active versions and blocks remain untouched. The migration file is created but never executed by the agent; Tony reviews the migration, updates the alembic head, and validates the seed before any version is activated.

---

## 5) Definition of Done

- Story branch is pushed to PR #85.
- All prompt/context changes are version-controlled: new `PromptTemplateVersion` and/or `PromptTemplateLocaleBlock` seed records are created via migration; no direct edits to active prompt text or existing versions.
- Migration file is present with new versioned seed records. No Alembic command (upgrade/downgrade/revision/history/current) was run by the agent.
- Tony reviews the migration, manually updates the alembic head, and validates the new seed records before any version is activated or tested in production paths.
- Focused automated checks pass and are recorded.
- AU eval evidence proves the production path is materially better than baseline and aligns with AU-005/AU-006 lessons.
- Story closeout recommends whether to proceed to 6.5a / image-to-form / further prompt tuning.
