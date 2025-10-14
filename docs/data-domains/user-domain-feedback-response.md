# User Domain - Response to Feedback

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Version:** 2.0.0

---

## Summary of Changes Based on Your Feedback

### ✅ **1. Multi-Company Access - NOW INCLUDED IN MVP**

**Your Feedback:** "Multi-company access should be included. I think very easy from the database."

**My Response:** Absolutely correct! It's straightforward from the database perspective.

**What I Changed:**

#### New Table: `UserCompany` (Many-to-Many Relationship)

```sql
CREATE TABLE [UserCompany] (
    UserCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,  -- Surrogate key per your requirement
    UserID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    Role NVARCHAR(20) NOT NULL,  -- Role per company (Admin in one, User in another)
    Status NVARCHAR(20) NOT NULL DEFAULT 'active',
    IsDefaultCompany BIT NOT NULL DEFAULT 0,  -- Which company loads on login
    JoinedDate DATETIME2 NOT NULL,
    JoinedVia NVARCHAR(20) NOT NULL,  -- 'signup', 'invitation', 'transfer'
    -- ... audit fields
);
```

**Use Cases Now Supported:**

| Scenario | Before (PRD) | After (v2) |
|----------|--------------|------------|
| Freelance designer works with 3 clients | ❌ Could only join 1 company | ✅ Joins 3 companies, switches via dropdown |
| Consultant joins client workspaces | ❌ Single company only | ✅ Joins multiple workspaces |
| User switches companies but needs historical access | ❌ Lost access to old company | ✅ Retains access to both |
| User creates personal workspace + joins team | ❌ Complex workaround needed | ✅ Natural flow (personal + team company) |

**Implementation Notes:**

1. **Default Company Logic:**
   - First company user joins → `IsDefaultCompany = 1`
   - User can change default company in settings
   - On login, load default company's dashboard
   - Navbar has company switcher dropdown

2. **RBAC Per Company:**
   - User can be **Admin** in Company A, **User** in Company B
   - Each `UserCompany` record has its own `Role` field
   - Middleware checks: "Does current user have 'company_admin' role in THIS company?"

3. **Database Queries (Example):**

```sql
-- Get all companies user belongs to
SELECT c.*, uc.Role, uc.IsDefaultCompany
FROM UserCompany uc
INNER JOIN Company c ON uc.CompanyID = c.CompanyID
WHERE uc.UserID = @CurrentUserID 
  AND uc.Status = 'active'
  AND uc.IsDeleted = 0;

-- Check if user has admin access to specific company
SELECT COUNT(*) 
FROM UserCompany 
WHERE UserID = @CurrentUserID 
  AND CompanyID = @TargetCompanyID 
  AND Role = 'company_admin'
  AND Status = 'active';
```

**Effort Estimate:** 2-3 days (database + backend models + frontend company switcher)

---

### ✅ **2. 2FA - Confirmed Phase 2**

**Your Feedback:** "2FA is practical for Stripe but our users are paying us and don't have access to anything where we pay them. Nice to have but Phase 2"

**My Response:** Agreed! Your reasoning is sound. Stripe needs 2FA because users access financial data and can initiate payouts. Your users pay you (one-way transaction), so 2FA is nice-to-have for account security but not critical.

**Recommendation:** Keep in Phase 2 roadmap for enterprise customers who may require 2FA for compliance (SOC 2, ISO 27001).

---

### ✅ **3. Company Info During Onboarding - Keep Mandatory**

**Your Feedback:** "I am hesitant to allow skipping company info because it is required for Billing and one of the main dashboard filters are tied to the Company. I suppose if we can make it work and not create a barrier at the checkout I am fine but let's try and get as much Company information as we can during the onboarding."

**My Response:** You're absolutely right to keep it mandatory! Your reasoning is solid:

1. **Billing Requirement:** You need ABN + Billing Address for GST-compliant Australian tax invoices (legal requirement)
2. **Dashboard Architecture:** Company is the primary tenant boundary - skipping it breaks dashboard filters
3. **Business Model:** Company-based billing (not per-user) requires company entity from day 1

**My Original Concern (Now Addressed):**
- I was worried about solo users feeling friction ("Why do I need a company if I'm alone?")
- But your freemium model ("Create Free, Pay to Publish") means no payment barrier upfront
- User can explore platform for free, create drafts, test forms
- Company info collected once during onboarding, used later at checkout (no barrier)

**Updated Recommendation: Keep Mandatory, Add One Improvement**

