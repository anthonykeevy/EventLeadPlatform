"""
CompanyRelationship Model (dbo.CompanyRelationship)
Represents relationships between companies (branch, subsidiary, partner)
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey, Boolean, UniqueConstraint, CheckConstraint, Integer
from sqlalchemy.orm import relationship
from common.database import Base


class CompanyRelationship(Base):
    """
    CompanyRelationship model to track hierarchical and peer relationships.
    
    Enables features like:
    - Branch/Head Office structures
    - Parent/Subsidiary relationships
    - Partner collaborations
    
    Attributes:
        CompanyRelationshipID: Primary key
        ParentCompanyID: FK to Company (the parent/primary company)
        ChildCompanyID: FK to Company (the child/related company)
        RelationshipTypeID: FK to ref.CompanyRelationshipType
        Status: Status of the relationship ('active', 'suspended', 'terminated')
        EstablishedBy: FK to User who created the relationship
        EstablishedAt: Timestamp when the relationship was established
    """
    
    __tablename__ = "CompanyRelationship"
    __table_args__ = (
        UniqueConstraint('ParentCompanyID', 'ChildCompanyID', name='UQ_CompanyRelationship'),
        CheckConstraint("ParentCompanyID <> ChildCompanyID", name='CK_CompanyRelationship_NotSelf'),
        {"schema": "dbo"}
    )
    
    # Primary Key
    CompanyRelationshipID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Relationship Definition
    ParentCompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    ChildCompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    RelationshipTypeID = Column(Integer, ForeignKey('ref.CompanyRelationshipType.CompanyRelationshipTypeID'), nullable=False, index=True)
    Status = Column(String(20), nullable=False, default='active')  # 'active', 'suspended', 'terminated'
    
    # Metadata
    EstablishedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    EstablishedAt = Column(DateTime, nullable=False, server_default=func.getutcdate())
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    parent_company = relationship("Company", foreign_keys=[ParentCompanyID], backref="child_relationships")
    child_company = relationship("Company", foreign_keys=[ChildCompanyID], backref="parent_relationships")
    relationship_type = relationship("CompanyRelationshipType", back_populates="company_relationships")
    
    established_by_user = relationship("User", foreign_keys=[EstablishedBy])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])

    def __repr__(self) -> str:
        return (
            f"<CompanyRelationship(ID={self.CompanyRelationshipID}, "
            f"Parent={self.ParentCompanyID}, Child={self.ChildCompanyID}, "
            f"TypeID='{self.RelationshipTypeID}', Status='{self.Status}')>"
        )
