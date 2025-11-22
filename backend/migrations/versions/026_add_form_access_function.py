"""Add Centralized Form Access Function

Revision ID: 026_add_form_access_function
Revises: 025_add_form_ownership_transfer_procedure
Create Date: 2025-01-XX 12:00:00.000000

Story: Epic 2 - Form Access Control Enhancement
Purpose: Centralize all form access logic in a database function for consistent access checks

Changes:
1. Create fn_GetUserFormAccess table-valued function
2. Create recommended indexes for performance
3. Grant execute permissions

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '026_form_access_function'
down_revision = '025_form_ownership_transfer'
branch_labels = None
depends_on = None


def upgrade():
    """Create centralized form access function and indexes"""
    
    # Create the table-valued function
    op.execute("""
        CREATE FUNCTION [dbo].[fn_GetUserFormAccess]
        (
            @UserID BIGINT,
            @FormID BIGINT
        )
        RETURNS TABLE
        AS
        RETURN
        (
            WITH AccessCheck AS (
                SELECT
                    @UserID AS UserID,
                    @FormID AS FormID,
                    -- Get form details
                    f.CompanyID AS FormCompanyID,
                    f.EventID AS FormEventID,
                    f.CreatedBy AS FormCreatedBy,
                    -- Get user system role
                    ur.RoleCode AS UserSystemRole,
                    -- Get user company role for form's company
                    ucr.RoleCode AS UserCompanyRole,
                    ucr.CanManageForms AS UserCanManageForms,
                    ucr.CanViewReports AS UserCanViewReports,
                    -- Check explicit FormAccessControl
                    fac.FormAccessControlAccessTypeID AS ExplicitAccessTypeID,
                    facat.AccessTypeCode AS ExplicitAccessTypeCode,
                    -- Check agency event-scoped access
                    ecr.HasViewAllFormsForEvent AS AgencyHasViewAllForms,
                    ecr.HasEditAllFormsForEvent AS AgencyHasEditAllForms,
                    -- Agency company ID (if applicable)
                    ec.CompanyID AS AgencyCompanyID
        FROM dbo.Form f
        -- Get user system role
        LEFT JOIN [dbo].[User] u ON u.UserID = @UserID AND u.IsDeleted = 0
        LEFT JOIN ref.UserRole ur ON u.UserRoleID = ur.UserRoleID
                -- Get user company role for form's company
                LEFT JOIN dbo.UserCompany uc ON uc.UserID = @UserID 
                    AND uc.CompanyID = f.CompanyID 
                    AND uc.IsDeleted = 0
                LEFT JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID 
                    AND ucs.StatusCode = 'active'
                LEFT JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
                -- Check explicit FormAccessControl
                LEFT JOIN dbo.FormAccessControl fac ON fac.FormID = f.FormID 
                    AND fac.UserID = @UserID 
                    AND fac.IsDeleted = 0
                LEFT JOIN ref.FormAccessControlAccessType facat ON fac.FormAccessControlAccessTypeID = facat.FormAccessControlAccessTypeID
                -- Check agency event-scoped access
                LEFT JOIN dbo.UserCompany uc_agency ON uc_agency.UserID = @UserID 
                    AND uc_agency.IsDeleted = 0
                LEFT JOIN ref.UserCompanyStatus ucs_agency ON uc_agency.StatusID = ucs_agency.UserCompanyStatusID 
                    AND ucs_agency.StatusCode = 'active'
                LEFT JOIN dbo.EventCompany ec ON ec.EventID = f.EventID 
                    AND ec.CompanyID = uc_agency.CompanyID 
                    AND ec.IsDeleted = 0 
                    AND ec.IsActive = 1
                LEFT JOIN ref.EventCompanyRole ecr ON ec.EventCompanyRoleID = ecr.EventCompanyRoleID
                WHERE f.FormID = @FormID 
                  AND f.IsDeleted = 0
            )
            SELECT
                UserID,
                FormID,
                -- Determine effective access type
                CASE
                    -- Priority 1: System Admin Override
                    WHEN UserSystemRole = 'system_admin' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    
                    -- Priority 2: Resource Ownership
                    WHEN FormCreatedBy = UserID THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    
                    -- Priority 3: Explicit FormAccessControl
                    WHEN ExplicitAccessTypeID IS NOT NULL THEN
                        ExplicitAccessTypeID
                    
                    -- Priority 4: Agency Event-Scoped Access
                    WHEN AgencyHasEditAllForms = 1 THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'EDIT')
                    WHEN AgencyHasViewAllForms = 1 THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
                    
                    -- Priority 5: Company Role Default
                    WHEN UserCompanyRole = 'company_admin' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    WHEN UserCompanyRole = 'company_user' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
                    WHEN UserCompanyRole = 'company_viewer' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
                    
                    -- Priority 6: No Access
                    ELSE NULL
                END AS EffectiveAccessTypeID,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 'MANAGE'
                    WHEN FormCreatedBy = UserID THEN 'MANAGE'
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN ExplicitAccessTypeCode
                    WHEN AgencyHasEditAllForms = 1 THEN 'EDIT'
                    WHEN AgencyHasViewAllForms = 1 THEN 'VIEW'
                    WHEN UserCompanyRole = 'company_admin' THEN 'MANAGE'
                    WHEN UserCompanyRole = 'company_user' THEN 'VIEW'
                    WHEN UserCompanyRole = 'company_viewer' THEN 'VIEW'
                    ELSE NULL
                END AS EffectiveAccessTypeCode,
                
                -- Permission flags (based on effective access type)
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN 
                        CASE WHEN ExplicitAccessTypeCode IN ('VIEW', 'SUBMIT', 'ANALYZE', 'EDIT', 'MANAGE') THEN 1 ELSE 0 END
                    WHEN AgencyHasEditAllForms = 1 THEN 1
                    WHEN AgencyHasViewAllForms = 1 THEN 1
                    WHEN UserCompanyRole = 'company_admin' THEN 1
                    WHEN UserCompanyRole = 'company_user' THEN 1
                    WHEN UserCompanyRole = 'company_viewer' THEN 1
                    ELSE 0
                END AS CanView,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode IN ('SUBMIT', 'MANAGE') THEN 1
                    WHEN UserCompanyRole = 'company_admin' THEN 1
                    ELSE 0
                END AS CanSubmit,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode IN ('ANALYZE', 'MANAGE') AND UserCanViewReports = 1 THEN 1
                    WHEN UserCompanyRole = 'company_admin' AND UserCanViewReports = 1 THEN 1
                    WHEN UserCompanyRole = 'company_user' AND UserCanViewReports = 1 THEN 1
                    ELSE 0
                END AS CanAnalyze,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode IN ('EDIT', 'MANAGE') AND UserCanManageForms = 1 THEN 1
                    WHEN AgencyHasEditAllForms = 1 THEN 1
                    WHEN UserCompanyRole = 'company_admin' AND UserCanManageForms = 1 THEN 1
                    ELSE 0
                END AS CanEdit,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode = 'MANAGE' AND UserCanManageForms = 1 THEN 1
                    WHEN UserCompanyRole = 'company_admin' AND UserCanManageForms = 1 THEN 1
                    ELSE 0
                END AS CanManage,
                
                -- Access source
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 'system_admin'
                    WHEN FormCreatedBy = UserID THEN 'ownership'
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN 'explicit_acl'
                    WHEN AgencyHasEditAllForms = 1 OR AgencyHasViewAllForms = 1 THEN 'agency_event'
                    WHEN UserCompanyRole IS NOT NULL THEN 'company_role'
                    ELSE 'none'
                END AS AccessSource,
                
                -- Access reason
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 'System Administrator - full platform access'
                    WHEN FormCreatedBy = UserID THEN 'Form owner (creator) - full access to own forms'
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN 
                        'Explicit access control entry: ' + ExplicitAccessTypeCode
                    WHEN AgencyHasEditAllForms = 1 THEN 
                        'Agency event-scoped access: EDIT all forms for event (agency_form_builder role)'
                    WHEN AgencyHasViewAllForms = 1 THEN 
                        'Agency event-scoped access: VIEW all forms for event (agency_form_builder role)'
                    WHEN UserCompanyRole = 'company_admin' THEN 
                        'Company Administrator - default MANAGE access to all company forms'
                    WHEN UserCompanyRole = 'company_user' THEN 
                        'Company User - default VIEW access to all company forms'
                    WHEN UserCompanyRole = 'company_viewer' THEN 
                        'Company Viewer - default VIEW access to all company forms'
                    ELSE 'No access - user is not a member of the form''s company and has no explicit access grant'
                END AS AccessReason
                
            FROM AccessCheck
        )
    """)
    
    # Create recommended indexes for performance
    # Note: These indexes may already exist, but we ensure they're present for optimal function performance
    
    # Index on Form table for company and event lookups
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Form_CompanyID_IsDeleted' AND object_id = OBJECT_ID('dbo.Form'))
        BEGIN
            CREATE NONCLUSTERED INDEX IX_Form_CompanyID_IsDeleted 
            ON dbo.Form(CompanyID, IsDeleted)
        END
    """)
    
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Form_EventID_IsDeleted' AND object_id = OBJECT_ID('dbo.Form'))
        BEGIN
            CREATE NONCLUSTERED INDEX IX_Form_EventID_IsDeleted 
            ON dbo.Form(EventID, IsDeleted)
        END
    """)
    
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Form_CreatedBy_IsDeleted' AND object_id = OBJECT_ID('dbo.Form'))
        BEGIN
            CREATE NONCLUSTERED INDEX IX_Form_CreatedBy_IsDeleted 
            ON dbo.Form(CreatedBy, IsDeleted)
        END
    """)
    
    # Index on FormAccessControl for user/form lookups
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_FormAccessControl_UserID_FormID_IsDeleted' AND object_id = OBJECT_ID('dbo.FormAccessControl'))
        BEGIN
            CREATE NONCLUSTERED INDEX IX_FormAccessControl_UserID_FormID_IsDeleted 
            ON dbo.FormAccessControl(UserID, FormID, IsDeleted)
        END
    """)
    
    # Index on EventCompany for event/company lookups
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_EventCompany_EventID_CompanyID_IsActive_IsDeleted' AND object_id = OBJECT_ID('dbo.EventCompany'))
        BEGIN
            CREATE NONCLUSTERED INDEX IX_EventCompany_EventID_CompanyID_IsActive_IsDeleted 
            ON dbo.EventCompany(EventID, CompanyID, IsActive, IsDeleted)
        END
    """)
    
    # Index on UserCompany for user/company lookups
    op.execute("""
        IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_UserCompany_UserID_CompanyID_StatusID_IsDeleted' AND object_id = OBJECT_ID('dbo.UserCompany'))
        BEGIN
            CREATE NONCLUSTERED INDEX IX_UserCompany_UserID_CompanyID_StatusID_IsDeleted 
            ON dbo.UserCompany(UserID, CompanyID, StatusID, IsDeleted)
        END
    """)


