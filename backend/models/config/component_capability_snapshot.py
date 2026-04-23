"""
ComponentCapabilitySnapshot Model (config.ComponentCapabilitySnapshot)
Framework-derived machine-readable capability snapshot versions.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class ComponentCapabilitySnapshot(Base):
    __tablename__ = "ComponentCapabilitySnapshot"
    __table_args__ = {"schema": "config"}

    ComponentCapabilitySnapshotID = Column(BigInteger, primary_key=True, autoincrement=True)
    SnapshotVersion = Column(String(80), nullable=False, unique=True)
    SnapshotJson = Column(String(None), nullable=False)
    SourceManifestHash = Column(String(64), nullable=False)
    IsActive = Column(Boolean, nullable=False, default=False)
    GeneratedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])

    def __repr__(self) -> str:
        return (
            f"<ComponentCapabilitySnapshot(ComponentCapabilitySnapshotID={self.ComponentCapabilitySnapshotID}, "
            f"SnapshotVersion='{self.SnapshotVersion}')>"
        )
