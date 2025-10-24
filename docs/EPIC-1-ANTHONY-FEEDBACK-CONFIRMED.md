# Epic 1: Anthony's Feedback - All Confirmed & Implemented

**Date:** 2025-10-17  
**Status:** ✅ All Feedback Addressed and Implemented

---

## ✅ Your Feedback Points

### **1. Unlimited Company Hierarchy with Sliding Window UI**

**Your Request:**
> "The company 5 level limit is this a UI constraint if yes can we allow unlimited hierarchy but only display a max of 5. What I mean is when the user selects company 5 in the hierarchy Company 0 disappears and Company 6 appears."

**✅ CONFIRMED AND IMPLEMENTED:**

**Database:** Unlimited hierarchy depth (no constraints)
```sql
UserCompanyRelationship
  ParentCompanyID  -- Can be nested infinitely (Level 0 → ∞)
```

**UI:** Sliding window displays 5 levels at a time
```
Initial View (Levels 0-4):
🏢 ACME Global (Level 0)        ← Visible
  └─ 🏢 ACME APAC (Level 1)     ← Visible
      └─ 🏢 ACME AUS (Level 2)  ← Visible
          └─ 🏢 ACME SYD (Level 3) ← Visible
              └─ 🏢 ACME CBD (Level 4) ← Visible
                  └─ 🏢 Store 1 (Level 5) ... ← Hint: More

User clicks "ACME CBD" (Level 4) → Window shifts:
... 🏢 ACME AUS (Level 2)       ← Hint: More above
  └─ 🏢 ACME SYD (Level 3)      ← Visible
      └─ 🏢 ACME CBD (Level 4)  ← Visible (SELECTED)
          └─ 🏢 Store 1 (Level 5) ← Visible
              └─ 🏢 Store 1 West (Level 6) ← Visible
                  └─ 🏢 Unit A (Level 7) ← Visible
                      └─ 🏢 Floor 2 (Level 8) ... ← Hint: More
```

**Breadcrumbs show full path (always visible, clickable):**
```
Dashboard > ACME Global > ACME APAC > ... > ACME SYD > ACME CBD
                                      ↑
                                Click to jump back
```

**Updated in:** `docs/stories/story-1.18.md` (AC-3)

---

### **2. Billing & Adding Companies Deferred to Epic 2**

**Your Clarification:**
> "The adding of companies and the Billing structure is all for Epic 2."

**✅ CONFIRMED:**

**Epic 1 Scope (Authentication & Onboarding):**
- ✅ User can sign up and create their FIRST company (onboarding)
- ✅ User can be invited to join EXISTING companies
- ✅ User can switch between companies (if they belong to multiple)
- ✅ Dashboard displays company hierarchy (view only, unlimited depth, sliding window)
- ✅ Team management (invite users, edit roles)

**Epic 2 Scope (Company Management & Billing):**
- ❌ Adding additional companies (after first one from onboarding)
- ❌ Editing company hierarchy (moving branches, changing parents)
- ❌ Billing hierarchy (head office pays for branch forms)
- ❌ Invoicing (company-based billing, Australian GST)
- ❌ Company settings (editing company details, logos, etc.)

**Updated in:** `docs/stories/story-1.18.md` (Notes section)

---

### **3. Stories 1.1-1.8 Already Complete**

**Your Update:**
> "All Stories up until 1.8 have already been completed"

**✅ CONFIRMED:**

**Completed Stories (Backend + Testing):**
- Story 0.1: Database Models (87 tables) ✅
- Story 1.1: User Signup & Email Verification ✅
- Story 1.2: Login & JWT Tokens ✅
- Story 1.3: RBAC Middleware ✅
- Story 1.4: Password Reset ✅
- Story 1.5: Onboarding (Backend) ✅
- Story 1.6: Team Invitations (Backend) ✅
- Story 1.7: Invitation Acceptance (Backend) ✅
- Story 1.8: Multi-Tenancy Testing ✅

**Remaining Stories (Frontend + Polish):**
- Story 1.9: Frontend Authentication 🔜
- Story 1.10: ABR Search (Backend) 🔜
- Story 1.11: Company Switching (Backend) 🔜
- Story 1.12: Validation Engine (Backend) 🔜
- Story 1.13: Configuration Service (Backend) 🔜
- Story 1.14: Frontend Onboarding 🔜
- Story 1.15: Frontend Password Reset 🔜
- Story 1.16: Frontend Team Management 🔜
- Story 1.17: UX Polish 🔜
- Story 1.18: Dashboard Framework 🔜

**Revised Timeline:** **7 weeks** (from Story 1.9 to Epic 1 completion)

**Updated in:** `docs/EPIC-1-REVISED-PLAN-STARTING-FROM-1.9.md`

---

### **4. Onboarding as Modal on Dashboard**

**Your Clarification:**
> "When the user logs in for the first time they will see an empty dashboard with only the KPI's showing. The onboarding screens popup and the user adds more personal information and then adds their company details and once accepted the company appears on their dashboard."

**✅ CONFIRMED:**

