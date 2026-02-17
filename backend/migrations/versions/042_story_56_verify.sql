-- Story 5.6: Verification queries
-- Run these to check if migration 042 was applied.

-- 1. Check alembic current revision
SELECT version_num FROM [dbo].[alembic_version];

-- 2. Check if RequirePublishApproval exists on CompanyFormTestConfig
SELECT c.name AS column_name, t.name AS type_name
FROM sys.columns c
INNER JOIN sys.tables t ON c.object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
INNER JOIN sys.types ty ON c.user_type_id = ty.user_type_id
WHERE s.name = 'dbo' AND t.name = 'CompanyFormTestConfig'
ORDER BY c.column_id;

-- 3. Check if FormPublishRequest table exists
SELECT s.name AS schema_name, t.name AS table_name
FROM sys.tables t
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE t.name = 'FormPublishRequest';

-- 4. Check if PENDING_REVIEW exists in ref.FormStatus
SELECT * FROM [ref].[FormStatus] WHERE StatusCode = N'PENDING_REVIEW';
