# Epic 1: Authentication & Onboarding - Complete Story Breakdown

**Epic Status:** Ready for Implementation  
**Stories Created:** 11 (0.1-0.3 ✅ Completed, 1.1-1.8 Ready)  
**Generated:** 2025-10-16

---

## 📊 Story Pipeline Overview

### **Phase 1: Infrastructure & Foundation** ✅ COMPLETE

| Story | Title | Status | Lines | Completed By |
|-------|-------|--------|-------|--------------|
| **0.1** | Database Models & Core Infrastructure | ✅ Approved | 324 | Amelia |
| **0.2** | Automated Logging Infrastructure | ✅ Approved | 556 | Amelia |
| **0.3** | Email Service Foundation | ✅ Approved | 895 | Amelia |

**Phase 1 Summary:**
- ✅ 33 SQLAlchemy models (45 database tables)
- ✅ Request logging middleware
- ✅ Global exception handler
- ✅ Email service with MailHog and SMTP providers
- ✅ Email templates with responsive design
- ✅ All dependencies committed to git

---

### **Phase 2: Authentication & Authorization** 📝 READY

| Story | Title | Status | Lines | AC Count | Tasks |
|-------|-------|--------|-------|----------|-------|
| **1.1** | User Signup & Email Verification | Ready | ~600 | 10 | 13 |
| **1.2** | Login & JWT Tokens | Ready | ~550 | 10 | 13 |
| **1.3** | RBAC Middleware & Authorization | Ready | ~650 | 10 | 13 |

**Phase 2 Deliverables:**
- Public signup endpoint with email verification
- Password strength validation (8+ chars, uppercase, lowercase, number, special char)
- Email verification tokens (24-hour expiry)
- Login endpoint with JWT tokens
- Access tokens (1-hour expiry) + refresh tokens (7-day expiry)
- JWT authentication middleware
- Role-based authorization decorators (`@require_role`)
- Multi-tenant company context
- Protected endpoint patterns

**Key Features:**
- Bcrypt password hashing
- Cryptographically secure tokens
- Automatic email sending (verification emails)
- JWT payload includes: user_id, email, role, company_id
- Request context integration for logging

---

### **Phase 3: Protected Endpoints - Onboarding & Team** 📝 READY

| Story | Title | Status | Lines | AC Count | Tasks |
|-------|-------|--------|-------|----------|-------|
| **1.4** | Password Reset Flow | Ready | ~350 | 10 | 9 |
| **1.5** | First-Time User Onboarding | Ready | ~380 | 10 | 7 |
| **1.6** | Team Invitation System | Ready | ~420 | 10 | 10 |
| **1.7** | Invited User Acceptance & Onboarding | Ready | ~450 | 10 | 8 |

**Phase 3 Deliverables:**
- Password reset request + confirmation endpoints
- Password reset tokens (1-hour expiry)
- User profile completion (phone, timezone)
- Company creation endpoint
- UserCompany relationship with role assignment
- Team invitation system (company_admin only)
- Invitation tokens (7-day expiry)
- Invitation acceptance flow
- Multi-company support (users can belong to multiple companies)
- Company switching functionality

**User Flows:**
1. **Password Reset:** Request → Email → Token validation → New password
2. **Onboarding:** Signup → Verify → Complete profile → Create company → Become admin
3. **Team Invitation:** Admin invites → Email sent → Invitee accepts → Joins company
4. **Multi-Company:** User can belong to multiple companies and switch between them

---

### **Phase 4: Multi-Tenancy** 📝 READY

| Story | Title | Status | Lines | AC Count | Tasks |
|-------|-------|--------|-------|----------|-------|
| **1.8** | Multi-Tenant Data Isolation & Testing | Ready | ~500 | 10 | 10 |

**Phase 4 Deliverables:**
- Multi-tenant query helpers
- Company filtering on all company-scoped endpoints
- Comprehensive data isolation tests
- Role-based access control tests
- Security tests (JWT forgery, role escalation attempts)
- Performance tests (query overhead)
- Cross-company access logging
- Multi-tenant testing utilities

