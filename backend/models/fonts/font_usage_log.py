"""
FontUsageLog Model (log.FontUsageLog)
Track font usage in the platform for analytics
"""
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontUsageLog(Base):
    """
    Font usage log model for tracking font selection and usage.
    
    Records when users select, apply, or preview fonts.
    
    Attributes:
        FontUsageLogID: Primary key
        FontFamilyID: Foreign key to FontFamily
        FontVariantID: Foreign key to FontVariant (optional)
        UsageContext: Where the font was used (FormBuilder, etc.)
        ActionType: What was done (Selected, Applied, Previewed)
        UserID: User who performed the action
        CompanyID: Company context
    """
    
    __tablename__ = "FontUsageLog"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    FontUsageLogID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Font Reference
    FontFamilyID = Column(Integer, ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False, index=True)
    FontVariantID = Column(Integer, ForeignKey('dbo.FontVariant.FontVariantID'), nullable=True)
    
    # Context
    UsageContext = Column(String(50), nullable=False)
    ContextEntityType = Column(String(50), nullable=True)
    ContextEntityID = Column(Integer, nullable=True)
    
    # User Context
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True, index=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True)
    
    # Action
    ActionType = Column(String(50), nullable=False)
    
    # Audit
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    IPAddress = Column(String(50), nullable=True)
    UserAgent = Column(String(500), nullable=True)
    
    # Relationships
    font_family = relationship("FontFamily", back_populates="usage_logs")
    font_variant = relationship("FontVariant")
    user = relationship("User")
    company = relationship("Company")
    
    def __repr__(self) -> str:
        return f"<FontUsageLog(FontUsageLogID={self.FontUsageLogID}, Action='{self.ActionType}', Context='{self.UsageContext}')>"

