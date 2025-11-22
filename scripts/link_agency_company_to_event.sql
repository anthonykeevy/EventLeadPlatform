-- =====================================================================
-- Script to Link Agency Company to Event with agency_form_builder Role
-- =====================================================================
-- Purpose: Test Script 11.1 - Link Agency Company to Event
-- 
-- Usage:
-- 1. Replace the variables below with your actual values
-- 2. Run this script in SQL Server Management Studio or Azure Data Studio
-- 3. Verify the EventCompany relationship was created
--
-- Variables:
--   @EventID: The ID of the event to link the agency to
--   @AgencyCompanyID: The ID of the agency company
--   @HostCompanyID: The ID of the host company (owner of the event)
--   @CreatedByUserID: The ID of the user creating this relationship (usually host company admin)
-- =====================================================================

-- DECLARE VARIABLES - UPDATED WITH TEST DATA VALUES FROM LOGS
-- Event: Australian Marketeers Expo (created 2025-11-20 23:14:55)
-- Agency Company: Event On & On (Test3@test.com's original company)
-- Host Company: THE TRUSTEE FOR YOG RITU PARESH BHAMBANI FAMILY TRUST (Test4@test.com's company)
-- Note: Test3@test.com (UserID 80) was invited to CompanyID 1030 as Company Viewer on 2025-11-20 23:23:00
--       Test4@test.com (UserID 107) created Event 29 and Form 9 ("Brand A")
DECLARE @EventID BIGINT = 29;             -- Australian Marketeers Expo (confirmed from logs)
DECLARE @AgencyCompanyID BIGINT = 1029;   -- Event On & On (Test3's original company)
DECLARE @HostCompanyID BIGINT = 1030;     -- THE TRUSTEE FOR YOG RITU PARESH BHAMBANI FAMILY TRUST (Test4's company - confirmed from logs)
DECLARE @CreatedByUserID BIGINT = 107;    -- Test4@test.com (host company admin - confirmed from logs: UserID 107, Email Test4@test.com)

-- =====================================================================
-- VALIDATION CHECKS
-- =====================================================================

-- 1. Verify event exists and is owned by host company
IF NOT EXISTS (
    SELECT 1 
    FROM dbo.Event 
    WHERE EventID = @EventID 
      AND CompanyID = @HostCompanyID 
      AND IsDeleted = 0
)
BEGIN
    RAISERROR('Error: Event with ID %d not found or not owned by company %d', 16, 1, @EventID, @HostCompanyID);
    RETURN;
END

-- 2. Verify agency company exists
IF NOT EXISTS (
    SELECT 1 
    FROM dbo.Company 
    WHERE CompanyID = @AgencyCompanyID 
      AND IsDeleted = 0
)
BEGIN
    RAISERROR('Error: Agency company with ID %d not found', 16, 1, @AgencyCompanyID);
    RETURN;
END

-- 3. Verify agency_form_builder role exists
DECLARE @AgencyRoleID BIGINT;
SELECT @AgencyRoleID = EventCompanyRoleID
FROM ref.EventCompanyRole
WHERE RoleCode = 'agency_form_builder'
  AND IsActive = 1;

IF @AgencyRoleID IS NULL
BEGIN
    RAISERROR('Error: agency_form_builder role not found or not active. Please ensure migration 024 has been run.', 16, 1);
    RETURN;
END

-- 4. Check if relationship already exists
IF EXISTS (
    SELECT 1 
    FROM dbo.EventCompany 
    WHERE EventID = @EventID 
      AND CompanyID = @AgencyCompanyID 
      AND IsActive = 1 
      AND IsDeleted = 0
)
BEGIN
    PRINT 'Warning: Active EventCompany relationship already exists. Updating to agency_form_builder role...';
    
    -- Update existing relationship to agency_form_builder role
    UPDATE dbo.EventCompany
    SET EventCompanyRoleID = @AgencyRoleID,
        UpdatedDate = GETUTCDATE(),
        UpdatedBy = @CreatedByUserID
    WHERE EventID = @EventID 
      AND CompanyID = @AgencyCompanyID 
      AND IsActive = 1 
      AND IsDeleted = 0;
    
    PRINT 'Success: EventCompany relationship updated to agency_form_builder role.';
    RETURN;
END

-- =====================================================================
-- CREATE EVENTCOMPANY RELATIONSHIP
-- =====================================================================

INSERT INTO dbo.EventCompany (
    EventID,
    CompanyID,
    EventCompanyRoleID,
    IsActive,
    CreatedBy,
    CreatedDate,
    UpdatedDate,
    UpdatedBy,
    IsDeleted
)
VALUES (
    @EventID,
    @AgencyCompanyID,
    @AgencyRoleID,
    1,  -- IsActive
    @CreatedByUserID,
    GETUTCDATE(),
    GETUTCDATE(),
    @CreatedByUserID,
    0   -- IsDeleted
);

DECLARE @NewEventCompanyID BIGINT = SCOPE_IDENTITY();

-- =====================================================================
-- VERIFICATION
-- =====================================================================

PRINT '=====================================================================';
PRINT 'SUCCESS: Agency Company linked to Event';
PRINT '=====================================================================';
PRINT 'EventCompanyID: ' + CAST(@NewEventCompanyID AS VARCHAR(20));
PRINT 'EventID: ' + CAST(@EventID AS VARCHAR(20));
PRINT 'AgencyCompanyID: ' + CAST(@AgencyCompanyID AS VARCHAR(20));
PRINT 'Role: agency_form_builder';
PRINT 'IsActive: 1';
PRINT '=====================================================================';

-- Display the created relationship
SELECT 
    ec.EventCompanyID,
    ec.EventID,
    e.Name AS EventName,
    ec.CompanyID AS AgencyCompanyID,
    c.CompanyName AS AgencyCompanyName,
    ecr.RoleCode,
    ecr.RoleName,
    ec.IsActive,
    ec.CreatedDate,
    u.Email AS CreatedByEmail
FROM dbo.EventCompany ec
INNER JOIN dbo.Event e ON ec.EventID = e.EventID
INNER JOIN dbo.Company c ON ec.CompanyID = c.CompanyID
INNER JOIN ref.EventCompanyRole ecr ON ec.EventCompanyRoleID = ecr.EventCompanyRoleID
LEFT JOIN dbo.[User] u ON ec.CreatedBy = u.UserID
WHERE ec.EventCompanyID = @NewEventCompanyID;

PRINT '';
PRINT 'Next Steps:';
PRINT '1. Log in as a user from the agency company';
PRINT '2. Verify the event appears in the agency user''s dashboard';
PRINT '3. Verify the agency user can view and edit all forms for this event';
PRINT '4. Verify the agency user CANNOT see the host company or other events';
PRINT '=====================================================================';

