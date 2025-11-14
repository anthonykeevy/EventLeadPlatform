-- =====================================================================
-- Assign System Admin Role to User
-- =====================================================================
-- Purpose: Helper script to assign system_admin role to existing users
-- Usage: 
--   1. Check existing users (Query 1)
--   2. Check which users are system admins (Query 2)
--   3. Assign system_admin role (Query 3) - Replace the email/UserID
--   4. Verify the assignment (Query 4)
-- =====================================================================

-- =====================================================================
-- QUERY 1: Check all users and their current roles
-- =====================================================================
SELECT 
    u.UserID,
    u.Email,
    u.FirstName,
    u.LastName,
    u.UserRoleID,
    ur.RoleCode AS SystemRoleCode,
    ur.RoleName AS SystemRoleName,
    u.CompanyID,
    u.IsDeleted,
    u.CreatedDate
FROM [User] u
LEFT JOIN [ref].[UserRole] ur ON u.UserRoleID = ur.UserRoleID
ORDER BY u.UserID;
GO

-- =====================================================================
-- QUERY 2: Check which users currently have system_admin role
-- =====================================================================
SELECT 
    u.UserID,
    u.Email,
    u.FirstName,
    u.LastName,
    ur.RoleCode,
    ur.RoleName
FROM [User] u
INNER JOIN [ref].[UserRole] ur ON u.UserRoleID = ur.UserRoleID
WHERE ur.RoleCode = 'system_admin'
    AND u.IsDeleted = 0;
GO

-- =====================================================================
-- QUERY 3: Assign system_admin role to a user by EMAIL
-- =====================================================================
-- Replace 'your-email@example.com' with the actual user's email
-- =====================================================================
DECLARE @UserEmail NVARCHAR(255) = 'your-email@example.com';  -- CHANGE THIS

UPDATE [User]
SET 
    UserRoleID = 1,  -- system_admin role ID
    UpdatedDate = GETUTCDATE(),
    UpdatedBy = (SELECT UserID FROM [User] WHERE Email = @UserEmail AND IsDeleted = 0)
WHERE Email = @UserEmail 
    AND IsDeleted = 0;

IF @@ROWCOUNT > 0
    PRINT 'SUCCESS: System admin role assigned to user: ' + @UserEmail;
ELSE
    PRINT 'ERROR: User not found or already deleted: ' + @UserEmail;
GO

-- =====================================================================
-- QUERY 4: Assign system_admin role to a user by UserID
-- =====================================================================
-- Replace 1 with the actual UserID
-- =====================================================================
DECLARE @UserID BIGINT = 1;  -- CHANGE THIS to the target user's UserID

UPDATE [User]
SET 
    UserRoleID = 1,  -- system_admin role ID
    UpdatedDate = GETUTCDATE(),
    UpdatedBy = @UserID  -- Self-assignment (or set to admin UserID if different)
WHERE UserID = @UserID 
    AND IsDeleted = 0;

IF @@ROWCOUNT > 0
    PRINT 'SUCCESS: System admin role assigned to UserID: ' + CAST(@UserID AS NVARCHAR(10));
ELSE
    PRINT 'ERROR: User not found or already deleted: UserID ' + CAST(@UserID AS NVARCHAR(10));
GO

-- =====================================================================
-- QUERY 5: Verify role assignment worked
-- =====================================================================
-- Run this after Query 3 or 4 to verify the role was assigned
-- =====================================================================
DECLARE @UserEmail NVARCHAR(255) = 'your-email@example.com';  -- CHANGE THIS

SELECT 
    u.UserID,
    u.Email,
    u.FirstName,
    u.LastName,
    u.UserRoleID,
    ur.RoleCode,
    ur.RoleName,
    ur.Description,
    u.UpdatedDate,
    u.UpdatedBy
FROM [User] u
LEFT JOIN [ref].[UserRole] ur ON u.UserRoleID = ur.UserRoleID
WHERE u.Email = @UserEmail 
    AND u.IsDeleted = 0;
GO

-- =====================================================================
-- QUERY 6: Remove system_admin role (set back to NULL)
-- =====================================================================
-- Use this if you need to remove the system_admin role from a user
-- =====================================================================
DECLARE @UserEmail NVARCHAR(255) = 'your-email@example.com';  -- CHANGE THIS

UPDATE [User]
SET 
    UserRoleID = NULL,
    UpdatedDate = GETUTCDATE(),
    UpdatedBy = (SELECT UserID FROM [User] WHERE UserRoleID = 1 AND IsDeleted = 0)  -- Set by existing system admin
WHERE Email = @UserEmail 
    AND IsDeleted = 0;

IF @@ROWCOUNT > 0
    PRINT 'SUCCESS: System admin role removed from user: ' + @UserEmail;
ELSE
    PRINT 'ERROR: User not found or already deleted: ' + @UserEmail;
GO

-- =====================================================================
-- NOTES:
-- =====================================================================
-- 1. UserRoleID = 1 corresponds to 'system_admin' role
-- 2. UserRoleID = NULL means the user is NOT a system admin
-- 3. The audit trail will automatically log this change in the AuditRole table
-- 4. After assigning the role, the user needs to log out and log back in
--    for the JWT token to reflect the new role
-- =====================================================================
