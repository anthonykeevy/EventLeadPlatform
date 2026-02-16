# T03 / T04 Execution Prompts (Story 5.2)

**Use:** Copy/paste into a **new Cursor window** with the **task worktree** open (T03 or T04).  
**CRITICAL:** Open `C:\wt\elp\task-5.2-T03-form-builder-init-api` OR `C:\wt\elp\task-5.2-T04-dashboard-form-branding-defaults` before running.

---

## T03 Prompt

```markdown
@ralf-dev

*run-task

**CONTEXT CHECK (mandatory):**
1. Verify you are in the **Story 5.2 worktree** on the **story branch** or the **T03 task worktree** on `task/5.2/T03-form-builder-init-api`. Path should be `C:\wt\elp\task-5.2-T03-form-builder-init-api` or `C:\wt\elp\story-epic5-5.2-company-form-defaults`. If not, STOP and ask the user to open the correct folder.
2. Story branch: `story/epic5-5.2-company-form-defaults`. Task branch: `task/5.2/T03-form-builder-init-api`.

**FULL CYCLE (do not stop until complete):** Implement → Automated verification → UAT attempt → Retro → Commit all → Push → Merge PR.

Scope + ACs are pre-approved; proceed end-to-end without waiting for interactive confirmations.

Task Spec: docs/tasks/5.2/T03-form-builder-init-api.md

**Mandatory steps (in order):**
1. Implement per task spec.
2. Automated verification: run lint/build/tests for touched areas; record evidence in completion note.
3. UAT: Open `T03-form-builder-init-api.uat.md`. For each step:
   - If automatable: execute and record result.
   - If manual-only: record "Human verification: [step] – not executed by agent."
   - Create/update `T03-form-builder-init-api.uat-results.md` with PASS/FAIL and evidence.
4. Retro: Update `T03-form-builder-init-api.retro.md` and LESSONS-LEARNED.md.
5. Commit: implementation first (feat(T03): ...), then closeout (docs: completion, uat-results, retro, spec status, TASK-PLAN.md, STATUS.md). Push.
6. Merge: Run `gh pr merge --squash` in the task worktree. If merge fails, output the exact command for the human to run.

**Rules:** PR targets Story branch. Before closeout: working tree clean. Use task doc naming `T{id}-{slug}.{type}.md`.
```

---

## T04 Prompt

```markdown
@ralf-dev

*run-task

**CONTEXT CHECK (mandatory):**
1. Verify you are in the **Story 5.2 worktree** on the **story branch** or the **T04 task worktree** on `task/5.2/T04-dashboard-form-branding-defaults`. Path should be `C:\wt\elp\task-5.2-T04-dashboard-form-branding-defaults` or `C:\wt\elp\story-epic5-5.2-company-form-defaults`. If not, STOP and ask the user to open the correct folder.
2. Story branch: `story/epic5-5.2-company-form-defaults`. Task branch: `task/5.2/T04-dashboard-form-branding-defaults`.

**FULL CYCLE (do not stop until complete):** Implement → Automated verification → UAT attempt → Retro → Commit all → Push → Merge PR.

Scope + ACs are pre-approved; proceed end-to-end without waiting for interactive confirmations.

Task Spec: docs/tasks/5.2/T04-dashboard-form-branding-defaults.md

**Mandatory steps (in order):**
1. Implement per task spec.
2. Automated verification: run lint/build/tests for touched areas; record evidence in completion note.
3. UAT: Open `T04-dashboard-form-branding-defaults.uat.md`. For each step:
   - If automatable: execute and record result.
   - If manual-only: record "Human verification: [step] – not executed by agent."
   - Create/update `T04-dashboard-form-branding-defaults.uat-results.md` with PASS/FAIL and evidence.
4. Retro: Update `T04-dashboard-form-branding-defaults.retro.md` and LESSONS-LEARNED.md.
5. Commit: implementation first (feat(T04): ...), then closeout (docs: completion, uat-results, retro, spec status, TASK-PLAN.md, STATUS.md). Push.
6. Merge: Run `gh pr merge --squash` in the task worktree. If merge fails, output the exact command for the human to run.

**Rules:** PR targets Story branch. Before closeout: working tree clean. Use task doc naming `T{id}-{slug}.{type}.md`.
```

---

## Summary

| Item | T03 | T04 |
|------|-----|-----|
| Worktree | `C:\wt\elp\task-5.2-T03-form-builder-init-api` | `C:\wt\elp\task-5.2-T04-dashboard-form-branding-defaults` |
| PR | #35 | #36 |
| Spec | T03-form-builder-init-api.md | T04-dashboard-form-branding-defaults.md |
| UAT | T03-form-builder-init-api.uat.md | T04-dashboard-form-branding-defaults.uat.md |

**Parallel:** Open one worktree per Cursor window; run T03 and T04 in separate sessions.
