# Epic 1: Dashboard Framework - Visual Summary

**Date:** 2025-10-17  
**For:** Anthony Keevy - Quick Reference

---

## 🎯 Your Vision → Our Implementation

### **Dashboard Container Architecture**

```
┌────────────────────────────────────────────────────────────────────┐
│ EVENT LEAD PLATFORM                          [Profile] [Settings]  │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📊 KPI DASHBOARD (Selected Companies)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Total Forms  │  │ Total Leads  │  │Active Events │             │
│  │     12       │  │     145      │  │      5       │             │
│  │  ↑ +3 this   │  │  ↑ +23 this  │  │  → Same as   │             │
│  │     week     │  │     week     │  │   last week  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
├────────────────────────────────────────────────────────────────────┤
│  MY COMPANIES                                                      │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│  ┃ 🏢 ACME Corporation                          [👥] [⚙️] [▼] ┃   │
│  ┃ Head Office · 3 Events · 7 Forms                            ┃   │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   │
│    ├─ 📊 Trade Show 2025 (3 forms, 89 leads)                       │
│    ├─ 📊 Expo Sydney 2025 (2 forms, 34 leads)                      │
│    ├─ 📊 Conference Melbourne (2 forms, 22 leads)                  │
│    │                                                                │
│    ├─ 🏢 ACME Sydney                            [👥] [▼]           │
│    │   └─ 📊 Sydney Tech Expo (1 form, 12 leads)                   │
│    │                                                                │
│    └─ 🏢 ACME Melbourne                         [👥] [▼]           │
│        └─ 📊 Melbourne Business Summit (2 forms, 45 leads)         │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │ 🏢 XYZ Consulting                          [👥] [⚙️] [▼]  │    │
│  │ Freelancer · 1 Event · 1 Form                             │    │
│  └───────────────────────────────────────────────────────────┘    │
│    └─ 📊 Client Workshop (1 form, 8 leads)                         │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │ 🏢 ABC Events                              [👥] [▼]        │    │
│  │ Branch · 2 Events · 3 Forms                               │    │
│  └───────────────────────────────────────────────────────────┘    │
│    ├─ 📊 Corporate Conference (2 forms, 67 leads)                  │
│    └─ 📊 Annual Gala (1 form, 23 leads)                            │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘

LEGEND:
━━━━ = Active/Selected Company (highlighted border)
──── = Non-active Company
[👥] = Team Management (YOUR SUGGESTION: Click to manage users)
[⚙️] = Company Settings (Admin only)
[▼] = Expand/Collapse Container
📊 = Event (click to view/edit event and forms)
```

---

## 🎯 Key Features

### **1. Company Switching (YOUR SUGGESTION)**
**Click Container → Switches Context:**
- User clicks "ACME Corporation" → Active (highlighted border)
- KPIs update to show ACME data only (<3 seconds)
- User clicks "XYZ Consulting" → Switches to XYZ
- KPIs update to show XYZ data
- **No separate dropdown needed!**

---

### **2. Team Management (YOUR SUGGESTION)**
**User Icon [👥] in Company Header:**

```
User clicks [👥] icon → Team Panel Opens:

┌─────────────────────────────────────────────────────────────┐
│ ACME Corporation - Team Members                      [✕]    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  👤 John Smith                                               │
│      john@acme.com · Company Admin                   [Edit]  │
│                                                              │
│  👤 Jane Doe                                                 │
│      jane@acme.com · Company User                    [Edit]  │
│                                                              │
│  👤 Bob Johnson                                              │
│      bob@acme.com · Company User                     [Edit]  │
│                                                              │
│  ⏳ alice@example.com                                        │
│      Invitation Pending (Sent 2 days ago)           [Resend]│
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  [+ Invite User]                                    [Close]  │
└─────────────────────────────────────────────────────────────┘
```

