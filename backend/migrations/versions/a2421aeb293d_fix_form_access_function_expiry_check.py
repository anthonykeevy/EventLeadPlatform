"""fix_form_access_function_expiry_check

Revision ID: a2421aeb293d
Revises: 026_form_access_function
Create Date: 2025-11-20 16:30:07.150172

Story: Epic 2 - Form Access Control Bug Fix
Purpose: Fix expiry date check in fn_GetUserFormAccess to exclude expired access entries

Changes:
1. Alter fn_GetUserFormAccess to add expiry date check to FormAccessControl JOIN
2. This ensures expired access grants are not included in access checks

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a2421aeb293d'
down_revision = '026_form_access_function'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add expiry date check to FormAccessControl JOIN in fn_GetUserFormAccess"""
    
    # Drop and recreate the function with expiry check added
    # SQL Server doesn't support ALTER FUNCTION for table-valued functions with significant changes
    op.execute("DROP FUNCTION IF EXISTS [dbo].[fn_GetUserFormAccess]")
    
    # Recreate function with expiry check in JOIN condition
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
                    -- Check explicit FormAccessControl (exclude expired entries)
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
                -- Check explicit FormAccessControl (exclude expired entries)
                -- CRITICAL FIX: Added expiry date check to JOIN condition
                LEFT JOIN dbo.FormAccessControl fac ON fac.FormID = f.FormID 
                    AND fac.UserID = @UserID 
                    AND fac.IsDeleted = 0
                    AND (fac.ExpiryDate IS NULL OR fac.ExpiryDate > GETUTCDATE())
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
                    
                    -- Priority 3: Explicit FormAccessControl (only if not expired - handled in JOIN)
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


def downgrade() -> None:
    """Revert expiry check fix - recreate function without expiry check in JOIN"""
    
    # Drop function
    op.execute("DROP FUNCTION IF EXISTS [dbo].[fn_GetUserFormAccess]")
    
    # Recreate function without expiry check (original version)
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
                    -- Check explicit FormAccessControl (without expiry check - reverted)
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
                -- Check explicit FormAccessControl (without expiry check)
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
