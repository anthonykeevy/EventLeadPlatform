"""
AssetType Model (ref.AssetType)
Reference table for asset types (e.g., IMAGE).
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class AssetType(Base):
    """
    Asset type reference model.

    Used to categorize assets (e.g., images, videos).
    """

    __tablename__ = "AssetType"
    __table_args__ = {"schema": "ref"}

    AssetTypeID = Column(BigInteger, primary_key=True, autoincrement=True)
    TypeCode = Column(String(20), nullable=False, unique=True)
    TypeName = Column(String(50), nullable=False)
    Description = Column(String(500), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    assets = relationship("Asset", back_populates="asset_type")

    def __repr__(self) -> str:
        return f"<AssetType(AssetTypeID={self.AssetTypeID}, TypeCode='{self.TypeCode}')>"
