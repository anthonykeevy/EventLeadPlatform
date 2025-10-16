# Invitation Acceptance & Multi-Company Support Guide

## Overview

This guide explains how the invitation acceptance and multi-company support system works in the EventLead platform (Story 1.7).

## Features

### 1. View Invitation Details (Public)
- **Endpoint**: `GET /api/invitations/{token}`
- **Authentication**: None required (public)
- **Purpose**: Allows invited users to view invitation details before accepting

### 2. Accept Invitation (Existing Users)
- **Endpoint**: `POST /api/invitations/{token}/accept`
- **Authentication**: Required (JWT)
- **Purpose**: Existing users can accept invitations to join companies

### 3. Signup with Invitation (New Users)
- **Endpoint**: `POST /api/auth/signup` with `invitation_token` parameter
- **Authentication**: None required (public)
- **Purpose**: New users can sign up and automatically join a company

### 4. Multi-Company Support
- **List Companies**: `GET /api/users/me/companies`
- **Switch Company**: `POST /api/users/me/switch-company`
- **Purpose**: Users can belong to multiple companies and switch between them

## User Flows

### Flow 1: Existing User Accepts Invitation

```
1. User receives invitation email
2. User clicks invitation link → Frontend shows invitation details
3. User clicks "Accept Invitation"
4. Frontend redirects to login (if not logged in)
5. User logs in
6. Frontend calls POST /api/invitations/{token}/accept
7. Backend creates UserCompany relationship
8. Backend issues new JWT with updated role/company
9. Frontend redirects to dashboard
```

**API Call:**
```bash
POST /api/invitations/{token}/accept
Authorization: Bearer {user_jwt}

Response:
{
  "success": true,
  "message": "Invitation accepted successfully",
  "company_id": 456,
  "role": "company_user",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Flow 2: New User Signup with Invitation

```
1. User receives invitation email
2. User clicks invitation link → Frontend shows invitation details
3. User clicks "Sign Up"
4. Frontend redirects to signup with invitation_token param
5. User completes signup form
6. Backend creates User and UserCompany atomically
7. Backend issues JWT with role and company_id
8. Frontend redirects to dashboard (onboarding skipped)
```

**API Call:**
```bash
POST /api/auth/signup
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "SecureP@ssw0rd123",
  "first_name": "Jane",
  "last_name": "Doe",
  "invitation_token": "abc123xyz789"
}

Response:
{
  "success": true,
  "message": "Signup successful! You can now access your team.",
  "data": {
    "user_id": 789,
    "email": "newuser@example.com",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "company_id": 456,
    "role": "company_user"
  }
}
```

### Flow 3: Multi-Company User Switches Company

```
1. User clicks company switcher in UI
2. Frontend fetches user's companies (GET /api/users/me/companies)
3. User selects different company
4. Frontend calls POST /api/users/me/switch-company
5. Backend issues new JWT with new company_id and role
6. Frontend updates state and redirects to dashboard
```

**API Calls:**
```bash
# List companies
GET /api/users/me/companies
Authorization: Bearer {user_jwt}

Response:
[
  {
    "company_id": 456,
    "company_name": "Acme Events Pty Ltd",
    "role": "company_admin",
    "is_primary": true,
    "joined_at": "2025-10-16T10:30:00Z"
  },
  {
    "company_id": 789,
    "company_name": "XYZ Corp Pty Ltd",
    "role": "company_user",
    "is_primary": false,
    "joined_at": "2025-10-20T14:15:00Z"
  }
]

# Switch company
POST /api/users/me/switch-company
Authorization: Bearer {user_jwt}
Content-Type: application/json

{
  "company_id": 789
}

