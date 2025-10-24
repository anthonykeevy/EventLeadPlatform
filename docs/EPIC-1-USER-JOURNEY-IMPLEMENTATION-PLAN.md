# Epic 1: User-Journey-Centric Implementation Plan

**Date:** 2025-10-16  
**Prepared by:** Sarah (Product Owner) with Sally (UX Expert)  
**Validated by:** User Experience Analysis  
**Status:** Ready for Review by Anthony

---

## 🎯 Philosophy: User Wins First

**Anthony's Key Insight:** Build backend components to support each user journey step, THEN build frontend that delivers the complete user experience.

**UX Expert Validation (Sally):**
> "This is the RIGHT approach. Too often we build technically convenient features that don't align with how users actually experience the product. By organizing around user journeys, we ensure every sprint delivers user value, not just technical checkboxes. This approach also allows us to validate each journey end-to-end before moving to the next, reducing risk and improving quality."

---

## 📖 Epic 1 User Journeys (From PRD)

### **Journey 1: New User Onboarding (First Company Creator)**

**User Goal:** Sign up, verify email, complete profile, create company, and start using platform

**Steps:**
1. **Signup:** Enter email and password → Submit
2. **Email Verification:** Check email → Click verification link → Confirm
3. **Login:** Enter credentials → Authenticate
4. **Onboarding Step 1:** Complete user details (name, phone, role)
5. **Onboarding Step 2:** Find company (ABR search) OR enter manually → Complete billing address
6. **Dashboard Access:** Redirected to dashboard → Start using platform

**Success Criteria:** <5 minutes from signup to dashboard, >85% completion rate

---

### **Journey 2: Invited User Onboarding (Team Member)**

**User Goal:** Accept invitation, create account, join team, start using platform

**Steps:**
1. **Receive Invitation:** Email with invitation link → Click link
2. **View Invitation:** See company name, role, inviter → Understand context
3. **Accept Invitation:** Enter password (name/email pre-filled) → Submit
4. **Simplified Onboarding:** Complete user details only (no company setup)
5. **Dashboard Access:** Redirected to company dashboard → Start using platform

**Success Criteria:** <3 minutes from email to dashboard, >90% acceptance rate

---

### **Journey 3: Password Reset (Forgotten Password)**

**User Goal:** Reset forgotten password and regain account access

**Steps:**
1. **Request Reset:** Click "Forgot password?" → Enter email → Submit
2. **Check Email:** Receive reset link → Click link
3. **Reset Password:** Enter new password with confirmation → Submit
4. **Login:** Redirected to login → Enter credentials → Access account

**Success Criteria:** <2 minutes from request to login, >95% completion rate

---

### **Journey 4: Multi-Company User (Branch/Freelancer)**

**User Goal:** Work with multiple companies and switch between them seamlessly

**Steps:**
1. **Join Second Company:** Accept invitation to Company B (already member of Company A)
2. **Verify Multi-Company Access:** See both companies in company switcher
3. **Switch Company Context:** Click Company B in switcher → Context changes
4. **Verify Data Isolation:** Confirm only Company B data visible (not Company A)
5. **Switch Back:** Click Company A → Context switches → Company A data visible

**Success Criteria:** <3 seconds to switch, 100% data isolation, 0% confusion

---

### **Journey 5: Returning User (Login)**

**User Goal:** Log in and access dashboard quickly

**Steps:**
1. **Login:** Enter email and password → Submit
2. **Dashboard Access:** Authenticated → Redirected to dashboard

**Success Criteria:** <3 seconds from submit to dashboard

---

## 🗺️ Stories Mapped to User Journeys

### **Journey 1: New User Onboarding** (PRIORITY 1 - Core Value)

| Journey Step | Backend Stories (Build First) | Frontend Stories (Build Second) |
|--------------|-------------------------------|----------------------------------|
| **1. Signup** | Story 1.1 (Signup API) | Story 1.9 (Signup Page) |
| **2. Email Verification** | Story 1.1 (Verification API) | Story 1.9 (Auth Context) |
| **3. Login** | Story 1.2 (Login API, JWT) | Story 1.9 (Login Page) |
| **4. Authorization** | Story 1.3 (RBAC Middleware) | Story 1.9 (Protected Routes) |
| **5. Configuration** | Story 1.13 (Config Service) | Story 1.14 (Dynamic Config) |
| **6. Validation** | Story 1.12 (Validation Engine) | Story 1.14 (Form Validation) |
| **7. Company Search** | Story 1.10 (ABR Search API) | Story 1.14 (Search Component) |
| **8. Onboarding Flow** | Story 1.5 (Onboarding API) | Story 1.14 (Onboarding Wizard) |

