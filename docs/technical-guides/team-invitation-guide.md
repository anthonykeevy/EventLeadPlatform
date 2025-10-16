```
# Team Invitation System Guide

## Overview

This guide documents the team invitation system implemented in Story 1.6. The system allows company admins to invite team members via email, with secure token-based invitations and comprehensive audit logging.

## Invitation Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                     Team Invitation Flow                            │
└────────────────────────────────────────────────────────────────────┘

1. Company Admin Sends Invitation
   ├─> Specifies: email, first name, last name, role
   ├─> System generates secure 7-day token
   ├─> Creates UserInvitation record
   └─> Sends invitation email with acceptance link

2. Invitation Email Sent
   ├─> Contains invitation link with token
   ├─> Includes company name, inviter name
   ├─> Specifies assigned role
   └─> Valid for 7 days

3. Invitee Receives Email
   ├─> Clicks invitation link
   └─> Lands on acceptance page (Story 1.7)

4. Admin Can Manage Invitations
   ├─> View all invitations
   ├─> Resend pending invitations (extends expiry)
   └─> Cancel pending invitations

5. Acceptance Flow (Story 1.7)
   ├─> If existing user: Accept invitation
   └─> If new user: Signup + accept invitation
```

## API Endpoints

### 1. Send Team Invitation

**Endpoint:** `POST /api/companies/{company_id}/invite`

**Authentication:** Required (Bearer token)

**Authorization:** Requires `company_admin` role and membership in the company

**Request Body:**
```json
{
  "email": "jane.smith@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "company_user"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Invitation sent successfully",
  "invitation_id": 123,
  "expires_at": "2025-10-23T10:30:00Z"
}
```

**Validation:**
- `email`: Valid email format, required
- `first_name`: 1-100 characters, required
- `last_name`: 1-100 characters, required
- `role`: Must be `company_admin` or `company_user`, required

**Business Rules:**
1. Only `company_admin` can send invitations
2. Admin must belong to the company
3. Cannot invite email that already belongs to the company
4. Cannot invite email with pending invitation
5. Invitation token valid for 7 days
6. Email sent automatically

**Error Responses:**
- `401 Unauthorized`: Missing or invalid JWT
- `403 Forbidden`: Not company_admin or wrong company
- `400 Bad Request`:
  - Email already in company
  - Pending invitation exists
  - Invalid role
  - Validation errors

### 2. List Company Invitations

**Endpoint:** `GET /api/companies/{company_id}/invitations`

**Authentication:** Required (Bearer token)

**Authorization:** Requires `company_admin` role

**Query Parameters:**
- `status_filter` (optional): Filter by status (pending, accepted, expired, cancelled)
- `page` (optional, default=1): Page number
- `page_size` (optional, default=20, max=100): Items per page

**Response (200 OK):**
```json
{
  "invitations": [
    {
      "invitation_id": 123,
      "company_id": 456,
      "email": "jane.smith@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "role": "company_user",
      "status": "pending",
      "invited_by": "John Doe",
      "invited_at": "2025-10-16T10:30:00Z",
      "expires_at": "2025-10-23T10:30:00Z",
      "accepted_at": null,
      "cancelled_at": null,
      "declined_at": null,
      "resend_count": 0,
      "last_resent_at": null
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20
}
```

### 3. Resend Invitation

**Endpoint:** `POST /api/companies/{company_id}/invitations/{invitation_id}/resend`

**Authentication:** Required (Bearer token)

**Authorization:** Requires `company_admin` role

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Invitation resent successfully",
  "invitation_id": 123,
  "new_expires_at": "2025-10-30T10:30:00Z",
  "resend_count": 1
}
```

**Business Rules:**
1. Only pending invitations can be resent
2. Extends expiry by 7 days from now
3. Increments resend_count
4. Resends invitation email
5. Tracks last_resent_at timestamp

**Error Responses:**
- `400 Bad Request`: Invitation cannot be resent (not pending or already accepted/cancelled)

### 4. Cancel Invitation

**Endpoint:** `DELETE /api/companies/{company_id}/invitations/{invitation_id}`

**Authentication:** Required (Bearer token)

**Authorization:** Requires `company_admin` role

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Invitation cancelled successfully",
  "invitation_id": 123
}
```

**Business Rules:**
1. Only pending invitations can be cancelled
2. Marks invitation as cancelled
3. Invalidates token (cannot be used)
4. Records cancellation timestamp and user

**Error Responses:**
- `400 Bad Request`: Invitation cannot be cancelled (already accepted/cancelled)

