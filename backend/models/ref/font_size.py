"""
FontSize Reference Model (ref.FontSize)
Font size options for users
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontSize(Base):
    """
    Font size reference table.
    
    Size options: Small (14px), Medium (16px), Large (18px)
    
    Attributes:
        FontSizeID: Primary key
        SizeCode: Unique size code (e.g., 'small', 'medium', 'large')
        SizeName: Display name (e.g., 'Small', 'Medium')
        Description: Full description of the font size
        CSSClass: CSS class for frontend integration
        BaseFontSize: Base font size in pixels (e.g., '14px', '16px', '18px')
        IsActive: Whether this size is available for selection
        SortOrder: Display order
    """
    
    __tablename__ = "FontSize"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    FontSizeID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    SizeCode = Column(String(20), nullable=False, unique=True)
    SizeName = Column(String(50), nullable=False)
    Description = Column(String(200), nullable=False)
    CSSClass = Column(String(50), nullable=False)
    BaseFontSize = Column(String(10), nullable=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="font_size", foreign_keys="[User.FontSizeID]")
    
    def __repr__(self) -> str:
        return f"<FontSize(FontSizeID={self.FontSizeID}, SizeCode='{self.SizeCode}', SizeName='{self.SizeName}')>"

