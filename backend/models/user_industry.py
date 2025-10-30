"""
UserIndustry Model (dbo.UserIndustry)
Junction table linking users to industries
"""
from sqlalchemy import Column, BigInteger, Boolean, Integer, DateTime, func, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from common.database import Base


class UserIndustry(Base):
    """
    UserIndustry junction table for many-to-many user-industry relationships.
    
    Tracks:
    - User industry associations
    - Primary industry designation
    - Sort order for secondary industries
    
    Attributes:
        UserIndustryID: Primary key
        UserID: Foreign key to dbo.User
        IndustryID: Foreign key to ref.Industry
        IsPrimary: Whether this is user's primary industry
        SortOrder: Display order (0 for primary, >0 for secondary)
    """
    
    __tablename__ = "UserIndustry"
    __table_args__ = (
        UniqueConstraint('UserID', 'IndustryID', name='UX_UserIndustry_User_Industry'),
        {"schema": "dbo"}
    )
    
    # Primary Key
    UserIndustryID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    IndustryID = Column(BigInteger, ForeignKey('ref.Industry.IndustryID'), nullable=False, index=True)
    
    # Industry Details
    IsPrimary = Column(Boolean, nullable=False, default=False, index=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="user_industries", foreign_keys=[UserID])
    industry = relationship("Industry", back_populates="user_industries", foreign_keys=[IndustryID])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])
    
    def __repr__(self) -> str:
        return f"<UserIndustry(UserIndustryID={self.UserIndustryID}, UserID={self.UserID}, IndustryID={self.IndustryID}, IsPrimary={self.IsPrimary})>"

