-- =====================================================================
-- Enhanced ABR Cache Schema - Multiple Search Types
-- =====================================================================
-- Author: Solomon 📜 (SQL Standards Sage)
-- Date: October 13, 2025
-- Version: 1.0.0
-- =====================================================================
-- Purpose:
--   Enhanced caching system for ABR API searches supporting multiple
--   search methods: ABN, ACN, and Company Name searches.
--   
--   Extends existing ABNCache table to support:
--   - ABN searches (existing functionality)
--   - ACN searches (new)
--   - Company name searches (new, multiple results per query)
--
-- Strategy:
--   - Single cache table for all ABR search types
--   - Composite primary key: (SearchType, SearchKey, ResultIndex)
--   - JSON storage for flexible result caching
--   - 30-day TTL for all search types
--
-- Standards:
--   - PascalCase naming (Solomon's requirement)
--   - NVARCHAR for text (UTF-8 support)
--   - DATETIME2 with UTC timestamps
--   - Audit columns for cache management
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- TABLE: ABRSearchCache (Enhanced Multi-Search Cache)
-- =====================================================================
-- Purpose: Cache ABR API search results for all search types
-- Key Insight: Single table supports ABN, ACN, and Name searches efficiently
-- =====================================================================

-- Drop existing ABNCache table if it exists (migration from simple to enhanced)
IF EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ABNCache')
BEGIN
    PRINT 'Dropping existing ABNCache table (migrating to enhanced ABRSearchCache)...';
    DROP TABLE [ABNCache];
END
GO

CREATE TABLE [ABRSearchCache] (
    -- =====================================================================
    -- Composite Primary Key (Search Type + Key + Result Index)
    -- =====================================================================
    SearchType NVARCHAR(10) NOT NULL,
    -- ^ Search method: 'ABN', 'ACN', 'Name'
    -- Used for: Distinguishing search types, composite key part 1
    
    SearchKey NVARCHAR(200) NOT NULL,
    -- ^ Search query: ABN (11 digits), ACN (9 digits), or Company Name
    -- Used for: Composite key part 2, search query lookup
    -- NVARCHAR(200): Handles long company names
    
    ResultIndex INT NOT NULL DEFAULT 0,
    -- ^ Result index for Name searches (0 = single result, 1+ = multiple results)
    -- Used for: Composite key part 3, handling multiple name search results
    -- ABN/ACN searches: Always 0 (single result)
    -- Name searches: 0, 1, 2, ... (multiple results)
    
    -- =====================================================================
    -- Cached Search Result
    -- =====================================================================
    ResultJSON NVARCHAR(MAX) NOT NULL,
    -- ^ Cached ABR API response as JSON
    -- Contains: ABN, entity_name, entity_type, business_names, etc.
    -- NVARCHAR(MAX): Flexible storage for varying result structures
    
    SearchMetadata NVARCHAR(MAX) NULL,
    -- ^ Additional search metadata (JSON)
    -- Contains: search_timestamp, api_endpoint, response_time_ms, etc.
    -- Used for: Analytics, performance monitoring, debugging
    
    -- =====================================================================
    -- Cache Management
    -- =====================================================================
    CachedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When result was cached (UTC)
    -- Used for: TTL calculation, cache expiration
    
    CacheTTLSeconds INT NOT NULL DEFAULT 2592000,
    -- ^ Cache TTL in seconds (default: 30 days = 2,592,000 seconds)
    -- Used for: Flexible cache expiration per search type
    -- ABR terms: 30-day cache allowed
    
    CacheVersion INT NOT NULL DEFAULT 1,
    -- ^ Cache version for invalidation
    -- Used for: Cache schema migrations, manual invalidation
    
    IsActive BIT NOT NULL DEFAULT 1,
    -- ^ Is cache entry active? (soft delete for cache management)
    -- Used for: Soft invalidation without data loss
    
    -- =====================================================================
    -- Audit Trail (Cache Management)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ Record creation timestamp (UTC)
    
    CreatedBy BIGINT NULL,
    -- ^ System process that created cache entry (usually NULL for API caches)
    
    UpdatedDate DATETIME2 NULL,
    -- ^ Last cache update timestamp (UTC)
    
    UpdatedBy BIGINT NULL,
    -- ^ System process that updated cache entry
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT PK_ABRSearchCache PRIMARY KEY (SearchType, SearchKey, ResultIndex),
    
    -- Search type validation
    CONSTRAINT CK_ABRSearchCache_SearchType CHECK (
        SearchType IN ('ABN', 'ACN', 'Name')
    ),
    
    -- Result index validation (0+ for all search types)
    CONSTRAINT CK_ABRSearchCache_ResultIndex CHECK (
        ResultIndex >= 0
    ),
    
    -- Cache TTL validation (reasonable range)
    CONSTRAINT CK_ABRSearchCache_TTL CHECK (
        CacheTTLSeconds BETWEEN 3600 AND 86400*90  -- 1 hour to 90 days
    ),
    
    -- Cache version validation
    CONSTRAINT CK_ABRSearchCache_Version CHECK (
        CacheVersion >= 1
    ),
    
    -- Foreign key constraints (optional - for audit trail)
    CONSTRAINT FK_ABRSearchCache_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_ABRSearchCache_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID)
);
GO

