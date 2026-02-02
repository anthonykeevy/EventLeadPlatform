# Next Task Workflow Instructions

<critical>This workflow manages task progression within a story.</critical>
<critical>Run this after each task chat completes (after retro).</critical>

<workflow>

<step n="1" goal="Load story and task context">
<action>Request from user if not provided:
- Story ID (e.g., "3.10")
- Just-completed Task ID (e.g., "T01")
</action>

<action>Load required files:</action>
- {output_folder}/{story_id}/TASK-PLAN.md
- {output_folder}/{story_id}/LESSONS-LEARNED.md
- {output_folder}/{story_id}/{completed_task_id}.retro.md (if exists)
- {output_folder}/{story_id}/{completed_task_id}.uat-results.md

<action>If TASK-PLAN.md does not exist, STOP and route to decompose-story workflow</action>

<output>Context loaded</output>
</step>

<step n="2" goal="Verify completed task status">
<action>Check the completed task's UAT results:</action>
- If FailedUAT: Report issues and ask if user wants to create a fix task
- If HumanDone: Proceed to step 3
- If no results: Ask user for status

<action>Update TASK-PLAN.md to mark completed task status:</action>

```markdown
| Task | Status | Notes |
|------|--------|-------|
| T01-xxx | ✅ HumanDone | Completed {date} |
```

<output>Task status verified and updated</output>
</step>

<step n="3" goal="Check for story completion">
<action>Review TASK-PLAN.md for remaining tasks:</action>
- Count tasks with status: Pending, Ready, In Progress
- Count tasks with status: HumanDone, Skipped

<action>If ALL tasks are HumanDone or Skipped:</action>
1. Display: "🎉 All tasks complete!"
2. Check story Done Criteria (if defined in story file)
3. For each Done Criterion:
   - Verify it is satisfied based on task completions
   - Mark as ✅ or ❌
4. If all Done Criteria pass: Recommend proceeding to Stage 4 (Story Finalization)
5. If any fail: Identify gap and propose additional task

<action>If tasks remain, proceed to step 4</action>

<output>Story completion check done</output>
</step>

<step n="4" goal="Identify next task">
<action>From TASK-PLAN.md, find the next task:</action>
1. Look for tasks with status: Ready
2. If no Ready tasks, look for Pending tasks whose dependencies are met
3. Respect the dependency order in TASK-PLAN.md

<action>Display next task summary:</action>

## Next Task: {task_id}
**Name:** {task_name}
**Dependencies:** {dependencies or "None"}
**Estimated Complexity:** {complexity if noted}

<output>Next task identified</output>
</step>

<step n="5" goal="Review and refine next task spec">
<action>If next task spec already exists ({output_folder}/{story_id}/{task_id}.md):</action>
1. Read the existing spec
2. Check if any LESSONS-LEARNED items affect this task
3. Check if any BACKLOG-ITEMS should be incorporated
4. Propose refinements if needed

<action>If next task spec does NOT exist (skeleton was placeholder):</action>
1. Load the story file for requirements context
2. Load LESSONS-LEARNED.md for patterns to apply
3. Create the full task spec following Task Spec template

<action>Apply lessons learned:</action>
- Check LESSONS-LEARNED.md for patterns that apply to this task
- Update task spec with preventive measures if applicable

<output>Task spec ready</output>
</step>

<step n="6" goal="Update status and prepare handoff">
<action>Update TASK-PLAN.md:</action>
- Mark next task as "In Progress"
- Update "Last Updated" timestamp

<action>Create or update STATUS.md:</action>

```markdown
# Story {story_id} Status

**Last Updated:** {date}
**Current Task:** {next_task_id}

## Progress
| Task | Status | Completed |
|------|--------|-----------|
| T01 | ✅ HumanDone | {date} |
| T02 | 🔄 In Progress | - |
| T03 | ⏳ Pending | - |

## Blockers
[None or list blockers]

## Scope Changes
[None or list routed items]
```

<output>Status updated</output>
</step>

<step n="7" goal="Generate new chat instructions">
<action>Provide copy-paste instructions for the user:</action>

---

## Ready for Next Task

**Open a new Cursor chat** and paste:

```markdown
@ralf-dev

*run-task

Task Spec: docs/tasks/{story_id}/{next_task_id}.md

Rules:
- Do not expand scope.
- If anything is out-of-scope, stop and route it.

Outputs:
- docs/tasks/{story_id}/{next_task_id}.completion.md
```

After dev completes, in the SAME chat:

```markdown
@ralf-uat *generate-uat
Task Spec: docs/tasks/{story_id}/{next_task_id}.md
Completion Note: docs/tasks/{story_id}/{next_task_id}.completion.md
```

Then test manually, record results:

```markdown
@ralf-uat *record-uat
[Paste your pass/fail results]
```

Then run retro:

```markdown
@ralf-retro *run-retro
[Task files from above]
```

**Return to this main chat when task chat is complete.**

---

<output>Handoff complete</output>
</step>

</workflow>

## Error Handling

### If TASK-PLAN.md is missing:
- STOP
- Route to decompose-story workflow first

### If task has failed dependencies:
- Report the failed dependency
- Ask if user wants to re-run the dependency or skip

### If all tasks complete but Done Criteria fail:
- Identify which criterion failed
- Propose a new task to address the gap
- Add to TASK-PLAN.md as new task

### If scope creep is discovered in lessons:
- Check BACKLOG-ITEMS.md
- Confirm items should remain out of scope
- Do NOT add to current task
