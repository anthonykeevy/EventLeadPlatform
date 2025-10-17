"""
SettingType Reference Model (ref.SettingType)
Data types for application settings
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from backend.common.database import Base


class SettingType(Base):
    """
    Setting type reference table.
    
    Types: String, Integer, Boolean, Decimal, JSON, URL, Email, etc.
    
    Attributes:
        SettingTypeID: Primary key
        TypeCode: Unique type code (e.g., 'string', 'integer', 'boolean', 'json')
        TypeName: Display name (e.g., 'String', 'Integer', 'Boolean')
        Description: Full description of the data type
        ValidationPattern: Optional regex pattern for validation
        IsActive: Whether this type is available for use
        SortOrder: Display order
    """
    
    __tablename__ = "SettingType"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    SettingTypeID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    TypeCode = Column(String(20), nullable=False, unique=True)
    TypeName = Column(String(50), nullable=False)
    Description = Column(String(500), nullable=False)
    ValidationPattern = Column(String(200), nullable=True)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    settings = relationship("AppSetting", back_populates="setting_type")
    
    def __repr__(self) -> str:
        return f"<SettingType(SettingTypeID={self.SettingTypeID}, TypeCode='{self.TypeCode}', TypeName='{self.TypeName}')>"

