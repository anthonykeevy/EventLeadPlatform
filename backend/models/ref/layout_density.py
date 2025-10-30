"""
LayoutDensity Reference Model (ref.LayoutDensity)
Layout density options for users
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class LayoutDensity(Base):
    """
    Layout density reference table.
    
    Density options: Compact, Comfortable, Spacious
    
    Attributes:
        LayoutDensityID: Primary key
        DensityCode: Unique density code (e.g., 'compact', 'comfortable', 'spacious')
        DensityName: Display name (e.g., 'Compact', 'Comfortable')
        Description: Full description of the layout density
        CSSClass: CSS class for frontend integration
        IsActive: Whether this density is available for selection
        SortOrder: Display order
    """
    
    __tablename__ = "LayoutDensity"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    LayoutDensityID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    DensityCode = Column(String(20), nullable=False, unique=True)
    DensityName = Column(String(50), nullable=False)
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
    users = relationship("User", back_populates="layout_density", foreign_keys="[User.LayoutDensityID]")
    
    def __repr__(self) -> str:
        return f"<LayoutDensity(LayoutDensityID={self.LayoutDensityID}, DensityCode='{self.DensityCode}', DensityName='{self.DensityName}')>"

