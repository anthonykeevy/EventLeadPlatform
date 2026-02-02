# Spec Improvement Workflow Instructions

<critical>This workflow improves Task Spec clarity ONLY - NO SCOPE EXPANSION.</critical>
<critical>Clarify existing ACs, don't add new requirements.</critical>

<workflow>

<step n="1" goal="Load inputs">
<action>Load Task Spec</action>
<action>Load retro findings</action>

<output>Inputs loaded</output>
</step>

<step n="2" goal="Identify clarity issues">
<action>Review each AC for ambiguity:</action>
- Is the expected behavior specific?
- Is the verification method clear?
- Could different people interpret it differently?

<action>Document issues:</action>

| AC | Clarity Issue |
|----|---------------|
| AC1 | "works correctly" is vague |
| AC2 | No error case specified |

<output>Clarity issues identified</output>
</step>

<step n="3" goal="Identify missing verification">
<action>For each AC, check if verification is specified:</action>
- How would you prove this AC is met?
- What test would verify it?
- What evidence would you show?

<action>Document gaps:</action>

| AC | Missing Verification |
|----|---------------------|
| AC1 | No test command specified |
| AC2 | No expected output defined |

<output>Missing verification identified</output>
</step>

<step n="4" goal="Identify scope boundary issues">
<action>Review Scope (In) and Scope (Out):</action>
- Are boundaries explicit?
- Any ambiguous items?
- Any items that caused confusion during dev/UAT?

<action>Document issues:</action>

| Item | Issue |
|------|-------|
| [item] | Could be interpreted as in-scope or out |

<output>Scope boundary issues identified</output>
</step>

<step n="5" goal="Propose improvements">
<action>For each issue, propose a clarification:</action>

## AC Clarifications

| Original AC | Issue | Improved AC |
|-------------|-------|-------------|
| "Form works correctly" | Vague | "Form submits successfully and shows confirmation message within 2 seconds" |

## Missing Verification Additions

| AC | Addition |
|----|----------|
| AC1 | **Verification:** Run `npm test form.test.ts` and expect all tests pass |

## Scope Boundary Clarifications

| Item | Current | Clearer |
|------|---------|---------|
| "Styling" | Vague | "Basic styling only - no custom themes or responsive breakpoints" |

<output>Improvements proposed</output>
</step>

<step n="6" goal="CRITICAL: Scope check">
<action>Before updating, verify each improvement:</action>

| Improvement | Is this CLARITY only? | Adds new scope? |
|-------------|----------------------|-----------------|
| [improvement] | YES | NO |

<action>REJECT any improvement that adds scope:</action>
- New feature → Route to ralf-sm
- New requirement → Route to ralf-sm
- Expanded boundary → Route to ralf-sm

<output>Scope check passed</output>
</step>

<step n="7" goal="Update Task Spec">
<action>Apply approved clarifications:</action>
- Update AC text inline
- Add "[Clarified: {date}]" marker
- Add verification where missing
- Clarify scope boundaries

<action>Do NOT:</action>
- Add new ACs
- Expand scope
- Add new requirements

<action>Save to: {task_spec_path}</action>

<output>Task Spec updated</output>
</step>

<step n="8" goal="Present summary">
<action>Display:</action>
- Number of clarifications made
- Any scope expansion requests routed
- Updated spec location

<output>Spec improvement complete</output>
</step>

</workflow>

## Scope Expansion Examples (REJECT)

These are NOT clarifications - route to ralf-sm:
- "Add email notification" (new feature)
- "Support multiple file types" (expanded requirement)
- "Improve performance" (new NFR)
- "Add error logging" (new functionality)

## Clarity Examples (ACCEPT)

These ARE clarifications - apply them:
- "Shows confirmation" → "Shows green confirmation banner with 'Saved' text"
- "Validates input" → "Shows red error text below field when invalid"
- "Works on mobile" → "Renders correctly at 375px width"
