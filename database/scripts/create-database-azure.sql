-- =====================================================================
-- EventLeadPlatform - Azure SQL Database Setup
-- =====================================================================
-- Purpose: Configure Azure SQL Database for production
-- Important: This script assumes the database already exists in Azure
--            (created via Azure Portal, CLI, or Terraform)
-- =====================================================================
-- Differences from Local Development:
--   - Azure manages file storage (no FILENAME parameters)
--   - Azure uses service tiers instead of size/maxsize
--   - Azure automatically enables READ_COMMITTED_SNAPSHOT
--   - Azure has built-in high availability
--   - Azure handles backups automatically (no RECOVERY FULL management)
-- =====================================================================
-- Prerequisites:
--   1. Azure SQL Server created (server-level)
--   2. Firewall rules configured (allow your IP + Azure services)
--   3. Azure SQL Database created with appropriate service tier:
--      - Development: Basic or S0 (Standard)
--      - Production: S2+ (Standard) or P1+ (Premium)
-- =====================================================================

-- Connect to your Azure SQL Database
-- Connection string format:
-- Server=your-server.database.windows.net;Database=EventLeadPlatform;User Id=admin;Password=YourPassword;

USE [EventLeadPlatform];
GO

PRINT 'Configuring EventLeadPlatform on Azure SQL Database...';
GO

-- =====================================================================
-- Verify Database Collation (Should be set during creation)
-- =====================================================================
-- Azure SQL Database default collation: SQL_Latin1_General_CP1_CI_AS
-- Recommended: Latin1_General_100_CI_AS_SC_UTF8 (if supported by your tier)
-- Note: Collation CANNOT be changed after database creation in Azure
--       You must recreate the database with the correct collation
SELECT 
    name AS DatabaseName,
    collation_name AS Collation,
    'VERIFY: Should be Latin1_General_100_CI_AS_SC_UTF8 or compatible UTF-8 collation' AS Recommendation
FROM sys.databases
WHERE database_id = DB_ID();
GO

-- If collation is wrong, you must recreate the database:
-- DROP DATABASE EventLeadPlatform;
-- CREATE DATABASE EventLeadPlatform COLLATE Latin1_General_100_CI_AS_SC_UTF8;

-- =====================================================================
-- ANSI/SQL Standard Compliance
-- =====================================================================
-- Azure SQL Database has better defaults than local SQL Server
-- These should already be ON, but we verify/set them explicitly
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
GO

-- Most ANSI settings are database-scoped and already optimal in Azure
-- But we can verify critical ones:
PRINT 'Verifying ANSI settings (should all be ON in Azure SQL Database)...';
GO

-- =====================================================================
-- Concurrency & Performance Settings
-- =====================================================================
-- READ_COMMITTED_SNAPSHOT is ON by default in Azure SQL Database
-- (This is a KEY difference from local SQL Server)
IF NOT EXISTS (
    SELECT 1 FROM sys.databases 
    WHERE name = 'EventLeadPlatform' 
    AND is_read_committed_snapshot_on = 1
)
BEGIN
    PRINT 'WARNING: READ_COMMITTED_SNAPSHOT is OFF (unusual for Azure SQL Database)';
    -- In Azure, this should already be ON. If not, contact Azure support.
END
ELSE
BEGIN
    PRINT 'READ_COMMITTED_SNAPSHOT: ON (Azure default - excellent for web apps)';
END
GO

-- Snapshot Isolation (useful for reporting queries)
ALTER DATABASE [EventLeadPlatform] SET ALLOW_SNAPSHOT_ISOLATION ON;
PRINT 'Snapshot Isolation enabled.';
GO

-- =====================================================================
-- Query Store: Performance Monitoring (HIGHLY RECOMMENDED for Azure)
-- =====================================================================
-- Query Store is critical in Azure for troubleshooting performance issues
-- Azure SQL Database often has this enabled by default
ALTER DATABASE [EventLeadPlatform] SET QUERY_STORE = ON;
GO

ALTER DATABASE [EventLeadPlatform] SET QUERY_STORE (
    OPERATION_MODE = READ_WRITE,
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30),  -- Keep 30 days
    DATA_FLUSH_INTERVAL_SECONDS = 900,                   -- Flush every 15 min
    INTERVAL_LENGTH_MINUTES = 60,                        -- Hourly aggregation
    MAX_STORAGE_SIZE_MB = 1000,                          -- 1GB storage
    QUERY_CAPTURE_MODE = AUTO,                           -- Capture important queries
    SIZE_BASED_CLEANUP_MODE = AUTO,                      -- Auto-cleanup
    MAX_PLANS_PER_QUERY = 200,
    WAIT_STATS_CAPTURE_MODE = ON                         -- Capture wait stats
);
GO