**Journey Completion:** After Story 1.14, users can complete full onboarding journey

---

### **Journey 2: Invited User Onboarding** (PRIORITY 2 - Team Growth)

| Journey Step | Backend Stories (Build First) | Frontend Stories (Build Second) |
|--------------|-------------------------------|----------------------------------|
| **1. Send Invitation** | Story 1.6 (Invitation API) | Story 1.16 (Invite Modal) |
| **2. View Invitations** | Story 1.6 (List API) | Story 1.16 (Invitation List) |
| **3. Accept Invitation** | Story 1.7 (Acceptance API) | Story 1.16 (Acceptance Page) |
| **4. Simplified Onboarding** | Story 1.5 (User Details API) | Story 1.14 (Onboarding Step 1 only) |

**Journey Completion:** After Story 1.16, admins can invite team members and they can join

---

### **Journey 3: Password Reset** (PRIORITY 3 - Account Recovery)

| Journey Step | Backend Stories (Build First) | Frontend Stories (Build Second) |
|--------------|-------------------------------|----------------------------------|
| **1. Request Reset** | Story 1.4 (Reset Request API) | Story 1.15 (Request Page) |
| **2. Confirm Reset** | Story 1.4 (Reset Confirm API) | Story 1.15 (Confirm Page) |

**Journey Completion:** After Story 1.15, users can recover forgotten passwords

---

### **Journey 4: Multi-Company User** (PRIORITY 4 - Advanced Feature)

| Journey Step | Backend Stories (Build First) | Frontend Stories (Build Second) |
|--------------|-------------------------------|----------------------------------|
| **1. Multi-Company Support** | Story 1.11 (Relationships API) | Story 1.16 (Company Switcher) |
| **2. Company Switching** | Story 1.11 (Switch API) | Story 1.16 (Switcher Dropdown) |
| **3. Data Isolation Testing** | Story 1.8 (Multi-Tenancy Tests) | Story 1.16 (UI Verification) |

**Journey Completion:** After Story 1.11 + 1.16, multi-company users can switch seamlessly

---

### **Journey 5: Returning User** (DEPENDS ON Journey 1)

| Journey Step | Backend Stories | Frontend Stories |
|--------------|----------------|------------------|
| **Login** | Story 1.2 (Already built) | Story 1.9 (Already built) |

**Journey Completion:** Covered by Journey 1 implementation

---

## 🏗️ User-Journey-Centric Implementation Order

### **WAVE 1: Journey 1 - Core Onboarding (Weeks 1-6)**

**Goal:** New users can sign up, verify email, log in, and complete onboarding

#### **Sprint 1-2: Authentication Backend (Weeks 1-2)**
1. **Story 1.1:** User Signup & Email Verification (Backend)
2. **Story 1.2:** Login & JWT Tokens (Backend)
3. **Story 1.3:** RBAC Middleware & Authorization (Backend)

**Deliverable:** Complete authentication APIs ready for frontend

**User Validation:** Can test via Postman/curl (no UI yet)

---

#### **Sprint 3: Foundation Services (Week 3)**
1. **Story 1.12:** International Foundation & Validation Engine (Backend)
2. **Story 1.13:** Configuration Service Implementation (Backend)

**Deliverable:** Validation and configuration services ready for frontend forms

**User Validation:** Can test configuration changes via admin API

---

#### **Sprint 4: Company Search & Onboarding Backend (Week 4)**
1. **Story 1.10:** Enhanced ABR Search Implementation (Backend)
2. **Story 1.5:** First-Time User Onboarding (Backend)

**Deliverable:** Complete onboarding APIs with ABR search ready

**User Validation:** Can test complete onboarding flow via API

---

#### **Sprint 5: Authentication Frontend (Week 5)**
1. **Story 1.9:** Frontend Authentication (Signup & Login Pages)

**Deliverable:** Users can sign up, verify email, and log in via UI

**User Validation:** ✅ **FIRST USER-FACING MILESTONE** - Users can create accounts!

---

#### **Sprint 6: Onboarding Frontend (Week 6)**
1. **Story 1.14:** Frontend Onboarding Flow

**Deliverable:** ✅ **JOURNEY 1 COMPLETE** - Users can complete full onboarding!

**User Validation:** Full user journey testable end-to-end

**UAT Checkpoint:** Run Journey 1 UAT scenarios with real users

---

### **WAVE 2: Journey 3 - Password Reset (Week 7)**

**Goal:** Users can recover forgotten passwords

