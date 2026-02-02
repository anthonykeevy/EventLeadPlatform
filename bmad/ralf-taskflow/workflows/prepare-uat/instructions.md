# Prepare UAT Workflow Instructions

<critical>This workflow creates a human-friendly UAT checklist.</critical>
<critical>Each step must be binary (pass/fail) and deterministic.</critical>

<workflow>

<step n="1" goal="Load Task Spec and changes">
<action>Load the Task Spec file</action>
<action>Review the changes made during implementation</action>
<action>Extract all Acceptance Criteria</action>

<output>Context loaded</output>
</step>

<step n="2" goal="Map ACs to verification steps">
<action>For each Acceptance Criterion:</action>
- Create 1-3 specific, observable test steps
- Each step must describe an action and expected result
- Include exact values, paths, or UI elements

<action>Ensure steps are:
- Self-contained (no prior knowledge needed)
- Deterministic (same action = same result)
- Binary (clearly pass or fail)
</action>

<output>Verification steps mapped</output>
</step>

<step n="3" goal="Add environment and regression checks">
<action>Add environment setup section:</action>
- Required application state
- Data prerequisites
- Login/authentication requirements

<action>Add regression check section:</action>
- Verify related functionality still works
- Check for obvious side effects

<output>Full checklist prepared</output>
</step>

<step n="4" goal="Output UAT checklist">
<action>Generate checklist in this format:</action>

```markdown
# UAT Checklist: {task_id}

**Story:** {story_id}
**Task:** {task_name}
**Date:** {date}

---

## Environment Setup

- [ ] Application is running at [URL/state]
- [ ] User is logged in as [role]
- [ ] Test data is available: [description]

---

## Acceptance Criteria Verification

### AC1: [criterion text]

- [ ] Step 1: [action]
  - Expected: [result]
  - Actual: ___________

- [ ] Step 2: [action]
  - Expected: [result]
  - Actual: ___________

### AC2: [criterion text]

- [ ] Step 1: [action]
  - Expected: [result]
  - Actual: ___________

---

## Regression Checks

- [ ] [Related feature] still works as expected
- [ ] No console errors appear
- [ ] No visual glitches

---

## Test Result

- [ ] ALL criteria PASS
- [ ] Some criteria FAIL (document below)

### Failures (if any)

| AC | Step | Expected | Actual |
|----|------|----------|--------|
|    |      |          |        |

---

## Tester Sign-off

**Tester:** ___________
**Date:** ___________
**Result:** [ ] PASS [ ] FAIL
```

<output>UAT checklist saved</output>
</step>

</workflow>

## Avoid

- Vague verifications ("works correctly", "looks good")
- Steps requiring developer judgment
- Multiple outcomes in one step
- Dependencies on specific timing
