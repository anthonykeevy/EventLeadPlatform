"""
FontSubsetRef Model (dbo.FontSubsetRef)
Reference table for font subsets/language support
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from common.database import Base


class FontSubsetRef(Base):
    """
    Font subset reference model.
    
    Defines the available font subsets (latin, cyrillic, etc.).
    
    Attributes:
        SubsetCode: Primary key (e.g., "latin", "cyrillic")
        SubsetName: Display name
        SubsetGroup: Grouping (Latin, Cyrillic, Asian, etc.)
        PrimaryLanguages: Languages supported by this subset
        DisplayOrder: Sort order
    """
    
    __tablename__ = "FontSubsetRef"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    SubsetCode = Column(String(50), primary_key=True)
    
    # Subset Info
    SubsetName = Column(String(100), nullable=False)
    SubsetGroup = Column(String(50), nullable=False)
    Description = Column(String(500), nullable=True)
    PrimaryLanguages = Column(String(500), nullable=True)
    
    # Display
    DisplayOrder = Column(Integer, nullable=False, default=0)
    
    # Audit
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    def __repr__(self) -> str:
        return f"<FontSubsetRef(SubsetCode='{self.SubsetCode}', SubsetName='{self.SubsetName}')>"

