-- =====================================================================
-- EventLeadPlatform - Simple Database Creation (Local Development)
-- =====================================================================
-- This version uses SQL Server's default data directory
-- Works on any machine without path configuration
-- =====================================================================

USE [master]
GO

-- Drop existing if exists
IF EXISTS (SELECT name FROM sys.databases WHERE name = N'EventLeadPlatform')
BEGIN
    ALTER DATABASE [EventLeadPlatform] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE [EventLeadPlatform];
    PRINT 'Existing EventLeadPlatform database dropped.';
END
GO

-- Create database (SQL Server will use default data directory)
CREATE DATABASE [EventLeadPlatform]
    COLLATE Latin1_General_100_CI_AS_SC_UTF8;
GO

PRINT 'Database EventLeadPlatform created with UTF-8 collation.';
GO

-- Configure for SQLAlchemy and web apps
ALTER DATABASE [EventLeadPlatform] SET ANSI_NULLS ON;
ALTER DATABASE [EventLeadPlatform] SET ANSI_WARNINGS ON;
ALTER DATABASE [EventLeadPlatform] SET ANSI_PADDING ON;
ALTER DATABASE [EventLeadPlatform] SET QUOTED_IDENTIFIER ON;
ALTER DATABASE [EventLeadPlatform] SET READ_COMMITTED_SNAPSHOT ON WITH NO_WAIT;
ALTER DATABASE [EventLeadPlatform] SET RECOVERY SIMPLE;
ALTER DATABASE [EventLeadPlatform] SET QUERY_STORE = ON;
GO

PRINT 'Database configured for SQLAlchemy and web applications.';
GO

-- Verify configuration
USE [EventLeadPlatform];
GO

SELECT 
    DB_NAME() AS DatabaseName,
    DATABASEPROPERTYEX(DB_NAME(), 'Collation') AS Collation,
    DATABASEPROPERTYEX(DB_NAME(), 'Status') AS Status;
GO

PRINT '=====================================================================';
PRINT 'EventLeadPlatform Database Ready!';
PRINT 'Connection String: Server=localhost;Database=EventLeadPlatform;Trusted_Connection=yes;TrustServerCertificate=yes;';
PRINT '=====================================================================';
GO

