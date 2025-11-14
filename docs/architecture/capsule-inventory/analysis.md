# Capsule Inventory Analysis (Current 20% Scope)

## Purpose
- Fuse the frontend and backend inventories with the existing database schema to understand how much of the platform is already implemented.
- Cluster current functionality into candidate vertical capsules that respect FE ⇄ BE ⇄ DB ownership.
- Provide a baseline capsule count for the completed ~20% of the project and highlight gaps for future expansion.

## Method
1. **Frontend Scan:** `frontend/src/features/**` mapped to backend endpoints in `docs/architecture/capsule-inventory/frontend.md`.
2. **Backend Scan:** `backend/modules/**` routers/services mapped to consuming UI in `docs/architecture/capsule-inventory/backend.md`.
3. **Database Reference:** `docs/database-schema.md` establishes entity ownership and cross-module dependencies.
4. **Logging/Middleware Layer:** Considered the shared observability stack (JWT middleware, enhanced request logger, auth event decorator) to ensure each capsule maintains traceability.

## Candidate Capsules (Current Scope)
| Capsule | Vertical Slice Coverage | Frontend Features | Backend Modules / Services | Primary Tables / Schemas | Notes |
| --- | --- | --- | --- | --- | --- |
| **auth-core** | Credential lifecycle, token issuance, password reset, invitation-based signup | `features/auth`, `features/invitations`, shared AuthContext | `modules.auth` (router, token_service, user_service, audit_service), `modules.invitations` | `dbo.User`, `dbo.UserRefreshToken`, `dbo.UserEmailVerificationToken`, `dbo.UserPasswordResetToken`, `dbo.UserInvitation`, `log.AuthEvent`, `log.ApplicationError` | Already instrumented with auth event decorator and JWT middleware; aligns with previously proposed auth capsules (credential-policy + session-store + audit). |
| **user-profile** | Profile management, onboarding steps, preferences, industry links | `features/onboarding`, `features/profile`, `features/preferences`, parts of `features.dashboard` (user header) | `modules.users` (profile endpoints, company switch service), `modules.config` (theme settings), reference data modules (`modules.countries`, `modules.users.reference`) | `dbo.User`, `dbo.UserCompany`, `dbo.UserIndustry`, `ref.ThemePreference`, `ref.LayoutDensity`, `ref.FontSize`, `ref.Country`, `audit.User`, `audit.ActivityLog` | Bridges onboarding and account management; depends on auth capsule for identity context. |
| **company-directory** | Company search, hierarchy, team management | `features/dashboard` (company tree, team panel), `features/companies` | `modules.users` (company list), `modules.companies` (smart search, company users), `modules.dashboard` (KPI aggregation) | `dbo.Company`, `dbo.UserCompany`, `cache.ABRSearch`, `ref.UserCompanyRole`, `ref.CompanyRelationshipType`, `audit.Company` | ABR smart search is public; needs capsule-level governance of caching and external calls. |
| **event-management** | Event catalog, CRUD, review workflow, smart inference | `features/events`, dashboard event lists, admin review panels (partial) | `modules.events` (router + services + reference), `modules.admin` (review endpoints), `modules.analytics` (event metrics) | `dbo.Event`, `dbo.EventCompany`, `ref.EventType`, `ref.EventStatus`, `ref.PublicReviewStatus`, `audit.ActivityLog`, `audit.Role` | Largest slice; integrates with company-directory for participants and dashboard metrics. |
| **admin-oversight** | Administrative dashboards, audit views, approvals | `features/admin` | `modules.admin`, `modules.audit`, `modules.analytics` | `audit.ActivityLog`, `audit.Company`, `log.ApiRequest`, `dbo.Company`, `dbo.Event` | Dependent on other capsules’ data projections; candidates for read-only views and shared reporting. |
| **platform-observability** (shared) | Logging, middleware, diagnostics, email service | Shared UI utilities (`lib/config`, `components/common`) | `middleware/**`, `common.logger`, `common.request_context`, `services.email_service`, `middleware/diagnostic_logs` | `log.ApiRequest`, `log.ApplicationError`, `log.AuthEvent`, `audit.ActivityLog` | Cross-cutting; treat as platform layer with explicit contract to capsules (time/uuid/log primitives, request tracing). |

These capsules represent functionality already implemented (≈20% of planned scope). Additional capsules (e.g., payments, forms, external integrations) will emerge as remaining epics ship.

## Observations
- **Auth depth is highest:** Token storage, audit logging, and invitation flows are all in place, validating the need for the earlier multi-capsule auth architecture.
- **Company & Event domains intertwined:** Dashboard and events share company context. Capsule contracts should expose read-only projections (e.g., `company-directory` publishes “company summary” view consumed by `event-management` and `admin-oversight`).
- **Logging & middleware already unified:** `JWTAuthMiddleware`, enhanced request logger, and auth event decorator are active; capsules must embed these hooks in their contracts to maintain traceability.
- **Database columns still centralized (`dbo.User`):** Future migrations will move auth-specific fields into capsule schemas (`auth_credential`, `auth_session`) but today they live in shared tables.
- **Admin area early stage:** Admin router exists with review endpoints; frontend has scaffolding. Capsule boundaries should keep admin read-only for other domains’ data until platform label authorizes cross-capsule updates.

## Recommended Next Steps
1. **Contract Drafting:** For each capsule above, generate `CONTRACT.md`, `CONTEXT.md`, `RUNBOOK.md`, `TESTS.md` (using the templates defined earlier for auth capsules).
2. **Capsule Guardrails:** Update lint/CI rules to ensure changes stay within capsule paths:
   - `frontend/src/features/<capsule>/**`
   - `backend/modules/<capsule>/**`
   - `database/schemas/<capsule>/**` (future state)
   - `docs/auth/<capsule>/**` (for auth; extend to general `docs/<area>/<capsule>/**`)
3. **Migration Planning:** Prioritize auth-related migrations (move data out of `dbo.User`) followed by company/event projections.
4. **Owner Approval Flow:** Apply the preflight + PLAN.md + `go-ahead:<capsule>` protocol per capsule before code changes.
5. **Capsule Dashboard:** Configure Archon/CI to tag tasks and PRs with capsule metadata for progress tracking.

With this analysis, we can confidently say the current implementation covers **five product capsules** (`auth-core`, `user-profile`, `company-directory`, `event-management`, `admin-oversight`) plus one cross-cutting platform capsule. This anchors the architecture for both ongoing development and the remaining 80% of planned work.

