"""
CompanyFont Model (dbo.CompanyFont)
Junction table for Company-Font relationship with per-company display name aliases
"""
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class CompanyFont(Base):
    """
    Company-Font junction table for managing font access and licensing.
    
    Features:
    - Many-to-many relationship between companies and fonts
    - Per-company display name override (aliases)
    - License tracking with expiry dates
    - Ownership vs shared access distinction
    
    Attributes:
        CompanyFontID: Primary key
        CompanyID: Foreign key to Company
        FontFamilyID: Foreign key to FontFamily
        DisplayNameOverride: Company-specific display name (NULL = use FamilyName)
        IsOwner: TRUE if company originally uploaded this font
        IsLicensed: TRUE if company can use this font
        LicenseType: Type of license ('Owned', 'Shared', 'Platform', 'Trial')
        LicenseExpiryDate: When the license expires (NULL = perpetual)
    """
    
    __tablename__ = "CompanyFont"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key (INT IDENTITY per project standards)
    CompanyFontID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    FontFamilyID = Column(Integer, ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=False, index=True)
    
    # Per-company display name (allows "XeroxFont" vs "FujitsuFont" for same file)
    DisplayNameOverride = Column(String(200), nullable=True)  # NULL = use FontFamily.FamilyName
    
    # Relationship type
    IsOwner = Column(Boolean, nullable=False, default=False)  # TRUE = company uploaded this font
    IsLicensed = Column(Boolean, nullable=False, default=True)  # TRUE = company can use this font
    
    # License tracking
    LicenseType = Column(String(50), nullable=True)  # 'Owned', 'Shared', 'Platform', 'Trial'
    LicenseExpiryDate = Column(Date, nullable=True)
    LicenseNotes = Column(String(500), nullable=True)
    
    # Audit
    GrantedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    GrantedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    RevokedDate = Column(DateTime, nullable=True)
    RevokedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(String(100), nullable=False, default='SYSTEM')
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(String(100), nullable=True)
    
    # Relationships
    company = relationship("Company", foreign_keys=[CompanyID])
    font_family = relationship("FontFamily", back_populates="company_fonts")
    granted_by_user = relationship("User", foreign_keys=[GrantedBy])
    revoked_by_user = relationship("User", foreign_keys=[RevokedBy])
    
    @property
    def effective_display_name(self) -> str:
        """Get the effective display name (override or family name)."""
        if self.DisplayNameOverride:
            return self.DisplayNameOverride
        return self.font_family.FamilyName if self.font_family else ''
    
    def __repr__(self) -> str:
        return f"<CompanyFont(CompanyFontID={self.CompanyFontID}, CompanyID={self.CompanyID}, FontFamilyID={self.FontFamilyID}, DisplayName='{self.effective_display_name}')>"

