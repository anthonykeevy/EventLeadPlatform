# Story 1.6: Team Invitation System

Status: Ready for Review

## Story

As a company admin,
I want to invite team members to my company via email,
so that I can build my team on the EventLead platform.

## Acceptance Criteria

1. **AC-1.6.1**: Protected endpoint for sending invitations (requires company_admin role)
2. **AC-1.6.2**: Invitation created with email, role, and company association
3. **AC-1.6.3**: Invitation token generated (valid 7 days)
4. **AC-1.6.4**: Team invitation email sent automatically
5. **AC-1.6.5**: Cannot invite email that already belongs to company
6. **AC-1.6.6**: Admin can specify role (company_admin or company_user)
7. **AC-1.6.7**: Admin can resend invitation if pending
8. **AC-1.6.8**: Admin can cancel pending invitation
9. **AC-1.6.9**: Admin can view all company invitations (pending, accepted, expired)
10. **AC-1.6.10**: All invitation events logged to audit tables

## Tasks / Subtasks

- [x] **Task 1: Create Invitation Model/Schema** (AC: 1.6.2, 1.6.6)
  - [x] Verify ref.Invitation table exists (from Story 0.1)
  - [x] Create invitation schemas (Pydantic)
  - [x] InvitationRequest (email, role)
  - [x] InvitationResponse
  - [x] Test: Schemas validate correctly

- [x] **Task 2: Create Send Invitation Endpoint** (AC: 1.6.1, 1.6.2, 1.6.3, 1.6.5)
  - [x] Add POST /api/companies/{company_id}/invite to companies router
  - [x] Require company_admin role
  - [x] Verify admin belongs to company
  - [x] Check email not already in company
  - [x] Create Invitation record
  - [x] Generate invitation token (7-day expiry)
  - [x] Send invitation email
  - [x] Test: Admin can send invitation
  - [x] Test: Non-admin cannot send invitation
  - [x] Test: Cannot invite existing member

- [x] **Task 3: Send Invitation Email** (AC: 1.6.4)
  - [x] Update team_invitation.html template
  - [x] Include invitation URL with token
  - [x] Include company name and inviter name
  - [x] Include role information
  - [x] Send via email service
  - [x] Test: Email sent successfully

- [x] **Task 4: Create Resend Invitation Endpoint** (AC: 1.6.7)
  - [x] Add POST /api/companies/{company_id}/invitations/{invitation_id}/resend
  - [x] Require company_admin role
  - [x] Verify invitation is pending
  - [x] Extend token expiry (new 7-day window)
  - [x] Resend email
  - [x] Test: Invitation resent successfully

- [x] **Task 5: Create Cancel Invitation Endpoint** (AC: 1.6.8)
  - [x] Add DELETE /api/companies/{company_id}/invitations/{invitation_id}
  - [x] Require company_admin role
  - [x] Mark invitation as cancelled
  - [x] Invalidate token
  - [x] Test: Invitation cancelled

- [x] **Task 6: Create List Invitations Endpoint** (AC: 1.6.9)
  - [x] Add GET /api/companies/{company_id}/invitations
  - [x] Require company_admin role
  - [x] Return all company invitations
  - [x] Filter by status (pending, accepted, expired, cancelled)
  - [x] Pagination support
  - [x] Test: Invitations listed correctly

- [x] **Task 7: Implement Invitation Token** (AC: 1.6.3)
  - [x] Generate secure token
  - [x] Store in UserInvitation table
  - [x] Link to Invitation record
  - [x] 7-day expiry
  - [x] Test: Token generated and stored

- [x] **Task 8: Audit Logging** (AC: 1.6.10)
  - [x] Log invitation sent events
  - [x] Log invitation resent events
  - [x] Log invitation cancelled events
  - [x] Test: All events logged

- [x] **Task 9: Testing** (AC: All)
  - [x] Integration tests: Complete invitation flow
  - [x] Security tests: Role requirements
  - [x] Validation tests: Email validation

- [x] **Task 10: Documentation** (AC: All)
  - [x] Document invitation flow
  - [x] Update API documentation

## Dev Notes

**Invitation Flow:**
```
1. Company admin invites user by email
2. System creates Invitation record
3. System generates invitation token
4. System sends invitation email
5. Invitee clicks link in email
6. Invitee lands on invitation acceptance page
7. If invitee has account: Accept invitation (Story 1.7)
8. If invitee is new: Signup + accept invitation (Story 1.7)
```

### References

- [Story 1.3: RBAC Middleware](docs/stories/story-1.3.md)
- [Story 1.5: First-Time Onboarding](docs/stories/story-1.5.md)
- [Story 0.3: Email Service](docs/stories/story-0.3.md)

## Dev Agent Record

### Context Reference

- [Story Context 1.6](../story-context-1.6.xml)

### Agent Model Used

- Claude Sonnet 4.5 (Amelia - Developer Agent)

### Completion Notes List

1. **Invitation Schemas**: Created comprehensive Pydantic models for all invitation operations including send, list, resend, and cancel responses.

2. **Invitation Service**: Complete business logic module (`invitation_service.py`) with:
   - Secure token generation (64-character URL-safe tokens)
   - Duplicate prevention (email already in company check)
   - 7-day expiry management
   - Resend tracking with resend_count
   - Status validation for operations

3. **Router Endpoints**: Four invitation endpoints with role-based authorization:
   - POST /api/companies/{company_id}/invite
   - GET /api/companies/{company_id}/invitations (with filtering/pagination)
   - POST /api/companies/{company_id}/invitations/{invitation_id}/resend
   - DELETE /api/companies/{company_id}/invitations/{invitation_id}

4. **RBAC Integration**: Added `require_company_admin_for_company()` helper to enforce both role and company membership requirements.

5. **Email Integration**: Extended email service with `send_team_invitation_email()` method using existing team_invitation.html template.

6. **Audit Logging**: All invitation events logged to audit.ActivityLog:
   - INVITATION_SENT: Captures invitation details
   - INVITATION_RESENT: Tracks resend count and new expiry
   - INVITATION_CANCELLED: Records cancellation reason

7. **Comprehensive Testing**: Created `test_team_invitations.py` with 20+ tests covering:
   - Authentication and authorization requirements
   - Role-based access control
   - Invitation sending with token generation
   - Email delivery (AC-1.6.4 verified via service call)
   - Duplicate member prevention
   - Role specification
   - Resending with expiry extension
   - Cancellation workflow
   - Invitation listing with filters
   - Complete audit trail verification

8. **Security Features**:
   - Cryptographically secure tokens (secrets.token_urlsafe)
   - Role-based endpoint protection
   - Company membership validation
   - Multi-tenant data isolation
   - Token expiry enforcement

9. **Documentation**: Complete technical guide at `docs/technical-guides/team-invitation-guide.md` covering:
   - API endpoint specifications
   - Token security details
   - Role-based access control
   - Email integration
   - Database schema
   - Audit logging
   - Frontend integration examples
   - Troubleshooting guide

### File List

**Created Files:**
- `backend/modules/companies/invitation_service.py` - Core invitation business logic
- `backend/tests/test_team_invitations.py` - Comprehensive integration tests
- `docs/technical-guides/team-invitation-guide.md` - Complete technical documentation

**Modified Files:**
- `backend/modules/companies/schemas.py` - Added invitation request/response schemas
- `backend/modules/companies/router.py` - Added 4 invitation endpoints
- `backend/services/email_service.py` - Added team invitation email method
- `backend/common/rbac.py` - Added company admin verification helper

