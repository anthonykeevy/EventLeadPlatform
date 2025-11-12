-- Update excluded endpoints to NOT include industries
-- This allows payload capture for debugging industry API calls
UPDATE [config].[AppSetting]
SET SettingValue = '["/api/health", "/api/test-database"]'
WHERE SettingKey = 'logging.excluded_endpoints';

-- Verify the update
SELECT SettingKey, SettingValue 
FROM [config].[AppSetting] 
WHERE SettingKey = 'logging.excluded_endpoints';

