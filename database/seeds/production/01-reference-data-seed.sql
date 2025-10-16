-- =====================================================================
-- EventLead Platform - Reference Data Seed (Production)
-- =====================================================================
-- Author: Amelia (Developer Agent)
-- Date: October 15, 2025
-- Version: 1.0.0
-- =====================================================================
-- Purpose:
--   Populate ALL lookup/reference tables with required seed data.
--   This ensures no foreign key violations occur during production operations.
--
-- Execution:
--   sqlcmd -S localhost -d EventLeadPlatform -i 01-reference-data-seed.sql
--
-- Idempotence:
--   This script is idempotent - safe to run multiple times.
--   Uses "IF NOT EXISTS" checks to prevent duplicate inserts.
-- =====================================================================

USE [EventLeadPlatform];
GO

PRINT '========================================';
PRINT 'EventLead Platform - Reference Data Seed';
PRINT '========================================';
PRINT '';

-- =====================================================================
-- 1. UserStatus Lookup Table
-- =====================================================================
PRINT '1. Seeding UserStatus lookup table...';

-- Check if data already exists
IF NOT EXISTS (SELECT 1 FROM [UserStatus] WHERE StatusCode = 'active')
BEGIN
    INSERT INTO [UserStatus] (StatusCode, DisplayName, Description, AllowLogin, IsSystemStatus, SortOrder)
    VALUES
        ('active', 'Active', 'User account is active and can log in normally', 1, 1, 1),
        ('unverified', 'Unverified Email', 'User signed up but has not verified email address yet', 0, 1, 2),
        ('suspended', 'Suspended', 'User account suspended by admin (temporary - billing issue, policy violation)', 0, 1, 3),
        ('locked', 'Locked (Brute Force)', 'Account temporarily locked due to failed login attempts (auto-unlocks after 15 min)', 0, 1, 4),
        ('deleted', 'Deleted', 'User account soft-deleted (retain data for audit trail)', 0, 1, 5);
    
    PRINT '   ✓ Inserted 5 user statuses';
END
ELSE
BEGIN
    PRINT '   ℹ UserStatus already populated (5 statuses)';
END
GO

-- =====================================================================
-- 2. InvitationStatus Lookup Table
-- =====================================================================
PRINT '2. Seeding InvitationStatus lookup table...';

-- Check if data already exists
IF NOT EXISTS (SELECT 1 FROM [InvitationStatus] WHERE StatusCode = 'pending')
BEGIN
    INSERT INTO [InvitationStatus] (StatusCode, DisplayName, Description, CanResend, CanCancel, IsFinalState, IsSystemStatus, SortOrder)
    VALUES
        ('pending', 'Pending', 'Invitation sent, awaiting acceptance by invitee', 1, 1, 0, 1, 1),
        ('accepted', 'Accepted', 'Invitee accepted invitation and joined company', 0, 0, 1, 1, 2),
        ('expired', 'Expired', 'Invitation expired (7 days passed) without acceptance', 1, 0, 1, 1, 3),
        ('cancelled', 'Cancelled', 'Admin cancelled invitation before acceptance', 0, 0, 1, 1, 4),
        ('declined', 'Declined', 'Invitee declined invitation (Phase 2 feature)', 0, 0, 1, 1, 5);
    
    PRINT '   ✓ Inserted 5 invitation statuses';
END
ELSE
BEGIN
    PRINT '   ℹ InvitationStatus already populated (5 statuses)';
END
GO

-- =====================================================================
-- 3. System User (UserID = 1)
-- =====================================================================
PRINT '3. Creating System User...';

-- Check if system user exists
IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = 1)
BEGIN
    SET IDENTITY_INSERT [User] ON;
    
    INSERT INTO [User] (
        UserID,
        Email, 
        PasswordHash,
        FirstName, 
        LastName,
        Status,
        EmailVerified,
        OnboardingComplete,
        LoginAttempts,
        TwoFactorEnabled,
        AccessTokenVersion,
        RefreshTokenVersion,
        IsDeleted,
        CreatedDate,
        CreatedBy
    ) VALUES (
        1,
        'system@eventlead.com.au',
        '$2b$12$SystemUserNoPasswordHashRequiredForSystemOperations',  -- Not a real password - system user cannot login
        'System',
        'User',
        'active',
        1,  -- Email verified
        1,  -- Onboarding complete
        0,  -- No login attempts
        0,  -- 2FA disabled
        1,  -- Access token version
        1,  -- Refresh token version
        0,  -- Not deleted
        GETUTCDATE(),
        1   -- Self-referencing (system creates itself)
    );
    
    SET IDENTITY_INSERT [User] OFF;
    
    PRINT '   ✓ System User (UserID = 1) created successfully';
END
ELSE
BEGIN
    PRINT '   ℹ System User (UserID = 1) already exists';
END
GO

-- =====================================================================
-- Verification & Summary
-- =====================================================================
PRINT '';
PRINT '========================================';
PRINT 'Seed Data Summary';
PRINT '========================================';

-- Count records in each table
DECLARE @UserStatusCount INT;
DECLARE @InvitationStatusCount INT;
DECLARE @SystemUserExists BIT;

SELECT @UserStatusCount = COUNT(*) FROM [UserStatus];
SELECT @InvitationStatusCount = COUNT(*) FROM [InvitationStatus];
SELECT @SystemUserExists = CASE WHEN EXISTS(SELECT 1 FROM [User] WHERE UserID = 1) THEN 1 ELSE 0 END;

PRINT '';
PRINT 'Reference Tables:';
PRINT '  UserStatus: ' + CAST(@UserStatusCount AS VARCHAR) + ' statuses';
PRINT '  InvitationStatus: ' + CAST(@InvitationStatusCount AS VARCHAR) + ' statuses';
PRINT '';
PRINT 'System Records:';
PRINT '  System User (UserID = 1): ' + CASE WHEN @SystemUserExists = 1 THEN 'EXISTS ✓' ELSE 'MISSING ✗' END;
PRINT '';

-- Validation checks
IF @UserStatusCount < 5
BEGIN
    PRINT '⚠ WARNING: UserStatus table has fewer than 5 statuses!';
    PRINT '   Expected: active, unverified, suspended, locked, deleted';
END

IF @InvitationStatusCount < 5
BEGIN
    PRINT '⚠ WARNING: InvitationStatus table has fewer than 5 statuses!';
    PRINT '   Expected: pending, accepted, expired, cancelled, declined';
END

IF @SystemUserExists = 0
BEGIN
    PRINT '⚠ WARNING: System User (UserID = 1) does not exist!';
    PRINT '   Required for audit trails (CreatedBy, UpdatedBy)';
END

PRINT '';
PRINT '========================================';
PRINT 'Reference Data Seed Complete!';
PRINT '========================================';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Run EventLead Platform seed (Company, Billing, etc.)';
PRINT '  2. Test user signup: POST /api/auth/signup';
PRINT '  3. Verify no foreign key violations occur';
PRINT '';
GO

