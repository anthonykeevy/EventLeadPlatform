# Scope Check Workflow Instructions

<critical>This workflow determines if a user request is within the Task Spec scope.</critical>
<critical>NEVER implement out-of-scope requests.</critical>

<workflow>

<step n="1" goal="Load Task Spec scope boundaries">
<action>Load the current Task Spec file</action>
<action>Extract:
  - Scope (In) items
  - Scope (Out) items
  - Forbidden Zones
  - Acceptance Criteria
</action>

<output>Scope boundaries loaded</output>
</step>

<step n="2" goal="Analyze user request">
<action>Parse the user request to understand:
  - What action is being requested
  - What files/components would be affected
  - What the expected outcome is
</action>

<output>Request analysis complete</output>
</step>

<step n="3" goal="Classify request">
<action>Compare request against scope boundaries:</action>

**IN SCOPE if:**
- Directly listed in Scope (In)
- Required to satisfy an existing Acceptance Criterion
- Uses only allowed files/components

**OUT OF SCOPE if:**
- Listed in Scope (Out)
- Would touch Forbidden Zones
- Not related to any Acceptance Criterion
- Would require new Acceptance Criteria

<output>Classification determined</output>
</step>

<step n="4" goal="Provide verdict and routing">
<action>Output structured result:</action>

## Scope Check Result

**Request:** [summary of what user asked]

**Task Spec:** [task ID]

**Classification:** [IN_SCOPE | OUT_OF_SCOPE]

**Rationale:**
- [cite specific scope item or forbidden zone]
- [explain why it is/isn't within scope]

**Action:**
- If IN_SCOPE: "Proceed with implementation"
- If OUT_OF_SCOPE: "Do NOT implement. Route to [ralf-sm for new task | PM backlog for future story]"

<output>Verdict delivered</output>
</step>

</workflow>

## Routing Guidelines

### Route to ralf-sm when:
- Request is a reasonable extension of current story
- Request could be a new task in the same story
- Request clarifies ambiguity in existing tasks

### Route to PM backlog when:
- Request is a new feature outside current story
- Request conflicts with architectural decisions
- Request requires business decision
