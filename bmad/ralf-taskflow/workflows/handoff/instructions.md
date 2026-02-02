# Handoff Workflow Instructions

<critical>This workflow creates final documentation for completed task.</critical>
<critical>All evidence must be captured for UAT and retrospective.</critical>

<workflow>

<step n="1" goal="Gather implementation summary">
<action>Collect:
  - Summary of what was implemented
  - All files changed (with change types)
  - Test commands run and results
  - Any blockers or issues encountered
</action>

<output>Implementation data gathered</output>
</step>

<step n="2" goal="Verify all ACs are addressed">
<action>For each Acceptance Criterion:</action>
- Confirm it was implemented
- Document how it was verified
- Include specific evidence (test output, screenshots, etc.)

<action>If any AC is NOT satisfied:</action>
- Document the gap
- Explain why (blocker, scope issue, etc.)
- Recommend resolution path

<output>AC verification complete</output>
</step>

<step n="3" goal="Generate completion note">
<action>Create completion note with full structure:</action>

```markdown
# Task Completion: {task_id}

**Story:** {story_id}
**Task:** {task_name}
**Completed:** {date}
**Status:** [Complete | Partial | Blocked]

---

## Summary of Changes

[1-3 sentence summary of what was implemented and why]

## Files Changed

| File | Change | Reason |
|------|--------|--------|
| `path/to/file.ts` | Modified | Implement AC1 |
| `path/to/new.ts` | Created | New component for AC2 |

## Acceptance Criteria Verification

### AC1: [criterion text]
- **Status:** PASS / FAIL / BLOCKED
- **Evidence:** [specific proof - test output, behavior, etc.]

### AC2: [criterion text]
- **Status:** PASS / FAIL / BLOCKED
- **Evidence:** [specific proof]

## Test Evidence

### Automated Tests

```bash
$ npm test -- --grep "feature"
PASS src/feature.test.ts
  ✓ should handle X (15ms)
  ✓ should reject Y (8ms)
```

### Build Verification

```bash
$ npm run build
Build successful. No errors.
```

### Lint Check

```bash
$ npm run lint
No lint errors found.
```

## Manual UAT Steps

For human verification:

1. [ ] [Navigate to X] -> Verify: [Y appears]
2. [ ] [Click Z] -> Verify: [W happens]
3. [ ] [Enter invalid data] -> Verify: [Error message shown]

## Known Limitations / Out-of-Scope Items

Items discovered during implementation that need future work:

- [ ] [Description] -> Route to: ralf-sm
- [ ] [Description] -> Route to: PM backlog

## Recommended Next Step

**[Choose one]:**
- ✅ Ready for UAT by human
- ⚠️ Blocked - needs ralf-sm attention: [reason]
- 🔀 Split recommended - see details above
```

<action>Save to: {output_folder}/{story_id}/{task_id}.completion.md</action>

<output>Completion note saved</output>
</step>

<step n="4" goal="Generate QA notes (optional)">
<action>If there are insights for QA/retrospective:</action>

```markdown
# QA Notes: {task_id}

## Testing Insights

- [What worked well in testing]
- [What was tricky to verify]

## Potential Regression Areas

- [Areas that might break in future]
- [Related components to watch]

## Improvement Suggestions

- [How the task could have been specified better]
- [Tests that would have caught issues earlier]
```

<action>Save to: {output_folder}/{story_id}/{task_id}.qa-notes.md</action>

<output>QA notes saved (if applicable)</output>
</step>

<step n="5" goal="Update lessons learned">
<action>Append any new insights to LESSONS-LEARNED.md:</action>

```markdown
### {date} - Task Completion: {task_id}

**What worked:** [brief]
**What was hard:** [brief]
**Improvement for next time:** [actionable]
```

<output>Lessons recorded</output>
</step>

<step n="6" goal="Final summary">
<action>Display handoff summary:</action>

## Handoff Complete

- **Task:** {task_id}
- **Files changed:** {count}
- **ACs verified:** {count}/{total}
- **Completion note:** {path}

**Next step:** [UAT by human | ralf-sm attention | etc.]

<output>Handoff complete</output>
</step>

</workflow>