**Current Flow:**
1. Signup → Email verification → Login
2. Onboarding Step 1: User details
3. Onboarding Step 2: Company details
4. Dashboard unlocked

**Improvement: Auto-Save Progress (No Data Loss)**

```
┌─────────────────────────────────────────────┐
│ Onboarding - Step 1 of 2: User Details     │
├─────────────────────────────────────────────┤
│ First Name: [Jane         ] ✓ Auto-saved   │
│ Last Name:  [Smith        ] ✓ Auto-saved   │
│ Phone:      [+61 4XX XXX  ] ✓ Auto-saved   │
│                                             │
│ [Next: Company Details →]                   │
└─────────────────────────────────────────────┘
```

**Implementation:**
- Auto-save Step 1 fields to database (set `User.OnboardingComplete = 0`)
- If user closes browser, next login → Resume at Step 2 (Step 1 already saved)
- No "Save Draft" button needed - auto-save on blur/change

**Database State:**

| Field | After Step 1 | After Step 2 |
|-------|--------------|--------------|
| `User.FirstName` | "Jane" ✓ | "Jane" ✓ |
| `User.OnboardingComplete` | 0 (incomplete) | 1 (complete) ✓ |
| `User.CompanyID` | NULL | 123 ✓ |
| `Company` record | Not created yet | Created ✓ |
| `UserCompany` record | Not created yet | Created ✓ |

**Benefit:** User doesn't lose Step 1 data if browser crashes during Step 2. Reduces friction without removing company requirement.

---

### ✅ **4. Invited User Flow Recommendations - Agreed!**

**Your Feedback:** "I agree with recommendation"

**My Response:** Great! Here's what we're implementing:

#### Recommendation 1: Invitation Preview Page

**Current Flow (PRD):**
```
Invitee clicks link → Immediately prompted to set password → Committed to joining
```

**Improved Flow:**
```
Invitee clicks link → Preview page shows:
  - "You've been invited to join Acme Corp as Company User"
  - Invited by: Jane Smith (jane@acmecorp.com)
  - Company logo
  - [Accept & Join] button
  - [Decline Invitation] button
  
If Accept → Proceed to password setup
If Decline → Mark invitation as 'declined', notify Admin
```

**Database Changes:**
- `InvitationStatus` lookup table includes 'declined' status
- `Invitation.DeclinedAt` timestamp
- `Invitation.DeclineReason` (optional feedback from invitee)

**Benefit:** Invitee sees what they're committing to before setting password. Can gracefully decline if wrong email or company.

---

### ✅ **5. Password Reset Flow - Agreed (Clarified)**

**Your Feedback:** "I agree with first 3 Recommendations but not 4th Problem"

**My Response:** You're absolutely right! I was confusing two different flows. Let me clarify:

#### Two Separate Flows (Not One)

