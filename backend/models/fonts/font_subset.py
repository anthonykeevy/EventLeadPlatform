"""
FontSubset Model (dbo.FontSubset)
Character set support for each font family
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontSubset(Base):
    """
    Font subset model representing character set/language support.
    
    Each font family supports multiple subsets (e.g., Latin, Cyrillic).
    
    Attributes:
        FontSubsetID: Primary key
        FontFamilyID: Foreign key to FontFamily
        SubsetCode: Subset identifier (e.g., "latin", "cyrillic-ext")
        SubsetName: Display name
        SubsetGroup: Grouping (Latin, Cyrillic, Asian, etc.)
        IsExtended: Whether this is an extended variant
    """
    
    __tablename__ = "FontSubset"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    FontSubsetID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    FontFamilyID = Column(Integer, ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False, index=True)
    
    # Subset Identification
    SubsetCode = Column(String(50), nullable=False, index=True)
    SubsetName = Column(String(100), nullable=False)
    
    # Categorization
    SubsetGroup = Column(String(50), nullable=True)
    IsExtended = Column(Boolean, nullable=False, default=False)
    
    # Language Support
    PrimaryLanguages = Column(String(500), nullable=True)
    
    # Display
    DisplayOrder = Column(Integer, nullable=False, default=0)
    
    # Audit
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Relationships
    font_family = relationship("FontFamily", back_populates="subsets")
    
    def __repr__(self) -> str:
        return f"<FontSubset(FontSubsetID={self.FontSubsetID}, SubsetCode='{self.SubsetCode}')>"

