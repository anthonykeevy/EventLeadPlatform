# Epic 1: Story-to-Journey Component Mapping

**Date:** 2025-10-16  
**Purpose:** Visual mapping of how each story enables specific user journey components  
**Status:** Ready for Implementation

---

## 🗺️ Visual Journey Mapping

### **Legend:**
- 🔴 **Core Journey Step** (Blocks all downstream steps)
- 🟡 **Enhancement** (Improves UX but not blocking)
- 🟢 **Polish** (Nice-to-have, enhances quality)

---

## Journey 1: New User Onboarding (First Company Creator)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      JOURNEY 1: NEW USER ONBOARDING                         │
│                    (Priority 1 - Core Platform Value)                       │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: SIGNUP
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Enter email + password → Submit                    │
│ Expected: Account created, verification email sent              │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.1 (Signup API, Email Verification) 🔴         │
│ FRONTEND: Story 1.9 (Signup Page, Form Validation)  🔴          │
│ SUPPORT:  Story 1.13 (Config Service for validation rules) 🔴   │
└──────────────────────────────────────────────────────────────────┘

STEP 2: EMAIL VERIFICATION
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Click verification link in email                   │
│ Expected: Email verified, redirected to login                   │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.1 (Verification token validation) 🔴          │
│ FRONTEND: Story 1.9 (Verification confirmation page) 🔴         │
└──────────────────────────────────────────────────────────────────┘

STEP 3: LOGIN
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Enter email + password → Submit                    │
│ Expected: Authenticated, JWT issued, onboarding check           │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.2 (Login API, JWT tokens, Refresh) 🔴         │
│ FRONTEND: Story 1.9 (Login Page, Auth Context) 🔴               │
│ SUPPORT:  Story 1.3 (RBAC Middleware for authorization) 🔴      │
└──────────────────────────────────────────────────────────────────┘

STEP 4: ONBOARDING - USER DETAILS (Step 1 of Wizard)
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Enter first/last name, phone, role                 │
│ Expected: Real-time validation, auto-save, progress indicator   │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.5 (Onboarding API, User Details) 🔴           │
│           Story 1.12 (Phone validation engine) 🔴               │
│           Story 1.13 (Config for validation rules) 🔴           │
│ FRONTEND: Story 1.14 (Onboarding Wizard, Step 1) 🔴             │
│           Story 1.17 (Auto-save, Progress bar) 🟡               │
└──────────────────────────────────────────────────────────────────┘

STEP 5: ONBOARDING - COMPANY SEARCH (Step 2 of Wizard)
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Search ABN/ACN/Name → Select company               │
│ Expected: Smart auto-detect, 90% success, cached results        │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.10 (Enhanced ABR Search, Caching) 🔴          │
│           Story 1.13 (Config for ABR API credentials) 🔴        │
│ FRONTEND: Story 1.14 (Search component, Results) 🔴             │
│           Story 1.17 (Loading states, Animations) 🟡            │
└──────────────────────────────────────────────────────────────────┘

STEP 6: ONBOARDING - COMPANY DETAILS (Step 2 cont.)
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Manual entry OR auto-fill from ABR → Submit        │
│ Expected: Company created, billing address validated            │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.5 (Company creation, Address validation) 🔴   │
│           Story 1.12 (Address validation engine) 🔴             │
│ FRONTEND: Story 1.14 (Company form, Validation) 🔴              │
│           Story 1.17 (Success animations, Transitions) 🟡       │
└──────────────────────────────────────────────────────────────────┘

STEP 7: DASHBOARD ACCESS
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Submit onboarding → Redirect to dashboard          │
│ Expected: Onboarding complete, role = Company Admin             │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.5 (Onboarding completion API) 🔴              │
│           Story 1.3 (RBAC assigns Company Admin role) 🔴        │
│ FRONTEND: Story 1.9 (Protected route guards) 🔴                 │
│           Story 1.14 (Redirect logic) 🔴                         │
└──────────────────────────────────────────────────────────────────┘

