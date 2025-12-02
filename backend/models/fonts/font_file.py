"""
FontFile Model (dbo.FontFile)
Uploaded font file storage with hash-based deduplication
"""
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, LargeBinary, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontFile(Base):
    """
    Font file storage model with hash-based deduplication.
    
    Features:
    - SHA-256 hash-based deduplication (unique constraint on FileHash)
    - Full metadata extraction from uploaded font files
    - Validation status tracking
    - Support for TTF, OTF, WOFF, WOFF2 formats
    
    Attributes:
        FontFileID: Primary key
        FontVariantID: Foreign key to FontVariant
        FileFormat: Font file format ('ttf', 'otf', 'woff', 'woff2')
        FileData: Actual font file bytes
        FileSizeBytes: File size for display/limits
        FileHash: SHA-256 hash for deduplication
        MimeType: MIME type of the font file
        OriginalFileName: Original filename when uploaded
        
    Extracted Metadata:
        ExtractedFontName: Internal name from font file
        ExtractedFamily: Family name from font file
        ExtractedSubfamily: Subfamily (e.g., "Bold Italic")
        ExtractedVersion: Version string from font
        ExtractedCopyright: Copyright notice
        ExtractedLicense: License text
        ExtractedDesigner: Designer name
        ExtractedVendor: Vendor/foundry name
        SupportedScripts: Comma-separated script list
        GlyphCount: Number of glyphs in font
        UnitsPerEm: Design units per em
    """
    
    __tablename__ = "FontFile"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key (INT IDENTITY per project standards)
    FontFileID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key to FontVariant
    FontVariantID = Column(Integer, ForeignKey('dbo.FontVariant.FontVariantID'), nullable=False, index=True)
    
    # File storage
    FileFormat = Column(String(10), nullable=False)  # 'ttf', 'otf', 'woff', 'woff2'
    FileData = Column(LargeBinary, nullable=False)  # Actual font file bytes
    FileSizeBytes = Column(BigInteger, nullable=False)
    FileHash = Column(String(64), nullable=False, unique=True, index=True)  # SHA-256 for deduplication
    MimeType = Column(String(100), nullable=False)
    OriginalFileName = Column(String(255), nullable=True)
    
    # Extracted metadata (from font validation using fonttools)
    ExtractedFontName = Column(String(200), nullable=True)  # Internal name from font file
    ExtractedFamily = Column(String(200), nullable=True)  # Family name from font file
    ExtractedSubfamily = Column(String(200), nullable=True)  # Subfamily (e.g., "Bold Italic")
    ExtractedVersion = Column(String(50), nullable=True)
    ExtractedCopyright = Column(String(500), nullable=True)
    ExtractedLicense = Column(String(500), nullable=True)
    ExtractedDesigner = Column(String(200), nullable=True)
    ExtractedVendor = Column(String(200), nullable=True)
    SupportedScripts = Column(String(500), nullable=True)  # 'latin,cyrillic,greek'
    GlyphCount = Column(Integer, nullable=True)
    UnitsPerEm = Column(Integer, nullable=True)
    
    # Validation status
    IsValid = Column(Boolean, nullable=False, default=True)
    ValidationDate = Column(DateTime, nullable=True)
    ValidationErrors = Column(String, nullable=True)  # JSON or comma-separated errors
    
    # Audit
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    font_variant = relationship("FontVariant", back_populates="font_files")
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    
    def __repr__(self) -> str:
        return f"<FontFile(FontFileID={self.FontFileID}, FileFormat='{self.FileFormat}', FileHash='{self.FileHash[:8]}...')>"

