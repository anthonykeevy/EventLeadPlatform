"""
FontColorCapability Model (dbo.FontColorCapability)
Color font capabilities for each font family
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontColorCapability(Base):
    """
    Font color capability model representing color font features.
    
    Color fonts can support multiple color technologies (COLR, SVG, etc.).
    
    Attributes:
        FontColorCapabilityID: Primary key
        FontFamilyID: Foreign key to FontFamily
        CapabilityCode: Capability identifier (e.g., "COLR", "SVG")
        CapabilityName: Display name
        CapabilityVersion: Version of the capability (e.g., "v0", "v1")
    """
    
    __tablename__ = "FontColorCapability"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    FontColorCapabilityID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    FontFamilyID = Column(Integer, ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False, index=True)
    
    # Capability
    CapabilityCode = Column(String(20), nullable=False)
    CapabilityName = Column(String(100), nullable=False)
    CapabilityVersion = Column(String(20), nullable=True)
    
    # Audit
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Relationships
    font_family = relationship("FontFamily", back_populates="color_capabilities")
    
    def __repr__(self) -> str:
        return f"<FontColorCapability(FontColorCapabilityID={self.FontColorCapabilityID}, CapabilityCode='{self.CapabilityCode}')>"

