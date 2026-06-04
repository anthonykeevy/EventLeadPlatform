/*
  Dev DB alignment: Signal Platforms (CompanyID 1) + platform owner UserID 1
  Mirrors migrations 009 (company seed), 073 (user/company link), 074 (onboarding + system_admin).

  Run against your DEV database (SSMS / Azure Data Studio). Review the diagnostic SELECTs first.
  Password: copies hash from anthonykeevy@gmail.com if present; otherwise leaves existing UserID 1 hash.
  If login fails after this, use app password reset or copy PasswordHash from TEST for UserID 1.

  After success, run: alembic upgrade head  (096 landing demo shells if not already applied)
*/

SET NOCOUNT ON;
DECLARE @Now DATETIME2 = GETUTCDATE();

-- ─── Reference IDs ───
DECLARE @AuCountry BIGINT = (SELECT TOP (1) CountryID FROM ref.[Country] WHERE CountryCode = N'AU' ORDER BY CountryID);
DECLARE @ActiveStatus BIGINT = (SELECT TOP (1) UserStatusID FROM ref.[UserStatus] WHERE StatusCode = N'active' ORDER BY SortOrder);
DECLARE @AdminRole BIGINT = (SELECT TOP (1) UserCompanyRoleID FROM ref.[UserCompanyRole] WHERE RoleCode = N'company_admin');
DECLARE @CompanyUserActive BIGINT = (SELECT TOP (1) UserCompanyStatusID FROM ref.[UserCompanyStatus] WHERE StatusCode = N'active');
DECLARE @SignupVia BIGINT = (SELECT TOP (1) JoinedViaID FROM ref.[JoinedVia] WHERE MethodCode = N'signup' ORDER BY SortOrder);
DECLARE @SystemAdminRole BIGINT = (
    SELECT TOP (1) ur.UserRoleID FROM ref.[UserRole] ur
    WHERE ur.RoleCode = N'system_admin' AND ur.IsActive = 1 ORDER BY ur.UserRoleID
);

IF @AuCountry IS NULL RAISERROR(N'Missing ref.Country AU', 16, 1);
IF @ActiveStatus IS NULL RAISERROR(N'Missing ref.UserStatus active', 16, 1);
IF @AdminRole IS NULL RAISERROR(N'Missing ref.UserCompanyRole company_admin', 16, 1);
IF @CompanyUserActive IS NULL RAISERROR(N'Missing ref.UserCompanyStatus active', 16, 1);
IF @SystemAdminRole IS NULL RAISERROR(N'Missing ref.UserRole system_admin', 16, 1);

-- ─── BEFORE (diagnostics) ───
PRINT N'--- BEFORE ---';
SELECT CompanyID, CompanyName, LegalEntityName, ABN, IsActive, IsDeleted FROM dbo.[Company] WHERE CompanyID = 1 OR CompanyName = N'Signal Platforms';
SELECT UserID, Email, FirstName, LastName, OnboardingComplete, OnboardingStep, UserRoleID, IsDeleted FROM dbo.[User] WHERE UserID = 1 OR Email LIKE N'%anthony%signalplatforms%';
SELECT uc.UserCompanyID, uc.UserID, uc.CompanyID, uc.IsPrimaryCompany, uc.IsDeleted
FROM dbo.[UserCompany] uc WHERE uc.UserID = 1 OR uc.CompanyID = 1;

BEGIN TRANSACTION;

-- ═══════════════════════════════════════════════════════════════════
-- STEP 1: CompanyID 1 = Signal Platforms (migration 009 scenario 1/2)
-- ═══════════════════════════════════════════════════════════════════
IF NOT EXISTS (SELECT 1 FROM dbo.[Company] WHERE CompanyID = 1)
BEGIN
    SET IDENTITY_INSERT dbo.[Company] ON;
    INSERT INTO dbo.[Company] (
        CompanyID, CompanyName, LegalEntityName, DisplayNameSource,
        ABN, ACN, ABNStatus, EntityType, GSTRegistered,
        Email, Website, CountryID, IsActive, IsDeleted, CreatedDate, UpdatedDate
    )
    VALUES (
        1, N'Signal Platforms', N'SIGNAL PLATFORMS PTY LTD', N'Legal',
        N'23695192511', N'695192511', N'Active', N'Australian Private Company', 0,
        N'noreply@signalplatforms.com.au', N'https://signalplatforms.com.au',
        @AuCountry, 1, 0, @Now, @Now
    );
    SET IDENTITY_INSERT dbo.[Company] OFF;
    PRINT N'STEP 1: Inserted CompanyID 1 (Signal Platforms).';
