"""
Asset Model (dbo.Asset)
Background asset metadata storage with hash-based deduplication.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class Asset(Base):
    """
    Asset metadata model.

    Stores storage references (provider + key) without absolute URLs.
    """

    __tablename__ = "Asset"
    __table_args__ = {"schema": "dbo"}

    AssetID = Column(BigInteger, primary_key=True, autoincrement=True)
    CompanyID = Column(BigInteger, ForeignKey("dbo.Company.CompanyID"), nullable=False, index=True)
    AssetTypeID = Column(BigInteger, ForeignKey("ref.AssetType.AssetTypeID"), nullable=False, index=True)

    Sha256 = Column(String(64), nullable=False, index=True)
    MimeType = Column(String(100), nullable=False)
    SizeBytes = Column(BigInteger, nullable=False)
    WidthPx = Column(Integer, nullable=False)
    HeightPx = Column(Integer, nullable=False)
    StorageProvider = Column(String(50), nullable=False)
    StorageKey = Column(String(500), nullable=False)
    OriginalFileName = Column(String(255), nullable=True)
    DisplayName = Column(String(255), nullable=True)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    company = relationship("Company")
    asset_type = relationship("AssetType", back_populates="assets")

    def __repr__(self) -> str:
        return f"<Asset(AssetID={self.AssetID}, Sha256='{self.Sha256[:8]}...')>"
