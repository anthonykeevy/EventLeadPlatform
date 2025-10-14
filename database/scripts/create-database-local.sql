-- =====================================================================
-- EventLeadPlatform - Local Development Database Setup
-- =====================================================================
-- Purpose: Create database optimized for local development
-- Features:
--   - International/multi-language support (UTF-8 collation)
--   - SQLAlchemy-compatible settings (ANSI standards ON)
--   - Optimized for web application concurrency
--   - Simplified recovery model for development
--   - Query Store enabled for performance monitoring
-- =====================================================================
-- Prerequisites:
--   - SQL Server 2019+ (for UTF-8 support)
--   - Run as sysadmin or dbcreator role
-- =====================================================================

USE [master]
GO

-- Drop existing database if exists (CAUTION: Data loss!)
IF EXISTS (SELECT name FROM sys.databases WHERE name = N'EventLeadPlatform')
BEGIN
    ALTER DATABASE [EventLeadPlatform] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE [EventLeadPlatform];
    PRINT 'Existing EventLeadPlatform database dropped.';
END
GO

-- =====================================================================
-- CREATE DATABASE with International Support
-- =====================================================================
CREATE DATABASE [EventLeadPlatform]
 CONTAINMENT = NONE
 ON PRIMARY 
( 
    NAME = N'EventLeadPlatform',
    -- Use default SQL Server data directory (portable across machines)
    FILENAME = N'EventLeadPlatform.mdf',
    SIZE = 512MB,           -- Initial size (reasonable for development)
    MAXSIZE = UNLIMITED,    -- No size limit
    FILEGROWTH = 256MB      -- Auto-grow in 256MB chunks
)
LOG ON 
( 
    NAME = N'EventLeadPlatform_log',
    -- Use default SQL Server log directory
    FILENAME = N'EventLeadPlatform_log.ldf',
    SIZE = 256MB,           -- Initial log size
    MAXSIZE = 10GB,         -- Limit log size for development (prevent runaway growth)
    FILEGROWTH = 128MB      -- Log growth in 128MB chunks
)
WITH 
    CATALOG_COLLATION = DATABASE_DEFAULT,
    LEDGER = OFF
GO

-- =====================================================================
-- Set Database Collation (CRITICAL for International Support)
-- =====================================================================
-- Note: Collation must be set during database creation or via ALTER DATABASE
-- For UTF-8 support in SQL Server 2019+:
ALTER DATABASE [EventLeadPlatform] 
    COLLATE Latin1_General_100_CI_AS_SC_UTF8;
GO

PRINT 'Database created with UTF-8 collation for international support.';
GO

-- =====================================================================
-- Enable Full-Text Search (for future search features)
-- =====================================================================
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
BEGIN
    EXEC [EventLeadPlatform].[dbo].[sp_fulltext_database] @action = 'enable';
    PRINT 'Full-text search enabled.';
END
GO

-- =====================================================================
-- ANSI/SQL Standard Compliance (REQUIRED for SQLAlchemy)
-- =====================================================================
-- These settings ensure compatibility with Python SQLAlchemy ORM
ALTER DATABASE [EventLeadPlatform] SET ANSI_NULL_DEFAULT ON;      -- NULL handling
ALTER DATABASE [EventLeadPlatform] SET ANSI_NULLS ON;             -- NULL = NULL is FALSE (SQL standard)
ALTER DATABASE [EventLeadPlatform] SET ANSI_PADDING ON;           -- Preserve trailing spaces
ALTER DATABASE [EventLeadPlatform] SET ANSI_WARNINGS ON;          -- Warn on data truncation
ALTER DATABASE [EventLeadPlatform] SET ARITHABORT ON;             -- Stop query on overflow
ALTER DATABASE [EventLeadPlatform] SET QUOTED_IDENTIFIER ON;      -- Allow quoted identifiers (SQLAlchemy uses this)
ALTER DATABASE [EventLeadPlatform] SET CONCAT_NULL_YIELDS_NULL ON; -- NULL + string = NULL (SQL standard)
GO

PRINT 'ANSI/SQL standards enabled (SQLAlchemy compatible).';
GO

-- =====================================================================
-- Concurrency & Performance Settings (Web Application Optimized)
-- =====================================================================
-- READ_COMMITTED_SNAPSHOT: Critical for web apps (reduces blocking)
ALTER DATABASE [EventLeadPlatform] SET READ_COMMITTED_SNAPSHOT ON;
PRINT 'Read Committed Snapshot Isolation enabled (no blocking reads).';
GO

-- Snapshot Isolation: Optional, but useful for reporting queries
ALTER DATABASE [EventLeadPlatform] SET ALLOW_SNAPSHOT_ISOLATION ON;
GO

-- Async statistics update (better for write-heavy workloads)
ALTER DATABASE [EventLeadPlatform] SET AUTO_UPDATE_STATISTICS ON;
ALTER DATABASE [EventLeadPlatform] SET AUTO_UPDATE_STATISTICS_ASYNC ON;
GO

-- =====================================================================
-- Database Maintenance Settings
-- =====================================================================
ALTER DATABASE [EventLeadPlatform] SET AUTO_CLOSE OFF;             -- Don't close after last user
ALTER DATABASE [EventLeadPlatform] SET AUTO_SHRINK OFF;            -- Never shrink automatically (bad for performance)
ALTER DATABASE [EventLeadPlatform] SET AUTO_CREATE_STATISTICS ON;  -- Auto-create missing statistics
GO