**Security Features:**
- Automatic company_id filtering from JWT
- Users cannot access other companies' data
- Role requirements enforced on all endpoints
- Failed access attempts logged
- Database constraints prevent data leaks

---

## 🎯 Implementation Sequence (Correct Order)

### **Critical Dependency Chain:**

```
Story 0.1 (Database Models)
    ↓
Story 0.2 (Logging Infrastructure) + Story 0.3 (Email Service)
    ↓
Story 1.1 (User Signup & Email Verification)
    ↓
Story 1.2 (Login & JWT Tokens)
    ↓
Story 1.3 (RBAC Middleware) ← MUST BE DONE BEFORE ANY PROTECTED ENDPOINTS
    ↓
Story 1.4 (Password Reset) ← Public endpoints, no RBAC needed
    ↓
Story 1.5 (First-Time Onboarding) ← Requires RBAC (protected endpoints)
    ↓
Story 1.6 (Team Invitation System) ← Requires RBAC (company_admin role check)
    ↓
Story 1.7 (Invited User Acceptance) ← Depends on Story 1.6
    ↓
Story 1.8 (Multi-Tenant Testing) ← Tests all previous stories
```

**Why Story 1.3 (RBAC) Comes Before Stories 1.5-1.7:**
- Story 1.5 (Onboarding) needs authentication for protected endpoints
- Story 1.6 (Invitations) needs `company_admin` role enforcement
- Story 1.7 (Acceptance) needs multi-company context
- Story 1.3 MUST be complete before any role-based protected endpoints

---

## 📋 Story Details Summary

### **Story 1.1: User Signup & Email Verification**

**Endpoints:**
- `POST /api/auth/signup` (public)
- `POST /api/auth/verify-email` (public)

**Key Features:**
- Email uniqueness validation
- Password strength validation (8+ chars, complexity)
- Bcrypt password hashing (cost factor 12)
- User created with EmailVerified=false, IsActive=false
- Email verification token (24-hour expiry)
- Verification email sent automatically
- Token expiry enforced
- Auth events logged

**Acceptance Criteria:** 10  
**Tasks:** 13  
**Dependencies:** Stories 0.1, 0.2, 0.3

---

### **Story 1.2: Login & JWT Tokens**

**Endpoints:**
- `POST /api/auth/login` (public)
- `POST /api/auth/refresh` (public)

**Key Features:**
- Email + password authentication
- Bcrypt password verification
- Requires EmailVerified=true and IsActive=true
- JWT access token (1-hour expiry)
- JWT refresh token (7-day expiry)
- JWT payload: user_id, email, role (optional), company_id (optional)
- Refresh tokens stored in database
- Token refresh endpoint
- Auth events logged (LOGIN_SUCCESS, LOGIN_FAILED, TOKEN_REFRESH)

**Security:**
- Timing-safe password comparison
- No email existence leakage
- HTTPS required in production

**Acceptance Criteria:** 10  
**Tasks:** 13  
**Dependencies:** Story 1.1

---

### **Story 1.3: RBAC Middleware & Authorization**

**Key Features:**
- JWT authentication middleware
- Token validation (signature, expiry)
- Current user injection (request.state.user)
- Role-based authorization decorator: `@require_role("role_name")`
- Multi-tenant company context
- Public path exclusions
- Error handling (401 for auth, 403 for authorization)
- Request context integration

**Authorization Patterns:**
```python
# Pattern 1: Require authentication only
@router.get("/endpoint")
async def endpoint(current_user: CurrentUser = Depends(get_current_user)):
    pass

# Pattern 2: Require specific role
@router.post("/admin-endpoint")
@require_role("company_admin")
async def admin_endpoint(current_user: CurrentUser = Depends(get_current_user)):
    pass

# Pattern 3: Multiple roles allowed
@router.get("/dashboard")
@require_role(["company_admin", "company_user"])
async def dashboard(current_user: CurrentUser = Depends(get_current_user)):
    pass
```

**Acceptance Criteria:** 10  
**Tasks:** 13  
**Dependencies:** Story 1.2