🎯 JOURNEY 1 SUCCESS CRITERIA:
- ✅ <5 minutes from signup to dashboard
- ✅ >85% onboarding completion rate
- ✅ >90% company search success rate
- ✅ Zero data loss (auto-save prevents abandonment)
```

---

## Journey 2: Invited User Onboarding (Team Member)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   JOURNEY 2: INVITED USER ONBOARDING                        │
│                    (Priority 2 - Team Collaboration)                        │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: ADMIN SENDS INVITATION
┌──────────────────────────────────────────────────────────────────┐
│ Admin Action: Enter email, name, role → Send invitation         │
│ Expected: Invitation created, email sent to invitee             │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.6 (Invitation API, Email service) 🔴          │
│ FRONTEND: Story 1.16 (Invite modal, Validation) 🔴              │
└──────────────────────────────────────────────────────────────────┘

STEP 2: USER RECEIVES & VIEWS INVITATION
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Click invitation link in email                     │
│ Expected: See company name, role, inviter, understand context   │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.6 (Invitation details API) 🔴                 │
│ FRONTEND: Story 1.16 (Invitation preview page) 🔴               │
└──────────────────────────────────────────────────────────────────┘

STEP 3: USER ACCEPTS INVITATION
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Enter password (email/name pre-filled) → Accept    │
│ Expected: Account created, user-company relationship created    │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.7 (Acceptance API, Account creation) 🔴       │
│           Story 1.11 (User-Company relationship) 🔴             │
│ FRONTEND: Story 1.16 (Acceptance form, Validation) 🔴           │
└──────────────────────────────────────────────────────────────────┘

STEP 4: SIMPLIFIED ONBOARDING (User Details Only)
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Complete user details (no company setup)           │
│ Expected: Onboarding complete, joined team                      │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.5 (User details API, Skip company) 🔴         │
│ FRONTEND: Story 1.14 (Onboarding Step 1 only) 🔴                │
└──────────────────────────────────────────────────────────────────┘

STEP 5: DASHBOARD ACCESS
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Submit onboarding → Redirect to dashboard          │
│ Expected: Access company data, role permissions applied         │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.3 (RBAC enforces role permissions) 🔴         │
│ FRONTEND: Story 1.9 (Protected routes) 🔴                       │
└──────────────────────────────────────────────────────────────────┘

🎯 JOURNEY 2 SUCCESS CRITERIA:
- ✅ <3 minutes from email to dashboard
- ✅ >90% invitation acceptance rate
- ✅ No confusion about which company they're joining
```

---

## Journey 3: Password Reset (Forgotten Password)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      JOURNEY 3: PASSWORD RESET                              │
│                    (Priority 3 - Account Recovery)                          │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: REQUEST PASSWORD RESET
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Click "Forgot password?" → Enter email → Submit    │
│ Expected: Reset email sent (or silent fail for security)        │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.4 (Reset request API, Email) 🔴               │
│ FRONTEND: Story 1.15 (Request page, Validation) 🔴              │
└──────────────────────────────────────────────────────────────────┘

STEP 2: VERIFY & RESET PASSWORD
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Click reset link → Enter new password → Submit     │
│ Expected: Password changed, redirect to login                   │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.4 (Token validation, Password update) 🔴      │
│ FRONTEND: Story 1.15 (Reset page, Password strength) 🔴         │
└──────────────────────────────────────────────────────────────────┘

STEP 3: LOGIN WITH NEW PASSWORD
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Enter email + new password → Submit                │
│ Expected: Login successful, account recovered                   │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.2 (Login API) 🔴 (Already built)              │
│ FRONTEND: Story 1.9 (Login page) 🔴 (Already built)             │
└──────────────────────────────────────────────────────────────────┘

