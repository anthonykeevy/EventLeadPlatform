# Run Task Validation Checklist

## Pre-Execution Validation

- [ ] Task Spec file exists and is readable
- [ ] Task status is Ready or In Progress
- [ ] All dependencies are marked complete
- [ ] Scope boundaries have been restated and confirmed

## Scope Compliance

- [ ] All changes are within Scope (In)
- [ ] No Scope (Out) items were implemented
- [ ] No Forbidden Zones were touched
- [ ] Any new files are justified and recorded

## Implementation Quality

- [ ] Changes are minimal for the requirements
- [ ] Implementation follows codebase patterns
- [ ] No unnecessary refactoring or cleanup
- [ ] Code is consistent with existing style

## Verification Completeness

- [ ] All acceptance criteria have verification methods
- [ ] All required tests were run
- [ ] All tests pass (or blockers documented)
- [ ] Test evidence is captured with exact commands/outputs

## Documentation

- [ ] Completion note created at correct path
- [ ] Summary of changes is accurate
- [ ] Files changed list is complete
- [ ] AC verification is criterion-by-criterion
- [ ] Test evidence is included
- [ ] Manual UAT steps are clear and deterministic
- [ ] Out-of-scope items are documented (if any)

## UAT Checklist Generation

- [ ] UAT checklist created at correct path
- [ ] All acceptance criteria have test steps
- [ ] Pre-conditions are clearly defined
- [ ] Test steps are deterministic (binary pass/fail)
- [ ] Regression checks included
- [ ] Edge cases identified (if applicable)

## Handoff Readiness

- [ ] Recommended next step is clear
- [ ] Completion note path provided
- [ ] UAT checklist path provided
- [ ] LESSONS-LEARNED.md updated (if insights emerged)
- [ ] Memory files updated (if patterns discovered)

## Issues Found

### Critical Issues
<!-- Must be fixed before task can be marked complete -->

### Blockers
<!-- Issues that prevent completion -->

### Out-of-Scope Items
<!-- Discovered items to route to ralf-sm or PM -->