-- =====================================================================
-- Recovery Model: SIMPLE for Development
-- =====================================================================
-- SIMPLE = No transaction log backups needed (easier for local dev)
-- Change to FULL in production (Azure SQL Database handles this automatically)
ALTER DATABASE [EventLeadPlatform] SET RECOVERY SIMPLE;
PRINT 'Recovery model set to SIMPLE (development mode).';
GO

-- =====================================================================
-- Advanced Settings
-- =====================================================================
ALTER DATABASE [EventLeadPlatform] SET MULTI_USER;                 -- Allow multiple connections
ALTER DATABASE [EventLeadPlatform] SET PAGE_VERIFY CHECKSUM;       -- Data integrity checks
ALTER DATABASE [EventLeadPlatform] SET DB_CHAINING OFF;            -- Security: No cross-database ownership chaining
ALTER DATABASE [EventLeadPlatform] SET TRUSTWORTHY OFF;            -- Security: Prevent elevation attacks
ALTER DATABASE [EventLeadPlatform] SET PARAMETERIZATION SIMPLE;    -- Simple query parameterization
ALTER DATABASE [EventLeadPlatform] SET NUMERIC_ROUNDABORT OFF;     -- Don't abort on rounding errors
ALTER DATABASE [EventLeadPlatform] SET RECURSIVE_TRIGGERS OFF;     -- No recursive triggers (good practice)
ALTER DATABASE [EventLeadPlatform] SET CURSOR_CLOSE_ON_COMMIT OFF; -- Cursors survive commits
ALTER DATABASE [EventLeadPlatform] SET CURSOR_DEFAULT GLOBAL;      -- Global cursor scope
ALTER DATABASE [EventLeadPlatform] SET TARGET_RECOVERY_TIME = 60 SECONDS; -- Checkpoint every 60 seconds
ALTER DATABASE [EventLeadPlatform] SET DELAYED_DURABILITY = DISABLED; -- Full durability (no data loss)
ALTER DATABASE [EventLeadPlatform] SET HONOR_BROKER_PRIORITY OFF;
ALTER DATABASE [EventLeadPlatform] SET DATE_CORRELATION_OPTIMIZATION OFF;
GO

-- =====================================================================
-- Query Store: Performance Monitoring (Highly Recommended)
-- =====================================================================
-- Query Store captures query performance data for troubleshooting
ALTER DATABASE [EventLeadPlatform] SET QUERY_STORE = ON;
GO

ALTER DATABASE [EventLeadPlatform] SET QUERY_STORE (
    OPERATION_MODE = READ_WRITE,                    -- Capture query data
    CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), -- Keep 30 days of history
    DATA_FLUSH_INTERVAL_SECONDS = 900,              -- Flush to disk every 15 minutes
    INTERVAL_LENGTH_MINUTES = 60,                   -- Aggregate data hourly
    MAX_STORAGE_SIZE_MB = 1000,                     -- 1GB max storage
    QUERY_CAPTURE_MODE = AUTO,                      -- Capture important queries only
    SIZE_BASED_CLEANUP_MODE = AUTO,                 -- Auto-clean when storage full
    MAX_PLANS_PER_QUERY = 200,                      -- Keep up to 200 plans per query
    WAIT_STATS_CAPTURE_MODE = ON                    -- Capture wait statistics
);
GO

PRINT 'Query Store enabled for performance monitoring.';
GO

-- =====================================================================
-- Accelerated Database Recovery (SQL Server 2019+)
-- =====================================================================
-- ADR speeds up database recovery after crashes (recommended for production)
-- Enabled by default in Azure SQL Database
IF SERVERPROPERTY('ProductMajorVersion') >= 15  -- SQL Server 2019+
BEGIN
    ALTER DATABASE [EventLeadPlatform] SET ACCELERATED_DATABASE_RECOVERY = ON;
    PRINT 'Accelerated Database Recovery enabled.';
END
GO

-- =====================================================================
-- Set Database to READ_WRITE Mode
-- =====================================================================
ALTER DATABASE [EventLeadPlatform] SET READ_WRITE;
GO

-- =====================================================================
-- Verification
-- =====================================================================
USE [EventLeadPlatform];
GO

-- Display database configuration
SELECT 
    name AS DatabaseName,
    collation_name AS Collation,
    compatibility_level AS CompatibilityLevel,
    recovery_model_desc AS RecoveryModel,
    is_read_committed_snapshot_on AS ReadCommittedSnapshotOn,
    snapshot_isolation_state_desc AS SnapshotIsolationState,
    is_query_store_on AS QueryStoreOn
FROM sys.databases
WHERE name = 'EventLeadPlatform';
GO

PRINT '';
PRINT '=====================================================================';
PRINT 'EventLeadPlatform Database Created Successfully!';
PRINT '=====================================================================';
PRINT 'Collation: Latin1_General_100_CI_AS_SC_UTF8 (International support)';
PRINT 'ANSI Settings: ON (SQLAlchemy compatible)';
PRINT 'Read Committed Snapshot: ON (Web application optimized)';
PRINT 'Recovery Model: SIMPLE (Development mode)';
PRINT 'Query Store: ON (Performance monitoring enabled)';
PRINT '';
PRINT 'Next Steps:';
PRINT '1. Configure backend/.env.local with connection string';
PRINT '2. Run Alembic migrations: alembic upgrade head';
PRINT '3. Verify connection: http://localhost:8000/api/test-database';
PRINT '=====================================================================';
GO

