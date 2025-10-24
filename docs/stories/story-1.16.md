# Story 1.16: Frontend Team Management UI

**Status:** Ready  
**Priority:** High  
**Estimated Lines:** ~700  
**Dependencies:** Story 1.6 (Backend Invitations), Story 1.7 (Invitation Acceptance), Story 1.9 (Auth Context)

---

## Story

As a **Company Admin**,
I want **a team management dashboard to invite users, view invitations, and manage team members**,
so that **I can build my team and collaborate effectively**.

---

## Acceptance Criteria

### **AC-1.16.1: Team Management Dashboard**
- System provides `/team` route (company_admin only)
- Dashboard displays:
  - Team members list (name, email, role, status)
  - Pending invitations list (email, role, sent date, status)
  - "Invite User" button
- System fetches team data: `GET /api/companies/{company_id}/users`
- System fetches invitations: `GET /api/companies/{company_id}/invitations`

### **AC-1.16.2: Invite User Modal**
- System displays modal when "Invite User" clicked
- Form includes: First Name, Last Name, Email, Role (dropdown)
- System validates all fields before submission
- System calls `POST /api/companies/{company_id}/invite` endpoint
- System refreshes invitation list on success
- System displays success toast: "Invitation sent to [email]"

### **AC-1.16.3: Invitation List with Actions**
- System displays pending invitations with:
  - Invited user details (name, email)
  - Assigned role
  - Sent date
  - Status badge (Pending, Accepted, Expired, Cancelled)
  - Actions: Resend, Cancel
- System calls `POST /api/companies/{company_id}/invitations/{id}/resend` for resend
- System calls `DELETE /api/companies/{company_id}/invitations/{id}` for cancel
- System disables actions for non-pending invitations

### **AC-1.16.4: Invitation Acceptance Page (Invitee)**
- System provides `/invitations/:token` route (public)
- System fetches invitation details: `GET /api/invitations/{token}`
- System displays invitation details: Company name, assigned role, inviter name
- Form includes: First Name (pre-filled), Last Name (pre-filled), Email (read-only), Password, Confirm Password
- System calls `POST /api/invitations/{token}/accept` endpoint
- System redirects to onboarding (simplified, no company setup) on success

### **AC-1.16.5: Role-Based Access Control**
- System checks user role before allowing access to `/team`
- If user is not `company_admin`: Display "Access Denied" message
- System uses `useAuth` hook to check role

### **AC-1.16.6: Mobile Responsive**
- System optimizes for mobile devices
- Responsive table layout (stacked on mobile)
- Touch-friendly buttons

---

## Tasks

- [ ] Create `TeamManagement.tsx` page component
- [ ] Create `TeamMembersList.tsx` component
- [ ] Create `InvitationList.tsx` component
- [ ] Create `InviteUserModal.tsx` component
- [ ] Create `InvitationAcceptance.tsx` page component
- [ ] Integrate with backend endpoints (Story 1.6, 1.7)
- [ ] Add role-based access control
- [ ] Add status badges (using lookup values from Story 1.12)
- [ ] Add error handling
- [ ] Test on mobile devices
- [ ] Write component tests

---

## References

- [Source: docs/tech-spec-epic-1.md#AC-5, AC-6 (Lines 2636-2664)]
- [Source: docs/stories/story-1.6.md] - Backend invitation endpoints
- [Source: docs/stories/story-1.7.md] - Backend invitation acceptance

