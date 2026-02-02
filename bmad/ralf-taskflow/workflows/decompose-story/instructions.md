# Decompose Story Workflow Instructions

<critical>This workflow produces TASK-PLAN.md and individual Task Spec files from a BMAD story.</critical>

<workflow>

<step n="1" goal="Gather and validate inputs">
<action>Confirm story identifier and load story content</action>
<action>Load PRD from specified path (default: {project-root}/docs/prd.md)</action>
<action>Load Architecture from specified path (default: {project-root}/docs/solution-architecture.md)</action>
<action>Load any domain docs if specified</action>
<action>Load memory patterns from {project-root}/bmad/ralf-taskflow/memory/decomposition-patterns.yaml if exists</action>

<validation>
- Story content is loaded and readable
- PRD is loaded
- Architecture is loaded
- Story has clear acceptance criteria
</validation>
</step>

<step n="2" goal="Confirm story boundaries">
<action>Extract and display the story's explicit scope</action>
<action>Identify what is explicitly OUT of scope for this story</action>
<action>Ask user to confirm boundaries are correct</action>
<action>Document any clarifications in the TASK-PLAN preamble</action>

<output>Confirmed story scope boundaries</output>
</step>

<step n="3" goal="Analyze story for task decomposition">
<action>Identify all acceptance criteria (ACs) in the story</action>
<action>Map ACs to logical implementation units</action>
<action>Identify dependencies between implementation units</action>
<action>Consider: What can be tested independently?</action>
<action>Apply learned patterns from decomposition-patterns.yaml</action>

<principles>
- Each task should be completable in a single conversation session
- Each task must have at least one automated test
- Each task must have binary (pass/fail) acceptance criteria
- Tasks should minimize file/module overlap
- Prefer vertical slices over horizontal layers
</principles>

<output>Preliminary task list with dependencies</output>
</step>

<step n="4" goal="Define forbidden zones per task">
<action>For each task, identify files/modules that are OUT of scope</action>
<action>Cross-reference with completed epics (load docs/epic-status.md if exists)</action>
<action>Mark any shared infrastructure that requires extra care</action>
<action>Document WHY each forbidden zone exists</action>

<output>Forbidden zone mapping per task</output>
</step>

<step n="5" goal="Generate TASK-PLAN.md">
<action>Create output folder: {output_folder}/{story_id}/</action>
<action>Generate TASK-PLAN.md using the task_plan_template from agent</action>
<action>Include:
  - Story summary
  - Explicit out-of-scope items
  - Dependency graph (ASCII art)
  - Task list table with status, dependencies, estimates
  - Brief summaries per task
  - Plan-level validation criteria
</action>
<action>Save to {output_folder}/{story_id}/TASK-PLAN.md</action>

<output>TASK-PLAN.md file</output>
</step>

<step n="6" goal="Generate individual Task Spec files">
<action>For each task in the plan:</action>
<action>Create T{nn}-{slug}.md using the task_spec_template from agent</action>
<action>Ensure each Task Spec includes:
  - Scope (In) - checkboxes
  - Scope (Out) - FORBIDDEN items with ❌
  - Acceptance Criteria table with verification methods
  - Required Tests (automated + manual UAT)
  - Expected error cases
  - Forbidden zones with paths
  - Out-of-scope handling rules
  - Test-first improvement note (leave blank for dev to fill)
  - Dev agent instructions
</action>
<action>Save each to {output_folder}/{story_id}/T{nn}-{slug}.md</action>

<output>Individual Task Spec files</output>
</step>

<step n="7" goal="Initialize LESSONS-LEARNED.md">
<action>Create LESSONS-LEARNED.md with template:</action>

```markdown
# Lessons Learned: {story_id}

**Story:** {story_title}
**Started:** {date}
**Status:** In Progress

---

## Development Lessons

<!-- Append lessons here with timestamps -->

## Testing Lessons

<!-- Append lessons here with timestamps -->

## Scope Creep Requests

<!-- Document out-of-scope requests and where routed -->

| Date | Request | Classification | Routed To |
|------|---------|----------------|-----------|

---

*This file is append-only. Each lesson should include actionable insight for future stories.*
```

<action>Save to {output_folder}/{story_id}/LESSONS-LEARNED.md</action>

<output>LESSONS-LEARNED.md file</output>
</step>

<step n="8" goal="Validate decomposition quality">
<action>Run validation checklist:</action>
- [ ] All story ACs are covered by at least one task
- [ ] No task exceeds "M" effort estimate
- [ ] Each task has at least one automated test requirement
- [ ] Each task has binary acceptance criteria
- [ ] Dependency graph has no cycles
- [ ] Forbidden zones are consistent (no overlapping "allowed" and "forbidden")
- [ ] Each task can be executed in isolation (no implicit context dependencies)

<action>If validation fails, refine tasks and re-validate</action>

<output>Validated task decomposition</output>
</step>

<step n="9" goal="Present summary to user">
<action>Display:</action>
- Number of tasks generated
- Estimated total effort
- Suggested execution order
- File locations for all generated artifacts
- Any warnings or recommendations

<action>Ask if user wants to:
- Approve the plan
- Refine specific tasks
- Regenerate with different approach
</action>

<output>User confirmation or refinement request</output>
</step>

</workflow>

## Post-Workflow

After user approves the plan:
1. Tasks are ready for ralf-dev agent (or dev agent) to execute
2. Each task should be executed in its own conversation session
3. After each task completes, dev should update LESSONS-LEARNED.md
4. Ralf-SM can be re-invoked with *refine-task if UAT finds issues
