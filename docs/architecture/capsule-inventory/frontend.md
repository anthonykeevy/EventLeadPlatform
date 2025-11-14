# Frontend Feature Inventory & Backend Touchpoints

## Purpose
- Establish a current-state map of shipping frontend experiences and the backend modules they depend on.
- Provide raw material for capsule slicing by linking UI, API, logging, and database touchpoints.
- Capture logging/middleware flows so future capsules keep observability intact.

## High-Level Summary
| Frontend Feature (path) | User-Facing Scope | Primary API Endpoints | Backend Modules / Routers | Logging & Middleware | Key DB Entities |
| --- | --- | --- | --- | --- | --- |
| `features/auth` | Signup, login, refresh, password reset, email verification flows | `/api/auth/signup`, `/api/auth/login`, `/api/auth/refresh`, `/api/auth/password-reset/*`, `/api/auth/me` | `modules.auth.router`, `modules.auth.token_service`, `modules.auth.user_service` | `middleware.auth.JWTAuthMiddleware`, `common.auth_event_decorator.log_auth_attempts`, request logger stack | `dbo.User`, `dbo.UserRefreshToken`, `dbo.UserEmailVerificationToken`, `dbo.UserPasswordResetToken`, `log.AuthEvent`, `log.ApplicationError` |
| `features/invitations` | Invitation acceptance landing and activation | `/api/invitations/{token}`, `/api/auth/signup` (invitation flow), `/api/users/me/companies` | `modules.invitations.router`, `modules.auth.router`, `modules.users.router` | JWT middleware (protected for follow-up calls), invitation acceptance events logged via auth decorator | `dbo.UserInvitation`, `dbo.UserCompany`, `ref.UserCompanyRole`, `dbo.User` |
| `features/dashboard` | Company dashboards, KPI cards, team panel, company switcher | `/api/users/me/companies`, `/api/dashboard/kpis`, `/api/companies/{id}/users`, `/api/users/me/switch-company`, `/api/companies/{id}/events` | `modules.users.router`, `modules.dashboard.router`, `modules.companies.router`, `modules.events.router` | Request + enhanced logger middleware, JWT middleware, audit hooks inside service layer | `dbo.UserCompany`, `dbo.Company`, `dbo.Event`, `ref.EventStatus`, `ref.UserCompanyRole`, derived KPI views |
| `features/events` | Event discovery, CRUD, review workflow, smart field inference | `/api/events`, `/api/events/{id}`, `/api/events/search`, `/api/events/reference/*`, `/api/events/inference/*`, `/api/events/{id}/participate`, `/api/events/public/search` | `modules.events.router`, `modules.events.service`, `modules.events.reference_router` | JWT middleware, enhanced request logger, event audit hooks in service layer | `dbo.Event`, `dbo.EventCompany`, `ref.EventType`, `ref.EventStatus`, `ref.PublicReviewStatus`, `dbo.Company` |
| `features/companies` | ABR smart search, company selection widgets | `/api/companies/smart-search` | `modules.companies.router` (smart search + caching), `modules.companies.abr_service` | Public endpoint exempted in JWT middleware; results logged via request logger | `cache.ABRSearch` (lookup cache), external ABR integration metadata |
| `features/onboarding` | Onboarding modal & progressive checklist | `/api/users/me`, `/api/users/me/details`, `/api/users/me/companies` | `modules.users.router`, `modules.auth.router` for profile completion state | JWT middleware, audit logging for profile updates | `dbo.User`, `dbo.UserCompany`, `audit.User` |
| `features/profile` & `features/preferences` | Profile editor, preferences (theme, industry), account settings | `/api/users/me`, `/api/users/me/details`, `/api/users/me/preferences`, `/api/users/industries/*`, `/api/users/reference/*` | `modules.users.router`, `modules.users.service`, reference data routers (`modules.countries`, `modules.config`) | JWT middleware, request logger, audit tables via service layer | `dbo.User`, `dbo.UserIndustry`, `ref.ThemePreference`, `ref.LayoutDensity`, `ref.FontSize`, `ref.Country`, `ref.Industry`, `audit.User` |
| `features/admin` | Admin dashboard skeleton: company review queue, event reviews | `/api/admin/dashboard`, `/api/admin/review/*`, `/api/companies/{id}/users` | `modules.admin.router`, `modules.audit.router`, `modules.companies.router` | JWT middleware, admin audit logs | `dbo.Company`, `audit.Company`, `audit.ActivityLog`, `log.AuthEvent` |
| Shared libs (`lib/auth`, `components/AuthLayout`, `ConfigProvider`) | Auth context, token storage, global settings | `/api/auth/refresh`, `/api/auth/me`, `/api/config/*` | `modules.auth.router`, `modules.config.router`, config services | JWT middleware, request context instrumentation | `dbo.UserRefreshToken`, `config.AppSetting` |

## Feature Notes

### Authentication (`frontend/src/features/auth`)
- **UI/Flows:** Signup, login, password reset, email verification, AuthContext.
- **Backend Dependence:** FastAPI `modules.auth.router` handles all primary endpoints; `modules.users.router` supplements current-user fetch. Token lifecycle via `modules.auth.token_service`, `modules.auth.jwt_service`.
- **Logging:** `common.auth_event_decorator.log_auth_attempts` captures success/failure into `log.AuthEvent`; request pipeline instrumented by `middleware.auth.JWTAuthMiddleware` and enhanced request loggers (`middleware.request_logger`, `middleware.enhanced_request_logger`).
- **Data:** Relies on `dbo.User`, associated token tables (`dbo.UserRefreshToken`, `dbo.UserEmailVerificationToken`, `dbo.UserPasswordResetToken`), and audit/log schemas (`log.AuthEvent`, `log.ApplicationError`).

