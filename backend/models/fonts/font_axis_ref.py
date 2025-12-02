"""
FontAxisRef Model (dbo.FontAxisRef)
Reference table for standard variable font axes
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, DECIMAL, func
from common.database import Base


class FontAxisRef(Base):
    """
    Font axis reference model.
    
    Defines the available variable font axes (weight, width, etc.).
    
    Attributes:
        AxisTag: Primary key (e.g., "wght", "wdth")
        AxisName: Display name (e.g., "Weight", "Width")
        Description: Axis description
        IsStandard: Whether this is a standard OpenType axis
        DefaultMin: Default minimum value
        DefaultMax: Default maximum value
        CssProperty: Corresponding CSS property
    """
    
    __tablename__ = "FontAxisRef"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    AxisTag = Column(String(10), primary_key=True)
    
    # Axis Info
    AxisName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=True)
    
    # Classification
    IsStandard = Column(Boolean, nullable=False, default=True)
    
    # Defaults
    DefaultMin = Column(DECIMAL(10, 4), nullable=True)
    DefaultMax = Column(DECIMAL(10, 4), nullable=True)
    
    # CSS
    CssProperty = Column(String(100), nullable=True)
    
    # Display
    DisplayOrder = Column(Integer, nullable=False, default=0)
    
    # Audit
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    def __repr__(self) -> str:
        return f"<FontAxisRef(AxisTag='{self.AxisTag}', AxisName='{self.AxisName}')>"

