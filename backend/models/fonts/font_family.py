"""
FontFamily Model (dbo.FontFamily)
Primary font registry for Google Fonts caching AND custom corporate fonts
"""
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontFamily(Base):
    """
    Font family model representing cached Google Fonts and custom corporate fonts.
    
    Features:
    - Complete font metadata from Google Fonts API
    - Custom corporate font uploads with validation
    - Variable font support (axes)
    - Platform-specific metadata (popularity, featured, recommended)
    - Sync tracking for monthly updates
    - Usage analytics integration
    
    Attributes:
        FontFamilyID: Primary key
        FontSource: Origin of font ('Google', 'Custom', 'System')
        UploadedByCompanyID: Company that uploaded custom font (NULL for Google fonts)
        GoogleFontID: Google's unique identifier (NULL for custom fonts)
        FamilyName: Display name (e.g., "Roboto")
        FamilyNameNormalized: Lowercase for search
        InternalFontName: Name extracted from font file metadata
        InternalVersion: Version from font file metadata
        Category: Font classification (serif, sans-serif, etc.)
        Version: Font version from Google
        LastModifiedDate: Last update date from Google API
        IsVariableFont: Has variable font axes
        HasColorCapabilities: Has color font features
        PopularityRank: Platform popularity ranking
        UsageCount: Times used in platform forms
        IsFeatured: Curated featured font
        IsRecommended: Recommended for users
    """
    
    __tablename__ = "FontFamily"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key (INT IDENTITY per project standards)
    FontFamilyID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Font Source (Google, Custom, System)
    FontSource = Column(String(20), nullable=False, default='Google', index=True)
    UploadedByCompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True, index=True)
    
    # Core Identification
    GoogleFontID = Column(String(100), nullable=True, unique=True, index=True)  # NULL for custom fonts
    FamilyName = Column(String(200), nullable=False, index=True)
    FamilyNameNormalized = Column(String(200), nullable=False, index=True)
    
    # Internal font metadata (extracted from font file)
    InternalFontName = Column(String(200), nullable=True)
    InternalVersion = Column(String(50), nullable=True)
    
    # Classification
    Category = Column(String(50), nullable=False, index=True)
    SubCategory = Column(String(100), nullable=True)
    
    # Version & Updates
    Version = Column(String(20), nullable=False)
    VersionNumber = Column(Integer, nullable=True)
    LastModifiedDate = Column(Date, nullable=False)
    
    # URLs
    MenuFileUrl = Column(String(500), nullable=True)
    SpecimenUrl = Column(String(500), nullable=True)
    
    # Font Characteristics
    IsVariableFont = Column(Boolean, nullable=False, default=False)
    HasColorCapabilities = Column(Boolean, nullable=False, default=False)
    
    # Weight & Style Range
    MinWeight = Column(Integer, nullable=True)
    MaxWeight = Column(Integer, nullable=True)
    HasItalic = Column(Boolean, nullable=False, default=False)
    HasRegular = Column(Boolean, nullable=False, default=True)
    
    # Subset Summary (for quick filtering)
    SupportsLatin = Column(Boolean, nullable=False, default=True)
    SupportsCyrillic = Column(Boolean, nullable=False, default=False)
    SupportsGreek = Column(Boolean, nullable=False, default=False)
    SupportsArabic = Column(Boolean, nullable=False, default=False)
    SupportsHebrew = Column(Boolean, nullable=False, default=False)
    SupportsAsian = Column(Boolean, nullable=False, default=False)
    TotalSubsets = Column(Integer, nullable=False, default=1)
    
    # Variant Summary
    TotalVariants = Column(Integer, nullable=False, default=1)
    VariantList = Column(String(500), nullable=True)
    
    # Platform Metadata (EventLead-specific)
    PopularityRank = Column(Integer, nullable=True, index=True)
    UsageCount = Column(Integer, nullable=False, default=0)
    IsRecommended = Column(Boolean, nullable=False, default=False)
    IsFeatured = Column(Boolean, nullable=False, default=False, index=True)
    DisplayOrder = Column(Integer, nullable=True)
    
    # Licensing
    LicenseType = Column(String(100), nullable=True, default='Open Font License')
    LicenseUrl = Column(String(500), nullable=True)
    
    # Designer/Foundry
    Designer = Column(String(200), nullable=True)
    DesignerUrl = Column(String(500), nullable=True)
    Foundry = Column(String(200), nullable=True)
    
    # Sync Metadata
    FirstSyncDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    LastSyncDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    SyncVersion = Column(Integer, nullable=False, default=1)
    SyncStatus = Column(String(20), nullable=False, default='Active')
    
    # Audit Trail
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(String(100), nullable=False, default='SYSTEM')
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(String(100), nullable=True)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(String(100), nullable=True)
    
    # Relationships
    variants = relationship("FontVariant", back_populates="font_family", lazy="dynamic")
    subsets = relationship("FontSubset", back_populates="font_family", lazy="dynamic")
    axes = relationship("FontAxis", back_populates="font_family", lazy="dynamic")
    color_capabilities = relationship("FontColorCapability", back_populates="font_family", lazy="dynamic")
    usage_logs = relationship("FontUsageLog", back_populates="font_family", lazy="dynamic")
    
    # Company relationships
    uploaded_by_company = relationship("Company", foreign_keys=[UploadedByCompanyID])
    company_fonts = relationship("CompanyFont", back_populates="font_family", lazy="dynamic")
    
    def __repr__(self) -> str:
        return f"<FontFamily(FontFamilyID={self.FontFamilyID}, FamilyName='{self.FamilyName}', FontSource='{self.FontSource}')>"

