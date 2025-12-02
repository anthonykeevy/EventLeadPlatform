"""
Google Fonts Domain - Complete schema with custom font support

This migration creates the complete Google Fonts domain including:
- Reference tables (FontCategoryRef, FontSubsetRef, FontAxisRef)
- Core tables (FontFamily with FontSource, FontVariant, FontSubset, FontAxis, FontColorCapability)
- Company-Font junction table (CompanyFont with DisplayNameOverride)
- Font file storage (FontFile with hash-based deduplication)
- Logging tables (FontSyncLog, FontSyncDetail, FontUsageLog)

Revision ID: 031_google_fonts_domain
Revises: 030_add_form_version_table
Create Date: 2025-12-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql
from datetime import datetime

# revision identifiers
revision = '031_google_fonts_domain'
down_revision = '030'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # =========================================================================
    # REFERENCE TABLES
    # =========================================================================
    
    # FontCategoryRef - Font category definitions
    op.create_table(
        'FontCategoryRef',
        sa.Column('CategoryCode', sa.String(50), primary_key=True),
        sa.Column('CategoryName', sa.String(100), nullable=False),
        sa.Column('Description', sa.String(500), nullable=True),
        sa.Column('DisplayOrder', sa.Integer, nullable=False, server_default='0'),
        sa.Column('IconClass', sa.String(100), nullable=True),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='dbo'
    )
    
    # Seed font categories
    op.execute("""
        INSERT INTO dbo.FontCategoryRef (CategoryCode, CategoryName, Description, DisplayOrder, IconClass) VALUES
        ('serif', 'Serif', 'Traditional fonts with decorative strokes (serifs) at the ends of letters. Best for print and formal documents.', 1, 'icon-font-serif'),
        ('sans-serif', 'Sans Serif', 'Modern, clean fonts without decorative strokes. Excellent for digital interfaces and contemporary designs.', 2, 'icon-font-sans'),
        ('display', 'Display', 'Decorative fonts designed for headlines and large text. Use sparingly for impact.', 3, 'icon-font-display'),
        ('handwriting', 'Handwriting', 'Script and handwritten style fonts. Perfect for personal touches and creative projects.', 4, 'icon-font-handwriting'),
        ('monospace', 'Monospace', 'Fixed-width fonts where each character takes the same space. Ideal for code and technical content.', 5, 'icon-font-mono')
    """)
    
    # FontSubsetRef - Character set/language support definitions
    op.create_table(
        'FontSubsetRef',
        sa.Column('SubsetCode', sa.String(50), primary_key=True),
        sa.Column('SubsetName', sa.String(100), nullable=False),
        sa.Column('SubsetGroup', sa.String(50), nullable=False),
        sa.Column('Description', sa.String(500), nullable=True),
        sa.Column('PrimaryLanguages', sa.String(500), nullable=True),
        sa.Column('DisplayOrder', sa.Integer, nullable=False, server_default='0'),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='dbo'
    )
    
    # Seed font subsets
    op.execute("""
        INSERT INTO dbo.FontSubsetRef (SubsetCode, SubsetName, SubsetGroup, PrimaryLanguages, DisplayOrder) VALUES
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
        ('gujarati', 'Gujarati', 'Asian', 'Gujarati', 21)
    """)
    
    # FontAxisRef - Variable font axis definitions
    op.create_table(
        'FontAxisRef',
        sa.Column('AxisTag', sa.String(10), primary_key=True),
        sa.Column('AxisName', sa.String(100), nullable=False),
        sa.Column('Description', sa.String(500), nullable=True),
        sa.Column('IsStandard', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('DefaultMin', sa.Numeric(10, 4), nullable=True),
        sa.Column('DefaultMax', sa.Numeric(10, 4), nullable=True),
        sa.Column('CssProperty', sa.String(100), nullable=True),
        sa.Column('DisplayOrder', sa.Integer, nullable=False, server_default='0'),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='dbo'
    )
    
    # Seed standard font axes
    op.execute("""
        INSERT INTO dbo.FontAxisRef (AxisTag, AxisName, Description, IsStandard, DefaultMin, DefaultMax, CssProperty, DisplayOrder) VALUES
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
        ('WONK', 'Wonky', 'Controls irregularity/playfulness', 0, 0, 1, NULL, 14)
    """)
    
    # =========================================================================
    # CORE TABLES
    # =========================================================================
    
    # FontFamily - Primary font registry (with custom font support)
    op.create_table(
        'FontFamily',
        sa.Column('FontFamilyID', sa.Integer, primary_key=True, autoincrement=True),
        # Font Source
        sa.Column('FontSource', sa.String(20), nullable=False, server_default='Google'),
        sa.Column('UploadedByCompanyID', sa.BigInteger, sa.ForeignKey('dbo.Company.CompanyID'), nullable=True),
        # Core Identification
        sa.Column('GoogleFontID', sa.String(100), nullable=True),  # NULL for custom fonts
        sa.Column('FamilyName', sa.String(200), nullable=False),
        sa.Column('FamilyNameNormalized', sa.String(200), nullable=False),
        # Internal font metadata
        sa.Column('InternalFontName', sa.String(200), nullable=True),
        sa.Column('InternalVersion', sa.String(50), nullable=True),
        # Classification
        sa.Column('Category', sa.String(50), nullable=False),
        sa.Column('SubCategory', sa.String(100), nullable=True),
        # Version & Updates
        sa.Column('Version', sa.String(20), nullable=False),
        sa.Column('VersionNumber', sa.Integer, nullable=True),
        sa.Column('LastModifiedDate', sa.Date, nullable=False),
        # URLs
        sa.Column('MenuFileUrl', sa.String(500), nullable=True),
        sa.Column('SpecimenUrl', sa.String(500), nullable=True),
        # Font Characteristics
        sa.Column('IsVariableFont', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('HasColorCapabilities', sa.Boolean, nullable=False, server_default='0'),
        # Weight & Style Range
        sa.Column('MinWeight', sa.Integer, nullable=True),
        sa.Column('MaxWeight', sa.Integer, nullable=True),
        sa.Column('HasItalic', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('HasRegular', sa.Boolean, nullable=False, server_default='1'),
        # Subset Summary
        sa.Column('SupportsLatin', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('SupportsCyrillic', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('SupportsGreek', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('SupportsArabic', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('SupportsHebrew', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('SupportsAsian', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('TotalSubsets', sa.Integer, nullable=False, server_default='1'),
        # Variant Summary
        sa.Column('TotalVariants', sa.Integer, nullable=False, server_default='1'),
        sa.Column('VariantList', sa.String(500), nullable=True),
        # Platform Metadata
        sa.Column('PopularityRank', sa.Integer, nullable=True),
        sa.Column('UsageCount', sa.Integer, nullable=False, server_default='0'),
        sa.Column('IsRecommended', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('IsFeatured', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('DisplayOrder', sa.Integer, nullable=True),
        # Licensing
        sa.Column('LicenseType', sa.String(100), nullable=True, server_default="'Open Font License'"),
        sa.Column('LicenseUrl', sa.String(500), nullable=True),
        # Designer/Foundry
        sa.Column('Designer', sa.String(200), nullable=True),
        sa.Column('DesignerUrl', sa.String(500), nullable=True),
        sa.Column('Foundry', sa.String(200), nullable=True),
        # Sync Metadata
        sa.Column('FirstSyncDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('LastSyncDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('SyncVersion', sa.Integer, nullable=False, server_default='1'),
        sa.Column('SyncStatus', sa.String(20), nullable=False, server_default="'Active'"),
        # Audit Trail
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('IsDeleted', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('CreatedBy', sa.String(100), nullable=False, server_default="'SYSTEM'"),
        sa.Column('UpdatedDate', sa.DateTime, nullable=True),
        sa.Column('UpdatedBy', sa.String(100), nullable=True),
        sa.Column('DeletedDate', sa.DateTime, nullable=True),
        sa.Column('DeletedBy', sa.String(100), nullable=True),
        schema='dbo'
    )
    
    # FontFamily indexes
    op.create_index('IX_FontFamily_GoogleFontID', 'FontFamily', ['GoogleFontID'], 
                    schema='dbo', unique=True, 
                    mssql_where='GoogleFontID IS NOT NULL')
    op.create_index('IX_FontFamily_FamilyName', 'FontFamily', ['FamilyName'], schema='dbo')
    op.create_index('IX_FontFamily_FamilyNameNormalized', 'FontFamily', ['FamilyNameNormalized'], schema='dbo')
    op.create_index('IX_FontFamily_Category', 'FontFamily', ['Category'], schema='dbo')
    op.create_index('IX_FontFamily_FontSource', 'FontFamily', ['FontSource'], schema='dbo')
    op.create_index('IX_FontFamily_PopularityRank', 'FontFamily', ['PopularityRank'], schema='dbo')
    op.create_index('IX_FontFamily_UploadedByCompanyID', 'FontFamily', ['UploadedByCompanyID'], 
                    schema='dbo', mssql_where='UploadedByCompanyID IS NOT NULL')
    
    # FontFamily check constraints
    op.execute("""
        ALTER TABLE dbo.FontFamily ADD CONSTRAINT CK_FontFamily_FontSource 
        CHECK (FontSource IN ('Google', 'Custom', 'System'))
    """)
    op.execute("""
        ALTER TABLE dbo.FontFamily ADD CONSTRAINT CK_FontFamily_Category 
        CHECK (Category IN ('serif', 'sans-serif', 'display', 'handwriting', 'monospace'))
    """)
    op.execute("""
        ALTER TABLE dbo.FontFamily ADD CONSTRAINT CK_FontFamily_SyncStatus 
        CHECK (SyncStatus IN ('Active', 'Deprecated', 'Removed', 'Pending'))
    """)
    
    # FontVariant - Weight/style combinations
    op.create_table(
        'FontVariant',
        sa.Column('FontVariantID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FontFamilyID', sa.Integer, sa.ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False),
        sa.Column('VariantName', sa.String(50), nullable=False),
        sa.Column('VariantNameNormalized', sa.String(50), nullable=False),
        sa.Column('Weight', sa.Integer, nullable=False, server_default='400'),
        sa.Column('WeightName', sa.String(50), nullable=True),
        sa.Column('IsItalic', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('TtfFileUrl', sa.String(500), nullable=True),
        sa.Column('WoffFileUrl', sa.String(500), nullable=True),
        sa.Column('Woff2FileUrl', sa.String(500), nullable=True),
        sa.Column('IsFileCached', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('CachedFilePath', sa.String(500), nullable=True),
        sa.Column('FileSizeBytes', sa.BigInteger, nullable=True),
        sa.Column('FileHash', sa.String(64), nullable=True),
        sa.Column('DisplayOrder', sa.Integer, nullable=False, server_default='0'),
        sa.Column('IsDefault', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('IsDeleted', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('UpdatedDate', sa.DateTime, nullable=True),
        schema='dbo'
    )
    
    op.create_index('IX_FontVariant_FontFamilyID', 'FontVariant', ['FontFamilyID'], schema='dbo')
    op.create_index('IX_FontVariant_Weight', 'FontVariant', ['Weight', 'IsItalic'], schema='dbo')
    op.execute("""
        ALTER TABLE dbo.FontVariant ADD CONSTRAINT UQ_FontVariant_Family_Variant 
        UNIQUE (FontFamilyID, VariantName)
    """)
    
    # FontSubset - Character set support
    op.create_table(
        'FontSubset',
        sa.Column('FontSubsetID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FontFamilyID', sa.Integer, sa.ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False),
        sa.Column('SubsetCode', sa.String(50), nullable=False),
        sa.Column('SubsetName', sa.String(100), nullable=False),
        sa.Column('SubsetGroup', sa.String(50), nullable=True),
        sa.Column('IsExtended', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('PrimaryLanguages', sa.String(500), nullable=True),
        sa.Column('DisplayOrder', sa.Integer, nullable=False, server_default='0'),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='dbo'
    )
    
    op.create_index('IX_FontSubset_FontFamilyID', 'FontSubset', ['FontFamilyID'], schema='dbo')
    op.create_index('IX_FontSubset_SubsetCode', 'FontSubset', ['SubsetCode'], schema='dbo')
    op.execute("""
        ALTER TABLE dbo.FontSubset ADD CONSTRAINT UQ_FontSubset_Family_Subset 
        UNIQUE (FontFamilyID, SubsetCode)
    """)
    
    # FontAxis - Variable font axes
    op.create_table(
        'FontAxis',
        sa.Column('FontAxisID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FontFamilyID', sa.Integer, sa.ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False),
        sa.Column('AxisTag', sa.String(10), nullable=False),
        sa.Column('AxisName', sa.String(100), nullable=False),
        sa.Column('MinValue', sa.Numeric(10, 4), nullable=False),
        sa.Column('MaxValue', sa.Numeric(10, 4), nullable=False),
        sa.Column('DefaultValue', sa.Numeric(10, 4), nullable=True),
        sa.Column('Step', sa.Numeric(10, 4), nullable=True),
        sa.Column('IsStandard', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('IsRegistered', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('DisplayOrder', sa.Integer, nullable=False, server_default='0'),
        sa.Column('CssProperty', sa.String(100), nullable=True),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='dbo'
    )
    
    op.create_index('IX_FontAxis_FontFamilyID', 'FontAxis', ['FontFamilyID'], schema='dbo')
    op.create_index('IX_FontAxis_AxisTag', 'FontAxis', ['AxisTag'], schema='dbo')
    op.execute("""
        ALTER TABLE dbo.FontAxis ADD CONSTRAINT UQ_FontAxis_Family_Tag 
        UNIQUE (FontFamilyID, AxisTag)
    """)
    
    # FontColorCapability - Color font capabilities
    op.create_table(
        'FontColorCapability',
        sa.Column('FontColorCapabilityID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FontFamilyID', sa.Integer, sa.ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False),
        sa.Column('CapabilityCode', sa.String(20), nullable=False),
        sa.Column('CapabilityName', sa.String(100), nullable=False),
        sa.Column('CapabilityVersion', sa.String(20), nullable=True),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='dbo'
    )
    
    op.create_index('IX_FontColorCapability_FontFamilyID', 'FontColorCapability', ['FontFamilyID'], schema='dbo')
    op.execute("""
        ALTER TABLE dbo.FontColorCapability ADD CONSTRAINT UQ_FontColorCapability_Family_Code 
        UNIQUE (FontFamilyID, CapabilityCode)
    """)
    
    # =========================================================================
    # COMPANY-FONT JUNCTION TABLE
    # =========================================================================
    
    # CompanyFont - Company-Font relationship with display name override
    op.create_table(
        'CompanyFont',
        sa.Column('CompanyFontID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('CompanyID', sa.BigInteger, sa.ForeignKey('dbo.Company.CompanyID'), nullable=False),
        sa.Column('FontFamilyID', sa.Integer, sa.ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False),
        # Per-company display name override
        sa.Column('DisplayNameOverride', sa.String(200), nullable=True),
        # Relationship type
        sa.Column('IsOwner', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('IsLicensed', sa.Boolean, nullable=False, server_default='1'),
        # License tracking
        sa.Column('LicenseType', sa.String(50), nullable=True),
        sa.Column('LicenseExpiryDate', sa.Date, nullable=True),
        sa.Column('LicenseNotes', sa.String(500), nullable=True),
        # Audit
        sa.Column('GrantedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('GrantedBy', sa.BigInteger, sa.ForeignKey('dbo.User.UserID'), nullable=True),
        sa.Column('RevokedDate', sa.DateTime, nullable=True),
        sa.Column('RevokedBy', sa.BigInteger, sa.ForeignKey('dbo.User.UserID'), nullable=True),
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('IsDeleted', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('CreatedBy', sa.String(100), nullable=False, server_default="'SYSTEM'"),
        sa.Column('UpdatedDate', sa.DateTime, nullable=True),
        sa.Column('UpdatedBy', sa.String(100), nullable=True),
        schema='dbo'
    )
    
    op.create_index('IX_CompanyFont_CompanyID', 'CompanyFont', ['CompanyID'], schema='dbo')
    op.create_index('IX_CompanyFont_FontFamilyID', 'CompanyFont', ['FontFamilyID'], schema='dbo')
    op.execute("""
        ALTER TABLE dbo.CompanyFont ADD CONSTRAINT UQ_CompanyFont_Company_Font 
        UNIQUE (CompanyID, FontFamilyID)
    """)
    op.execute("""
        ALTER TABLE dbo.CompanyFont ADD CONSTRAINT CK_CompanyFont_LicenseType 
        CHECK (LicenseType IS NULL OR LicenseType IN ('Owned', 'Shared', 'Platform', 'Trial'))
    """)
    
    # =========================================================================
    # FONT FILE STORAGE (with deduplication)
    # =========================================================================
    
    # FontFile - Uploaded font files with hash-based deduplication
    op.create_table(
        'FontFile',
        sa.Column('FontFileID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FontVariantID', sa.Integer, sa.ForeignKey('dbo.FontVariant.FontVariantID'), nullable=False),
        # File storage
        sa.Column('FileFormat', sa.String(10), nullable=False),
        sa.Column('FileData', mssql.VARBINARY(None), nullable=False),  # VARBINARY(MAX)
        sa.Column('FileSizeBytes', sa.BigInteger, nullable=False),
        sa.Column('FileHash', sa.String(64), nullable=False, unique=True),  # SHA-256
        sa.Column('MimeType', sa.String(100), nullable=False),
        sa.Column('OriginalFileName', sa.String(255), nullable=True),
        # Extracted metadata
        sa.Column('ExtractedFontName', sa.String(200), nullable=True),
        sa.Column('ExtractedFamily', sa.String(200), nullable=True),
        sa.Column('ExtractedSubfamily', sa.String(200), nullable=True),
        sa.Column('ExtractedVersion', sa.String(50), nullable=True),
        sa.Column('ExtractedCopyright', sa.String(500), nullable=True),
        sa.Column('ExtractedLicense', sa.String(500), nullable=True),
        sa.Column('ExtractedDesigner', sa.String(200), nullable=True),
        sa.Column('ExtractedVendor', sa.String(200), nullable=True),
        sa.Column('SupportedScripts', sa.String(500), nullable=True),
        sa.Column('GlyphCount', sa.Integer, nullable=True),
        sa.Column('UnitsPerEm', sa.Integer, nullable=True),
        # Validation
        sa.Column('IsValid', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('ValidationDate', sa.DateTime, nullable=True),
        sa.Column('ValidationErrors', sa.Text, nullable=True),
        # Audit
        sa.Column('IsActive', sa.Boolean, nullable=False, server_default='1'),
        sa.Column('IsDeleted', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('CreatedBy', sa.BigInteger, sa.ForeignKey('dbo.User.UserID'), nullable=True),
        schema='dbo'
    )
    
    op.create_index('IX_FontFile_FontVariantID', 'FontFile', ['FontVariantID'], schema='dbo')
    op.create_index('IX_FontFile_FileHash', 'FontFile', ['FileHash'], schema='dbo')
    op.execute("""
        ALTER TABLE dbo.FontFile ADD CONSTRAINT CK_FontFile_Format 
        CHECK (FileFormat IN ('ttf', 'otf', 'woff', 'woff2', 'eot'))
    """)
    
    # =========================================================================
    # LOGGING TABLES
    # =========================================================================
    
    # FontSyncLog - Sync operation tracking
    op.create_table(
        'FontSyncLog',
        sa.Column('FontSyncLogID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('SyncStartTime', sa.DateTime, nullable=False),
        sa.Column('SyncEndTime', sa.DateTime, nullable=True),
        sa.Column('SyncStatus', sa.String(20), nullable=False, server_default="'Running'"),
        # Metrics
        sa.Column('TotalFontsInAPI', sa.Integer, nullable=True),
        sa.Column('FontsAdded', sa.Integer, nullable=False, server_default='0'),
        sa.Column('FontsUpdated', sa.Integer, nullable=False, server_default='0'),
        sa.Column('FontsDeprecated', sa.Integer, nullable=False, server_default='0'),
        sa.Column('FontsRemoved', sa.Integer, nullable=False, server_default='0'),
        sa.Column('FontsUnchanged', sa.Integer, nullable=False, server_default='0'),
        sa.Column('VariantsProcessed', sa.Integer, nullable=False, server_default='0'),
        sa.Column('SubsetsProcessed', sa.Integer, nullable=False, server_default='0'),
        sa.Column('AxesProcessed', sa.Integer, nullable=False, server_default='0'),
        # API Details
        sa.Column('APIEndpoint', sa.String(500), nullable=True),
        sa.Column('APIVersion', sa.String(20), nullable=True),
        sa.Column('APIResponseTimeMs', sa.Integer, nullable=True),
        sa.Column('APIResponseSizeBytes', sa.BigInteger, nullable=True),
        # Error Handling
        sa.Column('ErrorMessage', sa.Text, nullable=True),
        sa.Column('ErrorDetails', sa.Text, nullable=True),
        sa.Column('RetryCount', sa.Integer, nullable=False, server_default='0'),
        # Trigger
        sa.Column('TriggerType', sa.String(50), nullable=False, server_default="'Scheduled'"),
        sa.Column('TriggeredBy', sa.String(100), nullable=True),
        # Audit
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='log'
    )
    
    op.create_index('IX_FontSyncLog_SyncStartTime', 'FontSyncLog', ['SyncStartTime'], schema='log')
    op.create_index('IX_FontSyncLog_SyncStatus', 'FontSyncLog', ['SyncStatus'], schema='log')
    op.execute("""
        ALTER TABLE log.FontSyncLog ADD CONSTRAINT CK_FontSyncLog_SyncStatus 
        CHECK (SyncStatus IN ('Running', 'Success', 'Failed', 'Partial', 'Cancelled'))
    """)
    op.execute("""
        ALTER TABLE log.FontSyncLog ADD CONSTRAINT CK_FontSyncLog_TriggerType 
        CHECK (TriggerType IN ('Scheduled', 'Manual', 'Webhook', 'Startup'))
    """)
    
    # FontSyncDetail - Individual font sync details
    op.create_table(
        'FontSyncDetail',
        sa.Column('FontSyncDetailID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FontSyncLogID', sa.Integer, sa.ForeignKey('log.FontSyncLog.FontSyncLogID'), nullable=False),
        sa.Column('FontFamilyID', sa.Integer, sa.ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=True),
        sa.Column('GoogleFontID', sa.String(100), nullable=True),
        sa.Column('FamilyName', sa.String(200), nullable=True),
        sa.Column('Operation', sa.String(20), nullable=False),
        sa.Column('PreviousVersion', sa.String(20), nullable=True),
        sa.Column('NewVersion', sa.String(20), nullable=True),
        sa.Column('ChangeSummary', sa.String(500), nullable=True),
        sa.Column('ErrorMessage', sa.Text, nullable=True),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        schema='log'
    )
    
    op.create_index('IX_FontSyncDetail_FontSyncLogID', 'FontSyncDetail', ['FontSyncLogID'], schema='log')
    op.create_index('IX_FontSyncDetail_FontFamilyID', 'FontSyncDetail', ['FontFamilyID'], schema='log')
    op.create_index('IX_FontSyncDetail_Operation', 'FontSyncDetail', ['Operation'], schema='log')
    op.execute("""
        ALTER TABLE log.FontSyncDetail ADD CONSTRAINT CK_FontSyncDetail_Operation 
        CHECK (Operation IN ('Added', 'Updated', 'Deprecated', 'Removed', 'Unchanged', 'Error'))
    """)
    
    # FontUsageLog - Font usage tracking
    op.create_table(
        'FontUsageLog',
        sa.Column('FontUsageLogID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('FontFamilyID', sa.Integer, sa.ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False),
        sa.Column('FontVariantID', sa.Integer, sa.ForeignKey('dbo.FontVariant.FontVariantID'), nullable=True),
        sa.Column('UsageContext', sa.String(50), nullable=False),
        sa.Column('ContextEntityType', sa.String(50), nullable=True),
        sa.Column('ContextEntityID', sa.Integer, nullable=True),
        sa.Column('UserID', sa.Integer, nullable=True),
        sa.Column('CompanyID', sa.Integer, nullable=True),
        sa.Column('ActionType', sa.String(50), nullable=False),
        sa.Column('CreatedDate', sa.DateTime, nullable=False, server_default=sa.func.getutcdate()),
        sa.Column('IPAddress', sa.String(50), nullable=True),
        sa.Column('UserAgent', sa.String(500), nullable=True),
        schema='log'
    )
    
    op.create_index('IX_FontUsageLog_FontFamilyID', 'FontUsageLog', ['FontFamilyID'], schema='log')
    op.create_index('IX_FontUsageLog_UserID', 'FontUsageLog', ['UserID'], schema='log')
    op.create_index('IX_FontUsageLog_CreatedDate', 'FontUsageLog', ['CreatedDate'], schema='log')
    op.create_index('IX_FontUsageLog_UsageContext', 'FontUsageLog', ['UsageContext', 'CreatedDate'], schema='log')
    op.execute("""
        ALTER TABLE log.FontUsageLog ADD CONSTRAINT CK_FontUsageLog_UsageContext 
        CHECK (UsageContext IN ('FormBuilder', 'TemplateCreation', 'Preview', 'Export', 'Settings'))
    """)
    op.execute("""
        ALTER TABLE log.FontUsageLog ADD CONSTRAINT CK_FontUsageLog_ActionType 
        CHECK (ActionType IN ('Selected', 'Applied', 'Previewed', 'Removed', 'Downloaded'))
    """)


def downgrade() -> None:
    # Drop in reverse order of creation
    
    # Logging tables
    op.drop_index('IX_FontUsageLog_UsageContext', 'FontUsageLog', schema='log')
    op.drop_index('IX_FontUsageLog_CreatedDate', 'FontUsageLog', schema='log')
    op.drop_index('IX_FontUsageLog_UserID', 'FontUsageLog', schema='log')
    op.drop_index('IX_FontUsageLog_FontFamilyID', 'FontUsageLog', schema='log')
    op.drop_table('FontUsageLog', schema='log')
    
    op.drop_index('IX_FontSyncDetail_Operation', 'FontSyncDetail', schema='log')
    op.drop_index('IX_FontSyncDetail_FontFamilyID', 'FontSyncDetail', schema='log')
    op.drop_index('IX_FontSyncDetail_FontSyncLogID', 'FontSyncDetail', schema='log')
    op.drop_table('FontSyncDetail', schema='log')
    
    op.drop_index('IX_FontSyncLog_SyncStatus', 'FontSyncLog', schema='log')
    op.drop_index('IX_FontSyncLog_SyncStartTime', 'FontSyncLog', schema='log')
    op.drop_table('FontSyncLog', schema='log')
    
    # Font file storage
    op.drop_index('IX_FontFile_FileHash', 'FontFile', schema='dbo')
    op.drop_index('IX_FontFile_FontVariantID', 'FontFile', schema='dbo')
    op.drop_table('FontFile', schema='dbo')
    
    # Company-Font junction
    op.drop_index('IX_CompanyFont_FontFamilyID', 'CompanyFont', schema='dbo')
    op.drop_index('IX_CompanyFont_CompanyID', 'CompanyFont', schema='dbo')
    op.drop_table('CompanyFont', schema='dbo')
    
    # Core tables
    op.drop_index('IX_FontColorCapability_FontFamilyID', 'FontColorCapability', schema='dbo')
    op.drop_table('FontColorCapability', schema='dbo')
    
    op.drop_index('IX_FontAxis_AxisTag', 'FontAxis', schema='dbo')
    op.drop_index('IX_FontAxis_FontFamilyID', 'FontAxis', schema='dbo')
    op.drop_table('FontAxis', schema='dbo')
    
    op.drop_index('IX_FontSubset_SubsetCode', 'FontSubset', schema='dbo')
    op.drop_index('IX_FontSubset_FontFamilyID', 'FontSubset', schema='dbo')
    op.drop_table('FontSubset', schema='dbo')
    
    op.drop_index('IX_FontVariant_Weight', 'FontVariant', schema='dbo')
    op.drop_index('IX_FontVariant_FontFamilyID', 'FontVariant', schema='dbo')
    op.drop_table('FontVariant', schema='dbo')
    
    op.drop_index('IX_FontFamily_UploadedByCompanyID', 'FontFamily', schema='dbo')
    op.drop_index('IX_FontFamily_PopularityRank', 'FontFamily', schema='dbo')
    op.drop_index('IX_FontFamily_FontSource', 'FontFamily', schema='dbo')
    op.drop_index('IX_FontFamily_Category', 'FontFamily', schema='dbo')
    op.drop_index('IX_FontFamily_FamilyNameNormalized', 'FontFamily', schema='dbo')
    op.drop_index('IX_FontFamily_FamilyName', 'FontFamily', schema='dbo')
    op.drop_index('IX_FontFamily_GoogleFontID', 'FontFamily', schema='dbo')
    op.drop_table('FontFamily', schema='dbo')
    
    # Reference tables
    op.drop_table('FontAxisRef', schema='dbo')
    op.drop_table('FontSubsetRef', schema='dbo')
    op.drop_table('FontCategoryRef', schema='dbo')

