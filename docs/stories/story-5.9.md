# Story 5.9: Hardening + End-to-End UAT

## 1. Goal
Validate the complete Epic 5 Form Builder Readiness and Review & Publishing lifecycle through comprehensive end-to-end testing, and fix any identified regressions or bugs.

## 2. Business Value
Ensures the core customer journeys (Company User creating/testing a form and Company Admin reviewing/publishing it) are robust and frictionless before we conclude Epic 5.

## 3. Scope
- Execute the Comprehensive E2E UAT Strategy.
- Validate Form Builder Readiness (assets, defaults, schema parity).
- Validate Review/Test/Publish Governance (preview vs production, test thresholds, publish request, review queue, activation windows, stable URLs).
- Address any bugs, styling regressions, or critical UX friction points discovered during UAT.

### Out of Scope
- Major new feature development.
- UX consolidation (Unified Workspace) - deferred to a potential Story 5.10 or later epic.
- Payments (Stripe) and invoicing - deferred to Epic 6.

## 4. Key Work Streams
1. **UAT Execution**: Human executes the E2E UAT Guide (`STORY-5.9-UAT-TEST-GUIDE.md`).
2. **Defect Tracking**: Any failures are logged directly in the UAT Guide.
3. **Hardening**: Dev agent resolves identified defects.
4. **Verification**: Re-test to ensure fixes don't introduce new regressions.

## 5. Done Criteria
- [ ] End-to-End UAT executed for both Company User and Company Admin paths.
- [ ] Background asset upload/rendering verified end-to-end.
- [ ] Company-level defaults inheritance verified end-to-end.
- [ ] Preview testing gate and threshold logic verified.
- [ ] Publish request and Admin review approval workflow verified.
- [ ] Activation windows and stable public URLs verified.
- [ ] All critical bugs and regressions found during UAT are fixed.