---

### **Story 1.4: Password Reset Flow**

**Endpoints:**
- `POST /api/auth/password-reset/request` (public)
- `POST /api/auth/password-reset/confirm` (public)

**Key Features:**
- Password reset token (1-hour expiry)
- Reset email sent automatically
- No email existence leakage (security)
- New password validation
- Token single-use enforcement
- Old tokens invalidated when new one generated
- Auth events logged

**Acceptance Criteria:** 10  
**Tasks:** 9  
**Dependencies:** Stories 1.1, 1.2

---

### **Story 1.5: First-Time User Onboarding**

**Endpoints:**
- `POST /api/users/me/details` (protected)
- `POST /api/companies` (protected)

**Key Features:**
- User profile completion (phone, timezone)
- Company creation
- UserCompany relationship with role="company_admin"
- JWT refreshed with role and company_id
- ABN/ACN validation (Australian format)
- Timezone validation
- Cannot create company if already has one
- Audit logging

**Flow:**
```
1. User signs up and verifies email
2. User logs in (JWT has no role/company)
3. User completes profile details
4. User creates company
5. User becomes company_admin
6. New JWT issued with role and company_id
7. User can now access protected company endpoints
```

**Acceptance Criteria:** 10  
**Tasks:** 7  
**Dependencies:** Stories 1.1, 1.2, 1.3

---

### **Story 1.6: Team Invitation System**

**Endpoints:**
- `POST /api/companies/{company_id}/invite` (protected, company_admin)
- `GET /api/companies/{company_id}/invitations` (protected, company_admin)
- `POST /api/companies/{company_id}/invitations/{id}/resend` (protected, company_admin)
- `DELETE /api/companies/{company_id}/invitations/{id}` (protected, company_admin)

**Key Features:**
- Company admin can invite team members
- Invitation with email, role, company
- Invitation token (7-day expiry)
- Team invitation email sent
- Cannot invite existing company member
- Admin can resend invitation
- Admin can cancel invitation
- Admin can view all invitations (with status filtering)
- Audit logging

**Acceptance Criteria:** 10  
**Tasks:** 10  
**Dependencies:** Stories 1.3, 1.5

---

### **Story 1.7: Invited User Acceptance & Onboarding**

**Endpoints:**
- `GET /api/invitations/{token}` (public)
- `POST /api/invitations/{token}/accept` (protected)
- `POST /api/users/me/switch-company` (protected)

**Key Features:**
- View invitation details (company, role, inviter)
- Accept invitation (existing user)
- Signup with invitation (new user)
- UserCompany relationship created with invited role
- JWT refreshed with new role/company
- Multi-company support
- Company switching
- Email verification integration
- Audit logging

**Flows:**
```
Flow 1: Existing User
1. Receive invitation email
2. View invitation details
3. Accept invitation
4. UserCompany created
5. New JWT with updated role/company

Flow 2: New User
1. Receive invitation email
2. Sign up with invitation token
3. Verify email
4. Auto-accept invitation
5. User + UserCompany created together
6. JWT with role and company_id
```

**Acceptance Criteria:** 10  
**Tasks:** 8  
**Dependencies:** Stories 1.6, 1.1, 1.2

---

### **Story 1.8: Multi-Tenant Data Isolation & Testing**

