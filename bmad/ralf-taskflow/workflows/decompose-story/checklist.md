# Decompose Story Validation Checklist

## Input Validation

- [ ] Story identifier is specified and valid
- [ ] Story content is loaded (not empty)
- [ ] PRD document is loaded
- [ ] Architecture document is loaded
- [ ] Story has at least one acceptance criterion

## Scope Validation

- [ ] Story scope boundaries are explicitly confirmed with user
- [ ] Out-of-scope items are documented in TASK-PLAN
- [ ] No ambiguous scope items remain unresolved

## Task Decomposition Quality

- [ ] All story ACs are covered by at least one task
- [ ] No task exceeds "M" (Medium) effort estimate
- [ ] Each task has at least one automated test requirement
- [ ] Each task has binary (pass/fail) acceptance criteria
- [ ] Each task can be executed in a single conversation session
- [ ] Tasks follow vertical slice pattern where possible

## Dependency Validation

- [ ] Dependency graph has no cycles
- [ ] Dependencies are correctly ordered (prereqs before dependents)
- [ ] No implicit dependencies (all are documented)

## Forbidden Zone Validation

- [ ] Each task has explicit forbidden zones defined
- [ ] Forbidden zones are consistent across tasks (no conflicts)
- [ ] Completed epic code is marked as forbidden
- [ ] Reasons for forbidden zones are documented

## File Output Validation

- [ ] TASK-PLAN.md created in {output_folder}/{story_id}/
- [ ] All Task Spec files created (T01, T02, etc.)
- [ ] LESSONS-LEARNED.md initialized
- [ ] File names follow convention: T{nn}-{slug}.md

## Content Completeness

Each Task Spec must contain:
- [ ] Scope (In) section with checkboxes
- [ ] Scope (Out) section with forbidden items
- [ ] Acceptance Criteria table with verification methods
- [ ] Required Tests section (automated + manual)
- [ ] Expected Error Cases
- [ ] Forbidden Zones with file paths
- [ ] Out-of-Scope Handling rules
- [ ] Dev Agent Instructions

## Issues Found

### Critical Issues
<!-- Must be fixed before plan can be approved -->

### Warnings
<!-- Should be addressed but don't block approval -->

### Recommendations
<!-- Optional improvements -->
