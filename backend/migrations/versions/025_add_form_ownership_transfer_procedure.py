"""Add Form Ownership Transfer Stored Procedure

Revision ID: 025_add_form_ownership_transfer_procedure
Revises: 024_add_agency_form_builder_role
Create Date: 2025-01-XX 12:00:00.000000

Story: Epic 2 - Form Access Control Enhancement
Purpose: Enable bulk ownership transfer of forms for user off-boarding scenarios

Changes:
1. Create sp_TransferFormOwnership stored procedure
2. Grant execute permissions to appropriate roles

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '025_form_ownership_transfer'
down_revision = '024_add_agency_form_builder_role'
branch_labels = None
depends_on = None


def upgrade():
    """Create form ownership transfer stored procedure"""
    
    op.execute("""
        CREATE PROCEDURE [dbo].[sp_TransferFormOwnership]
            @FromUserID BIGINT,
            @ToUserID BIGINT,
            @CompanyID BIGINT,
            @PerformedBy BIGINT,
            @Reason NVARCHAR(500) = NULL
        AS
        BEGIN
            SET NOCOUNT ON;
            
            BEGIN TRANSACTION;
            
            BEGIN TRY
                -- =====================================================================
                -- VALIDATION
                -- =====================================================================
                
                -- Verify @PerformedBy has Company Admin privileges OR is System Admin
                DECLARE @IsSystemAdmin BIT = 0;
                DECLARE @IsCompanyAdmin BIT = 0;
                
                -- Check if System Admin
                SELECT @IsSystemAdmin = 1
                FROM [dbo].[User] u
                INNER JOIN ref.UserRole ur ON u.UserRoleID = ur.UserRoleID
                WHERE u.UserID = @PerformedBy
                  AND u.IsDeleted = 0
                  AND ur.RoleCode = 'system_admin';
                
                -- Check if Company Admin
                IF @IsSystemAdmin = 0
                BEGIN
                    SELECT @IsCompanyAdmin = 1
                    FROM dbo.UserCompany uc
                    INNER JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
                    INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
                    WHERE uc.UserID = @PerformedBy
                      AND uc.CompanyID = @CompanyID
                      AND uc.IsDeleted = 0
                      AND ucs.StatusCode = 'active'
                      AND ucr.RoleCode = 'company_admin';
                END
                
                IF @IsSystemAdmin = 0 AND @IsCompanyAdmin = 0
                BEGIN
                    RAISERROR('User performing transfer must be Company Admin for the company or System Admin', 16, 1);
                    RETURN;
                END
                
                -- Verify @FromUserID is a member of @CompanyID
                IF NOT EXISTS (
                    SELECT 1
                    FROM dbo.UserCompany uc
                    INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
                    WHERE uc.UserID = @FromUserID
                      AND uc.CompanyID = @CompanyID
                      AND uc.IsDeleted = 0
                      AND ucs.StatusCode = 'active'
                )
                BEGIN
                    RAISERROR('FromUserID must be an active member of the specified company', 16, 1);
                    RETURN;
                END
                
                -- Verify @ToUserID is a member of @CompanyID
                IF NOT EXISTS (
                    SELECT 1
                    FROM dbo.UserCompany uc
                    INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
                    WHERE uc.UserID = @ToUserID
                      AND uc.CompanyID = @CompanyID
                      AND uc.IsDeleted = 0
                      AND ucs.StatusCode = 'active'
                )
                BEGIN
                    RAISERROR('ToUserID must be an active member of the specified company', 16, 1);
                    RETURN;
                END
                
                -- Verify users are not the same
                IF @FromUserID = @ToUserID
                BEGIN
                    RAISERROR('FromUserID and ToUserID cannot be the same', 16, 1);
                    RETURN;
                END
                
                -- =====================================================================
                -- OWNERSHIP TRANSFER
                -- =====================================================================
                
                DECLARE @FormsTransferred INT = 0;
                DECLARE @AccessControlsTransferred INT = 0;
                
                -- Update Form.CreatedBy
                UPDATE f
                SET f.CreatedBy = @ToUserID,
                    f.UpdatedBy = @PerformedBy,
                    f.UpdatedDate = GETUTCDATE()
                FROM dbo.Form f
                WHERE f.CompanyID = @CompanyID
                  AND f.CreatedBy = @FromUserID
                  AND f.IsDeleted = 0;
                
                SET @FormsTransferred = @@ROWCOUNT;
                
                -- Update FormAccessControl.UserID (transfer access grants)
                UPDATE fac
                SET fac.UserID = @ToUserID,
                    fac.UpdatedBy = @PerformedBy,
                    fac.UpdatedDate = GETUTCDATE()
                FROM dbo.FormAccessControl fac
                INNER JOIN dbo.Form f ON fac.FormID = f.FormID
                WHERE f.CompanyID = @CompanyID
                  AND fac.UserID = @FromUserID
                  AND fac.IsDeleted = 0;
                
                SET @AccessControlsTransferred = @@ROWCOUNT;
                
                -- =====================================================================
                -- AUDIT TRAIL
                -- =====================================================================
                
                -- Get user details for audit
                DECLARE @FromUserEmail NVARCHAR(255);
                DECLARE @ToUserEmail NVARCHAR(255);
                DECLARE @PerformedByEmail NVARCHAR(255);
                
                SELECT @FromUserEmail = Email FROM [dbo].[User] WHERE UserID = @FromUserID;
                SELECT @ToUserEmail = Email FROM [dbo].[User] WHERE UserID = @ToUserID;
                SELECT @PerformedByEmail = Email FROM [dbo].[User] WHERE UserID = @PerformedBy;
                
                -- Insert audit records for each transferred form
                INSERT INTO audit.ActivityLog (
                    UserID,
                    UserEmail,
                    CompanyID,
                    Action,
                    EntityType,
                    EntityID,
                    OldValue,
                    NewValue,
                    CreatedDate
                )
                SELECT
                    @PerformedBy,  -- User who performed the transfer
                    @PerformedByEmail,  -- Email of user who performed the transfer
                    @CompanyID,
                    'form.ownership.transferred',
                    'Form',
                    f.FormID,
                    JSON_OBJECT(
                        'old_owner_id': @FromUserID,
                        'old_owner_email': @FromUserEmail,
                        'form_id': f.FormID,
                        'form_name': f.FormName
                    ),
                    JSON_OBJECT(
                        'new_owner_id': @ToUserID,
                        'new_owner_email': @ToUserEmail,
                        'form_id': f.FormID,
                        'form_name': f.FormName,
                        'transferred_by': @PerformedBy,
                        'transferred_by_email': @PerformedByEmail,
                        'reason': ISNULL(@Reason, 'Bulk ownership transfer on offboarding'),
                        'transferred_at': GETUTCDATE()
                    ),
                    GETUTCDATE()
                FROM dbo.Form f
                WHERE f.CompanyID = @CompanyID
                  AND f.CreatedBy = @ToUserID  -- Now owned by new user
                  AND f.UpdatedBy = @PerformedBy  -- Just updated by this procedure
                  AND f.UpdatedDate >= DATEADD(SECOND, -5, GETUTCDATE());  -- Within last 5 seconds
                
                -- =====================================================================
                -- SUCCESS
                -- =====================================================================
                
                COMMIT TRANSACTION;
                
                SELECT 
                    @FormsTransferred AS FormsTransferred,
                    @AccessControlsTransferred AS AccessControlsTransferred,
                    'SUCCESS' AS Status,
                    'Ownership transfer completed successfully' AS Message;
                
            END TRY
            BEGIN CATCH
                IF @@TRANCOUNT > 0
                    ROLLBACK TRANSACTION;
                
                DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
                DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
                DECLARE @ErrorState INT = ERROR_STATE();
                
                RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
            END CATCH
        END
    """)


def downgrade():
    """Drop form ownership transfer stored procedure"""
    
    op.execute("DROP PROCEDURE IF EXISTS [dbo].[sp_TransferFormOwnership]")

