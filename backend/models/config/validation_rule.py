"""
ValidationRule Model (config.ValidationRule)
Country-specific validation rules for form fields
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from common.database import Base


class ValidationRule(Base):
    """
    Validation rule model for country-specific field validation.
    
    Supports different validation patterns per country (e.g., Australian ABN vs Canadian BN).
    Rules include regex patterns and custom validation messages.
    
    Attributes:
        ValidationRuleID: Primary key
        RuleKey: Rule key identifier (e.g., 'abn', 'phone', 'postal_code')
        RuleTypeID: Foreign key to ref.RuleType
        CountryID: Foreign key to ref.Country (null = applies to all countries)
        ValidationPattern: Regex pattern for validation
        ValidationMessage: Error message when validation fails
        Description: Human-readable description of the rule
        MinLength: Minimum length constraint (quick validation before regex)
        MaxLength: Maximum length constraint (quick validation before regex)
        ExampleValue: Example valid value for user guidance
        IsActive: Whether rule is active
        Priority: Priority when multiple rules match (higher = higher priority)
    """
    
    __tablename__ = "ValidationRule"
    __table_args__ = (
        UniqueConstraint('RuleKey', 'CountryID', 'RuleTypeID', name='UQ_ValidationRule_Key_Country_Type'),
        {"schema": "config"}
    )
    
    # Primary Key
    ValidationRuleID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    RuleKey = Column(String(100), nullable=False)
    ValidationPattern = Column(String(500), nullable=False)
    ValidationMessage = Column(String(500), nullable=False)
    Description = Column(String(500), nullable=False)
    
    # Foreign Keys
    RuleTypeID = Column(BigInteger, ForeignKey('ref.RuleType.RuleTypeID'), nullable=False, index=True)
    CountryID = Column(BigInteger, ForeignKey('ref.Country.CountryID'), nullable=True, index=True)
    
    # Validation Constraints (Story 1.12 enhancement)
    MinLength = Column(Integer, nullable=True)
    MaxLength = Column(Integer, nullable=True)
    ExampleValue = Column(String(100), nullable=True)
    
    # Display Formatting (Story 1.20 enhancement)
    DisplayFormat = Column(String(100), nullable=True)  # e.g., '04XX XXX XXX'
    DisplayExample = Column(String(100), nullable=True)  # e.g., '0412 345 678'
    StripPrefix = Column(Boolean, nullable=False, default=False)  # Remove +61 for display
    SpacingPattern = Column(String(50), nullable=True)  # e.g., 'XXXX XXX XXX'
    
    # Status and Priority
    IsActive = Column(Boolean, nullable=False, default=True, index=True)
    Priority = Column(Integer, nullable=False, default=0)
    SortOrder = Column(Integer, nullable=False, default=999)  # Standardized ordering (Story 1.20)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    rule_type = relationship("RuleType", back_populates="validation_rules")
    country = relationship("Country", back_populates="validation_rules")
    
    def __repr__(self) -> str:
        return f"<ValidationRule(ValidationRuleID={self.ValidationRuleID}, RuleKey='{self.RuleKey}', CountryID={self.CountryID})>"

