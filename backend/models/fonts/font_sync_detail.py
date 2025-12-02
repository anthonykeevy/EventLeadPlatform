"""
FontSyncDetail Model (log.FontSyncDetail)
Individual font sync details for each sync operation
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FontSyncDetail(Base):
    """
    Font sync detail model for tracking individual font changes.
    
    Records changes to each font during sync operations.
    
    Attributes:
        FontSyncDetailID: Primary key
        FontSyncLogID: Foreign key to FontSyncLog
        FontFamilyID: Foreign key to FontFamily (nullable for new fonts)
        GoogleFontID: Google's font identifier
        FamilyName: Font family name
        Operation: What was done (Added, Updated, Deprecated, etc.)
        PreviousVersion: Version before update
        NewVersion: Version after update
    """
    
    __tablename__ = "FontSyncDetail"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    FontSyncDetailID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    FontSyncLogID = Column(Integer, ForeignKey('log.FontSyncLog.FontSyncLogID'), nullable=False, index=True)
    FontFamilyID = Column(Integer, ForeignKey('dbo.FontFamily.FontFamilyID'), nullable=True, index=True)
    
    # Font Identification
    GoogleFontID = Column(String(100), nullable=True)
    FamilyName = Column(String(200), nullable=True)
    
    # Operation
    Operation = Column(String(20), nullable=False)
    
    # Change Details
    PreviousVersion = Column(String(20), nullable=True)
    NewVersion = Column(String(20), nullable=True)
    ChangeSummary = Column(String(500), nullable=True)
    
    # Error
    ErrorMessage = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    
    # Audit
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Relationships
    sync_log = relationship("FontSyncLog")
    font_family = relationship("FontFamily")
    
    def __repr__(self) -> str:
        return f"<FontSyncDetail(FontSyncDetailID={self.FontSyncDetailID}, Operation='{self.Operation}', Font='{self.FamilyName}')>"

