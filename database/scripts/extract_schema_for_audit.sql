-- =====================================================================
-- Database Schema Extraction for Standards Audit
-- Run this in SSMS against EventLeadPlatform database
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- PART 1: All Tables with Primary Keys
-- =====================================================================
PRINT '========================================';
PRINT 'PART 1: ALL TABLES WITH PRIMARY KEYS';
PRINT '========================================';
PRINT '';

SELECT 
    t.TABLE_SCHEMA + '.' + t.TABLE_NAME AS [Table],
    STUFF((
        SELECT ', ' + c.COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE c
        WHERE OBJECTPROPERTY(OBJECT_ID(c.CONSTRAINT_SCHEMA + '.' + c.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
        AND c.TABLE_NAME = t.TABLE_NAME
        ORDER BY c.ORDINAL_POSITION
        FOR XML PATH('')
    ), 1, 2, '') AS [Primary Key Columns],
    CASE 
        WHEN EXISTS (
            SELECT 1 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE c
            WHERE OBJECTPROPERTY(OBJECT_ID(c.CONSTRAINT_SCHEMA + '.' + c.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
            AND c.TABLE_NAME = t.TABLE_NAME
            AND c.COLUMN_NAME LIKE '%ID'
            AND c.COLUMN_NAME = t.TABLE_NAME + 'ID'
        ) THEN 'COMPLIANT'
        WHEN EXISTS (
            SELECT 1 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE c
            WHERE OBJECTPROPERTY(OBJECT_ID(c.CONSTRAINT_SCHEMA + '.' + c.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
            AND c.TABLE_NAME = t.TABLE_NAME
            AND c.COLUMN_NAME LIKE '%ID'
        ) THEN 'PARTIAL'
        ELSE 'VIOLATION'
    END AS [Standards Check]
FROM INFORMATION_SCHEMA.TABLES t
WHERE t.TABLE_TYPE = 'BASE TABLE'
AND t.TABLE_NAME NOT LIKE 'alembic%'
ORDER BY t.TABLE_NAME;
GO

PRINT '';
PRINT '========================================';
PRINT 'PART 2: DETAILED COLUMN INFORMATION';
PRINT '========================================';
PRINT '';

-- =====================================================================
-- PART 2: All Columns for Each Table
-- =====================================================================
SELECT 
    c.TABLE_NAME AS [Table],
    c.COLUMN_NAME AS [Column],
    c.DATA_TYPE AS [Data Type],
    CASE 
        WHEN c.DATA_TYPE IN ('varchar', 'nvarchar', 'char', 'nchar') 
        THEN c.DATA_TYPE + '(' + 
             CASE 
                WHEN c.CHARACTER_MAXIMUM_LENGTH = -1 THEN 'MAX'
                ELSE CAST(c.CHARACTER_MAXIMUM_LENGTH AS VARCHAR(10))
             END + ')'
        WHEN c.DATA_TYPE IN ('decimal', 'numeric')
        THEN c.DATA_TYPE + '(' + CAST(c.NUMERIC_PRECISION AS VARCHAR(10)) + ',' + CAST(c.NUMERIC_SCALE AS VARCHAR(10)) + ')'
        ELSE c.DATA_TYPE
    END AS [Full Type],
    c.IS_NULLABLE AS [Nullable],
    CASE 
        WHEN pk.COLUMN_NAME IS NOT NULL THEN 'PK'
        ELSE ''
    END AS [Is PK],
    CASE 
        WHEN fk.COLUMN_NAME IS NOT NULL THEN 'FK -> ' + fk.REFERENCED_TABLE + '.' + fk.REFERENCED_COLUMN
        ELSE ''
    END AS [Foreign Key],
    CASE 
        WHEN c.DATA_TYPE IN ('varchar', 'char', 'text') THEN 'USE NVARCHAR'
        WHEN c.DATA_TYPE NOT LIKE 'n%' AND c.DATA_TYPE IN ('varchar', 'char') THEN 'VARCHAR VIOLATION'
        ELSE 'OK'
    END AS [Unicode Check]
FROM INFORMATION_SCHEMA.COLUMNS c
LEFT JOIN (
    SELECT 
        ku.TABLE_NAME,
        ku.COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku
    WHERE OBJECTPROPERTY(OBJECT_ID(ku.CONSTRAINT_SCHEMA + '.' + ku.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
) pk ON c.TABLE_NAME = pk.TABLE_NAME AND c.COLUMN_NAME = pk.COLUMN_NAME
LEFT JOIN (
    SELECT 
        fk.name AS FK_NAME,
        tp.name AS TABLE_NAME,
        cp.name AS COLUMN_NAME,
        tr.name AS REFERENCED_TABLE,
        cr.name AS REFERENCED_COLUMN
    FROM sys.foreign_keys fk
    INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
    INNER JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
    INNER JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
    INNER JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
    INNER JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
) fk ON c.TABLE_NAME = fk.TABLE_NAME AND c.COLUMN_NAME = fk.COLUMN_NAME
WHERE c.TABLE_NAME NOT LIKE 'alembic%'
ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION;
GO

PRINT '';
PRINT '========================================';
PRINT 'PART 3: PRIMARY KEY STANDARDS VIOLATIONS';
PRINT '========================================';
PRINT '';

-- =====================================================================
-- PART 3: Primary Key Standards Violations
-- =====================================================================
SELECT 
    t.TABLE_NAME AS [Table Name],
    STUFF((
        SELECT ', ' + c.COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE c
        WHERE OBJECTPROPERTY(OBJECT_ID(c.CONSTRAINT_SCHEMA + '.' + c.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
        AND c.TABLE_NAME = t.TABLE_NAME
        ORDER BY c.ORDINAL_POSITION
        FOR XML PATH('')
    ), 1, 2, '') AS [Current Primary Key],
    t.TABLE_NAME + 'ID' AS [Expected Primary Key],
    CASE 
        WHEN NOT EXISTS (
            SELECT 1 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE c
            WHERE OBJECTPROPERTY(OBJECT_ID(c.CONSTRAINT_SCHEMA + '.' + c.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
            AND c.TABLE_NAME = t.TABLE_NAME
            AND c.COLUMN_NAME = t.TABLE_NAME + 'ID'
        ) THEN 'VIOLATION: Does not follow [TableName]ID pattern'
        ELSE 'COMPLIANT'
    END AS [Issue]
FROM INFORMATION_SCHEMA.TABLES t
WHERE t.TABLE_TYPE = 'BASE TABLE'
AND t.TABLE_NAME NOT LIKE 'alembic%'
AND NOT EXISTS (
    SELECT 1 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE c
    WHERE OBJECTPROPERTY(OBJECT_ID(c.CONSTRAINT_SCHEMA + '.' + c.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
    AND c.TABLE_NAME = t.TABLE_NAME
    AND c.COLUMN_NAME = t.TABLE_NAME + 'ID'
)
ORDER BY t.TABLE_NAME;
GO

PRINT '';
PRINT '========================================';
PRINT 'PART 4: VARCHAR vs NVARCHAR VIOLATIONS';
PRINT '========================================';
PRINT '';

-- =====================================================================
-- PART 4: VARCHAR vs NVARCHAR Violations
-- =====================================================================
SELECT 
    c.TABLE_NAME AS [Table],
    c.COLUMN_NAME AS [Column],
    c.DATA_TYPE AS [Current Type],
    CASE 
        WHEN c.CHARACTER_MAXIMUM_LENGTH = -1 THEN 'NVARCHAR(MAX)'
        ELSE 'NVARCHAR(' + CAST(c.CHARACTER_MAXIMUM_LENGTH AS VARCHAR(10)) + ')'
    END AS [Should Be],
    'CRITICAL: Use NVARCHAR for Unicode support' AS [Issue]
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE c.DATA_TYPE IN ('varchar', 'char', 'text')
AND c.TABLE_NAME NOT LIKE 'alembic%'
ORDER BY c.TABLE_NAME, c.COLUMN_NAME;
GO

PRINT '';
PRINT '========================================';
PRINT 'PART 5: FOREIGN KEY RELATIONSHIPS';
PRINT '========================================';
PRINT '';

-- =====================================================================
-- PART 5: All Foreign Key Relationships
-- =====================================================================
SELECT 
    fk.name AS [FK Constraint Name],
    tp.name AS [From Table],
    cp.name AS [From Column],
    tr.name AS [To Table],
    cr.name AS [To Column],
    CASE 
        WHEN cp.name = tr.name + 'ID' THEN 'COMPLIANT'
        WHEN cp.name LIKE '%' + tr.name + '%ID' THEN 'CONTEXTUAL (OK)'
        ELSE 'VIOLATION: FK name does not follow [ReferencedTable]ID pattern'
    END AS [Standards Check]
FROM sys.foreign_keys fk
INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
INNER JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
INNER JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
INNER JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
INNER JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
WHERE tp.name NOT LIKE 'alembic%'
ORDER BY tp.name, fk.name;
GO

PRINT '';
PRINT '========================================';
PRINT 'PART 6: MISSING AUDIT TRAIL COLUMNS';
PRINT '========================================';
PRINT '';

-- =====================================================================
-- PART 6: Tables Missing Standard Audit Trail Columns
-- =====================================================================
SELECT 
    t.TABLE_NAME AS [Table],
    CASE WHEN c1.COLUMN_NAME IS NULL THEN 'MISSING' ELSE 'OK' END AS [CreatedDate],
    CASE WHEN c2.COLUMN_NAME IS NULL THEN 'MISSING' ELSE 'OK' END AS [CreatedBy],
    CASE WHEN c3.COLUMN_NAME IS NULL THEN 'MISSING' ELSE 'OK' END AS [UpdatedDate],
    CASE WHEN c4.COLUMN_NAME IS NULL THEN 'MISSING' ELSE 'OK' END AS [UpdatedBy],
    CASE WHEN c5.COLUMN_NAME IS NULL THEN 'MISSING' ELSE 'OK' END AS [IsDeleted],
    CASE WHEN c6.COLUMN_NAME IS NULL THEN 'MISSING' ELSE 'OK' END AS [DeletedDate],
    CASE WHEN c7.COLUMN_NAME IS NULL THEN 'MISSING' ELSE 'OK' END AS [DeletedBy]
FROM INFORMATION_SCHEMA.TABLES t
LEFT JOIN INFORMATION_SCHEMA.COLUMNS c1 ON t.TABLE_NAME = c1.TABLE_NAME AND c1.COLUMN_NAME = 'CreatedDate'
LEFT JOIN INFORMATION_SCHEMA.COLUMNS c2 ON t.TABLE_NAME = c2.TABLE_NAME AND c2.COLUMN_NAME = 'CreatedBy'
LEFT JOIN INFORMATION_SCHEMA.COLUMNS c3 ON t.TABLE_NAME = c3.TABLE_NAME AND c3.COLUMN_NAME = 'UpdatedDate'
LEFT JOIN INFORMATION_SCHEMA.COLUMNS c4 ON t.TABLE_NAME = c4.TABLE_NAME AND c4.COLUMN_NAME = 'UpdatedBy'
LEFT JOIN INFORMATION_SCHEMA.COLUMNS c5 ON t.TABLE_NAME = c5.TABLE_NAME AND c5.COLUMN_NAME = 'IsDeleted'
LEFT JOIN INFORMATION_SCHEMA.COLUMNS c6 ON t.TABLE_NAME = c6.TABLE_NAME AND c6.COLUMN_NAME = 'DeletedDate'
LEFT JOIN INFORMATION_SCHEMA.COLUMNS c7 ON t.TABLE_NAME = c7.TABLE_NAME AND c7.COLUMN_NAME = 'DeletedBy'
WHERE t.TABLE_TYPE = 'BASE TABLE'
AND t.TABLE_NAME NOT LIKE 'alembic%'
AND (c1.COLUMN_NAME IS NULL OR c2.COLUMN_NAME IS NULL OR c5.COLUMN_NAME IS NULL)
ORDER BY t.TABLE_NAME;
GO

PRINT '';
PRINT '========================================';
PRINT 'PART 7: SUMMARY STATISTICS';
PRINT '========================================';
PRINT '';

-- =====================================================================
-- PART 7: Summary Statistics
-- =====================================================================
DECLARE @TotalTables INT;
DECLARE @CompliantTables INT;
DECLARE @ViolationTables INT;
DECLARE @VarcharColumns INT;

SELECT @TotalTables = COUNT(*)
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
AND TABLE_NAME NOT LIKE 'alembic%';

SELECT @CompliantTables = COUNT(*)
FROM INFORMATION_SCHEMA.TABLES t
WHERE t.TABLE_TYPE = 'BASE TABLE'
AND t.TABLE_NAME NOT LIKE 'alembic%'
AND EXISTS (
    SELECT 1 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE c
    WHERE OBJECTPROPERTY(OBJECT_ID(c.CONSTRAINT_SCHEMA + '.' + c.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
    AND c.TABLE_NAME = t.TABLE_NAME
    AND c.COLUMN_NAME = t.TABLE_NAME + 'ID'
);

SET @ViolationTables = @TotalTables - @CompliantTables;

SELECT @VarcharColumns = COUNT(*)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE DATA_TYPE IN ('varchar', 'char', 'text')
AND TABLE_NAME NOT LIKE 'alembic%';

PRINT 'Total Tables: ' + CAST(@TotalTables AS VARCHAR(10));
PRINT 'Compliant Tables (correct [TableName]ID): ' + CAST(@CompliantTables AS VARCHAR(10));
PRINT 'Violation Tables: ' + CAST(@ViolationTables AS VARCHAR(10));
PRINT 'Compliance Rate: ' + CAST((@CompliantTables * 100.0 / @TotalTables) AS VARCHAR(10)) + '%';
PRINT '';
PRINT 'VARCHAR Columns (should be NVARCHAR): ' + CAST(@VarcharColumns AS VARCHAR(10));
PRINT '';
PRINT '========================================';
PRINT 'AUDIT COMPLETE';
PRINT '========================================';
GO