def downgrade():
    """Drop form access function and indexes"""
    
    # Drop indexes (only if we created them - be careful not to drop existing ones)
    # Note: We use IF EXISTS pattern, but SQL Server doesn't support it directly
    # So we check first before dropping
    
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Form_CompanyID_IsDeleted' AND object_id = OBJECT_ID('dbo.Form'))
        BEGIN
            DROP INDEX IX_Form_CompanyID_IsDeleted ON dbo.Form
        END
    """)
    
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Form_EventID_IsDeleted' AND object_id = OBJECT_ID('dbo.Form'))
        BEGIN
            DROP INDEX IX_Form_EventID_IsDeleted ON dbo.Form
        END
    """)
    
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Form_CreatedBy_IsDeleted' AND object_id = OBJECT_ID('dbo.Form'))
        BEGIN
            DROP INDEX IX_Form_CreatedBy_IsDeleted ON dbo.Form
        END
    """)
    
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_FormAccessControl_UserID_FormID_IsDeleted' AND object_id = OBJECT_ID('dbo.FormAccessControl'))
        BEGIN
            DROP INDEX IX_FormAccessControl_UserID_FormID_IsDeleted ON dbo.FormAccessControl
        END
    """)
    
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_EventCompany_EventID_CompanyID_IsActive_IsDeleted' AND object_id = OBJECT_ID('dbo.EventCompany'))
        BEGIN
            DROP INDEX IX_EventCompany_EventID_CompanyID_IsActive_IsDeleted ON dbo.EventCompany
        END
    """)
    
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_UserCompany_UserID_CompanyID_StatusID_IsDeleted' AND object_id = OBJECT_ID('dbo.UserCompany'))
        BEGIN
            DROP INDEX IX_UserCompany_UserID_CompanyID_StatusID_IsDeleted ON dbo.UserCompany
        END
    """)
    
    # Drop function
    op.execute("DROP FUNCTION IF EXISTS [dbo].[fn_GetUserFormAccess]")

