---
stepsCompleted: ['step-01-load-context', 'step-02-discover-tests', 'step-03-map-criteria', 'step-04-analyze-gaps', 'step-05-gate-decision']
lastStep: 'step-05-gate-decision'
lastSaved: '2026-02-25'
---

## Requirements Context

### Source Documents
- **PRD (`docs/prd.md`)**: Analyzed the MVP Scope (3 Months) section, specifically focusing on the 11 Core Features required for launch.
- **Epic 5 Status (`docs/stories/EPIC-5-STATUS.md`)**: Analyzed the "Epic 5 Done Criteria" and recent feature additions (Background Assets, Company Defaults, Preview/Production Governance, Admin Publish Review, and Activation Windows).

### Key Acceptance Criteria / Functional Areas to Trace
1. **User Auth & RBAC**: Signup, login, verification, onboarding, JWT, RBAC middleware.
2. **Company Management**: Company profile, activity log, data isolation.
3. **Events Management**: CRUD, event types, private events, activation logic.
4. **Team Collaboration**: Invitations, expiry handling, role assignment.
5. **Preview & Testing System**: Preview mode toggle, test thresholds, audit logging.
6. **Form Builder Core**: Component rendering, drag-and-drop, validation rules.
7. **Form Asset & Brand Governance (Epic 5)**: Custom backgrounds (Azure blob ready), Company-level defaults, definition schema alignment.
8. **Form Publishing & Hosting**: Publish requests (User -> Admin), approval queue, stable public URLs, Unpublish logic.
9. **Lead Collection**: Data storage, preview vs production lead flagging.
10. **Analytics & Export**: Lead counts, CSV export formats (Salesforce, etc.).

---

## Knowledge Base Summary
Loaded principles from the TEA methodology:
- **Test Priorities Matrix**: P0 (Auth, Lead Collection, Publishing), P1 (Events, Company Settings), P2/P3 (Secondary builder UX).
- **Risk Governance / Probability-Impact**: Identifying areas where failure blocks revenue or data collection.
- **Test Quality**: Emphasizing deterministic assertions for backend tests (Pytest).
- **Selective Testing**: Mapping coverage to ensure we don't over-test simple CRUD vs critical workflows.

---

## Discovered Tests

I have successfully scanned the `backend/tests` directory and cataloged the current test suite. There are currently **0** E2E tests in the newly scaffolded Playwright framework. All coverage resides in the Pytest backend test suite.

### Backend Tests (API / Integration / Unit)

**Authentication & Security (Area 1)**
- `test_auth_signup.py`
- `test_auth_login.py`
- `test_auth_email_verification.py`
- `test_password_reset.py`
- `test_jwt_service.py`
- `test_password_validator.py`
- `test_auth_middleware.py`
- `test_rbac.py`, `test_rbac_unit.py`
- `test_security.py`

**Company & Multi-Tenancy (Area 2)**
- `test_company_users_endpoint.py`
- `test_multi_tenancy.py`
- `test_company_verification.py`

**Team & Invitations (Area 4)**
- `test_team_invitations.py`
- `test_invitation_acceptance.py`

**Form Asset & Governance - Epic 5 (Area 7)**
- `test_assets_upload.py` (Background assets)
- `test_form_defaults_service.py` (Company defaults)
- `test_form_definition_schema_5_3.py` (Schema alignment)
- `test_resolver_parity.py` (Resolver parity)

**Validation & Schema (Area 6)**
- `test_schema_validation.py`
- `test_validators.py`

**Core Integration / Misc**
- `test_story_1_9_integration.py`
- `test_story_1_11_integration.py` (and access requests, relationships, switching)
- `test_onboarding_flow.py`

### Coverage Heuristics Inventory

1. **API Endpoint Coverage:** High concentration of tests around Auth endpoints (`/api/auth/*`), Company data, and newly added Epic 5 Asset/Defaults endpoints. *Missing/Low visibility:* Event Management endpoints and specific Form Publishing/Status endpoints from recent Epic 5 workflows.
2. **Auth/Authz Coverage:** Excellent coverage mapping to RBAC middleware, JWT validation, and negative paths (e.g. `test_rbac.py`, `test_auth_middleware.py`).
3. **Error-Path Coverage:** Many tests focus on schema validation and expected errors (e.g. duplicate emails, invalid passwords, expired tokens), though recent backend failures suggest some error paths might be brittle due to shared database state.
4. **E2E Coverage Gap:** Currently a **100% gap** in actual E2E coverage. No tests actually open a browser, click buttons, and verify the frontend/backend integration from the user's perspective.

---

## Traceability Matrix (Requirements -> Tests)