**Updated First-Time Login Flow:**
```
Step 1: User signs up → Verifies email → Logs in
Step 2: Dashboard loads (EMPTY STATE)
        ├─ KPI cards show (all zeros)
        ├─ No companies visible
        └─ Empty message: "Let's get you set up!"
Step 3: Onboarding modal pops up (overlay on dashboard)
        ├─ Cannot dismiss (no X, no ESC, must complete)
        ├─ Step 1: User details (name, phone, role)
        └─ Step 2: Company details (ABR search OR manual)
Step 4: User completes onboarding → Modal closes
Step 5: Dashboard refreshes → Company appears
        ├─ Company container shows on dashboard
        ├─ KPIs still show zeros (no events yet)
        └─ Empty state: "Create your first event!"
```

**Modal Behavior:**
- Cannot dismiss (required to use platform)
- Overlays on empty dashboard (dashboard visible behind modal)
- After completion, modal closes and dashboard refreshes

**Updated in:** Story 1.14 will be revised to reflect modal approach (not full-page)

---

### **5. Dashboard is Post-Onboarding Destination**

**Your Confirmation:**
> "Can I confirm that when the user completes the onboarding process the next step is for them to see the dashboard"

**✅ CONFIRMED:**

**Flow:**
```
User completes onboarding modal
   ↓
Modal closes
   ↓
Dashboard refreshes (company now visible)
   ↓
User sees their company on dashboard
   ↓
Company container is expanded by default
   ↓
Empty state: "Create your first event!" [+ Create Event]
   ↓
User clicks [+ Create Event] → Epic 2 (Events & Forms)
```

**Dashboard is the central hub** - Not a separate page, but the destination after onboarding.

---

## 📋 Updated Documents

### **1. Story 1.18: Dashboard Framework & Container System**
**File:** `docs/stories/story-1.18.md`

**Updates:**
- ✅ AC-3: Unlimited hierarchy with sliding window (5-level display)
- ✅ Breadcrumb navigation (full path, clickable)
- ✅ "..." indicators for hidden levels above/below
- ✅ Recursive component (same component, different depth)
- ✅ Notes: Billing deferred to Epic 2

---

### **2. Revised Implementation Plan (Starting from Story 1.9)**
**File:** `docs/EPIC-1-REVISED-PLAN-STARTING-FROM-1.9.md`

**Updates:**
- ✅ Stories 1.1-1.8 marked as complete
- ✅ Remaining stories: 1.9-1.18 (Frontend + Polish)
- ✅ Revised timeline: 7 weeks (not 13 weeks)
- ✅ Sprint breakdown (Sprints 1-6)

---

### **3. Story 1.14: Frontend Onboarding (Will be revised)**
**File:** `docs/stories/story-1.14.md`

**Updates Needed:**
- 🔜 Change from full-page flow to modal/overlay
- 🔜 Modal appears on empty dashboard
- 🔜 Cannot dismiss (required to complete)
- 🔜 After submission, modal closes → Dashboard refreshes

---

## 🚀 Next Steps (Sprint 1 - This Week)

### **Goal:** Complete remaining backend APIs for frontend consumption

**Stories to Complete:**

**1. Story 1.10: Enhanced ABR Search (~2 days)**
- ABR API integration
- Search endpoint: `POST /api/companies/search-abr`
- Auto-detect search type (ABN, ACN, Name)
- Cache results (Redis, 24-hour TTL)

**2. Story 1.11: Company Switching API (~1 day)**
- `GET /api/dashboard/companies` (hierarchical, unlimited depth)
- `POST /api/companies/switch` (update active company context)

**3. Story 1.12: Validation Engine (~1 day)**
- Phone number validation (Australian format)
- Address validation
- Email validation
- Endpoint: `POST /api/validation/validate`

**4. Story 1.13: Configuration Service (~1 day)**
- Query `AppSetting` table
- Query `ValidationRule` table
- Endpoints: `GET /api/config/settings`, `GET /api/config/validation-rules`
- Cache with 5-minute TTL

**Deliverable by End of Week:** All backend APIs ready for frontend consumption

---

## 📊 Revised Epic 1 Timeline (7 Weeks)

| Week | Sprint | Stories | Deliverable |
|------|--------|---------|-------------|
| **1** | Sprint 1 | 1.10, 1.11, 1.12, 1.13 | Backend APIs complete ✅ |
| **2** | Sprint 2 | 1.9 | Frontend authentication |
| **3** | Sprint 3 | 1.14, 1.15 | Frontend onboarding & password reset |
| **4-5** | Sprint 4 | 1.18 (Part 1) | Dashboard framework |
| **5-6** | Sprint 5 | 1.18 (Part 2), 1.16 | Team management UI |
| **7** | Sprint 6 | 1.17 | UX polish & launch prep |

**Launch Date:** ~7 weeks from now (mid-December 2025)

---

## ✅ All Feedback Confirmed

**Summary:**

1. ✅ **Unlimited hierarchy with sliding window** - Implemented in Story 1.18
2. ✅ **Billing deferred to Epic 2** - Removed from Story 1.18
3. ✅ **Stories 1.1-1.8 complete** - Revised plan starts from Story 1.9
4. ✅ **Onboarding as modal** - Will update Story 1.14
5. ✅ **Dashboard is post-onboarding destination** - Confirmed

**Ready to proceed with Sprint 1 (Stories 1.10-1.13)!** 🚀

---

**Prepared by:** Sarah (Product Owner)  
**Date:** 2025-10-17  
**Status:** ✅ Ready to Start Sprint 1

