# Run Task Workflow Instructions

<critical>This workflow executes ONE task from a Task Spec with full verification.</critical>
<critical>One session = one task. If task is too large, propose split and STOP.</critical>

<workflow>

<step n="1" goal="Load and validate Task Spec">
<action>Load the Task Spec file from the provided path</action>
<action>Extract and display:
  - Task ID and name
  - Story ID
  - Status (must be Ready or In Progress)
  - Dependencies (verify they are complete)
</action>

<validation>
- Task Spec exists and is readable
- Task status allows execution
- All dependencies are marked complete
</validation>

<output>Loaded Task Spec with metadata</output>
</step>

<step n="2" goal="Restate scope boundaries">
<action>Extract and PROMINENTLY display:</action>

## Scope Confirmation

### Scope (In) - I WILL:
[List all items from Scope In section]

### Scope (Out) - I WILL NOT:
[List all items from Scope Out section]

### Forbidden Zones - I MUST NOT TOUCH:
[List all forbidden files/modules]

<action>Ask user to confirm understanding before proceeding</action>

<output>Confirmed scope boundaries</output>
</step>

<step n="3" goal="Map acceptance criteria to verification">
<action>For each Acceptance Criterion in the Task Spec:</action>
- State the criterion
- Identify the verification method from the spec
- If verification method is missing or unclear, propose one

<action>Create verification plan:</action>

| AC ID | Criterion | Verification Method | Status |
|-------|-----------|---------------------|--------|
| AC1   | ...       | ...                 | Pending |
| AC2   | ...       | ...                 | Pending |

<output>Verification plan ready</output>
</step>

<step n="4" goal="Plan implementation approach">
<action>Based on the Task Spec requirements:</action>
- Identify files to create/modify (must be within allowed scope)
- Identify tests to write/run
- Propose implementation order (smallest viable steps)

<action>Load dev patterns from memory if available:</action>
- {project-root}/bmad/ralf-taskflow/memory/dev-patterns.yaml
- {project-root}/bmad/ralf-taskflow/memory/common-failures.yaml

<action>Apply relevant patterns to implementation plan</action>

<validation>
- All planned file changes are within allowed scope
- No Forbidden Zones are touched
- Implementation is minimal for the requirements
</validation>

<output>Implementation plan ready</output>
</step>

<step n="5" goal="Implement changes incrementally">
<action>For each planned change:</action>
1. Make the change
2. Verify it works (run relevant tests/lint)
3. Record the file and change type (created/modified)

<action>Track all files touched:</action>

| File | Change Type | Reason |
|------|-------------|--------|
| path/to/file.ts | Modified | Implement AC1 |
| path/to/test.ts | Created | Test for AC1 |

<critical>If you need to touch a file NOT in the allowed list:</critical>
1. Document why it's necessary
2. Verify it's not in Forbidden Zones
3. Add to tracking list with justification

<critical>If implementation reveals task is too large:</critical>
1. STOP implementation
2. Document what was completed
3. Propose split into smaller tasks
4. Route to ralf-sm for task decomposition

<output>Implementation complete with file tracking</output>
</step>

<step n="6" goal="Run required tests and verification">
<action>Execute all tests listed in Task Spec "Required Tests" section</action>
<action>Run any additional verification commands</action>
<action>Capture exact commands and outputs:</action>

```bash
# Command run
$ npm test -- --grep "feature"

# Output
PASS  src/feature.test.ts
  ✓ should handle X (15ms)
  ✓ should reject Y (8ms)
```

<action>If any tests fail:</action>
1. Diagnose the failure
2. Fix and rerun
3. Repeat until green or until blocker identified

<action>Update verification plan with results:</action>

| AC ID | Criterion | Verification Method | Status | Evidence |
|-------|-----------|---------------------|--------|----------|
| AC1   | ...       | ...                 | PASS   | test output |
| AC2   | ...       | ...                 | PASS   | manual check |

<output>All tests passing with evidence</output>
</step>

<step n="7" goal="Generate completion note">
<action>Create completion note at: {output_folder}/{story_id}/{task_id}.completion.md</action>

Template:

```markdown
# Task Completion: {task_id}

**Story:** {story_id}
**Task:** {task_name}
**Completed:** {date}
**Status:** Complete

---

## Summary of Changes

[1-3 sentence summary of what was implemented]

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| [path] | [created/modified/deleted] | [why] |

## Acceptance Criteria Verification

### AC1: [criterion]
- **Status:** PASS
- **Evidence:** [how verified]

### AC2: [criterion]
- **Status:** PASS
- **Evidence:** [how verified]

## Test Evidence

### Automated Tests
```bash
[exact commands and outputs]
```

### Build Verification
```bash
[build commands if applicable]
```

## Manual UAT Steps

For human verification:

1. [ ] [step] -> Verify: [expected]
2. [ ] [step] -> Verify: [expected]

## Known Limitations / Out-of-Scope Items

[Any items discovered during implementation that belong in future tasks]

- [ ] [item] -> Route to: [ralf-sm / PM backlog]

## Recommended Next Step

[Ready for UAT | Blocked - reason | Split recommended]
```

