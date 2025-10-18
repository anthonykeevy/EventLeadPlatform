"""
Timezone Reference Model (ref.Timezone)
IANA timezone identifiers for user and company localization
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, func
from common.database import Base


class Timezone(Base):
    """
    Timezone reference table for IANA timezone identifiers.
    
    Stores standard timezone identifiers used for date/time localization.
    
    Attributes:
        TimezoneID: Primary key
        TimezoneIdentifier: IANA timezone identifier (e.g., 'Australia/Sydney')
        DisplayName: Human-readable display name
        OffsetMinutes: UTC offset in minutes (varies with DST)
        CountryCode: ISO 2-letter country code
    """
    
    __tablename__ = "Timezone"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    TimezoneID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    TimezoneIdentifier = Column(String(50), nullable=False, unique=True, index=True)
    DisplayName = Column(String(100), nullable=False)
    OffsetMinutes = Column(Integer, nullable=False)
    CountryCode = Column(String(2), nullable=True)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Timezone(TimezoneID={self.TimezoneID}, TimezoneIdentifier='{self.TimezoneIdentifier}')>"

