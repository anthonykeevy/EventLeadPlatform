# Retro Run Workflow Instructions

<critical>This workflow runs a full retrospective on a completed task.</critical>
<critical>Evidence-first: every lesson must cite a file/output.</critical>
<critical>NO CODE CHANGES: only update specs, lessons, memory.</critical>

<workflow>

<step n="1" goal="Load all task artifacts">
<action>Load these files (request paths if not provided):</action>
- Task Spec: docs/tasks/{story_id}/{task_id}.md
- Completion Note: docs/tasks/{story_id}/{task_id}.completion.md
- UAT Checklist: docs/tasks/{story_id}/{task_id}.uat.md
- UAT Results: docs/tasks/{story_id}/{task_id}.uat-results.md

<action>Optionally load if provided:</action>
- Session transcript
- Test output logs
- Story TASK-PLAN.md

<validation>
- All required files exist and are loaded
- UAT Results shows final status (HumanDone or FailedUAT)
</validation>

<output>All artifacts loaded</output>
</step>

<step n="2" goal="Analyze what went well">
<action>Identify positive patterns:</action>
- ACs that passed on first try
- Tests that caught issues early
- Scope boundaries that prevented creep
- Efficient verification methods

<action>Document with evidence:</action>

| What Went Well | Evidence |
|----------------|----------|
| [positive] | [file:line or output reference] |

<output>What Went Well section</output>
</step>

<step n="3" goal="Analyze what went wrong">
<action>Identify issues:</action>
- UAT failures and their root causes
- Rework required during dev
- Scope ambiguities discovered
- Missing tests or verification

<action>For each issue, determine root cause:</action>
- Task Spec issue? (ambiguous AC)
- Implementation issue? (dev error)
- Test gap? (missing verification)
- Process issue? (wrong sequence)

<action>Document with evidence:</action>

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| [issue] | [cause] | [file reference] |

<output>What Went Wrong section</output>
</step>

<step n="4" goal="Define prevention actions">
<action>For each issue, define prevention:</action>

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| Ambiguous AC | Add explicit test step to AC | ralf-sm |
| Missing test | Add unit test for [x] | ralf-dev |
| UAT gap | Add check for [y] to checklist | ralf-uat |

<action>Be specific and actionable</action>

<output>Prevention Actions section</output>
</step>

<step n="5" goal="Generate test improvements">
<action>Identify tests that would have caught issues earlier:</action>

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| unit | [what to test] | [file path] | `npm test [file]` |
| integration | [flow to test] | [file path] | `npm run test:int` |
| e2e | [user journey] | [file path] | `npm run test:e2e` |

### UAT Automation Candidates

Identify manual UAT steps that are:
- Repeated across multiple tasks
- Purely mechanical (no judgment needed)
- Time-consuming

<output>Test Improvements section</output>
</step>

<step n="6" goal="Generate process improvements">
<action>Recommend improvements for each agent:</action>

### For ralf-sm (Decomposition)
- How to decompose similar stories better
- AC templates to use
- Scope boundaries to clarify upfront

### For ralf-dev (Execution)
- Earlier verification points
- Test patterns to apply
- Common pitfalls to avoid

### For ralf-uat (Validation)
- Checklist improvements
- Evidence requirements to add
- Scope check triggers

<output>Process Improvements section</output>
</step>

<step n="7" goal="Document scope creep">
<action>List any scope creep discovered:</action>
- New features requested during dev/UAT
- Enhancements suggested
- Related bugs found outside task scope

<action>Recommend routing:</action>

| Item | Classification | Routing |
|------|----------------|---------|
| [item] | NEW_FEATURE | ralf-sm for new task |
| [item] | ENHANCEMENT | PM backlog |

<output>Scope Creep section</output>
</step>

<step n="8" goal="Summarize key learnings">
<action>Answer: "If we ran this again, what would we do differently?"</action>

Top 3 changes:
1. [key change]
2. [key change]
3. [key change]

<output>Key Learnings summary</output>
</step>

<step n="9" goal="Generate retro summary">
<action>Compile all sections into retro.md:</action>

# Task Retrospective: {task_id}

**Story:** {story_id}
**Task:** {task_name}
**Final Status:** {status}
**Date:** {date}

---

## What Went Well
[table from step 2]

## What Went Wrong
[table from step 3]

## Prevention Actions
[table from step 4]

## Test Improvements
[from step 5]

## Process Improvements
[from step 6]

## Scope Creep Discovered
[table from step 7]

## If We Ran This Again
[from step 8]

<action>Save to: docs/tasks/{story_id}/{task_id}.retro.md</action>

<output>Retro summary saved</output>
</step>

<step n="10" goal="Append to LESSONS-LEARNED.md">
<action>Append new entry:</action>

---

## Task: {task_id} ({date})

**Dev Lessons:**
- [lesson from what went wrong/well]

**Testing Lessons:**
- [lesson from test improvements]

**Process Lessons:**
- [lesson from process improvements]

**Links:**
- Completion: {task_id}.completion.md
- UAT: {task_id}.uat-results.md
- Retro: {task_id}.retro.md

<action>Save to: docs/tasks/{story_id}/LESSONS-LEARNED.md</action>

<output>Lessons appended</output>
</step>

<step n="11" goal="Update memory files">
<action>Update retro-patterns.yaml:</action>
- Add new root cause patterns
- Add new prevention patterns

<action>Update test-gap-patterns.yaml:</action>
- Add new test gaps discovered
- Add new test templates

<action>Update process-improvements.yaml:</action>
- Add decomposition improvements
- Add verification improvements

<output>Memory updated</output>
</step>

<step n="12" goal="Present summary">
<action>Display:</action>
- Retro file location
- Number of lessons captured
- Key prevention actions
- Test improvements recommended
- Next steps (route scope creep if any)

<output>Retro complete</output>
</step>

</workflow>
