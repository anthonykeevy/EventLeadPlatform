# Story 1.2: User Login and JWT Token Generation

Status: ContextReadyDraft

## Story

As a **verified EventLead Platform user**,
I want **to log in with my email and password to receive secure access tokens**,
so that **I can access the platform and maintain an authenticated session**.

## Acceptance Criteria

1. **AC-2.1:** User can submit login form with email and password
2. **AC-2.2:** System validates credentials and returns JWT access token (15-minute expiration)
3. **AC-2.3:** System returns JWT refresh token (7-day expiration)
4. **AC-2.4:** JWT tokens include: user_id, email, role, company_id, exp, iat
5. **AC-2.5:** System returns 200 success response with tokens
6. **AC-2.6:** System returns 401 error for invalid credentials
7. **AC-2.7:** System returns 403 error if email not verified

## Tasks / Subtasks

- [ ] **Backend Login Service** (AC: 2.1, 2.2, 2.6, 2.7)
  - [ ] Create login endpoint in `backend/modules/auth/router.py`
  - [ ] Implement credential validation against User table
  - [ ] Implement bcrypt password verification
  - [ ] Check email verification status before allowing login
  - [ ] Handle invalid credentials with appropriate HTTP status codes
  - [ ] Add rate limiting to prevent brute force attacks (5 attempts per minute)

- [ ] **JWT Token Generation** (AC: 2.2, 2.3, 2.4)
  - [ ] Create JWT token service in `backend/modules/auth/service.py`
  - [ ] Implement access token generation (15-minute expiration)
  - [ ] Implement refresh token generation (7-day expiration)
  - [ ] Include required claims: user_id, email, role, company_id, exp, iat
  - [ ] Use secure JWT secret from Application Specification system
  - [ ] Implement token signing with RS256 algorithm

- [ ] **Token Response Handling** (AC: 2.5)
  - [ ] Create login response model with access_token, refresh_token, user_info
  - [ ] Return user information (id, email, first_name, last_name, role)
  - [ ] Implement proper HTTP status codes and error messages
  - [ ] Add CORS headers for frontend integration

- [ ] **Frontend Login Components** (AC: 2.1)
  - [ ] Create `frontend/features/auth/components/LoginForm.tsx`
  - [ ] Implement form validation with react-hook-form
  - [ ] Add real-time email format validation
  - [ ] Implement loading states and error handling
  - [ ] Add accessibility features (ARIA labels, keyboard navigation)
  - [ ] Handle form submission with proper error states

- [ ] **Frontend Authentication Context** (AC: 2.2, 2.3, 2.4)
  - [ ] Create `frontend/features/auth/contexts/AuthContext.tsx`
  - [ ] Implement token storage in localStorage
  - [ ] Create authentication state management
  - [ ] Implement automatic token refresh logic
  - [ ] Add logout functionality
  - [ ] Handle token expiration gracefully

- [ ] **Protected Route Implementation** (AC: 2.4)
  - [ ] Create `frontend/features/auth/components/ProtectedRoute.tsx`
  - [ ] Implement route protection based on authentication status
  - [ ] Add role-based route protection
  - [ ] Redirect unauthenticated users to login page
  - [ ] Handle token refresh on protected route access

- [ ] **Backend Authentication Middleware** (AC: 2.4)
  - [ ] Create `backend/modules/auth/middleware.py`
  - [ ] Implement JWT token validation middleware
  - [ ] Extract user information from JWT claims
  - [ ] Add user context to request objects
  - [ ] Handle token expiration and refresh scenarios

- [ ] **Security Implementation** (All ACs)
  - [ ] Implement secure JWT secret management
  - [ ] Add token blacklisting for logout scenarios
  - [ ] Implement request rate limiting
  - [ ] Add security headers (CORS, CSP)
  - [ ] Log authentication attempts for monitoring

- [ ] **Testing Implementation** (All ACs)
  - [ ] Unit tests for login service logic
  - [ ] Unit tests for JWT token generation and validation
  - [ ] Integration tests for complete login flow
  - [ ] Integration tests for token refresh mechanism
  - [ ] E2E tests for browser login and session management
  - [ ] Security tests for token validation and expiration

## Dev Notes

### Architecture Patterns and Constraints
- **JWT-based Authentication**: Stateless tokens with secure signing
- **Token Refresh Strategy**: Short-lived access tokens with longer-lived refresh tokens
- **Multi-tenant Support**: Tokens include company_id for future multi-tenant features
- **Security First**: Rate limiting, secure token storage, proper error handling
- **Role-based Access**: JWT includes role information for authorization
- **Application Configuration**: Token expiration times managed via Application Specification system

### Project Structure Notes
- **Backend**: `backend/modules/auth/` for authentication logic and middleware
- **Frontend**: `frontend/features/auth/` for authentication UI and context
- **Security**: `backend/common/security.py` for JWT utilities and password hashing
- **Configuration**: Application Specification system for JWT secrets and expiration times
- **Middleware**: Authentication middleware for protected routes

### Testing Standards Summary
- **Unit Tests**: 80%+ coverage for auth module using pytest
- **Integration Tests**: Complete login flow with token generation using TestClient
- **E2E Tests**: Browser login, session management, and token refresh using Playwright
- **Security Tests**: JWT validation, token expiration, rate limiting verification
- **Performance Tests**: Token generation and validation response times

### Token Claims Structure
```json
{
  "user_id": "123",
  "email": "user@example.com",
  "role": "company_admin",
  "company_id": "456",
  "exp": 1640995200,
  "iat": 1640991600
}
```

### References
- **Technical Specification**: [Source: docs/tech-spec-epic-1.md#AC-2-User-Login-and-JWT-Token-Generation]
- **JWT Implementation**: [Source: docs/tech-spec-epic-1.md#JWT-Token-Management]
- **Security Requirements**: [Source: docs/tech-spec-epic-1.md#Security]
- **UX Requirements**: [Source: docs/tech-spec-epic-1.md#UX-Design-Specifications]
- **Application Configuration**: [Source: docs/tech-spec-epic-1.md#Application-Specification-System]

## Dev Agent Record

### Context Reference
- docs/story-context-1.2.xml

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
