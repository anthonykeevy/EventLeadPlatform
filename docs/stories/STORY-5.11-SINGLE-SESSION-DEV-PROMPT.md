# Story 5.11: Tech Debt Remediation (Single-Session Dev Prompt)

## Instructions for @dev

We are executing **Story 5.11: Tech Debt Remediation**. Your goal is to restore the platform's automated testing and code quality baselines to a "Green" state.

### 🎯 Your Goal
1. Fix the backend `pytest` suite so it runs and passes 100%. (Currently crashing with a SQLAlchemy metadata `InvalidRequestError` regarding `ref.Country`).
2. Fix the frontend `vitest` suite so `npm run test:unit` passes 100%. (Currently 25 failures, many due to using `jest.fn()` instead of `vi.fn()`).
3. Fix the frontend TypeScript linting so `npm run lint` returns 0 warnings. (Currently 241 warnings, almost all `@typescript-eslint/no-explicit-any`).

### 📚 Context
- **Story Context**: Read `docs/stories/story-context-5.11.xml`
- **Story Goals**: Read `docs/stories/story-5.11.md`

### 🚀 The "Green CI/CD" Workflow Loop
You are strictly bound by the Green CI/CD Rule. You MUST follow these steps:
1. **Diagnose & Fix Backend**: Run `python -m pytest` in the `backend` folder. Fix the circular import / metadata issue. Ensure all tests pass.
2. **Diagnose & Fix Frontend Tests**: Run `npm run test:unit` in the `frontend` folder. Fix the Vitest vs Jest mismatch and update any stale test files to match Epic 5 component props. Ensure all tests pass.
3. **Purge 'any' Types**: Run `npm run lint` in the `frontend` folder. Methodically replace `any` with proper types, interfaces, or `unknown` where strictly necessary. Do not just suppress the warnings with `eslint-disable`.
4. **Verification**: You may only create your closeout commit when ALL THREE commands (`pytest`, `test:unit`, `lint`) are 100% green.

**Commit Protocol**: Commit your fixes incrementally as you solve each phase (e.g., `fix(5.11): resolve backend sqlalchemy test crash`).

---

**Human**: I am handing this story over to you. Please begin by diagnosing the backend test crash and the frontend test failures. Do not stop until all tests are green and all lint warnings are resolved!