## Invitation Token Security

### Token Generation

**Method:** Cryptographically secure random tokens

**Format:** URL-safe base64 encoded (64 characters)

**Expiry:** 7 days from creation (or last resend)

**Code Example:**
```python
import secrets

def generate_invitation_token() -> str:
    return secrets.token_urlsafe(48)  # 64 characters when encoded
```

### Token Validation

Tokens are:
- Stored in `UserInvitation.InvitationToken`
- Unique per invitation
- URL-safe (can be used in links)
- Single-use (invalidated upon acceptance or cancellation)
- Automatically expired after 7 days

### Invitation URL Structure

```
https://app.example.com/invitations/accept?token={invitation_token}
```

Frontend URL configured via `FRONTEND_URL` environment variable.

## Role-Based Access Control

### Allowed Roles

Invitations can assign these roles:
- `company_admin`: Full administrative access
- `company_user`: Regular team member access

### Role Validation

```python
ALLOWED_INVITATION_ROLES = ["company_admin", "company_user"]
```

Attempting to invite with other roles results in `400 Bad Request`.

### Permission Requirements

| Action | Required Role | Required Company Membership |
|--------|---------------|----------------------------|
| Send Invitation | company_admin | Yes (sender's company) |
| List Invitations | company_admin | Yes |
| Resend Invitation | company_admin | Yes |
| Cancel Invitation | company_admin | Yes |

## Email Integration

### Team Invitation Email

**Template:** `backend/templates/emails/team_invitation.html`

**Variables:**
- `invitee_name`: Name of person being invited
- `inviter_name`: Name of person sending invitation
- `company_name`: Company name
- `role_name`: Role being assigned (display name)
- `invitation_url`: Full URL with token
- `expiry_days`: Days until expiration (7)

**Subject:** `{inviter_name} invited you to join {company_name}`

**Example Email Service Call:**
```python
from services.email_service import get_email_service

email_service = get_email_service()
await email_service.send_team_invitation_email(
    to="jane@example.com",
    invitee_name="Jane Smith",
    inviter_name="John Doe",
    company_name="Acme Events",
    role_name="Team Member",
    invitation_url="https://app.example.com/invitations/accept?token=abc123...",
    expiry_days=7
)
```

## Database Schema

### dbo.UserInvitation Table

| Column | Type | Description |
|--------|------|-------------|
| UserInvitationID | BIGINT | Primary key |
| CompanyID | BIGINT | Company sending invitation |
| InvitedBy | BIGINT | User who sent invitation |
| Email | VARCHAR(255) | Invitee email |
| FirstName | VARCHAR(100) | Invitee first name |
| LastName | VARCHAR(100) | Invitee last name |
| UserCompanyRoleID | BIGINT | Role to assign |
| StatusID | BIGINT | Invitation status |
| InvitationToken | VARCHAR(500) | Secure token (unique) |
| InvitedAt | DATETIME | When invitation was sent |
| ExpiresAt | DATETIME | When invitation expires |
| AcceptedAt | DATETIME | When accepted (nullable) |
| CancelledAt | DATETIME | When cancelled (nullable) |
| ResendCount | INT | Number of times resent |
| LastResentAt | DATETIME | Last resend timestamp |

### Invitation Status Codes

| Status Code | Description | CanResend | CanCancel | IsFinalState |
|-------------|-------------|-----------|-----------|--------------|
| pending | Awaiting response | Yes | Yes | No |
| accepted | Invitation accepted | No | No | Yes |
| declined | Invitation declined | No | No | Yes |
| expired | Invitation expired | No | No | Yes |
| cancelled | Invitation cancelled | No | No | Yes |

## Audit Logging

All invitation events are logged to `audit.ActivityLog`:

### Actions Logged

1. **INVITATION_SENT**
   - UserID: Admin who sent invitation
   - CompanyID: Company
   - EntityType: UserInvitation
   - EntityID: Invitation ID
   - NewValue: JSON with invitation details

2. **INVITATION_RESENT**
   - UserID: Admin who resent
   - CompanyID: Company
   - EntityID: Invitation ID
   - NewValue: JSON with new expiry and resend count

3. **INVITATION_CANCELLED**
   - UserID: Admin who cancelled
   - CompanyID: Company
   - EntityID: Invitation ID
   - OldValue: Previous status
   - NewValue: New status and reason

### Audit Query Example

```sql
SELECT 
    al.Action,
    al.CreatedDate,
    u.Email as AdminEmail,
    al.NewValue
FROM audit.ActivityLog al
JOIN dbo.User u ON al.UserID = u.UserID
WHERE al.EntityType = 'UserInvitation'
  AND al.CompanyID = 123
ORDER BY al.CreatedDate DESC;
```

## Frontend Integration

### Sending Invitation

```typescript
const sendInvitation = async (companyId: number) => {
  const response = await fetch(`/api/companies/${companyId}/invite`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'jane@example.com',
      first_name: 'Jane',
      last_name: 'Smith',
      role: 'company_user'
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    // Handle error: error.detail
    return;
  }
  
  const data = await response.json();
  // Show success: data.message
  // Invitation sent with ID: data.invitation_id
};
```

### Listing Invitations

```typescript
const listInvitations = async (companyId: number, statusFilter?: string) => {
  const params = new URLSearchParams();
  if (statusFilter) params.append('status_filter', statusFilter);
  params.append('page', '1');
  params.append('page_size', '20');
  
  const response = await fetch(
    `/api/companies/${companyId}/invitations?${params}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
  
  if (!response.ok) {
    // Handle error
    return;
  }
  
  const data = await response.json();
  // data.invitations: array of invitation objects
  // data.total: total count
  // data.page: current page
};
```

### Resending Invitation

```typescript
const resendInvitation = async (companyId: number, invitationId: number) => {
  const response = await fetch(
    `/api/companies/${companyId}/invitations/${invitationId}/resend`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
  
  if (!response.ok) {
    const error = await response.json();
    // Handle error: invitation cannot be resent
    return;
  }
  
  const data = await response.json();
  // Show success: data.message
  // New expiry: data.new_expires_at
};
```

## Testing

### Integration Tests

Location: `backend/tests/test_team_invitations.py`

**Coverage:**
- AC-1.6.1: Protected endpoint requires company_admin
- AC-1.6.2: Invitation created with details
- AC-1.6.3: Token generated with 7-day expiry
- AC-1.6.4: Email sent automatically
- AC-1.6.5: Cannot invite existing member
- AC-1.6.6: Admin can specify role
- AC-1.6.7: Resend invitation
- AC-1.6.8: Cancel invitation
- AC-1.6.9: List invitations with filtering
- AC-1.6.10: Audit logging

### Running Tests

```bash
# Run invitation tests
pytest backend/tests/test_team_invitations.py -v

# Run with coverage
pytest backend/tests/test_team_invitations.py --cov=modules.companies.invitation_service

# Run specific test
pytest backend/tests/test_team_invitations.py::test_send_invitation_success -v
```

## Troubleshooting

### Invitation Not Received

**Symptom:** User reports not receiving invitation email

**Resolution:**
1. Check `log.EmailDelivery` table for delivery status
2. Verify email service is configured (`EMAIL_PROVIDER` env var)
3. Check spam folder
4. Resend invitation via admin panel

### Cannot Send Invitation

**Symptom:** `403 Forbidden` when sending invitation

**Causes:**
- User doesn't have `company_admin` role
- User belongs to different company
- JWT token doesn't include role/company_id

**Resolution:**
1. Verify user role: `SELECT role FROM UserCompany WHERE UserID = X`
2. Check JWT payload includes `role` and `company_id`
3. User may need to re-login to get updated token

### Already Member Error

**Symptom:** `400 Bad Request: Email already belongs to company`

**Resolution:**
- Email already has active membership
- Check `dbo.UserCompany` for existing relationship
- If user should have duplicate role, contact support

### Invitation Expired

**Symptom:** User cannot accept invitation

**Resolution:**
- Invitations expire after 7 days
- Admin can resend invitation (extends expiry)
- Or send new invitation

## Related Documentation

- [Story 1.3: RBAC Middleware](./rbac-middleware-guide.md)
- [Story 1.5: First-Time Onboarding](./onboarding-flow-guide.md)
- [Story 1.6: Team Invitation System](../stories/story-1.6.md)
- [Story 1.7: Invitation Acceptance](../stories/story-1.7.md) (Future)

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| FRONTEND_URL | Frontend base URL for invitation links | http://localhost:3000 | Yes |
| EMAIL_PROVIDER | Email service provider (mailhog/smtp) | mailhog | Yes |
| MAILHOG_HOST | MailHog SMTP host | localhost | If using MailHog |
| MAILHOG_PORT | MailHog SMTP port | 1025 | If using MailHog |

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-16 | 1.0 | Initial documentation for Story 1.6 |
```

