"""
SettingCategory Reference Model (ref.SettingCategory)
Categories for application settings
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from backend.common.database import Base


class SettingCategory(Base):
    """
    Setting category reference table.
    
    Categories: General, Email, Security, Billing, Integrations, etc.
    
    Attributes:
        SettingCategoryID: Primary key
        CategoryCode: Unique category code (e.g., 'general', 'email', 'security')
        CategoryName: Display name (e.g., 'General Settings', 'Email Configuration')
        Description: Full description of the category
        IsActive: Whether this category is available for use
        SortOrder: Display order
    """
    
    __tablename__ = "SettingCategory"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    SettingCategoryID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    CategoryCode = Column(String(50), nullable=False, unique=True)
    CategoryName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    settings = relationship("AppSetting", back_populates="category")
    
    def __repr__(self) -> str:
        return f"<SettingCategory(SettingCategoryID={self.SettingCategoryID}, CategoryCode='{self.CategoryCode}')>"

