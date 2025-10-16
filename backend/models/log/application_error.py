"""
ApplicationError Model (log.ApplicationError)
Application error logging for debugging and monitoring
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class ApplicationError(Base):
    """
    Application error log model.
    
    Captures all application errors with stack traces for debugging.
    Severity levels: CRITICAL, ERROR, WARNING
    
    Attributes:
        ApplicationErrorID: Primary key
        ErrorType: Type of error (e.g., 'ValidationError', 'DatabaseError', 'APIError')
        ErrorMessage: Error message
        StackTrace: Full stack trace (for debugging)
        Severity: Severity level (CRITICAL, ERROR, WARNING)
        RequestID: Unique request ID (correlation ID)
        Path: Request path where error occurred
        Method: HTTP method
        UserID: Foreign key to dbo.User (nullable)
        CompanyID: Foreign key to dbo.Company (nullable)
        IPAddress: Client IP address
        UserAgent: Browser user agent string
        AdditionalData: Additional context data (JSON-encoded)
        CreatedDate: Timestamp when error occurred
    """
    
    __tablename__ = "ApplicationError"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    ApplicationErrorID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Error Details
    ErrorType = Column(String(100), nullable=False, index=True)
    ErrorMessage = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    StackTrace = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    Severity = Column(String(20), nullable=False, index=True)  # CRITICAL, ERROR, WARNING
    
    # Request Context
    RequestID = Column(String(100), nullable=True)
    Path = Column(String(500), nullable=True, index=True)
    Method = Column(String(10), nullable=True)
    
    # User Context
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True)
    
    # Security Context
    IPAddress = Column(String(50), nullable=True)
    UserAgent = Column(String(500), nullable=True)
    
    # Additional Context
    AdditionalData = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    
    # Timestamp
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="application_errors")
    company = relationship("Company", back_populates="application_errors")
    
    def __repr__(self) -> str:
        return f"<ApplicationError(ApplicationErrorID={self.ApplicationErrorID}, ErrorType='{self.ErrorType}', Severity='{self.Severity}')>"