#### **Sprint 7: Password Reset Complete (Week 7)**
1. **Story 1.4:** Password Reset Flow (Backend)
2. **Story 1.15:** Frontend Password Reset Pages (Frontend)

**Deliverable:** ✅ **JOURNEY 3 COMPLETE** - Users can reset forgotten passwords!

**User Validation:** Full password reset journey testable

**UAT Checkpoint:** Run Journey 3 UAT scenarios

---

### **WAVE 3: Journey 2 & 4 - Team Collaboration (Weeks 8-10)**

**Goal:** Teams can collaborate, multi-company users supported

#### **Sprint 8: Team Invitations Backend (Week 8)**
1. **Story 1.6:** Team Invitation System (Backend)
2. **Story 1.7:** Invited User Acceptance & Onboarding (Backend)

**Deliverable:** Complete team invitation APIs ready

**User Validation:** Can test invitation flow via API

---

#### **Sprint 9: Multi-Company Backend (Week 9)**
1. **Story 1.11:** Branch Company Scenarios & Company Switching (Backend)

**Deliverable:** Multi-company support APIs ready

**User Validation:** Can test company switching via API

---

#### **Sprint 10: Team & Multi-Company Frontend (Week 10)**
1. **Story 1.16:** Frontend Team Management UI

**Deliverable:** ✅ **JOURNEYS 2 & 4 COMPLETE** - Teams can collaborate, multi-company works!

**User Validation:** Full team invitation and multi-company journeys testable

**UAT Checkpoint:** Run Journey 2 and Journey 4 UAT scenarios

---

### **WAVE 4: Testing & Polish (Weeks 11-12)**

**Goal:** Ensure quality, security, and delightful UX

#### **Sprint 11: Multi-Tenancy Testing (Week 11)**
1. **Story 1.8:** Multi-Tenant Data Isolation & Testing

**Deliverable:** Comprehensive security testing complete, 100% data isolation verified

**User Validation:** Security audit complete, no data leakage

---

#### **Sprint 12: UX Polish (Week 12)**
1. **Story 1.17:** UX Enhancement & Polish

**Deliverable:** ✅ **EPIC 1 COMPLETE** - Professional, polished, accessible UX!

**User Validation:** WCAG 2.1 AA compliance, >85% onboarding completion, <5 min time-to-value

**UAT Checkpoint:** Run all UAT scenarios, verify all success criteria met

---

## 📊 Implementation Strategy Summary

### **Backend-First Strategy:**

**Advantages:**
1. ✅ Frontend has complete APIs to work with (no mocking needed)
2. ✅ Backend can be tested independently via API calls
3. ✅ Frontend developers can see real data and responses
4. ✅ Integration is smoother (backend already validated)
5. ✅ Reduces frontend rework (API contracts already stable)

**Implementation Pattern:**
```
Sprint N:   Build Backend APIs for Journey Step
Sprint N+1: Build Frontend UI that consumes those APIs
Sprint N+2: Test Complete Journey End-to-End
```

---

### **Journey-Centric Strategy:**

**Advantages:**
1. ✅ Each wave delivers complete user value (testable journey)
2. ✅ UAT can validate complete journeys, not isolated features
3. ✅ Product Owner can demonstrate complete flows to stakeholders
4. ✅ Reduces risk of building features users don't need
5. ✅ Prioritization is clear (core journeys first, advanced later)

**Journey Priority:**
```
Priority 1: Journey 1 (New User Onboarding) - Core Value
Priority 2: Journey 3 (Password Reset) - Account Recovery
Priority 3: Journey 2 (Team Invitations) - Team Growth  
Priority 4: Journey 4 (Multi-Company) - Advanced Feature
Priority 5: Journey 5 (Returning User) - Already covered
```

---

## 🎨 UX Expert Validation (Sally's Analysis)

### **User Journey Completeness:**

✅ **Journey 1 (New User Onboarding):**
- All steps covered from signup to dashboard
- ABR search significantly improves onboarding UX (90% vs 20% success rate)
- Auto-save prevents data loss (critical for multi-step wizards)
- Progress indicators provide clarity

✅ **Journey 2 (Invited User):**
- Simplified onboarding (no company setup) respects context
- Pre-filled information reduces friction
- Clear company/role context prevents confusion

✅ **Journey 3 (Password Reset):**
- Standard pattern users expect
- Token expiry handled gracefully
- Security messaging clear but not alarming

✅ **Journey 4 (Multi-Company):**
- Company switcher is visible and accessible
- Relationship context (Branch, Head Office) prevents confusion
- Data isolation is critical security requirement

✅ **Journey 5 (Returning User):**
- Fast and frictionless (<3 seconds)
- Remember me option (if implemented) reduces login frequency

