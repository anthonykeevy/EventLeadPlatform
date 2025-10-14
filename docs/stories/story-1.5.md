# Story 1.5: Team Invitation Management

Status: ContextReadyDraft

## Story

As a **Company Admin**,
I want **to invite team members to join my company with specific roles**,
so that **I can build a collaborative team for event lead generation and management**.

## Acceptance Criteria

1. **AC-5.1:** Company Admin can create invitations for new team members
2. **AC-5.2:** System validates invitation email format and prevents duplicate invitations
3. **AC-5.3:** System generates secure invitation token with 7-day expiration
4. **AC-5.4:** System sends invitation email with secure token link
5. **AC-5.5:** Company Admin can assign specific roles (Company User) to invitations
6. **AC-5.6:** System displays pending invitations with status and expiration
7. **AC-5.7:** Company Admin can resend invitations to pending users
8. **AC-5.8:** Company Admin can cancel pending invitations
9. **AC-5.9:** System logs all invitation activities for audit trail
10. **AC-5.10:** System enforces invitation limits (configurable per company)
11. **AC-5.11:** Invitation emails include company branding and context

## Tasks / Subtasks

- [ ] **Backend Invitation Service** (AC: 5.1, 5.2, 5.3, 5.5, 5.7, 5.8, 5.9, 5.10)
  - [ ] Create `backend/modules/team/router.py` with invitation endpoints
  - [ ] Create `backend/modules/team/service.py` with invitation business logic
  - [ ] Implement invitation creation with role assignment
  - [ ] Implement email validation and duplicate prevention
  - [ ] Generate secure invitation tokens with 7-day expiration
  - [ ] Implement invitation resending functionality
  - [ ] Implement invitation cancellation
  - [ ] Add invitation limits enforcement
  - [ ] Implement comprehensive activity logging

- [ ] **Email Service Integration** (AC: 5.4, 5.11)
  - [ ] Create invitation email template in `backend/templates/emails/team_invitation_email.html`
  - [ ] Implement async email sending for invitations
  - [ ] Configure secure invitation link with token parameter
  - [ ] Add company branding and context to invitation emails
  - [ ] Implement email delivery tracking and error handling

- [ ] **Frontend Team Management** (AC: 5.1, 5.6, 5.7, 5.8)
  - [ ] Create `frontend/features/team/components/TeamManagement.tsx`
  - [ ] Create `frontend/features/team/components/InvitationList.tsx`
  - [ ] Create `frontend/features/team/components/InviteUserModal.tsx`
  - [ ] Implement invitation creation form with role selection
  - [ ] Implement pending invitations display with status
  - [ ] Add resend and cancel functionality for invitations
  - [ ] Implement real-time updates for invitation status

- [ ] **Role Management** (AC: 5.5)
  - [ ] Implement role validation for invitations
  - [ ] Add role selection dropdown with available roles
  - [ ] Implement role-based invitation permissions
  - [ ] Add role description and permissions display
  - [ ] Implement role assignment validation

- [ ] **Token Management** (AC: 5.3, 5.7, 5.8)
  - [ ] Create invitations table with audit trail
  - [ ] Implement token storage with expiration timestamp
  - [ ] Add invitation status tracking (pending, accepted, expired, cancelled)
  - [ ] Implement token regeneration for resend functionality
  - [ ] Add invitation cleanup for expired tokens

- [ ] **RBAC Integration** (AC: 5.1, 5.6, 5.7, 5.8)
  - [ ] Implement Company Admin role verification for invitation management
  - [ ] Add role-based access control for team management features
  - [ ] Implement company isolation for invitation management
  - [ ] Add permission checks for invitation operations

- [ ] **Database Schema Implementation** (AC: 5.3, 5.9)
  - [ ] Create invitations table with proper constraints
  - [ ] Add audit trail fields (CreatedDate, CreatedBy, UpdatedDate, UpdatedBy)
  - [ ] Implement proper foreign key relationships to User and Company tables
  - [ ] Add indexes for performance optimization
  - [ ] Create activity logging tables for invitation events

- [ ] **Invitation Limits and Validation** (AC: 5.2, 5.10)
  - [ ] Implement configurable invitation limits per company
  - [ ] Add email format validation for invitations
  - [ ] Implement duplicate invitation prevention
  - [ ] Add invitation limit enforcement and user feedback
  - [ ] Implement invitation quota management

- [ ] **Error Handling and User Feedback** (AC: 5.11)
  - [ ] Implement comprehensive error handling for invitation scenarios
  - [ ] Add user-friendly error messages for different failure cases
  - [ ] Implement success feedback for invitation operations
  - [ ] Add validation feedback for invitation form
  - [ ] Handle edge cases (expired invitations, invalid emails, role conflicts)

- [ ] **Testing Implementation** (All ACs)
  - [ ] Unit tests for invitation service logic
  - [ ] Unit tests for token generation and validation
  - [ ] Integration tests for complete invitation flow
  - [ ] Integration tests for email sending and invitation management
  - [ ] E2E tests for browser invitation management flow
  - [ ] Security tests for role-based access control

## Dev Notes

### Architecture Patterns and Constraints
- **Role-based Access Control**: Only Company Admins can manage team invitations
- **Secure Token Generation**: Cryptographically secure invitation tokens with expiration
- **Email-based Invitations**: Secure invitation flow via email with company context
- **Multi-tenant Isolation**: Invitations are company-specific and isolated
- **Activity Logging**: Comprehensive audit trail for invitation management
- **Configurable Limits**: Invitation limits managed via Application Specification system

### Project Structure Notes
- **Backend**: `backend/modules/team/` for invitation management logic
- **Frontend**: `frontend/features/team/` for team management UI components
- **Email Templates**: `backend/templates/emails/` for invitation email template
- **Database**: invitations table with audit trail and proper relationships
- **RBAC**: Integration with authentication middleware for role verification

### Invitation Flow
```
1. Company Admin creates invitation → Role assignment → Token generation
2. Email sent with invitation link → User clicks link → Token validation
3. User accepts invitation → Role assignment → Company access granted
```

### Role Management
- **Company Admin**: Can invite users with Company User role
- **Company User**: Standard team member with limited permissions
- **System Admin**: Backend-only role for platform administration

### Testing Standards Summary
- **Unit Tests**: 80%+ coverage for team invitation module using pytest
- **Integration Tests**: Complete invitation flow using TestClient
- **E2E Tests**: Browser invitation management flow using Playwright
- **Security Tests**: Role-based access control and token validation
- **Performance Tests**: Email delivery and invitation processing times

### References
- **Technical Specification**: [Source: docs/tech-spec-epic-1.md#AC-5-Invitation-Management]
- **RBAC Implementation**: [Source: docs/tech-spec-epic-1.md#AC-7-RBAC-Middleware]
- **Email Service**: [Source: docs/tech-spec-epic-1.md#Email-Service-Integration]
- **UX Requirements**: [Source: docs/tech-spec-epic-1.md#UX-Design-Specifications]
- **Application Configuration**: [Source: docs/tech-spec-epic-1.md#Application-Specification-System]

## Dev Agent Record

### Context Reference
- docs/story-context-1.5.xml

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