### Invitations (`frontend/src/features/invitations`)
- **UI/Flows:** Invitation acceptance page, verifies token, completes signup.
- **Backend Dependence:** `modules.invitations.router` serves invitation lookup/validation; final signup uses `modules.auth.router` invitation flow; post-accept redirect pulls `/api/users/me/companies` from `modules.users.router`.
- **Logging:** Invitation success/failure funneled through auth decorator, enabling capsule awareness via `log.AuthEvent`. JWT middleware bypass for invite lookup, enforced for subsequent authenticated calls.
- **Data:** Works with `dbo.UserInvitation`, `dbo.UserCompany`, and `ref.UserCompanyRole`.

### Dashboard (`frontend/src/features/dashboard`)
- **UI/Flows:** Company hierarchy view, KPI cards, team management modal, company switcher, event lists.
- **Backend Dependence:** `modules.users.router` (`/api/users/me/companies`, `/api/users/me/switch-company`), `modules.dashboard.router` (`/api/dashboard/kpis`), `modules.companies.router` (`/api/companies/{id}/users`), `modules.events.router` (`/api/companies/{id}/events`).
- **Logging:** Protected by JWT middleware. Actions logged through enhanced request logger and service-level audit (e.g., company switch via `modules.users.switch_service`, writing to `audit.ActivityLog` and `log.AuthEvent`).
- **Data:** `dbo.UserCompany`, `dbo.Company`, `dbo.Event`, reference tables for statuses/roles.

### Events (`frontend/src/features/events`)
- **UI/Flows:** Event catalog, filters, create/edit modals, review workflow, smart inference helper functions.
- **Backend Dependence:** `modules.events.router` (CRUD, search, participation), reference router for event status/type data, inference endpoints, and public search route.
- **Logging:** JWT middleware validates tokens; request logger + event-specific audit hooks capture changes (written to `audit.ActivityLog`, potential `log.IntegrationEvent`).
- **Data:** `dbo.Event`, `dbo.EventCompany`, `ref.EventType`, `ref.EventStatus`, `ref.PublicReviewStatus`, and associated company metrics.

### Companies (`frontend/src/features/companies`)
- **UI/Flows:** Smart company search with ABR integration, selection widgets for onboarding/event flows.
- **Backend Dependence:** `modules.companies.router` smart-search endpoint with caching via ABR service.
- **Logging:** Path is whitelisted in JWT middleware as public; still traverses enhanced request logger for trace IDs.
- **Data:** `cache.ABRSearch` for cached hits; reference to `dbo.Company` for enrichments.

### Onboarding (`frontend/src/features/onboarding`)
- **UI/Flows:** Modal-based walkthrough, tracks onboarding steps.
- **Backend Dependence:** `/api/users/me` and `/api/users/me/details` from `modules.users.router`; may trigger auth module for verification state.
- **Logging:** JWT middleware + audit trail for user detail updates (`audit.User`).
- **Data:** `dbo.User` onboarding fields, `audit.User` for change log.

### Profile & Preferences (`frontend/src/features/profile`, `frontend/src/features/preferences`)
- **UI/Flows:** Profile editor, theme selection, industry associations, account settings popup.
- **Backend Dependence:** `modules.users.router` (profile update, industries), `modules.countries.router`, `modules.config.router`/`modules.users.reference` for dropdown references.
- **Logging:** Protected by JWT middleware; updates logged to `audit.User`, `audit.ActivityLog`.
- **Data:** `dbo.User`, `dbo.UserIndustry`, reference tables (`ref.ThemePreference`, `ref.LayoutDensity`, `ref.FontSize`, `ref.Country`, `ref.Industry`).

### Admin (`frontend/src/features/admin`)
- **UI/Flows:** Administrative dashboard placeholders (company review, event review history).
- **Backend Dependence:** `modules.admin.router` for dashboard metrics and review actions; reuses `modules.companies` and `modules.events`.
- **Logging:** Admin actions funnel into audit + request logging stacks; RBAC enforced via JWT + `common.rbac`.
- **Data:** `audit.Company`, `audit.ActivityLog`, plus shared event/company tables.

### Shared Libraries & Middleware Awareness
- `frontend/src/lib/auth.ts`, `frontend/src/features/auth/context/AuthContext.tsx` manage token storage and refresh, aligning with backend JWT middleware expectations.
- Backend middleware stack (`middleware/auth.JWTAuthMiddleware`, `middleware/enhanced_request_logger`, `middleware.exception_handler`) ensures every capsule can tap into consistent context (`common.request_context`, `common.logger`).
- Event logging relies on `common.auth_event_decorator` and `log.AuthEvent`, forming the backbone for future `auth-audit-anomaly` capsule.

---

**Next Steps:** Produce complementary backend inventory summarizing module responsibilities, then cross-reference with this frontend view and the existing `docs/database-schema.md` to define final capsule boundaries.