END
ELSE
BEGIN
    UPDATE dbo.[Company]
    SET CompanyName = N'Signal Platforms',
        LegalEntityName = N'SIGNAL PLATFORMS PTY LTD',
        DisplayNameSource = N'Legal',
        ABN = N'23695192511',
        ACN = N'695192511',
        ABNStatus = N'Active',
        EntityType = N'Australian Private Company',
        GSTRegistered = 0,
        Email = N'noreply@signalplatforms.com.au',
        Website = N'https://signalplatforms.com.au',
        CountryID = @AuCountry,
        IsActive = 1,
        IsDeleted = 0,
        DeletedDate = NULL,
        DeletedBy = NULL,
        UpdatedDate = @Now
    WHERE CompanyID = 1;
    PRINT N'STEP 1: Updated CompanyID 1 to Signal Platforms profile.';
END

DECLARE @CompanyID BIGINT = 1;
DECLARE @TargetEmail NVARCHAR(255) = N'anthony@signalplatforms.com.au';
DECLARE @LegacyEmail NVARCHAR(255) = N'anthonykeevy@gmail.com';

-- ═══════════════════════════════════════════════════════════════════
-- STEP 2: UserID 1 + UserCompany (migration 073)
-- ═══════════════════════════════════════════════════════════════════
DECLARE @LegacyUid BIGINT = (
    SELECT TOP (1) u.UserID FROM dbo.[User] u
    WHERE u.IsDeleted = 0 AND LOWER(u.Email) = LOWER(@LegacyEmail) ORDER BY u.UserID
);
DECLARE @PwdFromLegacy NVARCHAR(500);
SELECT @PwdFromLegacy = u.PasswordHash FROM dbo.[User] u
WHERE @LegacyUid IS NOT NULL AND u.UserID = @LegacyUid AND u.IsDeleted = 0;

DECLARE @DupTargetUid BIGINT = (
    SELECT TOP (1) u.UserID FROM dbo.[User] u
    WHERE u.IsDeleted = 0 AND LOWER(u.Email) = LOWER(@TargetEmail) ORDER BY u.UserID
);
IF @DupTargetUid IS NOT NULL AND @DupTargetUid <> 1
BEGIN
    UPDATE dbo.[User]
    SET Email = N'superseded-uid-' + CAST(@DupTargetUid AS NVARCHAR(20)) + N'@orphan.invalid',
        UpdatedDate = @Now
    WHERE UserID = @DupTargetUid AND IsDeleted = 0;
END

DECLARE @PwdUser1 NVARCHAR(500);
DECLARE @HadUser1 BIT = CASE WHEN EXISTS (SELECT 1 FROM dbo.[User] WHERE UserID = 1 AND IsDeleted = 0) THEN 1 ELSE 0 END;

IF @HadUser1 = 1
BEGIN
    SELECT @PwdUser1 = PasswordHash FROM dbo.[User] WHERE UserID = 1 AND IsDeleted = 0;
    IF @PwdFromLegacy IS NOT NULL SET @PwdUser1 = @PwdFromLegacy;
    UPDATE dbo.[User]
    SET Email = @TargetEmail,
        PasswordHash = COALESCE(NULLIF(@PwdUser1, N''), PasswordHash),
        FirstName = N'Anthony',
        LastName = N'Keevy',
        StatusID = @ActiveStatus,
        IsEmailVerified = 1,
        EmailVerifiedAt = COALESCE(EmailVerifiedAt, @Now),
        CountryID = COALESCE(CountryID, @AuCountry),
        TimezoneIdentifier = COALESCE(TimezoneIdentifier, N'Australia/Sydney'),
        IsLocked = 0,
        LockedUntil = NULL,
        LockedReason = NULL,
        FailedLoginAttempts = 0,
        UpdatedDate = @Now
    WHERE UserID = 1 AND IsDeleted = 0;
    PRINT N'STEP 2a: Updated UserID 1.';
END
ELSE
BEGIN
    SET @PwdUser1 = COALESCE(NULLIF(@PwdFromLegacy, N''), N'MIGRATION_ONLY_NOT_FOR_LOGIN');
    SET IDENTITY_INSERT dbo.[User] ON;
    INSERT INTO dbo.[User] (
        UserID, Email, PasswordHash, FirstName, LastName, StatusID,
        IsEmailVerified, EmailVerifiedAt, CountryID, TimezoneIdentifier,
        OnboardingComplete, OnboardingStep, CreatedDate, UpdatedDate, IsDeleted
    )
    VALUES (
        1, @TargetEmail, @PwdUser1, N'Anthony', N'Keevy', @ActiveStatus,
        1, @Now, @AuCountry, N'Australia/Sydney',
        0, 0, @Now, @Now, 0
    );
    SET IDENTITY_INSERT dbo.[User] OFF;
    PRINT N'STEP 2a: Inserted UserID 1 (no prior row).';
