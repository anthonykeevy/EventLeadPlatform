# First-Time User Onboarding Flow Guide

## Overview

This guide documents the first-time user onboarding flow implemented in Story 1.5. The flow takes a newly verified user through profile completion and company creation, resulting in a fully onboarded user with company_admin role.

## Onboarding Sequence

```
┌─────────────────────────────────────────────────────────────────────┐
│                     First-Time Onboarding Flow                      │
└─────────────────────────────────────────────────────────────────────┘

1. User Signs Up & Verifies Email (Story 1.1)
   ├─> User provides: email, password, first name, last name
   ├─> Email verification token sent
   └─> User clicks verification link

2. User Logs In (Story 1.2)
   ├─> JWT issued WITHOUT role/company_id
   ├─> Token payload: { sub, email, type: "access" }
   └─> OnboardingComplete: false

3. User Updates Profile Details (Story 1.5 - Step 1)
   ├─> POST /api/users/me/details
   ├─> Updates: phone, timezone, role_title
   ├─> Timezone validated against ref.Timezone
   └─> Changes logged to audit.UserAudit

4. User Creates Company (Story 1.5 - Step 2)
   ├─> POST /api/companies
   ├─> Validates: ABN/ACN (if provided), country, industry
   ├─> Creates: Company record
   ├─> Creates: UserCompany with role='company_admin'
   ├─> Logs: audit.CompanyAudit
   └─> Returns: New JWT with role and company_id

5. Onboarding Complete
   ├─> User.OnboardingComplete = true
   ├─> User.OnboardingStep = 5
   └─> User can now access company-scoped endpoints
```

## API Endpoints

### 1. Update User Profile Details

**Endpoint:** `POST /api/users/me/details`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "phone": "+61412345678",
  "timezone_identifier": "Australia/Sydney",
  "role_title": "Marketing Manager"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "User details updated successfully",
  "user_id": 123
}
```

**Validation:**
- `phone`: Optional, max 20 characters
- `timezone_identifier`: Required, must exist in `ref.Timezone` table
- `role_title`: Optional, max 100 characters

**Error Responses:**
- `401 Unauthorized`: Missing or invalid JWT
- `400 Bad Request`: Invalid timezone or validation error

### 2. Create First Company

**Endpoint:** `POST /api/companies`

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "company_name": "Acme Events Pty Ltd",
  "abn": "51824753556",
  "acn": "123456782",
  "phone": "+61298765432",
  "email": "info@acmeevents.com.au",
  "website": "https://acmeevents.com.au",
  "country_id": 1,
  "industry_id": 5
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Company created successfully",
  "company_id": 456,
  "user_company_id": 789,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "company_admin"
}
```

**Validation:**
- `company_name`: Required, 1-200 characters
- `abn`: Optional, 11 digits with checksum validation
- `acn`: Optional, 9 digits with checksum validation
- `phone`: Optional, max 20 characters
- `email`: Optional, valid email format
- `website`: Optional, max 500 characters
- `country_id`: Required, must exist in `ref.Country`
- `industry_id`: Optional, must exist in `ref.Industry`

**Business Rules:**
1. User can only create ONE company via this endpoint
2. Attempting to create a second company returns `400 Bad Request`
3. ABN/ACN validated if provided (optional fields)
4. UserCompany created with `role='company_admin'` and `IsPrimaryCompany=true`
5. New JWT issued with `role` and `company_id` claims
6. User's `OnboardingComplete` set to `true`

**Error Responses:**
- `401 Unauthorized`: Missing or invalid JWT
- `400 Bad Request`: 
  - User already has active company
  - Invalid ABN/ACN checksum
  - Invalid country_id or industry_id
  - Validation errors

## ABN/ACN Validation

### Australian Business Number (ABN)

**Format:** 11 digits (spaces allowed)

