# Refine Task Workflow Instructions

<critical>This workflow updates a Task Spec based on feedback without expanding scope.</critical>

<workflow>

<step n="1" goal="Load task context">
<action>Load the specified Task Spec from {output_folder}/{story_id}/{task_id}-*.md</action>
<action>Load the TASK-PLAN.md for context</action>
<action>Load the original story for reference</action>
<action>Load LESSONS-LEARNED.md to check for related patterns</action>

<validation>
- Task Spec file exists and is loaded
- Feedback is provided and clear
</validation>
</step>

<step n="2" goal="Classify feedback type">
<action>Categorize the feedback:</action>

1. **UAT Failure** - Acceptance criteria not met
   - Criteria ambiguity?
   - Missing test coverage?
   - Implementation bug (not task spec issue)?
   
2. **Dev Blocker** - Cannot implement as specified
   - Missing context?
   - Conflicting requirements?
   - Technical impossibility?
   
3. **Scope Creep Detection** - Request exceeds task scope
   - Route to *scope-check
   - Do NOT expand task
   
4. **Clarity Issue** - Spec is ambiguous
   - Tighten acceptance criteria
   - Add examples
   - Clarify forbidden zones

<output>Classified feedback with recommended action</output>
</step>

<step n="3" goal="Determine refinement scope">
<action>CRITICAL: Refinement must NOT expand task scope</action>

Allowed refinements:
- ✅ Clarify existing acceptance criteria
- ✅ Add missing verification methods
- ✅ Fix incorrect forbidden zones
- ✅ Add expected error cases
- ✅ Improve test specifications
- ✅ Add examples/clarifications

NOT allowed (requires new task or scope-check):
- ❌ Add new acceptance criteria
- ❌ Expand scope (in) section
- ❌ Add new features
- ❌ Remove forbidden zones without justification

<action>If feedback requires scope expansion, stop and invoke *scope-check</action>

<output>Approved refinement actions</output>
</step>

<step n="4" goal="Apply refinements">
<action>Update the Task Spec with approved refinements</action>
<action>Maintain the original task structure</action>
<action>Add a "Refinement History" section at bottom if not present:</action>

```markdown
## Refinement History

| Date | Change | Reason |
|------|--------|--------|
| {date} | {what changed} | {feedback that prompted it} |
```

<action>Save updated Task Spec</action>

<output>Refined Task Spec file</output>
</step>

<step n="5" goal="Update Test-First Improvement Note">
<action>Based on the feedback, update the "Test-First Improvement Note":</action>

> What test would have caught this issue earlier?

<action>This is the key learning for future tasks</action>

<output>Updated improvement note</output>
</step>

<step n="6" goal="Record lesson learned">
<action>Append to LESSONS-LEARNED.md:</action>

```markdown
### {date} - Task Refinement: {task_id}

**Feedback Type:** {UAT Failure | Dev Blocker | Clarity Issue}
**Root Cause:** {what caused the issue}
**Resolution:** {how it was fixed}
**Prevention:** {how to avoid in future tasks}
```

<output>Updated LESSONS-LEARNED.md</output>
</step>

<step n="7" goal="Update memory patterns">
<action>If this represents a recurring pattern, update:</action>
- {project-root}/bmad/ralf-taskflow/memory/failure-patterns.yaml

<action>Add pattern with:
- Pattern name
- Symptoms
- Root cause
- Prevention strategy
</action>

<output>Updated failure patterns (if applicable)</output>
</step>

<step n="8" goal="Present refinement summary">
<action>Display:</action>
- Original issue
- Changes made
- Files updated
- Lesson recorded

<action>Confirm task is ready for re-execution</action>

<output>Refinement complete confirmation</output>
</step>

</workflow>
