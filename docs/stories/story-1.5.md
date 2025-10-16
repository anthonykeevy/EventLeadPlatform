# Story 1.5: First-Time User Onboarding

Status: Ready for Review

## Story

As a newly verified user,
I want to complete my profile and create my first company,
so that I can start using the EventLead platform.

## Acceptance Criteria

1. **AC-1.5.1**: Protected endpoint for completing user details (requires authentication)
2. **AC-1.5.2**: User can update: phone number, timezone, profile information
3. **AC-1.5.3**: Protected endpoint for creating first company (requires authentication)
4. **AC-1.5.4**: Company created with name, ABN/ACN, address details
5. **AC-1.5.5**: UserCompany relationship created with role = "company_admin"
6. **AC-1.5.6**: JWT refreshed to include role and company_id
7. **AC-1.5.7**: All operations logged to audit tables
8. **AC-1.5.8**: User cannot create company if already has active company
9. **AC-1.5.9**: ABN/ACN validation (optional, Australian format)
10. **AC-1.5.10**: Timezone validation against ref.Timezone table

## Tasks / Subtasks

- [x] **Task 1: Create User Details Endpoint** (AC: 1.5.1, 1.5.2, 1.5.10)
  - [x] Create `backend/modules/users/router.py`
  - [x] Add POST /api/users/me/details endpoint
  - [x] Require authentication (Depends(get_current_user))
  - [x] Define UpdateUserDetailsSchema
  - [x] Update User: Phone, TimezoneID
  - [x] Validate timezone exists in ref.Timezone
  - [x] Test: User details updated

- [x] **Task 2: Create Company Endpoint** (AC: 1.5.3, 1.5.4, 1.5.5, 1.5.8, 1.5.9)
  - [x] Create `backend/modules/companies/router.py`
  - [x] Add POST /api/companies endpoint
  - [x] Require authentication
  - [x] Check user doesn't already have company
  - [x] Define CreateCompanySchema
  - [x] Validate ABN/ACN format (if provided)
  - [x] Create Company record
  - [x] Create UserCompany relationship (role = "company_admin")
  - [x] Test: Company created successfully
  - [x] Test: Duplicate company rejected

- [x] **Task 3: Refresh JWT with Role** (AC: 1.5.6)
  - [x] After company creation, issue new access token
  - [x] Include role = "company_admin"
  - [x] Include company_id
  - [x] Return new token in response
  - [x] Test: New token includes role and company_id

- [x] **Task 4: ABN/ACN Validation** (AC: 1.5.9)
  - [x] Update common validators
  - [x] Implement validate_abn()
  - [x] Implement validate_acn()
  - [x] Check format and checksum
  - [x] Test: Valid ABN/ACN passes
  - [x] Test: Invalid ABN/ACN fails

- [x] **Task 5: Audit Logging** (AC: 1.5.7)
  - [x] Log user details update to audit.UserAudit
  - [x] Log company creation to audit.CompanyAudit
  - [x] Log UserCompany creation to audit trail
  - [x] Test: All changes logged

- [x] **Task 6: Testing** (AC: All)
  - [x] Integration tests: Complete onboarding flow
  - [x] Security tests: Cannot create company without auth
  - [x] Validation tests: ABN/ACN, timezone

- [x] **Task 7: Documentation** (AC: All)
  - [x] Document onboarding flow
  - [x] Update API documentation

## Dev Notes

**Onboarding Flow:**
```
1. User signs up and verifies email (Story 1.1)
2. User logs in, gets JWT (no role/company) (Story 1.2)
3. User updates profile details (this story)
4. User creates company (this story)
5. UserCompany created with role = "company_admin"
6. New JWT issued with role and company_id
7. User can now access protected company endpoints
```

### References

- [Story 1.1: User Signup](docs/stories/story-1.1.md)
- [Story 1.2: Login & JWT](docs/stories/story-1.2.md)
- [Story 1.3: RBAC Middleware](docs/stories/story-1.3.md)

## Dev Agent Record

### Context Reference

- [Story Context 1.5](../story-context-1.5.xml)

### Agent Model Used

- Claude Sonnet 4.5 (Amelia - Developer Agent)

### Completion Notes List

1. **User Details Endpoint**: Created complete user profile management module (`backend/modules/users/`) with authentication-protected endpoint for updating phone, timezone, and role title.

2. **Company Creation Endpoint**: Created complete company management module (`backend/modules/companies/`) with business logic for first-time company creation, including:
   - Check for existing company (prevents duplicates)
   - ABN/ACN validation with checksum algorithms
   - UserCompany relationship creation with `company_admin` role
   - JWT refresh with role and company_id claims

3. **ABN/ACN Validation**: Implemented Australian business number validation in `backend/common/validators.py`:
   - ABN: 11-digit validation with weighted checksum algorithm
   - ACN: 9-digit validation with check digit algorithm
   - Handles spaces and formatting
   - Optional fields (validated only if provided)

4. **Audit Logging**: All operations logged to audit tables:
   - `audit.UserAudit` for profile updates
   - `audit.CompanyAudit` for company creation
   - Includes old/new values, timestamp, and user ID

5. **JWT Enhancement**: After company creation, new JWT issued with:
   - `role`: "company_admin"
   - `company_id`: <created company ID>
   - Enables access to company-scoped endpoints

6. **Testing**: Comprehensive test suites created:
   - `test_onboarding_flow.py`: Integration tests covering all ACs
   - `test_validators.py`: Unit tests for ABN/ACN validation
   - Tests cover security, validation, and complete onboarding flow

7. **Documentation**: Created comprehensive guide at `docs/technical-guides/onboarding-flow-guide.md` covering:
   - Onboarding sequence
   - API endpoints
   - ABN/ACN validation algorithms
   - JWT token structure
   - Frontend integration examples
   - Troubleshooting guide

8. **Router Registration**: Registered new routers in `backend/main.py` to expose endpoints.

9. **Linting**: Fixed type-checking issues. Remaining linting errors are SQLAlchemy ORM type-checking false positives (safe to ignore).

### File List

**Created Files:**
- `backend/modules/users/__init__.py` - Users module initialization
- `backend/modules/users/schemas.py` - Pydantic schemas for user endpoints
- `backend/modules/users/service.py` - Business logic for user profile management
- `backend/modules/users/router.py` - FastAPI router with user endpoints
- `backend/modules/companies/__init__.py` - Companies module initialization
- `backend/modules/companies/schemas.py` - Pydantic schemas for company endpoints
- `backend/modules/companies/service.py` - Business logic for company creation
- `backend/modules/companies/router.py` - FastAPI router with company endpoints
- `backend/common/validators.py` - ABN/ACN validation functions
- `backend/tests/test_onboarding_flow.py` - Integration tests for onboarding
- `backend/tests/test_validators.py` - Unit tests for ABN/ACN validators
- `docs/technical-guides/onboarding-flow-guide.md` - Complete onboarding documentation

**Modified Files:**
- `backend/main.py` - Added users and companies router registration

