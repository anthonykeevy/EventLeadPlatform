-- =====================================================================
-- User Domain Schema - Authentication, RBAC & Team Collaboration
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: October 13, 2025
-- Version: 1.0.0
-- =====================================================================
-- Purpose:
--   Supports EventLead Platform's User domain with:
--   1. User Identity & Authentication (email/password, verification, reset)
--   2. Role-Based Access Control (3 roles: System Admin, Company Admin, Company User)
--   3. Team Collaboration (invitation-based onboarding)
--   4. Multi-Tenant Isolation (user-to-company relationships)
-- 
-- Standards:
--   - PascalCase naming (Solomon's requirement)
--   - NVARCHAR for text (UTF-8 support)
--   - DATETIME2 with UTC timestamps
--   - Soft deletes (IsDeleted flag)
--   - Full audit trail on all tables
-- =====================================================================
-- Industry Research:
--   - Canva: Freemium team collaboration, invitation expiry (7 days)
--   - Typeform: Workspace-based multi-tenancy, 2-role system
--   - Eventbrite: Multi-brand support, organizer roles
--   - Slack: Workspace-based, magic link auth
--   - Stripe: Multi-account support, 2FA for financial operations
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- TABLE 1: User (Core Identity & Authentication)
-- =====================================================================
CREATE TABLE [User] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    UserID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Authentication Credentials
    -- =====================================================================
    Email NVARCHAR(100) NOT NULL,
    -- ^ User email (unique identifier, login username)
    -- Example: "jane.admin@acmecorp.com.au"
    -- Validation: Must contain @ and . (enforced by check constraint)
    
    PasswordHash NVARCHAR(255) NOT NULL,
    -- ^ Bcrypt password hash (60 chars, but 255 for future algorithms)
    -- NEVER store plain passwords (security requirement)
    -- Hash algorithm: Bcrypt with salt rounds = 12 (industry standard)
    
    -- =====================================================================
    -- User Profile (Basic Information)
    -- =====================================================================
    FirstName NVARCHAR(100) NOT NULL,
    -- ^ User first name (collected during onboarding)
    -- Example: "Jane"
    
    LastName NVARCHAR(100) NOT NULL,
    -- ^ User last name (collected during onboarding)
    -- Example: "Smith"
    
    RoleTitle NVARCHAR(100) NULL,
    -- ^ Optional job title (e.g., "Marketing Manager", "Event Coordinator")
    -- Collected during onboarding, displayed in team member list
    
    PhoneNumber NVARCHAR(20) NULL,
    -- ^ Optional phone number (Australian format: +61 4XX XXX XXX)
    -- International format supported for future expansion
    
    ProfilePictureUrl NVARCHAR(500) NULL,
    -- ^ Profile picture URL (Azure Blob Storage)
    -- Phase 2 feature: User uploads profile picture
    -- Default: Show initials (JD for Jane Doe) if no picture
    
    TimezoneIdentifier NVARCHAR(50) NULL DEFAULT 'Australia/Sydney',
    -- ^ IANA timezone for displaying dates in user's local time
    -- Australia has 3 main timezones: Australia/Sydney, Australia/Melbourne, Australia/Perth
    -- Used for: Event start times, activity log timestamps, email scheduling
    
    -- =====================================================================
    -- Company Relationship (Multi-Tenant Isolation)
    -- =====================================================================
    CompanyID BIGINT NULL,
    -- ^ Foreign key to Company table
    -- NULL = User hasn't completed onboarding OR personal workspace (Phase 2)
    -- NOT NULL = User belongs to company (multi-tenant isolation)
    -- Note: Phase 2 will migrate to UserCompany many-to-many table (multi-company access)
    
    -- =====================================================================
    -- Role-Based Access Control (RBAC)
    -- =====================================================================
    Role NVARCHAR(20) NOT NULL DEFAULT 'company_user',
    -- ^ User role (determines permissions)
    -- Options:
    --   'system_admin' = Platform-level access (backend only for MVP)
    --   'company_admin' = Full company access (publish, billing, invite users)
    --   'company_user' = Limited access (create drafts, cannot publish)
    -- Check constraint enforced below
    
    -- =====================================================================
    -- Account Status Flags
    -- =====================================================================
    EmailVerified BIT NOT NULL DEFAULT 0,
    -- ^ Has user verified their email address? (0 = no, 1 = yes)
    -- User cannot access dashboard until email verified
    -- Set to 1 after clicking email verification link
    
    OnboardingComplete BIT NOT NULL DEFAULT 0,
    -- ^ Has user completed onboarding flow? (0 = no, 1 = yes)
    -- Gates access to dashboard (redirect to onboarding if 0)
    -- Set to 1 after completing onboarding steps (user details + company setup)
    
    IsActive BIT NOT NULL DEFAULT 1,
    -- ^ Is user account active? (0 = suspended, 1 = active)
    -- Suspended accounts cannot log in (admin action)
    -- Different from soft delete (IsDeleted = retain data, IsActive = temporary suspension)
    
    -- =====================================================================
    -- Email Verification Tokens
    -- =====================================================================
    EmailVerificationToken NVARCHAR(255) NULL,
    -- ^ Secure random token for email verification link
    -- Generated on signup, sent via email
    -- Format: UUID v4 (36 chars) or cryptographically secure random string
    -- NULL after email verified (token consumed)
    
    EmailVerificationExpiresAt DATETIME2 NULL,
    -- ^ Token expiry timestamp (UTC)
    -- Standard: 24 hours from signup
    -- After expiry, user must request new verification email
    
    -- =====================================================================
    -- Password Reset Tokens
    -- =====================================================================
    PasswordResetToken NVARCHAR(255) NULL,
    -- ^ Secure random token for password reset link
    -- Generated when user clicks "Forgot Password"
    -- Format: UUID v4 or cryptographically secure random string
    -- NULL after password reset (token consumed)
    
    PasswordResetExpiresAt DATETIME2 NULL,
    -- ^ Token expiry timestamp (UTC)
    -- Standard: 1 hour from request (shorter than email verification)
    -- Security: Reset tokens more sensitive than verification tokens
    
    LastPasswordChange DATETIME2 NULL,
    -- ^ Last password change timestamp (UTC)
    -- Used for: Security audit, force password change (e.g., every 90 days for admins)
    -- NULL = Password never changed since signup
    
    -- =====================================================================
    -- Session Management
    -- =====================================================================
    SessionToken NVARCHAR(255) NULL,
    -- ^ Current session token (for "logout all devices" feature)
    -- JWT tokens contain session_token claim
    -- When user resets password, SessionToken is regenerated
    -- All JWTs with old SessionToken become invalid
    -- Phase 2 feature: "Logout all devices" button
    
    LastLogin DATETIME2 NULL,
    -- ^ Last successful login timestamp (UTC)
    -- Used for: Security audit, "Last seen" display, inactive user cleanup
    
    -- =====================================================================
    -- Security (Brute Force Protection)
    -- =====================================================================
    FailedLoginCount INT NOT NULL DEFAULT 0,
    -- ^ Number of consecutive failed login attempts
    -- Reset to 0 on successful login
    -- After 5 failed attempts, account locked for 15 minutes
    
    LockedUntil DATETIME2 NULL,
    -- ^ Account lockout expiry timestamp (UTC)
    -- NULL = Not locked
    -- NOT NULL = Locked until this timestamp (failed login attempts)
    -- After LockedUntil passes, FailedLoginCount reset to 0
    
    -- =====================================================================
    -- Audit Trail (Solomon's Standards - matches Company/Event schemas)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ Account creation timestamp (UTC)
    -- Set automatically on INSERT
    
    UpdatedDate DATETIME2 NULL,
    -- ^ Last profile update timestamp (UTC)
    -- Updated on any profile field change (name, phone, role, etc.)
    
    UpdatedBy BIGINT NULL,
    -- ^ UserID who last updated this record
    -- Self-update (user edits own profile) OR admin update (admin changes user role)
    
    IsDeleted BIT NOT NULL DEFAULT 0,
    -- ^ Soft delete flag (0 = active, 1 = deleted)
    -- Retain historical data for audit trail (who created this form? Deleted user)
    -- Deleted users cannot log in, but data preserved
    
    DeletedDate DATETIME2 NULL,
    -- ^ Deletion timestamp (UTC)
    
    DeletedBy BIGINT NULL,
    -- ^ UserID who soft-deleted this record
    -- Self-delete (user deletes own account) OR admin delete (admin removes user)
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_User_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_User_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_User_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [User](UserID),
    
    -- Role validation (must be one of 3 valid roles)
    CONSTRAINT CK_User_Role CHECK (
        Role IN ('system_admin', 'company_admin', 'company_user')
    ),
    
    -- Email format validation (must contain @ and .)
    CONSTRAINT CK_User_Email_Format CHECK (
        Email LIKE '%@%.%'
    ),
    
    -- Audit trail consistency (CreatedDate must be before UpdatedDate/DeletedDate)
    CONSTRAINT CK_User_AuditDates CHECK (
        CreatedDate <= ISNULL(UpdatedDate, '9999-12-31') AND
        CreatedDate <= ISNULL(DeletedDate, '9999-12-31')
    )
);
GO

-- =====================================================================
-- Indexes (Performance Optimization)
-- =====================================================================

-- Unique email constraint (one email per active user)
-- Filtered index: Only enforce uniqueness for non-deleted users
CREATE UNIQUE INDEX UX_User_Email ON [User](Email) 
    WHERE IsDeleted = 0;
GO

-- Company's users (team member list, RBAC checks)
CREATE INDEX IX_User_Company ON [User](CompanyID, IsDeleted) 
    INCLUDE (FirstName, LastName, Email, Role)
    WHERE IsDeleted = 0;
GO

-- Email verification token lookup (when user clicks verification link)
CREATE INDEX IX_User_EmailVerificationToken ON [User](EmailVerificationToken) 
    WHERE EmailVerificationToken IS NOT NULL;
GO

-- Password reset token lookup (when user clicks reset link)
CREATE INDEX IX_User_PasswordResetToken ON [User](PasswordResetToken) 
    WHERE PasswordResetToken IS NOT NULL;
GO

-- Role-based queries (system admins list, company admins list)
CREATE INDEX IX_User_Role ON [User](Role, IsDeleted) 
    WHERE IsDeleted = 0;
GO

PRINT 'User table created successfully (core identity & authentication)!';
GO

-- =====================================================================
-- TABLE 2: Invitation (Team Collaboration)
-- =====================================================================
CREATE TABLE [Invitation] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    InvitationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Company & Inviter (Who Sent This Invitation?)
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    -- ^ Company inviting this user
    -- Used for: Multi-tenant isolation, show "Join [Company Name]" in email
    
    InvitedByUserID BIGINT NOT NULL,
    -- ^ Company Admin who sent invitation
    -- Used for: Audit trail, display "Invited by [Name]" in email
    
    -- =====================================================================
    -- Invitee Details (Pre-filled by Admin)
    -- =====================================================================
    InvitedEmail NVARCHAR(100) NOT NULL,
    -- ^ Email address of invitee
    -- User account will be created with this email
    -- Validation: Check if email already exists (duplicate handling)
    
    InvitedFirstName NVARCHAR(100) NOT NULL,
    -- ^ Pre-filled first name (Admin enters this during invitation)
    -- Editable by invitee during signup (Admin might have typos)
    
    InvitedLastName NVARCHAR(100) NOT NULL,
    -- ^ Pre-filled last name (Admin enters this during invitation)
    -- Editable by invitee during signup
    
    AssignedRole NVARCHAR(20) NOT NULL,
    -- ^ Role assigned to invitee (set by Admin during invitation)
    -- Options: 'company_admin', 'company_user'
    -- Note: 'system_admin' role cannot be assigned via invitation (platform-level)
    
    -- =====================================================================
    -- Invitation Token (Secure)
    -- =====================================================================
    InvitationToken NVARCHAR(255) NOT NULL,
    -- ^ Secure random token for invitation link
    -- Format: UUID v4 or cryptographically secure random string
    -- URL format: https://eventlead.com/accept-invitation?token={InvitationToken}
    
    -- =====================================================================
    -- Invitation Lifecycle
    -- =====================================================================
    Status NVARCHAR(20) NOT NULL DEFAULT 'pending',
    -- ^ Invitation status
    -- Options:
    --   'pending' = Invitation sent, awaiting acceptance
    --   'accepted' = Invitee accepted and joined company
    --   'cancelled' = Admin cancelled invitation before acceptance
    --   'expired' = Invitation expired (7 days passed)
    --   'declined' = Invitee declined invitation (Phase 2 feature)
    
    InvitedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ Invitation sent timestamp (UTC)
    
    ExpiresAt DATETIME2 NOT NULL,
    -- ^ Invitation expiry timestamp (UTC)
    -- Standard: InvitedAt + 7 days (industry norm from Canva research)
    -- After expiry, invitation marked as 'expired' (cron job runs daily)
    
    AcceptedAt DATETIME2 NULL,
    -- ^ Invitation acceptance timestamp (UTC)
    -- NULL = Not accepted yet
    -- NOT NULL = Accepted (status = 'accepted')
    
    AcceptedByUserID BIGINT NULL,
    -- ^ UserID of user who accepted invitation
    -- Audit trail: Who accepted? (important if invitation email forwarded)
    -- Links invitation to actual User record created
    
    -- =====================================================================
    -- Cancellation Audit
    -- =====================================================================
    CancelledAt DATETIME2 NULL,
    -- ^ Cancellation timestamp (UTC)
    
    CancelledBy BIGINT NULL,
    -- ^ UserID of Admin who cancelled invitation
    -- Audit trail: Who cancelled and when?
    
    -- =====================================================================
    -- Resend Tracking (Rate Limiting)
    -- =====================================================================
    ResendCount INT NOT NULL DEFAULT 0,
    -- ^ Number of times invitation email resent
    -- Used for: Rate limiting (max 3 resends per invitation)
    -- Prevents abuse (spamming invitee's inbox)
    
    LastResentAt DATETIME2 NULL,
    -- ^ Last resend timestamp (UTC)
    -- Used for: Rate limiting (max 1 resend per hour)
    
    -- =====================================================================
    -- Email Delivery Tracking
    -- =====================================================================
    EmailSentAt DATETIME2 NULL,
    -- ^ Email sent timestamp (UTC)
    -- Confirms invitation email actually sent (not just queued)
    
    EmailSentStatus NVARCHAR(20) NULL,
    -- ^ Email delivery status from SendGrid/Azure Communication
    -- Options: 'sent', 'delivered', 'bounced', 'failed'
    -- Used for: Troubleshooting (invitee says "I never got email")
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Invitation_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_Invitation_InvitedBy FOREIGN KEY (InvitedByUserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_Invitation_AcceptedBy FOREIGN KEY (AcceptedByUserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_Invitation_CancelledBy FOREIGN KEY (CancelledBy) 
        REFERENCES [User](UserID),
    
    -- Role validation (only company-level roles can be assigned)
    CONSTRAINT CK_Invitation_Role CHECK (
        AssignedRole IN ('company_admin', 'company_user')
    ),
    
    -- Status validation
    CONSTRAINT CK_Invitation_Status CHECK (
        Status IN ('pending', 'accepted', 'cancelled', 'expired', 'declined')
    ),
    
    -- Email format validation
    CONSTRAINT CK_Invitation_Email_Format CHECK (
        InvitedEmail LIKE '%@%.%'
    ),
    
    -- Expiry must be after InvitedAt
    CONSTRAINT CK_Invitation_ExpiryDate CHECK (
        ExpiresAt > InvitedAt
    )
);
GO

-- =====================================================================
-- Indexes
-- =====================================================================

-- Unique invitation token (one token per invitation)
CREATE UNIQUE INDEX UX_Invitation_Token ON [Invitation](InvitationToken);
GO

-- Company's invitations (pending invitations list in UI)
CREATE INDEX IX_Invitation_Company_Status ON [Invitation](CompanyID, Status)
    INCLUDE (InvitedEmail, InvitedFirstName, InvitedLastName, AssignedRole, InvitedAt, ExpiresAt);
GO

-- Email-based queries (check if email already invited)
CREATE INDEX IX_Invitation_Email_Status ON [Invitation](InvitedEmail, Status);
GO

-- Expiry queries (cron job to mark expired invitations)
CREATE INDEX IX_Invitation_Expiry ON [Invitation](ExpiresAt, Status) 
    WHERE Status = 'pending';
GO

PRINT 'Invitation table created successfully (team collaboration)!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'User Domain Schema Complete!';
PRINT '========================================';
PRINT 'Tables Created:';
PRINT '  1. User (core identity - 27 fields)';
PRINT '  2. Invitation (team collaboration - 18 fields)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Email-based authentication with verification';
PRINT '  ✅ Secure password reset flow (1-hour expiry)';
PRINT '  ✅ 3-role RBAC (System Admin, Company Admin, Company User)';
PRINT '  ✅ Invitation-based team onboarding (7-day expiry)';
PRINT '  ✅ Brute force protection (5 failed logins = 15 min lockout)';
PRINT '  ✅ Session management (logout all devices)';
PRINT '  ✅ Full audit trail (Solomon standards)';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Create Alembic migration for User table';
PRINT '  2. Create Alembic migration for Invitation table';
PRINT '  3. Validate schema with Solomon (Database Migration Validator)';
PRINT '  4. Import test seed data (20 test users)';
PRINT '  5. Import production seed data (2-3 demo accounts)';
PRINT '  6. Implement backend models (backend/models/user.py)';
PRINT '  7. Implement auth module (backend/modules/auth/)';
PRINT '========================================';
GO

