# Epic 1: Ready to Start - Final Summary

**Date:** 2025-10-17  
**For:** Anthony Keevy  
**Status:** ✅ All Feedback Addressed - Ready to Begin Sprint 1

---

## 🎉 All Your Feedback Implemented!

### **✅ 1. Unlimited Hierarchy with Sliding Window**
- Database: Unlimited depth (no constraints)
- UI: Display 5 levels at a time (sliding window)
- Breadcrumbs: Show full path (always visible, clickable)
- "..." indicators: Show hidden levels above/below
- **Updated in:** Story 1.18

### **✅ 2. Billing & Company Management Deferred to Epic 2**
- Epic 1: View hierarchy, switch companies, team invitations
- Epic 2: Add companies, edit hierarchy, billing, invoicing
- **Updated in:** Story 1.18 (Notes)

### **✅ 3. Starting from Story 1.9 (Backend Complete)**
- Stories 1.1-1.8: ✅ DONE (Backend + Testing)
- Stories 1.9-1.18: 🔜 TODO (Frontend + Polish)
- Timeline: **7 weeks** (not 13 weeks)
- **Updated in:** EPIC-1-REVISED-PLAN-STARTING-FROM-1.9.md

### **✅ 4. Onboarding as Modal on Dashboard**
- Dashboard loads first (empty state)
- Onboarding modal pops up (overlay)
- Cannot dismiss (required)
- After completion: Modal closes → Company appears
- **Updated in:** Story 1.14

### **✅ 5. Dashboard is Post-Onboarding Destination**
- Confirmed: Dashboard is central hub
- User sees company on dashboard after onboarding
- Empty state: "Create your first event!"
- **Confirmed in:** All documentation

---

## 📊 Revised Timeline (7 Weeks from Today)

| Week | Sprint | Stories | Goal |
|------|--------|---------|------|
| **1** | Sprint 1 | 1.10, 1.11, 1.12, 1.13 | **Complete remaining backend APIs** |
| **2** | Sprint 2 | 1.9 | Frontend authentication (signup & login) |
| **3** | Sprint 3 | 1.14, 1.15 | Frontend onboarding & password reset |
| **4-5** | Sprint 4 | 1.18 (Part 1) | Dashboard framework & containers |
| **5-6** | Sprint 5 | 1.18 (Part 2), 1.16 | Team management UI |
| **7** | Sprint 6 | 1.17 | UX polish & launch prep |

**Launch Date:** ~7 weeks (mid-December 2025)

---

## 🚀 Sprint 1 (This Week): Backend Support Services

### **Goal:** Complete all remaining backend APIs so frontend can consume them

**Stories to Complete:**

### **Story 1.10: Enhanced ABR Search (~2 days)**
**What:** Australian Business Register search with auto-detection
**Endpoints:**
- `POST /api/companies/search-abr`
- Request: `{ "query": "12 345 678 901" }`
- Response: Company name, ABN, ACN, address

**Implementation:**
- Integrate ABR API (ASIC business names)
- Auto-detect search type (ABN, ACN, or Name)
- Cache results (Redis, 24-hour TTL)
- Return top 10 matches

**Testing:**
- Unit tests: Auto-detection logic
- Integration tests: ABR API calls
- Cache tests: Verify Redis caching

---

### **Story 1.11: Company Switching API (~1 day)**
**What:** APIs for company hierarchy and context switching
**Endpoints:**
- `GET /api/dashboard/companies` (hierarchical, unlimited depth)
- `POST /api/companies/switch` (update active company in session)

**Implementation:**
- Recursive SQL query (CTE) to fetch hierarchy
- Return nested company structure with full parent-child relationships
- Update user session with active company ID
- Return: `{ companyId, companyName, relationshipType, parentCompanyId, childCompanies[], eventCount, formCount, hierarchyLevel }`

**Testing:**
- Unit tests: Recursive hierarchy logic
- Integration tests: API endpoints
- Multi-tenancy tests: Data isolation

---

### **Story 1.12: Validation Engine (~1 day)**
**What:** Country-specific validation rules (Australian format)
**Endpoints:**
- `POST /api/validation/validate`
- Request: `{ "field": "phone", "value": "+61412345678", "country": "AU" }`
- Response: `{ "valid": true, "message": "", "formatted": "+61 412 345 678" }`

**Validation Rules:**
- Phone numbers: Australian format (+61...)
- Addresses: Australian states/postcodes
- ABN: 11-digit Australian Business Number
- ACN: 9-digit Australian Company Number
- Email: RFC 5322 compliance

**Implementation:**
- Query `ValidationRule` table (country-specific rules)
- Regex validation for phone, ABN, ACN
- Address validation (states: NSW, VIC, QLD, SA, WA, TAS, NT, ACT)
- Return user-friendly error messages

