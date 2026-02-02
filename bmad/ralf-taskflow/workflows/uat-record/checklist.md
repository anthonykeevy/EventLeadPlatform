# UAT Record Validation Checklist

## 🚨 Auto-Complete Verification (CRITICAL)

- [ ] Did NOT ask "Would you like me to..." for any file operation
- [ ] Created uat-results.md AUTOMATICALLY without asking
- [ ] Updated TASK-PLAN.md AUTOMATICALLY without asking
- [ ] Provided clear handoff instructions without asking

## Input Validation

- [ ] Tester name provided (or used {user_name} from config)
- [ ] Date captured (or used today's date)
- [ ] UAT checklist loaded

## Results Collection

- [ ] Every step has a result (Pass/Fail)
- [ ] Failed steps have notes
- [ ] Evidence provided for failures

## Classification

- [ ] All failures classified (Defect/Out-of-Scope/Enhancement)
- [ ] Defects cite which AC they violate
- [ ] Out-of-scope requests have routing

## Documentation (MANDATORY - No Confirmation Required)

- [ ] UAT Results file created at correct path
- [ ] Step results table complete
- [ ] Defects table (if any defects, otherwise "None")
- [ ] Out-of-scope table (if any, otherwise "None")
- [ ] Testing improvements noted
- [ ] Sign-off section complete

## Status Update (MANDATORY - No Confirmation Required)

- [ ] TASK-PLAN.md Task Skeleton table updated
- [ ] TASK-PLAN.md Task Files table updated
- [ ] Task status set correctly (✅ HumanDone / ❌ FailedUAT)

## Handoff (MANDATORY - Always Provide)

- [ ] If PASS: Clear instruction to run `@ralf-retro *run-retro`
- [ ] If FAIL: Clear instruction to return to `@ralf-dev` with defect list
- [ ] Next steps are copy-paste ready

## Memory Update

- [ ] Failure patterns recorded (if defects found)
- [ ] Automation opportunities recorded

## Issues Found

### Unclassified Failures
<!-- Failures without proper classification -->

### Missing Evidence
<!-- Failures without evidence -->
