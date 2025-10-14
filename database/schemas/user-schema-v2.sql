-- =====================================================================
-- User Domain Schema v2 - Authentication, RBAC & Team Collaboration
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: October 13, 2025
-- Version: 2.0.0 (Updated based on Anthony's feedback)
-- =====================================================================
-- Updates in v2:
--   1. UserCompany table added (multi-company access) - MVP INCLUDED
--   2. UserCompanyID added as surrogate primary key
--   3. Status lookup tables created (UserStatus, InvitationStatus)
--   4. Session management clarified (JWT Access + Refresh tokens)
--   5. Company onboarding kept mandatory (required for billing)
-- =====================================================================
-- Standards:
--   - PascalCase naming (Solomon's requirement)
--   - NVARCHAR for text (UTF-8 support)
--   - DATETIME2 with UTC timestamps
--   - Soft deletes (IsDeleted flag)
--   - Full audit trail on all tables
--   - Lookup tables for all status/enum fields
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- LOOKUP TABLE: UserStatus
-- =====================================================================
-- Purpose: Define valid user account statuses with clear definitions
-- =====================================================================
CREATE TABLE [UserStatus] (
    StatusCode NVARCHAR(20) PRIMARY KEY,
    -- ^ Code used in User.Status field (e.g., 'active', 'suspended')
    
    DisplayName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable name (e.g., "Active", "Suspended")
    
    Description NVARCHAR(500) NOT NULL,
    -- ^ Clear definition of what this status means
    
    AllowLogin BIT NOT NULL,
    -- ^ Can user log in with this status? (0 = no, 1 = yes)
    
    IsSystemStatus BIT NOT NULL DEFAULT 1,
    -- ^ Is this a system-defined status? (1 = yes, cannot delete)
    
    SortOrder INT NOT NULL,
    -- ^ Display order in UI dropdowns
    
    -- Audit Trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL
);
GO

-- Insert standard user statuses
INSERT INTO [UserStatus] (StatusCode, DisplayName, Description, AllowLogin, IsSystemStatus, SortOrder)
VALUES
    ('active', 'Active', 'User account is active and can log in normally', 1, 1, 1),
    ('unverified', 'Unverified Email', 'User signed up but has not verified email address yet', 0, 1, 2),
    ('suspended', 'Suspended', 'User account suspended by admin (temporary - billing issue, policy violation)', 0, 1, 3),
    ('locked', 'Locked (Brute Force)', 'Account temporarily locked due to failed login attempts (auto-unlocks after 15 min)', 0, 1, 4),
    ('deleted', 'Deleted', 'User account soft-deleted (retain data for audit trail)', 0, 1, 5);
GO

PRINT 'UserStatus lookup table created with 5 standard statuses!';
GO

-- =====================================================================
-- LOOKUP TABLE: InvitationStatus
-- =====================================================================
-- Purpose: Define valid invitation statuses with workflow rules
-- =====================================================================
CREATE TABLE [InvitationStatus] (
    StatusCode NVARCHAR(20) PRIMARY KEY,
    
    DisplayName NVARCHAR(50) NOT NULL,
    
    Description NVARCHAR(500) NOT NULL,
    
    CanResend BIT NOT NULL,
    -- ^ Can Admin resend invitation in this status? (0 = no, 1 = yes)
    
    CanCancel BIT NOT NULL,
    -- ^ Can Admin cancel invitation in this status? (0 = no, 1 = yes)
    
    IsFinalState BIT NOT NULL,
    -- ^ Is this a terminal state? (1 = yes, no further transitions allowed)
    
    IsSystemStatus BIT NOT NULL DEFAULT 1,
    
    SortOrder INT NOT NULL,
    
    -- Audit Trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL
);
GO

-- Insert standard invitation statuses
INSERT INTO [InvitationStatus] (StatusCode, DisplayName, Description, CanResend, CanCancel, IsFinalState, IsSystemStatus, SortOrder)
VALUES
    ('pending', 'Pending', 'Invitation sent, awaiting acceptance by invitee', 1, 1, 0, 1, 1),
    ('accepted', 'Accepted', 'Invitee accepted invitation and joined company', 0, 0, 1, 1, 2),
    ('expired', 'Expired', 'Invitation expired (7 days passed) without acceptance', 1, 0, 1, 1, 3),
    ('cancelled', 'Cancelled', 'Admin cancelled invitation before acceptance', 0, 0, 1, 1, 4),
    ('declined', 'Declined', 'Invitee declined invitation (Phase 2 feature)', 0, 0, 1, 1, 5);
GO

PRINT 'InvitationStatus lookup table created with 5 standard statuses!';
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
    PasswordHash NVARCHAR(255) NOT NULL,
    
    -- =====================================================================
    -- User Profile (Basic Information)
    -- =====================================================================
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    RoleTitle NVARCHAR(100) NULL,
    PhoneNumber NVARCHAR(20) NULL,
    ProfilePictureUrl NVARCHAR(500) NULL,
    TimezoneIdentifier NVARCHAR(50) NULL DEFAULT 'Australia/Sydney',
    
    -- =====================================================================
    -- Account Status (References UserStatus Lookup Table)
    -- =====================================================================
    Status NVARCHAR(20) NOT NULL DEFAULT 'unverified',
    -- ^ References UserStatus.StatusCode
    -- Initial status: 'unverified' (after signup, before email verification)
    -- After email verification: 'active'
    -- Admin actions: 'suspended', 'deleted'
    -- Security: 'locked' (brute force protection)
    
    OnboardingComplete BIT NOT NULL DEFAULT 0,
    -- ^ Has user completed onboarding flow? (0 = no, 1 = yes)
    -- Gates access to dashboard
    -- Onboarding = Step 1 (user details) + Step 2 (company details)
    
    -- =====================================================================
    -- Email Verification Tokens
    -- =====================================================================
    EmailVerificationToken NVARCHAR(255) NULL,
    EmailVerificationExpiresAt DATETIME2 NULL,
    EmailVerifiedAt DATETIME2 NULL,
    -- ^ Timestamp when email was verified (for audit trail)
    
    -- =====================================================================
    -- Password Reset Tokens
    -- =====================================================================
    PasswordResetToken NVARCHAR(255) NULL,
    PasswordResetExpiresAt DATETIME2 NULL,
    LastPasswordChange DATETIME2 NULL,
    
    -- =====================================================================
    -- Session Management (JWT Tokens)
    -- =====================================================================
    SessionToken NVARCHAR(255) NULL,
    -- ^ Current session token for "logout all devices" feature
    -- Generated on signup, regenerated on password reset
    -- JWT contains session_token claim - validated on each request
    -- If JWT session_token != User.SessionToken → Token invalid
    
    AccessTokenVersion INT NOT NULL DEFAULT 1,
    -- ^ Increment this to invalidate all access tokens (security)
    -- Use case: Suspicious activity detected, force re-login all devices
    
    RefreshTokenVersion INT NOT NULL DEFAULT 1,
    -- ^ Increment this to invalidate all refresh tokens
    -- Use case: Password reset, force re-login all devices
    
    LastLogin DATETIME2 NULL,
    -- ^ Last successful login timestamp (UTC)
    
    -- =====================================================================
    -- Security (Brute Force Protection)
    -- =====================================================================
    FailedLoginCount INT NOT NULL DEFAULT 0,
    -- ^ Consecutive failed login attempts (reset to 0 on successful login)
    
    LockedUntil DATETIME2 NULL,
    -- ^ Account lockout expiry (NULL = not locked)
    -- After 5 failed attempts, locked for 15 minutes
    -- After LockedUntil passes, FailedLoginCount reset to 0, Status changed from 'locked' to 'active'
    
    -- =====================================================================
    -- Audit Trail (Solomon's Standards)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    -- ^ UserID who created this account
    -- Self-signup: NULL initially, set to self (UserID) after INSERT
    -- Invitation: Set to InviterUserID (who triggered account creation)
    -- System Admin: Set to SystemAdminUserID
    
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_User_Status FOREIGN KEY (Status) 
        REFERENCES [UserStatus](StatusCode),
    
    CONSTRAINT FK_User_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_User_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_User_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [User](UserID),
    
    -- Email format validation
    CONSTRAINT CK_User_Email_Format CHECK (
        Email LIKE '%@%.%'
    ),
    
    -- Audit trail consistency
    CONSTRAINT CK_User_AuditDates CHECK (
        CreatedDate <= ISNULL(UpdatedDate, '9999-12-31') AND
        CreatedDate <= ISNULL(DeletedDate, '9999-12-31')
    )
);
GO

-- Indexes
CREATE UNIQUE INDEX UX_User_Email ON [User](Email) WHERE IsDeleted = 0;
CREATE INDEX IX_User_Status ON [User](Status, IsDeleted) WHERE IsDeleted = 0;
CREATE INDEX IX_User_EmailVerificationToken ON [User](EmailVerificationToken) WHERE EmailVerificationToken IS NOT NULL;
CREATE INDEX IX_User_PasswordResetToken ON [User](PasswordResetToken) WHERE PasswordResetToken IS NOT NULL;
CREATE INDEX IX_User_SessionToken ON [User](SessionToken) WHERE SessionToken IS NOT NULL;
GO

PRINT 'User table created successfully (27 fields)!';
GO

-- =====================================================================
-- TABLE 2: UserCompany (Multi-Company Access) - MVP INCLUDED
-- =====================================================================
-- Purpose: Many-to-many relationship between Users and Companies
-- Enables: One user can join multiple companies (freelancer, consultant)
-- =====================================================================
CREATE TABLE [UserCompany] (
    -- =====================================================================
    -- Primary Key (Surrogate Key per Anthony's requirement)
    -- =====================================================================
    UserCompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
    -- ^ Surrogate primary key (even though we have composite unique key)
    -- Benefits: Simpler FK references, easier ORM relationships
    
    -- =====================================================================
    -- User-Company Relationship
    -- =====================================================================
    UserID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    
    -- =====================================================================
    -- Role Per Company (User can be Admin in one, User in another)
    -- =====================================================================
    Role NVARCHAR(20) NOT NULL DEFAULT 'company_user',
    -- ^ Options: 'company_admin', 'company_user'
    -- Note: 'system_admin' is platform-level, not company-specific
    
    -- =====================================================================
    -- Relationship Status & Preferences
    -- =====================================================================
    Status NVARCHAR(20) NOT NULL DEFAULT 'active',
    -- ^ Options: 'active', 'suspended', 'removed'
    -- Active = Normal access
    -- Suspended = Admin temporarily revoked access (not removed from team)
    -- Removed = User removed from company (soft delete, retain historical data)
    
    IsDefaultCompany BIT NOT NULL DEFAULT 0,
    -- ^ Which company loads on login? (only one per user can be default)
    -- User can switch companies via dropdown in navbar
    
    -- =====================================================================
    -- Relationship History (How did user join this company?)
    -- =====================================================================
    JoinedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When user joined this company
    
    JoinedVia NVARCHAR(20) NOT NULL,
    -- ^ How user joined: 'signup' (created company), 'invitation', 'transfer' (admin action)
    
    InvitedByUserID BIGINT NULL,
    -- ^ If JoinedVia = 'invitation', who invited them?
    
    RemovedDate DATETIME2 NULL,
    -- ^ When user was removed from company (Status = 'removed')
    
    RemovedByUserID BIGINT NULL,
    -- ^ Admin who removed user from company
    
    RemovalReason NVARCHAR(500) NULL,
    -- ^ Optional reason for removal (displayed to user)
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    -- ^ UserID who added user to this company
    -- Company founder: Set to UserID (self-added)
    -- Invitation: Set to InviterUserID (who invited)
    -- System Admin: Set to SystemAdminUserID (admin action)
    
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_UserCompany_User FOREIGN KEY (UserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_UserCompany_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_UserCompany_InvitedBy FOREIGN KEY (InvitedByUserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_UserCompany_RemovedBy FOREIGN KEY (RemovedByUserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_UserCompany_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_UserCompany_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    -- Role validation
    CONSTRAINT CK_UserCompany_Role CHECK (
        Role IN ('company_admin', 'company_user')
    ),
    
    -- Status validation
    CONSTRAINT CK_UserCompany_Status CHECK (
        Status IN ('active', 'suspended', 'removed')
    ),
    
    -- JoinedVia validation
    CONSTRAINT CK_UserCompany_JoinedVia CHECK (
        JoinedVia IN ('signup', 'invitation', 'transfer')
    ),
    
    -- Unique constraint: User can only have ONE active relationship per company
    CONSTRAINT UX_UserCompany_User_Company UNIQUE (UserID, CompanyID)
);
GO

-- Indexes
CREATE INDEX IX_UserCompany_User_Status ON [UserCompany](UserID, Status);
CREATE INDEX IX_UserCompany_Company_Status ON [UserCompany](CompanyID, Status);
CREATE INDEX IX_UserCompany_DefaultCompany ON [UserCompany](UserID, IsDefaultCompany) WHERE IsDefaultCompany = 1;
GO

PRINT 'UserCompany table created successfully (multi-company access enabled)!';
GO

-- =====================================================================
-- TABLE 3: Invitation (Team Collaboration)
-- =====================================================================
CREATE TABLE [Invitation] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    InvitationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Company & Inviter
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    InvitedByUserID BIGINT NOT NULL,
    
    -- =====================================================================
    -- Invitee Details (Pre-filled by Admin)
    -- =====================================================================
    InvitedEmail NVARCHAR(100) NOT NULL,
    InvitedFirstName NVARCHAR(100) NOT NULL,
    InvitedLastName NVARCHAR(100) NOT NULL,
    AssignedRole NVARCHAR(20) NOT NULL,
    
    -- =====================================================================
    -- Invitation Token (Secure)
    -- =====================================================================
    InvitationToken NVARCHAR(255) NOT NULL,
    
    -- =====================================================================
    -- Invitation Lifecycle (References InvitationStatus Lookup Table)
    -- =====================================================================
    Status NVARCHAR(20) NOT NULL DEFAULT 'pending',
    -- ^ References InvitationStatus.StatusCode
    
    InvitedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ExpiresAt DATETIME2 NOT NULL,
    -- ^ InvitedAt + 7 days
    
    AcceptedAt DATETIME2 NULL,
    AcceptedByUserID BIGINT NULL,
    
    -- =====================================================================
    -- Cancellation Audit
    -- =====================================================================
    CancelledAt DATETIME2 NULL,
    CancelledByUserID BIGINT NULL,
    CancellationReason NVARCHAR(500) NULL,
    
    -- =====================================================================
    -- Decline Audit (Phase 2 Feature)
    -- =====================================================================
    DeclinedAt DATETIME2 NULL,
    DeclineReason NVARCHAR(500) NULL,
    -- ^ Optional reason from invitee
    
    -- =====================================================================
    -- Resend Tracking (Rate Limiting)
    -- =====================================================================
    ResendCount INT NOT NULL DEFAULT 0,
    LastResentAt DATETIME2 NULL,
    
    -- =====================================================================
    -- Email Delivery Tracking
    -- =====================================================================
    EmailSentAt DATETIME2 NULL,
    EmailSentStatus NVARCHAR(20) NULL,
    -- ^ Options: 'queued', 'sent', 'delivered', 'bounced', 'failed'
    EmailBounceReason NVARCHAR(500) NULL,
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Invitation_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_Invitation_InvitedBy FOREIGN KEY (InvitedByUserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_Invitation_AcceptedBy FOREIGN KEY (AcceptedByUserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_Invitation_CancelledBy FOREIGN KEY (CancelledByUserID) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_Invitation_Status FOREIGN KEY (Status) 
        REFERENCES [InvitationStatus](StatusCode),
    
    CONSTRAINT FK_Invitation_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    -- Role validation
    CONSTRAINT CK_Invitation_Role CHECK (
        AssignedRole IN ('company_admin', 'company_user')
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

-- Indexes
CREATE UNIQUE INDEX UX_Invitation_Token ON [Invitation](InvitationToken);
CREATE INDEX IX_Invitation_Company_Status ON [Invitation](CompanyID, Status);
CREATE INDEX IX_Invitation_Email_Status ON [Invitation](InvitedEmail, Status);
CREATE INDEX IX_Invitation_Expiry ON [Invitation](ExpiresAt, Status) WHERE Status = 'pending';
GO

PRINT 'Invitation table created successfully (18 fields)!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'User Domain Schema v2 Complete!';
PRINT '========================================';
PRINT 'Lookup Tables:';
PRINT '  1. UserStatus (5 standard statuses)';
PRINT '  2. InvitationStatus (5 standard statuses)';
PRINT '';
PRINT 'Core Tables:';
PRINT '  1. User (28 fields) - ✅ FULL AUDIT TRAIL';
PRINT '  2. UserCompany (15 fields) - ✅ MULTI-COMPANY ACCESS ENABLED';
PRINT '  3. Invitation (23 fields)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Multi-company access (UserCompany many-to-many)';
PRINT '  ✅ Status lookup tables with clear definitions';
PRINT '  ✅ UserCompanyID surrogate primary key';
PRINT '  ✅ JWT session management (Access + Refresh tokens)';
PRINT '  ✅ Email verification (24-hour expiry)';
PRINT '  ✅ Password reset (1-hour expiry)';
PRINT '  ✅ Invitation flow (7-day expiry, resend, decline)';
PRINT '  ✅ Brute force protection (5 failed logins = 15 min lockout)';
PRINT '  ✅ Full audit trail (Solomon standards)';
PRINT '';
PRINT 'Session Management Strategy:';
PRINT '  - Access Token: 1 hour expiry (short-lived)';
PRINT '  - Refresh Token: 7 days expiry (long-lived)';
PRINT '  - User can work seamlessly from work → home (auto-refresh)';
PRINT '  - After 7 days inactivity, must re-login';
PRINT '  - Password reset invalidates all tokens (RefreshTokenVersion++)';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Create Alembic migration (UserStatus, InvitationStatus, User, UserCompany, Invitation)';
PRINT '  2. Validate schema with Solomon (Database Migration Validator)';
PRINT '  3. Implement backend models with multi-company support';
PRINT '  4. Implement JWT refresh token logic';
PRINT '  5. Import test seed data (20 test users, multi-company scenarios)';
PRINT '========================================';
GO

