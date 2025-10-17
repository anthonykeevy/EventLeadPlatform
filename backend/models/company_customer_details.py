"""
CompanyCustomerDetails Model (dbo.CompanyCustomerDetails)
Customer-specific details for companies (1-to-1 with Company)
"""
from sqlalchemy import Column, BigInteger, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.common.database import Base


class CompanyCustomerDetails(Base):
    """
    Company customer details (1-to-1 with Company).
    
    Tracks subscription tier, usage metrics, and customer lifecycle.
    
    Attributes:
        CompanyCustomerDetailsID: Primary key
        CompanyID: Unique foreign key to dbo.Company
        CustomerSince: Date when company became a customer
        CustomerTierID: Foreign key to ref.CustomerTier (Free, Starter, Pro, Enterprise)
        TotalEvents: Count of events created by company
        TotalLeadsCaptured: Count of leads captured by company
    """
    
    __tablename__ = "CompanyCustomerDetails"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    CompanyCustomerDetailsID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, unique=True)
    CustomerTierID = Column(BigInteger, ForeignKey('ref.CustomerTier.CustomerTierID'), nullable=False, index=True)
    
    # Customer Lifecycle
    CustomerSince = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Usage Metrics
    TotalEvents = Column(Integer, nullable=False, default=0)
    TotalLeadsCaptured = Column(Integer, nullable=False, default=0)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="customer_details")
    tier = relationship("CustomerTier", back_populates="customer_details")
    
    def __repr__(self) -> str:
        return f"<CompanyCustomerDetails(CompanyID={self.CompanyID}, TotalEvents={self.TotalEvents})>"

