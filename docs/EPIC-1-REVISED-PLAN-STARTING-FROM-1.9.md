# Epic 1: Revised Implementation Plan (Starting from Story 1.9)

**Date:** 2025-10-17  
**Status Update:** Stories 1.1-1.8 COMPLETED  
**Remaining:** Stories 1.9-1.18 (Frontend + Polish)  
**Revised Timeline:** **7 weeks** (from story 1.9 to Epic 1 completion)

---

## ✅ COMPLETED: Backend Foundation (Stories 1.1-1.8)

**Completed by Anthony's team:**

| Story | Description | Status |
|-------|-------------|--------|
| **0.1** | Database Models (87 tables) | ✅ DONE |
| **1.1** | User Signup & Email Verification | ✅ DONE |
| **1.2** | Login & JWT Tokens | ✅ DONE |
| **1.3** | RBAC Middleware & Authorization | ✅ DONE |
| **1.4** | Password Reset Flow | ✅ DONE |
| **1.5** | First-Time User Onboarding (Backend) | ✅ DONE |
| **1.6** | Team Invitation System (Backend) | ✅ DONE |
| **1.7** | Invited User Acceptance (Backend) | ✅ DONE |
| **1.8** | Multi-Tenant Data Isolation Testing | ✅ DONE |

**Result:** 🎉 **Backend is COMPLETE! All APIs ready for frontend consumption.**

---

## 🔜 REMAINING: Frontend Implementation (Stories 1.9-1.18)

**What's Left:**

| Story | Description | Priority | Estimated Days |
|-------|-------------|----------|----------------|
| **1.9** | Frontend Authentication (Signup & Login Pages) | Critical | 4 days |
| **1.10** | Enhanced ABR Search Implementation (Backend) | High | 2 days |
| **1.11** | Branch Company Scenarios & Switching (Backend) | High | 1 day |
| **1.12** | International Foundation & Validation (Backend) | High | 1 day |
| **1.13** | Configuration Service (Backend) | High | 1 day |
| **1.14** | Frontend Onboarding Flow (Modal) | Critical | 4 days |
| **1.15** | Frontend Password Reset Pages | High | 2 days |
| **1.16** | Frontend Team Management UI | High | 4 days |
| **1.17** | UX Enhancement & Polish | Medium | 5 days |
| **1.18** | Dashboard Framework & Container System | Critical | 8 days |

**Total Remaining:** ~32 days (~7 weeks with parallel work)

---

## 🗺️ Revised Implementation Waves

### **WAVE 3: Frontend Foundation (Weeks 1-3)**

**Sprint 1 (Week 1): Backend Support Services**
- Story 1.10: Enhanced ABR Search (Backend API)
- Story 1.11: Company Switching API (Backend)
- Story 1.12: Validation Engine (Backend)
- Story 1.13: Configuration Service (Backend)

**Deliverable:** All backend APIs complete and ready for frontend

---

**Sprint 2 (Week 2): Core Frontend - Authentication**
- Story 1.9: Frontend Authentication (Signup & Login Pages)
  - Signup page with email verification flow
  - Login page with JWT handling
  - Auth context (React Context API)
  - Protected route guards
  - Consumes: Stories 1.1, 1.2, 1.3 (already built)

**Deliverable:** ✅ Users can sign up, verify email, and log in via UI

---

**Sprint 3 (Week 3): Core Frontend - Onboarding & Password Reset**
- Story 1.14: Frontend Onboarding Flow (Modal on Dashboard)
  - Onboarding modal (not full-page)
  - Step 1: User details (name, phone, role)
  - Step 2: Company details (ABR search OR manual entry)
  - Auto-save functionality
  - Consumes: Stories 1.5, 1.10, 1.12, 1.13

- Story 1.15: Frontend Password Reset Pages
  - Request reset page
  - Confirm reset page (with token validation)
  - Consumes: Story 1.4 (already built)

**Deliverable:** ✅ Users can complete onboarding and reset passwords via UI

---

### **WAVE 4: Dashboard & Team Collaboration (Weeks 4-6)**

**Sprint 4 (Weeks 4-5): Dashboard Framework**
- Story 1.18: Dashboard Framework & Container System (Part 1)
  - Dashboard layout (KPIs + company containers)
  - Company container component (recursive)
  - **Unlimited hierarchy with sliding window** (5-level display)
  - Breadcrumb navigation (full path, clickable)
  - Company switching (click containers)
  - KPI components (Total Forms, Total Leads, Active Events)
  - Empty states (before and after onboarding)
  - Consumes: Stories 1.11 (already built)