<output>Completion note saved</output>
</step>

<step n="8" goal="Update lessons learned">
<action>If any insights emerged during implementation:</action>
- Add to {output_folder}/{story_id}/LESSONS-LEARNED.md

<action>If pattern is reusable across tasks:</action>
- Update {project-root}/bmad/ralf-taskflow/memory/dev-patterns.yaml

<action>If common failure was encountered:</action>
- Update {project-root}/bmad/ralf-taskflow/memory/common-failures.yaml

<output>Lessons recorded</output>
</step>

<step n="9" goal="Auto-generate UAT checklist">
<critical>AUTOMATIC: Generate UAT checklist immediately after completion note.</critical>

<action>Create UAT checklist at: {output_folder}/{story_id}/{task_id}.uat.md</action>

Template:

```markdown
# UAT Checklist: {task_id}

**Story:** {story_id}
**Task:** {task_name}
**Generated:** {date}

---

## Pre-conditions

- [ ] Backend server is running
- [ ] Frontend is running
- [ ] User is logged in (if applicable)
- [ ] [Any specific state required]

## Test Steps

### AC1: [First acceptance criterion]

- [ ] Step 1: [action] → Verify: [expected result]
- [ ] Step 2: [action] → Verify: [expected result]

### AC2: [Second acceptance criterion]

- [ ] Step 1: [action] → Verify: [expected result]

## Regression Check

- [ ] Verify existing functionality still works: [specific check]
- [ ] No console errors in browser
- [ ] No new backend errors in logs

## Post-conditions

- [ ] [Expected end state]

## Edge Cases (if applicable)

- [ ] [Edge case to verify]

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results
```

<output>UAT checklist generated</output>
</step>

<step n="10" goal="Final handoff">
<action>Display summary:</action>

## Task Complete: {task_id}

| Metric | Value |
|--------|-------|
| Files Changed | [count] |
| All ACs Verified | [yes/no] |
| Completion Note | [path] |
| UAT Checklist | [path] |

### Next Steps

**For Human Tester:**
1. Review the UAT checklist at: `{output_folder}/{story_id}/{task_id}.uat.md`
2. Execute the test steps manually
3. Record results with: `@ralf-uat *record-uat`

**After UAT:**
- Run retro: `@ralf-retro *run-retro`
- Then return to main chat for next task

<action>Recommend status:</action>
- "✅ Task is ready for human UAT"
- OR "⚠️ Blocked - needs attention from ralf-sm"
- OR "🔀 Split recommended - completion note has details"

<output>Task handoff complete</output>
</step>

</workflow>

## Safe Verification Methods

### TypeScript Compilation Check

<critical>AVOID running `npx tsc --noEmit ... | Select-Object` - this can crash Cursor chat!</critical>

**Safe alternatives (in order of preference):**

1. **Use ReadLints tool** (BEST - built into Cursor):
   ```
   Use ReadLints tool on the files you changed
   ```

2. **Redirect to file** (SAFE - no piping):
   ```bash
   npx tsc --noEmit --skipLibCheck > tsc-check.txt 2>&1
   # Then read the file
   ```

3. **Use DevTools MCP** (for runtime errors):
   ```
   Use user-chrome-devtools MCP to:
   - navigate_page to the app
   - list_console_messages to check for errors
   ```

4. **Run build directly** (shows errors in output):
   ```bash
   npm run build
   ```

### Using DevTools MCP for Verification

When the task involves UI changes, use the DevTools MCP for real verification:

```
1. navigate_page to the affected page
2. take_snapshot to verify UI elements exist
3. list_console_messages to check for errors
4. evaluate_script to check React state/props
5. list_network_requests to verify API calls
```

---

## Error Handling

### If Task Spec is invalid:
- Report specific issue
- Do not proceed
- Route to ralf-sm for Task Spec refinement

### If scope violation detected:
- STOP immediately
- Label as OUT OF SCOPE
- Do not implement
- Route to ralf-sm

### If tests fail repeatedly:
- Document the failure
- Check if it's a Task Spec issue (AC too vague)
- Either fix or flag as blocker

### If task is too large:
- STOP at a clean point
- Document completed portion
- Propose split strategy
- Route to ralf-sm for new task creation