🎯 JOURNEY 3 SUCCESS CRITERIA:
- ✅ <2 minutes from request to login
- ✅ >95% reset completion rate
- ✅ Clear security messaging (not alarming)
```

---

## Journey 4: Multi-Company User (Branch/Freelancer)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   JOURNEY 4: MULTI-COMPANY USER                             │
│                    (Priority 4 - Advanced Feature)                          │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: JOIN SECOND COMPANY
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Accept invitation to Company B (already in A)      │
│ Expected: Second user-company relationship created              │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.7 (Accepts second invitation) 🔴              │
│           Story 1.11 (Multiple relationships support) 🔴        │
│ FRONTEND: Story 1.16 (Invitation acceptance) 🔴                 │
└──────────────────────────────────────────────────────────────────┘

STEP 2: VERIFY COMPANY SWITCHER VISIBLE
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Log in → See both companies in header              │
│ Expected: Company switcher shows Company A (active) & Company B │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.11 (List user's companies API) 🔴             │
│ FRONTEND: Story 1.16 (Company switcher dropdown) 🔴             │
└──────────────────────────────────────────────────────────────────┘

STEP 3: SWITCH TO COMPANY B
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Click Company B in switcher                        │
│ Expected: Context switches, only Company B data visible         │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.11 (Company switch API, Session update) 🔴    │
│           Story 1.3 (RBAC filters by active company) 🔴         │
│ FRONTEND: Story 1.16 (Switcher, Context update) 🔴              │
│           Story 1.17 (Smooth transition animation) 🟡           │
└──────────────────────────────────────────────────────────────────┘

STEP 4: VERIFY DATA ISOLATION
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Browse forms, events, leads                        │
│ Expected: ONLY Company B data visible, NO Company A data        │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.8 (Multi-tenancy tests, 100% isolation) 🔴    │
│           Story 1.3 (RBAC enforces company_id filter) 🔴        │
│ FRONTEND: Story 1.16 (UI reflects active company only) 🔴       │
└──────────────────────────────────────────────────────────────────┘

STEP 5: SWITCH BACK TO COMPANY A
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Click Company A in switcher                        │
│ Expected: Context switches, only Company A data visible         │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.11 (Company switch API) 🔴                    │
│ FRONTEND: Story 1.16 (Switcher, Context update) 🔴              │
└──────────────────────────────────────────────────────────────────┘

🎯 JOURNEY 4 SUCCESS CRITERIA:
- ✅ <3 seconds to switch companies
- ✅ 100% data isolation (CRITICAL SECURITY)
- ✅ 0% confusion about active company
- ✅ Relationship context visible (Branch, Head Office)
```

---

## Journey 5: Returning User (Login)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      JOURNEY 5: RETURNING USER                              │
│                    (Covered by Journey 1 Implementation)                    │
└─────────────────────────────────────────────────────────────────────────────┘

STEP 1: LOGIN
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Enter email + password → Submit                    │
│ Expected: Authenticated, redirect to dashboard (<3 seconds)     │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.2 (Login API, JWT) 🔴 (Already built)         │
│ FRONTEND: Story 1.9 (Login page) 🔴 (Already built)             │
└──────────────────────────────────────────────────────────────────┘

STEP 2: DASHBOARD ACCESS
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Dashboard loads                                    │
│ Expected: Fast load, personalized welcome                       │
├──────────────────────────────────────────────────────────────────┤
│ BACKEND:  Story 1.3 (RBAC loads permissions) 🔴                 │
│ FRONTEND: Story 1.9 (Protected routes) 🔴                       │
└──────────────────────────────────────────────────────────────────┘

