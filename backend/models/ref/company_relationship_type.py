"""
CompanyRelationshipType Model (ref.CompanyRelationshipType)
Reference table for company relationship types (e.g., branch, subsidiary)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class CompanyRelationshipType(Base):
    """
    CompanyRelationshipType reference model.
    
    Attributes:
        CompanyRelationshipTypeID: Primary key
        TypeName: Name of the relationship type (e.g., 'branch')
        TypeDescription: Description of the type
        IsActive: Whether the type is active
    """
    
    __tablename__ = "CompanyRelationshipType"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    CompanyRelationshipTypeID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Fields
    TypeName = Column(String(50), nullable=False, unique=True)
    TypeDescription = Column(String(255), nullable=True)
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
    company_relationships = relationship("CompanyRelationship", back_populates="relationship_type")

    def __repr__(self) -> str:
        return f"<CompanyRelationshipType(ID={self.CompanyRelationshipTypeID}, Name='{self.TypeName}')>"
