"""
PromptAssemblyRegistry Model (config.PromptAssemblyRegistry)

Top-level named registry entry (e.g. ``FORM_AI_V1``) for the Prompt Assembly
Registry introduced by Story 6.5b. Versioned activation lives on
``PromptAssemblyRegistryVersion``; ordered sections live on
``PromptSection``; per-section variants live on ``PromptSectionVariant``.

Naming note: this is intentionally distinct from the legacy
``config.PromptAssemblyProfile`` table (Story 6.3.1, FK'd from
``GenerationRun.PromptAssemblyProfileID``) which represents a runtime
governance step profile rather than a registry of prompt sections. The
two concepts are kept separate in the SQL Server schema; the
architecture document will be reconciled to the implementation name in
Story 6.5c.
"""

from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy.orm import relationship

from common.database import Base


class PromptAssemblyRegistry(Base):
    __tablename__ = "PromptAssemblyRegistry"
    __table_args__ = {"schema": "config"}

    PromptAssemblyRegistryID = Column(BigInteger, primary_key=True, autoincrement=True)
    Code = Column(NVARCHAR(length=120), nullable=False)
    Description = Column(NVARCHAR(length=1000), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)

    CreatedUtc = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    LastUpdatedUtc = Column(DateTime, nullable=True)
    LastUpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    versions = relationship(
        "PromptAssemblyRegistryVersion",
        back_populates="registry",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<PromptAssemblyRegistry(PromptAssemblyRegistryID={self.PromptAssemblyRegistryID}, "
            f"Code='{self.Code}')>"
        )
