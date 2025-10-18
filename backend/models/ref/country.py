"""
Country Reference Model (ref.Country)
Countries supported by the platform with currency, tax, and integration config
"""
from sqlalchemy import Column, BigInteger, String, Numeric, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class Country(Base):
    """
    Country reference table with currency, tax, and API integration configuration.
    
    Attributes:
        CountryID: Primary key
        CountryCode: ISO 3166-1 alpha-2 code (e.g., 'AU')
        CountryName: Full country name (e.g., 'Australia')
        PhonePrefix: International dialing prefix (e.g., '+61')
        CurrencyCode: ISO 4217 currency code (e.g., 'AUD')
        CurrencySymbol: Currency symbol (e.g., '$')
        CurrencyName: Full currency name (e.g., 'Australian Dollar')
        TaxRate: Default tax rate as decimal (e.g., 0.10 for 10%)
        TaxName: Tax name (e.g., 'GST', 'VAT')
        TaxInclusive: Whether prices include tax by default
        TaxNumberLabel: Label for tax identification number (e.g., 'ABN')
        CompanyValidationProvider: API provider for company validation (e.g., 'ABR')
        AddressValidationProvider: API provider for address validation (e.g., 'Geoscape')
        IntegrationConfig: JSON configuration for integrations
        IsActive: Whether country is active in the platform
        SortOrder: Display order for country selection
    """
    
    __tablename__ = "Country"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    CountryID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    CountryCode = Column(String(2), nullable=False, unique=True, index=True)
    CountryName = Column(String(100), nullable=False)
    PhonePrefix = Column(String(10), nullable=False)
    
    # Currency Information
    CurrencyCode = Column(String(3), nullable=False, index=True)
    CurrencySymbol = Column(String(5), nullable=False)
    CurrencyName = Column(String(100), nullable=False)
    
    # Tax Configuration
    TaxRate = Column(Numeric(5, 2), nullable=True)
    TaxName = Column(String(50), nullable=True)
    TaxInclusive = Column(Boolean, nullable=False, default=False)
    TaxNumberLabel = Column(String(50), nullable=True)
    
    # Integration Configuration
    CompanyValidationProvider = Column(String(50), nullable=True)
    AddressValidationProvider = Column(String(50), nullable=True)
    IntegrationConfig = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    
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
    companies = relationship("Company", back_populates="country", foreign_keys="[Company.CountryID]")
    users = relationship("User", back_populates="country", foreign_keys="[User.CountryID]")
    validation_rules = relationship("ValidationRule", back_populates="country")
    
    def __repr__(self) -> str:
        return f"<Country(CountryID={self.CountryID}, CountryCode='{self.CountryCode}', CountryName='{self.CountryName}')>"