**Key Features:**
- Multi-tenant query helpers
- Company filtering on all queries
- Data isolation tests (User A cannot access Company B's data)
- Role-based access control tests
- Security tests (JWT forgery, role escalation)
- Performance tests (query overhead)
- Cross-company access logging
- Database constraints review

**Testing Utilities:**
```python
# Create multi-tenant test scenarios
create_test_company(db, "Company A")
create_test_user(db, email, company_id, role)
create_test_data(db, company_id)

# Test data isolation
test_user_cannot_access_other_company_data()
test_company_admin_can_invite_company_user_cannot()
test_jwt_forgery_prevented()
```

**Security Checklist:**
- ✅ All company-scoped endpoints filter by company_id
- ✅ Company_id extracted from JWT (not request body)
- ✅ Users cannot forge JWT tokens
- ✅ Users cannot access other companies via direct IDs
- ✅ Role requirements enforced
- ✅ Failed access attempts logged
- ✅ Database foreign keys enforce integrity
- ✅ Indexes support efficient filtering

**Acceptance Criteria:** 10  
**Tasks:** 10  
**Dependencies:** Stories 1.3, 1.5, 1.6, 1.7

---

## 🔧 Technical Stack Summary

**Backend Framework:**
- FastAPI (async/await support)
- Python 3.x

**Database:**
- SQL Server
- SQLAlchemy ORM
- Alembic migrations

**Authentication:**
- JWT tokens (access + refresh)
- PyJWT library
- Bcrypt password hashing (passlib)

**Email:**
- Email service abstraction (provider pattern)
- MailHog (development)
- SMTP (production)
- Jinja2 templates

**Logging:**
- Automatic request logging
- Global exception handler
- Audit tables (audit.*)
- Log tables (log.*)

**Testing:**
- pytest
- FastAPI TestClient
- Database fixtures
- Mock objects

---

## 📁 File Structure Summary

```
backend/
├── common/
│   ├── database.py           # DB connection, session management
│   ├── security.py           # Password hashing, token generation
│   ├── request_context.py    # Request-scoped context
│   ├── log_filters.py        # Sensitive data filtering
│   ├── logger.py             # Structured logging
│   ├── rbac.py               # Role-based authorization
│   ├── multi_tenant.py       # Multi-tenant query helpers
│   └── password_validator.py # Password strength validation
├── middleware/
│   ├── request_logger.py     # API request logging
│   ├── exception_handler.py  # Global exception handler
│   └── auth.py               # JWT authentication middleware
├── config/
│   ├── email.py              # Email configuration
│   └── jwt.py                # JWT configuration
├── modules/
│   ├── auth/
│   │   ├── router.py         # Auth endpoints
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── user_service.py   # User business logic
│   │   ├── token_service.py  # Token generation/validation
│   │   ├── jwt_service.py    # JWT creation/decoding
│   │   ├── audit_service.py  # Auth event logging
│   │   ├── models.py         # CurrentUser model
│   │   └── dependencies.py   # get_current_user dependency
│   ├── users/
│   │   └── router.py         # User profile endpoints
│   └── companies/
│       └── router.py         # Company and invitation endpoints
├── services/
│   ├── email_service.py      # Email service
│   └── email_providers/
│       ├── mailhog.py        # MailHog provider
│       └── smtp.py           # SMTP provider
├── models/
│   ├── user.py               # User model
│   ├── company.py            # Company model
│   ├── user_company.py       # UserCompany relationship
│   ├── ref/                  # Reference tables
│   ├── audit/                # Audit tables
│   └── log/                  # Log tables
├── templates/
│   └── emails/
│       ├── layouts/base.html
│       ├── email_verification.html
│       ├── password_reset.html
│       └── team_invitation.html
└── tests/
    ├── test_auth_signup.py
    ├── test_auth_login.py
    ├── test_auth_verification.py
    ├── test_password_reset.py
    ├── test_onboarding.py
    ├── test_invitations.py
    ├── test_rbac.py
    ├── test_multi_tenancy.py
    └── test_security.py
```

---

## 🚀 Implementation Plan

### **Sprint 1: Authentication Core (Stories 1.1-1.3)**
**Duration:** 1-2 weeks  
**Stories:** 1.1, 1.2, 1.3  
**Deliverables:**
- User signup with email verification
- Login with JWT tokens
- RBAC middleware and authorization

**Critical Path:**
1. Story 1.1 (Signup) → Email verification working
2. Story 1.2 (Login) → JWT tokens working
3. Story 1.3 (RBAC) → Protected endpoints working

---

### **Sprint 2: User Flows (Stories 1.4-1.5)**
**Duration:** 1 week  
**Stories:** 1.4, 1.5  
**Deliverables:**
- Password reset flow
- User onboarding and company creation

---

### **Sprint 3: Team Collaboration (Stories 1.6-1.7)**
**Duration:** 1 week  
**Stories:** 1.6, 1.7  
**Deliverables:**
- Team invitation system
- Invitation acceptance
- Multi-company support

---

### **Sprint 4: Testing & Hardening (Story 1.8)**
**Duration:** 3-5 days  
**Stories:** 1.8  
**Deliverables:**
- Comprehensive test suite
- Data isolation verification
- Security validation
- Performance optimization

---

## ✅ Acceptance Criteria Totals

| Phase | Stories | Total AC | Completed |
|-------|---------|----------|-----------|
| Phase 1 | 0.1-0.3 | 30 | ✅ 30/30 |
| Phase 2 | 1.1-1.3 | 30 | 0/30 |
| Phase 3 | 1.4-1.7 | 40 | 0/40 |
| Phase 4 | 1.8 | 10 | 0/10 |
| **TOTAL** | **11 stories** | **110 AC** | **30/110 (27%)** |

---

## 📊 Progress Tracking

**Completed:**
- ✅ Phase 1 complete (Stories 0.1, 0.2, 0.3)
- ✅ Database models (33 models, 45 tables)
- ✅ Logging infrastructure
- ✅ Email service

**Next Up:**
- 📝 Story 1.1: User Signup & Email Verification
- 📝 Story 1.2: Login & JWT Tokens
- 📝 Story 1.3: RBAC Middleware & Authorization

---

## 🎯 Success Metrics

**Phase 2 Complete When:**
- [ ] Users can signup and verify email
- [ ] Users can login and receive JWT tokens
- [ ] Protected endpoints require authentication
- [ ] Role-based authorization works
- [ ] All tests passing

**Phase 3 Complete When:**
- [ ] Users can reset forgotten passwords
- [ ] Users can complete onboarding
- [ ] Company admins can invite team members
- [ ] Invited users can accept and join
- [ ] Multi-company support works

**Phase 4 Complete When:**
- [ ] Data isolation verified (no cross-company access)
- [ ] All role checks enforced
- [ ] Security tests passing
- [ ] Performance acceptable
- [ ] Ready for production

---

## 📚 Documentation Created

**Story Files:** (11 files)
- `docs/stories/story-0.1.md` ✅
- `docs/stories/story-0.2.md` ✅
- `docs/stories/story-0.3.md` ✅
- `docs/stories/story-1.1.md` ✅
- `docs/stories/story-1.2.md` ✅
- `docs/stories/story-1.3.md` ✅
- `docs/stories/story-1.4.md` ✅
- `docs/stories/story-1.5.md` ✅
- `docs/stories/story-1.6.md` ✅
- `docs/stories/story-1.7.md` ✅
- `docs/stories/story-1.8.md` ✅

**Context Files:** (To be generated as needed)
- `docs/story-context-0.1.xml` ✅
- `docs/story-context-0.2.xml` ✅
- `docs/story-context-0.3.xml` ✅
- `docs/story-context-1.1.xml` - Ready to generate
- `docs/story-context-1.2.xml` - Ready to generate
- `docs/story-context-1.3.xml` - Ready to generate
- `docs/story-context-1.4.xml` - Ready to generate
- `docs/story-context-1.5.xml` - Ready to generate
- `docs/story-context-1.6.xml` - Ready to generate
- `docs/story-context-1.7.xml` - Ready to generate
- `docs/story-context-1.8.xml` - Ready to generate

---

## 🎉 Ready for Implementation!

All stories are fully documented with:
- ✅ Clear acceptance criteria
- ✅ Detailed tasks and subtasks
- ✅ Architecture patterns and code examples
- ✅ Security considerations
- ✅ Testing requirements
- ✅ Dependencies identified
- ✅ Implementation sequence defined

**Amelia (Developer Agent) can now proceed with implementation following the correct sequence!**

---

**Generated by:** Sarah (Product Owner Agent)  
**Date:** 2025-10-16  
**Epic:** Epic 1 - Authentication & Onboarding  
**Status:** Complete Story Breakdown Ready

