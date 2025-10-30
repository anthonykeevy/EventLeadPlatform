"""
Industry Reference Model (ref.Industry)
Industry classifications for companies
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class Industry(Base):
    """
    Industry reference table for company classification.
    
    Attributes:
        IndustryID: Primary key
        IndustryCode: Unique industry code (e.g., 'tech', 'hospitality')
        IndustryName: Display name (e.g., 'Technology', 'Hospitality')
        Description: Full description of the industry
        IsActive: Whether industry is available for selection
        SortOrder: Display order for industry selection
    """
    
    __tablename__ = "Industry"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    IndustryID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    IndustryCode = Column(String(50), nullable=False, unique=True)
    IndustryName = Column(String(100), nullable=False)
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
    companies = relationship("Company", back_populates="industry")
    user_industries = relationship("UserIndustry", back_populates="industry", foreign_keys="[UserIndustry.IndustryID]")
    
    def __repr__(self) -> str:
        return f"<Industry(IndustryID={self.IndustryID}, IndustryCode='{self.IndustryCode}', IndustryName='{self.IndustryName}')>"

