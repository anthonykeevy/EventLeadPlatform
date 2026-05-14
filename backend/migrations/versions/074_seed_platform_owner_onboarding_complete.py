"""Platform owner (UserID 1): onboarding complete + system_admin when UserCompany exists.

073 seeds anthony@signalplatforms.com.au as company_admin with an active UserCompany but
left OnboardingComplete = 0, so the SPA shows onboarding and POST /companies fails with
'User already has an active company'.

Also assigns ref.UserRole system_admin (User.UserRoleID) so JWT role is system_admin and
Admin Dashboard / useRequireAdmin work (Story 2.6). Product UI calls this "Global admin".

Revision ID: 074
Revises: 073
Create Date: 2026-05-14
"""

from alembic import op

revision = "074"
down_revision = "073"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        r"""
        DECLARE @Now DATETIME2 = GETUTCDATE();
        DECLARE @SystemAdminRole BIGINT = (
            SELECT TOP (1) ur.UserRoleID
            FROM ref.[UserRole] ur
            WHERE ur.RoleCode = N'system_admin' AND ur.IsActive = 1
            ORDER BY ur.UserRoleID ASC
        );

        IF @SystemAdminRole IS NULL
        BEGIN
            RAISERROR(N'074: ref.UserRole row with RoleCode=system_admin is required', 16, 1);
        END

        UPDATE dbo.[User]
        SET
            OnboardingComplete = 1,
            OnboardingStep = 5,
            UserRoleID = @SystemAdminRole,
            UpdatedDate = @Now,
            UpdatedBy = 1
        WHERE UserID = 1
          AND IsDeleted = 0
          AND EXISTS (
              SELECT 1
              FROM dbo.[UserCompany] uc
              INNER JOIN ref.[UserCompanyStatus] ucs ON ucs.UserCompanyStatusID = uc.StatusID
              WHERE uc.UserID = dbo.[User].UserID
                AND uc.IsDeleted = 0
                AND ucs.StatusCode = N'active'
          );
        """
    )


def downgrade() -> None:
    pass
