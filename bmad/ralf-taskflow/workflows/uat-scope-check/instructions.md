# UAT Scope Check Workflow Instructions

<critical>Distinguish between DEFECTS and OUT-OF-SCOPE requests during UAT.</critical>
<critical>Only violations of Acceptance Criteria are defects.</critical>

<workflow>

<step n="1" goal="Load Task Spec">
<action>Load the Task Spec being tested</action>
<action>Extract all Acceptance Criteria</action>
<action>Note the Scope (Out) items</action>

<output>AC list loaded</output>
</step>

<step n="2" goal="Analyze the request">
<action>Understand what the tester is asking about:</action>
- Is it about existing behavior?
- Is it about new functionality?
- Is it about an error/bug?

<output>Request understood</output>
</step>

<step n="3" goal="Check against Acceptance Criteria">
<action>For each AC, ask:</action>
- Does this request relate to this AC?
- Does the current behavior violate this AC?

<action>Classification:</action>

**DEFECT** if:
- An AC explicitly states behavior X
- The implementation does NOT exhibit behavior X
- This is a clear violation of the spec

**OUT OF SCOPE** if:
- No AC covers this functionality
- The request is for NEW behavior
- The implementation works as specified, but user wants more

**ENHANCEMENT** if:
- Implementation meets all ACs
- Request is about "nicer" or "better" behavior
- Not a failure, just a suggestion

<output>Classification determined</output>
</step>

<step n="4" goal="Provide verdict">
<action>Output structured result:</action>

## Scope Check Result

**Request:** [what tester asked about]

**Task Spec:** {task_id}

**Classification:** [DEFECT | OUT_OF_SCOPE | ENHANCEMENT]

**Rationale:**
- If DEFECT: "This violates AC{n}: '{criterion}' because [explanation]"
- If OUT_OF_SCOPE: "No AC covers this. The relevant ACs are: [list]"
- If ENHANCEMENT: "All ACs are satisfied. This is a suggestion for improvement."

**Routing:**
- DEFECT: Add to defects list → ralf-dev must fix
- OUT_OF_SCOPE: Add to out-of-scope list → ralf-sm or PM backlog
- ENHANCEMENT: Add to suggestions → future consideration

<output>Verdict delivered</output>
</step>

</workflow>

## Key Principle

**A tester discovering something they WANT is not the same as a DEFECT.**

Only classify as DEFECT if:
1. There is an explicit AC that describes expected behavior
2. The implementation does NOT match that expected behavior

Everything else is OUT_OF_SCOPE or ENHANCEMENT.
