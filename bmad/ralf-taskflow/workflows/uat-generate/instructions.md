# UAT Generate Workflow Instructions

<critical>This workflow generates a deterministic UAT checklist from Task Spec + Completion Note.</critical>
<critical>The checklist must be executable by a human tester with no ambiguity.</critical>

<workflow>

<step n="1" goal="Load inputs">
<action>Load the Task Spec from provided path</action>
<action>Load the Completion Note from provided path</action>
<action>Extract story_id and task_id from paths</action>
<action>Load UAT patterns from memory if available</action>

<validation>
- Task Spec exists and contains Acceptance Criteria
- Completion Note exists and contains test evidence
</validation>

<output>Loaded context</output>
</step>

<step n="2" goal="Extract acceptance criteria">
<action>From Task Spec, extract:</action>
- All Acceptance Criteria (AC1, AC2, etc.)
- Expected behaviors for each AC
- Error cases / edge cases specified
- Required Tests section

<action>From Completion Note, extract:</action>
- Files changed
- Test evidence already provided
- Manual UAT steps suggested by ralf-dev
- Any known limitations

<output>AC list with verification requirements</output>
</step>

<step n="3" goal="Generate preconditions">
<action>Determine environment setup required:</action>
- Application state
- User role/login requirements
- Test data needed
- Dependencies on other tasks

<action>Format as checklist:</action>

## Preconditions

- [ ] Application is running at [specific URL]
- [ ] User is logged in as [specific role]
- [ ] Test data: [specific data description]
- [ ] Dependencies: [list completed prerequisite tasks]

<output>Preconditions checklist</output>
</step>

<step n="4" goal="Generate AC verification steps">
<action>For each Acceptance Criterion:</action>

1. Create specific, observable test steps
2. Each step has:
   - Action (what to do)
   - Expected result (what should happen)
   - Evidence column (for screenshots/logs)

3. Format as table:

### AC1: [criterion text]

| Step | Action | Expected Result | Pass/Fail | Evidence |
|------|--------|-----------------|-----------|----------|
| 1.1 | Navigate to [page] | [page] loads | | |
| 1.2 | Click [button] | [result] appears | | |
| 1.3 | Enter [value] | [validation] shown | | |

<output>AC verification tables</output>
</step>

<step n="5" goal="Generate negative tests">
<action>Create edge case and error handling tests:</action>

## Negative Tests / Edge Cases

| Step | Action | Expected Result | Pass/Fail | Evidence |
|------|--------|-----------------|-----------|----------|
| N1 | Enter empty value | Error message shown | | |
| N2 | Enter invalid format | Validation error | | |
| N3 | Submit without required field | Submit blocked | | |

<action>Include at least 2-3 negative tests per task</action>

<output>Negative test table</output>
</step>

<step n="6" goal="Add evidence requirements">
<action>Specify what evidence is needed for failures:</action>

## Evidence Requirements

For any FAILED step, provide:
1. **Screenshot** of the failure state
2. **Console errors** (if any)
3. **Network errors** (if API related)
4. **Specific values** observed vs expected
5. **Steps to reproduce** if not obvious

<output>Evidence requirements section</output>
</step>

<step n="7" goal="Add regression checks">
<action>Add general regression checks:</action>

## Regression Checks

- [ ] Related features still work as before
- [ ] No console errors during testing
- [ ] No visual glitches or layout issues
- [ ] Performance is acceptable

<output>Regression checklist</output>
</step>

<step n="8" goal="Save UAT checklist">
<action>Compile all sections into final checklist</action>
<action>Add header with metadata:</action>

# UAT Checklist: {task_id}

**Task:** {task_name}
**Story:** {story_id}
**Generated:** {date}
**Source:** Task Spec + Completion Note

---

[All sections from above]

---

## Summary

- **Total AC Steps:** {count}
- **Negative Tests:** {count}
- **Regression Checks:** {count}

<action>Save to: {output_folder}/{story_id}/{task_id}.uat.md</action>

<output>UAT checklist saved</output>
</step>

<step n="9" goal="Present to tester">
<action>Display summary:</action>
- Checklist location
- Number of steps
- Estimated time to complete

<action>Ask if tester is ready to begin</action>

<output>Ready for human UAT execution</output>
</step>

</workflow>

## Quality Criteria

- Every AC has at least one verification step
- Every step has specific action and expected result
- No vague terms like "works correctly"
- Evidence requirements are clear
- Negative tests cover common error cases