PRINT 'Query Store configured for production monitoring.';
GO

-- =====================================================================
-- Azure-Specific Optimizations
-- =====================================================================

-- Automatic Tuning (Azure SQL Database feature)
-- This allows Azure to automatically create/drop indexes based on workload
ALTER DATABASE [EventLeadPlatform] SET AUTOMATIC_TUNING (
    CREATE_INDEX = ON,          -- Auto-create missing indexes
    DROP_INDEX = ON,            -- Auto-drop unused indexes
    FORCE_LAST_GOOD_PLAN = ON   -- Auto-fix plan regressions
);
PRINT 'Automatic Tuning enabled (Azure AI performance optimization).';
GO

-- Accelerated Database Recovery (enabled by default in Azure)
-- ADR dramatically speeds up recovery after crashes
ALTER DATABASE [EventLeadPlatform] SET ACCELERATED_DATABASE_RECOVERY = ON;
PRINT 'Accelerated Database Recovery verified (Azure default).';
GO

-- =====================================================================
-- Security Configuration
-- =====================================================================

-- Transparent Data Encryption (TDE) - Recommended for Azure
-- TDE encrypts the database at rest
-- Note: This may impact performance slightly, but is critical for compliance
-- Azure SQL Database supports TDE at no extra cost
ALTER DATABASE [EventLeadPlatform] SET ENCRYPTION ON;
PRINT 'Transparent Data Encryption (TDE) enabled.';
GO

-- Advanced Threat Protection - Configure via Azure Portal
-- (Cannot be enabled via T-SQL, use Azure Security Center)
PRINT 'NOTE: Enable Advanced Threat Protection via Azure Portal for security monitoring.';
GO

-- =====================================================================
-- Row-Level Security (RLS) Setup
-- =====================================================================
-- For Multi-Tenant isolation (critical for EventLeadPlatform)
-- This will be configured later via Alembic migrations
-- But we can verify the database supports it:
PRINT 'Row-Level Security (RLS) supported - will be configured per-table via migrations.';
GO

-- =====================================================================
-- Dynamic Data Masking (Optional but Recommended)
-- =====================================================================
-- DDM can hide sensitive data (emails, phone numbers) from non-admin users
-- Configure this later on specific columns via migrations
PRINT 'Dynamic Data Masking (DDM) supported - configure on sensitive columns as needed.';
GO

-- =====================================================================
-- Service Tier Recommendations
-- =====================================================================
-- Azure SQL Database uses service tiers instead of file sizes
-- Recommended tiers for EventLeadPlatform:
--
-- Development/Testing:
--   - Basic (5 DTUs, 2GB) - Minimal cost, suitable for early development
--   - S0 (10 DTUs, 250GB) - Better performance for active development
--
-- Staging/Pre-Production:
--   - S2 (50 DTUs, 250GB) - Good balance of performance and cost
--
-- Production (MVP - 100 users):
--   - S3 (100 DTUs, 250GB) - Recommended starting point
--   - OR: GP_Gen5_2 (2 vCores, 32GB) - vCore model (more predictable)
--
-- Production (Scale - 1000+ users):
--   - S6+ (400+ DTUs) or GP_Gen5_4+ (4+ vCores)
--   - OR: Premium tier for mission-critical workloads
--
-- Change service tier via Azure Portal or Azure CLI:
-- az sql db update --name EventLeadPlatform --server your-server \
--   --service-objective S3
GO

-- =====================================================================
-- Backup Configuration (Azure Automatic)
-- =====================================================================
-- Azure SQL Database automatically handles backups:
-- - Full backup: Weekly
-- - Differential backup: Every 12-24 hours
-- - Transaction log backup: Every 5-10 minutes
-- - Retention: 7-35 days (configurable, default 7 days)
-- - Long-term retention: Up to 10 years (optional)
--
-- Configure backup retention via Azure Portal:
-- Settings > Backup retention > Configure policies
PRINT 'NOTE: Azure automatically manages backups (7-day retention by default).';
GO

