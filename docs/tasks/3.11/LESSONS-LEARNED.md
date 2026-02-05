# Lessons Learned: Story 3.11 - Dynamic Submission (Outbox)

**Story:** 3.11  
**Epic:** Epic 3 - Form Builder & Logic Engine  
**Created:** 2026-02-03  

---

## 📝 Lessons Log

_Append lessons as tasks are completed. Format:_

```markdown
### {date} - {lesson_type} Lesson

**Task:** {task_id}
**Context:** {brief context}
**Issue:** {what went wrong or could be improved}
**Lesson:** {actionable insight}
**Prevention:** {how to avoid in future}
```

---

## Lessons

## Task: T02 (2026-02-03)

**Dev Lessons:**
- Document rollback steps in migration completion notes for safe verification.

**Testing Lessons:**
- Record AC-level UAT evidence immediately after migration execution.

**Process Lessons:**
- Update TASK-PLAN status as part of UAT recording to keep story tracking current.

**Links:**
- Completion: `T02-db-migration-formsubmission.completion.md`
- UAT: `T02-db-migration-formsubmission.uat-results.md`
- Retro: `T02-db-migration-formsubmission.retro.md`

---

## Task: T05 (2026-02-04)

**Dev Lessons:**
- Ensure the backend worktree includes the public submissions endpoint before testing online submit flows.

**Testing Lessons:**
- Add a public submissions endpoint smoke test and a frontend API base URL unit test to catch 404s early.

**Process Lessons:**
- Add a preflight UAT step to verify `POST /api/public/forms/{token}/submissions` is registered before AC2–AC5.

**Links:**
- Completion: `T05-renderer-submit-integration.completion.md`
- UAT: `T05-renderer-submit-integration.uat-results.md`
- Retro: `T05-renderer-submit-integration.retro.md`

---

## Task: T06 (2026-02-04)

**Dev Lessons:**
- Preview shell links must preserve kiosk query params; missing passthrough prevents AC verification.

**Testing Lessons:**
- Add a unit test that asserts preview URL query params reach the embed/public link.

**Process Lessons:**
- Verify `npm install` completes before lint/build checks to avoid false failures.

**Links:**
- Completion: `T06-kiosk-mode-auto-reset.completion.md`
- UAT: `T06-kiosk-mode-auto-reset.uat-results.md`
- Retro: `T06-kiosk-mode-auto-reset.retro.md`

---

## Task: T07 (2026-02-05)

**Dev Lessons:**
- Privacy-safe value diagnostics still provide actionable validation insights without raw values.

**Testing Lessons:**
- Add a resolved-flow check that verifies a `validation_failed_submit` event occurs before a successful submission in the same session.

**Process Lessons:**
- Capture telemetry correlation evidence (SessionID ↔ ContextJSON) as part of UAT notes.

**Links:**
- Completion: `T07-validation-telemetry-events.completion.md`
- UAT: `T07-validation-telemetry-events.uat-results.md`
- Retro: `T07-validation-telemetry-events.retro.md`

---