**Admin Actions:**
- Click [+ Invite User] → Opens invitation modal (Story 1.16)
- Click [Edit] → Opens role editor (if role is equal or lower than admin's)
- Click [Resend] → Resends invitation email

**Non-Admin View:**
- Same panel, but NO [Edit], NO [Invite User], NO [Resend]
- Read-only: See who's on the team

---

### **3. Hierarchical Company Structure**
**Parent-Child Relationships:**
```
🏢 ACME Corporation (Head Office)  ← Parent
  ├─ 🏢 ACME Sydney (Branch)       ← Child
  ├─ 🏢 ACME Melbourne (Branch)    ← Child
  └─ 🏢 ACME Brisbane (Branch)     ← Child
```

**Expand/Collapse:**
- Click [▼] → Expands to show children + events
- Click [▲] → Collapses (hides children)

---

### **4. KPI Dashboard (Selected Companies)**
**Updates Dynamically:**
- User selects ACME Corporation → KPIs show ACME data
- User selects XYZ Consulting → KPIs show XYZ data
- User selects ACME + XYZ → KPIs show aggregated data (future)

**KPI Cards:**
1. **Total Forms:** Count of published forms
2. **Total Leads:** Count of lead submissions
3. **Active Events:** Count of active events

**Trend Indicators:**
- ↑ +12% this week (green)
- ↓ -5% this week (red)
- → Same as last week (gray)

---

## 🗺️ User Journey Flows

### **Journey 2: Team Invitations**
```
1. Admin logs in
   ↓
2. Dashboard loads → Sees ACME Corporation
   ↓
3. Admin clicks [👥] in ACME header (YOUR SUGGESTION)
   ↓
4. Team panel opens → Shows current team
   ↓
5. Admin clicks [+ Invite User]
   ↓
6. Invitation modal opens (Story 1.16)
   ↓
7. Admin enters email, name, role → Sends invitation
   ↓
8. Invitee receives email → Accepts → Joins team
   ↓
9. Admin sees invitee in team panel (status: Active)
```

**✅ Dashboard Framework Enables:** User icon in company header (contextual team management)

---

### **Journey 4: Multi-Company User**
```
1. User logs in
   ↓
2. Dashboard loads → Sees all companies (ACME, XYZ, ABC)
   ↓
3. User clicks ACME container (YOUR SUGGESTION)
   ↓
4. ACME highlights (active state)
   ↓
5. KPIs update to show ACME data (<3 seconds)
   ↓
6. User clicks XYZ container
   ↓
7. XYZ becomes active, ACME loses active state
   ↓
8. KPIs update to show XYZ data (<3 seconds)
   ↓
9. User clicks [👥] in XYZ header → Sees XYZ team (different from ACME)
```

**✅ Dashboard Framework Enables:** Company switching by clicking containers + contextual team panels

---

## 📊 Updated Wave 3 (Includes Dashboard Framework)

**Wave 3: Team Collaboration + Dashboard Framework (Weeks 8-11)**

| Week | Sprint | Stories | Deliverable |
|------|--------|---------|-------------|
| 8 | Sprint 8 | 1.6, 1.7 | Backend: Team Invitation APIs |
| 9 | Sprint 9 | 1.11, **1.18** (Backend) | Backend: Company Switching + Dashboard APIs |
| 10 | Sprint 10 | **1.18** (Frontend) | Frontend: Dashboard Containers + KPIs |
| 11 | Sprint 11 | **1.18** (Team Panel) + 1.16 | Frontend: Team Management UI + Invitation Modal |

**Wave 3 Deliverable:**
✅ **Dashboard Framework Complete**
✅ **Journey 2 Complete** (Team Invitations via user icon in company header)
✅ **Journey 4 Complete** (Company Switching via container clicks)

---

## ⏱️ Updated Timeline

**Epic 1 Duration:** **13 weeks** (was 12 weeks, +1 week for dashboard framework)

| Wave | Duration | Stories | User Win |
|------|----------|---------|----------|
| Wave 1 | Weeks 1-6 | 1.1, 1.2, 1.3, 1.12, 1.13, 1.10, 1.5, 1.9, 1.14 | ✅ Journey 1: "I can sign up and onboard in <5 minutes!" |
| Wave 2 | Week 7 | 1.4, 1.15 | ✅ Journey 3: "I recovered my account in <2 minutes!" |
| Wave 3 | **Weeks 8-11** | 1.6, 1.7, 1.11, **1.18**, 1.16 | ✅ Journey 2 & 4: "I can manage my team and switch companies seamlessly!" |
| Wave 4 | Weeks 12-13 | 1.8, 1.17 | ✅ Epic 1 Complete: "This platform is polished, secure, and accessible!" |

**Why +1 Week?**
- Dashboard framework is substantial (~1,200 lines)
- Critical infrastructure (can't rush)
- Foundation for Epic 2 (Events & Forms)
- Better to build it right the first time

---

## ✅ Confirmation: Your Vision is Implemented

### **Your Request:**
> "Dashboard will show all companies the user belongs to... hierarchy to the company structure... list of all the top level companies which have their own containers where the customer can expand the container to reveal the contents... user can easily switch between companies just by clicking on the company container or objects within it."

**Our Implementation:** ✅ **Story 1.18 implements exactly this**

---

### **Your Request:**
> "In the Header of the company container... have a user icon and when clicked displays a list of the users in their company and in that view they can add or remove users or edit the users Role with the company as long as they have a role that is equal or higher than the role they are changing."

**Our Implementation:** ✅ **Story 1.18 implements exactly this (user icon [👥] in company header)**

---

### **Your Request:**
> "Based on what I am seeing is we need to have the framework for the dashboard included in this sprint to achieve our User Journey goals... I am hoping by the completion of Wave 3 we have the dashboard framework in place to enable the goals in Wave 3."

**Our Implementation:** ✅ **Wave 3 now includes Story 1.18 (Dashboard Framework)**

---

## 🚀 Next Steps

1. **Approve Story 1.18** (Dashboard Framework & Container System)
2. **Approve Updated Wave 3** (+1 week, includes dashboard framework)
3. **Start Wave 1, Sprint 1** (Backend Authentication: Stories 1.1, 1.2, 1.3)

---

**Your architectural thinking is spot-on, Anthony!** The dashboard framework is the RIGHT approach for Epic 1. 🎉

**Awaiting your approval to proceed!** 🚀

