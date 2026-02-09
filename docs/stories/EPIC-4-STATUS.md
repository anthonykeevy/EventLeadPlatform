# Epic 4 Status - Team Collaboration (Advanced / Future)

**Epic ID:** Epic 4  
**Status:** ⏳ Pending (deferred; PRD “team collaboration” foundations exist)  
**Created:** 2026-02-06  
**Product Manager:** John (PM Agent)  
**Developer:** Developer Agent  

---

## ✅ PRD Reality Check: “Team Collaboration” Scope

Per `docs/prd.md` (Section **4. Team Collaboration & Invitations**), “team collaboration” for MVP means:
- Company Admin invites users via email (first name, last name, email, role)
- Invitation email with secure token link
- Pending invitations list (can cancel)
- Assign role during invitation (Company Admin or Company User)
- User management screen (list users, change roles, remove users)
- Role-based UI rendering (show/hide features based on role)
- Expired invitation handling (7-day expiry + resend)

**Interpretation:** This scope is **invitations + roles + user management**, not “multi-user live editing”.

These foundations already exist in the codebase (Epic 1/2: auth/onboarding + companies/RBAC + invitations modules).  
So Epic 4 is **not the next delivery-critical epic** unless we explicitly choose to add *advanced* collaboration features.

---

## 🎯 Epic 4 Objective (Advanced Collaboration)

If/when we implement Epic 4, it should focus on **collaboration beyond invitations**, such as:
- Concurrency controls for the builder (edit locks / conflict-safe saves)
- Comments / mentions / review notes on forms
- Notifications (e.g., “publish requested”, “changes requested”)
- Activity feed improvements (who changed what, when) beyond baseline audit logs

---

## 🧭 Scope Boundary (Epic 4)

### In Scope
- Advanced collaboration behaviors (above), if approved.

### Out of Scope
- Unified Form Workspace (better aligned to Epic 5 Review/Publishing UX).
- Preview/Test thresholds, publish flow, public URL generation (Epic 5).
- Payments/invoicing (Epic 6).

---

## ✅ Epic 4 Done Criteria (Draft)

- [ ] Collaboration feature set is explicitly chosen and implemented (no “accidental” scope growth).
- [ ] UAT proves collaboration workflows are safe (no lost work, no permission bypass).
- [ ] Documentation updated (status + workflow + UAT guides).

---

*Epic 4 Status Document - Updated to align with PRD scope*  
*Last Updated: 2026-02-06*

