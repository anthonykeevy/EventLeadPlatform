# Update Testing Playbook Workflow Instructions

<critical>This workflow updates the testing playbook with patterns from retros.</critical>
<critical>Focus on reusable patterns that prevent future UAT churn.</critical>

<workflow>

<step n="1" goal="Load retro findings">
<action>Load the most recent retro.md file(s)</action>
<action>Extract test improvements section</action>
<action>Load existing testing-playbook.md if it exists</action>

<output>Retro findings loaded</output>
</step>

<step n="2" goal="Identify high-leverage test patterns">
<action>From retro, extract tests that would have caught issues:</action>
- What type of test? (unit/integration/e2e)
- What pattern does it follow?
- When should this test be written?

<action>Generalize into reusable pattern:</action>

### Pattern: [Name]

**When to Use:** [task type or situation]

**Test Type:** unit | integration | e2e

**Template:**
```typescript
describe('[Component/Feature]', () => {
  it('[should behavior]', () => {
    // [setup]
    // [action]
    // [assertion]
  });
});
```

**Command:** `npm test [pattern]`

<output>High-leverage test patterns</output>
</step>

<step n="3" goal="Identify regression checks">
<action>From retro, extract checks that should run earlier:</action>

| Check | When to Run | Command |
|-------|-------------|---------|
| [description] | Before commit | `npm run lint` |
| [description] | Before PR | `npm test` |
| [description] | Before deploy | `npm run test:e2e` |

<output>Regression checks list</output>
</step>

<step n="4" goal="Create AC templates by task type">
<action>Based on retro learnings, create AC templates:</action>

### Task Type: Form Component

**Standard ACs:**
- [ ] Component renders with correct label
- [ ] Input accepts valid values
- [ ] Validation shows appropriate errors
- [ ] Submit includes field value

**Required Tests:**
- Unit: Render, validation
- E2E: Full form flow

### Task Type: API Endpoint

**Standard ACs:**
- [ ] Returns correct status codes
- [ ] Validates input
- [ ] Auth required
- [ ] Persists data

<output>AC templates by task type</output>
</step>

<step n="5" goal="Update or create testing-playbook.md">
<action>If file exists, merge new patterns:</action>
- Add new patterns without duplicating
- Update existing patterns if improved
- Preserve all existing content

<action>If file doesn't exist, create with structure:</action>

# Testing Playbook

> Reusable testing patterns extracted from task retrospectives.
> Last updated: {date}

---

## High-Leverage Tests

[patterns from step 2]

---

## Regression Checks

[table from step 3]

---

## AC Templates by Task Type

[templates from step 4]

---

## Quick Reference Commands

| Situation | Command |
|-----------|---------|
| Before commit | `npm run lint && npm test` |
| Before PR | `npm run test:all` |
| Check coverage | `npm run test:coverage` |

<action>Save to: docs/learning/testing-playbook.md</action>

<output>Testing playbook updated</output>
</step>

</workflow>
