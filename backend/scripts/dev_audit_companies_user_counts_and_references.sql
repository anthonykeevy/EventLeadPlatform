/*
  Dev cleanup helper: companies vs user membership + FK reference audit.

  Run in SSMS / Azure Data Studio against DEV. Review all result sets before deleting anything.

  Sections:
    1) Every company with user/membership counts (sorted: fewest users first)
    2) Companies with ZERO active UserCompany rows (likely erroneous signups)
    3) Summary counts for section 2
    4) Per-table row counts referencing orphan companies (dynamic from sys.foreign_keys)
    5) Detail sample for orphans (top 50 by CompanyID)
    6) Orphans that look safe to remove (no FK rows except optional logs) — manual review only

  Notes:
    - "User" association = dbo.UserCompany (not CreatedBy on Company).
    - CompanyID 1 (Signal Platforms) may show users; do not delete without intent.
    - Platform uses soft delete (IsDeleted); prefer soft-delete over hard DELETE.
    - Hard DELETE requires removing child rows in dependency order; section 4 guides that.
*/

SET NOCOUNT ON;

-- ─── 1) User counts per company ───
;WITH UserCounts AS (
    SELECT
        uc.CompanyID,
        COUNT(*) AS TotalMembershipRows,
        SUM(CASE WHEN uc.IsDeleted = 0 THEN 1 ELSE 0 END) AS ActiveMembershipRows,
        COUNT(DISTINCT uc.UserID) AS DistinctUsers_All,
        COUNT(DISTINCT CASE WHEN uc.IsDeleted = 0 THEN uc.UserID END) AS DistinctUsers_Active
    FROM dbo.UserCompany uc
    GROUP BY uc.CompanyID
)
SELECT
    c.CompanyID,
    c.CompanyName,
    c.ABN,
    c.IsActive,
    c.IsDeleted AS CompanyIsDeleted,
    c.CreatedDate,
    COALESCE(uc.DistinctUsers_Active, 0) AS ActiveUsers,
    COALESCE(uc.ActiveMembershipRows, 0) AS ActiveMembershipRows,
    COALESCE(uc.DistinctUsers_All, 0) AS Users_IncludingDeletedMemberships,
    COALESCE(uc.TotalMembershipRows, 0) AS TotalMembershipRows
FROM dbo.Company c
LEFT JOIN UserCounts uc ON uc.CompanyID = c.CompanyID
ORDER BY ActiveUsers ASC, c.CreatedDate DESC;

-- ─── 2) Orphans: no active UserCompany ───
IF OBJECT_ID('tempdb..#OrphanCompany') IS NOT NULL DROP TABLE #OrphanCompany;

SELECT
    c.CompanyID,
    c.CompanyName,
    c.ABN,
    c.IsActive,
    c.IsDeleted,
    c.CreatedDate,
    c.CreatedBy
INTO #OrphanCompany
FROM dbo.Company c
WHERE c.IsDeleted = 0
  AND NOT EXISTS (
      SELECT 1
      FROM dbo.UserCompany uc
      WHERE uc.CompanyID = c.CompanyID
        AND uc.IsDeleted = 0
  );

SELECT *
FROM #OrphanCompany
ORDER BY CompanyID;

-- ─── 3) Orphan summary ───
SELECT
    COUNT(*) AS OrphanCompanyCount,
    MIN(CompanyID) AS MinCompanyID,
    MAX(CompanyID) AS MaxCompanyID
FROM #OrphanCompany;

-- ─── 4) FK reference audit (all columns referencing dbo.Company) ───
IF OBJECT_ID('tempdb..#CompanyRefCounts') IS NOT NULL DROP TABLE #CompanyRefCounts;

CREATE TABLE #CompanyRefCounts (
    RefSchema sysname NOT NULL,
    RefTable sysname NOT NULL,
    RefColumn sysname NOT NULL,
    ReferencingRows bigint NOT NULL
);

DECLARE @dyn nvarchar(max) = N'';

