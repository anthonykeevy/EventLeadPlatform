# Story 1.6: Invitation Acceptance and User Onboarding

Status: ContextReadyDraft

## Story

As a **user who has received a team invitation**,
I want **to accept the invitation and complete my user onboarding**,
so that **I can join the company team and access the EventLead Platform**.

## Acceptance Criteria

1. **AC-6.1:** User can access invitation via secure token link from email
2. **AC-6.2:** System validates invitation token and checks expiration
3. **AC-6.3:** System displays invitation details (company name, inviter, role)
4. **AC-6.4:** User can accept or decline the invitation
5. **AC-6.5:** System creates UserCompany relationship with assigned role upon acceptance
6. **AC-6.6:** System redirects accepted users to simplified onboarding flow
7. **AC-6.7:** **Simplified Onboarding:** User enters first name, last name, role title, phone
8. **AC-6.8:** System validates required fields and Australian phone format
9. **AC-6.9:** System saves user details and completes onboarding
10. **AC-6.10:** System redirects to dashboard upon completion
11. **AC-6.11:** System logs all invitation acceptance activities
12. **AC-6.12:** System handles expired or invalid invitation tokens gracefully
13. **AC-6.13:** User can only accept invitation once (prevents duplicate acceptance)

## Tasks / Subtasks

- [ ] **Backend Invitation Acceptance Service** (AC: 6.1, 6.2, 6.5, 6.11, 6.12, 6.13)
  - [ ] Create invitation acceptance endpoint in `backend/modules/team/router.py`
  - [ ] Implement token validation and expiration checking
  - [ ] Implement invitation acceptance logic with UserCompany relationship creation
  - [ ] Add invitation status update (pending → accepted)
  - [ ] Implement invitation token invalidation after acceptance
  - [ ] Add comprehensive activity logging for acceptance events
  - [ ] Handle edge cases (expired tokens, already accepted invitations)

- [ ] **Backend Simplified Onboarding** (AC: 6.6, 6.7, 6.8, 6.9, 6.10)
  - [ ] Create simplified onboarding endpoint in `backend/modules/users/router.py`
  - [ ] Implement user details update for invited users
  - [ ] Add Australian phone format validation
  - [ ] Implement role title validation and storage
  - [ ] Add onboarding completion tracking
  - [ ] Implement redirect to dashboard after completion

- [ ] **Frontend Invitation Acceptance** (AC: 6.1, 6.3, 6.4, 6.12)
  - [ ] Create `frontend/features/auth/components/InvitationAcceptance.tsx`
  - [ ] Implement invitation details display (company name, inviter, role)
  - [ ] Add accept/decline functionality
  - [ ] Implement loading states and error handling
  - [ ] Add accessibility features (ARIA labels, keyboard navigation)
  - [ ] Handle expired and invalid token scenarios

- [ ] **Frontend Simplified Onboarding** (AC: 6.6, 6.7, 6.8, 6.9, 6.10)
  - [ ] Create `frontend/features/onboarding/components/InvitedUserOnboarding.tsx`
  - [ ] Implement simplified form with required fields only
  - [ ] Add Australian phone format validation
  - [ ] Implement form validation with react-hook-form
  - [ ] Add loading states and error handling
  - [ ] Implement completion redirect to dashboard

- [ ] **Token Validation and Security** (AC: 6.2, 6.12, 6.13)
  - [ ] Implement secure token validation logic
  - [ ] Add token expiration checking
  - [ ] Implement single-use token enforcement
  - [ ] Add protection against token replay attacks
  - [ ] Implement comprehensive error handling for invalid tokens

- [ ] **UserCompany Relationship Management** (AC: 6.5)
  - [ ] Implement UserCompany table relationship creation
  - [ ] Add role assignment validation
  - [ ] Implement company access granting
  - [ ] Add relationship audit trail
  - [ ] Implement duplicate relationship prevention

- [ ] **Database Schema Implementation** (AC: 6.5, 6.11)
  - [ ] Create UserCompany junction table with proper constraints
  - [ ] Add audit trail fields (CreatedDate, CreatedBy, UpdatedDate, UpdatedBy)
  - [ ] Implement proper foreign key relationships
  - [ ] Add indexes for performance optimization
  - [ ] Create activity logging tables for invitation acceptance events

- [ ] **Error Handling and User Experience** (AC: 6.12)
  - [ ] Implement comprehensive error handling for all invitation scenarios
  - [ ] Add user-friendly error messages for different failure cases
  - [ ] Implement graceful handling of expired invitations
  - [ ] Add clear feedback for successful acceptance
  - [ ] Handle network errors and retry scenarios

- [ ] **Onboarding Flow Integration** (AC: 6.6, 6.10)
  - [ ] Integrate with existing onboarding flow components
  - [ ] Implement simplified onboarding for invited users
  - [ ] Add dashboard redirect after completion
  - [ ] Implement onboarding completion tracking
  - [ ] Add progress indicators for invited user onboarding

- [ ] **Testing Implementation** (All ACs)
  - [ ] Unit tests for invitation acceptance service logic
  - [ ] Unit tests for token validation and expiration
  - [ ] Unit tests for simplified onboarding flow
  - [ ] Integration tests for complete invitation acceptance flow
  - [ ] Integration tests for simplified onboarding
  - [ ] E2E tests for browser invitation acceptance and onboarding

## Dev Notes

### Architecture Patterns and Constraints
- **Secure Token Validation**: Cryptographically secure token validation with expiration
- **Simplified Onboarding**: Streamlined onboarding flow for invited users
- **Role-based Access**: Automatic role assignment upon invitation acceptance
- **Multi-tenant Integration**: UserCompany relationship creation for company access
- **Activity Logging**: Comprehensive audit trail for invitation acceptance
- **Single-use Tokens**: Invitation tokens invalidated after acceptance

### Project Structure Notes
- **Backend**: `backend/modules/team/` for invitation acceptance logic
- **Frontend**: `frontend/features/auth/` and `frontend/features/onboarding/` for UI components
- **Database**: UserCompany junction table with audit trail
- **Integration**: Seamless integration with existing onboarding flow

### Invitation Acceptance Flow
```
1. User clicks invitation link → Token validation → Invitation details display
2. User accepts invitation → UserCompany relationship creation → Token invalidation
3. User redirected to simplified onboarding → User details entry → Dashboard access
```

### Simplified Onboarding vs Full Onboarding
- **Full Onboarding**: New users create companies (Story 1.3)
- **Simplified Onboarding**: Invited users join existing companies (Story 1.6)
- **Key Differences**: No company creation, no ABR search, streamlined form

### Testing Standards Summary
- **Unit Tests**: 80%+ coverage for invitation acceptance module using pytest
- **Integration Tests**: Complete invitation acceptance flow using TestClient
- **E2E Tests**: Browser invitation acceptance and onboarding using Playwright
- **Security Tests**: Token validation, expiration, and single-use enforcement
- **Performance Tests**: Invitation processing and onboarding completion times

### References
- **Technical Specification**: [Source: docs/tech-spec-epic-1.md#AC-6-Invitation-Acceptance]
- **User Domain Schema**: [Source: docs/tech-spec-epic-1.md#User-Domain-Schema]
- **RBAC Implementation**: [Source: docs/tech-spec-epic-1.md#AC-7-RBAC-Middleware]
- **UX Requirements**: [Source: docs/tech-spec-epic-1.md#UX-Design-Specifications]
- **Database Schema**: [Source: docs/tech-spec-epic-1.md#Database-Schema-Implementation]

## Dev Agent Record

### Context Reference
- docs/story-context-1.6.xml

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
