# Epic 1: Dashboard Framework Update

**Date:** 2025-10-17  
**Prepared by:** Sarah (Product Owner)  
**For:** Anthony Keevy  
**Status:** Awaiting Approval

---

## 🎯 Anthony's Feedback Summary

### **Critical Insights:**

1. **Dashboard as Container Architecture:**
   - Dashboard is the top-level container, not just a page
   - Shows ALL companies user belongs to (hierarchical structure)
   - Companies are expandable containers revealing sub-companies or events/forms
   - **Company switching happens by clicking containers** (not separate dropdown)
   - KPI components at top summarize data for selected companies (1, 3, or all)

2. **Team Management Location:**
   - **User icon (👥) in company container header** (not separate page)
   - Click → Opens panel showing users in THAT specific company
   - Admins can add/remove/edit roles (equal or lower than theirs)
   - Non-admins see read-only view
   - Contextual to each company (company-specific user list)

3. **Framework Needed for Wave 3:**
   - Can't complete Journey 2 (Team Invitations) without company header with user icon
   - Can't complete Journey 4 (Company Switching) without container hierarchy system
   - **Dashboard framework must be part of Epic 1 (Wave 3) to achieve user journey goals**

---

## ✅ Confirmation: Your Vision is Correct

**Anthony, your architectural thinking is spot-on.** The dashboard framework is NOT a separate page - it's the **central container system** that enables:

1. ✅ **Journey 4 (Company Switching):** Users click containers to switch context
2. ✅ **Journey 2 (Team Management):** User icon in company header provides contextual team management
3. ✅ **Journey 1 (Onboarding):** New users land on dashboard and see their company
4. ✅ **Future (Epic 2):** Events and forms are navigated through company containers

**This aligns perfectly with user-journey-centric implementation because:**
- The dashboard IS the primary navigation paradigm
- Company switching is intuitive (click what you want to see)
- Team management is contextual (in the company header where it belongs)
- KPI dashboard provides immediate value (see data at a glance)

---

## 🆕 New Story: Story 1.18 - Dashboard Framework & Container System

**Created:** `docs/stories/story-1.18.md`

**Story Overview:**
- **Priority:** Critical (Blocks Journey 2 and Journey 4)
- **Estimated Lines:** ~1,200
- **Dependencies:** Story 1.9 (Auth Context), Story 1.11 (Company Relationships)

**What It Includes:**

### **1. Dashboard Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ DASHBOARD                                    [User Profile]  │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│ │  KPI Card 1 │ │  KPI Card 2 │ │  KPI Card 3 │            │
│ │ Total Forms │ │ Total Leads │ │Active Events│            │
│ └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│ MY COMPANIES                                                │
├─────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────────┐   │
│ │ 🏢 ACME Corporation (Head Office)     [👥][⚙️][▼]     │   │
│ └───────────────────────────────────────────────────────┘   │
│   ├─ 📊 Event: Trade Show 2025 (3 forms)                    │
│   ├─ 📊 Event: Expo Sydney (1 form)                         │
│   └─ 🏢 ACME Melbourne (Branch)        [👥][▼]              │
│       └─ 📊 Event: Melbourne Tech Conf (2 forms)            │
│                                                             │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ 🏢 XYZ Consulting (Freelancer)        [👥][⚙️][▼]     │   │
│ └───────────────────────────────────────────────────────┘   │
│   └─ 📊 Event: Client Workshop (1 form)                     │
└─────────────────────────────────────────────────────────────┘
```

**Legend:**
- 🏢 = Company container (clickable to select/expand)
- 👥 = User management icon → Opens team panel (YOUR SUGGESTION)
- ⚙️ = Company settings (only if admin)
- ▼ = Expand/collapse toggle
- 📊 = Event (clickable, leads to event/form management)

---

### **2. Company Container System:**

**Hierarchical Display:**
- Parent companies at top level
- Child companies indented under parents
- Expand/collapse toggles to show/hide children
- Visual hierarchy (indentation, connecting lines)

**Company Switching:**
- Click container → Becomes active (highlighted)
- KPIs update to show selected company data
- Events/forms within container are revealed
- No page reload (<3 seconds)

**Multi-Select (Future):**
- Architecture supports selecting multiple companies
- KPIs aggregate across selected companies
- Not required for Epic 1, but built into foundation

---

### **3. Team Management in Company Header (YOUR SUGGESTION):**

**User Icon (👥) in Company Header:**
```
┌───────────────────────────────────────────────────────┐
│ 🏢 ACME Corporation (Head Office)     [👥][⚙️][▼]     │
└───────────────────────────────────────────────────────┘
                                          ↑
                              Click here to manage team
