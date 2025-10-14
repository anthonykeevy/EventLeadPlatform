# User Domain Analysis - EventLeadPlatform

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Version:** 1.0.0  
**Status:** Complete Analysis - Ready for Implementation

---

## Executive Summary

### Domain Purpose

The **User domain** is the foundation of EventLeadPlatform's multi-tenant SaaS architecture. It manages:
- **User Identity & Authentication** - Email/password, email verification, password reset, JWT sessions
- **Role-Based Access Control (RBAC)** - 3 roles: System Admin, Company Admin, Company User
- **Team Collaboration** - Invitation-based user onboarding, team management
- **Multi-Tenant Isolation** - User-to-Company relationships, data access control

### Current Status

❗ **CRITICAL GAP IDENTIFIED:**

| Component | Status |
|-----------|--------|
| PRD Design | ✅ Complete (detailed user model, flows, RBAC) |
| Database Schema | ❌ **MISSING** - No `user-schema.sql` |
| Database Migrations | ❌ **MISSING** - No Alembic migrations |
| Backend Models | ❌ **MISSING** - `backend/models/` is empty |
| Auth Module | ❌ **MISSING** - `backend/modules/auth/` is empty |
| Domain Documentation | ❌ **MISSING** - This is first User domain doc |

**Consequence:** Company and Event schemas cannot be executed (FK constraints reference non-existent User table).

**Recommendation:** Implement User domain FIRST before proceeding with other domains.

---

## Industry Research - Competitor Analysis

### Multi-Tenant SaaS Platforms (User Management Patterns)

#### 1. **Canva** (Design Collaboration Platform)

**User Model:**
- Email-based signup with social auth (Google, Facebook)
- Free tier (unlimited users) + Paid teams (Canva Pro, Enterprise)
- Invitation-based team onboarding (7-day expiry, resend capability)
- Roles: Owner, Admin, Member, Template Designer
- Onboarding: Progressive disclosure (start designing immediately, upgrade prompts later)

**Key Insights:**
- ✅ **Freemium without seat limits** (like EventLead MVP) - increases viral adoption
- ✅ **Invitation expiry + resend** - prevents stale invites cluttering system
- ✅ **Progressive onboarding** - Collect minimal info upfront, more details later
- ⚠️ **Complex RBAC** - 4 roles may be overkill for MVP (EventLead has 3, good balance)

**Lessons for EventLead:**
- Match invitation expiry (7 days standard)
- Allow resend capability
- Progressive onboarding: User details first, company details optional at start (contradicts current PRD - see recommendations)

---

#### 2. **Typeform** (Form Builder SaaS)

