"""
Language Reference Model (ref.Language)
Languages supported by the platform
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from backend.common.database import Base


class Language(Base):
    """
    Language reference table for platform localization.
    
    Attributes:
        LanguageID: Primary key
        LanguageCode: ISO 639-1 language code (e.g., 'en', 'fr')
        LanguageName: Full language name (e.g., 'English', 'French')
        IsActive: Whether language is available in the platform
        SortOrder: Display order for language selection
    """
    
    __tablename__ = "Language"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    LanguageID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    LanguageCode = Column(String(5), nullable=False, unique=True)
    LanguageName = Column(String(100), nullable=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=999)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="preferred_language", foreign_keys="[User.PreferredLanguageID]")
    
    def __repr__(self) -> str:
        return f"<Language(LanguageID={self.LanguageID}, LanguageCode='{self.LanguageCode}', LanguageName='{self.LanguageName}')>"