**Testing:**
- Unit tests: Each validation rule
- Integration tests: API endpoint
- Edge cases: Invalid formats, null values

---

### **Story 1.13: Configuration Service (~1 day)**
**What:** Runtime-changeable business rules and settings
**Endpoints:**
- `GET /api/config/settings` (all settings)
- `GET /api/config/settings/:key` (single setting)
- `GET /api/config/validation-rules` (validation rules)

**Implementation:**
- Query `AppSetting` table
- Query `ValidationRule` table
- Cache with 5-minute TTL (Redis)
- Filter by `IsActive = 1` and `IsDeleted = 0`
- Return: `{ settingKey, settingValue, settingType, description }`

**Settings Categories:**
- Authentication (JWT expiry, password rules)
- Validation (phone format, ABN/ACN rules)
- Email (verification timeout, templates)
- Invitation (expiry duration, roles allowed)
- Security (max login attempts, rate limits)

**Testing:**
- Unit tests: Query logic
- Integration tests: API endpoints
- Cache tests: TTL verification

---

## ✅ Sprint 1 Deliverable (End of Week 1)

**Goal:** All backend APIs complete and ready for frontend consumption

**Deliverables:**
- ✅ Story 1.10: ABR search endpoint functional (tested via Postman)
- ✅ Story 1.11: Company hierarchy API returns unlimited depth (tested via Postman)
- ✅ Story 1.12: Validation engine validates AU phone/address/ABN (tested via Postman)
- ✅ Story 1.13: Configuration service returns runtime settings (tested via Postman)

**Validation:**
- All endpoints tested via Postman/curl
- Unit tests passing (>80% coverage)
- Integration tests passing
- Documentation updated (API specs)

**After Sprint 1:**
- Frontend team can start Story 1.9 (Authentication UI)
- No backend blockers for frontend work

---

## 📚 Updated Documentation

### **Key Documents:**

1. **EPIC-1-REVISED-PLAN-STARTING-FROM-1.9.md**
   - Stories 1.1-1.8 marked complete
   - Stories 1.9-1.18 breakdown
   - 7-week timeline

2. **EPIC-1-ANTHONY-FEEDBACK-CONFIRMED.md**
   - All 5 feedback points addressed
   - Unlimited hierarchy with sliding window
   - Billing deferred to Epic 2
   - Onboarding as modal
   - Dashboard as destination

3. **Story 1.18: Dashboard Framework**
   - Unlimited hierarchy (database)
   - Sliding window (5-level UI display)
   - Breadcrumb navigation
   - Team management (user icon in header)
   - KPI dashboard

4. **Story 1.14: Onboarding Modal**
   - Changed from full-page to modal
   - Appears on empty dashboard
   - Cannot dismiss (required)
   - After completion: Company appears

---

## 🎯 Epic 1 Success Criteria

**When Epic 1 is complete, users can:**

1. ✅ Sign up and verify email (Journey 1 - Step 1)
2. ✅ Log in (Journey 1 - Step 2)
3. ✅ Complete onboarding modal (Journey 1 - Step 3)
4. ✅ See company on dashboard (Journey 1 - Step 4)
5. ✅ Invite team members (Journey 2)
6. ✅ Accept invitations (Journey 2)
7. ✅ Switch between companies (Journey 4)
8. ✅ Reset forgotten passwords (Journey 3)
9. ✅ View unlimited company hierarchy (sliding window display)
10. ✅ Manage team (user icon in company header)

**What users CANNOT do in Epic 1 (deferred to Epic 2):**
- ❌ Add additional companies (after first from onboarding)
- ❌ Edit company hierarchy (move branches, change parents)
- ❌ Access billing/invoicing
- ❌ Create events or forms (Epic 2 scope)

---

## 🚀 Ready to Start!

**Next Actions:**

1. **This Week (Sprint 1):**
   - Start Story 1.10 (ABR Search)
   - Start Story 1.11 (Company Switching API)
   - Start Story 1.12 (Validation Engine)
   - Start Story 1.13 (Configuration Service)

2. **End of Week 1:**
   - All backend APIs complete
   - Tested via Postman
   - Documentation updated
   - Ready for frontend work

3. **Week 2 (Sprint 2):**
   - Start Story 1.9 (Frontend Authentication)
   - Build signup and login pages
   - Integrate with backend APIs (1.1, 1.2, 1.3)

**You have a clear path forward!** 🎉

---

**Prepared by:** Sarah (Product Owner)  
**Date:** 2025-10-17  
**Status:** ✅ Ready to Begin Sprint 1

**Let's build this! 🚀**

