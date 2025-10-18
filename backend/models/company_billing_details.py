"""
CompanyBillingDetails Model (dbo.CompanyBillingDetails)
Billing and payment details for companies (1-to-1 with Company)
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class CompanyBillingDetails(Base):
    """
    Company billing details (1-to-1 with Company).
    
    Tracks billing contact, address, and payment integration data.
    
    Attributes:
        CompanyBillingDetailsID: Primary key
        CompanyID: Unique foreign key to dbo.Company
        BillingContactName: Name of billing contact person
        BillingEmail: Email for invoices and billing notifications
        BillingPhone: Phone number for billing contact
        BillingAddressLine1: Billing address line 1
        BillingAddressLine2: Billing address line 2
        BillingCity: Billing city
        BillingState: Billing state/province
        BillingPostalCode: Billing postal/zip code
        BillingCountryID: Foreign key to ref.Country
        StripeCustomerID: Stripe customer ID for payment processing
    """
    
    __tablename__ = "CompanyBillingDetails"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    CompanyBillingDetailsID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, unique=True)
    BillingCountryID = Column(BigInteger, ForeignKey('ref.Country.CountryID'), nullable=True)
    
    # Billing Contact
    BillingContactName = Column(String(200), nullable=True)
    BillingEmail = Column(String(255), nullable=True)
    BillingPhone = Column(String(20), nullable=True)
    
    # Billing Address
    BillingAddressLine1 = Column(String(255), nullable=True)
    BillingAddressLine2 = Column(String(255), nullable=True)
    BillingCity = Column(String(100), nullable=True)
    BillingState = Column(String(100), nullable=True)
    BillingPostalCode = Column(String(20), nullable=True)
    
    # Payment Integration
    StripeCustomerID = Column(String(100), nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="billing_details")
    billing_country = relationship("Country", foreign_keys=[BillingCountryID])
    
    def __repr__(self) -> str:
        return f"<CompanyBillingDetails(CompanyID={self.CompanyID}, BillingEmail='{self.BillingEmail}')>"