-- =====================================================================
-- INDEXES: Performance Optimization
-- =====================================================================

-- Index for cache lookup by search type and key
CREATE INDEX IX_ABRSearchCache_Lookup ON [ABRSearchCache](SearchType, SearchKey, IsActive)
    WHERE IsActive = 1;
GO

-- Index for cache expiration cleanup (TTL management)
CREATE INDEX IX_ABRSearchCache_Expiration ON [ABRSearchCache](CachedDate, CacheTTLSeconds, IsActive)
    WHERE IsActive = 1;
GO

-- Index for cache analytics (search type usage)
CREATE INDEX IX_ABRSearchCache_Analytics ON [ABRSearchCache](SearchType, CachedDate, IsActive)
    WHERE IsActive = 1;
GO

PRINT 'ABRSearchCache table created successfully (enhanced multi-search cache)!';
GO

-- =====================================================================
-- MIGRATION: Copy existing ABN cache data (if any)
-- =====================================================================

-- Note: This migration assumes the old ABNCache table structure
-- If migrating from existing system, uncomment and modify as needed:

/*
PRINT 'Migrating existing ABN cache data...';

-- Copy existing ABN cache entries to new table structure
INSERT INTO [ABRSearchCache] (
    SearchType, SearchKey, ResultIndex, ResultJSON, 
    CachedDate, CacheTTLSeconds, CacheVersion, IsActive,
    CreatedDate, CreatedBy, UpdatedDate, UpdatedBy
)
SELECT 
    'ABN' as SearchType,
    abn as SearchKey,
    0 as ResultIndex,
    response_json as ResultJSON,
    cached_at as CachedDate,
    2592000 as CacheTTLSeconds,  -- 30 days
    cache_version as CacheVersion,
    1 as IsActive,
    cached_at as CreatedDate,
    NULL as CreatedBy,
    NULL as UpdatedDate,
    NULL as UpdatedBy
FROM [ABNCache]  -- Old table (if exists)
WHERE abn IS NOT NULL;

PRINT 'ABN cache migration completed successfully!';
*/

-- =====================================================================
-- CACHE MANAGEMENT STORED PROCEDURES
-- =====================================================================

-- Stored procedure for cache cleanup (expired entries)
CREATE PROCEDURE [sp_ABRSearchCache_Cleanup]
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ExpiredCount INT;
    DECLARE @CleanupDate DATETIME2 = GETUTCDATE();
    
    -- Soft delete expired cache entries
    UPDATE [ABRSearchCache] 
    SET 
        IsActive = 0,
        UpdatedDate = @CleanupDate,
        UpdatedBy = NULL  -- System process
    WHERE 
        IsActive = 1 
        AND CachedDate < DATEADD(SECOND, -CacheTTLSeconds, @CleanupDate);
    
    SET @ExpiredCount = @@ROWCOUNT;
    
    -- Log cleanup results
    PRINT CONCAT('ABR Search Cache cleanup completed: ', @ExpiredCount, ' expired entries deactivated');
    
    -- Optionally: Hard delete old soft-deleted entries (after 7 days)
    DELETE FROM [ABRSearchCache] 
    WHERE 
        IsActive = 0 
        AND UpdatedDate < DATEADD(DAY, -7, @CleanupDate);
    
    PRINT CONCAT('Hard delete completed: ', @@ROWCOUNT, ' old entries removed');
END
GO

-- Stored procedure for cache statistics
CREATE PROCEDURE [sp_ABRSearchCache_Statistics]
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        SearchType,
        COUNT(*) as TotalEntries,
        COUNT(CASE WHEN IsActive = 1 THEN 1 END) as ActiveEntries,
        COUNT(CASE WHEN IsActive = 0 THEN 1 END) as InactiveEntries,
        MIN(CachedDate) as OldestEntry,
        MAX(CachedDate) as NewestEntry,
        AVG(CAST(LEN(ResultJSON) AS FLOAT)) as AvgResultSizeBytes
    FROM [ABRSearchCache]
    GROUP BY SearchType
    ORDER BY SearchType;
END
GO

-- =====================================================================
-- SAMPLE DATA: Cache Usage Examples
-- =====================================================================

