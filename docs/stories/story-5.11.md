# Story 5.11: Tech Debt Remediation

## 1. Goal
Restore the platform's automated testing and code quality baselines to a "Green" state before beginning Epic 6. This ensures the upcoming AI Generation and Monetization features are built on a stable, rigorously tested foundation.

## 2. Business Value
Prevents future regressions, reduces maintenance costs, and dramatically speeds up future development by giving the Dev agent reliable, automated feedback loops (CI/CD) to verify its own code.

## 3. Scope
- **Backend Tests:** Resolve the SQLAlchemy metadata errors (`InvalidRequestError: Table 'ref.Country' is already defined`) so that `pytest` can run and all backend tests pass.
- **Frontend Tests:** Fix the failing unit tests (replacing `jest.fn()` with `vi.fn()`, updating tests to match Epic 5 component changes) so that `npm run test:unit` passes 100%.
- **Frontend Linting:** Systematically purge the 241 `@typescript-eslint/no-explicit-any` warnings by replacing `any` with proper TypeScript interfaces, particularly around the Form Builder schemas and state management.

### Out of Scope
- Building new features or fixing non-critical functional bugs (unless they block tests).
- Modifying the underlying business logic of how forms are saved or published.

## 4. Key Work Streams
1. **Test Infrastructure Fixes**: Diagnose and resolve the root cause of the test suite crashes.
2. **Type Hardening**: Audit and type the frontend `any` usage.
3. **Verification**: Achieve a strict `0 errors, 0 warnings` on linters and `100% pass rate` on both test suites.

## 5. Done Criteria
- [ ] Backend: `python -m pytest` passes 100% of tests.
- [ ] Frontend: `npm run test:unit` passes 100% of tests.
- [ ] Frontend: `npm run lint` returns 0 errors and 0 warnings.
