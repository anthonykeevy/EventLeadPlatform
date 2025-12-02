"""
FontVariant Model (dbo.FontVariant)
Individual weight/style combinations for each font family
"""
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontVariant(Base):
    """
    Font variant model representing weight/style combinations.
    
    Each font family has multiple variants (e.g., Regular, Bold, Italic).
    
    Attributes:
        FontVariantID: Primary key
        FontFamilyID: Foreign key to FontFamily
        VariantName: Variant identifier (e.g., "regular", "700italic")
        Weight: Numeric weight (100-900)
        WeightName: Display name (e.g., "Bold", "Light")
        IsItalic: Whether this is an italic variant
        TtfFileUrl: URL to TrueType font file
    """
    
    __tablename__ = "FontVariant"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    FontVariantID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    FontFamilyID = Column(Integer, ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False, index=True)
    
    # Variant Identification
    VariantName = Column(String(50), nullable=False)
    VariantNameNormalized = Column(String(50), nullable=False)
    
    # Weight & Style
    Weight = Column(Integer, nullable=False, default=400)
    WeightName = Column(String(50), nullable=True)
    IsItalic = Column(Boolean, nullable=False, default=False)
    
    # File URLs
    TtfFileUrl = Column(String(500), nullable=True)
    WoffFileUrl = Column(String(500), nullable=True)
    Woff2FileUrl = Column(String(500), nullable=True)
    
    # Local Caching
    IsFileCached = Column(Boolean, nullable=False, default=False)
    CachedFilePath = Column(String(500), nullable=True)
    FileSizeBytes = Column(BigInteger, nullable=True)
    FileHash = Column(String(64), nullable=True)
    
    # Display
    DisplayOrder = Column(Integer, nullable=False, default=0)
    IsDefault = Column(Boolean, nullable=False, default=False)
    
    # Audit Trail
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    UpdatedDate = Column(DateTime, nullable=True)
    
    # Relationships
    font_family = relationship("FontFamily", back_populates="variants")
    font_files = relationship("FontFile", back_populates="font_variant", lazy="dynamic")
    
    def __repr__(self) -> str:
        return f"<FontVariant(FontVariantID={self.FontVariantID}, VariantName='{self.VariantName}', Weight={self.Weight})>"

