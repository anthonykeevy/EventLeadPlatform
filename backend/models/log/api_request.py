"""
ApiRequest Model (log.ApiRequest)
API request logging for performance monitoring and debugging
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class ApiRequest(Base):
    """
    API request log model for monitoring and debugging.
    
    Captures all API requests with timing, user context, and response status.
    Used for performance monitoring, debugging, and usage analytics.
    
    Attributes:
        ApiRequestID: Primary key
        RequestID: Unique request ID (correlation ID)
        Method: HTTP method (GET, POST, PUT, DELETE, etc.)
        Path: Request path (e.g., '/api/v1/events')
        QueryParams: Query string parameters (JSON-encoded)
        StatusCode: HTTP status code (200, 404, 500, etc.)
        DurationMs: Request duration in milliseconds
        UserID: Foreign key to dbo.User (nullable for anonymous requests)
        CompanyID: Foreign key to dbo.Company (nullable)
        IPAddress: Client IP address
        UserAgent: Browser user agent string
        RequestPayload: Request body payload (JSON-encoded, Epic 2)
        ResponsePayload: Response body payload (JSON-encoded, Epic 2)
        Headers: Request headers (JSON-encoded, Epic 2)
        CreatedDate: Timestamp when request was made
    """
    
    __tablename__ = "ApiRequest"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    ApiRequestID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Request Details
    RequestID = Column(String(100), nullable=False)
    Method = Column(String(10), nullable=False)
    Path = Column(String(500), nullable=False, index=True)
    QueryParams = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    
    # Response Details
    StatusCode = Column(Integer, nullable=False, index=True)
    DurationMs = Column(Integer, nullable=False)
    
    # User Context
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True, index=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True)
    
    # Security Context
    IPAddress = Column(String(50), nullable=True)
    UserAgent = Column(String(500), nullable=True)
    
    # Enhanced Logging (Epic 2)
    RequestPayload = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    ResponsePayload = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    Headers = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON
    
    # Timestamp
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="api_requests")
    company = relationship("Company", back_populates="api_requests")
    
    def __repr__(self) -> str:
        return f"<ApiRequest(ApiRequestID={self.ApiRequestID}, Method='{self.Method}', Path='{self.Path}', StatusCode={self.StatusCode})>"

