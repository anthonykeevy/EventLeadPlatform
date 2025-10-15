# Story 1.7: RBAC Middleware and Authorization

Status: ContextReadyDraft

## Story

As a **EventLead Platform system**,
I want **to enforce role-based access control across all protected endpoints**,
so that **users can only access resources and perform actions appropriate to their role**.

## Acceptance Criteria

1. **AC-7.1:** System validates JWT tokens on all protected endpoints
2. **AC-7.2:** System extracts user information from JWT claims (user_id, role, company_id)
3. **AC-7.3:** System enforces role-based permissions for different endpoint access
4. **AC-7.4:** Company Admin can access all company resources and team management
5. **AC-7.5:** Company User can access limited company resources (no team management)
6. **AC-7.6:** System returns 401 error for invalid or expired tokens
7. **AC-7.7:** System returns 403 error for insufficient permissions

## Tasks / Subtasks

- [ ] **Backend RBAC Middleware** (AC: 7.1, 7.2, 7.6, 7.7)
  - [ ] Create `backend/modules/auth/middleware.py` with authentication middleware
  - [ ] Implement JWT token validation and extraction
  - [ ] Implement user context injection into request objects
  - [ ] Add token expiration checking and error handling
  - [ ] Implement comprehensive error responses (401, 403)
  - [ ] Add middleware logging for security monitoring

- [ ] **RBAC Decorators Using Permission Service** (AC: 7.3, 7.4, 7.5)
  - [ ] Import `PermissionService` from `backend/modules/permissions/service.py` (Story 1.8)
  - [ ] Create `@require_permission(permission)` decorator using `PermissionService.has_permission()`
  - [ ] Create `@require_role(role)` decorator for role-level checks
  - [ ] Create `@require_company_access` decorator for company isolation
  - [ ] Document how to use decorators in service layer and API endpoints
  - [ ] Add role-based endpoint protection using new decorators

- [ ] **Multi-tenant Data Isolation** (AC: 7.4, 7.5)
  - [ ] Implement company_id filtering for all company-specific resources
  - [ ] Add automatic company context injection for authenticated users
  - [ ] Implement cross-company access prevention
  - [ ] Add company isolation validation in service layer
  - [ ] Implement company boundary enforcement

- [ ] **Frontend Authorization Context** (AC: 7.3, 7.4, 7.5)
  - [ ] Update `frontend/features/auth/contexts/AuthContext.tsx` with role information
  - [ ] Use `usePermissions()` hook from Story 1.8 for permission checks
  - [ ] Implement role-based UI component rendering using `PermissionGate` component
  - [ ] Implement role-based navigation and menu items using `hasPermission()` checks
  - [ ] Add user role display and management

- [ ] **Protected Route Implementation** (AC: 7.3, 7.6, 7.7)
  - [ ] Create `frontend/features/auth/components/ProtectedRoute.tsx`
  - [ ] Implement authentication status checking
  - [ ] Add role-based route protection
  - [ ] Implement redirect logic for unauthorized access
  - [ ] Add loading states for authentication checks

- [ ] **Permission Decorators and Utilities** (AC: 7.3, 7.4, 7.5)
  - [ ] Create `@require_auth` decorator for authentication
  - [ ] Create `@require_role` decorator for role-based access
  - [ ] Create `@require_permission` decorator for specific permissions
  - [ ] Implement permission checking utilities
  - [ ] Add role validation helpers

- [ ] **Service Layer Authorization** (AC: 7.4, 7.5)
  - [ ] Implement authorization checks in all service layer functions
  - [ ] Add company_id filtering for all company-specific operations
  - [ ] Implement role-based operation validation
  - [ ] Add authorization logging for security audit
  - [ ] Implement permission escalation prevention

- [ ] **Error Handling and Security** (AC: 7.6, 7.7)
  - [ ] Implement comprehensive error handling for authorization failures
  - [ ] Add security headers and CORS configuration
  - [ ] Implement rate limiting for authentication endpoints
  - [ ] Add security logging and monitoring
  - [ ] Implement protection against privilege escalation

- [ ] **Testing Implementation** (All ACs)
  - [ ] Unit tests for JWT token validation and extraction
  - [ ] Unit tests for role-based permission checking
  - [ ] Unit tests for multi-tenant data isolation
  - [ ] Integration tests for protected endpoint access
  - [ ] Integration tests for role-based authorization
  - [ ] E2E tests for browser authorization scenarios
  - [ ] Security tests for privilege escalation prevention

## Dev Notes

### Architecture Patterns and Constraints
- **JWT-based Authentication**: Stateless token validation with role information
- **Role-based Access Control**: Three-tier role system with defined permissions
- **Multi-tenant Isolation**: Company-specific data access and filtering
- **Middleware Architecture**: Centralized authorization enforcement
- **Security First**: Comprehensive error handling and security logging
- **Permission-based Access**: Granular permission checking for different operations

### Project Structure Notes
- **Backend**: `backend/modules/auth/middleware.py` for authorization middleware
- **Frontend**: `frontend/features/auth/` for authorization context and components
- **Service Layer**: Authorization checks integrated into all service functions
- **Database**: Company_id filtering for all company-specific resources
- **Security**: Comprehensive logging and monitoring for authorization events

### Role Definitions
- **System Admin**: Platform-wide access (backend only for MVP)
- **Company Admin**: Full company access, team management, billing
- **Company User**: Limited company access, no team management

### Permission Matrix
```
Resource                | System Admin | Company Admin | Company User
------------------------|--------------|---------------|-------------
User Management         | ✅           | ✅            | ❌
Team Management         | ✅           | ✅            | ❌
Company Settings        | ✅           | ✅            | ❌
Event Management        | ✅           | ✅            | ✅
Form Management         | ✅           | ✅            | ✅
Analytics               | ✅           | ✅            | ✅
Billing                 | ✅           | ✅            | ❌
```

### Testing Standards Summary
- **Unit Tests**: 80%+ coverage for authorization middleware using pytest
- **Integration Tests**: Protected endpoint access using TestClient
- **E2E Tests**: Browser authorization scenarios using Playwright
- **Security Tests**: Privilege escalation prevention and token validation
- **Performance Tests**: Authorization middleware response times

### References
- **Technical Specification**: [Source: docs/tech-spec-epic-1.md#AC-7-RBAC-Middleware]
- **Multi-tenant Architecture**: [Source: docs/tech-spec-epic-1.md#AC-8-Multi-Tenant-Isolation]
- **Security Requirements**: [Source: docs/tech-spec-epic-1.md#Security]
- **JWT Implementation**: [Source: docs/tech-spec-epic-1.md#JWT-Token-Management]
- **UX Requirements**: [Source: docs/tech-spec-epic-1.md#UX-Design-Specifications]

## Dependencies

**Critical:** This story depends on Story 1.8 (Role Management) being completed first.

### From Story 1.8:
- `backend/modules/permissions/service.py` - PermissionService class
- `backend/modules/permissions/service.py` - Permission enum
- `frontend/src/hooks/usePermissions.ts` - usePermissions hook
- `frontend/src/components/PermissionGate.tsx` - PermissionGate component

**Implementation Order:**
1. ✅ Story 1.8 must be completed first (provides permission abstraction layer)
2. ➡️ Story 1.7 implements RBAC decorators using PermissionService
3. ➡️ Stories 1.5 & 1.6 use decorators from Story 1.7

## Dev Agent Record

### Context Reference
- docs/story-context-1.7.xml

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
