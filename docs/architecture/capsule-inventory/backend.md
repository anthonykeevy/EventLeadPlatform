# Backend Module Inventory & Cross-Layer Touchpoints

## Purpose
- Document the backend routers/services currently live, the frontend features they support, and the data/logging surfaces they own.
- Provide the mirror view to the frontend inventory so we can derive capsule boundaries with clear FE ⇄ BE ⇄ DB relationships.
- Highlight middleware, logging, and cross-cutting concerns that capsules must respect.

## High-Level Summary
| Backend Module / Router | Core Responsibilities | Primary Endpoints | Consuming Frontend Features | Key DB Tables / Schemas | Logging & Middleware |
| --- | --- | --- | --- | --- | --- |
| `modules.auth.router` | Signup, login, email verification, token refresh, password reset | `/api/auth/*` | `features/auth`, `features/invitations`, shared AuthContext | `dbo.User`, `dbo.UserEmailVerificationToken`, `dbo.UserPasswordResetToken`, `dbo.UserRefreshToken`, `log.AuthEvent`, `log.ApplicationError` | `middleware.auth.JWTAuthMiddleware`, `common.auth_event_decorator.log_auth_attempts`, enhanced request logger, email service |
| `modules.users.router` | User profile, company list, company switch, industries, references | `/api/users/me*`, `/api/users/industries/*`, `/api/users/reference/*` | `features/dashboard`, `features/onboarding`, `features/profile`, `features/preferences`, `features.auth` (current user), `features.admin` | `dbo.User`, `dbo.UserCompany`, `dbo.UserIndustry`, `ref.UserCompanyRole`, `audit.User`, `audit.ActivityLog` | JWT middleware, enhanced request logger, audit trail helpers (`update_user_details`, `CompanySwitchService`) |
| `modules.dashboard.router` | KPI aggregation + dashboard metrics | `/api/dashboard/kpis`, dashboard health checks | `features/dashboard` | Aggregated metrics over `dbo.Event`, `dbo.Company`, cached KPI tables | JWT middleware, enhanced request logger |
| `modules.companies.router` | ABR smart search, company CRUD, company users | `/api/companies/smart-search`, `/api/companies/{id}/users`, `/api/companies` | `features/companies`, `features/dashboard`, `features.events` (relationship fetch), `features.admin` | `dbo.Company`, `dbo.UserCompany`, `cache.ABRSearch`, `ref.CompanyRelationshipType`, `audit.Company` | JWT middleware (except smart-search), request logger; ABR service logs |
| `modules.events.router` (+ `reference_router`, `inference` helpers) | Event CRUD, search, participation, reference data, smart inference | `/api/events`, `/api/events/{id}`, `/api/events/search`, `/api/events/reference/*`, `/api/events/inference/*`, `/api/events/public/*` | `features/events`, `features.dashboard` (lazy load company events), `features.profile` (inference) | `dbo.Event`, `dbo.EventCompany`, `ref.EventType`, `ref.EventStatus`, `ref.PublicReviewStatus`, `audit.ActivityLog` | JWT middleware (public search exempt), enhanced request logger, event audit hooks |
| `modules.invitations.router` | Invitation issuance, acceptance, resend | `/api/invitations/*` | `features.invitations`, `features.auth` (invitation signup) | `dbo.UserInvitation`, `dbo.UserCompany`, `ref.UserCompanyRole`, `log.AuthEvent` | Invitation flows share auth decorator logging + JWT middleware for secure endpoints |
| `modules.admin.router` | Admin dashboards, event/company review queue | `/api/admin/dashboard`, `/api/admin/review/*` | `features.admin` | `audit.ActivityLog`, `audit.Company`, `dbo.Company`, `dbo.Event`, `ref.UserRole` | JWT middleware, RBAC guard via `common.rbac`, enhanced logger |
| `modules.analytics`, `modules.audit` (supporting) | Reporting endpoints, audit exports | `/api/analytics/*`, `/api/audit/*` | Future admin dashboards (partial UI) | `log.*`, `audit.*`, `dbo.Event`, `dbo.Company` | Request logger, specialized audit pipeline |
| Shared services (`common.database`, `common.logger`, `services.email_service`) | DB sessions, logging configuration, email transport | n/a | All | n/a | Provide observability and context for every capsule |
| Middleware stack (`middleware/auth`, `middleware/enhanced_request_logger`, `middleware/exception_handler`) | Authn enforcement, structured logging, exception handling | Applied globally | All frontend features | n/a | Ensures consistent tracing, request IDs, user context |

## Module Notes

### Authentication (`backend/modules/auth`)
- **Routers & Services:** `router.py`, `token_service.py`, `user_service.py`, `jwt_service.py`, `audit_service.py`, plus `dependencies.py`.
- **Frontend Dependents:** `features/auth` (login/signup/forgot password), `features/invitations` (invitation acceptance path), shared `AuthContext`, token refresh utilities in `lib/auth.ts`.
- **Data Ownership:** Writes to `dbo.User`, manages token tables (`dbo.UserRefreshToken`, `dbo.UserEmailVerificationToken`, `dbo.UserPasswordResetToken`), draws password policy from `common.password_validator` and `config.AppSetting`. Logs to `log.AuthEvent`, `log.ApplicationError`.
- **Observability:** Decorated by `common.auth_event_decorator.log_auth_attempts` to auto-log success/failure. Uses email service for verification/reset (templates in `backend/templates`).

