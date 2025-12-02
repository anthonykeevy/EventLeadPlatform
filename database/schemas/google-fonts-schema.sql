-- ============================================================================
-- Google Fonts Domain Schema
-- EventLead Platform
-- ============================================================================
-- Version: 2.0.0
-- Author: Data Domain Architect
-- Date: December 2025
-- 
-- Purpose: Local caching of Google Fonts metadata AND custom corporate font
--          uploads for responsive font selection in the Form Builder.
--
-- Key Features:
-- - Google Fonts API caching with monthly sync
-- - Custom corporate font uploads with validation
-- - Company-Font junction table for licensing/sharing
-- - Per-company display name aliases
-- - Hash-based deduplication to prevent duplicate storage
-- - Full font file metadata extraction
--
-- Standards Applied:
-- - INT IDENTITY(1,1) for primary keys (project standard)
-- - Logging tables under 'log' schema (project standard)
-- - PascalCase naming (Solomon's standards)
-- - NVARCHAR for text (UTF-8 support)
-- - DATETIME2 with UTC timestamps
-- - Soft deletes with full audit trail
-- ============================================================================

-- ============================================================================
-- SCHEMA CREATION
-- ============================================================================

-- Ensure log schema exists (for logging tables)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'log')
BEGIN
    EXEC('CREATE SCHEMA [log]');
END
GO

-- ============================================================================
-- REFERENCE TABLES
-- ============================================================================

