# UAT Handoff Workflow Instructions

<critical>This workflow completes UAT and routes to the appropriate next agent.</critical>

<workflow>

<step n="1" goal="Gather UAT summary">
<action>Load UAT results file</action>
<action>Extract:</action>
- Overall result (PASS/FAIL)
- Number of steps tested
- Number of defects
- Number of out-of-scope requests
- Automation opportunities identified

<output>Summary data gathered</output>
</step>

<step n="2" goal="Confirm status update">
<action>Verify status was updated:</action>
- TASK-PLAN.md or STATUS.md has correct status
- UATCompletedAt is set
- Link to results file is included

<output>Status confirmed</output>
</step>

<step n="3" goal="Determine next agent">
<action>Based on result:</action>

**If PASS (HumanDone):**
- Task is complete
- Ready for retrospective
- Route to: `@ralf-retro`

**If FAIL (FailedUAT):**
- Defects must be fixed
- Route to: `@ralf-dev` with defect list
- After fix, return to `@ralf-uat`

<output>Next agent determined</output>
</step>

<step n="4" goal="Generate handoff summary">
<action>Display:</action>

## UAT Handoff: {task_id}

**Story:** {story_id}
**Result:** [PASS | FAIL]
**Date:** {date}

---

### Summary

| Metric | Count |
|--------|-------|
| Steps Tested | {n} |
| Passed | {n} |
| Failed | {n} |
| Defects | {n} |
| Out-of-Scope | {n} |

---

### Files Updated

- `{task_id}.uat.md` - UAT Checklist
- `{task_id}.uat-results.md` - UAT Results
- `TASK-PLAN.md` - Status updated

---

### Automation Opportunities

[List tests that should be added]

---

### Next Agent

**If PASS:**
```
@ralf-retro
```
Run retrospective for this task to capture learnings.

**If FAIL:**
```
@ralf-dev
```
Fix defects:
- D1: [description]
- D2: [description]

After fixes, return to `@ralf-uat` to re-test.

<output>Handoff summary displayed</output>
</step>

<step n="5" goal="Update memory">
<action>If automation opportunities identified:</action>
- Append to {project-root}/bmad/ralf-taskflow/memory/automation-opportunities.yaml

<action>If new failure patterns discovered:</action>
- Append to {project-root}/bmad/ralf-taskflow/memory/uat-failure-patterns.yaml

<output>Memory updated</output>
</step>

</workflow>

## Routing Summary

| UAT Result | Task Status | Next Agent | Action |
|------------|-------------|------------|--------|
| PASS | HumanDone | ralf-retro | Retrospective |
| FAIL | FailedUAT | ralf-dev | Fix defects |