-- Example ABN cache entry
INSERT INTO [ABRSearchCache] (
    SearchType, SearchKey, ResultIndex, ResultJSON, SearchMetadata,
    CachedDate, CacheTTLSeconds, CacheVersion, IsActive
) VALUES (
    'ABN', '53004085616', 0,
    '{"abn": "53004085616", "entity_name": "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD", "entity_type": "Australian Private Company", "abn_status": "Active", "gst_registered": true, "business_names": ["ICC SYDNEY"], "trading_names": [], "state": "NSW", "postcode": "2000", "retrieved_at": "2025-10-13T12:34:56"}',
    '{"search_timestamp": "2025-10-13T12:34:56", "api_endpoint": "SearchByABNv202001", "response_time_ms": 1250}',
    GETUTCDATE(), 2592000, 1, 1
);

-- Example ACN cache entry
INSERT INTO [ABRSearchCache] (
    SearchType, SearchKey, ResultIndex, ResultJSON, SearchMetadata,
    CachedDate, CacheTTLSeconds, CacheVersion, IsActive
) VALUES (
    'ACN', '123456789', 0,
    '{"abn": "53004085616", "entity_name": "EXAMPLE COMPANY PTY LTD", "entity_type": "Australian Private Company", "abn_status": "Active", "gst_registered": false, "business_names": [], "trading_names": [], "state": "VIC", "postcode": "3000", "retrieved_at": "2025-10-13T12:35:10"}',
    '{"search_timestamp": "2025-10-13T12:35:10", "api_endpoint": "SearchByACNv202001", "response_time_ms": 980}',
    GETUTCDATE(), 2592000, 1, 1
);

-- Example Name search cache entries (multiple results)
INSERT INTO [ABRSearchCache] (
    SearchType, SearchKey, ResultIndex, ResultJSON, SearchMetadata,
    CachedDate, CacheTTLSeconds, CacheVersion, IsActive
) VALUES 
('Name', 'ICC Sydney', 0,
    '{"abn": "53004085616", "entity_name": "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD", "entity_type": "Australian Private Company", "abn_status": "Active", "gst_registered": true, "business_names": ["ICC SYDNEY"], "trading_names": [], "state": "NSW", "postcode": "2000", "retrieved_at": "2025-10-13T12:36:00"}',
    '{"search_timestamp": "2025-10-13T12:36:00", "api_endpoint": "SearchByNamev202001", "response_time_ms": 2100, "total_results": 3}',
    GETUTCDATE(), 2592000, 1, 1),

('Name', 'ICC Sydney', 1,
    '{"abn": "98765432101", "entity_name": "ICC SYDNEY EVENTS PTY LTD", "entity_type": "Australian Private Company", "abn_status": "Active", "gst_registered": false, "business_names": ["ICC SYDNEY EVENTS"], "trading_names": [], "state": "NSW", "postcode": "2000", "retrieved_at": "2025-10-13T12:36:00"}',
    '{"search_timestamp": "2025-10-13T12:36:00", "api_endpoint": "SearchByNamev202001", "response_time_ms": 2100, "total_results": 3}',
    GETUTCDATE(), 2592000, 1, 1),

('Name', 'ICC Sydney', 2,
    '{"abn": "11223344556", "entity_name": "ICC SYDNEY CATERING PTY LTD", "entity_type": "Australian Private Company", "abn_status": "Active", "gst_registered": true, "business_names": ["ICC SYDNEY CATERING"], "trading_names": [], "state": "NSW", "postcode": "2000", "retrieved_at": "2025-10-13T12:36:00"}',
    '{"search_timestamp": "2025-10-13T12:36:00", "api_endpoint": "SearchByNamev202001", "response_time_ms": 2100, "total_results": 3}',
    GETUTCDATE(), 2592000, 1, 1);

GO

-- =====================================================================
-- SUMMARY
-- =====================================================================

PRINT '========================================';
PRINT 'Enhanced ABR Search Cache Complete!';
PRINT '========================================';
PRINT 'Table Created:';
PRINT '  ABRSearchCache (enhanced multi-search cache)';
PRINT '';
PRINT 'Supported Search Types:';
PRINT '  ✅ ABN Search (11 digits, single result)';
PRINT '  ✅ ACN Search (9 digits, single result)';
PRINT '  ✅ Name Search (partial match, multiple results)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Composite primary key (SearchType, SearchKey, ResultIndex)';
PRINT '  ✅ JSON storage for flexible result caching';
PRINT '  ✅ 30-day TTL for all search types';
PRINT '  ✅ Soft delete for cache management';
PRINT '  ✅ Performance indexes for fast lookups';
PRINT '  ✅ Cache cleanup stored procedures';
PRINT '  ✅ Analytics and monitoring support';
PRINT '';
PRINT 'Performance Optimizations:';
PRINT '  ✅ Index on (SearchType, SearchKey, IsActive)';
PRINT '  ✅ Index on (CachedDate, CacheTTLSeconds, IsActive)';
PRINT '  ✅ Index on (SearchType, CachedDate, IsActive)';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Update ABR client to use enhanced cache';
PRINT '  2. Implement smart search detection logic';
PRINT '  3. Test with real ABR API endpoints';
PRINT '  4. Set up cache cleanup job (daily)';
PRINT '========================================';
GO