Response:
{
  "success": true,
  "message": "Switched to XYZ Corp Pty Ltd",
  "company_id": 789,
  "company_name": "XYZ Corp Pty Ltd",
  "role": "company_user",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Database Schema

### Key Tables

#### UserInvitation
```sql
dbo.UserInvitation
- UserInvitationID (PK)
- CompanyID (FK → Company)
- Email
- UserCompanyRoleID (FK → UserCompanyRole)
- InvitedBy (FK → User)
- InvitedAt
- ExpiresAt
- AcceptedAt
- AcceptedBy (FK → User)
- InvitationToken (unique, indexed)
- StatusID (FK → UserInvitationStatus)
```

#### UserCompany
```sql
dbo.UserCompany
- UserCompanyID (PK)
- UserID (FK → User)
- CompanyID (FK → Company)
- UserCompanyRoleID (FK → UserCompanyRole)
- StatusID (FK → UserCompanyStatus)
- IsPrimaryCompany (bool)
- JoinedDate
- JoinedViaID (FK → JoinedVia)
- InvitedBy (FK → User, nullable)
- InvitedDate (nullable)
```

### Relationships

```
User ──────< UserCompany >────── Company
              │
              └─── UserCompanyRole (company_admin, company_user)
              └─── UserCompanyStatus (active, inactive, suspended)

UserInvitation
  ├─ CompanyID → Company
  ├─ InvitedBy → User
  ├─ AcceptedBy → User
  └─ StatusID → UserInvitationStatus (pending, accepted, expired, cancelled)
```

## Security Considerations

### 1. Email Validation
- Invitation email MUST match the authenticated user's email
- New signups must use the exact email address from the invitation
- Case-insensitive comparison

### 2. Token Security
- Tokens are cryptographically secure (32 bytes, URL-safe)
- Tokens expire after 7 days
- Tokens can only be used once (marked as used after acceptance)
- Expired or already-used tokens cannot be accepted

### 3. Company Access Control
- Users can only accept invitations for their own email
- Users can only switch to companies they belong to
- JWT contains single company at a time for data isolation
- Multi-tenant data queries use JWT company_id claim

### 4. Audit Logging
All invitation acceptance events are logged to `audit.ActivityLog`:
- INVITATION_ACCEPTED: When existing user accepts invitation
- USER_SIGNUP_WITH_INVITATION: When new user signs up with invitation
- COMPANY_SWITCHED: When user switches active company

## Frontend Integration

### Invitation Link Format
```
https://app.eventlead.com/invite?token={invitation_token}
```

### Frontend Flow
1. Extract token from URL query parameter
2. Call `GET /api/invitations/{token}` to display details
3. If user has account: Prompt to login, then accept
4. If new user: Redirect to signup with token param

### JWT Refresh
After accepting invitation or switching companies:
1. Store new `access_token` and `refresh_token` in local storage/cookies
2. Update application state with new `company_id` and `role`
3. Redirect to dashboard or company-specific route

## Testing

### Integration Tests
Comprehensive integration tests are in `backend/tests/test_invitation_acceptance.py`:
- View invitation details (public)
- Accept invitation (existing user)
- Signup with invitation (new user)
- Email validation
- Token validation
- Multi-company scenarios
- Audit logging

### Manual Testing Checklist
- [ ] Invite user to company
- [ ] Existing user accepts invitation
- [ ] New user signs up with invitation
- [ ] Email mismatch rejected
- [ ] Expired invitation rejected
- [ ] User can see all their companies
- [ ] User can switch between companies
- [ ] JWT contains correct role and company_id after switch
- [ ] Audit logs created for all events

## Troubleshooting

### "Invitation not found"
- Check invitation token is correct
- Verify invitation hasn't been deleted
- Check invitation hasn't expired

### "Email does not match invitation"
- User must use exact email address from invitation
- Check for typos in email
- Email comparison is case-insensitive but must be exact match

### "Invitation has expired"
- Invitations expire after 7 days
- Admin can resend invitation (creates new token)

### "You are already a member of this company"
- User already has active UserCompany relationship
- Check if user is trying to accept duplicate invitation

### "You do not belong to this company"
- User trying to switch to company they don't have access to
- Verify UserCompany relationship exists and is active

## Related Documentation

- [Team Invitation System](../stories/story-1.6.md) - How to send invitations
- [RBAC Middleware Guide](./rbac-middleware-guide.md) - Role-based access control
- [Onboarding Flow Guide](./onboarding-flow-guide.md) - First-time user onboarding
- [JWT Authentication](./jwt-authentication.md) - JWT token structure and claims

## Database Queries

### Find all companies a user belongs to
```sql
SELECT 
    c.CompanyName,
    ucr.RoleName,
    uc.IsPrimaryCompany,
    uc.JoinedDate
FROM dbo.UserCompany uc
JOIN dbo.Company c ON c.CompanyID = uc.CompanyID
JOIN ref.UserCompanyRole ucr ON ucr.UserCompanyRoleID = uc.UserCompanyRoleID
JOIN ref.UserCompanyStatus ucs ON ucs.UserCompanyStatusID = uc.StatusID
WHERE uc.UserID = @UserID
  AND uc.IsDeleted = 0
  AND ucs.StatusCode = 'active'
ORDER BY uc.IsPrimaryCompany DESC, uc.JoinedDate ASC;
```

### Find pending invitations for a company
```sql
SELECT 
    ui.Email,
    ucr.RoleName,
    ui.InvitedAt,
    ui.ExpiresAt,
    u.FirstName + ' ' + u.LastName AS InviterName
FROM dbo.UserInvitation ui
JOIN ref.UserCompanyRole ucr ON ucr.UserCompanyRoleID = ui.UserCompanyRoleID
JOIN dbo.[User] u ON u.UserID = ui.InvitedBy
JOIN ref.UserInvitationStatus uis ON uis.UserInvitationStatusID = ui.StatusID
WHERE ui.CompanyID = @CompanyID
  AND ui.IsDeleted = 0
  AND uis.StatusCode = 'pending'
  AND ui.ExpiresAt > GETUTCDATE()
ORDER BY ui.InvitedAt DESC;
```

## Configuration

### Environment Variables
- `FRONTEND_URL`: Base URL for invitation links (e.g., `https://app.eventlead.com`)
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiry (default: 30)

## API Reference

### GET /api/invitations/{token}
View invitation details (public endpoint).

**Response:**
```json
{
  "invitation_id": 123,
  "company_name": "Acme Events Pty Ltd",
  "role_name": "Team Member",
  "inviter_name": "John Doe",
  "invited_email": "jane@example.com",
  "expires_at": "2025-10-23T10:30:00Z",
  "is_expired": false,
  "status": "pending"
}
```

### POST /api/invitations/{token}/accept
Accept invitation (requires authentication).

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "success": true,
  "message": "Invitation accepted successfully",
  "company_id": 456,
  "role": "company_user",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### POST /api/auth/signup
Signup (optionally with invitation token).

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecureP@ssw0rd123",
  "first_name": "Jane",
  "last_name": "Doe",
  "invitation_token": "abc123xyz789"  // Optional
}
```

**Response (with invitation):**
```json
{
  "success": true,
  "message": "Signup successful! You can now access your team.",
  "data": {
    "user_id": 789,
    "email": "user@example.com",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "company_id": 456,
    "role": "company_user"
  }
}
```

### GET /api/users/me/companies
List companies user belongs to (requires authentication).

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response:**
```json
[
  {
    "company_id": 456,
    "company_name": "Acme Events Pty Ltd",
    "role": "company_admin",
    "is_primary": true,
    "joined_at": "2025-10-16T10:30:00Z"
  }
]
```

### POST /api/users/me/switch-company
Switch active company (requires authentication).

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "company_id": 789
}
```

**Response:**
```json
{
  "success": true,
  "message": "Switched to XYZ Corp Pty Ltd",
  "company_id": 789,
  "company_name": "XYZ Corp Pty Ltd",
  "role": "company_user",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-16 | 1.0 | Initial release (Story 1.7) |