```

**When User Clicks 👥:**
```
┌─────────────────────────────────────────────────────┐
│ ACME Corporation - Team Members                     │
├─────────────────────────────────────────────────────┤
│ 👤 John Smith          Company Admin     [Edit]     │
│ 👤 Jane Doe            Company User      [Edit]     │
│ 👤 Bob Johnson         Company User      [Edit]     │
│ 👤 alice@example.com   Pending (Invited)            │
├─────────────────────────────────────────────────────┤
│ [+ Invite User]                           [Close]   │
└─────────────────────────────────────────────────────┘
```

**Contextual to Company:**
- Each company container has its own team panel
- Shows users for THAT specific company only
- Admins can invite/edit/remove (role-based)
- Non-admins see read-only view

**This Enables:**
- ✅ Journey 2 (Team Invitations) - Admin clicks 👥 → Invite User
- ✅ Journey 4 (Multi-Company) - Each company has its own team panel
- ✅ Intuitive UX - Team management is where you expect it (in company header)

---

### **4. KPI Components:**

**Minimum 3 KPI Cards:**
1. **Total Forms:** Count of all forms for selected company(ies)
2. **Total Leads:** Count of all lead submissions for selected company(ies)
3. **Active Events:** Count of active events for selected company(ies)

**Dynamic Updates:**
- KPIs update when company selected (<1 second)
- Smooth transitions (fade out old, fade in new)
- Loading states (skeleton placeholders)

**Future Enhancements:**
- Trend indicators (↑ +12% this week)
- Time range filters (Last 7 days, Last 30 days)
- Export KPI data

---

### **5. Backend API Endpoints:**

**Dashboard APIs:**
```
GET  /api/dashboard/companies           # List all user's companies (hierarchical)
GET  /api/dashboard/kpis?companyIds[]   # Get KPI data for selected companies
GET  /api/companies/{id}/events         # Get events for a company (lazy load)
GET  /api/companies/{id}/users          # Get users for team management panel
POST /api/companies/switch              # Switch active company context
```

**Response Example (Hierarchical Companies):**
```json
{
  "companies": [
    {
      "companyId": "123",
      "companyName": "ACME Corporation",
      "relationshipType": "Head Office",
      "userRole": "Company Admin",
      "parentCompanyId": null,
      "childCompanies": [
        {
          "companyId": "124",
          "companyName": "ACME Sydney",
          "relationshipType": "Branch",
          "userRole": "Company Admin",
          "parentCompanyId": "123"
        }
      ],
      "eventCount": 3,
      "formCount": 7
    }
  ]
}
```

---

## 🗺️ Updated Implementation Plan

### **Wave 3 Now Includes Dashboard Framework**

**Original Wave 3 (Weeks 8-10):**
- Sprint 8: Backend Invitations (Stories 1.6, 1.7)
- Sprint 9: Backend Multi-Company (Story 1.11)
- Sprint 10: Frontend Team UI (Story 1.16)

**UPDATED Wave 3 (Weeks 8-11):**

**Sprint 8: Backend Invitations (Week 8)**
- Story 1.6 (Team Invitation API)
- Story 1.7 (Invitation Acceptance API)

**Sprint 9: Backend Multi-Company & Dashboard APIs (Week 9)**
- Story 1.11 (Company Switching API)
- Story 1.18 Backend APIs (Dashboard companies, KPIs, company switching)

**Sprint 10-11: Frontend Dashboard & Team UI (Weeks 10-11)**
- Story 1.18 Frontend (Dashboard layout, containers, KPIs, team panel)
- Story 1.16 (Invitation modal, user role editing - integrated with Story 1.18)

**Result:** ✅ **WAVE 3 COMPLETE** → Dashboard framework in place, Journey 2 & 4 achievable

---

### **Updated Epic 1 Timeline:**

| Wave | Weeks | Stories | Deliverable |
|------|-------|---------|-------------|
| **Wave 1** | 1-6 | 1.1, 1.2, 1.3, 1.12, 1.13, 1.10, 1.5, 1.9, 1.14 | ✅ Journey 1: New User Onboarding |
| **Wave 2** | 7 | 1.4, 1.15 | ✅ Journey 3: Password Reset |
| **Wave 3** | 8-11 | 1.6, 1.7, 1.11, **1.18**, 1.16 | ✅ Journey 2 & 4: Team & Multi-Company + **Dashboard Framework** |
| **Wave 4** | 12-13 | 1.8, 1.17 | ✅ Epic 1 Complete: Testing & Polish |

**Total Duration:** **13 weeks** (was 12 weeks, +1 week for dashboard framework)

---

## 🎯 How Dashboard Framework Enables User Journeys

### **Journey 1: New User Onboarding**
**After Story 1.14 (Onboarding Wizard):**
- User completes onboarding → **Redirected to dashboard**
- Dashboard shows company they just created
- Company container is expanded by default
- KPIs show zeros (no events yet)
- Empty state: "Create your first event!"

**Dashboard is the destination** after successful onboarding.

---

### **Journey 2: Invited User Onboarding**
**After Story 1.18 (Dashboard Framework):**
1. Admin logs in → Sees dashboard with company containers
2. Admin clicks **user icon (👥)** in company header (YOUR SUGGESTION)
3. Team panel opens showing current team members
4. Admin clicks **"Invite User"** → Invitation modal opens (Story 1.16)
5. Admin sends invitation → Invitee receives email
6. Invitee accepts → Joins team
7. Admin sees invitee in team panel (status: Active)

**Dashboard enables:** Contextual team management in company header.

---

### **Journey 4: Multi-Company User**
**After Story 1.18 (Dashboard Framework):**
1. User logs in → Sees dashboard with all companies (ACME, XYZ, ABC)
2. User clicks **ACME company container** (YOUR SUGGESTION)
3. ACME container highlights (active state)
4. KPIs update to show ACME data (<3 seconds)
5. Events/forms within ACME are revealed
6. User clicks **XYZ company container**
7. XYZ becomes active, ACME loses active state
8. KPIs update to show XYZ data (<3 seconds)

**Dashboard enables:** Company switching by clicking containers (no separate dropdown).

**Multi-Company Team Management:**
- User clicks **👥 in ACME header** → See ACME team members
- User clicks **👥 in XYZ header** → See XYZ team members (different list)
- Team panels are contextual to each company

---

## ✅ Answers to Your Questions

### **Question 1: Does the Dashboard Layout Align with Your Thoughts?**

**Your Vision:**
> "Dashboard will show all companies the user belongs to... there is a hierarchy to the company structure... list of all the top level companies which have their own containers where the customer can expand the container to reveal the contents... user can easily switch between companies just by clicking on the company container or objects within it."

**Our Answer:** ✅ **YES, Story 1.18 implements exactly this:**
- Dashboard shows ALL companies user belongs to
- Hierarchical structure (parent → children)
- Expandable containers
- Company switching by clicking containers (no separate dropdown)
- KPI components at top summarize selected company data

---

### **Question 2: How Does Company Admin Send Invitations?**

**Your Vision:**
> "In the Header of the company container... have a user icon and when clicked displays a list of the users in their company and in that view they can add or remove users or edit the users Role... as long as they have a role that is equal or higher than the role they are changing."

**Our Answer:** ✅ **YES, Story 1.18 implements exactly this:**
- **User icon (👥) in company container header**
- Click → Opens team panel for THAT company
- Admins see "Invite User" button
- Admins can edit roles (equal or lower than theirs)
- Non-admins see read-only view
- Contextual to each company (company-specific team list)

**Integration with Story 1.16:**
- Story 1.18: Provides company header with user icon and team panel
- Story 1.16: Provides invitation modal and user role editing logic
- Together: Complete team management experience

---

### **Question 3: Do We Need Dashboard Framework in Epic 1?**

**Your Insight:**
> "Based on what I am seeing is we need to have the framework for the dashboard included in this sprint to achieve our User Journey goals... I am hoping by the completion of Wave 3 we have the dashboard framework in place to enable the goals in Wave 3."

**Our Answer:** ✅ **ABSOLUTELY CORRECT:**
- Journey 2 (Team Invitations) REQUIRES company header with user icon
- Journey 4 (Company Switching) REQUIRES container hierarchy system
- Dashboard framework is NOT "nice-to-have" - it's **critical infrastructure** for Epic 1
- **Updated Wave 3 includes Story 1.18** (Dashboard Framework)
- By Wave 3 completion, dashboard framework is in place and Journey 2 & 4 are achievable

**Without dashboard framework:**
- ❌ Can't demonstrate company switching (no containers)
- ❌ Can't send invitations (no user icon in company header)
- ❌ User journeys are incomplete (missing critical UI)

**With dashboard framework:**
- ✅ Company switching is intuitive (click containers)
- ✅ Team management is contextual (user icon in company header)
- ✅ User journeys are complete and testable
- ✅ Foundation for Epic 2 (Events & Forms) is ready

---

### **Question 4: Does This Approach Align with What We're Trying to Achieve?**

**Your Question:**
> "Do my thoughts align with what we are trying to achieve?"

**Our Answer:** ✅ **100% YES - Your thoughts are EXACTLY aligned:**

1. ✅ **Backend-First Strategy:** You said "we have got most of the backend functionality work to ensure that when we start building the frontend we have the components already" - This is precisely our approach.

2. ✅ **User-Journey-Centric:** You identified that Journey 2 and Journey 4 can't be completed without dashboard framework - This is user-journey-centric thinking.

3. ✅ **Dashboard as Container System:** Your vision of the dashboard as a container architecture is the RIGHT mental model - not just a page, but the central navigation paradigm.

4. ✅ **Contextual Team Management:** Putting team management in company header (user icon) is brilliant UX - it's where users expect it to be.

5. ✅ **Intuitive Company Switching:** Switching by clicking containers (not a separate dropdown) is more intuitive and aligns with the container mental model.

**Your architectural thinking is spot-on, Anthony!**

---

## 📈 Impact on Timeline

**Original Epic 1 Timeline:** 12 weeks  
**Updated Epic 1 Timeline:** **13 weeks** (+1 week for dashboard framework)

**Why +1 Week?**
- Story 1.18 is substantial (~1,200 lines, complex UI)
- Dashboard framework is critical infrastructure (can't rush)
- Better to allocate adequate time than compromise quality

**Trade-off Analysis:**
- ✅ **Worth it:** Dashboard framework enables Journey 2 & 4 properly
- ✅ **Foundation for Epic 2:** Events and forms will navigate through dashboard
- ✅ **Better UX:** Company switching and team management are intuitive
- ✅ **No rework:** Building it right the first time (not retrofitting later)

**Alternative (NOT Recommended):**
- Defer dashboard to Epic 2 → Journey 2 & 4 incomplete, user confusion
- Build minimal dashboard now → Rework later (waste of time)
- Rush dashboard in Wave 3 → Poor quality, bugs, frustrated users

**Recommendation:** ✅ **Accept +1 week, build dashboard framework properly in Wave 3**

---

## 🎯 Updated Wave 3 Goals

**Wave 3 (Weeks 8-11): Team Collaboration + Dashboard Framework**

**Sprint 8 (Week 8):**
- Story 1.6: Team Invitation API (Backend)
- Story 1.7: Invitation Acceptance API (Backend)

**Sprint 9 (Week 9):**
- Story 1.11: Company Switching API (Backend)
- Story 1.18: Dashboard APIs (Backend)
  - `GET /api/dashboard/companies` (hierarchical)
  - `GET /api/dashboard/kpis` (aggregated KPIs)
  - `POST /api/companies/switch` (context switching)

**Sprint 10 (Week 10):**
- Story 1.18: Dashboard Framework (Frontend)
  - Dashboard layout (KPIs + company containers)
  - Company hierarchy display
  - Expand/collapse containers
  - Company selection and switching

**Sprint 11 (Week 11):**
- Story 1.18: Team Management Panel (Frontend)
  - User icon in company header
  - Team panel (user list, contextual to company)
  - Role-based access (admin vs non-admin)
- Story 1.16: Invitation & Role Editing (Frontend)
  - Invitation modal (triggered from team panel)
  - User role editing (admin only)

**Wave 3 Deliverable:**
✅ **Dashboard Framework Complete**
- Users can see all their companies
- Users can switch between companies by clicking containers
- Admins can manage teams via user icon in company header
- KPIs update dynamically based on selected company
- **Journey 2 & 4 Complete and Testable!**

---

## 📋 Next Steps (Awaiting Your Approval)

1. **Review Story 1.18** (`docs/stories/story-1.18.md`)
   - Confirm dashboard layout matches your vision
   - Confirm team management location (user icon in company header)
   - Confirm company switching approach (click containers)

2. **Approve Updated Wave 3**
   - Accepts +1 week for dashboard framework (13 weeks total)
   - Includes Story 1.18 (Dashboard Framework)
   - Enables Journey 2 & 4 properly

3. **Update All Documentation**
   - Update `EPIC-1-USER-JOURNEY-IMPLEMENTATION-PLAN.md`
   - Update `EPIC-1-STORY-TO-JOURNEY-MAPPING.md`
   - Update `EPIC-1-STORIES-SUMMARY.md` (add Story 1.18)

4. **Start Wave 1, Sprint 1**
   - Begin backend authentication (Stories 1.1, 1.2, 1.3)
   - Validate APIs via Postman
   - Proceed through waves as planned

---

## ✅ Recommendation

**Approve Story 1.18 (Dashboard Framework) and Updated Wave 3**

**Why this is the RIGHT decision:**
1. ✅ **Aligns with your vision** (container architecture, team management location)
2. ✅ **Enables Journey 2 & 4 properly** (not half-baked)
3. ✅ **Backend-first approach maintained** (APIs before frontend)
4. ✅ **User-journey-centric** (dashboard is critical for user experience)
5. ✅ **Foundation for Epic 2** (events/forms navigate through dashboard)
6. ✅ **No rework needed** (building it right the first time)

**User is the winner:** Dashboard framework provides intuitive navigation, contextual team management, and seamless company switching.

---

**Prepared by:** Sarah (Product Owner)  
**Date:** 2025-10-17  
**Status:** ✅ Awaiting Anthony's Approval

---

## 💬 Questions for Anthony

1. **Does Story 1.18 match your vision?** (Dashboard layout, company containers, user icon)
2. **Is +1 week acceptable for dashboard framework?** (13 weeks total for Epic 1)
3. **Any adjustments needed to the dashboard design?**
4. **Ready to proceed with updated Wave 3?**

**Awaiting your feedback and approval!** 🚀