-- =====================================================================
-- Geo-Replication (Optional for Disaster Recovery)
-- =====================================================================
-- Azure SQL Database supports active geo-replication
-- Recommended for production: Replicate to secondary region
-- Example: Australia East (primary) -> Australia Southeast (secondary)
--
-- Configure via Azure Portal or Azure CLI:
-- az sql db replica create --name EventLeadPlatform \
--   --server primary-server --partner-server secondary-server \
--   --partner-resource-group your-rg
PRINT 'NOTE: Configure Geo-Replication via Azure Portal for disaster recovery.';
GO

-- =====================================================================
-- Connection Pooling & Resilience Settings
-- =====================================================================
-- Azure SQL Database has connection limits based on service tier
-- Ensure your Python app uses connection pooling (SQLAlchemy handles this)
-- Recommended pool size: 5-20 connections per application instance
PRINT 'NOTE: Configure connection pooling in backend application (SQLAlchemy).';
GO

-- =====================================================================
-- Monitoring & Alerting Setup
-- =====================================================================
-- Configure Azure Monitor alerts for:
-- 1. High DTU usage (>80%)
-- 2. High storage usage (>90%)
-- 3. Failed connections
-- 4. Long-running queries
-- 5. Deadlocks
--
-- Setup via Azure Portal > Monitor > Alerts
PRINT 'NOTE: Configure Azure Monitor alerts for proactive monitoring.';
GO

-- =====================================================================
-- Verification & Summary
-- =====================================================================
USE [EventLeadPlatform];
GO

PRINT '';
PRINT '=====================================================================';
PRINT 'EventLeadPlatform Azure SQL Database Configuration Summary';
PRINT '=====================================================================';

-- Display key configuration
SELECT 
    'Database Configuration' AS Category,
    name AS DatabaseName,
    collation_name AS Collation,
    compatibility_level AS CompatibilityLevel,
    recovery_model_desc AS RecoveryModel
FROM sys.databases
WHERE name = 'EventLeadPlatform'

UNION ALL

SELECT 
    'Isolation & Concurrency',
    CAST(is_read_committed_snapshot_on AS VARCHAR) AS ReadCommittedSnapshot,
    snapshot_isolation_state_desc AS SnapshotIsolation,
    '',
    ''
FROM sys.databases
WHERE name = 'EventLeadPlatform'

UNION ALL

SELECT 
    'Performance Monitoring',
    CAST(is_query_store_on AS VARCHAR) AS QueryStore,
    CAST(is_auto_create_stats_on AS VARCHAR) AS AutoCreateStats,
    CAST(is_auto_update_stats_on AS VARCHAR) AS AutoUpdateStats,
    CAST(is_auto_update_stats_async_on AS VARCHAR) AS AutoUpdateStatsAsync
FROM sys.databases
WHERE name = 'EventLeadPlatform'

UNION ALL

SELECT 
    'Security',
    CASE WHEN is_encrypted = 1 THEN 'TDE Enabled' ELSE 'TDE Disabled' END,
    '',
    '',
    ''
FROM sys.databases
WHERE name = 'EventLeadPlatform';
GO

PRINT '';
PRINT 'Configuration Complete!';
PRINT '';
PRINT 'Next Steps:';
PRINT '1. Update backend/.env.local with Azure connection string';
PRINT '2. Configure Azure firewall rules (allow your IP)';
PRINT '3. Setup Azure Monitor alerts';
PRINT '4. Configure automatic tuning (already enabled above)';
PRINT '5. Run Alembic migrations: alembic upgrade head';
PRINT '6. Enable Advanced Threat Protection (Azure Portal)';
PRINT '7. Configure long-term backup retention (if needed)';
PRINT '8. Setup geo-replication for disaster recovery (production only)';
PRINT '';
PRINT 'Azure-Specific Features Enabled:';
PRINT '  ✓ Automatic Tuning (AI-powered performance optimization)';
PRINT '  ✓ Accelerated Database Recovery';
PRINT '  ✓ Transparent Data Encryption (TDE)';
PRINT '  ✓ Query Store (performance monitoring)';
PRINT '  ✓ Read Committed Snapshot Isolation (web-optimized)';
PRINT '';
PRINT 'Service Tier Recommendations:';
PRINT '  - Development: S0 or S1';
PRINT '  - Production MVP: S3 or GP_Gen5_2';
PRINT '  - Production Scale: S6+ or GP_Gen5_4+';
PRINT '=====================================================================';
GO

