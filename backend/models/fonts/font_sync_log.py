"""
FontSyncLog Model (log.FontSyncLog)
Track synchronization operations with Google Fonts API
"""
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func
from common.database import Base


class FontSyncLog(Base):
    """
    Font sync log model for tracking synchronization operations.
    
    Records each sync attempt with metrics and status.
    
    Attributes:
        FontSyncLogID: Primary key
        SyncStartTime: When sync started
        SyncEndTime: When sync completed
        SyncStatus: Status (Running, Success, Failed, Partial)
        TotalFontsInAPI: Total fonts returned by API
        FontsAdded: New fonts added
        FontsUpdated: Existing fonts updated
        FontsDeprecated: Fonts marked deprecated
        TriggerType: How sync was triggered (Scheduled, Manual)
    """
    
    __tablename__ = "FontSyncLog"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    FontSyncLogID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Sync Operation
    SyncStartTime = Column(DateTime, nullable=False)
    SyncEndTime = Column(DateTime, nullable=True)
    
    # Status
    SyncStatus = Column(String(20), nullable=False, default='Running')
    
    # Metrics
    TotalFontsInAPI = Column(Integer, nullable=True)
    FontsAdded = Column(Integer, nullable=False, default=0)
    FontsUpdated = Column(Integer, nullable=False, default=0)
    FontsDeprecated = Column(Integer, nullable=False, default=0)
    FontsRemoved = Column(Integer, nullable=False, default=0)
    FontsUnchanged = Column(Integer, nullable=False, default=0)
    VariantsProcessed = Column(Integer, nullable=False, default=0)
    SubsetsProcessed = Column(Integer, nullable=False, default=0)
    AxesProcessed = Column(Integer, nullable=False, default=0)
    
    # API Details
    APIEndpoint = Column(String(500), nullable=True)
    APIVersion = Column(String(20), nullable=True)
    APIResponseTimeMs = Column(Integer, nullable=True)
    APIResponseSizeBytes = Column(BigInteger, nullable=True)
    
    # Error Handling
    ErrorMessage = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    ErrorDetails = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    RetryCount = Column(Integer, nullable=False, default=0)
    
    # Trigger
    TriggerType = Column(String(50), nullable=False, default='Scheduled')
    TriggeredBy = Column(String(100), nullable=True)
    
    # Audit
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    def __repr__(self) -> str:
        return f"<FontSyncLog(FontSyncLogID={self.FontSyncLogID}, Status='{self.SyncStatus}', Added={self.FontsAdded})>"

