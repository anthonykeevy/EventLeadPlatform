"""
AppSetting Model (config.AppSetting)
Application configuration settings
"""
from sqlalchemy import Column, BigInteger, String, Numeric, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class AppSetting(Base):
    """
    Application setting model for platform configuration.
    
    Settings are organized by category (General, Email, Security, etc.)
    and typed (String, Integer, Boolean, JSON, etc.) with validation.
    
    Attributes:
        AppSettingID: Primary key
        SettingKey: Unique setting key (e.g., 'email.smtp.host')
        SettingValue: Current setting value (stored as string, type-converted on use)
        SettingCategoryID: Foreign key to ref.SettingCategory
        SettingTypeID: Foreign key to ref.SettingType
        Description: Human-readable description of the setting
        DefaultValue: Default value for the setting
        IsEditable: Whether setting can be edited via UI
        ValidationRegex: Optional regex pattern for validation
        MinValue: Minimum value for numeric settings
        MaxValue: Maximum value for numeric settings
        IsActive: Whether setting is active
        SortOrder: Display order within category
    """
    
    __tablename__ = "AppSetting"
    __table_args__ = {"schema": "config"}
    
    # Primary Key
    AppSettingID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    SettingKey = Column(String(100), nullable=False, unique=True)
    SettingValue = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    Description = Column(String(500), nullable=False)
    DefaultValue = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    
    # Foreign Keys
    SettingCategoryID = Column(BigInteger, ForeignKey('ref.SettingCategory.SettingCategoryID'), nullable=False, index=True)
    SettingTypeID = Column(BigInteger, ForeignKey('ref.SettingType.SettingTypeID'), nullable=False, index=True)
    
    # Validation
    IsEditable = Column(Boolean, nullable=False, default=True)
    ValidationRegex = Column(String(500), nullable=True)
    MinValue = Column(Numeric(18, 2), nullable=True)
    MaxValue = Column(Numeric(18, 2), nullable=True)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True, index=True)
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
    category = relationship("SettingCategory", back_populates="settings")
    setting_type = relationship("SettingType", back_populates="settings")
    
    def __repr__(self) -> str:
        return f"<AppSetting(AppSettingID={self.AppSettingID}, SettingKey='{self.SettingKey}', SettingValue='{self.SettingValue}')>"