**Deliverable:** ✅ Dashboard with company hierarchy and KPI dashboard

---

**Sprint 5 (Weeks 5-6): Team Management UI**
- Story 1.18: Dashboard Framework (Part 2)
  - User icon [👥] in company header
  - Team management panel (contextual to each company)
  - Role-based access (admin vs non-admin)

- Story 1.16: Invitation Modal & User Role Editing
  - Invitation modal (triggered from team panel)
  - User role editing (admin only, if role is equal or lower)
  - Pending invitation display
  - Consumes: Stories 1.6, 1.7 (already built)

**Deliverable:** ✅ Full team management and multi-company support

---

### **WAVE 5: Polish & Launch (Week 7)**

**Sprint 6 (Week 7): UX Enhancement & Final Polish**
- Story 1.17: UX Enhancement & Polish
  - Smooth animations and transitions
  - Loading states (skeletons, spinners)
  - Error handling (user-friendly messages)
  - Empty states (helpful CTAs)
  - Accessibility (WCAG 2.1 AA compliance)
  - Mobile responsiveness (tablet, phone)
  - Performance optimization (lazy loading, code splitting)
  - Browser testing (Chrome, Firefox, Safari, Edge)

**Deliverable:** ✅ **EPIC 1 COMPLETE - Production-ready platform!**

---

## 🎯 Key Changes Based on Anthony's Feedback

### **1. Unlimited Company Hierarchy with Sliding Window UI**

**Database:** Unlimited depth (no constraints)
```sql
UserCompanyRelationship
  ParentCompanyID  -- Can be nested infinitely (Level 0 → ∞)
```

**UI:** Display 5 levels at a time (sliding window)
```
Initial View (Levels 0-4 visible):
🏢 ACME Global (Level 0)        ← Visible
  └─ 🏢 ACME APAC (Level 1)     ← Visible
      └─ 🏢 ACME AUS (Level 2)  ← Visible
          └─ 🏢 ACME SYD (Level 3) ← Visible
              └─ 🏢 ACME CBD (Level 4) ← Visible
                  └─ 🏢 Store 1 (Level 5) ... ← Hint: More below

User clicks "ACME CBD" (Level 4) → Window shifts:
... 🏢 ACME AUS (Level 2)       ← Hint: More above
  └─ 🏢 ACME SYD (Level 3)      ← Visible
      └─ 🏢 ACME CBD (Level 4)  ← Visible (SELECTED)
          └─ 🏢 Store 1 (Level 5) ← Visible
              └─ 🏢 Store 1 West (Level 6) ← Visible
                  └─ 🏢 Store 1 West A (Level 7) ← Visible
                      └─ 🏢 Floor 2 (Level 8) ... ← Hint: More below
```

**Breadcrumb Navigation:**
```
DASHBOARD > ACME Global > ACME APAC > ... > ACME SYD > ACME CBD
                                      ↑
                                Click to jump back
```

**Implementation:**
- Store full hierarchy in state
- Calculate visible window (5 levels) based on selected company
- Show "..." indicators for hidden levels above/below
- Breadcrumbs show full path (always visible)

---

### **2. Onboarding as Modal (Not Full-Page)**

**Flow:**
1. User logs in for first time
2. Dashboard loads (empty state: KPIs showing zeros, no companies)
3. Onboarding modal pops up (overlay on dashboard)
4. User completes Step 1 (user details) and Step 2 (company details)
5. Modal closes → Dashboard refreshes → Company appears
6. User sees company with empty state: "Create your first event!"

**Modal Behavior:**
- Cannot dismiss (no X button, no ESC key, no click outside)
- Required to complete (blocks platform use until done)
- After submission, modal closes and dashboard refreshes

---

### **3. Billing & Adding Companies Deferred to Epic 2**

**Epic 1 Scope (Authentication & Onboarding):**
- ✅ User can sign up and create their FIRST company
- ✅ User can be invited to join EXISTING companies
- ✅ User can switch between companies (if they belong to multiple)
- ✅ Dashboard displays company hierarchy (view only)

**Epic 2 Scope (Events & Forms + Company Management):**
- ❌ Adding additional companies (after first one)
- ❌ Editing company hierarchy (moving branches, changing parents)
- ❌ Billing and invoicing (head office pays for branches)
- ❌ Company settings (editing company details)

**Epic 1 delivers:** User onboarding, authentication, team invitations, company hierarchy viewing

**Epic 2 delivers:** Company management, events, forms, billing

---

## 📊 Revised Timeline (7 Weeks)