---

### **UX Risks & Mitigations:**

**Risk 1: Onboarding Abandonment (Journey 1)**
- **Mitigation:** Auto-save, progress indicators, <5 min time-to-value
- **Story Coverage:** Story 1.14 (Auto-save), Story 1.17 (Progress indicators)

**Risk 2: Company Search Frustration (Journey 1)**
- **Mitigation:** Enhanced ABR search (90% success), manual entry fallback
- **Story Coverage:** Story 1.10 (ABR search with caching)

**Risk 3: Multi-Company Confusion (Journey 4)**
- **Mitigation:** Relationship badges, active company indicator, <3s switch time
- **Story Coverage:** Story 1.11 (Company switcher), Story 1.16 (UI)

**Risk 4: Accessibility Compliance (All Journeys)**
- **Mitigation:** WCAG 2.1 AA compliance, screen reader support, keyboard navigation
- **Story Coverage:** Story 1.17 (UX Enhancement & Accessibility)

---

### **UX Success Metrics:**

| Journey | Key UX Metric | Target | Story Validation |
|---------|---------------|--------|------------------|
| **Journey 1** | Onboarding completion rate | >85% | Story 1.14 UAT |
| **Journey 1** | Time to value | <5 minutes | Story 1.14 UAT |
| **Journey 1** | Company search success | >90% | Story 1.10 UAT |
| **Journey 2** | Invitation acceptance rate | >90% | Story 1.16 UAT |
| **Journey 2** | Time to join team | <3 minutes | Story 1.16 UAT |
| **Journey 3** | Password reset completion | >95% | Story 1.15 UAT |
| **Journey 4** | Company switch time | <3 seconds | Story 1.11 UAT |
| **Journey 4** | Data isolation | 100% | Story 1.8 UAT |
| **All Journeys** | WCAG 2.1 AA compliance | 100% | Story 1.17 UAT |

---

## 🎯 User Wins by Wave

### **Wave 1 Complete (Week 6):**
**User Win:** "I can create an account and set up my company in under 5 minutes!"
- New users can sign up, verify email, log in, and complete onboarding
- Company search finds their company 90% of the time
- Onboarding feels smooth and professional

---

### **Wave 2 Complete (Week 7):**
**User Win:** "I forgot my password but recovered my account in 2 minutes!"
- Users never permanently locked out of accounts
- Password reset is fast and secure

---

### **Wave 3 Complete (Week 10):**
**User Win:** "I invited my team and they were up and running in 3 minutes!"
- Admins can build teams easily
- Invitations are clear and professional
- Multi-company users can switch contexts seamlessly

---

### **Wave 4 Complete (Week 12):**
**User Win:** "This platform feels polished, fast, and accessible!"
- Professional UX with smooth animations
- Accessible to users with disabilities
- Fast and responsive
- Data is secure (100% isolation verified)

---

## 📋 Recommended Approach

### **Anthony's Request: Backend → Frontend → Journey Validation**

**Implementation Pattern Per Wave:**

1. **Build Backend APIs** (1-2 sprints)
   - Complete all backend stories for journey
   - Test via Postman/curl
   - Validate data, security, performance

2. **Build Frontend UI** (1 sprint)
   - Consume backend APIs
   - Implement UX design
   - Add polish and validation

3. **Validate Complete Journey** (UAT)
   - Run UAT scenarios with real users
   - Measure success criteria
   - Iterate if needed before next wave

4. **Stakeholder Demo** (Optional)
   - Demonstrate complete user journey
   - Collect feedback
   - Adjust priorities if needed

**Benefits:**
- ✅ Each wave delivers complete user value
- ✅ Backend is stable before frontend work starts
- ✅ UAT validates real user experience, not isolated features
- ✅ Stakeholders see progress in user-meaningful terms
- ✅ Risk is managed (core journeys first)

---

## ✅ Recommendation: Proceed with User-Journey-Centric Plan

**This approach ensures:**
1. ✅ User experience drives implementation (not technical convenience)
2. ✅ Backend built first provides stable foundation for frontend
3. ✅ Each wave delivers testable, demonstrable user value
4. ✅ UAT validates complete journeys (most realistic testing)
5. ✅ Core journeys prioritized (new user onboarding first)
6. ✅ UX expert validated (Sally approves this approach)

**User is the winner:** Every sprint delivers user-facing value, not just technical checkboxes.

---

**Prepared by:** Sarah (Product Owner) & Sally (UX Expert)  
**Date:** 2025-10-16  
**Status:** Ready for Anthony's Review and Approval

