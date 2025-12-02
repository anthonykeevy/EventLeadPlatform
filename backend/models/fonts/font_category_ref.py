"""
FontCategoryRef Model (dbo.FontCategoryRef)
Reference table for font categories
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from common.database import Base


class FontCategoryRef(Base):
    """
    Font category reference model.
    
    Defines the available font categories (serif, sans-serif, etc.).
    
    Attributes:
        CategoryCode: Primary key (e.g., "serif", "sans-serif")
        CategoryName: Display name
        Description: Category description
        DisplayOrder: Sort order
        IconClass: CSS icon class for UI
    """
    
    __tablename__ = "FontCategoryRef"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    CategoryCode = Column(String(50), primary_key=True)
    
    # Category Info
    CategoryName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=True)
    
    # Display
    DisplayOrder = Column(Integer, nullable=False, default=0)
    IconClass = Column(String(100), nullable=True)
    
    # Audit
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    def __repr__(self) -> str:
        return f"<FontCategoryRef(CategoryCode='{self.CategoryCode}', CategoryName='{self.CategoryName}')>"

