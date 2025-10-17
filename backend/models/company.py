"""
Company Model (dbo.Company)
Core business entity representing companies/organizations
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.common.database import Base


class Company(Base):
    """
    Company model representing organizations using the platform.
    
    Supports ABR integration for Australian companies with ABN/ACN validation.
    Hierarchical structure supports parent companies and subsidiaries.
    
    Attributes:
        CompanyID: Primary key
        CompanyName: User-entered or ABR-retrieved company name
        LegalEntityName: Official legal name from ABR
        BusinessNames: JSON array of registered business names from ABR
        CustomDisplayName: User-provided custom display name
        DisplayNameSource: Source of display name (Legal, Business, Custom, User)
        ABN: Australian Business Number (11 digits)
        ACN: Australian Company Number (9 digits)
        ABNStatus: ABN status from ABR (Active, Cancelled, Historical)
        EntityType: Entity type from ABR (e.g., 'Company', 'Partnership')
        GSTRegistered: Whether company is GST registered
        Phone: Contact phone number
        Email: Contact email
        Website: Company website URL
        CountryID: Foreign key to ref.Country
        IndustryID: Foreign key to ref.Industry
        ParentCompanyID: Self-referential FK for company hierarchies
        IsActive: Whether company is active in the platform
    """
    
    __tablename__ = "Company"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    CompanyID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Company Names
    CompanyName = Column(String(200), nullable=False, index=True)
    LegalEntityName = Column(String(200), nullable=True)
    BusinessNames = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON array
    CustomDisplayName = Column(String(200), nullable=True)
    DisplayNameSource = Column(String(20), nullable=False, default='User')  # Legal, Business, Custom, User
    
    # ABR Integration Fields
    ABN = Column(String(11), nullable=True, index=True)
    ACN = Column(String(9), nullable=True)
    ABNStatus = Column(String(20), nullable=True)  # Active, Cancelled, Historical
    EntityType = Column(String(100), nullable=True)
    GSTRegistered = Column(Boolean, nullable=True)
    
    # Contact Information
    Phone = Column(String(20), nullable=True)
    Email = Column(String(255), nullable=True)
    Website = Column(String(500), nullable=True)
    
    # Foreign Keys
    CountryID = Column(BigInteger, ForeignKey('ref.Country.CountryID'), nullable=False, index=True)
    IndustryID = Column(BigInteger, ForeignKey('ref.Industry.IndustryID'), nullable=True, index=True)
    ParentCompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True, index=True)
    
    # Status
    IsActive = Column(Boolean, nullable=False, default=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    country = relationship("Country", back_populates="companies", foreign_keys=[CountryID])
    industry = relationship("Industry", back_populates="companies")
    parent = relationship("Company", remote_side=[CompanyID], backref="subsidiaries")
    
    users = relationship("UserCompany", back_populates="company")
    customer_details = relationship("CompanyCustomerDetails", back_populates="company", uselist=False)
    billing_details = relationship("CompanyBillingDetails", back_populates="company", uselist=False)
    organizer_details = relationship("CompanyOrganizerDetails", back_populates="company", uselist=False)
    invitations = relationship("UserInvitation", back_populates="company")
    
    activity_logs = relationship("ActivityLog", back_populates="company")
    api_requests = relationship("ApiRequest", back_populates="company")
    application_errors = relationship("ApplicationError", back_populates="company")
    email_deliveries = relationship("EmailDelivery", back_populates="company")
    
    def __repr__(self) -> str:
        return f"<Company(CompanyID={self.CompanyID}, CompanyName='{self.CompanyName}', ABN='{self.ABN}')>"