END

IF @LegacyUid IS NOT NULL AND @LegacyUid <> 1
BEGIN
    IF EXISTS (SELECT 1 FROM dbo.[UserCompany] WHERE UserID = 1 AND CompanyID = @CompanyID AND IsDeleted = 0)
        UPDATE dbo.[UserCompany]
        SET IsDeleted = 1, RemovedDate = @Now, RemovalReason = N'Superseded by UserID 1 (dev align)', UpdatedDate = @Now
        WHERE UserID = @LegacyUid AND CompanyID = @CompanyID AND IsDeleted = 0;
    ELSE
    BEGIN
        DELETE FROM dbo.[UserCompany] WHERE UserID = 1 AND CompanyID = @CompanyID AND IsDeleted = 1;
        UPDATE dbo.[UserCompany]
        SET UserID = 1, UpdatedDate = @Now, UpdatedBy = 1,
            InvitedBy = CASE WHEN InvitedBy = @LegacyUid THEN 1 ELSE InvitedBy END
        WHERE UserID = @LegacyUid AND CompanyID = @CompanyID AND IsDeleted = 0;
    END;
END

IF EXISTS (SELECT 1 FROM dbo.[UserCompany] WHERE UserID = 1 AND CompanyID = @CompanyID AND IsDeleted = 0)
    UPDATE dbo.[UserCompany]
    SET UserCompanyRoleID = @AdminRole, StatusID = @CompanyUserActive, IsPrimaryCompany = 1,
        JoinedViaID = COALESCE(JoinedViaID, @SignupVia), UpdatedDate = @Now, UpdatedBy = 1
    WHERE UserID = 1 AND CompanyID = @CompanyID AND IsDeleted = 0;
ELSE
    INSERT INTO dbo.[UserCompany] (
        UserID, CompanyID, UserCompanyRoleID, StatusID, IsPrimaryCompany,
        JoinedViaID, CreatedDate, UpdatedDate, CreatedBy, UpdatedBy, IsDeleted
    )
    VALUES (1, @CompanyID, @AdminRole, @CompanyUserActive, 1, @SignupVia, @Now, @Now, 1, 1, 0);

PRINT N'STEP 2b: UserCompany link UserID 1 <-> CompanyID 1 (company_admin, active, primary).';

-- ═══════════════════════════════════════════════════════════════════
-- STEP 3: Onboarding complete + system_admin (migration 074)
-- ═══════════════════════════════════════════════════════════════════
UPDATE dbo.[User]
SET OnboardingComplete = 1,
    OnboardingStep = 5,
    UserRoleID = @SystemAdminRole,
    UpdatedDate = @Now,
    UpdatedBy = 1
WHERE UserID = 1 AND IsDeleted = 0
  AND EXISTS (
      SELECT 1 FROM dbo.[UserCompany] uc
      INNER JOIN ref.[UserCompanyStatus] ucs ON ucs.UserCompanyStatusID = uc.StatusID
      WHERE uc.UserID = 1 AND uc.IsDeleted = 0 AND ucs.StatusCode = N'active'
  );

PRINT N'STEP 3: OnboardingComplete=1, OnboardingStep=5, UserRole=system_admin.';

COMMIT TRANSACTION;

-- ─── AFTER (verify) ───
PRINT N'--- AFTER ---';
SELECT CompanyID, CompanyName, LegalEntityName, ABN, Email, Website, IsActive, IsDeleted
FROM dbo.[Company] WHERE CompanyID = 1;

SELECT u.UserID, u.Email, u.FirstName, u.LastName, u.OnboardingComplete, u.OnboardingStep,
       ur.RoleCode AS GlobalRole, u.IsEmailVerified, u.IsDeleted
FROM dbo.[User] u
LEFT JOIN ref.[UserRole] ur ON ur.UserRoleID = u.UserRoleID
WHERE u.UserID = 1;

SELECT uc.UserCompanyID, uc.UserID, uc.CompanyID, r.RoleCode, s.StatusCode, uc.IsPrimaryCompany
FROM dbo.[UserCompany] uc
INNER JOIN ref.[UserCompanyRole] r ON r.UserCompanyRoleID = uc.UserCompanyRoleID
INNER JOIN ref.[UserCompanyStatus] s ON s.UserCompanyStatusID = uc.StatusID
WHERE uc.UserID = 1 AND uc.CompanyID = 1 AND uc.IsDeleted = 0;