-- FontCategoryRef: Category definitions
-- Drop if exists for clean recreation
IF OBJECT_ID('[dbo].[FontCategoryRef]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontCategoryRef];
GO

CREATE TABLE [dbo].[FontCategoryRef] (
    CategoryCode NVARCHAR(50) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    DisplayOrder INT NOT NULL DEFAULT 0,
    IconClass NVARCHAR(100) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

-- Seed font categories
INSERT INTO [dbo].[FontCategoryRef] (CategoryCode, CategoryName, Description, DisplayOrder, IconClass) VALUES
('serif', 'Serif', 'Traditional fonts with decorative strokes (serifs) at the ends of letters. Best for print and formal documents.', 1, 'icon-font-serif'),
('sans-serif', 'Sans Serif', 'Modern, clean fonts without decorative strokes. Excellent for digital interfaces and contemporary designs.', 2, 'icon-font-sans'),
('display', 'Display', 'Decorative fonts designed for headlines and large text. Use sparingly for impact.', 3, 'icon-font-display'),
('handwriting', 'Handwriting', 'Script and handwritten style fonts. Perfect for personal touches and creative projects.', 4, 'icon-font-handwriting'),
('monospace', 'Monospace', 'Fixed-width fonts where each character takes the same space. Ideal for code and technical content.', 5, 'icon-font-mono');
GO

-- FontSubsetRef: Subset/language definitions
IF OBJECT_ID('[dbo].[FontSubsetRef]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontSubsetRef];
GO

CREATE TABLE [dbo].[FontSubsetRef] (
    SubsetCode NVARCHAR(50) PRIMARY KEY,
    SubsetName NVARCHAR(100) NOT NULL,
    SubsetGroup NVARCHAR(50) NOT NULL,
    Description NVARCHAR(500) NULL,
    PrimaryLanguages NVARCHAR(500) NULL,
    DisplayOrder INT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

-- Seed font subsets
INSERT INTO [dbo].[FontSubsetRef] (SubsetCode, SubsetName, SubsetGroup, PrimaryLanguages, DisplayOrder) VALUES
('latin', 'Latin', 'Latin', 'English, Spanish, French, German, Portuguese, Italian', 1),
('latin-ext', 'Latin Extended', 'Latin', 'Polish, Czech, Romanian, Vietnamese, Turkish', 2),
('cyrillic', 'Cyrillic', 'Cyrillic', 'Russian, Bulgarian', 3),
('cyrillic-ext', 'Cyrillic Extended', 'Cyrillic', 'Ukrainian, Serbian, Macedonian', 4),
('greek', 'Greek', 'Greek', 'Greek', 5),
('greek-ext', 'Greek Extended', 'Greek', 'Ancient Greek, Polytonic Greek', 6),
('vietnamese', 'Vietnamese', 'Asian', 'Vietnamese', 7),
('arabic', 'Arabic', 'Middle Eastern', 'Arabic, Persian, Urdu', 8),
('hebrew', 'Hebrew', 'Middle Eastern', 'Hebrew', 9),
('devanagari', 'Devanagari', 'Asian', 'Hindi, Sanskrit, Nepali', 10),
('thai', 'Thai', 'Asian', 'Thai', 11),
('korean', 'Korean', 'Asian', 'Korean', 12),
('japanese', 'Japanese', 'Asian', 'Japanese', 13),
('chinese-simplified', 'Chinese Simplified', 'Asian', 'Mandarin (China)', 14),
('chinese-traditional', 'Chinese Traditional', 'Asian', 'Mandarin (Taiwan, Hong Kong)', 15),
('tamil', 'Tamil', 'Asian', 'Tamil', 16),
('bengali', 'Bengali', 'Asian', 'Bengali, Assamese', 17),
('telugu', 'Telugu', 'Asian', 'Telugu', 18),
('kannada', 'Kannada', 'Asian', 'Kannada', 19),
('malayalam', 'Malayalam', 'Asian', 'Malayalam', 20),
('gujarati', 'Gujarati', 'Asian', 'Gujarati', 21);
GO

-- FontAxisRef: Standard variable font axis definitions
IF OBJECT_ID('[dbo].[FontAxisRef]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontAxisRef];
GO

CREATE TABLE [dbo].[FontAxisRef] (
    AxisTag NVARCHAR(10) PRIMARY KEY,
    AxisName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    IsStandard BIT NOT NULL DEFAULT 1,
    DefaultMin DECIMAL(10, 4) NULL,
    DefaultMax DECIMAL(10, 4) NULL,
    CssProperty NVARCHAR(100) NULL,
    DisplayOrder INT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

-- Seed standard font axes
INSERT INTO [dbo].[FontAxisRef] (AxisTag, AxisName, Description, IsStandard, DefaultMin, DefaultMax, CssProperty, DisplayOrder) VALUES
('wght', 'Weight', 'Controls the thickness of the font strokes', 1, 100, 900, 'font-weight', 1),
('wdth', 'Width', 'Controls the horizontal scaling of the font', 1, 50, 200, 'font-stretch', 2),
('ital', 'Italic', 'Controls the degree of italic styling', 1, 0, 1, 'font-style', 3),
('slnt', 'Slant', 'Controls the angle of the font (oblique)', 1, -90, 90, 'font-style', 4),
('opsz', 'Optical Size', 'Optimizes the font for different display sizes', 1, 8, 144, 'font-optical-sizing', 5),
('GRAD', 'Grade', 'Adjusts stroke thickness without changing width', 0, -200, 150, NULL, 6),
('XTRA', 'X-Height Extra', 'Adjusts counter width', 0, NULL, NULL, NULL, 7),
('YOPQ', 'Y Opaque', 'Adjusts stroke contrast', 0, NULL, NULL, NULL, 8),
('CASL', 'Casual', 'Transitions between formal and casual styles', 0, 0, 1, NULL, 9),
('CRSV', 'Cursive', 'Controls cursive styling', 0, 0, 1, NULL, 10),
('FILL', 'Fill', 'Controls icon fill (for icon fonts)', 0, 0, 1, NULL, 11),
('MONO', 'Monospace', 'Transitions between proportional and monospace', 0, 0, 1, NULL, 12),
('SOFT', 'Softness', 'Controls corner rounding', 0, 0, 100, NULL, 13),
('WONK', 'Wonky', 'Controls irregularity/playfulness', 0, 0, 1, NULL, 14);
GO

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- FontFamily: Primary font registry
IF OBJECT_ID('[dbo].[FontFamily]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontFamily];
GO

CREATE TABLE [dbo].[FontFamily] (
    -- Primary Key (INT IDENTITY per project standards)
    FontFamilyID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Font Source (Google, Custom, System)
    FontSource NVARCHAR(20) NOT NULL DEFAULT 'Google',
    UploadedByCompanyID BIGINT NULL,  -- FK to Company, NULL for Google fonts
    
    -- Core Identification
    GoogleFontID NVARCHAR(100) NULL,  -- NULL for custom fonts
    FamilyName NVARCHAR(200) NOT NULL,
    FamilyNameNormalized NVARCHAR(200) NOT NULL,
    
    -- Internal font metadata (extracted from font file)
    InternalFontName NVARCHAR(200) NULL,  -- Name from font file metadata
    InternalVersion NVARCHAR(50) NULL,     -- Version from font file
    
    -- Classification
    Category NVARCHAR(50) NOT NULL,
    SubCategory NVARCHAR(100) NULL,
    
    -- Version & Updates
    Version NVARCHAR(20) NOT NULL,
    VersionNumber INT NULL,
    LastModifiedDate DATE NOT NULL,
    
    -- URLs
    MenuFileUrl NVARCHAR(500) NULL,
    SpecimenUrl NVARCHAR(500) NULL,
    
    -- Font Characteristics
    IsVariableFont BIT NOT NULL DEFAULT 0,
    HasColorCapabilities BIT NOT NULL DEFAULT 0,
    
    -- Weight & Style Range
    MinWeight INT NULL,
    MaxWeight INT NULL,
    HasItalic BIT NOT NULL DEFAULT 0,
    HasRegular BIT NOT NULL DEFAULT 1,
    
    -- Subset Summary (for quick filtering)
    SupportsLatin BIT NOT NULL DEFAULT 1,
    SupportsCyrillic BIT NOT NULL DEFAULT 0,
    SupportsGreek BIT NOT NULL DEFAULT 0,
    SupportsArabic BIT NOT NULL DEFAULT 0,
    SupportsHebrew BIT NOT NULL DEFAULT 0,
    SupportsAsian BIT NOT NULL DEFAULT 0,
    TotalSubsets INT NOT NULL DEFAULT 1,
    
    -- Variant Summary
    TotalVariants INT NOT NULL DEFAULT 1,
    VariantList NVARCHAR(500) NULL,
    
    -- Platform Metadata (EventLead-specific)
    PopularityRank INT NULL,
    UsageCount INT NOT NULL DEFAULT 0,
    IsRecommended BIT NOT NULL DEFAULT 0,
    IsFeatured BIT NOT NULL DEFAULT 0,
    DisplayOrder INT NULL,
    
    -- Licensing
    LicenseType NVARCHAR(100) DEFAULT 'Open Font License',
    LicenseUrl NVARCHAR(500) NULL,
    
    -- Designer/Foundry
    Designer NVARCHAR(200) NULL,
    DesignerUrl NVARCHAR(500) NULL,
    Foundry NVARCHAR(200) NULL,
    
    -- Sync Metadata
    FirstSyncDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    LastSyncDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    SyncVersion INT NOT NULL DEFAULT 1,
    SyncStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',
    
    -- Audit Trail
    IsActive BIT NOT NULL DEFAULT 1,
    IsDeleted BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy NVARCHAR(100) NOT NULL DEFAULT 'SYSTEM',
    UpdatedDate DATETIME2 NULL,
    UpdatedBy NVARCHAR(100) NULL,
    DeletedDate DATETIME2 NULL,
    DeletedBy NVARCHAR(100) NULL,
    
    -- Foreign Key to Company for custom fonts
    CONSTRAINT FK_FontFamily_UploadedByCompany
        FOREIGN KEY (UploadedByCompanyID) REFERENCES [dbo].[Company](CompanyID)
);
GO

-- Unique constraint on GoogleFontID (only for non-null values)
CREATE UNIQUE NONCLUSTERED INDEX UQ_FontFamily_GoogleFontID 
ON [dbo].[FontFamily](GoogleFontID) 
WHERE GoogleFontID IS NOT NULL;
GO

-- Check constraint for FontSource
ALTER TABLE [dbo].[FontFamily]
ADD CONSTRAINT CK_FontFamily_FontSource 
CHECK (FontSource IN ('Google', 'Custom', 'System'));
GO

-- Index for custom fonts by company
CREATE NONCLUSTERED INDEX IX_FontFamily_UploadedByCompanyID 
ON [dbo].[FontFamily](UploadedByCompanyID) 
WHERE UploadedByCompanyID IS NOT NULL;
GO

-- Index for FontSource filtering
CREATE NONCLUSTERED INDEX IX_FontFamily_FontSource 
ON [dbo].[FontFamily](FontSource);
GO

-- Check constraints
ALTER TABLE [dbo].[FontFamily]
ADD CONSTRAINT CK_FontFamily_Category 
CHECK (Category IN ('serif', 'sans-serif', 'display', 'handwriting', 'monospace'));
GO

ALTER TABLE [dbo].[FontFamily]
ADD CONSTRAINT CK_FontFamily_SyncStatus 
CHECK (SyncStatus IN ('Active', 'Deprecated', 'Removed', 'Pending'));
GO

ALTER TABLE [dbo].[FontFamily]
ADD CONSTRAINT CK_FontFamily_MinWeight 
CHECK (MinWeight IS NULL OR (MinWeight >= 100 AND MinWeight <= 900));
GO

ALTER TABLE [dbo].[FontFamily]
ADD CONSTRAINT CK_FontFamily_MaxWeight 
CHECK (MaxWeight IS NULL OR (MaxWeight >= 100 AND MaxWeight <= 900));
GO

-- Indexes for FontFamily
CREATE NONCLUSTERED INDEX IX_FontFamily_FamilyName 
ON [dbo].[FontFamily](FamilyName);
GO

CREATE NONCLUSTERED INDEX IX_FontFamily_FamilyNameNormalized 
ON [dbo].[FontFamily](FamilyNameNormalized);
GO

CREATE NONCLUSTERED INDEX IX_FontFamily_Category 
ON [dbo].[FontFamily](Category);
GO

CREATE NONCLUSTERED INDEX IX_FontFamily_PopularityRank 
ON [dbo].[FontFamily](PopularityRank);
GO

CREATE NONCLUSTERED INDEX IX_FontFamily_LastModifiedDate 
ON [dbo].[FontFamily](LastModifiedDate DESC);
GO

CREATE NONCLUSTERED INDEX IX_FontFamily_SyncStatus 
ON [dbo].[FontFamily](SyncStatus) 
WHERE IsDeleted = 0;
GO

CREATE NONCLUSTERED INDEX IX_FontFamily_Featured 
ON [dbo].[FontFamily](IsFeatured, DisplayOrder) 
WHERE IsDeleted = 0 AND IsFeatured = 1;
GO

CREATE NONCLUSTERED INDEX IX_FontFamily_Active 
ON [dbo].[FontFamily](IsActive, IsDeleted);
GO

-- ============================================================================
-- FontVariant: Individual weight/style combinations
-- ============================================================================

IF OBJECT_ID('[dbo].[FontVariant]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontVariant];
GO

CREATE TABLE [dbo].[FontVariant] (
    -- Primary Key
    FontVariantID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Key
    FontFamilyID INT NOT NULL,
    
    -- Variant Identification
    VariantName NVARCHAR(50) NOT NULL,
    VariantNameNormalized NVARCHAR(50) NOT NULL,
    
    -- Weight & Style
    Weight INT NOT NULL DEFAULT 400,
    WeightName NVARCHAR(50) NULL,
    IsItalic BIT NOT NULL DEFAULT 0,
    
    -- File URLs
    TtfFileUrl NVARCHAR(500) NULL,
    WoffFileUrl NVARCHAR(500) NULL,
    Woff2FileUrl NVARCHAR(500) NULL,
    
    -- Local Caching
    IsFileCached BIT NOT NULL DEFAULT 0,
    CachedFilePath NVARCHAR(500) NULL,
    FileSizeBytes BIGINT NULL,
    FileHash NVARCHAR(64) NULL,
    
    -- Display
    DisplayOrder INT NOT NULL DEFAULT 0,
    IsDefault BIT NOT NULL DEFAULT 0,
    
    -- Audit Trail
    IsActive BIT NOT NULL DEFAULT 1,
    IsDeleted BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedDate DATETIME2 NULL,
    
    -- Foreign Key constraint
    CONSTRAINT FK_FontVariant_FontFamily 
        FOREIGN KEY (FontFamilyID) REFERENCES [dbo].[FontFamily](FontFamilyID)
);
GO

-- Unique constraint on Family + Variant
ALTER TABLE [dbo].[FontVariant]
ADD CONSTRAINT UQ_FontVariant_Family_Variant UNIQUE (FontFamilyID, VariantName);
GO

-- Weight constraint
ALTER TABLE [dbo].[FontVariant]
ADD CONSTRAINT CK_FontVariant_Weight 
CHECK (Weight IN (100, 200, 300, 400, 500, 600, 700, 800, 900));
GO

-- Indexes for FontVariant
CREATE NONCLUSTERED INDEX IX_FontVariant_FontFamilyID 
ON [dbo].[FontVariant](FontFamilyID);
GO

CREATE NONCLUSTERED INDEX IX_FontVariant_Weight 
ON [dbo].[FontVariant](Weight, IsItalic);
GO

-- ============================================================================
-- FontSubset: Character set support for each font
-- ============================================================================

IF OBJECT_ID('[dbo].[FontSubset]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontSubset];
GO

CREATE TABLE [dbo].[FontSubset] (
    -- Primary Key
    FontSubsetID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Key
    FontFamilyID INT NOT NULL,
    
    -- Subset Identification
    SubsetCode NVARCHAR(50) NOT NULL,
    SubsetName NVARCHAR(100) NOT NULL,
    
    -- Categorization
    SubsetGroup NVARCHAR(50) NULL,
    IsExtended BIT NOT NULL DEFAULT 0,
    
    -- Language Support
    PrimaryLanguages NVARCHAR(500) NULL,
    
    -- Display
    DisplayOrder INT NOT NULL DEFAULT 0,
    
    -- Audit
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    
    -- Foreign Key constraint
    CONSTRAINT FK_FontSubset_FontFamily 
        FOREIGN KEY (FontFamilyID) REFERENCES [dbo].[FontFamily](FontFamilyID)
);
GO

-- Unique constraint on Family + Subset
ALTER TABLE [dbo].[FontSubset]
ADD CONSTRAINT UQ_FontSubset_Family_Subset UNIQUE (FontFamilyID, SubsetCode);
GO

-- Indexes for FontSubset
CREATE NONCLUSTERED INDEX IX_FontSubset_FontFamilyID 
ON [dbo].[FontSubset](FontFamilyID);
GO

CREATE NONCLUSTERED INDEX IX_FontSubset_SubsetCode 
ON [dbo].[FontSubset](SubsetCode);
GO

-- ============================================================================
-- FontAxis: Variable font axes
-- ============================================================================

IF OBJECT_ID('[dbo].[FontAxis]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontAxis];
GO

CREATE TABLE [dbo].[FontAxis] (
    -- Primary Key
    FontAxisID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Key
    FontFamilyID INT NOT NULL,
    
    -- Axis Identification
    AxisTag NVARCHAR(10) NOT NULL,
    AxisName NVARCHAR(100) NOT NULL,
    
    -- Range
    MinValue DECIMAL(10, 4) NOT NULL,
    MaxValue DECIMAL(10, 4) NOT NULL,
    DefaultValue DECIMAL(10, 4) NULL,
    Step DECIMAL(10, 4) NULL,
    
    -- Classification
    IsStandard BIT NOT NULL DEFAULT 1,
    IsRegistered BIT NOT NULL DEFAULT 0,
    
    -- Display
    DisplayOrder INT NOT NULL DEFAULT 0,
    CssProperty NVARCHAR(100) NULL,
    
    -- Audit
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    
    -- Foreign Key constraint
    CONSTRAINT FK_FontAxis_FontFamily 
        FOREIGN KEY (FontFamilyID) REFERENCES [dbo].[FontFamily](FontFamilyID)
);
GO

-- Unique constraint on Family + Axis
ALTER TABLE [dbo].[FontAxis]
ADD CONSTRAINT UQ_FontAxis_Family_Tag UNIQUE (FontFamilyID, AxisTag);
GO

-- Indexes for FontAxis
CREATE NONCLUSTERED INDEX IX_FontAxis_FontFamilyID 
ON [dbo].[FontAxis](FontFamilyID);
GO

CREATE NONCLUSTERED INDEX IX_FontAxis_AxisTag 
ON [dbo].[FontAxis](AxisTag);
GO

-- ============================================================================
-- FontColorCapability: Color font capabilities
-- ============================================================================

IF OBJECT_ID('[dbo].[FontColorCapability]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontColorCapability];
GO

CREATE TABLE [dbo].[FontColorCapability] (
    -- Primary Key
    FontColorCapabilityID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Key
    FontFamilyID INT NOT NULL,
    
    -- Capability
    CapabilityCode NVARCHAR(20) NOT NULL,
    CapabilityName NVARCHAR(100) NOT NULL,
    CapabilityVersion NVARCHAR(20) NULL,
    
    -- Audit
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    
    -- Foreign Key constraint
    CONSTRAINT FK_FontColorCapability_FontFamily 
        FOREIGN KEY (FontFamilyID) REFERENCES [dbo].[FontFamily](FontFamilyID)
);
GO

-- Unique constraint
ALTER TABLE [dbo].[FontColorCapability]
ADD CONSTRAINT UQ_FontColorCapability_Family_Code UNIQUE (FontFamilyID, CapabilityCode);
GO

-- Index
CREATE NONCLUSTERED INDEX IX_FontColorCapability_FontFamilyID 
ON [dbo].[FontColorCapability](FontFamilyID);
GO

-- ============================================================================
-- CompanyFont: Junction table for Company-Font relationship (M:N)
-- Enables font sharing, licensing, and per-company display name aliases
-- ============================================================================

IF OBJECT_ID('[dbo].[CompanyFont]', 'U') IS NOT NULL
    DROP TABLE [dbo].[CompanyFont];
GO

CREATE TABLE [dbo].[CompanyFont] (
    -- Primary Key
    CompanyFontID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Keys
    CompanyID BIGINT NOT NULL,
    FontFamilyID INT NOT NULL,
    
    -- Per-company display name (allows "XeroxFont" vs "FujitsuFont" for same file)
    DisplayNameOverride NVARCHAR(200) NULL,  -- NULL = use FontFamily.FamilyName
    
    -- Relationship type
    IsOwner BIT NOT NULL DEFAULT 0,         -- TRUE = company uploaded this font
    IsLicensed BIT NOT NULL DEFAULT 1,      -- TRUE = company can use this font
    
    -- License tracking
    LicenseType NVARCHAR(50) NULL,          -- 'Owned', 'Shared', 'Platform'
    LicenseExpiryDate DATE NULL,
    LicenseNotes NVARCHAR(500) NULL,
    
    -- Audit
    GrantedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    GrantedBy BIGINT NULL,                  -- FK to User
    RevokedDate DATETIME2 NULL,
    RevokedBy BIGINT NULL,
    
    IsActive BIT NOT NULL DEFAULT 1,
    IsDeleted BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy NVARCHAR(100) NOT NULL DEFAULT 'SYSTEM',
    UpdatedDate DATETIME2 NULL,
    UpdatedBy NVARCHAR(100) NULL,
    
    -- Foreign Key constraints
    CONSTRAINT FK_CompanyFont_Company 
        FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyFont_FontFamily 
        FOREIGN KEY (FontFamilyID) REFERENCES [dbo].[FontFamily](FontFamilyID),
    CONSTRAINT FK_CompanyFont_GrantedBy 
        FOREIGN KEY (GrantedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_CompanyFont_RevokedBy 
        FOREIGN KEY (RevokedBy) REFERENCES [dbo].[User](UserID)
);
GO

-- Unique constraint - one relationship per company-font pair
ALTER TABLE [dbo].[CompanyFont]
ADD CONSTRAINT UQ_CompanyFont_Company_Font UNIQUE (CompanyID, FontFamilyID);
GO

-- Check constraint for LicenseType
ALTER TABLE [dbo].[CompanyFont]
ADD CONSTRAINT CK_CompanyFont_LicenseType 
CHECK (LicenseType IS NULL OR LicenseType IN ('Owned', 'Shared', 'Platform', 'Trial'));
GO

-- Indexes for CompanyFont
CREATE NONCLUSTERED INDEX IX_CompanyFont_CompanyID 
ON [dbo].[CompanyFont](CompanyID);
GO

CREATE NONCLUSTERED INDEX IX_CompanyFont_FontFamilyID 
ON [dbo].[CompanyFont](FontFamilyID);
GO

CREATE NONCLUSTERED INDEX IX_CompanyFont_Active 
ON [dbo].[CompanyFont](CompanyID, IsActive, IsLicensed) 
WHERE IsDeleted = 0;
GO

-- ============================================================================
-- FontFile: Uploaded font file storage with deduplication
-- Hash-based deduplication prevents storing the same file multiple times
-- ============================================================================

IF OBJECT_ID('[dbo].[FontFile]', 'U') IS NOT NULL
    DROP TABLE [dbo].[FontFile];
GO

CREATE TABLE [dbo].[FontFile] (
    -- Primary Key
    FontFileID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Key to FontVariant
    FontVariantID INT NOT NULL,
    
    -- File storage
    FileFormat NVARCHAR(10) NOT NULL,       -- 'ttf', 'otf', 'woff', 'woff2'
    FileData VARBINARY(MAX) NOT NULL,       -- Actual font file bytes
    FileSizeBytes BIGINT NOT NULL,
    FileHash NVARCHAR(64) NOT NULL,         -- SHA-256 for deduplication
    MimeType NVARCHAR(100) NOT NULL,
    OriginalFileName NVARCHAR(255) NULL,
    
    -- Extracted metadata (from font validation using fonttools)
    ExtractedFontName NVARCHAR(200) NULL,   -- Internal name from font file
    ExtractedFamily NVARCHAR(200) NULL,      -- Family name from font file
    ExtractedSubfamily NVARCHAR(200) NULL,   -- Subfamily (e.g., "Bold Italic")
    ExtractedVersion NVARCHAR(50) NULL,
    ExtractedCopyright NVARCHAR(500) NULL,
    ExtractedLicense NVARCHAR(500) NULL,
    ExtractedDesigner NVARCHAR(200) NULL,
    ExtractedVendor NVARCHAR(200) NULL,
    SupportedScripts NVARCHAR(500) NULL,    -- 'latin,cyrillic,greek' 
    GlyphCount INT NULL,
    UnitsPerEm INT NULL,
    
    -- Validation status
    IsValid BIT NOT NULL DEFAULT 1,
    ValidationDate DATETIME2 NULL,
    ValidationErrors NVARCHAR(MAX) NULL,
    
    -- Audit
    IsActive BIT NOT NULL DEFAULT 1,
    IsDeleted BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CreatedBy BIGINT NULL,
    
    -- Foreign Key constraint
    CONSTRAINT FK_FontFile_FontVariant 
        FOREIGN KEY (FontVariantID) REFERENCES [dbo].[FontVariant](FontVariantID),
    CONSTRAINT FK_FontFile_CreatedBy 
        FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID)
);
GO

-- Unique constraint on FileHash for deduplication
ALTER TABLE [dbo].[FontFile]
ADD CONSTRAINT UQ_FontFile_Hash UNIQUE (FileHash);
GO

-- Check constraint for FileFormat
ALTER TABLE [dbo].[FontFile]
ADD CONSTRAINT CK_FontFile_Format 
CHECK (FileFormat IN ('ttf', 'otf', 'woff', 'woff2', 'eot'));
GO

-- Indexes for FontFile
CREATE NONCLUSTERED INDEX IX_FontFile_FontVariantID 
ON [dbo].[FontFile](FontVariantID);
GO

CREATE NONCLUSTERED INDEX IX_FontFile_Hash 
ON [dbo].[FontFile](FileHash);
GO

CREATE NONCLUSTERED INDEX IX_FontFile_Format 
ON [dbo].[FontFile](FileFormat);
GO

-- ============================================================================
-- LOGGING TABLES (log schema)
-- ============================================================================

-- FontSyncLog: Track synchronization operations
IF OBJECT_ID('[log].[FontSyncLog]', 'U') IS NOT NULL
    DROP TABLE [log].[FontSyncLog];
GO

CREATE TABLE [log].[FontSyncLog] (
    -- Primary Key
    FontSyncLogID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Sync Operation
    SyncStartTime DATETIME2 NOT NULL,
    SyncEndTime DATETIME2 NULL,
    SyncDurationSeconds AS DATEDIFF(SECOND, SyncStartTime, SyncEndTime),
    
    -- Status
    SyncStatus NVARCHAR(20) NOT NULL DEFAULT 'Running',
    
    -- Metrics
    TotalFontsInAPI INT NULL,
    FontsAdded INT NOT NULL DEFAULT 0,
    FontsUpdated INT NOT NULL DEFAULT 0,
    FontsDeprecated INT NOT NULL DEFAULT 0,
    FontsRemoved INT NOT NULL DEFAULT 0,
    FontsUnchanged INT NOT NULL DEFAULT 0,
    VariantsProcessed INT NOT NULL DEFAULT 0,
    SubsetsProcessed INT NOT NULL DEFAULT 0,
    AxesProcessed INT NOT NULL DEFAULT 0,
    
    -- API Details
    APIEndpoint NVARCHAR(500) NULL,
    APIVersion NVARCHAR(20) NULL,
    APIResponseTimeMs INT NULL,
    APIResponseSizeBytes BIGINT NULL,
    
    -- Error Handling
    ErrorMessage NVARCHAR(MAX) NULL,
    ErrorDetails NVARCHAR(MAX) NULL,
    RetryCount INT NOT NULL DEFAULT 0,
    
    -- Trigger
    TriggerType NVARCHAR(50) NOT NULL DEFAULT 'Scheduled',
    TriggeredBy NVARCHAR(100) NULL,
    
    -- Audit
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

-- Check constraint for SyncStatus
ALTER TABLE [log].[FontSyncLog]
ADD CONSTRAINT CK_FontSyncLog_SyncStatus 
CHECK (SyncStatus IN ('Running', 'Success', 'Failed', 'Partial', 'Cancelled'));
GO

-- Check constraint for TriggerType
ALTER TABLE [log].[FontSyncLog]
ADD CONSTRAINT CK_FontSyncLog_TriggerType 
CHECK (TriggerType IN ('Scheduled', 'Manual', 'Webhook', 'Startup'));
GO

-- Indexes for FontSyncLog
CREATE NONCLUSTERED INDEX IX_FontSyncLog_SyncStartTime 
ON [log].[FontSyncLog](SyncStartTime DESC);
GO

CREATE NONCLUSTERED INDEX IX_FontSyncLog_SyncStatus 
ON [log].[FontSyncLog](SyncStatus);
GO

-- ============================================================================
-- FontSyncDetail: Individual font sync details
-- ============================================================================

IF OBJECT_ID('[log].[FontSyncDetail]', 'U') IS NOT NULL
    DROP TABLE [log].[FontSyncDetail];
GO

CREATE TABLE [log].[FontSyncDetail] (
    -- Primary Key
    FontSyncDetailID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Foreign Keys
    FontSyncLogID INT NOT NULL,
    FontFamilyID INT NULL,
    
    -- Font Identification
    GoogleFontID NVARCHAR(100) NULL,
    FamilyName NVARCHAR(200) NULL,
    
    -- Operation
    Operation NVARCHAR(20) NOT NULL,
    
    -- Change Details
    PreviousVersion NVARCHAR(20) NULL,
    NewVersion NVARCHAR(20) NULL,
    ChangeSummary NVARCHAR(500) NULL,
    
    -- Error
    ErrorMessage NVARCHAR(MAX) NULL,
    
    -- Audit
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    
    -- Foreign Key constraints
    CONSTRAINT FK_FontSyncDetail_FontSyncLog 
        FOREIGN KEY (FontSyncLogID) REFERENCES [log].[FontSyncLog](FontSyncLogID),
    CONSTRAINT FK_FontSyncDetail_FontFamily 
        FOREIGN KEY (FontFamilyID) REFERENCES [dbo].[FontFamily](FontFamilyID)
);
GO

-- Check constraint for Operation
ALTER TABLE [log].[FontSyncDetail]
ADD CONSTRAINT CK_FontSyncDetail_Operation 
CHECK (Operation IN ('Added', 'Updated', 'Deprecated', 'Removed', 'Unchanged', 'Error'));
GO

-- Indexes for FontSyncDetail
CREATE NONCLUSTERED INDEX IX_FontSyncDetail_FontSyncLogID 
ON [log].[FontSyncDetail](FontSyncLogID);
GO

CREATE NONCLUSTERED INDEX IX_FontSyncDetail_FontFamilyID 
ON [log].[FontSyncDetail](FontFamilyID);
GO

CREATE NONCLUSTERED INDEX IX_FontSyncDetail_Operation 
ON [log].[FontSyncDetail](Operation);
GO

-- ============================================================================
-- FontUsageLog: Track font usage in platform
-- ============================================================================

IF OBJECT_ID('[log].[FontUsageLog]', 'U') IS NOT NULL
    DROP TABLE [log].[FontUsageLog];
GO

CREATE TABLE [log].[FontUsageLog] (
    -- Primary Key
    FontUsageLogID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Font Reference
    FontFamilyID INT NOT NULL,
    FontVariantID INT NULL,
    
    -- Context
    UsageContext NVARCHAR(50) NOT NULL,
    ContextEntityType NVARCHAR(50) NULL,
    ContextEntityID INT NULL,
    
    -- User Context
    UserID INT NULL,
    CompanyID INT NULL,
    
    -- Action
    ActionType NVARCHAR(50) NOT NULL,
    
    -- Audit
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    IPAddress NVARCHAR(50) NULL,
    UserAgent NVARCHAR(500) NULL,
    
    -- Foreign Key constraints
    CONSTRAINT FK_FontUsageLog_FontFamily 
        FOREIGN KEY (FontFamilyID) REFERENCES [dbo].[FontFamily](FontFamilyID),
    CONSTRAINT FK_FontUsageLog_FontVariant 
        FOREIGN KEY (FontVariantID) REFERENCES [dbo].[FontVariant](FontVariantID)
);
GO

-- Check constraint for UsageContext
ALTER TABLE [log].[FontUsageLog]
ADD CONSTRAINT CK_FontUsageLog_UsageContext 
CHECK (UsageContext IN ('FormBuilder', 'TemplateCreation', 'Preview', 'Export', 'Settings'));
GO

-- Check constraint for ActionType
ALTER TABLE [log].[FontUsageLog]
ADD CONSTRAINT CK_FontUsageLog_ActionType 
CHECK (ActionType IN ('Selected', 'Applied', 'Previewed', 'Removed', 'Downloaded'));
GO

-- Indexes for FontUsageLog
CREATE NONCLUSTERED INDEX IX_FontUsageLog_FontFamilyID 
ON [log].[FontUsageLog](FontFamilyID);
GO

CREATE NONCLUSTERED INDEX IX_FontUsageLog_UserID 
ON [log].[FontUsageLog](UserID);
GO

CREATE NONCLUSTERED INDEX IX_FontUsageLog_CreatedDate 
ON [log].[FontUsageLog](CreatedDate DESC);
GO

CREATE NONCLUSTERED INDEX IX_FontUsageLog_UsageContext 
ON [log].[FontUsageLog](UsageContext, CreatedDate DESC);
GO

-- ============================================================================
-- VIEWS (for common queries)
-- ============================================================================

-- View: Active fonts with summary data
IF OBJECT_ID('[dbo].[vw_ActiveFonts]', 'V') IS NOT NULL
    DROP VIEW [dbo].[vw_ActiveFonts];
GO

CREATE VIEW [dbo].[vw_ActiveFonts]
AS
SELECT 
    ff.FontFamilyID,
    ff.FontSource,
    ff.GoogleFontID,
    ff.FamilyName,
    ff.InternalFontName,
    ff.Category,
    ff.Version,
    ff.LastModifiedDate,
    ff.IsVariableFont,
    ff.HasColorCapabilities,
    ff.MinWeight,
    ff.MaxWeight,
    ff.HasItalic,
    ff.TotalVariants,
    ff.TotalSubsets,
    ff.MenuFileUrl,
    ff.PopularityRank,
    ff.UsageCount,
    ff.IsFeatured,
    ff.IsRecommended,
    ff.Designer,
    ff.VariantList,
    ff.LastSyncDate,
    ff.UploadedByCompanyID
FROM [dbo].[FontFamily] ff
WHERE ff.IsDeleted = 0 
    AND ff.IsActive = 1
    AND ff.SyncStatus = 'Active';
GO

-- View: Company fonts with effective display name
IF OBJECT_ID('[dbo].[vw_CompanyFonts]', 'V') IS NOT NULL
    DROP VIEW [dbo].[vw_CompanyFonts];
GO

CREATE VIEW [dbo].[vw_CompanyFonts]
AS
SELECT 
    cf.CompanyFontID,
    cf.CompanyID,
    cf.FontFamilyID,
    COALESCE(cf.DisplayNameOverride, ff.FamilyName) AS EffectiveDisplayName,
    cf.DisplayNameOverride,
    ff.FamilyName AS OriginalFamilyName,
    ff.InternalFontName,
    ff.FontSource,
    ff.Category,
    ff.IsVariableFont,
    ff.MinWeight,
    ff.MaxWeight,
    ff.HasItalic,
    ff.TotalVariants,
    ff.MenuFileUrl,
    cf.IsOwner,
    cf.IsLicensed,
    cf.LicenseType,
    cf.LicenseExpiryDate,
    cf.GrantedDate,
    ff.UsageCount
FROM [dbo].[CompanyFont] cf
INNER JOIN [dbo].[FontFamily] ff ON cf.FontFamilyID = ff.FontFamilyID
WHERE cf.IsDeleted = 0 
    AND cf.IsActive = 1
    AND cf.IsLicensed = 1
    AND ff.IsDeleted = 0 
    AND ff.IsActive = 1;
GO

-- View: Font usage statistics
IF OBJECT_ID('[dbo].[vw_FontUsageStats]', 'V') IS NOT NULL
    DROP VIEW [dbo].[vw_FontUsageStats];
GO

CREATE VIEW [dbo].[vw_FontUsageStats]
AS
SELECT 
    ff.FontFamilyID,
    ff.FamilyName,
    ff.Category,
    COUNT(ful.FontUsageLogID) AS TotalUsageCount,
    COUNT(DISTINCT ful.UserID) AS UniqueUsers,
    COUNT(DISTINCT ful.CompanyID) AS UniqueCompanies,
    MAX(ful.CreatedDate) AS LastUsedDate
FROM [dbo].[FontFamily] ff
LEFT JOIN [log].[FontUsageLog] ful ON ff.FontFamilyID = ful.FontFamilyID
WHERE ff.IsDeleted = 0
GROUP BY ff.FontFamilyID, ff.FamilyName, ff.Category;
GO

-- ============================================================================
-- STORED PROCEDURES
-- ============================================================================

-- Procedure: Search fonts
IF OBJECT_ID('[dbo].[sp_SearchFonts]', 'P') IS NOT NULL
    DROP PROCEDURE [dbo].[sp_SearchFonts];
GO

CREATE PROCEDURE [dbo].[sp_SearchFonts]
    @Query NVARCHAR(200) = NULL,
    @Category NVARCHAR(50) = NULL,
    @Subset NVARCHAR(50) = NULL,
    @IsVariable BIT = NULL,
    @HasItalic BIT = NULL,
    @IsFeatured BIT = NULL,
    @SortBy NVARCHAR(20) = 'popularity',
    @PageNumber INT = 1,
    @PageSize INT = 20
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @Offset INT = (@PageNumber - 1) * @PageSize;
    
    -- Get total count
    DECLARE @TotalCount INT;
    SELECT @TotalCount = COUNT(*)
    FROM [dbo].[FontFamily] ff
    WHERE ff.IsDeleted = 0
        AND ff.IsActive = 1
        AND ff.SyncStatus = 'Active'
        AND (@Query IS NULL OR ff.FamilyNameNormalized LIKE '%' + LOWER(@Query) + '%')
        AND (@Category IS NULL OR ff.Category = @Category)
        AND (@Subset IS NULL OR 
            (@Subset = 'latin' AND ff.SupportsLatin = 1) OR
            (@Subset = 'cyrillic' AND ff.SupportsCyrillic = 1) OR
            (@Subset = 'greek' AND ff.SupportsGreek = 1) OR
            (@Subset = 'arabic' AND ff.SupportsArabic = 1) OR
            (@Subset = 'hebrew' AND ff.SupportsHebrew = 1) OR
            (@Subset = 'asian' AND ff.SupportsAsian = 1))
        AND (@IsVariable IS NULL OR ff.IsVariableFont = @IsVariable)
        AND (@HasItalic IS NULL OR ff.HasItalic = @HasItalic)
        AND (@IsFeatured IS NULL OR ff.IsFeatured = @IsFeatured);
    
    -- Return results
    SELECT 
        ff.FontFamilyID,
        ff.GoogleFontID,
        ff.FamilyName,
        ff.Category,
        ff.Version,
        ff.IsVariableFont,
        ff.MinWeight,
        ff.MaxWeight,
        ff.HasItalic,
        ff.TotalVariants,
        ff.TotalSubsets,
        ff.MenuFileUrl,
        ff.PopularityRank,
        ff.UsageCount,
        ff.IsFeatured,
        ff.IsRecommended,
        ff.VariantList,
        @TotalCount AS TotalCount
    FROM [dbo].[FontFamily] ff
    WHERE ff.IsDeleted = 0
        AND ff.IsActive = 1
        AND ff.SyncStatus = 'Active'
        AND (@Query IS NULL OR ff.FamilyNameNormalized LIKE '%' + LOWER(@Query) + '%')
        AND (@Category IS NULL OR ff.Category = @Category)
        AND (@Subset IS NULL OR 
            (@Subset = 'latin' AND ff.SupportsLatin = 1) OR
            (@Subset = 'cyrillic' AND ff.SupportsCyrillic = 1) OR
            (@Subset = 'greek' AND ff.SupportsGreek = 1) OR
            (@Subset = 'arabic' AND ff.SupportsArabic = 1) OR
            (@Subset = 'hebrew' AND ff.SupportsHebrew = 1) OR
            (@Subset = 'asian' AND ff.SupportsAsian = 1))
        AND (@IsVariable IS NULL OR ff.IsVariableFont = @IsVariable)
        AND (@HasItalic IS NULL OR ff.HasItalic = @HasItalic)
        AND (@IsFeatured IS NULL OR ff.IsFeatured = @IsFeatured)
    ORDER BY 
        CASE WHEN @SortBy = 'popularity' THEN ff.PopularityRank END ASC,
        CASE WHEN @SortBy = 'name' THEN ff.FamilyName END ASC,
        CASE WHEN @SortBy = 'date' THEN ff.LastModifiedDate END DESC,
        CASE WHEN @SortBy = 'featured' THEN ff.IsFeatured END DESC,
        ff.FamilyName ASC
    OFFSET @Offset ROWS
    FETCH NEXT @PageSize ROWS ONLY;
END;
GO

-- Procedure: Get font details with variants
IF OBJECT_ID('[dbo].[sp_GetFontDetails]', 'P') IS NOT NULL
    DROP PROCEDURE [dbo].[sp_GetFontDetails];
GO

CREATE PROCEDURE [dbo].[sp_GetFontDetails]
    @FontFamilyID INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Font family details
    SELECT 
        ff.*
    FROM [dbo].[FontFamily] ff
    WHERE ff.FontFamilyID = @FontFamilyID
        AND ff.IsDeleted = 0;
    
    -- Variants
    SELECT 
        fv.*
    FROM [dbo].[FontVariant] fv
    WHERE fv.FontFamilyID = @FontFamilyID
        AND fv.IsDeleted = 0
    ORDER BY fv.DisplayOrder, fv.Weight, fv.IsItalic;
    
    -- Subsets
    SELECT 
        fs.*
    FROM [dbo].[FontSubset] fs
    WHERE fs.FontFamilyID = @FontFamilyID
        AND fs.IsActive = 1
    ORDER BY fs.DisplayOrder;
    
    -- Axes (for variable fonts)
    SELECT 
        fa.*
    FROM [dbo].[FontAxis] fa
    WHERE fa.FontFamilyID = @FontFamilyID
        AND fa.IsActive = 1
    ORDER BY fa.DisplayOrder;
    
    -- Color capabilities
    SELECT 
        fc.*
    FROM [dbo].[FontColorCapability] fc
    WHERE fc.FontFamilyID = @FontFamilyID
        AND fc.IsActive = 1;
END;
GO

-- Procedure: Update font usage count
IF OBJECT_ID('[dbo].[sp_UpdateFontUsageCount]', 'P') IS NOT NULL
    DROP PROCEDURE [dbo].[sp_UpdateFontUsageCount];
GO

CREATE PROCEDURE [dbo].[sp_UpdateFontUsageCount]
    @FontFamilyID INT
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE [dbo].[FontFamily]
    SET UsageCount = UsageCount + 1,
        UpdatedDate = SYSUTCDATETIME(),
        UpdatedBy = 'SYSTEM'
    WHERE FontFamilyID = @FontFamilyID;
END;
GO

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

PRINT 'Google Fonts Domain Schema created successfully!';
PRINT '';
PRINT 'Tables created:';
PRINT '  - dbo.FontCategoryRef (reference)';
PRINT '  - dbo.FontSubsetRef (reference)';
PRINT '  - dbo.FontAxisRef (reference)';
PRINT '  - dbo.FontFamily (core - with FontSource, UploadedByCompanyID, InternalFontName)';
PRINT '  - dbo.FontVariant (core)';
PRINT '  - dbo.FontSubset (core)';
PRINT '  - dbo.FontAxis (core)';
PRINT '  - dbo.FontColorCapability (core)';
PRINT '  - dbo.CompanyFont (junction - with DisplayNameOverride)';
PRINT '  - dbo.FontFile (storage - with hash deduplication)';
PRINT '  - log.FontSyncLog (logging)';
PRINT '  - log.FontSyncDetail (logging)';
PRINT '  - log.FontUsageLog (logging)';
PRINT '';
PRINT 'Views created:';
PRINT '  - dbo.vw_ActiveFonts';
PRINT '  - dbo.vw_CompanyFonts';
PRINT '  - dbo.vw_FontUsageStats';
PRINT '';
PRINT 'Stored procedures created:';
PRINT '  - dbo.sp_SearchFonts';
PRINT '  - dbo.sp_GetFontDetails';
PRINT '  - dbo.sp_UpdateFontUsageCount';
PRINT '';
PRINT 'Key features:';
PRINT '  - FontSource column for tracking Google/Custom/System fonts';
PRINT '  - DisplayNameOverride for per-company font aliases';
PRINT '  - FileHash-based deduplication for uploaded fonts';
PRINT '  - Full font metadata extraction from uploaded files';
GO

