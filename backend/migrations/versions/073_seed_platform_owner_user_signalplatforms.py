"""Ensure Anthony is dbo.User.UserID = 1 and company_admin for Signal Platforms.

Former login anthonykeevy@gmail.com -> anthony@signalplatforms.com.au.
Runs after schema head; merges legacy row and superseded migration.seed if present.

Revision ID: 073
Revises: 072
Create Date: 2026-05-13
"""

from alembic import op

revision = "073"
down_revision = "072"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        r"""
        DECLARE @Now DATETIME2 = GETUTCDATE();
        DECLARE @TargetEmail NVARCHAR(255) = N'anthony@signalplatforms.com.au';
        DECLARE @LegacyEmail NVARCHAR(255) = N'anthonykeevy@gmail.com';

        DECLARE @CompanyID BIGINT = (
            SELECT TOP (1) c.CompanyID
            FROM dbo.[Company] c
            WHERE c.IsDeleted = 0
              AND c.CompanyName = N'Signal Platforms'
            ORDER BY c.CompanyID ASC
        );
        DECLARE @AuCountry BIGINT = (
            SELECT TOP (1) CountryID FROM ref.[Country] WHERE CountryCode = N'AU' ORDER BY CountryID ASC
        );
        DECLARE @ActiveStatus BIGINT = (
            SELECT TOP (1) UserStatusID FROM ref.[UserStatus] WHERE StatusCode = N'active' ORDER BY SortOrder ASC
        );
        DECLARE @AdminRole BIGINT = (
            SELECT TOP (1) UserCompanyRoleID FROM ref.[UserCompanyRole] WHERE RoleCode = N'company_admin'
        );
        DECLARE @CompanyUserActive BIGINT = (
            SELECT TOP (1) UserCompanyStatusID FROM ref.[UserCompanyStatus] WHERE StatusCode = N'active'
        );
        DECLARE @SignupVia BIGINT = (
            SELECT TOP (1) JoinedViaID FROM ref.[JoinedVia] WHERE MethodCode = N'signup' ORDER BY SortOrder ASC
        );

        DECLARE @LegacyUid BIGINT = (
            SELECT TOP (1) u.UserID
            FROM dbo.[User] u
            WHERE u.IsDeleted = 0 AND LOWER(u.Email) = LOWER(@LegacyEmail)
            ORDER BY u.UserID ASC
        );

        DECLARE @PwdFromLegacy NVARCHAR(500);
        SELECT @PwdFromLegacy = u.PasswordHash
        FROM dbo.[User] u
        WHERE @LegacyUid IS NOT NULL AND u.UserID = @LegacyUid AND u.IsDeleted = 0;

        -- Target email occupied by another UserID — rename away so UID 1 can claim it (filtered unique UX_User_Email).
        DECLARE @DupTargetUid BIGINT = (
            SELECT TOP (1) u.UserID
            FROM dbo.[User] u
            WHERE u.IsDeleted = 0 AND LOWER(u.Email) = LOWER(@TargetEmail)
            ORDER BY u.UserID ASC
        );
        IF @DupTargetUid IS NOT NULL AND @DupTargetUid <> 1
            UPDATE dbo.[User]
            SET Email = N'superseded-uid-' + CAST(@DupTargetUid AS NVARCHAR(20)) + N'@orphan.invalid',
                UpdatedDate = @Now
            WHERE UserID = @DupTargetUid AND IsDeleted = 0;

        DECLARE @PwdUser1 NVARCHAR(500);
        DECLARE @HadUser1 BIT = CASE WHEN EXISTS (SELECT 1 FROM dbo.[User] WHERE UserID = 1 AND IsDeleted = 0) THEN 1 ELSE 0 END;

        IF @HadUser1 = 1
        BEGIN
            SELECT @PwdUser1 = PasswordHash FROM dbo.[User] WHERE UserID = 1 AND IsDeleted = 0;
            IF @PwdFromLegacy IS NOT NULL
                SET @PwdUser1 = @PwdFromLegacy;
            ELSE IF (@PwdUser1 IS NOT NULL AND (
                    LTRIM(RTRIM(@PwdUser1)) = N''
                    OR @PwdUser1 = N'MIGRATION_ONLY_NOT_FOR_LOGIN'
                    OR @PwdUser1 LIKE N'TEMPORARY_BCRYPT%' COLLATE Latin1_General_CI_AI
                    OR @PwdUser1 LIKE N'%NOT_FOR_LOGIN%'))
                SET @PwdUser1 = COALESCE(NULLIF(@PwdFromLegacy, N''), @PwdUser1);

            UPDATE dbo.[User]
            SET Email = @TargetEmail,
                PasswordHash = COALESCE(NULLIF(@PwdUser1, N''), PasswordHash),
                FirstName = N'Anthony',
                LastName = N'Keevy',
                StatusID = @ActiveStatus,
                IsEmailVerified = 1,
                EmailVerifiedAt = COALESCE(EmailVerifiedAt, @Now),
                CountryID = COALESCE(CountryID, @AuCountry),
                IsLocked = 0,
                LockedUntil = NULL,
                LockedReason = NULL,
                FailedLoginAttempts = 0,
                UpdatedDate = @Now
            WHERE UserID = 1 AND IsDeleted = 0;
        END
        ELSE
        BEGIN
            SET @PwdUser1 = COALESCE(NULLIF(@PwdFromLegacy, N''), N'MIGRATION_ONLY_NOT_FOR_LOGIN');
            SET IDENTITY_INSERT dbo.[User] ON;
            INSERT INTO dbo.[User] (
                UserID,
                Email,
                PasswordHash,
                FirstName,
                LastName,
                StatusID,
                IsEmailVerified,
                EmailVerifiedAt,
                CountryID,
                TimezoneIdentifier,
                CreatedDate,
                UpdatedDate
            )
            VALUES (
                1,
                @TargetEmail,
                @PwdUser1,
                N'Anthony',
                N'Keevy',
                @ActiveStatus,
                1,
                @Now,
                @AuCountry,
                N'Australia/Sydney',
                @Now,
                @Now
            );
            SET IDENTITY_INSERT dbo.[User] OFF;
        END;

        -- Merge legacy gmail: move Signal Platforms UserCompany onto UserID 1, then retire duplicate user row.
        IF @LegacyUid IS NOT NULL AND @LegacyUid <> 1 AND @CompanyID IS NOT NULL
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM dbo.[UserCompany] uc
                WHERE uc.UserID = 1 AND uc.CompanyID = @CompanyID AND uc.IsDeleted = 0
            )
                UPDATE dbo.[UserCompany]
                SET IsDeleted = 1,
                    RemovedDate = @Now,
                    RemovalReason = N'Superseded by UserID 1 (073 seed)',
                    UpdatedDate = @Now
                WHERE UserID = @LegacyUid AND CompanyID = @CompanyID AND IsDeleted = 0;
            ELSE
            BEGIN
                DELETE FROM dbo.[UserCompany]
                WHERE UserID = 1 AND CompanyID = @CompanyID AND IsDeleted = 1;

                UPDATE dbo.[UserCompany]
                SET UserID = 1,
                    UpdatedDate = @Now,
                    UpdatedBy = 1,
                    InvitedBy = CASE WHEN InvitedBy = @LegacyUid THEN 1 ELSE InvitedBy END
                WHERE UserID = @LegacyUid AND CompanyID = @CompanyID AND IsDeleted = 0;
            END;

            IF (
                SELECT COUNT(*) FROM dbo.[UserCompany] uc
                WHERE uc.UserID = @LegacyUid AND uc.IsDeleted = 0
            ) = 0
                UPDATE dbo.[User]
                SET IsDeleted = 1,
                    DeletedDate = @Now,
                    DeletedBy = 1,
                    Email = N'superseded-gmail-' + CAST(@LegacyUid AS NVARCHAR(20)) + N'@orphan.invalid',
                    UpdatedDate = @Now,
                    UpdatedBy = 1
                WHERE UserID = @LegacyUid AND IsDeleted = 0 AND LOWER(Email) = LOWER(@LegacyEmail);
            ELSE
                UPDATE dbo.[User]
                SET Email = N'legacy-uid-' + CAST(@LegacyUid AS NVARCHAR(20)) + N'@orphan.invalid',
                    UpdatedDate = @Now,
                    UpdatedBy = 1
                WHERE UserID = @LegacyUid AND IsDeleted = 0 AND LOWER(Email) = LOWER(@LegacyEmail);
        END;

        IF @CompanyID IS NOT NULL
        BEGIN
            IF EXISTS (
                SELECT 1 FROM dbo.[UserCompany] uc
                WHERE uc.UserID = 1 AND uc.CompanyID = @CompanyID AND uc.IsDeleted = 0
            )
                UPDATE dbo.[UserCompany]
                SET UserCompanyRoleID = @AdminRole,
                    StatusID = @CompanyUserActive,
                    IsPrimaryCompany = 1,
                    JoinedViaID = COALESCE(JoinedViaID, @SignupVia),
                    UpdatedDate = @Now,
                    UpdatedBy = 1
                WHERE UserID = 1 AND CompanyID = @CompanyID AND IsDeleted = 0;
            ELSE
                INSERT INTO dbo.[UserCompany] (
                    UserID,
                    CompanyID,
                    UserCompanyRoleID,
                    StatusID,
                    IsPrimaryCompany,
                    JoinedViaID,
                    CreatedDate,
                    UpdatedDate,
                    CreatedBy,
                    UpdatedBy
                )
                VALUES (
                    1,
                    @CompanyID,
                    @AdminRole,
                    @CompanyUserActive,
                    1,
                    @SignupVia,
                    @Now,
                    @Now,
                    1,
                    1
                );
        END;

        DECLARE @MigrateSeedUid BIGINT = (
            SELECT TOP (1) u.UserID
            FROM dbo.[User] u
            WHERE u.IsDeleted = 0 AND u.Email LIKE N'%migration.seed%internal%'
            ORDER BY u.UserID ASC
        );
        IF @MigrateSeedUid IS NOT NULL AND @MigrateSeedUid <> 1
            UPDATE dbo.[User]
            SET IsDeleted = 1,
                DeletedDate = @Now,
                DeletedBy = 1,
                Email = N'inactive-seed-' + CAST(@MigrateSeedUid AS NVARCHAR(20)) + N'@orphan.invalid',
                UpdatedDate = @Now,
                UpdatedBy = 1
            WHERE UserID = @MigrateSeedUid;
        """
    )


def downgrade() -> None:
    pass
