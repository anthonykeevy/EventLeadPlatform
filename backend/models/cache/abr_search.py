"""
ABRSearch Model (cache.ABRSearch)
Cache for Australian Business Register (ABR) API search results
"""
from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class ABRSearch(Base):
    """
    ABR search cache model for Australian Business Register API results.
    
    Caches ABR API responses to reduce API calls and improve performance.
    Supports search by ABN, ACN, or company name.
    Multiple results per search stored with ResultIndex.
    
    Composite Primary Key: (SearchType, SearchValue, ResultIndex)
    
    Attributes:
        SearchType: Type of search performed ('ABN', 'ACN', 'Name')
        SearchValue: Value searched for (e.g., '51824753556' for ABN)
        ResultIndex: Index of result in response (0-based, for multiple results)
        ABN: Australian Business Number from result
        LegalEntityName: Legal entity name from ABR
        EntityType: Entity type (e.g., 'Company', 'Partnership')
        ABNStatus: ABN status (Active, Cancelled, Historical)
        GSTRegistered: Whether entity is GST registered
        FullResponse: Complete API response (JSON)
        SearchDate: Timestamp when search was performed
        ExpiresAt: Timestamp when cache expires
        HitCount: Number of times this cache entry was accessed (analytics)
        LastHitAt: Timestamp when cache entry was last accessed (analytics)
        IsDeleted: Soft delete flag
        CreatedDate: Timestamp when cache entry was created
        CreatedBy: User who performed search
        UpdatedDate: Timestamp when cache entry was updated
        UpdatedBy: User who updated cache
        CompanyID: Foreign key to dbo.Company (if search linked to company)
        UserID: Foreign key to dbo.User (who performed search)
    """
    
    __tablename__ = "ABRSearch"
    __table_args__ = {"schema": "cache"}
    
    # Composite Primary Key
    SearchType = Column(String(10), primary_key=True)  # ABN, ACN, Name
    SearchValue = Column(String(255), primary_key=True)
    ResultIndex = Column(Integer, primary_key=True, default=0)
    
    # Result Fields (extracted from API response)
    ABN = Column(String(11), nullable=True, index=True)
    LegalEntityName = Column(String(255), nullable=True)
    EntityType = Column(String(100), nullable=True)
    ABNStatus = Column(String(20), nullable=True)
    GSTRegistered = Column(Boolean, nullable=True)
    
    # Full API Response
    FullResponse = Column(String(None), nullable=False)  # NVARCHAR(MAX) - JSON
    
    # Cache Metadata
    SearchDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    ExpiresAt = Column(DateTime, nullable=False, index=True)
    IsDeleted = Column(Boolean, nullable=False, default=False, index=True)
    
    # Analytics Fields (Story 1.10 AC-1.10.8, AC-1.10.11)
    HitCount = Column(Integer, nullable=False, default=0)
    LastHitAt = Column(DateTime, nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Context (optional)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True)
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    company = relationship("Company", foreign_keys=[CompanyID])
    user = relationship("User", foreign_keys=[UserID])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    
    def __repr__(self) -> str:
        return f"<ABRSearch(SearchType='{self.SearchType}', SearchValue='{self.SearchValue}', ResultIndex={self.ResultIndex}, ABN='{self.ABN}')>"