**User Model:**
- Email-based signup + Google SSO
- Free tier (10 responses/month) + Paid plans (per-seat pricing)
- Workspaces (equivalent to EventLead's Company)
- Roles: Admin, Member
- Onboarding: Email verification → Build first form immediately (no mandatory company setup)

**Key Insights:**
- ✅ **2-role system** - Simpler than EventLead (3 roles), but EventLead needs Company User (can't publish) - justified
- ✅ **No mandatory company setup** - Users can start alone, add company later
- ✅ **JWT + Refresh tokens** - Standard auth pattern
- ⚠️ **Per-seat pricing** - EventLead avoiding this for MVP (smart - reduces friction)

**Lessons for EventLead:**
- Consider making company setup optional at signup (user creates personal workspace, converts to company later)
- Refresh token pattern for JWT (longer sessions, better UX)

---

#### 3. **Eventbrite** (Event Management Platform)

**User Model:**
- Email-based signup + social auth
- Free tier (free events) + Paid tier (% of ticket sales)
- Organizer accounts (single user or team)
- Roles: Account Owner, Admin, Manager (financial), Team Member
- Multi-brand support: One user can manage multiple organizer accounts

**Key Insights:**
- ✅ **Multi-brand support** - One user, multiple companies (EventLead should consider this)
- ✅ **Financial role separation** - "Manager" can view reports but not change event settings
- ✅ **Progressive company creation** - Start solo, add team later
- ⚠️ **4 roles** - More complex, but EventLead's 3 roles cover same use cases

**Lessons for EventLead:**
- **Multi-company user access** - User should be able to join multiple companies (not in current PRD)
- **Audit trail importance** - Track who created/published what (EventLead already has this in Company/Event schemas)

---

#### 4. **Slack** (Team Collaboration SaaS)

**User Model:**
- Email-based signup + magic link (passwordless option)
- Workspace-based multi-tenancy (like EventLead's Company)
- Roles: Workspace Owner, Workspace Admin, Member, Guest
- Invitation via email or shareable link (no expiry for open workspaces)
- Onboarding: Setup workspace → Invite team → Guided tour

**Key Insights:**
- ✅ **Magic link option** - Passwordless auth (modern UX, consider for Phase 2)
- ✅ **Workspace-first onboarding** - Name workspace immediately (EventLead does this)
- ✅ **Guest role** - Limited access for external collaborators (EventLead could add this)
- ⚠️ **No expiry on open workspaces** - Security risk, EventLead's 7-day expiry better

**Lessons for EventLead:**
- Guest role for Phase 2 (external designers/consultants)
- Magic link authentication for Phase 2 (improves UX)

---

#### 5. **Stripe** (Payment Platform - Billing Context)

**User Model:**
- Email-based signup + 2FA for financial operations
- Account-based (like EventLead's Company)
- Roles: Administrator, Developer, Analyst, View-only, Support
- Multi-account support: One user, multiple Stripe accounts
- Invitation via email (no expiry, but requires 2FA on acceptance)

**Key Insights:**
- ✅ **Financial operations 2FA** - EventLead should consider for publishing (payment trigger)
- ✅ **Multi-account support** - One user, many companies (EventLead missing this)
- ✅ **Granular roles** - 5 roles, EventLead's 3 roles simpler (good for MVP)
- ⚠️ **No invitation expiry** - Security concern, EventLead's 7-day expiry better

**Lessons for EventLead:**
- 2FA for publishing/payments in Phase 2 (reduces fraud)
- Multi-company user access (one user joins multiple companies)

---

### Industry Standards Summary

| Feature | Canva | Typeform | Eventbrite | Slack | Stripe | **EventLead (Proposed)** |
|---------|-------|----------|------------|-------|--------|--------------------------|
| **Signup Method** | Email + Social | Email + Google | Email + Social | Email + Magic Link | Email only | Email only (MVP) → Social (Phase 2) |
| **Email Verification** | Yes | Yes | Yes | Yes | Yes | **Yes (MVP)** |
| **Password Reset** | Yes | Yes | Yes | Yes | Yes | **Yes (MVP)** |
| **Invitation Expiry** | 7 days | No expiry | No expiry | No expiry | No expiry | **7 days (MVP) ✅ BEST PRACTICE** |
| **Resend Invitation** | Yes | Yes | Yes | Yes | Yes | **Yes (MVP)** |
| **Multi-Company Access** | Yes | No | Yes | No | Yes | **❌ MISSING (Recommend Phase 2)** |
| **Roles (MVP)** | 4 | 2 | 4 | 4 | 5 | **3 (balanced) ✅** |
| **Mandatory Company Setup** | No | No | No | Yes | No | **Yes (PRD) - Recommend Optional** |
| **2FA** | Optional | Optional | Optional | Optional | Required (financial) | **❌ MISSING (Recommend Phase 2 for publish)** |
| **Session Management** | JWT + Refresh | JWT + Refresh | JWT + Refresh | JWT + Refresh | JWT + Refresh | **JWT only (MVP) - Add Refresh tokens** |

---

## PRD Requirements Analysis

### User Data Model (from PRD lines 652-666)

```yaml
User:
  user_id: BIGINT IDENTITY(1,1) PRIMARY KEY
  email: NVARCHAR(100) UNIQUE NOT NULL
  password_hash: NVARCHAR(255) NOT NULL
  first_name: NVARCHAR(100) NOT NULL
  last_name: NVARCHAR(100) NOT NULL
  role_title: NVARCHAR(100) NULL  # Optional job title
  phone_number: NVARCHAR(20) NULL  # Australian format +61
  company_id: BIGINT NULL  # Nullable until onboarding complete
  role: NVARCHAR(20) NOT NULL  # system_admin, company_admin, company_user
  email_verified: BIT NOT NULL DEFAULT 0
  onboarding_complete: BIT NOT NULL DEFAULT 0
  created_at: DATETIME2 NOT NULL DEFAULT GETUTCDATE()
  last_login: DATETIME2 NULL
  is_active: BIT NOT NULL DEFAULT 1
```

**PRD Gaps Identified:**

1. **No audit trail fields** - Company/Event schemas have CreatedBy, UpdatedBy, DeletedBy. User table should have UpdatedDate, UpdatedBy, IsDeleted (soft delete), DeletedDate, DeletedBy
2. **No password reset fields** - Missing password_reset_token, password_reset_expires_at
3. **No email verification token** - Missing email_verification_token, email_verification_expires_at
4. **No session/refresh token tracking** - Missing last_password_change, session_token (for logout all devices)
5. **No failed login tracking** - Security concern: No failed_login_count, locked_until (prevent brute force)
6. **No multi-company support** - User can only belong to ONE company (industry norm: users join multiple companies)
7. **No timezone preference** - User timezone for displaying dates (Australia has 3 main timezones)
8. **No profile picture** - Missing profile_picture_url (standard in modern SaaS)

---

### Invitation Data Model (from PRD lines 777-789)

```yaml
Invitation:
  invitation_id: BIGINT IDENTITY(1,1) PRIMARY KEY
  company_id: BIGINT FK (Company)
  invited_by_user_id: BIGINT FK (User)
  invited_email: NVARCHAR(100) NOT NULL
  invited_first_name: NVARCHAR(100) NOT NULL
  invited_last_name: NVARCHAR(100) NOT NULL
  assigned_role: NVARCHAR(20) NOT NULL  # company_admin, company_user
  invitation_token: NVARCHAR(255) UNIQUE NOT NULL
  status: NVARCHAR(20) NOT NULL  # pending, accepted, cancelled, expired
  invited_at: DATETIME2 NOT NULL DEFAULT GETUTCDATE()
  accepted_at: DATETIME2 NULL
  expires_at: DATETIME2 NOT NULL  # invited_at + 7 days
```

**PRD Gaps Identified:**

1. **No resend tracking** - Missing resend_count, last_resent_at (for rate limiting abuse)
2. **No cancellation audit** - Missing cancelled_by, cancelled_at (who cancelled invitation?)
3. **No email sent tracking** - Missing email_sent_at, email_sent_status (did email actually send?)
4. **No accepted_by_user_id** - Who accepted invitation? (for audit trail)

---

### RBAC Requirements (from PRD lines 108-141)

#### Role Definitions

| Role | Access Level | Key Permissions |
|------|--------------|-----------------|
| **System Admin** | Platform-level | - Full access across ALL companies<br>- Manage platform settings<br>- Monitor system health<br>- Backend access only (no UI for MVP)<br>- Handle customer support escalations |
| **Company Admin** | Company-level | - Full company dashboard access<br>- Manage company details (name, ABN, billing)<br>- Invite/remove team members<br>- Assign roles (promote to Admin, demote to User)<br>- View/manage billing and invoices<br>- Create/edit/delete/publish events<br>- Create/edit/delete/publish forms<br>- View analytics for ALL company forms<br>- Export data |
| **Company User** | Company-level (Limited) | - Read-only company settings<br>- Create/edit/delete events<br>- Create/edit/delete forms (CANNOT publish)<br>- Request Admin to publish forms<br>- View analytics for THEIR forms only<br>- Export data from THEIR forms<br>- **CANNOT:** Publish forms, manage billing, invite users, modify company |

**RBAC Gap Identified:**

- **No permission granularity** - All-or-nothing permissions per role. Industry norm: Permission matrix (e.g., Stripe's 5 roles with granular permissions).
- **Recommendation:** For MVP, keep 3 roles simple. For Phase 2, add permission matrix (e.g., Company User can "view all analytics" if Admin grants permission).

---

## Authentication Flows Analysis

### 1. New Company Sign Up & Onboarding (from PRD lines 819-860)

**Phase 1 - Sign Up & Verification (Unauthenticated):**
1. User visits landing page → Clicks "Get Started" / "Sign Up"
2. Enters email and password on signup form
3. Submits form
4. System sends verification email with secure token link
5. Message displayed: "Check your email to verify your account"
6. User checks email, clicks verification link
7. Redirected to login page with "Email verified! Please log in" message

**Phase 2 - Login & Authentication:**
8. User enters email/password on login page
9. System validates credentials
10. System generates JWT token for session
11. System checks: Has user completed onboarding? → NO

**Phase 3 - Onboarding (Authenticated, Inside App):**
12. Onboarding modal/screen appears (cannot dismiss, required)
13. **Onboarding Step 1 - User Details:**
    - First Name (required)
    - Last Name (required)
    - Role/Title (optional, e.g., "Marketing Manager")
    - Phone Number (optional, Australian format +61)
    - Click "Next"
14. **Onboarding Step 2 - Company Setup:**
    - Company Name (required)
    - ABN (Australian Business Number - 11 digits, validated)
    - Billing Address (required, Australian address)
    - Company Phone (optional)
    - Industry (dropdown, optional)
    - Click "Complete Setup"
15. System creates company record
16. User automatically assigned Company Admin role
17. Onboarding complete flag set (`user.onboarding_complete = true`)
18. Dashboard loads with welcome overlay/tutorial

**Flow Issues Identified:**

❌ **Problem 1: Mandatory Company Setup Too Early**
- **Issue:** Forces single user to create company before exploring platform
- **Industry Norm:** Typeform, Canva, Figma allow solo users to start immediately, add team later
- **User Story:** "I want to try the platform alone before inviting my team"
- **Recommendation:** Make company setup OPTIONAL at signup. User starts with "Personal Workspace" (no company_id), converts to company when inviting first team member.

❌ **Problem 2: No "Save Draft" in Onboarding**
- **Issue:** If user closes browser mid-onboarding, they lose progress
- **Recommendation:** Auto-save onboarding progress (Step 1 complete → can resume at Step 2)

❌ **Problem 3: No "Skip for Now" on Optional Fields**
- **Issue:** User must fill optional fields or leave blank (unclear UX)
- **Recommendation:** Add "Skip for Now" button, return later in settings

❌ **Problem 4: Email Verification Before Login**
- **Issue:** User cannot log in until email verified (industry standard BUT causes friction)
- **Alternative:** Let user log in immediately, show banner "Please verify email" (Slack pattern)
- **Recommendation:** Keep current flow for MVP (more secure), consider Slack pattern for Phase 2

---

### 2. Invited User Flow (from PRD lines 882-935)

**Phase 1 - Invitation & Verification (Public, Unauthenticated):**
1. Company Admin sends invitation with:
   - Invitee's First Name (required)
   - Invitee's Last Name (required)
   - Invitee's Email (required)
   - Assigned Role: Company Admin OR Company User
2. Invitee receives invitation email with:
   - Welcome message
   - Company name they're joining
   - Role they'll have
   - Secure invitation token link (expires in 7 days)
3. Invitee clicks invitation link
4. Lands on invitation acceptance page showing:
   - "Join [Company Name] as [Role]"
   - Email pre-filled (read-only)
   - Password field (set new password)
5. Invitee sets password and submits
6. Email automatically marked as verified (invitation email = verification)
7. System generates JWT token for session

**Phase 2 - Onboarding (Authenticated, Inside App):**
8. After successful signup/login, check if user has completed onboarding
9. **Onboarding Step 1 - User Details:**
   - First Name (pre-filled from invitation, editable)
   - Last Name (pre-filled from invitation, editable)
   - Role/Title (optional)
   - Phone Number (optional, Australian format)
10. NO Company Setup step (joining existing company)
11. Role already assigned by Admin
12. Onboarding complete flag set
13. Redirect to company dashboard (sees existing events/forms)
14. Company Admin notified that invitee has joined

**Flow Issues Identified:**

✅ **Good Design Choices:**
- Email verification automatic (invitation link = verified email) - Smart!
- First/Last name pre-filled but editable - Good UX (Admin might have typos)
- No company setup step (already joining existing company) - Correct

❌ **Problem 1: No Invitation Preview**
- **Issue:** Invitee doesn't know what company/role they're joining until they click link and set password (committed)
- **Recommendation:** Show "Join [Company] as [Role]" BEFORE password setup (add "Decline Invitation" button)

❌ **Problem 2: No Duplicate Email Check**
- **Issue:** What if invited email already exists in system?
  - Scenario A: User exists, same company → Show error "Already a member"
  - Scenario B: User exists, different company → **Multi-company access needed** (not in PRD)
  - Scenario C: User exists, email not verified → Auto-verify on invitation acceptance
- **Recommendation:** Add duplicate email check logic in invitation flow

---

### 3. Password Reset Flow (from PRD lines 216-224)

**Flow:**
1. User clicks "Forgot Password" on login page
2. Enters email address
3. System sends password reset email with secure token link
4. User clicks link, lands on reset page
5. Enters new password (with confirmation)
6. Password updated
7. Redirect to login with success message
8. User logs in with new password

**Flow Issues Identified:**

❌ **Problem 1: No Token Expiry Specified**
- **Issue:** Password reset links should expire (security best practice)
- **Industry Norm:** 1 hour expiry (shorter than invitation 7 days)
- **Recommendation:** Add password_reset_expires_at (1 hour from generation)

❌ **Problem 2: No Rate Limiting**
- **Issue:** Attacker can spam reset emails to user's inbox (DoS attack)
- **Recommendation:** Rate limit: Max 3 reset requests per email per hour

❌ **Problem 3: No "All Devices Logged Out"**
- **Issue:** Password reset should invalidate ALL active sessions (security best practice)
- **Recommendation:** Add session_token field, invalidate on password reset

❌ **Problem 4: No Old Password Required**
- **Issue:** Current flow doesn't require old password (less secure than "Change Password" inside app)
- **Recommendation:** "Forgot Password" (no old password) vs "Change Password" (requires old password) - two separate flows

---

## Schema Design Recommendations

### Core User Tables

#### Table 1: User (Core Identity)

**Proposed Schema:**

```sql
CREATE TABLE [User] (
    -- Primary Key
    UserID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Authentication Credentials
    Email NVARCHAR(100) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    
    -- User Profile (Basic)
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    RoleTitle NVARCHAR(100) NULL,  -- Job title (optional)
    PhoneNumber NVARCHAR(20) NULL,  -- Australian format +61
    ProfilePictureUrl NVARCHAR(500) NULL,  -- Azure Blob Storage
    TimezoneIdentifier NVARCHAR(50) NULL DEFAULT 'Australia/Sydney',  -- IANA timezone
    
    -- Company Relationship (Nullable until onboarding)
    CompanyID BIGINT NULL,
    
    -- RBAC Role
    Role NVARCHAR(20) NOT NULL DEFAULT 'company_user',
    -- Options: 'system_admin', 'company_admin', 'company_user'
    
    -- Account Status Flags
    EmailVerified BIT NOT NULL DEFAULT 0,
    OnboardingComplete BIT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    
    -- Email Verification Tokens
    EmailVerificationToken NVARCHAR(255) NULL,
    EmailVerificationExpiresAt DATETIME2 NULL,
    
    -- Password Reset Tokens
    PasswordResetToken NVARCHAR(255) NULL,
    PasswordResetExpiresAt DATETIME2 NULL,
    LastPasswordChange DATETIME2 NULL,
    
    -- Session Management
    SessionToken NVARCHAR(255) NULL,  -- For "logout all devices"
    LastLogin DATETIME2 NULL,
    
    -- Security (Brute Force Protection)
    FailedLoginCount INT NOT NULL DEFAULT 0,
    LockedUntil DATETIME2 NULL,  -- Account locked after 5 failed logins
    
    -- Audit Trail (Solomon's Standards)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- Constraints
    CONSTRAINT FK_User_Company FOREIGN KEY (CompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_User_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_User_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    
    -- Role validation
    CONSTRAINT CK_User_Role CHECK (
        Role IN ('system_admin', 'company_admin', 'company_user')
    ),
    
    -- Email format validation
    CONSTRAINT CK_User_Email_Format CHECK (
        Email LIKE '%@%.%'
    )
);
GO

-- Indexes
CREATE UNIQUE INDEX UX_User_Email ON [User](Email) WHERE IsDeleted = 0;
CREATE INDEX IX_User_Company ON [User](CompanyID, IsDeleted) WHERE IsDeleted = 0;
CREATE INDEX IX_User_EmailVerificationToken ON [User](EmailVerificationToken) WHERE EmailVerificationToken IS NOT NULL;
CREATE INDEX IX_User_PasswordResetToken ON [User](PasswordResetToken) WHERE PasswordResetToken IS NOT NULL;
```

**Key Improvements Over PRD:**

| Feature | PRD Design | Improved Design | Benefit |
|---------|------------|-----------------|---------|
| **Audit Trail** | ❌ Missing | ✅ UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy | Compliance (matches Company/Event schemas) |
| **Password Reset** | ❌ No token fields | ✅ PasswordResetToken, PasswordResetExpiresAt, LastPasswordChange | Secure reset flow with expiry |
| **Email Verification** | ❌ No token fields | ✅ EmailVerificationToken, EmailVerificationExpiresAt | Secure verification with expiry |
| **Session Management** | ❌ No logout all devices | ✅ SessionToken field | Security: Invalidate all sessions on password reset |
| **Brute Force Protection** | ❌ Missing | ✅ FailedLoginCount, LockedUntil | Security: Lock account after 5 failed logins (15 min lockout) |
| **Timezone Preference** | ❌ Missing | ✅ TimezoneIdentifier | UX: Show dates in user's timezone (Australia has 3 zones) |
| **Profile Picture** | ❌ Missing | ✅ ProfilePictureUrl | UX: Modern SaaS standard |

---

#### Table 2: Invitation (Team Onboarding)

**Proposed Schema:**

```sql
CREATE TABLE [Invitation] (
    -- Primary Key
    InvitationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Company & Inviter
    CompanyID BIGINT NOT NULL,
    InvitedByUserID BIGINT NOT NULL,
    
    -- Invitee Details (Pre-filled by Admin)
    InvitedEmail NVARCHAR(100) NOT NULL,
    InvitedFirstName NVARCHAR(100) NOT NULL,
    InvitedLastName NVARCHAR(100) NOT NULL,
    AssignedRole NVARCHAR(20) NOT NULL,  -- company_admin, company_user
    
    -- Invitation Token (Secure)
    InvitationToken NVARCHAR(255) NOT NULL UNIQUE,
    
    -- Invitation Lifecycle
    Status NVARCHAR(20) NOT NULL DEFAULT 'pending',
    -- Options: 'pending', 'accepted', 'cancelled', 'expired'
    
    InvitedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ExpiresAt DATETIME2 NOT NULL,  -- InvitedAt + 7 days
    AcceptedAt DATETIME2 NULL,
    AcceptedByUserID BIGINT NULL,  -- Who accepted (for audit)
    
    -- Cancellation Audit
    CancelledAt DATETIME2 NULL,
    CancelledBy BIGINT NULL,  -- Admin who cancelled
    
    -- Resend Tracking (Rate Limiting)
    ResendCount INT NOT NULL DEFAULT 0,
    LastResentAt DATETIME2 NULL,
    
    -- Email Delivery Tracking
    EmailSentAt DATETIME2 NULL,
    EmailSentStatus NVARCHAR(20) NULL,  -- 'sent', 'failed', 'bounced'
    
    -- Audit Trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NULL,
    
    -- Constraints
    CONSTRAINT FK_Invitation_Company FOREIGN KEY (CompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_Invitation_InvitedBy FOREIGN KEY (InvitedByUserID) REFERENCES [User](UserID),
    CONSTRAINT FK_Invitation_AcceptedBy FOREIGN KEY (AcceptedByUserID) REFERENCES [User](UserID),
    CONSTRAINT FK_Invitation_CancelledBy FOREIGN KEY (CancelledBy) REFERENCES [User](UserID),
    
    -- Role validation
    CONSTRAINT CK_Invitation_Role CHECK (
        AssignedRole IN ('company_admin', 'company_user')
    ),
    
    -- Status validation
    CONSTRAINT CK_Invitation_Status CHECK (
        Status IN ('pending', 'accepted', 'cancelled', 'expired')
    )
);
GO

-- Indexes
CREATE UNIQUE INDEX UX_Invitation_Token ON [Invitation](InvitationToken);
CREATE INDEX IX_Invitation_Company_Status ON [Invitation](CompanyID, Status);
CREATE INDEX IX_Invitation_Email_Status ON [Invitation](InvitedEmail, Status);
CREATE INDEX IX_Invitation_Expiry ON [Invitation](ExpiresAt, Status) WHERE Status = 'pending';
```

**Key Improvements Over PRD:**

| Feature | PRD Design | Improved Design | Benefit |
|---------|------------|-----------------|---------|
| **Resend Tracking** | ❌ Missing | ✅ ResendCount, LastResentAt | Rate limiting: Max 3 resends per hour (prevent abuse) |
| **Cancellation Audit** | ❌ Missing | ✅ CancelledAt, CancelledBy | Compliance: Who cancelled and when |
| **Email Tracking** | ❌ Missing | ✅ EmailSentAt, EmailSentStatus | Operations: Did email actually send? Bounce handling |
| **Accepted By** | ❌ Missing | ✅ AcceptedByUserID | Audit: Who accepted invitation (important if email forwarded) |

---

#### Table 3: UserCompany (Multi-Company Access) - **NEW RECOMMENDATION**

**Problem:** PRD design allows user to belong to ONLY ONE company (`User.CompanyID` field).

**Industry Norm:** Users can join multiple companies (Eventbrite, Canva, Stripe all support this).

**Use Cases:**
1. Freelance designer works with 3 different client companies
2. Consultant joins multiple client workspaces
3. Employee switches companies but retains access to old company for historical data
4. User has personal workspace + joins team workspace

**Proposed Schema (Many-to-Many Relationship):**

```sql
CREATE TABLE [UserCompany] (
    -- Composite Primary Key
    UserID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    
    -- Role Per Company (User can be Admin in one, User in another)
    Role NVARCHAR(20) NOT NULL DEFAULT 'company_user',
    
    -- Relationship Status
    Status NVARCHAR(20) NOT NULL DEFAULT 'active',
    -- Options: 'active', 'suspended', 'removed'
    
    -- Default Company Flag (Which company loads on login)
    IsDefaultCompany BIT NOT NULL DEFAULT 0,
    
    -- Audit Trail
    JoinedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    JoinedVia NVARCHAR(20) NOT NULL,  -- 'signup', 'invitation', 'transfer'
    RemovedDate DATETIME2 NULL,
    RemovedBy BIGINT NULL,
    
    -- Constraints
    PRIMARY KEY (UserID, CompanyID),
    CONSTRAINT FK_UserCompany_User FOREIGN KEY (UserID) REFERENCES [User](UserID),
    CONSTRAINT FK_UserCompany_Company FOREIGN KEY (CompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_UserCompany_RemovedBy FOREIGN KEY (RemovedBy) REFERENCES [User](UserID),
    
    -- Role validation
    CONSTRAINT CK_UserCompany_Role CHECK (
        Role IN ('company_admin', 'company_user')
    ),
    
    -- Status validation
    CONSTRAINT CK_UserCompany_Status CHECK (
        Status IN ('active', 'suspended', 'removed')
    )
);
GO

-- Indexes
CREATE INDEX IX_UserCompany_User ON [UserCompany](UserID, Status);
CREATE INDEX IX_UserCompany_Company ON [UserCompany](CompanyID, Status);
```

**Migration Path:**

**Phase 1 (MVP):** Keep `User.CompanyID` field (simpler implementation, single company per user)

**Phase 2 (Multi-Company Support):**
1. Create UserCompany table
2. Migrate existing `User.CompanyID` → `UserCompany` rows (one row per user)
3. Remove `User.CompanyID` field (replaced by UserCompany relationship)
4. Update all queries to use UserCompany join

**Recommendation:** Implement UserCompany table from start (future-proof), but enforce single company in MVP business logic.

---

#### Table 4: ActivityLog (Audit Trail) - Already Designed in PRD

**From PRD lines 805-813:**

```sql
CREATE TABLE [ActivityLog] (
    ActivityID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    UserID BIGINT NOT NULL,
    Action NVARCHAR(50) NOT NULL,
    -- Options: 'created', 'updated', 'deleted', 'published', 'unpublished', 
    --          'invited_user', 'publish_requested', 'publish_approved', 'publish_declined', etc.
    EntityType NVARCHAR(50) NOT NULL,
    -- Options: 'form', 'event', 'user', 'company', 'invitation', 'publish_request'
    EntityID BIGINT NOT NULL,
    DetailsJSON NVARCHAR(MAX) NULL,  -- Additional context about the action
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- Constraints
    CONSTRAINT FK_ActivityLog_Company FOREIGN KEY (CompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_ActivityLog_User FOREIGN KEY (UserID) REFERENCES [User](UserID)
);
GO

-- Indexes
CREATE INDEX IX_ActivityLog_Company ON [ActivityLog](CompanyID, CreatedDate);
CREATE INDEX IX_ActivityLog_User ON [ActivityLog](UserID, CreatedDate);
CREATE INDEX IX_ActivityLog_Entity ON [ActivityLog](EntityType, EntityID);
```

**User-Related Activity Log Events:**

| Action | EntityType | DetailsJSON Example | Use Case |
|--------|------------|---------------------|----------|
| `user_signup` | user | `{"email": "user@example.com", "signup_method": "email"}` | Track signups |
| `email_verified` | user | `{"email": "user@example.com"}` | Track verification rate |
| `onboarding_complete` | user | `{"company_id": 123, "role": "company_admin"}` | Track onboarding completion |
| `password_reset` | user | `{"email": "user@example.com"}` | Security audit |
| `login` | user | `{"email": "user@example.com", "ip_hash": "abc123"}` | Security audit |
| `login_failed` | user | `{"email": "user@example.com", "reason": "invalid_password"}` | Security audit |
| `account_locked` | user | `{"email": "user@example.com", "failed_attempts": 5}` | Security audit |
| `invitation_sent` | invitation | `{"invited_email": "newuser@example.com", "role": "company_user"}` | Team management audit |
| `invitation_accepted` | invitation | `{"accepted_by_user_id": 456}` | Team management audit |
| `invitation_cancelled` | invitation | `{"cancelled_by_user_id": 123}` | Team management audit |
| `user_role_changed` | user | `{"old_role": "company_user", "new_role": "company_admin"}` | RBAC audit |
| `user_removed` | user | `{"removed_by_user_id": 123}` | Team management audit |

---

## Strategic Recommendations

### Priority 1: Critical Fixes (MVP Blockers)

#### ✅ **Recommendation 1: Implement User Schema FIRST**

**Why:** Company and Event schemas reference User table (FK constraints). Cannot execute database migrations without User table.

**Action Plan:**
1. Create `database/schemas/user-schema.sql` (use proposed schema above)
2. Create Alembic migration for User table
3. Create Alembic migration for Invitation table
4. Test FK constraints with Company/Event schemas
5. Validate with Solomon (Database Migration Validator)

**Estimated Effort:** 2-3 days (schema design + migrations + validation)

---

#### ✅ **Recommendation 2: Add Missing Security Fields**

**Why:** PRD design missing critical security features (brute force protection, token expiry, session management).

**Fields to Add:**

| Field | Purpose | Benefit |
|-------|---------|---------|
| `FailedLoginCount` | Track failed login attempts | Prevent brute force attacks |
| `LockedUntil` | Account lockout timestamp | Lock account after 5 failed logins (15 min) |
| `EmailVerificationToken` | Secure email verification | Replace guessable URLs with random tokens |
| `EmailVerificationExpiresAt` | Token expiry | Expire verification links after 24 hours |
| `PasswordResetToken` | Secure password reset | Replace guessable URLs with random tokens |
| `PasswordResetExpiresAt` | Token expiry | Expire reset links after 1 hour |
| `SessionToken` | Session invalidation | Logout all devices on password reset |
| `LastPasswordChange` | Security audit | Track password change history |

**Action Plan:** Include these fields in user-schema.sql (already in proposed schema above).

---

#### ✅ **Recommendation 3: Add Audit Trail to User Table**

**Why:** Company and Event tables have full audit trail (CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy). User table must match for consistency.

**Fields to Add:**

| Field | Purpose |
|-------|---------|
| `UpdatedDate` | Last profile update timestamp |
| `UpdatedBy` | UserID who updated (self or admin) |
| `IsDeleted` | Soft delete flag (retain historical data) |
| `DeletedDate` | Deletion timestamp |
| `DeletedBy` | UserID who deleted (self or admin) |

**Solomon's Standards Compliance:** ✅ Matches Company/Event schemas

---

### Priority 2: UX Improvements (Recommended for MVP)

#### ✅ **Recommendation 4: Make Company Setup Optional at Signup**

**Current Flow (PRD):** User signs up → Email verification → Login → **Mandatory** onboarding (user details + company setup)

**Problem:**
- Forces single user to create company before exploring platform
- Solo users abandon if forced to enter company details upfront
- Industry norm: Let users start alone, add team later (Typeform, Canva)

**Proposed Flow (Better UX):**

**Option A: "Personal Workspace" Mode**
1. User signs up → Email verification → Login
2. Onboarding Step 1: User details (first name, last name, phone)
3. Onboarding Step 2: "Start Solo or Create Company?"
   - **Option A:** "Start with Personal Workspace" (no company_id, user can create forms alone)
   - **Option B:** "Create Company Workspace" (enter company details)
4. If Personal Workspace → Skip company setup, set `user.company_id = NULL`
5. Later: User clicks "Invite Team" → Prompt to create company (converts personal → company workspace)

**Option B: Skip Company Setup, Auto-Create Personal Company**
1. User signs up → Email verification → Login
2. Onboarding Step 1: User details only
3. System auto-creates "Personal Company" (company name = user's name, no ABN, single-user company)
4. User can rename company later or convert to real company when inviting team

**Recommendation:** Option A (Personal Workspace) - cleaner separation, no fake company records.

**Implementation:**
- Change `User.CompanyID` to nullable (already nullable in PRD)
- Add `User.WorkspaceType` enum: 'personal', 'company'
- Update RBAC middleware: Personal workspace users are implicitly "company_admin" of their own data
- Add "Upgrade to Company" flow when user clicks "Invite Team"

---

#### ✅ **Recommendation 5: Add Invitation Preview & Decline**

**Current Flow (PRD):** Invitee clicks link → Immediately prompted to set password → Committed to joining

**Problem:**
- Invitee doesn't see company name or role until after clicking link
- No way to decline invitation gracefully
- Invitation acceptance is all-or-nothing (click link = committed)

**Proposed Flow (Better UX):**
1. Invitee clicks invitation link
2. Landing page shows:
   - "You've been invited to join **[Company Name]** as **[Role]**"
   - Company logo (if available)
   - "Invited by [Admin Name] ([Admin Email])"
   - Two buttons: "Accept & Join" | "Decline Invitation"
3. If "Accept & Join" → Proceed to password setup
4. If "Decline Invitation" → Mark invitation as declined, send notification to Admin

**Implementation:**
- Add `Status` option: 'declined' (in addition to pending, accepted, cancelled, expired)
- Add `DeclinedAt` timestamp field
- Send email to Admin when invitation declined

---

### Priority 3: Future Enhancements (Phase 2)

#### 🔮 **Recommendation 6: Multi-Company User Access**

**Why:** Industry standard (Eventbrite, Canva, Stripe all support this). Enables:
- Freelancers working with multiple client companies
- Consultants joining multiple workspaces
- Users switching companies but retaining historical access

**Implementation:**
- Phase 1 (MVP): Keep `User.CompanyID` single-company relationship (simpler)
- Phase 2: Implement UserCompany many-to-many table (see schema above)

**Effort:** 1-2 weeks (migration + UI updates)

---

#### 🔮 **Recommendation 7: 2FA for Publishing & Payments**

**Why:** Publishing triggers payment ($99 charge). 2FA reduces fraud risk.

**Implementation:**
- Phase 2: Add 2FA fields to User table: `TwoFactorEnabled`, `TwoFactorSecret`, `TwoFactorBackupCodes`
- Require 2FA verification on publish button (only if enabled)
- Use TOTP standard (Google Authenticator, Authy)

**Effort:** 1 week

---

#### 🔮 **Recommendation 8: Social Auth (Google, Microsoft)**

**Why:** Faster signup, better UX (no password to remember)

**Implementation:**
- Phase 2: Add OAuth integration (Google, Microsoft)
- Add fields to User: `AuthProvider` (email, google, microsoft), `OAuthProviderID`

**Effort:** 1-2 weeks

---

#### 🔮 **Recommendation 9: Magic Link Authentication (Passwordless)**

**Why:** Modern UX (Slack, Notion use this). No password to forget.

**Implementation:**
- Phase 2: Add magic link login option
- Add field: `MagicLinkToken`, `MagicLinkExpiresAt`

**Effort:** 3-5 days

---

## Data Governance

### Test Data (Development/Testing)

**Purpose:** Development and testing environments

**Characteristics:**
- Verbose, varied, edge cases
- Clearly fictional names
- Australian addresses (use test addresses like "123 Test Street, Sydney NSW 2000")
- Example emails: `testuser1@example.com`, `testuser2@example.com`

**Test User Scenarios:**

| User Type | Email | First Name | Last Name | Company | Role | Purpose |
|-----------|-------|------------|-----------|---------|------|---------|
| Solo User (Personal Workspace) | `solo@example.com` | Alex | Solo | NULL | company_admin | Test personal workspace flow |
| Company Creator | `admin@acmecorp.example.com` | Jane | Admin | Acme Corp | company_admin | Test first-time company signup |
| Invited Admin | `admin2@acmecorp.example.com` | Bob | AdminTwo | Acme Corp | company_admin | Test invitation as Admin |
| Invited User | `user1@acmecorp.example.com` | Charlie | User | Acme Corp | company_user | Test invitation as User |
| Multi-Company User (Phase 2) | `freelance@example.com` | Dana | Freelance | Acme Corp + Beta Inc | company_user | Test multi-company access |
| System Admin | `sysadmin@eventlead.com` | System | Admin | NULL | system_admin | Test platform-level access |
| Locked Account | `locked@example.com` | Locked | User | Acme Corp | company_user | Test brute force protection |
| Unverified Email | `unverified@example.com` | Unverified | User | Acme Corp | company_user | Test email verification flow |
| Pending Invitation | N/A (not signed up yet) | Pending | User | Acme Corp | company_user | Test invitation flow |

**Test Data Files:**
- Create: `database/seeds/test/user-test-data.sql`
- Include: 20 test users covering all scenarios above
- Label: ALWAYS label as TEST DATA in file headers

---

### Production Seed Data

**Purpose:** Initial platform seed data (real users for QA/demo)

**Characteristics:**
- Clean, verified, realistic
- Real Australian names (common Australian names)
- Attribution included (if sourced from public data)

**Production Seed Users:**

| User Type | Email | First Name | Last Name | Company | Role | Purpose |
|-----------|-------|------------|-----------|---------|------|---------|
| Demo Company Admin | `demo.admin@eventlead.com` | Sarah | Thompson | EventLead Demo Co | company_admin | Demo account for sales |
| Demo Company User | `demo.user@eventlead.com` | Michael | Chen | EventLead Demo Co | company_user | Demo account for sales |

**Production Data Files:**
- Create: `database/seeds/production/user-production-data.sql`
- Include: 2-3 demo accounts only
- Label: PRODUCTION SEED DATA with source attribution

**⚠️ CRITICAL RULE:** NEVER pollute production with test data. ALWAYS separate files and clear labeling.

---

## Validation Checklist

### Database Schema Validation (Solomon's Standards)

Before submitting to Solomon (Database Migration Validator):

- [ ] **PascalCase Naming:** User, UserID, CompanyID (✅ Compliant)
- [ ] **NVARCHAR for Text:** Email, FirstName, LastName (✅ Compliant)
- [ ] **DATETIME2 with UTC:** CreatedDate, UpdatedDate (✅ Compliant)
- [ ] **Soft Deletes:** IsDeleted, DeletedDate, DeletedBy (✅ Compliant)
- [ ] **Full Audit Trail:** CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy (✅ Compliant)
- [ ] **Foreign Keys:** CompanyID → Company, UpdatedBy → User, DeletedBy → User (✅ Compliant)
- [ ] **Check Constraints:** Role enum, Status enum, Email format (✅ Compliant)
- [ ] **Unique Constraints:** Email unique index (✅ Compliant)
- [ ] **Indexes:** Email, CompanyID, EmailVerificationToken, PasswordResetToken (✅ Compliant)

**Validation Command:** Run Sentinel (Epic Boundary Guardian) to validate schema against Solomon's standards.

---

### RBAC Validation

- [ ] **3 Roles Defined:** system_admin, company_admin, company_user (✅ Compliant)
- [ ] **Role Permissions Documented:** See PRD lines 108-141 (✅ Compliant)
- [ ] **Role Check Constraints:** `CK_User_Role` enforces valid roles (✅ Compliant)
- [ ] **Role-Based UI Rendering:** Frontend shows/hides features based on role (⚠️ To be implemented in frontend)

---

### Authentication Flow Validation

- [ ] **Email Verification:** Token-based, 24-hour expiry (✅ Proposed)
- [ ] **Password Reset:** Token-based, 1-hour expiry (✅ Proposed)
- [ ] **Invitation Flow:** Token-based, 7-day expiry, resend capability (✅ Proposed)
- [ ] **Brute Force Protection:** Failed login tracking, account lockout (✅ Proposed)
- [ ] **Session Management:** JWT tokens, logout all devices on password reset (✅ Proposed)

---

## Next Steps

### Immediate Actions (Before Epic 1 Development)

1. **Create User Schema SQL File**
   - File: `database/schemas/user-schema.sql`
   - Use proposed schema from this document
   - Include: User, Invitation, UserCompany (Phase 2) tables

2. **Create Database Migrations**
   - Tool: Alembic (Python)
   - Migrations: User table, Invitation table
   - Order: User → Company → Event (User must be first due to FK dependencies)

3. **Validate with Solomon**
   - Run: Solomon (Database Migration Validator) agent
   - Check: PascalCase, NVARCHAR, DATETIME2, audit trail compliance
   - Fix: Any issues flagged by Solomon

4. **Create Test Seed Data**
   - File: `database/seeds/test/user-test-data.sql`
   - Include: 20 test users (cover all scenarios)
   - Label: TEST DATA

5. **Create Production Seed Data**
   - File: `database/seeds/production/user-production-data.sql`
   - Include: 2-3 demo accounts
   - Label: PRODUCTION SEED DATA

6. **Backend Models Implementation**
   - Create: `backend/models/user.py`
   - Create: `backend/models/invitation.py`
   - Use: SQLAlchemy ORM
   - Include: All fields from proposed schema

7. **Auth Module Implementation**
   - Create: `backend/modules/auth/` directory
   - Implement: Signup, login, email verification, password reset, invitation flows
   - Use: FastAPI + JWT (PyJWT library)
   - Include: Brute force protection, rate limiting

---

### Epic 1 Dependencies

**Epic 1: User Authentication, Onboarding & RBAC** (PRD lines 241-250)

**Epic 1 CANNOT START until:**
- [ ] User schema created and validated (database/schemas/user-schema.sql)
- [ ] Database migrations executed (Alembic)
- [ ] Backend models implemented (backend/models/)
- [ ] Auth module scaffolded (backend/modules/auth/)

**Estimated Prep Time:** 3-5 days (before Epic 1 starts)

---

## Summary & Key Takeaways

### What We Found

✅ **Strengths (PRD Design):**
- Well-thought-out RBAC (3 roles: System Admin, Company Admin, Company User)
- Comprehensive authentication flows (signup, verification, reset, invitation)
- Invitation expiry (7 days) + resend capability
- Multi-tenant isolation (user → company relationship)
- Activity log for audit trail

❌ **Gaps Identified:**

| Gap | Impact | Priority |
|-----|--------|----------|
| No User schema SQL file | BLOCKER: Cannot execute Company/Event schemas | 🔴 Critical |
| No audit trail on User table | Compliance: Inconsistent with Company/Event | 🔴 Critical |
| No security fields (brute force, token expiry) | Security: Vulnerable to attacks | 🔴 Critical |
| No multi-company user access | UX: Industry norm, limits platform flexibility | 🟡 Phase 2 |
| Mandatory company setup at signup | UX: Friction for solo users exploring platform | 🟡 Recommended |
| No invitation preview/decline | UX: Poor invitation acceptance experience | 🟡 Recommended |

### Strategic Recommendations (Priority Order)

**Priority 1: Critical Fixes (MVP Blockers)**
1. ✅ Create User schema with full audit trail + security fields
2. ✅ Implement database migrations (User → Invitation)
3. ✅ Validate schema with Solomon

**Priority 2: UX Improvements (Recommended for MVP)**
4. ✅ Make company setup optional (Personal Workspace mode)
5. ✅ Add invitation preview & decline flow

**Priority 3: Future Enhancements (Phase 2)**
6. 🔮 Multi-company user access (UserCompany table)
7. 🔮 2FA for publishing & payments
8. 🔮 Social auth (Google, Microsoft)
9. 🔮 Magic link authentication (passwordless)

### Industry Insights

**Patterns We Should Adopt:**
- ✅ Invitation expiry (7 days) - EventLead already has this
- ✅ Resend capability - EventLead already has this
- ✅ Progressive onboarding - Collect minimal info upfront (recommend)
- ✅ Multi-company access - Industry standard (recommend Phase 2)
- ✅ 2FA for financial operations - Stripe standard (recommend Phase 2)

**Patterns We Should Avoid:**
- ❌ No invitation expiry - Security risk (Slack, Typeform mistake)
- ❌ Mandatory company setup for solo users - Friction (our recommendation to change)
- ❌ Complex RBAC (5+ roles) - Overkill for MVP (EventLead's 3 roles perfect)

---

## Appendix: SQL Schema Files

### File 1: user-schema.sql

See **Schema Design Recommendations → Table 1: User (Core Identity)** section above for full SQL.

**Location:** `database/schemas/user-schema.sql`

---

### File 2: invitation-schema.sql

See **Schema Design Recommendations → Table 2: Invitation (Team Onboarding)** section above for full SQL.

**Location:** `database/schemas/invitation-schema.sql` (or include in user-schema.sql as single file)

---

### File 3: user-test-data.sql

**Location:** `database/seeds/test/user-test-data.sql`

**Content:** See **Data Governance → Test Data** section for test user scenarios.

---

### File 4: user-production-data.sql

**Location:** `database/seeds/production/user-production-data.sql`

**Content:** See **Data Governance → Production Seed Data** section for demo accounts.

---

## Collaboration Handoffs

### With Solomon (Database Migration Validator)

**Deliverables to Solomon:**
- `database/schemas/user-schema.sql`
- `database/schemas/invitation-schema.sql`

**Validation Requests:**
1. Check PascalCase naming (User, UserID, CompanyID)
2. Validate NVARCHAR usage (Email, FirstName, LastName)
3. Confirm DATETIME2 with UTC (CreatedDate, UpdatedDate)
4. Verify audit trail completeness (CreatedDate, CreatedBy, UpdatedDate, UpdatedBy, IsDeleted, DeletedDate, DeletedBy)
5. Check FK constraints (CompanyID → Company, UpdatedBy → User, DeletedBy → User)

---

### With UX Expert

**Deliverables to UX:**
1. Onboarding flow recommendation (Personal Workspace vs Mandatory Company)
2. Invitation preview/decline flow mockup requirements
3. RBAC UI rendering requirements (show/hide features per role)

---

### With Product Manager

**Deliverables to PM:**
1. Multi-company access recommendation (Phase 2 priority)
2. 2FA recommendation (Phase 2 for publishing/payments)
3. Social auth recommendation (Phase 2 feature)

---

### With Developer

**Deliverables to Dev:**
1. User schema SQL files (user-schema.sql, invitation-schema.sql)
2. Test seed data (user-test-data.sql)
3. Production seed data (user-production-data.sql)
4. Backend model requirements (SQLAlchemy)
5. Auth module requirements (FastAPI + JWT)

---

**End of User Domain Analysis**

**Next Action:** Create `database/schemas/user-schema.sql` (use proposed schema from this document).

---

**Questions? Run `*help` or `*exit` when ready to proceed.**