### Users (`backend/modules/users`)
- **Scope:** User details, company relationships, switching active company, profile preferences, theme settings, industry associations.
- **Frontend Dependents:** Dashboard (company tree, team panel, company switch), onboarding modal (profile completion), profile/preferences UI, authentication “current user” fetch.
- **Data:** `dbo.User`, `dbo.UserCompany`, `dbo.UserIndustry`, reference tables (`ref.ThemePreference`, `ref.LayoutDensity`, `ref.FontSize`, `ref.Industry`), audit tables (`audit.User`, `audit.ActivityLog`).
- **Flows:** For company lists, collaborates with `modules.companies` to fetch relationships; exposes aggregated responses consumed by dashboard features.

### Dashboard (`backend/modules/dashboard`)
- **Scope:** KPI metrics for companies, team summaries.
- **Frontend Dependents:** Dashboard KPI cards, summary views.
- **Data:** Aggregates from `dbo.Event`, `dbo.Company`, `dbo.EventCompany`, and derived metrics tables; some queries involve multi-tenant filters (company IDs, roles).
- **Observability:** Standard JWT + request logging; metrics ready for eventual capsule integration with `auth-audit-anomaly` for anomaly detection.

### Companies (`backend/modules/companies`)
- **Scope:** Company details, team members, ABR smart search, onboarding helpers.
- **Frontend Dependents:** Smart company search components, dashboard company lists, events module (when linking events to companies), admin review.
- **Data:** `dbo.Company`, `dbo.UserCompany`, `cache.ABRSearch`, reference tables for company relationships and statuses. Smart search caches results to reduce ABR calls.
- **Observability:** Smart search endpoint is public (whitelisted in JWT middleware) but still logs via enhanced request logger. Protected endpoints enforce RBAC and log to audit.

### Events (`backend/modules/events`)
- **Scope:** Full event lifecycle (CRUD, search, review, participation), reference lookups, smart field inference, event metrics.
- **Frontend Dependents:** Events feature (catalog, create/edit), dashboard (company events), admin review panels.
- **Data:** `dbo.Event`, `dbo.EventCompany`, `ref.EventType`, `ref.EventStatus`, `ref.PublicReviewStatus`, `audit.ActivityLog`. Inference endpoints pull from `dbo.Company`, `dbo.User`, reference tables.
- **Observability:** JWT middleware (public search exempt), enhanced request logging, domain-specific audit entries.

### Invitations (`backend/modules/invitations`)
- **Scope:** Manage invitation lifecycle from issuance to acceptance.
- **Frontend Dependents:** Invitation acceptance page, onboarding flows.
- **Data:** `dbo.UserInvitation`, `dbo.UserCompany`, `ref.UserCompanyRole`; integrates with auth module for final account creation.
- **Observability:** Shares `log_auth_attempts` decorator for consistent auth logging; uses email service for invitation emails.

### Admin (`backend/modules/admin`)
- **Scope:** Admin dashboard data, review queues, administrative actions (company/event approvals).
- **Frontend Dependents:** `features/admin` components (review modals, history panels).
- **Data:** Reads/writes `audit.Company`, `audit.ActivityLog`, `dbo.Company`, `dbo.Event`, `ref.UserRole`.
- **Observability:** Enforces RBAC via `common.rbac`. Actions logged to audit tables for compliance tracking.

### Supporting Modules
- **Analytics (`modules.analytics`)**: Early reporting endpoints; not fully wired in frontend yet but ties to future capsules.
- **Audit (`modules.audit`)**: Exposes audit data for admin review; complements `auth-audit-anomaly` concept.
- **Config (`modules.config`)**: Supplies application settings to frontend’s `ConfigProvider`.
- **Countries / Reference modules**: Feed dropdowns and inference logic (countries, timezones, themes, etc.).

### Middleware & Cross-Cutting Concerns
- **JWTAuthMiddleware (`backend/middleware/auth.py`)** enforces authentication, except for explicit public routes (signup, smart search, etc.) and seeds request context with user/company IDs for logging.
- **Enhanced request loggers (`middleware/enhanced_request_logger.py`, `middleware.request_logger.py`)** produce structured logs with trace IDs, integrating with `log.ApiRequest` tables.
- **Exception & diagnostic middleware** capture failures for `log.ApplicationError`.
- **`common.request_context`** ensures each request carries metadata (trace ID, user ID) that future capsules should continue to publish for observability.
- **Email service (`services.email_service`)** centralizes outbound emails for auth, invitations, etc., supporting capsule-specific runbooks.

---

**Next Steps:** Combine this backend inventory with the frontend view (`frontend.md`) and the existing `docs/database-schema.md` to cluster features into vertical capsules and finalize the capsule map, contracts, and guardrails.