**Flow 1: "Forgot Password" (User Locked Out)**
- **Trigger:** User clicks "Forgot Password" on login page
- **Old Password Required?** ❌ NO (that's the point - they forgot it!)
- **Flow:** Enter email → Receive reset link → Set new password → Login
- **Your PRD:** ✅ Correct as-is
- **My #4 Recommendation:** ❌ Wrong - Ignore it

**Flow 2: "Change Password" (User Logged In)**
- **Trigger:** User clicks "Change Password" in settings (while logged in)
- **Old Password Required?** ✅ YES (security best practice)
- **Flow:** Enter old password → Enter new password → Confirm → Password updated
- **Your PRD:** Not documented (assumed not in MVP)
- **Recommendation:** Add in Phase 2

**What I Got Wrong:**
I suggested requiring old password for "Forgot Password" flow - that's nonsensical! You're right to disagree.

**What I Should Have Said:**
"Forgot Password" (your PRD) is correct. "Change Password" (future feature) should require old password.

**Updated Recommendations (Agreed Upon):**

| # | Recommendation | Status |
|---|----------------|--------|
| 1 | Password reset token expiry (1 hour) | ✅ Agreed - Implemented in v2 schema |
| 2 | Rate limiting (max 3 reset requests per hour) | ✅ Agreed - Implement in backend |
| 3 | "Logout all devices" on password reset | ✅ Agreed - Implemented via `RefreshTokenVersion` |
| 4 | ~~Old password required for reset~~ | ❌ Wrong recommendation - Discard |

---

### ✅ **6. Status Fields → Lookup Tables**

**Your Feedback:** "For fields like Status (or any type of status) we need to create a UserStatus table with clear definitions for each status."

**My Response:** EXCELLENT architectural decision! This is a best practice I should have recommended from the start.

#### What I Changed

**Before (CHECK Constraint Pattern):**
```sql
CREATE TABLE [User] (
    Status NVARCHAR(20) NOT NULL DEFAULT 'active',
    CONSTRAINT CK_User_Status CHECK (
        Status IN ('active', 'suspended', 'locked', 'deleted')
    )
);
```

**After (Lookup Table Pattern):**

**Step 1: Create Lookup Table**
```sql
CREATE TABLE [UserStatus] (
    StatusCode NVARCHAR(20) PRIMARY KEY,  -- 'active', 'suspended', 'locked', 'deleted'
    DisplayName NVARCHAR(50) NOT NULL,     -- "Active", "Suspended", "Locked", "Deleted"
    Description NVARCHAR(500) NOT NULL,    -- Clear definition of what status means
    AllowLogin BIT NOT NULL,               -- Can user log in with this status?
    IsSystemStatus BIT NOT NULL,           -- Can admin delete this status?
    SortOrder INT NOT NULL                 -- Display order in UI
);

-- Insert standard statuses
INSERT INTO [UserStatus] VALUES
    ('active', 'Active', 'User account is active and can log in normally', 1, 1, 1),
    ('unverified', 'Unverified Email', 'User signed up but has not verified email yet', 0, 1, 2),
    ('suspended', 'Suspended', 'Account suspended by admin (billing issue, policy violation)', 0, 1, 3),
    ('locked', 'Locked', 'Temporarily locked due to failed login attempts (15 min)', 0, 1, 4),
    ('deleted', 'Deleted', 'Soft-deleted account (retain data for audit trail)', 0, 1, 5);
```

**Step 2: Reference in User Table**
```sql
CREATE TABLE [User] (
    Status NVARCHAR(20) NOT NULL DEFAULT 'unverified',
    CONSTRAINT FK_User_Status FOREIGN KEY (Status) REFERENCES [UserStatus](StatusCode)
);
```

**Benefits (Why This is Better):**

| Aspect | CHECK Constraint | Lookup Table | Winner |
|--------|------------------|--------------|--------|
| **Add New Status** | ALTER TABLE + Constraint change (requires downtime) | INSERT INTO lookup table (no downtime) | ✅ Lookup |
| **Status Definition** | No definition stored (developers guess) | Clear description per status | ✅ Lookup |
| **Business Rules** | Hardcoded in application code | Stored with status (`AllowLogin` flag) | ✅ Lookup |
| **UI Display** | Hardcode display names in frontend | Query lookup table for `DisplayName` | ✅ Lookup |
| **Audit Trail** | No audit of status changes | Can audit when status definitions change | ✅ Lookup |
| **Workflow Rules** | No workflow stored | Can add `ValidTransitions` field (Phase 2) | ✅ Lookup |

**Example Workflow Rules (Phase 2):**
```sql
-- Add workflow transitions to UserStatus
ALTER TABLE [UserStatus] ADD ValidNextStatuses NVARCHAR(200);

UPDATE [UserStatus] SET ValidNextStatuses = 'unverified,suspended,deleted' WHERE StatusCode = 'active';
UPDATE [UserStatus] SET ValidNextStatuses = 'active,deleted' WHERE StatusCode = 'unverified';
-- etc.
```

**Lookup Tables Created in v2:**

1. **UserStatus** (5 standard statuses)
   - active, unverified, suspended, locked, deleted

2. **InvitationStatus** (5 standard statuses)
   - pending, accepted, expired, cancelled, declined

**Future Lookup Tables (Other Domains):**
- `EventStatus` (draft, published, live, completed, cancelled)
- `FormStatus` (draft, published, unpublished, archived)
- `PaymentStatus` (pending, succeeded, failed, refunded)

---

### ✅ **7. UserCompanyID - Added as Surrogate Primary Key**

**Your Feedback:** "For the Table UserCompany it must have an UserCompanyID even if it has a composite key."

**My Response:** Good catch! You want a surrogate primary key even though we have a natural composite key (UserID, CompanyID).

#### What I Changed

**Before (Composite Primary Key Only):**
```sql
CREATE TABLE [UserCompany] (
    UserID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    -- ... other fields
    PRIMARY KEY (UserID, CompanyID)  -- Composite key
);
```

**After (Surrogate + Composite Unique):**
```sql
CREATE TABLE [UserCompany] (
    UserCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,  -- Surrogate key
    UserID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    -- ... other fields
    CONSTRAINT UX_UserCompany_User_Company UNIQUE (UserID, CompanyID)  -- Still enforce uniqueness
);
```

**Benefits of Surrogate Key:**

| Scenario | Composite PK | Surrogate PK + Unique | Winner |
|----------|--------------|------------------------|--------|
| **Foreign Keys from Other Tables** | `FOREIGN KEY (UserID, CompanyID)` (2 columns) | `FOREIGN KEY (UserCompanyID)` (1 column) | ✅ Surrogate (simpler) |
| **ORM Relationships** | Complex (multi-column FK) | Simple (single-column FK) | ✅ Surrogate |
| **URL Routes** | `/api/user-companies/{userId}/{companyId}` (2 params) | `/api/user-companies/{id}` (1 param) | ✅ Surrogate |
| **Change User or Company** | Cannot change PK columns (must delete + re-insert) | Can change UserID/CompanyID (PK unchanged) | ✅ Surrogate |
| **Uniqueness Enforcement** | Built-in via PK | Requires separate UNIQUE constraint | ✅ Composite |

**Best Practice:** Surrogate PK (`UserCompanyID`) + Unique constraint on natural key (`UserID, CompanyID`) = Best of both worlds ✅

**Example Future Use Case:**
```sql
-- ActivityLog references UserCompanyID (simpler than composite FK)
CREATE TABLE [ActivityLog] (
    ActivityID BIGINT PRIMARY KEY,
    UserCompanyID BIGINT NOT NULL,  -- Single-column FK
    Action NVARCHAR(50),
    -- ...
    CONSTRAINT FK_ActivityLog_UserCompany FOREIGN KEY (UserCompanyID) 
        REFERENCES [UserCompany](UserCompanyID)
);
```

---

### ✅ **8. Session Management - Clarified with JWT Strategy**

**Your Feedback:** "If a user does not logout at work and gets home to continue working what happens to the session Management?"

**My Response:** Great question! This is critical for UX. Let me explain how JWT tokens work in modern SaaS:

#### JWT Token Strategy (Access + Refresh Tokens)

**Problem:** If JWT never expires, security risk (stolen token = permanent access). If JWT expires quickly, user must re-login constantly (poor UX).

**Solution:** Two-token system

##### Token 1: Access Token (Short-Lived, 1 Hour)

```json
{
  "user_id": 123,
  "email": "jane@acmecorp.com",
  "company_id": 456,
  "role": "company_admin",
  "session_token": "abc123xyz",
  "access_token_version": 1,
  "exp": 1697234567  // Expires in 1 hour
}
```

- **Lifetime:** 1 hour (short-lived)
- **Storage:** Frontend memory (React state) OR httpOnly cookie
- **Usage:** Included in every API request (`Authorization: Bearer {access_token}`)
- **When Expired:** Frontend requests new access token using refresh token (auto-refresh, user doesn't notice)

##### Token 2: Refresh Token (Long-Lived, 7 Days)

```json
{
  "user_id": 123,
  "refresh_token_version": 1,
  "exp": 1697838367  // Expires in 7 days
}
```

- **Lifetime:** 7 days (long-lived)
- **Storage:** httpOnly cookie (secure, JavaScript cannot access)
- **Usage:** ONLY used to get new access token (not for API requests)
- **When Expired:** User must re-login

#### Your Scenario: Work → Home

| Time | Location | What Happens |
|------|----------|--------------|
| **9:00 AM** | Work | User logs in → Backend returns:<br>- Access Token (expires 10:00 AM)<br>- Refresh Token (expires in 7 days) |
| **9:30 AM** | Work | User makes API request → Access Token sent → ✅ Valid (not expired) |
| **10:05 AM** | Work | User makes API request → Access Token sent → ❌ Expired<br>Frontend auto-sends Refresh Token to `/auth/refresh` endpoint<br>Backend validates Refresh Token → Returns NEW Access Token (expires 11:05 AM)<br>Frontend retries original API request → ✅ Success<br>**User doesn't notice anything** (seamless) |
| **6:00 PM** | Home | User opens laptop → Access Token expired<br>Frontend auto-refreshes using Refresh Token → ✅ Success<br>User continues working seamlessly |
| **7 Days Later** | Home | Refresh Token expires → Frontend tries to refresh → ❌ Failed<br>User redirected to login page ("Session expired, please log in") |

**Bottom Line:** User can work seamlessly from work → home → work for up to 7 days without re-logging in. After 7 days of inactivity, they must login again.

#### Special Cases

**Case 1: User Resets Password**
```
User clicks "Forgot Password" → Resets password → Backend increments RefreshTokenVersion
All existing Refresh Tokens now invalid (old version number)
User must re-login on ALL devices (forced logout)
```

**Case 2: Security Breach (Suspicious Activity)**
```
Admin flags user account → Backend increments RefreshTokenVersion + AccessTokenVersion
All tokens (Access + Refresh) invalidated immediately
User forced to re-login on ALL devices
```

**Case 3: User Manually Logs Out**
```
User clicks "Logout" → Frontend deletes Access Token and Refresh Token from browser
User must re-login
```

**Case 4: "Logout All Devices" Button (Phase 2)**
```
User in Settings clicks "Logout All Devices" → Backend increments RefreshTokenVersion
All other devices forced to re-login (current device stays logged in)
Use case: User suspects stolen credentials, wants to kill all other sessions
```

#### Implementation in Schema

**Fields Added to User Table:**

```sql
SessionToken NVARCHAR(255) NULL,
-- ^ Used for "logout all devices" on password reset
-- JWT contains session_token claim - validated on each request

AccessTokenVersion INT NOT NULL DEFAULT 1,
-- ^ Increment to invalidate all access tokens immediately

RefreshTokenVersion INT NOT NULL DEFAULT 1,
-- ^ Increment to invalidate all refresh tokens (force re-login all devices)
```

**Backend Validation Logic:**

```python
# Validate Access Token on every API request
def validate_access_token(token):
    payload = jwt.decode(token)
    user = User.get(payload['user_id'])
    
    # Check 1: Token expired?
    if payload['exp'] < now():
        raise TokenExpired("Access token expired")
    
    # Check 2: Session token matches?
    if payload['session_token'] != user.SessionToken:
        raise TokenInvalid("Session invalidated (password reset)")
    
    # Check 3: Access token version matches?
    if payload['access_token_version'] != user.AccessTokenVersion:
        raise TokenInvalid("Access token revoked (security)")
    
    return user  # ✅ Valid
```

```python
# Refresh Access Token when expired
def refresh_access_token(refresh_token):
    payload = jwt.decode(refresh_token)
    user = User.get(payload['user_id'])
    
    # Check 1: Refresh token expired?
    if payload['exp'] < now():
        raise TokenExpired("Refresh token expired - login required")
    
    # Check 2: Refresh token version matches?
    if payload['refresh_token_version'] != user.RefreshTokenVersion:
        raise TokenInvalid("Refresh token revoked (password reset)")
    
    # Generate NEW Access Token
    new_access_token = jwt.encode({
        'user_id': user.UserID,
        'session_token': user.SessionToken,
        'access_token_version': user.AccessTokenVersion,
        'exp': now() + 1.hour
    })
    
    return new_access_token  # ✅ Valid for next hour
```

**Password Reset Invalidation:**

```python
def reset_password(user, new_password):
    user.PasswordHash = hash(new_password)
    user.LastPasswordChange = now()
    user.RefreshTokenVersion += 1  # Invalidate ALL refresh tokens
    user.SessionToken = generate_new_token()  # Invalidate ALL access tokens
    user.save()
    # All devices now forced to re-login
```

---

## Summary of v2 Schema Changes

| Change | Reason | Impact |
|--------|--------|--------|
| **1. UserCompany table added** | Multi-company access (Anthony's request) | ✅ Users can join multiple companies |
| **2. UserCompanyID surrogate key** | Simpler FK references (Anthony's requirement) | ✅ Easier ORM, simpler API routes |
| **3. UserStatus lookup table** | Clear status definitions (Anthony's requirement) | ✅ Better maintainability, workflow rules |
| **4. InvitationStatus lookup table** | Clear status definitions | ✅ Invitation workflow rules |
| **5. JWT token version fields** | Session management clarity (Anthony's question) | ✅ Logout all devices, password reset invalidation |
| **6. Invitation decline fields** | Invitation preview recommendation (Anthony agreed) | ✅ Invitee can decline gracefully |
| **7. Email verification timestamp** | Audit trail improvement | ✅ Track when email verified |

---

## Files Updated

| File | Version | Description |
|------|---------|-------------|
| `database/schemas/user-schema-v2.sql` | 2.0.0 | ✅ **NEW** - Includes all feedback changes |
| `database/schemas/user-schema.sql` | 1.0.0 | Deprecated (use v2 instead) |
| `docs/data-domains/user-domain-analysis.md` | 1.0.0 | Original analysis (still valid for industry research) |
| `docs/data-domains/user-domain-feedback-response.md` | 2.0.0 | ✅ **NEW** - This document |

---

## Next Steps

### Immediate (This Week)

1. ✅ Review `user-schema-v2.sql` (this document)
2. ⚠️ Run Solomon (Database Migration Validator) on v2 schema
3. ⚠️ Create Alembic migrations:
   - Migration 001: UserStatus lookup table
   - Migration 002: InvitationStatus lookup table
   - Migration 003: User table
   - Migration 004: UserCompany table (multi-company)
   - Migration 005: Invitation table

### Backend Implementation (Next Week)

4. ⚠️ Implement models:
   - `models/user.py` with multi-company relationship
   - `models/user_company.py`
   - `models/invitation.py`
   - `models/user_status.py`
   - `models/invitation_status.py`

5. ⚠️ Implement JWT refresh token logic:
   - `/auth/login` → Return access token + refresh token
   - `/auth/refresh` → Accept refresh token, return new access token
   - Middleware to validate access token version + session token

6. ⚠️ Implement multi-company context:
   - Middleware to detect current company (from JWT or header)
   - Company switcher API (`POST /auth/switch-company/{companyId}`)
   - Default company logic

### Frontend Implementation (Week After)

7. ⚠️ Implement JWT token management:
   - Store access token in memory (React Context)
   - Store refresh token in httpOnly cookie
   - Auto-refresh logic (intercept 401 errors, refresh, retry)

8. ⚠️ Implement company switcher:
   - Navbar dropdown: "Switch Company"
   - List all companies user belongs to
   - Click company → Call `/auth/switch-company` → Reload dashboard

---

## Questions Answered

### Q1: "Multi-company access - is it easy from database?"

**A:** Yes! It's a classic many-to-many relationship (UserCompany junction table). Implementation is straightforward:
- **Database:** 1 new table (UserCompany)
- **Backend:** 1 new model + multi-company context middleware
- **Frontend:** Company switcher dropdown in navbar
- **Effort:** 2-3 days

### Q2: "What happens to session if user doesn't logout at work, goes home?"

**A:** User continues working seamlessly for up to 7 days:
- **Access Token (1 hour)** expires → Auto-refreshes using Refresh Token → User doesn't notice
- **Refresh Token (7 days)** expires → User must re-login
- **Password Reset** → Invalidates all tokens → User forced to re-login all devices

### Q3: "Should company info be optional during onboarding?"

**A:** No, keep mandatory because:
1. **Billing:** ABN + Address required for GST invoices (legal)
2. **Architecture:** Company is primary tenant boundary
3. **Your business model:** No payment upfront, so no friction

**Improvement:** Add auto-save progress (user doesn't lose data if browser crashes mid-onboarding)

---

## Compliance Check

### Solomon's Standards (Database Schema)

| Standard | v1 Schema | v2 Schema | Status |
|----------|-----------|-----------|--------|
| PascalCase naming | ✅ | ✅ | Pass |
| NVARCHAR for text | ✅ | ✅ | Pass |
| DATETIME2 with UTC | ✅ | ✅ | Pass |
| Soft deletes (IsDeleted) | ✅ | ✅ | Pass |
| Full audit trail | ✅ | ✅ | Pass |
| Foreign key constraints | ✅ | ✅ | Pass |
| Lookup tables for enums | ❌ | ✅ | **Improved in v2** |
| Surrogate keys | Partial | ✅ | **Fixed in v2** |

---

## Conclusion

All your feedback has been incorporated into **user-schema-v2.sql**. The schema now includes:

✅ Multi-company access (UserCompany table)  
✅ Lookup tables for statuses (UserStatus, InvitationStatus)  
✅ UserCompanyID surrogate primary key  
✅ JWT session management clarity (Access + Refresh tokens)  
✅ Company onboarding kept mandatory (required for billing)  
✅ Invitation decline flow (invitee can decline gracefully)  
✅ Full audit trails (Solomon's standards)

Ready for Solomon's validation and Alembic migration creation!

---

**Dimitri** 🔍  
*Data Domain Architect*  
*"Listening to your feedback, building what you need"*



