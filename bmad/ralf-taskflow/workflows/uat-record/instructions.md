# UAT Record Workflow Instructions

<critical>This workflow records human UAT results and updates task status.</critical>
<critical>Distinguish between DEFECTS (AC violations) and OUT OF SCOPE (new requests).</critical>
<critical>🚨 AUTO-COMPLETE: Do NOT ask "Would you like me to..." - JUST CREATE THE FILES.</critical>
<critical>🚨 MANDATORY: Steps 6-9 MUST execute automatically without user confirmation.</critical>
<critical>🚨 NEVER end a UAT pass without: (1) creating uat-results.md, (2) updating TASK-PLAN.md, (3) providing retro handoff.</critical>

<workflow>

<step n="1" goal="Collect tester information">
<action>Ask for:</action>
- Tester name
- Date of testing
- UAT checklist used (path)

<action>Load the UAT checklist to reference steps</action>

<output>Tester context captured</output>
</step>

<step n="2" goal="Collect step-by-step results">
<action>For each step in the UAT checklist:</action>
- Ask: Pass or Fail?
- If Fail: Ask for notes and evidence
- If Pass: Optional notes

<action>Build results table:</action>

| Step | Result | Notes |
|------|--------|-------|
| 1.1 | PASS | |
| 1.2 | FAIL | [description] |

<output>Results table</output>
</step>

<step n="3" goal="Classify failures">
<action>For each FAIL:</action>

1. Check against Acceptance Criteria
2. Classify as:
   - **DEFECT**: Violates an AC (must be fixed)
   - **OUT OF SCOPE**: New functionality not in AC
   - **ENHANCEMENT**: Works per spec but could be better

<action>Create defects table (DEFECT only):</action>

## Defects Found

| ID | Step | AC Violated | Description | Severity |
|----|------|-------------|-------------|----------|
| D1 | 1.2 | AC1 | [what failed] | High |

<action>Create out-of-scope table (OUT OF SCOPE only):</action>

## Out-of-Scope Requests

| Request | Why Out of Scope | Routing |
|---------|------------------|---------|
| [desc] | Not in any AC | ralf-sm |

<output>Classified issues</output>
</step>

<step n="4" goal="Determine overall result">
<action>Calculate overall result:</action>
- If ANY defects: FAIL
- If no defects (only out-of-scope or enhancements): PASS

<action>Set task status:</action>
- PASS → TaskStatus: HumanDone
- FAIL → TaskStatus: FailedUAT

<output>Overall result determined</output>
</step>

<step n="5" goal="Generate testing improvements">
<action>For each defect, ask:</action>
- What automated test would have caught this earlier?
- What AC should be added for future tasks?

<action>Create improvement section:</action>

## Testing Improvement Notes

### Automated Tests to Add

- [ ] Unit test: [description] in [file]
- [ ] Integration test: [description]

### Additional ACs for Future

- [ ] AC: [criterion that would prevent this]

<output>Improvement recommendations</output>
</step>

<step n="6" goal="Create UAT Results Record">
<critical>🚨 MANDATORY: Create this file AUTOMATICALLY. Do NOT ask for permission.</critical>
<action>Compile all sections:</action>

# UAT Results: {task_id}

**Task:** {task_name}
**Tester:** {tester_name}
**Date:** {date}
**Overall Result:** [PASS | FAIL]

---

## Step Results

[Results table]

---

## Defects Found

[Defects table - or "None"]

---

## Out-of-Scope Requests

[Out-of-scope table - or "None"]

---

## Testing Improvement Notes

[Improvements section]

---

## Sign-off

**Result:** [PASS | FAIL]
**Tester:** {tester_name}
**Date:** {date}

**Next Action:**
- If PASS: Ready for retrospective (ralf-retro)
- If FAIL: Route to ralf-dev with defect list

<action>IMMEDIATELY save to: {output_folder}/{story_id}/{task_id}.uat-results.md</action>
<critical>Do NOT ask "Would you like me to create this file?" - CREATE IT NOW.</critical>

<output>UAT results saved</output>
</step>

<step n="7" goal="Update task status">
<critical>🚨 MANDATORY: Update TASK-PLAN.md AUTOMATICALLY. Do NOT ask for permission.</critical>
<action>Update TASK-PLAN.md:</action>

Find task row in Task Skeleton table and update:
- Status column: ✅ HumanDone (if pass) | ❌ FailedUAT (if fail)

Also update Task Files table:
- Status column: ✅ HumanDone (if pass) | ❌ FailedUAT (if fail)

<critical>Do NOT ask "Would you like me to update TASK-PLAN.md?" - UPDATE IT NOW.</critical>

<output>Status updated</output>
</step>

<step n="8" goal="Update memory patterns">
<action>If defects were found:</action>
- Add to {project-root}/bmad/ralf-taskflow/memory/uat-failure-patterns.yaml

<action>If automation opportunities identified:</action>
- Add to {project-root}/bmad/ralf-taskflow/memory/automation-opportunities.yaml

<output>Memory updated</output>
</step>

<step n="9" goal="Present summary and handoff">
<critical>🚨 MANDATORY: Provide clear next-step instructions. Do NOT ask what to do next.</critical>

<action>Display summary:</action>

---
## ✅ UAT Recording Complete

**Result:** [PASS | FAIL]
**Steps Tested:** {count}
**Defects:** {count}
**Out-of-Scope:** {count}

**Files Updated:**
- ✅ Created: `{output_folder}/{story_id}/{task_id}.uat-results.md`
- ✅ Updated: `{output_folder}/{story_id}/TASK-PLAN.md`

---

<action>If PASS, display:</action>

### Next Step: Run Retrospective

In this same chat, run:
```
@ralf-retro *run-retro
Task: {task_id}
Story: {story_id}
```

After retro, return to main chat and run `@ralf-sm *next-task`.

<action>If FAIL, display:</action>

### Next Step: Fix Defects

Return to dev and fix defects:
```
@ralf-dev *run-task
Task Spec: {task_spec_path}
Defects to fix:
- D1: [description]
```

After fixes, run UAT again with `@ralf-uat *record-uat`.

---

<output>UAT recording complete with clear handoff</output>
</step>

</workflow>
