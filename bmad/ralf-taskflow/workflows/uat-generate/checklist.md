# UAT Generate Validation Checklist

## Input Validation

- [ ] Task Spec file exists and is loaded
- [ ] Completion Note file exists and is loaded
- [ ] Story ID and Task ID extracted correctly

## Checklist Quality

- [ ] Every AC has at least one verification step
- [ ] Every step has specific action (not vague)
- [ ] Every step has specific expected result
- [ ] No ambiguous terms ("works correctly", "looks good")
- [ ] Steps are deterministic (same action = same result)

## Coverage

- [ ] All Acceptance Criteria are covered
- [ ] At least 2-3 negative tests included
- [ ] Regression checks included
- [ ] Evidence requirements specified

## Structure

- [ ] Preconditions section complete
- [ ] AC verification tables formatted correctly
- [ ] Negative tests section included
- [ ] Evidence requirements section included
- [ ] Summary section with counts

## Output

- [ ] Checklist saved to correct path
- [ ] File is valid markdown
- [ ] Ready for human execution

## Issues Found

### Missing Coverage
<!-- ACs not covered -->

### Ambiguous Steps
<!-- Steps that need clarification -->
