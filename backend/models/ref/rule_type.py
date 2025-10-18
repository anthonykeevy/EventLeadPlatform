"""
RuleType Reference Model (ref.RuleType)
Types of validation rules
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import relationship
from common.database import Base


class RuleType(Base):
    """
    Rule type reference table for validation rules.
    
    Types: Email, Phone, ABN, ACN, PostalCode, CreditCard, etc.
    
    Attributes:
        RuleTypeID: Primary key
        TypeCode: Unique type code (e.g., 'email', 'phone', 'abn')
        TypeName: Display name (e.g., 'Email Validation', 'Phone Number')
        Description: Full description of the rule type
        IsActive: Whether this type is available for use
        SortOrder: Display order
    """
    
    __tablename__ = "RuleType"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    RuleTypeID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Core Fields
    TypeCode = Column(String(50), nullable=False, unique=True)
    TypeName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns (minimal for reference tables)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, nullable=True)
    
    # Relationships
    validation_rules = relationship("ValidationRule", back_populates="rule_type")
    
    def __repr__(self) -> str:
        return f"<RuleType(RuleTypeID={self.RuleTypeID}, TypeCode='{self.TypeCode}', TypeName='{self.TypeName}')>"

