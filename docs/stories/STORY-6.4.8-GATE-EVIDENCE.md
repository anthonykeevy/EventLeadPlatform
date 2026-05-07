# Story 6.4.8 Gate Evidence

**Story:** 6.4.8 - Promote AU-005 Into Production Prompt Context  
**Branch:** `story/epic6-6.4.8-au-production-prompt-context`  
**PR:** [#85](https://github.com/anthonykeevy/EventLeadPlatform/pull/85)

This file must be filled by Dev as implementation and verification proceeds.

---

## Preflight

Status: Pending Dev execution.

Expected command:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.8-au-production-prompt-context" `
  -ExpectedBranch "story/epic6-6.4.8-au-production-prompt-context" `
  -ReportFile "docs/stories/STORY-6.4.8-PREFLIGHT.md"
```

---

## Implementation Evidence

Status: Pending.

Record:

- Production prompt/context files changed.
- Migration file added, if any.
- Whether `backend/modules/form_ai/service.py` changed and why.
- Confirmation that no Alembic command was run by the agent.

---

## Focused Automated Tests

Status: Pending.

Expected minimum:

```powershell
python -m pytest `
  backend/tests/test_form_ai_locale_assembly.py `
  backend/tests/test_form_ai_locale_resolution.py `
  backend/tests/test_story_6441_migrations_static.py `
  backend/tests/test_form_ai_eval_harness.py `
  backend/tests/test_form_ai_eval_experiment.py `
  backend/tests/test_judge_pack.py `
  backend/tests/test_judge_ingest.py `
  backend/tests/test_eval_diff.py `
  --tb=short
```

Record exact summary:

```text
Pending
```

---

## AU Production Candidate Eval

Status: Pending.

Record:

- Run ID.
- Command.
- Output folder.
- Prompt-context lint findings.
- Generated-output deterministic findings.
- p11-specific findings.

---

## Judge / Diff Evidence

Status: Pending.

Record:

- Judge package path.
- Judge outputs ingested.
- Score comparison to baseline, AU-005, and AU-006.
- Policy, validation, and copy-quality regression check.

---

## Migration Handoff

Status: Pending / N/A.

If migration exists:

- File:
- Purpose:
- Tony-run command:
- Downgrade behaviour:
- Verification query or check:

---

## Gate Decision

Status: Pending.

Decision:

- Promote / revise / stop:
- Rationale:
- Follow-up:
