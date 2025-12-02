"""
FontAxis Model (dbo.FontAxis)
Variable font axes for each font family
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontAxis(Base):
    """
    Font axis model representing variable font axes.
    
    Variable fonts can have multiple axes (e.g., weight, width, slant).
    
    Attributes:
        FontAxisID: Primary key
        FontFamilyID: Foreign key to FontFamily
        AxisTag: Axis identifier (e.g., "wght", "wdth")
        AxisName: Display name (e.g., "Weight", "Width")
        MinValue: Minimum axis value
        MaxValue: Maximum axis value
        DefaultValue: Default axis value
        IsStandard: Whether this is a standard OpenType axis
    """
    
    __tablename__ = "FontAxis"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    FontAxisID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    FontFamilyID = Column(Integer, ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False, index=True)
    
    # Axis Identification
    AxisTag = Column(String(10), nullable=False, index=True)
    AxisName = Column(String(100), nullable=False)
    
    # Range
    MinValue = Column(DECIMAL(10, 4), nullable=False)
    MaxValue = Column(DECIMAL(10, 4), nullable=False)
    DefaultValue = Column(DECIMAL(10, 4), nullable=True)
    Step = Column(DECIMAL(10, 4), nullable=True)
    
    # Classification
    IsStandard = Column(Boolean, nullable=False, default=True)
    IsRegistered = Column(Boolean, nullable=False, default=False)
    
    # Display
    DisplayOrder = Column(Integer, nullable=False, default=0)
    CssProperty = Column(String(100), nullable=True)
    
    # Audit
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Relationships
    font_family = relationship("FontFamily", back_populates="axes")
    
    def __repr__(self) -> str:
        return f"<FontAxis(FontAxisID={self.FontAxisID}, AxisTag='{self.AxisTag}', Range=[{self.MinValue}, {self.MaxValue}])>"