| # | Functional Area / Requirement | Priority | Mapped Tests (Pytest) | E2E Tests | Coverage Status | Heuristic Notes |
|---|---|---|---|---|---|---|
| 1 | **User Auth & RBAC**<br>Signup, login, verify, JWT | P0 | `test_auth_signup.py`, `test_auth_login.py`, `test_auth_email_verification.py`, `test_auth_middleware.py`, `test_rbac.py` | None | **INTEGRATION-ONLY** | Strong negative path coverage (invalid tokens, missing fields). Fully covered at API layer. |
| 2 | **Company Management**<br>Profile, data isolation | P1 | `test_multi_tenancy.py`, `test_company_verification.py` | None | **PARTIAL** | Multi-tenancy isolation tested at backend. Lacks E2E UI verification. |
| 3 | **Events Management**<br>CRUD, activation logic | P1 | *No explicit event test files discovered* | None | **NONE** | **Gap Alert:** Core entity (Events) appears missing dedicated backend test suites. |
| 4 | **Team Collaboration**<br>Invites, role assignment | P1 | `test_team_invitations.py`, `test_invitation_acceptance.py` | None | **INTEGRATION-ONLY** | Invite lifecycle tested. Needs E2E for email link flow. |
| 5 | **Preview & Testing System**<br>Preview toggle, test thresholds | P1 | *No explicit tests discovered* | None | **NONE** | **Gap Alert:** New Epic 5 governance rules (thresholds) missing backend validation. |
| 6 | **Form Builder Core**<br>Component rendering, validation | P0 | `test_schema_validation.py`, `test_validators.py` | None | **PARTIAL** | Schema validation exists, but drag-and-drop/rendering is inherently an E2E concern (0% covered). |
| 7 | **Form Asset & Brand Gov.**<br>Assets, Defaults, Parity | P1 | `test_assets_upload.py`, `test_form_defaults_service.py`, `test_form_definition_schema_5_3.py`, `test_resolver_parity.py` | None | **INTEGRATION-ONLY** | High coverage from Epic 5, but completely lacks UI verification of defaults applying correctly. |
| 8 | **Form Publishing & Hosting**<br>Requests, approval queue, URL | P0 | *No explicit tests discovered* | None | **NONE** | **Gap Alert:** Critical P0 path. No API or E2E tests verifying the publish state machine. |
| 9 | **Lead Collection**<br>Data storage, preview flags | P0 | *No explicit tests discovered* | None | **NONE** | **Gap Alert:** Critical P0 path. Submitting a form must be tested immediately. |
| 10 | **Analytics & Export**<br>Lead counts, CSV export | P2 | `test_dashboard_kpis.py` | None | **PARTIAL** | Basic KPI coverage. CSV export format coverage unknown. |

---

## Gap Analysis & Recommendations

### Coverage Statistics
- **Total Requirements Mapped:** 10
- **Fully Covered:** 0 (0%)
- **Integration-Only / Partial:** 6 (60%)
- **Uncovered (NONE):** 4 (40%)

### Priority Coverage
- **P0 Requirements:** 4 total. (0 Fully Covered, 2 Partial/Integration, 2 NONE). **0% Full Coverage**.
- **P1 Requirements:** 5 total. (0 Fully Covered, 3 Partial/Integration, 2 NONE). **0% Full Coverage**.

### Heuristics & Blind Spots
- **E2E Gap:** 100% blind spot on all frontend UI rendering, navigation, and user-flows.
- **Backend Gaps:** The core domain entities `Events` (Area 3), `Publishing/Status` (Area 8), and `Lead Collection` (Area 9) show severe backend testing gaps, likely overlooked during Epic 5 development.

### Recommendations

1. **[URGENT] P0 E2E Automation:** 
   Run `/bmad:tea:automate` to generate an E2E test for Area 8 (Publishing) and Area 9 (Lead Collection). A user must be able to publish a form and submit a lead.
2. **[URGENT] P0 Backend Gap:** 
   The backend lacks API tests for Form Publishing and Lead Collection. These must be written immediately to ensure data integrity.
3. **[HIGH] P1 Backend Gap:** 
   Create backend tests for Event CRUD and the new Epic 5 Preview Testing Thresholds.
4. **[HIGH] E2E Builder Coverage:** 
   Run `/bmad:tea:automate` to create a basic E2E test proving a user can log in, open the builder, and drag a component onto the canvas (Area 6).

---

## Gate Decision

### 🚨 GATE DECISION: FAIL

**Rationale:** P0 coverage is 0% (required: 100%). 2 critical requirements (Form Publishing and Lead Collection) are completely uncovered by both Backend API and E2E tests. Additionally, there is a 100% gap in E2E coverage across the entire platform.

**Gate Criteria Status:**
- P0 Coverage Required: 100% → **Actual: 0%** (NOT MET)
- P1 Coverage Minimum: 80% → **Actual: 0%** (NOT MET)
- Overall Coverage Minimum: 80% → **Actual: 0%** (NOT MET)

🚫 **GATE: FAIL - Release BLOCKED until coverage improves**

Before advancing to Epic 6, the system **must** be stabilized by addressing the P0 Backend and E2E gaps identified above.