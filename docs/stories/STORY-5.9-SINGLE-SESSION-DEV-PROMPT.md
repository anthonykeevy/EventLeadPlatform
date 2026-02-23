# Story 5.9: Hardening & UAT (Single-Session Dev Prompt)

## Instructions for @dev

We are executing **Story 5.9: Hardening + End-to-End UAT** for Epic 5. The feature foundation is completely built. Your role in this session is to **fix regressions and bugs** discovered by the human during the execution of the UAT Guide.

### 🎯 Your Goal
Address the specific defects logged in the Defect Tracking table within `docs/stories/STORY-5.9-UAT-TEST-GUIDE.md` as the human executes the tests.

### 📚 Context
- **Story Context**: Read `docs/stories/story-context-5.9.xml`
- **UAT Guide & Defects**: Read `docs/stories/STORY-5.9-UAT-TEST-GUIDE.md`
- **Constraints**: 
  - Do NOT introduce major new features.
  - Fixes must respect the existing architectures (assets, company defaults, shared resolvers, activation windows, publish requests).
  - Focus purely on stabilization and resolving friction.

### 🚀 Workflow Loop
The human will run the UAT steps and identify bugs. For each bug (or batch of bugs):
1. **Identify**: Read the updated Defect Tracking table in the UAT Guide.
2. **Analyze**: Use `Grep` or `SemanticSearch` to locate the source of the defect in the frontend or backend.
3. **Fix**: Implement the fix.
4. **Automated Verification**: Run frontend/backend linting, type-checking, or tests to ensure no syntax errors were introduced.
5. **Commit**: Commit the implementation changes with a clear message (e.g., `fix(5.9): resolve asset upload bug on preview`).
6. **Handoff**: Ask the human to re-verify the UAT step.

*If there are no open bugs currently logged, wait for the human to execute the UAT and provide the next issue.*

---

**Human**: I am beginning the UAT execution now. Stand by, or review the current open defects in `STORY-5.9-UAT-TEST-GUIDE.md` if any exist.