| Week | Sprint | Stories | Deliverable |
|------|--------|---------|-------------|
| **1** | Sprint 1 | 1.10, 1.11, 1.12, 1.13 | Backend APIs complete |
| **2** | Sprint 2 | 1.9 | Frontend authentication |
| **3** | Sprint 3 | 1.14, 1.15 | Frontend onboarding & password reset |
| **4-5** | Sprint 4 | 1.18 (Part 1) | Dashboard framework |
| **5-6** | Sprint 5 | 1.18 (Part 2), 1.16 | Team management UI |
| **7** | Sprint 6 | 1.17 | UX polish & launch prep |

**Launch Date:** ~7 weeks from now (mid-December 2025)

---

## 🚀 Immediate Next Steps (Sprint 1 - This Week)

### **Goal:** Complete remaining backend APIs

**Stories to Complete:**

**Story 1.10: Enhanced ABR Search (~2 days)**
- Integrate ABR API
- Create search endpoint: `POST /api/companies/search-abr`
- Auto-detect search type (ABN, ACN, or Name)
- Cache results (Redis, 24-hour TTL)
- Return: Company name, ABN, ACN, address

**Story 1.11: Company Switching API (~1 day)**
- Create endpoint: `GET /api/dashboard/companies` (hierarchical, unlimited depth)
- Create endpoint: `POST /api/companies/switch` (update active company in session)
- Return company hierarchy with full parent-child relationships

**Story 1.12: Validation Engine (~1 day)**
- Phone number validation (Australian format: +61...)
- Address validation (Australian states/postcodes)
- Email validation (RFC 5322)
- Create endpoint: `POST /api/validation/validate`

**Story 1.13: Configuration Service (~1 day)**
- Query `AppSetting` table
- Query `ValidationRule` table
- Create endpoint: `GET /api/config/settings`
- Create endpoint: `GET /api/config/validation-rules`
- Cache with 5-minute TTL

**Deliverable by End of Week:** All backend APIs ready for frontend to consume

---

## 📋 Updated Story Priorities

**CRITICAL (Must-have for Epic 1):**
- Story 1.9: Frontend Authentication
- Story 1.14: Frontend Onboarding
- Story 1.18: Dashboard Framework

**HIGH (Important for Epic 1):**
- Story 1.10: ABR Search
- Story 1.11: Company Switching
- Story 1.12: Validation Engine
- Story 1.13: Configuration Service
- Story 1.15: Password Reset
- Story 1.16: Team Management

**MEDIUM (Nice-to-have for Epic 1):**
- Story 1.17: UX Polish (can be iterative post-launch)

---

## ✅ Success Criteria (Epic 1 Complete)

**User Journey 1: New User Onboarding**
- ✅ User can sign up and verify email
- ✅ User can log in
- ✅ User completes onboarding modal (user details + company details)
- ✅ User sees company on dashboard
- ✅ Time to complete: <5 minutes

**User Journey 2: Invited User Onboarding**
- ✅ Admin can invite users via user icon in company header
- ✅ User receives invitation email
- ✅ User accepts invitation and joins company
- ✅ User sees company on dashboard
- ✅ Time to complete: <3 minutes

**User Journey 3: Password Reset**
- ✅ User can request password reset
- ✅ User receives reset email
- ✅ User resets password
- ✅ User can log in with new password
- ✅ Time to complete: <2 minutes

**User Journey 4: Multi-Company User**
- ✅ User can belong to multiple companies
- ✅ User can switch between companies by clicking containers
- ✅ Dashboard shows all companies (unlimited hierarchy, 5-level sliding window)
- ✅ KPIs update based on selected company
- ✅ Time to switch: <3 seconds

**User Journey 5: Returning User**
- ✅ User can log in
- ✅ User sees dashboard with companies
- ✅ Time to dashboard: <3 seconds

---

## 🎯 Definition of Done (Epic 1)

✅ All user journeys testable end-to-end  
✅ All UAT scenarios pass  
✅ WCAG 2.1 AA compliance verified  
✅ Performance targets met (<3s load, <1s KPI update)  
✅ Mobile responsive (phone, tablet, desktop)  
✅ Browser testing complete (Chrome, Firefox, Safari, Edge)  
✅ Security audit passed (data isolation, RBAC, JWT)  
✅ Production deployment successful  
✅ User documentation complete  

---

**Prepared by:** Sarah (Product Owner)  
**Date:** 2025-10-17  
**Status:** Ready to start Sprint 1 (Stories 1.10-1.13)

**Next Step:** Begin Sprint 1 (Backend Support Services) 🚀