SELECT @dyn = @dyn + N'
INSERT INTO #CompanyRefCounts (RefSchema, RefTable, RefColumn, ReferencingRows)
SELECT '
    + QUOTENAME(OBJECT_SCHEMA_NAME(fk.parent_object_id), '''')
    + N', '
    + QUOTENAME(OBJECT_NAME(fk.parent_object_id), '''')
    + N', '
    + QUOTENAME(COL_NAME(fkc.parent_object_id, fkc.parent_column_id), '''')
    + N', COUNT_BIG(*)
FROM '
    + QUOTENAME(OBJECT_SCHEMA_NAME(fk.parent_object_id)) + N'.' + QUOTENAME(OBJECT_NAME(fk.parent_object_id)) + N' AS t
INNER JOIN #OrphanCompany o ON o.CompanyID = t.' + QUOTENAME(COL_NAME(fkc.parent_object_id, fkc.parent_column_id)) + N'
;'
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc
    ON fkc.constraint_object_id = fk.object_id
WHERE fk.referenced_object_id = OBJECT_ID(N'dbo.Company');

IF LEN(@dyn) > 0
    EXEC sys.sp_executesql @dyn;

SELECT
    RefSchema,
    RefTable,
    RefColumn,
    ReferencingRows
FROM #CompanyRefCounts
WHERE ReferencingRows > 0
ORDER BY ReferencingRows DESC, RefSchema, RefTable, RefColumn;

-- Tables/columns with zero orphan references are omitted above.

-- ─── 5) Per-orphan rollup (which orphans have any non-log data) ───
;WITH RefByCompany AS (
    -- dbo.Company self-reference (parent)
    SELECT o.CompanyID, N'dbo.Company' AS RefTable, N'ParentCompanyID' AS RefColumn, COUNT(*) AS Cnt
    FROM #OrphanCompany o
    INNER JOIN dbo.Company ch ON ch.ParentCompanyID = o.CompanyID AND ch.IsDeleted = 0
    GROUP BY o.CompanyID
    UNION ALL
    SELECT o.CompanyID, N'dbo.UserCompany', N'CompanyID', COUNT(*)
    FROM #OrphanCompany o
    INNER JOIN dbo.UserCompany uc ON uc.CompanyID = o.CompanyID
    GROUP BY o.CompanyID
    UNION ALL
    SELECT o.CompanyID, N'dbo.Event', N'CompanyID', COUNT(*)
    FROM #OrphanCompany o
    INNER JOIN dbo.Event e ON e.CompanyID = o.CompanyID AND e.IsDeleted = 0
    GROUP BY o.CompanyID
    UNION ALL
    SELECT o.CompanyID, N'dbo.Form', N'CompanyID', COUNT(*)
    FROM #OrphanCompany o
    INNER JOIN dbo.Form f ON f.CompanyID = o.CompanyID AND f.IsDeleted = 0
    GROUP BY o.CompanyID
    UNION ALL
    SELECT o.CompanyID, N'dbo.Asset', N'CompanyID', COUNT(*)
    FROM #OrphanCompany o
    INNER JOIN dbo.Asset a ON a.CompanyID = o.CompanyID AND a.IsDeleted = 0
    GROUP BY o.CompanyID
    UNION ALL
    SELECT o.CompanyID, N'config.CompanyValidationRule', N'CompanyID', COUNT(*)
    FROM #OrphanCompany o
    INNER JOIN config.CompanyValidationRule r ON r.CompanyID = o.CompanyID AND r.IsDeleted = 0
    GROUP BY o.CompanyID
)
SELECT
    o.CompanyID,
    o.CompanyName,
    o.ABN,
    o.CreatedDate,
    STRING_AGG(CONCAT(r.RefTable, N'.', r.RefColumn, N'=', r.Cnt), N'; ') WITHIN GROUP (ORDER BY r.RefTable) AS KeyReferences
FROM #OrphanCompany o
LEFT JOIN RefByCompany r ON r.CompanyID = o.CompanyID
GROUP BY o.CompanyID, o.CompanyName, o.ABN, o.CreatedDate
ORDER BY o.CompanyID;

-- ─── 6) Orphans with NO blocking domain rows (still may have audit/log FKs) ───
SELECT o.*
FROM #OrphanCompany o
WHERE NOT EXISTS (SELECT 1 FROM dbo.UserCompany uc WHERE uc.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.Event e WHERE e.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.Form f WHERE f.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.Asset a WHERE a.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM config.CompanyValidationRule r WHERE r.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.CompanyCustomerDetails d WHERE d.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.CompanyBillingDetails d WHERE d.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.CompanyOrganizerDetails d WHERE d.CompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.CompanyRelationship cr WHERE cr.ParentCompanyID = o.CompanyID OR cr.ChildCompanyID = o.CompanyID)
  AND NOT EXISTS (SELECT 1 FROM dbo.Company ch WHERE ch.ParentCompanyID = o.CompanyID AND ch.IsDeleted = 0)
ORDER BY o.CompanyID;

/*
  Optional soft-delete (ONLY after you confirm CompanyIDs in #OrphanCompany):

  BEGIN TRAN;
  UPDATE dbo.Company
  SET IsDeleted = 1, DeletedDate = GETUTCDATE(), DeletedBy = 1  -- your admin UserID
  WHERE CompanyID IN (SELECT CompanyID FROM #OrphanCompany WHERE CompanyID <> 1);
  -- ROLLBACK TRAN;  -- review first
  COMMIT TRAN;

  Hard DELETE is not recommended on dev with FK graph; use section 4 to delete children first if required.
*/