🎯 JOURNEY 5 SUCCESS CRITERIA:
- ✅ <3 seconds from submit to dashboard
- ✅ JWT refresh transparent (no re-login)
```

---

## 📊 Story Dependency Matrix

| Story | Journey 1 | Journey 2 | Journey 3 | Journey 4 | Journey 5 |
|-------|-----------|-----------|-----------|-----------|-----------|
| **0.1** | ✅ (Foundation) | ✅ | ✅ | ✅ | ✅ |
| **1.1** | 🔴 Steps 1-2 | - | - | - | - |
| **1.2** | 🔴 Step 3 | - | 🔴 Step 3 | - | 🔴 Step 1 |
| **1.3** | 🔴 Steps 3,7 | 🔴 Step 5 | - | 🔴 Steps 3-4 | 🔴 Step 2 |
| **1.4** | - | - | 🔴 Steps 1-2 | - | - |
| **1.5** | 🔴 Steps 4,6-7 | 🔴 Step 4 | - | - | - |
| **1.6** | - | 🔴 Step 1 | - | - | - |
| **1.7** | - | 🔴 Step 3 | - | 🔴 Step 1 | - |
| **1.8** | - | - | - | 🔴 Step 4 | - |
| **1.9** | 🔴 Steps 1-3,7 | 🔴 Step 5 | 🔴 Step 3 | - | 🔴 Steps 1-2 |
| **1.10** | 🔴 Step 5 | - | - | - | - |
| **1.11** | - | - | - | 🔴 Steps 1-5 | - |
| **1.12** | 🔴 Steps 4,6 | - | - | - | - |
| **1.13** | 🔴 Steps 1,4-5 | - | - | - | - |
| **1.14** | 🔴 Steps 4-7 | 🔴 Step 4 | - | - | - |
| **1.15** | - | - | 🔴 Steps 1-2 | - | - |
| **1.16** | - | 🔴 Steps 1-3,5 | - | 🔴 Steps 1-5 | - |
| **1.17** | 🟡 All steps | 🟡 All steps | 🟡 All steps | 🟡 Step 3 | 🟡 All steps |

**Legend:**
- 🔴 **Core Dependency** (Journey step cannot function without this story)
- 🟡 **Enhancement** (Improves UX but journey works without it)
- `-` **Not Required** (Story not needed for this journey)

---

## 🎯 Backend vs Frontend Story Classification

### **Backend Stories (Build First):**

| Story | Description | User Journey Impact |
|-------|-------------|---------------------|
| **1.1** | Signup & Email Verification API | Enables Journey 1 Steps 1-2 |
| **1.2** | Login & JWT Tokens | Enables Journey 1 Step 3, Journey 3 Step 3, Journey 5 Step 1 |
| **1.3** | RBAC Middleware | Enables authorization across all journeys |
| **1.4** | Password Reset API | Enables Journey 3 Steps 1-2 |
| **1.5** | Onboarding API | Enables Journey 1 Steps 4,6-7, Journey 2 Step 4 |
| **1.6** | Team Invitation API | Enables Journey 2 Step 1 |
| **1.7** | Invitation Acceptance API | Enables Journey 2 Step 3, Journey 4 Step 1 |
| **1.8** | Multi-Tenancy Testing | Validates Journey 4 Step 4 (100% data isolation) |
| **1.10** | Enhanced ABR Search | Enables Journey 1 Step 5 (90% search success) |
| **1.11** | Company Switching | Enables Journey 4 Steps 1-5 |
| **1.12** | Validation Engine | Enables Journey 1 Steps 4,6 (phone/address validation) |
| **1.13** | Configuration Service | Enables Journey 1 Steps 1,4-5 (dynamic rules) |

---

### **Frontend Stories (Build Second):**

| Story | Description | User Journey Impact |
|-------|-------------|---------------------|
| **1.9** | Authentication Pages | Delivers Journey 1 Steps 1-3,7, Journey 5 |
| **1.14** | Onboarding Wizard | Delivers Journey 1 Steps 4-7, Journey 2 Step 4 |
| **1.15** | Password Reset Pages | Delivers Journey 3 Steps 1-2 |
| **1.16** | Team Management UI | Delivers Journey 2, Journey 4 |
| **1.17** | UX Enhancement & Polish | Improves all journeys (animations, accessibility) |

---

## ✅ Implementation Sequence (Backend → Frontend → Journey)

### **Wave 1: Journey 1 - Core Onboarding**

**Sprint 1-2: Backend Foundation (Weeks 1-2)**
```
Story 1.1 → Story 1.2 → Story 1.3
↓
USER VALIDATION: Can test authentication via Postman
```

**Sprint 3: Backend Services (Week 3)**
```
Story 1.12 → Story 1.13
↓
USER VALIDATION: Can test validation/config via API
```

**Sprint 4: Backend Onboarding (Week 4)**
```
Story 1.10 → Story 1.5
↓
USER VALIDATION: Can test complete onboarding flow via API
```

**Sprint 5: Frontend Auth (Week 5)**
```
Story 1.9 (consumes Stories 1.1, 1.2, 1.3)
↓
USER VALIDATION: ✅ Users can sign up, verify, login via UI!
```

**Sprint 6: Frontend Onboarding (Week 6)**
```
Story 1.14 (consumes Stories 1.5, 1.10, 1.12, 1.13)
↓
USER VALIDATION: ✅ JOURNEY 1 COMPLETE! Users can onboard end-to-end!
UAT CHECKPOINT: Run Journey 1 UAT scenarios
```

---

### **Wave 2: Journey 3 - Password Reset**

**Sprint 7: Backend + Frontend (Week 7)**
```
Story 1.4 (Backend) → Story 1.15 (Frontend)
↓
USER VALIDATION: ✅ JOURNEY 3 COMPLETE! Users can reset passwords!
UAT CHECKPOINT: Run Journey 3 UAT scenarios
```

---

### **Wave 3: Journey 2 & 4 - Team Collaboration**

**Sprint 8: Backend Invitations (Week 8)**
```
Story 1.6 → Story 1.7
↓
USER VALIDATION: Can test invitation flow via API
```

**Sprint 9: Backend Multi-Company (Week 9)**
```
Story 1.11
↓
USER VALIDATION: Can test company switching via API
```

**Sprint 10: Frontend Team UI (Week 10)**
```
Story 1.16 (consumes Stories 1.6, 1.7, 1.11)
↓
USER VALIDATION: ✅ JOURNEYS 2 & 4 COMPLETE! Teams work, multi-company works!
UAT CHECKPOINT: Run Journey 2 & 4 UAT scenarios
```

---

### **Wave 4: Testing & Polish**

**Sprint 11: Security Testing (Week 11)**
```
Story 1.8 (Multi-tenancy security tests)
↓
USER VALIDATION: 100% data isolation verified, security audit complete
```

**Sprint 12: UX Polish (Week 12)**
```
Story 1.17 (UX enhancements across all journeys)
↓
USER VALIDATION: ✅ EPIC 1 COMPLETE! Professional, polished, accessible!
UAT CHECKPOINT: Run all UAT scenarios, validate success criteria
```

---

## 🎯 Key Insight: Every Backend Story Serves a User Journey Step

**No "technical debt" stories - Every story delivers user value:**

- Story 1.1 → User can **create an account**
- Story 1.2 → User can **log in**
- Story 1.3 → User has **proper permissions**
- Story 1.4 → User can **recover account**
- Story 1.5 → User can **complete onboarding**
- Story 1.6 → Admin can **invite team**
- Story 1.7 → User can **join team**
- Story 1.8 → User's data is **secure**
- Story 1.9 → User has **auth UI**
- Story 1.10 → User can **find company easily**
- Story 1.11 → User can **work with multiple companies**
- Story 1.12 → User gets **accurate validation**
- Story 1.13 → Rules can **change without code deploy**
- Story 1.14 → User has **smooth onboarding UI**
- Story 1.15 → User has **password reset UI**
- Story 1.16 → User has **team management UI**
- Story 1.17 → User has **polished experience**

---

**Prepared by:** Sarah (Product Owner)  
**Date:** 2025-10-16  
**Status:** Ready for Implementation

