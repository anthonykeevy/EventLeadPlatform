"""
PromptAssemblyRegistryVersion Model (config.PromptAssemblyRegistryVersion)

Versioned activation row for a PromptAssemblyRegistry. Only one IsActive
version per registry at a time (enforced by partial unique index).
"""

from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy.orm import relationship

from common.database import Base


class PromptAssemblyRegistryVersion(Base):
    __tablename__ = "PromptAssemblyRegistryVersion"
    __table_args__ = {"schema": "config"}

    PromptAssemblyRegistryVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    PromptAssemblyRegistryID = Column(
        BigInteger,
        ForeignKey("config.PromptAssemblyRegistry.PromptAssemblyRegistryID"),
        nullable=False,
    )
    VersionNumber = Column(Integer, nullable=False)
    IsActive = Column(Boolean, nullable=False, default=False)
    IsLockedForEdits = Column(Boolean, nullable=False, default=False)
    ReleaseNotes = Column(NVARCHAR(length=2000), nullable=True)
    ActivatedUtc = Column(DateTime, nullable=True)

    CreatedUtc = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    LastUpdatedUtc = Column(DateTime, nullable=True)
    LastUpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    registry = relationship("PromptAssemblyRegistry", back_populates="versions")
    sections = relationship(
        "PromptSection",
        back_populates="registry_version",
        cascade="all, delete-orphan",
        order_by="PromptSection.SortOrder",
    )

    def __repr__(self) -> str:
        return (
            f"<PromptAssemblyRegistryVersion(PromptAssemblyRegistryVersionID="
            f"{self.PromptAssemblyRegistryVersionID}, VersionNumber={self.VersionNumber}, "
            f"IsActive={self.IsActive})>"
        )