**Validation Algorithm:**
1. Remove all non-digit characters
2. Check length = 11 digits
3. Subtract 1 from first digit
4. Apply weights: [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
5. Calculate: sum(digit * weight)
6. Check: sum % 89 == 0

**Valid Example:** `51 824 753 556`

**Code Example:**
```python
from common.validators import validate_abn

is_valid, error = validate_abn("51 824 753 556")
if not is_valid:
    print(f"Invalid ABN: {error}")
```

### Australian Company Number (ACN)

**Format:** 9 digits (spaces allowed)

**Validation Algorithm:**
1. Remove all non-digit characters
2. Check length = 9 digits
3. Apply weights to first 8 digits: [8, 7, 6, 5, 4, 3, 2, 1]
4. Calculate: (10 - (sum % 10)) % 10
5. Compare with 9th digit (check digit)

**Valid Example:** `123 456 782`

**Code Example:**
```python
from common.validators import validate_acn

is_valid, error = validate_acn("123 456 782")
if not is_valid:
    print(f"Invalid ACN: {error}")
```

## JWT Token Claims

### Before Company Creation

```json
{
  "sub": 123,
  "email": "user@example.com",
  "type": "access",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### After Company Creation

```json
{
  "sub": 123,
  "email": "user@example.com",
  "role": "company_admin",
  "company_id": 456,
  "type": "access",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Note:** Frontend must store and use the NEW token returned from company creation endpoint.

## Database Changes

### Tables Modified

1. **dbo.User**
   - `Phone` updated
   - `TimezoneIdentifier` updated
   - `RoleTitle` updated
   - `OnboardingComplete` set to `true`
   - `OnboardingStep` set to `5`

2. **dbo.Company** (created)
   - New company record with provided details

3. **dbo.UserCompany** (created)
   - Links user to company
   - `UserCompanyRoleID` → company_admin role
   - `IsPrimaryCompany` = `true`
   - `StatusID` → active status
   - `JoinedViaID` → signup method

4. **audit.UserAudit** (logged)
   - Action: `UPDATE_PROFILE`
   - OldValue/NewValue: JSON of changed fields

5. **audit.CompanyAudit** (logged)
   - Action: `CREATE`
   - NewValue: JSON of company details

## Security Considerations

### Authentication Requirements
- Both endpoints require valid JWT Bearer token
- JWT must not be expired
- User must exist and be active

### Authorization Rules
1. Users can only update their OWN profile
2. Users can only create ONE company
3. ABN/ACN validation prevents fraudulent business numbers
4. SQL injection prevented via Pydantic validation and parameterized queries

### Audit Trail
All operations logged with:
- User ID who made the change
- Timestamp (UTC)
- Old and new values
- IP address (optional, via request context)
- User agent (optional, via request context)

## Frontend Integration

### Onboarding Component Flow

```typescript
// Step 1: Update user profile
const updateProfile = async () => {
  const response = await fetch('/api/users/me/details', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      phone: '+61412345678',
      timezone_identifier: 'Australia/Sydney',
      role_title: 'Event Manager'
    })
  });
  
  if (!response.ok) {
    // Handle error
    return;
  }
  
  // Proceed to company creation
};

// Step 2: Create company
const createCompany = async () => {
  const response = await fetch('/api/companies', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      company_name: 'Acme Events Pty Ltd',
      abn: '51 824 753 556',
      acn: '123 456 782',
      country_id: 1,
      industry_id: 5
    })
  });
  
  if (!response.ok) {
    // Handle error
    return;
  }
  
  const data = await response.json();
  
  // IMPORTANT: Store new tokens
  localStorage.setItem('accessToken', data.access_token);
  localStorage.setItem('refreshToken', data.refresh_token);
  
  // Redirect to dashboard
  window.location.href = '/dashboard';
};
```

### Error Handling

```typescript
interface ErrorResponse {
  detail: string;
}

const handleApiError = (error: ErrorResponse) => {
  if (error.detail.includes('timezone')) {
    // Show timezone error
  } else if (error.detail.includes('ABN')) {
    // Show ABN validation error
  } else if (error.detail.includes('already has')) {
    // User already has company - redirect to dashboard
    window.location.href = '/dashboard';
  }
};
```

## Testing

### Integration Tests

Location: `backend/tests/test_onboarding_flow.py`

**Coverage:**
- AC-1.5.1: Protected endpoints require auth
- AC-1.5.2: User details update
- AC-1.5.3: Company creation requires auth
- AC-1.5.4: Company created with details
- AC-1.5.5: UserCompany relationship created
- AC-1.5.6: JWT refreshed with role and company_id
- AC-1.5.7: Audit logging
- AC-1.5.8: Duplicate company prevention
- AC-1.5.9: ABN/ACN validation
- AC-1.5.10: Timezone validation

### Unit Tests

Location: `backend/tests/test_validators.py`

**Coverage:**
- ABN validation with checksum
- ACN validation with checksum
- Edge cases (spaces, empty strings, None)
- Invalid inputs (wrong length, non-numeric, SQL injection)

### Running Tests

```bash
# Run all onboarding tests
pytest backend/tests/test_onboarding_flow.py -v

# Run validator tests
pytest backend/tests/test_validators.py -v

# Run with coverage
pytest backend/tests/test_onboarding_flow.py --cov=modules.users --cov=modules.companies
```

## Troubleshooting

### User Cannot Create Company

**Symptom:** `400 Bad Request: User already has an active company`

**Cause:** User already has a UserCompany relationship with active status

**Resolution:**
1. Check `dbo.UserCompany` for existing relationships
2. If user legitimately needs new company, admin must deactivate existing relationship
3. Or: Direct user to their existing company dashboard

### Invalid Timezone Error

**Symptom:** `400 Bad Request: Invalid timezone`

**Cause:** Timezone not found in `ref.Timezone` table

**Resolution:**
1. Check available timezones: `SELECT * FROM ref.Timezone`
2. Use IANA timezone identifiers (e.g., "Australia/Sydney", not "AEST")
3. Ensure reference data is seeded correctly

### ABN/ACN Validation Fails

**Symptom:** `400 Bad Request: Invalid ABN checksum`

**Cause:** ABN/ACN has invalid checksum

**Resolution:**
1. Verify ABN/ACN with ABR (Australian Business Register)
2. ABN/ACN are optional fields - can be left empty
3. Use ABN Lookup tool: https://abr.business.gov.au/

## Related Documentation

- [Story 1.1: User Signup](../stories/story-1.1.md)
- [Story 1.2: Login & JWT](../stories/story-1.2.md)
- [Story 1.3: RBAC Middleware](./rbac-middleware-guide.md)
- [Story 1.5: First-Time User Onboarding](../stories/story-1.5.md)

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-16 | 1.0 | Initial documentation for Story 1.5 |

