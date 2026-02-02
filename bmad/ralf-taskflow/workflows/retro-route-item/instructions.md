# Route Item Workflow Instructions

<critical>This workflow routes scope creep and new work to the appropriate backlog.</critical>
<critical>DO NOT implement the item - only document and route.</critical>

<workflow>

<step n="1" goal="Collect item details">
<action>Gather information about the item:</action>
- Description: What is the request?
- Source: Where was it discovered? (task, UAT, retro)
- Why out of scope: Which AC/scope boundary excludes it?

<output>Item details collected</output>
</step>

<step n="2" goal="Classify the item">
<action>Determine classification:</action>

**NEW_FEATURE:**
- Functionality not in any AC
- New user capability
- New integration

**BUG_IN_OTHER_TASK:**
- Defect found, but outside current task scope
- Issue in existing functionality not being modified
- Problem in dependency

**ENHANCEMENT:**
- Current spec is met, but could be better
- UX improvement
- Performance improvement

**TECH_DEBT:**
- Code quality issue
- Refactoring opportunity
- Documentation gap

<output>Classification: [NEW_FEATURE | BUG_IN_OTHER_TASK | ENHANCEMENT | TECH_DEBT]</output>
</step>

<step n="3" goal="Determine routing">
<action>Based on classification, recommend routing:</action>

| Classification | Routing Options |
|----------------|-----------------|
| NEW_FEATURE | ralf-sm (new task in current story) OR PM backlog (future sprint) |
| BUG_IN_OTHER_TASK | Bug tracker OR ralf-sm (urgent fix task) |
| ENHANCEMENT | PM backlog (prioritize) |
| TECH_DEBT | Tech debt backlog (refinement) |

<action>Consider urgency:</action>
- Blocks current work? → Add to current story
- Nice to have? → Future backlog
- Breaking production? → Urgent bug

<output>Routing recommendation</output>
</step>

<step n="4" goal="Format backlog item">
<action>Create formatted backlog note:</action>

## Backlog Item: [Title]

**ID:** BI-{story_id}-{sequence}

**Source:** Discovered during {task_id} {phase}

**Date:** {date}

**Classification:** [NEW_FEATURE | BUG_IN_OTHER_TASK | ENHANCEMENT | TECH_DEBT]

---

### Description

[Detailed description of what is needed]

### Rationale

[Why this matters / impact if not done]

### Out of Scope Because

[Cite specific AC or scope boundary from Task Spec]

---

### Suggested Routing

- [ ] **Option A:** Add to current story as new task
  - Route to: `@ralf-sm` with story context
  
- [ ] **Option B:** Add to PM backlog for next sprint
  - Priority: [High | Medium | Low]
  
- [ ] **Option C:** Add to tech debt backlog
  - Owner: [team/person]

### Priority Suggestion

**Priority:** [High | Medium | Low]

**Rationale:** [why this priority]

---

### Acceptance Criteria (Draft)

If this becomes a task, suggested ACs:

- [ ] [draft AC 1]
- [ ] [draft AC 2]

<output>Backlog item formatted</output>
</step>

<step n="5" goal="Save to BACKLOG-ITEMS.md">
<action>Append to docs/tasks/{story_id}/BACKLOG-ITEMS.md</action>
<action>If file doesn't exist, create with header:</action>

# Backlog Items: {story_id}

> Items discovered during task execution that are out of scope.
> Route to appropriate backlog after review.

---

[item]

<output>Backlog item saved</output>
</step>

<step n="6" goal="Notify user">
<action>Display:</action>
- Item saved to BACKLOG-ITEMS.md
- Classification and routing recommendation
- Next steps (who to notify)

<action>Suggest notification:</action>
- "To add to current story: `@ralf-sm *decompose-story` with this item"
- "To add to PM backlog: Forward to [PM] with priority"

<output>Routing complete</output>
</step>

</workflow>
