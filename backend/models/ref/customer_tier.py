"""
CustomerTier Reference Model (ref.CustomerTier)
Subscription tiers for customers
"""
from sqlalchemy import Column, BigInteger, String, Numeric, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from backend.common.database import Base


class CustomerTier(Base):
    """
    Customer tier reference table for subscription plans.
    
    Tiers: Free, Starter, Professional, Enterprise
    
    Attributes:
        CustomerTierID: Primary key
        TierCode: Unique tier code (e.g., 'free', 'starter', 'pro', 'enterprise')
        TierName: Display name (e.g., 'Free', 'Professional', 'Enterprise')
        Description: Full description of tier features and limits
        MonthlyPrice: Monthly subscription price (null for free tier)
        AnnualPrice: Annual subscription price (null for free tier)
        MaxUsers: Maximum users allowed (null for unlimited)
        MaxForms: Maximum forms allowed (null for unlimited)
        MaxSubmissionsPerMonth: Maximum form submissions per month (null for unlimited)
        IsActive: Whether this tier is available for new subscriptions
        SortOrder: Display order
    """
    
    __tablename__ = "CustomerTier"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    CustomerTierID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    TierCode = Column(String(50), nullable=False, unique=True)
    TierName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=False)
    
    # Pricing
    MonthlyPrice = Column(Numeric(10, 2), nullable=True)
    AnnualPrice = Column(Numeric(10, 2), nullable=True)
    
    # Limits
    MaxUsers = Column(Integer, nullable=True)
    MaxForms = Column(Integer, nullable=True)
    MaxSubmissionsPerMonth = Column(Integer, nullable=True)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    customer_details = relationship("CompanyCustomerDetails", back_populates="tier")
    
    def __repr__(self) -> str:
        return f"<CustomerTier(CustomerTierID={self.CustomerTierID}, TierCode='{self.TierCode}', TierName='{self.TierName}')>"

