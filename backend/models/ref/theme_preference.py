"""
ThemePreference Reference Model (ref.ThemePreference)
Theme preference options for users
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class ThemePreference(Base):
    """
    Theme preference reference table.
    
    Theme options: Light, Dark, High-Contrast, System
    
    Attributes:
        ThemePreferenceID: Primary key
        ThemeCode: Unique theme code (e.g., 'light', 'dark', 'high-contrast')
        ThemeName: Display name (e.g., 'Light Theme', 'Dark Theme')
        Description: Full description of the theme
        CSSClass: CSS class for frontend integration
        IsActive: Whether this theme is available for selection
        SortOrder: Display order
    """
    
    __tablename__ = "ThemePreference"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    ThemePreferenceID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    ThemeCode = Column(String(20), nullable=False, unique=True)
    ThemeName = Column(String(50), nullable=False)
    Description = Column(String(200), nullable=False)
    CSSClass = Column(String(50), nullable=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="theme_preference", foreign_keys="[User.ThemePreferenceID]")
    
    def __repr__(self) -> str:
        return f"<ThemePreference(ThemePreferenceID={self.ThemePreferenceID}, ThemeCode='{self.ThemeCode}', ThemeName='{self.ThemeName}')>"

