"""upgrade_agency_access_to_manage

Revision ID: 1d6fd98cc9ea
Revises: 96cfcbf141d3
Create Date: 2025-11-21 11:30:31.086395

Story: Epic 2 - Form Access Control Enhancement
Purpose: Upgrade agency form builder access from EDIT to MANAGE access

Changes:
1. Change Priority 4 (Agency Event-Scoped Access) from EDIT to MANAGE access type
2. Add AgencyHasEditAllForms = 1 to CanManage flag
3. Update access reason message to reflect MANAGE access

Rationale:
Agency form builders are hired to BUILD and MANAGE forms, not just edit them.
They need full MANAGE access to:
- Create forms
- Edit forms
- Delete forms
- Grant/revoke access to forms
- Manage form settings

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '1d6fd98cc9ea'
down_revision = '96cfcbf141d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade agency access from EDIT to MANAGE in fn_GetUserFormAccess"""
    
    # Drop and recreate the function with MANAGE access for agency form builders
    op.execute("DROP FUNCTION IF EXISTS [dbo].[fn_GetUserFormAccess]")
    
    # Recreate function with MANAGE access for agency (instead of EDIT)
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
                    -- Check agency event-scoped access (use subquery to find any agency relationship)
                    (SELECT MAX(CAST(ecr_agency.HasViewAllFormsForEvent AS INT)) 
                     FROM dbo.UserCompany uc_agency
                     INNER JOIN ref.UserCompanyStatus ucs_agency ON uc_agency.StatusID = ucs_agency.UserCompanyStatusID 
                         AND ucs_agency.StatusCode = 'active'
                     INNER JOIN dbo.EventCompany ec_agency ON ec_agency.EventID = f.EventID 
                         AND ec_agency.CompanyID = uc_agency.CompanyID 
                         AND ec_agency.IsDeleted = 0 
                         AND ec_agency.IsActive = 1
                     INNER JOIN ref.EventCompanyRole ecr_agency ON ec_agency.EventCompanyRoleID = ecr_agency.EventCompanyRoleID
                     WHERE uc_agency.UserID = @UserID 
                       AND uc_agency.IsDeleted = 0
                    ) AS AgencyHasViewAllForms,
                    (SELECT MAX(CAST(ecr_agency.HasEditAllFormsForEvent AS INT))
                     FROM dbo.UserCompany uc_agency
                     INNER JOIN ref.UserCompanyStatus ucs_agency ON uc_agency.StatusID = ucs_agency.UserCompanyStatusID 
                         AND ucs_agency.StatusCode = 'active'
                     INNER JOIN dbo.EventCompany ec_agency ON ec_agency.EventID = f.EventID 
                         AND ec_agency.CompanyID = uc_agency.CompanyID 
                         AND ec_agency.IsDeleted = 0 
                         AND ec_agency.IsActive = 1
                     INNER JOIN ref.EventCompanyRole ecr_agency ON ec_agency.EventCompanyRoleID = ecr_agency.EventCompanyRoleID
                     WHERE uc_agency.UserID = @UserID 
                       AND uc_agency.IsDeleted = 0
                    ) AS AgencyHasEditAllForms
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
                LEFT JOIN dbo.FormAccessControl fac ON fac.FormID = f.FormID 
                    AND fac.UserID = @UserID 
                    AND fac.IsDeleted = 0
                    AND (fac.ExpiryDate IS NULL OR fac.ExpiryDate > GETUTCDATE())
                LEFT JOIN ref.FormAccessControlAccessType facat ON fac.FormAccessControlAccessTypeID = facat.FormAccessControlAccessTypeID
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
                    
                    -- Priority 4: Agency Event-Scoped Access (UPGRADED: EDIT → MANAGE)
                    WHEN AgencyHasEditAllForms = 1 THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    WHEN AgencyHasViewAllForms = 1 THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
                    
                    -- Priority 5: Company Role Default (company_admin and company_user only - NOT company_viewer)
                    WHEN UserCompanyRole = 'company_admin' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    WHEN UserCompanyRole = 'company_user' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
                    
                    -- Priority 6: No Access (includes company_viewer with no explicit access)
                    ELSE NULL
                END AS EffectiveAccessTypeID,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 'MANAGE'
                    WHEN FormCreatedBy = UserID THEN 'MANAGE'
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN ExplicitAccessTypeCode
                    WHEN AgencyHasEditAllForms = 1 THEN 'MANAGE'
                    WHEN AgencyHasViewAllForms = 1 THEN 'VIEW'
                    WHEN UserCompanyRole = 'company_admin' THEN 'MANAGE'
                    WHEN UserCompanyRole = 'company_user' THEN 'VIEW'
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
                    -- CRITICAL: company_viewer removed - they only get access through explicit grants
                    ELSE 0
                END AS CanView,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode IN ('SUBMIT', 'MANAGE') THEN 1
                    WHEN AgencyHasEditAllForms = 1 THEN 1
                    WHEN UserCompanyRole = 'company_admin' THEN 1
                    ELSE 0
                END AS CanSubmit,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode IN ('ANALYZE', 'MANAGE') AND UserCanViewReports = 1 THEN 1
                    WHEN AgencyHasEditAllForms = 1 AND UserCanViewReports = 1 THEN 1
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
                    WHEN AgencyHasEditAllForms = 1 THEN 1
                    WHEN UserCompanyRole = 'company_admin' AND UserCanManageForms = 1 THEN 1
                    ELSE 0
                END AS CanManage,
                
                -- Access source
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 'system_admin'
                    WHEN FormCreatedBy = UserID THEN 'ownership'
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN 'explicit_acl'
                    WHEN AgencyHasEditAllForms = 1 OR AgencyHasViewAllForms = 1 THEN 'agency_event'
                    WHEN UserCompanyRole = 'company_admin' THEN 'company_role'
                    WHEN UserCompanyRole = 'company_user' THEN 'company_role'
                    -- company_viewer with no explicit access falls through to 'none'
                    ELSE 'none'
                END AS AccessSource,
                
                -- Access reason
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 'System Administrator - full platform access'
                    WHEN FormCreatedBy = UserID THEN 'Form owner (creator) - full access to own forms'
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN 
                        'Explicit access control entry: ' + ExplicitAccessTypeCode
                    WHEN AgencyHasEditAllForms = 1 THEN 
                        'Agency event-scoped access: MANAGE all forms for event (agency_form_builder role)'
                    WHEN AgencyHasViewAllForms = 1 THEN 
                        'Agency event-scoped access: VIEW all forms for event (agency_form_builder role)'
                    WHEN UserCompanyRole = 'company_admin' THEN 
                        'Company Administrator - default MANAGE access to all company forms'
                    WHEN UserCompanyRole = 'company_user' THEN 
                        'Company User - default VIEW access to all company forms'
                    -- CRITICAL: company_viewer with no explicit access gets no access
                    ELSE 'No access - user is not a member of the form''s company and has no explicit access grant'
                END AS AccessReason
                
            FROM AccessCheck
        )
    """)


def downgrade() -> None:
    """Downgrade agency access back to EDIT (revert to previous version)"""
    
    # Drop function
    op.execute("DROP FUNCTION IF EXISTS [dbo].[fn_GetUserFormAccess]")
    
    # Recreate function with EDIT access for agency (previous version)
    # This is the same as migration 96cfcbf141d3 but with EDIT instead of MANAGE
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
                    f.CompanyID AS FormCompanyID,
                    f.EventID AS FormEventID,
                    f.CreatedBy AS FormCreatedBy,
                    ur.RoleCode AS UserSystemRole,
                    ucr.RoleCode AS UserCompanyRole,
                    ucr.CanManageForms AS UserCanManageForms,
                    ucr.CanViewReports AS UserCanViewReports,
                    fac.FormAccessControlAccessTypeID AS ExplicitAccessTypeID,
                    facat.AccessTypeCode AS ExplicitAccessTypeCode,
                    ecr.HasViewAllFormsForEvent AS AgencyHasViewAllForms,
                    ecr.HasEditAllFormsForEvent AS AgencyHasEditAllForms,
                    ec.CompanyID AS AgencyCompanyID
                FROM dbo.Form f
                LEFT JOIN [dbo].[User] u ON u.UserID = @UserID AND u.IsDeleted = 0
                LEFT JOIN ref.UserRole ur ON u.UserRoleID = ur.UserRoleID
                LEFT JOIN dbo.UserCompany uc ON uc.UserID = @UserID 
                    AND uc.CompanyID = f.CompanyID 
                    AND uc.IsDeleted = 0
                LEFT JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID 
                    AND ucs.StatusCode = 'active'
                LEFT JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
                LEFT JOIN dbo.FormAccessControl fac ON fac.FormID = f.FormID 
                    AND fac.UserID = @UserID 
                    AND fac.IsDeleted = 0
                    AND (fac.ExpiryDate IS NULL OR fac.ExpiryDate > GETUTCDATE())
                LEFT JOIN ref.FormAccessControlAccessType facat ON fac.FormAccessControlAccessTypeID = facat.FormAccessControlAccessTypeID
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
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    WHEN FormCreatedBy = UserID THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    WHEN ExplicitAccessTypeID IS NOT NULL THEN
                        ExplicitAccessTypeID
                    WHEN AgencyHasEditAllForms = 1 THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'EDIT')
                    WHEN AgencyHasViewAllForms = 1 THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
                    WHEN UserCompanyRole = 'company_admin' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
                    WHEN UserCompanyRole = 'company_user' THEN
                        (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
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
                    ELSE NULL
                END AS EffectiveAccessTypeCode,
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 1
                    WHEN FormCreatedBy = UserID THEN 1
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN 
                        CASE WHEN ExplicitAccessTypeCode IN ('VIEW', 'SUBMIT', 'ANALYZE', 'EDIT', 'MANAGE') THEN 1 ELSE 0 END
                    WHEN AgencyHasEditAllForms = 1 THEN 1
                    WHEN AgencyHasViewAllForms = 1 THEN 1
                    WHEN UserCompanyRole = 'company_admin' THEN 1
                    WHEN UserCompanyRole = 'company_user' THEN 1
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
                
                CASE
                    WHEN UserSystemRole = 'system_admin' THEN 'system_admin'
                    WHEN FormCreatedBy = UserID THEN 'ownership'
                    WHEN ExplicitAccessTypeCode IS NOT NULL THEN 'explicit_acl'
                    WHEN AgencyHasEditAllForms = 1 OR AgencyHasViewAllForms = 1 THEN 'agency_event'
                    WHEN UserCompanyRole = 'company_admin' THEN 'company_role'
                    WHEN UserCompanyRole = 'company_user' THEN 'company_role'
                    ELSE 'none'
                END AS AccessSource,
                
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
                    ELSE 'No access - user is not a member of the form''s company and has no explicit access grant'
                END AS AccessReason
                
            FROM AccessCheck
        )
    """)